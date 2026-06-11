"""
werewolf_stats — daily user-activity snapshot for the Werewolf game.

Companion to monitor_keys: that watches what the free tier *costs* (provider
balances); this watches what the free tier *produces* (signups, games, burn).
Both read the same Firestore via the same read-only service account.

v1 metrics (what Alex asked for — "start with this, we can add more"):
  1. New users     — created today / 7d / 30d, plus total + tier split.
  2. Games created — started today / 7d / 30d, plus total.
  3. Money spent   — the free tier's AI burn, two honest cuts (see below).

Money, carefully:
  `games.totalGameCost` is the provider cost a game has run up *so far*. It
  GROWS as the game is played across days, so summing the cost of games
  *created today* undercounts them (they just started). So we report two cuts:
    - created_cost_usd  — Σ totalGameCost of games CREATED in the window.
      "What this window's games have cost so far." A lower bound; keeps rising.
    - live_cost_usd     — Σ totalGameCost across ALL current (≤30d) games.
      The running cumulative. The day-over-day DELTA of this number (from the
      snapshot history) is the *true money spent that day*. We compute that
      delta here as `daily_burn_usd` when a prior snapshot exists.
  This is why we snapshot: games auto-expire after 30 days (Firestore TTL on
  `expireAt`), so without a daily history the burn series is unrecoverable.

  User-side spend (`users.spendings`, monthly free/api/paid buckets) is carried
  as a secondary `user_spend_mtd_usd` line. NOT revenue: `free` is OUR cost
  (free-tier credits), `api` is users' own API keys (never our money), and only
  `paid` is actual paid-tier income. Today `paid` is ~$0, so this is almost
  entirely consumption — the right field to watch if a paid tier ever grows,
  but do not read the total as money coming in.

Credentials: MARLOW_FIREBASE_CREDS → the read-only service-account JSON
(roles/datastore.viewer). Same wiring as monitor_keys; fails clean if unset.

CLI:
    python handlers/werewolf_stats.py report   → full JSON snapshot, persisted
    python handlers/werewolf_stats.py show      → last snapshot, human-readable
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Mirror plist env so a standalone `uv run python handlers/werewolf_stats.py`
# sees the same secrets a launchd-fired tick sees.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from driver.env_loader import import_plist_env  # noqa: E402
import_plist_env()

# Reuse monitor_keys' Firestore init so creds/app handling stays single-sourced.
from handlers.monitor_keys import _firestore_db  # noqa: E402
from driver.budget_state import STATE_DIR  # noqa: E402

USERS = "users"
GAMES = "games"

# created_at (users) is a Firestore Timestamp; createdAt (games) is epoch millis.
# Two windows' worth of cutoffs, computed once per run off a single "now".


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _checked_at(now: datetime) -> str:
    return now.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _day_start(now: datetime) -> datetime:
    return now.replace(hour=0, minute=0, second=0, microsecond=0)


def _windows(now: datetime) -> dict[str, datetime]:
    """UTC cutoffs: 'today' = since UTC-midnight; 7d/30d = rolling."""
    return {
        "today": _day_start(now),
        "7d": now - timedelta(days=7),
        "30d": now - timedelta(days=30),
    }


# ─── Users ───────────────────────────────────────────────────────────────────


def _count(query) -> int:
    """Run a Firestore count() aggregation → int (no per-doc reads)."""
    return int(query.count().get()[0][0].value)


def _user_stats(db, now: datetime) -> dict:
    from google.cloud.firestore_v1 import FieldFilter

    col = db.collection(USERS)
    wins = _windows(now)
    new = {k: _count(col.where(filter=FieldFilter("created_at", ">=", cut)))
           for k, cut in wins.items()}
    total = _count(col)
    tiers = {t: _count(col.where(filter=FieldFilter("tier", "==", t)))
             for t in ("free", "api", "paid")}

    # Today's new-user emails — small set; used to attribute "their" games.
    today_emails = sorted(
        (d.to_dict().get("email") or d.id)
        for d in col.where(filter=FieldFilter("created_at", ">=", wins["today"])).stream()
    )
    return {
        "total": total,
        "new": new,                 # {today, 7d, 30d}
        "tiers": tiers,             # {free, api, paid}
        "new_today_emails": today_emails,
    }


# ─── Games (+ money) ─────────────────────────────────────────────────────────


def _game_stats(db, now: datetime, new_today_emails: list[str]) -> dict:
    """Single read of the live game set (≤30d, TTL-bounded), bucketed in Python.

    Volume is tiny (free tier ~tens of games live), so one stream beats juggling
    sum()/count() aggregations across windows — and we need per-doc fields anyway
    (cost, ownerEmail) to attribute games to today's new users.
    """
    wins = _windows(now)
    cut_ms = {k: int(c.timestamp() * 1000) for k, c in wins.items()}
    new_set = set(new_today_emails)

    created_count = {"today": 0, "7d": 0, "30d": 0}
    created_cost = {"today": 0.0, "7d": 0.0, "30d": 0.0}
    live_cost = 0.0
    total = 0
    by_new_users_today = 0   # games created today *by* users who signed up today
    today_games = []         # per-game detail for the ones started today

    for snap in db.collection(GAMES).stream():
        g = snap.to_dict() or {}
        total += 1
        cost = float(g.get("totalGameCost") or 0.0)
        live_cost += cost
        created = g.get("createdAt")
        if not isinstance(created, (int, float)):
            continue
        for k in ("today", "7d", "30d"):
            if created >= cut_ms[k]:
                created_count[k] += 1
                created_cost[k] += cost
        if created >= cut_ms["today"]:
            owner = g.get("ownerEmail")
            is_new = owner in new_set
            if is_new:
                by_new_users_today += 1
            # Games have no "name" — `theme` is the human-readable label.
            today_games.append({
                "id": snap.id,
                "theme": g.get("theme") or "(untitled)",
                "owner": owner,
                "by_new_user": is_new,
                "state": g.get("gameState"),
                "cost_usd": round(cost, 4),
            })

    today_games.sort(key=lambda x: x["id"])
    return {
        "total": total,
        "created": {k: created_count[k] for k in created_count},
        "created_cost_usd": {k: round(created_cost[k], 4) for k in created_cost},
        "live_cost_usd": round(live_cost, 4),
        "created_today_by_new_users": by_new_users_today,
        "today_games": today_games,
    }


def _user_spend_mtd(db, now: datetime) -> dict:
    """Current-month user spend from users.spendings (free/api/paid split).

    Reads all user docs (low volume) and sums the bucket whose period matches
    this UTC month. NOT revenue — see module docstring: only `paid` is income.
    Secondary to game burn; the right field if a paid tier grows.
    """
    from google.cloud.firestore_v1 import FieldFilter

    period = now.strftime("%Y-%m")
    out = {"period": period, "total": 0.0, "free": 0.0, "api": 0.0, "paid": 0.0}
    # Only users that have any spendings — still cheap, but skips the untouched.
    for d in db.collection(USERS).where(
        filter=FieldFilter("spendings", "!=", None)
    ).stream():
        for b in (d.to_dict().get("spendings") or []):
            if b.get("period") != period:
                continue
            out["total"] += float(b.get("amountUSD") or 0.0)
            out["free"] += float(b.get("freeAmountUSD") or 0.0)
            out["api"] += float(b.get("apiAmountUSD") or 0.0)
            out["paid"] += float(b.get("paidAmountUSD") or 0.0)
    return {k: (round(v, 4) if isinstance(v, float) else v) for k, v in out.items()}


# ─── Snapshot persistence (own files; budget_state is balance-shaped) ────────

STATS_LATEST = STATE_DIR / "stats_latest.json"
STATS_HISTORY = STATE_DIR / "stats_history.jsonl"


def _prev_snapshot() -> dict | None:
    try:
        with STATS_LATEST.open() as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def _daily_burn(prev: dict | None, live_cost: float, now: datetime) -> dict | None:
    """True money-spent-since-last-snapshot = Δ live cumulative game cost.

    Honest about its caveats: a negative delta means games expired out of the
    30d window between snapshots (their cost left the live set) — we floor at 0
    and flag it rather than report negative spend.
    """
    if not prev:
        return None
    prev_live = prev.get("games", {}).get("live_cost_usd")
    prev_at = prev.get("checked_at")
    if prev_live is None or prev_at is None:
        return None
    try:
        hrs = (now - datetime.fromisoformat(prev_at.replace("Z", "+00:00"))).total_seconds() / 3600
    except ValueError:
        return None
    delta = round(live_cost - float(prev_live), 4)
    return {
        "since": prev_at,
        "hours": round(hrs, 1),
        "usd": max(delta, 0.0),
        "raw_delta_usd": delta,
        "expired_games_suspected": delta < 0,
    }


def _compact(report: dict) -> dict:
    u, g = report.get("users", {}), report.get("games", {})
    return {
        "checked_at": report.get("checked_at"),
        "new_users_today": u.get("new", {}).get("today"),
        "games_created_today": g.get("created", {}).get("today"),
        "live_cost_usd": g.get("live_cost_usd"),
        "daily_burn_usd": (report.get("daily_burn") or {}).get("usd"),
        "users_total": u.get("total"),
    }


def _save(report: dict) -> None:
    """Overwrite stats_latest.json, append stats_history.jsonl. Best-effort."""
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        tmp = STATS_LATEST.with_suffix(".json.tmp")
        with tmp.open("w") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        tmp.replace(STATS_LATEST)
        with STATS_HISTORY.open("a") as f:
            f.write(json.dumps(_compact(report), ensure_ascii=False) + "\n")
    except OSError:
        pass


# ─── Report ──────────────────────────────────────────────────────────────────


def report() -> dict:
    now = _now_utc()
    try:
        db = _firestore_db()
    except RuntimeError as e:
        return {"ok": False, "checked_at": _checked_at(now), "error": str(e)}

    users = _user_stats(db, now)
    games = _game_stats(db, now, users["new_today_emails"])
    user_spend = _user_spend_mtd(db, now)
    burn = _daily_burn(_prev_snapshot(), games["live_cost_usd"], now)

    result = {
        "ok": True,
        "checked_at": _checked_at(now),
        "users": users,
        "games": games,
        "user_spend_mtd_usd": user_spend,
        "daily_burn": burn,   # null on first run (no prior snapshot to diff)
    }
    _save(result)
    return result


# ─── Human-readable render ───────────────────────────────────────────────────


def render(report: dict) -> str:
    if not report.get("ok"):
        return f"werewolf_stats failed: {report.get('error', 'unknown')}"
    u, g = report["users"], report["games"]
    n, c = u["new"], g["created"]
    cc = g["created_cost_usd"]
    out = [
        f"Werewolf activity — {report['checked_at']}",
        "",
        f"  Users    {u['total']} total  ({u['tiers']['free']} free / "
        f"{u['tiers']['api']} api / {u['tiers']['paid']} paid)",
        f"    new:   {n['today']} today · {n['7d']} 7d · {n['30d']} 30d",
        f"  Games    {g['total']} live  (TTL 30d)",
        f"    new:   {c['today']} today · {c['7d']} 7d · {c['30d']} 30d"
        + (f"  ({g['created_today_by_new_users']} by today's new users)"
           if g["created_today_by_new_users"] else ""),
        f"  Burn     ${g['live_cost_usd']:.2f} live cumulative",
        f"    cost of games started: ${cc['today']:.2f} today · "
        f"${cc['7d']:.2f} 7d · ${cc['30d']:.2f} 30d",
    ]
    b = report.get("daily_burn")
    if b:
        flag = "  ⚠ (some games expired out of window)" if b.get("expired_games_suspected") else ""
        out.append(f"    spent since last snapshot ({b['hours']}h): ${b['usd']:.2f}{flag}")
    else:
        out.append("    spent since last snapshot: n/a (first run — baseline set)")
    r = report.get("user_spend_mtd_usd") or report.get("revenue_mtd_usd") or {}
    if r:
        out.append(f"  User spend  ${r['total']:.2f} MTD ({r['period']}): "
                   f"${r['free']:.2f} free / ${r['api']:.2f} api / ${r['paid']:.2f} paid")
        out.append(f"    (free = our cost · api = users' own keys · "
                   f"paid = actual revenue: ${r['paid']:.4f})")

    # Today's detail — who signed up, what they're playing.
    emails = u.get("new_today_emails") or []
    if emails:
        out.append("")
        out.append(f"  New users today ({len(emails)}):")
        out.extend(f"    · {e}" for e in emails)
    tg = g.get("today_games") or []
    if tg:
        out.append("")
        out.append(f"  Games started today ({len(tg)}):")
        for gm in tg:
            tag = " [new user]" if gm["by_new_user"] else ""
            out.append(f"    · {gm['theme']} — {gm['owner']} · {gm['state']} · "
                       f"${gm['cost_usd']:.2f}{tag}")
    return "\n".join(out)


# ─── Digest line (what lands in the end-of-day Telegram digest) ──────────────

# Above these counts, the detail lists collapse to bare counts so a busy day
# can't flood the digest. Tune via editorial feedback if the cap feels wrong.
DIGEST_LIST_CAP = 5


def render_digest(report: dict) -> str:
    """Compact, capped block for `notify --digest`. Header always; per-section
    detail (new-user emails, game themes) only while small."""
    if not report.get("ok"):
        return f"Werewolf stats: report failed ({report.get('error', 'unknown')})."
    u, g = report["users"], report["games"]
    date = (report.get("checked_at") or "")[:10]
    new_n = u["new"]["today"]
    games_n = g["created"]["today"]
    b = report.get("daily_burn")
    money = (f"${b['usd']:.2f} since yesterday" if b
             else f"${g['created_cost_usd']['today']:.2f} today (baseline set)")
    lines = [f"Werewolf — {date}: +{new_n} user{'s' * (new_n != 1)} "
             f"({u['total']} total), {games_n} game{'s' * (games_n != 1)}, {money}"]

    emails = u.get("new_today_emails") or []
    if 0 < len(emails) <= DIGEST_LIST_CAP:
        lines.append("  new: " + ", ".join(emails))
    tg = g.get("today_games") or []
    if 0 < len(tg) <= DIGEST_LIST_CAP:
        lines.append("  games: " + ", ".join(
            f"{gm['theme']} ({gm['owner']}{', new user' if gm['by_new_user'] else ''})"
            for gm in tg))
    return "\n".join(lines)


# ─── CLI ─────────────────────────────────────────────────────────────────────


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("report", help="Compute + persist a full activity snapshot (JSON)")
    sub.add_parser("show", help="Render the last persisted snapshot, human-readable")
    sub.add_parser("digest", help="Capped digest block from the last snapshot (for notify --digest)")
    args = ap.parse_args()
    if args.cmd == "report":
        res = report()
        # Append the digest block deterministically here — do NOT rely on the
        # session to run a separate `digest | notify --digest` step. That step
        # was silently skipped for days, so user stats never reached the digest
        # even though the snapshot persisted fine. Same lesson as monitor_self:
        # delivery a human depends on must not hinge on the LLM remembering to.
        if res.get("ok"):
            try:
                from tools.notify import notify_alex
                notify_alex(render_digest(res), urgency="digest")
            except Exception as e:  # noqa: BLE001 — never let delivery break the snapshot
                print(f"warning: digest append failed: {e}", file=sys.stderr)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        sys.exit(0 if res.get("ok") else 1)
    elif args.cmd == "show":
        prev = _prev_snapshot()
        print(render(prev) if prev else "No snapshot yet — run `report` first.")
    elif args.cmd == "digest":
        prev = _prev_snapshot()
        print(render_digest(prev) if prev else "No snapshot yet — run `report` first.")


if __name__ == "__main__":
    main()
