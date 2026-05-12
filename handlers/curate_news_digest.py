"""
curate_news_digest — end-of-day news curation orchestration.

During the day, feed_scan ticks have Marlow write candidate notes to
projects/research/notes/<date>/candidates/<slug>.md — one per item
worth considering. At end of day, this handler is invoked. Marlow's
session does the editorial work in-tick:

    1. Run `list --date X` → JSON of today's candidates
    2. Rank, pick top 3-5 across all sources
    3. For each pick, run handlers/fetch_article.py to get body
    4. Write the composed digest message (in Marlow's voice) to
       digests/news/<date>.md
    5. Run `send --date X` → chunks + delivers via Telegram

CLI:
    python handlers/curate_news_digest.py list --date YYYY-MM-DD
        → JSON list of candidate notes for that date
    python handlers/curate_news_digest.py send --date YYYY-MM-DD
        → read digests/news/<date>.md, chunk, send to Telegram
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CANDIDATES_ROOT = REPO_ROOT / "projects" / "research" / "notes"
NEWS_DIGEST_DIR = REPO_ROOT / "digests" / "news"

sys.path.insert(0, str(REPO_ROOT))
from tools import notify  # noqa: E402

TG_MAX_LEN = 4000  # Telegram caps at 4096; leave headroom for chunk markers


def _today() -> str:
    """Return the date this curate run should cover.

    Scheduled at 22:00 UTC. If the agent was asleep and the tick fires
    after UTC rollover, defaulting to `now().date()` would point at the
    new day's empty candidates dir. Within the first 4 hours after UTC
    midnight, default to yesterday — that's the day the schedule meant.
    """
    now = datetime.now(timezone.utc)
    if now.hour < 4:
        return (now - timedelta(days=1)).strftime("%Y-%m-%d")
    return now.strftime("%Y-%m-%d")


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse a simple key: value YAML-ish frontmatter block. Returns (meta, body)."""
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


def list_candidates(date: str) -> list[dict]:
    """Read all candidate notes for the given date. Returns list of dicts."""
    dir_path = CANDIDATES_ROOT / date / "candidates"
    if not dir_path.exists():
        return []
    out = []
    for f in sorted(dir_path.glob("*.md")):
        try:
            text = f.read_text()
        except OSError:
            continue
        meta, body = _parse_frontmatter(text)
        out.append({
            "path": str(f.relative_to(REPO_ROOT)),
            "slug": f.stem,
            "title": meta.get("title", ""),
            "url": meta.get("url", ""),
            "source": meta.get("source", ""),
            "captured_at": meta.get("captured_at", ""),
            "body": body.strip(),
        })
    return out


def _chunk(text: str, max_len: int = TG_MAX_LEN) -> list[str]:
    """Split text into <= max_len chunks, breaking on paragraph boundaries."""
    if len(text) <= max_len:
        return [text]
    chunks: list[str] = []
    current = ""
    for paragraph in text.split("\n\n"):
        if not paragraph:
            continue
        candidate = (current + "\n\n" + paragraph) if current else paragraph
        if len(candidate) > max_len:
            if current:
                chunks.append(current)
                current = paragraph
            else:
                while len(paragraph) > max_len:
                    chunks.append(paragraph[:max_len])
                    paragraph = paragraph[max_len:]
                current = paragraph
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks


def send(date: str) -> dict:
    """Read the composed news digest for date and deliver via Telegram."""
    path = NEWS_DIGEST_DIR / f"{date}.md"
    if not path.exists():
        return {"date": date, "ok": False, "error": f"no composed digest at {path}"}
    body = path.read_text().strip()
    if not body:
        return {"date": date, "ok": False, "error": "composed digest is empty"}
    chunks = _chunk(body)
    sent, failed = [], []
    total = len(chunks)
    for i, chunk in enumerate(chunks, 1):
        prefix = f"[{i}/{total}] " if total > 1 else ""
        ok, detail = notify.send_telegram(prefix + chunk)
        (sent if ok else failed).append({"chunk": i, "detail": detail})
    return {
        "date": date,
        "ok": len(failed) == 0,
        "chunks_total": total,
        "chunks_sent": len(sent),
        "chunks_failed": len(failed),
        "details": {"sent": sent, "failed": failed},
    }


# ─── CLI ───────────────────────────────────────────────────────────────────


def cmd_list(args):
    date = args.date or _today()
    items = list_candidates(date)
    print(json.dumps({"date": date, "count": len(items), "items": items}, indent=2, ensure_ascii=False))


def cmd_send(args):
    date = args.date or _today()
    result = send(date)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="List today's candidate notes")
    p_list.add_argument("--date", help="YYYY-MM-DD; defaults to today UTC")

    p_send = sub.add_parser("send", help="Send the composed news digest for date")
    p_send.add_argument("--date", help="YYYY-MM-DD; defaults to today UTC")

    args = parser.parse_args()
    if args.cmd == "list":
        cmd_list(args)
    elif args.cmd == "send":
        cmd_send(args)


if __name__ == "__main__":
    main()
