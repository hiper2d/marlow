#!/bin/bash
# Install Marlow's tick as a per-user launchd LaunchAgent. Replaces the
# earlier cron approach — LaunchAgents run inside the user's login
# session, so the Claude CLI can reach its OAuth tokens in the macOS
# Keychain (cron jobs cannot).
#
# Idempotent — safe to re-run. If already loaded, the agent is
# bootout'd first and then bootstrapped fresh with the current plist.
#
# After install: agent fires tick.sh every 20 min while the system is
# awake. macOS auto-loads it at every login. Closing the lid puts the
# system to sleep, which pauses the agent until you reopen.
#
# Stop temporarily with:  touch ~/.marlow/stop
# Stop permanently with:  bash driver/uninstall-agent.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TICK_PATH="${REPO_ROOT}/driver/tick.sh"
MARLOW_DIR="${HOME}/.marlow"
LOG_PATH="${MARLOW_DIR}/log"
LABEL="com.marlow.tick"
PLIST_PATH="${HOME}/Library/LaunchAgents/${LABEL}.plist"
INTERVAL=1200   # 20 minutes

if [ ! -x "$TICK_PATH" ]; then
    echo "error: $TICK_PATH not found or not executable" >&2
    exit 1
fi

mkdir -p "$MARLOW_DIR" "$(dirname "$PLIST_PATH")"

# If already loaded, bootout first so we can replace.
if launchctl print "gui/$(id -u)/${LABEL}" >/dev/null 2>&1; then
    echo "agent already loaded — bootout to refresh"
    launchctl bootout "gui/$(id -u)/${LABEL}" || true
fi

cat > "$PLIST_PATH" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>${TICK_PATH}</string>
    </array>
    <key>StartInterval</key>
    <integer>${INTERVAL}</integer>
    <key>RunAtLoad</key>
    <false/>
    <key>StandardOutPath</key>
    <string>${LOG_PATH}</string>
    <key>StandardErrorPath</key>
    <string>${LOG_PATH}</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>${HOME}/.local/bin:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>
EOF

launchctl bootstrap "gui/$(id -u)" "$PLIST_PATH"

echo "installed"
echo ""
echo "  plist:    ${PLIST_PATH}"
echo "  label:    ${LABEL}"
echo "  interval: ${INTERVAL}s ($(( INTERVAL / 60 )) min)"
echo "  log:      ${LOG_PATH}"
echo ""
echo "verify:    launchctl print gui/\$(id -u)/${LABEL} | head"
echo "watch log: tail -f ${LOG_PATH}"
echo "pause:     touch ~/.marlow/stop  (agent still fires, tick exits clean)"
echo "uninstall: bash driver/uninstall-agent.sh"
