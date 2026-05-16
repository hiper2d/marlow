"""
blog_pipeline — state scanner for the autonomous draft pipeline.

The pipeline has four stages: draft → self_review → (revise) → publish, with a
hold-for-alex exit. Each runs on its own tick. This handler is the dispatcher:
it scans drafts/, classifies each one's state, and reports the single
next action Marlow's session should take this tick.

Order of precedence (one action per tick):
  1. status:draft, no .self-review.md          → self_review
  2. status:draft, verdict=hold-for-alex       → hold
  3. status:draft, verdict=ship                → publish
  4. status:draft, verdict=revise, no versions → revise
  5. status:draft, verdict=revise, >=1 version → publish (revised once, ship)
  6. status:held                               → none (Alex's gate)
  7. nothing matches                           → none

Marlow's session reads the returned `next_action`, then calls the
corresponding downstream handler (self_review.py, revise_draft.py,
publish_article.py). This handler is read-only — it never mutates state.

CLI:
    python handlers/blog_pipeline.py state
        → JSON: per-draft state + next_action + next_slug
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DRAFTS = REPO_ROOT / "projects" / "blog" / "drafts"
VERSIONS = DRAFTS / "versions"


def _parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    rest = text[3:]
    end = rest.find("\n---")
    if end == -1:
        return {}
    fm_block = rest[:end]
    meta: dict = {}
    for line in fm_block.strip().splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta


def _read(path: Path) -> str:
    try:
        return path.read_text()
    except OSError:
        return ""


def _version_count(slug: str) -> int:
    d = VERSIONS / slug
    if not d.exists():
        return 0
    return len([f for f in d.glob("v*.md") if ".self-review" not in f.name])


def _classify(draft_path: Path) -> dict:
    slug = draft_path.stem
    meta = _parse_frontmatter(_read(draft_path))
    status = meta.get("status")
    review = DRAFTS / f"{slug}.self-review.md"
    review_meta = _parse_frontmatter(_read(review)) if review.exists() else {}
    verdict = review_meta.get("verdict")
    version_count = _version_count(slug)

    if status == "held":
        return {
            "slug": slug,
            "status": status,
            "verdict": verdict,
            "version_count": version_count,
            "action": "none",
            "reason": "held for editorial review",
        }
    if status != "draft":
        return {
            "slug": slug,
            "status": status,
            "verdict": verdict,
            "version_count": version_count,
            "action": "none",
            "reason": f"unexpected status: {status}",
        }
    if not review.exists():
        return {
            "slug": slug,
            "status": status,
            "verdict": None,
            "version_count": version_count,
            "action": "self_review",
            "reason": "draft has no self-review yet",
        }
    if verdict == "hold-for-alex":
        return {
            "slug": slug,
            "status": status,
            "verdict": verdict,
            "version_count": version_count,
            "action": "hold",
            "reason": "self-review verdict triggered pre-publish pause",
        }
    if verdict == "ship":
        return {
            "slug": slug,
            "status": status,
            "verdict": verdict,
            "version_count": version_count,
            "action": "publish",
            "reason": "self-review verdict is ship",
        }
    if verdict == "revise":
        if version_count >= 1:
            return {
                "slug": slug,
                "status": status,
                "verdict": verdict,
                "version_count": version_count,
                "action": "publish",
                "reason": "already revised once; one-pass rule, publishing",
            }
        return {
            "slug": slug,
            "status": status,
            "verdict": verdict,
            "version_count": version_count,
            "action": "revise",
            "reason": "self-review verdict is revise, no prior versions",
        }
    return {
        "slug": slug,
        "status": status,
        "verdict": verdict,
        "version_count": version_count,
        "action": "none",
        "reason": f"unrecognized verdict: {verdict}",
    }


def state() -> dict:
    if not DRAFTS.exists():
        return {"count": 0, "drafts": [], "next_action": "none", "next_slug": None}

    drafts = []
    for f in sorted(DRAFTS.glob("*.md")):
        if any(s in f.name for s in (".self-review", ".simona-review", ".revision-notes", ".hold-reason")):
            continue
        drafts.append(_classify(f))

    actionable_order = ["self_review", "hold", "revise", "publish"]
    next_pick = None
    for action in actionable_order:
        for d in drafts:
            if d["action"] == action:
                next_pick = d
                break
        if next_pick:
            break

    return {
        "count": len(drafts),
        "drafts": drafts,
        "next_action": next_pick["action"] if next_pick else "none",
        "next_slug": next_pick["slug"] if next_pick else None,
        "next_reason": next_pick["reason"] if next_pick else "no actionable drafts",
    }


def cmd_state(args):
    print(json.dumps(state(), indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("state", help="Classify all drafts; report next action + slug")
    args = parser.parse_args()
    if args.cmd == "state":
        cmd_state(args)


if __name__ == "__main__":
    main()
