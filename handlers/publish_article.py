"""
publish_article — the publish / hold / release / reject primitives.

In the autonomous pipeline Marlow drafts, self-reviews, optionally revises,
and publishes herself. This handler exposes the deterministic actions; the
editorial decisions happen upstream in self_review / revise_draft.

Verbs:
  publish — autonomous Marlow path. Requires status:draft. Moves the draft
            to published/, flips status to `published`, archives any
            versions/, and commits + pushes.
  hold    — pre-publish-pause path. Requires status:draft. Flips status to
            `held`. No move, no push. The draft sits in drafts/ until the
            next editorial review releases or rejects it.
  release — Alex's path for held drafts. Requires status:held. Flips back
            to `draft`, then publishes. Single CLI command for the common
            "Alex looked, it's fine, ship it" flow.
  reject  — Move the draft to drafts/rejected/<slug>-<timestamp>/. Works
            on either status:draft or status:held.

`approve` is kept as an alias for `publish` for backward compat with the
existing `marlow approve` CLI command. Will be removed once the CLI is
updated to use `publish` / `release` explicitly.

CLI:
    python handlers/publish_article.py publish --slug <slug>
    python handlers/publish_article.py hold    --slug <slug> [--reason <r>]
    python handlers/publish_article.py release --slug <slug>
    python handlers/publish_article.py reject  --slug <slug> [--reason <r>]
    python handlers/publish_article.py status  --slug <slug>
    python handlers/publish_article.py approve --slug <slug>   # alias for publish
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
SITE_BASE = "https://marlow.hiper2d.workers.dev"

sys.path.insert(0, str(REPO_ROOT))
from tools import notify, reactions_store  # noqa: E402


def _read_frontmatter(path: Path) -> tuple[dict, str]:
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


def _filter_stageable(paths: list[str]) -> list[str]:
    """Keep paths that exist on disk OR are tracked by git.

    `git add <pathspec>` fails the whole stage with "did not match any files"
    when given a path that's neither on disk nor in the index. Paths that
    formerly existed but vanish during the publish (the source versions/
    directory after `_archive_versions` rmdir's it, e.g.) need a tracked-status
    check before being passed to `git add`.
    """
    valid = []
    for p in paths:
        if (REPO_ROOT / p).exists():
            valid.append(p)
            continue
        rc, _ = _git("ls-files", "--error-unmatch", "--", p)
        if rc == 0:
            valid.append(p)
    return valid


def _commit_and_push(message: str, paths: list[str]) -> dict:
    stageable = _filter_stageable(paths)
    if not stageable:
        return {"committed": False, "pushed": False, "error": "no stageable paths"}
    rc, out = _git("add", "--", *stageable)
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


def _publish_internal(slug: str, commit_message: str | None = None) -> dict:
    """Move draft → published, delete the entire draft trail, commit, push.

    Caller must enforce the precondition on draft status. This function
    trusts the gate is already checked.

    On publish, only `published/<slug>.md` survives in the working tree.
    All draft-side artifacts (self-review, revision-notes, hold-reason,
    versions/<slug>/, legacy simona-review siblings) are deleted. The
    audit trail lives in git history — `git log -- projects/blog/drafts/<slug>*`
    shows every iteration before the publish wiped them.
    """
    draft = DRAFTS / f"{slug}.md"
    if not draft.exists():
        return {"ok": False, "error": f"no draft at {draft}"}

    PUBLISHED.mkdir(parents=True, exist_ok=True)
    published_path = PUBLISHED / f"{slug}.md"
    if published_path.exists():
        return {"ok": False, "error": f"published file already exists: {published_path}"}

    shutil.move(str(draft), str(published_path))
    _flip_status(published_path, "published")

    trail_siblings = [
        f"{slug}.self-review.md",
        f"{slug}.simona-review.md",
        f"{slug}.revision-notes.md",
        f"{slug}.revision-notes.simona-review.md",
        f"{slug}.hold-reason.md",
    ]
    deleted_paths = []
    for sibling in trail_siblings:
        path = DRAFTS / sibling
        if path.exists():
            path.unlink()
            deleted_paths.append(str(path.relative_to(REPO_ROOT)))

    versions_src = VERSIONS / slug
    if versions_src.exists():
        for f in versions_src.iterdir():
            if f.is_file():
                f.unlink()
                deleted_paths.append(str(f.relative_to(REPO_ROOT)))
        try:
            versions_src.rmdir()
            deleted_paths.append(str(versions_src.relative_to(REPO_ROOT)))
        except OSError:
            pass

    paths_to_commit = [
        str(published_path.relative_to(REPO_ROOT)),
        str(draft.relative_to(REPO_ROOT)),
    ]
    paths_to_commit.extend(deleted_paths)

    git_result = _commit_and_push(
        commit_message or f"Publish: {slug}",
        paths_to_commit,
    )

    return {
        "ok": git_result.get("pushed", False) or git_result.get("committed", False),
        "slug": slug,
        "published_path": str(published_path.relative_to(REPO_ROOT)),
        "deleted_trail": deleted_paths,
        "git": git_result,
    }


def _request_reaction(slug: str, meta: dict) -> None:
    """After a successful publish, ping Alex for a one-line gut reaction and
    register it so `crosspost.poll` can capture his reply. Best-effort: a failed
    ping must never fail the publish. Reactions are Simona's review surface —
    Marlow never reads them (see tools/reactions_store)."""
    try:
        url_slug = meta.get("slug") or slug
        title = meta.get("title") or url_slug
        url = f"{SITE_BASE}/post/{url_slug}"
        msg = (
            f"📄 Published: {title}\n{url}\n\n"
            f"One-line gut reaction? Reply to this — bored, loved the opening, "
            f"too dry, whatever you've got. (No reply is fine.)"
        )
        res = notify.send_telegram_message(msg)
        if res.get("ok") and res.get("message_id"):
            reactions_store.request(res["message_id"], slug, title, url)
    except Exception:  # noqa: BLE001 — a publish that pushed must report success
        pass


def publish(slug: str) -> dict:
    """Marlow's autonomous publish path. Requires status:draft."""
    draft = DRAFTS / f"{slug}.md"
    if not draft.exists():
        return {"ok": False, "error": f"no draft at {draft}"}
    meta, _ = _read_frontmatter(draft)
    if meta.get("status") != "draft":
        return {
            "ok": False,
            "error": f"status is '{meta.get('status')}', expected 'draft' (use 'release' for held drafts)",
        }
    result = _publish_internal(slug)
    if result.get("ok"):
        _request_reaction(slug, meta)
    return result


def hold(slug: str, reason: str | None = None) -> dict:
    """Flip status:draft → status:held. Marlow's pre-publish-pause path."""
    draft = DRAFTS / f"{slug}.md"
    if not draft.exists():
        return {"ok": False, "error": f"no draft at {draft}"}
    meta, _ = _read_frontmatter(draft)
    if meta.get("status") != "draft":
        return {
            "ok": False,
            "error": f"status is '{meta.get('status')}', expected 'draft'",
        }
    _flip_status(draft, "held")
    note_path = None
    if reason:
        note_path = DRAFTS / f"{slug}.hold-reason.md"
        note_path.write_text(
            f"---\nslug: {slug}\nheld_at: {datetime.now(timezone.utc).isoformat()}\n---\n\n{reason}\n"
        )
    return {
        "ok": True,
        "slug": slug,
        "status": "held",
        "draft_path": str(draft.relative_to(REPO_ROOT)),
        "hold_reason_path": str(note_path.relative_to(REPO_ROOT)) if note_path else None,
    }


def release(slug: str) -> dict:
    """Alex's path: release a held draft → publish. Requires status:held."""
    draft = DRAFTS / f"{slug}.md"
    if not draft.exists():
        return {"ok": False, "error": f"no draft at {draft}"}
    meta, _ = _read_frontmatter(draft)
    if meta.get("status") != "held":
        return {
            "ok": False,
            "error": f"status is '{meta.get('status')}', expected 'held'",
        }
    _flip_status(draft, "draft")
    hold_reason = DRAFTS / f"{slug}.hold-reason.md"
    if hold_reason.exists():
        hold_reason.unlink()
    return _publish_internal(slug, commit_message=f"Publish (released from hold): {slug}")


def reject(slug: str, reason: str | None = None) -> dict:
    """Move draft to drafts/rejected/<slug>-<timestamp>/. Works on draft or held."""
    draft = DRAFTS / f"{slug}.md"
    if not draft.exists():
        return {"ok": False, "error": f"no draft at {draft}"}

    now = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")
    dest_dir = REJECTED / f"{slug}-{now}"
    dest_dir.mkdir(parents=True, exist_ok=True)

    shutil.move(str(draft), str(dest_dir / f"{slug}.md"))
    moved_paths = [str((dest_dir / f"{slug}.md").relative_to(REPO_ROOT))]

    for sibling_name in (f"{slug}.self-review.md", f"{slug}.simona-review.md", f"{slug}.hold-reason.md", f"{slug}.revision-notes.md"):
        sibling = DRAFTS / sibling_name
        if sibling.exists():
            shutil.move(str(sibling), str(dest_dir / sibling_name))
            moved_paths.append(str((dest_dir / sibling_name).relative_to(REPO_ROOT)))

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
    review = DRAFTS / f"{slug}.self-review.md"
    legacy_review = DRAFTS / f"{slug}.simona-review.md"
    hold_reason = DRAFTS / f"{slug}.hold-reason.md"
    versions_dir = VERSIONS / slug
    version_count = (
        len([f for f in versions_dir.glob("v*.md") if ".self-review" not in f.name])
        if versions_dir.exists()
        else 0
    )
    return {
        "slug": slug,
        "draft_exists": draft.exists(),
        "published_exists": published.exists(),
        "self_review_exists": review.exists(),
        "legacy_simona_review_exists": legacy_review.exists(),
        "hold_reason_exists": hold_reason.exists(),
        "version_count": version_count,
        "frontmatter_status": _read_frontmatter(draft)[0].get("status") if draft.exists() else None,
    }


def approve(slug: str) -> dict:
    """`marlow approve <slug>` entry point — smart wrapper for human use.

    Dispatches by current status: draft → publish, held → release. Lets Alex
    use a single CLI verb regardless of which gate the draft is sitting at.
    Autonomous code should call publish() or release() directly.
    """
    draft = DRAFTS / f"{slug}.md"
    if not draft.exists():
        return {"ok": False, "error": f"no draft at {draft}"}
    meta, _ = _read_frontmatter(draft)
    status_value = meta.get("status")
    if status_value == "draft":
        return publish(slug)
    if status_value == "held":
        return release(slug)
    return {
        "ok": False,
        "error": f"status is '{status_value}', expected 'draft' or 'held'",
    }


def cmd_publish(args):
    print(json.dumps(publish(args.slug), indent=2, ensure_ascii=False))


def cmd_hold(args):
    print(json.dumps(hold(args.slug, args.reason), indent=2, ensure_ascii=False))


def cmd_release(args):
    print(json.dumps(release(args.slug), indent=2, ensure_ascii=False))


def cmd_reject(args):
    print(json.dumps(reject(args.slug, args.reason), indent=2, ensure_ascii=False))


def cmd_status(args):
    print(json.dumps(status(args.slug), indent=2, ensure_ascii=False))


def cmd_approve(args):
    print(json.dumps(approve(args.slug), indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_pub = sub.add_parser("publish", help="Marlow's autonomous publish — requires status:draft")
    p_pub.add_argument("--slug", required=True)

    p_hold = sub.add_parser("hold", help="Flip status:draft → status:held (pre-publish-pause)")
    p_hold.add_argument("--slug", required=True)
    p_hold.add_argument("--reason", help="Optional one-line hold reason")

    p_rel = sub.add_parser("release", help="Release a held draft → publish (Alex's path)")
    p_rel.add_argument("--slug", required=True)

    p_rej = sub.add_parser("reject", help="Move draft to drafts/rejected/")
    p_rej.add_argument("--slug", required=True)
    p_rej.add_argument("--reason", help="Optional one-line rejection note")

    p_stat = sub.add_parser("status", help="Inspect draft/published state for a slug")
    p_stat.add_argument("--slug", required=True)

    p_approve = sub.add_parser("approve", help="Alias for publish (legacy CLI compat)")
    p_approve.add_argument("--slug", required=True)

    args = parser.parse_args()
    if args.cmd == "publish":
        cmd_publish(args)
    elif args.cmd == "hold":
        cmd_hold(args)
    elif args.cmd == "release":
        cmd_release(args)
    elif args.cmd == "reject":
        cmd_reject(args)
    elif args.cmd == "status":
        cmd_status(args)
    elif args.cmd == "approve":
        cmd_approve(args)


if __name__ == "__main__":
    main()
