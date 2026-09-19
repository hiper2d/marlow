"""
werewolf_stats — daily user-activity snapshot for the Werewolf game.

Companion to monitor_keys: that watches what the free tier *costs* (provider
balances); this watches what the free tier *produces* (signups, games, burn).
Both read the same Firestore via the same read-only service account.

The report is FIVE numbers for one closed local day (2026-09-11; was three):
  1. New users on that day.
  2. New games on that day.
  3. What those games have cost so far.
  4. What users were CHARGED that day, per user.   (added 2026-09-11)
  5. How many users hit their daily spend cap.     (added 2026-09-11)
Everything else is a live reading of a TTL-bounded collection and is printed
under "Reference" with no deltas on it. Alex: "Just count new users and new
games for the current day." The day counts were already right; every wrong line
in the reports came from differencing the live readings around them.

Why 4 and 5 were added (2026-09-11): the Gemini prepaid key drained from $20.59
to $0 over eleven days and this report never showed it coming. Numbers 3 and 4
are NOT the same number and the difference is the point - 3 is what games
recorded, 4 is what users were charged. Preview and image calls used to charge
the user but write no `requestStats` row, and previews belong to no game at all,
so a report built on games alone was structurally blind to roughly two thirds of
Gemini spend. `spend_reconciliation` now asserts the two against each other and
prints the gap.

Since 2026-09-11 (werewolf `recordSpend`) EVERY spend - game turns, previews,
images, voice - writes one `requestStats` row (`kind` field) in the same
transaction as the charge, and the user doc carries a UTC-day `dailySpend`
ledger. `daily_ledger_reconciliation` asserts the two against each other for
the current UTC day, so a spend path that stops writing its row shows up the
day it stops, not eleven days later.

Two rules this file now enforces:
  - The only user total that gets differenced is `total_day_end`, measured at
    the same boundary as the day counts. `_reconcile` asserts
    total_day_end(N) - total_day_end(N-1) == new_users_day(N).
  - A failed invariant prints BROKEN and stops. It never gets an explanation.
    Every mismatch here so far was a clock bug wearing a plausible sentence.

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

    # ── The total must be measured at the SAME boundary as `new` (2026-09-08) ──
    # `total` is a live count: whatever the collection held at the instant the
    # tick fired, which is 5-17 hours into the day AFTER the one being reported.
    # `new["day"]` is a closed local calendar day. Differencing the first and
    # reading it as the second compares two different clocks, and it disagreed
    # on 10 of the 12 rows on the tape (2026-08-29 .. 2026-09-07). Marlow then
    # narrated the residue away as a "prior-window-rolling effect" three days
    # running - there is no window on a total, so there was nothing to roll.
    # `total_day_end` is the count as of the reported day's local midnight, so
    #     total_day_end(N) - total_day_end(N-1) == new["day"](N)
    # holds exactly. `_reconcile` ASSERTS that. It is never explained.
    total_day_end = _count(
        col.where(filter=FieldFilter("created_at", "<", period["_end_dt"])))

    tiers = {t: _count(col.where(filter=FieldFilter("tier", "==", t)))
             for t in ("free", "api", "paid")}
    # `paid` means "has money on the account", not "pressed the free Upgrade
    # button in /profile" (see _paid_tier_line). A paid-tier doc with no balance
    # has never been through Stripe; Alex asked on 2026-09-14 never to hear about
    # those. The paid set is tiny (two docs), so stream it instead of a count()
    # that would need a composite index for tier + balance.
    tiers["paid"] = sum(
        1 for d in col.where(filter=FieldFilter("tier", "==", "paid")).stream()
        if float((d.to_dict() or {}).get("balance") or 0.0) > 0)

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
        if created < period["_end_dt"]:
            total_day_end = max(total_day_end - 1, 0)
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
        "total": total,             # live count at read time — reference only, never differenced
        "total_day_end": total_day_end,   # count at the reported day's midnight — the one that reconciles
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
    day_refusals = []      # provider content refusals stamped in the day (any game age)

    for snap in db.collection(GAMES).stream():
        g = snap.to_dict() or {}
        cost = float(g.get("totalGameCost") or 0.0)
        # live_cost counts EVERY game, excluded or not: it is what reconciles
        # against the provider balances. The exclusion is reported as a split.
        live_cost += cost
        # A provider refusing this game's story (`providerBlocks`, written by the
        # game on the first content-filter refusal, one entry per provider, `at`
        # in epoch ms). Collected for EVERY owner, Alex included: it is about
        # the platform key, not the audience. Joined with the content screen.
        for block in (g.get("providerBlocks") or {}).values():
            at = (block or {}).get("at")
            if isinstance(at, (int, float)) and day_start_ms <= at < day_end_ms:
                day_refusals.append({
                    "id": snap.id,
                    "theme": g.get("theme") or "(untitled)",
                    "owner": g.get("ownerEmail"),
                    "provider": block.get("provider"),
                    "reason": block.get("reason"),
                    "bot": block.get("botName"),
                    "day": block.get("day"),
                })
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
        "day_refusals": sorted(day_refusals, key=lambda x: x["id"]),
    }


def _median(values: list[float]) -> float:
    if not values:
        return 0.0
    v = sorted(values)
    mid = len(v) // 2
    return v[mid] if len(v) % 2 else (v[mid - 1] + v[mid]) / 2


def _user_spend(db, now: datetime, period: dict, prev_row: dict | None) -> dict:
    """Per-user spend: the current month, and the reported day.

    `users.spendings` is the ONLY complete record of what a user cost us. It
    carries game turns, previews, images and voice alike, because every one of
    those paths goes through recordSpend. `requestStats` did NOT until
    2026-09-11: measured that day, it held $7.14 of Gemini spend for Sept 1-11
    against $20.56 the provider actually billed, because image and preview
    calls wrote no stats row. Fixed the same day (every spend now writes a row
    with `kind`), but per-user money is still read HERE: the ledger is the
    charge, requestStats is the cost, and `_daily_ledger_reconcile` asserts
    they agree rather than trusting either alone.

    The day figure, and why it is a delta. `spendings` is bucketed by UTC
    MONTH, so Firestore holds no daily number to read. We build one the same
    way `_daily_burn` builds its own: snapshot every user's month-to-date total
    each day and difference it against the previous day's row. Same caveat,
    stated the same way - the interval is snapshot-to-snapshot, not exactly
    midnight-to-midnight.

    Month rollover zeroes MTD, so a delta across it is meaningless. When the
    previous row carries a different period we report NO day figure and say
    why. A negative or invented number here would be worse than a gap.

    `dailySpend` (shipped 2026-09-11; `{period: 'YYYY-MM-DD' UTC, totalUSD,
    buckets: {free, paid}, limitHits}` - note the day key is `period`, not the
    `date` the plan doc said) is read when present, but it is a UTC-day field
    and this report is anchored to Alex's LOCAL day, so it is carried as a
    separate read-time reference (`daily_field_utc`) and NOT substituted for
    the delta. Mixing a UTC day into a local-day report is exactly the class
    of bug the period rewrite above removed.
    """
    from google.cloud.firestore_v1 import FieldFilter

    mtd_period = now.strftime("%Y-%m")
    out = {"period": mtd_period, "total": 0.0, "free": 0.0, "api": 0.0, "paid": 0.0}
    own = {"total": 0.0, "free": 0.0, "api": 0.0, "paid": 0.0}
    by_user: dict[str, float] = {}          # our-cost (free bucket) MTD, per user
    utc_today = now.strftime("%Y-%m-%d")
    hits: dict[str, int] = {}
    daily_seen = False
    daily_by_user: dict[str, float] = {}
    daily_free_total = 0.0      # whole population, Alex included (ledger side of the reconcile)
    daily_paid_total = 0.0

    for d in db.collection(USERS).where(
        filter=FieldFilter("spendings", "!=", None)
    ).stream():
        doc = d.to_dict() or {}
        key = ((doc.get("email") or d.id) or "").lower()
        # Alex's own spend is not audience spend, and his is the ONLY paid row -
        # left in, "paid revenue" reads as income when it is him paying himself.
        is_own = key in EXCLUDED_OWNERS
        bucket = own if is_own else out
        for b in (doc.get("spendings") or []):
            if b.get("period") != mtd_period:
                continue
            bucket["total"] += float(b.get("amountUSD") or 0.0)
            bucket["free"] += float(b.get("freeAmountUSD") or 0.0)
            bucket["api"] += float(b.get("apiAmountUSD") or 0.0)
            bucket["paid"] += float(b.get("paidAmountUSD") or 0.0)
            if not is_own:
                free = float(b.get("freeAmountUSD") or 0.0)
                if free > 0:
                    by_user[key] = round(free, 6)

        # UTC-day ledger, shipped 2026-09-11. Overwritten (not appended) when
        # the UTC day rolls, so a stale `period` is yesterday's leftover.
        ds = doc.get("dailySpend")
        if isinstance(ds, dict):
            daily_seen = True
            if ds.get("period") == utc_today:
                n = int(ds.get("limitHits") or 0)
                if n > 0 and not is_own:
                    hits[key] = n
                amt = float(ds.get("totalUSD") or 0.0)
                if amt > 0 and not is_own:
                    daily_by_user[key] = round(amt, 6)
                buckets = ds.get("buckets") or {}
                daily_free_total += float(buckets.get("free") or 0.0)
                daily_paid_total += float(buckets.get("paid") or 0.0)

    res = {k: (round(v, 4) if isinstance(v, float) else v) for k, v in out.items()}
    res["excluded_own"] = {k: round(v, 4) for k, v in own.items()}
    res["by_user_free"] = by_user
    res["day"] = _spend_day(by_user, mtd_period, prev_row)
    res["limit_hits"] = (
        {
            "instrumented": True,
            "utc_date": utc_today,
            "users": len(hits),
            "hits": sum(hits.values()),
            "by_user": dict(sorted(hits.items(), key=lambda kv: -kv[1])),
        }
        if daily_seen
        else {
            "instrumented": False,
            "reason": "no user has a dailySpend field yet - the cap shipped "
                      "2026-09-11 and the field appears on a user's first charge "
                      "after that deploy",
        }
    )
    if daily_seen:
        res["daily_field_utc"] = {
            "utc_date": utc_today,
            "users_with_spend": len(daily_by_user),
            "total": round(sum(daily_by_user.values()), 4),
            # Whole-population bucket totals (Alex included): the ledger side
            # of _daily_ledger_reconcile, which must not exclude anyone one-sidedly.
            "free_total": round(daily_free_total, 4),
            "paid_total": round(daily_paid_total, 4),
            "note": "read-time UTC-day field, NOT the local day this report covers",
        }
    return res


def _spend_day(by_user: dict[str, float], mtd_period: str,
               prev_row: dict | None) -> dict:
    """Difference this run's per-user MTD map against the previous day's row.

    Returns `{"ok": False, "reason": ...}` rather than a number whenever the
    baseline cannot support one: no prior row, a prior row from before this
    function existed, or a month boundary in between.
    """
    if prev_row is None:
        return {"ok": False, "reason": "no prior day on the tape - baseline set"}
    prev_by_user = prev_row.get("user_mtd_by_user")
    prev_period = prev_row.get("user_mtd_period")
    if prev_by_user is None or prev_period is None:
        return {"ok": False,
                "reason": f"prior day {prev_row.get('period_date')} predates per-user "
                          f"spend tracking (added 2026-09-11)"}
    if prev_period != mtd_period:
        return {"ok": False,
                "reason": f"month rollover ({prev_period} -> {mtd_period}): "
                          f"month-to-date reset, so the delta is not spend"}

    deltas: dict[str, float] = {}
    for key, now_usd in by_user.items():
        d = round(now_usd - float(prev_by_user.get(key) or 0.0), 6)
        if d > 0.000005:
            deltas[key] = d
    # A user whose MTD went DOWN is a data problem, not a refund - surface it.
    shrank = [k for k, v in by_user.items()
              if v < float(prev_by_user.get(k) or 0.0) - 0.000005]
    amounts = list(deltas.values())
    top = sorted(deltas.items(), key=lambda kv: -kv[1])
    return {
        "ok": True,
        "prev_day": prev_row.get("period_date"),
        "users_with_spend": len(deltas),
        "total": round(sum(amounts), 4),
        "median": round(_median(amounts), 4),
        "max": round(max(amounts), 4) if amounts else 0.0,
        "top": [{"user": k, "usd": round(v, 4)} for k, v in top[:5]],
        "shrank": shrank,
    }


def _window_burn(prev_row: dict | None, live_cost_excl: float | None,
                 now: datetime) -> dict | None:
    """Game-recorded cost over EXACTLY the interval the per-user charge delta
    covers: since the previous reported day's row, the same `prev_row` that
    `_spend_day` differences against.

    Why a second burn figure (2026-09-14): `_daily_burn` anchors to the last
    snapshot before local midnight, `_spend_day` to the previous day's row.
    Those are the same row only when the daily run happens before midnight.
    On 2026-09-13 the run was at 01:36 ET, so the game side reached back one
    more snapshot (58h) while the user side covered 34h, and the digest said
    "games recorded $17.50 but users were charged $13.73 - cost with no payer".
    There was no such cost; the two numbers were different windows. Both
    sides of that comparison now come from this one interval, and the digest
    prints the interval next to the money.
    """
    if not prev_row or live_cost_excl is None:
        return None
    base = prev_row.get("live_cost_usd_excl_own")
    at = prev_row.get("checked_at")
    if base is None or not at:
        return None
    try:
        hrs = (now - datetime.fromisoformat(at.replace("Z", "+00:00"))).total_seconds() / 3600
    except ValueError:
        return None
    delta = round(float(live_cost_excl) - float(base), 4)
    return {
        "since": at,
        "hours": round(hrs, 1),
        "day_usd_excl_own": max(delta, 0.0),
        "raw_delta_usd": delta,
        "expired_games_suspected": delta < 0,
    }


def _window_label(since_iso: str | None, hours: float | None, tz: str | None) -> str:
    """"since Sep 13 01:36 ET (34h)" - the interval every money figure in the
    digest covers. Local time because the report is anchored to Alex's day."""
    if not since_iso:
        return ""
    try:
        from zoneinfo import ZoneInfo
        dt = datetime.fromisoformat(since_iso.replace("Z", "+00:00"))
        if tz:
            dt = dt.astimezone(ZoneInfo(tz))
        when = f"{dt:%b} {dt.day} {dt:%H:%M %Z}"
    except Exception:  # noqa: BLE001
        when = since_iso[:16].replace("T", " ") + "Z"
    return f"since {when}" + (f" ({hours:.0f}h)" if hours is not None else "")


def _spend_reconcile(user_spend: dict, burn: dict | None) -> dict:
    """Assert per-user day spend >= game-cost burn over the SAME window, name the gap.

    The two numbers come from opposite ends of the same money: `spendings` is
    what users were charged, `totalGameCost` is what games recorded. User spend
    must be the LARGER of the two, because preview/story generation charges the
    user before any game exists and so lands in no game's cost. The difference
    is therefore an estimate of preview spend - the hole this report existed to
    hide.

    If user spend comes in BELOW game burn, that is not a window effect. It
    means a game recorded cost that was never charged to anybody, and the
    report says BROKEN.

    Compared free-bucket against burn-excluding-Alex on purpose: Alex is paid
    tier, so his spend lands in `paid` WITH markup applied, and differencing a
    marked-up charge against a raw provider cost would drift by design.
    """
    day = user_spend.get("day") or {}
    if not day.get("ok"):
        return {"ok": None, "reason": day.get("reason", "no per-user day figure")}
    if not burn:
        return {"ok": None, "reason": "no daily burn figure to compare against"}
    burn_usd = burn.get("day_usd_excl_own")
    basis = "day_usd_excl_own"
    if burn_usd is None:
        return {"ok": None,
                "reason": "burn baseline carries no excl-own figure; a total-vs-free "
                          "comparison would drift on markup, so not attempted"}
    user_usd = float(day.get("total") or 0.0)
    burn_usd = float(burn_usd)
    # Both sides are snapshot deltas over the same interval, so they move
    # together; the tolerance only absorbs rounding, not a real divergence.
    tol = 0.01
    return {
        "ok": user_usd >= burn_usd - tol,
        "basis": basis,
        "user_spend_day_usd": round(user_usd, 4),
        "game_burn_day_usd": round(burn_usd, 4),
        "unattributed_usd": round(user_usd - burn_usd, 4),
        "note": "positive gap = spend charged to users but held by no game "
                "(previews); negative = cost recorded against no charge",
    }


def _ledger_compare(stats_free_usd: float, ledger_free_usd: float,
                    users_with_spend: int, utc_date: str, requests: int = 0) -> dict:
    """Pure half of _daily_ledger_reconcile: compare the two sums.

    Tolerance is $0.01 per user with spend (min $0.01): each user's bucket is
    a rounded running sum, so the drift budget scales with users, not dollars.
    """
    if users_with_spend == 0 and stats_free_usd <= 0.0 and requests == 0:
        return {"ok": None, "utc_date": utc_date,
                "reason": "no free-tier spend yet today (UTC)"}
    tol = max(0.01, 0.01 * users_with_spend)
    gap = round(stats_free_usd - ledger_free_usd, 4)
    return {
        "ok": abs(gap) <= tol,
        "utc_date": utc_date,
        "request_stats_free_usd": round(stats_free_usd, 4),
        "daily_ledger_free_usd": round(ledger_free_usd, 4),
        "gap_usd": gap,
        "tolerance_usd": round(tol, 4),
        "users_with_free_spend": users_with_spend,
        "free_requests": requests,
        "note": "positive gap = cost recorded that reached no user's ledger; "
                "negative = a user was charged with no stats row behind it",
    }


def _daily_ledger_reconcile(db, now: datetime) -> dict:
    """Assert Σ requestStats.costUSD == Σ users.dailySpend.buckets.free, today UTC.

    This is exactly the check that would have caught the 2026-09-11 gap on day
    one: requestStats held $7.14 of Gemini spend for Sept 1-11 while the
    provider billed $20.56, because preview and image calls charged the user
    but wrote no stats row. Both sides here are written by the same recordSpend
    transaction, so the moment any spend path stops writing its row the left
    side falls short of the right and this prints BROKEN - the same day.

    UTC-anchored on purpose, unlike everything else in this file: `dailySpend`
    is a UTC-day field and requestStats rows carry exact timestamps, so the two
    can be cut at the same UTC midnight with no snapshot delta in between. It
    is the one check here that needs no tape.

    Free tier only. `buckets.paid` records the CHARGE (raw cost + 15% markup)
    while `requestStats.costUSD` is the RAW provider cost, so a paid-side
    compare would drift by design. No owner exclusion either: the invariant is
    the same money seen from two sides, and dropping Alex from one side only
    would manufacture a gap (his rows are paid tier anyway).

    The tier filter is applied client-side: a range on createdAt plus an
    equality on tier needs a composite index the read-only account cannot
    create, and a day of rows is small.
    """
    from google.cloud.firestore_v1 import FieldFilter

    utc_date = now.strftime("%Y-%m-%d")
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)

    stats_free = 0.0
    requests = 0
    for d in db.collection("requestStats").where(
        filter=FieldFilter("createdAt", ">=", midnight)
    ).stream():
        row = d.to_dict() or {}
        if row.get("tier") != "free":
            continue
        requests += 1
        stats_free += float(row.get("costUSD") or 0.0)

    ledger_free = 0.0
    users_with_spend = 0
    for d in db.collection(USERS).where(
        filter=FieldFilter("dailySpend.period", "==", utc_date)
    ).stream():
        ds = (d.to_dict() or {}).get("dailySpend") or {}
        free = float((ds.get("buckets") or {}).get("free") or 0.0)
        if free > 0:
            ledger_free += free
            users_with_spend += 1

    return _ledger_compare(stats_free, ledger_free, users_with_spend, utc_date, requests)


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


def _history_rows() -> list[dict]:
    """Every snapshot row, deduped by `period_date` (last write wins), oldest first.

    A manual re-run appends a second row for the same reported day. Those
    duplicates are not data - they are the same day measured twice - and left in
    place they make every delta computed off the tape wrong (the 2026-09-03
    re-run produced a row reading `users_total` delta 0 against 2 new users).
    One row per reported day, and the newest wins because it saw the most.
    """
    try:
        lines = STATS_HISTORY.read_text().splitlines()
    except OSError:
        return []
    by_day: dict[str, dict] = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        day = row.get("period_date")
        if day:
            by_day[day] = row
    return [by_day[d] for d in sorted(by_day)]


def _prev_day_row(period_date: str) -> dict | None:
    """The snapshot for the most recent reported day BEFORE `period_date`."""
    prior = [r for r in _history_rows() if (r.get("period_date") or "") < period_date]
    return prior[-1] if prior else None


def _reconcile(period: dict, users: dict) -> dict:
    """Assert total_day_end(N) - total_day_end(N-1) == new_users_day(N).

    This is the invariant the report is not allowed to talk its way around. If
    it fails, the number is broken and the report says so, in those words, with
    both sides shown. It does NOT get a narrated explanation: every previous
    mismatch here was a clock bug wearing a plausible sentence, and a report
    that explains its own discrepancies is worse than one that just breaks.
    """
    today = users.get("total_day_end")
    new = (users.get("new") or {}).get("day")
    prev = _prev_day_row(period["date"])
    if prev is None:
        return {"ok": None, "reason": "no prior day on the tape - baseline set"}
    before = prev.get("users_total_day_end")
    if before is None:
        return {"ok": None,
                "reason": f"prior day {prev.get('period_date')} predates the "
                          f"day-boundary total (added 2026-09-08)"}
    if today is None or new is None:
        return {"ok": False, "reason": "missing users_total_day_end or new_users_day"}
    delta = today - int(before)
    return {
        "ok": delta == new,
        "prev_day": prev.get("period_date"),
        "users_total_day_end_prev": int(before),
        "users_total_day_end": today,
        "delta": delta,
        "new_users_day": new,
    }


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
    sp = report.get("user_spend_mtd_usd") or {}
    day = sp.get("day") or {}
    hits = sp.get("limit_hits") or {}
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
        "users_total": u.get("total"),               # read-time count, reference only
        "users_total_day_end": u.get("total_day_end"),  # the one deltas are taken on
        "reconciles": (report.get("reconciliation") or {}).get("ok"),
        # Per-user month-to-date, carried so the NEXT run can difference it into
        # a day figure. This is the one bulky field on the tape and it earns its
        # place: `spendings` has no daily bucket, so without the prior day's map
        # there is no way to recover per-user daily spend at all. Free bucket
        # only (our cost), nonzero only, excluded owners already dropped.
        "user_mtd_period": sp.get("period"),
        "user_mtd_by_user": sp.get("by_user_free") or {},
        "user_spend_day_usd": day.get("total") if day.get("ok") else None,
        "user_spend_day_users": day.get("users_with_spend") if day.get("ok") else None,
        "limit_hits_day": hits.get("hits") if hits.get("instrumented") else None,
        "spend_reconciles": (report.get("spend_reconciliation") or {}).get("ok"),
        "ledger_reconciles": (report.get("daily_ledger_reconciliation") or {}).get("ok"),
        # Content screen day counts (rows expire after 180 days; the tape keeps the series).
        "screened_day": ((report.get("content_screen") or {}).get("day") or {}).get("total"),
        "screen_would_block_day": (((report.get("content_screen") or {}).get("day") or {}).get("verdicts") or {}).get("would_block"),
        "screen_grey_day": (((report.get("content_screen") or {}).get("day") or {}).get("verdicts") or {}).get("grey"),
        "provider_refusals_day": len((report.get("content_screen") or {}).get("refusals") or []),
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


# ─── Account farms (device + IP clustering) ──────────────────────────────────
#
# Shipped 2026-09-13, the reporting half of the multi-account work. The game now
# stamps a device id (an httpOnly cookie mirrored into localStorage) and the
# Vercel-observed client IP onto `devices/{id}` and onto the user doc.
#
# WHY: on 2026-09-11 one person ran four Google accounts - `chase.benjamin.j@`
# plus `bchase1422/1423/1424@`, display names Ben Chase / Tom Petty / Tom Hanks /
# Tom Clancy - and hopped to the next one nine minutes after the daily cap refused
# him. $28.62 between them, 41% of the month's free-tier spend. It was only caught
# because a human eyeballed the surnames. This makes it a query.
#
# Both signals are SOFT and this report never treats them as proof. One device
# with several accounts is also what a family laptop looks like; one IP with
# several accounts is also what a university or a mobile carrier looks like. The
# output is a lead to look at, never a verdict, and nothing anywhere acts on it
# automatically.

DEVICES = "devices"
# Below this, a shared browser or a shared connection is unremarkable.
CLUSTER_MIN_ACCOUNTS = 2


def _cluster_rows(devices: list[dict], excluded: set[str] | None = None) -> dict:
    """Pure: fold device docs into the multi-account clusters worth a human look.

    Takes `[{deviceId, users, ips, geo}, ...]` and returns clusters by device and,
    separately, by IP - an account farm that clears its browser between accounts
    still shares a connection, so the two views catch different halves of the same
    behaviour and neither subsumes the other.

    Alex's own account is dropped before counting: he signs in from his own
    machines constantly and would otherwise sit at the top of this list forever.
    """
    excluded = {e.lower() for e in (excluded or set())}

    def keep(emails) -> list[str]:
        return sorted({e for e in (emails or []) if isinstance(e, str)
                       and e.lower() not in excluded})

    by_device = []
    for d in devices:
        users = keep(d.get("users"))
        if len(users) >= CLUSTER_MIN_ACCOUNTS:
            by_device.append({
                "device_id": d.get("deviceId"),
                "users": users,
                "accounts": len(users),
                "ips": sorted({i for i in (d.get("ips") or []) if isinstance(i, str)}),
                "geo": d.get("geo") or {},
            })
    by_device.sort(key=lambda c: (-c["accounts"], str(c["device_id"])))

    ip_map: dict[str, set[str]] = {}
    ip_devices: dict[str, set[str]] = {}
    for d in devices:
        for ip in (d.get("ips") or []):
            if not isinstance(ip, str):
                continue
            ip_map.setdefault(ip, set()).update(keep(d.get("users")))
            if d.get("deviceId"):
                ip_devices.setdefault(ip, set()).add(d["deviceId"])
    by_ip = [
        {"ip": ip, "users": sorted(users), "accounts": len(users),
         "devices": len(ip_devices.get(ip, set()))}
        for ip, users in ip_map.items() if len(users) >= CLUSTER_MIN_ACCOUNTS
    ]
    by_ip.sort(key=lambda c: (-c["accounts"], c["ip"]))

    return {
        "instrumented": bool(devices),
        "devices_seen": len(devices),
        "by_device": by_device,
        "by_ip": by_ip,
        # A device that cleared storage shows up as a NEW device id on an OLD ip,
        # so by_ip catching more accounts than by_device is the signature of
        # someone resetting their browser between accounts.
        "storage_resets_suspected": bool(by_ip) and (
            max((c["accounts"] for c in by_ip), default=0)
            > max((c["accounts"] for c in by_device), default=0)
        ),
    }


def _new_account_links(new_emails: list[str], devices: list[dict],
                       user_docs: dict[str, dict],
                       excluded: set[str] | None = None) -> list[dict]:
    """Pure: which of the day's NEW accounts arrived on a browser or a connection
    that already belongs to another account. This is the "existing user signed
    up again" signal Alex asked for on 2026-09-14 - reported the day it
    happens, not discovered later in a cluster list.

    Three ways a new account can be tied to an old one, strongest first:
      browser     the device doc lists both emails (same cookie/localStorage id)
      inherited   the new account's user doc says `linkedVia.via == "ip"`: it
                  arrived with no id and inherited a device seen from its IP in
                  the last 12h (werewolf device-actions.ts)
      connection  none of the above, but a device of the new account shares an
                  IP with a device of another account
    One entry per new account, with the strongest tie and everyone it links to.
    """
    excluded = {e.lower() for e in (excluded or set())}
    by_id = {d.get("deviceId"): d for d in devices if d.get("deviceId")}

    def others(emails, me) -> list[str]:
        return sorted({e for e in (emails or []) if isinstance(e, str)
                       and e.lower() not in excluded and e.lower() != me.lower()})

    out = []
    for email in new_emails:
        if email.lower() in excluded:
            continue
        udoc = user_docs.get(email) or {}
        my_devices = [by_id[i] for i in (udoc.get("knownDeviceIds") or []) if i in by_id]
        # Devices that list this email but the user doc does not know about.
        my_devices += [d for d in devices if email in (d.get("users") or []) and d not in my_devices]
        tie, linked, place = None, [], {}
        for d in my_devices:
            o = others(d.get("users"), email)
            if o:
                tie, linked, place = "browser", o, d.get("geo") or {}
                break
        linked_via = udoc.get("linkedVia") or {}
        if tie is None and linked_via.get("via") == "ip":
            d = by_id.get(linked_via.get("deviceId")) or {}
            o = others(d.get("users"), email)
            if o:
                tie, linked, place = "inherited", o, d.get("geo") or {}
        if tie is None:
            my_ips = {ip for d in my_devices for ip in (d.get("ips") or []) if isinstance(ip, str)}
            o = sorted({e for d in devices if d not in my_devices
                        and my_ips & {ip for ip in (d.get("ips") or []) if isinstance(ip, str)}
                        for e in others(d.get("users"), email)})
            if o:
                tie, linked = "connection", o
                place = next((d.get("geo") for d in my_devices if d.get("geo")), {}) or {}
        if tie:
            out.append({"email": email, "tie": tie, "linked_to": linked, "geo": place})
    return out


def _device_clusters(db, new_day_emails: list[str] | None = None) -> dict:
    """Read the `devices` collection and fold it. Fail-soft: a reporting extra
    must never take the whole snapshot down."""
    try:
        docs = [d.to_dict() or {} for d in db.collection(DEVICES).stream()]
    except Exception as e:  # noqa: BLE001
        return {"instrumented": False, "reason": f"could not read {DEVICES}: {e}"}
    if not docs:
        return {"instrumented": False,
                "reason": "no device records yet - the game stamps them from the "
                          "2026-09-13 deploy onward, so this fills in as users return"}
    out = _cluster_rows(docs, EXCLUDED_OWNERS)
    user_docs: dict[str, dict] = {}
    for email in (new_day_emails or []):
        try:
            snap = db.collection(USERS).document(email).get()
            user_docs[email] = snap.to_dict() or {} if snap.exists else {}
        except Exception:  # noqa: BLE001
            user_docs[email] = {}
    out["new_account_links"] = _new_account_links(new_day_emails or [], docs, user_docs,
                                                  EXCLUDED_OWNERS)
    return out


def _new_account_lines(links: list[dict]) -> list[str]:
    """One loud line per new account tied to an existing one - the thing Alex
    wants to hear about the day it happens."""
    out = []
    how = {"browser": "same browser as",
           "inherited": "inherited the browser of (same connection within 12h)",
           "connection": "same connection as"}
    for l in links[:DIGEST_LIST_CAP]:
        where = l.get("geo") or {}
        place = ", ".join(x for x in (where.get("city"), where.get("country")) if x)
        out.append(f"  *** NEW ACCOUNT ON A KNOWN {'BROWSER' if l['tie'] != 'connection' else 'CONNECTION'}: "
                   f"{l['email']} - {how[l['tie']]} {', '.join(l['linked_to'])}"
                   + (f" ({place})" if place else "") + " ***")
    return out


# ─── Report ──────────────────────────────────────────────────────────────────


# ─── Content screen (Jev) ────────────────────────────────────────────────────
#
# Added 2026-09-19. The game now runs every piece of HUMAN text - a chat
# message, a new game's name/theme/instructions - through a Jev (typesafe.ai)
# judge before it is saved or reaches an AI provider, and writes one row per
# call to `jevScreenCalls` (werewolf `app/api/jev-screen.ts`). WHY it exists:
# every provider call goes out on the platform keys, and a provider that keeps
# receiving content it has labeled prohibited flags the account. The per-game
# provider block list only stops the second hit; the screen is meant to stop
# the first. It runs in `monitor` mode first (records a verdict, never rejects)
# and Alex reads the flagged rows here before switching it to `enforce`.
#
# Row fields this reads: createdAt (epoch ms), userEmail, source (chat |
# preview), gameId, day, text, verdict (ok | grey | would_block | error),
# reason (the flag: sexual / minors / hate / real_harm / jailbreak, or
# 'score'), riskScore (0-3), highRisk (probability on the top two levels),
# mode (monitor | enforce), enforced (bool), durationMs, costUSD.
#
# Two rules, same as the rest of this file:
#   - The day figures are the closed local day. Rows are pulled for the last
#     7 days only so a provider refusal can be joined with the messages that
#     preceded it; nothing older is counted or differenced.
#   - The join with provider refusals says what the rows say and stops. "No
#     player message was flagged before this refusal" is a fact; "so the bots
#     drifted" is a guess, and guesses are not printed.

SCREEN_CALLS = "jevScreenCalls"
SCREEN_JOIN_DAYS = 7
SCREEN_EXCERPT_CHARS = 90


def _excerpt(text: str, limit: int = SCREEN_EXCERPT_CHARS) -> str:
    flat = " ".join(str(text or "").split())
    return flat if len(flat) <= limit else flat[: limit - 1] + "…"


def _screen_rows(db, since_ms: int) -> list[dict]:
    """Every screen row since `since_ms`, oldest first. Single-field range: no index."""
    from google.cloud.firestore_v1 import FieldFilter

    rows = []
    for snap in db.collection(SCREEN_CALLS).where(
        filter=FieldFilter("createdAt", ">=", since_ms)
    ).stream():
        row = snap.to_dict() or {}
        row["id"] = snap.id
        rows.append(row)
    rows.sort(key=lambda r: r.get("createdAt") or 0)
    return rows


def _flagged_row(r: dict, excluded: set[str]) -> dict:
    owner = (r.get("userEmail") or "").lower()
    return {
        "id": r.get("id"),
        "user": r.get("userEmail"),
        "own": owner in excluded,
        "source": r.get("source"),
        "game_id": r.get("gameId"),
        "day": r.get("day"),
        "reason": r.get("reason") or "score",
        "score": round(float(r.get("riskScore") or 0.0), 2),
        "high": round(float(r.get("highRisk") or 0.0), 2),
        "mode": r.get("mode"),
        "enforced": bool(r.get("enforced")),
        "excerpt": _excerpt(r.get("text") or ""),
    }


def _screen_summary(rows: list[dict], day_start_ms: int, day_end_ms: int,
                    refusals: list[dict], excluded: set[str] | None = None) -> dict:
    """Pure reducer: 7 days of screen rows -> the day's counts, the flagged
    rows, and the refusal join. No Firestore, so it is asserted in selftest.

    `instrumented` is False when there is not a single row in the window: that
    is what the screen looks like before it is deployed or with the key
    missing, and it must read as "not running", never as "nothing flagged".
    Alex's own rows are kept OUT of the counts (he tests with edgy input on
    purpose) but any would-block of his is still listed, tagged, because a
    flagged row is a row he wants to see regardless of whose it is.
    """
    excluded = excluded if excluded is not None else EXCLUDED_OWNERS
    if not rows:
        return {"instrumented": False, "day": {}, "flagged": [], "refusals": []}

    verdicts = {"ok": 0, "grey": 0, "would_block": 0, "error": 0}
    sources = {"chat": 0, "preview": 0}
    modes: dict[str, int] = {}
    own = {"total": 0, "would_block": 0}
    enforced = 0
    today_so_far = 0
    durations: list[float] = []
    cost = 0.0
    flagged: list[dict] = []
    grey: list[dict] = []
    max_score = 0.0

    for r in rows:
        created = r.get("createdAt")
        if not isinstance(created, (int, float)):
            continue
        if created >= day_end_ms:
            today_so_far += 1
            continue
        if created < day_start_ms:
            continue
        verdict = r.get("verdict") or "ok"
        is_own = (r.get("userEmail") or "").lower() in excluded
        if verdict == "would_block":
            flagged.append(_flagged_row(r, excluded))
        if is_own:
            own["total"] += 1
            if verdict == "would_block":
                own["would_block"] += 1
            continue
        verdicts[verdict] = verdicts.get(verdict, 0) + 1
        sources[r.get("source") or "chat"] = sources.get(r.get("source") or "chat", 0) + 1
        modes[r.get("mode") or "?"] = modes.get(r.get("mode") or "?", 0) + 1
        if r.get("enforced"):
            enforced += 1
        if isinstance(r.get("durationMs"), (int, float)):
            durations.append(float(r["durationMs"]))
        cost += float(r.get("costUSD") or 0.0)
        score = float(r.get("riskScore") or 0.0)
        max_score = max(max_score, score)
        if verdict == "grey":
            grey.append(_flagged_row(r, excluded))

    flagged.sort(key=lambda x: (-x["score"], x["user"] or ""))
    grey.sort(key=lambda x: -x["score"])
    durations.sort()
    total = sum(verdicts.values())

    # Refusal join: for each provider refusal on the day, the screen rows of
    # that game (any day in the window) and the worst verdict among them.
    by_game: dict[str, list[dict]] = {}
    for r in rows:
        if r.get("gameId"):
            by_game.setdefault(r["gameId"], []).append(r)
    joined = []
    for ref in refusals:
        game_rows = by_game.get(ref.get("id") or "", [])
        worst = None
        for r in game_rows:
            s = float(r.get("riskScore") or 0.0)
            if worst is None or s > float(worst.get("riskScore") or 0.0):
                worst = r
        joined.append({
            **ref,
            "screened_messages": len(game_rows),
            "worst_verdict": (worst or {}).get("verdict"),
            "worst_reason": (worst or {}).get("reason"),
            "worst_score": round(float((worst or {}).get("riskScore") or 0.0), 2),
            "worst_excerpt": _excerpt((worst or {}).get("text") or "") if worst else None,
            "flagged_before": any((r.get("verdict") == "would_block") for r in game_rows),
        })

    return {
        "instrumented": True,
        "day": {
            "total": total,
            "verdicts": verdicts,
            "sources": sources,
            "modes": modes,
            "enforced": enforced,
            "own": own,
            "max_score": round(max_score, 2),
            "latency_ms": {
                "p50": int(_median(durations)) if durations else None,
                "max": int(durations[-1]) if durations else None,
            },
            "cost_usd": round(cost, 4),
            "today_so_far": today_so_far,
        },
        "flagged": flagged,
        "grey_top": grey[:3],
        "refusals": joined,
    }


def _content_screen(db, now: datetime, period: dict, refusals: list[dict]) -> dict:
    day_start_ms = int(period["_start_dt"].timestamp() * 1000)
    day_end_ms = int(period["_end_dt"].timestamp() * 1000)
    since_ms = min(day_start_ms, int((now - timedelta(days=SCREEN_JOIN_DAYS)).timestamp() * 1000))
    try:
        rows = _screen_rows(db, since_ms)
    except Exception as e:  # noqa: BLE001 - the screen must never break the stats report
        return {"instrumented": False, "error": str(e), "day": {}, "flagged": [], "refusals": []}
    return _screen_summary(rows, day_start_ms, day_end_ms, refusals)


def _screen_flag_line(f: dict, with_game: bool = True) -> str:
    where = f["source"]
    if f["source"] == "chat" and with_game and f.get("game_id"):
        where = f"chat, game {f['game_id']} day {f.get('day')}"
    elif f["source"] == "preview":
        where = "new game setup"
    tag = " [yours]" if f.get("own") else ""
    fate = " REJECTED" if f.get("enforced") else ""
    return (f"{f['reason']} {f['score']:.2f} - {f['user']}{tag} ({where}){fate} "
            f"\"{f['excerpt']}\"")


def _screen_refusal_line(j: dict) -> str:
    who = f"{j.get('provider')} refused \"{j.get('theme')}\" ({j.get('owner')}) on day {j.get('day')}"
    if j.get("reason"):
        who += f" [{j['reason']}]"
    n = j.get("screened_messages") or 0
    if n == 0:
        return f"{who} - no player text of this game was screened"
    if j.get("flagged_before"):
        return (f"{who} - the screen had flagged a player message "
                f"({j.get('worst_reason')} {j.get('worst_score'):.2f}, let through in monitor mode)")
    return (f"{who} - {n} player message(s) screened, none flagged "
            f"(worst {j.get('worst_verdict')} {j.get('worst_score'):.2f})")


def _screen_render_lines(screen: dict, date: str) -> list[str]:
    """The `show` section. Empty list when the screen is not running."""
    if not screen.get("instrumented"):
        why = f": {screen['error']}" if screen.get("error") else " (no jevScreenCalls rows in 7d)"
        return ["", f"  Content screen  not instrumented{why}"]
    d = screen["day"]
    v, s = d["verdicts"], d["sources"]
    modes = "/".join(sorted(d["modes"])) or "?"
    out = [
        "",
        f"  Content screen on {date}: {d['total']} screened "
        f"({s.get('chat', 0)} chat / {s.get('preview', 0)} setups) · "
        f"{v['would_block']} would-block · {v['grey']} grey · {v['error']} errors · mode {modes}"
        + (f"  (+{d['own']['total']} yours, {d['own']['would_block']} would-block)" if d["own"]["total"] else ""),
    ]
    if d["latency_ms"].get("p50") is not None:
        out.append(f"    latency p50 {d['latency_ms']['p50']} ms · max {d['latency_ms']['max']} ms · "
                   f"${d['cost_usd']:.4f} · max score {d['max_score']:.2f}")
    if d["total"] and v["error"] * 5 >= d["total"]:
        out.append(f"    ⚠ {v['error']} of {d['total']} calls failed (fail-open: those messages went through unscreened)")
    if d["enforced"]:
        out.append(f"    {d['enforced']} message(s) REJECTED (enforce mode)")
    for f in screen.get("flagged") or []:
        out.append("    would-block: " + _screen_flag_line(f))
    for f in screen.get("grey_top") or []:
        out.append(f"    grey: {f['score']:.2f} - {f['user']} ({f['source']}) \"{f['excerpt']}\"")
    refs = screen.get("refusals") or []
    if refs:
        out.append(f"    Provider refusals on {date} ({len(refs)}):")
        out.extend("      · " + _screen_refusal_line(j) for j in refs)
    if d.get("today_so_far"):
        out.append(f"    (since local midnight, PARTIAL: {d['today_so_far']} screened)")
    return out


def _screen_digest_lines(screen: dict) -> list[str]:
    """Digest lines. One status line always (so a silent screen is visible),
    then every would-block row up to the cap, then the refusal join."""
    if not screen.get("instrumented"):
        return []
    d = screen["day"]
    v = d["verdicts"]
    modes = "/".join(sorted(d["modes"])) or "?"
    out = [f"  Screen {d['total']} screened · {v['would_block']} would-block · "
           f"{v['grey']} grey [{modes}]"
           + (f" · {v['error']} errors" if v["error"] else "")
           + (f" · {d['enforced']} rejected" if d["enforced"] else "")]
    flagged = screen.get("flagged") or []
    for f in flagged[:DIGEST_LIST_CAP]:
        out.append("  risk: " + _screen_flag_line(f, with_game=False))
    if len(flagged) > DIGEST_LIST_CAP:
        out.append(f"  risk: +{len(flagged) - DIGEST_LIST_CAP} more would-block rows in the report")
    for j in (screen.get("refusals") or [])[:DIGEST_LIST_CAP]:
        out.append("  refusal: " + _screen_refusal_line(j))
    return out


def report() -> dict:
    now = _now_utc()
    try:
        db = _firestore_db()
    except RuntimeError as e:
        return {"ok": False, "checked_at": _checked_at(now), "error": str(e)}

    period = _period(now)
    users = _user_stats(db, now, period)
    games = _game_stats(db, now, period, users["new_day_emails"])
    # Read once, pass to both: the per-user day delta and the user-count
    # invariant anchor to the SAME prior row, so they can never disagree about
    # which day they are differencing against.
    prev_day_row = _prev_day_row(period["date"])
    user_spend = _user_spend(db, now, period, prev_day_row)
    burn = _daily_burn(_prev_snapshot(), games["live_cost_usd"], now, period,
                       games.get("live_cost_usd_excl_own"))
    # Game cost over the same interval as the per-user charge delta - the only
    # pair of numbers it is honest to compare or to print side by side.
    window_burn = _window_burn(prev_day_row, games.get("live_cost_usd_excl_own"), now)
    reconciliation = _reconcile(period, users)
    spend_reconciliation = _spend_reconcile(user_spend, window_burn)
    ledger_reconciliation = _daily_ledger_reconcile(db, now)
    clusters = _device_clusters(db, users.get("new_day_emails") or [])
    screen = _content_screen(db, now, period, games.get("day_refusals") or [])

    result = {
        "ok": True,
        "checked_at": _checked_at(now),
        # The day this report is ABOUT, which is not the day it ran.
        "period": {k: v for k, v in period.items() if not k.startswith("_")},
        "users": users,
        "games": games,
        "user_spend_mtd_usd": user_spend,
        # ok=True passes, False is BROKEN and must be surfaced as such, None
        # means there is nothing to check against yet.
        "reconciliation": reconciliation,
        # Same contract as `reconciliation`: False is BROKEN, None means not
        # checkable yet. Asserts user-charged money against game-recorded money.
        "spend_reconciliation": spend_reconciliation,
        # Same contract again, but UTC-anchored and tape-free: asserts every
        # free-tier requestStats row today landed in a user's dailySpend ledger.
        "daily_ledger_reconciliation": ledger_reconciliation,
        "daily_burn": burn,   # null on first run (no prior snapshot to diff)
        # Game-recorded cost since the previous day's row: the window the Spend
        # line and the spend reconciliation both use.
        "window_burn": window_burn,
        # Multi-account leads. Soft signals, never a verdict - see _cluster_rows.
        "device_clusters": clusters,
        # The Jev content screen: what human text was flagged before it reached
        # a provider, and the provider refusals of the day joined against it.
        "content_screen": screen,
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
    # ── What the day actually produced. These three are the report (2026-09-08).
    # Everything under "Reference" is a live reading of a collection with a 30d
    # TTL: a stock with an eviction policy. Differencing a stock like that gives
    # you "games went 81 -> 78" when 3 were created and 6 aged out, and "burn
    # went down" when nobody refunded anything. Those deltas are gone.
    out = [
        f"Werewolf activity for {date} ({tz}, {label})",
        f"  reported {report['checked_at']}",
        "",
        f"  New users   {n['day']}",
        f"  New games   {c['day']}"
        + (f"   ({g['created_day_by_new_users']} by that day's new users)"
           if g["created_day_by_new_users"] else ""),
        f"  Their cost  ${cc['day']:.2f} so far  (games keep accruing; this only rises)",
    ]

    # ── What users were CHARGED that day (2026-09-11) ─────────────────────────
    # Distinct from "Their cost" above, which is what games RECORDED. This line
    # is the complete one: it includes previews and images, which belong to no
    # game (and wrote no requestStats row before 2026-09-11). See _user_spend.
    sp = report.get("user_spend_mtd_usd") or {}
    spd = sp.get("day") or {}
    if spd.get("ok"):
        if spd["users_with_spend"]:
            out.append(f"  Users spent ${spd['total']:.2f} across "
                       f"{spd['users_with_spend']} user(s)"
                       f"  (median ${spd['median']:.2f}, max ${spd['max']:.2f})")
        else:
            out.append("  Users spent $0.00  (nobody was charged)")
    elif spd.get("reason"):
        out.append(f"  Users spent n/a  ({spd['reason']})")

    hits = sp.get("limit_hits") or {}
    if hits.get("instrumented"):
        if hits.get("hits"):
            out.append(f"  Limit hits  {hits['users']} user(s) hit the daily cap "
                       f"({hits['hits']} refusals, UTC {hits.get('utc_date')})")
        else:
            out.append("  Limit hits  none")
    else:
        out.append(f"  Limit hits  not instrumented yet")

    rec = report.get("reconciliation") or {}
    if rec.get("ok") is False:
        out += [
            "",
            "  *** BROKEN: the user count does not reconcile. ***",
            f"    {rec.get('users_total_day_end_prev')} at end of {rec.get('prev_day')} "
            f"-> {rec.get('users_total_day_end')} at end of {date} "
            f"= {rec.get('delta')}, but {rec.get('new_users_day')} new users were counted.",
            "    Do not trust the user figures in this report. This is a bug, not a window effect.",
        ]
    elif rec.get("ok") is None and rec.get("reason"):
        out.append(f"    (user count not yet checkable: {rec['reason']})")

    srec = report.get("spend_reconciliation") or {}
    if srec.get("ok") is False:
        out += [
            "",
            "  *** BROKEN: game cost exceeds what users were charged. ***",
            f"    users charged ${srec.get('user_spend_day_usd')} but games recorded "
            f"${srec.get('game_burn_day_usd')} on {date}.",
            "    Money left a provider key without landing on a user. This is a bug.",
        ]
    elif srec.get("ok") is True and srec.get("unattributed_usd", 0) >= 0.01:
        out.append(f"    (${srec['unattributed_usd']:.2f} charged to users but held by "
                   f"no game - previews, which belong to no game by design)")
    elif srec.get("ok") is None and srec.get("reason"):
        out.append(f"    (spend not yet checkable: {srec['reason']})")

    lrec = report.get("daily_ledger_reconciliation") or {}
    if lrec.get("ok") is False:
        out += [
            "",
            "  *** BROKEN: requestStats does not reconcile with the daily ledger. ***",
            f"    free-tier requestStats ${lrec.get('request_stats_free_usd')} vs "
            f"users.dailySpend free ${lrec.get('daily_ledger_free_usd')} on UTC "
            f"{lrec.get('utc_date')} (gap ${lrec.get('gap_usd')}, tolerance "
            f"${lrec.get('tolerance_usd')}).",
            "    A spend path is writing one record and not the other. This is a bug.",
        ]
    elif lrec.get("ok") is True:
        out.append(f"    (ledger reconciles: ${lrec.get('request_stats_free_usd'):.2f} "
                   f"free-tier across {lrec.get('free_requests')} requests, "
                   f"UTC {lrec.get('utc_date')})")
    elif lrec.get("ok") is None and lrec.get("reason"):
        out.append(f"    (ledger not yet checkable: {lrec['reason']})")

    out += [
        "",
        "  Reference (live readings, not day figures - do not difference these)",
        f"    Users at end of {date}: {u.get('total_day_end', '?')}"
        f"  ·  now {u['total']} ({u['tiers']['free']} free / "
        f"{u['tiers']['api']} api / {u['tiers']['paid']} paid)",
        f"    New users 7d/30d: {n['7d']} / {n['30d']}"
        f"  ·  new games 7d/30d: {c['7d']} / {c['30d']}",
        f"    Games live now: {g['total']}  (30d TTL - old games are deleted, "
        f"so this falls without anything going wrong)",
        f"    Cost held in live games: ${g['live_cost_usd']:.2f}"
        + (f"  (${g['live_cost_usd_excl_own']:.2f} others / "
           f"${g['own_live_cost_usd']:.2f} yours)"
           if g.get("own_live_cost_usd") else "")
        + "  - NOT cumulative spend; expired games drop out of it",
        f"    Cost of games started 7d/30d: ${cc['7d']:.2f} / ${cc['30d']:.2f}",
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

    if spd.get("ok") and spd.get("top"):
        out.append("")
        out.append(f"  Top spenders on {date}:")
        out.extend(f"    · {t['user']}  ${t['usd']:.2f}" for t in spd["top"])
    if spd.get("shrank"):
        out.append(f"    ⚠ month-to-date FELL for {len(spd['shrank'])} user(s) "
                   f"({', '.join(spd['shrank'][:3])}) - spendings is append-only, "
                   f"so this should be impossible")
    if hits.get("instrumented") and hits.get("by_user"):
        out.append("")
        out.append("  Hit the daily cap:")
        out.extend(f"    · {k}  {v}x" for k, v in hits["by_user"].items())

    # What the content screen flagged, and the day's provider refusals against it.
    out += _screen_render_lines(report.get("content_screen") or {}, date)

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
def _cluster_lines(clusters: dict) -> list[str]:
    """Digest lines for multi-account leads. Silent when there is nothing to say.

    Worded as an observation, never an accusation: a shared browser is also a
    family laptop and a shared IP is also a campus. The emails are listed because
    the whole point is that Alex can judge in two seconds what no rule can.
    """
    if not clusters.get("instrumented"):
        return []
    out: list[str] = []
    for c in clusters.get("by_device", [])[:DIGEST_LIST_CAP]:
        where = c.get("geo") or {}
        place = ", ".join(x for x in (where.get("city"), where.get("country")) if x)
        out.append(f"  shared browser: {c['accounts']} accounts"
                   + (f" ({place})" if place else "")
                   + " - " + ", ".join(c["users"]))
    # Only worth printing when it says something the device view did not: the same
    # accounts on one device would otherwise be reported twice.
    device_emails = {e for c in clusters.get("by_device", []) for e in c["users"]}
    for c in clusters.get("by_ip", [])[:DIGEST_LIST_CAP]:
        if set(c["users"]) <= device_emails:
            continue
        out.append(f"  shared connection: {c['accounts']} accounts across "
                   f"{c['devices']} browser(s) - " + ", ".join(c["users"]))
    if out and clusters.get("storage_resets_suspected"):
        out.append("  (more accounts share a connection than share a browser - "
                   "consistent with clearing storage between accounts)")
    return out


def _paid_tier_line(paid_count: int, paid_revenue_usd: float) -> str | None:
    """The paid-tier line for the digest. Tier count is NOT revenue.

    Switching tier is a free one-click button in /profile
    (ProfileTierCards -> updateUserTier); Stripe only enters later, on a
    balance top-up. The old line called a tier flip a "real paying customer",
    fired on 2026-09-11 with paid revenue at $0.00, and sent Alex hunting for
    a Stripe transaction that did not exist. Root cause found 2026-09-14: two
    fresh sign-ups had pressed Upgrade and never topped up.

    Since 2026-09-14 `paid_count` only counts paid-tier docs with a positive
    balance (see _user_stats), and a flip with no money gets NO line at all -
    Alex: "no need to tell me about paid users with 0 balance". The only line
    left hangs on money: paid-bucket spend above zero, which can only happen
    after a real top-up is drawn down.
    """
    if paid_revenue_usd > 0:
        return (f"  *** PAID REVENUE: ${paid_revenue_usd:.2f} MTD from "
                f"{paid_count} paid-tier user(s) - real money ***")
    return None


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
    - `paid revenue` is not reported as its own figure while it is $0.00 -
      daily noise that reads as a problem. The paid TIER is surfaced (see
      _paid_tier_line), but quietly and labelled as $0.00 revenue, because a
      tier switch is free and is not a payment. Only revenue above zero gets
      the loud line.
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
    wb = report.get("window_burn") or {}

    # Every money figure in the digest covers ONE interval - since the previous
    # day's snapshot - and says so. Alex, 2026-09-14: "these spending numbers
    # are not clear without the time range". His own spend is excluded
    # everywhere by default and is no longer called out; the "(+$x yours)" and
    # "(excludes ...)" decorations were noise he had already assumed.
    window = _window_label(wb.get("since"), wb.get("hours"), per.get("tz"))
    if wb.get("day_usd_excl_own") is not None:
        money = f"${wb['day_usd_excl_own']:.2f} in games"
        if wb.get("expired_games_suspected"):
            money += " (partial: games expired out of window)"
    else:
        money = f"${cc['day']:.2f} in games started that day (baseline set)"

    # Lead with the day, not the stock (2026-09-08). This block used to read
    # "Users 341 total (+3 that day)" and "Games 82 live (+1 that day)", which
    # put a read-time count and a closed-day count on one line as if one were
    # the other, and called the TTL-bounded live cost "cumulative". Alex reads
    # this block every night; it says what happened that day first, and the
    # standing totals are labelled as standing totals.
    lines = [
        f"Werewolf - {date} ({per.get('label', 'full day')}, {per.get('tz', 'local')})",
        f"  New    {un['day']} users · {gn['day']} games",
        f"  7d     {un['7d']} users · {gn['7d']} games · ${cc['7d']:.2f} in games started",
        f"  Standing: {u.get('total_day_end', u['total'])} users at day end"
        f" · {g['total']} games live now (30d TTL)"
        f" · ${g['live_cost_usd']:.2f} held in live games",
    ]

    # Per-user charged spend + the cap (2026-09-11). `money` above is what games
    # recorded; this is what users were actually charged, previews and images
    # included. Both are in the digest on purpose - a divergence between them is
    # the signal, and hiding one of them is how the Gemini drain went unnoticed
    # for eleven days.
    sp = report.get("user_spend_mtd_usd") or {}
    spd = sp.get("day") or {}
    if spd.get("ok"):
        top = (spd.get("top") or [{}])[0]
        lines.insert(2, f"  Spend  ${spd['total']:.2f} charged to "
                        f"{spd['users_with_spend']} user(s)"
                        + (f" · median ${spd['median']:.2f} · top {top['user']} "
                           f"${top['usd']:.2f}" if top.get("user") else "")
                        + f" · {money}"
                        + (f"  [{window}]" if window else ""))
    elif spd.get("reason"):
        lines.insert(2, f"  Spend  n/a ({spd['reason']})")

    hits = sp.get("limit_hits") or {}
    if hits.get("instrumented") and hits.get("hits"):
        lines.insert(3, f"  Cap    {hits['users']} user(s) hit the daily limit "
                        f"({hits['hits']} refusals)")

    rec = report.get("reconciliation") or {}
    if rec.get("ok") is False:
        lines.append(f"  BROKEN: user count does not reconcile "
                     f"({rec.get('delta')} from totals vs {rec.get('new_users_day')} "
                     f"new users) - figures not trustworthy")
    srec = report.get("spend_reconciliation") or {}
    if srec.get("ok") is False:
        lines.append(f"  BROKEN: games recorded ${srec.get('game_burn_day_usd')} but "
                     f"users were charged ${srec.get('user_spend_day_usd')} over the "
                     f"same window{(' [' + window + ']') if window else ''} - cost "
                     f"with no payer")
    lrec = report.get("daily_ledger_reconciliation") or {}
    if lrec.get("ok") is False:
        lines.append(f"  BROKEN: requestStats ${lrec.get('request_stats_free_usd')} vs "
                     f"daily ledger ${lrec.get('daily_ledger_free_usd')} (free tier, UTC "
                     f"{lrec.get('utc_date')}) - a spend path is missing a record")

    r = report.get("user_spend_mtd_usd") or report.get("revenue_mtd_usd") or {}
    line = _paid_tier_line((u.get("tiers") or {}).get("paid") or 0,
                           float(r.get("paid") or 0.0))
    if line:
        lines.append(line)

    clusters = report.get("device_clusters") or {}
    # New accounts tied to existing ones go right under the day line: it is the
    # one thing in here Alex wants to see the day it happens.
    for i, l in enumerate(_new_account_lines(clusters.get("new_account_links") or [])):
        lines.insert(2 + i, l)
    lines.extend(_cluster_lines(clusters))
    # High-risk player text and provider refusals (2026-09-19): the rows Alex
    # reads to decide when the screen moves from monitor to enforce.
    lines.extend(_screen_digest_lines(report.get("content_screen") or {}))

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
    return "\n".join(lines)


# ─── Self-test ───────────────────────────────────────────────────────────────


def selftest() -> bool:
    """Exercise the pure reducers with no Firestore and no network.

    There is no test framework in this repo, and the per-user day figure is
    a DELTA - the class of number that is silently wrong rather than loudly
    broken. The month-rollover and MTD-went-down branches in particular cannot
    be triggered on demand against live data: one needs a calendar boundary,
    the other needs corrupt data. So they are asserted here instead.

    `python handlers/werewolf_stats.py selftest` - run it after touching
    _spend_day, _spend_reconcile or _ledger_compare.
    """
    fails: list[str] = []

    def check(label, got, want):
        if got != want:
            fails.append(f"{label}\n     got : {got}\n     want: {want}")
        print(("  PASS  " if got == want else "  FAIL  ") + label)

    prev = {"period_date": "2026-09-10", "user_mtd_period": "2026-09",
            "user_mtd_by_user": {"a@x": 1.00, "b@x": 5.00, "c@x": 2.00}}
    now = {"a@x": 3.50, "b@x": 5.00, "c@x": 2.25, "new@x": 0.75}

    print("_spend_day")
    d = _spend_day(now, "2026-09", prev)
    # a +2.50, c +0.25, new +0.75 = 3.50. b did not move and must not appear.
    check("counts only movers, sums to 3.50",
          (d["ok"], d["users_with_spend"], d["total"]), (True, 3, 3.50))
    check("median of [2.50, 0.25, 0.75]", d["median"], 0.75)
    check("max", d["max"], 2.50)
    check("unmoved user excluded from top",
          [t["user"] for t in d["top"]], ["a@x", "new@x", "c@x"])
    check("month rollover refuses a number",
          _spend_day(now, "2026-09", dict(prev, user_mtd_period="2026-08"))["ok"], False)
    check("no prior row refuses", _spend_day(now, "2026-09", None)["ok"], False)
    check("legacy row without the map refuses",
          _spend_day(now, "2026-09", {"period_date": "2026-09-01"})["ok"], False)
    shrunk = _spend_day({"b@x": 4.00}, "2026-09", prev)
    check("MTD going DOWN is surfaced", shrunk["shrank"], ["b@x"])
    check("MTD going DOWN is not counted as spend", shrunk["total"], 0.0)

    print("_spend_reconcile")
    day = {"ok": True, "total": 10.00}
    check("user > game passes, gap reported",
          (lambda r: (r["ok"], r["unattributed_usd"]))(
              _spend_reconcile({"day": day}, {"day_usd_excl_own": 7.50})), (True, 2.50))
    check("game > user is BROKEN",
          _spend_reconcile({"day": day}, {"day_usd_excl_own": 12.00})["ok"], False)
    check("rounding tolerated",
          _spend_reconcile({"day": day}, {"day_usd_excl_own": 10.005})["ok"], True)
    check("no day figure -> not checkable",
          _spend_reconcile({"day": {"ok": False, "reason": "x"}},
                           {"day_usd_excl_own": 1.0})["ok"], None)
    check("no burn -> not checkable", _spend_reconcile({"day": day}, None)["ok"], None)
    check("no excl-own basis -> not checkable, never a drifting compare",
          _spend_reconcile({"day": day}, {"day_usd": 5.0})["ok"], None)

    print("_window_burn / _window_label")
    row = {"checked_at": "2026-09-13T05:36:01Z", "live_cost_usd_excl_own": 67.5251}
    wb = _window_burn(row, 75.5805, datetime(2026, 9, 14, 15, 38, 32, tzinfo=timezone.utc))
    check("game burn over the user-delta window", (wb["day_usd_excl_own"], wb["hours"]), (8.0554, 34.0))
    check("no prior row -> no figure", _window_burn(None, 1.0, datetime.now(timezone.utc)), None)
    check("legacy row without excl-own -> no figure",
          _window_burn({"checked_at": "2026-09-13T05:36:01Z"}, 1.0, datetime.now(timezone.utc)), None)
    check("window label is local time",
          _window_label("2026-09-13T05:36:01Z", 34.0, "America/New_York"), "since Sep 13 01:36 EDT (34h)")

    print("_new_account_links")
    DEVS = [
        {"deviceId": "dev-A", "ips": ["1.1.1.1"], "geo": {"city": "Tampa", "country": "US"},
         "users": ["old@x", "fresh@x"]},
        {"deviceId": "dev-B", "ips": ["1.1.1.1"], "users": ["wiped@x"]},
        {"deviceId": "dev-C", "ips": ["9.9.9.9"], "users": ["alone@x"]},
        {"deviceId": "dev-D", "ips": ["5.5.5.5"], "users": ["inherit@x", "owner@x"]},
    ]
    UDOCS = {"fresh@x": {"knownDeviceIds": ["dev-A"]},
             "wiped@x": {"knownDeviceIds": ["dev-B"]},
             "alone@x": {"knownDeviceIds": ["dev-C"]},
             "inherit@x": {"knownDeviceIds": ["dev-D"], "linkedVia": {"via": "ip", "deviceId": "dev-D"}}}
    links = _new_account_links(["fresh@x", "wiped@x", "alone@x", "inherit@x", "alex@x"], DEVS, UDOCS, {"alex@x"})
    check("same browser is the strongest tie",
          [(l["email"], l["tie"], l["linked_to"]) for l in links if l["email"] == "fresh@x"],
          [("fresh@x", "browser", ["old@x"])])
    check("new device on an old IP is a connection tie",
          [(l["tie"], l["linked_to"]) for l in links if l["email"] == "wiped@x"], [("connection", ["fresh@x", "old@x"])])
    check("an account alone on its browser and IP is not reported",
          [l for l in links if l["email"] == "alone@x"], [])
    check("linkedVia ip on a shared device reads as browser (both emails on the doc)",
          [l["tie"] for l in links if l["email"] == "inherit@x"], ["browser"])
    check("excluded owner never reported", [l for l in links if l["email"] == "alex@x"], [])
    check("digest line names the tie and the place",
          _new_account_lines(links[:1])[0],
          "  *** NEW ACCOUNT ON A KNOWN BROWSER: fresh@x - same browser as old@x (Tampa, US) ***")

    print("_cluster_rows")
    FARM = [
        {"deviceId": "dev-A", "ips": ["1.1.1.1"], "geo": {"city": "Tampa", "country": "US"},
         "users": ["chase.benjamin.j@x", "bchase1423@x", "bchase1424@x"]},
        {"deviceId": "dev-B", "ips": ["2.2.2.2"], "users": ["solo@x"]},
    ]
    c = _cluster_rows(FARM)
    check("only multi-account devices are reported",
          [d["device_id"] for d in c["by_device"]], ["dev-A"])
    check("accounts are listed so a human can judge",
          c["by_device"][0]["users"],
          ["bchase1423@x", "bchase1424@x", "chase.benjamin.j@x"])
    check("a one-account device is not a cluster",
          any(d["device_id"] == "dev-B" for d in c["by_device"]), False)
    check("Alex's own account never makes a cluster",
          _cluster_rows([{"deviceId": "d", "users": ["hiper2d@gmail.com", "someone@x"]}],
                        {"hiper2d@gmail.com"})["by_device"], [])

    # Same person, storage cleared between accounts: three device ids, one IP.
    RESET = [
        {"deviceId": "d1", "ips": ["9.9.9.9"], "users": ["a@x"]},
        {"deviceId": "d2", "ips": ["9.9.9.9"], "users": ["b@x"]},
        {"deviceId": "d3", "ips": ["9.9.9.9"], "users": ["c@x"]},
    ]
    r = _cluster_rows(RESET)
    check("no shared BROWSER when storage was cleared each time", r["by_device"], [])
    check("but the shared CONNECTION still catches all three",
          (r["by_ip"][0]["accounts"], r["by_ip"][0]["devices"]), (3, 3))
    check("and the reset pattern is named", r["storage_resets_suspected"], True)
    check("a plain farm on one browser is not called a reset",
          _cluster_rows(FARM)["storage_resets_suspected"], False)
    check("no devices at all -> not instrumented", _cluster_rows([])["instrumented"], False)

    print("_cluster_lines")
    check("nothing instrumented -> no digest lines", _cluster_lines({"instrumented": False}), [])
    check("no clusters -> no digest lines",
          _cluster_lines(_cluster_rows([{"deviceId": "d", "users": ["solo@x"]}])), [])
    farm_lines = _cluster_lines(_cluster_rows(FARM))
    check("the farm produces one shared-browser line", len(farm_lines), 1)
    check("it names the place and every account",
          ("Tampa" in farm_lines[0], "bchase1424@x" in farm_lines[0]), (True, True))
    check("the wording observes, never accuses",
          any(w in farm_lines[0].lower() for w in ("abuse", "cheat", "fraud", "farm")), False)
    check("an IP cluster already covered by a device cluster is not repeated",
          len(_cluster_lines(_cluster_rows(FARM))), 1)

    print("_paid_tier_line")
    check("nobody on the paid tier -> no line", _paid_tier_line(0, 0.0), None)
    check("tier flip with no money prints nothing (Alex, 2026-09-14)",
          _paid_tier_line(1, 0.0), None)
    check("revenue above zero is the loud line",
          "*** PAID REVENUE: $4.20" in (_paid_tier_line(1, 4.20) or ""), True)
    check("revenue with no tier count still reports the money",
          "*** PAID REVENUE" in (_paid_tier_line(0, 1.00) or ""), True)

    print("_ledger_compare")
    check("agreeing sums pass",
          _ledger_compare(7.14, 7.145, 3, "2026-09-11", 40)["ok"], True)
    check("tolerance scales per user ($0.02 gap, 3 users)",
          _ledger_compare(7.14, 7.16, 3, "2026-09-11", 40)["ok"], True)
    check("the 2026-09-11 gap ($7.14 vs $20.56) is BROKEN",
          _ledger_compare(7.14, 20.56, 6, "2026-09-11", 40)["ok"], False)
    check("stats rows with no ledger behind them is BROKEN",
          _ledger_compare(0.50, 0.0, 0, "2026-09-11", 4)["ok"], False)
    check("a charge with no stats row behind it is BROKEN",
          _ledger_compare(0.0, 0.50, 1, "2026-09-11", 0)["ok"], False)
    check("nothing on either side -> not checkable",
          _ledger_compare(0.0, 0.0, 0, "2026-09-11", 0)["ok"], None)
    check("minimum tolerance is $0.01",
          _ledger_compare(1.00, 1.005, 1, "2026-09-11", 1)["ok"], True)

    print("_screen_summary")
    DAY0, DAY1 = 1_000_000, 2_000_000   # the closed day is [DAY0, DAY1)
    def srow(created, verdict, score, user="p@x", reason=None, **kw):
        return {"id": f"r{created}", "createdAt": created, "verdict": verdict,
                "riskScore": score, "highRisk": 0.9 if verdict == "would_block" else 0.05,
                "userEmail": user, "source": kw.get("source", "chat"),
                "gameId": kw.get("game", "g1"), "day": 2, "mode": kw.get("mode", "monitor"),
                "enforced": kw.get("enforced", False), "reason": reason,
                "text": kw.get("text", "Come here, my loyal boy."), "durationMs": 200, "costUSD": 0.00003}
    ROWS = [
        srow(DAY0 + 10, "ok", 0.15),
        srow(DAY0 + 20, "grey", 1.30, text="Guts all over the barn floor, head half chewed off."),
        srow(DAY0 + 30, "would_block", 1.97, reason="sexual"),
        srow(DAY0 + 40, "would_block", 2.80, user="q@x", reason="real_harm", source="preview", game=None),
        srow(DAY0 + 50, "would_block", 3.00, user="hiper2d@gmail.com", reason="minors", game="g9"),
        srow(DAY0 + 60, "error", 0.0),
        srow(DAY0 - 500, "would_block", 2.0, reason="hate", game="g7"),   # day before: joins, not counted
        srow(DAY1 + 5, "ok", 0.1),                                         # day in progress
    ]
    EXCL = {"hiper2d@gmail.com"}
    check("no rows at all -> not instrumented",
          _screen_summary([], DAY0, DAY1, [], EXCL)["instrumented"], False)
    s = _screen_summary(ROWS, DAY0, DAY1, [], EXCL)
    check("counts cover the closed day only, own rows excluded",
          (s["day"]["total"], s["day"]["verdicts"]), (5, {"ok": 1, "grey": 1, "would_block": 2, "error": 1}))
    check("sources split chat / preview", s["day"]["sources"], {"chat": 4, "preview": 1})
    check("own rows are counted apart", s["day"]["own"], {"total": 1, "would_block": 1})
    check("the day in progress is reported as partial", s["day"]["today_so_far"], 1)
    check("flagged rows are every would-block of the day, highest score first, own tagged",
          [(f["user"], f["score"], f["own"]) for f in s["flagged"]],
          [("hiper2d@gmail.com", 3.0, True), ("q@x", 2.8, False), ("p@x", 1.97, False)])
    check("a flagged row names the reason and quotes the text",
          _screen_flag_line(s["flagged"][2]),
          'sexual 1.97 - p@x (chat, game g1 day 2) "Come here, my loyal boy."')
    check("the digest opens with one status line and lists the would-blocks",
          (_screen_digest_lines(s)[0], len(_screen_digest_lines(s))),
          ("  Screen 5 screened · 2 would-block · 1 grey [monitor] · 1 errors", 4))
    check("the digest is silent when the screen is not running",
          _screen_digest_lines({"instrumented": False}), [])
    long_text = "x" * 200
    check("excerpts are capped", len(_excerpt(long_text)), SCREEN_EXCERPT_CHARS)
    REFS = [
        {"id": "g1", "theme": "Dracula", "owner": "p@x", "provider": "Google", "reason": "PROHIBITED_CONTENT", "day": 2},
        {"id": "g7", "theme": "Manor", "owner": "p@x", "provider": "Google", "reason": "SAFETY", "day": 3},
        {"id": "g5", "theme": "Island", "owner": "z@x", "provider": "Qwen", "reason": None, "day": 1},
    ]
    j = _screen_summary(ROWS, DAY0, DAY1, REFS, EXCL)["refusals"]
    # g1 has five rows in the window: four in the day and one from the day in
    # progress - the join takes the whole window on purpose.
    check("a refusal is joined with the game's flagged message",
          (j[0]["flagged_before"], j[0]["worst_reason"], j[0]["screened_messages"]), (True, "sexual", 5))
    check("the join reaches back before the reported day", (j[1]["flagged_before"], j[1]["worst_reason"]), (True, "hate"))
    check("a refused game with no screened text says so",
          _screen_refusal_line(j[2]), 'Qwen refused "Island" (z@x) on day 1 - no player text of this game was screened')
    check("the join states facts and never a mechanism",
          any(w in _screen_refusal_line(x).lower() for x in j for w in ("drift", "probably", "likely")), False)

    print()
    if fails:
        print(f"{len(fails)} FAILURE(S):")
        for f in fails:
            print("   " + f)
        return False
    print("all checks pass")
    return True


# ─── CLI ─────────────────────────────────────────────────────────────────────


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("report", help="Compute + persist a full activity snapshot (JSON)")
    sub.add_parser("show", help="Render the last persisted snapshot, human-readable")
    sub.add_parser("digest", help="Capped digest block from the last snapshot (for notify --digest)")
    sub.add_parser("selftest", help="Assert the pure spend reducers (no Firestore, no network)")
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
    elif args.cmd == "selftest":
        sys.exit(0 if selftest() else 1)


if __name__ == "__main__":
    main()
