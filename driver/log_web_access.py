#!/usr/bin/env python3
"""
PreToolUse hook: one JSONL line per WebSearch / WebFetch call, before the
permission check, so refused attempts are logged too. Alex's rule
(2026-11-07): everything Marlow does on the web is logged, in code, not left
to her session.

Log: ~/.marlow/<profile>/web-access.jsonl (~/.marlow/web-access.jsonl when no
profile, e.g. an interactive session in the repo). monitor_self reads it.
Never blocks: any failure here exits 0 and lets the call through to the
normal permission check.
"""
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> None:
    try:
        ev = json.load(sys.stdin)
    except Exception:
        return
    tool = ev.get("tool_name", "")
    if tool not in ("WebSearch", "WebFetch"):
        return
    ti = ev.get("tool_input") or {}
    profile = os.environ.get("MARLOW_PROFILE", "")
    d = Path.home() / ".marlow" / profile if profile else Path.home() / ".marlow"
    rec = {
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "profile": profile or "none",
        "subtask": os.environ.get("MARLOW_SUBTASK_ID", "interactive"),
        "handler": os.environ.get("MARLOW_SUBTASK_HANDLER", ""),
        "web_mode": os.environ.get("MARLOW_WEB_MODE", "0") == "1",
        "tool": tool,
        "query": ti.get("query"),
        "url": ti.get("url"),
        "allowed_domains": ti.get("allowed_domains"),
        "prompt": (ti.get("prompt") or "")[:300] or None,
        "session": ev.get("session_id"),
    }
    try:
        d.mkdir(parents=True, exist_ok=True)
        with (d / "web-access.jsonl").open("a") as f:
            f.write(json.dumps({k: v for k, v in rec.items() if v is not None}) + "\n")
    except Exception:
        pass


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
