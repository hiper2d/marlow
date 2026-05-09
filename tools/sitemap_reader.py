"""
Marlow sitemap reader.

Wraps fetching of XML sitemaps. Handles both flat <urlset> sitemaps and
<sitemapindex> documents that point at multiple sub-sitemaps (recurses
one level — that's all the sitemap spec allows). Returns entries with
the same shape as rss_reader.fetch() so handlers can treat both sources
the same way.

Optional prefix filter isolates a section of a site (e.g. only /news/
URLs under anthropic.com), and an optional limit caps results after
sorting by lastmod desc.

CLI for manual testing:
    python tools/sitemap_reader.py <sitemap_url> [--prefix URL_PREFIX] [--limit N]
"""

from __future__ import annotations

import argparse
import json
import sys
from xml.etree import ElementTree as ET

import requests

USER_AGENT = "Mozilla/5.0 (compatible; Marlow/0.1; +https://github.com/hiper2d/marlow)"
SM_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
HTTP_TIMEOUT = 15


def _slug_to_title(url: str) -> str:
    slug = url.rstrip("/").rsplit("/", 1)[-1]
    return slug.replace("-", " ").replace("_", " ").strip().capitalize()


def _fetch_xml(url: str) -> ET.Element:
    r = requests.get(url, timeout=HTTP_TIMEOUT, headers={"User-Agent": USER_AGENT})
    r.raise_for_status()
    return ET.fromstring(r.content)


def _strip_ns(tag: str) -> str:
    """Strip XML namespace prefix from a tag name."""
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def _parse_urlset(root: ET.Element, prefix: str | None) -> list[dict]:
    entries = []
    url_elems = root.findall("sm:url", SM_NS)
    if not url_elems:
        url_elems = root.findall("url")
    for url_elem in url_elems:
        loc_elem = url_elem.find("sm:loc", SM_NS)
        if loc_elem is None:
            loc_elem = url_elem.find("loc")
        if loc_elem is None or not loc_elem.text:
            continue
        loc = loc_elem.text.strip()
        if prefix and not loc.startswith(prefix):
            continue
        lastmod_elem = url_elem.find("sm:lastmod", SM_NS)
        if lastmod_elem is None:
            lastmod_elem = url_elem.find("lastmod")
        published = lastmod_elem.text.strip() if (lastmod_elem is not None and lastmod_elem.text) else None
        entries.append(
            {
                "id": loc,
                "title": _slug_to_title(loc),
                "link": loc,
                "published": published,
                "summary": "",  # sitemaps don't carry summaries; handlers can enrich if they want
            }
        )
    return entries


def fetch(url: str, prefix: str | None = None, limit: int | None = None) -> list[dict]:
    """Fetch a sitemap, recurse into a sitemapindex if needed, return entries.

    Sorted newest-first by `published` (lastmod). Entries with no lastmod
    sort last.
    """
    root = _fetch_xml(url)
    tag = _strip_ns(root.tag)

    if tag == "sitemapindex":
        # Recursively fetch each sub-sitemap and merge.
        entries = []
        sitemaps = root.findall("sm:sitemap", SM_NS)
        if not sitemaps:
            sitemaps = root.findall("sitemap")
        for sm in sitemaps:
            loc_elem = sm.find("sm:loc", SM_NS)
            if loc_elem is None:
                loc_elem = sm.find("loc")
            if loc_elem is None or not loc_elem.text:
                continue
            try:
                entries.extend(fetch(loc_elem.text.strip(), prefix=prefix))
            except (requests.RequestException, ET.ParseError):
                # One bad sub-sitemap shouldn't kill the whole scan.
                continue
    elif tag == "urlset":
        entries = _parse_urlset(root, prefix)
    else:
        raise RuntimeError(f"unexpected sitemap root tag: {tag!r}")

    # Sort newest first (None published → end).
    entries.sort(key=lambda e: e.get("published") or "", reverse=True)
    return entries[:limit] if limit else entries


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--prefix", default=None, help="Only return URLs starting with this prefix")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    try:
        entries = fetch(args.url, prefix=args.prefix, limit=args.limit)
    except (requests.RequestException, ET.ParseError, RuntimeError) as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(entries, indent=2))


if __name__ == "__main__":
    main()
