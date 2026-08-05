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
    """Read the authorized Studio source documents."""
    return {
        path.as_posix(): (root / path).read_text(encoding="utf-8")
        for path in SOURCE_PATHS
    }


def _require(source: str, fragment: str, source_name: str) -> None:
    """Fail compilation when an essential canon fragment is missing."""
    if fragment.casefold() not in source.casefold():
        raise ValueError(
            f"Required canon is missing from {source_name}: {fragment}"
        )


def compile_scene_graph(world_key: str) -> dict[str, Any]:
    """Compile normalized spatial nodes for a supported Studio world."""

    world_graphs: dict[str, list[dict[str, Any]]] = {
        "hacker-apartment": [
            {
                "id": "WINDOW_WALL",
                "region": "rear",
                "constraints": [
                    "occupies the entire rear wall",
                    "floor-to-ceiling rain-covered glass",
                    "dense Neo-Tokyo city beyond",
                    "must remain visually open",
                    "nothing blocks the principal city view",
                ],
            },
            {
                "id": "LOUNGE",
                "region": "left-third",
                "constraints": [
                    "compact dark-fabric sofa",
                    "faces the low coffee table",
                    "contains the red-panda plush",
                    "feels used and comfortable",
                ],
            },
            {
                "id": "COFFEE_TABLE",
                "region": "foreground-left",
                "constraints": [
                    "low worn-wood table",
                    "positioned between sofa and Bonsai",
                    "contains an open notebook and coffee mug",
                ],
            },
            {
                "id": "BONSAI",
                "region": "foreground-left-of-centre",
                "constraints": [
                    "positioned between lounge and workstation",
                    "prominent foreground hero object",
                    "never pushed against the window",
                    "never replaced by a generic plant",
                    "does not block the workstation",
                ],
            },
            {
                "id": "WORKSTATION",
                "region": "right-half",
                "constraints": [
                    "long dark-walnut workstation spans the right half",
                    "runs parallel to the rear windows",
                    "three identical large widescreen monitors",
                    "three monitors form one continuous working arrangement",
                    "empty ergonomic chair centered at the workstation",
                    "desk is the dominant functional mass",
                ],
            },
            {
                "id": "PEGBOARD",
                "region": "right-wall",
                "constraints": [
                    "mounted above or beside the workstation",
                    "contains practical tools and repaired equipment",
                ],
            },
            {
                "id": "SHELVING",
                "region": "right-wall",
                "constraints": [
                    "dark shelving above and beside the workstation",
                    "contains books, electronics and personal mementos",
                    "contains the large mech model",
                ],
            },
            {
                "id": "BACKPACK",
                "region": "floor-right",
                "constraints": [
                    "rests on the floor beside the workstation",
                    "visibly used and repaired",
                    "does not block the chair",
                ],
            },
            {
                "id": "PURPLE_NEON",
                "region": "upper-left-wall",
                "constraints": [
                    "small purple code-symbol neon",
                    "soft accent only",
                    "never the main light source",
                ],
            },
        ],
        "midnight-library": [
            {
                "id": "CLAIMED_DESK",
                "region": "study-corner",
                "constraints": [
                    "fixed viewpoint faces the claimed desk",
                    "desk remains inside a quiet library corner",
                ],
            },
            {
                "id": "DESK_LAMP",
                "region": "claimed-desk",
                "constraints": ["permanent lamp on the claimed desk"],
            },
            {
                "id": "WINDOW",
                "region": "distant-wall",
                "constraints": ["small", "distant", "secondary"],
            },
        ],
        "coffee-cafe": [
            {
                "id": "BOOTH",
                "region": "window-side",
                "constraints": [
                    "fixed viewpoint occupies the booth",
                    "booth sits beside the window",
                ],
            },
            {
                "id": "COFFEE_POT",
                "region": "table",
                "constraints": ["permanent coffee pot on the table"],
            },
            {
                "id": "WINDOW",
                "region": "beside-booth",
                "constraints": [
                    "flying traffic remains distant",
                    "outside world remains secondary",
                ],
            },
        ],
        "rainy-loft": [
            {
                "id": "LOUNGE",
                "region": "interior",
                "constraints": [
                    "fixed viewpoint faces the floor lounge or couch"
                ],
            },
            {
                "id": "PARK_WINDOW",
                "region": "exterior-wall",
                "constraints": ["faces a large city park"],
            },
            {
                "id": "LAPTOP_BAG",
                "region": "by-door",
                "constraints": ["closed", "permanent Beacon"],
            },
        ],
        "space-station": [
            {
                "id": "VIEWPORT",
                "region": "observation-wall",
                "constraints": [
                    "station's largest viewport",
                    "fixed viewpoint faces Earth",
                ],
            },
            {
                "id": "EARTH",
                "region": "beyond-viewport",
                "constraints": [
                    "dominant exterior anchor",
                    "remains fully recognizable",
                ],
            },
            {
                "id": "RED_PANDA",
                "region": "interior",
                "constraints": ["remains present"],
            },
        ],
    }

    if world_key not in world_graphs:
        raise ValueError(f"Unknown world key: {world_key}")

    return {
        "stage": "Scene Graph",
        "world": world_key,
        "nodes": world_graphs[world_key],
    }


def compile_render_spec(
    world_key: str,
    root: Path = STUDIO_ROOT,
) -> dict[str, Any]:
    """Compile the Hacker Apartment into a production-design specification."""

    if world_key != SUPPORTED_WORLD:
        raise ValueError(f"Unknown world key: {world_key}")

    sources = _read_sources(root)

    world = sources["WORLD_BIBLE.md"]
    art = sources["ART_DIRECTION.md"]
    objects = sources["OBJECTS.md"]
    brief = sources["artwork_briefs/hacker-apartment-v2.md"]

    requirements = (
        (
            world,
            "The camera remains stationary",
            "WORLD_BIBLE.md",
        ),
        (
            world,
            "The desk remains the visual center",
            "WORLD_BIBLE.md",
        ),
        (
            world,
            "You are the independent builder",
            "WORLD_BIBLE.md",
        ),
        (
            brief,
            "Eye-level perspective",
            "artwork brief",
        ),
        (
            brief,
            "compact Neo-Tokyo apartment during a rainy evening",
            "artwork brief",
        ),
        (
            brief,
            "Warm interior lighting",
            "artwork brief",
        ),
        (
            brief,
            "Cool rainy city beyond the window",
            "artwork brief",
        ),
        (
            brief,
            "evidence rather than explanation",
            "artwork brief",
        ),
        (
            art,
            "The resident is never present",
            "ART_DIRECTION.md",
        ),
        (
            objects,
            "`protagonist-bonsai`",
            "OBJECTS.md",
        ),
        (
            objects,
            "`mech-mementos`",
            "OBJECTS.md",
        ),
    )

    for source, fragment, source_name in requirements:
        _require(source, fragment, source_name)

    return {
        "world": world_key,
        "specification_type": "production_design_brief",
        "immutable_canon": [
            "static eye-level 35mm wide 16:9 camera",
            "no visible resident",
            "floor-to-ceiling rear windows",
            "rainy nighttime Neo-Tokyo",
            "long workstation across right half",
            "exactly three identical large monitors",
            "large mature Bonsai in the foreground, inside the room, left of centre",
            "compact lounge on left",
            "red-panda plush on sofa",
            "low coffee table",
            "right-wall pegboard and shelving",
            "large mech collectible on right shelving",
            "repaired backpack beside workstation",
            "small purple code-symbol neon on upper-left wall",
            "visible flying vehicles outside",
            "deep charcoal and dark walnut base",
            "warm amber interior lighting",
            "restrained cyan and purple exterior accents",
            "plausible 2056 technology",
            "no daylight",
            "no generic office",
            "no missing hero objects",
        ],
        "episode_brief": {
            "episode": 13,
            "time_advanced": "three months",
            "changes": [
                "software project has visibly progressed",
                "one notebook is nearly full",
                "one newer notebook is beside it",
                "one repaired cable is visible",
                "one new small personal keepsake has appeared",
                "coffee mug has moved",
                "Bonsai shows subtle healthy growth and careful pruning",
                "rain is slightly heavier",
                "room remains restrained and lived-in",
            ],
        },
        "scene_graph": compile_scene_graph(world_key),

        "camera": {
            "movement": "static",
            "height": "eye-level, approximately 1.6 metres",
            "lens": "35mm lens equivalent",
            "framing": "wide cinematic 16:9 view",
            "viewpoint": "viewer positioned naturally inside the room",
            "angle": "straight and calm with no dramatic angle",
            "perspective": "natural human perspective",
            "resident": "no visible resident",
            "forbidden": [
                "Dutch angle",
                "cinematic tilt",
                "dramatic perspective distortion",
                "extreme depth of field",
                "cropped room",
            ],
        },

        "composition": {
            "primary_focus": "triple-monitor workstation",
            "visual_anchor": "protagonist Bonsai",
            "dominant_light_source": "rain-covered rear window",
            "secondary_focus": "Neo-Tokyo city",
            "regions": {
                "left_third": [
                    "compact lounge",
                    "dark-fabric sofa",
                    "red-panda plush",
                    "low coffee table",
                ],
                "centre_third": [
                    "large mature Bonsai in foreground",
                    "rain-covered windows behind it",
                    "clear transition between lounge and workstation",
                ],
                "right_third": [
                    "long workstation",
                    "three identical large monitors",
                    "empty centered chair",
                    "pegboard",
                    "shelving",
                    "backpack",
                ],
            },
            "hierarchy": [
                "Bonsai is the emotional visual anchor",
                "workstation is the dominant functional mass",
                "rear window is the dominant environmental light source",
                "city frames the room but never overwhelms it",
                "room must feel more important than the skyline",
            ],
        },

        "hero_objects": [
            {
                "id": "protagonist-bonsai",
                "priority": 1,
                "required": True,
                "appearance": [
                    "large mature miniature tree",
                    "old thick twisted woody trunk",
                    "clearly trained branches",
                    "dense but imperfect foliage",
                    "visible roots",
                    "shallow dark ceramic pot",
                    "unmistakably a Bonsai",
                ],
                "placement": [
                    "foreground",
                    "left of centre",
                    "between lounge and workstation",
                ],
                "forbidden": [
                    "cactus",
                    "succulent",
                    "generic houseplant",
                    "thin young sapling",
                    "background decoration",
                ],
            },
            {
                "id": "triple-monitor-workstation",
                "priority": 2,
                "required": True,
                "appearance": [
                    "three identical large widescreen monitors",
                    "three monitors arranged as one coherent workspace",
                    "believable software-development interfaces",
                    "mechanical keyboard",
                    "mouse",
                    "open notebook",
                    "coffee mug",
                    "practical articulated desk lamp",
                    "PC tower under or beside desk",
                    "visible purposeful cables",
                    "evidence of repaired equipment",
                ],
                "placement": [
                    "dominates the right half",
                    "parallel to rear window",
                    "chair centered in front",
                ],
                "forbidden": [
                    "one monitor",
                    "tiny monitors",
                    "mismatched monitor sizes",
                    "gaming battlestation",
                    "excessive RGB",
                    "fake cinematic code",
                ],
            },
            {
                "id": "purple-code-symbol-neon",
                "priority": 3,
                "required": True,
                "appearance": [
                    "small purple code-symbol neon",
                    "restrained soft glow",
                    "recognizable code brackets or code symbol",
                ],
                "placement": ["upper-left wall"],
                "forbidden": [
                    "dominant neon sign",
                    "motivational slogan",
                    "large decorative typography",
                ],
            },
            {
                "id": "mech-model",
                "priority": 4,
                "required": True,
                "appearance": [
                    "detailed articulated mech collectible",
                    "approximately 40 centimetres tall",
                    "used personal collectible rather than showroom display",
                ],
                "placement": ["right-side shelving"],
            },
            {
                "id": "red-panda-plush",
                "priority": 5,
                "required": True,
                "appearance": [
                    "small worn red-panda plush",
                    "personal keepsake",
                ],
                "placement": ["left sofa"],
            },
        ],

        "room_layout": [
            "floor-to-ceiling rain-covered windows occupy the rear wall",
            "long dark-walnut workstation spans the entire right half",
            "compact lounge occupies the left third",
            "low coffee table sits in the foreground-left",
            "Bonsai separates the lounge from the workstation",
            "shelving and pegboard occupy the right wall",
            "backpack rests on the floor beside the workstation",
            "principal window view remains open",
            "objects must follow the scene graph",
        ],

        "workstation": [
            "three identical large widescreen monitors",
            "large monitors, not small office displays",
            "believable software-development interfaces",
            "no readable fake code",
            "mechanical keyboard",
            "mouse",
            "notebooks",
            "coffee mug",
            "practical desk lamp",
            "PC tower",
            "visible repaired cable",
            "future electronics prototypes",
            "advanced soldering equipment",
            "restrained accent lighting",
        ],

        "future_markers": [
            "the room unmistakably exists in 2056",
            "multiple distant flying vehicles visible outside",
            "layered aerial traffic at different depths",
            "small autonomous delivery drone charging on a shelf",
            "subtle smart-glass interface reflections",
            "advanced electronics prototypes",
            "future development equipment",
            "plausible near-future hardware",
            "future details remain grounded and functional",
            "nothing cartoonish",
            "nothing magical",
            "nothing fantasy",
        ],

        "city": [
            "dense futuristic Neo-Tokyo skyline",
            "high elevation above the city",
            "rain at night",
            "layered building depth extending toward the horizon",
            "distant flying traffic",
            "cyan and blue city light",
            "restrained purple neon",
            "recognizable futuristic tower",
            "city remains secondary to the apartment",
            "not a modern 2025 skyline",
            "not suburban",
        ],

        "canonical_objects": [
            "protagonist Bonsai",
            "evolving repaired backpack",
            "red-panda plush",
            "headphones",
            "used notebooks",
            "mechanical keyboard",
            "coffee mug",
            "large mech figure and smaller mementos",
            "practical tools",
            "future electronics prototypes",
            "repaired cable",
        ],

        "bonsai": [
            "large mature Bonsai",
            "thick aged woody trunk",
            "twisted trunk with visible roots",
            "trained branches",
            "dense miniature tree silhouette",
            "healthy but imperfect foliage",
            "shallow ceramic pot",
            "foreground hero object",
            "never cactus-like",
            "never succulent-like",
            "never replaced by another decorative plant",
        ],

        "materials": [
            "dark walnut",
            "worn dark wood",
            "softened used fabric",
            "scratched aged metal",
            "used matte plastic",
            "rain-streaked glass",
            "visible repair",
            "patina",
            "worn edges",
            "nothing feels newly purchased",
            "nothing glossy without a reason",
        ],

        "lighting": [
            "primary warm practical desk lighting",
            "secondary cool rain-filtered city light",
            "small restrained purple neon accent",
            "subtle monitor glow",
            "warm amber interior highlights",
            "deep charcoal shadows that retain visible detail",
            "high dynamic range",
            "image must not be underexposed",
            "image must not be overexposed",
            "image must not be oversaturated",
        ],

        "colour_script": {
            "dark_neutrals_percent": 65,
            "dark_neutrals": [
                "deep charcoal",
                "dark walnut",
                "black",
                "dark grey",
            ],
            "warm_light_percent": 25,
            "warm_light": [
                "warm amber",
                "soft tungsten",
            ],
            "future_accents_percent": 10,
            "future_accents": [
                "restrained purple",
                "restrained cyan",
            ],
            "rules": [
                "no other dominant colours",
                "purple and cyan remain accents",
                "city light does not wash out the interior",
                "warm interior and cool exterior remain balanced",
            ],
        },

        "story": [
            "independent software builder lives here",
            "resident has just stepped away",
            "room has accumulated naturally over years",
            "unfinished software and electronics projects",
            "coffee is still warm",
            "notebooks show active work",
            "objects reveal repeated routines",
            "evidence of quiet persistence",
            "nothing feels staged",
            "everything has a purpose",
            "no explanatory signage",
        ],

        "non_negotiable": [
            "large mature foreground Bonsai",
            "three identical large monitors",
            "purple code-symbol neon",
            "distant flying traffic",
            "large mech figure on right shelving",
            "evolving backpack beside workstation",
            "red-panda plush on left sofa",
            "rain",
            "large floor-to-ceiling rear window",
            "believable coding workstation",
            "right-wall tools and pegboard",
            "warm amber and cool cyan-purple colour scheme",
        ],

        "forbidden": [
            "missing Bonsai",
            "small Bonsai hidden in background",
            "generic office",
            "corporate workspace",
            "minimalist empty room",
            "one-monitor desk",
            "two-monitor desk",
            "more than three primary monitors",
            "tiny monitors",
            "gaming room",
            "gaming chair",
            "chair with excessive or anatomically impossible wheels",
            "visible person",
            "decorative houseplants replacing the Bonsai",
            "motivational text",
            "readable fake text",
            "fake readable code",
            "cinematic hacker clichés",
            "excessive neon",
            "excessive RGB",
            "excessive clutter",
            "dramatic camera angle",
            "daylight",
            "suburban skyline",
            "modern 2025 city",
            "missing future technology",
            "missing flying vehicles",
            "missing mech model",
            "missing purple neon",
            "anime bedroom",
            "hotel room",
            "sterile showroom",
            "underexposed image",
            "overexposed image",
            "random dominant colours outside the colour script",
            "obvious AI geometry errors",
            "duplicated furniture",
            "malformed chair",
            "impossible monitor stands",
        ],

        "motion_candidates": [
            "rain moving down the glass",
            "distant flying traffic",
            "subtle monitor activity",
            "steam rising from coffee mug",
            "small neon fluctuation",
            "gentle plant response to room airflow",
            "soft autonomous drone status light",
        ],
    }


def write_render_spec(
    world_key: str,
    root: Path = STUDIO_ROOT,
) -> Path:
    """Compile and write a render specification, returning its path."""

    spec = compile_render_spec(world_key, root)

    output_path = (
        root
        / "build"
        / "render_specs"
        / f"{world_key}.render.json"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        json.dumps(
            spec,
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    return output_path


def compile_world(world_key: str | None) -> int:
    """Compile a world through the command-line interface."""

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
    """Report malformed compile-command usage."""

    print("Compile accepts exactly one world key.")
    print(f"Valid world keys:\n- {SUPPORTED_WORLD}")
    return 2
