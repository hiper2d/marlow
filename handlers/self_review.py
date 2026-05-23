"""
self_review — Marlow's single self-critique pass before publish.

Replaces the previous Simona-driven external review. Marlow reads her own draft
against the behavioral files (voice, structure, topic, pre-publish-pauses) and
writes a verdict to `<slug>.self-review.md`. The next pipeline step (revise or
publish) reads the verdict and acts.

This handler is deterministic gathering only. Marlow's session does the
editorial scoring: reads `materials`, judges the draft against the rubric, and
writes the review file. The review file is the input to `revise_draft` or
`publish`.

Verdicts (Marlow writes one of these in the review frontmatter):
  - ship          : publish as-is.
  - revise        : one revision pass, then publish regardless.
  - hold-for-alex : a pre-publish-pause triggered. Flip status to `held`,
                    surface at next editorial review.

CLI:
    python handlers/self_review.py list-pending
        → JSON: drafts whose frontmatter has status:draft AND no sibling
          <slug>.self-review.md.
    python handlers/self_review.py materials --slug <slug>
        → JSON: draft body + the four behavioral files as the rubric.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DRAFTS = REPO_ROOT / "projects" / "blog" / "drafts"
MEMORY = REPO_ROOT / "memory"
THREADS = REPO_ROOT / "projects" / "research" / "threads"

BEHAVIORAL_FILES = {
    "voice_guidelines": MEMORY / "voice-guidelines.md",
    "structure_notes": MEMORY / "structure-notes.md",
    "topic_guidance": MEMORY / "topic-guidance.md",
    "pre_publish_pauses": MEMORY / "pre-publish-pauses.md",
}


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


def list_pending() -> dict:
    if not DRAFTS.exists():
        return {"count": 0, "drafts": []}
    out = []
    for f in sorted(DRAFTS.glob("*.md")):
        if any(suffix in f.name for suffix in (".self-review", ".simona-review", ".revision-notes")):
            continue
        meta, _ = _parse_frontmatter(_read(f))
        if meta.get("status") != "draft":
            continue
        slug = f.stem
        review_sibling = DRAFTS / f"{slug}.self-review.md"
        if review_sibling.exists():
            continue
        out.append({
            "slug": slug,
            "path": str(f.relative_to(REPO_ROOT)),
            "title": meta.get("title"),
        })
    return {"count": len(out), "drafts": out}


def materials(slug: str) -> dict:
    draft = DRAFTS / f"{slug}.md"
    if not draft.exists():
        return {"ok": False, "error": f"no draft at {draft}"}
    draft_text = _read(draft)
    draft_meta, draft_body = _parse_frontmatter(draft_text)
    if draft_meta.get("status") != "draft":
        return {
            "ok": False,
            "error": f"draft status is '{draft_meta.get('status')}', expected 'draft'",
        }
    rubric = {key: _read(path) for key, path in BEHAVIORAL_FILES.items()}
    return {
        "ok": True,
        "slug": slug,
        "draft_path": str(draft.relative_to(REPO_ROOT)),
        "draft_meta": draft_meta,
        "draft_body": draft_body,
        "review_target": str((DRAFTS / f"{slug}.self-review.md").relative_to(REPO_ROOT)),
        "rubric": rubric,
        "verdict_options": ["ship", "revise", "hold-for-alex"],
    }


def _git(*args: str) -> tuple[int, str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def commit_review(slug: str) -> dict:
    """Commit + push draft and self-review files.

    Skipped when verdict is `hold-for-alex` — held drafts stay private until
    Alex releases them via `marlow approve`.
    """
    draft = DRAFTS / f"{slug}.md"
    review = DRAFTS / f"{slug}.self-review.md"
    if not draft.exists():
        return {"ok": False, "error": f"no draft at {draft}"}
    if not review.exists():
        return {"ok": False, "error": f"no self-review at {review}"}

    review_meta, _ = _parse_frontmatter(_read(review))
    verdict = review_meta.get("verdict")
    if verdict == "hold-for-alex":
        return {
            "ok": True,
            "committed": False,
            "skipped": True,
            "reason": "verdict is hold-for-alex — draft stays private until release",
        }

    paths = [
        str(draft.relative_to(REPO_ROOT)),
        str(review.relative_to(REPO_ROOT)),
    ]
    image_path = REPO_ROOT / "projects" / "blog" / "site" / "public" / "images" / f"{slug}.png"
    if image_path.exists():
        paths.append(str(image_path.relative_to(REPO_ROOT)))

    # Thread files referenced in the draft's mentions — Marlow rewrites
    # each one during drafting to reflect the new article (see
    # memory/thread-structure.md). Ship the rewrite with this commit.
    # A missing thread file is a drafting-tick miss: the article will ship
    # with a mentions: link that 404s on the live site. Fail loudly so the
    # drafting tick is redone (write or open the thread) before publish.
    draft_meta, _ = _parse_frontmatter(_read(draft))
    mentions = [
        m.strip().strip('"').strip("'")
        for m in draft_meta.get("mentions", "").strip("[]").split(",")
        if m.strip()
    ]
    missing_threads = []
    for thread_slug in mentions:
        thread_path = THREADS / f"{thread_slug}.md"
        if thread_path.exists():
            paths.append(str(thread_path.relative_to(REPO_ROOT)))
        else:
            missing_threads.append(thread_slug)
    if missing_threads:
        return {
            "ok": False,
            "error": (
                f"draft references thread(s) with no file on disk: "
                f"{', '.join(missing_threads)}. Expected at "
                f"projects/research/threads/<slug>.md. Open or rewrite the "
                f"thread per memory/thread-structure.md before commit-review."
            ),
            "missing_threads": missing_threads,
        }

    rc, out = _git("add", "--", *paths)
    if rc != 0:
        return {"ok": False, "error": f"git add: {out}"}
    rc, out = _git(
        "commit",
        "-m", f"Draft + self-review: {slug} (verdict: {verdict})",
        "-m", "Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
    )
    if rc != 0:
        return {"ok": False, "error": f"git commit: {out}"}
    rc, out = _git("push", "origin", "master")
    if rc != 0:
        return {"ok": True, "committed": True, "pushed": False, "error": f"git push: {out}"}
    return {"ok": True, "committed": True, "pushed": True, "verdict": verdict}


def cmd_list_pending(args):
    print(json.dumps(list_pending(), indent=2, ensure_ascii=False))


def cmd_materials(args):
    result = materials(args.slug)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def cmd_commit_review(args):
    result = commit_review(args.slug)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list-pending", help="Drafts ready for self-review")

    p_mat = sub.add_parser("materials", help="Draft body + behavioral rubric for one slug")
    p_mat.add_argument("--slug", required=True)

    p_com = sub.add_parser("commit-review", help="Commit + push draft and self-review (skipped on hold-for-alex)")
    p_com.add_argument("--slug", required=True)

    args = parser.parse_args()
    if args.cmd == "list-pending":
        cmd_list_pending(args)
    elif args.cmd == "materials":
        cmd_materials(args)
    elif args.cmd == "commit-review":
        cmd_commit_review(args)


if __name__ == "__main__":
    main()
