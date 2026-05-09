#!/bin/bash
# Install Marlow's tick into the user's crontab. Idempotent — safe to
# re-run; will not add a duplicate entry. Touches only your user
# crontab; no system-wide daemons or LaunchAgents.
#
# After install, cron fires every 20 minutes while the laptop is awake.
# Stop temporarily with:  touch ~/.marlow-stop
# Stop permanently with:  bash driver/uninstall-cron.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TICK_PATH="${REPO_ROOT}/driver/tick.sh"
LOG_PATH="${HOME}/marlow.log"
CRON_LINE="*/20 * * * * ${TICK_PATH} >> ${LOG_PATH} 2>&1"
MARKER="# marlow tick — managed by driver/install-cron.sh"

if [ ! -x "$TICK_PATH" ]; then
    echo "error: $TICK_PATH not found or not executable" >&2
    exit 1
fi

# Snapshot current crontab (gracefully handle "no crontab installed").
EXISTING="$(crontab -l 2>/dev/null || true)"

if echo "$EXISTING" | grep -Fq "$TICK_PATH"; then
    echo "already installed (line referencing $TICK_PATH found in crontab)"
    echo ""
    echo "current crontab:"
    crontab -l 2>/dev/null | grep -F "$TICK_PATH"
    exit 0
fi

# Append our marker + line; preserve everything else.
{
    if [ -n "$EXISTING" ]; then
        printf '%s\n' "$EXISTING"
    fi
    printf '\n%s\n%s\n' "$MARKER" "$CRON_LINE"
} | crontab -

echo "installed"
echo ""
echo "  $CRON_LINE"
echo ""
echo "verify:    crontab -l | grep marlow"
echo "watch log: tail -f $LOG_PATH"
echo "pause:     touch ~/.marlow-stop  (cron still fires, tick exits clean)"
echo "uninstall: bash driver/uninstall-cron.sh"
echo ""
echo "macOS note: if ticks don't fire after install, grant Full Disk Access"
echo "to /usr/sbin/cron via System Settings > Privacy & Security."
