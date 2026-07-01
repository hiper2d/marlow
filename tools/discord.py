"""
Marlow Discord - post to the "AI Werewolf and other projects" community.

The bot ("Marlow", app id 1520835258553995364) posts directly via the REST API
under its own identity. No webhooks. Used for two flows:

  1. Auto-crosspost: when Marlow publishes a blog article, handlers/publish_article
     posts a short announcement (title + summary + link, NOT the full body) into
     #our-writings. Best-effort: a Discord failure never fails the publish.

  2. Alex's own articles: Simona runs the CLI (`announce --author Alex ...`) to
     post Alex's blog posts into #our-writings. Simona has no token of her own;
     she posts *through* Marlow's integration here.

Two gotchas baked in (learned 2026-06-28):
  - Discord's API sits behind Cloudflare, which 403s (error 1010) the default
    python User-Agent. We MUST send a real User-Agent header.
  - #our-writings / #game-updates deny Send Messages to @everyone (read-only for
    members). The bot is a member too, so a per-channel overwrite was added to let
    THIS bot post while members stay read-only. Nothing to do here, just don't be
    surprised by "Missing Access" if those overwrites ever get removed.

Importable:
    from tools.discord import announce_article, post_message
    announce_article("My title", "A one-line summary.", "https://.../post/slug")

CLI for manual posting / testing:
    python tools/discord.py announce --title "T" --summary "S" --url "https://..." --author Alex
    python tools/discord.py post --channel our-writings --content "hello"
    python tools/discord.py whoami
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
FALLBACK_LOG = REPO_ROOT / "digests" / "_discord_fallback.log"

API_BASE = "https://discord.com/api/v10"
# Cloudflare blocks the default urllib/requests UA with 403 code 1010.
USER_AGENT = "DiscordBot (https://aiwerewolf.net, 0.1)"
HTTP_TIMEOUT = 10  # seconds

GUILD_ID = "1519821471978098739"
BOT_ID = "1520835258553995364"

# Single source of truth for channel ids (server "AI Werewolf and other projects").
CHANNELS = {
    "welcome": "1521185432556273665",             # read-only newcomer landing channel (top of server)
    "our-writings": "1520820626439405578",       # blog crossposts (Marlow + Alex)
    "game-updates": "1520820917205205024",        # Werewolf game updates
    "issues": "1521893796084846773",               # Werewolf bug/issue reports (Werewolf category)
    "ai-news": "1520820557015416994",
    "general": "1519821472447729676",
    "general-discussion": "1520820825400545441",
    "rules": "1520816036411215883",
    "moderator-only": "1520816036897886381",       # private - bot has NO access
}
DEFAULT_CHANNEL = "our-writings"

# Embed accent per author, so Marlow's and Alex's posts read as distinct.
AUTHOR_COLORS = {
    "Marlow": 0x5865F2,  # Discord blurple
    "Alex": 0x2ECC71,    # green
}


def _token() -> str | None:
    load_dotenv(REPO_ROOT / ".env")
    return os.getenv("DISCORD_MARLOW_TOKEN")


def _headers(token: str) -> dict:
    return {
        "Authorization": f"Bot {token}",
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json",
    }


def _resolve_channel(channel: str) -> str:
    """Accept a friendly name ('our-writings') or a raw numeric id."""
    if channel in CHANNELS:
        return CHANNELS[channel]
    return channel  # assume a raw id


def _log_fallback(payload: dict, reason: str) -> None:
    """Never silently lose a post - log it locally when Discord delivery fails."""
    FALLBACK_LOG.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with open(FALLBACK_LOG, "a") as f:
        f.write(f"[{ts}] [{reason}] {json.dumps(payload)}\n")


def post_message(channel: str, content: str | None = None, embeds: list | None = None) -> dict:
    """Post one message to a channel. Returns {ok, message_id, detail}.

    `channel` is a friendly name from CHANNELS or a raw channel id. Provide
    `content`, `embeds`, or both (Discord requires at least one).
    """
    token = _token()
    if not token:
        out = {"ok": False, "message_id": None, "detail": "missing DISCORD_MARLOW_TOKEN in .env"}
        _log_fallback({"channel": channel, "content": content, "embeds": embeds}, out["detail"])
        return out
    if not content and not embeds:
        return {"ok": False, "message_id": None, "detail": "nothing to post (no content or embeds)"}

    body: dict = {}
    if content:
        body["content"] = content
    if embeds:
        body["embeds"] = embeds
    cid = _resolve_channel(channel)
    try:
        resp = requests.post(
            f"{API_BASE}/channels/{cid}/messages",
            headers=_headers(token),
            json=body,
            timeout=HTTP_TIMEOUT,
        )
        if resp.status_code not in (200, 201):
            out = {"ok": False, "message_id": None, "detail": f"discord returned {resp.status_code}: {resp.text[:200]}"}
            _log_fallback(body, out["detail"])
            return out
        mid = resp.json().get("id")
        return {"ok": True, "message_id": mid, "detail": "posted"}
    except (requests.RequestException, ValueError) as e:
        out = {"ok": False, "message_id": None, "detail": f"discord request failed: {e}"}
        _log_fallback(body, out["detail"])
        return out


def announce_article(
    title: str,
    summary: str,
    url: str,
    author: str = "Marlow",
    channel: str = DEFAULT_CHANNEL,
    image_url: str | None = None,
) -> dict:
    """Post a blog-publish announcement: title + summary + link, never the full body.

    Renders as an embed card (clickable title -> url, summary as the blurb, optional
    cover image), so the channel stays a clean feed. `image_url` must be a PUBLIC
    absolute URL - Discord fetches it server-side and drops it silently if it 404s
    or isn't reachable. Returns {ok, message_id, detail}.
    """
    embed = {
        "author": {"name": f"New post by {author}"},
        "title": title,
        "url": url,
        "color": AUTHOR_COLORS.get(author, 0x95A5A6),
    }
    if summary:
        embed["description"] = summary
    if image_url:
        embed["image"] = {"url": image_url}
    # A bare url line under the card gives a plain clickable link + reliable unfurl.
    return post_message(channel, content=url, embeds=[embed])


def get_channel_messages(channel: str, after: str | None = None, limit: int = 100) -> dict:
    """Fetch one page of messages from a channel, newest-first. Returns
    {ok, messages, detail}.

    `channel` is a friendly name or raw id. `after` is a message-id cursor: only
    messages newer than it are returned (used to poll just what's new since the
    last scan). `limit` caps the page at <=100 (Discord's max). The caller paginates
    by advancing `after` to the newest id it has seen.

    Reading OTHER users' message `content` over REST requires the bot to have the
    privileged Message Content intent enabled (Developer Portal -> Bot -> Privileged
    Gateway Intents). Without it, content/attachments come back empty for messages
    the bot didn't author. The monitor handler detects that case and flags it.
    """
    token = _token()
    if not token:
        return {"ok": False, "messages": [], "detail": "missing DISCORD_MARLOW_TOKEN in .env"}
    cid = _resolve_channel(channel)
    params: dict = {"limit": min(max(int(limit), 1), 100)}
    if after:
        params["after"] = after
    try:
        resp = requests.get(
            f"{API_BASE}/channels/{cid}/messages",
            headers=_headers(token),
            params=params,
            timeout=HTTP_TIMEOUT,
        )
        if resp.status_code != 200:
            return {"ok": False, "messages": [], "detail": f"discord returned {resp.status_code}: {resp.text[:200]}"}
        return {"ok": True, "messages": resp.json(), "detail": f"fetched {len(resp.json())}"}
    except (requests.RequestException, ValueError) as e:
        return {"ok": False, "messages": [], "detail": f"discord request failed: {e}"}


def get_guild_counts() -> dict:
    """Approximate member + online counts for the server. Returns
    {ok, member_count, presence_count, detail}. Cheap, one call; the counts are
    Discord's own approximations (fine for a trend stat)."""
    token = _token()
    if not token:
        return {"ok": False, "member_count": None, "presence_count": None, "detail": "missing DISCORD_MARLOW_TOKEN in .env"}
    try:
        resp = requests.get(
            f"{API_BASE}/guilds/{GUILD_ID}",
            headers=_headers(token),
            params={"with_counts": "true"},
            timeout=HTTP_TIMEOUT,
        )
        if resp.status_code != 200:
            return {"ok": False, "member_count": None, "presence_count": None, "detail": f"discord returned {resp.status_code}: {resp.text[:200]}"}
        d = resp.json()
        return {
            "ok": True,
            "member_count": d.get("approximate_member_count"),
            "presence_count": d.get("approximate_presence_count"),
            "detail": "ok",
        }
    except (requests.RequestException, ValueError) as e:
        return {"ok": False, "member_count": None, "presence_count": None, "detail": f"discord request failed: {e}"}


def whoami() -> dict:
    """Sanity check: confirm the token authenticates and report the bot identity."""
    token = _token()
    if not token:
        return {"ok": False, "detail": "missing DISCORD_MARLOW_TOKEN in .env"}
    try:
        resp = requests.get(f"{API_BASE}/users/@me", headers=_headers(token), timeout=HTTP_TIMEOUT)
        if resp.status_code != 200:
            return {"ok": False, "detail": f"discord returned {resp.status_code}: {resp.text[:200]}"}
        d = resp.json()
        return {"ok": True, "username": d.get("username"), "id": d.get("id"), "bot": d.get("bot")}
    except (requests.RequestException, ValueError) as e:
        return {"ok": False, "detail": f"discord request failed: {e}"}


def main():
    parser = argparse.ArgumentParser(description="Post to the AI Werewolf Discord server.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ann = sub.add_parser("announce", help="post a blog-publish announcement (title + summary + link)")
    p_ann.add_argument("--title", required=True)
    p_ann.add_argument("--summary", default="")
    p_ann.add_argument("--url", required=True)
    p_ann.add_argument("--author", default="Marlow")
    p_ann.add_argument("--channel", default=DEFAULT_CHANNEL)
    p_ann.add_argument("--image", default=None, help="public absolute URL of a cover image")

    p_post = sub.add_parser("post", help="post raw content to a channel")
    p_post.add_argument("--channel", default=DEFAULT_CHANNEL)
    p_post.add_argument("--content", required=True)

    sub.add_parser("whoami", help="confirm the token + show bot identity")

    args = parser.parse_args()
    if args.cmd == "announce":
        print(json.dumps(announce_article(args.title, args.summary, args.url, args.author, args.channel, args.image)))
    elif args.cmd == "post":
        print(json.dumps(post_message(args.channel, content=args.content)))
    elif args.cmd == "whoami":
        print(json.dumps(whoami()))


if __name__ == "__main__":
    main()
