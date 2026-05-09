#!/bin/bash
# Marlow tick driver. Cron entry point. Runs every 20 min.
#
# Flow:
#   1. Killswitch check (~/.marlow-stop)
#   2. Pause check (~/.marlow-pause)
#   3. Acquire lock (/tmp/marlow.lock)
#   4. Pick next subtask via scheduler.py
#   5. Invoke Claude Code session to execute handler   ← stubbed in v0.1
#   6. Record outcome via scheduler.py complete
#   7. Release lock
#
# v0.1: handler invocation is stubbed — we just print what would run and
# mark the subtask as done. Real Claude Code wiring lands in chunk 4.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCK_FILE="/tmp/marlow.lock"
RESULT_FILE="/tmp/marlow-tick-result.json"
KILLSWITCH="$HOME/.marlow-stop"
PAUSE="$HOME/.marlow-pause"

log() {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*"
}

cleanup() {
    rm -f "$LOCK_FILE" "$RESULT_FILE"
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

# 5. Invoke Claude Code session  [STUBBED in v0.1]
# Real wiring will look roughly like:
#
#   echo "$SUBTASK_JSON" > /tmp/marlow-subtask.json
#   timeout 300 claude --append-system-prompt-file CLAUDE.md \
#     "Execute the subtask in /tmp/marlow-subtask.json. \
#      Write outcome to /tmp/marlow-tick-result.json."
#
# For now, fake an outcome so we can validate the queue + complete flow.
log "[STUB] would invoke Claude Code with handler '$SUBTASK_HANDLER'"
cat > "$RESULT_FILE" <<EOF
{"status": "done", "result": "stubbed v0.1 — no handler executed", "checkpoint": null, "notify": null}
EOF

# 6. Record outcome
RESULT_STATUS=$(python3 -c "import json; print(json.load(open('$RESULT_FILE'))['status'])")
RESULT_TEXT=$(python3 -c "import json; print(json.load(open('$RESULT_FILE'))['result'])")
uv run python driver/scheduler.py complete "$SUBTASK_ID" "$RESULT_STATUS" --result "$RESULT_TEXT"

log "tick complete"
