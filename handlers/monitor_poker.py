"""
monitor_poker — broken-game watch + activity pulse for Poker with AI (pokerwithai.net).

Poker is the second game on the same Firebase project as Werewolf. Only `config`
is shared; every poker collection carries the `poker_` prefix (`poker_games`,
`poker_users`, `poker_requestStats`). The read-only service account Marlow
already holds (MARLOW_FIREBASE_CREDS) reads them — no new credential.

Why a separate handler and not a flag on monitor_health: the error model differs.
Werewolf keeps ONE `errorState` per game. Poker runs two independent lanes — the
game lane (cards, betting, memory compaction) and the chat lane (intros, table
talk) — and each lane keeps its own error slot on the game doc:
    gameError / chatError: {message, details, failedAction, actor?, model?,
                            retryable, timestamp(ms)}
A set error stops THAT lane's pump until the player clears it (clearing is the
retry, as in Werewolf). So:
  - a game-lane error means the hand is stuck → urgent (the player is staring
    at a frozen table and will leave);
  - a chat-lane error means the table went quiet but the hand plays on → digest.
`retryable: false` is a routing (Pit Boss) failure that left nothing queued; the
player recovers by nudging the table. Reported, not escalated.

Betterstack is NOT part of this watch (yet): Poker's production deployment has no
`LOGTAIL_SOURCE_TOKEN` set (poker-with-ai TODO.md, confirmed 2026-10-31 — zero
poker lines in the Werewolf source over 30 days), so the app ships no logs
anywhere. When a source exists, monitor_betterstack's table/field handling is the
model to copy; until then the lane errors on the game doc are the only error
signal, and they ARE the signal the player sees.

Noise control — monitor_health's discipline exactly: alert on errors that
appeared SINCE THE LAST SCAN, never the standing pile.
  - First run with no prior state → BASELINE the current errored set, one
    digest summary, no urgent ping.
  - Later runs → a lane error is keyed `<gameId>:<lane>:<timestamp>`, so a game
    that errors, is retried and errors again counts as new (the timestamp
    moves); a cleared error drops out.

Activity pulse (digest only, never urgent): Poker gets a handful of tables a
MONTH, each from a stranger who signs up, plays one game and leaves (read
2026-10-31: 14 live games, 16 users, nobody twice). A new table or signup since
the last scan is one digest line with theme, hands played, model cost and
whether the player is new — so Alex sees a stranger trying it the same day,
which the daily Werewolf digest never shows. Own-account games are tagged
`(own)` and never counted as a stranger.

CLI:
    python handlers/monitor_poker.py report   → scan + persist, JSON + issues
    python handlers/monitor_poker.py show      → last snapshot, human-readable
    python handlers/monitor_poker.py digest    → digest block for notify ("" if quiet)
    python handlers/monitor_poker.py selftest  → offline asserts, no network
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from driver.env_loader import import_plist_env  # noqa: E402
import_plist_env()

from handlers.monitor_keys import _firestore_db  # noqa: E402
from driver.budget_state import STATE_DIR  # noqa: E402

GAMES = "poker_games"
USERS = "poker_users"
LANES = {"game": "gameError", "chat": "chatError"}
OWN_ACCOUNTS = {"hiper2d@gmail.com"}
# Activity pulse: how far back a game/user counts as "new" when there is no prior
# scan to diff against (first run), and a hard cap so a dead scheduler coming back
# after a week does not replay a week as one burst.
ACTIVITY_LOOKBACK_H = 6
ACTIVITY_MAX_H = 48
MAX_ACTIVITY_LINES = 10

POKER_LATEST = STATE_DIR / "poker_latest.json"
POKER_HISTORY = STATE_DIR / "poker_history.jsonl"


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _iso(ms: int | float | None) -> str | None:
    if not ms:
        return None
    try:
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).replace(microsecond=0) \
            .isoformat().replace("+00:00", "Z")
    except (ValueError, OSError, OverflowError, TypeError):
        return None


def _age_hours(ms: int | float | None, now: datetime) -> float | None:
    if not ms:
        return None
    try:
        return round((now.timestamp() - ms / 1000) / 3600, 1)
    except TypeError:
        return None


def _mask(email: str | None) -> str:
    """Owner shown as `ab…@domain` — enough to tell accounts apart in Telegram,
    not a full address in a chat log."""
    if not email or "@" not in email:
        return email or "?"
    if email in OWN_ACCOUNTS:
        return "(own)"
    local, domain = email.split("@", 1)
    return f"{local[:2]}…@{domain}"


# ─── Errors ──────────────────────────────────────────────────────────────────


def _summarize_error(err: dict, lane: str, game: dict, game_id: str, now: datetime) -> dict:
    ts = err.get("timestamp")
    details = (err.get("details") or "")
    first_line = details.splitlines()[0].strip() if details else "(no details)"
    return {
        "key": f"{game_id}:{lane}:{ts}",
        "id": game_id,
        "lane": lane,
        "theme": game.get("theme") or "(untitled)",
        "owner": _mask(game.get("createdBy")),
        "state": game.get("status"),
        "hand": game.get("handNumber"),
        "actor": err.get("actor"),
        "model": err.get("model"),
        "failed_action": err.get("failedAction"),
        "retryable": bool(err.get("retryable", True)),
        "message": (err.get("message") or "")[:160],
        "summary": first_line[:160],
        "error_at": _iso(ts),
        "age_hours": _age_hours(ts, now),
    }


def _errors_of(game: dict, game_id: str, now: datetime) -> list[dict]:
    rows = []
    for lane, field in LANES.items():
        err = game.get(field)
        if err:
            rows.append(_summarize_error(err, lane, game, game_id, now))
    return rows


def _derive_error_issues(errored: list[dict], prior: set[str] | None) -> tuple[list[dict], bool]:
    """Issues for lane errors that appeared SINCE the last scan. Returns (issues, baselined)."""
    if prior is None:
        if errored:
            return ([{
                "severity": "digest",
                "kind": "poker_baseline",
                "target": GAMES,
                "detail": f"baseline: {len(errored)} lane error(s) on first scan "
                          f"(not alerting — pre-existing). New errors alert from here.",
            }], True)
        return ([], True)

    issues = []
    for r in errored:
        if r["key"] in prior:
            continue
        stuck = r["lane"] == "game"
        who = f" — {r['actor']}" if r.get("actor") else ""
        model = f" on {r['model']}" if r.get("model") else ""
        retry = "" if r["retryable"] else ", no retry offered"
        issues.append({
            "severity": "urgent" if stuck else "digest",
            "kind": "poker_hand_stuck" if stuck else "poker_chat_error",
            "target": r["id"],
            "detail": f"{r['theme']} ({r['owner']}) hand {r['hand']}: {r['lane']} lane "
                      f"failed in {r['failed_action'] or '?'}{who}{model}{retry}: "
                      f"{r['summary']}",
        })
    return (issues, False)


# ─── Activity ────────────────────────────────────────────────────────────────


def _summarize_game(game: dict, game_id: str, new_user_emails: set[str]) -> dict:
    owner = game.get("createdBy")
    return {
        "id": game_id,
        "theme": game.get("theme") or "(untitled)",
        "owner": _mask(owner),
        "own": owner in OWN_ACCOUNTS,
        "new_user": owner in new_user_emails,
        "tier": game.get("createdWithTier"),
        "status": game.get("status"),
        "hands": game.get("handNumber") or 0,
        "messages": game.get("messageCounter") or 0,
        "bots": len(game.get("bots") or []),
        "models": sorted({b.get("aiType") for b in (game.get("bots") or []) if b.get("aiType")}),
        "gm": game.get("gameMasterAiType"),
        "cost_usd": round(float(game.get("totalGameCost") or 0), 4),
        "created_at": _iso(game.get("createdAt")),
        "created_ms": game.get("createdAt") or 0,
    }


def _activity_since(prior_checked_ms: int | None, now: datetime) -> int:
    """Lower bound (ms) for 'new' — the last scan, else a short lookback; never
    further back than ACTIVITY_MAX_H so a stalled scheduler can't replay a week."""
    now_ms = int(now.timestamp() * 1000)
    floor = now_ms - ACTIVITY_MAX_H * 3600 * 1000
    if prior_checked_ms is None:
        return now_ms - ACTIVITY_LOOKBACK_H * 3600 * 1000
    return max(prior_checked_ms, floor)


def _derive_activity_issues(new_games: list[dict], new_users: int) -> list[dict]:
    issues = []
    for g in new_games[:MAX_ACTIVITY_LINES]:
        tag = "own game" if g["own"] else ("new player" if g["new_user"] else "returning player")
        issues.append({
            "severity": "digest",
            "kind": "poker_new_game",
            "target": g["id"],
            "detail": f"new table: {g['theme']} ({g['owner']}, {tag}, {g['tier']}) — "
                      f"{g['hands']} hand(s), {g['messages']} msgs, {g['bots']} bots, "
                      f"${g['cost_usd']:.3f}, state {g['status']}",
        })
    if len(new_games) > MAX_ACTIVITY_LINES:
        issues.append({"severity": "digest", "kind": "poker_new_game", "target": GAMES,
                       "detail": f"… +{len(new_games) - MAX_ACTIVITY_LINES} more new tables"})
    stranger_signups = new_users
    if stranger_signups:
        issues.append({
            "severity": "digest",
            "kind": "poker_new_user",
            "target": USERS,
            "detail": f"{stranger_signups} new signup(s) at pokerwithai.net",
        })
    return issues


# ─── Scan / state ────────────────────────────────────────────────────────────


def _prior() -> dict | None:
    try:
        with POKER_LATEST.open() as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def _scan(db, now: datetime, prior: dict | None) -> dict:
    since_ms = _activity_since(prior.get("checked_ms") if prior else None, now)

    users = [u.to_dict() or {} for u in db.collection(USERS).stream()]
    new_user_emails = {u.get("email") for u in users
                       if (u.get("createdAt") or 0) >= since_ms and u.get("email")}
    stranger_signups = len(new_user_emails - OWN_ACCOUNTS)

    errored: list[dict] = []
    new_games: list[dict] = []
    total = 0
    for snap in db.collection(GAMES).stream():
        g = snap.to_dict() or {}
        total += 1
        errored.extend(_errors_of(g, snap.id, now))
        if (g.get("createdAt") or 0) >= since_ms:
            new_games.append(_summarize_game(g, snap.id, new_user_emails))
    errored.sort(key=lambda r: r["error_at"] or "", reverse=True)
    new_games.sort(key=lambda g: g["created_ms"], reverse=True)
    return {
        "games_total": total,
        "users_total": len(users),
        "errored": errored,
        "new_games": new_games,
        "new_users": stranger_signups,
        "since": _iso(since_ms),
    }


def _compact(report: dict) -> dict:
    return {
        "checked_at": report.get("checked_at"),
        "games_total": report.get("games_total"),
        "users_total": report.get("users_total"),
        "errored_total": len(report.get("errored", [])),
        "new_games": len(report.get("new_games", [])),
        "new_users": report.get("new_users"),
        "any_urgent": report.get("any_urgent"),
        "issues": [f"{i['severity']}:{i['kind']}:{i['target']}" for i in report.get("issues", [])],
    }


def _save(report: dict) -> None:
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        tmp = POKER_LATEST.with_suffix(".json.tmp")
        with tmp.open("w") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        tmp.replace(POKER_LATEST)
        with POKER_HISTORY.open("a") as f:
            f.write(json.dumps(_compact(report), ensure_ascii=False) + "\n")
    except OSError:
        pass


def report() -> dict:
    now = _now_utc()
    try:
        db = _firestore_db()
    except RuntimeError as e:
        return {"ok": False, "checked_at": _checked_at(now), "error": str(e)}

    prior = _prior()                      # read BEFORE we overwrite latest
    prior_keys = {r["key"] for r in prior.get("errored", [])} if prior else None
    scan = _scan(db, now, prior)
    err_issues, baselined = _derive_error_issues(scan["errored"], prior_keys)
    act_issues = _derive_activity_issues(scan["new_games"], scan["new_users"])
    issues = err_issues + act_issues
    result = {
        "ok": True,
        "checked_at": _checked_at(now),
        "checked_ms": int(now.timestamp() * 1000),
        **scan,
        "errored_count": len(scan["errored"]),
        "issues": issues,
        "any_urgent": any(i["severity"] == "urgent" for i in issues),
        "baselined": baselined,
    }
    _save(result)
    return result


def _checked_at(now: datetime) -> str:
    return now.replace(microsecond=0).isoformat().replace("+00:00", "Z")


# ─── Renders ─────────────────────────────────────────────────────────────────


def render(report: dict) -> str:
    if not report.get("ok"):
        return f"monitor_poker failed: {report.get('error', 'unknown')}"
    out = [f"Poker health — {report['checked_at']}", ""]
    out.append(f"  {report.get('games_total', '?')} live table(s), {report.get('users_total', '?')} user(s); "
               f"{len(report.get('errored', []))} lane error(s) standing")
    for r in report.get("errored", [])[:10]:
        age = f"{r['age_hours']}h ago" if r["age_hours"] is not None else "age ?"
        out.append(f"    · {r['theme']} ({r['owner']}) — {r['lane']} lane, hand {r['hand']}, "
                   f"{age}, {r['state']}, {r.get('actor') or '?'} on {r.get('model') or '?'}")
        out.append(f"        {r['summary']}")
    new_games = report.get("new_games", [])
    out.append("")
    out.append(f"  Since {report.get('since')}: {len(new_games)} new table(s), "
               f"{report.get('new_users', 0)} new signup(s)")
    for g in new_games[:10]:
        out.append(f"    · {g['created_at']} {g['theme']} ({g['owner']}) — {g['hands']} hands, "
                   f"{g['bots']} bots on {', '.join(g['models']) or '?'}, GM {g['gm']}, ${g['cost_usd']:.3f}")
    issues = report.get("issues", [])
    out.append("")
    if issues:
        out.append("  Issues this scan:")
        for i in issues:
            mark = "🔴" if i["severity"] == "urgent" else "⚠️" if i["kind"].endswith("error") or i["kind"].endswith("stuck") else "·"
            out.append(f"    {mark} [{i['severity']}] {i['detail']}")
    else:
        out.append("  Quiet: no new errors, tables or signups since last scan.")
    return "\n".join(out)


def render_digest(report: dict) -> str | None:
    """Digest block — only when something happened. None on a quiet scan so the
    daily digest gets no Poker line at all on most days."""
    if not report.get("ok"):
        return f"Poker health: scan failed ({report.get('error', 'unknown')})."
    issues = report.get("issues", [])
    if not issues:
        return None
    date = (report.get("checked_at") or "")[:10]
    n_err = sum(1 for i in issues if i["kind"] in ("poker_hand_stuck", "poker_chat_error"))
    n_act = len(issues) - n_err
    parts = []
    if n_err:
        parts.append(f"{n_err} new error(s)" + (" (urgent)" if report.get("any_urgent") else ""))
    if n_act:
        parts.append(f"{len(report.get('new_games', []))} new table(s), {report.get('new_users', 0)} signup(s)")
    head = f"Poker — {date}: " + ", ".join(parts)
    return "\n".join([head] + [f"  · {i['detail']}" for i in issues])


# ─── Selftest ────────────────────────────────────────────────────────────────


def selftest() -> None:
    """Offline asserts on the pure parts — no Firestore, no state files."""
    now = datetime(2026, 10, 31, 12, 0, tzinfo=timezone.utc)
    ts = int(now.timestamp() * 1000) - 3600_000
    game = {
        "theme": "Dune", "createdBy": "ab@example.com", "status": "BETTING", "handNumber": 2,
        "gameError": {"message": "Paul's model timed out", "details": "AiCallError: timeout\n  at x",
                      "failedAction": "DECISION", "actor": "Paul", "model": "claude", "retryable": True,
                      "timestamp": ts},
        "chatError": {"message": "Table quiet", "details": "Pit Boss refused", "failedAction": "ROUTE",
                      "actor": "PIT_BOSS", "retryable": False, "timestamp": ts},
    }
    errs = _errors_of(game, "g1", now)
    assert [e["lane"] for e in errs] == ["game", "chat"], errs
    assert errs[0]["key"] == f"g1:game:{ts}" and errs[0]["age_hours"] == 1.0
    assert errs[0]["owner"] == "ab…@example.com"

    # first scan → baseline, nothing urgent
    issues, baselined = _derive_error_issues(errs, None)
    assert baselined and len(issues) == 1 and issues[0]["severity"] == "digest"
    # known keys → silent
    issues, baselined = _derive_error_issues(errs, {e["key"] for e in errs})
    assert not baselined and issues == []
    # game lane new → urgent; chat lane new → digest, flags no-retry
    issues, _ = _derive_error_issues(errs, set())
    assert [i["severity"] for i in issues] == ["urgent", "digest"], issues
    assert "no retry offered" in issues[1]["detail"]
    # same game re-erroring later (new timestamp) is new again
    later = dict(game, gameError=dict(game["gameError"], timestamp=ts + 1))
    issues, _ = _derive_error_issues(_errors_of(later, "g1", now), {e["key"] for e in errs})
    assert len(issues) == 1 and issues[0]["kind"] == "poker_hand_stuck"

    # activity window: first run = short lookback; later = since last scan, capped
    now_ms = int(now.timestamp() * 1000)
    assert _activity_since(None, now) == now_ms - ACTIVITY_LOOKBACK_H * 3600_000
    assert _activity_since(now_ms - 1000, now) == now_ms - 1000
    assert _activity_since(now_ms - 10 * 24 * 3600_000, now) == now_ms - ACTIVITY_MAX_H * 3600_000

    g = _summarize_game({"theme": "Dune", "createdBy": "hiper2d@gmail.com", "createdWithTier": "paid",
                         "status": "HAND_RESULTS", "handNumber": 3, "messageCounter": 40,
                         "bots": [{"aiType": "gpt"}, {"aiType": "claude"}], "gameMasterAiType": "gpt-mini",
                         "totalGameCost": 0.04123, "createdAt": now_ms}, "g2", set())
    assert g["own"] and g["owner"] == "(own)" and g["models"] == ["claude", "gpt"] and g["cost_usd"] == 0.0412
    act = _derive_activity_issues([g], 2)
    assert len(act) == 2 and "own game" in act[0]["detail"] and act[1]["kind"] == "poker_new_user"
    assert all(i["severity"] == "digest" for i in act)

    rep = {"ok": True, "checked_at": "2026-10-31T12:00:00Z", "issues": issues + act,
           "new_games": [g], "new_users": 2, "any_urgent": True, "errored": errs,
           "games_total": 1, "users_total": 3, "since": "x"}
    d = render_digest(rep)
    assert d and d.startswith("Poker — 2026-10-31: 1 new error(s) (urgent), 1 new table(s), 2 signup(s)"), d
    assert render_digest({"ok": True, "issues": []}) is None
    assert "Poker health" in render(rep)
    print("selftest ok")


# ─── CLI ─────────────────────────────────────────────────────────────────────


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("report", help="Scan poker_games/poker_users + persist (JSON)")
    sub.add_parser("show", help="Render the last persisted scan, human-readable")
    sub.add_parser("digest", help="Digest block from the last scan (empty if quiet)")
    sub.add_parser("selftest", help="Offline asserts, no network")
    args = ap.parse_args()
    if args.cmd == "report":
        res = report()
        print(json.dumps(res, indent=2, ensure_ascii=False))
        sys.exit(0 if res.get("ok") else 1)
    elif args.cmd == "show":
        try:
            with POKER_LATEST.open() as f:
                print(render(json.load(f)))
        except (OSError, json.JSONDecodeError):
            print("No scan yet — run `report` first.")
    elif args.cmd == "digest":
        try:
            with POKER_LATEST.open() as f:
                d = render_digest(json.load(f))
            print(d if d else "")
        except (OSError, json.JSONDecodeError):
            print("")
    elif args.cmd == "selftest":
        selftest()


if __name__ == "__main__":
    main()
