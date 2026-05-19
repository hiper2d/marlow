"""
monitor_cloudflare — daily health check for Cloudflare-hosted assets.

Auto-discovers everything reachable through the `C_F` API token (scoped
read-only via the dashboard). Returns deterministic JSON snapshots;
Marlow's session orchestrates the snapshot into a report + alert.

Targets covered:
  - Cloudflare Pages projects (Marlow's blog, etc.) — latest deployment
    status, age of last success.
  - Cloudflare Zones (werewolf domain, etc.) — zone status, DNS records,
    SSL/TLS certificate state.

Reads `C_F` from `os.environ`. Fails clean if missing.

CLI:
    python handlers/monitor_cloudflare.py check-pages
        → JSON: all Pages projects + latest deployment per project.
    python handlers/monitor_cloudflare.py check-zones
        → JSON: all zones + their status + DNS records + SSL certs.
    python handlers/monitor_cloudflare.py report
        → orchestrator: runs both, returns combined JSON with derived
          `issues` array (alert thresholds applied).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

# Mirror plist env so standalone `uv run python handlers/monitor_cloudflare.py`
# sees the same secrets that a launchd-fired tick sees.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from driver.env_loader import import_plist_env  # noqa: E402
import_plist_env()

API = "https://api.cloudflare.com/client/v4"

# Alert thresholds (default — tune via editorial feedback later).
PAGES_STALE_HOURS = 48          # alert if last success older AND no in-progress build
SSL_EXPIRING_DAYS = 14          # alert if any cert expires within this window


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _parse_iso(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def _token() -> str | None:
    return os.environ.get("C_F")


def _request(path: str, params: dict | None = None) -> dict:
    """GET against Cloudflare API. Returns the `result` field on success."""
    token = _token()
    if not token:
        raise RuntimeError("C_F not in environment")
    resp = requests.get(
        f"{API}{path}",
        headers={"Authorization": f"Bearer {token}"},
        params=params or {},
        timeout=30,
    )
    resp.raise_for_status()
    payload = resp.json()
    if not payload.get("success"):
        errors = payload.get("errors", [])
        raise RuntimeError(f"Cloudflare API errors: {errors}")
    return payload


def _list_accounts() -> list[dict]:
    return _request("/accounts", {"per_page": 50})["result"]


def _list_pages_projects(account_id: str) -> list[dict]:
    return _request(f"/accounts/{account_id}/pages/projects", {"per_page": 50})["result"]


def _latest_deployment(account_id: str, project_name: str) -> dict | None:
    res = _request(
        f"/accounts/{account_id}/pages/projects/{project_name}/deployments",
        {"per_page": 1},
    )["result"]
    return res[0] if res else None


def _list_zones() -> list[dict]:
    return _request("/zones", {"per_page": 50})["result"]


def _list_dns_records(zone_id: str) -> list[dict]:
    return _request(f"/zones/{zone_id}/dns_records", {"per_page": 100})["result"]


def _list_ssl_packs(zone_id: str) -> list[dict]:
    try:
        return _request(f"/zones/{zone_id}/ssl/certificate_packs", {"per_page": 50})["result"]
    except RuntimeError:
        # Some zones may not have SSL packs API enabled; skip silently.
        return []


def check_pages() -> dict:
    if not _token():
        return {"ok": False, "error": "C_F not in environment"}
    out_projects = []
    try:
        accounts = _list_accounts()
        for acct in accounts:
            account_id = acct["id"]
            account_name = acct.get("name", account_id)
            try:
                projects = _list_pages_projects(account_id)
            except RuntimeError:
                # Account may not have Pages: Read permission.
                continue
            for proj in projects:
                latest = _latest_deployment(account_id, proj["name"])
                latest_summary = None
                if latest:
                    stage = latest.get("latest_stage", {}) or {}
                    latest_summary = {
                        "id": latest.get("id"),
                        "stage": stage.get("name"),
                        "status": stage.get("status"),
                        "created_on": latest.get("created_on"),
                        "modified_on": latest.get("modified_on"),
                        "environment": latest.get("environment"),
                        "url": latest.get("url"),
                    }
                out_projects.append({
                    "account": account_name,
                    "account_id": account_id,
                    "project": proj["name"],
                    "subdomain": proj.get("subdomain"),
                    "domains": proj.get("domains", []),
                    "latest_deployment": latest_summary,
                })
    except (requests.RequestException, RuntimeError) as e:
        return {"ok": False, "error": str(e), "partial": out_projects}
    return {"ok": True, "projects": out_projects, "count": len(out_projects)}


def check_zones() -> dict:
    if not _token():
        return {"ok": False, "error": "C_F not in environment"}
    out_zones = []
    try:
        zones = _list_zones()
        for zone in zones:
            zone_id = zone["id"]
            records = _list_dns_records(zone_id)
            ssl_packs = _list_ssl_packs(zone_id)
            ssl_summary = []
            for pack in ssl_packs:
                ssl_summary.append({
                    "id": pack.get("id"),
                    "status": pack.get("status"),
                    "type": pack.get("type"),
                    "certificates": [
                        {
                            "expires_on": c.get("expires_on"),
                            "status": c.get("status"),
                        }
                        for c in (pack.get("certificates") or [])
                    ],
                })
            record_summary = [
                {"type": r.get("type"), "name": r.get("name"), "proxied": r.get("proxied")}
                for r in records
            ]
            out_zones.append({
                "zone_id": zone_id,
                "domain": zone.get("name"),
                "status": zone.get("status"),
                "name_servers": zone.get("name_servers", []),
                "original_name_servers": zone.get("original_name_servers", []),
                "dns_records": record_summary,
                "dns_count": len(record_summary),
                "ssl_packs": ssl_summary,
            })
    except (requests.RequestException, RuntimeError) as e:
        return {"ok": False, "error": str(e), "partial": out_zones}
    return {"ok": True, "zones": out_zones, "count": len(out_zones)}


def _derive_issues(pages: dict, zones: dict) -> list[dict]:
    issues: list[dict] = []
    now = _now_utc()

    # Pages issues.
    for proj in pages.get("projects", []):
        latest = proj.get("latest_deployment") or {}
        stage = latest.get("stage")
        status = latest.get("status")
        if status == "failure":
            issues.append({
                "severity": "urgent",
                "kind": "pages_deploy_failed",
                "target": proj["project"],
                "detail": f"latest deployment failed at stage `{stage}`",
            })
            continue
        # Stale-success check: only if the latest is success and old, and
        # there's no in-progress build (we'd see a non-success status if so).
        if status == "success":
            modified = _parse_iso(latest.get("modified_on"))
            if modified:
                age_hours = (now - modified).total_seconds() / 3600
                if age_hours > PAGES_STALE_HOURS:
                    issues.append({
                        "severity": "digest",  # not urgent; just informational
                        "kind": "pages_deploy_stale",
                        "target": proj["project"],
                        "detail": f"last successful deploy {age_hours:.1f}h ago (threshold {PAGES_STALE_HOURS}h)",
                    })

    # Zone issues.
    for zone in zones.get("zones", []):
        if zone.get("status") != "active":
            issues.append({
                "severity": "urgent",
                "kind": "zone_not_active",
                "target": zone.get("domain"),
                "detail": f"zone status is `{zone.get('status')}`, expected `active`",
            })
        for pack in zone.get("ssl_packs", []):
            for cert in pack.get("certificates", []):
                expires = _parse_iso(cert.get("expires_on"))
                if not expires:
                    continue
                days = (expires - now).total_seconds() / 86400
                if days < SSL_EXPIRING_DAYS:
                    issues.append({
                        "severity": "urgent",
                        "kind": "ssl_expiring_soon",
                        "target": zone.get("domain"),
                        "detail": f"cert expires in {days:.1f} days ({cert.get('expires_on')})",
                    })

    return issues


def report() -> dict:
    pages = check_pages()
    zones = check_zones()
    issues = []
    if pages.get("ok") and zones.get("ok"):
        issues = _derive_issues(pages, zones)
    return {
        "ok": pages.get("ok") and zones.get("ok"),
        "checked_at": _now_utc().replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "pages": pages,
        "zones": zones,
        "issues": issues,
        "any_urgent": any(i["severity"] == "urgent" for i in issues),
    }


def cmd_check_pages(args):
    result = check_pages()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def cmd_check_zones(args):
    result = check_zones()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def cmd_report(args):
    result = report()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check-pages", help="All Pages projects + latest deployment per project")
    sub.add_parser("check-zones", help="All zones + status + DNS records + SSL packs")
    sub.add_parser("report", help="Combined snapshot + derived issues per alert thresholds")
    args = parser.parse_args()
    if args.cmd == "check-pages":
        cmd_check_pages(args)
    elif args.cmd == "check-zones":
        cmd_check_zones(args)
    elif args.cmd == "report":
        cmd_report(args)


if __name__ == "__main__":
    main()
