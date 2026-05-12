#!/bin/bash
# Uninstall Marlow's launchd LaunchAgent. Idempotent — safe to re-run
# even when nothing is installed.

set -euo pipefail

LABEL="com.marlow.tick"
PLIST_PATH="${HOME}/Library/LaunchAgents/${LABEL}.plist"

if launchctl print "gui/$(id -u)/${LABEL}" >/dev/null 2>&1; then
    launchctl bootout "gui/$(id -u)/${LABEL}"
    echo "agent unloaded"
else
    echo "agent not loaded — nothing to bootout"
fi

if [ -f "$PLIST_PATH" ]; then
    rm -f "$PLIST_PATH"
    echo "plist removed: $PLIST_PATH"
else
    echo "no plist at $PLIST_PATH — nothing to remove"
fi

echo ""
echo "any tick currently mid-flight will finish naturally; no new ticks"
echo "will fire until you reinstall via driver/install-agent.sh."
