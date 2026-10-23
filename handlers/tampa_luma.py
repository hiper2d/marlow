"""
tampa_luma - mirror Tampa AI Build Club Discord events to the club's Luma calendar.

Alex is an admin (not owner) of the Tampa AI Build Club Discord and of its Luma
calendar (luma.com/tampa-ai-build-club). Discord is the home: meetups are created
there first, as Discord scheduled events. This handler carries them to Luma - but
only after Alex reviews them (Alex, 2026-10-22: "create events in Discord first,
then move them to Luma after my review").

Flow, per Discord event:

    new Discord event --scan--> pending_review --approve (Alex)--> pushed
                                      |                               |
                                      +--skip--> skipped              +--Discord edited--> update_pending --approve--> pushed

`scan` never writes to Luma. Only `approve` does, and only Simona runs it, on
Alex's word. Once an event is on Luma the ops tick handles the rest:
`guests` lists registrations (the session judges pending ones and approves the
real people via `approve-guest`), `remind` posts a day-before reminder to
tampa/announcements, `recap` posts a thank-you prompt to tampa/general after it.

Luma access - no paid API. Luma's public API needs Luma Plus, so this drives the
same internal JSON API (api2.luma.com) the luma.com web app calls, from inside a
luma.com tab of Marlow's persistent-profile Chrome (port 9223, where Alex logged
in to Luma once on 2026-10-22). The tab's cookies authenticate every call.
A logged-out session comes back 401/403 -> `reauth` issue (urgent).

Everything Marlow creates on Luma shows up as Alex - there is no separate Luma
identity for the bot.

CLI:
    python handlers/tampa_luma.py report                  -> scan + guests + due posts (the tick)
    python handlers/tampa_luma.py scan                    -> Discord diff only, JSON
    python handlers/tampa_luma.py show [DISCORD_EVENT_ID] -> drafts/state, human-readable
    python handlers/tampa_luma.py approve DISCORD_EVENT_ID [--tags "A,B"] [--cover IMG] [--private] [--dry-run]
    python handlers/tampa_luma.py tags [DISCORD_EVENT_ID "A,B"]   -> list calendar tags / set an event's tags
    python handlers/tampa_luma.py cover DISCORD_EVENT_ID IMG      -> upload a cover image to a pushed event
    python handlers/tampa_luma.py skip DISCORD_EVENT_ID
    python handlers/tampa_luma.py guests                  -> registrations for pushed upcoming events
    python handlers/tampa_luma.py approve-guest LUMA_EVENT_ID RSVP_ID [--decline]
    python handlers/tampa_luma.py remind [--dry-run]      -> post due day-before reminders
    python handlers/tampa_luma.py recap [--dry-run]       -> post due after-event recaps
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from driver.env_loader import import_plist_env  # noqa: E402
import_plist_env()

from driver.budget_state import STATE_DIR  # noqa: E402
from tools import discord  # noqa: E402

GUILD_ID = discord.OTHER_GUILDS["tampa"]
CALENDAR_API_ID = "cal-2GlGmBmK9ueMPCn"
CALENDAR_URL = "https://luma.com/tampa-ai-build-club"
TZ = "America/New_York"
# Luma's create form insists on a cover + tint + font. A stock Luma gallery
# image and the calendar's own orange; Alex can swap the cover on Luma.
DEFAULT_COVER = "https://images.lumacdn.com/gallery-images/s0/61f1dcc6-641e-4070-a32e-21a23ab8aeb6.png"
TINT_COLOR = "#e8521d"
STATE_FILE = STATE_DIR / "tampa_luma.json"

REMIND_CHANNEL = "tampa/announcements"
RECAP_CHANNEL = "tampa/general"
REMIND_WINDOW_H = (12, 36)   # post the reminder when the start is 12-36h away
RECAP_WINDOW_H = (1, 48)     # post the recap 1-48h after the end
POST_HOURS_ET = (8, 21)      # local hours when reminder/recap may post

# Persistent-profile Chrome, shared with scrape_stats / substack (same port, same
# profile, so the Luma login lives next to the provider-console logins).
CDP_PORT = os.environ.get("SCRAPE_CDP_PORT", "9223")
SIMONA_DIR = os.environ.get("SIMONA_DIR", str(Path.home() / "projects/simona-ai-computer-operator"))
BROWSER_CLI = f"{SIMONA_DIR}/mcp/browser/cli.py"
START_SCRIPT = f"{SIMONA_DIR}/mcp/browser/start-chrome-persistent.sh"
LUMA_API = "https://api2.luma.com"
CLI_TIMEOUT = 60

# Discord scheduled-event status codes.
D_SCHEDULED, D_ACTIVE, D_COMPLETED, D_CANCELED = 1, 2, 3, 4


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def _parse(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def _local(ts: str) -> str:
    return _parse(ts).astimezone(ZoneInfo(TZ)).strftime("%a %b %-d, %-I:%M %p")


# ─── State ───────────────────────────────────────────────────────────────────


def _load() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"events": {}, "venues": {}}


def _save(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


# ─── Discord side ────────────────────────────────────────────────────────────


def _discord_events() -> list[dict]:
    token = discord._token()
    if not token:
        raise RuntimeError("missing DISCORD_MARLOW_TOKEN")
    r = requests.get(f"{discord.API_BASE}/guilds/{GUILD_ID}/scheduled-events",
                     params={"with_user_count": "true"},
                     headers=discord._headers(token), timeout=discord.HTTP_TIMEOUT)
    r.raise_for_status()
    return r.json()


def _discord_url(ev_id: str) -> str:
    return f"https://discord.com/events/{GUILD_ID}/{ev_id}"


def _fingerprint(ev: dict) -> str:
    """Hash of the fields that are mirrored to Luma. A change re-opens review."""
    keys = (ev.get("name"), ev.get("description"), ev.get("scheduled_start_time"),
            ev.get("scheduled_end_time"), (ev.get("entity_metadata") or {}).get("location"))
    return hashlib.sha1(json.dumps(keys).encode()).hexdigest()[:12]


def _draft(ev: dict) -> dict:
    """The Luma-side view of a Discord event - what Alex reviews."""
    start = _parse(ev["scheduled_start_time"])
    end = _parse(ev["scheduled_end_time"]) if ev.get("scheduled_end_time") else start + timedelta(hours=2)
    minutes = int((end - start).total_seconds() // 60)
    return {
        "name": ev["name"].strip(),
        "description": (ev.get("description") or "").strip(),
        "start_at": _iso(start),
        "end_at": _iso(end),
        "duration_interval": f"PT{minutes // 60}H{minutes % 60}M" if minutes % 60 else f"PT{minutes // 60}H",
        "location": ((ev.get("entity_metadata") or {}).get("location") or "").strip(),
    }


def scan(state: dict) -> dict:
    """Diff Discord events against state. Never touches Luma."""
    events = _discord_events()
    seen = set()
    needs_review, cancelled = [], []
    for ev in events:
        eid = ev["id"]
        seen.add(eid)
        rec = state["events"].get(eid)
        fp = _fingerprint(ev)
        live = {"discord_status": ev.get("status"), "interested": ev.get("user_count", 0)}
        if rec is None:
            if ev.get("status") not in (D_SCHEDULED, D_ACTIVE):
                continue
            rec = {"status": "pending_review", "fingerprint": fp, "draft": _draft(ev),
                   "discord_url": _discord_url(eid), "first_seen": _iso(_now()), **live}
            state["events"][eid] = rec
            needs_review.append(eid)
            continue
        rec.update(live)
        if ev.get("status") == D_CANCELED and rec["status"] == "pushed" and not rec.get("cancel_flagged"):
            rec["cancel_flagged"] = True
            cancelled.append(eid)
        if fp != rec["fingerprint"] and rec["status"] in ("pushed", "pending_review", "update_pending"):
            rec["fingerprint"] = fp
            rec["draft"] = _draft(ev)
            if rec["status"] == "pushed":
                rec["status"] = "update_pending"
            if eid not in needs_review:
                needs_review.append(eid)
    # A Discord event that vanished (deleted, or completed and dropped by Discord)
    for eid, rec in state["events"].items():
        if eid not in seen and rec["status"] == "pending_review":
            rec["status"] = "gone"
    return {"needs_review": needs_review, "cancelled_on_discord": cancelled}


# ─── Luma side (internal API through the logged-in Chrome tab) ───────────────


class LumaAuthError(RuntimeError):
    pass


def _chrome_up() -> bool:
    try:
        with urllib.request.urlopen(f"http://localhost:{CDP_PORT}/json/version", timeout=3):
            return True
    except OSError:
        return False


def _ensure_chrome() -> bool:
    if _chrome_up():
        return True
    subprocess.Popen(["bash", START_SCRIPT, CDP_PORT], env={**os.environ, "HEADLESS": "1"},
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    for _ in range(25):
        if _chrome_up():
            return True
        time.sleep(1)
    return False


class Luma:
    """One dedicated luma.com tab, pinned by targetId so a concurrent scrape on
    the same Chrome can't steal it. Closed on exit."""

    def __enter__(self):
        if not _ensure_chrome():
            raise RuntimeError(f"persistent Chrome not reachable on :{CDP_PORT}")
        out = self._cli("newtab", "https://luma.com/home", pinned=False)
        self.target = json.loads(out)["id"]
        # fetch() from about:blank has no luma.com origin and fails CORS - wait
        # until the tab has actually landed on luma.com.
        for _ in range(30):
            if self._js("location.hostname+' '+document.readyState") == "luma.com complete":
                return self
            time.sleep(0.5)
        self._cli("navigate", "https://luma.com/home")
        time.sleep(4)
        return self

    def __exit__(self, *exc):
        try:
            urllib.request.urlopen(f"http://localhost:{CDP_PORT}/json/close/{self.target}", timeout=3)
        except OSError:
            pass

    def _cli(self, *args: str, pinned: bool = True) -> str:
        env = {**os.environ, "CDP_PORT": CDP_PORT}
        if pinned:
            env["CDP_TARGET"] = self.target
        res = subprocess.run(["uv", "run", "--project", SIMONA_DIR, "python", BROWSER_CLI, *args],
                             capture_output=True, text=True, cwd=SIMONA_DIR, env=env, timeout=CLI_TIMEOUT)
        if res.returncode != 0:
            raise RuntimeError(f"browser cli failed: {res.stderr[:200] or res.stdout[:200]}")
        return res.stdout

    def _js(self, expr: str):
        return json.loads(self._cli("js", expr)).get("result")

    def call(self, path: str, body: dict | None = None, params: dict | None = None) -> dict:
        """fetch() from the page (the CLI can't await, so park the result on
        window and poll for it)."""
        url = f"{LUMA_API}/{path.lstrip('/')}"
        if params:
            url += "?" + urllib.parse.urlencode(params)
        opts: dict = {"credentials": "include", "method": "POST" if body is not None else "GET"}
        if body is not None:
            opts["headers"] = {"content-type": "application/json"}
            opts["body"] = json.dumps(body)
        key = f"k{time.time_ns()}"
        self._js(
            f"window.__luma=window.__luma||{{}};fetch({json.dumps(url)},{json.dumps(opts)})"
            f".then(r=>r.text().then(t=>window.__luma['{key}']=JSON.stringify({{s:r.status,t}})))"
            f".catch(e=>window.__luma['{key}']=JSON.stringify({{s:0,t:String(e)}}));1"
        )
        for _ in range(60):
            raw = self._js(f"window.__luma['{key}']||''")
            if raw:
                res = json.loads(raw)
                if res["s"] in (401, 403):
                    raise LumaAuthError(f"Luma session rejected ({res['s']}) - log in again in the :{CDP_PORT} Chrome")
                if res["s"] != 200:
                    raise RuntimeError(f"luma {path} -> {res['s']}: {res['t'][:300]}")
                return json.loads(res["t"]) if res["t"] else {}
            time.sleep(0.5)
        raise RuntimeError(f"luma {path} timed out")



def _doc(text: str) -> dict:
    """Plain text -> Luma's description document (ProseMirror-style 'Spark' doc)."""
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    content = []
    for p in paras:
        lines = p.split("\n")
        nodes: list = []
        for i, line in enumerate(lines):
            if i:
                nodes.append({"type": "hard_break"})
            if line:
                nodes.append({"type": "text", "text": line})
        content.append({"type": "paragraph", "content": nodes})
    return {"type": "doc", "content": content or [{"type": "paragraph"}]}


def _location_fields(state: dict, location: str) -> dict:
    """A venue Alex pinned on Luma once (Google place) is reused by address;
    otherwise send a manual address, which Luma shows as 'Custom Address'."""
    if not location:
        return {"location_type": "missing", "geo_address_json": None}
    venue = state["venues"].get(location)
    if venue:
        return {"location_type": "offline", "geo_address_json": venue["geo_address_json"],
                "coordinate": venue.get("coordinate")}
    return {"location_type": "offline", "geo_address_json": {"type": "manual", "address": location}}


def _learn_venue(state: dict, location: str, luma_event: dict) -> None:
    geo = luma_event.get("geo_address_json")
    if location and geo and geo.get("type") == "google":
        state["venues"][location] = {"geo_address_json": geo, "coordinate": luma_event.get("coordinate")}


# ─── Calendar tags + cover image ─────────────────────────────────────────────
# Tags are the calendar's own labels (filter chips on the club page), not Luma's
# Discover categories - Luma assigns those itself (the meetup landed in "AI").
# They attach to the calendar-event link (`calev-...`), not the `evt-...` id.

TAG_COLORS = ["purple", "blue", "green", "orange", "cranberry", "yellow", "barney", "red"]


def calendar_tags(luma: "Luma") -> list[dict]:
    res = luma.call("calendar/admin/get", params={"calendar_api_id": CALENDAR_API_ID})
    return [{"api_id": t["api_id"], "name": t["name"], "color": t.get("color")} for t in res.get("event_tags", [])]


def _calev_id(luma: "Luma", rec: dict) -> str:
    if rec.get("luma_calev_id"):
        return rec["luma_calev_id"]
    for period in ("future", "past"):
        page = luma.call("calendar/admin/get-events",
                         params={"calendar_api_id": CALENDAR_API_ID, "period": period, "pagination_limit": 50})
        for e in page.get("entries", []):
            if e.get("event", {}).get("api_id") == rec["luma_api_id"]:
                rec["luma_calev_id"] = e["api_id"]
                return e["api_id"]
    raise RuntimeError(f"{rec['luma_api_id']} not found on the calendar")


def set_tags(luma: "Luma", rec: dict, names: list[str]) -> list[str]:
    """Make the event's tags exactly `names`, creating missing calendar tags."""
    calev = _calev_id(luma, rec)
    existing = {t["name"].lower(): t for t in calendar_tags(luma)}
    current = set(rec.get("tags", []))
    base = {"entity_type": "calendar_event", "owner_api_id": CALENDAR_API_ID, "owner_type": "calendar"}
    for name in names:
        t = existing.get(name.lower())
        if t is None:
            color = TAG_COLORS[len(existing) % len(TAG_COLORS)]
            res = luma.call("tag/create", {**base, "name": name, "color": color, "entity_api_ids": [calev]})
            existing[name.lower()] = {"api_id": res.get("tag_api_id"), "name": name}
        elif name not in current:
            luma.call("tag/apply", {"tag_api_id": t["api_id"], "entity_api_ids": [calev]})
    for name in current - set(names):
        t = existing.get(name.lower())
        if t:
            luma.call("tag/unapply", {"tag_api_id": t["api_id"], "entity_api_ids": [calev]})
    rec["tags"] = list(names)
    return rec["tags"]


def set_cover(luma: "Luma", rec: dict, image: Path) -> str:
    """Luma's own upload path: presigned S3 URL -> PUT the file -> cover_url."""
    ctype = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}[image.suffix.lower()]
    up = luma.call("cdn/create-presigned-url", {"content_type": ctype})
    r = requests.put(up["upload_url"], data=image.read_bytes(), headers={"Content-Type": ctype}, timeout=60)
    r.raise_for_status()
    luma.call("event/admin/update", {"event_api_id": rec["luma_api_id"], "cover_url": up["file_url"]})
    rec["cover_url"] = up["file_url"]
    return up["file_url"]


def approve(state: dict, eid: str, private: bool = False, dry_run: bool = False,
            tags: list[str] | None = None, cover: Path | None = None) -> dict:
    rec = state["events"].get(eid)
    if not rec:
        return {"ok": False, "error": f"unknown Discord event {eid} - run scan first"}
    if rec["status"] not in ("pending_review", "update_pending"):
        return {"ok": False, "error": f"event is {rec['status']}, nothing to approve"}
    d = rec["draft"]
    fields = {
        "name": d["name"],
        "start_at": d["start_at"],
        "duration_interval": d["duration_interval"],
        "timezone": TZ,
        "description_mirror": _doc(d["description"]),
        **_location_fields(state, d["location"]),
    }
    if dry_run:
        return {"ok": True, "dry_run": True, "mode": "update" if rec.get("luma_api_id") else "create",
                "payload": fields, "tags": tags, "cover": str(cover) if cover else None}
    with Luma() as luma:
        if rec.get("luma_api_id"):
            # Keep a Google pin Alex set by hand on Luma if the address didn't change.
            cur = luma.call("event/admin/get", params={"event_api_id": rec["luma_api_id"]}).get("event", {})
            if (cur.get("geo_address_json") or {}).get("type") == "google" and rec.get("pushed_location") == d["location"]:
                fields.pop("geo_address_json", None)
                fields.pop("location_type", None)
                fields.pop("coordinate", None)
            res = luma.call("event/admin/update", {"event_api_id": rec["luma_api_id"], **fields})
            ev = res.get("event", {})
        else:
            # Mirrors the body luma.com/create's own form sends (captured
            # 2026-10-22); a body missing cover_url/tint_color/font_title -> 400.
            body = {
                "meeting_url": "", "zoom_meeting_id": "", "zoom_meeting_password": "",
                "zoom_session_type": None, "meeting_creation_method": None, "coordinate": None,
                **fields,
                "calendar_api_id": CALENDAR_API_ID,
                "calendar_to_submit_to_api_id": None,
                "grant_manage_access": False,
                "_calendar_requires_manage_access": False,
                "supports_members_only": False,
                "visibility": "private" if private else "public",
                "geo_address_visibility": "public",
                "max_capacity": None,
                "waitlist_status": "disabled",
                "theme_meta": {"theme": "legacy"},
                "cover_url": DEFAULT_COVER,
                "tint_color": TINT_COLOR,
                "font_title": "new-spirit",
                "ticket_types": [{"type": "free", "currency": None, "cents": None, "is_flexible": False,
                                  "min_cents": None, "require_approval": False,
                                  "ethereum_token_requirements": [], "is_hidden": False}],
            }
            ev = luma.call("event/create", body)
            ev = ev.get("event", ev)
            rec["luma_api_id"] = ev.get("api_id")
        if ev.get("url"):
            rec["luma_url"] = f"https://luma.com/{ev['url']}"
        if tags is not None:
            set_tags(luma, rec, tags)
        if cover:
            set_cover(luma, rec, cover)
    rec["status"] = "pushed"
    rec["pushed_at"] = _iso(_now())
    rec["pushed_location"] = d["location"]
    rec["start_at"], rec["end_at"] = d["start_at"], d["end_at"]
    return {"ok": True, "luma_api_id": rec.get("luma_api_id"), "luma_url": rec.get("luma_url"),
            "tags": rec.get("tags", []), "cover_url": rec.get("cover_url")}


def guests(state: dict, luma: Luma) -> list[dict]:
    """Registrations for every pushed event that hasn't ended. Pending ones are
    returned in full so the session can judge them."""
    out = []
    for eid, rec in state["events"].items():
        if rec["status"] not in ("pushed", "update_pending") or not rec.get("luma_api_id"):
            continue
        if _parse(rec["end_at"]) < _now() - timedelta(hours=RECAP_WINDOW_H[1]):
            continue
        entries, cursor = [], None
        while True:
            params = {"event_api_id": rec["luma_api_id"], "pagination_limit": 100}
            if cursor:
                params["pagination_cursor"] = cursor
            page = luma.call("event/admin/get-guests", params=params)
            entries += page.get("entries", [])
            cursor = page.get("next_cursor")
            if not page.get("has_more") or not cursor:
                break
        counts: dict = {}
        for g in entries:
            counts[g.get("approval_status")] = counts.get(g.get("approval_status"), 0) + 1
        checked_in = sum(1 for g in entries if g.get("checked_in_at"))
        pending = [{"rsvp_api_id": g.get("api_id"), "name": g.get("name"), "email": g.get("email"),
                    "registered_at": g.get("registered_at") or g.get("created_at"),
                    "answers": g.get("registration_answers")}
                   for g in entries if g.get("approval_status") == "pending_approval"]
        # Cheap way to learn a Google pin Alex set on Luma.
        try:
            cur = luma.call("event/admin/get", params={"event_api_id": rec["luma_api_id"]}).get("event", {})
            _learn_venue(state, rec["draft"]["location"], cur)
        except RuntimeError:
            pass
        rec["guest_counts"], rec["checked_in"] = counts, checked_in
        out.append({"discord_event_id": eid, "name": rec["draft"]["name"], "start": _local(rec["start_at"]),
                    "luma_api_id": rec["luma_api_id"], "luma_url": rec.get("luma_url"),
                    "going": counts.get("approved", 0), "pending": pending,
                    "waitlist": counts.get("waitlist", 0), "declined": counts.get("declined", 0),
                    "checked_in": checked_in, "discord_interested": rec.get("interested", 0)})
    return out


def approve_guest(luma_event: str, rsvp: str, decline: bool = False) -> dict:
    with Luma() as luma:
        luma.call("event/admin/update-guest-status", {
            "event_api_id": luma_event, "rsvp_api_id": rsvp, "suppress_email": False,
            "custom_message": {"type": "doc", "content": [{"type": "paragraph"}]},
            "approval_status": "declined" if decline else "approved",
            "should_refund": False, **({} if decline else {"event_ticket_type_api_id": None}),
        })
    return {"ok": True, "rsvp_api_id": rsvp, "status": "declined" if decline else "approved"}


# ─── Reminder / recap posts ──────────────────────────────────────────────────
# Fixed templates. Alex approved the wording 2026-10-22; change it here, not in the tick.


def _reminder_text(rec: dict) -> str:
    d = rec["draft"]
    when = _parse(d["start_at"]).astimezone(ZoneInfo(TZ)).strftime("%A %-I:%M %p")
    lines = [f"**Tomorrow: {d['name']}** - {when}"]
    if d["location"]:
        lines.append(f"Where: {d['location']}")
    lines.append(f"RSVP on Luma: {rec['luma_url']}")
    lines.append(f"Discord event: {rec['discord_url']}")
    lines.append("Bring your laptop and whatever you're building.")
    return "\n".join(lines)


def _recap_text(rec: dict) -> str:
    n = rec.get("checked_in") or 0
    who = f"the {n} of you who came" if n > 1 else "everyone who came"
    return (f"Thanks to {who} to **{rec['draft']['name']}**! "
            "What did you build or learn? Drop a screenshot, a repo, or one line here.\n"
            f"Next meetups: {CALENDAR_URL}")


def _due(rec: dict, kind: str) -> bool:
    if rec["status"] != "pushed" or rec.get(f"{kind}_message_id") or rec.get("discord_status") == D_CANCELED:
        return False
    now = _now()
    # Nobody wants a 2:30 AM ping: posts only go out in daytime ET. Both windows
    # are wide enough that a 6h tick always lands inside one in daytime.
    if not POST_HOURS_ET[0] <= now.astimezone(ZoneInfo(TZ)).hour < POST_HOURS_ET[1]:
        return False
    if kind == "remind":
        h = (_parse(rec["start_at"]) - now).total_seconds() / 3600
        return REMIND_WINDOW_H[0] <= h <= REMIND_WINDOW_H[1]
    h = (now - _parse(rec["end_at"])).total_seconds() / 3600
    return RECAP_WINDOW_H[0] <= h <= RECAP_WINDOW_H[1]


def post_due(state: dict, kind: str, dry_run: bool = False) -> list[dict]:
    out = []
    for eid, rec in state["events"].items():
        if not _due(rec, kind):
            continue
        text = _reminder_text(rec) if kind == "remind" else _recap_text(rec)
        channel = REMIND_CHANNEL if kind == "remind" else RECAP_CHANNEL
        if dry_run:
            out.append({"discord_event_id": eid, "channel": channel, "text": text, "dry_run": True})
            continue
        r = discord.post_message(channel, content=text)
        if r.get("ok"):
            rec[f"{kind}_message_id"] = r["message_id"]
        out.append({"discord_event_id": eid, "channel": channel, "ok": r.get("ok"), "detail": r.get("detail")})
    return out


# ─── Report (the tick) ───────────────────────────────────────────────────────


def _render(eid: str, rec: dict) -> str:
    d = rec["draft"]
    lines = [f"[{rec['status']}] {d['name']}  (discord {eid})",
             f"  when:  {_local(d['start_at'])} - {_parse(d['end_at']).astimezone(ZoneInfo(TZ)).strftime('%-I:%M %p')} ET ({d['duration_interval']})",
             f"  where: {d['location'] or '(none)'}" + ("  [pinned venue]" if d["location"] in _load()["venues"] else ""),
             f"  description: {d['description'] or '(none)'}",
             f"  discord: {rec['discord_url']}  interested: {rec.get('interested', 0)}"]
    if rec.get("luma_url"):
        lines.append(f"  luma: {rec['luma_url']}  guests: {rec.get('guest_counts', {})}")
    return "\n".join(lines)


def report() -> dict:
    state = _load()
    result: dict = {"ok": True, "issues": []}
    try:
        result.update(scan(state))
    except (requests.RequestException, RuntimeError) as e:
        _save(state)
        return {"ok": False, "issues": [{"severity": "urgent", "kind": "discord", "detail": str(e)}]}
    result["review_drafts"] = {eid: _render(eid, state["events"][eid]) for eid in result["needs_review"]}
    if any(r["status"] in ("pushed", "update_pending") for r in state["events"].values()):
        try:
            with Luma() as luma:
                result["guests"] = guests(state, luma)
                result["calendar_tags"] = [t["name"] for t in calendar_tags(luma)]
        except LumaAuthError as e:
            result["issues"].append({"severity": "urgent", "kind": "reauth", "detail": str(e)})
        except RuntimeError as e:
            result["issues"].append({"severity": "digest", "kind": "luma", "detail": str(e)})
    result["reminders"] = post_due(state, "remind")
    result["recaps"] = post_due(state, "recap")
    result["checked_at"] = _iso(_now())
    _save(state)
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("report")
    sub.add_parser("scan")
    p = sub.add_parser("show"); p.add_argument("eid", nargs="?")
    p = sub.add_parser("approve"); p.add_argument("eid"); p.add_argument("--private", action="store_true"); p.add_argument("--dry-run", action="store_true")
    p.add_argument("--tags", help="comma-separated calendar tags, e.g. 'Vibe Coding'"); p.add_argument("--cover", type=Path)
    p = sub.add_parser("tags"); p.add_argument("eid", nargs="?"); p.add_argument("names", nargs="?", help="comma-separated; omit to list calendar tags")
    p = sub.add_parser("cover"); p.add_argument("eid"); p.add_argument("image", type=Path)
    p = sub.add_parser("skip"); p.add_argument("eid")
    sub.add_parser("guests")
    p = sub.add_parser("approve-guest"); p.add_argument("luma_event"); p.add_argument("rsvp"); p.add_argument("--decline", action="store_true")
    for k in ("remind", "recap"):
        p = sub.add_parser(k); p.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if a.cmd == "report":
        out = report()
    elif a.cmd == "scan":
        state = _load(); out = scan(state); _save(state)
    elif a.cmd == "show":
        state = _load()
        recs = {a.eid: state["events"][a.eid]} if a.eid else state["events"]
        print("\n\n".join(_render(k, v) for k, v in recs.items()) or "(no events tracked)")
        return
    elif a.cmd == "approve":
        state = _load()
        try:
            tags = [t.strip() for t in a.tags.split(",") if t.strip()] if a.tags is not None else None
            out = approve(state, a.eid, private=a.private, dry_run=a.dry_run, tags=tags, cover=a.cover)
        except LumaAuthError as e:
            out = {"ok": False, "kind": "reauth", "error": str(e)}
        except RuntimeError as e:
            out = {"ok": False, "error": str(e)}
        if not a.dry_run:
            _save(state)
    elif a.cmd == "skip":
        state = _load()
        state["events"][a.eid]["status"] = "skipped"; _save(state)
        out = {"ok": True, "skipped": a.eid}
    elif a.cmd == "guests":
        state = _load()
        with Luma() as luma:
            out = {"ok": True, "guests": guests(state, luma)}
        _save(state)
    elif a.cmd in ("tags", "cover"):
        state = _load()
        with Luma() as luma:
            if a.cmd == "tags" and not a.names:
                out = {"ok": True, "calendar_tags": calendar_tags(luma)}
            elif a.cmd == "tags":
                out = {"ok": True, "tags": set_tags(luma, state["events"][a.eid], [t.strip() for t in a.names.split(",") if t.strip()])}
            else:
                out = {"ok": True, "cover_url": set_cover(luma, state["events"][a.eid], a.image)}
        _save(state)
    elif a.cmd == "approve-guest":
        out = approve_guest(a.luma_event, a.rsvp, decline=a.decline)
    else:
        state = _load(); out = {"ok": True, "posts": post_due(state, a.cmd, dry_run=a.dry_run)}
        if not a.dry_run:
            _save(state)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
