#!/bin/bash
# Remove Marlow's tick from the user's crontab. Idempotent — safe to
# re-run on an already-uninstalled crontab.
#
# Removes only the line(s) referencing this repo's tick.sh and the
# managed-by marker comment immediately above it. All other crontab
# entries are preserved.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TICK_PATH="${REPO_ROOT}/driver/tick.sh"
MARKER="# marlow tick — managed by driver/install-cron.sh"

EXISTING="$(crontab -l 2>/dev/null || true)"

if [ -z "$EXISTING" ]; then
    echo "no crontab installed for this user — nothing to do"
    exit 0
fi

if ! echo "$EXISTING" | grep -Fq "$TICK_PATH"; then
    echo "not installed (no crontab line references $TICK_PATH)"
    exit 0
fi

# Strip both the marker line and any line referencing tick.sh.
NEW_CRONTAB="$(echo "$EXISTING" | grep -vF "$TICK_PATH" | grep -vF "$MARKER")"

if [ -z "$NEW_CRONTAB" ]; then
    # Nothing left — drop the crontab entirely rather than installing
    # an empty one (some cron implementations dislike empty crontabs).
    crontab -r
else
    printf '%s\n' "$NEW_CRONTAB" | crontab -
fi

echo "uninstalled"
echo ""
echo "verify: crontab -l 2>/dev/null | grep marlow  (should be empty)"
echo ""
echo "any tick currently mid-flight will finish naturally; no new ticks"
echo "will fire until you reinstall via driver/install-cron.sh."
