"""
monitor_betterstack — app-level error watch for the Werewolf game via Betterstack.

The FOURTH werewolf-ops workstream, and the companion to monitor_health.
monitor_keys watches what the free tier COSTS, werewolf_stats what it PRODUCES,
monitor_health whether a *game* WORKS (its `errorState` in Firestore). This
watches whether the *app* is throwing — the failures that never reach a game
doc: unhandled exceptions, provider 5xx, Next.js server errors, dead requests.

The game already ships structured logs to Betterstack via `@logtail/node`
(werewolf-client/app/utils/logger.ts). We read them back through Betterstack's
ClickHouse HTTP query API (the app's source token is ingest-only; this needs a
separate query credential — a ClickHouse connection, created under Telemetry →
Integrations → SQL API).

── Incidents, not lines (2026-10-23) ───────────────────────────────────────
Until 2026-10-23 the handler returned one row per error line with four fields
(time, level, env, the first 200 chars of `message`) and the alert was a dump of
those. On the game's error lines `message` is a throwaway ("Game action failed:
U") and the substance sits in `error` / `details` / `gameId` / `model` /
`botName` / `function`, none of which were read. The same afternoon four
timeouts of one slow bot in one game paged Alex twice (two hourly scans, six
"new" lines) with no way to tell from the alert what had happened.

Now the handler reads the structured fields, folds lines into INCIDENTS —
same game, same failure class, same model — classifies each against the known
failure classes (`classify`), attaches a read-only Firestore snapshot of the
game (state, day, error state, last message, who owns it, which models are at
the table) for every NEW incident, and fingerprints the incident rather than
the line. The session's job (see the task YAML) is the judgment on top: what
happened, what the player saw, whether it needs Alex.

── Storage, and why an S3 table shows up ────────────────────────────────────
Betterstack Telemetry is ClickHouse with tiered storage. Recent rows sit in a
fast hot table — `remote(<source>_logs)`; older rows are flushed to cheap S3 —
`s3Cluster(primary, <source>_s3)`. The Live-tail UI stitches both together so a
human never sees the seam. The raw SQL API does not: you address a table.
Which tier holds the fresh rows has flipped more than once, so every query reads
the UNION of both, DISTINCT on (dt, raw). If the union holds ZERO rows (any
env/level) in the window the report says `source_empty` instead of calling the
window quiet.

── Schema ───────────────────────────────────────────────────────────────────
There is no flat `level` column. Each row's `raw` is the full JSON log line;
every field comes out with `JSONExtractString(raw, '<field>')`. Fields the app
sets: level, message, env, gameId, function, botName, model, gameState,
recoverable, error, details (stack), deviceId, ip, city, userEmail, scope.

── Env filter (2026-09-23) ──────────────────────────────────────────────────
Local dev, Jest and production all ship to the SAME source; each line carries
`env` in `raw`. Only envs in BETTERSTACK_ENVS (default `production`) alert.
Lines with no `env` predate 2026-09-02 and are dropped. Non-production
error/warn lines are still COUNTED, once a day, as one informational digest
line - so a test leak coming back is visible without paging anyone.

── Alert model: presence, not rate-spike ───────────────────────────────────
At this volume the error baseline is ZERO — errors essentially never appear. So
"did the rate spike above normal?" is the wrong question; "did ANY error/warn
appear?" is both simpler and strictly more sensitive. We alert on INCIDENTS not
seen on a previous scan (fingerprint dedup, same noise discipline as
monitor_health diffing the errored-game set):
  - First run with no prior state → BASELINE the current incidents, emit one
    digest summary, no urgent ping (don't alarm on a pre-existing pile).
  - Later runs → a new incident whose worst line is error-level is urgent; a new
    warn-only incident is digest. A known incident that keeps producing lines is
    never re-pinged; it falls out of the dedup set INCIDENT_TTL_HOURS after its
    last line, so the same failure a day later counts as new again.
  - Upgrading from the pre-10-23 line fingerprints: the first scan that finds the
    old `seen` list re-baselines under incident fingerprints (one digest line).

Cadence: every 3 hours with a 4-hour window (was hourly / 90 min). Nobody acts
on these inside the hour, site liveness is monitor_uptime's job, and a slower
scan with overlap sees an incident whole instead of paging on each half.

Credentials (in the launchd plist, mirrored to os.environ by env_loader):
  BETTERSTACK_CH_HOST, BETTERSTACK_CH_USER, BETTERSTACK_CH_PASS.
  MARLOW_FIREBASE_CREDS (read-only) for the game snapshots; without it the
  incidents still come back, just without the `game` block.
Fails clean (ok: false) if the ClickHouse creds are unset — same failure
contract as monitor_keys/health.

── Two apps, one handler (2026-10-31) ───────────────────────────────────────
Poker with AI (pokerwithai.net) is the second game on the same Betterstack
account and the same Firebase project. `--app poker` runs the SAME scan against
Poker's source: its own tables, its own state files (`betterstack_poker_*`), its
own game snapshot (`poker_games`: two error lanes instead of one `errorState`),
and Poker's field names mapped onto the common row shape (`action`→function,
`actor`→botName, `user`→userEmail; plus `lane`, `failedAction`). The ClickHouse
connection is account-wide, so the same credential reads both sources.
Poker's tables come from BETTERSTACK_POKER_CH_TABLE / BETTERSTACK_POKER_CH_ALT_TABLE,
else from `projects/werewolf-ops/config/betterstack_sources.json` ({"poker":
{"table", "alt_table"}}). Until one of those is set, `--app poker` returns
`ok: true, configured: false` and says so — not a failure, nothing to page.
Poker's source lives on the us-west-2a cluster (Free plan: no region choice),
Werewolf's on eu-fsn-3, and a SQL API connection sees one cluster only, so Poker
queries go through its own connection: BETTERSTACK_POKER_CH_HOST/USER/PASS in
the plist (falls back to the shared BETTERSTACK_CH_* when unset).

CLI (add `--app poker` before the subcommand for Poker; default werewolf):
    python handlers/monitor_betterstack.py report   → scan + persist, JSON
    python handlers/monitor_betterstack.py show      → last scan, human-readable
    python handlers/monitor_betterstack.py digest    → digest block for notify
    python handlers/monitor_betterstack.py replay --since 2026-10-23T15:00Z --until 2026-10-23T18:00Z
                                                     → the incidents a scan of that window
                                                       would alert on, with game snapshots
                                                       (no state read or written)
    python handlers/monitor_betterstack.py selftest  → offline asserts, no network
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from driver.env_loader import import_plist_env  # noqa: E402
import_plist_env()

from driver.budget_state import STATE_DIR  # noqa: E402

# The durable store for this source. Hot tier is remote(t507167_ai_werewolf_2_logs);
# both are unioned on every query (see docstring). Override via env if the source moves.
TABLE = os.environ.get("BETTERSTACK_CH_TABLE", "s3Cluster(primary, t507167_ai_werewolf_2_s3)")
ALT_TABLE = os.environ.get("BETTERSTACK_CH_ALT_TABLE", "remote(t507167_ai_werewolf_2_logs)")
# Only these envs alert. Comma-separated; values go into SQL, so they're
# restricted to a safe charset rather than escaped.
ENVS = tuple(e for e in (x.strip() for x in os.environ.get("BETTERSTACK_ENVS", "production").split(","))
             if re.fullmatch(r"[A-Za-z0-9_-]+", e)) or ("production",)
WINDOW_MIN = int(os.environ.get("BETTERSTACK_WINDOW_MIN", "240"))
ALERT_LEVELS = ("error", "warn")
HTTP_TIMEOUT = 30
ROW_LIMIT = 500          # plenty at this volume; caps a runaway error storm
INCIDENT_TTL_HOURS = 24  # a known incident is forgotten this long after its last line
SEEN_CAP = 500           # incident fingerprints retained (errors are rare → never hit)
MESSAGES_PER_INCIDENT = 5

# Structured fields read off each row, as {column: json key in `raw`}. The columns are
# the common row shape the rest of the handler reads; the keys are what each app's
# logger attaches. `message` first; Werewolf's are in the Schema section, Poker's
# come from lib/actions/game-action.ts (`log.with({action, gameId, user})`, the lane
# failure warn carries {lane, message, details, failedAction, actor, model,
# retryable}, the crash error carries {error, durationMs}).
WEREWOLF_FIELDS = {f: f for f in ("message", "error", "details", "gameId", "function", "botName", "model",
                                  "gameState", "recoverable", "deviceId", "userEmail", "scope", "city", "ip")}
POKER_FIELDS = {"message": "message", "error": "error", "details": "details", "gameId": "gameId",
                "function": "action", "botName": "actor", "model": "model", "gameState": "lane",
                "recoverable": "retryable", "deviceId": "deviceId", "userEmail": "user",
                "scope": "scope", "city": "city", "ip": "ip", "failedAction": "failedAction"}
FIELD_CAP = {"message": 300, "error": 300, "details": 700}

CONFIG_SOURCES = STATE_DIR.parent / "config" / "betterstack_sources.json"


def _poker_tables() -> tuple[str, str]:
    """Poker's (table, alt_table): env first, then the config file, else ('', '')."""
    t = os.environ.get("BETTERSTACK_POKER_CH_TABLE", "")
    a = os.environ.get("BETTERSTACK_POKER_CH_ALT_TABLE", "")
    if t:
        return (t, a)
    try:
        with CONFIG_SOURCES.open() as f:
            cfg = (json.load(f) or {}).get("poker") or {}
        return (cfg.get("table") or "", cfg.get("alt_table") or "")
    except (OSError, json.JSONDecodeError, AttributeError):
        return ("", "")


APPS = {
    "werewolf": {
        "label": "Werewolf app logs",
        "tables": (TABLE, ALT_TABLE),
        "fields": WEREWOLF_FIELDS,
        "games": "games", "messages": "messages",
        "state": "betterstack",
        "repo": "~/projects/werewolf-ai-party-game/werewolf-client",
    },
    "poker": {
        "label": "Poker app logs",
        "tables": _poker_tables(),
        "fields": POKER_FIELDS,
        "games": "poker_games", "messages": "messages",
        "state": "betterstack_poker",
        "repo": "~/projects/poker-with-ai",
        "creds_prefix": "BETTERSTACK_POKER_CH_",   # its own SQL API connection (US cluster)
    },
}

# Selected app — module globals so the query/snapshot/render code stays flat.
# `configure()` swaps them; the defaults are Werewolf so imports behave as before.
APP = "werewolf"
LABEL = APPS["werewolf"]["label"]
FIELDS: tuple[str, ...] = tuple(WEREWOLF_FIELDS)
FIELD_SRC: dict[str, str] = WEREWOLF_FIELDS
BS_LATEST = STATE_DIR / "betterstack_latest.json"
BS_HISTORY = STATE_DIR / "betterstack_history.jsonl"
GAMES = "games"
MESSAGES = "messages"


def configure(app: str) -> None:
    """Point the module at one app's source, state and collections."""
    global APP, LABEL, TABLE, ALT_TABLE, FIELDS, FIELD_SRC, BS_LATEST, BS_HISTORY, GAMES, MESSAGES
    cfg = APPS[app]
    APP = app
    LABEL = cfg["label"]
    TABLE, ALT_TABLE = cfg["tables"]
    FIELD_SRC = cfg["fields"]
    FIELDS = tuple(FIELD_SRC)
    BS_LATEST = STATE_DIR / f"{cfg['state']}_latest.json"
    BS_HISTORY = STATE_DIR / f"{cfg['state']}_history.jsonl"
    GAMES, MESSAGES = cfg["games"], cfg["messages"]


def configured() -> bool:
    return bool(TABLE)


# ─── Failure classes ─────────────────────────────────────────────────────────
#
# Deterministic first guess at WHAT KIND of failure a line is, matched against
# message + error + the head of details. The session's playbook (task YAML) says
# what each class means and whether it needs Alex; this only labels. Order
# matters: the first match wins, so the specific tags come before the generic
# "parse_failure" catch-all. `unclassified` is a legitimate answer and the one
# the session should spend its attention on.
CLASSES: tuple[tuple[str, str], ...] = (
    ("device_link", r"DEVICE_LINKED_BY_IP"),
    ("free_cap", r"FREE_SPEND_LIMIT|free \$[\d.]+ of AI|free play is paused"),
    ("player_balance", r"insufficient balance"),
    ("stale_action", r"STALE_ACTION"),
    ("model_refusal", r"refused (?:the prompt|to answer)|PROHIBITED_CONTENT|ImageRefusalError|ModelRefusalError"),
    ("provider_budget", r"insufficient_quota|no credits remaining|credit balance is too low|used all available credits|spending limit"),
    ("timeout", r"did not respond within|ModelTimeoutError|timed out|timeout"),
    ("provider_busy", r"\b(?:429|503|529)\b|rate[\s_-]?limit|too many requests|overloaded|at capacity|service unavailable|resource[\s_-]?exhausted"),
    ("firestore_contention", r"transaction (?:has )?expired|\bABORTED\b|contention|too much contention"),
    ("empty_response", r"empty (?:or undefined )?response|returned no content|empty content"),
    ("parse_failure", r"\bJSON\b|schema|zod|parse|validation"),
)


def classify(text: str) -> str:
    low = (text or "").lower()
    for name, pattern in CLASSES:
        if re.search(pattern, low, re.IGNORECASE):
            return name
    return "unclassified"


# ─── Betterstack query ───────────────────────────────────────────────────────


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _checked_at(now: datetime) -> str:
    return now.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _creds() -> dict | None:
    """The ClickHouse connection for the selected app. A SQL API connection lives
    on ONE cluster and a source's data region picks its cluster: Werewolf is on
    eu-fsn-3 (BETTERSTACK_CH_*), Poker on us-west-2a (data regions are a paid
    feature, every new Free-plan source lands in the US), so Poker needs its own
    connection — BETTERSTACK_POKER_CH_HOST/USER/PASS. Falls back to the shared
    one when the app-specific set is absent."""
    prefix = APPS[APP].get("creds_prefix") or "BETTERSTACK_CH_"
    host = os.environ.get(f"{prefix}HOST")
    user = os.environ.get(f"{prefix}USER")
    pw = os.environ.get(f"{prefix}PASS")
    if not (host and user and pw):
        return None
    return {"host": host, "user": user, "pw": pw}


def _creds_pending() -> bool:
    """An app with its own connection whose creds are not in the plist yet.
    Treated as NOT CONFIGURED (quiet), never as a failure: the shared connection
    is on another cluster, so falling back to it can only produce
    CLUSTER_DOESNT_EXIST and page Alex every scan for a known setup gap
    (2026-10-31, the first evening of the poker watch)."""
    return bool(APPS[APP].get("creds_prefix")) and _creds() is None


def _query(creds: dict, sql: str) -> str:
    """POST a SQL statement to the ClickHouse HTTP endpoint, return raw text body.
    Raises requests.RequestException / RuntimeError on transport or query error."""
    resp = requests.post(
        f"{creds['host']}?output_format_pretty_row_numbers=0",
        auth=(creds["user"], creds["pw"]),
        headers={"Content-type": "plain/text"},
        data=sql,
        timeout=HTTP_TIMEOUT,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"HTTP {resp.status_code}: {resp.text[:200].strip()}")
    return resp.text


def _sql_list(values) -> str:
    return ", ".join(f"'{v}'" for v in values)


def _window_clause(since: datetime | None = None, until: datetime | None = None) -> str:
    """Default: the rolling WINDOW_MIN. With since/until: that fixed UTC range (replay)."""
    if since is None:
        return f"dt > now() - INTERVAL {WINDOW_MIN} MINUTE"
    until = until or _now_utc()
    fmt = "%Y-%m-%d %H:%M:%S"
    return (f"dt >= toDateTime('{since.strftime(fmt)}', 'UTC') "
            f"AND dt < toDateTime('{until.strftime(fmt)}', 'UTC')")


def _source(window: str) -> str:
    """Both tiers for the window, each row once."""
    if not ALT_TABLE:
        return f"(SELECT dt, raw FROM {TABLE} WHERE {window})"
    return (f"(SELECT DISTINCT dt, raw FROM ("
            f"SELECT dt, raw FROM {TABLE} WHERE {window} "
            f"UNION ALL SELECT dt, raw FROM {ALT_TABLE} WHERE {window}))")


def _rows_sql(window: str) -> str:
    cols = ["dt", "JSONExtractString(raw,'level') AS lvl", "JSONExtractString(raw,'env') AS env"]
    for f in FIELDS:
        cap = FIELD_CAP.get(f)
        expr = f"JSONExtractString(raw,'{FIELD_SRC[f]}')"
        cols.append(f"substring({expr},1,{cap}) AS {f}" if cap else f"{expr} AS {f}")
    return (
        "SELECT " + ", ".join(cols) + " "
        f"FROM {_source(window)} "
        f"WHERE JSONExtractString(raw,'level') IN ({_sql_list(ALERT_LEVELS)}) "
        f"AND JSONExtractString(raw,'env') IN ({_sql_list(ENVS)}) "
        f"ORDER BY dt DESC LIMIT {ROW_LIMIT} FORMAT JSONEachRow"
    )


def _count(creds: dict, window: str) -> int:
    """All rows in the window, any env/level: is the source live at all?"""
    body = _query(creds, f"SELECT count() FROM {_source(window)} FORMAT TSV").strip()
    return int(body or 0)


def _nonprod_counts(creds: dict, window: str) -> dict[str, int]:
    """Error/warn lines per NON-alerting env (test, development, preview...)."""
    body = _query(creds, (
        "SELECT JSONExtractString(raw,'env') AS env, count() AS n "
        f"FROM {_source(window)} "
        f"WHERE JSONExtractString(raw,'level') IN ({_sql_list(ALERT_LEVELS)}) "
        f"AND JSONExtractString(raw,'env') NOT IN ({_sql_list(ENVS)}) "
        "GROUP BY env ORDER BY n DESC FORMAT JSONEachRow"))
    out = {}
    for line in body.splitlines():
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            continue
        out[o.get("env") or "(none)"] = int(o.get("n", 0))
    return out


def _fetch_rows(creds: dict, window: str | None = None) -> list[dict]:
    """The error/warn rows in the window from alerting envs, newest first."""
    body = _query(creds, _rows_sql(window or _window_clause()))
    return _parse_rows(body)


def _parse_rows(body: str) -> list[dict]:
    rows = []
    for line in body.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            continue
        row = {"dt": o.get("dt"), "level": o.get("lvl"), "env": o.get("env") or ""}
        for f in FIELDS:
            v = o.get(f)
            row[f] = v.strip() if isinstance(v, str) else (v or "")
        row["msg"] = row.pop("message")
        if row["env"] not in ENVS:
            continue  # belt and braces: the SQL already filters this
        rows.append(row)
    return rows


# ─── Incidents ───────────────────────────────────────────────────────────────


def _error_text(row: dict) -> str:
    """The human error line. Some logger calls serialize the whole error object
    into `error` ('{"modelType":..,"message":..,"stack":..}'); unwrap to its
    message so the alert reads like the sibling lines and folds with them."""
    err = (row.get("error") or "").strip()
    if err.startswith("{"):
        try:
            o = json.loads(err)
            if isinstance(o, dict) and o.get("message"):
                return str(o["message"]).strip()
        except json.JSONDecodeError:
            m = re.search(r'"message"\s*:\s*"([^"]{1,200})"', err)
            if m:
                return m.group(1)
    return err or (row.get("msg") or "")


def _row_class(row: dict) -> str:
    return classify(" ".join([row.get("msg") or "", _error_text(row),
                              (row.get("details") or "")[:300]]))


def _normalize(text: str) -> str:
    """A message with its volatile parts removed, so lines that differ only in
    ids/numbers fold into one incident."""
    t = re.sub(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", "<uuid>", text or "")
    t = re.sub(r"\d+", "#", t)
    return t.strip().lower()[:80]


def incident_key(row: dict) -> tuple[str, str, str]:
    """(target, failure class, discriminator). Lines in one game that fail the
    same way are one incident whatever the function or the model: a stalled bot
    fails in vote AND in talkToAll, and the agent layer logs the same timeout a
    second time without the bot fields. Models and bots are collected on the
    incident instead, so the alert still names them."""
    cls = _row_class(row)
    if row.get("gameId"):
        return (f"game:{row['gameId']}", cls, "-")
    if cls == "device_link":
        return (f"device:{row.get('deviceId') or '?'}", cls, "-")
    if cls == "free_cap":
        return (f"user:{row.get('userEmail') or '?'}", cls, row.get("scope") or "-")
    return ("app", cls, _normalize(row.get("msg") or row.get("error") or ""))


def _fingerprint(key: tuple[str, str, str]) -> str:
    return hashlib.sha1("|".join(key).encode("utf-8")).hexdigest()[:16]


def fold_incidents(rows: list[dict]) -> list[dict]:
    """Group rows (newest first) into incidents, newest-last-line first."""
    by_key: dict[tuple, dict] = {}
    for r in rows:
        key = incident_key(r)
        inc = by_key.get(key)
        if inc is None:
            inc = by_key[key] = {
                "fingerprint": _fingerprint(key),
                "target": key[0], "class": key[1],
                "gameId": r.get("gameId") or "", "level": r.get("level"),
                "first_dt": _trim_dt(r.get("dt")), "last_dt": _trim_dt(r.get("dt")), "count": 0,
                "models": [], "functions": [], "bots": [], "actors": [], "gameStates": [], "envs": [],
                "error": _error_text(r),
                "details_head": (r.get("details") or "")[:400],
                "deviceId": r.get("deviceId") or "", "userEmail": r.get("userEmail") or "",
                "lines": [],
            }
        inc["count"] += 1
        if r.get("level") == "error":
            inc["level"] = "error"
        dt = _trim_dt(r.get("dt"))
        if dt and (not inc["first_dt"] or dt < inc["first_dt"]):
            inc["first_dt"] = dt
        if dt and (not inc["last_dt"] or dt > inc["last_dt"]):
            inc["last_dt"] = dt
        for field, bag in (("model", "models"), ("function", "functions"), ("botName", "bots"),
                           ("gameState", "gameStates"), ("env", "envs")):
            v = r.get(field)
            if v and v not in inc[bag]:
                inc[bag].append(v)
        # model/bot pairs as they occur ("minimax/Vexa"), for the alert line.
        actor = "/".join(x for x in (r.get("model"), r.get("botName")) if x)
        if actor and actor not in inc["actors"]:
            inc["actors"].append(actor)
        if len(inc["lines"]) < MESSAGES_PER_INCIDENT:
            inc["lines"].append({"dt": dt, "level": r.get("level"),
                                 "function": r.get("function") or "", "bot": r.get("botName") or "",
                                 "msg": r.get("msg") or "", "error": _error_text(r)})
    out = list(by_key.values())
    out.sort(key=lambda i: (i["level"] != "error", i["last_dt"] or ""), reverse=False)
    out.sort(key=lambda i: i["last_dt"] or "", reverse=True)
    return out


def _trim_dt(dt: str | None) -> str | None:
    """ClickHouse hands back '2026-10-23 16:32:19.878000'; keep whole seconds."""
    return dt.split(".")[0] if isinstance(dt, str) else dt


# ─── Firestore snapshot ──────────────────────────────────────────────────────


def _ms_iso(ms) -> str | None:
    try:
        return datetime.fromtimestamp(int(ms) / 1000, tz=timezone.utc).replace(microsecond=0) \
            .isoformat().replace("+00:00", "Z")
    except (TypeError, ValueError, OSError):
        return None


def _db():
    """Read-only Firestore client, or None when creds/dep are missing. The
    snapshot is an extra; a missing client never fails the scan."""
    try:
        from handlers.monitor_keys import _firestore_db  # noqa: PLC0415
        return _firestore_db()
    except Exception:  # noqa: BLE001
        return None


def _last_message(db, game_id: str, out: dict, now: datetime) -> None:
    """Attach the newest message of the game's `messages` subcollection (both apps
    keep {timestamp, authorName, messageType}; Werewolf adds `day`, Poker `handNumber`)."""
    try:
        last = list(db.collection(GAMES).document(game_id).collection(MESSAGES)
                    .order_by("timestamp", direction="DESCENDING").limit(1).stream())
        if last:
            m = last[0].to_dict() or {}
            out["last_message"] = {
                "at": _ms_iso(m.get("timestamp")),
                "author": m.get("authorName"),
                "type": m.get("messageType"),
                "day": m.get("day") if "day" in m else m.get("handNumber"),
            }
            iso = out["last_message"]["at"]
            if iso:
                dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
                out["minutes_since_last_message"] = int((now - dt).total_seconds() // 60)
    except Exception as e:  # noqa: BLE001
        out["last_message"] = {"error": str(e)[:120]}


def poker_snapshot(db, game_id: str, now: datetime | None = None) -> dict:
    """Poker's game doc: `status` + `handNumber` instead of gameState/day, seats
    carry liveness (bots don't), and TWO error lanes. The first set lane is
    reported as `errorState` so the renders read the same; both are in `lanes`."""
    now = now or _now_utc()
    try:
        snap = db.collection(GAMES).document(game_id).get()
        if not snap.exists:
            return {"exists": False}
        g = snap.to_dict() or {}
        bots = g.get("bots") or []
        seats = g.get("seats") or []
        alive = {s.get("name") for s in seats if s.get("status") == "active" and not s.get("isHuman")}
        out = {
            "exists": True,
            "theme": g.get("theme") or "(untitled)",
            "owner": g.get("createdBy"),
            "tier": g.get("createdWithTier"),
            "state": g.get("status"),
            "day": g.get("handNumber"),          # "day" slot = hand number for Poker
            "gameMaster": g.get("gameMasterAiType"),
            "createdAt": _ms_iso(g.get("createdAt")),
            "bots_alive": len([b for b in bots if b.get("name") in alive]) if seats else len(bots),
            "bots_total": len(bots),
            "models": sorted({(b.get("aiType") or "?") for b in bots}),
            "errorState": None,
            "lanes": {},
            "last_message": None,
        }
        for lane, field in (("game", "gameError"), ("chat", "chatError")):
            err = g.get(field) or None
            if not err:
                continue
            first = (err.get("details") or "").splitlines()
            rec = {
                "recoverable": bool(err.get("retryable", True)),
                "function": f"{lane} lane / {err.get('failedAction') or '?'}",
                "actor": err.get("actor"), "model": err.get("model"),
                "at": _ms_iso(err.get("timestamp")),
                "summary": (first[0].strip() if first else err.get("message") or "")[:160],
            }
            out["lanes"][lane] = rec
            if out["errorState"] is None:
                out["errorState"] = rec
        _last_message(db, game_id, out, now)
        return out
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)[:160]}


def game_snapshot(db, game_id: str, now: datetime | None = None) -> dict:
    """What the player sees: state, day, error state, who is at the table, when
    the game last moved. Fail-soft - returns {"error": ...} rather than raising."""
    if APP == "poker":
        return poker_snapshot(db, game_id, now)
    now = now or _now_utc()
    try:
        snap = db.collection(GAMES).document(game_id).get()
        if not snap.exists:
            return {"exists": False}
        g = snap.to_dict() or {}
        bots = g.get("bots") or []
        err = g.get("errorState") or None
        out = {
            "exists": True,
            "theme": g.get("theme") or "(untitled)",
            "owner": g.get("ownerEmail"),
            "tier": g.get("createdWithTier"),
            "state": g.get("gameState"),
            "day": g.get("currentDay"),
            "gameMaster": g.get("gameMasterAiType"),
            "createdAt": _ms_iso(g.get("createdAt")),
            "bots_alive": sum(1 for b in bots if b.get("isAlive")),
            "bots_total": len(bots),
            "models": sorted({(b.get("aiType") or "?") for b in bots if b.get("isAlive")}),
            "errorState": None,
            "last_message": None,
        }
        if err:
            ctx = err.get("context") or {}
            first = (err.get("details") or "").splitlines()
            out["errorState"] = {
                "recoverable": bool(err.get("recoverable")),
                "function": ctx.get("function"),
                "at": ctx.get("timestamp"),
                "summary": (first[0].strip() if first else "")[:160],
            }
        _last_message(db, game_id, out, now)
        return out
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)[:160]}


def attach_snapshots(incidents: list[dict], only_new: bool = True, now: datetime | None = None) -> None:
    """Add a `game` block to every (new) incident that names a game. One read per game."""
    wanted = [i for i in incidents if i.get("gameId") and (i.get("is_new") or not only_new)]
    if not wanted:
        return
    db = _db()
    cache: dict[str, dict] = {}
    for inc in wanted:
        gid = inc["gameId"]
        if gid not in cache:
            cache[gid] = game_snapshot(db, gid, now) if db is not None \
                else {"error": "MARLOW_FIREBASE_CREDS not available"}
        inc["game"] = cache[gid]


# ─── State & issues ──────────────────────────────────────────────────────────


def _prior_state() -> dict:
    try:
        with BS_LATEST.open() as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def _prior_seen(prev: dict) -> dict | None:
    """Incident fingerprints from the last run: {fp: {"last_dt", "class", "target"}}.
    None → never scanned (→ baseline). {} with a legacy `seen` list → migrate."""
    if not prev:
        return None
    seen = prev.get("seen_incidents")
    if isinstance(seen, dict):
        return seen
    return {}   # pre-10-23 state (line fingerprints): re-baseline


def _parse_dt(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        d = datetime.fromisoformat(s.replace("Z", "+00:00").replace(" ", "T"))
    except ValueError:
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def derive_issues(incidents: list[dict], prior: dict | None, legacy: bool = False,
                  now: datetime | None = None) -> tuple[list[dict], bool]:
    """Mark incidents new/known and return (issues, baselined).

    First run (prior is None) or an upgrade from line fingerprints (legacy=True):
    baseline — one digest line, no urgent, nothing marked new."""
    now = now or _now_utc()
    if prior is None or legacy:
        for inc in incidents:
            inc["is_new"] = False
        if incidents:
            errs = sum(1 for i in incidents if i["level"] == "error")
            why = "re-baselined under incident fingerprints (upgrade from per-line dedup)" if legacy \
                else "baseline on first scan"
            return ([{
                "severity": "digest", "kind": "betterstack_baseline", "target": "logs",
                "detail": f"{why}: {len(incidents)} {'/'.join(ENVS)} incident(s) in the last "
                          f"{WINDOW_MIN}m ({errs} error, {len(incidents) - errs} warn) — not alerting. "
                          f"New incidents alert from here.",
            }], True)
        return ([], True)

    issues = []
    for inc in incidents:
        known = prior.get(inc["fingerprint"])
        fresh = known is not None
        if fresh:
            last = _parse_dt(known.get("last_dt"))
            if last and now - last > timedelta(hours=INCIDENT_TTL_HOURS):
                fresh = False   # forgotten: the same failure a day later is news again
        inc["is_new"] = not fresh
        if fresh:
            continue
        is_err = inc["level"] == "error"
        issues.append({
            "severity": "urgent" if is_err else "digest",
            "kind": "app_error" if is_err else "app_warn",
            "target": inc["fingerprint"],
            "detail": incident_line(inc),
        })
    return (issues, False)


def next_seen(incidents: list[dict], prior: dict | None, now: datetime | None = None) -> dict:
    """Dedup state for the next run: every incident in this window (with its
    latest line time) plus the prior ones still inside the TTL."""
    now = now or _now_utc()
    out: dict[str, dict] = {}
    for inc in incidents:
        out[inc["fingerprint"]] = {"last_dt": inc["last_dt"], "class": inc["class"], "target": inc["target"]}
    for fp, rec in (prior or {}).items():
        if fp in out:
            continue
        last = _parse_dt(rec.get("last_dt"))
        if last and now - last <= timedelta(hours=INCIDENT_TTL_HOURS):
            out[fp] = rec
        if len(out) >= SEEN_CAP:
            break
    return out


def _nonprod_daily_issue(creds: dict, now: datetime, prev: dict) -> dict | None:
    """Once per UTC day: yesterday's non-production error/warn count, as one
    informational digest line. Never urgent. None when already reported or zero."""
    day = (now - timedelta(days=1)).date()
    if prev.get("nonprod_reported_for") == day.isoformat():
        return None
    start = datetime(day.year, day.month, day.day, tzinfo=timezone.utc)
    window = _window_clause(start, start + timedelta(days=1))
    counts = _nonprod_counts(creds, window)
    issue = {"severity": "digest", "kind": "nonprod_logs", "target": day.isoformat(),
             "date": day.isoformat(), "counts": counts}
    if not counts:
        return {**issue, "silent": True}      # mark the day done, add no line
    parts = ", ".join(f"{env}={n}" for env, n in counts.items())
    issue["detail"] = (f"[info] non-production error/warn lines on {day.isoformat()}: {parts} "
                       f"(not alerting - only {'/'.join(ENVS)} alerts)")
    return issue


def _compact(report: dict) -> dict:
    return {
        "checked_at": report.get("checked_at"),
        "window_min": report.get("window_min"),
        "counts": report.get("counts"),
        "incidents": len(report.get("incidents", [])),
        "new_incidents": len([i for i in report.get("incidents", []) if i.get("is_new")]),
        "any_urgent": report.get("any_urgent"),
        "issues": [f"{i['severity']}:{i['target']}" for i in report.get("issues", [])],
    }


def _save(report: dict) -> None:
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        tmp = BS_LATEST.with_suffix(".json.tmp")
        with tmp.open("w") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        tmp.replace(BS_LATEST)
        with BS_HISTORY.open("a") as f:
            f.write(json.dumps(_compact(report), ensure_ascii=False) + "\n")
    except OSError:
        pass


def _unconfigured(now: datetime) -> dict:
    """`--app poker` before its source or its own connection exists: a quiet,
    non-failing report. The `error` text says which half is missing."""
    prefix = APPS[APP].get("creds_prefix") or "BETTERSTACK_CH_"
    if not configured():
        why = (f"no Betterstack source configured yet — set BETTERSTACK_POKER_CH_TABLE "
               f"(or config/betterstack_sources.json) once the source exists")
    else:
        why = (f"source table set but {prefix}HOST/USER/PASS are not in the plist — this app's "
               f"source is on another cluster than the shared connection, so there is nothing to "
               f"query with until that SQL API connection exists and its creds are installed")
    return {"ok": True, "configured": False, "app": APP, "checked_at": _checked_at(now),
            "incidents": [], "new_incidents": [], "issues": [], "any_urgent": False,
            "error": f"{LABEL}: {why}; nothing to scan until then (not a failure — no report, no ping)"}


def report() -> dict:
    now = _now_utc()
    if not configured() or _creds_pending():
        return _unconfigured(now)
    creds = _creds()
    if not creds:
        return {"ok": False, "checked_at": _checked_at(now),
                "error": "BETTERSTACK_CH_HOST/USER/PASS not set (ClickHouse query creds)"}
    prev = _prior_state()
    try:
        window = _window_clause()
        source_empty = _count(creds, window) == 0
        rows = [] if source_empty else _fetch_rows(creds, window)
        nonprod_issue = _nonprod_daily_issue(creds, now, prev)
    except (requests.RequestException, RuntimeError, ValueError) as e:
        return {"ok": False, "checked_at": _checked_at(now), "error": str(e)[:200]}

    prior = _prior_seen(prev)                   # read BEFORE we overwrite latest
    legacy = bool(prev) and prior == {} and isinstance(prev.get("seen"), list)
    incidents = fold_incidents(rows)
    issues, baselined = derive_issues(incidents, prior, legacy=legacy, now=now)
    attach_snapshots(incidents, only_new=True, now=now)
    if nonprod_issue and not nonprod_issue.get("silent"):
        issues.append(nonprod_issue)
    counts = {lvl: sum(1 for r in rows if r["level"] == lvl) for lvl in ALERT_LEVELS}
    result = {
        "ok": True,
        "app": APP,
        "checked_at": _checked_at(now),
        "window_min": WINDOW_MIN,
        "envs": list(ENVS),
        "source_empty": source_empty,
        "nonprod_reported_for": (nonprod_issue or {}).get("date") or prev.get("nonprod_reported_for"),
        "counts": counts,
        "incidents": incidents,
        "new_incidents": [i for i in incidents if i.get("is_new")],
        "issues": issues,
        "any_urgent": any(i["severity"] == "urgent" for i in issues),
        "baselined": baselined,
        "seen_incidents": next_seen(incidents, prior, now),    # dedup state for the next run
    }
    _save(result)
    return result


# ─── Renders ─────────────────────────────────────────────────────────────────


def _hhmm(dt: str | None) -> str:
    d = _parse_dt(dt)
    return d.strftime("%H:%M") if d else "?"


def incident_line(inc: dict) -> str:
    """One line per incident for the digest / urgent message: what, where, how
    many times, over what span, the real error text. The session's analysis goes
    under it, not in it."""
    span = _hhmm(inc.get("first_dt")) if inc.get("count", 0) <= 1 \
        else f"{_hhmm(inc.get('first_dt'))}–{_hhmm(inc.get('last_dt'))}"
    where = inc.get("target", "")
    game = inc.get("game") or {}
    if where.startswith("game:"):
        where = game.get("theme") or where[5:]
        if game.get("owner"):
            where += f" ({game['owner']})"
    who = ", ".join(inc.get("actors") or inc.get("models") or [])
    fns = ", ".join(inc.get("functions") or [])
    parts = [f"[{inc.get('level')}/{'/'.join(inc.get('envs') or ENVS)}]", inc.get("class", "?"), where]
    if who:
        parts.append(who)
    if fns:
        parts.append(f"in {fns}")
    parts.append(f"{inc.get('count', 0)}× {span} UTC")
    err = (inc.get("error") or "").replace("\n", " ")[:140]
    return " · ".join(parts) + (f" — {err}" if err else "")


def _snapshot_lines(game: dict) -> list[str]:
    if not game:
        return []
    if game.get("error"):
        return [f"      game: snapshot unavailable ({game['error']})"]
    if not game.get("exists"):
        return ["      game: no longer in Firestore (expired or deleted)"]
    out = [f"      game: {game.get('state')} day {game.get('day')}, {game.get('bots_alive')}/{game.get('bots_total')} bots alive, "
           f"GM {game.get('gameMaster')}, tier {game.get('tier')}, created {game.get('createdAt')}"]
    out.append(f"      models at the table: {', '.join(game.get('models') or []) or '-'}")
    es = game.get("errorState")
    out.append("      errorState: " + (f"{'recoverable' if es['recoverable'] else 'UNRECOVERABLE'} in {es.get('function')} at {es.get('at')} — {es.get('summary')}" if es else "none"))
    lm = game.get("last_message") or {}
    if lm and not lm.get("error"):
        ago = game.get("minutes_since_last_message")
        out.append(f"      last message: {lm.get('type')} by {lm.get('author')} at {lm.get('at')}"
                   + (f" ({ago} min ago)" if ago is not None else ""))
    return out


def render(report: dict) -> str:
    if not report.get("ok"):
        return f"monitor_betterstack failed: {report.get('error', 'unknown')}"
    if report.get("configured") is False:
        return f"{LABEL} — {report.get('checked_at')}\n  {report.get('error')}"
    c = report.get("counts", {})
    envs = "/".join(report.get("envs") or ["?"])
    out = [f"{LABEL} (Betterstack) — {report['checked_at']}",
           f"  window: last {report.get('window_min')}m   env: {envs}   "
           f"error={c.get('error', 0)} warn={c.get('warn', 0)}", ""]
    incidents = report.get("incidents", [])
    if report.get("source_empty"):
        out.append("  Both log tiers are EMPTY for the window (any env) - can't call it quiet.")
    elif incidents:
        out.append(f"  {len(incidents)} incident(s) in the window:")
        for inc in incidents[:15]:
            mark = "NEW " if inc.get("is_new") else "    "
            out.append(f"    {mark}{incident_line(inc)}")
            out.extend(_snapshot_lines(inc.get("game") or {}))
            for ln in inc.get("lines", [])[:3]:
                out.append(f"        · {ln['dt']} [{ln['level']}] {ln.get('function') or ''} {ln.get('bot') or ''} {ln.get('error') or ln.get('msg')}".rstrip())
        if len(incidents) > 15:
            out.append(f"    … +{len(incidents) - 15} more")
    else:
        out.append(f"  No {envs} error/warn lines in the window.")
    issues = report.get("issues", [])
    out.append("")
    if issues:
        out.append("  Issues this scan:")
        for i in issues:
            mark = "🔴" if i["severity"] == "urgent" else "⚠️"
            out.append(f"    {mark} [{i['severity']}] {i['detail']}")
    else:
        out.append("  No new incidents since last scan.")
    return "\n".join(out)


def render_digest(report: dict) -> str | None:
    """Digest block — only when there's something new. Returns None on a quiet
    scan so it adds no line to the daily digest."""
    if not report.get("ok"):
        return f"{LABEL}: scan failed ({report.get('error', 'unknown')})."
    issues = report.get("issues", [])
    if not issues:
        return None
    date = (report.get("checked_at") or "")[:10]
    head = f"{LABEL} — {date}: {len(issues)} new" \
           + (" (urgent)" if report.get("any_urgent") else "")
    lines = [head] + [f"  · {i['detail']}" for i in issues]
    return "\n".join(lines)


def replay(since: datetime, until: datetime) -> dict:
    """The incidents a scan over [since, until) WOULD alert on, as if nothing were
    seen before, with game snapshots. Reads and writes no state."""
    if not configured() or _creds_pending():
        return {**_unconfigured(until), "ok": False}
    creds = _creds()
    if not creds:
        return {"ok": False, "error": "BETTERSTACK_CH_HOST/USER/PASS not set"}
    window = _window_clause(since, until)
    try:
        source_empty = _count(creds, window) == 0
        rows = [] if source_empty else _fetch_rows(creds, window)
        nonprod = _nonprod_counts(creds, window)
    except (requests.RequestException, RuntimeError, ValueError) as e:
        return {"ok": False, "error": str(e)[:200]}
    incidents = fold_incidents(rows)
    issues, _ = derive_issues(incidents, {}, now=until)
    attach_snapshots(incidents, only_new=False)
    return {"ok": True, "since": since.isoformat(), "until": until.isoformat(),
            "envs": list(ENVS), "source_empty": source_empty, "rows": len(rows),
            "alerts": len(issues), "urgent": sum(i["severity"] == "urgent" for i in issues),
            "incidents": incidents, "issues": issues, "nonprod_counts": nonprod}


# ─── Selftest ────────────────────────────────────────────────────────────────


def selftest() -> None:
    """Offline asserts - no network, no state. Marlow has no pytest; handlers
    self-check this way (see werewolf_stats selftest)."""
    sql = _rows_sql(_window_clause())
    assert f"JSONExtractString(raw,'env') IN ({_sql_list(ENVS)})" in sql, sql
    assert "AS gameId" in sql and "AS details" in sql, sql
    assert TABLE in sql and (not ALT_TABLE or ALT_TABLE in sql), sql   # both tiers

    def line(dt, lvl, env, **kw):
        o = {"dt": dt, "lvl": lvl, "env": env}
        o.update(kw)
        return json.dumps(o)

    # Today's real shape (2026-10-23): one game, one slow bot, four timeouts in two
    # functions, plus an Argon timeout in the same game, plus a device link.
    body = "\n".join([
        line("2026-10-23 16:32:19", "error", "production", message="Game action failed: U",
             gameId="g1", function="U", botName="Vexa", model="minimax", gameState="DAY_DISCUSSION",
             error="MiniMax-M3 did not respond within 60s", details="ModelTimeoutError: ..."),
        line("2026-10-23 16:31:50", "error", "production", message="Error in talkToAll function: x",
             gameId="g1", function="talkToAll", botName="Vexa", model="minimax",
             error="MiniMax-M3 did not respond within 60s"),
        line("2026-10-23 16:18:02", "error", "production", message="Game action failed: Q",
             gameId="g1", function="Q", botName="Vexa", model="minimax",
             error="MiniMax-M3 did not respond within 60s"),
        line("2026-10-23 16:03:11", "error", "production", message="Game action failed: Q",
             gameId="g1", function="Q", botName="Narrator", model="gemini-argon",
             error="Gemini 4 Argon did not respond within 60s"),
        line("2026-10-23 15:58:00", "warn", "production", deviceId="dev-1",
             message="DEVICE_LINKED_BY_IP: keyless browser inherited device dev-1"),
        line("2026-10-23 15:50:00", "error", "test", message="Game action failed: U", gameId="t"),
        line("2026-10-23 15:49:00", "error", "", message="pre-09-02 line"),
    ])
    rows = _parse_rows(body)
    assert len(rows) == 5, [r["msg"] for r in rows]          # test / no-env dropped
    assert rows[0]["error"].startswith("MiniMax-M3"), rows[0]
    assert rows[0]["msg"] == "Game action failed: U"

    incidents = fold_incidents(rows)
    # One game, one failure class → ONE incident, both models and all three functions on it.
    assert len(incidents) == 2, [(i["target"], i["class"], i["models"]) for i in incidents]
    mm = next(i for i in incidents if i["target"] == "game:g1")
    assert mm["count"] == 4 and mm["class"] == "timeout", mm
    assert sorted(mm["models"]) == ["gemini-argon", "minimax"] and sorted(mm["functions"]) == ["Q", "U", "talkToAll"], mm
    assert sorted(mm["bots"]) == ["Narrator", "Vexa"], mm
    assert mm["first_dt"] == "2026-10-23 16:03:11" and mm["last_dt"] == "2026-10-23 16:32:19", mm
    dev = next(i for i in incidents if i["class"] == "device_link")
    assert dev["level"] == "warn" and dev["target"] == "device:dev-1"
    # The agent layer's JSON-shaped error folds in and reads as its message.
    blob = _parse_rows(line("2026-10-23 16:32:19.791000", "error", "production", gameId="g1",
                            error='{"modelType":"MiniMax-M3","name":"ModelTimeoutError","message":"MiniMax-M3 did not respond within 60s","stack":"..."}'))
    assert _error_text(blob[0]) == "MiniMax-M3 did not respond within 60s", blob
    assert incident_key(blob[0]) == incident_key(rows[0]), (incident_key(blob[0]), incident_key(rows[0]))
    assert fold_incidents(rows + blob)[0]["count"] == 5
    assert blob[0]["dt"].endswith(".791000") and _trim_dt(blob[0]["dt"]) == "2026-10-23 16:32:19"

    # Classifier: specific tags win over the generic parse catch-all.
    assert classify("STALE_ACTION cancelBotResponses: game is in VOTE") == "stale_action"
    assert classify("Insufficient balance: your prepaid balance can't cover") == "player_balance"
    assert classify("HTTP 503 Service Unavailable from Mistral") == "provider_busy"
    assert classify("Zod validation failed for JSON") == "parse_failure"
    assert classify("Transaction has expired") == "firestore_contention"
    assert classify("something nobody has seen") == "unclassified"

    now = datetime(2026, 10, 23, 17, 0, tzinfo=timezone.utc)
    # First scan ever: baseline, nothing new, one digest line.
    issues, baselined = derive_issues(incidents, None, now=now)
    assert baselined and len(issues) == 1 and issues[0]["severity"] == "digest"
    assert not any(i["is_new"] for i in incidents)
    # Second scan, nothing known: one urgent (the error incident), one digest (the warn).
    issues, baselined = derive_issues(incidents, {}, now=now)
    assert not baselined and len(issues) == 2
    assert sum(i["severity"] == "urgent" for i in issues) == 1, issues
    detail = next(i["detail"] for i in issues if i["target"] == mm["fingerprint"])
    assert "minimax/Vexa, gemini-argon/Narrator" in detail, detail
    # Third scan: the incident keeps producing lines → known, not re-pinged.
    seen = next_seen(incidents, {}, now=now)
    issues, _ = derive_issues(incidents, seen, now=now)
    assert issues == [], issues
    # ... until it has been quiet for the TTL: then the same failure is news again.
    later = now + timedelta(hours=INCIDENT_TTL_HOURS + 1)
    issues, _ = derive_issues(incidents, seen, now=later)
    assert len(issues) == 2, issues
    assert next_seen([], seen, now=later) == {}      # and it is forgotten from the state
    # Upgrade from the pre-10-23 per-line state: re-baseline, no urgent.
    issues, baselined = derive_issues(incidents, {}, legacy=True, now=now)
    assert baselined and "re-baselined" in issues[0]["detail"]

    # Incident line reads like the alert should.
    mm["game"] = {"exists": True, "theme": "Spaceship crew", "owner": "p@x"}
    s = incident_line(mm)
    assert s.startswith("[error/production] · timeout · Spaceship crew (p@x) · minimax/Vexa, gemini-argon/Narrator · in "), s
    assert "4× 16:03–16:32 UTC — " in s and "did not respond within 60s" in s, s

    w = _window_clause(datetime(2026, 9, 22, 18, tzinfo=timezone.utc),
                       datetime(2026, 9, 23, 2, tzinfo=timezone.utc))
    assert "2026-09-22 18:00:00" in w and "2026-09-23 02:00:00" in w, w

    # ── Poker: same pipeline, its own source/state/fields ──
    configure("poker")
    assert BS_LATEST.name == "betterstack_poker_latest.json" and GAMES == "poker_games"
    saved = (TABLE, ALT_TABLE)
    globals()["TABLE"], globals()["ALT_TABLE"] = "remote(t1_poker_logs)", ""
    sql = _rows_sql(_window_clause())
    assert "JSONExtractString(raw,'action') AS function" in sql, sql      # Poker's names → common columns
    assert "JSONExtractString(raw,'actor') AS botName" in sql and "AS failedAction" in sql, sql
    assert "remote(t1_poker_logs)" in sql and "UNION" not in sql, sql    # single tier when no alt
    # Poker's lane-failure warn + the crash error of one server action fold into one incident.
    # (Rows arrive under the COMMON column names — the SQL above already aliased
    # action→function, actor→botName, user→userEmail, lane→gameState.)
    body = "\n".join([
        line("2026-10-31 12:00:01", "error", "production", message="action failed", gameId="p1",
             function="advanceGame", userEmail="ab@x", error="AiCallError: Claude did not respond within 60s"),
        line("2026-10-31 12:00:00", "warn", "production", message="lane stopped — awaiting player retry",
             gameId="p1", function="advanceGame", userEmail="ab@x", gameState="game", failedAction="DECISION",
             botName="Paul", model="claude", details="AiCallError: Claude did not respond within 60s"),
        line("2026-10-31 11:00:00", "error", "development", message="action failed", gameId="dev"),
    ])
    prow = _parse_rows(body)
    assert len(prow) == 2 and prow[0]["function"] == "advanceGame" and prow[0]["userEmail"] == "ab@x", prow
    assert prow[1]["botName"] == "Paul" and prow[1]["gameState"] == "game" and prow[1]["failedAction"] == "DECISION", prow[1]
    pinc = fold_incidents(prow)
    assert len(pinc) == 1 and pinc[0]["class"] == "timeout" and pinc[0]["level"] == "error", pinc
    assert pinc[0]["actors"] == ["claude/Paul"] and pinc[0]["gameStates"] == ["game"], pinc[0]
    pinc[0]["game"] = {"exists": True, "theme": "Dune", "owner": "ab@x"}
    assert incident_line(pinc[0]).startswith("[error/production] · timeout · Dune (ab@x) · claude/Paul · in advanceGame"), incident_line(pinc[0])
    # Unconfigured Poker: a quiet ok report, no digest line, render says why.
    globals()["TABLE"], globals()["ALT_TABLE"] = "", ""
    assert not configured()
    u = _unconfigured(now)
    assert u["ok"] and u["configured"] is False and render_digest(u) is None and "no Benchmark" not in render(u)
    assert "no Betterstack source" in render(u), render(u)
    assert replay(now, now)["ok"] is False
    # Tables set but Poker's own connection creds missing: STILL quiet — never fall
    # back to the shared (other-cluster) connection and page on CLUSTER_DOESNT_EXIST.
    globals()["TABLE"] = "remote(t1_poker_logs)"
    for k in ("BETTERSTACK_POKER_CH_HOST", "BETTERSTACK_POKER_CH_USER", "BETTERSTACK_POKER_CH_PASS"):
        os.environ.pop(k, None)
    assert configured() and _creds() is None and _creds_pending()
    u = _unconfigured(now)
    assert u["ok"] and u["configured"] is False and "not in the plist" in u["error"], u
    assert report()["configured"] is False          # the real entry point takes the quiet path too
    os.environ.update(BETTERSTACK_POKER_CH_HOST="https://us", BETTERSTACK_POKER_CH_USER="u", BETTERSTACK_POKER_CH_PASS="p")
    assert _creds() == {"host": "https://us", "user": "u", "pw": "p"} and not _creds_pending()
    for k in ("BETTERSTACK_POKER_CH_HOST", "BETTERSTACK_POKER_CH_USER", "BETTERSTACK_POKER_CH_PASS"):
        os.environ.pop(k, None)
    globals()["TABLE"], globals()["ALT_TABLE"] = saved
    configure("werewolf")
    assert GAMES == "games" and "AS function" in _rows_sql(_window_clause()) and FIELD_SRC["function"] == "function"
    print("selftest ok")


def _parse_utc(s: str) -> datetime:
    d = datetime.fromisoformat(s.replace("Z", "+00:00"))
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


# ─── CLI ─────────────────────────────────────────────────────────────────────


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--app", choices=sorted(APPS), default="werewolf",
                    help="which game's source to scan (default werewolf)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("report", help="Scan Betterstack for new incidents + persist (JSON)")
    sub.add_parser("show", help="Render the last persisted scan, human-readable")
    sub.add_parser("digest", help="Digest block from the last scan (empty if nothing new)")
    p_replay = sub.add_parser("replay", help="Incidents a scan of a fixed UTC window would alert on (no state touched)")
    p_replay.add_argument("--since", required=True, help="e.g. 2026-10-23T15:00Z")
    p_replay.add_argument("--until", required=True)
    p_replay.add_argument("--text", action="store_true", help="render like `show` instead of JSON")
    sub.add_parser("selftest", help="Offline asserts (no network)")
    args = ap.parse_args()
    configure(args.app)
    if args.cmd == "selftest":
        selftest()
        return
    if args.cmd == "replay":
        res = replay(_parse_utc(args.since), _parse_utc(args.until))
        if args.text and res.get("ok"):
            res = {**res, "checked_at": f"replay {res['since']} → {res['until']}", "window_min": "-"}
            res["counts"] = {}
            print(render(res))
        else:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        sys.exit(0 if res.get("ok") else 1)
    if args.cmd == "report":
        res = report()
        print(json.dumps(res, indent=2, ensure_ascii=False))
        sys.exit(0 if res.get("ok") else 1)
    elif args.cmd == "show":
        try:
            with BS_LATEST.open() as f:
                print(render(json.load(f)))
        except (OSError, json.JSONDecodeError):
            print("No scan yet — run `report` first.")
    elif args.cmd == "digest":
        try:
            with BS_LATEST.open() as f:
                d = render_digest(json.load(f))
            print(d if d else "")
        except (OSError, json.JSONDecodeError):
            print("")


if __name__ == "__main__":
    main()
