"""
scrape_stats — console scraping for the 4 Werewolf providers that have NO usable
balance/cost API (so they can't go through monitor_keys):

  - GLM / Z.AI   → cash + credits balance        (a real depleting balance)
  - Gemini       → spend vs. billing tier cap     (postpaid, pay-as-you-go)
  - Mistral      → month usage vs. spending limit  (postpaid)
  - Sakana Fugu  → prepaid credit balance          (a real depleting balance)

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
    python handlers/scrape_stats.py report          # all three + derived issues
    python handlers/scrape_stats.py check <name>     # one provider (glm|gemini|mistral)
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
HTTP_TIMEOUT = 60

# Balance thresholds (GLM) — mirror monitor_keys.
LOW_USD = 10.0
CRITICAL_USD = 3.0
# Spend-vs-cap fraction thresholds (Gemini, Mistral): how close to the cap.
NEAR_CAP_FRAC = 0.80      # digest
CRITICAL_CAP_FRAC = 0.95  # urgent


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


def _navigate_and_extract(url: str, js: str, click_js: str | None = None,
                          settle_s: float = NAV_SETTLE_S) -> dict:
    """Navigate tab 0 to `url`, let it settle, optionally run `click_js` to
    reveal a sub-view (then settle again), run `js` (must return a JSON string),
    parse it. Returns the parsed dict, or {error:...} on failure."""
    nav = _cli("navigate", url, "--tab", "0")
    if nav.returncode != 0:
        return {"error": f"navigate failed: {nav.stderr[:160] or nav.stdout[:160]}"}
    time.sleep(settle_s)
    if click_js:
        _cli("js", click_js, "--tab", "0")
        time.sleep(settle_s)
    res = _cli("js", js, "--tab", "0")
    if res.returncode != 0:
        return {"error": f"js failed: {res.stderr[:160] or res.stdout[:160]}"}
    try:
        outer = json.loads(res.stdout)          # cli wraps as {"result": "<json string>"}
        return json.loads(outer["result"])
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        return {"error": f"unparseable extractor output: {e}"}


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

# Gemini is the awkward one: spend lives behind the "Spend" toggle on the usage
# view, and the $250 tier cap is on a different (billing) page. So we click into
# the Spend view, read the spend total, and treat the cap as a configured
# constant (a billing setting Alex controls; re-confirm if he changes it).
GEMINI_CAP_USD = float(os.environ.get("GEMINI_SPEND_CAP", "250"))
GEMINI = {
    "name": "gemini",
    "url": "https://aistudio.google.com/usage",
    "click_js": """(()=>{const b=[...document.querySelectorAll('button,a,[role=tab],span,div')].find(x=>x.textContent.trim()==='Spend'&&x.offsetParent!==null); if(b){b.click(); return 'clicked';} return 'no-spend-tab';})()""",
    "js": """(()=>{
      if(/accounts\\.google\\.com\\/v3\\/signin|ServiceLogin/i.test(location.href)) return JSON.stringify({login_wall:true});
      const t=document.body.innerText;
      // Spend view shows $ amounts; the period total is the largest of them.
      const all=[...t.matchAll(/\\$\\s*([0-9][0-9,]*\\.?[0-9]*)/g)].map(m=>parseFloat(m[1].replace(/,/g,'')));
      const spend = all.length ? Math.max(...all) : null;
      return JSON.stringify({login_wall:false, spend});
    })()""",
}

MISTRAL = {
    "name": "mistral",
    "url": "https://admin.mistral.ai/organization/billing",
    "js": """(()=>{
      const t=document.body.innerText;
      if(/auth\\.mistral|\\/login/i.test(location.href)) return JSON.stringify({login_wall:true});
      const num=(re)=>{const m=t.match(re); return m?parseFloat(m[1].replace(/,/g,'')):null;};
      return JSON.stringify({login_wall:false,
        usage: num(/Usage:\\s*\\$([0-9][0-9,]*\\.?[0-9]*)/i),
        pending: num(/Including \\$([0-9][0-9,]*\\.?[0-9]*) in pending/i),
        limit: num(/Monthly limit:\\s*\\$([0-9][0-9,]*\\.?[0-9]*)/i)});
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

PROVIDERS = {p["name"]: p for p in (GLM, GEMINI, MISTRAL, SAKANA)}


# ─── Normalize each provider's raw extract into a common shape ───────────────


def _last_balance(provider: str) -> float | None:
    """Last successfully-read balance for `provider` from the saved snapshot."""
    from driver.budget_state import load_latest
    rep = load_latest("scrape") or {}
    for p in rep.get("providers", []):
        if p.get("provider") == provider and p.get("ok"):
            return p.get("balance_usd")
    return None


def _check(provider: str) -> dict:
    cfg = PROVIDERS[provider]
    raw = _navigate_and_extract(cfg["url"], cfg["js"], cfg.get("click_js"))
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
                retry = _navigate_and_extract(cfg["url"], cfg["js"], cfg.get("click_js"), settle_s=settle)
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
        spend = raw.get("spend")
        if spend is None:
            return {**base, "ok": False, "kind": "parse_failed", "error": "no spend figure found in Spend view"}
        return {**base, "ok": True, "metric": "spend_cap", "spend_usd": round(spend, 4), "cap_usd": GEMINI_CAP_USD}
    if provider == "mistral":
        usage, limit, pending = raw.get("usage"), raw.get("limit"), raw.get("pending")
        if usage is None:
            return {**base, "ok": False, "kind": "parse_failed", "error": "no usage figure found"}
        return {**base, "ok": True, "metric": "spend_cap", "spend_usd": round(usage, 4),
                "cap_usd": limit, "pending_usd": pending}
    if provider == "sakana":
        bal = raw.get("balance")
        if bal is None:
            return {**base, "ok": False, "kind": "parse_failed", "error": "no credit balance found"}
        # Same SPA placeholder hazard as GLM: the billing tab can paint "$0.00"
        # before the balance request lands. Never trust a lone zero — re-read
        # with longer settles before believing the credit is dry.
        if bal == 0:
            for settle in (10.0, 15.0):
                retry = _navigate_and_extract(cfg["url"], cfg["js"], settle_s=settle)
                r_bal = retry.get("balance")
                if r_bal is None:
                    continue
                bal = r_bal
                if bal > 0:
                    break
            if bal == 0:
                prev = _last_balance("sakana")
                if prev and prev > 0:
                    return {**base, "ok": False, "kind": "suspect_zero",
                            "error": f"reads $0.00 across retries but last run saw ${prev:.2f} — "
                                     "likely placeholder render; verify in console before topping up"}
        return {**base, "ok": True, "metric": "balance", "balance_usd": round(bal, 4),
                "usage_usd": raw.get("usage"), "is_available": bal > 0}
    return {**base, "ok": False, "kind": "parse_failed", "error": "unknown provider"}


def _derive_issues(results: list[dict]) -> list[dict]:
    issues = []
    for r in results:
        name = r["provider"]
        if not r.get("ok"):
            sev = "urgent" if r.get("kind") == "reauth" else "digest"
            issues.append({"severity": sev, "kind": r.get("kind", "error"), "target": name, "detail": r.get("error", "")})
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
