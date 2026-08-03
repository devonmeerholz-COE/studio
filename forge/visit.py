"""Welcome visitors to canonical Studio worlds."""

from forge.worlds import ALL_WORLDS, WORLDS_BY_KEY


def _print_valid_world_keys() -> None:
    print("Valid world keys:")
    for world in ALL_WORLDS:
        print(f"- {world.stable_key}")


def visit(world_key: str | None) -> int:
    if world_key is None:
        print("A world key is required.")
        print()
        _print_valid_world_keys()
        return 2

    world = WORLDS_BY_KEY.get(world_key)
    if world is None:
        print(f"Unknown world key: {world_key}")
        print()
        _print_valid_world_keys()
        return 2

    print(world.canonical_name)
    print()
    print(world.first_impression)
    print()
    print(world.resident_identity)
    print()
    print(world.purpose)
    print()
    print("When you leave:")
    for state in world.leaving_this_world:
        print(f"- {state}")
    return 0


def malformed_visit_usage() -> int:
    print("Visit accepts exactly one world key.")
    print()
    _print_valid_world_keys()
    return 2
