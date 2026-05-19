"""
env_loader — populate os.environ from Marlow's launchd plist.

Single source of truth for Marlow-only env vars (O_K, C_F, future tokens)
is `~/Library/LaunchAgents/com.marlow.tick.plist`. Launchd-fired ticks
inherit those vars directly; standalone invocations of marlow_cli or any
handler don't, because they inherit only the shell env.

Calling `import_plist_env()` at module load (in marlow_cli or in a
handler that needs the secrets) closes that gap by mirroring the plist's
`EnvironmentVariables` dict into `os.environ` for any key not already
set. The shell wins on conflict — you can still override per-invocation.

Silent no-op on missing or malformed plist.
"""

from __future__ import annotations

import os
import plistlib
from pathlib import Path

PLIST_PATH = Path.home() / "Library" / "LaunchAgents" / "com.marlow.tick.plist"


def import_plist_env() -> None:
    if not PLIST_PATH.exists():
        return
    try:
        with PLIST_PATH.open("rb") as f:
            data = plistlib.load(f)
    except (plistlib.InvalidFileException, OSError):
        return
    env = data.get("EnvironmentVariables", {})
    if not isinstance(env, dict):
        return
    for k, v in env.items():
        if isinstance(v, str) and k not in os.environ:
            os.environ[k] = v
