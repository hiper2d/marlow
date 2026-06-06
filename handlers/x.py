"""
x — browser-driven X / Twitter posting for the news-crosspost flow.

Mechanical half only, same shape as handlers/substack.py: driving is delegated
to simona's browser CLI over CDP. X needs its OWN persistent logged-in profile
(Alex's X session), separate from Substack's. Substack lives on the 9223
scrape-profile; X gets a dedicated profile on 9224 so the two never collide:

    MARLOW_X_PROFILE=~/.config/marlow/x-profile   (default)
    X_CDP_PORT=9224                               (default)

One-time login (headful), then ticks reuse the cookies headless:

    MARLOW_SCRAPE_PROFILE=~/.config/marlow/x-profile \
        bash $SIMONA_DIR/mcp/browser/start-chrome-persistent.sh 9224
    # log into x.com once in that window, then close it / leave it running

This handler does NOT decide what to post — Marlow's session drafts the text in
Alex's voice (memory/voice-alex.md) and hands it here. We only push it and
verify it landed. For local testing against an already-logged-in session, set
X_CDP_PORT=9222 (the browser skill's default profile).

CLI:
    python handlers/x.py ensure-chrome
    python handlers/x.py session-check
    python handlers/x.py post --text-file /tmp/tweet.txt
    python handlers/x.py post-thread --text-file /tmp/thread.json   # JSON list of tweets
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
from driver.env_loader import import_plist_env  # noqa: E402
import_plist_env()

TWEET_LIMIT = 280

# X needs its own persistent profile (Alex's X login), separate from Substack's
# 9223 scrape-profile. start-chrome-persistent.sh keys the profile off
# MARLOW_SCRAPE_PROFILE, so we point it at a dedicated dir for the X port.
CDP_PORT = os.environ.get("X_CDP_PORT", "9224")
X_PROFILE = os.environ.get("MARLOW_X_PROFILE", str(Path.home() / ".config/marlow/x-profile"))
SIMONA_DIR = os.environ.get("SIMONA_DIR", str(Path.home() / "projects/simona-ai-computer-operator"))
BROWSER_CLI = f"{SIMONA_DIR}/mcp/browser/cli.py"
START_SCRIPT = f"{SIMONA_DIR}/mcp/browser/start-chrome-persistent.sh"
X_HANDLE = os.environ.get("X_HANDLE", "hiper2d")

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
    env = {**os.environ, "HEADLESS": "1" if headless else "0", "MARLOW_SCRAPE_PROFILE": X_PROFILE}
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
    res = _cli("js", expr, "--tab", "0")
    if res.returncode != 0:
        return None
    try:
        return json.loads(res.stdout).get("result")
    except (json.JSONDecodeError, AttributeError):
        return None


def _json_js(expr: str):
    raw = _raw_js(expr)
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None


# ─── session-check ───────────────────────────────────────────────────────────

# Logged in: the composer textarea exists on /compose/post. Logged out: X redirects
# to a login/onboarding flow and the testid is absent. We require BOTH the composer
# present AND not being on a login/onboarding URL — /compose/post can momentarily
# expose a textarea-like node during the login redirect, which once false-positived
# session-check (2026-06-05). The URL is the reliable tell.
_SESSION_JS = r"""(()=>{
  const url=location.href;
  const onboarding=/\/(login|i\/flow\/login|i\/jf\/onboarding|account\/access)/i.test(url);
  const ed=document.querySelector('[data-testid="tweetTextarea_0"]');
  const wall=onboarding || !!document.querySelector('a[href="/login"], a[href="/i/flow/login"], [data-testid="loginButton"]');
  return JSON.stringify({logged_in: !!ed && !onboarding, login_wall: wall, url: url});
})()"""


def session_check() -> dict:
    if not ensure_chrome(headless=True):
        return {"ok": False, "kind": "chrome_down", "detail": f"X Chrome not reachable on :{CDP_PORT}", "checked_at": _now_iso()}
    if not _navigate("https://x.com/compose/post"):
        return {"ok": False, "kind": "nav_failed", "detail": "could not navigate to X composer", "checked_at": _now_iso()}
    time.sleep(NAV_SETTLE_S)
    res = _json_js(_SESSION_JS)
    if res is None:
        return {"ok": False, "kind": "parse_failed", "detail": "session probe returned nothing", "checked_at": _now_iso()}
    if not res.get("logged_in"):
        return {"ok": False, "kind": "reauth",
                "detail": f"X session expired — log in once in the X persistent profile (port {CDP_PORT}, dir {X_PROFILE})",
                "url": res.get("url"), "checked_at": _now_iso()}
    return {"ok": True, "logged_in": True, "url": res.get("url"), "checked_at": _now_iso()}


# ─── posting ─────────────────────────────────────────────────────────────────

def _paste_js(b64_text: str) -> str:
    """Inject plain text into the focused tweet box via a synthetic paste.
    Draft.js only commits via a real ClipboardEvent paste of text/plain;
    execCommand('insertText') desyncs React state and the Post button never
    enables (hard-won in simona's x.md). Plain .value= won't work either."""
    return (
        "(function(){var ed=document.querySelector('[data-testid=\"tweetTextarea_0\"]');"
        "if(!ed){return 'no-editor';}ed.focus();"
        "var txt=decodeURIComponent(escape(atob('" + b64_text + "')));"
        "var dt=new DataTransfer();dt.setData('text/plain',txt);"
        "ed.dispatchEvent(new ClipboardEvent('paste',{clipboardData:dt,bubbles:true,cancelable:true}));"
        "return 'pasted';})()"
    )


# Click the modal Post button (single tweet / first of a thread).
_CLICK_POST_JS = r"""(()=>{const b=document.querySelector('[data-testid="tweetButton"]');if(b&&!b.disabled){b.click();return 'posted';}return 'no-post-button';})()"""
# Click the inline Reply button (subsequent tweets in a thread).
_CLICK_INLINE_JS = r"""(()=>{const b=document.querySelector('[data-testid="tweetButtonInline"]');if(b&&!b.disabled){b.click();return 'posted';}return 'no-inline-button';})()"""


def _find_permalink(marker: str) -> str | None:
    """After posting, find the new tweet's permalink by a unique text marker.
    The tweet takes a few seconds to render, so retry on a short loop."""
    js = (
        "(()=>{const M=" + json.dumps(marker[:40]) + ";"
        "for(const a of document.querySelectorAll('article')){"
        "const tt=a.querySelector('[data-testid=\"tweetText\"]');"
        "if(tt&&tt.textContent.includes(M)){"
        "const l=a.querySelector('a[href*=\"/" + X_HANDLE + "/status/\"]');"
        "if(l)return l.href.split('?')[0];}}return '';})()"
    )
    for _ in range(6):
        hit = _raw_js(js)
        if hit and "/status/" in hit:
            return hit
        time.sleep(3)
    return None


def _paste_and_post(text: str, inline: bool) -> str | None:
    """Paste text into the open composer and click the right Post button.
    Returns the click result string ('posted' / error token)."""
    b64 = base64.b64encode(text.encode()).decode()
    pasted = _raw_js(_paste_js(b64))
    if pasted in (None, "no-editor"):
        return "no-editor"
    time.sleep(ACT_SETTLE_S)
    return _raw_js(_CLICK_INLINE_JS if inline else _CLICK_POST_JS)


def post_tweet(text: str) -> dict:
    """Post a single tweet. Verifies via permalink lookup on the profile."""
    text = text.replace("—", "-").replace("–", "-").strip()
    base = {"posted_at": _now_iso(), "chars": len(text)}
    if len(text) > TWEET_LIMIT:
        return {**base, "ok": False, "kind_err": "too_long", "detail": f"{len(text)} chars > {TWEET_LIMIT}"}
    if not ensure_chrome(headless=True):
        return {**base, "ok": False, "kind_err": "chrome_down", "detail": f"X Chrome not reachable on :{CDP_PORT}"}
    if not _navigate("https://x.com/compose/post"):
        return {**base, "ok": False, "kind_err": "nav_failed", "detail": "navigate to composer failed"}
    time.sleep(NAV_SETTLE_S)
    sess = _json_js(_SESSION_JS) or {}
    if not sess.get("logged_in"):
        return {**base, "ok": False, "kind_err": "reauth", "detail": "X session expired"}
    clicked = _paste_and_post(text, inline=False)
    if clicked != "posted":
        return {**base, "ok": False, "kind_err": "no_post", "detail": f"could not post (got {clicked})"}
    time.sleep(NAV_SETTLE_S)
    _navigate(f"https://x.com/{X_HANDLE}")
    time.sleep(NAV_SETTLE_S)
    url = _find_permalink(text)
    return {**base, "ok": True, "url": url,
            "detail": "posted" + ("" if url else " (permalink not resolved — verify manually)")}


def post_thread(tweets: list[str]) -> dict:
    """Post a thread: tweet 1 is the hook, each subsequent tweet replies to the
    previous one so it reads as one thread. For a crosspost the last tweet
    carries the article link (its card is the click-through)."""
    tweets = [t.replace("—", "-").replace("–", "-").strip() for t in tweets if t and t.strip()]
    if not tweets:
        return {"ok": False, "kind_err": "empty", "detail": "no tweets given"}
    over = [(i, len(t)) for i, t in enumerate(tweets) if len(t) > TWEET_LIMIT]
    if over:
        return {"ok": False, "kind_err": "too_long", "detail": f"tweets over {TWEET_LIMIT}: {over}"}

    first = post_tweet(tweets[0])
    if not first.get("ok"):
        return {"ok": False, "kind_err": first.get("kind_err"), "detail": first.get("detail"), "urls": []}
    urls = [first.get("url")]
    parent = first.get("url")

    for t in tweets[1:]:
        if not parent:
            return {"ok": False, "kind_err": "chain_broke",
                    "detail": "could not resolve a parent permalink to attach the next tweet", "urls": urls}
        if not _navigate(parent):
            return {"ok": False, "kind_err": "nav_failed", "detail": f"navigate to {parent} failed", "urls": urls}
        time.sleep(NAV_SETTLE_S)
        clicked = _paste_and_post(t, inline=True)
        if clicked != "posted":
            return {"ok": False, "kind_err": "reply_failed", "detail": f"could not post reply (got {clicked})", "urls": urls}
        time.sleep(NAV_SETTLE_S)
        nxt = _find_permalink(t)
        urls.append(nxt)
        parent = nxt

    return {"ok": True, "url": urls[0], "urls": urls, "posted_at": _now_iso(),
            "detail": "thread posted" + ("" if all(urls) else " (some permalinks unresolved — verify manually)")}


# ─── CLI ─────────────────────────────────────────────────────────────────────

def _emit(result: dict):
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("ensure-chrome")
    sub.add_parser("session-check")
    p = sub.add_parser("post")
    p.add_argument("--text-file", required=True)
    pt = sub.add_parser("post-thread")
    pt.add_argument("--text-file", required=True, help="JSON list of tweet strings")
    args = ap.parse_args()

    if args.cmd == "ensure-chrome":
        _emit({"ok": ensure_chrome(headless=True), "port": CDP_PORT, "profile": X_PROFILE})
    elif args.cmd == "session-check":
        _emit(session_check())
    elif args.cmd == "post":
        text = Path(args.text_file).read_text()
        _emit(post_tweet(text))
    elif args.cmd == "post-thread":
        tweets = json.loads(Path(args.text_file).read_text())
        if not isinstance(tweets, list):
            _emit({"ok": False, "detail": "post-thread expects a JSON list of strings"})
        _emit(post_thread(tweets))


if __name__ == "__main__":
    main()
