"""
generate_header_image — call OpenAI Images API and write the result to disk.

Deterministic gathering. Marlow's session composes the prompt (per
`memory/visual-guidelines.md`), calls this handler to materialize the
image, and writes the path into the draft's frontmatter.

Output path is fixed: `projects/blog/site/public/images/<slug>.png`. Astro
serves this from `/images/<slug>.png` at site runtime. The handler is
idempotent — refuses to overwrite an existing file (use `--force` to
regenerate; rare, only after Alex requests a retry).

Requires the API key in the process environment as `O_K`. How it gets
there is a deployment decision (launchd plist EnvironmentVariables,
launchctl setenv, shell init, etc.) — not something this handler tries
to manage. If `O_K` is missing, the handler returns ok=False so Marlow's
session can fail clean rather than burn a tick on a misconfigured call.

CLI:
    python handlers/generate_header_image.py generate \
        --slug <slug> --prompt "<prompt text>" [--size 1536x1024] [--force]
        → JSON {ok, slug, output_path, model, size, bytes}
    python handlers/generate_header_image.py status --slug <slug>
        → JSON {slug, exists, path, bytes}
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = REPO_ROOT / "projects" / "blog" / "site" / "public" / "images"
MODEL = "gpt-image-2"
DEFAULT_SIZE = "1536x1024"


def _load_api_key() -> str | None:
    return os.environ.get("O_K")


def _generate(prompt: str, size: str, api_key: str) -> bytes:
    """Returns raw PNG bytes. Raises requests.HTTPError on API failure."""
    resp = requests.post(
        "https://api.openai.com/v1/images/generations",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "prompt": prompt,
            "size": size,
            "n": 1,
        },
        timeout=120,
    )
    resp.raise_for_status()
    payload = resp.json()
    item = payload["data"][0]
    if "b64_json" in item:
        return base64.b64decode(item["b64_json"])
    # Fallback to URL download for models that don't return b64.
    image_url = item["url"]
    img_resp = requests.get(image_url, timeout=60)
    img_resp.raise_for_status()
    return img_resp.content


def generate(slug: str, prompt: str, size: str, force: bool) -> dict:
    output_path = IMAGES_DIR / f"{slug}.png"
    if output_path.exists() and not force:
        return {
            "ok": False,
            "error": f"image already exists at {output_path.relative_to(REPO_ROOT)} — use --force to regenerate",
        }

    api_key = _load_api_key()
    if not api_key:
        return {
            "ok": False,
            "error": "image API key missing — `O_K` is not in the process environment",
        }

    try:
        image_bytes = _generate(prompt, size, api_key)
    except requests.HTTPError as e:
        return {
            "ok": False,
            "error": f"OpenAI API error: {e.response.status_code} {e.response.text[:300]}",
        }
    except requests.RequestException as e:
        return {"ok": False, "error": f"network error: {e}"}

    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(image_bytes)
    return {
        "ok": True,
        "slug": slug,
        "output_path": str(output_path.relative_to(REPO_ROOT)),
        "serve_path": f"/images/{slug}.png",
        "model": MODEL,
        "size": size,
        "bytes": len(image_bytes),
    }


def status(slug: str) -> dict:
    output_path = IMAGES_DIR / f"{slug}.png"
    return {
        "slug": slug,
        "exists": output_path.exists(),
        "path": str(output_path.relative_to(REPO_ROOT)),
        "serve_path": f"/images/{slug}.png",
        "bytes": output_path.stat().st_size if output_path.exists() else None,
    }


def cmd_generate(args):
    result = generate(args.slug, args.prompt, args.size, args.force)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("ok") else 1)


def cmd_status(args):
    print(json.dumps(status(args.slug), indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_gen = sub.add_parser("generate", help="Generate the header image for a draft")
    p_gen.add_argument("--slug", required=True)
    p_gen.add_argument("--prompt", required=True)
    p_gen.add_argument("--size", default=DEFAULT_SIZE, help=f"default {DEFAULT_SIZE}")
    p_gen.add_argument("--force", action="store_true", help="overwrite existing image")

    p_stat = sub.add_parser("status", help="Inspect whether a slug's image exists")
    p_stat.add_argument("--slug", required=True)

    args = parser.parse_args()
    if args.cmd == "generate":
        cmd_generate(args)
    elif args.cmd == "status":
        cmd_status(args)


if __name__ == "__main__":
    main()
