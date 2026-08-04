"""Present complete canonical reference views of Studio worlds."""

from forge.worlds import ALL_WORLDS, WORLDS_BY_KEY


def _print_valid_world_keys() -> None:
    print("Valid world keys:")
    for world in ALL_WORLDS:
        print(f"- {world.stable_key}")


def _print_section(title: str) -> None:
    print()
    print(title)
    print()


def _print_bullets(values: tuple[str, ...]) -> None:
    for value in values:
        print(f"- {value}")


def _print_prose(values: tuple[str, ...]) -> None:
    for index, value in enumerate(values):
        if index:
            print()
        print(value)


def inspect_world(world_key: str | None) -> int:
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
    print(f"Stable key: {world.stable_key}")
    print(f"Catalog number: {world.catalog_number}")
    print(f"Chronological stage: {world.chronological_stage}")

    _print_section("First Impression")
    print(world.first_impression)

    _print_section("Era")
    _print_bullets(world.era.lines)

    _print_section("Purpose")
    print(world.purpose)

    _print_section("Resident Identity")
    print(world.resident_identity)

    _print_section("Emotional Core")
    _print_prose(world.emotional_core)

    _print_section("Leaving This World")
    _print_bullets(world.leaving_this_world)

    _print_section("Setting")
    print(world.setting)

    _print_section("Beacon")
    print(f"Identity: {world.beacon.identity}")
    print(f"Emotional purpose: {world.beacon.emotional_purpose}")
    print(f"Natural aging: {world.beacon.natural_aging}")

    _print_section("Bonsai Relationship")
    print(f"Identity: {world.bonsai_relationship.identity}")
    print(f"Life stage: {world.bonsai_relationship.life_stage}")
    print(f"Beacon relationship: {world.bonsai_relationship.beacon_relationship}")

    _print_section("Soundscape")
    print(f"Music: {world.soundscape.music}")
    print(f"Ambient World: {world.soundscape.ambient_world}")
    print(f"Silence: {world.soundscape.silence}")

    _print_section("Personal Artifacts")
    _print_prose(world.personal_artifacts)

    _print_section("Passage of Time")
    print(world.passage_of_time)

    _print_section("Immutable Elements")
    _print_prose(world.immutable_elements)

    if world.motto is not None:
        _print_section("Motto")
        print(world.motto)

    if world.naming_note is not None:
        _print_section("Naming")
        print(world.naming_note)

    return 0


def malformed_inspect_usage() -> int:
    print("Inspect accepts exactly one world key.")
    print()
    _print_valid_world_keys()
    return 2
