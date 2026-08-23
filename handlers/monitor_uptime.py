"""
monitor_uptime - is the site actually serving? Both game sites, one handler.

The gap this fills: nothing in werewolf-ops ever fetched a page. monitor_cloudflare
reads zone status, DNS records, SSL state and Pages deploy results; monitor_health
reads game docs; monitor_betterstack reads logs. Every one of those can look
perfectly healthy while the site returns a 500 or a blank shell to a visitor - a
green deploy of a broken build is exactly that shape. So this does the dumb thing
none of the others do: GET the page like a stranger would.

Covers BOTH live sites, because as of 2026-08-22 they are one operation sharing
one set of provider keys:
  - aiwerewolf.net   (Cloudflare)
  - pokerwithai.net  (Vercel)

Three failures, deliberately distinguished:
  - unreachable / non-200        -> site_down      (urgent)
  - 200 but the content marker is gone -> content_missing (digest, urgent on repeat)
  - 200, correct, but slow       -> site_slow      (digest)

The middle one is the point. A 200 with an empty body is the failure a status-code
check calls healthy, and it is the most likely way a bad deploy presents. The
marker is a string that only renders when the app actually booted.

Transient-tolerant: every check retries once before it counts, same discipline as
monitor_keys._get - one dropped TCP connection on an unattended cron is not an
outage. A repeated content_missing escalates to urgent at REPEAT_URGENT_RUNS,
because three identical digests read the same as one (the lesson from the Mistral
parse_failed that sat unnoticed for three days, 2026-07-26).

No credentials. Nothing to provision, nothing to rotate, nothing to expire.

CLI:
    python handlers/monitor_uptime.py report   -> check every site + persist, JSON
    python handlers/monitor_uptime.py show      -> last check, human-readable
    python handlers/monitor_uptime.py digest    -> digest block (empty when all well)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from driver.budget_state import STATE_DIR  # noqa: E402

UPTIME_LATEST = STATE_DIR / "uptime_latest.json"
UPTIME_HISTORY = STATE_DIR / "uptime_history.jsonl"

# A marker is a string present only when the app actually rendered. Keep it to
# something a redesign is unlikely to touch: the <title> survives restyling, and
# a blank shell or an error page will not contain it.
SITES = [
    {"name": "werewolf", "url": "https://aiwerewolf.net", "marker": "Werewolf AI", "host": "Cloudflare"},
    {"name": "poker", "url": "https://pokerwithai.net", "marker": "Poker with AI", "host": "Vercel"},
]

HTTP_TIMEOUT = 25
# Generous on purpose: Vercel cold starts measured 1.6s on 2026-08-22 against
# Cloudflare's 0.24s. This threshold is for "something is wrong", not for
# performance tuning - tightening it would just teach us to ignore the digest.
SLOW_S = 10.0
REPEAT_URGENT_RUNS = 3


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _checked_at(now: datetime) -> str:
    return now.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _fetch(url: str) -> tuple[int | None, float, str, str | None]:
    """GET url, retrying once on a transport error. Returns
    (status, elapsed_s, body, error). A non-200 is NOT an error here - it's a
    status the caller judges; `error` means we never got a response at all."""
    last_err = None
    for attempt in range(2):
        started = time.monotonic()
        try:
            r = requests.get(
                url, timeout=HTTP_TIMEOUT, allow_redirects=True,
                headers={"User-Agent": "marlow-uptime/1.0 (+https://pokerwithai.net)"},
            )
            return r.status_code, time.monotonic() - started, r.text, None
        except requests.RequestException as e:
            last_err = f"{type(e).__name__}: {str(e)[:120]}"
            if attempt == 0:
                time.sleep(3)
    return None, 0.0, "", last_err


def _check(site: dict) -> dict:
    status, elapsed, body, err = _fetch(site["url"])
    row = {
        "site": site["name"], "url": site["url"], "host": site.get("host"),
        "status": status, "elapsed_s": round(elapsed, 3),
    }
    if err is not None:
        return {**row, "ok": False, "kind": "unreachable", "error": err}
    if status != 200:
        return {**row, "ok": False, "kind": "bad_status", "error": f"HTTP {status}"}
    if site["marker"] not in body:
        # Served something, but not the app. Report the size so a blank shell
        # (a few hundred bytes) is distinguishable from a rendered wrong page.
        return {**row, "ok": False, "kind": "content_missing", "bytes": len(body),
                "error": f"HTTP 200 but marker {site['marker']!r} absent ({len(body)} bytes)"}
    return {**row, "ok": True, "bytes": len(body)}


def _streak(site: str, kind: str) -> int:
    """Consecutive PRIOR runs where this site failed this same way. Stops at the
    first run where it was ok, absent, or broke differently - a content_missing
    run should not be extended by an unrelated timeout."""
    try:
        lines = UPTIME_HISTORY.read_text().splitlines()
    except OSError:
        return 0
    n = 0
    for ln in reversed(lines):
        try:
            row = next((s for s in json.loads(ln).get("sites", []) if s.get("site") == site), None)
        except json.JSONDecodeError:
            break
        if not row or row.get("ok") or row.get("kind") != kind:
            break
        n += 1
    return n


def _derive_issues(results: list[dict]) -> list[dict]:
    issues = []
    for r in results:
        site = r["site"]
        if r.get("ok"):
            if r.get("elapsed_s", 0) > SLOW_S:
                issues.append({"kind": "site_slow", "severity": "digest", "target": site,
                               "detail": f"{site} answered in {r['elapsed_s']:.1f}s (> {SLOW_S:g}s). Up, but degraded."})
            continue
        kind = r.get("kind")
        if kind in ("unreachable", "bad_status"):
            issues.append({"kind": "site_down", "severity": "urgent", "target": site,
                           "detail": f"{site} ({r['url']}) is DOWN: {r.get('error')}. Host: {r.get('host')}."})
        else:
            runs = _streak(site, kind) + 1
            repeat = runs >= REPEAT_URGENT_RUNS
            issues.append({
                "kind": "content_missing",
                "severity": "urgent" if repeat else "digest",
                "target": site, "failing_runs": runs,
                "detail": f"{site} served {r.get('error')}."
                          + (f" {runs} runs running - this is a broken deploy, not a blip."
                             if repeat else " Likely a bad deploy or a changed page title."),
            })
    return issues


def _compact(report: dict) -> dict:
    return {
        "checked_at": report.get("checked_at"),
        "any_urgent": report.get("any_urgent"),
        "sites": [{"site": s.get("site"), "ok": s.get("ok"),
                   "kind": s.get("kind") if not s.get("ok") else None,
                   "status": s.get("status"), "elapsed_s": s.get("elapsed_s")}
                  for s in report.get("sites", [])],
        "issues": [f"{i['severity']}:{i['target']}" for i in report.get("issues", [])],
    }


def _save(report: dict) -> None:
    """Best-effort - a disk problem must never take down the check itself."""
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        tmp = UPTIME_LATEST.with_suffix(".json.tmp")
        with tmp.open("w") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        tmp.replace(UPTIME_LATEST)
        with UPTIME_HISTORY.open("a") as f:
            f.write(json.dumps(_compact(report), ensure_ascii=False) + "\n")
    except OSError:
        pass


def report() -> dict:
    now = _now_utc()
    results = [_check(s) for s in SITES]      # streaks read history before _save
    issues = _derive_issues(results)
    result = {
        "ok": True,
        "checked_at": _checked_at(now),
        "sites": results,
        "issues": issues,
        "any_urgent": any(i["severity"] == "urgent" for i in issues),
    }
    _save(result)
    return result


def render(rep: dict) -> str:
    out = [f"Site uptime - {rep.get('checked_at', '?')}", ""]
    for s in rep.get("sites", []):
        if s.get("ok"):
            out.append(f"  {s['site']:10} UP    {s['elapsed_s']:>6.2f}s  {s.get('bytes', 0)} bytes  ({s.get('host')})")
        else:
            out.append(f"  {s['site']:10} DOWN  {s.get('kind')}: {s.get('error')}")
    out.append("")
    if rep.get("issues"):
        out.append("ISSUES")
        for i in rep["issues"]:
            out.append(f"  [{'!' if i['severity'] == 'urgent' else '~'}] {i['detail']}")
    else:
        out.append("All sites up.")
    return "\n".join(out)


def render_digest(rep: dict) -> str | None:
    """None when everything is fine, so a healthy check adds no digest line."""
    issues = rep.get("issues", [])
    if not issues:
        return None
    date = (rep.get("checked_at") or "")[:10]
    head = f"Site uptime - {date}: {len(issues)} issue(s)" + (" (urgent)" if rep.get("any_urgent") else "")
    return "\n".join([head] + [f"  · {i['detail']}" for i in issues])


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("report", help="Check every site + persist (JSON)")
    sub.add_parser("show", help="Render the last check, human-readable")
    sub.add_parser("digest", help="Digest block from the last check (empty when all well)")
    args = ap.parse_args()
    if args.cmd == "report":
        res = report()
        print(json.dumps(res, indent=2, ensure_ascii=False))
        sys.exit(0 if res.get("ok") else 1)
    elif args.cmd == "show":
        try:
            with UPTIME_LATEST.open() as f:
                print(render(json.load(f)))
        except (OSError, json.JSONDecodeError):
            print("No check yet - run `report` first.")
    elif args.cmd == "digest":
        try:
            with UPTIME_LATEST.open() as f:
                d = render_digest(json.load(f))
            print(d if d else "")
        except (OSError, json.JSONDecodeError):
            print("")


if __name__ == "__main__":
    main()
