"""
crosspost — surface Marlow's daily news picks and stash the ones Alex flags as
article ideas. (Legacy name: this used to draft + auto-post crossposts in Alex's
voice; that loop was retired 2026-06-05 — Alex writes his pieces himself, with
Simona, and only wants Marlow to REMEMBER which items he flagged. The draft/post
machinery below is dormant, kept only in case we co-post from here later.)

Current flow (full procedure: CLAUDE.md "### News highlights — handler `crosspost`"):
  1. daily_news_curate sends each pick as its own Telegram message and calls
     `send-item` here to register it (keyed by the message_id).
  2. Alex replies TO a message when he wants to WRITE about it himself (his reply
     is his seed/take). No reply = nothing happens.
  3. `poll` reads new replies and matches each to its item via reply_to_message_id.
  4. `save-idea` writes the flagged item + Alex's comment to the article-ideas
     folder. Simona reads that folder when Alex asks "anything from Marlow's
     findings?" and they craft the article together. Marlow does NOT draft or post.

NOTE on the Telegram offset: `poll` advances the shared getUpdates offset (same
one substack_approvals uses). While this task is active it must be the sole
inbound poller, or the two will consume each other's replies. substack_approvals
is disabled during the manual-polish phase, so there's no contention today; if it
comes back, they need a shared inbound dispatcher.

CLI:
    python handlers/crosspost.py send-item --url U --title T --source S --take-file F
    python handlers/crosspost.py poll
    python handlers/crosspost.py save-idea --msg-id N --comment "Alex's take"
    python handlers/crosspost.py list [--status sent|saved]
  (dormant, retired auto-post path: set-platforms / add-instruction / send-draft / post / skip)
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import re
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parent.parent
HANDLERS_DIR = Path(__file__).resolve().parent
ARTICLE_IDEAS_DIR = REPO_ROOT / "projects" / "research" / "article-ideas"
sys.path.insert(0, str(REPO_ROOT))

from tools import crosspost_store as store  # noqa: E402
from tools import notify  # noqa: E402
from tools import telegram_poll  # noqa: E402


# ─── send-item: deliver a news pick + register it ─────────────────────────────

def _news_message(title: str, source: str, take: str, url: str) -> str:
    src = f" ({source})" if source else ""
    return (
        f"{title}{src}\n\n"
        f"{take.strip()}\n\n"
        f"{url}\n\n"
        f"reply if you want to write about this — I'll save it to your article ideas"
    )


def send_item(url: str, title: str, source: str, take: str) -> dict:
    msg = _news_message(title, source, take, url)
    res = notify.send_telegram_message(msg)
    if not res.get("ok") or not res.get("message_id"):
        return {"ok": False, "detail": f"telegram send failed: {res.get('detail')}"}
    item = store.add_item(res["message_id"], url, title, source, take.strip())
    return {"ok": True, "msg_id": res["message_id"], "item": item}


# ─── poll: read replies, match to items ───────────────────────────────────────

def poll() -> dict:
    try:
        msgs = telegram_poll.fetch_new_messages(advance=True)
    except Exception as e:  # noqa: BLE001 — surface transport failure to the tick
        return {"ok": False, "detail": f"telegram poll failed: {e}"}
    actions, unmatched = [], []
    for m in msgs:
        rid = m.get("reply_to_message_id")
        item, which = store.find_by_reply(rid) if rid else (None, None)
        if item is None:
            unmatched.append({"text": m.get("text"), "reply_to_message_id": rid})
            continue
        actions.append({
            "reply_text": m.get("text"),
            "which": which,                      # "news" (route it) | "draft" (go/edit/voice)
            "item_msg_id": item["msg_id"],
            "item": {
                "title": item["title"], "url": item["url"], "source": item["source"],
                "status": item["status"], "platforms": item["platforms"],
                "instructions": item["instructions"], "drafts": item["drafts"],
            },
        })
    return {"ok": True, "count": len(actions), "actions": actions, "unmatched": unmatched}


# ─── save-idea: stash a flagged item as an article idea for Simona + Alex ──────

def _slug(text: str, maxlen: int = 50) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return (s[:maxlen].rstrip("-")) or "idea"


def save_idea(msg_id: int, comment: str) -> dict:
    """Write a flagged news item + Alex's comment to the article-ideas folder.
    This is the whole point of the retired crosspost loop now: Marlow remembers
    what Alex wants to write about; Simona reads this folder and they write it."""
    item = store.get(msg_id)
    if item is None:
        return {"ok": False, "detail": f"no item for msg_id {msg_id}"}
    ARTICLE_IDEAS_DIR.mkdir(parents=True, exist_ok=True)
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    path = ARTICLE_IDEAS_DIR / f"{date}-{_slug(item['title'])}.md"
    body = (
        f"---\n"
        f"title: \"{item['title']}\"\n"
        f"url: {item['url']}\n"
        f"source: {item['source']}\n"
        f"highlighted_at: {store._now_iso()}\n"
        f"status: idea\n"
        f"---\n\n"
        f"## Alex flagged this to write about\n\n"
        f"{(comment or '').strip() or '(no comment — flagged as interesting)'}\n\n"
        f"---\n"
        f"Marlow's note when she sent it:\n\n{item.get('take', '').strip()}\n"
    )
    path.write_text(body)
    store.set_status(msg_id, "saved")
    notify.send_telegram_message(f"Saved to your article ideas: {item['title']}")
    try:
        shown = str(path.relative_to(REPO_ROOT))
    except ValueError:
        shown = str(path)
    return {"ok": True, "path": shown, "title": item["title"]}


# ─── send-draft: store the draft(s) and send back for review (DORMANT) ─────────

def _draft_review_message(item: dict) -> str:
    lines = [f"Draft for: {item['title']}", f"Platforms: {', '.join(item['platforms']) or '(none set)'}", ""]
    d = item["drafts"]
    if d.get("substack"):
        lines += ["— Substack —", d["substack"], ""]
    if d.get("x"):
        lines.append("— X —")
        for i, t in enumerate(d["x"], 1):
            lines.append(f"{i}/ {t}")
        lines.append("")
    lines.append("reply 'go' to post, or tell me what to change")
    return "\n".join(lines)


def send_draft(msg_id: int, substack_text: str | None, x_tweets: list[str] | None) -> dict:
    item = store.get(msg_id)
    if item is None:
        return {"ok": False, "detail": f"no item for msg_id {msg_id}"}
    if substack_text is not None:
        store.set_draft(msg_id, "substack", substack_text.strip())
    if x_tweets is not None:
        store.set_draft(msg_id, "x", [t.strip() for t in x_tweets if t and t.strip()])
    item = store.get(msg_id)
    if not item["drafts"]:
        return {"ok": False, "detail": "no drafts provided"}
    res = notify.send_telegram_message(_draft_review_message(item))
    if not res.get("ok") or not res.get("message_id"):
        return {"ok": False, "detail": f"telegram send failed: {res.get('detail')}"}
    store.set_draft_msg_id(msg_id, res["message_id"])
    store.set_status(msg_id, "awaiting_approval")
    return {"ok": True, "draft_msg_id": res["message_id"], "item": store.get(msg_id)}


# ─── post: push the approved drafts to the platforms ──────────────────────────

def _run_handler(name: str, *args: str) -> dict:
    """Shell out to a sibling handler CLI (its own CDP port / env). Returns its
    parsed JSON, or a synthetic failure dict."""
    proc = subprocess.run(
        ["uv", "run", "python", str(HANDLERS_DIR / name), *args],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    try:
        return json.loads(proc.stdout)
    except (json.JSONDecodeError, ValueError):
        return {"ok": False, "detail": f"{name} returned no JSON (rc={proc.returncode}): {proc.stderr[:200]}"}


def post(msg_id: int) -> dict:
    item = store.get(msg_id)
    if item is None:
        return {"ok": False, "detail": f"no item for msg_id {msg_id}"}
    # Alex always crossposts to both; default to both if an older item has none set.
    platforms = item.get("platforms") or list(store.PLATFORMS)
    drafts = item.get("drafts") or {}
    already = item.get("posted") or {}
    results: dict[str, dict] = {}
    skipped: list[str] = []  # platforms already live (idempotent retry — never double-post)

    with tempfile.TemporaryDirectory() as td:
        if "substack" in platforms and drafts.get("substack"):
            if already.get("substack"):
                skipped.append("substack")
            else:
                p = Path(td) / "substack.txt"
                p.write_text(drafts["substack"])
                r = _run_handler("substack.py", "post-note", "--text-file", str(p))
                results["substack"] = r
                store.set_posted(msg_id, "substack", r.get("url"))
        if "x" in platforms and drafts.get("x"):
            if already.get("x"):
                skipped.append("x")
            else:
                p = Path(td) / "x.json"
                p.write_text(json.dumps(drafts["x"]))
                r = _run_handler("x.py", "post-thread", "--text-file", str(p))
                results["x"] = r
                store.set_posted(msg_id, "x", r.get("url"))

    failed = [pl for pl, r in results.items() if not r.get("ok")]
    # Status reflects the FULL posted state, not just this run (a retry that
    # finishes the missing half should land on "posted", not "partial").
    item = store.get(msg_id)
    live = [pl for pl in platforms if (item.get("posted") or {}).get(pl)]
    store.set_status(msg_id, "posted" if len(live) == len(platforms) else ("partial" if live else "sent"))

    item = store.get(msg_id)
    lines = [f"Posted: {item['title']}"]
    for pl in ("substack", "x"):
        if pl in skipped:
            lines.append(f"  {pl}: already live ({already.get(pl)})")
        elif pl in results:
            r = results[pl]
            lines.append(f"  {pl}: {r.get('url') or r.get('detail') or ('ok' if r.get('ok') else 'FAILED')}")
    notify.send_telegram_message("\n".join(lines))

    return {"ok": not failed, "posted": [pl for pl, r in results.items() if r.get("ok")],
            "skipped_already_live": skipped, "failed": failed, "results": results, "item": item}


# ─── CLI ─────────────────────────────────────────────────────────────────────

def _emit(result: dict):
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    si = sub.add_parser("send-item")
    si.add_argument("--url", required=True)
    si.add_argument("--title", required=True)
    si.add_argument("--source", default="")
    si.add_argument("--take-file", required=True)

    sub.add_parser("poll")

    sv = sub.add_parser("save-idea", help="stash a flagged item as an article idea")
    sv.add_argument("--msg-id", required=True, type=int)
    sv.add_argument("--comment", default="", help="Alex's reply / take to seed the article")

    sp = sub.add_parser("set-platforms")
    sp.add_argument("--msg-id", required=True, type=int)
    sp.add_argument("--platforms", required=True, help="comma list: substack,x")

    ai = sub.add_parser("add-instruction")
    ai.add_argument("--msg-id", required=True, type=int)
    ai.add_argument("--text", required=True)

    sd = sub.add_parser("send-draft")
    sd.add_argument("--msg-id", required=True, type=int)
    sd.add_argument("--substack-file", default=None)
    sd.add_argument("--x-file", default=None, help="JSON list of tweet strings")

    po = sub.add_parser("post")
    po.add_argument("--msg-id", required=True, type=int)

    sk = sub.add_parser("skip")
    sk.add_argument("--msg-id", required=True, type=int)

    ls = sub.add_parser("list")
    ls.add_argument("--status", default=None)

    args = ap.parse_args()

    if args.cmd == "send-item":
        _emit(send_item(args.url, args.title, args.source, Path(args.take_file).read_text()))
    elif args.cmd == "poll":
        _emit(poll())
    elif args.cmd == "save-idea":
        _emit(save_idea(args.msg_id, args.comment))
    elif args.cmd == "set-platforms":
        plats = [p.strip() for p in args.platforms.split(",") if p.strip()]
        it = store.set_platforms(args.msg_id, plats)
        _emit({"ok": bool(it), "item": it} if it else {"ok": False, "detail": "no such item"})
    elif args.cmd == "add-instruction":
        it = store.add_instruction(args.msg_id, args.text)
        _emit({"ok": bool(it), "item": it} if it else {"ok": False, "detail": "no such item"})
    elif args.cmd == "send-draft":
        substack_text = Path(args.substack_file).read_text() if args.substack_file else None
        x_tweets = json.loads(Path(args.x_file).read_text()) if args.x_file else None
        _emit(send_draft(args.msg_id, substack_text, x_tweets))
    elif args.cmd == "post":
        _emit(post(args.msg_id))
    elif args.cmd == "skip":
        it = store.set_status(args.msg_id, "skipped")
        _emit({"ok": bool(it), "item": it} if it else {"ok": False, "detail": "no such item"})
    elif args.cmd == "list":
        items = store.list_items(status=args.status)
        _emit({"ok": True, "count": len(items), "items": items})


if __name__ == "__main__":
    main()
