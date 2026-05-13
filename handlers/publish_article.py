"""
publish_article — the approval/publish primitive for Marlow's blog.

This is a *deterministic* handler (no editorial work). It's invoked by
Alex via `marlow approve <slug>` or `marlow reject <slug>`, never by
Marlow's own ticks — the approval gate is Alex's. The CLI wraps this
module; Marlow's session never imports it.

CLI:
    python handlers/publish_article.py approve --slug <slug>
        → move drafts/<slug>.md → published/<slug>.md, flip status,
          archive any versions, commit + push
    python handlers/publish_article.py reject --slug <slug>
        → move drafts/<slug>.md → drafts/rejected/<slug>/, archive versions
    python handlers/publish_article.py status --slug <slug>
        → JSON: current status, paths, version count
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DRAFTS = REPO_ROOT / "projects" / "blog" / "drafts"
PUBLISHED = REPO_ROOT / "projects" / "blog" / "published"
REJECTED = DRAFTS / "rejected"
VERSIONS = DRAFTS / "versions"


def _read_frontmatter(path: Path) -> tuple[dict, str]:
    """Return (frontmatter_dict, full_body). Caller can rewrite if needed."""
    text = path.read_text()
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    fm_block = text[4:end]
    body = text[end + 5:]
    meta: dict = {}
    for line in fm_block.splitlines():
        if ":" not in line:
            continue
        k, _, v = line.partition(":")
        meta[k.strip()] = v.strip()
    return meta, body


def _flip_status(path: Path, new_status: str) -> None:
    """Rewrite frontmatter `status: ...` line. Preserves everything else."""
    text = path.read_text()
    if not text.startswith("---\n"):
        raise ValueError(f"no frontmatter in {path}")
    lines = text.splitlines(keepends=True)
    out = []
    in_fm = False
    fm_seen = 0
    replaced = False
    for line in lines:
        if line.startswith("---") and fm_seen < 2:
            fm_seen += 1
            in_fm = fm_seen < 2
            out.append(line)
            continue
        if in_fm and line.startswith("status:") and not replaced:
            out.append(f"status: {new_status}\n")
            replaced = True
            continue
        out.append(line)
    if not replaced:
        raise ValueError(f"no status: line in {path} frontmatter")
    path.write_text("".join(out))


def _archive_versions(slug: str, dest_versions_dir: Path) -> list[str]:
    """Move drafts/versions/<slug>/ contents to dest if any. Returns moved paths."""
    src = VERSIONS / slug
    if not src.exists():
        return []
    dest_versions_dir.mkdir(parents=True, exist_ok=True)
    moved = []
    for f in sorted(src.glob("*.md")):
        target = dest_versions_dir / f.name
        shutil.move(str(f), str(target))
        moved.append(str(target.relative_to(REPO_ROOT)))
    try:
        src.rmdir()
    except OSError:
        pass
    return moved


def _git(*args: str) -> tuple[int, str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def _commit_and_push(message: str, paths: list[str]) -> dict:
    rc, out = _git("add", *paths)
    if rc != 0:
        return {"committed": False, "pushed": False, "error": f"git add: {out}"}
    rc, out = _git(
        "commit",
        "-m", message,
        "-m", "Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>",
    )
    if rc != 0:
        return {"committed": False, "pushed": False, "error": f"git commit: {out}"}
    rc, out = _git("push", "origin", "master")
    if rc != 0:
        return {"committed": True, "pushed": False, "error": f"git push: {out}"}
    return {"committed": True, "pushed": True}


def approve(slug: str) -> dict:
    draft = DRAFTS / f"{slug}.md"
    if not draft.exists():
        return {"ok": False, "error": f"no draft at {draft}"}

    meta, _ = _read_frontmatter(draft)
    if meta.get("status") != "draft":
        return {"ok": False, "error": f"status is '{meta.get('status')}', expected 'draft'"}

    PUBLISHED.mkdir(parents=True, exist_ok=True)
    published_path = PUBLISHED / f"{slug}.md"
    if published_path.exists():
        return {"ok": False, "error": f"published file already exists: {published_path}"}

    review = DRAFTS / f"{slug}.simona-review.md"
    moved_review = None
    if review.exists():
        target_review = PUBLISHED / f"{slug}.simona-review.md"
        shutil.move(str(review), str(target_review))
        moved_review = str(target_review.relative_to(REPO_ROOT))

    shutil.move(str(draft), str(published_path))
    _flip_status(published_path, "published")

    versions_dest = PUBLISHED / "versions" / slug
    archived = _archive_versions(slug, versions_dest)

    paths_to_commit = [
        str(published_path.relative_to(REPO_ROOT)),
        str(draft.relative_to(REPO_ROOT)),
    ]
    if moved_review:
        paths_to_commit.extend([
            moved_review,
            str(review.relative_to(REPO_ROOT)),
        ])
    if archived:
        paths_to_commit.extend(archived)
        paths_to_commit.append(str((VERSIONS / slug).relative_to(REPO_ROOT)))

    git_result = _commit_and_push(
        f"Publish: {slug}",
        paths_to_commit,
    )

    return {
        "ok": git_result.get("pushed", False) or git_result.get("committed", False),
        "slug": slug,
        "published_path": str(published_path.relative_to(REPO_ROOT)),
        "review_moved": moved_review,
        "versions_archived": archived,
        "git": git_result,
    }


def reject(slug: str, reason: str | None = None) -> dict:
    draft = DRAFTS / f"{slug}.md"
    if not draft.exists():
        return {"ok": False, "error": f"no draft at {draft}"}

    now = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
    dest_dir = REJECTED / f"{slug}-{now}"
    dest_dir.mkdir(parents=True, exist_ok=True)

    shutil.move(str(draft), str(dest_dir / f"{slug}.md"))
    moved_paths = [str((dest_dir / f"{slug}.md").relative_to(REPO_ROOT))]

    review = DRAFTS / f"{slug}.simona-review.md"
    if review.exists():
        shutil.move(str(review), str(dest_dir / f"{slug}.simona-review.md"))
        moved_paths.append(str((dest_dir / f"{slug}.simona-review.md").relative_to(REPO_ROOT)))

    archived = _archive_versions(slug, dest_dir / "versions")
    moved_paths.extend(archived)

    if reason:
        (dest_dir / "reject-reason.md").write_text(f"# Rejection reason\n\n{reason}\n")
        moved_paths.append(str((dest_dir / "reject-reason.md").relative_to(REPO_ROOT)))

    git_result = _commit_and_push(
        f"Reject: {slug}" + (f" — {reason[:60]}" if reason else ""),
        moved_paths,
    )

    return {
        "ok": git_result.get("committed", False),
        "slug": slug,
        "rejected_to": str(dest_dir.relative_to(REPO_ROOT)),
        "git": git_result,
    }


def status(slug: str) -> dict:
    draft = DRAFTS / f"{slug}.md"
    published = PUBLISHED / f"{slug}.md"
    review = DRAFTS / f"{slug}.simona-review.md"
    versions_dir = VERSIONS / slug
    version_count = len(list(versions_dir.glob("*.md"))) if versions_dir.exists() else 0
    return {
        "slug": slug,
        "draft_exists": draft.exists(),
        "published_exists": published.exists(),
        "review_exists": review.exists(),
        "version_count": version_count,
        "frontmatter_status": _read_frontmatter(draft)[0].get("status") if draft.exists() else None,
    }


def cmd_approve(args):
    print(json.dumps(approve(args.slug), indent=2, ensure_ascii=False))


def cmd_reject(args):
    print(json.dumps(reject(args.slug, args.reason), indent=2, ensure_ascii=False))


def cmd_status(args):
    print(json.dumps(status(args.slug), indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_approve = sub.add_parser("approve", help="Approve a draft → publish + push")
    p_approve.add_argument("--slug", required=True)

    p_reject = sub.add_parser("reject", help="Reject a draft → move to drafts/rejected/")
    p_reject.add_argument("--slug", required=True)
    p_reject.add_argument("--reason", help="Optional one-line rejection note")

    p_status = sub.add_parser("status", help="Inspect draft/published state for a slug")
    p_status.add_argument("--slug", required=True)

    args = parser.parse_args()
    if args.cmd == "approve":
        cmd_approve(args)
    elif args.cmd == "reject":
        cmd_reject(args)
    elif args.cmd == "status":
        cmd_status(args)


if __name__ == "__main__":
    main()
