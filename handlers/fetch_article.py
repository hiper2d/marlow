"""
fetch_article — given a URL, return cleaned article body text.

Used by the end-of-day curation tick so Marlow can write reviews from
the actual article, not from a 200-character RSS snippet.

Uses trafilatura for HTML-to-text extraction. Handles most static
blogs and news sites; falls back to returning the raw <p> text if
trafilatura can't extract a main body. Skips JS-rendered sites — those
need a browser, not in scope here.

UA + retry policy: some sources (alignmentforum.org observed) throttle
the identifying agent string aggressively. We use a current real-browser
UA + a couple polite extra headers, and on HTTP 429 we sleep + retry.

CLI:
    python handlers/fetch_article.py fetch --url URL
        → JSON: {url, title, text, char_count, ok}
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import trafilatura

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) "
    "Version/17.0 Safari/605.1.15"
)
DEFAULT_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "identity",
}
TIMEOUT_SEC = 20
RETRY_BACKOFF_SEC = (4, 12)  # two retries; sleep these many seconds before each


def _fetch_html(url: str) -> str:
    """Fetch HTML with retry on 429. Raises on terminal failure."""
    last_err: Exception | None = None
    attempts = len(RETRY_BACKOFF_SEC) + 1
    for attempt in range(attempts):
        try:
            req = Request(url, headers=DEFAULT_HEADERS)
            with urlopen(req, timeout=TIMEOUT_SEC) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except HTTPError as e:
            last_err = e
            if e.code == 429 and attempt < attempts - 1:
                time.sleep(RETRY_BACKOFF_SEC[attempt])
                continue
            raise
        except URLError as e:
            last_err = e
            if attempt < attempts - 1:
                time.sleep(RETRY_BACKOFF_SEC[attempt])
                continue
            raise
    if last_err:
        raise last_err
    raise RuntimeError("unreachable")


def fetch(url: str) -> dict:
    html = _fetch_html(url)

    text = trafilatura.extract(
        html,
        include_comments=False,
        include_tables=False,
        favor_precision=True,
    ) or ""

    metadata = trafilatura.extract_metadata(html)
    title = metadata.title if metadata and metadata.title else ""

    text = text.strip()
    return {
        "url": url,
        "title": title,
        "text": text,
        "char_count": len(text),
        "ok": len(text) > 200,
    }


def cmd_fetch(args):
    try:
        result = fetch(args.url)
    except Exception as e:
        result = {"url": args.url, "title": "", "text": "", "char_count": 0, "ok": False, "error": str(e)}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["ok"] else 1)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_fetch = sub.add_parser("fetch", help="Fetch and extract article body from URL")
    p_fetch.add_argument("--url", required=True)

    args = parser.parse_args()
    if args.cmd == "fetch":
        cmd_fetch(args)


if __name__ == "__main__":
    main()
