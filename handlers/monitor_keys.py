"""
monitor_keys — low-balance watch for the Werewolf game's free-tier API keys.

The Werewolf game (aiwerewolf.net) runs its free tier on a set of provider
keys Alex funds. They live in Firestore at `/config/freeTierApiKeys` as a
map `{keys: {<API_KEY_CONSTANTS name>: "<value>"}}`. Strangers playing the
free tier burn Alex's prepaid credit; the only thing he had before this was
manually eyeballing each provider's dashboard.

Of the 8 providers, only three expose a programmatic balance endpoint:
  - DeepSeek  — GET https://api.deepseek.com/user/balance      (normal key)
  - Moonshot  — GET https://api.moonshot.ai/v1/users/me/balance (normal key)
  - xAI/Grok  — needs a separate *management* key (not wired here yet)
The other five (OpenAI, Anthropic, Google, Mistral, GLM/Z.AI) have no balance
API — those are Tier 2 (estimate = recorded top-up minus game spend).

This handler covers the API-checkable providers (Tier 1: DeepSeek, Moonshot).
It returns deterministic JSON snapshots; Marlow's session turns the `issues`
array into a Telegram alert / digest entry.

Credentials:
  - Firestore read: a *read-only* service account (roles/datastore.viewer).
    Point `MARLOW_FIREBASE_CREDS` at its JSON key file. Fails clean if unset.
  - Provider keys: read live from `/config/freeTierApiKeys` — never copied
    into env, so they can't go stale when Alex rotates them.

CLI:
    python handlers/monitor_keys.py check-deepseek
    python handlers/monitor_keys.py check-moonshot
    python handlers/monitor_keys.py report   → both + derived `issues`
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

# Mirror plist env so a standalone `uv run python handlers/monitor_keys.py`
# sees the same secrets a launchd-fired tick sees.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from driver.env_loader import import_plist_env  # noqa: E402
import_plist_env()

# Firestore document holding the free-tier keys, and the map entry names
# (mirror API_KEY_CONSTANTS in the game's app/ai/ai-models.ts).
FREE_TIER_DOC = ("config", "freeTierApiKeys")
KEY_DEEPSEEK = "DEEPSEEK_API_KEY"
KEY_MOONSHOT = "MOONSHOT_API_KEY"

# Provider bases — overridable because China-origin providers have divergent
# .cn / international hosts; pin whichever the funded key actually belongs to.
DEEPSEEK_BASE = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
MOONSHOT_BASE = os.environ.get("MOONSHOT_BASE_URL", "https://api.moonshot.ai")
XAI_MGMT_BASE = os.environ.get("XAI_MANAGEMENT_BASE_URL", "https://management-api.x.ai")

# xAI/Grok is checked via the *management* API, not the inference key, and not
# via Firestore: the management key isn't a game key (the game never uses it),
# it's Marlow monitoring infra. So it comes from Marlow's own env, set in the
# launchd plist alongside MARLOW_FIREBASE_CREDS. Both must be present or xAI is
# skipped (no setup → no noise). NOTE: this management endpoint is undocumented
# and xAI may change it without notice — hence the defensive parsing below.
ENV_XAI_KEY = "XAI_MGMT_KEY"
ENV_XAI_TEAM = "XAI_TEAM_ID"

# Tier 2 — providers with NO balance API but WITH an admin cost/usage API.
# These accounts are shared across Alex's other projects (NOT game-dedicated),
# so game spend can't estimate them; only the provider's own cost API counts
# all usage. Model: remaining = a baseline Alex reads from the console once
# (stored in TIER2_BASELINES) minus cumulative spend since that baseline date
# (from the cost API). Admin keys are Marlow monitoring infra → env, not the
# game's Firestore key map. Each provider is opt-in: included only when BOTH
# its admin key (env) and its baseline entry exist.
OPENAI_BASE = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com")
ANTHROPIC_BASE = os.environ.get("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
ENV_OPENAI_ADMIN = "OPENAI_ADMIN_KEY"
ENV_ANTHROPIC_ADMIN = "ANTHROPIC_ADMIN_KEY"
ANTHROPIC_VERSION = "2023-06-01"

# Baselines file: {provider: {remaining_usd: float, since: "YYYY-MM-DD"}}.
# Alex updates remaining_usd + since whenever he tops up a provider. Lives in
# the repo (versioned, not secret); override path via env for tests.
TIER2_BASELINES = Path(
    os.environ.get(
        "TIER2_BASELINES_PATH",
        str(Path(__file__).resolve().parent.parent / "projects/werewolf-ops/config/tier2_baselines.json"),
    )
)

# Alert thresholds in USD-equivalent (tune later via editorial feedback).
LOW_USD = 10.0       # digest: top up soon
CRITICAL_USD = 3.0   # urgent: about to go dry
CNY_PER_USD = 7.1    # approximate; only to normalize a CNY balance for thresholding

HTTP_TIMEOUT = 20


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _checked_at() -> str:
    return _now_utc().replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _to_usd(amount: float, currency: str) -> float:
    cur = (currency or "USD").upper()
    if cur == "CNY":
        return amount / CNY_PER_USD
    return amount


# ─── Firestore: read the live free-tier key map ──────────────────────────────


def _load_free_tier_keys() -> dict[str, str]:
    """Read `/config/freeTierApiKeys` and return its inner `keys` map.

    Raises RuntimeError (caught by callers) if creds/dep are missing so the
    handler degrades to a clean `ok: false` rather than crashing.
    """
    creds_path = os.environ.get("MARLOW_FIREBASE_CREDS")
    if not creds_path:
        raise RuntimeError("MARLOW_FIREBASE_CREDS not set (read-only service-account JSON)")
    if not Path(creds_path).exists():
        raise RuntimeError(f"MARLOW_FIREBASE_CREDS points at missing file: {creds_path}")
    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
    except ImportError as e:
        raise RuntimeError("firebase-admin not installed (add it to Marlow's deps)") from e

    # Named app so we don't collide with any default app in the same process.
    app_name = "marlow-readonly"
    try:
        app = firebase_admin.get_app(app_name)
    except ValueError:
        app = firebase_admin.initialize_app(credentials.Certificate(creds_path), name=app_name)

    db = firestore.client(app)
    snap = db.collection(FREE_TIER_DOC[0]).document(FREE_TIER_DOC[1]).get()
    if not snap.exists:
        raise RuntimeError(f"Firestore doc /{FREE_TIER_DOC[0]}/{FREE_TIER_DOC[1]} not found")
    data = snap.to_dict() or {}
    keys = data.get("keys") or {}
    if not isinstance(keys, dict):
        raise RuntimeError("freeTierApiKeys.keys is not a map")
    return keys


# ─── Provider balance checks ─────────────────────────────────────────────────


def _check_deepseek(key: str) -> dict:
    """GET /user/balance → {is_available, balance_infos:[{currency,total_balance,...}]}."""
    try:
        resp = requests.get(
            f"{DEEPSEEK_BASE}/user/balance",
            headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
            timeout=HTTP_TIMEOUT,
        )
    except requests.RequestException as e:
        return {"provider": "deepseek", "ok": False, "error": f"request failed: {e}"}
    if resp.status_code != 200:
        return {
            "provider": "deepseek",
            "ok": False,
            "http_status": resp.status_code,
            "error": resp.text[:200],
        }
    data = resp.json()
    infos = data.get("balance_infos") or []
    primary = infos[0] if infos else {}
    currency = primary.get("currency", "USD")
    try:
        native = float(primary.get("total_balance", 0))
    except (TypeError, ValueError):
        native = 0.0
    return {
        "provider": "deepseek",
        "ok": True,
        "is_available": bool(data.get("is_available")),
        "currency": currency,
        "balance_native": native,
        "balance_usd": round(_to_usd(native, currency), 4),
        "balance_infos": infos,
    }


def _check_moonshot(key: str) -> dict:
    """GET /v1/users/me/balance → {data:{available_balance, voucher_balance, cash_balance}} (USD)."""
    try:
        resp = requests.get(
            f"{MOONSHOT_BASE}/v1/users/me/balance",
            headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
            timeout=HTTP_TIMEOUT,
        )
    except requests.RequestException as e:
        return {"provider": "moonshot", "ok": False, "error": f"request failed: {e}"}
    if resp.status_code != 200:
        return {
            "provider": "moonshot",
            "ok": False,
            "http_status": resp.status_code,
            "error": resp.text[:200],
        }
    data = resp.json()
    body = data.get("data") or {}
    try:
        native = float(body.get("available_balance", 0))
    except (TypeError, ValueError):
        native = 0.0
    return {
        "provider": "moonshot",
        "ok": True,
        "is_available": native > 0,
        "currency": "USD",
        "balance_native": native,
        "balance_usd": round(native, 4),
        "raw": body,
    }


def _xai_cents(obj) -> int | None:
    """Parse an xAI {"val": "<cents>"} money object to a signed int, or None."""
    try:
        return int((obj or {}).get("val"))
    except (TypeError, ValueError):
        return None


def _check_xai_ledger(key: str, team_id: str) -> dict:
    """Fallback: GET /prepaid/balance → {total:{val}}. `total.val` is USD *cents*,
    sign inverted (PURCHASE negative, SPEND positive) so remaining = -total/100.
    This is the raw prepaid ledger; it LAGS the console's "Credits remaining" by
    the current period's not-yet-posted usage. Used only if the invoice preview
    (which nets that usage out) is unavailable."""
    try:
        resp = requests.get(
            f"{XAI_MGMT_BASE}/v1/billing/teams/{team_id}/prepaid/balance",
            headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
            timeout=HTTP_TIMEOUT,
        )
    except requests.RequestException as e:
        return {"provider": "xai", "ok": False, "error": f"request failed: {e}"}
    if resp.status_code != 200:
        return {"provider": "xai", "ok": False, "http_status": resp.status_code, "error": resp.text[:200]}
    cents = _xai_cents(resp.json().get("total"))
    if cents is None:
        return {"provider": "xai", "ok": False, "error": "unexpected prepaid/balance total"}
    bal = round(-cents / 100.0, 4)
    return {
        "provider": "xai", "ok": True, "is_available": bal > 0, "currency": "USD",
        "balance_native": bal, "balance_usd": bal, "source": "prepaid/balance (ledger, approximate)",
        "approximate": True,
    }


def _check_xai_balance(key: str, team_id: str) -> dict:
    """True spendable balance from GET /postpaid/invoice/preview.

    The raw prepaid ledger (`/prepaid/balance`) lags by the current billing
    period's metered-but-unposted usage — it reads HIGH, the dangerous direction
    for a low-balance alarm. The invoice preview nets that out and matches the
    console's "Credits remaining" to the penny. From `coreInvoice` (USD cents,
    sign inverted like the ledger):
        prepaidCredits      = remaining prepaid ledger      (e.g. -258 → $2.58)
        prepaidCreditsUsed  = used against it this period   (e.g. -160 → $1.60)
        spendable = (-prepaidCredits) - (-prepaidCreditsUsed) = $0.98
    Falls back to the raw ledger if the preview is unavailable or lacks fields.
    Endpoint is undocumented and may change without notice → defensive parse.
    """
    try:
        resp = requests.get(
            f"{XAI_MGMT_BASE}/v1/billing/teams/{team_id}/postpaid/invoice/preview",
            headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
            timeout=HTTP_TIMEOUT,
        )
    except requests.RequestException:
        return _check_xai_ledger(key, team_id)
    if resp.status_code != 200:
        return _check_xai_ledger(key, team_id)

    core = (resp.json() or {}).get("coreInvoice") or {}
    ledger_cents = _xai_cents(core.get("prepaidCredits"))
    used_cents = _xai_cents(core.get("prepaidCreditsUsed"))
    if ledger_cents is None:
        return _check_xai_ledger(key, team_id)  # preview present but unusable

    ledger_usd = -ledger_cents / 100.0
    used_usd = (-used_cents / 100.0) if used_cents is not None else 0.0
    spendable = round(ledger_usd - used_usd, 4)
    return {
        "provider": "xai",
        "ok": True,
        "is_available": spendable > 0,
        "currency": "USD",
        "balance_native": spendable,
        "balance_usd": spendable,            # true "Credits remaining" (console-accurate)
        "ledger_balance_usd": round(ledger_usd, 4),   # raw prepaid ledger (pre-usage)
        "period_usage_usd": round(used_usd, 4),       # unposted current-period usage
        "source": "postpaid/invoice/preview",
    }


def check_xai() -> dict:
    """Read management key + team id from Marlow env (NOT Firestore). Fails
    clean if either is unset so report() can simply skip an unconfigured xAI."""
    key = os.environ.get(ENV_XAI_KEY)
    team_id = os.environ.get(ENV_XAI_TEAM)
    if not key:
        return {"provider": "xai", "ok": False, "error": f"{ENV_XAI_KEY} not set (management key)"}
    if not team_id:
        return {"provider": "xai", "ok": False, "error": f"{ENV_XAI_TEAM} not set"}
    return _check_xai_balance(key, team_id)


def _xai_configured() -> bool:
    return bool(os.environ.get(ENV_XAI_KEY) and os.environ.get(ENV_XAI_TEAM))


# ─── Tier 2: cost-API + console baseline (OpenAI, Anthropic) ─────────────────


def _load_baselines() -> dict:
    """Read the Tier-2 baselines file. Returns {} if absent/unparseable so a
    provider with no baseline is simply skipped rather than erroring."""
    try:
        with TIER2_BASELINES.open() as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def _baseline_for(provider: str) -> dict | None:
    b = _load_baselines().get(provider)
    if not isinstance(b, dict) or "remaining_usd" not in b or "since" not in b:
        return None
    return b


def set_baseline(provider: str, remaining_usd: float, since: str | None = None) -> dict:
    """Re-anchor a Tier-2 baseline: record `remaining_usd` as of `since`
    (default today UTC). Creates the file/dirs if missing. This is the one
    thing to run after a top-up (or to clear drift). Idempotent per provider."""
    since = since or _now_utc().date().isoformat()
    data = _load_baselines()
    data[provider] = {"remaining_usd": round(float(remaining_usd), 4), "since": since}
    TIER2_BASELINES.parent.mkdir(parents=True, exist_ok=True)
    with TIER2_BASELINES.open("w") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")
    return {"ok": True, "provider": provider, "baseline": data[provider], "path": str(TIER2_BASELINES)}


def _since_to_unix(since: str) -> int:
    """'YYYY-MM-DD' (UTC midnight) → unix seconds. Also accepts full RFC3339."""
    s = since.strip()
    dt = datetime.fromisoformat(s.replace("Z", "+00:00")) if "T" in s else datetime.fromisoformat(s + "T00:00:00+00:00")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp())


def _since_to_rfc3339(since: str) -> str:
    return datetime.fromtimestamp(_since_to_unix(since), tz=timezone.utc).isoformat().replace("+00:00", "Z")


def _openai_spend_since(admin_key: str, start_unix: int) -> float:
    """Sum GET /v1/organization/costs over [start_unix, now]. Amounts are USD
    floats at data[].results[].amount.value. Paginates via next_page."""
    total = 0.0
    page = None
    headers = {"Authorization": f"Bearer {admin_key}", "Accept": "application/json"}
    for _ in range(60):  # hard cap on pages — ~60 days of 1d buckets at limit 1, far more in practice
        params = {"start_time": start_unix, "bucket_width": "1d", "limit": 180}
        if page:
            params["page"] = page
        resp = requests.get(f"{OPENAI_BASE}/v1/organization/costs", headers=headers, params=params, timeout=HTTP_TIMEOUT)
        if resp.status_code != 200:
            raise _ProviderError(resp.status_code, resp.text[:200])
        body = resp.json()
        for bucket in body.get("data") or []:
            for r in bucket.get("results") or []:
                total += float((r.get("amount") or {}).get("value", 0) or 0)
        if body.get("has_more") and body.get("next_page"):
            page = body["next_page"]
        else:
            break
    return round(total, 6)


def _anthropic_spend_since(admin_key: str, starting_at: str) -> float:
    """Sum GET /v1/organizations/cost_report over [starting_at, now]. Amounts
    are *cents* as decimal strings → /100 for USD. Paginates via next_page."""
    total_cents = 0.0
    page = None
    # Anthropic's cost_report only returns COMPLETED 1d buckets — it rejects a
    # range covering only the current (incomplete) day ("ending must be after
    # starting"). So end the range at TODAY's UTC midnight (the last complete
    # boundary). If the baseline starts today, there's no completed bucket yet →
    # spend is 0 (today's usage posts in tomorrow's bucket; the baseline already
    # reflects today, so no gap and no double-count).
    ending_at = f"{_now_utc().date().isoformat()}T00:00:00Z"
    if starting_at >= ending_at:  # same RFC3339 format → lexicographic compare is valid
        return 0.0
    headers = {"x-api-key": admin_key, "anthropic-version": ANTHROPIC_VERSION, "Accept": "application/json"}
    for _ in range(60):
        params = {"starting_at": starting_at, "ending_at": ending_at, "bucket_width": "1d", "limit": 31}
        if page:
            params["page"] = page
        resp = requests.get(f"{ANTHROPIC_BASE}/v1/organizations/cost_report", headers=headers, params=params, timeout=HTTP_TIMEOUT)
        if resp.status_code != 200:
            raise _ProviderError(resp.status_code, resp.text[:200])
        body = resp.json()
        for bucket in body.get("data") or []:
            for r in bucket.get("results") or []:
                try:
                    total_cents += float(r.get("amount", 0) or 0)
                except (TypeError, ValueError):
                    pass
        if body.get("has_more") and body.get("next_page"):
            page = body["next_page"]
        else:
            break
    return round(total_cents / 100.0, 6)


class _ProviderError(Exception):
    def __init__(self, status: int, text: str):
        self.status = status
        self.text = text
        super().__init__(f"HTTP {status}: {text}")


def _check_cost_based(provider: str, admin_key_env: str, spend_fn, since_arg_fn) -> dict:
    """Shared Tier-2 path: remaining = baseline.remaining_usd − spend(since→now)."""
    admin_key = os.environ.get(admin_key_env)
    baseline = _baseline_for(provider)
    if not admin_key:
        return {"provider": provider, "ok": False, "error": f"{admin_key_env} not set (admin key)"}
    if not baseline:
        return {"provider": provider, "ok": False, "error": f"no baseline for {provider} in {TIER2_BASELINES.name}"}
    try:
        spend = spend_fn(admin_key, since_arg_fn(baseline["since"]))
    except _ProviderError as e:
        return {"provider": provider, "ok": False, "http_status": e.status, "error": e.text}
    except requests.RequestException as e:
        return {"provider": provider, "ok": False, "error": f"request failed: {e}"}
    try:
        base_usd = float(baseline["remaining_usd"])
    except (TypeError, ValueError):
        return {"provider": provider, "ok": False, "error": "baseline.remaining_usd not a number"}
    remaining = round(base_usd - spend, 4)
    return {
        "provider": provider,
        "ok": True,
        "is_available": remaining > 0,
        "currency": "USD",
        "balance_native": remaining,
        "balance_usd": remaining,
        "baseline_usd": round(base_usd, 4),
        "spend_since_usd": round(spend, 4),
        "since": baseline["since"],
        "source": "cost API − console baseline",
    }


def check_openai() -> dict:
    return _check_cost_based("openai", ENV_OPENAI_ADMIN, _openai_spend_since, _since_to_unix)


def check_anthropic() -> dict:
    return _check_cost_based("anthropic", ENV_ANTHROPIC_ADMIN, _anthropic_spend_since, _since_to_rfc3339)


def _cost_provider_configured(provider: str, admin_key_env: str) -> bool:
    return bool(os.environ.get(admin_key_env) and _baseline_for(provider))


_CHECKERS = {
    "deepseek": (KEY_DEEPSEEK, _check_deepseek),
    "moonshot": (KEY_MOONSHOT, _check_moonshot),
}


def _check_one(provider: str) -> dict:
    key_name, fn = _CHECKERS[provider]
    try:
        keys = _load_free_tier_keys()
    except RuntimeError as e:
        return {"provider": provider, "ok": False, "error": str(e)}
    key = keys.get(key_name)
    if not key:
        return {"provider": provider, "ok": False, "error": f"{key_name} missing from freeTierApiKeys"}
    return fn(key)


def check_deepseek() -> dict:
    return _check_one("deepseek")


def check_moonshot() -> dict:
    return _check_one("moonshot")


# ─── Report + derived issues ─────────────────────────────────────────────────


def _derive_issues(providers: list[dict]) -> list[dict]:
    issues: list[dict] = []
    for p in providers:
        name = p["provider"]
        if not p.get("ok"):
            # 401/403 means the key is dead/revoked — urgent. Other errors are
            # likely transient (network, 5xx) — surface as digest, not alarm.
            status = p.get("http_status")
            severity = "urgent" if status in (401, 403) else "digest"
            issues.append({
                "severity": severity,
                "kind": "balance_check_failed",
                "target": name,
                "detail": f"could not read balance: {p.get('error', 'unknown')}"
                          + (f" (HTTP {status})" if status else ""),
            })
            continue
        usd = p.get("balance_usd", 0.0)
        if not p.get("is_available") or usd <= 0:
            issues.append({
                "severity": "urgent",
                "kind": "balance_empty",
                "target": name,
                "detail": f"{name} key is dry — free tier will fail. Top up now.",
            })
        elif usd < CRITICAL_USD:
            issues.append({
                "severity": "urgent",
                "kind": "balance_critical",
                "target": name,
                "detail": f"{name} balance ${usd:.2f} (< ${CRITICAL_USD:.0f}). Top up now.",
            })
        elif usd < LOW_USD:
            issues.append({
                "severity": "digest",
                "kind": "balance_low",
                "target": name,
                "detail": f"{name} balance ${usd:.2f} (< ${LOW_USD:.0f}). Top up soon.",
            })
    return issues


def report() -> dict:
    providers = [check_deepseek(), check_moonshot()]
    # xAI is opt-in: only check it once the management key + team id are wired,
    # otherwise it would emit a "not set" digest issue on every run.
    if _xai_configured():
        providers.append(check_xai())
    # Tier-2 cost-API providers, each opt-in on (admin key + baseline).
    if _cost_provider_configured("openai", ENV_OPENAI_ADMIN):
        providers.append(check_openai())
    if _cost_provider_configured("anthropic", ENV_ANTHROPIC_ADMIN):
        providers.append(check_anthropic())
    # ok:false only when *every* provider failed to read (e.g. creds missing) —
    # a single provider hiccup shouldn't mask the others.
    all_failed = all(not p.get("ok") for p in providers)
    issues = _derive_issues(providers)
    return {
        "ok": not all_failed,
        "checked_at": _checked_at(),
        "providers": providers,
        "issues": issues,
        "any_urgent": any(i["severity"] == "urgent" for i in issues),
    }


# ─── CLI ─────────────────────────────────────────────────────────────────────


def _emit(result: dict):
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check-deepseek", help="DeepSeek free-tier key balance")
    sub.add_parser("check-moonshot", help="Moonshot free-tier key balance")
    sub.add_parser("check-xai", help="xAI/Grok prepaid balance (management API)")
    sub.add_parser("check-openai", help="OpenAI remaining = baseline − cost since (admin key)")
    sub.add_parser("check-anthropic", help="Anthropic remaining = baseline − cost since (admin key)")
    p_sb = sub.add_parser("set-baseline", help="Re-anchor a Tier-2 baseline after a top-up")
    p_sb.add_argument("provider", choices=["openai", "anthropic"])
    p_sb.add_argument("remaining_usd", type=float, help="Current 'credits remaining' from the provider console")
    p_sb.add_argument("--since", help="Anchor date YYYY-MM-DD (default: today UTC)")
    sub.add_parser("report", help="All API-checkable balances + derived issues")
    args = parser.parse_args()
    if args.cmd == "check-deepseek":
        _emit(check_deepseek())
    elif args.cmd == "check-moonshot":
        _emit(check_moonshot())
    elif args.cmd == "check-xai":
        _emit(check_xai())
    elif args.cmd == "check-openai":
        _emit(check_openai())
    elif args.cmd == "check-anthropic":
        _emit(check_anthropic())
    elif args.cmd == "set-baseline":
        _emit(set_baseline(args.provider, args.remaining_usd, args.since))
    elif args.cmd == "report":
        _emit(report())


if __name__ == "__main__":
    main()
