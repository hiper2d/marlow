"""
research_assignment — orchestration handler for externally-seeded research.

Marlow's research/draft pipeline accumulates organic threads from feed scans.
This handler complements that with an external injection point: Alex or Simona
drops an assignment brief into projects/research/assignments/pending/, and
Marlow processes it via this handler — reading the brief, fetching seed
material, composing a thread file with an angle memo, and either drafting
immediately (high-priority) or letting the next draft_review cycle pick it up.

The handler itself is deterministic: file shuffling and YAML reading. All
editorial work — fetching, composing, deciding angle — happens in Marlow's
session around the handler's CLI output. Same philosophy as draft_article.py.

CLI:
    research_assignment.py list-pending
        → JSON of slugs in pending/, sorted by (priority desc, assigned_at asc)
    research_assignment.py list-all
        → JSON of every assignment across states
    research_assignment.py read --slug <slug>
        → JSON: frontmatter + body + current file path
    research_assignment.py move-to-researching --slug <slug>
        → Moves pending/<slug>.md → researching/<slug>.md
    research_assignment.py mark-done --slug <slug> --outcome drafted
    research_assignment.py mark-done --slug <slug> --outcome abandoned --reason "..."
        → Moves to done/, writes outcome (+ abandon_reason) into frontmatter
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSIGNMENTS_ROOT = REPO_ROOT / "projects" / "research" / "assignments"
STATES = ("pending", "researching", "done")
PRIORITY_ORDER = {"high": 0, "normal": 1, "low": 2}


def _state_dir(state: str) -> Path:
    return ASSIGNMENTS_ROOT / state


def _find(slug: str) -> tuple[str, Path] | None:
    """Return (state, path) for a slug, searching all state folders."""
    for state in STATES:
        candidate = _state_dir(state) / f"{slug}.md"
        if candidate.exists():
            return state, candidate
    return None


def _split_frontmatter(text: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from a markdown file. Returns (meta, body)."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 5 :]
    try:
        meta = yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        meta = {}
    return meta, body


def _join_frontmatter(meta: dict, body: str) -> str:
    fm = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True).strip()
    return f"---\n{fm}\n---\n{body}"


def _read(path: Path) -> tuple[dict, str]:
    text = path.read_text()
    return _split_frontmatter(text)


def _stringify_dates(value):
    """Coerce yaml-parsed date/datetime into ISO strings for JSON.

    YAML parses bare date literals (e.g. `assigned_at: 2026-05-14`) into
    datetime.date objects, which json.dumps can't serialize. Walk the
    value recursively and stringify anything with .isoformat().
    """
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if isinstance(value, dict):
        return {k: _stringify_dates(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_stringify_dates(v) for v in value]
    return value


def _summary(state: str, path: Path) -> dict:
    meta, _ = _read(path)
    return {
        "slug": meta.get("slug", path.stem),
        "state": state,
        "path": str(path.relative_to(REPO_ROOT)),
        "priority": meta.get("priority", "normal"),
        "assigned_by": meta.get("assigned_by"),
        "assigned_at": _stringify_dates(meta.get("assigned_at")),
        "outcome": meta.get("outcome"),
    }


# ─── operations ────────────────────────────────────────────────────────────


def list_pending() -> list[dict]:
    pending_dir = _state_dir("pending")
    if not pending_dir.exists():
        return []
    rows = []
    for f in pending_dir.glob("*.md"):
        if f.name.startswith("."):
            continue
        rows.append(_summary("pending", f))
    rows.sort(key=lambda r: (PRIORITY_ORDER.get(r["priority"], 1), str(r["assigned_at"] or "")))
    return rows


def list_all() -> list[dict]:
    rows = []
    for state in STATES:
        d = _state_dir(state)
        if not d.exists():
            continue
        for f in sorted(d.glob("*.md")):
            if f.name.startswith("."):
                continue
            rows.append(_summary(state, f))
    return rows


def read_assignment(slug: str) -> dict:
    found = _find(slug)
    if found is None:
        return {"ok": False, "error": f"no assignment with slug {slug!r}"}
    state, path = found
    meta, body = _read(path)
    return {
        "ok": True,
        "slug": slug,
        "state": state,
        "path": str(path.relative_to(REPO_ROOT)),
        "frontmatter": _stringify_dates(meta),
        "body": body,
    }


def move_to_researching(slug: str) -> dict:
    found = _find(slug)
    if found is None:
        return {"ok": False, "error": f"no assignment with slug {slug!r}"}
    state, path = found
    if state == "researching":
        return {"ok": True, "slug": slug, "state": "researching", "path": str(path.relative_to(REPO_ROOT)), "note": "already in researching"}
    if state == "done":
        return {"ok": False, "error": f"assignment {slug!r} is already done; cannot move back"}
    target_dir = _state_dir("researching")
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / path.name
    path.rename(target)
    return {"ok": True, "slug": slug, "state": "researching", "path": str(target.relative_to(REPO_ROOT))}


def mark_done(slug: str, outcome: str, reason: str | None = None) -> dict:
    if outcome not in ("drafted", "abandoned"):
        return {"ok": False, "error": f"outcome must be 'drafted' or 'abandoned', got {outcome!r}"}
    found = _find(slug)
    if found is None:
        return {"ok": False, "error": f"no assignment with slug {slug!r}"}
    state, path = found
    if state == "done":
        return {"ok": False, "error": f"assignment {slug!r} already done"}
    meta, body = _read(path)
    meta["outcome"] = outcome
    if outcome == "abandoned":
        if not reason:
            return {"ok": False, "error": "abandoned outcome requires --reason"}
        meta["abandon_reason"] = reason
    target_dir = _state_dir("done")
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / path.name
    target.write_text(_join_frontmatter(meta, body))
    path.unlink()
    return {"ok": True, "slug": slug, "state": "done", "outcome": outcome, "path": str(target.relative_to(REPO_ROOT))}


# ─── CLI ───────────────────────────────────────────────────────────────────


def cmd_list_pending(args):
    rows = list_pending()
    print(json.dumps({"count": len(rows), "assignments": rows}, indent=2, ensure_ascii=False))


def cmd_list_all(args):
    rows = list_all()
    print(json.dumps({"count": len(rows), "assignments": rows}, indent=2, ensure_ascii=False))


def cmd_read(args):
    result = read_assignment(args.slug)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def cmd_move_to_researching(args):
    result = move_to_researching(args.slug)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def cmd_mark_done(args):
    result = mark_done(args.slug, args.outcome, args.reason)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list-pending", help="List pending assignments, priority-sorted")
    sub.add_parser("list-all", help="List every assignment across states")

    p_read = sub.add_parser("read", help="Read an assignment file (any state)")
    p_read.add_argument("--slug", required=True)

    p_move = sub.add_parser("move-to-researching", help="Move pending → researching")
    p_move.add_argument("--slug", required=True)

    p_done = sub.add_parser("mark-done", help="Mark assignment done with outcome")
    p_done.add_argument("--slug", required=True)
    p_done.add_argument("--outcome", required=True, choices=["drafted", "abandoned"])
    p_done.add_argument("--reason", help="Required when outcome is 'abandoned'")

    args = parser.parse_args()

    {
        "list-pending": cmd_list_pending,
        "list-all": cmd_list_all,
        "read": cmd_read,
        "move-to-researching": cmd_move_to_researching,
        "mark-done": cmd_mark_done,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
