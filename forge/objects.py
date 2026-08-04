"""The twelve canonical recurring Studio objects."""

from types import MappingProxyType
from typing import Mapping

from forge.object_model import (
    ObjectCategory,
    RecognitionLevel,
    StudioObject,
    WorldMoment,
)


PROTAGONIST_BONSAI = StudioObject(
    canonical_name="The Protagonist’s Bonsai",
    canonical_id="protagonist-bonsai",
    category=ObjectCategory.CANON,
    recognition_level=RecognitionLevel.FAMILIAR,
    first_appearance=WorldMoment("midnight-library", "earliest life stage"),
    purpose=(
        "Represents quiet growth across an entire lifetime.",
        "It reminds the viewer that meaningful change is measured in years rather than moments.",
    ),
    studio_rules=(
        "It remains present throughout its established continuity. It may age and grow "
        "naturally. In the Hacker Apartment, it is also the Beacon."
    ),
    evolution=(
        WorldMoment("midnight-library", "earliest life stage"),
        WorldMoment("hacker-apartment", "young and also the Beacon"),
        WorldMoment("rainy-loft", "mature and larger"),
        WorldMoment("space-station", "old, larger, and carefully sustained"),
    ),
    continuity_notes=(
        "This is the same protagonist-owned Bonsai across the Midnight Library, "
        "Hacker Apartment, Rainy Loft, and Space Station. It is distinct from the "
        "Coffee Café house Bonsai."
    ),
    appearances=(
        WorldMoment("midnight-library", "earliest life stage"),
        WorldMoment("hacker-apartment", "young and also the Beacon"),
        WorldMoment("rainy-loft", "mature"),
        WorldMoment("space-station", "old and carefully sustained"),
    ),
)

COFFEE_CAFE_HOUSE_BONSAI = StudioObject(
    canonical_name="Coffee Café House Bonsai",
    canonical_id="coffee-cafe-house-bonsai",
    category=ObjectCategory.CANON,
    recognition_level=RecognitionLevel.SUBTLE,
    first_appearance=WorldMoment(
        "coffee-cafe",
        "house Bonsai belonging to the café",
    ),
    purpose=("Brings patience, growth, continuity, and life into the diner.",),
    studio_rules=(
        "It belongs to the café and is cared for by the diner. It remains present in "
        "the Coffee Café and is distinct from the coffee pot Beacon."
    ),
    evolution=(
        WorldMoment("coffee-cafe", "house Bonsai with no defined life stage"),
    ),
    continuity_notes=(
        "This is a separate house Bonsai, not the protagonist’s personal tree. Its "
        "life stage is not specified."
    ),
    appearances=(
        WorldMoment("coffee-cafe", "house Bonsai belonging to the café"),
    ),
)

LIBRARY_DESK_LAMP = StudioObject(
    canonical_name="Library Desk Lamp",
    canonical_id="library-desk-lamp",
    category=ObjectCategory.BEACON,
    recognition_level=RecognitionLevel.IMMEDIATE,
    first_appearance=WorldMoment(
        "midnight-library",
        "the only lamp still burning",
    ),
    purpose=(
        "Creates a dependable pool of warmth and tells the returning learner that "
        "their claimed study corner is waiting.",
    ),
    studio_rules=(
        "It belongs to the library rather than the viewer. Its identity and emotional "
        "purpose remain constant. It may age naturally, but it cannot disappear from "
        "the Midnight Library."
    ),
    evolution=(
        WorldMoment(
            "midnight-library",
            "may age naturally while its identity and emotional purpose remain constant",
        ),
    ),
    continuity_notes=(
        "It is the Midnight Library’s Beacon and is distinct from the protagonist’s Bonsai."
    ),
    appearances=(
        WorldMoment("midnight-library", "the only lamp still burning"),
    ),
)

COFFEE_POT = StudioObject(
    canonical_name="Coffee Pot",
    canonical_id="coffee-pot",
    category=ObjectCategory.BEACON,
    recognition_level=RecognitionLevel.IMMEDIATE,
    first_appearance=WorldMoment(
        "coffee-cafe",
        "left on the table and quietly refilled",
    ),
    purpose=("Represents hospitality, fuel, and the feeling of being known.",),
    studio_rules=(
        "It remains on the visitor’s table and is quietly refilled. Its identity and "
        "emotional purpose remain constant. It may age naturally, but it cannot "
        "disappear from the Coffee Café."
    ),
    evolution=(
        WorldMoment(
            "coffee-cafe",
            "may age naturally while remaining on the visitor’s table",
        ),
    ),
    continuity_notes=(
        "It is the Coffee Café’s Beacon and is distinct from the café’s house Bonsai."
    ),
    appearances=(
        WorldMoment("coffee-cafe", "left on the table and quietly refilled"),
    ),
)

CLOSED_LAPTOP_BAG = StudioObject(
    canonical_name="Closed Laptop Bag",
    canonical_id="closed-laptop-bag",
    category=ObjectCategory.BEACON,
    recognition_level=RecognitionLevel.SUBTLE,
    first_appearance=WorldMoment("rainy-loft", "closed and resting by the door"),
    purpose=(
        "Represents work being safely put away and the resident’s permission to rest.",
    ),
    studio_rules=(
        "It remains closed and rests by the door. Its identity and emotional purpose "
        "remain constant. It may age naturally, but it cannot disappear from the "
        "Rainy Loft."
    ),
    evolution=(
        WorldMoment(
            "rainy-loft",
            "may age naturally while remaining closed by the door",
        ),
    ),
    continuity_notes=(
        "It is the Rainy Loft’s Beacon and is distinct from the protagonist’s Bonsai."
    ),
    appearances=(
        WorldMoment("rainy-loft", "closed and resting by the door"),
    ),
)

EARTH = StudioObject(
    canonical_name="Earth",
    canonical_id="earth",
    category=ObjectCategory.BEACON,
    recognition_level=RecognitionLevel.IMMEDIATE,
    first_appearance=WorldMoment(
        "space-station",
        "always visible through the largest viewport",
    ),
    purpose=(
        "Reminds the viewer that no matter how far they travel, home remains visible.",
    ),
    studio_rules=(
        "Earth always remains visible through the Space Station’s largest viewport. "
        "Its identity and emotional purpose remain constant."
    ),
    evolution=(
        WorldMoment("space-station", "remains visible through the largest viewport"),
    ),
    continuity_notes=(
        "Earth is the Space Station’s Beacon and is distinct from the protagonist’s Bonsai."
    ),
    appearances=(
        WorldMoment("space-station", "always visible through the largest viewport"),
    ),
)

RED_PANDA_PLUSH = StudioObject(
    canonical_name="Red Panda Plush",
    canonical_id="red-panda-plush",
    category=ObjectCategory.MEMORY,
    recognition_level=RecognitionLevel.FAMILIAR,
    first_appearance=WorldMoment("midnight-library", "loved study companion"),
    purpose=(
        "Preserves childhood wonder throughout adulthood and carries a quiet piece of "
        "home across the resident’s life.",
    ),
    studio_rules=(
        "It remains present in the Midnight Library. Wear and repair communicate its "
        "history without explanation or emphasis."
    ),
    evolution=(
        WorldMoment("midnight-library", "loved study companion"),
        WorldMoment("space-station", "repaired and worn"),
    ),
    continuity_notes="Physical continuity is not yet established.",
    appearances=(
        WorldMoment("midnight-library", "loved study companion"),
        WorldMoment("space-station", "repaired and worn"),
    ),
)

COLLEGE_LAPTOP = StudioObject(
    canonical_name="College Laptop",
    canonical_id="college-laptop",
    category=ObjectCategory.TOOL,
    recognition_level=RecognitionLevel.FAMILIAR,
    first_appearance=WorldMoment("midnight-library", "worn student laptop"),
    purpose=(
        "Records the resident’s transition from student life into professional life "
        "through accumulated wear and use.",
    ),
    studio_rules=(
        "It should feel used rather than newly purchased. Wear and stickers communicate "
        "history more naturally than explanatory text."
    ),
    evolution=(
        WorldMoment("midnight-library", "worn student laptop"),
        WorldMoment("coffee-cafe", "carried forward with more stickers and wear"),
    ),
    continuity_notes=(
        "The Coffee Café laptop is the same laptop carried forward from college. No "
        "later appearance is currently defined."
    ),
    appearances=(
        WorldMoment("midnight-library", "worn student laptop"),
        WorldMoment("coffee-cafe", "carried forward, more stickered and worn"),
    ),
)

TAPE_DECK = StudioObject(
    canonical_name="Tape Deck",
    canonical_id="tape-deck",
    category=ObjectCategory.MEMORY,
    recognition_level=RecognitionLevel.SUBTLE,
    first_appearance=WorldMoment(
        "midnight-library",
        "connected to the learner’s headset",
    ),
    purpose=(
        "Represents technology whose emotional value has outlived its practical value, "
        "connecting the resident’s listening habits across different stages of life.",
    ),
    studio_rules=(
        "Age, scratches, and continued use carry its history. It remains a purposeful "
        "listening object rather than decorative nostalgia."
    ),
    evolution=(
        WorldMoment("midnight-library", "connected to the learner’s headset"),
        WorldMoment("rainy-loft", "older and scratched"),
    ),
    continuity_notes="Physical continuity is not yet established.",
    appearances=(
        WorldMoment("midnight-library", "connected to the learner’s headset"),
        WorldMoment("rainy-loft", "older and scratched"),
    ),
)

EVOLVING_BACKPACK = StudioObject(
    canonical_name="Evolving Backpack",
    canonical_id="evolving-backpack",
    category=ObjectCategory.IDENTITY,
    recognition_level=RecognitionLevel.FAMILIAR,
    first_appearance=WorldMoment(
        "midnight-library",
        "evolving through stickers, study marks, and repeated visits",
    ),
    purpose=(
        "Carries the weight of learning, work, travel, and personal history without "
        "ever drawing attention to itself.",
    ),
    studio_rules=(
        "It evolves through accumulated evidence rather than explanatory messaging. "
        "Changes must feel gradual and lived in."
    ),
    evolution=(
        WorldMoment(
            "midnight-library",
            "accumulates stickers, study marks, wear, and evidence of repeated visits",
        ),
    ),
    continuity_notes="A later appearance is not yet defined.",
    appearances=(
        WorldMoment(
            "midnight-library",
            "evolving through stickers, study marks, and repeated visits",
        ),
    ),
)

MECH_FIGURE_AND_MEMENTOS = StudioObject(
    canonical_name="Mech Figure and Mementos",
    canonical_id="mech-mementos",
    category=ObjectCategory.IDENTITY,
    recognition_level=RecognitionLevel.HIDDEN,
    first_appearance=WorldMoment("hacker-apartment", "mech figure"),
    purpose=(
        "Quietly reveals a personal interest that remains meaningful after the "
        "resident’s years of building and ambition.",
    ),
    studio_rules=(
        "These objects remain subtle and reward careful observation. They must not "
        "compete with the primary focal point or become overt exposition."
    ),
    evolution=(
        WorldMoment("hacker-apartment", "mech figure"),
        WorldMoment("rainy-loft", "subtle mech mementos"),
    ),
    continuity_notes=(
        "Physical continuity is not yet established. Continuity currently ends in "
        "the Rainy Loft."
    ),
    appearances=(
        WorldMoment("hacker-apartment", "mech figure"),
        WorldMoment("rainy-loft", "subtle mech mementos"),
    ),
)

DINER_MUG = StudioObject(
    canonical_name="Diner Mug",
    canonical_id="diner-mug",
    category=ObjectCategory.MEMORY,
    recognition_level=RecognitionLevel.HIDDEN,
    first_appearance=WorldMoment("space-station", "quiet keepsake from the diner"),
    purpose=(
        "Serves as a keepsake from Earth and a quiet reference to a previous place.",
    ),
    studio_rules=(
        "It should read as an ordinary used possession rather than a displayed symbol. "
        "It remains a subtle reward for observant viewers."
    ),
    evolution=(
        WorldMoment("space-station", "diner mug kept among objects from Earth"),
    ),
    continuity_notes=(
        "Its Space Station appearance references the Coffee Café, but an earlier "
        "on-screen appearance of this physical mug is not yet established."
    ),
    appearances=(
        WorldMoment("space-station", "quiet keepsake from the diner"),
    ),
)


ALL_OBJECTS = (
    PROTAGONIST_BONSAI,
    COFFEE_CAFE_HOUSE_BONSAI,
    LIBRARY_DESK_LAMP,
    COFFEE_POT,
    CLOSED_LAPTOP_BAG,
    EARTH,
    RED_PANDA_PLUSH,
    COLLEGE_LAPTOP,
    TAPE_DECK,
    EVOLVING_BACKPACK,
    MECH_FIGURE_AND_MEMENTOS,
    DINER_MUG,
)

OBJECTS_BY_ID: Mapping[str, StudioObject] = MappingProxyType(
    {studio_object.canonical_id: studio_object for studio_object in ALL_OBJECTS}
)
