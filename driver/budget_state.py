"""
budget_state — persist + recall the API-budget monitoring results.

Both monitor_keys (5 providers, API) and scrape_stats (4 providers, console
scrape) call `save()` on every `report` run — cron OR manual — so there's
always a current snapshot to read back. We keep two things per source:

  - <kind>_latest.json   — the full last report (overwritten each run)
  - <kind>_history.jsonl — one compact line per run (append-only, all scans)

`show()` loads both latests and renders the unified 9-provider state, with a
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
            "balance_usd": p.get("balance_usd"),
            "spend_usd": p.get("spend_usd"),
            "cap_usd": p.get("cap_usd"),
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


def _fmt_provider(p: dict) -> str:
    name = p.get("provider", "?")
    if not p.get("ok"):
        return f"  {name:11} — {p.get('kind') or 'error'}: {(p.get('error') or '')[:48]}"
    metric = p.get("metric")
    if metric == "spend_cap" or (p.get("spend_usd") is not None and p.get("cap_usd")):
        spend, cap = p.get("spend_usd", 0.0), p.get("cap_usd")
        pend = f" +${p['pending_usd']:.2f} pending" if p.get("pending_usd") else ""
        return f"  {name:11} ${spend:>8.2f} / ${cap:g} cap{pend}"
    bal = p.get("balance_usd", 0.0)
    return f"  {name:11} ${bal:>8.2f}"


def render() -> str:
    out = ["API budget state — Werewolf provider keys", ""]
    any_data = False
    sev_rank = {"urgent": "🔴", "digest": "⚠️"}
    issue_lines = []
    for kind, name in (("keys", "monitor_keys (API)"), ("scrape", "scrape_stats (console)")):
        rep = load_latest(kind)
        if not rep:
            out.append(f"{name}: no run recorded yet")
            out.append("")
            continue
        any_data = True
        # Count providers live so the label never goes stale when one is added.
        label = name[:-1] + f" · {len(rep.get('providers', []))})"
        age_str, hrs = _age(rep.get("checked_at"))
        stale = " ⏰ STALE" if hrs > STALE_HOURS.get(kind, 24) else ""
        out.append(f"{label} — last run {rep.get('checked_at','?')} ({age_str}){stale}")
        for p in rep.get("providers", []):
            out.append(_fmt_provider(p))
        for i in rep.get("issues", []):
            issue_lines.append(f"  {sev_rank.get(i['severity'],'')} [{i['severity']}] {i['target']}: {i['detail']}")
        out.append("")
    if not any_data:
        return "No monitoring runs recorded yet. Run monitor_keys/scrape_stats report first."
    if issue_lines:
        out.append("Issues:")
        out.extend(issue_lines)
    else:
        out.append("No issues — all providers healthy.")
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
