"""
Marlow CLI — single entry point for setup, control, and inspection.

Wraps the existing driver scripts and Python modules. The shell scripts
(tick.sh, install-cron.sh, uninstall-cron.sh) remain the primitive units
that cron and other automation call directly; this CLI is a convenience
layer for human use.

Usage:
    marlow status              at-a-glance dashboard
    marlow tick                fire one tick now (manual)
    marlow install             install cron entry (turn loop on)
    marlow uninstall           remove cron entry (turn loop off)
    marlow pause               touch killswitch (loop pauses, doesn't uninstall)
    marlow resume              clear killswitch and pause flags
    marlow logs [-n N] [-f]    show last N lines of ~/marlow.log; -f to follow
    marlow digest preview      print what today's digest would send
    marlow digest send         assemble + send today's digest now
    marlow notify "msg"        send an urgent Telegram message
    marlow notify --digest "msg"   append to today's digest
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DRIVER_DIR = REPO_ROOT / "driver"
KILLSWITCH = Path.home() / ".marlow-stop"
PAUSE_FLAG = Path.home() / ".marlow-pause"
LOG_PATH = Path.home() / "marlow.log"


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
    sys.exit(_run_script(DRIVER_DIR / "install-cron.sh"))


def cmd_uninstall(args):
    sys.exit(_run_script(DRIVER_DIR / "uninstall-cron.sh"))


def cmd_pause(args):
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


# ─── main ──────────────────────────────────────────────────────────────────


def main():
    p = argparse.ArgumentParser(prog="marlow", description="Marlow control CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_status = sub.add_parser("status", help="At-a-glance dashboard")
    p_status.add_argument("--json", action="store_true", help="Machine-readable output")
    p_status.set_defaults(func=cmd_status)

    p_tick = sub.add_parser("tick", help="Fire one tick now (manual)")
    p_tick.set_defaults(func=cmd_tick)

    p_install = sub.add_parser("install", help="Install cron entry")
    p_install.set_defaults(func=cmd_install)

    p_uninstall = sub.add_parser("uninstall", help="Remove cron entry")
    p_uninstall.set_defaults(func=cmd_uninstall)

    p_pause = sub.add_parser("pause", help="Touch killswitch (loop pauses)")
    p_pause.set_defaults(func=cmd_pause)

    p_resume = sub.add_parser("resume", help="Clear killswitch and pause flags")
    p_resume.set_defaults(func=cmd_resume)

    p_logs = sub.add_parser("logs", help="Show recent ~/marlow.log entries")
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

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
