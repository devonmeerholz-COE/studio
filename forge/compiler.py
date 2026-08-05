"""Compile Studio canon into structured renderer data."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


STUDIO_ROOT = Path(__file__).resolve().parent.parent
SUPPORTED_WORLD = "hacker-apartment"
SOURCE_PATHS = (
    Path("WORLD_BIBLE.md"),
    Path("ART_DIRECTION.md"),
    Path("OBJECTS.md"),
    Path("artwork_briefs/hacker-apartment-v2.md"),
)


def _read_sources(root: Path) -> dict[str, str]:
    return {
        path.as_posix(): (root / path).read_text(encoding="utf-8")
        for path in SOURCE_PATHS
    }


def _require(source: str, fragment: str, source_name: str) -> None:
    if fragment.casefold() not in source.casefold():
        raise ValueError(f"Required canon is missing from {source_name}: {fragment}")


def compile_render_spec(
    world_key: str, root: Path = STUDIO_ROOT
) -> dict[str, Any]:
    """Compile the supported world's canon into renderer-facing data."""
    if world_key != SUPPORTED_WORLD:
        raise ValueError(f"Unknown world key: {world_key}")

    sources = _read_sources(root)
    world = sources["WORLD_BIBLE.md"]
    art = sources["ART_DIRECTION.md"]
    objects = sources["OBJECTS.md"]
    brief = sources["artwork_briefs/hacker-apartment-v2.md"]

    requirements = (
        (world, "The camera remains stationary", "WORLD_BIBLE.md"),
        (world, "The desk remains the visual center", "WORLD_BIBLE.md"),
        (world, "You are the independent builder", "WORLD_BIBLE.md"),
        (brief, "Eye-level perspective", "artwork brief"),
        (brief, "compact Neo-Tokyo apartment during a rainy evening", "artwork brief"),
        (brief, "Warm interior lighting", "artwork brief"),
        (brief, "Cool rainy city beyond the window", "artwork brief"),
        (brief, "evidence rather than explanation", "artwork brief"),
        (art, "The resident is never present", "ART_DIRECTION.md"),
        (objects, "`protagonist-bonsai`", "OBJECTS.md"),
        (objects, "`mech-mementos`", "OBJECTS.md"),
    )
    for source, fragment, source_name in requirements:
        _require(source, fragment, source_name)

    return {
        "world": world_key,
        "camera": {
            "movement": "static",
            "framing": "wide",
            "eye_level": True,
        },
        "environment": {
            "weather": "rain",
            "time": "evening",
            "city": "neo_tokyo",
        },
        "immutable": [
            "empty_chair",
            "camera",
            "protagonist-bonsai",
            "desk_position",
        ],
        "composition": {
            "primary_focus": "desk",
            "secondary_focus": "city",
        },
        "identity": [
            "independent_builder",
            "viewer_is_resident",
            "resident_absent",
        ],
        "storytelling": [
            "evidence_over_explanation",
            "lived_in",
            "quiet_persistence",
        ],
        "objects": [
            {"id": "protagonist-bonsai", "category": "canon"},
            {"id": "mech-mementos", "category": "identity"},
            {"id": "keyboard", "category": "tool"},
        ],
        "lighting": {
            "interior": "warm",
            "exterior": "cool",
            "monitor": "glow",
        },
        "motion_candidates": [
            "rain",
            "steam",
            "monitor_flicker",
        ],
    }


def write_render_spec(world_key: str, root: Path = STUDIO_ROOT) -> Path:
    """Compile and write a render specification, returning its path."""
    spec = compile_render_spec(world_key, root)
    output_path = root / "build" / "render_specs" / f"{world_key}.render.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(spec, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return output_path


def compile_world(world_key: str | None) -> int:
    if world_key is None:
        print("A world key is required.")
        print(f"Valid world keys:\n- {SUPPORTED_WORLD}")
        return 2
    try:
        output_path = write_render_spec(world_key)
    except (OSError, ValueError) as error:
        print(error)
        return 2
    print(output_path.relative_to(STUDIO_ROOT).as_posix())
    return 0


def malformed_compile_usage() -> int:
    print("Compile accepts exactly one world key.")
    print(f"Valid world keys:\n- {SUPPORTED_WORLD}")
    return 2
