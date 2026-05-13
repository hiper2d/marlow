"""
revise_draft — orchestration handler for Marlow's revision loop.

The flow: Simona's review has landed at drafts/<slug>.simona-review.md.
Marlow's revise_draft tick reads the current draft + the review + the
original thread/notes corpus, decides which critiques to apply and
which to reject (with reasoning), writes v2 to drafts/<slug>.md, and
records a revision note explaining her choices. Previous version is
archived to drafts/versions/<slug>/v<N>.md before overwrite.

Terminate the loop when:
  - Latest Simona review's verdict is `ship-as-is`
  - Marlow has 3 versions on record (v1, v2, v3) — hard cap
Alex's approval gate is independent of loop termination.

CLI:
    python handlers/revise_draft.py materials --slug <slug>
        → JSON: current draft body, review body, version count,
          thread bodies, related research/candidate notes
    python handlers/revise_draft.py archive --slug <slug>
        → move current drafts/<slug>.md to drafts/versions/<slug>/v<N>.md
          where N is the next available number. Used before overwriting
          with v2/v3.
    python handlers/revise_draft.py versions --slug <slug>
        → JSON: list of archived versions with bodies (for Simona's
          review of v2+ pushback)
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DRAFTS = REPO_ROOT / "projects" / "blog" / "drafts"
VERSIONS = DRAFTS / "versions"
THREADS = REPO_ROOT / "projects" / "research" / "threads"
NOTES = REPO_ROOT / "projects" / "research" / "notes"
MAX_VERSIONS = 3  # hard cap on revision rounds


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    rest = text[3:]
    end = rest.find("\n---")
    if end == -1:
        return {}, text
    fm_block = rest[:end]
    body = rest[end + 4:].lstrip("\n")
    meta: dict = {}
    for line in fm_block.strip().splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, body


def _read(path: Path) -> str:
    try:
        return path.read_text()
    except OSError:
        return ""


def _version_count(slug: str) -> int:
    d = VERSIONS / slug
    if not d.exists():
        return 0
    return len(list(d.glob("v*.md")))


def materials(slug: str) -> dict:
    draft = DRAFTS / f"{slug}.md"
    review = DRAFTS / f"{slug}.simona-review.md"
    if not draft.exists():
        return {"ok": False, "error": f"no draft at {draft}"}
    if not review.exists():
        return {"ok": False, "error": f"no review at {review} — Simona hasn't reviewed yet"}

    draft_text = _read(draft)
    draft_meta, draft_body = _parse_frontmatter(draft_text)
    review_text = _read(review)
    review_meta, review_body = _parse_frontmatter(review_text)
    verdict = review_meta.get("verdict")

    version_count = _version_count(slug)
    terminal = verdict == "ship-as-is" or version_count >= MAX_VERSIONS

    mentions = [
        m.strip().strip('"').strip("'")
        for m in draft_meta.get("mentions", "").strip("[]").split(",")
        if m.strip()
    ]
    thread_bodies = []
    for thread_slug in mentions:
        tpath = THREADS / f"{thread_slug}.md"
        if tpath.exists():
            thread_bodies.append({"slug": thread_slug, "body": _read(tpath)})

    return {
        "ok": True,
        "slug": slug,
        "verdict": verdict,
        "version_count": version_count,
        "max_versions": MAX_VERSIONS,
        "terminal": terminal,
        "termination_reason": (
            "verdict_ship_as_is" if verdict == "ship-as-is"
            else "max_versions_reached" if version_count >= MAX_VERSIONS
            else None
        ),
        "draft_path": str(draft.relative_to(REPO_ROOT)),
        "draft_meta": draft_meta,
        "draft_body": draft_body,
        "review_path": str(review.relative_to(REPO_ROOT)),
        "review_meta": review_meta,
        "review_body": review_body,
        "threads": thread_bodies,
    }


def archive(slug: str) -> dict:
    """Move current draft to versions/<slug>/v<N>.md before overwriting."""
    draft = DRAFTS / f"{slug}.md"
    if not draft.exists():
        return {"ok": False, "error": f"no draft at {draft}"}
    versions_dir = VERSIONS / slug
    versions_dir.mkdir(parents=True, exist_ok=True)
    next_n = _version_count(slug) + 1
    target = versions_dir / f"v{next_n}.md"
    shutil.copy2(str(draft), str(target))

    review = DRAFTS / f"{slug}.simona-review.md"
    if review.exists():
        review_target = versions_dir / f"v{next_n}.simona-review.md"
        shutil.copy2(str(review), str(review_target))
        review.unlink()

    return {
        "ok": True,
        "slug": slug,
        "archived_to": str(target.relative_to(REPO_ROOT)),
        "review_archived": str(review_target.relative_to(REPO_ROOT)) if review.exists() else None,
        "version_count_after": next_n,
    }


def versions(slug: str) -> dict:
    """For Simona's review of v2+: return all archived versions + their reviews."""
    versions_dir = VERSIONS / slug
    if not versions_dir.exists():
        return {"slug": slug, "count": 0, "versions": []}
    out = []
    for vfile in sorted(versions_dir.glob("v*.md")):
        if ".simona-review" in vfile.name:
            continue
        n = vfile.stem  # "v1", "v2", ...
        review_file = versions_dir / f"{n}.simona-review.md"
        out.append({
            "n": n,
            "draft_body": _read(vfile),
            "review_body": _read(review_file) if review_file.exists() else None,
        })
    return {"slug": slug, "count": len(out), "versions": out}


def cmd_materials(args):
    result = materials(args.slug)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def cmd_archive(args):
    result = archive(args.slug)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def cmd_versions(args):
    print(json.dumps(versions(args.slug), indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_mat = sub.add_parser("materials", help="Get draft + review + thread/note corpus for revising")
    p_mat.add_argument("--slug", required=True)

    p_arc = sub.add_parser("archive", help="Copy current draft to versions/<slug>/v<N>.md before overwriting")
    p_arc.add_argument("--slug", required=True)

    p_ver = sub.add_parser("versions", help="List archived versions + their reviews (for Simona's v2+ pass)")
    p_ver.add_argument("--slug", required=True)

    args = parser.parse_args()
    if args.cmd == "materials":
        cmd_materials(args)
    elif args.cmd == "archive":
        cmd_archive(args)
    elif args.cmd == "versions":
        cmd_versions(args)


if __name__ == "__main__":
    main()
