"""
framework_fix — diagnosis log + state machine for Marlow's self-healing flow.

Marlow can directly edit files under `handlers/`, `driver/`, `projects/*/tasks/`,
and other "tools" — but NOT identity files (`CLAUDE.md`, `README.md`, the
project READMEs). When she spots a framework bug during any tick, she:

  1. Records a diagnosis via `record-diagnosis`. Gets back an ID.
  2. Enqueues a high-priority `framework_fix` subtask (inline, in the same tick).
     The subtask context carries the diagnosis ID.
  3. Exits the current tick.

On the next tick the scheduler picks the high-priority fix subtask. Marlow's
session for that subtask:

  - Calls `next-open` to get the current open diagnosis.
  - Reads the named file, decides on a fix, edits it with the Edit tool.
  - Smoke-tests via the file's CLI if applicable.
  - Commits + pushes (one file scope, commit message references the diagnosis ID).
  - Calls `mark-resolved --id <id> --commit <sha>`.
  - Appends a DEVLOG entry.

If the fix doesn't stick (next tick hits the same failure), Marlow records a
NEW diagnosis and tries again. After MAX_ATTEMPTS (2) on a single diagnosis,
`next-open` returns the diagnosis with `should_escalate: true`. Marlow's
session then:

  - Calls `mark-escalated --id <id> --reason "<short>"`.
  - Sends urgent notify ("can't self-fix X, need Simona/Alex").
  - Does NOT re-attempt. Moves on.

Out-of-scope failures (require editing CLAUDE.md, README, or cross-file
changes) escalate immediately. Use `mark-escalated` directly without
incrementing attempts.

Log lives at `tasks/framework_fix_log.json`. Append-only history; status
transitions only via the documented commands.

CLI:
    python handlers/framework_fix.py log
        → JSON of all diagnoses.
    python handlers/framework_fix.py record-diagnosis --file <path> --failure-mode <m> --suggested-fix <s> [--line <n>]
        → JSON {ok, id, attempts}.
    python handlers/framework_fix.py next-open
        → JSON of highest-priority open diagnosis + should_escalate flag,
          or {ok: false, reason: "no open diagnoses"}.
    python handlers/framework_fix.py mark-attempt --id <id> --result <pass|fail> [--note <s>]
        → JSON {ok, id, attempts, should_escalate}.
    python handlers/framework_fix.py mark-resolved --id <id> --commit <sha>
        → JSON {ok}.
    python handlers/framework_fix.py mark-escalated --id <id> --reason <s>
        → JSON {ok}.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
LOG_PATH = REPO_ROOT / "tasks" / "framework_fix_log.json"
MAX_ATTEMPTS = 2

IDENTITY_FILES = {"CLAUDE.md", "README.md", "SOUL.md"}


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _load() -> list[dict]:
    if not LOG_PATH.exists():
        return []
    try:
        return json.loads(LOG_PATH.read_text())
    except json.JSONDecodeError:
        return []


def _save(entries: list[dict]) -> None:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text(json.dumps(entries, indent=2))


def _find(entries: list[dict], diag_id: str) -> dict | None:
    for e in entries:
        if e["id"] == diag_id:
            return e
    return None


def _is_identity_file(file_path: str) -> bool:
    name = Path(file_path).name
    if name in IDENTITY_FILES:
        return True
    if Path(file_path).parts and Path(file_path).parts[-1] == "README.md":
        return True
    return False


def record_diagnosis(file_path: str, failure_mode: str, suggested_fix: str, line: int | None) -> dict:
    entries = _load()
    now = _now_iso()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    slug = Path(file_path).stem.replace("_", "-")
    diag_id = f"diag_{stamp}_{slug}"

    out_of_scope = _is_identity_file(file_path)

    entry = {
        "id": diag_id,
        "detected_at": now,
        "file": file_path,
        "line": line,
        "failure_mode": failure_mode,
        "suggested_fix": suggested_fix,
        "attempts": 0,
        "attempt_notes": [],
        "status": "escalated" if out_of_scope else "open",
        "resolved_commit": None,
        "escalated_at": now if out_of_scope else None,
        "escalation_reason": "identity file — out of self-heal scope" if out_of_scope else None,
    }
    entries.append(entry)
    _save(entries)

    return {
        "ok": True,
        "id": diag_id,
        "attempts": 0,
        "out_of_scope": out_of_scope,
        "auto_escalated": out_of_scope,
        "message": (
            "diagnosis auto-escalated: identity files (CLAUDE.md, README.md, SOUL.md) are out of self-heal scope. Notify Alex urgently and exit."
            if out_of_scope
            else "diagnosis recorded; enqueue a high-priority framework_fix subtask with this ID before exiting the tick"
        ),
    }


def next_open() -> dict:
    entries = _load()
    open_entries = [e for e in entries if e["status"] == "open"]
    if not open_entries:
        return {"ok": False, "reason": "no open diagnoses"}
    # Highest priority = oldest detected_at (first-in-first-out).
    open_entries.sort(key=lambda e: e["detected_at"])
    head = open_entries[0]
    should_escalate = head["attempts"] >= MAX_ATTEMPTS
    return {
        "ok": True,
        "id": head["id"],
        "file": head["file"],
        "line": head["line"],
        "failure_mode": head["failure_mode"],
        "suggested_fix": head["suggested_fix"],
        "attempts": head["attempts"],
        "attempt_notes": head["attempt_notes"],
        "max_attempts": MAX_ATTEMPTS,
        "should_escalate": should_escalate,
        "next_step": (
            "ESCALATE — attempts exhausted. Run mark-escalated and notify Alex urgent."
            if should_escalate
            else "Attempt the fix. Edit the file, smoke-test, commit + push, then mark-resolved."
        ),
    }


def mark_attempt(diag_id: str, result: str, note: str | None) -> dict:
    if result not in ("pass", "fail"):
        return {"ok": False, "error": f"result must be 'pass' or 'fail', got '{result}'"}
    entries = _load()
    entry = _find(entries, diag_id)
    if entry is None:
        return {"ok": False, "error": f"no diagnosis with id {diag_id}"}
    if entry["status"] != "open":
        return {"ok": False, "error": f"diagnosis status is '{entry['status']}', not 'open'"}
    entry["attempts"] += 1
    entry["attempt_notes"].append({
        "n": entry["attempts"],
        "at": _now_iso(),
        "result": result,
        "note": note,
    })
    _save(entries)
    return {
        "ok": True,
        "id": diag_id,
        "attempts": entry["attempts"],
        "should_escalate": entry["attempts"] >= MAX_ATTEMPTS,
    }


def mark_resolved(diag_id: str, commit_sha: str) -> dict:
    entries = _load()
    entry = _find(entries, diag_id)
    if entry is None:
        return {"ok": False, "error": f"no diagnosis with id {diag_id}"}
    entry["status"] = "resolved"
    entry["resolved_commit"] = commit_sha
    entry["resolved_at"] = _now_iso()
    _save(entries)
    return {"ok": True, "id": diag_id, "status": "resolved", "commit": commit_sha}


def mark_escalated(diag_id: str, reason: str) -> dict:
    entries = _load()
    entry = _find(entries, diag_id)
    if entry is None:
        return {"ok": False, "error": f"no diagnosis with id {diag_id}"}
    entry["status"] = "escalated"
    entry["escalated_at"] = _now_iso()
    entry["escalation_reason"] = reason
    _save(entries)
    return {"ok": True, "id": diag_id, "status": "escalated", "reason": reason}


def show_log() -> dict:
    entries = _load()
    return {
        "count": len(entries),
        "open": sum(1 for e in entries if e["status"] == "open"),
        "resolved": sum(1 for e in entries if e["status"] == "resolved"),
        "escalated": sum(1 for e in entries if e["status"] == "escalated"),
        "entries": entries,
    }


def cmd_log(args):
    print(json.dumps(show_log(), indent=2, ensure_ascii=False))


def cmd_record(args):
    result = record_diagnosis(args.file, args.failure_mode, args.suggested_fix, args.line)
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_next_open(args):
    result = next_open()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def cmd_mark_attempt(args):
    result = mark_attempt(args.id, args.result, args.note)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def cmd_mark_resolved(args):
    result = mark_resolved(args.id, args.commit)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def cmd_mark_escalated(args):
    result = mark_escalated(args.id, args.reason)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("log", help="Show all diagnoses (open + resolved + escalated)")

    p_rec = sub.add_parser("record-diagnosis", help="Add a new diagnosis to the log")
    p_rec.add_argument("--file", required=True)
    p_rec.add_argument("--failure-mode", required=True)
    p_rec.add_argument("--suggested-fix", required=True)
    p_rec.add_argument("--line", type=int, default=None)

    sub.add_parser("next-open", help="Get the highest-priority open diagnosis")

    p_att = sub.add_parser("mark-attempt", help="Record an attempt outcome (pass | fail)")
    p_att.add_argument("--id", required=True)
    p_att.add_argument("--result", required=True, choices=["pass", "fail"])
    p_att.add_argument("--note", default=None)

    p_res = sub.add_parser("mark-resolved", help="Mark a diagnosis resolved with the fix commit SHA")
    p_res.add_argument("--id", required=True)
    p_res.add_argument("--commit", required=True)

    p_esc = sub.add_parser("mark-escalated", help="Mark a diagnosis escalated (needs human)")
    p_esc.add_argument("--id", required=True)
    p_esc.add_argument("--reason", required=True)

    args = parser.parse_args()

    if args.cmd == "log":
        cmd_log(args)
    elif args.cmd == "record-diagnosis":
        cmd_record(args)
    elif args.cmd == "next-open":
        cmd_next_open(args)
    elif args.cmd == "mark-attempt":
        cmd_mark_attempt(args)
    elif args.cmd == "mark-resolved":
        cmd_mark_resolved(args)
    elif args.cmd == "mark-escalated":
        cmd_mark_escalated(args)


if __name__ == "__main__":
    main()
