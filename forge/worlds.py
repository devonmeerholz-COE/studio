"""The five canonical Super Chilled Studio worlds."""

from types import MappingProxyType
from typing import Mapping

from forge.world import Beacon, BonsaiRelationship, Era, Soundscape, World


HACKER_APARTMENT = World(
    stable_key="hacker-apartment",
    canonical_name="The Hacker Apartment",
    catalog_number=1,
    chronological_stage=3,
    era=Era(
        (
            "Neo-Tokyo",
            "2056",
            "The working professional pursuing independent creative ambitions after hours.",
        )
    ),
    purpose=(
        "A private sanctuary where an engineer or IT professional builds the project, "
        "game, application, or future that belongs to them rather than an institution."
    ),
    resident_identity="You are the independent builder.",
    emotional_core=("Freedom, ownership, determination, possibility, hope.",),
    first_impression="Rain dances across the glass while the city glows beneath you.",
    leaving_this_world=("Inspired to build.",),
    setting=(
        "A compact high-rise apartment in a culturally merged American/Japanese "
        "metropolis. Always nighttime, usually rainy and occasionally stormy. The "
        "fixed viewpoint faces the desk; the exterior city remains softened and "
        "secondary."
    ),
    beacon=Beacon(
        identity="The protagonist’s Bonsai.",
        emotional_purpose=(
            "It represents patience, disciplined growth, life within the artificial "
            "city, and home."
        ),
        natural_aging=(
            "It may age naturally, but its identity and emotional purpose remain "
            "constant."
        ),
    ),
    bonsai_relationship=BonsaiRelationship(
        identity="The protagonist’s Bonsai.",
        life_stage="Young.",
        beacon_relationship="It is also this world’s Beacon.",
    ),
    soundscape=Soundscape(
        music=(
            "Neo-Tokyo Synthwave; Eastern-influenced electronic textures, analogue "
            "synth warmth, no vocals."
        ),
        ambient_world=(
            "Rain against the apartment and the occasional presence of a storm beyond "
            "the glass."
        ),
        silence="Private, focused, and full of possibility.",
    ),
    personal_artifacts=(
        "CRT monitor, futuristic laptop, mechanical keyboards, wired mouse, VR "
        "headset, handwritten notebook, espresso machine, mech figure.",
    ),
    passage_of_time=(
        "Technology changes. Keyboards change. Notebook contents accumulate. Room "
        "décor evolves. The Bonsai grows."
    ),
    immutable_elements=(
        "The chair remains empty because the viewer is the hacker. The camera remains "
        "stationary. The Bonsai remains present. The desk remains the visual center.",
    ),
)


MIDNIGHT_LIBRARY = World(
    stable_key="midnight-library",
    canonical_name="The Midnight Library",
    catalog_number=2,
    chronological_stage=1,
    era=Era(("The Grand Library", "Neo-Tokyo", "2056", "The student years.")),
    purpose=(
        "A dependable sanctuary away from a crowded home or cramped apartment where "
        "the learner prepares for tests, projects, and the future."
    ),
    resident_identity="You are the lifelong learner.",
    emotional_core=(
        "Solace, quiet determination, belonging, motivation, hope.",
    ),
    first_impression="The only lamp still burning is waiting for you.",
    leaving_this_world=("Prepared.", "Capable.", "Hopeful."),
    setting=(
        "The Grand Library in the same city. Classical architecture is preserved "
        "within the future. It is visited during late nights and early mornings in "
        "fall and winter. A small distant window shows only hints of rain, snow, or "
        "wind. The fixed viewpoint faces the learner’s claimed desk within the larger "
        "library."
    ),
    beacon=Beacon(
        identity="The library desk lamp.",
        emotional_purpose=(
            "It belongs to the library rather than the viewer and creates a dependable "
            "pool of warmth."
        ),
        natural_aging=(
            "It may age naturally, but its identity and emotional purpose remain "
            "constant."
        ),
    ),
    bonsai_relationship=BonsaiRelationship(
        identity="The protagonist’s Bonsai.",
        life_stage="Its earliest life stage.",
        beacon_relationship="It is distinct from the library desk lamp.",
    ),
    soundscape=Soundscape(
        music=(
            "Chilled piano, neo-classical orchestral music, and restrained gothic "
            "choral textures. No distracting percussion or vocals."
        ),
        ambient_world=(
            "Faint rain, snow, or wind reaches the claimed desk from the distant "
            "window."
        ),
        silence=(
            "Sheltering, attentive, and shared with everyone who has studied here "
            "after hours."
        ),
    ),
    personal_artifacts=(
        "Red panda plush, worn laptop, headset connected to a tape deck, evolving "
        "backpack, textbooks, library books, instant noodles, takeaway packaging, "
        "bright energy drink.",
    ),
    passage_of_time=(
        "The backpack and its stickers evolve. Study marks accumulate. More books "
        "gather around the desk. Repeated visits leave evidence. The Bonsai grows."
    ),
    immutable_elements=(
        "The claimed study corner remains. The desk lamp remains. The red panda plush "
        "remains. The camera remains stationary. The library remains a sanctuary.",
    ),
    motto="Knowledge is earned after everyone else goes home.",
)


COFFEE_CAFE = World(
    stable_key="coffee-cafe",
    canonical_name="The Coffee Café",
    catalog_number=3,
    chronological_stage=2,
    era=Era(
        (
            "The Coffee Café",
            "Neo-Tokyo",
            "2056",
            "Newly graduated and beginning a professional life.",
        )
    ),
    purpose=(
        "A welcoming third place for meetings, quick work, food, caffeine, and renewed "
        "energy while the city continues outside."
    ),
    resident_identity="You are the travelling professional.",
    emotional_core=("Optimism, connection, motivation, focus, welcome.",),
    first_impression="Someone has already poured your coffee.",
    leaving_this_world=("Energised.", "Connected."),
    setting=(
        "A retro-futuristic 1950s-inspired diner downstairs in the same city. It is "
        "daylight only, primarily during fall and winter. Pastel pinks, blues, "
        "yellows, cream, and chrome define the space. The fixed viewpoint occupies "
        "the familiar booth beside the window while pedestrians, bicycles, leaves, "
        "and distant flying traffic move outside."
    ),
    beacon=Beacon(
        identity="The coffee pot left on the table and quietly refilled.",
        emotional_purpose="It represents hospitality, fuel, and being known.",
        natural_aging=(
            "It may age naturally, but its identity and emotional purpose remain "
            "constant."
        ),
    ),
    bonsai_relationship=BonsaiRelationship(
        identity=(
            "A separate house Bonsai belonging to the café, not the protagonist’s "
            "personal tree."
        ),
        life_stage="Not specified.",
        beacon_relationship="It is distinct from the coffee pot.",
    ),
    soundscape=Soundscape(
        music=(
            "Neo Americana—vintage guitar, soft saxophone, electric piano, brush "
            "drums, and restrained futuristic synth accents."
        ),
        ambient_world=(
            "Friendly human activity inside while pedestrians, bicycles, leaves, and "
            "distant flying traffic pass outside."
        ),
        silence="A comfortable pause within a city that keeps moving.",
    ),
    personal_artifacts=(
        "Napkin dispenser, jukebox, diner booth, stickered and worn laptop carried "
        "forward from college, condiments, placemat, cutlery, breakfast or lunch.",
    ),
    passage_of_time=(
        "The menu changes. Clientele changes. Décor evolves. Weather passes beyond "
        "the window. The laptop gathers wear. Small details in the diner change while "
        "the familiar place remains."
    ),
    immutable_elements=(
        "The visitor’s booth remains. The coffee pot remains. The café Bonsai remains. "
        "The camera remains stationary. The atmosphere of friendly human activity "
        "remains.",
    ),
    motto="The world keeps moving. Your moment does not have to.",
    naming_note=(
        "The diner remains unnamed for now. The audience may eventually name it."
    ),
)


RAINY_LOFT = World(
    stable_key="rainy-loft",
    canonical_name="The Rainy Loft",
    catalog_number=4,
    chronological_stage=4,
    era=Era(
        (
            "The Rainy Loft",
            "Later adulthood",
            "After the years of chasing and building.",
        )
    ),
    purpose=(
        "A personal sanctuary where the resident switches off, pursues restful "
        "hobbies, reads, listens, and remembers that nothing must be proven tonight."
    ),
    resident_identity=(
        "You are the older and wiser resident who has learned to protect time for "
        "rest."
    ),
    emotional_core=("Contentment, peace, gratitude, calm, earned quiet.",),
    first_impression="The rain has already started.",
    leaving_this_world=("Rested.", "Peaceful."),
    setting=(
        "A comfortable loft home overlooking a large city park. Late afternoon moves "
        "toward sunset. The space is cool and cozy in any season and often gently "
        "rainy. The fixed viewpoint faces a floor lounge or comfortable couch rather "
        "than a work desk. The city remains present, but nature is finally audible."
    ),
    beacon=Beacon(
        identity="The closed laptop bag resting by the door.",
        emotional_purpose="It represents work being safely put away.",
        natural_aging=(
            "It may age naturally, but its identity and emotional purpose remain "
            "constant."
        ),
    ),
    bonsai_relationship=BonsaiRelationship(
        identity="The protagonist’s same Bonsai.",
        life_stage="Mature, larger, and proudly displayed.",
        beacon_relationship="It is distinct from the closed laptop bag.",
    ),
    soundscape=Soundscape(
        music=(
            "Lo-fi with tape warmth, minimal piano, gentle rain, and no productivity "
            "pressure."
        ),
        ambient_world=(
            "Gentle rain and the sounds of nature from the large city park."
        ),
        silence=(
            "Restful, unhurried, and free from the need to prove anything."
        ),
    ),
    personal_artifacts=(
        "Older scratched tape deck, teapot and unusual tea flavors, books, headphones, "
        "floor cushions, obscured diploma, subtle mech mementos.",
    ),
    passage_of_time=(
        "The Bonsai grows. The tape deck ages. Memories accumulate. The park changes "
        "with the seasons. Familiar belongings become worn."
    ),
    immutable_elements=(
        "Permission to rest remains. The park-facing window remains. The closed work "
        "bag remains. The camera remains stationary. The mature Bonsai remains.",
    ),
    motto="You have earned this quiet.",
)


SPACE_STATION = World(
    stable_key="space-station",
    canonical_name="The Space Station",
    catalog_number=5,
    chronological_stage=5,
    era=Era(
        (
            "Space Station Chill",
            "Low Earth Orbit",
            "2096",
            "Later life and a renewed adventure.",
        )
    ),
    purpose=(
        "A new chapter driven by curiosity, discovery, and renewed purpose rather "
        "than obligation or grinding."
    ),
    resident_identity=(
        "You are the lifelong learner who became a master and has chosen to become an "
        "explorer again."
    ),
    emotional_core=("Inspiration, gratitude, curiosity, motivation, hope.",),
    first_impression="Earth has been waiting outside the window all along.",
    leaving_this_world=("Curious.", "Optimistic.", "Full of possibility."),
    setting=(
        "Space Station Chill in low Earth orbit. Its grounded, recognizable "
        "retro-futuristic design is influenced by practical 1970s space aesthetics. "
        "Cold blues, greys, silver, and subdued white surround a small comfortable "
        "nook beside the station’s largest viewport. The stationary viewpoint faces "
        "Earth.\n\n"
        "The station feels more like a quiet orbital lighthouse than a sterile "
        "laboratory."
    ),
    beacon=Beacon(
        identity="Earth.",
        emotional_purpose=(
            "It represents home, origin, perspective, and everything worth protecting."
        ),
        natural_aging="Its identity and emotional purpose remain constant.",
    ),
    bonsai_relationship=BonsaiRelationship(
        identity="The protagonist’s same Bonsai.",
        life_stage="Old, wise, larger, and carefully sustained.",
        beacon_relationship="It is distinct from Earth.",
    ),
    soundscape=Soundscape(
        music=(
            "Hopeful future electronica with atmospheric pads, gentle pulses, and no "
            "aggressive techno elements."
        ),
        ambient_world=(
            "The quiet environment of Space Station Chill in low Earth orbit."
        ),
        silence="Expansive, reflective, and full of possibility.",
    ),
    personal_artifacts=(
        "Repaired and worn red panda plush, blue holographic tablet, energy drink, "
        "diner mug, keepsakes from Earth, references to previous places.",
    ),
    passage_of_time=(
        "The Bonsai continues to age. Mission information and destination names "
        "change. Signs of exploration appear. Keepsakes accumulate."
    ),
    immutable_elements=(
        "Earth remains visible. The red panda remains present. Humanity and hope remain "
        "central. The camera remains stationary.",
    ),
)


ALL_WORLDS = (
    HACKER_APARTMENT,
    MIDNIGHT_LIBRARY,
    COFFEE_CAFE,
    RAINY_LOFT,
    SPACE_STATION,
)

WORLDS_BY_KEY: Mapping[str, World] = MappingProxyType(
    {world.stable_key: world for world in ALL_WORLDS}
)
