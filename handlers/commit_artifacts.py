"""
commit_artifacts — nightly artifact snapshot.

Marlow's publish flow only commits *published articles*, so durable autonomous
output (news/daily digests, research notes, ops reports, working memory) piles
up untracked between publishes. This handler is the periodic backstop: stage
everything git isn't ignoring, commit it as a dated snapshot, and push — so the
repo is a real running backup rather than something Simona sweeps by hand once
a month.

Fully deterministic; there is no editorial judgment here. The session just calls
`snapshot` and relays the JSON result.

Runtime state is excluded by .gitignore (tasks/queue.json, *_offset.json, the
calorie DB, feed/budget state, substack poll state, etc.), so `git add -A` only
ever picks up durable content. Committing a draft here is a *backup*, not a
publish — the public site only deploys from projects/blog/published/ — so this
never touches the publish pipeline.

CLI:
    python handlers/commit_artifacts.py snapshot [--no-push]
        → git add -A; commit if anything is staged; push (also pushes any
          prior unpushed commits, e.g. a publish that committed but failed to
          push). Prints a JSON result.

Result status:
    clean   — nothing to commit and remote already current; no-op.
    ok      — committed and/or pushed successfully.
    partial — committed locally but push failed (network / remote moved);
              safe, the next run retries the push.
    failed  — git add/commit itself failed.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=REPO_ROOT, capture_output=True, text=True
    )


def _staged_count() -> int:
    r = _git("diff", "--cached", "--name-only")
    return len([n for n in r.stdout.splitlines() if n.strip()])


def _ahead_of_remote() -> bool:
    """True if HEAD has commits not on its upstream (or upstream is unknown)."""
    r = _git("rev-list", "--count", "@{u}..HEAD")
    if r.returncode != 0:
        return True
    try:
        return int(r.stdout.strip()) > 0
    except ValueError:
        return True


def snapshot(do_push: bool) -> dict:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    add = _git("add", "-A")
    if add.returncode != 0:
        return {"status": "failed", "committed": False, "pushed": False,
                "detail": f"git add failed: {add.stderr.strip()}"}

    files_changed = _staged_count()
    committed = False
    sha = None

    if files_changed > 0:
        msg = (
            f"chore(snapshot): nightly artifact backup {stamp}\n\n"
            f"Automated snapshot of durable artifacts ({files_changed} paths): "
            f"digests, research notes, ops reports, working memory. Runtime "
            f"state is gitignored. See handlers/commit_artifacts.py."
        )
        commit = _git("commit", "-m", msg)
        if commit.returncode != 0:
            return {"status": "failed", "committed": False, "pushed": False,
                    "files_changed": files_changed,
                    "detail": "git commit failed: "
                              + (commit.stderr.strip() or commit.stdout.strip())}
        committed = True
        sha = _git("rev-parse", "--short", "HEAD").stdout.strip()

    # Nothing new staged and nothing unpushed → genuinely clean.
    if not committed and not _ahead_of_remote():
        return {"status": "clean", "committed": False, "pushed": False,
                "files_changed": 0,
                "detail": "nothing to snapshot, remote up to date"}

    if not do_push:
        return {"status": "ok", "committed": committed, "pushed": False,
                "files_changed": files_changed, "sha": sha,
                "detail": "commit only (--no-push)"}

    push = _git("push")
    if push.returncode == 0:
        return {"status": "ok", "committed": committed, "pushed": True,
                "files_changed": files_changed, "sha": sha, "detail": "pushed"}

    # Push failed — remote may have advanced. Rebase once and retry.
    pull = _git("pull", "--rebase", "--autostash")
    if pull.returncode == 0 and _git("push").returncode == 0:
        return {"status": "ok", "committed": committed, "pushed": True,
                "files_changed": files_changed, "sha": sha,
                "detail": "pushed after rebase"}

    # Commit is safe locally; the next run retries the push.
    return {"status": "partial", "committed": committed, "pushed": False,
            "files_changed": files_changed, "sha": sha,
            "detail": f"committed locally; push failed: {push.stderr.strip()}"}


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("snapshot", help="git add -A, commit durable artifacts, push")
    p.add_argument("--no-push", action="store_true", help="commit only, skip push")
    args = parser.parse_args()
    if args.cmd == "snapshot":
        print(json.dumps(snapshot(do_push=not args.no_push), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
