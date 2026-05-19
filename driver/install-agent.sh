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

# Plist generation, delegated to Python (plistlib stdlib) so we can:
#   - PRESERVE existing EnvironmentVariables from the plist if it's already
#     there. Running install without an env var no longer wipes the var —
#     vars stay until you explicitly override them or delete the plist.
#   - Override with install-time env values when set:
#       `O_K=<key> bash driver/install-agent.sh`           — set/update O_K
#       `C_F=<token> bash driver/install-agent.sh`         — set/update C_F
#       `O_K=<key> C_F=<token> bash driver/install-agent.sh` — both at once
#       `bash driver/install-agent.sh`                     — preserve all
#   - PATH always gets the deterministic value (don't preserve a stale PATH).
#
# Plist file lives at ~/Library/LaunchAgents/ (not in the repo), so any
# baked secret never reaches git. To clear a baked secret, edit the plist
# directly with PlistBuddy or delete the whole file before re-running.

/usr/bin/python3 - "$PLIST_PATH" "$LABEL" "$TICK_PATH" "$LOG_PATH" "$INTERVAL" "$HOME" <<'PYEOF'
import os, plistlib, sys
from pathlib import Path

plist_path = Path(sys.argv[1])
label, tick_path, log_path, interval, home = sys.argv[2:7]

# Preserve any EnvironmentVariables already in the plist.
preserved = {}
if plist_path.exists():
    try:
        with plist_path.open("rb") as f:
            existing = plistlib.load(f)
        preserved = dict(existing.get("EnvironmentVariables", {}) or {})
    except Exception:
        preserved = {}

env = dict(preserved)
# Force PATH every time — it's a known deterministic value.
env["PATH"] = f"{home}/.local/bin:/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin"

# Pull known secret-style vars from install-time env if present.
# Add more names here when a new monitored target gets its own token.
for k in ("O_K", "C_F"):
    v = os.environ.get(k)
    if v:
        env[k] = v

plist = {
    "Label": label,
    "ProgramArguments": ["/bin/bash", tick_path],
    "StartInterval": int(interval),
    "RunAtLoad": False,
    "StandardOutPath": log_path,
    "StandardErrorPath": log_path,
    "EnvironmentVariables": env,
}

with plist_path.open("wb") as f:
    plistlib.dump(plist, f)

extra = sorted(k for k in env if k != "PATH")
if extra:
    print(f"plist EnvironmentVariables: PATH + {', '.join(extra)}")
else:
    print("plist EnvironmentVariables: PATH only (no secrets set)")
PYEOF

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
