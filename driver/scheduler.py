"""
Marlow scheduler — deterministic, runs outside Claude Code.

Owns: reading task definitions, computing what's due, decomposing tasks into
subtasks, maintaining the queue, picking the next subtask to run, and recording
outcomes when ticks complete.

Does NOT: invoke Claude Code, execute handlers, or make any LLM calls. That's
the tick driver's job. This module is pure scheduling logic.

CLI:
    scheduler.py pick                          → schedule and pick next subtask
    scheduler.py complete <id> <status> [--checkpoint <json>] [--result <text>]
    scheduler.py dry-run                       → show what would be picked
    scheduler.py status                        → human-readable queue dump
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from glob import glob
from pathlib import Path

import yaml
from croniter import croniter

REPO_ROOT = Path(__file__).resolve().parent.parent
TASKS_GLOB = str(REPO_ROOT / "projects" / "*" / "tasks" / "*.yaml")
QUEUE_PATH = REPO_ROOT / "tasks" / "queue.json"
LAST_SCHEDULED_PATH = REPO_ROOT / "tasks" / "last_scheduled.json"
COMPLETED_DIR = REPO_ROOT / "tasks" / "completed"

PRIORITY_ORDER = {"high": 0, "normal": 1, "low": 2}


# ─── data ──────────────────────────────────────────────────────────────────


@dataclass
class QueueItem:
    id: str
    parent_task: str
    project: str
    handler: str
    context: dict
    status: str  # pending | in_progress | done | failed
    priority: str
    queued_at: str
    started_at: str | None = None
    checkpoint: dict | None = None
    result: str | None = None


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.replace(microsecond=0).isoformat().replace("+00:00", "Z")


# ─── persistence ───────────────────────────────────────────────────────────


def load_queue() -> list[QueueItem]:
    if not QUEUE_PATH.exists():
        return []
    raw = json.loads(QUEUE_PATH.read_text())
    return [QueueItem(**item) for item in raw]


def save_queue(queue: list[QueueItem]) -> None:
    QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    QUEUE_PATH.write_text(json.dumps([asdict(item) for item in queue], indent=2))


def load_last_scheduled() -> dict[str, str]:
    if not LAST_SCHEDULED_PATH.exists():
        return {}
    return json.loads(LAST_SCHEDULED_PATH.read_text())


def save_last_scheduled(state: dict[str, str]) -> None:
    LAST_SCHEDULED_PATH.parent.mkdir(parents=True, exist_ok=True)
    LAST_SCHEDULED_PATH.write_text(json.dumps(state, indent=2))


# ─── scheduling ────────────────────────────────────────────────────────────


def load_task_definitions() -> list[dict]:
    """Read all YAML task definitions across projects."""
    defs = []
    for path in sorted(glob(TASKS_GLOB)):
        with open(path) as f:
            data = yaml.safe_load(f)
            if not data:
                continue
            data["_source"] = path
            defs.append(data)
    return defs


def is_due(task: dict, last_scheduled: dict[str, str], now: datetime) -> bool:
    """Has this task's cron schedule fired since we last scheduled it?

    First-sight tasks (no last_scheduled record) explicitly do NOT fire
    immediately. They're marked at `now` by `schedule_due_tasks` and
    will fire at the next scheduled time per their cron expression.
    """
    schedule = task.get("schedule")
    if not schedule:
        return False
    last_iso = last_scheduled.get(task["name"])
    if last_iso is None:
        return False
    last = datetime.fromisoformat(last_iso.replace("Z", "+00:00"))
    next_fire = croniter(schedule, last).get_next(datetime)
    if next_fire.tzinfo is None:
        next_fire = next_fire.replace(tzinfo=timezone.utc)
    return now >= next_fire


def _dedup_key(handler: str, context: dict) -> tuple:
    """Key used to detect equivalent subtasks already queued.

    Same handler + same URL + same prefix == duplicate. Other context
    fields (source_name, etc.) are display-only and don't affect work.
    """
    return (handler, context.get("url"), context.get("prefix"))


def _is_duplicate(item: QueueItem, queue: list[QueueItem]) -> bool:
    key = _dedup_key(item.handler, item.context)
    for existing in queue:
        if existing.status not in ("pending", "in_progress"):
            continue
        if _dedup_key(existing.handler, existing.context) == key:
            return True
    return False


def decompose(task: dict, now: datetime) -> list[QueueItem]:
    """Expand a task definition into queue items.

    v0.1: only static `subtasks` lists supported. Dynamic decompose_handler
    will land when we need it.
    """
    items = []
    subtasks = task.get("subtasks", [])
    project = task.get("project", "unknown")
    priority = task.get("priority", "normal")
    timestamp = now.strftime("%Y%m%d_%H%M")
    for sub in subtasks:
        item = QueueItem(
            id=f"{sub['id']}_{timestamp}",
            parent_task=task["name"],
            project=project,
            handler=sub["handler"],
            context=sub.get("context", {}),
            status="pending",
            priority=sub.get("priority", priority),
            queued_at=iso(now),
        )
        items.append(item)
    return items


def schedule_due_tasks(
    queue: list[QueueItem], now: datetime, commit: bool = True
) -> list[QueueItem]:
    """Check task definitions, push any newly-due subtasks onto the queue.

    When `commit=False` (used by dry-run), no state is persisted — neither
    queue nor last_scheduled. Caller decides whether to save.
    """
    last_scheduled = load_last_scheduled()
    defs = load_task_definitions()
    for task in defs:
        if is_due(task, last_scheduled, now):
            new_items = decompose(task, now)
            for item in new_items:
                if _is_duplicate(item, queue):
                    continue
                queue.append(item)
            last_scheduled[task["name"]] = iso(now)
        elif task["name"] not in last_scheduled:
            # Mark first-seen tasks so the next fire window is correct.
            last_scheduled[task["name"]] = iso(now)
    if commit:
        save_last_scheduled(last_scheduled)
    return queue


def pick_next(queue: list[QueueItem]) -> QueueItem | None:
    """Pick the highest-priority pending subtask. Resume in-progress first."""
    in_progress = [item for item in queue if item.status == "in_progress"]
    if in_progress:
        # If something is in_progress, resume it before picking new work.
        in_progress.sort(key=lambda i: i.queued_at)
        return in_progress[0]
    pending = [item for item in queue if item.status == "pending"]
    if not pending:
        return None
    pending.sort(key=lambda i: (PRIORITY_ORDER.get(i.priority, 1), i.queued_at))
    return pending[0]


# ─── commands ──────────────────────────────────────────────────────────────


def cmd_pick(args):
    now = now_utc()
    queue = load_queue()
    queue = schedule_due_tasks(queue, now)
    chosen = pick_next(queue)
    if chosen is None:
        save_queue(queue)
        print("nothing to do", file=sys.stderr)
        sys.exit(1)
    chosen.status = "in_progress"
    chosen.started_at = iso(now)
    save_queue(queue)
    print(json.dumps(asdict(chosen)))


def cmd_complete(args):
    queue = load_queue()
    item = next((i for i in queue if i.id == args.id), None)
    if item is None:
        print(f"unknown subtask id: {args.id}", file=sys.stderr)
        sys.exit(2)
    item.status = args.status
    if args.result:
        item.result = args.result
    if args.checkpoint:
        item.checkpoint = json.loads(args.checkpoint)
    if args.status == "done" or args.status == "failed":
        # Move out of the active queue into the dated archive.
        date_dir = COMPLETED_DIR / now_utc().strftime("%Y-%m-%d")
        date_dir.mkdir(parents=True, exist_ok=True)
        archive_path = date_dir / f"{item.id}.json"
        archive_path.write_text(json.dumps(asdict(item), indent=2))
        queue = [i for i in queue if i.id != args.id]
    save_queue(queue)
    print(f"marked {args.id} as {args.status}")


def cmd_requeue(args):
    """Return a subtask to `pending` without consuming it. For transient no-ops
    where the tick never really ran — e.g. the Claude session limit was hit, so
    the agent was throttled, not the task broken. NOT archived, NOT marked
    failed; the next tick re-picks it untouched. This is what stops a quota
    storm from silently dropping every task scheduled during the window."""
    queue = load_queue()
    item = next((i for i in queue if i.id == args.id), None)
    if item is None:
        print(f"unknown subtask id: {args.id}", file=sys.stderr)
        sys.exit(2)
    item.status = "pending"
    if args.result:
        item.result = args.result
    save_queue(queue)
    print(f"requeued {args.id} (back to pending)")


def cmd_dry_run(args):
    now = now_utc()
    queue = load_queue()
    queue = schedule_due_tasks(queue, now, commit=False)
    chosen = pick_next(queue)
    print(f"queue size: {len(queue)}")
    if chosen:
        print(f"would pick: {chosen.id} ({chosen.handler}, priority={chosen.priority})")
    else:
        print("nothing pending")


def cmd_status(args):
    queue = load_queue()
    if not queue:
        print("queue is empty")
        return
    for item in queue:
        print(f"  [{item.status}] [{item.priority}] {item.id} ({item.handler})")


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("pick", help="Schedule due tasks and pick the next subtask")

    p_complete = sub.add_parser("complete", help="Record a subtask outcome")
    p_complete.add_argument("id")
    p_complete.add_argument("status", choices=["done", "in_progress", "failed"])
    p_complete.add_argument("--checkpoint", help="JSON checkpoint state")
    p_complete.add_argument("--result", help="Short result summary")

    p_requeue = sub.add_parser("requeue", help="Return a subtask to pending (transient no-op, e.g. session limit)")
    p_requeue.add_argument("id")
    p_requeue.add_argument("--result", help="Short note on why")

    sub.add_parser("dry-run", help="Show what would be picked without modifying state")
    sub.add_parser("status", help="Print the current queue")

    args = parser.parse_args()

    if args.cmd == "pick":
        cmd_pick(args)
    elif args.cmd == "complete":
        cmd_complete(args)
    elif args.cmd == "requeue":
        cmd_requeue(args)
    elif args.cmd == "dry-run":
        cmd_dry_run(args)
    elif args.cmd == "status":
        cmd_status(args)


if __name__ == "__main__":
    main()
