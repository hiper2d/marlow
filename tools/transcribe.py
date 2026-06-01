"""
transcribe — local speech-to-text for the calorie tracker's voice notes.

Telegram voice messages arrive as OGG/Opus audio. Marlow (a Claude session)
can't *hear* audio, so we transcribe locally with faster-whisper — no API
call, no metered cost, consistent with the rest of the calorie pipeline.
The transcript then flows through the exact same path as a typed note.

Model is loaded lazily and cached per process. Default "small" (multilingual
— handles Alex's English and Russian); override with CALORIE_WHISPER_MODEL
(e.g. "base" for speed, "medium" for accuracy). faster-whisper downloads the
model on first use and caches it under ~/.cache/huggingface.

Importable:
    from tools.transcribe import transcribe_audio
    text = transcribe_audio(Path("inbox/2026-06-01/12.ogg"))

CLI:
    uv run python tools/transcribe.py path/to/audio.ogg
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

DEFAULT_MODEL = os.environ.get("CALORIE_WHISPER_MODEL", "small")

_model = None  # process-cached WhisperModel


def _get_model():
    global _model
    if _model is None:
        from faster_whisper import WhisperModel

        # int8 on CPU — fast and light; fine for short food notes.
        _model = WhisperModel(DEFAULT_MODEL, device="cpu", compute_type="int8")
    return _model


def transcribe_audio(path: Path) -> dict:
    """Transcribe an audio file. Returns {text, language, duration}."""
    model = _get_model()
    segments, info = model.transcribe(str(path), vad_filter=True)
    text = " ".join(seg.text.strip() for seg in segments).strip()
    return {
        "text": text,
        "language": info.language,
        "duration": round(info.duration, 1),
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Local speech-to-text (faster-whisper).")
    p.add_argument("path", help="Path to an audio file (ogg/wav/mp3/...).")
    args = p.parse_args()
    result = transcribe_audio(Path(args.path))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
