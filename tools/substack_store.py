"""
substack_store — persistent state + draft outbox for the Substack growth task.

Two stores, both under projects/blog/substack/:

  state.json          dedupe + daily caps. Shape:
      {"engaged": ["c-267323710", ...],          # note ids we've already touched
       "welcomed": ["someauthor", ...],           # handles we've WELCOMED (never welcome twice)
       "do_not_engage": ["asub", ...],            # manual/subscriber skip list (not auto-filled)
       "counters": {"date": "2026-06-01",         # rolls over at UTC midnight
                    "welcomes": 0, "comments": 0},
       "last_scan": "2026-06-01T16:00:00Z"}

  A welcome is a one-time hello, so we track the handle and never welcome the same
  person again. A plain comment is NOT tracked by handle - commenting on someone
  more than once (on different threads) is fine, so commenters never land on a skip
  list. The note_id dedupe still stops us double-commenting the same single thread.

  outbox/<YYYY-MM-DD>.json   Tier-B comment drafts awaiting Alex's review:
      [{"id": "1",                                # sequential within the day; Alex
        "created_at": "...Z",                     #   approves by id ("post 1,3")
        "note_url": "https://substack.com/@.../note/c-...",
        "note_id": "c-...",
        "author": "Some Writer",
        "snippet": "first ~200 chars of the thread",
        "draft_text": "the comment Marlow drafted",
        "status": "pending"}]                      # pending|approved|posted|rejected|failed

Dedupe is by note_id so we never comment on the same thread twice (across both
tiers). Caps are enforced by the caller via counters_today() before posting.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json

REPO_ROOT = Path(__file__).resolve().parent.parent
SUBSTACK_DIR = REPO_ROOT / "projects" / "blog" / "substack"
STATE_PATH = SUBSTACK_DIR / "state.json"
OUTBOX_DIR = SUBSTACK_DIR / "outbox"


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


# ─── state.json ──────────────────────────────────────────────────────────────

def load_state() -> dict:
    try:
        s = json.loads(STATE_PATH.read_text())
    except (OSError, ValueError):
        s = {}
    s.setdefault("engaged", [])
    s.setdefault("welcomed", [])        # handles we've welcomed once (never welcome again)
    s.setdefault("do_not_engage", [])   # manual/subscriber skip list (existing subscribers etc.)
    s.setdefault("counters", {"date": _today(), "welcomes": 0, "comments": 0})
    s.setdefault("last_scan", None)
    # Roll counters over at UTC midnight.
    if s["counters"].get("date") != _today():
        s["counters"] = {"date": _today(), "welcomes": 0, "comments": 0}
    return s


def save_state(state: dict) -> None:
    SUBSTACK_DIR.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def is_engaged(note_id: str) -> bool:
    return note_id in load_state()["engaged"]


def mark_engaged(note_id: str) -> None:
    s = load_state()
    if note_id not in s["engaged"]:
        s["engaged"].append(note_id)
    save_state(s)


def _norm_handle(handle: str) -> str:
    return (handle or "").lstrip("@").lower()


def is_blocked(handle: str) -> bool:
    """True if this author handle is on the do-not-engage list (e.g. already a
    subscriber). Comparison is case-insensitive and @-insensitive."""
    h = _norm_handle(handle)
    return bool(h) and h in (_norm_handle(x) for x in load_state()["do_not_engage"])


def block(handle: str) -> None:
    s = load_state()
    h = _norm_handle(handle)
    if h and h not in (_norm_handle(x) for x in s["do_not_engage"]):
        s["do_not_engage"].append(h)
    save_state(s)


def unblock(handle: str) -> None:
    """Remove a handle from the do-not-engage list (undo a manual/legacy block)."""
    s = load_state()
    h = _norm_handle(handle)
    s["do_not_engage"] = [x for x in s["do_not_engage"] if _norm_handle(x) != h]
    save_state(s)


def is_welcomed(handle: str) -> bool:
    """True if we've already sent this author a welcome (so we never welcome them
    twice). Case- and @-insensitive. Does NOT gate plain comments — only welcomes."""
    h = _norm_handle(handle)
    return bool(h) and h in (_norm_handle(x) for x in load_state()["welcomed"])


def mark_welcomed(handle: str) -> None:
    s = load_state()
    h = _norm_handle(handle)
    if h and h not in (_norm_handle(x) for x in s["welcomed"]):
        s["welcomed"].append(h)
    save_state(s)


def counters_today() -> dict:
    return load_state()["counters"]


def incr_counter(kind: str, n: int = 1) -> dict:
    """kind: 'welcomes' | 'comments'. Returns updated counters."""
    s = load_state()
    s["counters"][kind] = s["counters"].get(kind, 0) + n
    save_state(s)
    return s["counters"]


def set_last_scan() -> None:
    s = load_state()
    s["last_scan"] = _now_iso()
    save_state(s)


# ─── outbox/<date>.json ──────────────────────────────────────────────────────

def _outbox_path(date: str | None = None) -> Path:
    return OUTBOX_DIR / f"{date or _today()}.json"


def outbox_list(date: str | None = None, status: str | None = None) -> list[dict]:
    try:
        items = json.loads(_outbox_path(date).read_text())
    except (OSError, ValueError):
        items = []
    if status:
        items = [d for d in items if d.get("status") == status]
    return items


def _outbox_save(items: list[dict], date: str | None = None) -> None:
    OUTBOX_DIR.mkdir(parents=True, exist_ok=True)
    _outbox_path(date).write_text(json.dumps(items, indent=2, ensure_ascii=False))


def outbox_add(note_url: str, note_id: str, author: str, snippet: str, draft_text: str) -> dict:
    """Append a pending draft for today; returns the stored draft (with its id)."""
    items = outbox_list()
    draft = {
        "id": str(len(items) + 1),
        "created_at": _now_iso(),
        "note_url": note_url,
        "note_id": note_id,
        "author": author,
        "snippet": (snippet or "")[:200],
        "draft_text": draft_text,
        "status": "pending",
    }
    items.append(draft)
    _outbox_save(items)
    return draft


def outbox_set_status(draft_id: str, status: str, date: str | None = None) -> dict | None:
    items = outbox_list(date)
    hit = None
    for d in items:
        if d.get("id") == str(draft_id):
            d["status"] = status
            d["status_at"] = _now_iso()
            hit = d
            break
    if hit:
        _outbox_save(items, date)
    return hit
