"""
monitor_betterstack — app-level error watch for the Werewolf game via Betterstack.

The FOURTH werewolf-ops workstream, and the companion to monitor_health.
monitor_keys watches what the free tier COSTS, werewolf_stats what it PRODUCES,
monitor_health whether a *game* WORKS (its `errorState` in Firestore). This
watches whether the *app* is throwing — the failures that never reach a game
doc: unhandled exceptions, provider 5xx, Next.js server errors, dead requests.

The game already ships structured logs to Betterstack via `@logtail/node`
(werewolf-client/app/utils/logger.ts). We read them back through Betterstack's
ClickHouse HTTP query API (the app's source token is ingest-only; this needs a
separate query credential — a ClickHouse connection, created under Telemetry →
Integrations → SQL API).

── Storage, and why an S3 table shows up ────────────────────────────────────
Betterstack Telemetry is ClickHouse with tiered storage. Recent rows sit in a
fast hot table — `remote(<source>_logs)`; older rows are flushed to cheap S3 —
`s3Cluster(primary, <source>_s3)`. The Live-tail UI stitches both together so a
human never sees the seam. The raw SQL API does not: you address a table.
For THIS source the flush to S3 is aggressive and the volume is tiny, so the
hot table is almost always empty and S3 holds effectively everything, including
near-real-time rows. So we query S3. (The cost: the freshest ~couple minutes may
still be unflushed in the hot tier — caught on the next tick, since the window
overlaps. Fine for an hourly error watch. Union the two if we ever want lower
latency.)

── Schema ───────────────────────────────────────────────────────────────────
There is no flat `level` column. Each row's `raw` is the full JSON log line;
level + message come out with `JSONExtractString(raw, 'level' | 'message')`.
Levels seen in practice: info, debug (and warn/error when they happen).

── Env filter (2026-09-23) ──────────────────────────────────────────────────
Local dev, Jest and production all ship to the SAME source; each line carries
`env` in `raw`. On 09-22/23 this watch paged urgent on 26 lines that were all
`env: "test"` (Jest runs, gameId `test-game-id`, mocked 429). Only envs in
BETTERSTACK_ENVS (default `production`) alert. Lines with no `env` predate
2026-09-02 and are dropped. Non-production error/warn lines are still COUNTED,
once a day, as one informational digest line - so a test leak coming back is
visible without paging anyone.

The fingerprint is deliberately still dt|level|msg (no env): production rows
already in `seen` keep their fingerprints, and filtered-out rows simply stop
arriving, so the rollout run fires nothing new.

── Both tiers, and empty ≠ quiet (2026-09-23) ───────────────────────────────
The "S3 holds everything" claim below stopped being true: on 09-23 S3 lagged the
hot table by ~50 min (S3 newest 21:06, hot newest 21:54), and the 21:41 scan saw
nothing while two production lines from 21:03/21:06 already existed. Hot vs S3
has flipped before too. So every query now reads the UNION of both tiers,
DISTINCT on (dt, raw) so a row present in both counts once. If the union holds
ZERO rows (any env/level) in the window the report says `source_empty` instead
of calling the window quiet.

── Alert model: presence, not rate-spike ───────────────────────────────────
At this volume the error baseline is ZERO — errors essentially never appear. So
"did the rate spike above normal?" is the wrong question; "did ANY error/warn
appear?" is both simpler and strictly more sensitive. We alert on error/warn
rows NOT seen on a previous scan (fingerprint dedup, same noise discipline as
monitor_health diffing the errored-game set):
  - First run with no prior state → BASELINE the current error/warn rows, emit
    one digest summary, no urgent ping (don't alarm on a pre-existing pile).
  - Later runs → any error-level row that's new is urgent; any new warn is
    digest. Old rows already fingerprinted are never re-pinged.

Credentials (in the launchd plist, mirrored to os.environ by env_loader):
  BETTERSTACK_CH_HOST, BETTERSTACK_CH_USER, BETTERSTACK_CH_PASS.
Fails clean (ok: false) if unset — same failure contract as monitor_keys/health.

CLI:
    python handlers/monitor_betterstack.py report   → scan + persist, JSON
    python handlers/monitor_betterstack.py show      → last scan, human-readable
    python handlers/monitor_betterstack.py digest    → digest block for notify
    python handlers/monitor_betterstack.py replay --since 2026-09-22T18:00 --until 2026-09-23T02:00
                                                     → what WOULD alert in that window
                                                       (no state read or written)
    python handlers/monitor_betterstack.py selftest  → offline asserts, no network
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from driver.env_loader import import_plist_env  # noqa: E402
import_plist_env()

from driver.budget_state import STATE_DIR  # noqa: E402

# The durable store for this source. Hot tier is remote(t507167_ai_werewolf_2_logs);
# we query S3 (see module docstring). Override via env if the source/cluster moves.
TABLE = os.environ.get("BETTERSTACK_CH_TABLE", "s3Cluster(primary, t507167_ai_werewolf_2_s3)")
# The hot tier, unioned with TABLE on every query (see docstring). Empty = S3 only.
ALT_TABLE = os.environ.get("BETTERSTACK_CH_ALT_TABLE", "remote(t507167_ai_werewolf_2_logs)")
# Only these envs alert. Comma-separated; values go into SQL, so they're
# restricted to a safe charset rather than escaped.
ENVS = tuple(e for e in (x.strip() for x in os.environ.get("BETTERSTACK_ENVS", "production").split(","))
             if re.fullmatch(r"[A-Za-z0-9_-]+", e)) or ("production",)
WINDOW_MIN = int(os.environ.get("BETTERSTACK_WINDOW_MIN", "90"))
ALERT_LEVELS = ("error", "warn")
HTTP_TIMEOUT = 30
ROW_LIMIT = 500          # plenty at this volume; caps a runaway error storm
SEEN_CAP = 2000          # fingerprints retained for dedup (errors are rare → never hit)

BS_LATEST = STATE_DIR / "betterstack_latest.json"
BS_HISTORY = STATE_DIR / "betterstack_history.jsonl"


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _checked_at(now: datetime) -> str:
    return now.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _creds() -> dict | None:
    host = os.environ.get("BETTERSTACK_CH_HOST")
    user = os.environ.get("BETTERSTACK_CH_USER")
    pw = os.environ.get("BETTERSTACK_CH_PASS")
    if not (host and user and pw):
        return None
    return {"host": host, "user": user, "pw": pw}


def _query(creds: dict, sql: str) -> str:
    """POST a SQL statement to the ClickHouse HTTP endpoint, return raw text body.
    Raises requests.RequestException / RuntimeError on transport or query error."""
    resp = requests.post(
        f"{creds['host']}?output_format_pretty_row_numbers=0",
        auth=(creds["user"], creds["pw"]),
        headers={"Content-type": "plain/text"},
        data=sql,
        timeout=HTTP_TIMEOUT,
    )
    if resp.status_code != 200:
        # Betterstack returns a ClickHouse exception JSON or an auth error body.
        raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:200].strip()}")
    return resp.text


def _sql_list(values) -> str:
    return ", ".join(f"'{v}'" for v in values)


def _window_clause(since: datetime | None = None, until: datetime | None = None) -> str:
    """Default: the rolling WINDOW_MIN. With since/until: that fixed UTC range (replay)."""
    if since is None:
        return f"dt > now() - INTERVAL {WINDOW_MIN} MINUTE"
    until = until or _now_utc()
    fmt = "%Y-%m-%d %H:%M:%S"
    return (f"dt >= toDateTime('{since.strftime(fmt)}', 'UTC') "
            f"AND dt < toDateTime('{until.strftime(fmt)}', 'UTC')")


def _source(window: str) -> str:
    """Both tiers for the window, each row once."""
    if not ALT_TABLE:
        return f"(SELECT dt, raw FROM {TABLE} WHERE {window})"
    return (f"(SELECT DISTINCT dt, raw FROM ("
            f"SELECT dt, raw FROM {TABLE} WHERE {window} "
            f"UNION ALL SELECT dt, raw FROM {ALT_TABLE} WHERE {window}))")


def _rows_sql(window: str) -> str:
    return (
        "SELECT dt, JSONExtractString(raw,'level') AS lvl, "
        "JSONExtractString(raw,'env') AS env, "
        "substring(JSONExtractString(raw,'message'),1,200) AS msg "
        f"FROM {_source(window)} "
        f"WHERE JSONExtractString(raw,'level') IN ({_sql_list(ALERT_LEVELS)}) "
        f"AND JSONExtractString(raw,'env') IN ({_sql_list(ENVS)}) "
        f"ORDER BY dt DESC LIMIT {ROW_LIMIT} FORMAT JSONEachRow"
    )


def _count(creds: dict, window: str) -> int:
    """All rows in the window, any env/level: is the source live at all?"""
    body = _query(creds, f"SELECT count() FROM {_source(window)} FORMAT TSV").strip()
    return int(body or 0)


def _nonprod_counts(creds: dict, window: str) -> dict[str, int]:
    """Error/warn lines per NON-alerting env (test, development, preview...)."""
    body = _query(creds, (
        "SELECT JSONExtractString(raw,'env') AS env, count() AS n "
        f"FROM {_source(window)} "
        f"WHERE JSONExtractString(raw,'level') IN ({_sql_list(ALERT_LEVELS)}) "
        f"AND JSONExtractString(raw,'env') NOT IN ({_sql_list(ENVS)}) "
        "GROUP BY env ORDER BY n DESC FORMAT JSONEachRow"))
    out = {}
    for line in body.splitlines():
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            continue
        out[o.get("env") or "(none)"] = int(o.get("n", 0))
    return out


def _fetch_rows(creds: dict, window: str | None = None) -> list[dict]:
    """The error/warn rows in the window from alerting envs, newest first.
    Each: {dt, level, env, msg}."""
    body = _query(creds, _rows_sql(window or _window_clause()))
    return _parse_rows(body)


def _parse_rows(body: str) -> list[dict]:
    rows = []
    for line in body.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            continue
        row = {"dt": o.get("dt"), "level": o.get("lvl"), "env": o.get("env") or "",
               "msg": (o.get("msg") or "").strip()}
        if row["env"] not in ENVS:
            continue  # belt and braces: the SQL already filters this
        rows.append(row)
    return rows


def _fingerprint(row: dict) -> str:
    # No env on purpose - see "Env filter" in the module docstring.
    key = f"{row.get('dt')}|{row.get('level')}|{row.get('msg')}"
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:16]


def _prior_state() -> dict:
    try:
        with BS_LATEST.open() as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def _nonprod_daily_issue(creds: dict, now: datetime, prev: dict) -> dict | None:
    """Once per UTC day: yesterday's non-production error/warn count, as one
    informational digest line. Never urgent. None when already reported or zero."""
    day = (now - timedelta(days=1)).date()
    if prev.get("nonprod_reported_for") == day.isoformat():
        return None
    start = datetime(day.year, day.month, day.day, tzinfo=timezone.utc)
    window = _window_clause(start, start + timedelta(days=1))
    counts = _nonprod_counts(creds, window)
    issue = {"severity": "digest", "kind": "nonprod_logs", "target": day.isoformat(),
             "date": day.isoformat(), "counts": counts}
    if not counts:
        return {**issue, "silent": True}      # mark the day done, add no line
    parts = ", ".join(f"{env}={n}" for env, n in counts.items())
    issue["detail"] = (f"[info] non-production error/warn lines on {day.isoformat()}: {parts} "
                       f"(not alerting - only {'/'.join(ENVS)} alerts)")
    return issue


def _prior_seen() -> list[str] | None:
    """Fingerprints from the last run. None → never scanned (→ baseline)."""
    try:
        with BS_LATEST.open() as f:
            prev = json.load(f)
    except (OSError, json.JSONDecodeError):
        return None
    return list(prev.get("seen", []))


def _derive_issues(rows: list[dict], prior: list[str] | None) -> tuple[list[dict], bool]:
    """Issues for error/warn rows new since last scan. Returns (issues, baselined).

    First run (prior is None) sets a baseline: one digest line, no urgent — we
    don't alarm on the pre-existing pile we just discovered."""
    if prior is None:
        if rows:
            errs = sum(1 for r in rows if r["level"] == "error")
            return ([{
                "severity": "digest",
                "kind": "betterstack_baseline",
                "target": "logs",
                "detail": f"baseline: {len(rows)} {'/'.join(ENVS)} error/warn log line(s) in the last "
                          f"{WINDOW_MIN}m on first scan ({errs} error, {len(rows)-errs} warn) "
                          f"— not alerting (pre-existing). New lines alert from here.",
            }], True)
        return ([], True)

    seen = set(prior)
    issues = []
    for r in rows:
        if _fingerprint(r) in seen:
            continue  # already known — don't re-ping
        is_err = r["level"] == "error"
        issues.append({
            "severity": "urgent" if is_err else "digest",
            "kind": "app_error" if is_err else "app_warn",
            "target": r["dt"] or "?",
            "detail": f"[{r['level']}/{r.get('env') or '?'}] {r['msg'][:140] or '(no message)'}",
        })
    return (issues, False)


def _next_seen(rows: list[dict], prior: list[str] | None) -> list[str]:
    """Updated fingerprint list: current window's fps first, then prior, capped."""
    cur = [_fingerprint(r) for r in rows]
    merged, out = set(), []
    for fp in cur + (prior or []):
        if fp not in merged:
            merged.add(fp)
            out.append(fp)
        if len(out) >= SEEN_CAP:
            break
    return out


def _compact(report: dict) -> dict:
    return {
        "checked_at": report.get("checked_at"),
        "window_min": report.get("window_min"),
        "counts": report.get("counts"),
        "new_issues": len([i for i in report.get("issues", [])
                           if i["kind"] in ("app_error", "app_warn")]),
        "any_urgent": report.get("any_urgent"),
        "issues": [f"{i['severity']}:{i['target']}" for i in report.get("issues", [])],
    }


def _save(report: dict) -> None:
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        tmp = BS_LATEST.with_suffix(".json.tmp")
        with tmp.open("w") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        tmp.replace(BS_LATEST)
        with BS_HISTORY.open("a") as f:
            f.write(json.dumps(_compact(report), ensure_ascii=False) + "\n")
    except OSError:
        pass


def report() -> dict:
    now = _now_utc()
    creds = _creds()
    if not creds:
        return {"ok": False, "checked_at": _checked_at(now),
                "error": "BETTERSTACK_CH_HOST/USER/PASS not set (ClickHouse query creds)"}
    prev = _prior_state()
    try:
        window = _window_clause()
        source_empty = _count(creds, window) == 0
        rows = [] if source_empty else _fetch_rows(creds, window)
        nonprod_issue = _nonprod_daily_issue(creds, now, prev)
    except (requests.RequestException, RuntimeError, ValueError) as e:
        return {"ok": False, "checked_at": _checked_at(now), "error": str(e)[:200]}

    prior = _prior_seen()                       # read BEFORE we overwrite latest
    issues, baselined = _derive_issues(rows, prior)
    if nonprod_issue and not nonprod_issue.get("silent"):
        issues.append(nonprod_issue)
    counts = {lvl: sum(1 for r in rows if r["level"] == lvl) for lvl in ALERT_LEVELS}
    result = {
        "ok": True,
        "checked_at": _checked_at(now),
        "window_min": WINDOW_MIN,
        "envs": list(ENVS),
        "source_empty": source_empty,
        "nonprod_reported_for": (nonprod_issue or {}).get("date") or prev.get("nonprod_reported_for"),
        "counts": counts,
        "rows": rows[:50],                      # a sample for `show`; not the dedup state
        "issues": issues,
        "any_urgent": any(i["severity"] == "urgent" for i in issues),
        "baselined": baselined,
        "seen": _next_seen(rows, prior),        # dedup state for the next run
    }
    _save(result)
    return result


# ─── Renders ─────────────────────────────────────────────────────────────────


def render(report: dict) -> str:
    if not report.get("ok"):
        return f"monitor_betterstack failed: {report.get('error', 'unknown')}"
    c = report.get("counts", {})
    envs = "/".join(report.get("envs") or ["?"])
    out = [f"Werewolf app logs (Betterstack) — {report['checked_at']}",
           f"  window: last {report.get('window_min')}m   env: {envs}   "
           f"error={c.get('error', 0)} warn={c.get('warn', 0)}", ""]
    rows = report.get("rows", [])
    if report.get("source_empty"):
        out.append("  Both log tiers are EMPTY for the window (any env) - can't call it quiet.")
    elif rows:
        out.append("  Recent error/warn lines:")
        for r in rows[:10]:
            out.append(f"    · {r['dt']}  [{r['level']}/{r.get('env') or '?'}] {r['msg'][:120]}")
        if len(rows) > 10:
            out.append(f"    … +{len(rows) - 10} more")
    else:
        out.append(f"  No {envs} error/warn lines in the window.")
    issues = report.get("issues", [])
    out.append("")
    if issues:
        out.append("  Issues this scan:")
        for i in issues:
            mark = "🔴" if i["severity"] == "urgent" else "⚠️"
            out.append(f"    {mark} [{i['severity']}] {i['detail']}")
    else:
        out.append("  No new error/warn lines since last scan.")
    return "\n".join(out)


def render_digest(report: dict) -> str | None:
    """Digest block — only when there's something new. Returns None on a quiet
    scan so it adds no line to the daily digest."""
    if not report.get("ok"):
        return f"Werewolf app logs: scan failed ({report.get('error', 'unknown')})."
    issues = report.get("issues", [])
    if not issues:
        return None
    date = (report.get("checked_at") or "")[:10]
    head = f"Werewolf app logs — {date}: {len(issues)} new" \
           + (" (urgent)" if report.get("any_urgent") else "")
    lines = [head] + [f"  · {i['detail']}" for i in issues]
    return "\n".join(lines)


def replay(since: datetime, until: datetime) -> dict:
    """What a scan over [since, until) WOULD alert on, as if nothing were seen
    before. Reads and writes no state - safe to run next to the hourly tick."""
    creds = _creds()
    if not creds:
        return {"ok": False, "error": "BETTERSTACK_CH_HOST/USER/PASS not set"}
    window = _window_clause(since, until)
    try:
        source_empty = _count(creds, window) == 0
        rows = [] if source_empty else _fetch_rows(creds, window)
        nonprod = _nonprod_counts(creds, window)
    except (requests.RequestException, RuntimeError, ValueError) as e:
        return {"ok": False, "error": str(e)[:200]}
    issues, _ = _derive_issues(rows, [])
    return {"ok": True, "since": since.isoformat(), "until": until.isoformat(),
            "envs": list(ENVS), "source_empty": source_empty,
            "alerts": len(issues), "urgent": sum(i["severity"] == "urgent" for i in issues),
            "issues": issues, "nonprod_counts": nonprod}


def selftest() -> None:
    """Offline asserts - no network, no state. Marlow has no pytest; handlers
    self-check this way (see werewolf_stats selftest)."""
    sql = _rows_sql(_window_clause())
    assert f"JSONExtractString(raw,'env') IN ({_sql_list(ENVS)})" in sql, sql
    assert "AS env" in sql
    assert TABLE in sql and (not ALT_TABLE or ALT_TABLE in sql), sql   # both tiers

    body = "\n".join(json.dumps(o) for o in [
        {"dt": "2026-09-22 20:21:00", "lvl": "error", "env": "test",
         "msg": "Game action failed: replayNightImpl"},
        {"dt": "2026-09-22 20:21:01", "lvl": "warn", "env": "development", "msg": "dev noise"},
        {"dt": "2026-09-22 20:21:02", "lvl": "error", "env": "", "msg": "pre-09-02 line"},
        {"dt": "2026-09-22 20:22:00", "lvl": "error", "env": "production", "msg": "real one"},
    ])
    rows = _parse_rows(body)
    assert [r["msg"] for r in rows] == ["real one"], rows    # test/dev/no-env dropped

    issues, _ = _derive_issues(rows, [])
    assert len(issues) == 1 and issues[0]["severity"] == "urgent", issues
    assert "/production]" in issues[0]["detail"], issues[0]["detail"]

    # Rollout: a production row seen before the env change keeps its fingerprint.
    legacy = hashlib.sha1("2026-09-22 20:22:00|error|real one".encode()).hexdigest()[:16]
    assert _derive_issues(rows, [legacy]) == ([], False)

    w = _window_clause(datetime(2026, 9, 22, 18, tzinfo=timezone.utc),
                       datetime(2026, 9, 23, 2, tzinfo=timezone.utc))
    assert "2026-09-22 18:00:00" in w and "2026-09-23 02:00:00" in w, w
    print("selftest ok")


def _parse_utc(s: str) -> datetime:
    d = datetime.fromisoformat(s.replace("Z", "+00:00"))
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


# ─── CLI ─────────────────────────────────────────────────────────────────────


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("report", help="Scan Betterstack for new error/warn lines + persist (JSON)")
    sub.add_parser("show", help="Render the last persisted scan, human-readable")
    sub.add_parser("digest", help="Digest block from the last scan (empty if nothing new)")
    p_replay = sub.add_parser("replay", help="What WOULD alert in a fixed UTC window (no state touched)")
    p_replay.add_argument("--since", required=True, help="e.g. 2026-09-22T18:00Z")
    p_replay.add_argument("--until", required=True)
    sub.add_parser("selftest", help="Offline asserts (no network)")
    args = ap.parse_args()
    if args.cmd == "selftest":
        selftest()
        return
    if args.cmd == "replay":
        res = replay(_parse_utc(args.since), _parse_utc(args.until))
        print(json.dumps(res, indent=2, ensure_ascii=False))
        sys.exit(0 if res.get("ok") else 1)
    if args.cmd == "report":
        res = report()
        print(json.dumps(res, indent=2, ensure_ascii=False))
        sys.exit(0 if res.get("ok") else 1)
    elif args.cmd == "show":
        try:
            with BS_LATEST.open() as f:
                print(render(json.load(f)))
        except (OSError, json.JSONDecodeError):
            print("No scan yet — run `report` first.")
    elif args.cmd == "digest":
        try:
            with BS_LATEST.open() as f:
                d = render_digest(json.load(f))
            print(d if d else "")
        except (OSError, json.JSONDecodeError):
            print("")


if __name__ == "__main__":
    main()
