#!/bin/bash
# Marlow tick driver. Cron entry point. Runs every 20 min.
#
# Flow:
#   1. Killswitch check (~/.marlow-stop)
#   2. Pause check (~/.marlow-pause)
#   3. Acquire lock (/tmp/marlow.lock)
#   4. Pick next subtask via scheduler.py
#   5. Invoke Claude Code session (Marlow) to execute the named handler
#   6. Record outcome via scheduler.py complete
#   7. Release lock

set -euo pipefail

# Cron has a stripped-down environment — explicitly add common bin dirs so
# `claude` and `uv` resolve.
export PATH="$HOME/.local/bin:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:$PATH"

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCK_FILE="/tmp/marlow.lock"
SUBTASK_FILE="/tmp/marlow-subtask.json"
RESULT_FILE="/tmp/marlow-tick-result.json"
KILLSWITCH="$HOME/.marlow-stop"
PAUSE="$HOME/.marlow-pause"
TICK_TIMEOUT_SEC=300

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
    rm -f "$LOCK_FILE" "$SUBTASK_FILE" "$RESULT_FILE"
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

# 3. Lock
if [ -f "$LOCK_FILE" ]; then
    log "previous tick still running (lock held), exiting"
    exit 0
fi
echo $$ > "$LOCK_FILE"

# 4. Pick next subtask
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
log "picked subtask: $SUBTASK_ID (handler: $SUBTASK_HANDLER)"

# Stage subtask for the session to read.
echo "$SUBTASK_JSON" > "$SUBTASK_FILE"
rm -f "$RESULT_FILE"

# 5. Invoke Claude Code (Marlow's session)
PROMPT="A subtask is queued for you in $SUBTASK_FILE. Read it, execute the named handler per the contract in CLAUDE.md, write any editorial outputs to the appropriate project directory, then write your outcome JSON to $RESULT_FILE before exiting."

if run_with_timeout "$TICK_TIMEOUT_SEC" claude -p "$PROMPT" >> "$REPO_ROOT/marlow-sessions.log" 2>&1; then
    log "session exited cleanly"
else
    rc=$?
    log "session exited with code $rc (124 = timeout)"
fi

# 6. Record outcome
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
