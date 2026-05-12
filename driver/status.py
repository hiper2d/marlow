"""
Marlow status — at-a-glance dashboard. Pulls from queue, schedule state,
completed archives, recent memory, editorial outputs, and digest state.

Usage:
    uv run python driver/status.py
    uv run python driver/status.py --json     # machine-readable
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timedelta, timezone
from glob import glob
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
QUEUE_PATH = REPO_ROOT / "tasks" / "queue.json"
LAST_SCHEDULED_PATH = REPO_ROOT / "tasks" / "last_scheduled.json"
COMPLETED_DIR = REPO_ROOT / "tasks" / "completed"
RECENT_DIR = REPO_ROOT / "memory" / "recent"
WORKING_PATH = REPO_ROOT / "memory" / "working.md"
DIGEST_DIR = REPO_ROOT / "digests" / "daily"
FALLBACK_LOG = REPO_ROOT / "digests" / "_notify_fallback.log"
MARLOW_DIR = Path.home() / ".marlow"
KILLSWITCH = MARLOW_DIR / "stop"
PAUSE_FLAG = MARLOW_DIR / "pause"
SESSIONS_LOG = MARLOW_DIR / "sessions.log"
LOCK_FILE = Path("/tmp/marlow.lock")

EDITORIAL_GLOBS = [
    "projects/research/notes/*.md",
    "projects/research/threads/*.md",
    "projects/blog/drafts/*.md",
    "projects/blog/published/*.md",
    "projects/werewolf-ops/reports/*.md",
]


# ─── helpers ───────────────────────────────────────────────────────────────


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def parse_iso(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def humanize_ago(then: datetime | None, now: datetime | None = None) -> str:
    if then is None:
        return "—"
    now = now or now_utc()
    delta = now - then
    secs = int(delta.total_seconds())
    if secs < 0:
        return "just now"
    if secs < 60:
        return f"{secs}s ago"
    if secs < 3600:
        return f"{secs // 60}m ago"
    if secs < 86400:
        return f"{secs // 3600}h ago"
    return f"{secs // 86400}d ago"


def truncate(s: str, n: int = 70) -> str:
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1] + "…"


# ─── data collectors ───────────────────────────────────────────────────────


def get_flags() -> dict:
    lock_pid = None
    if LOCK_FILE.exists():
        try:
            lock_pid = int(LOCK_FILE.read_text().strip())
        except (ValueError, OSError):
            pass
    return {
        "killswitch": KILLSWITCH.exists(),
        "pause": PAUSE_FLAG.exists(),
        "lock_held": LOCK_FILE.exists(),
        "lock_pid": lock_pid,
    }


def get_queue() -> dict:
    if not QUEUE_PATH.exists():
        return {"pending": [], "in_progress": []}
    items = json.loads(QUEUE_PATH.read_text())
    return {
        "pending": [i for i in items if i["status"] == "pending"],
        "in_progress": [i for i in items if i["status"] == "in_progress"],
    }


def get_recent_completions(limit: int = 5) -> list[dict]:
    """Pull most recent completed subtasks across the last few days."""
    if not COMPLETED_DIR.exists():
        return []
    candidates = []
    # Look at last 7 days to catch quiet periods
    for i in range(7):
        date = (now_utc() - timedelta(days=i)).strftime("%Y-%m-%d")
        date_dir = COMPLETED_DIR / date
        if not date_dir.exists():
            continue
        for f in date_dir.glob("*.json"):
            try:
                data = json.loads(f.read_text())
                data["_completed_at"] = datetime.fromtimestamp(
                    f.stat().st_mtime, tz=timezone.utc
                ).isoformat()
                candidates.append(data)
            except (OSError, json.JSONDecodeError):
                continue
    candidates.sort(key=lambda d: d.get("_completed_at", ""), reverse=True)
    return candidates[:limit]


def get_schedule() -> dict[str, str]:
    if not LAST_SCHEDULED_PATH.exists():
        return {}
    return json.loads(LAST_SCHEDULED_PATH.read_text())


def get_recent_memory(limit: int = 3) -> list[dict]:
    if not RECENT_DIR.exists():
        return []
    files = sorted(
        [f for f in RECENT_DIR.glob("*.md")],
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )[:limit]
    out = []
    for f in files:
        try:
            text = f.read_text()
            # Skip frontmatter for excerpt
            if text.startswith("---"):
                _, _, body = text[3:].partition("---")
                excerpt = body.strip().split("\n\n")[0]
            else:
                excerpt = text.strip().split("\n\n")[0]
            out.append(
                {
                    "name": f.name,
                    "mtime": datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc).isoformat(),
                    "excerpt": truncate(excerpt, 80),
                }
            )
        except OSError:
            continue
    return out


def get_editorial_outputs(within_days: int = 7) -> list[dict]:
    cutoff = now_utc() - timedelta(days=within_days)
    out = []
    for pattern in EDITORIAL_GLOBS:
        for path in glob(str(REPO_ROOT / pattern)):
            p = Path(path)
            if p.name == ".gitkeep":
                continue
            mtime = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc)
            if mtime < cutoff:
                continue
            out.append(
                {
                    "path": str(p.relative_to(REPO_ROOT)),
                    "mtime": mtime.isoformat(),
                    "size": p.stat().st_size,
                }
            )
    out.sort(key=lambda d: d["mtime"], reverse=True)
    return out


def get_digest_today_count() -> int:
    today = now_utc().strftime("%Y-%m-%d")
    path = DIGEST_DIR / f"{today}.md"
    if not path.exists():
        return 0
    return path.read_text().count("\n## ")


def get_fallback_log_size() -> int:
    return FALLBACK_LOG.stat().st_size if FALLBACK_LOG.exists() else 0


def collect() -> dict:
    return {
        "now": now_utc().isoformat(timespec="seconds"),
        "flags": get_flags(),
        "queue": get_queue(),
        "recent_completions": get_recent_completions(),
        "schedule": get_schedule(),
        "memory_recent": get_recent_memory(),
        "editorial_outputs_this_week": get_editorial_outputs(),
        "digest_today_count": get_digest_today_count(),
        "fallback_log_bytes": get_fallback_log_size(),
        "sessions_log_exists": SESSIONS_LOG.exists(),
    }


# ─── formatting ────────────────────────────────────────────────────────────


def fmt_status_text(s: dict) -> str:
    out = []
    now = parse_iso(s["now"])

    out.append(f"Marlow status — {s['now']}")
    out.append("─" * 56)

    f = s["flags"]
    flags_line = (
        f"Killswitch: {'ACTIVE' if f['killswitch'] else 'inactive'}    "
        f"Pause: {'ACTIVE' if f['pause'] else 'inactive'}    "
        f"Lock: {'held (pid ' + str(f['lock_pid']) + ')' if f['lock_held'] else 'not held'}"
    )
    out.append(flags_line)
    out.append("")

    q = s["queue"]
    out.append(f"Queue: {len(q['pending'])} pending, {len(q['in_progress'])} in_progress")
    for item in q["in_progress"]:
        out.append(f"  → [in_progress] {item['id']} ({item['handler']})")
    for item in q["pending"][:5]:
        out.append(f"    [{item['priority']}] {item['id']} ({item['handler']})")
    if len(q["pending"]) > 5:
        out.append(f"    ... and {len(q['pending']) - 5} more")
    out.append("")

    out.append("Last 5 ticks:")
    if not s["recent_completions"]:
        out.append("  (none yet)")
    else:
        for c in s["recent_completions"]:
            symbol = "✓" if c["status"] == "done" else ("✗" if c["status"] == "failed" else "·")
            ago = humanize_ago(parse_iso(c.get("_completed_at")), now)
            out.append(f"  {symbol} {c['status']:7} {c['id']} — {ago}")
            if c.get("result"):
                out.append(f"            \"{truncate(c['result'], 70)}\"")
    out.append("")

    out.append("Schedule (last fired):")
    if not s["schedule"]:
        out.append("  (no tasks scheduled yet)")
    else:
        for name, ts in sorted(s["schedule"].items()):
            out.append(f"  {name:30}  @ {ts}  ({humanize_ago(parse_iso(ts), now)})")
    out.append("")

    out.append("Recent memory:")
    if not s["memory_recent"]:
        out.append("  (none yet)")
    else:
        for m in s["memory_recent"]:
            ago = humanize_ago(parse_iso(m["mtime"]), now)
            out.append(f"  {m['name']}  ({ago})")
            out.append(f"    \"{m['excerpt']}\"")
    out.append("")

    eo = s["editorial_outputs_this_week"]
    out.append(f"Editorial outputs this week ({len(eo)}):")
    if not eo:
        out.append("  (none)")
    else:
        for e in eo[:8]:
            ago = humanize_ago(parse_iso(e["mtime"]), now)
            kb = e["size"] / 1024
            out.append(f"  {e['path']}  ({kb:.1f}KB, {ago})")
        if len(eo) > 8:
            out.append(f"  ... and {len(eo) - 8} more")
    out.append("")

    out.append(f"Today's digest:        {s['digest_today_count']} entries")
    out.append(
        f"Notify fallback log:   "
        f"{'has entries (' + str(s['fallback_log_bytes']) + ' bytes)' if s['fallback_log_bytes'] else 'empty'}"
    )
    out.append("")
    out.append(f"Live session output:   tail -f {SESSIONS_LOG}")

    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    args = parser.parse_args()

    data = collect()
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(fmt_status_text(data))


if __name__ == "__main__":
    main()
