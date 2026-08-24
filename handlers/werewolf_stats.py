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
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

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
#
# ── The reported day is a COMPLETE day in ALEX'S timezone (fixed 2026-08-22) ──
# It used to be "since UTC midnight", which was wrong twice over. The task fires
# at 09:00 UTC, so it counted a 9-hour slice and labelled it a day; and that
# slice (00:00-09:00 UTC) is 20:00-05:00 Eastern, the deadest hours of Alex's
# day. On 2026-08-22 it reported 1 new user and 1 game; the real local day was
# 6 users and 8 games. The whole stats_history tape shows the same shape - rows
# reading `new_users_today: 2` on days `users_total` jumped by 5.
#
# So the day window is now [local midnight, local midnight) for the last day
# that has actually ENDED. Anchoring to a closed calendar day also means a
# manual mid-afternoon run reports the same number as the scheduled one, which
# is the same property `_prev_day_baseline` already protects for money.
# The still-running local day is reported separately as `today_so_far`, always
# labelled partial, so nobody mistakes it for a total again.
LOCAL_TZ_NAME = os.environ.get("MARLOW_LOCAL_TZ", "America/New_York")
LOCAL_TZ = ZoneInfo(LOCAL_TZ_NAME)

# ── Alex's own account is not audience (2026-08-22) ──────────────────────────
# He plays to test, so his signups and games inflate exactly the numbers the
# report exists to answer ("are strangers finding this?"). Excluded from every
# ACTIVITY metric: user totals, tier split, new-user counts, games created,
# and the per-game detail lists.
#
# Money is deliberately NOT excluded the same way. His games cost real dollars
# off the same provider keys the budget watch reconciles against, so quietly
# dropping them would make `live_cost_usd` stop matching the drain - the exact
# failure we spent tonight fixing elsewhere. Instead the total stays whole and
# the report shows the split: total, and how much of it is his.
#
# Comma-separated override for test accounts: MARLOW_STATS_EXCLUDE.
EXCLUDED_OWNERS = {
    e.strip().lower()
    for e in os.environ.get("MARLOW_STATS_EXCLUDE", "hiper2d@gmail.com").split(",")
    if e.strip()
}


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _checked_at(now: datetime) -> str:
    return now.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _local_midnight(dt: datetime) -> datetime:
    """Midnight of dt's LOCAL calendar date, as an aware datetime."""
    return dt.astimezone(LOCAL_TZ).replace(hour=0, minute=0, second=0, microsecond=0)


def _period(now: datetime) -> dict:
    """The complete local day being reported, plus the partial one in progress."""
    today_start = _local_midnight(now)
    # Step back a day then re-normalise: on a DST boundary `- 1 day` lands at
    # 23:00 or 01:00, and we want midnight of that calendar date either way.
    day_start = _local_midnight(today_start - timedelta(days=1))
    return {
        "date": day_start.strftime("%Y-%m-%d"),
        "tz": LOCAL_TZ_NAME,
        "label": "full day",
        "start": day_start.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "end": today_start.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "_start_dt": day_start,
        "_end_dt": today_start,
    }


def _cutoffs(now: datetime) -> dict[str, datetime]:
    """Rolling cutoffs for the trend windows (unchanged semantics)."""
    return {"7d": now - timedelta(days=7), "30d": now - timedelta(days=30)}


# ─── Users ───────────────────────────────────────────────────────────────────


def _count(query) -> int:
    """Run a Firestore count() aggregation → int (no per-doc reads)."""
    return int(query.count().get()[0][0].value)


def _user_stats(db, now: datetime, period: dict) -> dict:
    from google.cloud.firestore_v1 import FieldFilter

    col = db.collection(USERS)
    day_q = (col.where(filter=FieldFilter("created_at", ">=", period["_start_dt"]))
                .where(filter=FieldFilter("created_at", "<", period["_end_dt"])))
    new = {"day": _count(day_q)}
    for k, cut in _cutoffs(now).items():
        new[k] = _count(col.where(filter=FieldFilter("created_at", ">=", cut)))
    # The local day still in progress. Explicitly partial - never a day total.
    new["today_so_far"] = _count(
        col.where(filter=FieldFilter("created_at", ">=", period["_end_dt"])))

    total = _count(col)
    tiers = {t: _count(col.where(filter=FieldFilter("tier", "==", t)))
             for t in ("free", "api", "paid")}

    # Subtract the excluded accounts from whichever buckets they actually land
    # in. Docs are keyed by email, so this is a direct get per excluded address -
    # no scan, and it silently no-ops if the account doesn't exist.
    dropped = 0
    for email in EXCLUDED_OWNERS:
        snap = col.document(email).get()
        if not snap.exists:
            continue
        d = snap.to_dict() or {}
        dropped += 1
        total -= 1
        tier = d.get("tier")
        if tier in tiers:
            tiers[tier] = max(tiers[tier] - 1, 0)
        created = d.get("created_at")
        if created is None:
            continue
        if period["_start_dt"] <= created < period["_end_dt"]:
            new["day"] = max(new["day"] - 1, 0)
        if created >= period["_end_dt"]:
            new["today_so_far"] = max(new["today_so_far"] - 1, 0)
        for k, cut in _cutoffs(now).items():
            if created >= cut:
                new[k] = max(new[k] - 1, 0)

    # The day's new-user emails — small set; used to attribute "their" games.
    day_emails = sorted(e for e in
                        ((d.to_dict().get("email") or d.id) for d in day_q.stream())
                        if (e or "").lower() not in EXCLUDED_OWNERS)
    return {
        "total": total,
        "new": new,                 # {day, 7d, 30d, today_so_far} — excluded accounts removed
        "tiers": tiers,             # {free, api, paid}
        "new_day_emails": day_emails,
        "excluded_users": dropped,
    }


# ─── Games (+ money) ─────────────────────────────────────────────────────────


def _game_stats(db, now: datetime, period: dict, new_day_emails: list[str]) -> dict:
    """Single read of the live game set (≤30d, TTL-bounded), bucketed in Python.

    Volume is tiny (free tier ~tens of games live), so one stream beats juggling
    sum()/count() aggregations across windows — and we need per-doc fields anyway
    (cost, ownerEmail) to attribute games to today's new users.
    """
    cut_ms = {k: int(c.timestamp() * 1000) for k, c in _cutoffs(now).items()}
    day_start_ms = int(period["_start_dt"].timestamp() * 1000)
    day_end_ms = int(period["_end_dt"].timestamp() * 1000)
    new_set = set(new_day_emails)

    created_count = {"day": 0, "7d": 0, "30d": 0, "today_so_far": 0}
    created_cost = {"day": 0.0, "7d": 0.0, "30d": 0.0, "today_so_far": 0.0}
    live_cost = 0.0          # ALL games — this is the figure that reconciles
    own_live_cost = 0.0      # the excluded accounts' share of it
    own_games = 0
    total = 0
    by_new_users_day = 0   # games created in the day *by* users who signed up in it
    day_games = []         # per-game detail for the ones started in the day

    for snap in db.collection(GAMES).stream():
        g = snap.to_dict() or {}
        cost = float(g.get("totalGameCost") or 0.0)
        # live_cost counts EVERY game, excluded or not: it is what reconciles
        # against the provider balances. The exclusion is reported as a split.
        live_cost += cost
        if (g.get("ownerEmail") or "").lower() in EXCLUDED_OWNERS:
            own_live_cost += cost
            own_games += 1
            continue
        total += 1
        created = g.get("createdAt")
        if not isinstance(created, (int, float)):
            continue
        for k in ("7d", "30d"):
            if created >= cut_ms[k]:
                created_count[k] += 1
                created_cost[k] += cost
        if created >= day_end_ms:
            created_count["today_so_far"] += 1
            created_cost["today_so_far"] += cost
        if day_start_ms <= created < day_end_ms:
            created_count["day"] += 1
            created_cost["day"] += cost
            owner = g.get("ownerEmail")
            is_new = owner in new_set
            if is_new:
                by_new_users_day += 1
            # Games have no "name" — `theme` is the human-readable label.
            day_games.append({
                "id": snap.id,
                "theme": g.get("theme") or "(untitled)",
                "owner": owner,
                "by_new_user": is_new,
                "state": g.get("gameState"),
                "cost_usd": round(cost, 4),
            })

    day_games.sort(key=lambda x: x["id"])
    return {
        "total": total,
        "created": {k: created_count[k] for k in created_count},
        "created_cost_usd": {k: round(created_cost[k], 4) for k in created_cost},
        "live_cost_usd": round(live_cost, 4),
        "live_cost_usd_excl_own": round(live_cost - own_live_cost, 4),
        "own_live_cost_usd": round(own_live_cost, 4),
        "own_games": own_games,
        "created_day_by_new_users": by_new_users_day,
        "day_games": day_games,
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
    own = {"total": 0.0, "free": 0.0, "api": 0.0, "paid": 0.0}
    for d in db.collection(USERS).where(
        filter=FieldFilter("spendings", "!=", None)
    ).stream():
        doc = d.to_dict() or {}
        # Alex's own spend is not audience spend, and his is the ONLY paid row -
        # left in, "paid revenue" reads as income when it is him paying himself.
        bucket = own if ((doc.get("email") or d.id) or "").lower() in EXCLUDED_OWNERS else out
        for b in (doc.get("spendings") or []):
            if b.get("period") != period:
                continue
            bucket["total"] += float(b.get("amountUSD") or 0.0)
            bucket["free"] += float(b.get("freeAmountUSD") or 0.0)
            bucket["api"] += float(b.get("apiAmountUSD") or 0.0)
            bucket["paid"] += float(b.get("paidAmountUSD") or 0.0)
    res = {k: (round(v, 4) if isinstance(v, float) else v) for k, v in out.items()}
    res["excluded_own"] = {k: round(v, 4) for k, v in own.items()}
    return res


# ─── Snapshot persistence (own files; budget_state is balance-shaped) ────────

STATS_LATEST = STATE_DIR / "stats_latest.json"
STATS_HISTORY = STATE_DIR / "stats_history.jsonl"


def _prev_snapshot() -> dict | None:
    try:
        with STATS_LATEST.open() as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def _prev_day_baseline(period: dict) -> tuple[str, float] | None:
    """Last snapshot taken BEFORE the reported day began: (checked_at, live_cost_usd).

    Scans stats_history.jsonl newest-first for the first row stamped earlier
    than the day's local-midnight start. Anchoring to the day boundary (rather
    than to "whenever I last ran") is what stops a second manual `report` from
    shrinking the reported spend. Was UTC-midnight-based; moved onto the local
    day with everything else 2026-08-22.
    """
    day_start_iso = period["start"]
    try:
        lines = STATS_HISTORY.read_text().splitlines()
    except OSError:
        return None
    for line in reversed(lines):
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        at, live = row.get("checked_at"), row.get("live_cost_usd")
        # Both are Z-suffixed ISO-8601, so lexicographic order is chronological.
        if not at or live is None or at >= day_start_iso:
            continue
        return row
    return None


def _daily_burn(prev: dict | None, live_cost: float, now: datetime, period: dict,
                live_cost_excl: float | None = None) -> dict | None:
    """Δ live cumulative game cost, on TWO baselines.

    `usd` / `hours` / `since` = since the previous snapshot, whenever that was.
    `today_usd` / `today_since` = since the last snapshot of a PREVIOUS DAY,
    i.e. the true money spent today.

    Why both (2026-08-03): there was only the since-last-snapshot delta, and
    `render_digest` labelled it "since yesterday". That is true only when
    snapshots happen exactly once a day. Run `report` a second time and the
    baseline resets, so the digest reports the sliver since the last run and
    silently understates the day. It bit us today: four snapshots turned a
    $2.33 day into a reported $0.93. The day figure must be anchored to a
    calendar boundary, not to "whenever I last ran", or any manual/on-demand
    run corrupts the number that gets reported.

    Honest about its caveats: a negative delta means games expired out of the
    30d window between snapshots (their cost left the live set) - we floor at 0
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
    out = {
        "since": prev_at,
        "hours": round(hrs, 1),
        "usd": max(delta, 0.0),
        "raw_delta_usd": delta,
        "expired_games_suspected": delta < 0,
    }
    base = _prev_day_baseline(period)
    if base:
        base_at = base.get("checked_at")
        day_delta = round(live_cost - float(base.get("live_cost_usd")), 4)
        out["day_since"] = base_at
        out["day_usd"] = max(day_delta, 0.0)
        out["day_raw_delta_usd"] = day_delta
        # The same delta with the excluded accounts' games taken out. Only
        # computable once BOTH ends of the interval carry the field, so it stays
        # absent for baselines written before 2026-08-22 rather than being
        # silently computed against a total and reported as a net figure.
        base_excl = base.get("live_cost_usd_excl_own")
        if live_cost_excl is not None and base_excl is not None:
            excl_delta = round(live_cost_excl - float(base_excl), 4)
            out["day_usd_excl_own"] = max(excl_delta, 0.0)
    return out


def _compact(report: dict) -> dict:
    u, g = report.get("users", {}), report.get("games", {})
    return {
        "checked_at": report.get("checked_at"),
        "period_date": (report.get("period") or {}).get("date"),
        "new_users_day": u.get("new", {}).get("day"),
        "games_created_day": g.get("created", {}).get("day"),
        "live_cost_usd": g.get("live_cost_usd"),
        "live_cost_usd_excl_own": g.get("live_cost_usd_excl_own"),
        "own_games": g.get("own_games"),
        "daily_burn_usd": (report.get("daily_burn") or {}).get("usd"),
        "daily_burn_day_usd": (report.get("daily_burn") or {}).get("day_usd"),
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

    period = _period(now)
    users = _user_stats(db, now, period)
    games = _game_stats(db, now, period, users["new_day_emails"])
    user_spend = _user_spend_mtd(db, now)
    burn = _daily_burn(_prev_snapshot(), games["live_cost_usd"], now, period,
                       games.get("live_cost_usd_excl_own"))

    result = {
        "ok": True,
        "checked_at": _checked_at(now),
        # The day this report is ABOUT, which is not the day it ran.
        "period": {k: v for k, v in period.items() if not k.startswith("_")},
        "users": users,
        "games": games,
        "user_spend_mtd_usd": user_spend,
        "daily_burn": burn,   # null on first run (no prior snapshot to diff)
        # Never leave a filter implicit — an exclusion nobody can see is how a
        # number ends up meaning something other than its label.
        "excluded": {
            "owners": sorted(EXCLUDED_OWNERS),
            "users": users.get("excluded_users", 0),
            "games": games.get("own_games", 0),
            "games_cost_usd": games.get("own_live_cost_usd", 0.0),
        },
    }
    _save(result)
    return result


# ─── Human-readable render ───────────────────────────────────────────────────


def _upgrade_legacy(rep: dict) -> dict:
    """Map pre-2026-08-22 snapshots onto the local-day key names.

    Older files carry `today`/`new_today_emails`/`today_games`, which are the
    UTC-partial-day numbers. `show` and `digest` must still read them rather
    than raising KeyError on an archived report. Note what this does NOT do:
    the values keep their original partial-day meaning. We are relabelling a
    stored number, not retroactively widening the window it was measured over -
    so the period is stamped as legacy rather than given a real local date.
    """
    if not rep.get("ok"):
        return rep
    u, g = rep.get("users") or {}, rep.get("games") or {}
    new = u.get("new") or {}
    if "today" in new and "day" not in new:
        new["day"] = new["today"]
        u.setdefault("new_day_emails", u.get("new_today_emails") or [])
    created = g.get("created") or {}
    if "today" in created and "day" not in created:
        created["day"] = created["today"]
        cost = g.get("created_cost_usd") or {}
        cost.setdefault("day", cost.get("today", 0.0))
        g.setdefault("created_day_by_new_users", g.get("created_today_by_new_users") or 0)
        g.setdefault("day_games", g.get("today_games") or [])
    b = rep.get("daily_burn") or {}
    if "today_usd" in b and "day_usd" not in b:
        b["day_usd"] = b["today_usd"]
    if "period" not in rep:
        rep["period"] = {"date": (rep.get("checked_at") or "")[:10],
                         "tz": "UTC", "label": "PARTIAL legacy slice, not a full day"}
    return rep


def render(report: dict) -> str:
    if not report.get("ok"):
        return f"werewolf_stats failed: {report.get('error', 'unknown')}"
    report = _upgrade_legacy(report)
    u, g = report["users"], report["games"]
    n, c = u["new"], g["created"]
    cc = g["created_cost_usd"]
    per = report.get("period") or {}
    date, tz = per.get("date", "?"), per.get("tz", "?")
    label = per.get("label", "full day")
    out = [
        f"Werewolf activity for {date} ({tz}, {label})",
        f"  reported {report['checked_at']}",
        "",
        f"  Users    {u['total']} total  ({u['tiers']['free']} free / "
        f"{u['tiers']['api']} api / {u['tiers']['paid']} paid)",
        f"    new:   {n['day']} on {date} · {n['7d']} 7d · {n['30d']} 30d",
        f"  Games    {g['total']} live  (TTL 30d)",
        f"    new:   {c['day']} on {date} · {c['7d']} 7d · {c['30d']} 30d"
        + (f"  ({g['created_day_by_new_users']} by that day's new users)"
           if g["created_day_by_new_users"] else ""),
        f"  Burn     ${g['live_cost_usd']:.2f} live cumulative"
        + (f"  (${g['live_cost_usd_excl_own']:.2f} others / "
           f"${g['own_live_cost_usd']:.2f} yours)"
           if g.get("own_live_cost_usd") else ""),
        f"    cost of games started: ${cc['day']:.2f} on {date} · "
        f"${cc['7d']:.2f} 7d · ${cc['30d']:.2f} 30d",
    ]
    b = report.get("daily_burn")
    if b:
        flag = "  ⚠ (some games expired out of window)" if b.get("expired_games_suspected") else ""
        if b.get("day_usd") is not None:
            excl = b.get("day_usd_excl_own")
            split = f"  (${excl:.2f} excluding your games)" if excl is not None else ""
            out.append(f"    spent on {date} (vs last snapshot before it): "
                       f"${b['day_usd']:.2f}{split}{flag}")
        out.append(f"    spent since last snapshot ({b['hours']}h): ${b['usd']:.2f}")
    else:
        out.append("    spent since last snapshot: n/a (first run - baseline set)")
    r = report.get("user_spend_mtd_usd") or report.get("revenue_mtd_usd") or {}
    if r:
        own = r.get("excluded_own") or {}
        out.append(f"  User spend  ${r['total']:.2f} MTD ({r['period']}): "
                   f"${r['free']:.2f} free / ${r['api']:.2f} api / ${r['paid']:.2f} paid"
                   + (f"  (yours, excluded: ${own.get('total', 0):.2f})" if own.get("total") else ""))
        out.append(f"    (free = our cost · api = users' own keys · "
                   f"paid = actual revenue: ${r['paid']:.4f})")

    # The day's detail — who signed up, what they're playing.
    emails = u.get("new_day_emails") or []
    if emails:
        out.append("")
        out.append(f"  New users on {date} ({len(emails)}):")
        out.extend(f"    · {e}" for e in emails)
    tg = g.get("day_games") or []
    if tg:
        out.append("")
        out.append(f"  Games started on {date} ({len(tg)}):")
        for gm in tg:
            tag = " [new user]" if gm["by_new_user"] else ""
            out.append(f"    · {gm['theme']} — {gm['owner']} · {gm['state']} · "
                       f"${gm['cost_usd']:.2f}{tag}")
    ex = report.get("excluded") or {}
    if ex.get("owners"):
        out.append("")
        out.append(f"  Excluded from all activity counts: {', '.join(ex['owners'])}"
                   f"  ({ex.get('users', 0)} user, {ex.get('games', 0)} live games, "
                   f"${ex.get('games_cost_usd', 0):.2f} — still counted in burn)")

    # The day in progress, always flagged partial so it can't be read as a total.
    sf_u, sf_g = n.get("today_so_far"), c.get("today_so_far")
    if sf_u is not None or sf_g is not None:
        out.append("")
        out.append(f"  Since local midnight (PARTIAL, day still running): "
                   f"{sf_u or 0} new users · {sf_g or 0} games")
    return "\n".join(out)


# ─── Digest line (what lands in the end-of-day Telegram digest) ──────────────

# Above these counts, the detail lists collapse to bare counts so a busy day
# can't flood the digest. Tune via editorial feedback if the cap feels wrong.
DIGEST_LIST_CAP = 5


def render_digest(report: dict) -> str:
    """Compact block for `notify --digest`.

    Rewritten 2026-08-03 on Alex's request: the old version was three lines
    (counts + emails + game themes) and dropped everything he actually reads -
    the 7d/30d trend, the cumulative burn, and each game's state and cost. He
    was reading the fuller `show` output in chat and asking why Telegram
    differed. Now the digest carries the same numbers as `show`; `show` stays
    the wider terminal render.

    Two deliberate omissions:
    - The `paid` tier and `paid revenue` are NOT reported. The only paid user
      is Alex himself, so "$0.00 revenue" is noise that reads as a problem
      every single day. A paid count above 1 IS surfaced, loudly, because that
      would be the first real paying user.
    - Money is the day-anchored `today_usd`, never the since-last-snapshot
      delta, so an extra manual run cannot shrink the reported day.
    """
    if not report.get("ok"):
        return f"Werewolf stats: report failed ({report.get('error', 'unknown')})."
    report = _upgrade_legacy(report)
    u, g = report["users"], report["games"]
    # The date this report is ABOUT (the completed local day), NOT the date it
    # ran. Before 2026-08-22 this was checked_at[:10], which on a just-past
    # -midnight run would have stamped the wrong day on the right numbers.
    per = report.get("period") or {}
    date = per.get("date") or (report.get("checked_at") or "")[:10]
    un, gn, cc = u["new"], g["created"], g["created_cost_usd"]
    b = report.get("daily_burn") or {}

    # Prefer the day-anchored figure; fall back only if there's no prior day.
    if b.get("day_usd_excl_own") is not None:
        own = b["day_usd"] - b["day_usd_excl_own"]
        money = f"${b['day_usd_excl_own']:.2f}" + (f" (+${own:.2f} yours)" if own >= 0.005 else "")
    elif b.get("day_usd") is not None:
        money = f"${b['day_usd']:.2f} incl. yours"
    elif b.get("usd") is not None:
        money = f"${b['usd']:.2f} in the last {b.get('hours', 0)}h"
    else:
        money = f"${cc['day']:.2f} (baseline set)"
    if b.get("expired_games_suspected"):
        money += " (partial: games expired out of window)"

    lines = [
        f"Werewolf - {date} ({per.get('label', 'full day')}, {per.get('tz', 'local')})",
        f"  Users  {u['total']} total  (+{un['day']} that day · {un['7d']} 7d · {un['30d']} 30d)",
        f"  Games  {g['total']} live  (+{gn['day']} that day · {gn['7d']} 7d · {gn['30d']} 30d)",
        f"  Burn   {money} · ${cc['7d']:.2f} 7d · ${g['live_cost_usd']:.2f} cumulative",
    ]

    # Threshold dropped from >1 to >=1 on 2026-08-22: Alex used to be counted
    # here, so "more than one" was the test for a stranger paying. He is now
    # excluded, which makes the very first paid user the milestone. Left at >1
    # it would have stayed silent for the actual first paying customer.
    paid = (u.get("tiers") or {}).get("paid") or 0
    if paid >= 1:
        lines.append(f"  *** PAID USERS: {paid} - real paying customer(s), Alex excluded ***")

    emails = u.get("new_day_emails") or []
    if 0 < len(emails) <= DIGEST_LIST_CAP:
        lines.append("  new: " + ", ".join(emails))
    elif emails:
        lines.append(f"  new: {len(emails)} signups")
    tg = g.get("day_games") or []
    if 0 < len(tg) <= DIGEST_LIST_CAP:
        for gm in tg:
            tag = ", new user" if gm.get("by_new_user") else ""
            lines.append(f"  game: {gm['theme']} ({gm['owner']}{tag}) · "
                         f"{gm.get('state', '?')} · ${gm.get('cost_usd', 0):.2f}")
    elif tg:
        lines.append(f"  games: {len(tg)} started")
    ex = report.get("excluded") or {}
    if ex.get("games") or ex.get("users"):
        lines.append(f"  (excludes {', '.join(ex.get('owners') or [])})")
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
