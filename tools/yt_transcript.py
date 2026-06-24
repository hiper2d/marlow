"""
yt_transcript — fetch a YouTube video's caption transcript as plain text.

The YouTube per-channel RSS feed gives Marlow only title + link +
description, so video scans had thin signal. This tool pulls the video's
own caption track (manual or auto-generated) via youtube-transcript-api —
no audio download, no Whisper, no API key — so the scan tick can judge a
video on what it actually says, not just its title.

Transcripts are immutable, so we cache them to disk under
projects/research/threads/_yt_transcripts/<video_id>.json. A re-scan or a
re-run of the same tick is then free and offline.

Accepts a bare id, a watch/youtu.be URL, or the RSS "yt:video:<ID>" form.

Importable:
    from tools.yt_transcript import fetch_transcript
    result = fetch_transcript("gC76aeibdFA")   # {video_id, text, ...}

CLI:
    uv run python tools/yt_transcript.py <video_id_or_url>
    uv run python tools/yt_transcript.py <id> --lang en --max-chars 12000
        → JSON: {video_id, text, char_count, language, source, cached, ok}
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

REPO_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = REPO_ROOT / "projects" / "research" / "threads" / "_yt_transcripts"

DEFAULT_LANGS = ["en", "en-US", "en-GB"]


def extract_video_id(value: str) -> str:
    """Pull an 11-char YouTube id from a bare id, a URL, or yt:video:<ID>."""
    value = value.strip()
    # RSS entry id form: "yt:video:gC76aeibdFA"
    if value.startswith("yt:video:"):
        value = value.rsplit(":", 1)[-1]
    # Full URLs
    if "://" in value:
        parsed = urlparse(value)
        if parsed.hostname and "youtu.be" in parsed.hostname:
            cand = parsed.path.lstrip("/").split("/")[0]
            if cand:
                return cand
        qs = parse_qs(parsed.query)
        if "v" in qs and qs["v"]:
            return qs["v"][0]
        # /embed/<id> or /shorts/<id>
        m = re.search(r"/(?:embed|shorts|v)/([A-Za-z0-9_-]{11})", parsed.path)
        if m:
            return m.group(1)
    # Bare id (allow the canonical 11-char form, but don't be strict)
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", value):
        return value
    m = re.search(r"([A-Za-z0-9_-]{11})", value)
    if m:
        return m.group(1)
    raise ValueError(f"could not extract a video id from: {value!r}")


def _fetch_segments(video_id: str, languages: list[str]) -> tuple[list[dict], str]:
    """Return (segments, language_code). Adapts to the API version split.

    youtube-transcript-api 0.6.x exposes the classmethod get_transcript;
    1.x moved to an instance .fetch()/.list() API. Support both, and fall
    back to any available transcript (translated to English if possible)
    when the preferred languages aren't present.
    """
    from youtube_transcript_api import YouTubeTranscriptApi

    # --- 0.6.x classmethod API ---------------------------------------
    if hasattr(YouTubeTranscriptApi, "get_transcript"):
        try:
            segs = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
            return segs, languages[0]
        except Exception:
            pass  # fall through to the list-and-pick path below
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        chosen = None
        for t in transcripts:  # prefer a manually created track
            if not t.is_generated:
                chosen = t
                break
        if chosen is None:
            chosen = next(iter(transcripts))
        lang = chosen.language_code
        if not lang.startswith("en") and chosen.is_translatable:
            try:
                chosen = chosen.translate("en")
                lang = "en"
            except Exception:
                pass
        return chosen.fetch(), lang

    # --- 1.x instance API --------------------------------------------
    api = YouTubeTranscriptApi()
    try:
        fetched = api.fetch(video_id, languages=languages)
        segs = [{"text": s.text, "start": s.start, "duration": s.duration} for s in fetched]
        return segs, getattr(fetched, "language_code", languages[0])
    except Exception:
        pass
    listing = api.list(video_id)
    chosen = None
    for t in listing:
        if not t.is_generated:
            chosen = t
            break
    if chosen is None:
        chosen = next(iter(listing))
    lang = chosen.language_code
    if not lang.startswith("en") and chosen.is_translatable:
        try:
            chosen = chosen.translate("en")
            lang = "en"
        except Exception:
            pass
    fetched = chosen.fetch()
    segs = [{"text": s.text, "start": s.start, "duration": s.duration} for s in fetched]
    return segs, lang


def _segments_to_text(segments: list[dict]) -> str:
    parts = []
    for s in segments:
        txt = (s.get("text") if isinstance(s, dict) else getattr(s, "text", "")) or ""
        txt = txt.replace("\n", " ").strip()
        if txt and txt != "[Music]":
            parts.append(txt)
    return " ".join(parts).strip()


def fetch_transcript(
    value: str,
    languages: list[str] | None = None,
    max_chars: int | None = None,
    use_cache: bool = True,
) -> dict:
    """Fetch a video transcript. Never raises on a missing/disabled track —
    returns {ok: False, error: ...} so a scan can degrade to title+desc."""
    languages = languages or DEFAULT_LANGS
    try:
        video_id = extract_video_id(value)
    except ValueError as e:
        return {"video_id": None, "text": "", "char_count": 0, "ok": False, "error": str(e)}

    cache_path = CACHE_DIR / f"{video_id}.json"
    if use_cache and cache_path.exists():
        try:
            cached = json.loads(cache_path.read_text())
            cached["cached"] = True
            if max_chars and len(cached.get("text", "")) > max_chars:
                cached["text"] = cached["text"][:max_chars]
                cached["truncated"] = True
            return cached
        except (json.JSONDecodeError, OSError):
            pass  # corrupt cache — just refetch

    try:
        segments, lang = _fetch_segments(video_id, languages)
    except Exception as e:
        # TranscriptsDisabled / NoTranscriptFound / VideoUnavailable / network
        return {
            "video_id": video_id,
            "text": "",
            "char_count": 0,
            "ok": False,
            "cached": False,
            "error": f"{type(e).__name__}: {e}",
        }

    text = _segments_to_text(segments)
    result = {
        "video_id": video_id,
        "text": text,
        "char_count": len(text),
        "language": lang,
        "source": "captions",
        "cached": False,
        "ok": len(text) > 0,
    }

    if use_cache and result["ok"]:
        try:
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            cache_path.write_text(json.dumps(result, ensure_ascii=False))
        except OSError:
            pass  # caching is best-effort

    if max_chars and len(result["text"]) > max_chars:
        result["text"] = result["text"][:max_chars]
        result["truncated"] = True
    return result


def main() -> int:
    p = argparse.ArgumentParser(description="Fetch a YouTube transcript as plain text.")
    p.add_argument("video", help="Video id, watch/youtu.be URL, or yt:video:<ID>.")
    p.add_argument("--lang", action="append", help="Preferred language code (repeatable).")
    p.add_argument("--max-chars", type=int, default=None, help="Truncate text to N chars.")
    p.add_argument("--no-cache", action="store_true", help="Ignore the on-disk cache.")
    args = p.parse_args()

    result = fetch_transcript(
        args.video,
        languages=args.lang or None,
        max_chars=args.max_chars,
        use_cache=not args.no_cache,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
