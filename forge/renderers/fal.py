"""Fal text-to-image renderer for the Hacker Apartment."""

from __future__ import annotations

import base64
import importlib.util
import json
import os
from pathlib import Path
import re
from typing import Any, Callable
from urllib.request import urlopen

from forge.compiler import STUDIO_ROOT, compile_render_spec
from forge.vision_inspector import inspect_hacker_apartment


MODEL_ID = "fal-ai/flux-pro"
CORRECTIVE_MODEL_ID = "fal-ai/flux-pro/kontext"
SOURCE_IMAGE = Path("assets/hacker-apartment/source/hacker-apartment-master-v2.png")
PROOFS_DIRECTORY = Path("output/proofs")
EPISODE_STEM = "hacker-apartment-episode-"
EPISODE_PATTERN = re.compile(rf"^{re.escape(EPISODE_STEM)}(\d+)\.png$")


def _master_episode_number() -> int:
    match = re.search(r"-v(\d+)\.png$", SOURCE_IMAGE.name)
    if match is None:
        raise ValueError(f"Source image has no version number: {SOURCE_IMAGE}")
    return int(match.group(1))


def _episode_image(number: int) -> Path:
    return PROOFS_DIRECTORY / f"{EPISODE_STEM}{number:03d}.png"


OUTPUT_IMAGE = _episode_image(_master_episode_number())
REQUEST_METADATA = OUTPUT_IMAGE.with_suffix(".request.json")
VALIDATOR_PATH = Path("studio/worlds/hacker-apartment/validator.py")
ACCEPTANCE_SCORE = 8
MAX_ATTEMPTS = 3


def _render_paths(root: Path) -> tuple[Path, Path, Path]:
    proofs = root / PROOFS_DIRECTORY
    episodes = []
    if proofs.is_dir():
        for candidate in proofs.iterdir():
            match = EPISODE_PATTERN.fullmatch(candidate.name)
            if match is not None and candidate.is_file():
                episodes.append((int(match.group(1)), candidate))

    if episodes:
        latest_number, source_path = max(episodes, key=lambda item: item[0])
        output_number = latest_number + 1
    else:
        source_path = root / SOURCE_IMAGE
        output_number = _master_episode_number()

    output_path = root / _episode_image(output_number)
    metadata_path = output_path.with_suffix(".request.json")
    return source_path, output_path, metadata_path


def _prompt_layers(
    spec: dict[str, Any],
    corrective_patch: dict[str, list[str]] | None = None,
) -> dict[str, Any]:
    return {
        "immutable_canon": list(spec["immutable_canon"]),
        "episode_brief": dict(spec["episode_brief"]),
        "corrective_patch": corrective_patch,
    }


def _build_prompt(layers: dict[str, Any]) -> str:
    canon = "\n".join(f"- {item}" for item in layers["immutable_canon"])
    episode = layers["episode_brief"]
    changes = "\n".join(f"- {item}" for item in episode["changes"])
    sections = [
        f"IMMUTABLE CANON\n{canon}",
        (
            "EPISODE BRIEF\n"
            f"Episode: {episode['episode']}\n"
            f"Time advanced: {episode['time_advanced']}\n"
            f"Changes:\n{changes}"
        ),
    ]
    corrective = layers["corrective_patch"]
    if corrective is not None:
        failed = "\n".join(f"- {item}" for item in corrective["failed_rules"])
        passed = "\n".join(f"- {item}" for item in corrective["passed_rules"])
        sections.append(
            "CORRECTIVE PATCH\n"
            f"Failed requirements:\n{failed}\n\n"
            f"Preserve these already-passing requirements:\n{passed}"
        )
    return "\n\n".join(sections)


def build_instruction(spec: dict[str, Any]) -> str:
    """Build the concise immutable and episode prompt layers."""
    return _build_prompt(_prompt_layers(spec))


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


def _load_validator() -> Any:
    validator_path = STUDIO_ROOT / VALIDATOR_PATH
    module_spec = importlib.util.spec_from_file_location(
        "hacker_apartment_validator", validator_path
    )
    if module_spec is None or module_spec.loader is None:
        raise ImportError(f"Unable to load validator: {validator_path}")
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


def _attempt_path(output_path: Path, attempt: int) -> Path:
    return output_path.with_name(f"{output_path.stem}-attempt-{attempt}.png")


def _print_scorecard(validation: dict[str, Any]) -> None:
    for rule in validation["rules"]:
        mark = "✓" if rule["passed"] else "✗"
        try:
            print(f"{mark} {rule['label']}")
        except UnicodeEncodeError:
            fallback = "PASS" if rule["passed"] else "FAIL"
            print(f"{fallback} {rule['label']}")
    score = validation["overall_score"]
    print()
    print(f"Overall score: {score['earned']}/{score['possible']}")


def _corrective_prompt(
    spec: dict[str, Any],
    failed_rules: list[str],
    passed_rules: list[str],
) -> tuple[str, dict[str, Any]]:
    patch = {
        "failed_rules": list(failed_rules),
        "passed_rules": list(passed_rules),
    }
    layers = _prompt_layers(spec, patch)
    return _build_prompt(layers), layers


def render_hacker_apartment(
    root: Path = STUDIO_ROOT,
    *,
    fal_module: Any | None = None,
    load_environment: Callable[..., Any] | None = None,
    open_url: Callable[..., Any] = urlopen,
) -> int:
    """Render the next Hacker Apartment episode and return an exit code."""
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
        source_path, output_path, metadata_path = _render_paths(root)
        if not source_path.is_file():
            raise FileNotFoundError(f"Source image not found: {source_path}")
        current_layers = _prompt_layers(spec)
        prompt = _build_prompt(current_layers)
        arguments: dict[str, Any] = {
            "prompt": prompt,
            "image_size": "landscape_16_9",
            "num_images": 1,
            "output_format": "png",
        }
        request_metadata = {
            "model": MODEL_ID,
            "render_spec": spec,
            "prompt": prompt,
            "prompt_layers": current_layers,
            "source_image": source_path.relative_to(root).as_posix(),
            "output_image": output_path.relative_to(root).as_posix(),
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        validator = _load_validator()
        attempt_records = []
        accepted_bytes = None
        current_model = MODEL_ID
        current_arguments = arguments

        for attempt in range(1, MAX_ATTEMPTS + 1):
            attempt_path = _attempt_path(output_path, attempt)
            prompt_path = attempt_path.with_suffix(".prompt.txt")
            prompt_path.write_text(current_arguments["prompt"], encoding="utf-8")
            print(f"Rendering attempt {attempt} with {current_model}...")
            print(
                json.dumps(
                    {"model": current_model, "arguments": current_arguments},
                    indent=2,
                )
            )
            result = fal_module.subscribe(
                current_model,
                arguments=current_arguments,
                with_logs=True,
                on_queue_update=_queue_progress,
            )
            generated_url = _image_url(result)
            with open_url(generated_url) as response:
                attempt_bytes = response.read()

            attempt_path.write_bytes(attempt_bytes)
            observations = inspect_hacker_apartment(attempt_bytes, fal_module)
            validation = validator.validate({"observations": observations})
            validation["observations"] = observations
            _print_scorecard(validation)
            validator_path = attempt_path.with_suffix(".validator.json")
            validator_path.write_text(
                json.dumps(validation, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            attempt_records.append(
                {
                    "attempt": attempt,
                    "image": attempt_path.relative_to(root).as_posix(),
                    "prompt": prompt_path.relative_to(root).as_posix(),
                    "prompt_layers": current_layers,
                    "validator": validator_path.relative_to(root).as_posix(),
                    "score": validation["overall_score"],
                }
            )

            score = validation["overall_score"]["earned"]
            if score >= ACCEPTANCE_SCORE:
                accepted_bytes = attempt_bytes
                break
            if attempt < MAX_ATTEMPTS:
                corrective_prompt, current_layers = _corrective_prompt(
                    spec,
                    validation["failed_rules"],
                    validation["passed_rules"],
                )
                source_data = base64.b64encode(attempt_bytes).decode("ascii")
                current_model = CORRECTIVE_MODEL_ID
                current_arguments = {
                    "prompt": corrective_prompt,
                    "image_url": f"data:image/png;base64,{source_data}",
                    "image_prompt_strength": 0.65,
                    "output_format": "png",
                }

        request_metadata["attempts"] = attempt_records
        request_metadata["prompt"] = current_arguments["prompt"]
        request_metadata["prompt_layers"] = current_layers
        request_metadata["accepted"] = accepted_bytes is not None
        metadata_path.write_text(
            json.dumps(request_metadata, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        if accepted_bytes is None:
            print(f"Render failed validation after {MAX_ATTEMPTS} attempts.")
            return 1
        output_path.write_bytes(accepted_bytes)
        print(output_path.relative_to(root).as_posix())
        print(metadata_path.relative_to(root).as_posix())
        return 0
    except Exception as error:
        print(f"Render failed: {error}")
        return 1


def malformed_render_usage() -> int:
    print("Render accepts exactly one world key.")
    print("Valid world keys:\n- hacker-apartment")
    return 2
