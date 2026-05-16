"""
revise_draft — single revision pass driven by Marlow's own self-review.

Flow: self_review has landed a `<slug>.self-review.md` with verdict
ship / revise / hold-for-alex. This handler is the revision step that fires
only when verdict is `revise`. Marlow reads the review, rewrites the draft
once, archives v1 to `versions/<slug>/v1.md`. After this, the orchestrator
calls publish — no second review, no further iteration.

Terminal cases (handler reports terminal=True and Marlow exits without
rewriting):
  - verdict ship           — go straight to publish.
  - verdict hold-for-alex  — flip status to `held`, no publish.
  - version_count >= 1     — already revised once; publish v2 as-is.

The behavioral files (voice, structure, topic, pre-publish-pauses) are
included in materials so the revision can reference the same rubric the
self-review used.

CLI:
    python handlers/revise_draft.py materials --slug <slug>
        → JSON: draft + self-review + version count + terminal flag +
          rubric + thread bodies.
    python handlers/revise_draft.py archive --slug <slug>
        → move current drafts/<slug>.md → drafts/versions/<slug>/v<N>.md
          and remove the existing self-review file (archived alongside).
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DRAFTS = REPO_ROOT / "projects" / "blog" / "drafts"
VERSIONS = DRAFTS / "versions"
THREADS = REPO_ROOT / "projects" / "research" / "threads"
MEMORY = REPO_ROOT / "memory"

MAX_VERSIONS = 2  # one revision pass; v2 ships regardless.

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


def _version_count(slug: str) -> int:
    d = VERSIONS / slug
    if not d.exists():
        return 0
    return len([f for f in d.glob("v*.md") if ".self-review" not in f.name])


def _terminal_reason(verdict: str | None, version_count: int) -> str | None:
    if verdict == "ship":
        return "verdict_ship"
    if verdict == "hold-for-alex":
        return "verdict_hold_for_alex"
    if version_count >= MAX_VERSIONS - 1:
        # Already revised once (v1 archived). v2 is the current draft; publish it.
        return "max_versions_reached"
    return None


def materials(slug: str) -> dict:
    draft = DRAFTS / f"{slug}.md"
    review = DRAFTS / f"{slug}.self-review.md"
    if not draft.exists():
        return {"ok": False, "error": f"no draft at {draft}"}
    if not review.exists():
        return {
            "ok": False,
            "error": f"no self-review at {review} — run self_review first",
        }

    draft_meta, draft_body = _parse_frontmatter(_read(draft))
    review_meta, review_body = _parse_frontmatter(_read(review))
    verdict = review_meta.get("verdict")

    version_count = _version_count(slug)
    term_reason = _terminal_reason(verdict, version_count)

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

    rubric = {key: _read(path) for key, path in BEHAVIORAL_FILES.items()}

    return {
        "ok": True,
        "slug": slug,
        "verdict": verdict,
        "verdict_options": ["ship", "revise", "hold-for-alex"],
        "version_count": version_count,
        "max_versions": MAX_VERSIONS,
        "terminal": term_reason is not None,
        "termination_reason": term_reason,
        "draft_path": str(draft.relative_to(REPO_ROOT)),
        "draft_meta": draft_meta,
        "draft_body": draft_body,
        "review_path": str(review.relative_to(REPO_ROOT)),
        "review_meta": review_meta,
        "review_body": review_body,
        "threads": thread_bodies,
        "rubric": rubric,
    }


def archive(slug: str) -> dict:
    """Move current draft to versions/<slug>/v<N>.md before overwriting with the revision."""
    draft = DRAFTS / f"{slug}.md"
    if not draft.exists():
        return {"ok": False, "error": f"no draft at {draft}"}
    versions_dir = VERSIONS / slug
    versions_dir.mkdir(parents=True, exist_ok=True)
    next_n = _version_count(slug) + 1
    target = versions_dir / f"v{next_n}.md"
    shutil.copy2(str(draft), str(target))

    review = DRAFTS / f"{slug}.self-review.md"
    review_target = None
    if review.exists():
        review_target = versions_dir / f"v{next_n}.self-review.md"
        shutil.copy2(str(review), str(review_target))
        review.unlink()

    return {
        "ok": True,
        "slug": slug,
        "archived_to": str(target.relative_to(REPO_ROOT)),
        "review_archived": str(review_target.relative_to(REPO_ROOT)) if review_target else None,
        "version_count_after": next_n,
    }


def _git(*args: str) -> tuple[int, str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def commit_revision(slug: str) -> dict:
    """Commit + push the revised draft, revision-notes, and archived v1 files.

    Captures the v1 → v2 transition cleanly: archived versions become
    `drafts/versions/<slug>/v1.md` and `v1.self-review.md`; the draft file
    is the v2 content; `revision-notes.md` records what was applied vs
    defended.
    """
    draft = DRAFTS / f"{slug}.md"
    notes = DRAFTS / f"{slug}.revision-notes.md"
    versions_dir = VERSIONS / slug
    if not draft.exists():
        return {"ok": False, "error": f"no v2 draft at {draft}"}
    if not notes.exists():
        return {"ok": False, "error": f"no revision-notes at {notes}"}

    # Stage everything under the relevant slug paths so deletions of the
    # original draft+review get captured alongside additions. The self-review
    # file was tracked by an earlier commit-review and has now been moved into
    # versions/ by `archive`, so its old path needs to be in the pathspec for
    # `git add -A` to stage the deletion.
    paths = [
        str(draft.relative_to(REPO_ROOT)),
        str(notes.relative_to(REPO_ROOT)),
        str((DRAFTS / f"{slug}.self-review.md").relative_to(REPO_ROOT)),
    ]
    if versions_dir.exists():
        paths.append(str(versions_dir.relative_to(REPO_ROOT)))
    # Header image lives in the Astro public dir, outside drafts/. If a
    # revision regenerated it, picking up the change here keeps the commit
    # coherent. If unchanged, the path is a no-op for `git add`.
    image_path = REPO_ROOT / "projects" / "blog" / "site" / "public" / "images" / f"{slug}.png"
    if image_path.exists():
        paths.append(str(image_path.relative_to(REPO_ROOT)))

    rc, out = _git("add", "-A", "--", *paths)
    if rc != 0:
        return {"ok": False, "error": f"git add: {out}"}
    rc, out = _git(
        "commit",
        "-m", f"Revise: {slug} (v2)",
        "-m", "Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
    )
    if rc != 0:
        return {"ok": False, "error": f"git commit: {out}"}
    rc, out = _git("push", "origin", "master")
    if rc != 0:
        return {"ok": True, "committed": True, "pushed": False, "error": f"git push: {out}"}
    return {"ok": True, "committed": True, "pushed": True}


def cmd_materials(args):
    result = materials(args.slug)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def cmd_archive(args):
    result = archive(args.slug)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def cmd_commit_revision(args):
    result = commit_revision(args.slug)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_mat = sub.add_parser("materials", help="Draft + self-review + rubric for revising")
    p_mat.add_argument("--slug", required=True)

    p_arc = sub.add_parser("archive", help="Copy current draft to versions/<slug>/v<N>.md before overwriting")
    p_arc.add_argument("--slug", required=True)

    p_com = sub.add_parser("commit-revision", help="Commit + push v2 draft, revision-notes, archived versions")
    p_com.add_argument("--slug", required=True)

    args = parser.parse_args()
    if args.cmd == "materials":
        cmd_materials(args)
    elif args.cmd == "archive":
        cmd_archive(args)
    elif args.cmd == "commit-revision":
        cmd_commit_revision(args)


if __name__ == "__main__":
    main()
