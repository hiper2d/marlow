#!/bin/bash
# Marlow tick driver. Cron entry point. Runs every 20 min.
#
# Flow:
#   1. Killswitch check (~/.marlow/stop)
#   2. Pause check (~/.marlow/pause)
#   3. Daily operational self-audit (out-of-session, monitor_self)
#   4. Acquire lock (/tmp/marlow.lock)
#   5. Pick next subtask via scheduler.py
#   6. Invoke Claude Code session (Marlow) to execute the named handler
#   7. Record outcome via scheduler.py complete
#   8. Release lock

set -euo pipefail

# Cron has a stripped-down environment — explicitly add common bin dirs so
# `claude` and `uv` resolve.
export PATH="$HOME/.local/bin:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:$PATH"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Profile. "" = legacy single-loop (pre-split, byte-identical behavior).
# "writer"/"ops" = one of the two split loops: own queue/lock/temp/heartbeat,
# its identity appended to the session, MARLOW_PROFILE exported so scheduler.py
# scopes state + task set. Each split loop must be fully independent so a wedged
# writer tick can't block the ops loop.
PROFILE="${1:-}"
if [ -n "$PROFILE" ]; then
    export MARLOW_PROFILE="$PROFILE"
    SUFFIX="-$PROFILE"
    MARLOW_DIR="$HOME/.marlow/$PROFILE"
    IDENTITY_FILE="$REPO_ROOT/profiles/$PROFILE/IDENTITY.md"
else
    SUFFIX=""
    MARLOW_DIR="$HOME/.marlow"
    IDENTITY_FILE=""
fi

# Agent + model switchboard (driver/agent.conf). Resolved here, before any queue
# work, so a misconfigured backend fails fast without consuming a subtask.
#   - Pins the model explicitly so ticks IGNORE the global Claude Code default:
#     flipping the interactive default (e.g. to Fable) no longer drags autonomous
#     ticks onto that model and burns quota.
#   - Two tiers: writer/legacy -> heavy, ops -> light (cheap model for mechanical
#     work). Var name is MARLOW_MODEL_<TIER>_<AGENT>, resolved by indirection.
AGENT_CONF="$REPO_ROOT/driver/agent.conf"
[ -f "$AGENT_CONF" ] && source "$AGENT_CONF"
MARLOW_AGENT="${MARLOW_AGENT:-claude}"

case "$PROFILE" in
    ops) MARLOW_TIER="light" ;;
    *)   MARLOW_TIER="heavy" ;;   # writer + legacy no-profile
esac

# Respect an explicit MARLOW_MODEL override (handy for one-off debugging);
# otherwise resolve from the tier/agent matrix, with a hard fallback so a
# missing/incomplete agent.conf can never crash the loop.
if [ -z "${MARLOW_MODEL:-}" ]; then
    _model_var="MARLOW_MODEL_$(echo "${MARLOW_TIER}_${MARLOW_AGENT}" | tr '[:lower:]' '[:upper:]')"
    MARLOW_MODEL="${!_model_var:-}"
    if [ -z "$MARLOW_MODEL" ]; then
        case "$MARLOW_TIER" in
            light) MARLOW_MODEL="claude-sonnet-5" ;;
            *)     MARLOW_MODEL="claude-opus-4-8" ;;
        esac
    fi
fi

# Only the Claude backend is operational. Refuse any other backend up front so a
# deliberate-but-premature flip (e.g. to codex before it's wired) does not pick,
# stage, then fail a subtask. Queue is untouched. See agent.conf wiring notes.
if [ "$MARLOW_AGENT" != "claude" ]; then
    # log() is defined further down; use echo directly for this early exit.
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] FATAL: MARLOW_AGENT='$MARLOW_AGENT' is not operational yet (only 'claude' works; codex needs a subscription + a Codex-shaped cost parser in tools/cost.py). Not ticking; queue untouched."
    exit 0
fi

LOCK_FILE="/tmp/marlow${SUFFIX}.lock"
LOCK_SKIPS="/tmp/marlow${SUFFIX}.lock.skips"   # consecutive blocked-tick counter (staleness signal, not time)
MAX_LOCK_SKIPS=3                       # force-break the lock after this many blocked AWAKE ticks
SUBTASK_FILE="/tmp/marlow${SUFFIX}-subtask.json"
RESULT_FILE="/tmp/marlow${SUFFIX}-tick-result.json"
STREAM_FILE="/tmp/marlow${SUFFIX}-tick-stream.jsonl"
KILLSWITCH="$HOME/.marlow/stop"   # killswitch + pause are GLOBAL (one stop halts both loops)
PAUSE="$HOME/.marlow/pause"
SESSIONS_LOG="$MARLOW_DIR/sessions.log"
LOCK_BREAK_LOG="$MARLOW_DIR/lock_breaks.log"   # append-only record of auto-recovered stale/wedged locks
SESSION_LIMIT_LOG="$MARLOW_DIR/session_limits.log"   # append-only record of Claude-quota throttle re-queues
HEARTBEAT_LOG="$MARLOW_DIR/heartbeat.log"   # one ISO ts per tick the driver actually ran — the loop's proof-of-liveness
TICK_TIMEOUT_SEC=300
OWNS_LOCK=0   # flips to 1 once THIS tick acquires the lock, so cleanup only frees its own

mkdir -p "$MARLOW_DIR"

log() {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*"
}

# Wall-clock timeout wrapper. macOS doesn't ship GNU `timeout` by default;
# fall back to gtimeout (brew coreutils), then to Perl's alarm builtin
# which is universally available on macOS and Linux.
run_with_timeout() {
    local seconds=$1; shift
    if command -v timeout >/dev/null 2>&1; then
        timeout "$seconds" "$@"
    elif command -v gtimeout >/dev/null 2>&1; then
        gtimeout "$seconds" "$@"
    else
        perl -e 'use POSIX qw(SIGTERM); my $pid = fork; if ($pid == 0) { exec @ARGV[1..$#ARGV] or exit 127; } eval { local $SIG{ALRM} = sub { kill SIGTERM, $pid; die "timeout\n"; }; alarm $ARGV[0]; waitpid $pid, 0; alarm 0; }; exit ($@ eq "timeout\n" ? 124 : ($? >> 8));' "$seconds" "$@"
    fi
}

cleanup() {
    rm -f "$SUBTASK_FILE" "$RESULT_FILE" "$STREAM_FILE"
    # Only release the lock if WE acquired it. A tick that skipped because the
    # lock was held by a live holder must never delete that holder's lock.
    if [ "$OWNS_LOCK" = "1" ]; then
        rm -f "$LOCK_FILE" "$LOCK_SKIPS"
    fi
}
trap cleanup EXIT

# 1. Killswitch
if [ -f "$KILLSWITCH" ]; then
    log "killswitch present, exiting"
    exit 0
fi

# 2. Pause
if [ -f "$PAUSE" ]; then
    log "paused, skipping tick"
    exit 0
fi

# Heartbeat — record that the driver actually fired THIS tick. Placed after the
# killswitch/pause gates (an intentionally-stopped loop should NOT heartbeat, so
# overdue ticks during a stop/pause read as expected dormancy) but before the
# lock and scheduler, so even a "nothing to do" or lock-skipped tick still proves
# the loop was alive. monitor_self reads this log to tell "this tick silently
# stopped firing" (driver alive, tick skipped) from "the whole loop was dormant"
# (laptop asleep/offline — no heartbeats in the window). Trimmed to bound growth.
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$HEARTBEAT_LOG"
tail -n 2000 "$HEARTBEAT_LOG" > "$HEARTBEAT_LOG.tmp" 2>/dev/null && mv "$HEARTBEAT_LOG.tmp" "$HEARTBEAT_LOG" || true

# 3. Daily operational self-audit — runs OUTSIDE Marlow's session so a broken
#    session or a missed scheduler pick can't suppress it, and BEFORE the lock so
#    a stuck previous tick can't either. Rate-limited to once per UTC day; the
#    handler does its own deterministic Telegram escalation, and its daily "all
#    green" digest line doubles as the audit's proof-of-life.
SELF_AUDIT_STAMP="$MARLOW_DIR/last_self_audit"
TODAY="$(date -u +%Y-%m-%d)"
if [ "$(cat "$SELF_AUDIT_STAMP" 2>/dev/null || echo '')" != "$TODAY" ]; then
    cd "$REPO_ROOT"
    log "running operational self-audit (out-of-session)"
    if run_with_timeout 120 uv run python handlers/monitor_self.py report >/dev/null 2>>"$SESSIONS_LOG"; then
        echo "$TODAY" > "$SELF_AUDIT_STAMP"
        log "self-audit complete"
    else
        log "WARNING: self-audit failed — see $SESSIONS_LOG"
    fi
fi

# 4. Lock — staleness-aware, no wall-clock (sleep makes elapsed time lie).
# If the lock is held, decide whether the holder is alive (skip) or wedged
# (break it) from two signals:
#   fast path — PID check: the recorded holder process is plainly gone -> break.
#   slow path — skip counter: holder looks alive but has blocked MAX_LOCK_SKIPS
#               consecutive AWAKE ticks -> force-break. The counter only advances
#               when a tick actually fires, so an overnight sleep never inflates
#               it, and a holder that's merely paused gets a grace window to
#               resume and clean up before we break its lock.
if [ -f "$LOCK_FILE" ]; then
    holder_pid="$(cat "$LOCK_FILE" 2>/dev/null || echo '')"
    if [ -n "$holder_pid" ] && ! kill -0 "$holder_pid" 2>/dev/null; then
        # Fast path: the recorded holder process is dead. Stale lock -> break it.
        log "lock held by dead PID $holder_pid — breaking stale lock"
        echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) stale-lock-break: holder PID $holder_pid was dead" >> "$LOCK_BREAK_LOG"
        rm -f "$LOCK_FILE" "$LOCK_SKIPS"
    else
        # Holder looks alive (or PID unreadable): count this blocked attempt.
        skips="$(cat "$LOCK_SKIPS" 2>/dev/null || echo 0)"
        case "$skips" in ''|*[!0-9]*) skips=0 ;; esac
        skips=$((skips + 1))
        if [ "$skips" -ge "$MAX_LOCK_SKIPS" ]; then
            log "lock blocked $skips consecutive ticks (holder PID ${holder_pid:-?}) — force-breaking wedged lock"
            echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) force-lock-break: blocked $skips ticks, holder PID ${holder_pid:-?}" >> "$LOCK_BREAK_LOG"
            rm -f "$LOCK_FILE" "$LOCK_SKIPS"
        else
            echo "$skips" > "$LOCK_SKIPS"
            log "previous tick still running (lock held, skip $skips/$MAX_LOCK_SKIPS), exiting"
            exit 0
        fi
    fi
fi
# Acquire: claim the lock, reset the skip counter, mark ownership.
echo $$ > "$LOCK_FILE"
rm -f "$LOCK_SKIPS"
OWNS_LOCK=1

# 5. Pick next subtask
cd "$REPO_ROOT"
SUBTASK_JSON=$(uv run python driver/scheduler.py pick 2>&1) || {
    rc=$?
    if [ $rc -eq 1 ]; then
        log "nothing to do"
        exit 0
    fi
    log "scheduler error (exit $rc): $SUBTASK_JSON"
    exit $rc
}

SUBTASK_ID=$(echo "$SUBTASK_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")
SUBTASK_HANDLER=$(echo "$SUBTASK_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['handler'])")
# Per-handler timeout. Heavy ticks (draft_article, grade_memory) declare a larger
# timeout_sec in their task context; everything else uses the 300s default. Keep
# values < the launchd interval (1200s) so a long tick releases the lock before
# the next fire — we use 900s.
SUBTASK_TIMEOUT=$(echo "$SUBTASK_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin).get('context',{}).get('timeout_sec') or '')" 2>/dev/null || echo '')
TICK_TIMEOUT="${SUBTASK_TIMEOUT:-$TICK_TIMEOUT_SEC}"
log "picked subtask: $SUBTASK_ID (handler: $SUBTASK_HANDLER, timeout ${TICK_TIMEOUT}s)"

# Stage subtask for the session to read.
echo "$SUBTASK_JSON" > "$SUBTASK_FILE"
rm -f "$RESULT_FILE"

# 6. Invoke Claude Code (Marlow's session)
PROMPT="A subtask is queued for you in $SUBTASK_FILE. Read it, execute the named handler per your operating contract (CLAUDE.md plus your appended profile), write any outputs to the appropriate project directory, then write your outcome JSON to $RESULT_FILE before exiting."

# Per-profile identity. The repo-root CLAUDE.md is the shared, identity-neutral
# contract (auto-loaded by every session). When a profile is active we append
# its IDENTITY.md so writer gets the full persona and ops gets the lean faceless
# prompt. Legacy (no profile) appends nothing — CLAUDE.md alone, as before.
# bash 3.2-safe empty-array expansion (macOS /bin/bash) via ${arr[@]+...}.
IDENTITY_ARGS=()
if [ -n "$IDENTITY_FILE" ] && [ -f "$IDENTITY_FILE" ]; then
    IDENTITY_ARGS=(--append-system-prompt "$(cat "$IDENTITY_FILE")")
fi

# Stream raw JSONL to a temp file so cost.py can extract usage/cost after.
# Stderr still goes to SESSIONS_LOG for crash diagnostics.
rm -f "$STREAM_FILE"
if run_with_timeout "$TICK_TIMEOUT" claude -p --model "$MARLOW_MODEL" --output-format stream-json --verbose ${IDENTITY_ARGS[@]+"${IDENTITY_ARGS[@]}"} "$PROMPT" >"$STREAM_FILE" 2>>"$SESSIONS_LOG"; then
    log "session exited cleanly"
    SESSION_OK=1
else
    rc=$?
    log "session exited with code $rc (124 = timeout)"
    SESSION_OK=0
fi

# Log cost record (always — even on crash, so the audit trail is complete).
uv run python tools/cost.py log --tick-id "$SUBTASK_ID" --handler "$SUBTASK_HANDLER" < "$STREAM_FILE" || true
# Extract human-readable assistant text into the session log.
{
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] === $SUBTASK_ID ($SUBTASK_HANDLER) ==="
    uv run python tools/cost.py extract-text < "$STREAM_FILE" || true
} >> "$SESSIONS_LOG"

# Session-limit re-queue. If the session died because the Claude quota was
# exhausted, the tick never really ran — the task was picked but not attempted.
# Put it back to pending (don't consume it) and exit; the next tick after the
# quota resets re-picks it untouched. This is what stops a storm (e.g. 06-07)
# from silently marking-failed every task scheduled during the throttle window.
if [ "${SESSION_OK:-1}" = "0" ] && grep -qiE "hit your (session|usage) limit|session limit|usage limit reached" "$STREAM_FILE" 2>/dev/null; then
    log "Claude session limit hit — re-queueing $SUBTASK_ID (not consumed), exiting"
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) session-limit: re-queued $SUBTASK_ID ($SUBTASK_HANDLER)" >> "$SESSION_LIMIT_LOG"
    uv run python driver/scheduler.py requeue "$SUBTASK_ID" --result "re-queued: Claude session limit (transient, not consumed)" || true
    exit 0
fi

# 7. Record outcome
if [ ! -f "$RESULT_FILE" ]; then
    log "WARNING: session did not write a result file — marking subtask failed"
    cat > "$RESULT_FILE" <<EOF
{"status": "failed", "result": "session exited without writing result file", "checkpoint": null, "notify": null}
EOF
fi

RESULT_STATUS=$(python3 -c "import json; print(json.load(open('$RESULT_FILE'))['status'])")
RESULT_TEXT=$(python3 -c "import json; print(json.load(open('$RESULT_FILE'))['result'])")
RESULT_NOTIFY=$(python3 -c "import json; r=json.load(open('$RESULT_FILE')); print(json.dumps(r.get('notify')) if r.get('notify') else '')")

uv run python driver/scheduler.py complete "$SUBTASK_ID" "$RESULT_STATUS" --result "$RESULT_TEXT"

# Fire notify if session asked for one
if [ -n "$RESULT_NOTIFY" ]; then
    NOTIFY_URGENCY=$(echo "$RESULT_NOTIFY" | python3 -c "import json,sys; print(json.load(sys.stdin)['urgency'])")
    NOTIFY_MSG=$(echo "$RESULT_NOTIFY" | python3 -c "import json,sys; print(json.load(sys.stdin)['message'])")
    if [ "$NOTIFY_URGENCY" = "urgent" ]; then
        uv run python tools/notify.py "$NOTIFY_MSG" || true
    else
        uv run python tools/notify.py "$NOTIFY_MSG" --digest || true
    fi
fi

log "tick complete"
