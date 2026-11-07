"""
sources - Marlow's research source list, and the only code that changes it.

The list (projects/research/feeds/sources.yaml) is hers since 2026-11-07: she
adds and drops sources as she finds what's worth reading. She decides; this
tool checks. The explore tick (web, no shell) can't run this, so it writes
proposals to projects/research/feeds/proposals.yaml, and tick.sh runs
`apply` once a day, out of session, before the writer loop picks a task.

Every check here is mechanical, not editorial:
  - http(s) only, and the host must resolve to PUBLIC addresses. A proposal
    pointing at localhost / a LAN address (e.g. the Chrome debug port) is
    refused: a page read on the web must not be able to aim a shell-enabled
    tick at the machine it runs on.
  - the feed has to actually parse: RSS returns >=1 entry; a sitemap returns
    >=1 URL under the given prefix.
  - at most MAX_SOURCES, at least MIN_SOURCES, no duplicate url+prefix.
Every outcome (applied or refused, with the reason) is appended to
projects/research/feeds/sources-log.md, which she reads on her next explore.

CLI:
    sources.py list
    sources.py add --name N --kind rss|sitemap --url U [--prefix P] --why W
    sources.py remove --id ID --why W
    sources.py apply          # process proposals.yaml, then clear it
"""
from __future__ import annotations

import argparse
import ipaddress
import json
import re
import socket
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))
FEEDS = REPO_ROOT / "projects" / "research" / "feeds"
SOURCES = FEEDS / "sources.yaml"
PROPOSALS = FEEDS / "proposals.yaml"
LOG = FEEDS / "sources-log.md"

MAX_SOURCES = 15   # each source costs one writer tick a day
MIN_SOURCES = 3
KINDS = ("rss", "sitemap")

PROPOSALS_TEMPLATE = """# Source changes Marlow wants. Written by the explore tick, applied (or refused,
# with the reason) once a day by tools/sources.py; results land in sources-log.md.
# Each item:
#   - action: add            # or: remove
#     name: "Site name"      # add only
#     kind: rss              # add only: rss | sitemap
#     url: "https://..."     # add only: the feed URL, or the sitemap.xml
#     prefix: "https://..."  # add + sitemap only: the section to watch
#     id: some_id            # remove only
#     why: "one line"        # always
proposals: []
"""


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def _load() -> tuple[str, list[dict]]:
    text = SOURCES.read_text()
    header = "".join(l for l in text.splitlines(keepends=True) if l.startswith("#"))
    data = yaml.safe_load(text) or {}
    return header, list(data.get("sources") or [])


def _save(header: str, sources: list[dict]) -> None:
    SOURCES.write_text(header + yaml.safe_dump({"sources": sources}, sort_keys=False,
                                                allow_unicode=True, width=200))


def _log(line: str) -> None:
    if not LOG.exists():
        LOG.write_text("# Source list changes\n\nEvery add/remove Marlow proposed, and what the check said. Newest at the bottom.\n\n")
    with LOG.open("a") as f:
        f.write(f"- {_now()} {line}\n")


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")[:40] or "source"


def _public_url(url: str) -> str | None:
    """None if OK, else the reason it's refused."""
    u = urlparse(url or "")
    if u.scheme not in ("http", "https") or not u.hostname:
        return "not an http(s) URL"
    try:
        infos = socket.getaddrinfo(u.hostname, u.port or (443 if u.scheme == "https" else 80))
    except socket.gaierror:
        return f"host {u.hostname} does not resolve"
    for info in infos:
        ip = ipaddress.ip_address(info[4][0].split("%")[0])
        if not ip.is_global:
            return f"host {u.hostname} resolves to a non-public address ({ip})"
    return None


def _check_feed(kind: str, url: str, prefix: str | None) -> str | None:
    """None if the feed parses with >=1 item, else the reason."""
    try:
        if kind == "rss":
            import rss_reader
            entries = rss_reader.fetch(url, limit=5, attempts=1)
        else:
            if not prefix:
                return "a sitemap source needs a prefix (the section URL to watch)"
            import sitemap_reader
            entries = sitemap_reader.fetch(url, prefix=prefix, limit=5)
    except Exception as e:  # network, parse, anything
        return f"fetch failed: {type(e).__name__}: {str(e)[:120]}"
    if not entries:
        return "parsed, but returned no entries" + (" under that prefix" if prefix else "")
    return None


def add(name: str, kind: str, url: str, prefix: str | None, why: str) -> dict:
    header, sources = _load()
    if kind not in KINDS:
        return {"ok": False, "reason": f"kind must be one of {KINDS}"}
    if not why or not why.strip():
        return {"ok": False, "reason": "a one-line why is required"}
    if len(sources) >= MAX_SOURCES:
        return {"ok": False, "reason": f"already at the cap of {MAX_SOURCES} sources; drop one first"}
    for u in (url, prefix):
        if u:
            bad = _public_url(u)
            if bad:
                return {"ok": False, "reason": bad}
    if any(s.get("url") == url and s.get("prefix") == prefix for s in sources):
        return {"ok": False, "reason": "already in the list"}
    bad = _check_feed(kind, url, prefix)
    if bad:
        return {"ok": False, "reason": bad}
    sid, ids = _slug(name), {s["id"] for s in sources}
    base, n = sid, 2
    while sid in ids:
        sid, n = f"{base}_{n}", n + 1
    entry = {"id": sid, "name": name, "kind": kind, "url": url}
    if prefix:
        entry["prefix"] = prefix
    entry["added"] = f"{_now()[:10]} (Marlow): {why.strip()}"
    sources.append(entry)
    _save(header, sources)
    return {"ok": True, "id": sid}


def remove(sid: str, why: str) -> dict:
    header, sources = _load()
    if not why or not why.strip():
        return {"ok": False, "reason": "a one-line why is required"}
    keep = [s for s in sources if s.get("id") != sid]
    if len(keep) == len(sources):
        return {"ok": False, "reason": f"no source with id {sid}"}
    if len(keep) < MIN_SOURCES:
        return {"ok": False, "reason": f"would leave fewer than {MIN_SOURCES} sources"}
    _save(header, keep)
    return {"ok": True, "id": sid}


def apply() -> dict:
    if not PROPOSALS.exists():
        PROPOSALS.write_text(PROPOSALS_TEMPLATE)
        return {"applied": 0, "refused": 0}
    try:
        items = (yaml.safe_load(PROPOSALS.read_text()) or {}).get("proposals") or []
    except yaml.YAMLError as e:
        _log(f"REFUSED all proposals: proposals.yaml does not parse ({str(e)[:100]})")
        PROPOSALS.write_text(PROPOSALS_TEMPLATE)
        return {"applied": 0, "refused": 1, "error": "yaml"}
    applied = refused = 0
    for it in items[:10]:   # a flood of proposals is itself a signal; cap per day
        if not isinstance(it, dict):
            continue
        act, why = it.get("action"), str(it.get("why") or "")
        if act == "add":
            r = add(str(it.get("name") or ""), str(it.get("kind") or ""), str(it.get("url") or ""),
                    (str(it["prefix"]) if it.get("prefix") else None), why)
            what = f"add '{it.get('name')}' ({it.get('kind')}) {it.get('url')}" + (f" prefix {it.get('prefix')}" if it.get("prefix") else "")
        elif act == "remove":
            r = remove(str(it.get("id") or ""), why)
            what = f"remove '{it.get('id')}'"
        else:
            r, what = {"ok": False, "reason": "action must be add or remove"}, f"'{act}'"
        if r["ok"]:
            applied += 1
            _log(f"APPLIED {what} - why: {why}")
        else:
            refused += 1
            _log(f"REFUSED {what} - {r['reason']}")
    if len(items) > 10:
        _log(f"REFUSED {len(items) - 10} more proposals over the 10-a-day cap")
    PROPOSALS.write_text(PROPOSALS_TEMPLATE)
    return {"applied": applied, "refused": refused}


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    a = sub.add_parser("add")
    a.add_argument("--name", required=True); a.add_argument("--kind", required=True, choices=KINDS)
    a.add_argument("--url", required=True); a.add_argument("--prefix"); a.add_argument("--why", required=True)
    r = sub.add_parser("remove")
    r.add_argument("--id", required=True); r.add_argument("--why", required=True)
    sub.add_parser("apply")
    args = ap.parse_args()
    if args.cmd == "list":
        print(json.dumps({"count": len(_load()[1]), "max": MAX_SOURCES, "sources": _load()[1]}, indent=2))
    elif args.cmd == "add":
        res = add(args.name, args.kind, args.url, args.prefix, args.why)
        _log(("APPLIED" if res["ok"] else "REFUSED") + f" add '{args.name}' {args.url}" + ("" if res["ok"] else f" - {res['reason']}") + f" - why: {args.why}")
        print(json.dumps(res))
    elif args.cmd == "remove":
        res = remove(args.id, args.why)
        _log(("APPLIED" if res["ok"] else "REFUSED") + f" remove '{args.id}'" + ("" if res["ok"] else f" - {res['reason']}") + f" - why: {args.why}")
        print(json.dumps(res))
    else:
        print(json.dumps(apply()))


if __name__ == "__main__":
    main()
