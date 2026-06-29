"""
monitor_discord - community activity + behavior watch for the Discord server.

The fifth werewolf-ops monitoring workstream, but the first that watches PEOPLE
rather than infrastructure. monitor_keys watches what the free tier COSTS,
werewolf_stats what the game PRODUCES, monitor_health / monitor_betterstack
whether the app WORKS. This watches the community server "AI Werewolf and other
projects": who is talking, how much, and whether anyone is misbehaving.

This handler is the DETERMINISTIC half only. It polls the conversational channels
for messages new since the last scan (per-channel id cursor), computes activity
stats, and applies cheap deterministic heuristics for the obvious bad-behavior
shapes (someone posting too much, repeating the same message, mass-mentioning,
flooding links). It returns the new messages as a capped sample so the SESSION
(Marlow, who is the model) can read them and judge the things rules cannot - rude,
hostile, or pestering tone. The split is the same as every other ops monitor:
handler gathers, session interprets and alerts.

Alert model - cursor diff, not rate-spike. We only ever look at messages NEW since
the last scan (per-channel `last_message_ids`). First sight of a channel baselines
it (records the latest id, gathers NO history, emits one digest line) so we never
dump a backlog or alarm on a pre-existing pile. Same discipline as monitor_health
/ monitor_betterstack.

Reading other users' message content over REST needs the privileged Message
Content intent (Developer Portal -> Bot -> Privileged Gateway Intents). If it is
off, non-bot messages come back with empty content; the handler detects that and
emits a digest issue so Marlow can tell Alex to enable it. The watch is blind to
tone until then (it can still count messages and catch volume/mention floods).

Credentials: DISCORD_MARLOW_TOKEN (same bot token the poster uses), in the
launchd plist (mirrored to os.environ by env_loader) or .env. Fails clean
(ok: false) if unset - same failure contract as the other monitors.

CLI:
    python handlers/monitor_discord.py report   -> poll + persist, JSON
    python handlers/monitor_discord.py show      -> last scan, human-readable
    python handlers/monitor_discord.py digest    -> digest block (empty if quiet)
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from driver.env_loader import import_plist_env  # noqa: E402
import_plist_env()

from driver.budget_state import STATE_DIR  # noqa: E402
from tools import discord  # noqa: E402

# Conversational channels where members can actually post (and thus misbehave).
# The read-only feeds (our-writings, game-updates, rules) carry no member chat,
# and moderator-only is invisible to the bot - so none of them are monitored.
MONITORED = ["general", "general-discussion", "ai-news"]

PER_PAGE = 100          # Discord's max page size
MAX_PAGES = 5           # cap fetch at 500 new msgs / channel / run (bounds a flood)
SAMPLE_CAP = 60         # messages handed to the session for tone judgment
SAMPLE_CHARS = 6000     # total content budget for that sample

# Deterministic bad-behavior thresholds, per author within one scan window.
VOLUME_DIGEST = 15      # "posts a lot" - worth a mention
VOLUME_URGENT = 40      # firehose - ping now
REPEAT_DIGEST = 4       # same message N times = spammy
REPEAT_URGENT = 8       # same message N times = clearly spam/flood
LINK_FLOOD = 5          # this many links from one author in the window
MENTION_FLOOD = 6       # this many user-mentions in a single message

DISCORD_LATEST = STATE_DIR / "discord_latest.json"
DISCORD_HISTORY = STATE_DIR / "discord_history.jsonl"


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _checked_at(now: datetime) -> str:
    return now.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _prior() -> dict | None:
    """Last scan's persisted state. None -> never scanned."""
    try:
        with DISCORD_LATEST.open() as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def _fetch_new(channel: str, after: str | None) -> tuple[list[dict], str | None, str | None]:
    """All messages in `channel` newer than `after`, oldest-first.

    Returns (messages, new_cursor, error). `new_cursor` is the newest message id
    now seen (carry forward even when no new messages, so it never regresses).
    Pages forward by advancing the cursor to the newest id in each page.
    """
    cursor = after
    collected: list[dict] = []
    for _ in range(MAX_PAGES):
        res = discord.get_channel_messages(channel, after=cursor, limit=PER_PAGE)
        if not res["ok"]:
            return ([], after, res["detail"])
        page = res["messages"]            # newest-first
        if not page:
            break
        collected.extend(page)
        cursor = max((m["id"] for m in page), key=int)  # advance to newest in page
        if len(page) < PER_PAGE:
            break
    new_cursor = max((m["id"] for m in collected), key=int) if collected else after
    collected.sort(key=lambda m: int(m["id"]))         # oldest-first for reading
    return (collected, new_cursor, None)


def _has_link(text: str) -> bool:
    return "http://" in text or "https://" in text


def _flatten(channel: str, m: dict) -> dict:
    """The fields we keep per message - small, JSON-safe, enough to judge tone."""
    a = m.get("author", {})
    content = m.get("content") or ""
    return {
        "channel": channel,
        "id": m.get("id"),
        "author_id": a.get("id"),
        "author": a.get("global_name") or a.get("username") or a.get("id"),
        "bot": bool(a.get("bot")),
        "ts": m.get("timestamp"),
        "content": content,
        "mentions": len(m.get("mentions") or []),
        "mention_everyone": bool(m.get("mention_everyone")),
        "attachments": len(m.get("attachments") or []),
        "has_link": _has_link(content),
    }


def _derive_issues(msgs: list[dict]) -> list[dict]:
    """Deterministic bad-behavior flags from the new (non-bot) messages.

    These are the shapes rules catch cleanly: volume, repetition, mention/link
    floods. Tone (rude/hostile/pestering) is left to the session's judgment pass.
    """
    issues: list[dict] = []
    human = [m for m in msgs if not m["bot"]]
    if not human:
        return issues

    by_author: dict[str, list[dict]] = {}
    for m in human:
        by_author.setdefault(m["author"], []).append(m)

    for author, ms in by_author.items():
        n = len(ms)
        if n >= VOLUME_URGENT:
            issues.append({"severity": "urgent", "kind": "high_volume", "target": author,
                           "detail": f"{author} posted {n} messages this window (firehose)"})
        elif n >= VOLUME_DIGEST:
            issues.append({"severity": "digest", "kind": "high_volume", "target": author,
                           "detail": f"{author} posted {n} messages this window"})

        # repeated identical content (spam/flood)
        repeats = Counter(m["content"].strip() for m in ms if m["content"].strip())
        top, cnt = (repeats.most_common(1) or [("", 0)])[0]
        if cnt >= REPEAT_URGENT:
            issues.append({"severity": "urgent", "kind": "repeat_spam", "target": author,
                           "detail": f"{author} sent the same message {cnt}x: {top[:80]!r}"})
        elif cnt >= REPEAT_DIGEST:
            issues.append({"severity": "digest", "kind": "repeat_spam", "target": author,
                           "detail": f"{author} sent the same message {cnt}x: {top[:80]!r}"})

        links = sum(1 for m in ms if m["has_link"])
        if links >= LINK_FLOOD:
            issues.append({"severity": "digest", "kind": "link_flood", "target": author,
                           "detail": f"{author} posted {links} links this window"})

    for m in human:
        if m["mention_everyone"] or m["mentions"] >= MENTION_FLOOD:
            who = "@everyone/@here" if m["mention_everyone"] else f"{m['mentions']} users"
            issues.append({"severity": "digest", "kind": "mass_mention", "target": m["author"],
                           "detail": f"{m['author']} mass-mentioned {who} in #{m['channel']}"})

    # Message Content intent off? Non-bot messages exist but all are empty (no text,
    # no attachment) -> the bot can't see content, so tone judgment is impossible.
    blind = [m for m in human if not m["content"].strip() and m["attachments"] == 0]
    if human and len(blind) == len(human):
        issues.append({"severity": "digest", "kind": "content_intent_off", "target": "config",
                       "detail": "all member messages came back empty - enable the Message "
                                 "Content intent (Developer Portal -> Bot -> Privileged Gateway "
                                 "Intents) so tone can be judged"})
    return issues


def _sample(msgs: list[dict]) -> list[dict]:
    """A capped slice of new messages for the session to read and judge for tone.
    Most-recent-first, bounded by count and total characters."""
    out, used = [], 0
    for m in reversed(msgs):
        c = (m["content"] or "")[:500]
        if used + len(c) > SAMPLE_CHARS and out:
            break
        out.append({"channel": m["channel"], "author": m["author"], "bot": m["bot"],
                    "ts": m["ts"], "content": c})
        used += len(c)
        if len(out) >= SAMPLE_CAP:
            break
    out.reverse()
    return out


def _compact(report: dict) -> dict:
    return {
        "checked_at": report.get("checked_at"),
        "new_messages": report.get("new_messages"),
        "active_authors": report.get("active_authors"),
        "members": (report.get("server") or {}).get("member_count"),
        "issues": [f"{i['severity']}:{i['kind']}:{i['target']}" for i in report.get("issues", [])],
        "any_urgent": report.get("any_urgent"),
        "baselined": report.get("baselined"),
    }


def _save(report: dict) -> None:
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        tmp = DISCORD_LATEST.with_suffix(".json.tmp")
        with tmp.open("w") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        tmp.replace(DISCORD_LATEST)
        with DISCORD_HISTORY.open("a") as f:
            f.write(json.dumps(_compact(report), ensure_ascii=False) + "\n")
    except OSError:
        pass


def report() -> dict:
    now = _now_utc()
    prior = _prior()                              # read BEFORE we overwrite
    prior_cursors = (prior or {}).get("last_message_ids", {})
    first_overall = prior is None

    server = discord.get_guild_counts()

    all_new: list[dict] = []
    channels_out: list[dict] = []
    cursors: dict[str, str] = dict(prior_cursors)
    errors: list[str] = []
    baselined_channels: list[str] = []

    for ch in MONITORED:
        had_cursor = ch in prior_cursors
        if not had_cursor:
            # First sight of this channel: baseline to latest, gather no history.
            res = discord.get_channel_messages(ch, after=None, limit=1)
            if not res["ok"]:
                errors.append(f"{ch}: {res['detail']}")
                continue
            latest = res["messages"]
            cursors[ch] = latest[0]["id"] if latest else cursors.get(ch, "0")
            baselined_channels.append(ch)
            channels_out.append({"name": ch, "new": 0, "baselined": True})
            continue

        msgs, new_cursor, err = _fetch_new(ch, prior_cursors[ch])
        if err:
            errors.append(f"{ch}: {err}")
            continue
        if new_cursor:
            cursors[ch] = new_cursor
        flat = [_flatten(ch, m) for m in msgs]
        all_new.extend(flat)
        channels_out.append({"name": ch, "new": len([m for m in flat if not m["bot"]])})

    human_new = [m for m in all_new if not m["bot"]]
    issues = _derive_issues(all_new) if not first_overall else []
    authors = Counter(m["author"] for m in human_new)

    result = {
        "ok": True if not errors or len(errors) < len(MONITORED) else False,
        "checked_at": _checked_at(now),
        "baselined": first_overall or bool(baselined_channels),
        "baselined_channels": baselined_channels,
        "server": {"member_count": server.get("member_count"),
                   "online": server.get("presence_count")},
        "channels": channels_out,
        "new_messages": len(human_new),
        "active_authors": len(authors),
        "top_authors": authors.most_common(10),
        "sample": _sample(all_new),               # for the session's tone judgment
        "issues": issues,
        "any_urgent": any(i["severity"] == "urgent" for i in issues),
        "errors": errors,
        "last_message_ids": cursors,              # cursors for the next run
    }
    _save(result)
    return result


# --- renders ----------------------------------------------------------------


def render(report: dict) -> str:
    if not report.get("ok") and not report.get("channels"):
        return f"monitor_discord failed: {report.get('errors') or 'unknown'}"
    s = report.get("server", {})
    out = [f"Discord activity - {report.get('checked_at')}",
           f"  server: {s.get('member_count')} members ({s.get('online')} online)",
           f"  new member messages: {report.get('new_messages')} "
           f"from {report.get('active_authors')} author(s)", ""]
    if report.get("baselined"):
        bc = report.get("baselined_channels") or "all"
        out.append(f"  (baselined {bc} this run - no history gathered)")
    out.append("  Per channel:")
    for c in report.get("channels", []):
        tag = " [baselined]" if c.get("baselined") else ""
        out.append(f"    #{c['name']}: {c.get('new', 0)} new{tag}")
    if report.get("top_authors"):
        out.append("")
        out.append("  Most active:")
        for name, n in report["top_authors"]:
            out.append(f"    {name}: {n}")
    issues = report.get("issues", [])
    out.append("")
    if issues:
        out.append("  Flags this scan (heuristic - tone still needs a read):")
        for i in issues:
            mark = "URGENT" if i["severity"] == "urgent" else "digest"
            out.append(f"    [{mark}] {i['detail']}")
    else:
        out.append("  No heuristic flags this scan.")
    if report.get("errors"):
        out.append("")
        out.append("  Errors: " + "; ".join(report["errors"]))
    return "\n".join(out)


def render_digest(report: dict) -> str | None:
    """One digest block. Returns None on a fully quiet scan so it adds no line."""
    if not report.get("ok") and not report.get("channels"):
        return f"Discord monitor: scan failed ({report.get('errors') or 'unknown'})."
    if report.get("baselined") and not report.get("new_messages"):
        bc = report.get("baselined_channels") or "all channels"
        return f"Discord monitor: started watching {bc}."
    if not report.get("new_messages") and not report.get("issues"):
        return None
    date = (report.get("checked_at") or "")[:10]
    head = (f"Discord - {date}: {report.get('new_messages')} new msg(s) "
            f"from {report.get('active_authors')} author(s)")
    lines = [head]
    for i in report.get("issues", []):
        lines.append(f"  - [{i['severity']}] {i['detail']}")
    return "\n".join(lines)


# --- CLI --------------------------------------------------------------------


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("report", help="Poll Discord for new messages + persist (JSON)")
    sub.add_parser("show", help="Render the last persisted scan, human-readable")
    sub.add_parser("digest", help="Digest block from the last scan (empty if quiet)")
    args = ap.parse_args()
    if args.cmd == "report":
        res = report()
        print(json.dumps(res, indent=2, ensure_ascii=False))
        sys.exit(0 if res.get("ok") else 1)
    elif args.cmd == "show":
        try:
            with DISCORD_LATEST.open() as f:
                print(render(json.load(f)))
        except (OSError, json.JSONDecodeError):
            print("No scan yet - run `report` first.")
    elif args.cmd == "digest":
        try:
            with DISCORD_LATEST.open() as f:
                d = render_digest(json.load(f))
            print(d if d else "")
        except (OSError, json.JSONDecodeError):
            print("")


if __name__ == "__main__":
    main()
