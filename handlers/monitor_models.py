"""
monitor_models — new-model watch on the providers Alex uses.

Alex kept learning about new model releases from other people's posts. Every
provider the Werewolf game uses exposes a model-list endpoint, and a new model
shows up there the moment it is callable. This handler lists all of them,
diffs against the last acknowledged snapshot, and returns what appeared or
disappeared. Marlow's ops session filters noise (dated snapshots of a known
model, `-latest` aliases, internal test ids) and sends the real releases to the
news Telegram chat.

Keys: the game's provider keys, read live from Firestore
(`/config/freeTierApiKeys`, same read-only path as monitor_keys).

State: projects/research/model_releases/state.json (acknowledged lists) and
pending.json (the latest check, not yet acknowledged). A check never moves the
baseline; `send` or `ack` does, so a tick that dies between check and alert
reports the same models again next time. The first run for a provider seeds
its baseline silently.

CLI:
    python handlers/monitor_models.py check              → JSON: new/removed per provider, errors
    python handlers/monitor_models.py send --stdin       → post message to news chat, then ack
    python handlers/monitor_models.py ack                → accept pending as the new baseline, no message
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
from handlers.monitor_keys import _get, _load_free_tier_keys  # noqa: E402
from tools import notify  # noqa: E402

STATE_DIR = REPO_ROOT / "projects" / "research" / "model_releases"
STATE = STATE_DIR / "state.json"
PENDING = STATE_DIR / "pending.json"
LOG = STATE_DIR / "log.md"
HTTP_TIMEOUT = 20


def _bearer(key: str) -> dict:
    return {"Authorization": f"Bearer {key}"}


# provider → (key name in freeTierApiKeys, url, headers(key), params(key))
PROVIDERS = {
    "OpenAI": ("OPENAI_API_KEY", "https://api.openai.com/v1/models", _bearer, lambda k: {}),
    "Anthropic": ("ANTHROPIC_API_KEY", "https://api.anthropic.com/v1/models",
                  lambda k: {"x-api-key": k, "anthropic-version": "2023-06-01"}, lambda k: {"limit": 1000}),
    "Google": ("GOOGLE_API_KEY", "https://generativelanguage.googleapis.com/v1beta/models",
               lambda k: {}, lambda k: {"key": k, "pageSize": 1000}),
    "Mistral": ("MISTRAL_API_KEY", "https://api.mistral.ai/v1/models", _bearer, lambda k: {}),
    "DeepSeek": ("DEEPSEEK_API_KEY", "https://api.deepseek.com/models", _bearer, lambda k: {}),
    "xAI": ("GROK_API_KEY", "https://api.x.ai/v1/models", _bearer, lambda k: {}),
    "Moonshot": ("MOONSHOT_API_KEY", "https://api.moonshot.ai/v1/models", _bearer, lambda k: {}),
    "Z.AI": ("Z_AI_API_KEY", "https://api.z.ai/api/paas/v4/models", _bearer, lambda k: {}),
    "Sakana": ("FUGU_API_KEY", "https://api.sakana.ai/v1/models", _bearer, lambda k: {}),
    "Qwen": ("QWEN_API_KEY", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/models", _bearer, lambda k: {}),
    "MiniMax": ("MINIMAX_API_KEY", "https://api.minimax.io/v1/models", _bearer, lambda k: {}),
    "Meta": ("META_API_KEY", "https://api.meta.ai/v1/models", _bearer, lambda k: {}),
}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _list_models(name: str, key: str) -> list[str]:
    _, url, headers, params = PROVIDERS[name]
    ids: list[str] = []
    page_params = params(key)
    while True:
        resp = _get(url, headers=headers(key), params=page_params, timeout=HTTP_TIMEOUT)
        resp.raise_for_status()
        body = resp.json()
        items = body.get("data") or body.get("models") or []
        for it in items:
            mid = it.get("id") or it.get("name") or ""
            if mid:
                ids.append(mid.removeprefix("models/"))
        token = body.get("nextPageToken")  # Google pages; the rest return everything
        if not token:
            break
        page_params = {**params(key), "pageToken": token}
    if not ids:
        raise RuntimeError("empty model list")
    return sorted(set(ids))


def _load(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return {}


def check() -> dict:
    try:
        keys = _load_free_tier_keys()
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": f"key load failed: {e}"}
    state = _load(STATE)
    current: dict[str, list[str]] = {}
    new, removed, errors, seeded = {}, {}, {}, []
    for name, (key_name, *_rest) in PROVIDERS.items():
        key = keys.get(key_name)
        if not key:
            errors[name] = f"no {key_name} in freeTierApiKeys"
            continue
        try:
            ids = _list_models(name, key)
        except Exception as e:  # noqa: BLE001
            errors[name] = str(e)[:200]
            continue
        current[name] = ids
        known = state.get(name, {}).get("models")
        if known is None:
            seeded.append(name)
            continue
        added = sorted(set(ids) - set(known))
        gone = sorted(set(known) - set(ids))
        if added:
            new[name] = added
        if gone:
            removed[name] = gone
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    PENDING.write_text(json.dumps({"checked_at": _now(), "models": current}, indent=1))
    return {
        "ok": bool(current),
        "checked_at": _now(),
        "new": new,
        "removed": removed,
        "seeded": seeded,
        "errors": errors,
        "providers_read": len(current),
        "next": "send --stdin (real releases) or ack (nothing worth a message)" if (new or removed or seeded) else "ack",
    }


def ack(message: str | None = None) -> dict:
    pending = _load(PENDING)
    if not pending.get("models"):
        return {"ok": False, "error": "no pending check; run `check` first"}
    state = _load(STATE)
    for name, ids in pending["models"].items():
        state[name] = {"models": ids, "acked_at": _now()}
    STATE.write_text(json.dumps(state, indent=1))
    PENDING.unlink(missing_ok=True)
    if message:
        with open(LOG, "a") as f:
            f.write(f"## {_now()}\n{message.strip()}\n\n")
    return {"ok": True, "providers_acked": len(pending["models"])}


def send(message: str) -> dict:
    if not message.strip():
        return {"ok": False, "error": "empty message"}
    res = notify.send_telegram_message(message.strip(), channel="news")
    if not res.get("ok"):
        return {"ok": False, "error": f"telegram: {res.get('detail')}", "acked": False}
    out = ack(message)
    return {"ok": out.get("ok", False), "msg_id": res.get("message_id"), "acked": out.get("ok", False)}


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    s = sub.add_parser("send")
    s.add_argument("--stdin", action="store_true", required=True)
    sub.add_parser("ack")
    a = ap.parse_args()
    if a.cmd == "check":
        out = check()
    elif a.cmd == "send":
        out = send(sys.stdin.read())
    else:
        out = ack()
    print(json.dumps(out, indent=2, ensure_ascii=False))
    sys.exit(0 if out.get("ok") else 1)


if __name__ == "__main__":
    main()
