"""
odu_data.py — Ifá Oracle: Data for the 16 Principal Odu (Meji)

Each Odu is represented by a 4-mark figure.  In Ifá, each arm of the Ọ̀pẹ̀lẹ̀
casting chain shows either a single mark (I, representing an odd count) or a
double mark (II, representing an even count).  The 16 principal Odu (called
Meji, meaning "double") have identical left and right columns.

Cultural note: This data is provided for educational and cultural-appreciation
purposes only.  Traditional Ifá knowledge is vast, oral, and sacred.  The
information here is a simplified academic overview.  For authentic divination,
consult a qualified Babalawo.
"""

from dataclasses import dataclass, field
from typing import List, Tuple


# ---------------------------------------------------------------------------
# Mark symbols
# ---------------------------------------------------------------------------
SINGLE = "  |  "   # I  – odd  – represents 1
DOUBLE = " | | "   # II – even – represents 0


@dataclass
class Odu:
    """Represents one of the 16 principal Ifá Odu (Meji)."""

    # --- Identity ---
    number: int                        # 1–16 in traditional ordering
    yoruba_name: str                   # e.g. "Ogbe" / "Ejiogbe"
    meji_name: str                     # Full Meji name
    english_name: str                  # Approximate English translation
    alternate_spellings: List[str]     # Common variant spellings

    # --- Visual figure ---
    # 4-element tuple of True (single / I) or False (double / II)
    marks: Tuple[bool, bool, bool, bool]

    # --- Core meaning ---
    primary_meaning: str               # One-sentence essence
    themes: List[str]                  # Key life areas (health, wealth, etc.)
    positive_aspects: List[str]
    challenges: List[str]

    # --- Narrative & wisdom ---
    story_summary: str                 # Brief ẹsẹ / teaching story summary
    moral_teaching: str                # Core ethical lesson
    advice: str                        # Practical guidance

    # --- Ebo (offering) guidance ---
    ebo_suggestion: str                # Simplified ebo; always note caveat
    ebo_caveat: str = (
        "⚠️  Ebo guidance here is simplified for educational purposes only. "
        "Actual ebo prescription requires consultation with a qualified Babalawo."
    )

    # --- Ruling Orisha & associations ---
    orisha: str = ""                   # Primary associated Orisha
    colors: List[str] = field(default_factory=list)
    numbers: List[int] = field(default_factory=list)

    def figure_lines(self) -> List[str]:
        """Return the 4 lines of the Odu figure as a list of strings.

        Each line shows the left and right columns (identical for Meji)
        separated by a space.
        """
        lines = []
        for mark in self.marks:
            sym = SINGLE if mark else DOUBLE
            lines.append(f"{sym}   {sym}")
        return lines

    def figure_str(self) -> str:
        """Return the full figure as a single multi-line string."""
        return "\n".join(self.figure_lines())


# ---------------------------------------------------------------------------
# The 16 Principal Odu (Meji) — Traditional ordering
# ---------------------------------------------------------------------------
# Mark encoding: True = single (|), False = double (| |)

ODU_LIST: List[Odu] = [
    # 1 ─────────────────────────────────────────────────────────────────────
    Odu(
        number=1,
        yoruba_name="Ogbe",
        meji_name="Ejiogbe",
        english_name="The Fullness of Light",
        alternate_spellings=["Ogbe", "Ogbè", "Eji-Ogbe"],
        marks=(True, True, True, True),  # | | | |  all singles
        primary_meaning=(
            "Ejiogbe is the first and most luminous of all Odu, representing "
            "the dawn of creation, divine light, and the fullness of blessings."
        ),
        themes=["beginnings", "light", "life", "abundance", "leadership", "spirituality"],
        positive_aspects=[
            "New beginnings and fresh starts",
            "Abundance and prosperity",
            "Spiritual clarity and divine favour",
            "Victory over adversaries",
            "Long life and good health",
        ],
        challenges=[
            "Pride and arrogance can undermine blessings",
            "Overconfidence may lead to neglect of spiritual duties",
        ],
        story_summary=(
            "In the beginning Orunmila cast Ejiogbe and saw the entire world "
            "bathed in light. The odu teaches that when Olodumare sent the "
            "sixteen original Odu to Earth, Ejiogbe led them, carrying the "
            "torch of divine knowledge.  It reminds us that life begins in "
            "light and that every new dawn is a gift to be received with "
            "gratitude and humility."
        ),
        moral_teaching=(
            "Gratitude opens the door to abundance. Do not let success breed "
            "arrogance; the greatest light casts no shadow on others."
        ),
        advice=(
            "This is a time of new beginnings and great potential. Move "
            "forward with confidence, but remain humble and give thanks. "
            "Offer prayers at dawn and honour your ancestors."
        ),
        ebo_suggestion=(
            "White cloth, white kola nuts (obi abata), and fresh water offered "
            "to Obatala or at a crossroads at dawn."
        ),
        orisha="Obatala",
        colors=["white", "gold"],
        numbers=[1, 8],
    ),

    # 2 ─────────────────────────────────────────────────────────────────────
    Odu(
        number=2,
        yoruba_name="Oyeku",
        meji_name="Oyeku Meji",
        english_name="The Darkness Before Renewal",
        alternate_spellings=["Oyèkú", "Oyeku", "Eji-Oko"],
        marks=(False, False, False, False),  # || || || ||  all doubles
        primary_meaning=(
            "Oyeku Meji governs death, endings, transformation, and the "
            "passage from one state of being to another.  It is not a sign "
            "of misfortune but of profound transition."
        ),
        themes=["death", "transformation", "ancestors", "endings", "rebirth", "mystery"],
        positive_aspects=[
            "Liberation from what no longer serves",
            "Deep ancestral connection and wisdom",
            "Profound spiritual transformation",
            "Completion of cycles",
        ],
        challenges=[
            "Fear of endings or change",
            "Neglect of ancestral veneration",
            "Stagnation through refusal to let go",
        ],
        story_summary=(
            "Oyeku came to Earth wearing a dark cloak and was feared by all. "
            "Yet the Babalawo who consulted Ifá learned that Oyeku brings not "
            "destruction but the sacred darkness from which new life emerges — "
            "as the seed must be buried before it can sprout. Orunmila himself "
            "went through Oyeku's gate and returned, proving that death is not "
            "the end but a transformation."
        ),
        moral_teaching=(
            "Honour endings as you honour beginnings. The ancestors who have "
            "gone before you are a source of strength, not sorrow."
        ),
        advice=(
            "Something in your life is completing its cycle. Release it with "
            "grace. Connect with your ancestors through prayer and remembrance. "
            "This is a time for reflection, not new ventures."
        ),
        ebo_suggestion=(
            "Black-eyed beans (ewa), palm wine, and a candle placed at the "
            "ancestral shrine (egungun) or at a grave."
        ),
        orisha="Egungun / Oya",
        colors=["black", "white"],
        numbers=[2, 9],
    ),

    # 3 ─────────────────────────────────────────────────────────────────────
    Odu(
        number=3,
        yoruba_name="Iwori",
        meji_name="Iwori Meji",
        english_name="The Inner Vision",
        alternate_spellings=["Ìwòrì", "Iwori"],
        marks=(False, False, True, True),  # || || | |
        primary_meaning=(
            "Iwori Meji is the Odu of inner sight, introspection, and the "
            "hidden knowledge that resides within the heart. It governs "
            "secrets, the subconscious, and deep spiritual perception."
        ),
        themes=["inner wisdom", "secrets", "intuition", "introspection", "hidden matters"],
        positive_aspects=[
            "Deep intuitive insight",
            "Ability to perceive hidden truths",
            "Strong connection to inner guidance",
            "Wisdom gained through self-reflection",
        ],
        challenges=[
            "Tendency toward secrecy and isolation",
            "Inner conflicts and self-doubt",
            "Difficulty trusting others",
        ],
        story_summary=(
            "Iwori came to Earth looking inward rather than outward and was "
            "mocked for seeming to ignore the world. Yet when crisis came, "
            "only Iwori knew the hidden path to safety, for the answers were "
            "always within. The odu teaches that the greatest journeys are "
            "those taken into one's own heart."
        ),
        moral_teaching=(
            "The answers you seek are already within you. Quiet the noise of "
            "the world and listen to the still voice of Ori (inner self)."
        ),
        advice=(
            "Trust your intuition above external voices. Spend time in quiet "
            "reflection. Be mindful of secrets — both keeping and revealing them."
        ),
        ebo_suggestion=(
            "Honey, white cloth, and a personal item placed before Ori "
            "(one's personal spiritual essence)."
        ),
        orisha="Ori / Obatala",
        colors=["white", "silver"],
        numbers=[3, 6],
    ),

    # 4 ─────────────────────────────────────────────────────────────────────
    Odu(
        number=4,
        yoruba_name="Odi",
        meji_name="Odi Meji",
        english_name="The Womb of Creation",
        alternate_spellings=["Òdí", "Odi"],
        marks=(True, True, False, False),  # | | || ||
        primary_meaning=(
            "Odi Meji rules the womb, fertility, hidden things, the belly, "
            "and all matters of creation and gestation. It also governs "
            "concealment, witchcraft defence, and the power of the feminine."
        ),
        themes=["fertility", "creation", "pregnancy", "hidden dangers", "protection", "femininity"],
        positive_aspects=[
            "Fertility and new creative endeavours",
            "Protection from hidden enemies",
            "Abundance in family and community",
            "Strength of character",
        ],
        challenges=[
            "Hidden opposition or betrayal",
            "Issues related to the stomach or reproductive health",
            "Concealed problems that must be brought to light",
        ],
        story_summary=(
            "Odi went to Earth as a silent keeper of secrets. She taught that "
            "the most powerful things grow quietly in the dark — as the child "
            "grows in the womb unseen. Those who tried to expose her secrets "
            "prematurely were warned: some things must be revealed only in "
            "their own time."
        ),
        moral_teaching=(
            "Respect the creative process. Not everything must be spoken "
            "immediately; allow things to develop in their right season."
        ),
        advice=(
            "There are unseen factors at play. Be patient; what is being "
            "created will be revealed at the right time. Protect yourself "
            "from hidden negativity."
        ),
        ebo_suggestion=(
            "Plantain, palm oil, and a calabash of water offered at a "
            "body of water or at home."
        ),
        orisha="Yemoja / Osun",
        colors=["blue", "white"],
        numbers=[4, 7],
    ),

    # 5 ─────────────────────────────────────────────────────────────────────
    Odu(
        number=5,
        yoruba_name="Irosun",
        meji_name="Irosun Meji",
        english_name="The Flow of Life Blood",
        alternate_spellings=["Ìròsùn", "Irosun", "Rosun"],
        marks=(True, False, True, True),  # | || | |
        primary_meaning=(
            "Irosun Meji governs blood, life force, medicine, and the "
            "transmission of vital energy.  It is associated with healing, "
            "menstruation, sacrifice, and the continuity of lineage."
        ),
        themes=["health", "healing", "blood", "medicine", "lineage", "sacrifice"],
        positive_aspects=[
            "Physical vitality and good health",
            "Healing and recovery",
            "Strong family bloodline",
            "Success in medicine and herbal work",
        ],
        challenges=[
            "Illnesses related to blood or internal organs",
            "Family disputes over inheritance",
            "Excessive loss — of blood, energy, or resources",
        ],
        story_summary=(
            "Irosun wore red and carried the knowledge of life's most "
            "precious fluid. The odu taught that blood binds families across "
            "generations and that the healer who respects the body's sacred "
            "river can cure what others cannot. Waste not what is vital."
        ),
        moral_teaching=(
            "Life force is precious. Protect your health and the health of "
            "those in your care. Honour the sacrifice of those who bled "
            "so you could live."
        ),
        advice=(
            "Pay attention to your physical health. This is a good time for "
            "healing practices. Honour your family lineage and ancestors."
        ),
        ebo_suggestion=(
            "Red palm oil, camwood (osun) powder, and kola nuts offered "
            "at the family shrine or ancestral altar."
        ),
        orisha="Osun / Sopona",
        colors=["red", "coral"],
        numbers=[5, 9],
    ),

    # 6 ─────────────────────────────────────────────────────────────────────
    Odu(
        number=6,
        yoruba_name="Owonrin",
        meji_name="Owonrin Meji",
        english_name="The Unpredictable Wind",
        alternate_spellings=["Òwónrín", "Owonrin", "Wonrin"],
        marks=(False, True, False, False),  # || | || ||
        primary_meaning=(
            "Owonrin Meji embodies chaos, sudden change, unpredictability, "
            "and the wild creative energy that disrupts in order to renew. "
            "It is the Odu of lightning, Sango's domain."
        ),
        themes=["change", "unpredictability", "chaos", "creativity", "lightning", "disruption"],
        positive_aspects=[
            "Sudden positive reversals of fortune",
            "Creative breakthroughs and innovation",
            "Speed and agility in overcoming problems",
            "Divine intervention in difficult situations",
        ],
        challenges=[
            "Instability and erratic behaviour",
            "Hasty decisions with unforeseen consequences",
            "Conflicts and quarrels",
        ],
        story_summary=(
            "Owonrin danced wildly and could not be still. The other Odu "
            "complained, but when the storm came it was Owonrin who knew "
            "every escape route, for chaos is also the seed of creativity. "
            "Orunmila said: the one who can ride the wind will go further "
            "than the one who fears it."
        ),
        moral_teaching=(
            "Embrace necessary change rather than clinging to the familiar. "
            "Chaos is often the doorway to a better order."
        ),
        advice=(
            "Expect the unexpected and stay flexible. Do not resist the "
            "changes coming your way — they may be the answer to your prayers."
        ),
        ebo_suggestion=(
            "Bitter kola (obi ata), red palm oil, and rum or gin offered "
            "at a crossroads or to Sango."
        ),
        orisha="Sango / Eshu",
        colors=["red", "white"],
        numbers=[6, 12],
    ),

    # 7 ─────────────────────────────────────────────────────────────────────
    Odu(
        number=7,
        yoruba_name="Obara",
        meji_name="Obara Meji",
        english_name="The Royalty of Ogun",
        alternate_spellings=["Òbàrà", "Obara"],
        marks=(True, True, True, False),  # | | | ||
        primary_meaning=(
            "Obara Meji is the Odu of royalty, majesty, wealth, and "
            "eloquence. It governs leadership, generosity, and the splendour "
            "of one who carries themselves with dignified authority."
        ),
        themes=["wealth", "leadership", "royalty", "generosity", "fame", "prestige"],
        positive_aspects=[
            "Great wealth and material success",
            "Natural leadership and authority",
            "Charisma and eloquence",
            "Generosity that attracts more blessings",
        ],
        challenges=[
            "Arrogance and boastfulness",
            "Extravagance leading to financial difficulties",
            "Pride preventing the receipt of help",
        ],
        story_summary=(
            "Obara walked into town dressed as a king though he had nothing. "
            "The townspeople, impressed by his bearing, gave him gifts — and "
            "by the day's end he truly was a king. Ifá teaches through Obara "
            "that dignity and generosity attract abundance."
        ),
        moral_teaching=(
            "Carry yourself with dignity regardless of your circumstances. "
            "Generosity is the crown that earns more than it gives away."
        ),
        advice=(
            "Present yourself with confidence and grace. Share your resources "
            "generously — abundance flows toward the generous heart. Leadership "
            "opportunities may be near."
        ),
        ebo_suggestion=(
            "Yellow fabric, honey, cowries, and brass ornaments offered "
            "to Osun or placed at a prosperous crossroads."
        ),
        orisha="Osun / Ogun",
        colors=["yellow", "gold", "green"],
        numbers=[7, 14],
    ),

    # 8 ─────────────────────────────────────────────────────────────────────
    Odu(
        number=8,
        yoruba_name="Okanran",
        meji_name="Okanran Meji",
        english_name="The Spark of Conflict",
        alternate_spellings=["Òkànràn", "Okanran"],
        marks=(False, False, False, True),  # || || || |
        primary_meaning=(
            "Okanran Meji rules sudden conflicts, confrontations, unexpected "
            "events, and the fierce energy that both destroys and clears the "
            "way for new growth. It is associated with fire and iron."
        ),
        themes=["conflict", "fire", "sudden events", "courage", "clearing obstacles"],
        positive_aspects=[
            "The courage to confront what must be faced",
            "Sudden resolution of long-standing problems",
            "Strength and determination",
            "Clearing of obstacles",
        ],
        challenges=[
            "Hot temper and impulsive actions",
            "Accidents, particularly involving sharp objects or fire",
            "Quarrels and legal disputes",
        ],
        story_summary=(
            "Okanran arrived unexpectedly, like a spark landing in dry grass. "
            "Destruction followed — yet in the ashes farmers found the "
            "richest soil they had ever seen. Ifá teaches: every conflict "
            "carries within it the seeds of resolution and renewal."
        ),
        moral_teaching=(
            "Not every battle is yours to fight, but some conflicts must be "
            "faced with courage. Know the difference between recklessness "
            "and necessary confrontation."
        ),
        advice=(
            "Be mindful of your temper and avoid unnecessary arguments. If "
            "conflict is unavoidable, face it with calm courage. Guard "
            "against accidents, especially with fire and sharp instruments."
        ),
        ebo_suggestion=(
            "Iron implements, palm oil, and kolanuts offered to Ogun "
            "at the base of an iron object or at a forge."
        ),
        orisha="Ogun / Sango",
        colors=["green", "black", "red"],
        numbers=[8, 3],
    ),

    # 9 ─────────────────────────────────────────────────────────────────────
    Odu(
        number=9,
        yoruba_name="Ogunda",
        meji_name="Ogunda Meji",
        english_name="The Path-Opener",
        alternate_spellings=["Ògúndá", "Ogunda", "Ogunda"],
        marks=(True, False, True, False),  # | || | ||
        primary_meaning=(
            "Ogunda Meji is Ogun's own Odu, governing the clearing of paths, "
            "iron, technology, medicine through surgery, and the warrior "
            "spirit that cuts through all obstacles."
        ),
        themes=["paths", "obstacles", "iron", "surgery", "travel", "strength", "medicine"],
        positive_aspects=[
            "Clearing of blocked paths and opportunities",
            "Physical strength and recovery",
            "Success in medicine, surgery, and technology",
            "Protection in travel and ventures",
        ],
        challenges=[
            "Aggression and brutality if energy is not channelled wisely",
            "Injuries from sharp objects or accidents in transit",
            "Difficulty accepting help from others",
        ],
        story_summary=(
            "When the Orisha first came to Earth the path was overgrown and "
            "impassable. Ogun took his cutlass and cleared the way for all "
            "of them. Ogunda teaches that the warrior does not fight for "
            "glory but to open the path for those who follow."
        ),
        moral_teaching=(
            "Use your strength in service of others. Clear the path not only "
            "for yourself but for your community."
        ),
        advice=(
            "Blocked paths are about to open. Move forward with determination. "
            "If you face surgery or a medical procedure, this Odu offers "
            "protection. Honour Ogun before important journeys."
        ),
        ebo_suggestion=(
            "A dog, palm wine, and roasted yam offered to Ogun at a "
            "crossroads or at the base of a palm tree. (Note: animal "
            "offerings require proper ritual context.)"
        ),
        orisha="Ogun",
        colors=["green", "black"],
        numbers=[3, 7],
    ),

    # 10 ────────────────────────────────────────────────────────────────────
    Odu(
        number=10,
        yoruba_name="Osa",
        meji_name="Osa Meji",
        english_name="The Storm of Transformation",
        alternate_spellings=["Òsá", "Osa"],
        marks=(False, True, False, True),  # || | || |
        primary_meaning=(
            "Osa Meji is a powerful and revolutionary Odu associated with "
            "the storm, female power, spiritual rebellion, and the sudden "
            "overturning of unjust situations."
        ),
        themes=["revolution", "female power", "storms", "upheaval", "justice", "healing"],
        positive_aspects=[
            "Overturning oppressive situations",
            "Powerful healing and spiritual protection",
            "Leadership of women and the marginalised",
            "Sudden elevation in status",
        ],
        challenges=[
            "Volatile emotions and explosive confrontations",
            "Opposition from powerful forces",
            "Health crises that demand urgent attention",
        ],
        story_summary=(
            "Osa was once enslaved and mocked. But Osa prayed, worked, and "
            "endured. When the storm she called finally arrived, every chain "
            "broke and every oppressor fled. Ifá teaches through Osa that "
            "the most powerful transformation often follows the deepest trial."
        ),
        moral_teaching=(
            "Endure with dignity; the storm that tests you is also the storm "
            "that sets you free. Never give up at the threshold of liberation."
        ),
        advice=(
            "A significant transformation is underway in your life. Though "
            "it may feel like upheaval, trust the process. Stand firm in "
            "your integrity and call on the power within you."
        ),
        ebo_suggestion=(
            "Nine purple eggplants, palm oil, and a purple or brown cloth "
            "offered to Oya at the entrance of a market or cemetery."
        ),
        orisha="Oya",
        colors=["purple", "brown", "maroon"],
        numbers=[9, 4],
    ),

    # 11 ────────────────────────────────────────────────────────────────────
    Odu(
        number=11,
        yoruba_name="Ika",
        meji_name="Ika Meji",
        english_name="The Covenant of Character",
        alternate_spellings=["Ìká", "Ika"],
        marks=(False, True, True, False),  # || | | ||
        primary_meaning=(
            "Ika Meji governs character (iwa), agreements, covenants, and "
            "the consequences of one's words and promises. It teaches that "
            "character is the foundation of all blessings."
        ),
        themes=["character", "integrity", "agreements", "honesty", "reputation", "consequences"],
        positive_aspects=[
            "Excellent character attracting abundant blessings",
            "Trustworthiness opening doors of opportunity",
            "Success through ethical behaviour",
            "Strength of word and bond",
        ],
        challenges=[
            "Broken promises leading to serious consequences",
            "Dishonesty and deception undermining progress",
            "Conflicts arising from poor character",
        ],
        story_summary=(
            "Ika made a covenant at the crossroads and kept it even when it "
            "cost dearly. Years later, that promise returned as an unexpected "
            "blessing. The odu reminds us that Orunmila weighs not our wealth "
            "but our word."
        ),
        moral_teaching=(
            "Iwa pele — gentle, good character — is the greatest ebo. "
            "Your reputation is your most valuable possession."
        ),
        advice=(
            "Examine your words, commitments, and conduct. Honour all "
            "agreements you have made. This is not a time for shortcuts "
            "or deception — integrity is your greatest protection."
        ),
        ebo_suggestion=(
            "White kola nuts, obi abata, and a white candle; meditate on "
            "promises made and take action to honour them."
        ),
        orisha="Obatala / Orunmila",
        colors=["white", "light blue"],
        numbers=[11, 4],
    ),

    # 12 ────────────────────────────────────────────────────────────────────
    Odu(
        number=12,
        yoruba_name="Oturupon",
        meji_name="Oturupon Meji",
        english_name="The Mystery of the Deep",
        alternate_spellings=["Òtúrúpòn", "Oturupon", "Turupon"],
        marks=(False, True, False, False),  # Wait - let me recalculate
        # || | || || — this would be (False, True, False, False)
        primary_meaning=(
            "Oturupon Meji governs the mysteries of the deep, secret "
            "knowledge, spiritual debts, and the karmic consequences of "
            "actions in past lives or earlier in this life."
        ),
        themes=["mystery", "karma", "debts", "deep water", "ancestral obligations", "hidden"],
        positive_aspects=[
            "Access to deep spiritual knowledge",
            "Resolution of long-standing spiritual debts",
            "Protection through ancestral wisdom",
            "Breakthroughs after sustained effort",
        ],
        challenges=[
            "Unresolved spiritual debts blocking progress",
            "Illnesses with hidden or mysterious causes",
            "Feeling lost or confused about one's path",
        ],
        story_summary=(
            "Oturupon descended into the deepest part of the ocean to "
            "retrieve a blessing that had been swallowed by the waters. "
            "Only by confronting the darkness at the bottom could the "
            "treasure be reclaimed. What we fear to face holds our "
            "greatest gifts."
        ),
        moral_teaching=(
            "Do not run from the mysteries of your past. Face your "
            "spiritual obligations with honesty and they will transform "
            "from burdens into blessings."
        ),
        advice=(
            "Look into matters that have been hidden or avoided. There may "
            "be a spiritual or ancestral obligation requiring your attention. "
            "Seek guidance from an elder or spiritual advisor."
        ),
        ebo_suggestion=(
            "Fish, cool water, and white cloth offered at a body of water; "
            "prayers for ancestral debts to be resolved."
        ),
        orisha="Yemoja / Olokun",
        colors=["deep blue", "black"],
        numbers=[12, 7],
    ),

    # 13 ────────────────────────────────────────────────────────────────────
    Odu(
        number=13,
        yoruba_name="Otura",
        meji_name="Otura Meji",
        english_name="The Reconciliation",
        alternate_spellings=["Òtúrá", "Otura"],
        marks=(False, True, True, True),  # || | | |
        primary_meaning=(
            "Otura Meji is the Odu of reconciliation, diplomacy, peace-making, "
            "and the restoration of harmony between opposing forces. "
            "It also governs trade, commerce, and the marketplace."
        ),
        themes=["reconciliation", "peace", "trade", "harmony", "diplomacy", "marketplace"],
        positive_aspects=[
            "Peaceful resolution of conflicts",
            "Success in commerce and trade",
            "Healing of broken relationships",
            "Community harmony and cooperation",
        ],
        challenges=[
            "Difficulty letting go of grudges",
            "Deception in business dealings",
            "Being too accommodating at one's own expense",
        ],
        story_summary=(
            "Two kingdoms had warred for generations. When Otura arrived, "
            "both sides believed only they had sent for the diviner. Yet "
            "Otura had come to both, bearing the same message: 'The market "
            "feeds all; war starves all.' Peace was made and trade flourished."
        ),
        moral_teaching=(
            "Seek the common ground. Those who make peace prosper; "
            "those who cling to conflict are consumed by it."
        ),
        advice=(
            "Now is the time to mend broken relationships and resolve disputes. "
            "Business and trade ventures are favoured. Approach negotiations "
            "with honesty and a spirit of mutual benefit."
        ),
        ebo_suggestion=(
            "Two white pigeons, eko (maize pudding), and honey offered "
            "at the marketplace or at a family gathering place."
        ),
        orisha="Eshu / Orunmila",
        colors=["white", "yellow"],
        numbers=[13, 8],
    ),

    # 14 ────────────────────────────────────────────────────────────────────
    Odu(
        number=14,
        yoruba_name="Irete",
        meji_name="Irete Meji",
        english_name="The Patience of the Mountain",
        alternate_spellings=["Ìrẹtẹ̀", "Irete"],
        marks=(True, False, False, False),  # | || || ||
        primary_meaning=(
            "Irete Meji governs patience, endurance, the slow but certain "
            "accumulation of wisdom and wealth, and the dignity of elders. "
            "It teaches that lasting achievement requires time."
        ),
        themes=["patience", "wisdom", "longevity", "elders", "endurance", "long-term success"],
        positive_aspects=[
            "Long life and enduring success",
            "Deep wisdom accumulated through experience",
            "Respect and honour in old age",
            "Steady, reliable progress toward goals",
        ],
        challenges=[
            "Impatience causing premature actions",
            "Stubbornness resisting necessary change",
            "Delays that test one's resolve",
        ],
        story_summary=(
            "Irete planted a palm tree and waited. Neighbours mocked him for "
            "waiting twenty years for oil. But when the palm bore fruit, it "
            "fed three generations. The mountain, says Irete, does not hurry "
            "to meet the sunrise; yet it is always there to receive it."
        ),
        moral_teaching=(
            "The deepest roots produce the tallest trees. Invest in what "
            "lasts, not what is immediate. Honour those who have walked "
            "the long road before you."
        ),
        advice=(
            "Do not rush the process. Your efforts are building something "
            "enduring. Honour the elders and ancestors in your life. "
            "Patience will be your greatest asset right now."
        ),
        ebo_suggestion=(
            "Palm kernel oil, roasted groundnuts, and a small offering "
            "of food to the eldest members of the family."
        ),
        orisha="Obatala / Orunmila",
        colors=["white", "grey"],
        numbers=[14, 7],
    ),

    # 15 ────────────────────────────────────────────────────────────────────
    Odu(
        number=15,
        yoruba_name="Ose",
        meji_name="Ose Meji",
        english_name="The Abundance of Osun",
        alternate_spellings=["Òsé", "Ose"],
        marks=(True, True, False, True),  # | | || |
        primary_meaning=(
            "Ose Meji is Osun's Odu, governing love, beauty, fertility, "
            "wealth through sweet things, and the power of the feminine "
            "divine. It is one of the most auspicious Odu for matters "
            "of the heart and creative abundance."
        ),
        themes=["love", "beauty", "fertility", "wealth", "Osun", "relationships", "arts"],
        positive_aspects=[
            "Abundance in love and relationships",
            "Fertility and childbearing blessings",
            "Artistic talent and creative expression",
            "Financial prosperity through beauty and service",
        ],
        challenges=[
            "Vanity and excessive focus on appearance",
            "Jealousy in romantic relationships",
            "Overindulgence in pleasures",
        ],
        story_summary=(
            "When the Orisha first came to Earth they overlooked Osun because "
            "she was a woman. Their plans all failed until they returned to "
            "honour her. Ose Meji teaches that the sweetness and wisdom of "
            "the divine feminine are indispensable to all human flourishing."
        ),
        moral_teaching=(
            "Honour the sacred feminine in all its forms. Love generously "
            "and beauty will flow through all you do."
        ),
        advice=(
            "Love and abundance are flowing toward you. Open your heart and "
            "hands to receive. This is a favourable time for romance, "
            "creative projects, and matters of beauty. Honour Osun."
        ),
        ebo_suggestion=(
            "Yellow flowers, honey, sweet oranges, brass jewellery and "
            "a yellow candle offered to Osun at a river or fountain."
        ),
        orisha="Osun",
        colors=["yellow", "gold", "amber"],
        numbers=[5, 15],
    ),

    # 16 ────────────────────────────────────────────────────────────────────
    Odu(
        number=16,
        yoruba_name="Ofun",
        meji_name="Ofun Meji",
        english_name="The Wisdom of the Completed Cycle",
        alternate_spellings=["Òfún", "Ofun"],
        marks=(False, False, True, False),  # || || | ||
        primary_meaning=(
            "Ofun Meji is the sixteenth and final principal Odu, governing "
            "completion, transformation through suffering, the power of "
            "speech, and the ultimate reconciliation of opposites."
        ),
        themes=["completion", "speech", "power of words", "transformation", "cycles", "blessings"],
        positive_aspects=[
            "Completion of major life cycles with great blessing",
            "Powerful, life-changing speech and communication",
            "Transformation of past suffering into profound wisdom",
            "Arrival at a long-awaited destination",
        ],
        challenges=[
            "Destructive use of words — curses and harmful speech",
            "Health challenges, particularly involving the skin or extremities",
            "The difficulty of accepting an ending",
        ],
        story_summary=(
            "Ofun had suffered greatly and carried many scars. Yet when "
            "Ofun spoke, everyone fell silent, for each word carried the "
            "weight of a lifetime. Ifá says: the one who has walked through "
            "fire speaks words that can either burn or illuminate — choose "
            "your words with great care."
        ),
        moral_teaching=(
            "Guard your speech. Words once spoken cannot be recalled. "
            "Use your voice as a tool of healing, not destruction. "
            "Your life's trials are your greatest teachers."
        ),
        advice=(
            "A major cycle in your life is completing. Reflect on what you "
            "have learned and speak your truth with care and wisdom. "
            "Watch your words — they carry great power now."
        ),
        ebo_suggestion=(
            "Sixteen cowries, white and red cloth, and an offering of "
            "obi kola at the base of a large tree or at the family shrine."
        ),
        orisha="Obatala / Orunmila",
        colors=["white", "red"],
        numbers=[16, 10],
    ),
]

# ---------------------------------------------------------------------------
# Quick-access dictionary by number
# ---------------------------------------------------------------------------
ODU_BY_NUMBER: dict[int, Odu] = {odu.number: odu for odu in ODU_LIST}

# ---------------------------------------------------------------------------
# Quick-access dictionary by Yoruba name (lower-case, no diacritics stripped)
# ---------------------------------------------------------------------------
ODU_BY_NAME: dict[str, Odu] = {odu.yoruba_name.lower(): odu for odu in ODU_LIST}
