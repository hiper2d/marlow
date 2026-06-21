"""
monitor_self — Marlow's operational self-audit.

Checks invariants about Marlow's *own* operation (not external resources)
and escalates failures deterministically. Built after the early-June 2026
blog stall: a draft sat `held` for days, a thread page rendered empty, and
the curate slot silently stopped firing — all three were *observed* in
working.md and none of them reached Alex.

DESIGN RULE — the urgent → Telegram escalation happens HERE, in the
handler, via notify_alex(urgency="urgent"). It does NOT depend on the LLM
session choosing to alert: that judgment step is exactly what failed last
time. This handler runs straight from driver/tick.sh (step 3), OUTSIDE
Marlow's session and BEFORE the lock/scheduler — so a broken session, a
missed scheduler pick, or a stuck previous tick can't suppress it. tick.sh
rate-limits it to once per UTC day via a stamp file; the daily "all green"
digest line doubles as the audit's proof-of-life (if it stops appearing,
the audit — or the whole agent — is down). The only thing that can silence
it now is cron/launchd itself dying, which is total-agent-death and visible
externally.

Invariant registry — each check(now) returns a list of Issue dicts:
  - claude_auth          no recent Claude session died on auth (401). THE shared
                         root cause: when the `claude` login expires, EVERY
                         LLM-backed handler fails at once and failed_ticks pages
                         each one separately — N identical failures that read as N
                         bugs instead of one expired login (the 2026-06-20 ~12h
                         writer outage: 8 'handler broken' pages, one re-auth fix).
                         Names the cause so the fix is `claude login`, not triage.
  - scheduler_freshness  every scheduled task fired within its window.
                         Catches the whole class of "a tick silently
                         stopped firing" (the 2026-06 curate slot).
                         DORMANCY-AWARE: an overdue tick only pages urgent if
                         the DRIVER was alive across the overdue window. If the
                         heartbeat log shows a dormancy gap (laptop asleep /
                         offline), the miss is expected — it folds into one
                         digest line instead of paging per-tick (the 2026-06-14
                         overnight-sleep false alarm).
  - failed_ticks         no automation's most-recent run failed. Catches a
                         tick that ran but CRASHED (the 2026-06-07 werewolf
                         stats session that died "without writing a result
                         file") — a failed run looks identical to a quiet day
                         in the digest otherwise. THE big one: silent automation
                         death you can't know to ask about.
  - output_freshness     declared daily artifacts are recent. Catches a tick
                         marked "done" that produced nothing, or an output
                         series that silently went stale — verifies the EFFECT,
                         not just that the task was dispatched. (last_scheduled
                         updates even on failure, so freshness-of-dispatch is
                         not enough — 06-07 was "scheduled" yet produced no
                         snapshot.)
  - held_artifacts       no blog draft has been status:held past the SLA.
                         Catches "draft blocked on Alex, nobody told Alex".
  - site_integrity       every active thread file has >=1 published post and
                         its `posts:` count matches reality. Catches the
                         empty-thread / bookkeeping-drift class.

Severity → channel:
  urgent → notify_alex(urgency="urgent")  immediate Telegram.
  digest → notify_alex(urgency="digest")  folded into the 23:00 digest.

CLI:
  python handlers/monitor_self.py report   run checks, escalate, write report
  python handlers/monitor_self.py check    run checks, print JSON, send nothing
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import yaml
from croniter import croniter

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from driver.scheduler import load_last_scheduled, load_task_definitions  # noqa: E402
from tools.notify import notify_alex  # noqa: E402

# Profile scoping. When run from a split loop, MARLOW_PROFILE is exported by
# tick.sh before this audit runs. The scheduler loaders we import
# (load_last_scheduled, load_task_definitions) already scope themselves off it,
# so scheduler_freshness is profile-aware for free. These path constants must
# match too: tick.sh writes each loop's driver state under ~/.marlow/<profile>/
# and the scheduler archives completed subtasks under tasks/completed/<profile>/.
# Unset profile → `/ ""` is a no-op join, i.e. the legacy global paths.
_PROFILE = os.environ.get("MARLOW_PROFILE") or ""
_MARLOW_DIR = Path.home() / ".marlow" / _PROFILE

DRAFTS_DIR = REPO_ROOT / "projects" / "blog" / "drafts"
THREADS_DIR = REPO_ROOT / "projects" / "research" / "threads"
PUBLISHED_DIR = REPO_ROOT / "projects" / "blog" / "published"
COMPLETED_DIR = REPO_ROOT / "tasks" / "completed" / _PROFILE
REPORT_DIR = REPO_ROOT / "projects" / "_framework" / "reports" / "self-audit"
# tick.sh appends here whenever it auto-recovers a stale/wedged tick lock. A
# break self-heals, but it means a prior tick died hard — worth surfacing.
LOCK_BREAK_LOG = _MARLOW_DIR / "lock_breaks.log"
# tick.sh appends here when it re-queues a task because the Claude session limit
# was hit. The task is NOT lost (it's re-queued), but a cluster means Marlow was
# throttled for a window — surface it so it doesn't read as a quiet evening.
SESSION_LIMIT_LOG = _MARLOW_DIR / "session_limits.log"
# tick.sh appends one ISO timestamp here every time the driver actually fires
# (before the lock, so even a "nothing to do" tick records it). This is the
# loop's liveness timeline — scheduler_freshness uses it to distinguish a tick
# that silently stopped (driver alive, tick skipped) from the whole driver being
# dormant (laptop asleep/offline, no heartbeats in the window).
HEARTBEAT_LOG = _MARLOW_DIR / "heartbeat.log"
# The driver appends one block per session here: a `[ISO] === subtask (handler)
# ===` header line followed by that session's stderr. check_claude_auth scans it
# for the 401/invalid-credentials signature that downs every LLM tick at once.
SESSIONS_LOG = _MARLOW_DIR / "sessions.log"

# Look back this far over completed-task records. Wider than the daily audit
# cadence so a failure can't slip between two runs; a still-broken task simply
# re-reports until it recovers.
FAILED_LOOKBACK_HOURS = 36

# How far back check_claude_auth scans sessions.log for auth failures. A live
# outage emits a 401 every tick (~20 min), so a short window still catches an
# ongoing break; once re-auth lands the window goes quiet and the check clears.
AUTH_FAIL_LOOKBACK_HOURS = 6
AUTH_FAIL_SIGNATURES = (
    "Failed to authenticate",
    "401 Invalid authentication",
    "Invalid authentication credentials",
)
_SESSION_HEADER_RE = re.compile(r"^\[([^\]]+)\]")

# Declared daily artifacts that must stay fresh. A tick can be marked "done"
# yet produce nothing (06-05) or stop producing silently — this verifies the
# OUTPUT exists and is recent, not just that the task was dispatched.
# (name, path, jsonl timestamp key, max age in hours)
FRESH_ARTIFACTS = [
    (
        "werewolf_stats snapshot",
        REPO_ROOT / "projects" / "werewolf-ops" / "state" / "stats_history.jsonl",
        "checked_at",
        26,
    ),
]

# A scheduled tick is "overdue" only once it's past its expected next fire
# PLUS a grace window — the task's own must_run_within_hours, or this default.
DEFAULT_GRACE_HOURS = 6
# The driver fires every ~20 min. A silence of at least this long inside an
# overdue window means the loop went dormant (sleep/offline/crash) — so a tick
# that didn't fire across it was deferred, not silently killed. 60 min ≈ 3
# missed cycles: tolerant of one or two jittered/skipped ticks, decisive about a
# real outage. Below this, the driver was effectively continuous → a still-unfired
# tick is a genuine "stopped firing" bug and pages urgent.
DRIVER_DORMANT_GAP_MIN = 60
HELD_SLA_HOURS = 48
# A thread opened with no published post is NORMAL in Marlow's pipeline (she
# opens thread files before the first article). Only flag it once it's gone
# this long without an article — i.e. genuinely abandoned, not in-progress.
STALE_THREAD_DAYS = 14


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _parse_iso(s: str) -> datetime:
    dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def _aware(dt: datetime) -> datetime:
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def _mtime(path: Path) -> datetime:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)


def _frontmatter(path: Path) -> dict:
    """Parse the leading --- ... --- YAML block. Returns {} if absent."""
    text = path.read_text()
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        data = yaml.safe_load(parts[1])
        return data if isinstance(data, dict) else {}
    except yaml.YAMLError:
        return {}


def _thread_age_days(fm: dict, now: datetime) -> int | None:
    """Days since a thread's `opened` date. None if unparseable — in which
    case we don't raise a staleness flag (don't nag on uncertain metadata)."""
    opened = fm.get("opened")
    if isinstance(opened, datetime):
        dt = _aware(opened)
    elif isinstance(opened, date):  # yaml parses `opened: 2026-05-31` to a date
        dt = datetime(opened.year, opened.month, opened.day, tzinfo=timezone.utc)
    elif isinstance(opened, str):
        try:
            dt = _parse_iso(opened)
        except ValueError:
            return None
    else:
        return None
    return (now - dt).days


def _issue(check: str, severity: str, summary: str, action: str, detail: str = "") -> dict:
    return {
        "check": check,
        "severity": severity,
        "summary": summary,
        "action": action,
        "detail": detail,
    }


# --- invariant checks --------------------------------------------------------


def _load_heartbeats() -> list[datetime] | None:
    """Sorted driver-heartbeat timestamps. Returns None if the log doesn't exist
    yet — in which case the dormancy mechanism isn't deployed and the caller
    falls back to the old always-urgent behavior (don't silently disable the
    detector on a host whose tick.sh predates the heartbeat)."""
    if not HEARTBEAT_LOG.exists():
        return None
    out: list[datetime] = []
    for line in HEARTBEAT_LOG.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(_parse_iso(line))
        except ValueError:
            continue
    out.sort()
    return out


def _max_dormant_gap_min(hbs: list[datetime], start: datetime, end: datetime) -> float:
    """Largest silence (minutes) between consecutive driver heartbeats across
    [start, end]. start and end bound the window so leading dormancy (driver was
    already asleep when the tick came due) and trailing dormancy both count. With
    no heartbeats in range the whole window is one gap → reads as fully dormant."""
    pts = [start] + [h for h in hbs if start <= h <= end] + [end]
    pts.sort()
    return max((b - a).total_seconds() / 60 for a, b in zip(pts, pts[1:]))


def check_scheduler_freshness(now: datetime) -> list[dict]:
    """Every scheduled task should have fired within its window. A task whose
    last_scheduled timestamp has fallen past (next cron fire + grace) has
    silently stopped — the generic detector for a dead tick.

    Dormancy-aware: an overdue tick only pages urgent when the DRIVER was alive
    across the overdue window (heartbeats roughly continuous). If the heartbeat
    log shows a dormancy gap (laptop asleep/offline), the miss is expected —
    those ticks fold into a single digest line rather than paging one-per-tick.
    Gap-based, not heartbeat-count: after a long sleep the scheduler drains the
    backlog one tick per cycle, so a still-overdue laggard keeps its leading
    dormancy gap until it finally fires — which a count-based rule would misread
    as a live driver skipping it."""
    issues: list[dict] = []
    deferred: list[tuple[str, float, float]] = []  # (name, overdue_h, gap_min)
    last = load_last_scheduled()
    hbs = _load_heartbeats()
    for task in load_task_definitions():
        name, sched = task.get("name"), task.get("schedule")
        if not name or not sched:
            continue
        last_iso = last.get(name)
        if last_iso is None:
            continue  # never scheduled yet — not our alarm to raise
        next_fire = _aware(croniter(sched, _parse_iso(last_iso)).get_next(datetime))
        grace = task.get("must_run_within_hours", DEFAULT_GRACE_HOURS)
        if now <= next_fire + timedelta(hours=grace):
            continue
        overdue_h = (now - next_fire).total_seconds() / 3600
        # Was the loop dormant for a stretch of the overdue window? If so the
        # tick was deferred by the outage, not silently killed. hbs is None only
        # on a host whose tick.sh predates the heartbeat → keep old behavior.
        gap_min = _max_dormant_gap_min(hbs, next_fire, now) if hbs is not None else 0.0
        if gap_min >= DRIVER_DORMANT_GAP_MIN:
            deferred.append((name, overdue_h, gap_min))
            continue
        issues.append(_issue(
            "scheduler_freshness", "urgent",
            f"Tick '{name}' is {overdue_h:.0f}h overdue — last scheduled {last_iso} (cron '{sched}').",
            f"Inspect driver/scheduler + the {name} handler; the tick has silently stopped firing.",
            f"Expected next fire {_iso(next_fire)}, grace {grace}h exceeded; driver was alive across the window.",
        ))
    if deferred:
        names = ", ".join(sorted(n for n, _, _ in deferred))
        worst_gap_h = max(g for _, _, g in deferred) / 60
        issues.append(_issue(
            "scheduler_freshness", "digest",
            f"{len(deferred)} scheduled tick(s) overdue across a driver-dormant window "
            f"(~{worst_gap_h:.0f}h gap — laptop asleep/offline): {names}.",
            "Expected after sleep/offline; they catch up once the loop resumes. No action unless it persists while the driver is up.",
        ))
    return issues


def check_held_artifacts(now: datetime) -> list[dict]:
    """No blog draft should sit status:held past the SLA without Alex hearing
    about it. (glob('*.md') is top-level only — excludes drafts/rejected/.)"""
    issues: list[dict] = []
    if not DRAFTS_DIR.exists():
        return issues
    for md in sorted(DRAFTS_DIR.glob("*.md")):
        fm = _frontmatter(md)
        if fm.get("status") != "held":
            continue
        age_h = (now - _mtime(md)).total_seconds() / 3600
        if age_h < HELD_SLA_HOURS:
            continue
        slug = fm.get("slug", md.stem)
        issues.append(_issue(
            "held_artifacts", "urgent",
            f"Draft '{slug}' held {age_h / 24:.1f}d — blocked on you, no decision yet.",
            f"marlow approve {slug}   |   marlow reject {slug}",
            fm.get("summary", ""),
        ))
    return issues


def _published_mention_counts() -> dict[str, int]:
    counts: dict[str, int] = {}
    if not PUBLISHED_DIR.exists():
        return counts
    for md in PUBLISHED_DIR.glob("*.md"):
        mentions = _frontmatter(md).get("mentions") or []
        if isinstance(mentions, str):
            mentions = [mentions]
        for slug in mentions:
            counts[slug] = counts.get(slug, 0) + 1
    return counts


def check_site_integrity(now: datetime) -> list[dict]:
    """Every active thread file should have >=1 published post mentioning it,
    and its `posts:` frontmatter should match the real count. Catches threads
    opened ahead of their first article and stale post-count bookkeeping."""
    issues: list[dict] = []
    if not THREADS_DIR.exists():
        return issues
    counts = _published_mention_counts()
    for tf in sorted(THREADS_DIR.glob("*.md")):
        fm = _frontmatter(tf)
        slug = fm.get("slug", tf.stem)
        status = fm.get("status", "active")
        actual = counts.get(slug, 0)
        if status != "archived" and actual == 0:
            age = _thread_age_days(fm, now)
            if age is not None and age >= STALE_THREAD_DAYS:
                issues.append(_issue(
                    "site_integrity", "digest",
                    f"Thread '{slug}' has been active with 0 published posts for {age}d (opened {fm.get('opened')}).",
                    "Write its first article, or set status: archived in the thread file.",
                ))
        claimed = fm.get("posts")
        if isinstance(claimed, int) and claimed != actual:
            issues.append(_issue(
                "site_integrity", "digest",
                f"Thread '{slug}' frontmatter says posts:{claimed} but {actual} published mention it.",
                "Correct the posts: count in the thread file.",
            ))
    return issues


def _completed_records(now: datetime, hours: int) -> list[tuple[Path, dict]]:
    """Load completion records from date-dirs covering the lookback window."""
    out: list[tuple[Path, dict]] = []
    if not COMPLETED_DIR.exists():
        return out
    cutoff_date = (now - timedelta(hours=hours)).date()
    for daydir in sorted(COMPLETED_DIR.glob("20*-*-*")):
        try:
            if date.fromisoformat(daydir.name) < cutoff_date:
                continue
        except ValueError:
            continue
        for rec in daydir.glob("*.json"):
            try:
                out.append((rec, json.loads(rec.read_text())))
            except (json.JSONDecodeError, OSError):
                continue
    return out


def _record_time(rec_path: Path, data: dict) -> datetime:
    for key in ("started_at", "queued_at"):
        v = data.get(key)
        if v:
            try:
                return _parse_iso(v)
            except ValueError:
                pass
    return _mtime(rec_path)


def check_claude_auth(now: datetime) -> list[dict]:
    """Recent Claude sessions dying on auth (401) — the SHARED root cause that
    downs every LLM-backed handler at once. Without this, failed_ticks pages each
    dead handler on its own and N identical failures read as N separate bugs
    instead of one expired login. Scans the profile's sessions.log (driver writes
    a `[ISO] === subtask (handler) ===` header, then the session's stderr) for an
    auth-failure signature whose tick ran inside the lookback. The 2026-06-20
    outage: `claude` login expired, 401 on every writer session for ~12h, surfaced
    as 8 'handler broken' pages with no hint they were one thing — re-auth, not
    eight fixes."""
    issues: list[dict] = []
    if not SESSIONS_LOG.exists():
        return issues
    cutoff = now - timedelta(hours=AUTH_FAIL_LOOKBACK_HOURS)
    cur_ts: datetime | None = None
    hits = 0
    last_hit: datetime | None = None
    for line in SESSIONS_LOG.read_text(errors="replace").splitlines():
        m = _SESSION_HEADER_RE.match(line)
        if m:
            try:
                cur_ts = _parse_iso(m.group(1))
            except ValueError:
                cur_ts = None
            continue
        if (
            cur_ts is not None
            and cur_ts >= cutoff
            and any(sig in line for sig in AUTH_FAIL_SIGNATURES)
        ):
            hits += 1
            last_hit = cur_ts
    if hits:
        issues.append(_issue(
            "claude_auth", "urgent",
            f"Claude auth is failing — {hits} session(s) hit a 401/invalid-credentials "
            f"error in the last {AUTH_FAIL_LOOKBACK_HOURS}h (latest {_iso(last_hit)}). "
            "Every LLM-backed tick is down until this is fixed.",
            "Re-authenticate Claude Code (run `claude login`); this is the shared root "
            "cause behind any failed_ticks pages — re-auth, don't chase each handler.",
            "Signature in sessions.log: 'Failed to authenticate. API Error: 401 Invalid "
            "authentication credentials'.",
        ))
    return issues


def check_failed_ticks(now: datetime) -> list[dict]:
    """An automation whose MOST RECENT run (within the lookback) ended in
    `failed` is currently broken, not just quiet. Group by parent_task, keep
    the latest record per group, flag if it failed. Grouping dedupes retries —
    a failure that already recovered won't nag, but at the time it would page.
    This is the check that catches a tick that ran and crashed (06-07 werewolf
    stats: 'session exited without writing result file')."""
    issues: list[dict] = []
    cutoff = now - timedelta(hours=FAILED_LOOKBACK_HOURS)
    latest: dict[str, tuple[datetime, dict]] = {}
    for path, data in _completed_records(now, FAILED_LOOKBACK_HOURS):
        t = _record_time(path, data)
        if t < cutoff:
            continue
        key = data.get("parent_task") or data.get("handler") or data.get("id", "?")
        if key not in latest or t > latest[key][0]:
            latest[key] = (t, data)
    for key, (t, data) in sorted(latest.items()):
        if data.get("status") == "failed":
            age_h = max(0.0, (now - t).total_seconds() / 3600)
            issues.append(_issue(
                "failed_ticks", "urgent",
                f"Automation '{key}' last run FAILED {age_h:.0f}h ago — currently broken, not just quiet.",
                f"Check handler '{data.get('handler', key)}' + the session log; re-run or fix.",
                str(data.get("result", ""))[:300],
            ))
    return issues


def _jsonl_last(path: Path, ts_key: str) -> datetime | None:
    if not path.exists():
        return None
    last = None
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            last = json.loads(line)
        except json.JSONDecodeError:
            continue
    if not isinstance(last, dict) or not last.get(ts_key):
        return None
    try:
        return _parse_iso(last[ts_key])
    except ValueError:
        return None


def check_output_freshness(now: datetime) -> list[dict]:
    """Declared daily artifacts must exist and be recent. Catches the case a
    failed/empty run looks identical to a quiet day: the task is 'done' but no
    output landed. Verifies the effect, which last_scheduled does not."""
    issues: list[dict] = []
    for name, path, ts_key, max_age in FRESH_ARTIFACTS:
        ts = _jsonl_last(path, ts_key)
        if ts is None:
            issues.append(_issue(
                "output_freshness", "urgent",
                f"{name}: no readable artifact ({path.name}) — its producing tick may never have run.",
                f"Check the handler that writes {path}.",
            ))
            continue
        age_h = (now - ts).total_seconds() / 3600
        if age_h > max_age:
            issues.append(_issue(
                "output_freshness", "urgent",
                f"{name} is {age_h:.0f}h stale (newest {_iso(ts)}, max {max_age}h) — the tick ran but produced nothing, or stopped.",
                f"Check the handler that writes {path.name}; a failed/empty run looks identical to a quiet day.",
            ))
    return issues


def check_lock_health(now: datetime) -> list[dict]:
    """Surface tick-lock auto-recoveries from the last 24h. tick.sh self-heals a
    stale/wedged lock (dead-PID fast path or skip-counter slow path), but a break
    means a prior tick died hard — reboot, OOM, or a sleep-kill mid-tick. It
    recovered, so digest-level, but it shouldn't be invisible."""
    issues: list[dict] = []
    if not LOCK_BREAK_LOG.exists():
        return issues
    cutoff = now - timedelta(hours=24)
    recent = []
    for line in LOCK_BREAK_LOG.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ts = _parse_iso(line.split(None, 1)[0])
        except (ValueError, IndexError):
            continue
        if ts >= cutoff:
            recent.append(line)
    if recent:
        issues.append(_issue(
            "lock_health", "digest",
            f"Tick lock auto-recovered {len(recent)}x in 24h — a prior tick died hard (reboot/OOM/sleep-kill mid-tick).",
            "Self-healed; act only if it recurs often. Detail in ~/.marlow/lock_breaks.log.",
            recent[-1][:200],
        ))
    return issues


def check_session_limits(now: datetime) -> list[dict]:
    """Surface Claude session-limit re-queues from the last 24h. The tasks were
    re-queued (not lost) and retried after reset, but a cluster means Marlow was
    throttled for a window — so it reads as 'rate-limited 18:50–21:30' instead of
    a quiet evening. Frequent = a plan-capacity ceiling (she shares the quota)."""
    issues: list[dict] = []
    if not SESSION_LIMIT_LOG.exists():
        return issues
    cutoff = now - timedelta(hours=24)
    recent = []
    for line in SESSION_LIMIT_LOG.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ts = _parse_iso(line.split(None, 1)[0])
        except (ValueError, IndexError):
            continue
        if ts >= cutoff:
            recent.append(line)
    if recent:
        issues.append(_issue(
            "session_limits", "digest",
            f"Claude session limit hit {len(recent)}x in 24h — Marlow was throttled; tasks re-queued (not lost), retried after reset.",
            "If this recurs, it's a plan-capacity ceiling (Marlow shares your Claude quota), not a bug.",
            recent[-1][:200],
        ))
    return issues


CHECKS = [
    check_claude_auth,
    check_scheduler_freshness,
    check_failed_ticks,
    check_output_freshness,
    check_held_artifacts,
    check_site_integrity,
    check_lock_health,
    check_session_limits,
]


def run_checks(now: datetime) -> tuple[list[dict], list[dict]]:
    """Run every check. A check that *crashes* is itself a framework bug —
    captured as an error (escalated urgent), never swallowed."""
    issues: list[dict] = []
    errors: list[dict] = []
    for chk in CHECKS:
        try:
            issues.extend(chk(now))
        except Exception as e:  # noqa: BLE001 — a broken check must not hide others
            errors.append({"check": chk.__name__, "error": repr(e)})
    return issues, errors


def _format_urgent(urgent: list[dict], errors: list[dict]) -> str:
    lines = ["Marlow self-audit — needs you:"]
    for i in urgent:
        lines.append(f"\n• {i['summary']}\n  → {i['action']}")
    for e in errors:
        lines.append(f"\n• self-audit check '{e['check']}' crashed: {e['error']}\n  → the audit itself is broken; fix it.")
    return "\n".join(lines)


def _write_report(now: datetime, result: dict) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIR / f"{now.date().isoformat()}.md"
    lines = [f"# Self-audit — {_iso(now)}", ""]
    if not result["issues"] and not result["errors"]:
        lines.append("All invariants green.")
    for i in result["issues"]:
        lines.append(f"- **[{i['severity']}] {i['check']}** — {i['summary']}  \n  → {i['action']}")
    for e in result["errors"]:
        lines.append(f"- **[error] {e['check']}** — {e['error']}")
    path.write_text("\n".join(lines) + "\n")
    return path


def report(send: bool = True) -> dict:
    now = _now()
    issues, errors = run_checks(now)
    urgent = [i for i in issues if i["severity"] == "urgent"]
    digest = [i for i in issues if i["severity"] == "digest"]
    deliveries = []
    if send:
        if urgent or errors:
            deliveries.append(notify_alex(_format_urgent(urgent, errors), urgency="urgent"))
        for i in digest:
            deliveries.append(notify_alex(f"[self-audit] {i['summary']} — {i['action']}", urgency="digest"))
        if not issues and not errors:
            deliveries.append(notify_alex("[self-audit] all invariants green.", urgency="digest"))
    result = {
        "ok": not errors,
        "ts": _iso(now),
        "any_urgent": bool(urgent or errors),
        "issues": issues,
        "errors": errors,
        "deliveries": deliveries,
        "report_path": str(_write_report(now, {"issues": issues, "errors": errors})),
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Marlow operational self-audit.")
    parser.add_argument("command", choices=["report", "check"],
                        help="report: run + escalate + write report. check: dry-run, print JSON, send nothing.")
    args = parser.parse_args()
    if args.command == "check":
        now = _now()
        issues, errors = run_checks(now)
        print(json.dumps({"ts": _iso(now), "issues": issues, "errors": errors}, indent=2))
        return 0
    print(json.dumps(report(send=True), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
