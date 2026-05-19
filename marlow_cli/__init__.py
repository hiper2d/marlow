"""
Marlow CLI — single entry point for setup, control, and inspection.

Wraps the driver shell scripts and Python modules. The shell scripts
(tick.sh, install-agent.sh, uninstall-agent.sh) remain the primitive
units that launchd and other automation call directly; this CLI is a
convenience layer for human use.

Usage:
    marlow status              at-a-glance dashboard
    marlow tick                fire one tick now (manual)
    marlow install             install launchd agent (turn loop on)
    marlow uninstall           remove launchd agent (turn loop off)
    marlow pause               touch killswitch (loop pauses, doesn't uninstall)
    marlow resume              clear killswitch and pause flags
    marlow logs [-n N] [-f]    show last N lines of ~/.marlow/log; -f to follow
    marlow digest preview      print what today's digest would send
    marlow digest send         assemble + send today's digest now
    marlow notify "msg"        send an urgent Telegram message
    marlow notify --digest "msg"   append to today's digest
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DRIVER_DIR = REPO_ROOT / "driver"
MARLOW_DIR = Path.home() / ".marlow"
KILLSWITCH = MARLOW_DIR / "stop"
PAUSE_FLAG = MARLOW_DIR / "pause"
LOG_PATH = MARLOW_DIR / "log"

# Mirror plist env into os.environ so interactive `marlow ...` invocations
# see the same secrets that launchd-fired ticks do. Shared with handlers
# via driver/env_loader.py.
sys.path.insert(0, str(REPO_ROOT))
from driver.env_loader import import_plist_env  # noqa: E402
import_plist_env()

THREADS_DIR = REPO_ROOT / "projects" / "research" / "threads"
NOTES_DIR = REPO_ROOT / "projects" / "research" / "notes"
WORKING_PATH = REPO_ROOT / "memory" / "working.md"
RECENT_DIR = REPO_ROOT / "memory" / "recent"
NEWS_DIGEST_DIR = REPO_ROOT / "digests" / "news"


# ─── helpers ───────────────────────────────────────────────────────────────


def _run_script(path: Path) -> int:
    """Run a bash script in the repo root, stream output, return exit code."""
    return subprocess.call(["bash", str(path)], cwd=REPO_ROOT)


def _ensure_repo_cwd():
    """Most subcommands need to operate from the repo root."""
    os.chdir(REPO_ROOT)


# ─── commands ──────────────────────────────────────────────────────────────


def cmd_status(args):
    _ensure_repo_cwd()
    sys.path.insert(0, str(REPO_ROOT))
    from driver import status  # noqa: E402

    data = status.collect()
    if args.json:
        import json

        print(json.dumps(data, indent=2))
    else:
        print(status.fmt_status_text(data))


def cmd_tick(args):
    sys.exit(_run_script(DRIVER_DIR / "tick.sh"))


def cmd_install(args):
    sys.exit(_run_script(DRIVER_DIR / "install-agent.sh"))


def cmd_uninstall(args):
    sys.exit(_run_script(DRIVER_DIR / "uninstall-agent.sh"))


def cmd_pause(args):
    MARLOW_DIR.mkdir(parents=True, exist_ok=True)
    KILLSWITCH.touch()
    print(f"paused — {KILLSWITCH} created")
    print("cron will still fire every 20 min, but each tick will exit clean.")
    print("resume with: marlow resume")


def cmd_resume(args):
    removed = []
    for flag in (KILLSWITCH, PAUSE_FLAG):
        if flag.exists():
            flag.unlink()
            removed.append(str(flag))
    if removed:
        print("resumed — removed:")
        for r in removed:
            print(f"  {r}")
    else:
        print("not paused — no killswitch or pause flag was set")


def cmd_logs(args):
    if not LOG_PATH.exists():
        print(f"{LOG_PATH} does not exist yet — no ticks have run via cron.")
        sys.exit(1)
    if args.follow:
        os.execvp("tail", ["tail", "-n", str(args.lines), "-f", str(LOG_PATH)])
    else:
        os.execvp("tail", ["tail", "-n", str(args.lines), str(LOG_PATH)])


def cmd_digest(args):
    _ensure_repo_cwd()
    sys.path.insert(0, str(REPO_ROOT))
    from handlers import compose_daily_digest  # noqa: E402

    if args.action == "preview":
        ns = argparse.Namespace(date=args.date)
        compose_daily_digest.cmd_preview(ns)
    elif args.action == "send":
        ns = argparse.Namespace(date=args.date)
        compose_daily_digest.cmd_send(ns)


def cmd_notify(args):
    _ensure_repo_cwd()
    sys.path.insert(0, str(REPO_ROOT))
    from tools import notify  # noqa: E402

    urgency = "digest" if args.digest else "urgent"
    result = notify.notify_alex(args.message, urgency=urgency)
    print(result)
    sys.exit(0 if result.get("delivered") else 1)


# ─── inspection commands ──────────────────────────────────────────────────


def _humanize_size(n: int) -> str:
    if n < 1024:
        return f"{n}B"
    if n < 1024 * 1024:
        return f"{n / 1024:.1f}KB"
    return f"{n / (1024 * 1024):.1f}MB"


def _humanize_age(path: Path) -> str:
    from datetime import datetime, timezone

    mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    delta = datetime.now(timezone.utc) - mtime
    secs = int(delta.total_seconds())
    if secs < 60:
        return f"{secs}s ago"
    if secs < 3600:
        return f"{secs // 60}m ago"
    if secs < 86400:
        return f"{secs // 3600}h ago"
    return f"{secs // 86400}d ago"


def cmd_threads(args):
    if not THREADS_DIR.exists():
        print(f"no threads directory at {THREADS_DIR}")
        return
    threads = sorted(
        [f for f in THREADS_DIR.glob("*.md") if f.name != ".gitkeep"],
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )
    if args.name:
        target = THREADS_DIR / f"{args.name}.md"
        if not target.exists():
            print(f"thread '{args.name}' not found at {target}")
            sys.exit(1)
        print(target.read_text())
        return
    if not threads:
        print("(no threads tracked yet)")
        return
    print(f"Threads tracked ({len(threads)}):\n")
    for t in threads:
        print(f"  {t.stem:40}  {_humanize_size(t.stat().st_size):>8}  {_humanize_age(t)}")


def cmd_notes(args):
    if not NOTES_DIR.exists():
        print(f"no notes directory at {NOTES_DIR}")
        return
    date = args.date

    if args.candidates:
        if not date:
            from datetime import datetime, timezone
            date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        cdir = NOTES_DIR / date / "candidates"
        if not cdir.exists():
            print(f"no candidates for {date}")
            return
        files = sorted(cdir.glob("*.md"))
        print(f"Candidate notes for {date} ({len(files)}):\n")
        for f in files:
            print(f"  {f.stem}")
        return

    if date:
        # All deep-dive notes whose filename starts with date
        files = sorted(NOTES_DIR.glob(f"{date}-*.md"))
        cdir = NOTES_DIR / date / "candidates"
        ccount = len(list(cdir.glob("*.md"))) if cdir.exists() else 0
        print(f"Notes for {date}:")
        print(f"  Deep-dive notes: {len(files)}")
        for f in files:
            print(f"    {f.name}  ({_humanize_size(f.stat().st_size)})")
        print(f"  Candidate notes: {ccount}")
        return

    # Default: show recent deep-dive notes + per-day candidate counts
    deep = sorted(
        [f for f in NOTES_DIR.glob("*.md") if f.name != ".gitkeep"],
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )
    print(f"Recent deep-dive notes ({len(deep)}):\n")
    for f in deep[:15]:
        print(f"  {f.name:60}  {_humanize_size(f.stat().st_size):>8}  {_humanize_age(f)}")
    if len(deep) > 15:
        print(f"  ... and {len(deep) - 15} more")
    print()

    # Per-day candidate counts (last 7 days that exist)
    day_dirs = sorted(
        [d for d in NOTES_DIR.iterdir() if d.is_dir()],
        reverse=True,
    )[:7]
    if day_dirs:
        print("Candidate counts by day:")
        for d in day_dirs:
            cdir = d / "candidates"
            count = len(list(cdir.glob("*.md"))) if cdir.exists() else 0
            print(f"  {d.name}: {count} candidates")


def cmd_memory(args):
    if WORKING_PATH.exists():
        body = WORKING_PATH.read_text()
        print(f"=== working.md ({_humanize_size(len(body))}, last updated {_humanize_age(WORKING_PATH)}) ===\n")
        print(body)
    else:
        print(f"(no working.md at {WORKING_PATH})")

    print()
    if RECENT_DIR.exists():
        recent = sorted(RECENT_DIR.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
        print(f"=== memory/recent/ ({len(recent)} tick logs) ===")
        for f in recent[: args.n]:
            print(f"  {f.name}  ({_humanize_size(f.stat().st_size):>8}, {_humanize_age(f)})")
        if len(recent) > args.n:
            print(f"  ... and {len(recent) - args.n} older")
    else:
        print("(no memory/recent/ directory)")


def cmd_news(args):
    from datetime import datetime, timezone

    date = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path = NEWS_DIGEST_DIR / f"{date}.md"
    if not path.exists():
        print(f"no composed news digest at {path}")
        sys.exit(1)
    print(f"=== {path.name} ({_humanize_size(path.stat().st_size)}, {_humanize_age(path)}) ===\n")
    print(path.read_text())


def cmd_draft(args):
    """Inject an on-demand draft_review subtask for a specific thread."""
    _ensure_repo_cwd()
    sys.path.insert(0, str(REPO_ROOT))
    from datetime import datetime, timezone
    from driver.scheduler import QueueItem, load_queue, save_queue, iso

    thread_slug = args.thread
    thread_path = REPO_ROOT / "projects" / "research" / "threads" / f"{thread_slug}.md"
    if not thread_path.exists():
        print(f"no thread file at {thread_path}", file=sys.stderr)
        print(f"available threads: {[f.stem for f in (REPO_ROOT / 'projects' / 'research' / 'threads').glob('*.md') if f.name != '.gitkeep']}", file=sys.stderr)
        sys.exit(1)

    now = datetime.now(timezone.utc)
    queue = load_queue()
    item = QueueItem(
        id=f"draft_{thread_slug}_{now.strftime('%Y%m%d_%H%M')}",
        parent_task="draft_review_ondemand",
        project="blog",
        handler="draft_article",
        context={"thread": thread_slug, "on_demand": True},
        status="pending",
        priority="high",
        queued_at=iso(now),
    )
    queue.append(item)
    save_queue(queue)
    print(f"queued draft request: {item.id} (thread={thread_slug})")
    print(f"next tick within 20min will pick this up; or run `uv run marlow tick` to fire now")


def cmd_approve(args):
    """Approve a draft → publish + push. Alex's gate, never auto-invoked."""
    _ensure_repo_cwd()
    sys.path.insert(0, str(REPO_ROOT))
    from handlers import publish_article  # noqa: E402

    result = publish_article.approve(args.slug)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def cmd_reject(args):
    """Reject a draft → move to drafts/rejected/."""
    _ensure_repo_cwd()
    sys.path.insert(0, str(REPO_ROOT))
    from handlers import publish_article  # noqa: E402

    result = publish_article.reject(args.slug, args.reason)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


# ─── main ──────────────────────────────────────────────────────────────────


def main():
    p = argparse.ArgumentParser(prog="marlow", description="Marlow control CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_status = sub.add_parser("status", help="At-a-glance dashboard")
    p_status.add_argument("--json", action="store_true", help="Machine-readable output")
    p_status.set_defaults(func=cmd_status)

    p_tick = sub.add_parser("tick", help="Fire one tick now (manual)")
    p_tick.set_defaults(func=cmd_tick)

    p_install = sub.add_parser("install", help="Install launchd agent")
    p_install.set_defaults(func=cmd_install)

    p_uninstall = sub.add_parser("uninstall", help="Remove launchd agent")
    p_uninstall.set_defaults(func=cmd_uninstall)

    p_pause = sub.add_parser("pause", help="Touch killswitch (loop pauses)")
    p_pause.set_defaults(func=cmd_pause)

    p_resume = sub.add_parser("resume", help="Clear killswitch and pause flags")
    p_resume.set_defaults(func=cmd_resume)

    p_logs = sub.add_parser("logs", help="Show recent ~/.marlow/log entries")
    p_logs.add_argument("-n", "--lines", type=int, default=50, help="Lines to show")
    p_logs.add_argument("-f", "--follow", action="store_true", help="Follow new entries")
    p_logs.set_defaults(func=cmd_logs)

    p_digest = sub.add_parser("digest", help="Daily digest operations")
    p_digest.add_argument("action", choices=["preview", "send"])
    p_digest.add_argument("--date", help="Override date (YYYY-MM-DD); defaults to today")
    p_digest.set_defaults(func=cmd_digest)

    p_notify = sub.add_parser("notify", help="Send a notification")
    p_notify.add_argument("message")
    p_notify.add_argument("--digest", action="store_true", help="Append to digest instead of urgent send")
    p_notify.set_defaults(func=cmd_notify)

    p_threads = sub.add_parser("threads", help="List threads Marlow is tracking, or show one")
    p_threads.add_argument("name", nargs="?", help="Thread slug to show in full; omit to list")
    p_threads.set_defaults(func=cmd_threads)

    p_notes = sub.add_parser("notes", help="List Marlow's notes (deep-dives + candidates)")
    p_notes.add_argument("--date", help="YYYY-MM-DD; show notes for a specific day")
    p_notes.add_argument("--candidates", action="store_true", help="List candidate notes for the date")
    p_notes.set_defaults(func=cmd_notes)

    p_memory = sub.add_parser("memory", help="Show working.md and list recent tick logs")
    p_memory.add_argument("-n", type=int, default=15, help="Number of recent tick logs to list")
    p_memory.set_defaults(func=cmd_memory)

    p_news = sub.add_parser("news", help="Show the composed news digest for a date")
    p_news.add_argument("action", nargs="?", choices=["preview"], default="preview")
    p_news.add_argument("--date", help="YYYY-MM-DD; defaults to today UTC")
    p_news.set_defaults(func=cmd_news)

    p_draft = sub.add_parser("draft", help="Queue an on-demand draft for a thread")
    p_draft.add_argument("thread", help="Thread slug (no .md extension)")
    p_draft.set_defaults(func=cmd_draft)

    p_approve = sub.add_parser("approve", help="Ship a draft — publishes a draft or releases a held draft")
    p_approve.add_argument("slug", help="Draft slug (no .md extension)")
    p_approve.set_defaults(func=cmd_approve)

    p_reject = sub.add_parser("reject", help="Reject a draft → move to drafts/rejected/")
    p_reject.add_argument("slug")
    p_reject.add_argument("--reason", help="Optional one-line rejection note")
    p_reject.set_defaults(func=cmd_reject)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
