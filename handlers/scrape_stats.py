"""
scrape_stats — console scraping for the 8 Werewolf providers that have NO usable
balance/cost API (so they can't go through monitor_keys):

  - GLM / Z.AI   → cash + credits balance        (a real depleting balance)
  - Gemini       → prepaid credit balance          (a real depleting balance;
                   was spend-vs-cap until Alex moved to prepay on 2026-08-27)
  - Mistral      → month usage vs. spending limit  (postpaid)
  - Sakana Fugu  → prepaid credit balance          (a real depleting balance)
  - MiniMax      → prepaid effective balance       (a real depleting balance)
  - Qwen         → month spend, postpaid + uncapped (free-token quota while the
                   one-time grant lasted — see QWEN below)
  - OpenAI       → prepaid credit balance          (a real depleting balance)
  - Anthropic    → prepaid credit balance          (a real depleting balance)

These numbers live ONLY in each provider's web console, so we read them with a
real Chrome that's logged in once (a dedicated persistent profile on port 9223;
see simona/mcp/browser/start-chrome-persistent.sh). The cron runs it headless
and reuses the stored cookies. When a session lapses the page shows a login
wall — we detect that and raise a `reauth` issue (urgent) instead of reporting a
bogus number. Console redesigns will break the per-provider extractors; those
surface as `parse_failed` (digest), never as a silent wrong value. A zero GLM
balance is never trusted from one read — the SPA paints $0.00 placeholders
before the balance request lands — so zeros are re-read with longer settles,
and an unconfirmable zero right after a run that saw money surfaces as
`suspect_zero` (digest), not `balance_empty` (urgent).

Driving is delegated to simona's browser CLI (CDP_PORT=9223) rather than a
second automation stack — same machinery the browser skill uses.

CLI:
    python handlers/scrape_stats.py report          # all eight + derived issues
    python handlers/scrape_stats.py check <name>     # one provider (see PROVIDERS)
    python handlers/scrape_stats.py ensure-chrome    # (re)launch the headless profile
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from driver.env_loader import import_plist_env  # noqa: E402
import_plist_env()

# Persistent-profile Chrome: dedicated port so it never collides with the
# browser skill's 9222. simona owns the browser tooling + its uv env.
CDP_PORT = os.environ.get("SCRAPE_CDP_PORT", "9223")
SIMONA_DIR = os.environ.get("SIMONA_DIR", str(Path.home() / "projects/simona-ai-computer-operator"))
BROWSER_CLI = f"{SIMONA_DIR}/mcp/browser/cli.py"
START_SCRIPT = f"{SIMONA_DIR}/mcp/browser/start-chrome-persistent.sh"

NAV_SETTLE_S = 4.0     # let the SPA render after navigation before extracting
PARSE_RETRY_SETTLE_S = 12.0  # second, slower read before believing a parse failure
HTTP_TIMEOUT = 60

# Balance thresholds (GLM) — mirror monitor_keys.
LOW_USD = 10.0
CRITICAL_USD = 3.0
# Spend-vs-cap fraction thresholds (Gemini, Mistral): how close to the cap.
NEAR_CAP_FRAC = 0.80      # digest
CRITICAL_CAP_FRAC = 0.95  # urgent
# Free-quota thresholds (Qwen): percent of the per-model token grant still left.
# Set high on purpose. The dollar thresholds can be tight because a balance
# drains slowly; a 1M-token grant does not — the game burned ~20% of all three
# Qwen models in the first day of play (2026-08-05→06). At one scrape a day,
# a 25% threshold would fire once and be at zero on the next run. 50/20 buys
# roughly two days and one day of notice at that rate; lower them if the real
# steady-state burn turns out slower than launch week.
#
# These apply ONLY to models whose auto-stop switch is on, where hitting zero is
# an outage. With auto-stop off, exhaustion just starts billing and there is
# nothing to warn ahead of, so _derive_issues skips both thresholds and reports
# the crossover alone.
QUOTA_LOW_PCT = 50.0       # digest
QUOTA_CRITICAL_PCT = 20.0  # urgent
QUOTA_EXPIRY_WARN_DAYS = 7  # digest — the grant expires on a date, not just on use
# Consecutive runs of the SAME failure on the SAME provider before a digest
# issue escalates to urgent. A one-off is console flakiness; a run of them is a
# broken extractor that nobody is going to notice in a digest line.
REPEAT_URGENT_RUNS = 3


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
    """Make sure the persistent-profile Chrome is listening on CDP_PORT.
    Launches it (headless for the cron) if not. Returns True once reachable."""
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


def _eval_json(js: str, frame: str | None = None) -> dict:
    """Run `js` in tab 0 (it must return a JSON string) and parse the result.
    Returns the parsed dict, or {error:...} on failure.

    `frame` runs the extractor inside the sub-frame whose URL contains that
    substring. Needed when the number lives in an embedded widget rather than
    the host page - AI Studio renders the Gemini credit balance in a
    payments.google.com iframe, which the parent document cannot read across.
    """
    args = ["js", js, "--tab", "0"] + (["--frame", frame] if frame else [])
    res = _cli(*args)
    if res.returncode != 0:
        return {"error": f"js failed: {res.stderr[:160] or res.stdout[:160]}"}
    try:
        outer = json.loads(res.stdout)          # cli wraps as {"result": "<json string>"}
        return json.loads(outer["result"])
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        return {"error": f"unparseable extractor output: {e}"}


def _navigate(url: str, settle_s: float = NAV_SETTLE_S) -> str | None:
    """Navigate tab 0 to `url` and let the SPA settle. Returns an error string
    on failure, None on success."""
    nav = _cli("navigate", url, "--tab", "0")
    if nav.returncode != 0:
        return f"navigate failed: {nav.stderr[:160] or nav.stdout[:160]}"
    time.sleep(settle_s)
    return None


def _navigate_and_extract(url: str, js: str, click_js: str | None = None,
                          settle_s: float = NAV_SETTLE_S, frame: str | None = None) -> dict:
    """Navigate tab 0 to `url`, let it settle, optionally run `click_js` to
    reveal a sub-view (then settle again), run `js` (must return a JSON string),
    parse it. Returns the parsed dict, or {error:...} on failure.

    `frame` targets an embedded widget instead of the host document (see
    `_eval_json`).
    """
    err = _navigate(url, settle_s)
    if err:
        return {"error": err}
    if click_js:
        _cli("js", click_js, "--tab", "0")
        time.sleep(settle_s)
    return _eval_json(js, frame=frame)


# ─── Per-provider extractors (JS returns a JSON string) ──────────────────────
# Each returns {login_wall: bool, ...fields...}. Defensive: a login page or a
# missing number yields login_wall/None rather than a wrong value.

_LOGIN_GUARD = (
    "if(/sign[ -]?in|log[ -]?in|/i.test(document.title) && "
    "/accounts\\.google\\.com|auth\\.mistral|login/i.test(location.href)) "
    "return JSON.stringify({login_wall:true});"
)

GLM = {
    "name": "glm",
    "url": "https://z.ai/manage-apikey/billing",
    "js": """(()=>{
      const t=document.body.innerText;
      if(/sign in|log in/i.test(document.title)||/accounts\\.google|login/i.test(location.href)) return JSON.stringify({login_wall:true});
      const after=(label)=>{const i=t.indexOf(label); if(i<0)return null;
        const m=t.slice(i,i+40).match(/\\$\\s*([0-9][0-9,]*\\.?[0-9]*)/); return m?parseFloat(m[1].replace(/,/g,'')):null;};
      const cash=after('Cash balance'), credits=after('Credits balance');
      return JSON.stringify({login_wall:false, cash, credits});
    })()""",
}

# Gemini is PREPAID as of 2026-08-27, and the metric changed with it. Alex moved
# the billing account onto prepay credits, so the number that matters is a
# depleting balance, not spend-against-a-cap. Reporting the old pair was worse
# than useless: "$22.62 of $2000 (1%)" reads as an account with room to spare on
# the exact day the real balance was $9.83.
#
# The balance is on aistudio.google.com/billing under "Payments" - but NOT in
# that page's DOM. AI Studio embeds a payments.google.com widget in an iframe,
# so `document.body.innerText` on the host page has no "Credit balance" in it at
# all, which is why no host-page regex could ever have found it. payments.google
# .com and aistudio.google.com are different ORIGINS but the same SITE, so the
# frame shares the renderer and never appears as its own CDP target either.
# `--frame` (added to simona's browser CLI 2026-08-27) attaches an isolated
# world to it and reads it directly.
#
# Month-to-date cost stays as CONTEXT, read from the host page's "Total cost".
# It is not the headline any more and never gates the read: a balance with no
# spend figure is still a good balance. Caveat from the page itself: "Cost
# information may take up to 24 hours to update".
GEMINI_FRAME = "payments.google.com/payments"
GEMINI = {
    "name": "gemini",
    "url": "https://aistudio.google.com/billing",
    "frame": GEMINI_FRAME,
    # Runs INSIDE the payments frame. The frame has no login chrome of its own -
    # when the session lapses the host page redirects, so the login guard is the
    # host-page check in `js_host` below.
    "js": """(()=>{
      const t=document.body.innerText;
      if(!/Credit balance/.test(t)) return JSON.stringify({login_wall:false, balance:null});
      const after=(label,win)=>{const i=t.indexOf(label); if(i<0)return null;
        const m=t.slice(i+label.length,i+label.length+(win||40))
                 .match(/\\$\\s*([0-9][0-9,]*\\.?[0-9]*)/);
        return m?parseFloat(m[1].replace(/,/g,'')):null;};
      const ar=t.match(/Auto-reload:\\s*(On|Off)/i);
      const added=t.match(/\\$\\s*([0-9][0-9,]*\\.?[0-9]*)\\s*added on\\s*([A-Za-z]{3}\\s*[0-9]{1,2})/);
      return JSON.stringify({login_wall:false, balance:after('Credit balance'),
        prepay: /Prepay/.test(t),
        auto_reload: ar?ar[1].toLowerCase()==='on':null,
        last_topup_usd: added?parseFloat(added[1].replace(/,/g,'')):null,
        last_topup_on: added?added[2]:null});
    })()""",
    # Runs on the HOST page: login guard + month-to-date spend for context.
    "js_host": """(()=>{
      if(/accounts\\.google\\.com\\/v3\\/signin|ServiceLogin/i.test(location.href))
        return JSON.stringify({login_wall:true});
      const t=document.body.innerText;
      const after=(label,win)=>{const i=t.indexOf(label); if(i<0)return null;
        const m=t.slice(i+label.length,i+label.length+(win||60))
                 .match(/\\$\\s*([0-9][0-9,]*\\.?[0-9]*)/);
        return m?parseFloat(m[1].replace(/,/g,'')):null;};
      return JSON.stringify({login_wall:false, spend: after('Total cost')});
    })()""",
}

# Mistral redesigned the console again (2026-07-28, three days of parse_failed):
# the billing page no longer carries month usage OR a dollar spending cap at all
# — it's payment methods, a credits balance, and invoices. The month figure moved
# to /organization/usage, where it renders WITHOUT a "$" ("Total Cost / 3.25 /
# USD"), which is why every $-anchored regex went null. The "Monthly limit: $30"
# cap is gone from the UI entirely (the Limits page is now rate limits, TPM/RPS),
# so the cap becomes a configured constant like Gemini's — re-confirm if Alex
# changes it in the account. Pending pay-as-you-go still lives on billing; it's
# context, not the metric, so we don't spend a second navigation on it.
MISTRAL_CAP_USD = float(os.environ.get("MISTRAL_SPEND_CAP", "30"))
MISTRAL = {
    "name": "mistral",
    "url": "https://admin.mistral.ai/organization/usage",
    "js": """(()=>{
      const t=document.body.innerText;
      if(/auth\\.mistral|\\/login/i.test(location.href)) return JSON.stringify({login_wall:true});
      // Numbers here are bare and followed by a USD unit line, e.g.
      // "Total Cost\\n3.25\\nUSD". Anchor on the label, take the first number.
      const after=(label,win)=>{const i=t.indexOf(label); if(i<0)return null;
        const m=t.slice(i+label.length,i+label.length+(win||40))
                 .match(/([0-9][0-9,]*\\.?[0-9]*)\\s*(?:USD)?/);
        return m?parseFloat(m[1].replace(/,/g,'')):null;};
      return JSON.stringify({login_wall:false,
        usage: after('Total Cost') ?? after('Total:'), pending: null});
    })()""",
}

# Sakana Fugu — prepaid credit, OpenAI-compatible inference API but NO balance
# endpoint (api.sakana.ai serves /v1/models only; the console is a Next.js RSC
# app with no REST balance route). The real number lives ONLY on the pay-as-you-
# go *tab* of the billing page — the default billing tab shows subscription
# plans and no balance, so the ?tab=payAsYouGo query param is load-bearing.
# "Credit balance | $X.XX" is the depleting prepaid total; "Total: $Y.YY" is the
# period usage we also capture for context.
SAKANA = {
    "name": "sakana",
    "url": "https://console.sakana.ai/billing?tab=payAsYouGo",
    "js": """(()=>{
      const t=document.body.innerText;
      const authed=/Toggle Sidebar/.test(t);
      if(!authed && /sign[ -]?in|log[ -]?in|continue with/i.test(t)) return JSON.stringify({login_wall:true});
      const after=(label,win)=>{const i=t.indexOf(label); if(i<0)return null;
        const m=t.slice(i,i+(win||60)).match(/\\$\\s*([0-9][0-9,]*\\.?[0-9]*)/); return m?parseFloat(m[1].replace(/,/g,'')):null;};
      return JSON.stringify({login_wall:false, balance:after('Credit balance'), usage:after('Total:')});
    })()""",
}

# MiniMax — prepaid balance, added 2026-08-06 with the M3 models. No balance API
# exists for pay-as-you-go accounts (probed live: /v1/get_account_balance,
# /v1/query/account, /v1/user/balance all 404; /v1/token_plan/remains answers but
# only for a *subscription* key, and Alex is on PAYG) — so, console. The balance
# widget lives on the recharge-records page; /user-center/payment/balance
# redirects there, so we go straight to the canonical URL. "Effective balance"
# is cash + voucher + credit − outstanding, i.e. what the game can actually
# spend; the components are captured for context only.
MINIMAX = {
    "name": "minimax",
    "url": "https://platform.minimax.io/console/recharge-records",
    "js": """(()=>{
      const t=document.body.innerText;
      if(/account\\.minimax\\.io\\/unified-login/i.test(location.href)||
         /Sign in or create an account/i.test(t)) return JSON.stringify({login_wall:true});
      const after=(label,win)=>{const i=t.indexOf(label); if(i<0)return null;
        const m=t.slice(i+label.length,i+label.length+(win||40))
                 .match(/\\$?\\s*([0-9][0-9,]*\\.?[0-9]*)/); return m?parseFloat(m[1].replace(/,/g,'')):null;};
      return JSON.stringify({login_wall:false, balance:after('Effective balance'),
        cash:after('Cash'), voucher:after('Voucher'), outstanding:after('Outstanding')});
    })()""",
}

# Qwen / QwenCloud — added 2026-08-06 with the Qwen3.7/3.8 models. This one is
# NOT a money balance and doesn't fit either existing metric. QwenCloud gives new
# accounts a 90-day free tier of 1M tokens PER MODEL (Alex registered 2026-08-05
# → expires 2026-11-05). It is one-time and does not renew: per QwenCloud's docs
# the remainder is void at expiry and is never reissued, though a model released
# AFTER signup gets its own fresh grant dated from its release (and a dated
# snapshot counts as a separate model from the undated latest).
#
# Whether exhaustion hurts depends on the per-model auto-stop switch. On, calls
# to that model FAIL rather than bill. Off, they roll onto pay-as-you-go, since
# the free grant is always spent before the card. Alex turned auto-stop OFF for
# the tracked models on 2026-08-12, so exhaustion is now a billing crossover and
# not an outage. Percent-of-grant is still the only number the console gives
# while the grant lasts (its pay-as-you-go page reads $0.00 throughout), so we
# keep reading it - but see _derive_issues for how much noise it earns.
#
# The console's own JSON endpoint (/data/api.json?product=freetier&action=
# ListBailianFreetier) is POST-with-CSRF ("PostonlyOrTokenError" on a plain GET),
# so we read the rendered table instead. It paginates 10-per-page over 260 models,
# so we drive the "Search models" box once per tracked model and read the single
# matching row — matching on an exact cell value, since a search for
# "qwen3.7-plus" also returns "qwen3.7-plus-2026-05-26" (a dated snapshot with an
# untouched grant, which would read as healthy and mask the real one).
QWEN_MODELS = [m.strip() for m in os.environ.get(
    "QWEN_MODELS", "qwen3.8-max,qwen3.7-plus,qwen3.7-flash").split(",") if m.strip()]

QWEN = {
    "name": "qwen",
    "url": "https://home.qwencloud.com/benefits",
    # Logged out, the page still renders its chrome (sidebar, headings) and only
    # the content area says so — hence matching on the copy, not on a redirect.
    "login_js": """(()=>{const t=document.body.innerText;
      return JSON.stringify({login_wall:/You are currently not logged in|Log in to QwenCloud/i.test(t)});})()""",
    "search_js": """(()=>{const i=document.querySelector('input[placeholder="Search models"]');
      if(!i) return JSON.stringify({ok:false, error:'search box not found'});
      const set=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
      set.call(i, __CODE__); i.dispatchEvent(new Event('input',{bubbles:true}));
      return JSON.stringify({ok:true});})()""",
    # Row cells: ['', code, quota, consumed, 'NN.NN%', 'YYYY-MM-DD\\nN days remaining',
    # status, actions] - a leading blank cell (row selector), so index off the code cell.
    #
    # The last cell is NOT a state readout. It holds the auto-stop toggle plus a
    # STATIC label reading "Free quota only" that never changes. Until 2026-08-12
    # this extractor took that label as `mode` and so reported every model as
    # guarded no matter where the switch sat - it had never once observed the
    # real setting. The state lives on the control:
    #   <button role="switch" aria-checked="true|false"
    #           data-autolog="key=benefits.free_tier.table.safe_mode.toggle">
    # so read aria-checked and emit a bool. null means the control was missing,
    # which the caller treats as "assume guarded" rather than guessing.
    "row_js": """(()=>{const code=__CODE__;
      const row=[...document.querySelectorAll('tr')].find(r=>
        [...r.querySelectorAll('td')].some(c=>c.innerText.trim()===code));
      if(!row) return JSON.stringify({found:false});
      const cells=[...row.querySelectorAll('td')].map(c=>c.innerText.trim());
      const k=cells.indexOf(code);
      const pct=parseFloat(String(cells[k+3]||'').replace('%',''));
      const exp=String(cells[k+4]||'');
      const days=(exp.match(/([0-9]+)\\s*days? remaining/)||[])[1];
      const sw=row.querySelector('[role="switch"]');
      const aria=sw?sw.getAttribute('aria-checked'):null;
      return JSON.stringify({found:true, code, quota:cells[k+1]||null, consumed:cells[k+2]||null,
        remaining_pct: isNaN(pct)?null:pct, expires:(exp.match(/[0-9]{4}-[0-9]{2}-[0-9]{2}/)||[])[0]||null,
        days_left: days?parseInt(days,10):null, status:cells[k+5]||null,
        auto_stop: aria===null?null:aria==='true'});})()""",
}

QWEN_SEARCH_SETTLE_S = 2.5   # the table re-renders client-side; no network wait needed

# Qwen's MONEY page, added 2026-08-27. Until the free grant ran out this handler
# reported percent-of-grant alone, and the note in the config above said the
# dollar page "reads $0.00 either way" - true while the grant was paying for
# everything. It stopped being true on the crossover (2026-08-25): calls now bill
# pay-as-you-go and the console shows real spend, so a row that says only
# "0% left" hides the one number Alex is actually being charged.
#
# There is no balance here to deplete - QwenCloud is postpaid and metered, with
# no cap exposed in the UI. So the honest headline is spend-to-date plus what is
# currently due, and quota stays as the sub-note it now is.
QWEN_BILLING = {
    "url": "https://home.qwencloud.com/billing/overview",
    # Figures render as a label, then a bare "$", then the number on its own
    # line ("Total Spend | 2026-08 | $ | 1.85"), so the $ and the digits cannot
    # be matched as one token the way every other console allows.
    "js": """(()=>{
      const t=document.body.innerText;
      if(/You are currently not logged in|Log in to QwenCloud/i.test(t))
        return JSON.stringify({login_wall:true});
      const after=(label,win)=>{const i=t.indexOf(label); if(i<0)return null;
        const m=t.slice(i+label.length,i+label.length+(win||60))
                 .match(/\\$\\s*\\n?\\s*([0-9][0-9,]*\\.?[0-9]*)/);
        return m?parseFloat(m[1].replace(/,/g,'')):null;};
      const period=(t.match(/([0-9]{4}-[0-9]{2})/)||[])[1]||null;
      return JSON.stringify({login_wall:false, spend:after('Total Spend'),
        due:after('Total Due'), period});
    })()""",
}

# OpenAI - prepaid API credit. Moved here from monitor_keys' Tier 2 on
# 2026-08-24. Tier 2 derived the balance as (a console figure Alex read once)
# minus cost-API spend since that date, which is true only until he tops up: a
# top-up is invisible to the cost API, so the derivation kept subtracting real
# spend from a pre-payment number and produced two confident, wrong CRITICALs
# (08-22 $2.26, 08-24 $0.40 - the real balance was $20.05). A stale baseline
# fails quiet and wrong. Reading the console every run fails loud instead, and
# deletes the manual re-anchor-after-every-top-up step entirely.
#
# "API credit balance" is the depleting prepaid total. Do NOT scan for the
# largest $ on the page - it also prints auto-reload copy and plan pricing.
# `auto_reload` is context, not the metric: with it ON, a low balance refills
# itself and is much less urgent than the number alone suggests.
OPENAI = {
    "name": "openai",
    "url": "https://platform.openai.com/settings/organization/billing/overview",
    "js": """(()=>{
      const t=document.body.innerText;
      if(/auth\\.openai\\.com|\\/log[- ]?in|\\/login/i.test(location.href)) return JSON.stringify({login_wall:true});
      if(!/API credit balance/.test(t) && /sign[ -]?in|log[ -]?in|continue with/i.test(t))
        return JSON.stringify({login_wall:true});
      const after=(label,win)=>{const i=t.indexOf(label); if(i<0)return null;
        const m=t.slice(i+label.length,i+label.length+(win||40))
                 .match(/\\$\\s*([0-9][0-9,]*\\.?[0-9]*)/); return m?parseFloat(m[1].replace(/,/g,'')):null;};
      const ar=t.match(/Auto-reload is\\s*\\n?\\s*(ON|OFF)/i);
      return JSON.stringify({login_wall:false, balance:after('API credit balance'),
        auto_reload: ar?ar[1].toUpperCase()==='ON':null});
    })()""",
}


# Anthropic - prepaid credit. Joined OpenAI in leaving monitor_keys' Tier 2 on
# 2026-08-24, for the same reason: a console baseline is only true until a
# top-up, and a top-up is invisible to the cost API. This one had not gone
# wrong yet (derived $16.24 vs an actual $16.08 - the key genuinely had not
# been topped up since the 2026-05-31 anchor, which closes that open question),
# but an 85-day-old baseline was one payment away from OpenAI's failure.
#
# Anchoring is the fiddly part here. "Credit balance" is a section HEADING
# followed by a two-sentence blurb, so the number is ~150 chars downstream of
# it and a windowed search would sweep in whatever else rendered. The number is
# instead pinned by the label that TRAILS it ("$16.08 / Remaining balance"), so
# we match backwards off that. Sidebar "Credits $NN.NN" is the fallback.
#
# Do NOT scan for the largest $: this page also prints the monthly spend limit
# ($100), month-to-date spend ($9.85) and every historical credit grant ($50).
# The spend/limit pair is captured as context - it is a notification threshold
# Alex set, not money he holds.
ANTHROPIC = {
    "name": "anthropic",
    "url": "https://console.anthropic.com/settings/billing",
    "js": """(()=>{
      const t=document.body.innerText;
      const authed=/Remaining balance|Credit balance/i.test(t);
      if(!authed && /continue with google|continue with email|build on the claude platform/i.test(t))
        return JSON.stringify({login_wall:true});
      if(!authed && /\\/login|auth\\.anthropic\\.com/i.test(location.href))
        return JSON.stringify({login_wall:true});
      const num=(x)=>x?parseFloat(String(x).replace(/,/g,'')):null;
      const trailing=t.match(/\\$\\s*([0-9][0-9,]*\\.?[0-9]*)\\s*\\n?\\s*Remaining balance/i);
      const sidebar=t.match(/Credits\\s*\\n?\\s*\\$\\s*([0-9][0-9,]*\\.?[0-9]*)/i);
      const spent=t.match(/\\$\\s*([0-9][0-9,]*\\.?[0-9]*)\\s*spent/i);
      const limit=t.match(/^Monthly spend limit$[\\s\\S]{0,60}?\\$\\s*([0-9][0-9,]*\\.?[0-9]*)/m);
      return JSON.stringify({login_wall:false,
        balance: num(trailing?trailing[1]:(sidebar?sidebar[1]:null)),
        spend_usd: num(spent?spent[1]:null),
        spend_limit_usd: num(limit?limit[1]:null),
        auto_reload: /Auto reload is off/i.test(t) ? false : (/Auto reload is on/i.test(t) ? true : null)});
    })()""",
}


PROVIDERS = {p["name"]: p for p in (GLM, GEMINI, MISTRAL, SAKANA, MINIMAX, QWEN, OPENAI, ANTHROPIC)}


# ─── Normalize each provider's raw extract into a common shape ───────────────


def _last_balance(provider: str) -> float | None:
    """Last successfully-read balance for `provider` from the saved snapshot."""
    from driver.budget_state import load_latest
    rep = load_latest("scrape") or {}
    for p in rep.get("providers", []):
        if p.get("provider") == provider and p.get("ok"):
            return p.get("balance_usd")
    return None


def _confirmed_balance(cfg: dict, provider: str, value: float, field: str = "balance") -> tuple[float, float | None]:
    """Re-read a balance that came back as exactly 0, and report a prior balance
    if it stays 0 without explanation.

    An SPA paints "$0.00" placeholders before the balance request lands, and a
    placeholder zero parses exactly like a real one (GLM, 2026-06-11: $9.23
    reported as dry). Returns (value, suspect_prev): `suspect_prev` is the last
    successfully-read balance when it was positive and this read insists on zero
    — the caller turns that into `suspect_zero` (digest) rather than
    `balance_empty` (urgent). None means the zero is trustworthy.
    """
    if value != 0:
        return value, None
    for settle in (10.0, 15.0):
        retry = _navigate_and_extract(cfg["url"], cfg["js"], cfg.get("click_js"),
                                      settle_s=settle, frame=cfg.get("frame"))
        v = retry.get(field)
        if v is None:
            continue
        value = v
        if v > 0:
            return v, None
    prev = _last_balance(provider)
    return value, (prev if prev and prev > 0 else None)


def _check_qwen(settle_s: float = NAV_SETTLE_S) -> dict:
    """Qwen's free-tier grants: one search + one row read per tracked model.

    Unlike the other providers this needs several round trips on ONE page load,
    so it doesn't go through _navigate_and_extract. A model whose row never
    appears is dropped rather than counted as 0% — a missing row means the search
    or the layout broke, not that the grant is gone. Only if *no* tracked model
    resolves do we call the whole check parse_failed.
    """
    base = {"provider": "qwen", "checked_at": _now_iso()}
    err = _navigate(QWEN["url"], settle_s)
    if err:
        return {**base, "ok": False, "kind": "parse_failed", "error": err}
    guard = _eval_json(QWEN["login_js"])
    if guard.get("error"):
        return {**base, "ok": False, "kind": "parse_failed", "error": guard["error"]}
    if guard.get("login_wall"):
        return {**base, "ok": False, "kind": "reauth", "error": "login wall — session expired, re-auth needed"}

    models, misses = [], []
    for code in QWEN_MODELS:
        setres = _eval_json(QWEN["search_js"].replace("__CODE__", json.dumps(code)))
        if not setres.get("ok"):
            return {**base, "ok": False, "kind": "parse_failed",
                    "error": setres.get("error") or "could not drive the model search box"}
        time.sleep(QWEN_SEARCH_SETTLE_S)
        row = _eval_json(QWEN["row_js"].replace("__CODE__", json.dumps(code)))
        if row.get("found") and row.get("remaining_pct") is not None:
            models.append(row)
        else:
            misses.append(code)
    if not models:
        return {**base, "ok": False, "kind": "parse_failed",
                "error": f"no free-tier row found for any of {', '.join(QWEN_MODELS)}"}

    worst = min(models, key=lambda m: m["remaining_pct"])
    days = [m["days_left"] for m in models if m.get("days_left") is not None]

    # The money page is a second navigation off the benefits page. A failure
    # here degrades the row to quota-only rather than failing the whole check -
    # the grant numbers we already have are still worth reporting.
    money = _navigate_and_extract(QWEN_BILLING["url"], QWEN_BILLING["js"], settle_s=settle_s)
    spend, due = money.get("spend"), money.get("due")
    # Once the grant is gone the spend figure IS the headline; while it lasts,
    # percent-of-grant still is. Switching the metric on the data rather than on
    # a date means the row describes whatever is actually paying for the calls.
    metric = "spend" if (spend is not None and worst["remaining_pct"] <= 0) else "quota"
    return {**base, "ok": True, "metric": metric,
            "spend_usd": spend, "due_usd": due, "spend_period": money.get("period"),
            "remaining_pct": worst["remaining_pct"], "worst_model": worst["code"],
            "days_left": min(days) if days else None,
            "expires": worst.get("expires"),
            # Auto-stop of the model the headline is about, so the issue text and
            # the number it quotes always describe the same row.
            "auto_stop": worst.get("auto_stop"),
            # Any tracked model still guarded is worth naming even when it isn't
            # the worst one: that's the one that will fail instead of billing.
            "guarded_models": [m["code"] for m in models if m.get("auto_stop") is True],
            "models": models, "missing_models": misses}


def _check(provider: str) -> dict:
    """Check one provider, re-reading once with a longer settle before calling
    it a parse failure.

    A cold headless Chrome (the state every cron run starts in) can need well
    over NAV_SETTLE_S to paint: Gemini went parse_failed on the 2026-08-06 runs
    and read $1.95 fine on a warm page seconds later. "The number isn't there
    yet" and "the console got redesigned" look identical from one read, so pay
    one slow retry to tell them apart rather than tuning a per-provider constant
    every time a console gets heavier.
    """
    result = _check_once(provider)
    if result.get("kind") == "parse_failed":
        result = _check_once(provider, settle_s=PARSE_RETRY_SETTLE_S)
    return result


def _check_once(provider: str, settle_s: float = NAV_SETTLE_S) -> dict:
    if provider == "qwen":
        return _check_qwen(settle_s)
    cfg = PROVIDERS[provider]
    raw = _navigate_and_extract(cfg["url"], cfg["js"], cfg.get("click_js"),
                                settle_s=settle_s, frame=cfg.get("frame"))
    base = {"provider": provider, "checked_at": _now_iso()}
    if raw.get("error"):
        return {**base, "ok": False, "kind": "parse_failed", "error": raw["error"]}
    if raw.get("login_wall"):
        return {**base, "ok": False, "kind": "reauth", "error": "login wall — session expired, re-auth needed"}

    if provider == "glm":
        cash, credits = raw.get("cash"), raw.get("credits")
        if cash is None and credits is None:
            return {**base, "ok": False, "kind": "parse_failed", "error": "no cash/credits balance found"}
        total = (cash or 0.0) + (credits or 0.0)
        # The billing SPA paints "$0.00" placeholders before the balance
        # request lands, and a placeholder zero parses exactly like a real
        # one (bit us 2026-06-11: $9.23 reported as dry). Never trust a
        # zero from a single read — re-extract with longer settles.
        if total == 0:
            for settle in (10.0, 15.0):
                retry = _navigate_and_extract(cfg["url"], cfg["js"], cfg.get("click_js"),
                                              settle_s=settle, frame=cfg.get("frame"))
                r_cash, r_credits = retry.get("cash"), retry.get("credits")
                if r_cash is None and r_credits is None:
                    continue
                cash, credits = r_cash, r_credits
                total = (cash or 0.0) + (credits or 0.0)
                if total > 0:
                    break
        # Still zero after retries: if the last saved run had money, a
        # one-window drop to exactly $0.00 is far more likely a render/parse
        # issue than a real drain — report suspect (digest), not dry (urgent).
        # If it IS a real drain, the next run has no prior balance and the
        # confirmed zero goes through as balance_empty.
        if total == 0:
            prev = _last_balance(provider)
            if prev and prev > 0:
                return {**base, "ok": False, "kind": "suspect_zero",
                        "error": f"reads $0.00 across retries but last run saw ${prev:.2f} — "
                                 "likely placeholder render; verify in console before topping up"}
        return {**base, "ok": True, "metric": "balance", "balance_usd": round(total, 4),
                "cash_usd": cash, "credits_usd": credits, "is_available": total > 0}
    if provider == "gemini":
        # `raw` came from the payments FRAME. The host page carries the login
        # guard and the month-to-date spend, so read it separately - the page is
        # already loaded, so this is one extra eval, not a second navigation.
        host = _eval_json(cfg["js_host"])
        if host.get("login_wall"):
            return {**base, "ok": False, "kind": "reauth",
                    "error": "login wall - session expired, re-auth needed"}
        bal = raw.get("balance")
        if bal is None:
            return {**base, "ok": False, "kind": "parse_failed",
                    "error": "no 'Credit balance' in the AI Studio payments frame"}
        bal, suspect_prev = _confirmed_balance(cfg, provider, bal)
        if suspect_prev:
            return {**base, "ok": False, "kind": "suspect_zero",
                    "error": f"reads $0.00 across retries but last run saw ${suspect_prev:.2f} - "
                             "likely placeholder render; verify in console before topping up"}
        return {**base, "ok": True, "metric": "balance", "balance_usd": round(bal, 4),
                "spend_mtd_usd": host.get("spend"), "auto_reload": raw.get("auto_reload"),
                "last_topup_usd": raw.get("last_topup_usd"),
                "last_topup_on": raw.get("last_topup_on"),
                "is_available": bal > 0}
    if provider == "mistral":
        usage, pending = raw.get("usage"), raw.get("pending")
        if usage is None:
            return {**base, "ok": False, "kind": "parse_failed", "error": "no usage figure found"}
        return {**base, "ok": True, "metric": "spend_cap", "spend_usd": round(usage, 4),
                "cap_usd": MISTRAL_CAP_USD, "pending_usd": pending}
    if provider in ("sakana", "minimax", "openai", "anthropic"):
        bal = raw.get("balance")
        if bal is None:
            return {**base, "ok": False, "kind": "parse_failed", "error": "no credit balance found"}
        # Same SPA placeholder hazard as GLM: the balance can paint "$0.00"
        # before its request lands. Never trust a lone zero.
        bal, suspect_prev = _confirmed_balance(cfg, provider, bal)
        if suspect_prev:
            return {**base, "ok": False, "kind": "suspect_zero",
                    "error": f"reads $0.00 across retries but last run saw ${suspect_prev:.2f} — "
                             "likely placeholder render; verify in console before topping up"}
        if provider == "sakana":
            extra = {"usage_usd": raw.get("usage")}
        elif provider == "openai":
            extra = {"auto_reload": raw.get("auto_reload")}
        elif provider == "anthropic":
            extra = {"auto_reload": raw.get("auto_reload"),
                     "spend_usd": raw.get("spend_usd"),
                     "spend_limit_usd": raw.get("spend_limit_usd")}
        else:
            extra = {"cash_usd": raw.get("cash"), "voucher_usd": raw.get("voucher"),
                     "outstanding_usd": raw.get("outstanding")}
        return {**base, "ok": True, "metric": "balance", "balance_usd": round(bal, 4),
                **extra, "is_available": bal > 0}
    return {**base, "ok": False, "kind": "parse_failed", "error": "unknown provider"}


def _derive_issues(results: list[dict]) -> list[dict]:
    from driver.budget_state import failure_streak
    issues = []
    for r in results:
        name = r["provider"]
        if not r.get("ok"):
            sev = "urgent" if r.get("kind") == "reauth" else "digest"
            detail = r.get("error", "")
            # A break that keeps breaking is a different thing from a flaky run.
            # Failing loud on the first run is correct, but three identical
            # digest lines read exactly like one, which is how Mistral went dark
            # for three days twice (07-24, 07-28). Escalate on the Nth in a row.
            runs = failure_streak("scrape", name, r.get("kind")) + 1
            if runs >= REPEAT_URGENT_RUNS:
                sev = "urgent"
                detail = f"{detail} ({runs} runs running — not flakiness, the check is broken)"
            issues.append({"severity": sev, "kind": r.get("kind", "error"), "target": name,
                           "detail": detail, "failing_runs": runs})
            continue
        if r.get("metric") == "balance":
            usd = r["balance_usd"]
            if usd <= 0:
                issues.append({"severity": "urgent", "kind": "balance_empty", "target": name,
                               "detail": f"{name} balance is dry. Top up now."})
            elif usd < CRITICAL_USD:
                issues.append({"severity": "urgent", "kind": "balance_critical", "target": name,
                               "detail": f"{name} balance ${usd:.2f} (< ${CRITICAL_USD:.0f}). Top up now."})
            elif usd < LOW_USD:
                issues.append({"severity": "digest", "kind": "balance_low", "target": name,
                               "detail": f"{name} balance ${usd:.2f} (< ${LOW_USD:.0f}). Top up soon."})
        elif r.get("metric") in ("quota", "spend"):
            # Qwen: percent of the per-model free-token grant still left, taken
            # from whichever tracked model is furthest along. What running out
            # MEANS depends on that model's auto-stop switch, so the severity
            # has to branch on it:
            #   guarded   -> calls to the model start FAILING. Outage-shaped,
            #                so warn early and loudly, and page on the zero.
            #   unguarded -> calls roll onto pay-as-you-go. No disruption, so
            #                the pre-warnings are pure noise; say it once at the
            #                crossover so the spend doesn't start unannounced.
            pct, model = r.get("remaining_pct"), r.get("worst_model")
            guarded = r.get("auto_stop")
            if guarded is None:
                # Never guess this one. A missing switch means the extractor is
                # broken, and silently assuming either mode invents a fact.
                issues.append({"severity": "digest", "kind": "parse_failed", "target": name,
                               "detail": f"{name} auto-stop switch unreadable on {model}; "
                                         "assuming guarded, so the quota lines below may overstate this."})
            if pct is None:
                pass
            elif guarded is False:
                # The crossover is only news while we cannot yet quote the money.
                # Once the billing page reads (metric "spend"), the row itself
                # carries the dollar figure and repeating this every run is the
                # noise Alex flagged on 2026-08-27 - it fired identically for
                # three days running with no new information in it.
                if pct <= 0 and r.get("metric") == "quota":
                    issues.append({"severity": "digest", "kind": "quota_crossover", "target": name,
                                   "detail": f"{name} free grant used up on {model}. Calls to it now bill "
                                             "pay-as-you-go instead of failing, so track spend from here, "
                                             "not quota. The billing page could not be read this run, so "
                                             "there is no dollar figure to show. The grant is one-time and "
                                             "won't come back."})
            elif pct <= 0:
                issues.append({"severity": "urgent", "kind": "quota_exhausted", "target": name,
                               "detail": f"{name} free quota exhausted on {model} - that model is now failing in-game."})
            elif pct < QUOTA_CRITICAL_PCT:
                issues.append({"severity": "urgent", "kind": "quota_critical", "target": name,
                               "detail": f"{name} free quota {pct:.1f}% left on {model} (< {QUOTA_CRITICAL_PCT:.0f}%). "
                                         "Auto-stop is ON for it, so it stops rather than bills - turn auto-stop "
                                         "off, swap the model, or add credit."})
            elif pct < QUOTA_LOW_PCT:
                issues.append({"severity": "digest", "kind": "quota_low", "target": name,
                               "detail": f"{name} free quota {pct:.1f}% left on {model} (< {QUOTA_LOW_PCT:.0f}%)."})
            # A guarded model that isn't the worst one still fails on its own
            # zero, and nothing above would ever mention it.
            others = [c for c in (r.get("guarded_models") or []) if c != model]
            if others and guarded is False:
                issues.append({"severity": "digest", "kind": "quota_guarded", "target": name,
                               "detail": f"{name} auto-stop still ON for: {', '.join(others)}. "
                                         "Those fail instead of billing when their grant runs out."})
            days = r.get("days_left")
            if days is not None and days <= QUOTA_EXPIRY_WARN_DAYS:
                issues.append({"severity": "digest", "kind": "quota_expiring", "target": name,
                               "detail": f"{name} free tier expires in {days}d ({r.get('expires')}) — unused grant is lost."})
            if r.get("missing_models"):
                # A tracked model that no longer resolves is either renamed or the
                # search/layout changed; either way its grant is unwatched.
                issues.append({"severity": "digest", "kind": "parse_failed", "target": name,
                               "detail": f"{name} free-tier row not found for: {', '.join(r['missing_models'])}"})
        elif r.get("metric") == "spend_cap":
            spend, cap = r.get("spend_usd"), r.get("cap_usd")
            if cap and cap > 0:
                frac = spend / cap
                if frac >= CRITICAL_CAP_FRAC:
                    issues.append({"severity": "urgent", "kind": "near_cap", "target": name,
                                   "detail": f"{name} spend ${spend:.2f} of ${cap:.0f} cap ({frac*100:.0f}%). API will suspend at the cap."})
                elif frac >= NEAR_CAP_FRAC:
                    issues.append({"severity": "digest", "kind": "approaching_cap", "target": name,
                                   "detail": f"{name} spend ${spend:.2f} of ${cap:.0f} cap ({frac*100:.0f}%)."})
    return issues


def report() -> dict:
    from driver.budget_state import save
    if not ensure_chrome(headless=True):
        result = {"ok": False, "checked_at": _now_iso(), "providers": [],
                  "issues": [{"severity": "urgent", "kind": "chrome_down", "target": "scraper",
                              "detail": f"persistent Chrome not reachable on :{CDP_PORT}"}],
                  "any_urgent": True}
        save("scrape", result)
        return result
    results = [_check(p) for p in PROVIDERS]
    issues = _derive_issues(results)
    result = {"ok": any(r.get("ok") for r in results), "checked_at": _now_iso(),
              "providers": results, "issues": issues,
              "any_urgent": any(i["severity"] == "urgent" for i in issues)}
    save("scrape", result)
    return result


def _emit(result: dict):
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("report")
    c = sub.add_parser("check")
    c.add_argument("name", choices=list(PROVIDERS))
    sub.add_parser("ensure-chrome")
    args = ap.parse_args()
    if args.cmd == "report":
        _emit(report())
    elif args.cmd == "check":
        if not ensure_chrome(headless=True):
            _emit({"ok": False, "provider": args.name, "error": f"Chrome not reachable on :{CDP_PORT}"})
        _emit(_check(args.name))
    elif args.cmd == "ensure-chrome":
        ok = ensure_chrome(headless=True)
        _emit({"ok": ok, "port": CDP_PORT})


if __name__ == "__main__":
    main()
