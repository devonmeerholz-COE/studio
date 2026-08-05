"""Fal image-to-image renderer for the Hacker Apartment."""

from __future__ import annotations

import base64
import json
import os
from pathlib import Path
from typing import Any, Callable
from urllib.request import urlopen

from forge.compiler import STUDIO_ROOT, compile_render_spec


MODEL_ID = "fal-ai/flux-pro/kontext"
SOURCE_IMAGE = Path("assets/hacker-apartment/source/hacker-apartment-master-v2.png")
OUTPUT_IMAGE = Path("output/proofs/hacker-apartment-episode-002.png")
REQUEST_METADATA = Path(
    "output/proofs/hacker-apartment-episode-002.request.json"
)


def build_instruction(spec: dict[str, Any]) -> str:
    """Build the editing instruction from compiled Studio canon."""
    return f"""Edit the supplied canonical Hacker Apartment image in place. This is a subtle continuity update approximately three months later, not a redesign.

PRESERVE EXACTLY: the existing camera position and eye-level, natural human field of view; the room layout; the desk placement as the visual centre; the Neo-Tokyo skyline; the flying cars; the purple code-symbol neon; the protagonist's Bonsai in its current location; the rainy nighttime atmosphere with warm practical interior light and cool rainy city beyond the glass; and the empty chair because the viewer is the resident. Keep the apartment modest, believable, restrained, and uncluttered. The city remains secondary to the room.

PROGRESS THE LIVING WORLD BY APPROXIMATELY THREE MONTHS: give the young Bonsai subtle healthy new growth and evidence of careful pruning while retaining its woody trunk, trained branching, miniature-tree silhouette, identity, and location. The old handwritten notebook is nearly full, and one new notebook has appeared beside it. Show that the software project has visibly progressed through a believable, restrained software interface, without fake code or invented text. Give the mechanical keyboard and desk slightly more natural use and wear. Show one existing cable carefully repaired. Add one small, quiet personal keepsake with a clear reason to be there. Everything must feel accumulated through routine rather than staged.

DO NOT: redesign the apartment; move or alter the camera; change the room layout or desk position; replace furniture; introduce a visible resident or any person; fill the chair; add slogans, motivational posters, decorative typography, cinematic hacker interfaces, meaningless streams of code, fake code, unreadable text, AI gibberish, excess RGB lighting, clutter, or exaggerated cyberpunk styling. Do not make the city dominate the room.

Canon anchors from the compiled render specification: camera movement={spec['camera']['movement']}; primary focus={spec['composition']['primary_focus']}; weather={spec['environment']['weather']}; city={spec['environment']['city']}; immutable elements={', '.join(spec['immutable'])}; storytelling={', '.join(spec['storytelling'])}. Preserve the source image's composition and materials. Make only quiet, plausible continuity changes."""


def _queue_progress(update: Any) -> None:
    """Print Fal queue updates without assuming a particular event class."""
    if isinstance(update, dict):
        message = update.get("message") or update.get("status") or update
    else:
        message = getattr(update, "message", None) or update
    print(f"Fal queue: {message}")


def _image_url(result: Any) -> str:
    if not isinstance(result, dict):
        raise ValueError("Fal returned an unexpected response.")
    images = result.get("images")
    if not isinstance(images, list) or not images:
        raise ValueError("Fal returned no generated image.")
    first = images[0]
    if not isinstance(first, dict) or not isinstance(first.get("url"), str):
        raise ValueError("Fal returned an invalid generated image URL.")
    return first["url"]


def render_hacker_apartment(
    root: Path = STUDIO_ROOT,
    *,
    fal_module: Any | None = None,
    load_environment: Callable[..., Any] | None = None,
    open_url: Callable[..., Any] = urlopen,
) -> int:
    """Render episode 002 and return a process-style exit code."""
    try:
        if load_environment is None:
            from dotenv import load_dotenv

            load_environment = load_dotenv
        load_environment(dotenv_path=root / ".env")

        if not os.environ.get("FAL_KEY"):
            raise RuntimeError("FAL_KEY is missing from the Studio root .env file.")

        if fal_module is None:
            import fal_client

            fal_module = fal_client

        spec = compile_render_spec("hacker-apartment", root)
        source_path = root / SOURCE_IMAGE
        if not source_path.is_file():
            raise FileNotFoundError(f"Source image not found: {source_path}")

        encoded_source = base64.b64encode(source_path.read_bytes()).decode("ascii")
        source_data_uri = f"data:image/png;base64,{encoded_source}"
        arguments = {
            "prompt": build_instruction(spec),
            "image_url": source_data_uri,
        }
        request_metadata = {
            "model": MODEL_ID,
            "prompt": arguments["prompt"],
            "source_image": SOURCE_IMAGE.as_posix(),
            "output_image": OUTPUT_IMAGE.as_posix(),
        }

        print(f"Rendering with {MODEL_ID}...")
        result = fal_module.subscribe(
            MODEL_ID,
            arguments=arguments,
            with_logs=True,
            on_queue_update=_queue_progress,
        )
        generated_url = _image_url(result)

        output_path = root / OUTPUT_IMAGE
        metadata_path = root / REQUEST_METADATA
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open_url(generated_url) as response:
            output_path.write_bytes(response.read())
        metadata_path.write_text(
            json.dumps(request_metadata, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(OUTPUT_IMAGE.as_posix())
        print(REQUEST_METADATA.as_posix())
        return 0
    except Exception as error:
        print(f"Render failed: {error}")
        return 1


def malformed_render_usage() -> int:
    print("Render accepts exactly one world key.")
    print("Valid world keys:\n- hacker-apartment")
    return 2
