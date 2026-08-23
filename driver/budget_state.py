"""
budget_state — persist + recall the API-budget monitoring results.

Both monitor_keys (5 providers, API) and scrape_stats (6 providers, console
scrape) call `save()` on every `report` run — cron OR manual — so there's
always a current snapshot to read back. We keep two things per source:

  - <kind>_latest.json   — the full last report (overwritten each run)
  - <kind>_history.jsonl — one compact line per run (append-only, all scans)

`show()` loads both latests and renders the unified 11-provider state, with a
staleness flag if a snapshot is older than its cadence. This is what answers
"what's my API budget state?" without re-hitting any provider.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

STATE_DIR = Path(__file__).resolve().parent.parent / "projects/werewolf-ops/state"
# How old a snapshot can be before we flag it stale (cadence + slack).
STALE_HOURS = {"keys": 16, "scrape": 30}  # keys twice-daily, scrape daily


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _compact(report: dict) -> dict:
    """One history line: timestamp + per-provider headline number + flags."""
    rows = []
    for p in report.get("providers", []):
        rows.append({
            "provider": p.get("provider"),
            "ok": p.get("ok"),
            # Failure kind is on the tape so `failure_streak` can tell "same
            # break, N runs running" from "a different thing broke today".
            # Added 2026-07-30; rows written before that have no "kind" and the
            # streak counter falls back to matching on ok:false alone.
            "kind": p.get("kind") if not p.get("ok") else None,
            "balance_usd": p.get("balance_usd"),
            "spend_usd": p.get("spend_usd"),
            "cap_usd": p.get("cap_usd"),
            # Qwen's headline isn't money — percent of its free-token grant left.
            "remaining_pct": p.get("remaining_pct"),
        })
    return {
        "checked_at": report.get("checked_at"),
        "any_urgent": report.get("any_urgent"),
        "providers": rows,
        "issues": [f"{i['severity']}:{i['target']}" for i in report.get("issues", [])],
    }


def save(kind: str, report: dict) -> None:
    """Persist a report: overwrite <kind>_latest.json, append <kind>_history.jsonl.
    Best-effort — never raises into the caller (monitoring must not break on IO)."""
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        latest = STATE_DIR / f"{kind}_latest.json"
        tmp = latest.with_suffix(".json.tmp")
        with tmp.open("w") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        tmp.replace(latest)  # atomic
        with (STATE_DIR / f"{kind}_history.jsonl").open("a") as f:
            f.write(json.dumps(_compact(report), ensure_ascii=False) + "\n")
    except OSError:
        pass


def failure_streak(kind: str, provider: str, failure_kind: str | None = None) -> int:
    """How many of the most recent runs in a row `provider` has been failing.

    Counts back from the newest history line and stops at the first run where
    the provider read OK (or wasn't in the run at all). When `failure_kind` is
    given, only runs failing the SAME way count — a parse_failed streak isn't
    extended by an unrelated reauth. History rows written before 2026-07-30
    carry no "kind"; those match any failure_kind rather than breaking a streak,
    so the check works on the existing tape.

    Returns PRIOR runs only — callers add the current run themselves. This is
    what lets a permanently-broken check escalate instead of emitting the same
    digest line forever (Mistral sat 3 days twice: 07-24 and 07-28).
    """
    try:
        with (STATE_DIR / f"{kind}_history.jsonl").open() as f:
            lines = f.readlines()
    except OSError:
        return 0
    streak = 0
    for line in reversed(lines):
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        match = next((p for p in row.get("providers", []) if p.get("provider") == provider), None)
        if match is None or match.get("ok"):
            break
        row_kind = match.get("kind")
        if failure_kind and row_kind and row_kind != failure_kind:
            break
        streak += 1
    return streak


def load_latest(kind: str) -> dict | None:
    try:
        with (STATE_DIR / f"{kind}_latest.json").open() as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def _age(checked_at: str | None) -> tuple[str, float]:
    """Return ('2h ago', hours) for an RFC3339 timestamp."""
    if not checked_at:
        return ("never", 1e9)
    try:
        dt = datetime.fromisoformat(checked_at.replace("Z", "+00:00"))
    except ValueError:
        return ("?", 1e9)
    hrs = (_now() - dt).total_seconds() / 3600
    if hrs < 1:
        return (f"{int(hrs*60)}m ago", hrs)
    if hrs < 48:
        return (f"{hrs:.1f}h ago", hrs)
    return (f"{hrs/24:.1f}d ago", hrs)


# ─── Report rendering ────────────────────────────────────────────────────────
#
# The report answers one question first: how much money is left on each key.
# Everything else is subordinate to that, which drives three choices here.
#
#   1. Grouped by WHAT THE NUMBER IS, not by which handler read it. Whether a
#      balance came from an API or a console scrape is our plumbing detail;
#      mixing a real balance, a postpaid spend-vs-cap and a token quota into one
#      list made three unlike things look alike.
#   2. Sorted ascending, with a total. What needs a top-up floats to the top.
#   3. Every row says how the number was obtained. A Tier-2 balance is DERIVED
#      (baseline minus cost-API spend), and a top-up Alex didn't tell us about
#      is invisible to it - so the row carries the baseline's age and asks for a
#      re-anchor once it's old. On 2026-08-22 a 13-day-old OpenAI baseline fired
#      a false CRITICAL after a top-up; the number looked exactly as trustworthy
#      as a directly-read one. Now it doesn't.

LOW_USD = 10.0
CRITICAL_USD = 3.0
BASELINE_STALE_DAYS = 14


def _days_since(date_str: str | None) -> int | None:
    try:
        d = datetime.fromisoformat(date_str).replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return None
    return (_now() - d).days


def _bucket(p: dict) -> str:
    """money = a balance that depletes · cap = postpaid metered spend · quota = free tokens."""
    if p.get("metric") == "quota" or p.get("remaining_pct") is not None:
        return "quota"
    if p.get("metric") == "spend_cap" or (p.get("spend_usd") is not None and p.get("cap_usd")):
        return "cap"
    return "money"


def _status(bal: float) -> str:
    if bal < CRITICAL_USD:
        return "CRITICAL"
    return "low" if bal < LOW_USD else "ok"


def _read_note(p: dict, kind: str, age_str: str, bal: float) -> str:
    """How this number was obtained, and how far to trust it."""
    if "baseline" in (p.get("source") or ""):
        days = _days_since(p.get("since"))
        if days is None:
            return "derived from a console baseline"
        # Prompt for a re-anchor when the derivation is about to cause action,
        # not only when the baseline is old. A derived balance under the low
        # threshold is the moment Alex reaches for his card - and the moment a
        # top-up he already made would be invisible. On 2026-08-22 the OpenAI
        # baseline was 13 days old (inside any sane staleness window) and the
        # $2.26 it produced was pure fiction: he had already topped up.
        prompt = days > BASELINE_STALE_DAYS or bal < LOW_USD
        return f"derived, baseline {days}d old{'  <-- RE-ANCHOR if topped up since' if prompt else ''}"
    return f"{'read live' if kind == 'keys' else 'scraped'} {age_str}"


def render() -> str:
    money, caps, quotas, broken, issue_lines, notes = [], [], [], [], [], []
    icon = {"urgent": "[!]", "digest": "[~]"}
    any_data = False

    for kind, label in (("keys", "API"), ("scrape", "console")):
        rep = load_latest(kind)
        if not rep:
            notes.append(f"{label} monitor has no run recorded yet")
            continue
        any_data = True
        age_str, hrs = _age(rep.get("checked_at"))
        if hrs > STALE_HOURS.get(kind, 24):
            notes.append(f"{label} snapshot is STALE: {age_str}, cadence is {STALE_HOURS[kind]}h")
        for p in rep.get("providers", []):
            row = (p, kind, age_str)
            if not p.get("ok"):
                broken.append(row)
            else:
                {"money": money, "cap": caps, "quota": quotas}[_bucket(p)].append(row)
        for i in rep.get("issues", []):
            issue_lines.append(f"  {icon.get(i['severity'], '')} {i['severity']:6} {i['target']:10} {i['detail']}")

    if not any_data:
        return "No monitoring runs recorded yet. Run monitor_keys/scrape_stats report first."

    # One set of keys, two live sites. Verified 2026-08-22: all 11 provider keys
    # in pokerwithai.net's .env are byte-identical to the werewolf Firestore map,
    # so every balance here is the COMBINED drain of both games and neither site's
    # spend is separable from the other's. Say so, rather than let the header keep
    # implying these numbers belong to Werewolf alone.
    out = ["API budget - shared game keys (aiwerewolf.net + pokerwithai.net)", ""]

    if money:
        money.sort(key=lambda r: r[0].get("balance_usd") or 0.0)
        out.append("MONEY LEFT (prepaid balances)")
        total = 0.0
        for p, kind, age_str in money:
            bal = p.get("balance_usd") or 0.0
            total += bal
            out.append(f"  {p['provider']:10} ${bal:>8.2f}   {_status(bal):8}  {_read_note(p, kind, age_str, bal)}")
        out.append(f"  {'':10} {'-' * 9}")
        out.append(f"  {'TOTAL':10} ${total:>8.2f}   across {len(money)} prepaid keys")
        out.append("")

    if caps:
        out.append("POSTPAID (metered against a cap - no balance to run out of)")
        for p, kind, age_str in caps:
            spend, cap = p.get("spend_usd") or 0.0, p.get("cap_usd") or 0.0
            pct = f"{spend / cap * 100:.0f}%" if cap else "?"
            pend = f", +${p['pending_usd']:.2f} pending" if p.get("pending_usd") else ""
            out.append(f"  {p['provider']:10} ${spend:>8.2f}   of ${cap:g} cap ({pct}){pend}")
        out.append("")

    if quotas:
        out.append("FREE GRANT (tokens, not money)")
        for p, kind, age_str in quotas:
            models = p.get("models") or []
            dead = [m for m in models if not (m.get("remaining_pct") or 0)]
            pct = p.get("remaining_pct") or 0.0
            # Headline is the WORST model, so say how many share that fate -
            # "0% on qwen3.8-max" reads like one model when all three are dry.
            spread = f", {len(dead)}/{len(models)} models exhausted" if models else ""
            billing = "spend now bills pay-as-you-go" if not p.get("auto_stop") else "auto-stop on, calls fail instead of billing"
            exp = f", expires {p['expires']} ({p['days_left']}d)" if p.get("days_left") is not None else ""
            out.append(f"  {p['provider']:10} {pct:>7.1f}% left{spread}{exp}")
            out.append(f"  {'':10} {billing}")
        out.append("")

    if broken:
        out.append("NOT READ")
        for p, kind, age_str in broken:
            out.append(f"  {p.get('provider', '?'):10} {p.get('kind') or 'error'}: {(p.get('error') or '')[:60]}")
        out.append("")

    if notes:
        out.extend(f"  ! {n}" for n in notes)
        out.append("")

    if issue_lines:
        out.append("ISSUES")
        out.extend(issue_lines)
    else:
        out.append("No issues - all providers healthy.")
    return "\n".join(out)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("show", help="Unified last-run state across both monitors (default)")
    h = sub.add_parser("history", help="Recent runs from history")
    h.add_argument("kind", choices=["keys", "scrape"])
    h.add_argument("-n", type=int, default=10)
    args = ap.parse_args()
    if args.cmd == "history":
        path = STATE_DIR / f"{args.kind}_history.jsonl"
        lines = path.read_text().splitlines() if path.exists() else []
        for ln in lines[-args.n:]:
            print(ln)
    else:
        print(render())


if __name__ == "__main__":
    main()
