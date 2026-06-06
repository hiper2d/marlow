"""
substack — browser-driven Substack engagement for the substack_growth task.

Mechanical half only. Driving is delegated to simona's browser CLI on the
persistent-profile Chrome (CDP_PORT 9223 — the same logged-in profile
scrape_stats uses; Alex logs into Substack there once and the session is reused
every tick). When the session lapses, session-check / scan / post surface a
`reauth` signal instead of acting, and Marlow's session pings Alex urgently.

This handler does NOT decide what to say or which threads matter — that judgment
(AI-audience? comment-worthy? welcome vs substantive?) lives in Marlow's session
reading the scan output. Here we only:

  session-check                 → is the Substack session alive?
  scan --url <u> --scrolls N    → pull candidate notes (permalink, author, text)
  post --note-url <u> --text-file <p>   → post one reply, verify it landed

CLI:
    python handlers/substack.py ensure-chrome
    python handlers/substack.py session-check
    python handlers/substack.py scan --url https://substack.com/home --scrolls 4
    python handlers/substack.py post --note-url <url> --text-file /tmp/c.txt

For local testing against the browser-skill profile instead of the persistent
one, set SUBSTACK_CDP_PORT=9222.
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
from driver.env_loader import import_plist_env  # noqa: E402
import_plist_env()

from tools import substack_store as store  # noqa: E402

CONFIG_PATH = REPO_ROOT / "projects" / "blog" / "substack" / "config.yaml"


def _config() -> dict:
    try:
        return yaml.safe_load(CONFIG_PATH.read_text()) or {}
    except (OSError, ValueError):
        return {}


def _caps() -> tuple[int, int]:
    """(welcomes_per_day, comment_drafts_per_day) from config; safe defaults."""
    caps = _config().get("caps", {})
    try:
        return int(caps.get("welcomes_per_day", 3)), int(caps.get("comment_drafts_per_day", 5))
    except (ValueError, TypeError):
        return 3, 5

# Same persistent profile as scrape_stats (9223); override for local tests.
CDP_PORT = os.environ.get("SUBSTACK_CDP_PORT") or os.environ.get("SCRAPE_CDP_PORT", "9223")
SIMONA_DIR = os.environ.get("SIMONA_DIR", str(Path.home() / "projects/simona-ai-computer-operator"))
BROWSER_CLI = f"{SIMONA_DIR}/mcp/browser/cli.py"
START_SCRIPT = f"{SIMONA_DIR}/mcp/browser/start-chrome-persistent.sh"

NAV_SETTLE_S = 4.0
ACT_SETTLE_S = 2.0
HTTP_TIMEOUT = 90


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


# ─── Chrome plumbing (delegate to simona's CLI on CDP_PORT) ──────────────────

def _chrome_up() -> bool:
    try:
        with urllib.request.urlopen(f"http://localhost:{CDP_PORT}/json/version", timeout=3):
            return True
    except OSError:
        return False


def ensure_chrome(headless: bool = True, wait_s: int = 25) -> bool:
    if _chrome_up():
        return True
    env = {**os.environ, "HEADLESS": "1" if headless else "0"}
    subprocess.Popen(
        ["bash", START_SCRIPT, CDP_PORT],
        env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    for _ in range(wait_s):
        if _chrome_up():
            return True
        time.sleep(1)
    return False


def _cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["uv", "run", "--project", SIMONA_DIR, "python", BROWSER_CLI, *args],
        capture_output=True, text=True, cwd=SIMONA_DIR,
        env={**os.environ, "CDP_PORT": CDP_PORT}, timeout=HTTP_TIMEOUT,
    )


def _navigate(url: str) -> bool:
    return _cli("navigate", url, "--tab", "0").returncode == 0


def _raw_js(expr: str) -> str | None:
    """Run JS, return the raw .result value (a string), or None on failure."""
    res = _cli("js", expr, "--tab", "0")
    if res.returncode != 0:
        return None
    try:
        return json.loads(res.stdout).get("result")
    except (json.JSONDecodeError, AttributeError):
        return None


def _json_js(expr: str) -> dict | list | None:
    """Run JS that returns a JSON string; parse it."""
    raw = _raw_js(expr)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None


# ─── session-check ───────────────────────────────────────────────────────────

# When logged in, /home renders the Notes feed (composer "What's on your mind?").
# Logged out, Substack shows a marketing / sign-in page.
_SESSION_JS = r"""(()=>{
  const t=(document.body.innerText||'');
  const loggedIn=/What's on your mind/i.test(t) || !!document.querySelector('textarea, [contenteditable="true"]');
  const wall=/\bSign in\b|\bLog in\b|Create your account|Start writing/i.test(t) && !loggedIn;
  return JSON.stringify({logged_in:!!loggedIn, login_wall:!!wall, url:location.href});
})()"""


def session_check() -> dict:
    if not ensure_chrome(headless=True):
        return {"ok": False, "kind": "chrome_down", "detail": f"persistent Chrome not reachable on :{CDP_PORT}", "checked_at": _now_iso()}
    if not _navigate("https://substack.com/home"):
        return {"ok": False, "kind": "nav_failed", "detail": "could not navigate to substack home", "checked_at": _now_iso()}
    time.sleep(NAV_SETTLE_S)
    res = _json_js(_SESSION_JS)
    if res is None:
        return {"ok": False, "kind": "parse_failed", "detail": "session probe returned nothing", "checked_at": _now_iso()}
    if not res.get("logged_in"):
        return {"ok": False, "kind": "reauth", "detail": "Substack session expired — log in once in the persistent Chrome profile (port %s)" % CDP_PORT,
                "url": res.get("url"), "checked_at": _now_iso()}
    return {"ok": True, "logged_in": True, "url": res.get("url"), "checked_at": _now_iso()}


# ─── scan ──────────────────────────────────────────────────────────────────

# Walk every note permalink on the page, climb to its container, grab author
# handle + a text snippet. Rough but enough for Marlow's session to classify.
_SCAN_JS = r"""(()=>{
  const out=[]; const seen=new Set();
  for(const a of document.querySelectorAll('a[href*="/note/c-"]')){
    const m=a.href.match(/\/note\/(c-\d+)/); if(!m) continue;
    const id=m[1]; if(seen.has(id)) continue; seen.add(id);
    let box=a;
    for(let i=0;i<6 && box.parentElement;i++){ box=box.parentElement; if((box.innerText||'').length>140) break; }
    const text=(box.innerText||'').replace(/\s+/g,' ').trim();
    const ah=box.querySelector('a[href*="/@"]');
    const handle = ah ? ((ah.getAttribute('href')||'').match(/@([^/?]+)/)||[])[1] : null;
    out.push({note_id:id, note_url:a.href.split('?')[0], author_handle:handle, snippet:text.slice(0,400)});
  }
  return JSON.stringify(out.slice(0,80));
})()"""


def scan(url: str, scrolls: int = 4, include_engaged: bool = False) -> dict:
    if not ensure_chrome(headless=True):
        return {"ok": False, "kind": "chrome_down", "detail": f"Chrome not reachable on :{CDP_PORT}"}
    if not _navigate(url):
        return {"ok": False, "kind": "nav_failed", "detail": f"navigate failed: {url}"}
    time.sleep(NAV_SETTLE_S)
    for _ in range(max(0, scrolls)):
        _cli("scroll", "--direction", "down", "--amount", "1600", "--tab", "0")
        time.sleep(1.2)
    notes = _json_js(_SCAN_JS)
    if notes is None:
        # could be a login wall
        sess = _json_js(_SESSION_JS) or {}
        if sess.get("login_wall") or not sess.get("logged_in"):
            return {"ok": False, "kind": "reauth", "detail": "session expired during scan"}
        return {"ok": False, "kind": "parse_failed", "detail": "scan extractor returned nothing"}
    # Never surface authors on the do-not-engage list (existing subscribers etc.).
    notes = [n for n in notes if not store.is_blocked(n.get("author_handle"))]
    if not include_engaged:
        notes = [n for n in notes if not store.is_engaged(n["note_id"])]
    return {"ok": True, "url": url, "count": len(notes), "candidates": notes, "scanned_at": _now_iso()}


# ─── subscribers (do-not-engage source) ──────────────────────────────────────

# Pull every email off the publisher subscriber dashboard. Substack keys this list
# on email only (no handle/display name), so the *matching* of a subscriber to a
# Notes author is left to Marlow's session (fuzzy: email local-part vs handle/name).
# NOTE: reads only the first page — fine while the list is small; revisit at scale.
_SUBS_JS = r"""(()=>{
  const set=new Set();
  for(const m of (document.body.innerText||'').matchAll(/[\w.+-]+@[\w.-]+\.\w+/g)) set.add(m[0].toLowerCase());
  return JSON.stringify([...set]);
})()"""


def subscribers() -> dict:
    pub = (_config().get("publication_url") or "").rstrip("/")
    if not pub:
        return {"ok": False, "detail": "no publication_url in config"}
    if not ensure_chrome(headless=True):
        return {"ok": False, "kind": "chrome_down", "detail": f"Chrome not reachable on :{CDP_PORT}"}
    if not _navigate(pub + "/publish/subscribers"):
        return {"ok": False, "kind": "nav_failed", "detail": "navigate to subscribers dashboard failed"}
    time.sleep(NAV_SETTLE_S)
    emails = _json_js(_SUBS_JS)
    if emails is None:
        return {"ok": False, "kind": "reauth", "detail": "subscribers page unreadable — session may have expired"}
    return {"ok": True, "count": len(emails), "emails": emails, "checked_at": _now_iso()}


# ─── post ──────────────────────────────────────────────────────────────────

_URL_RE = re.compile(r"(https?://[^\s<]+)")


def _text_to_html(text: str) -> str:
    """Escape, turn bare URLs into anchors, wrap in a paragraph. The pasted
    anchor is what Substack expands into a rich preview card."""
    escaped = html.escape(text.strip())
    linked = _URL_RE.sub(lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>', escaped)
    return f"<p>{linked}</p>"


_OPEN_REPLY_JS = r"""(()=>{const b=[...document.querySelectorAll('button')].find(x=>/leave a reply/i.test(x.textContent||'')); if(b){b.click(); return 'opened';} return 'no-reply-trigger';})()"""

_CLICK_POST_JS = r"""(()=>{const b=[...document.querySelectorAll('button')].find(x=>(x.textContent||'').trim()==='Post'&&!x.disabled); if(b){b.click(); return 'posted';} return 'no-post-button';})()"""

# NOTE on like/follow/subscribe (decided 2026-06-01): the gesture is the COMMENT
# ONLY. Note permalink pages are feeds (target note + more notes below), so the
# like button and author affordance can't be hit reliably by selector or
# coordinate — attempts kept landing on the wrong card and NAVIGATING away on
# Alex's live account (.click() doesn't register a like; trusted coordinate clicks
# hit neighboring note cards / link-preview cards). Substack also no longer gives a
# note's author a plain "Follow" — only "Subscribe" (the mailing list Alex doesn't
# want); the page's "Follow" buttons are sidebar suggestions. Too fragile + risky
# to automate, and secondary to the comment. Alex likes/subscribes by hand.


def _paste_js(b64_html: str) -> str:
    # CRITICAL: select all existing content first so the paste REPLACES it. The
    # persistent Chrome profile restores Substack's auto-saved note-reply drafts
    # into the composer on open; without this, the paste APPENDS to the leftover
    # draft, producing a doubled/malformed ProseMirror doc whose "Post" silently
    # no-ops. (Diagnosed 2026-06-01: every failed 9223 post had a restored draft;
    # a clean composer posts fine.) A paste over a selection replaces it.
    return (
        "(function(){var ed=document.querySelector('[contenteditable=\"true\"]');"
        "if(!ed){return 'no-editor';}ed.focus();"
        "var sel=window.getSelection();sel.removeAllRanges();"
        "var r=document.createRange();r.selectNodeContents(ed);sel.addRange(r);"
        "var html=decodeURIComponent(escape(atob('" + b64_html + "')));"
        "var dt=new DataTransfer();dt.setData('text/html',html);"
        "dt.setData('text/plain',html.replace(/<[^>]+>/g,''));"
        "ed.dispatchEvent(new ClipboardEvent('paste',{clipboardData:dt,bubbles:true,cancelable:true}));"
        "return (ed.innerText||'').slice(0,80);})()"
    )


def post(note_url: str, text: str, kind: str = "comment", enforce_caps: bool = True) -> dict:
    """Post one reply to a note. kind: 'welcome' | 'comment' (for counters).
    Verifies the comment landed by reloading and matching a distinctive snippet."""
    note_id = (re.search(r"/note/(c-\d+)", note_url) or [None, None])[1]
    base = {"note_url": note_url, "note_id": note_id, "kind": kind, "posted_at": _now_iso()}

    # Em/en dashes are an AI tell — always post plain hyphens (Alex's rule). Applied
    # to the raw text so the verification probe below matches what actually posts.
    text = text.replace("—", "-").replace("–", "-")

    if note_id and store.is_engaged(note_id):
        return {**base, "ok": False, "kind_err": "already_engaged", "detail": "already commented on this note"}

    # A welcome is a one-time hello. Never welcome the same person twice (it reads
    # as botted). Plain comments are NOT gated this way — re-commenting on someone
    # across different threads is fine and stays a per-note (is_engaged) check only.
    handle = ((re.search(r"/@([^/?]+)", note_url) or [None, None])[1] or "").strip()
    if kind == "welcome" and handle and store.is_welcomed(handle):
        return {**base, "ok": False, "kind_err": "already_welcomed", "detail": f"already welcomed @{handle}"}

    if enforce_caps and kind == "welcome":
        wcap, _ = _caps()
        if store.counters_today().get("welcomes", 0) >= wcap:
            return {**base, "ok": False, "kind_err": "cap_reached", "detail": f"daily welcome cap ({wcap}) reached"}

    if not ensure_chrome(headless=True):
        return {**base, "ok": False, "kind_err": "chrome_down", "detail": f"Chrome not reachable on :{CDP_PORT}"}
    if not _navigate(note_url):
        return {**base, "ok": False, "kind_err": "nav_failed", "detail": "navigate to note failed"}
    time.sleep(NAV_SETTLE_S)

    # Bail if the session lapsed.
    sess = _json_js(_SESSION_JS) or {}
    if sess.get("login_wall"):
        return {**base, "ok": False, "kind_err": "reauth", "detail": "session expired"}

    opened = _raw_js(_OPEN_REPLY_JS)
    time.sleep(ACT_SETTLE_S)

    b64 = base64.b64encode(_text_to_html(text).encode()).decode()
    pasted = _raw_js(_paste_js(b64))
    if pasted in (None, "no-editor"):
        return {**base, "ok": False, "kind_err": "no_editor", "detail": f"composer not found (open={opened})"}
    time.sleep(ACT_SETTLE_S)

    clicked = _raw_js(_CLICK_POST_JS)
    if clicked != "posted":
        return {**base, "ok": False, "kind_err": "no_post_button", "detail": f"could not click Post (got {clicked})"}
    time.sleep(NAV_SETTLE_S)

    # The gesture is the COMMENT only. Like + subscribe/follow were dropped from
    # automation (2026-06-01): note permalink pages are feeds, so the like/follow
    # targets can't be hit reliably by selector or coordinate without risking a
    # misclick that navigates away on Alex's live account. Alex likes/subscribes by
    # hand for anyone worth it. We parse the author handle from the URL (no page
    # interaction); on a welcome we record it so we never re-welcome the same person,
    # but a comment leaves the handle free to surface again on other threads.
    time.sleep(0.8)

    # Verify: reload, check a distinctive chunk of the text is present.
    probe = re.sub(r"https?://\S+", "", text).strip()
    probe = (probe[:40] or text[:40]).strip()
    _navigate(note_url)
    time.sleep(NAV_SETTLE_S)
    body = _raw_js("document.body.innerText") or ""
    verified = probe[:30] in body

    # Track a WELCOME by handle so we never welcome this person again. A plain
    # comment records nothing at the handle level — only the note id below — so the
    # same person can be commented on again on other threads. (Was: block(handle)
    # for every post, which buried every commenter in do_not_engage forever.)
    if kind == "welcome" and handle:
        store.mark_welcomed(handle)
    if note_id:
        store.mark_engaged(note_id)
    store.incr_counter("welcomes" if kind == "welcome" else "comments")

    return {**base, "ok": True, "verified": verified, "handle": handle,
            "detail": "posted (verified)" if verified else "posted but verification probe not found — check manually"}


# ─── post_note (original Note, for the news-crosspost flow) ──────────────────
#
# Different from post() above (which REPLIES to someone else's note). This posts
# an ORIGINAL Note to Alex's own feed — the fast cross-post format. Proven by
# hand 2026-06-04; the two gotchas it encodes:
#   * "What's on your mind?" is a <button> that needs a TRUSTED click — .click()
#     is a silent no-op on it. Click its rect via CDP, then the inline
#     [contenteditable] editor appears.
#   * A bare URL on its own paragraph auto-links into a clickable note link, so
#     put the article link as the last paragraph of the text.

def _text_to_html_note(text: str) -> str:
    """One <p> per paragraph (blank-line separated), bare URLs anchored. Multi-
    paragraph notes need real paragraph breaks, unlike the single-<p> reply."""
    out = []
    for para in text.strip().split("\n\n"):
        escaped = html.escape(para.strip())
        linked = _URL_RE.sub(lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>', escaped)
        out.append(f"<p>{linked}</p>")
    return "".join(out)


_COMPOSER_RECT_JS = r"""(()=>{const b=[...document.querySelectorAll('button')].find(x=>(x.textContent||'').trim()==="What's on your mind?");if(!b)return JSON.stringify({found:false});b.scrollIntoView({block:'center'});const r=b.getBoundingClientRect();return JSON.stringify({found:true,x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)});})()"""


def post_note(text: str) -> dict:
    """Post an original Note to Alex's own Substack feed. Verifies + resolves the
    note permalink from the profile /notes page afterward."""
    text = text.replace("—", "-").replace("–", "-").strip()
    base = {"posted_at": _now_iso(), "kind": "note"}
    if not ensure_chrome(headless=True):
        return {**base, "ok": False, "kind_err": "chrome_down", "detail": f"Chrome not reachable on :{CDP_PORT}"}
    _cli("viewport", "1280x1600", "--scale", "1")
    if not _navigate("https://substack.com/home"):
        return {**base, "ok": False, "kind_err": "nav_failed", "detail": "navigate to home failed"}
    time.sleep(NAV_SETTLE_S)
    sess = _json_js(_SESSION_JS) or {}
    if sess.get("login_wall") or not sess.get("logged_in"):
        return {**base, "ok": False, "kind_err": "reauth", "detail": "Substack session expired"}

    rect = _json_js(_COMPOSER_RECT_JS)
    if not isinstance(rect, dict) or not rect.get("found"):
        return {**base, "ok": False, "kind_err": "no_composer", "detail": "composer button not found"}
    _trusted_click(rect["x"], rect["y"])
    time.sleep(ACT_SETTLE_S)

    b64 = base64.b64encode(_text_to_html_note(text).encode()).decode()
    pasted = _raw_js(_paste_js(b64))
    if pasted in (None, "no-editor"):
        return {**base, "ok": False, "kind_err": "no_editor", "detail": "note editor not found after opening composer"}
    time.sleep(ACT_SETTLE_S)

    clicked = _raw_js(_CLICK_POST_JS)
    if clicked != "posted":
        return {**base, "ok": False, "kind_err": "no_post_button", "detail": f"could not click Post (got {clicked})"}
    time.sleep(NAV_SETTLE_S)

    probe = re.sub(r"https?://\S+", "", text).strip()
    probe = (probe[:40] or text[:40]).strip()
    profile = (_config().get("profile_url") or "https://substack.com/@hiper2d").rstrip("/")
    _navigate(profile + "/notes")
    time.sleep(NAV_SETTLE_S)
    finder = (
        "(()=>{const M=" + json.dumps(probe[:30]) + ";"
        "for(const a of document.querySelectorAll('a[href*=\"/note/c-\"]')){"
        "let box=a;for(let i=0;i<8&&box.parentElement;i++){box=box.parentElement;"
        "if((box.innerText||'').includes(M))return a.href.split('?')[0];}}return '';})()"
    )
    url = None
    for _ in range(4):
        hit = _raw_js(finder)
        if hit and "/note/" in hit:
            url = hit
            break
        time.sleep(2)
    return {**base, "ok": True, "url": url, "verified": url is not None,
            "detail": "posted" + ("" if url else " (permalink not resolved — verify manually)")}


def post_approved() -> dict:
    """Post every draft in today's outbox marked 'approved'; update each status."""
    drafts = store.outbox_list(status="approved")
    results = []
    for d in drafts:
        r = post(d["note_url"], d["draft_text"], kind="comment")
        store.outbox_set_status(d["id"], "posted" if r.get("ok") else "failed")
        results.append({"id": d["id"], "ok": r.get("ok"), "verified": r.get("verified"), "detail": r.get("detail")})
    return {"ok": True, "approved": len(drafts), "posted": sum(1 for r in results if r["ok"]), "results": results}


# ─── like-replies ────────────────────────────────────────────────────────────
#
# Likes the notes we've replied to, from Alex's own "Likes & Replies" tab. This
# surface is reliable where the note-permalink feed was not: it's a clean newest-
# first list of exactly the notes we replied to, so we never misnavigate, and a
# liked heart is distinguishable from an unliked one.
#
# Hard-won gotchas (2026-06-01), do NOT "simplify" these away:
#   * Substack keeps the heart's aria-label="Like" even AFTER liking — there is no
#     "Unlike" label and no aria-pressed. The only reliable liked/unliked signal is
#     the SVG <path> fill: solid colour = liked, "rgba(0, 0, 0, 0)" (transparent) =
#     unliked. We use that both to skip already-liked notes (a second click would
#     UN-like them) and to verify a like took.
#   * .click() and synthetic mouse/pointer events do NOT register a like. Only a
#     trusted CDP Input.dispatchMouseEvent does — AND it needs buttons:1 on press +
#     a realistic (~180ms) press-hold. Without buttons/hold it lands but no-ops.
#   * Set a tall viewport and scrollIntoView the button first, or the click misses
#     (headless default viewport is short; off-screen coords do nothing).

def _like_entry_js(note_id: str) -> str:
    nid = note_id.replace("'", "").replace('"', "")
    return (
        "(()=>{const link=document.querySelector('a[href*=\"/note/" + nid + "\"]');"
        "if(!link)return JSON.stringify({found:false});let box=link;"
        "for(let i=0;i<10&&box.parentElement;i++){box=box.parentElement;"
        "const b=box.querySelector('button[aria-label=\"Like\"],button[aria-label=\"Unlike\"]');"
        "if(b){b.scrollIntoView({block:'center'});const r=b.getBoundingClientRect();"
        "const p=b.querySelector('path,svg *');const f=p?getComputedStyle(p).fill:'';"
        "const liked=f!=='rgba(0, 0, 0, 0)'&&f!=='';"
        "return JSON.stringify({found:true,liked:liked,x:Math.round(r.x+r.width/2),"
        "y:Math.round(r.y+r.height/2),count:(b.textContent||'').trim()});}}"
        "return JSON.stringify({found:false});})()"
    )


def _trusted_click(x: float, y: float) -> None:
    """A real (isTrusted) left click via CDP — the only kind Substack's like
    button honours. buttons:1 on press + a press-hold are both required."""
    _cli("cdp", "Input.dispatchMouseEvent", json.dumps({"type": "mouseMoved", "x": x, "y": y}))
    _cli("cdp", "Input.dispatchMouseEvent", json.dumps({"type": "mousePressed", "x": x, "y": y, "button": "left", "buttons": 1, "clickCount": 1}))
    time.sleep(0.18)
    _cli("cdp", "Input.dispatchMouseEvent", json.dumps({"type": "mouseReleased", "x": x, "y": y, "button": "left", "buttons": 0, "clickCount": 1}))


def like_replies(max_likes: int = 15) -> dict:
    """Like the PARENT notes we've commented on, from the Likes & Replies tab,
    skipping any already liked. Scoped strictly to note ids in our `engaged` state
    (newest first) — never anything else on the tab. This matters: that tab also
    lists Alex's OWN replies (each reply is itself a note with its own c- id); a
    naive "like everything un-liked here" would make Alex like his own comments.
    Secondary, best-effort gesture; safe to re-run (already-liked → skipped)."""
    engaged = list(reversed(store.load_state().get("engaged", [])))  # newest first
    if not engaged:
        return {"ok": True, "liked": [], "already_liked": [], "detail": "no engaged notes yet"}
    profile = (_config().get("profile_url") or "https://substack.com/@hiper2d").rstrip("/")
    if not ensure_chrome(headless=True):
        return {"ok": False, "kind": "chrome_down", "detail": f"Chrome not reachable on :{CDP_PORT}"}
    _cli("viewport", "1280x1600", "--scale", "1")
    if not _navigate(profile + "/likes"):
        return {"ok": False, "kind": "nav_failed", "detail": "navigate to Likes & Replies failed"}
    time.sleep(NAV_SETTLE_S)
    # Load a few screens so recently-commented notes are in the DOM.
    for _ in range(3):
        _cli("scroll", "--direction", "down", "--amount", "1600", "--tab", "0")
        time.sleep(1.0)

    liked, already, failed, missing = [], [], [], []
    for nid in engaged:
        if len(liked) >= max_likes:
            break
        st = _json_js(_like_entry_js(nid))
        if not isinstance(st, dict) or not st.get("found"):
            missing.append(nid)          # not in the loaded list (likely older) — skip
            continue
        if st.get("liked"):
            already.append(nid)
            continue
        time.sleep(0.4)
        _trusted_click(st["x"], st["y"])
        time.sleep(1.3)
        st2 = _json_js(_like_entry_js(nid))
        (liked if isinstance(st2, dict) and st2.get("liked") else failed).append(nid)
    return {"ok": True, "liked": liked, "already_liked": already, "failed": failed, "not_loaded": missing,
            "detail": f"liked {len(liked)}, skipped {len(already)} already-liked, {len(failed)} failed",
            "checked_at": _now_iso()}


# ─── CLI ─────────────────────────────────────────────────────────────────────

def _emit(result: dict):
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("ensure-chrome")
    sub.add_parser("session-check")
    sc = sub.add_parser("scan")
    sc.add_argument("--url", default="https://substack.com/home")
    sc.add_argument("--scrolls", type=int, default=4)
    sc.add_argument("--include-engaged", action="store_true")
    po = sub.add_parser("post")
    po.add_argument("--note-url", required=True)
    po.add_argument("--text-file", required=True)
    po.add_argument("--kind", choices=["welcome", "comment"], default="comment")
    pn = sub.add_parser("post-note", help="post an ORIGINAL Note to Alex's own feed")
    pn.add_argument("--text-file", required=True)

    oa = sub.add_parser("outbox-add")
    oa.add_argument("--note-url", required=True)
    oa.add_argument("--author", default="")
    oa.add_argument("--snippet", default="")
    oa.add_argument("--text-file", required=True)
    ol = sub.add_parser("outbox-list")
    ol.add_argument("--status", default=None)
    os_ = sub.add_parser("outbox-set-status")
    os_.add_argument("--id", required=True)
    os_.add_argument("--status", required=True, choices=["pending", "approved", "posted", "rejected", "failed"])
    sub.add_parser("post-approved")
    lr = sub.add_parser("like-replies")
    lr.add_argument("--max", type=int, default=15)
    sub.add_parser("subscribers")
    bl = sub.add_parser("block")
    bl.add_argument("--handle", required=True)
    ub = sub.add_parser("unblock")
    ub.add_argument("--handle", required=True)
    sub.add_parser("blocklist")
    sub.add_parser("welcomed")
    args = ap.parse_args()

    if args.cmd == "ensure-chrome":
        _emit({"ok": ensure_chrome(headless=True), "port": CDP_PORT})
    elif args.cmd == "session-check":
        _emit(session_check())
    elif args.cmd == "scan":
        _emit(scan(args.url, args.scrolls, args.include_engaged))
    elif args.cmd == "post":
        text = Path(args.text_file).read_text()
        _emit(post(args.note_url, text, kind=args.kind))
    elif args.cmd == "post-note":
        _emit(post_note(Path(args.text_file).read_text()))
    elif args.cmd == "outbox-add":
        _, ccap = _caps()
        if len(store.outbox_list()) >= ccap:
            _emit({"ok": False, "kind_err": "cap_reached", "detail": f"daily comment-draft cap ({ccap}) reached"})
        note_id = (re.search(r"/note/(c-\d+)", args.note_url) or [None, None])[1]
        text = Path(args.text_file).read_text().strip()
        _emit({"ok": True, "draft": store.outbox_add(args.note_url, note_id, args.author, args.snippet, text)})
    elif args.cmd == "outbox-list":
        items = store.outbox_list(status=args.status)
        _emit({"ok": True, "count": len(items), "drafts": items})
    elif args.cmd == "outbox-set-status":
        hit = store.outbox_set_status(args.id, args.status)
        _emit({"ok": bool(hit), "draft": hit, "detail": None if hit else f"no draft with id {args.id} today"})
    elif args.cmd == "post-approved":
        _emit(post_approved())
    elif args.cmd == "like-replies":
        _emit(like_replies(max_likes=args.max))
    elif args.cmd == "subscribers":
        _emit(subscribers())
    elif args.cmd == "block":
        store.block(args.handle)
        _emit({"ok": True, "blocked": store._norm_handle(args.handle), "blocklist": store.load_state()["do_not_engage"]})
    elif args.cmd == "unblock":
        store.unblock(args.handle)
        _emit({"ok": True, "unblocked": store._norm_handle(args.handle), "blocklist": store.load_state()["do_not_engage"]})
    elif args.cmd == "blocklist":
        _emit({"ok": True, "do_not_engage": store.load_state()["do_not_engage"]})
    elif args.cmd == "welcomed":
        _emit({"ok": True, "welcomed": store.load_state()["welcomed"]})


if __name__ == "__main__":
    main()
