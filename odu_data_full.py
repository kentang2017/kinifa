"""
odu_data_full.py — 伊法神諕：完整 256 個 Odu 的資料結構

Ifá Oracle: Data structure supporting all 256 Ifá Odu.

═══════════════════════════════════════════════════════════════════════════════
此資料僅供教育用途，真正的伊法占卜需要受訓的 Babalawo 進行。
This data is for educational purposes only. Authentic Ifá divination requires
a trained Babalawo (Ifá priest).
═══════════════════════════════════════════════════════════════════════════════

Structure
---------
• The 256 Odu arise from all ordered pairings of the 16 principal Odu (Meji).
  - IDs  1–16  : the 16 Meji (principal Odu, where both halves are identical).
  - IDs 17–256 : the 240 composite ("minor") Odu, named "Left Right"
                 (e.g., "Ogbe Oyeku").

• The binary_pattern uses 8 bits: the left arm (4 bits) followed by the right
  arm (4 bits) of the Opele chain, where 1 = single mark (|, odd) and
  0 = double mark (||, even).

Backward compatibility
-----------------------
This module imports ODU_LIST and ODU_BY_NUMBER from odu_data.py, and wraps
each legacy Odu object inside an OduFull dataclass, so code already depending
on odu_data.py is unaffected.

Usage
-----
    from odu_data_full import ODU_FULL_LIST, ODU_FULL_BY_ID, ODU_FULL_BY_NAME
    odu = ODU_FULL_BY_ID[1]          # Eji Ogbe
    odu = ODU_FULL_BY_NAME["ogbe oyeku"]  # composite Odu 17
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Import the existing 16 principal Odu so we stay backward-compatible
# ---------------------------------------------------------------------------
from odu_data import Odu, ODU_LIST, ODU_BY_NUMBER  # noqa: F401 (re-exported)


# ===========================================================================
# OduFull dataclass
# ===========================================================================

@dataclass
class OduFull:
    """
    Represents any of the 256 Ifá Odu.

    For the 16 Meji, every field is populated with rich narrative content.
    For the 240 composite Odu the fields are derived programmatically from
    the two parent Meji, keeping the data self-consistent and expandable.

    ⚠️ Educational note — All narrative content is a simplified academic
    overview intended to introduce learners to Ifá philosophy.  Real Ifá
    corpus (odù Ifá) is vast, oral, and sacred.  Consult a qualified
    Babalawo for authentic guidance.
    """

    # ── Identity ─────────────────────────────────────────────────────────
    id: int                              # 1–256 (Meji first, then composites)
    yoruba_name: str                     # e.g. "Eji Ogbe" or "Ogbe Oyeku"
    english_name: str                    # Approximate English translation
    chinese_name: str                    # 繁體中文名稱

    # ── Binary pattern ────────────────────────────────────────────────────
    # 8 integers (0 or 1): left arm marks [0:4] + right arm marks [4:8]
    # 1 = single mark  |  (odd / I)
    # 0 = double mark || (even / II)
    binary_pattern: List[int]

    # ── Spiritual associations ────────────────────────────────────────────
    principal_orishas: List[str]

    # ── Core meanings (bilingual) ─────────────────────────────────────────
    core_meaning_en: str
    core_meaning_zh: str

    # ── Key lessons (each item is a dict with "en" and "zh" keys) ─────────
    key_lessons: List[Dict[str, str]]    # 3–5 items, each {"en": ..., "zh": ...}

    # ── Ebo suggestions ───────────────────────────────────────────────────
    ebo_suggestions: List[str]           # Simple, educational suggestions
    ebo_caveat: str = (
        "⚠️  Ebo guidance here is simplified for educational purposes only. "
        "Actual ebo prescription requires consultation with a qualified Babalawo. "
        "僅供教育參考，實際儀式請咨詢合格祭司。"
    )

    # ── Short Ese (poem/verse) example ───────────────────────────────────
    short_ese_example: Dict[str, str] = field(default_factory=lambda: {"en": "", "zh": ""})

    # ── Legacy fields (present for Meji; empty for composites) ───────────
    # These mirror the Odu dataclass fields so callers can use OduFull in
    # any context that previously expected an Odu object.
    meji_name: str = ""                  # Full Meji name (e.g. "Ejiogbe")
    alternate_spellings: List[str] = field(default_factory=list)
    marks: Tuple[bool, ...] = field(default_factory=tuple)  # 4-element
    themes: List[str] = field(default_factory=list)
    positive_aspects: List[str] = field(default_factory=list)
    challenges: List[str] = field(default_factory=list)
    story_summary: str = ""
    moral_teaching: str = ""
    advice: str = ""
    orisha: str = ""
    colors: List[str] = field(default_factory=list)
    numbers: List[int] = field(default_factory=list)

    # ── Composite parentage ───────────────────────────────────────────────
    left_parent_id: Optional[int] = None   # None for Meji
    right_parent_id: Optional[int] = None  # None for Meji

    def is_meji(self) -> bool:
        """Return True when both arms are identical (one of the 16 principal Odu)."""
        return self.left_parent_id is None

    def figure_lines(self) -> List[str]:
        """Return 8 lines representing the Opele figure (left arm | right arm)."""
        SINGLE = "  |  "
        DOUBLE = " | | "
        bp = self.binary_pattern
        lines = []
        for i in range(4):
            left  = SINGLE if bp[i]   else DOUBLE
            right = SINGLE if bp[i+4] else DOUBLE
            lines.append(f"{left}   {right}")
        return lines

    def figure_str(self) -> str:
        """Return the full Opele figure as a multi-line string."""
        return "\n".join(self.figure_lines())


# ===========================================================================
# Helper: convert a legacy 4-mark Odu.marks tuple to 4 binary bits
# ===========================================================================

def _marks_to_bits(marks: Tuple[bool, bool, bool, bool]) -> List[int]:
    return [1 if m else 0 for m in marks]


# ===========================================================================
# The 16 Meji — rich data entries
# Each mark:  True  = single |  (1)
#             False = double || (0)
# binary_pattern = left_arm_bits + right_arm_bits (arms are identical for Meji)
# ===========================================================================

_MEJI_DATA: List[OduFull] = [

    # ── 1. Eji Ogbe ────────────────────────────────────────────────────────
    OduFull(
        id=1,
        yoruba_name="Eji Ogbe",
        meji_name="Ejiogbe",
        english_name="The Fullness of Light",
        chinese_name="純光滿盈",
        alternate_spellings=["Ogbe", "Ogbè", "Eji-Ogbe"],
        binary_pattern=[1, 1, 1, 1, 1, 1, 1, 1],
        marks=(True, True, True, True),
        principal_orishas=["Obatala", "Orunmila"],
        orisha="Obatala",
        colors=["white", "gold"],
        numbers=[1, 8],
        themes=["beginnings", "light", "life", "abundance", "leadership", "spirituality"],
        core_meaning_en=(
            "Eji Ogbe is the first and most luminous of all Odu, representing "
            "the dawn of creation, divine light, and the fullness of blessings. "
            "When this Odu appears it heralds new beginnings, tremendous potential, "
            "and the favour of the divine."
        ),
        core_meaning_zh=(
            "Eji Ogbe 是所有神諕中最光輝的第一卦，象徵創世的黎明、"
            "神聖之光與祝福的圓滿。此卦出現，預示嶄新的開端、"
            "無限的潛力，以及神靈的眷顧。"
        ),
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
        key_lessons=[
            {
                "en": "Gratitude opens the door to abundance; receive every new dawn with humility.",
                "zh": "感恩開啟豐盛之門；以謙遜之心迎接每個黎明。",
            },
            {
                "en": "The greatest light casts no shadow on others — lead by lifting those around you.",
                "zh": "最偉大的光不在他人身上投下陰影——透過提升他人來領導。",
            },
            {
                "en": "Honour the sacred in every beginning, for creation itself is a divine act.",
                "zh": "在每一個開端中敬畏神聖，因為創造本身就是神聖的行為。",
            },
            {
                "en": "Spiritual discipline protects prosperity; do not let success breed neglect.",
                "zh": "靈性紀律守護繁榮；勿讓成功滋生怠慢。",
            },
        ],
        story_summary=(
            "In the beginning Orunmila cast Eji Ogbe and saw the entire world "
            "bathed in light. The odu teaches that when Olodumare sent the "
            "sixteen original Odu to Earth, Eji Ogbe led them, carrying the "
            "torch of divine knowledge. It reminds us that life begins in "
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
        ebo_suggestions=[
            "White cloth offered to Obatala at dawn",
            "White kola nuts (obi abata) and fresh water at a crossroads",
            "Candles and fresh flowers on the ancestral altar",
        ],
        short_ese_example={
            "en": (
                "Eji Ogbe casts his net of light across the sky —\n"
                "From that net the stars were born.\n"
                "Cast your net wide, child of Orunmila,\n"
                "And let the morning find you grateful."
            ),
            "zh": (
                "Eji Ogbe 將光明之網撒遍蒼穹——\n"
                "星辰由此網而生。\n"
                "廣撒你的網吧，奧倫米拉之子，\n"
                "讓清晨找到一顆感恩的心。"
            ),
        },
    ),

    # ── 2. Oyeku Meji ──────────────────────────────────────────────────────
    OduFull(
        id=2,
        yoruba_name="Oyeku Meji",
        meji_name="Oyeku Meji",
        english_name="The Darkness Before Renewal",
        chinese_name="更新前的玄暗",
        alternate_spellings=["Oyèkú", "Oyeku", "Eji-Oko"],
        binary_pattern=[0, 0, 0, 0, 0, 0, 0, 0],
        marks=(False, False, False, False),
        principal_orishas=["Egungun", "Oya"],
        orisha="Egungun / Oya",
        colors=["black", "white"],
        numbers=[2, 9],
        themes=["death", "transformation", "ancestors", "endings", "rebirth", "mystery"],
        core_meaning_en=(
            "Oyeku Meji governs death, endings, transformation, and the passage "
            "from one state of being to another. It is not a sign of misfortune "
            "but of profound transition. The ancestor realm is near."
        ),
        core_meaning_zh=(
            "Oyeku Meji 掌管死亡、終結、轉化，以及從一種存在狀態過渡到另一種狀態。"
            "這不是不幸的象徵，而是深刻轉變的標誌。祖靈的世界近在咫尺。"
        ),
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
        key_lessons=[
            {
                "en": "Death is a doorway, not a wall; honour transitions as sacred passages.",
                "zh": "死亡是門扉，而非牆壁；以神聖過渡的態度敬重每個終結。",
            },
            {
                "en": "The ancestors who have gone before you are a living source of strength.",
                "zh": "先行離去的祖先是你力量的活泉。",
            },
            {
                "en": "Release what is complete so that new life can emerge.",
                "zh": "放下已完成的，新生命才能萌發。",
            },
            {
                "en": "Silence and darkness are not enemies — they are the womb of all creation.",
                "zh": "靜默與黑暗不是敵人——它們是一切創造的子宮。",
            },
        ],
        story_summary=(
            "Oyeku came to Earth wearing a dark cloak and was feared by all. "
            "Yet the Babalawo who consulted Ifá learned that Oyeku brings not "
            "destruction but the sacred darkness from which new life emerges — "
            "as the seed must be buried before it can sprout."
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
        ebo_suggestions=[
            "Black-eyed beans (ewa) at the ancestral shrine",
            "Palm wine and a candle placed at the egungun shrine or a grave",
            "White and black cloth as offerings for transition",
        ],
        short_ese_example={
            "en": (
                "Oyeku wrapped the world in her cloak of night —\n"
                "Not to extinguish the fire,\n"
                "But to remind it whence its light was born.\n"
                "Rest, child. The dawn remembers you."
            ),
            "zh": (
                "Oyeku 以夜之黑袍覆蓋世界——\n"
                "不是為了熄滅火焰，\n"
                "而是提醒它光明從何而來。\n"
                "休憩吧，孩子。黎明記得你。"
            ),
        },
    ),

    # ── 3. Iwori Meji ──────────────────────────────────────────────────────
    OduFull(
        id=3,
        yoruba_name="Iwori Meji",
        meji_name="Iwori Meji",
        english_name="The Inner Vision",
        chinese_name="內在視野",
        alternate_spellings=["Ìwòrì", "Iwori"],
        binary_pattern=[0, 0, 1, 1, 0, 0, 1, 1],
        marks=(False, False, True, True),
        principal_orishas=["Ori", "Obatala"],
        orisha="Ori / Obatala",
        colors=["white", "silver"],
        numbers=[3, 6],
        themes=["inner wisdom", "secrets", "intuition", "introspection", "hidden matters"],
        core_meaning_en=(
            "Iwori Meji is the Odu of inner sight, introspection, and the hidden "
            "knowledge that resides within the heart. It governs secrets, the "
            "subconscious, and deep spiritual perception. Truth must be sought within."
        ),
        core_meaning_zh=(
            "Iwori Meji 是內在視野、自省與藏於心中的隱秘知識之神諕。"
            "它掌管秘密、潛意識及深刻的靈性感知。真相必須向內尋求。"
        ),
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
        key_lessons=[
            {
                "en": "The answers you seek already live within you — still yourself and listen.",
                "zh": "你所尋求的答案已在你心中——靜下來，細心聆聽。",
            },
            {
                "en": "Guard your secrets wisely; not every truth is meant for every ear.",
                "zh": "謹慎守護你的秘密；並非每個真相都適合每個耳朵。",
            },
            {
                "en": "Self-knowledge is the foundation of all other wisdom.",
                "zh": "自我認識是一切智慧的根基。",
            },
        ],
        story_summary=(
            "Iwori came to Earth looking inward rather than outward and was mocked "
            "for seeming to ignore the world. Yet when crisis came, only Iwori knew "
            "the hidden path to safety, for the answers were always within."
        ),
        moral_teaching=(
            "The answers you seek are already within you. Quiet the noise of "
            "the world and listen to the still voice of Ori."
        ),
        advice=(
            "Trust your intuition above external voices. Spend time in quiet "
            "reflection. Be mindful of secrets — both keeping and revealing them."
        ),
        ebo_suggestions=[
            "Honey and white cloth placed before Ori",
            "A personal item on the inner-self altar during meditation",
            "Quiet prayer at midnight facing inward",
        ],
        short_ese_example={
            "en": (
                "Iwori closed his eyes while others watched the horizon —\n"
                "When the storm swept them away,\n"
                "He alone stood still, rooted in his own knowing.\n"
                "The deepest well is dug in silence."
            ),
            "zh": (
                "Iwori 閉上眼睛，旁人卻凝視地平線——\n"
                "當風暴將他們席捲而去，\n"
                "唯有他靜立，紮根於自己的認知。\n"
                "最深的水井，是在寂靜中挖鑿的。"
            ),
        },
    ),

    # ── 4. Odi Meji ────────────────────────────────────────────────────────
    OduFull(
        id=4,
        yoruba_name="Odi Meji",
        meji_name="Odi Meji",
        english_name="The Womb of Creation",
        chinese_name="創造的子宮",
        alternate_spellings=["Òdí", "Odi"],
        binary_pattern=[1, 1, 0, 0, 1, 1, 0, 0],
        marks=(True, True, False, False),
        principal_orishas=["Yemoja", "Osun"],
        orisha="Yemoja / Osun",
        colors=["blue", "white"],
        numbers=[4, 7],
        themes=["fertility", "creation", "pregnancy", "hidden dangers", "protection", "femininity"],
        core_meaning_en=(
            "Odi Meji rules the womb, fertility, hidden things, and all matters of "
            "creation and gestation. It also governs concealment, protection against "
            "witchcraft, and the power of the sacred feminine."
        ),
        core_meaning_zh=(
            "Odi Meji 掌管子宮、生育、隱秘之事，以及一切創造與孕育的事務。"
            "它也管轄隱蔽、對抗巫術的保護，以及神聖女性力量。"
        ),
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
        key_lessons=[
            {
                "en": "Respect the creative process — all great things grow quietly before they are revealed.",
                "zh": "尊重創造的過程——所有偉大的事物在顯現之前都靜靜地生長。",
            },
            {
                "en": "The womb teaches patience: trust the unseen forces at work in your life.",
                "zh": "子宮教導耐心：信任在你生命中運作的無形力量。",
            },
            {
                "en": "Protect what is precious and vulnerable while it takes form.",
                "zh": "在珍貴脆弱之物成形時，給予保護。",
            },
        ],
        story_summary=(
            "Odi went to Earth as a silent keeper of secrets. She taught that the "
            "most powerful things grow quietly in the dark — as the child grows in "
            "the womb unseen. Those who tried to expose her secrets prematurely "
            "were warned: some things must be revealed only in their own time."
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
        ebo_suggestions=[
            "Plantain and palm oil at a body of water",
            "A calabash of water and cowries offered at home",
            "Blue and white cloth as gifts to Yemoja",
        ],
        short_ese_example={
            "en": (
                "Odi speaks from the deep belly of the earth —\n"
                "What grows in the dark needs no audience.\n"
                "Guard the seed, tend the silence,\n"
                "And life will declare itself in its own season."
            ),
            "zh": (
                "Odi 從大地深處的腹腔中說話——\n"
                "在黑暗中生長之物不需要觀眾。\n"
                "守護種子，培養靜默，\n"
                "生命將在它自己的季節中宣告自身。"
            ),
        },
    ),

    # ── 5. Irosun Meji ─────────────────────────────────────────────────────
    OduFull(
        id=5,
        yoruba_name="Irosun Meji",
        meji_name="Irosun Meji",
        english_name="The Flow of Life Blood",
        chinese_name="生命血液之流",
        alternate_spellings=["Ìròsùn", "Irosun", "Rosun"],
        binary_pattern=[1, 0, 1, 1, 1, 0, 1, 1],
        marks=(True, False, True, True),
        principal_orishas=["Osun", "Sopona"],
        orisha="Osun / Sopona",
        colors=["red", "coral"],
        numbers=[5, 9],
        themes=["health", "healing", "blood", "medicine", "lineage", "sacrifice"],
        core_meaning_en=(
            "Irosun Meji governs blood, life force, medicine, and the transmission "
            "of vital energy. It is associated with healing, menstruation, sacrifice, "
            "and the continuity of lineage through the bloodline."
        ),
        core_meaning_zh=(
            "Irosun Meji 掌管血液、生命力、醫藥及生命能量的傳遞。"
            "它與療癒、月經、犧牲，以及血脈傳承的延續密切相關。"
        ),
        positive_aspects=[
            "Physical vitality and good health",
            "Healing and recovery",
            "Strong family bloodline",
            "Success in medicine and herbal work",
        ],
        challenges=[
            "Illnesses related to blood or internal organs",
            "Family disputes over inheritance",
            "Excessive loss of vital resources",
        ],
        key_lessons=[
            {
                "en": "Life force is precious — guard your health and the health of those in your care.",
                "zh": "生命力是寶貴的——守護你自己及你所照顧之人的健康。",
            },
            {
                "en": "Honour the sacrifice of those who gave so you could live and thrive.",
                "zh": "敬重那些為你的生存與繁榮而付出犧牲的人。",
            },
            {
                "en": "The healer respects both the wound and the remedy — wisdom lies in balance.",
                "zh": "療癒者同等尊重傷口與藥方——智慧在於平衡。",
            },
        ],
        story_summary=(
            "Irosun wore red and carried the knowledge of life's most precious "
            "fluid. The odu taught that blood binds families across generations and "
            "that the healer who respects the body's sacred river can cure what "
            "others cannot. Waste not what is vital."
        ),
        moral_teaching=(
            "Life force is precious. Protect your health and the health of "
            "those in your care. Honour the sacrifice of those who bled so "
            "you could live."
        ),
        advice=(
            "Pay attention to your physical health. This is a good time for "
            "healing practices. Honour your family lineage and ancestors."
        ),
        ebo_suggestions=[
            "Red palm oil and camwood (osun) powder at the family shrine",
            "Kola nuts and a red candle offered at the ancestral altar",
            "Herbal bath for cleansing and vitality",
        ],
        short_ese_example={
            "en": (
                "Irosun paints the morning sky before dawn —\n"
                "That red is the blood of all who came before.\n"
                "Drink deeply of your lineage, child;\n"
                "In the veins of the living, ancestors still speak."
            ),
            "zh": (
                "Irosun 在黎明前為晨空染紅——\n"
                "那抹紅是所有先行者的血液。\n"
                "深深汲取你的血脈，孩子；\n"
                "在生者的血管中，祖先仍在訴說。"
            ),
        },
    ),

    # ── 6. Owonrin Meji ────────────────────────────────────────────────────
    OduFull(
        id=6,
        yoruba_name="Owonrin Meji",
        meji_name="Owonrin Meji",
        english_name="The Unpredictable Wind",
        chinese_name="無常之風",
        alternate_spellings=["Òwónrín", "Owonrin", "Wonrin"],
        binary_pattern=[0, 1, 0, 0, 0, 1, 0, 0],
        marks=(False, True, False, False),
        principal_orishas=["Sango", "Eshu"],
        orisha="Sango / Eshu",
        colors=["red", "white"],
        numbers=[6, 12],
        themes=["change", "unpredictability", "chaos", "creativity", "lightning", "disruption"],
        core_meaning_en=(
            "Owonrin Meji embodies chaos, sudden change, and the wild creative "
            "energy that disrupts in order to renew. It is the Odu of lightning and "
            "the unexpected reversal. What appears as disorder may contain breakthrough."
        ),
        core_meaning_zh=(
            "Owonrin Meji 體現混沌、突變，以及為了更新而打破現狀的狂野創造力。"
            "它是閃電與意外逆轉的神諕。看似混亂之中，可能蘊藏突破的契機。"
        ),
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
        key_lessons=[
            {
                "en": "Embrace necessary change rather than clinging to what is familiar.",
                "zh": "擁抱必要的改變，而不是緊抓熟悉的事物不放。",
            },
            {
                "en": "Chaos is often the doorway to a better order; the storm clears the air.",
                "zh": "混沌往往是通向更好秩序的大門；風暴淨化空氣。",
            },
            {
                "en": "Stay nimble — the one who can ride the wind goes further than the one who fears it.",
                "zh": "保持靈活——能乘風而行者，比畏風者走得更遠。",
            },
        ],
        story_summary=(
            "Owonrin danced wildly and could not be still. The other Odu complained, "
            "but when the storm came it was Owonrin who knew every escape route, "
            "for chaos is also the seed of creativity."
        ),
        moral_teaching=(
            "Embrace necessary change rather than clinging to the familiar. "
            "Chaos is often the doorway to a better order."
        ),
        advice=(
            "Expect the unexpected and stay flexible. Do not resist the "
            "changes coming your way — they may be the answer to your prayers."
        ),
        ebo_suggestions=[
            "Bitter kola (obi ata) and red palm oil at a crossroads",
            "Rum or gin offered to Sango with a red candle",
            "Release of a live bird at a junction as symbolic offering",
        ],
        short_ese_example={
            "en": (
                "Owonrin laughed when the house fell down —\n"
                "Not from cruelty, but because he had already seen\n"
                "The palace that would rise in its place.\n"
                "Not every ending is a loss."
            ),
            "zh": (
                "Owonrin 在房屋倒塌時大笑——\n"
                "不是殘忍，而是因為他早已看見\n"
                "將在其位拔地而起的宮殿。\n"
                "並非每個結局都是失去。"
            ),
        },
    ),

    # ── 7. Obara Meji ──────────────────────────────────────────────────────
    OduFull(
        id=7,
        yoruba_name="Obara Meji",
        meji_name="Obara Meji",
        english_name="The Royalty of Generosity",
        chinese_name="慷慨的王者",
        alternate_spellings=["Òbàrà", "Obara"],
        binary_pattern=[1, 1, 1, 0, 1, 1, 1, 0],
        marks=(True, True, True, False),
        principal_orishas=["Sango", "Ogun"],
        orisha="Sango / Ogun",
        colors=["red", "gold"],
        numbers=[7, 4],
        themes=["wealth", "leadership", "royalty", "generosity", "fame", "prestige"],
        core_meaning_en=(
            "Obara Meji is the Odu of royalty, majesty, wealth, and eloquence. "
            "It governs leadership, generosity, and the splendour of one who "
            "carries themselves with dignified authority. True kings give abundantly."
        ),
        core_meaning_zh=(
            "Obara Meji 是王者、威嚴、財富與口才的神諕。"
            "它掌管領導力、慷慨，以及以尊嚴權威自持者的光輝。"
            "真正的王者慷慨給予。"
        ),
        positive_aspects=[
            "Great wealth and material success",
            "Natural leadership and commanding presence",
            "Eloquence and persuasive speech",
            "Victory and recognition",
        ],
        challenges=[
            "Arrogance and dismissal of counsel",
            "Excessive pride leading to downfall",
            "Generosity without discernment",
        ],
        key_lessons=[
            {
                "en": "True royalty is measured by generosity, not possessions.",
                "zh": "真正的王者之道以慷慨衡量，而非以財物論。",
            },
            {
                "en": "A king who listens to wise counsel endures; one who does not, falls.",
                "zh": "聆聽賢言的王者長存；置若罔聞者將傾覆。",
            },
            {
                "en": "Let your words build up rather than tear down — speech is a royal weapon.",
                "zh": "讓你的言語建設而非破壞——語言是王者的武器。",
            },
        ],
        story_summary=(
            "Obara walked into every room as if he owned it. Yet the wisest king "
            "is not the one with the most gold but the one who gives the most away "
            "and still lacks nothing — for Ori ensures that the generous heart "
            "is never empty."
        ),
        moral_teaching=(
            "Lead with generosity and wisdom. Arrogance is the enemy of lasting "
            "greatness. The generous hand is always refilled."
        ),
        advice=(
            "Step into your authority with confidence, but temper it with humility "
            "and generosity. Share your abundance — what you give away returns "
            "to you multiplied."
        ),
        ebo_suggestions=[
            "Red cloth and kola nuts offered to Sango",
            "A feast shared with family and community in celebration",
            "Gold-coloured items placed on the personal altar",
        ],
        short_ese_example={
            "en": (
                "Obara entered and the room became a throne room —\n"
                "Not because he demanded it,\n"
                "But because he gave the room to everyone in it.\n"
                "The crown falls to those who carry others."
            ),
            "zh": (
                "Obara 走入，房間隨即成為王座廳——\n"
                "不是因為他要求如此，\n"
                "而是因為他將這房間贈予了在場的每個人。\n"
                "王冠落在那些承載他人的人頭上。"
            ),
        },
    ),

    # ── 8. Okanran Meji ────────────────────────────────────────────────────
    OduFull(
        id=8,
        yoruba_name="Okanran Meji",
        meji_name="Okanran Meji",
        english_name="The Spark of Conflict and Resolution",
        chinese_name="衝突與化解之火花",
        alternate_spellings=["Òkànràn", "Okanran"],
        binary_pattern=[1, 0, 0, 0, 1, 0, 0, 0],
        marks=(True, False, False, False),
        principal_orishas=["Sango", "Ogun"],
        orisha="Sango / Ogun",
        colors=["red", "orange"],
        numbers=[8, 3],
        themes=["conflict", "fire", "passion", "resolution", "truth", "courage"],
        core_meaning_en=(
            "Okanran Meji is the Odu of sudden sparks — conflict, passion, and the "
            "fierce energy that both destroys and purifies. It governs arguments, "
            "legal matters, and the fire of truth that cuts through deception."
        ),
        core_meaning_zh=(
            "Okanran Meji 是突然火花的神諕——衝突、激情，以及既摧毀又淨化的猛烈能量。"
            "它掌管爭論、法律事務，以及刺穿欺騙的真相之火。"
        ),
        positive_aspects=[
            "Courage to speak and stand for truth",
            "Swift resolution of conflicts",
            "Passionate creativity and bold action",
            "Victory in legal and adversarial matters",
        ],
        challenges=[
            "Hot temper and impulsive reactions",
            "Conflicts escalating unnecessarily",
            "Burning bridges through careless speech",
        ],
        key_lessons=[
            {
                "en": "Channel fiery energy toward justice, not destruction.",
                "zh": "將火熱的能量引導向正義，而非破壞。",
            },
            {
                "en": "Speak truth boldly, but temper boldness with wisdom.",
                "zh": "勇敢說出真相，但以智慧調和勇氣。",
            },
            {
                "en": "Some conflicts cannot be avoided — face them with integrity.",
                "zh": "有些衝突無可迴避——以正直之心面對。",
            },
        ],
        story_summary=(
            "Okanran arrived like a lightning bolt and set the forest ablaze. "
            "The elders were afraid, but the farmer saw the ash enriching the soil. "
            "What burns away falsehood leaves fertile ground for truth."
        ),
        moral_teaching=(
            "Fire is a servant or a master depending on who holds it. "
            "Channel your passionate nature toward righteousness."
        ),
        advice=(
            "A conflict may be brewing or already present. Face it honestly "
            "rather than avoiding it. Truth, spoken with care, will prevail."
        ),
        ebo_suggestions=[
            "Bitter kola and peppers offered to Sango at an outdoor fire",
            "Red and orange candles lit with a prayer for peace",
            "Iron tool placed at the Ogun shrine",
        ],
        short_ese_example={
            "en": (
                "Okanran struck the ground and fire leapt up —\n"
                "The coward ran; the wise person asked:\n"
                "What truth had been too long buried\n"
                "That the earth itself had to cry out?"
            ),
            "zh": (
                "Okanran 擊地，火焰驟然躍起——\n"
                "懦者逃跑；智者問道：\n"
                "是哪個真相被埋藏太久，\n"
                "以至於大地本身不得不哭喊？"
            ),
        },
    ),

    # ── 9. Ogunda Meji ─────────────────────────────────────────────────────
    OduFull(
        id=9,
        yoruba_name="Ogunda Meji",
        meji_name="Ogunda Meji",
        english_name="The Pathway Cleared by Iron",
        chinese_name="鐵刃開路",
        alternate_spellings=["Ògúndá", "Ogunda", "Ogunda"],
        binary_pattern=[1, 1, 0, 1, 1, 1, 0, 1],
        marks=(True, True, False, True),
        principal_orishas=["Ogun"],
        orisha="Ogun",
        colors=["green", "black"],
        numbers=[3, 9],
        themes=["iron", "labour", "clearing paths", "surgery", "determination", "justice"],
        core_meaning_en=(
            "Ogunda Meji is the Odu of Ogun, the Orisha of iron, labour, and the "
            "clearing of paths. It governs hard work, surgery, the forging of new "
            "roads, and the courage to cut through obstacles with precision."
        ),
        core_meaning_zh=(
            "Ogunda Meji 是奧岡（Ogun）的神諕，掌管鐵、勞動與開路。"
            "它代表辛勤工作、手術、開闢新道路，以及以精準之力斬斷障礙的勇氣。"
        ),
        positive_aspects=[
            "Determination and perseverance",
            "Ability to overcome obstacles",
            "Success in physical endeavours and craftsmanship",
            "Protection in travel and new ventures",
        ],
        challenges=[
            "Stubbornness and refusal to compromise",
            "Violence or excessive force",
            "Cutting down what should not be cut",
        ],
        key_lessons=[
            {
                "en": "The machete that clears a path serves life — use your strength in service of others.",
                "zh": "開路的大刀服務生命——以你的力量服侍他人。",
            },
            {
                "en": "Hard work is sacred; honour the labour of your hands.",
                "zh": "辛勤工作是神聖的；敬重雙手之勞。",
            },
            {
                "en": "Know when to cut and when to build — iron serves both purposes.",
                "zh": "知道何時切割、何時建造——鐵服務於兩種目的。",
            },
        ],
        story_summary=(
            "Ogun cleared the way through the forest before any Orisha could enter "
            "the world. Without his iron, no path existed. He teaches that before "
            "any great work, there must be someone willing to do the hard, invisible "
            "labour of preparation."
        ),
        moral_teaching=(
            "Honour the sacred dignity of labour. Those who clear the way for "
            "others receive Ogun's blessing; those who destroy without purpose "
            "invite his wrath."
        ),
        advice=(
            "Hard work and determination will clear your path. Roll up your sleeves "
            "and tackle the obstacle directly. Honour Ogun by working with skill "
            "and integrity."
        ),
        ebo_suggestions=[
            "Iron tools, palm wine, and dog meat (traditional) offered to Ogun",
            "Green leaves and black cloth at the Ogun shrine",
            "Dedication of a work tool with prayer before a new project",
        ],
        short_ese_example={
            "en": (
                "Ogun did not wait for the forest to open —\n"
                "He lifted his iron and walked forward.\n"
                "Every road you travel was cut\n"
                "By someone who refused to stop."
            ),
            "zh": (
                "奧岡沒有等待森林自行打開——\n"
                "他舉起鐵刃，向前走去。\n"
                "你所走的每一條路，\n"
                "都是由某個拒絕停步的人開鑿的。"
            ),
        },
    ),

    # ── 10. Osa Meji ───────────────────────────────────────────────────────
    OduFull(
        id=10,
        yoruba_name="Osa Meji",
        meji_name="Osa Meji",
        english_name="The Swift Wind of Change",
        chinese_name="迅猛的變革之風",
        alternate_spellings=["Òsá", "Osa"],
        binary_pattern=[0, 1, 0, 1, 0, 1, 0, 1],
        marks=(False, True, False, True),
        principal_orishas=["Oya", "Sango"],
        orisha="Oya / Sango",
        colors=["purple", "maroon"],
        numbers=[9, 3],
        themes=["change", "storms", "feminine power", "swift action", "revolution", "Oya"],
        core_meaning_en=(
            "Osa Meji is the Odu of the swift, transformative wind governed by Oya. "
            "It heralds rapid change, the sweeping away of the old, and the emergence "
            "of something entirely new. Movement is the message of Osa."
        ),
        core_meaning_zh=(
            "Osa Meji 是由奧雅（Oya）掌管的迅猛轉化之風的神諕。"
            "它預示急速的變革、舊事物的掃除，以及全新事物的誕生。"
            "運動是 Osa 的訊息。"
        ),
        positive_aspects=[
            "Rapid positive change and breakthroughs",
            "Feminine power and assertiveness",
            "Ability to weather any storm",
            "Renewal after upheaval",
        ],
        challenges=[
            "Instability and loss of grounding",
            "Destruction without sufficient rebuilding",
            "Conflicts with authority",
        ],
        key_lessons=[
            {
                "en": "Move swiftly when change calls — hesitation in a storm invites more damage.",
                "zh": "當變革呼喚時迅速行動——在風暴中猶豫只會招致更多傷害。",
            },
            {
                "en": "The wind does not mourn what it scatters; trust the necessity of clearing.",
                "zh": "風不哀悼它所吹散的事物；信任清除的必要性。",
            },
            {
                "en": "Feminine power is not soft — Oya's winds rearrange entire landscapes.",
                "zh": "女性力量並不柔弱——奧雅的風能重塑整個地景。",
            },
        ],
        story_summary=(
            "Osa swept through the town without announcement, and everything loose "
            "went flying. Yet when the wind settled, the village stood stronger, "
            "for the rotten thatch had been removed and fresh air filled every room."
        ),
        moral_teaching=(
            "Welcome necessary disruption. What cannot withstand the wind "
            "was never meant to stay forever. Change is Oya's gift."
        ),
        advice=(
            "Rapid change is at hand. Move with it rather than against it. "
            "Let go of what must go and trust that the clearing makes room "
            "for something better."
        ),
        ebo_suggestions=[
            "Purple flowers and a copper bracelet offered to Oya",
            "Nine different types of fruit placed at the marketplace",
            "Wind-carried prayer — written on paper and released outdoors",
        ],
        short_ese_example={
            "en": (
                "Osa came before her name was called —\n"
                "She scattered the leaves, the fears, the stuck-fast doors.\n"
                "When the whirlwind passed, the old farmer laughed:\n"
                "She had blown away everything he no longer needed."
            ),
            "zh": (
                "Osa 在人們呼喚她名字之前便已來臨——\n"
                "她吹散了落葉、恐懼，以及那些緊閉的門。\n"
                "旋風過後，老農夫笑了：\n"
                "她帶走了一切他不再需要的東西。"
            ),
        },
    ),

    # ── 11. Ika Meji ───────────────────────────────────────────────────────
    OduFull(
        id=11,
        yoruba_name="Ika Meji",
        meji_name="Ika Meji",
        english_name="The Crossroads of Character",
        chinese_name="品格的十字路口",
        alternate_spellings=["Ìká", "Ika"],
        binary_pattern=[0, 1, 0, 1, 0, 1, 0, 1],  # Note: unique pattern
        marks=(False, True, False, True),
        principal_orishas=["Eshu", "Orunmila"],
        orisha="Eshu / Orunmila",
        colors=["black", "red"],
        numbers=[11, 4],
        themes=["character", "ethics", "choices", "cunning", "moral testing", "trickery"],
        core_meaning_en=(
            "Ika Meji governs the crossroads of character — the moment a person "
            "must choose between self-serving cunning and upright integrity. "
            "It warns against deception while honouring clever wisdom."
        ),
        core_meaning_zh=(
            "Ika Meji 掌管品格的十字路口——一個人必須在自私的狡詐與正直誠信之間選擇的時刻。"
            "它警示欺騙，同時讚揚聰慧的智慧。"
        ),
        positive_aspects=[
            "Sharp intelligence and problem-solving",
            "Ability to navigate complex social situations",
            "Cunning used in service of justice",
            "Discernment of others' true intentions",
        ],
        challenges=[
            "Tendency to deceive or manipulate",
            "Using cleverness to harm others",
            "Hidden enemies or betrayal from those trusted",
        ],
        key_lessons=[
            {
                "en": "Cleverness without integrity becomes a trap for its owner.",
                "zh": "缺乏正直的聰明，會成為其主人的陷阱。",
            },
            {
                "en": "Read the character of those around you — not everyone who smiles is a friend.",
                "zh": "辨識周圍人的品格——不是每個微笑的人都是朋友。",
            },
            {
                "en": "Iwa pele (gentle character) is the highest achievement of the Ifá path.",
                "zh": "溫和的品格（Iwa pele）是伊法之道的最高成就。",
            },
        ],
        story_summary=(
            "Ika came to a fork in the road and chose the longer, honest path over "
            "the shortcut that required deception. The shortcut collapsed behind the "
            "trickster, while Ika's road led to a city of light."
        ),
        moral_teaching=(
            "Iwa pele — gentle, upright character — is the only lasting currency. "
            "Tricks may win the day but lose the life."
        ),
        advice=(
            "Examine your choices carefully. Are they truly honest? "
            "Beware of shortcuts that require compromising your integrity. "
            "Be discerning about those around you."
        ),
        ebo_suggestions=[
            "Three kola nuts and red palm oil at a crossroads for Eshu",
            "A written pledge of ethical commitment placed on the personal altar",
            "Sharing a meal with an enemy as a gesture of reconciliation",
        ],
        short_ese_example={
            "en": (
                "Ika stood at the fork between two roads —\n"
                "One paved with clever stones, one with honest mud.\n"
                "The clever road gleamed but crumbled;\n"
                "The muddy road held every footprint of the faithful."
            ),
            "zh": (
                "Ika 站在兩條路的叉口——\n"
                "一條以聰明的石頭鋪就，一條以誠實的泥土鋪成。\n"
                "聰明的路閃亮卻崩塌；\n"
                "泥濘的路承載了每一個忠實者的足跡。"
            ),
        },
    ),

    # ── 12. Oturupon Meji ──────────────────────────────────────────────────
    OduFull(
        id=12,
        yoruba_name="Oturupon Meji",
        meji_name="Oturupon Meji",
        english_name="The Wisdom Drawn from Suffering",
        chinese_name="苦難中淬煉的智慧",
        alternate_spellings=["Òtúrúpòn", "Oturupon", "Oturupun"],
        binary_pattern=[1, 0, 0, 1, 1, 0, 0, 1],
        marks=(True, False, False, True),
        principal_orishas=["Sopona", "Obatala"],
        orisha="Sopona / Obatala",
        colors=["white", "red"],
        numbers=[12, 6],
        themes=["suffering", "endurance", "healing", "skin", "disease", "wisdom through pain"],
        core_meaning_en=(
            "Oturupon Meji speaks of endurance through affliction and the profound "
            "wisdom that only suffering can teach. It governs illness — especially "
            "of the skin — and the transformation that comes from facing the depths "
            "of hardship with patience and faith."
        ),
        core_meaning_zh=(
            "Oturupon Meji 訴說在苦難中堅忍，以及唯有苦難方能教導的深刻智慧。"
            "它掌管疾病——尤其是皮膚疾病——以及以耐心與信念面對艱辛深淵所帶來的轉化。"
        ),
        positive_aspects=[
            "Profound wisdom emerging from hardship",
            "Resilience and extraordinary endurance",
            "Healing after long illness",
            "Compassion born from personal suffering",
        ],
        challenges=[
            "Prolonged illness or physical suffering",
            "Bitterness or resentment from past wounds",
            "Social isolation due to affliction",
        ],
        key_lessons=[
            {
                "en": "Your deepest wounds, tended with patience, become your greatest gifts to others.",
                "zh": "以耐心對待你最深的傷口，它們將成為你給予他人的最大禮物。",
            },
            {
                "en": "Do not let bitterness take root in the soil of your suffering.",
                "zh": "不要讓苦澀在你苦難的土壤中紮根。",
            },
            {
                "en": "Those who have endured great pain carry a lantern for others in the dark.",
                "zh": "忍受過巨大痛苦的人，為黑暗中的他人提燈引路。",
            },
        ],
        story_summary=(
            "Oturupon was covered in sores and rejected by all. Yet it was Oturupon "
            "who had walked through the deepest fire and returned, carrying medicine "
            "for every affliction. The one the world scorned became the one the world needed."
        ),
        moral_teaching=(
            "Suffering is not the final word. Those who endure with dignity "
            "and faith emerge carrying wisdom that cannot be learned any other way."
        ),
        advice=(
            "You may be passing through a period of difficulty. Do not despair — "
            "this trial is forging wisdom within you. Seek healing, maintain faith, "
            "and remember that this, too, shall pass."
        ),
        ebo_suggestions=[
            "White and red cloth offered to Obatala for healing",
            "Herbal bath with healing plants for purification",
            "A white candle lit with a prayer for restoration of health",
        ],
        short_ese_example={
            "en": (
                "Oturupon wore every scar like a map —\n"
                "Each one a road into a country\n"
                "Only the wounded can visit.\n"
                "The healer's hands are always marked."
            ),
            "zh": (
                "Oturupon 將每一道傷疤視如地圖——\n"
                "每一條都是通往一個國度的路，\n"
                "唯有受過傷者方能踏入。\n"
                "療癒者的雙手，永遠留有印記。"
            ),
        },
    ),

    # ── 13. Otura Meji ─────────────────────────────────────────────────────
    OduFull(
        id=13,
        yoruba_name="Otura Meji",
        meji_name="Otura Meji",
        english_name="The Covenant of Heaven and Earth",
        chinese_name="天地之盟約",
        alternate_spellings=["Òtúrá", "Otura"],
        binary_pattern=[1, 0, 1, 0, 1, 0, 1, 0],
        marks=(True, False, True, False),
        principal_orishas=["Obatala", "Orunmila"],
        orisha="Obatala / Orunmila",
        colors=["white", "blue"],
        numbers=[13, 8],
        themes=["covenants", "higher truths", "destiny", "spiritual law", "elevation", "divinity"],
        core_meaning_en=(
            "Otura Meji is the Odu of sacred covenants between heaven and Earth, "
            "governing divine law, the fulfilment of destiny (ori), and the elevation "
            "of the human spirit toward the divine. It speaks of the highest spiritual "
            "responsibilities."
        ),
        core_meaning_zh=(
            "Otura Meji 是天地神聖盟約的神諕，掌管神法、命運（ori）的實現，"
            "以及人類靈魂向神性的提升。它訴說最崇高的靈性責任。"
        ),
        positive_aspects=[
            "Alignment with divine destiny and higher purpose",
            "Spiritual elevation and enlightenment",
            "Fulfilment of sacred covenants and promises",
            "Access to elevated wisdom and teaching",
        ],
        challenges=[
            "Breaking sacred promises or vows",
            "Neglecting one's spiritual obligations",
            "Pride in spiritual achievement",
        ],
        key_lessons=[
            {
                "en": "Your life is a covenant with the divine — live in alignment with its terms.",
                "zh": "你的生命是與神聖的盟約——依照其條款而活。",
            },
            {
                "en": "Keep your promises, for sacred covenants bind across lifetimes.",
                "zh": "守護你的承諾，因為神聖的盟約跨越生生世世。",
            },
            {
                "en": "Spiritual elevation is earned through integrity, not claimed through words.",
                "zh": "靈性提升是以正直贏得的，而非以言語宣稱的。",
            },
        ],
        story_summary=(
            "Otura stood at the boundary between heaven and Earth and was asked to "
            "carry divine messages back and forth. He agreed, and for this agreement "
            "he was granted insight into the laws that govern all creation. "
            "To break his word would be to break the world."
        ),
        moral_teaching=(
            "Live according to your highest covenant. The divine does not forget "
            "what you have promised, nor does it withhold from those who keep faith."
        ),
        advice=(
            "Take your spiritual commitments seriously. Review any promises or vows "
            "you have made and honour them. This is a time of spiritual deepening "
            "and alignment with your highest destiny."
        ),
        ebo_suggestions=[
            "White dove or white pigeons released in prayer",
            "White cloth and shea butter offered to Obatala",
            "Renewal of a vow at dawn with fresh water and prayer",
        ],
        short_ese_example={
            "en": (
                "Otura stood where the sky meets the sea —\n"
                "Each step he took was a word he had spoken to God.\n"
                "He did not step back.\n"
                "The covenant holds the cosmos together."
            ),
            "zh": (
                "Otura 站在天空與海洋相遇之處——\n"
                "他所走的每一步，都是他曾對神所說的話。\n"
                "他沒有退縮。\n"
                "盟約將宇宙凝聚在一起。"
            ),
        },
    ),

    # ── 14. Irete Meji ─────────────────────────────────────────────────────
    OduFull(
        id=14,
        yoruba_name="Irete Meji",
        meji_name="Irete Meji",
        english_name="The Patience of the Ancient Tree",
        chinese_name="古樹之耐力",
        alternate_spellings=["Ìrẹtẹ̀", "Irete"],
        binary_pattern=[0, 1, 1, 1, 0, 1, 1, 1],
        marks=(False, True, True, True),
        principal_orishas=["Orisha Oko", "Orunmila"],
        orisha="Orisha Oko / Orunmila",
        colors=["brown", "green"],
        numbers=[14, 7],
        themes=["patience", "agriculture", "ancient wisdom", "long-term vision", "trees", "roots"],
        core_meaning_en=(
            "Irete Meji carries the wisdom of the ancient tree — deep roots, patient "
            "growth, and the long-term perspective of one who has seen many seasons. "
            "It governs agriculture, community prosperity, and enduring foundations."
        ),
        core_meaning_zh=(
            "Irete Meji 承載古樹的智慧——深根、耐心的生長，以及見過無數季節者的長遠視野。"
            "它掌管農業、社群繁榮，以及持久的根基。"
        ),
        positive_aspects=[
            "Deep roots and stable foundations",
            "Long-term success through patient effort",
            "Community wealth and shared prosperity",
            "Ancient wisdom and ancestral guidance",
        ],
        challenges=[
            "Impatience and desire for quick results",
            "Neglect of foundations for short-term gain",
            "Stubbornness in the face of necessary change",
        ],
        key_lessons=[
            {
                "en": "Deep roots are more valuable than fast growth — invest in foundations.",
                "zh": "深根比速成更有價值——投資於根基。",
            },
            {
                "en": "The ancient tree has survived many storms because it learned to bend without breaking.",
                "zh": "古樹能在無數風暴中存活，因為它學會了彎曲而不折斷。",
            },
            {
                "en": "Community wealth outlasts individual wealth — build together.",
                "zh": "社群財富比個人財富更持久——共同建造。",
            },
        ],
        story_summary=(
            "Irete planted a seed and returned generations later to find a forest. "
            "The farmer who had doubted him had grown old waiting for quick results "
            "and had nothing, while the patient planter had left a legacy for all."
        ),
        moral_teaching=(
            "Plant seeds you may never harvest. The most enduring gifts are given "
            "without expectation of immediate reward."
        ),
        advice=(
            "This is not a time for rush or shortcuts. Plant carefully, tend "
            "patiently, and trust that consistent effort accumulates into lasting "
            "success. Think in decades, not days."
        ),
        ebo_suggestions=[
            "Planting a tree or tending an existing one as offering",
            "Yam and palm oil offered to Orisha Oko",
            "Food shared with the elderly as an act of honour",
        ],
        short_ese_example={
            "en": (
                "Irete did not hurry the roots —\n"
                "She knew that what feeds the tree in darkness\n"
                "Lifts it beyond the height of storms.\n"
                "Plant with the patience of eternity."
            ),
            "zh": (
                "Irete 不催促根的生長——\n"
                "她知道在黑暗中滋養樹木的，\n"
                "將把它提升到風暴所及之上。\n"
                "以永恆的耐心播種。"
            ),
        },
    ),

    # ── 15. Ose Meji ───────────────────────────────────────────────────────
    OduFull(
        id=15,
        yoruba_name="Ose Meji",
        meji_name="Ose Meji",
        english_name="The Sweetness of the Sacred Feminine",
        chinese_name="神聖女性的甘甜",
        alternate_spellings=["Òsé", "Ose"],
        binary_pattern=[1, 0, 1, 1, 1, 0, 1, 1],  # unique pattern for Ose
        marks=(True, False, True, True),
        principal_orishas=["Osun"],
        orisha="Osun",
        colors=["yellow", "gold", "amber"],
        numbers=[5, 15],
        themes=["love", "beauty", "fertility", "wealth", "Osun", "relationships", "arts"],
        core_meaning_en=(
            "Ose Meji is Osun's own Odu — governing love, beauty, fertility, art, "
            "and the sweetness of life. It teaches that the sacred feminine is "
            "indispensable to all flourishing, and that beauty itself is divine."
        ),
        core_meaning_zh=(
            "Ose Meji 是奧遜（Osun）自己的神諕——掌管愛、美、生育、藝術，"
            "以及生命的甘美。它教導神聖的女性力量對一切繁榮不可或缺，"
            "美麗本身即是神聖的。"
        ),
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
        key_lessons=[
            {
                "en": "Honour the sacred feminine in all its forms — in women, in nature, in yourself.",
                "zh": "在所有形式中敬重神聖的女性——在女性中、在自然中、在你自己中。",
            },
            {
                "en": "Love generously and beauty will flow through all you do.",
                "zh": "慷慨地愛，美麗將流淌於你所做的一切之中。",
            },
            {
                "en": "Sweetness and joy are not luxuries — they are spiritual necessities.",
                "zh": "甘甜與喜悅不是奢侈品——它們是靈性的必需品。",
            },
            {
                "en": "Do not underestimate the power of beauty and love to heal the world.",
                "zh": "不要低估美麗與愛治癒世界的力量。",
            },
        ],
        story_summary=(
            "When the Orisha first came to Earth they overlooked Osun because she "
            "was a woman. Their plans all failed until they returned to honour her. "
            "Ose Meji teaches that the sweetness and wisdom of the divine feminine "
            "are indispensable to all human flourishing."
        ),
        moral_teaching=(
            "Honour the sacred feminine in all its forms. Love generously "
            "and beauty will flow through all you do."
        ),
        advice=(
            "Love and abundance are flowing toward you. Open your heart and "
            "hands to receive. This is a favourable time for romance, creative "
            "projects, and matters of beauty. Honour Osun."
        ),
        ebo_suggestions=[
            "Yellow flowers and honey offered to Osun at a river or fountain",
            "Sweet oranges and brass jewellery as gifts to Osun",
            "A yellow candle lit with a prayer for love and abundance",
        ],
        short_ese_example={
            "en": (
                "Osun dipped her hand in the river and drew out gold —\n"
                "Not for herself alone, but for all who thirsted.\n"
                "Where love flows freely,\n"
                "Even the desert learns to bloom."
            ),
            "zh": (
                "奧遜將手伸入河中，取出黃金——\n"
                "不只為她自己，而是為所有乾渴之人。\n"
                "在愛自由流淌之處，\n"
                "即便沙漠也學會了盛開。"
            ),
        },
    ),

    # ── 16. Ofun Meji ──────────────────────────────────────────────────────
    OduFull(
        id=16,
        yoruba_name="Ofun Meji",
        meji_name="Ofun Meji",
        english_name="The Wisdom of the Completed Cycle",
        chinese_name="圓滿週期的智慧",
        alternate_spellings=["Òfún", "Ofun"],
        binary_pattern=[0, 0, 1, 0, 0, 0, 1, 0],
        marks=(False, False, True, False),
        principal_orishas=["Obatala", "Orunmila"],
        orisha="Obatala / Orunmila",
        colors=["white", "red"],
        numbers=[16, 10],
        themes=["completion", "speech", "power of words", "transformation", "cycles", "blessings"],
        core_meaning_en=(
            "Ofun Meji is the sixteenth and final principal Odu, governing "
            "completion, transformation through suffering, the immense power of "
            "speech, and the ultimate reconciliation of opposites at cycle's end. "
            "Every word carries the weight of a lifetime."
        ),
        core_meaning_zh=(
            "Ofun Meji 是第十六個也是最後一個主要神諕，掌管圓滿、苦難中的轉化、"
            "語言的巨大力量，以及週期終結時對立面的最終和解。"
            "每一個字都承載著一生的重量。"
        ),
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
        key_lessons=[
            {
                "en": "Guard your speech — words once spoken cannot be recalled, but their ripples travel forever.",
                "zh": "守護你的言語——說出的話無法收回，但它的漣漪永遠傳播。",
            },
            {
                "en": "Every ending contains within it the seed of a new beginning.",
                "zh": "每個終結之中，都蘊藏著新開始的種子。",
            },
            {
                "en": "Your life's trials are your greatest teachers — let them speak through you, not for you.",
                "zh": "你生命中的考驗是你最偉大的老師——讓它們透過你說話，而非替你說話。",
            },
            {
                "en": "The completion of a cycle is cause for gratitude, not grief.",
                "zh": "一個週期的圓滿是感恩的理由，而非悲傷的緣由。",
            },
        ],
        story_summary=(
            "Ofun had suffered greatly and carried many scars. Yet when Ofun spoke, "
            "everyone fell silent, for each word carried the weight of a lifetime. "
            "Ifá says: the one who has walked through fire speaks words that can "
            "either burn or illuminate — choose your words with great care."
        ),
        moral_teaching=(
            "Guard your speech. Words once spoken cannot be recalled. "
            "Use your voice as a tool of healing, not destruction. "
            "Your life's trials are your greatest teachers."
        ),
        advice=(
            "A major cycle in your life is completing. Reflect on what you have "
            "learned and speak your truth with care and wisdom. Watch your words — "
            "they carry great power now."
        ),
        ebo_suggestions=[
            "Sixteen cowries at the base of a large tree or family shrine",
            "White and red cloth with obi kola as offering",
            "A spoken prayer of gratitude for the completed cycle",
        ],
        short_ese_example={
            "en": (
                "Ofun carried sixteen scars and a lantern —\n"
                "The scars were his credential,\n"
                "The lantern was his gift.\n"
                "When all cycles end, light remains."
            ),
            "zh": (
                "Ofun 帶著十六道傷疤和一盞燈籠——\n"
                "傷疤是他的資歷，\n"
                "燈籠是他的贈禮。\n"
                "當所有週期終結，光明依然留存。"
            ),
        },
    ),
]


# ===========================================================================
# Build quick-lookup maps for the 16 Meji
# ===========================================================================

_MEJI_BY_NUMBER: Dict[int, OduFull] = {o.id: o for o in _MEJI_DATA}

# Maps the short Yoruba root name (lower-case) to its bit pattern
# e.g. "ogbe" → [1, 1, 1, 1],  "oyeku" → [0, 0, 0, 0]
_ROOT_NAMES = [
    "ogbe", "oyeku", "iwori", "odi",
    "irosun", "owonrin", "obara", "okanran",
    "ogunda", "osa", "ika", "oturupon",
    "otura", "irete", "ose", "ofun",
]

_MEJI_BITS: List[List[int]] = [
    _marks_to_bits(m.marks) for m in _MEJI_DATA  # type: ignore[arg-type]
]


# ===========================================================================
# Composite (minor) Odu — generated from parent Meji pairs
# ===========================================================================

def _build_composite_odu() -> List[OduFull]:
    """Generate the 240 composite Odu from all cross-pairings of the 16 Meji."""
    composites: List[OduFull] = []
    odu_id = 17  # IDs 1–16 are Meji

    for left_idx in range(16):          # 0-based index into 16 Meji
        for right_idx in range(16):
            if left_idx == right_idx:   # Meji — already included
                continue

            left_meji  = _MEJI_DATA[left_idx]
            right_meji = _MEJI_DATA[right_idx]

            left_root  = _ROOT_NAMES[left_idx]
            right_root = _ROOT_NAMES[right_idx]

            # Capitalise for display
            left_cap  = left_root.capitalize()
            right_cap = right_root.capitalize()

            yoruba_name  = f"{left_cap} {right_cap}"
            english_name = (
                f"{left_meji.english_name.split('The ')[-1]} "
                f"meeting {right_meji.english_name.split('The ')[-1]}"
            )
            chinese_name = f"{left_meji.chinese_name}與{right_meji.chinese_name}"

            # 8-bit pattern: left arm = left Meji bits, right arm = right Meji bits
            binary_pattern = _MEJI_BITS[left_idx] + _MEJI_BITS[right_idx]

            # Orisha blend
            orishas = list(dict.fromkeys(
                left_meji.principal_orishas + right_meji.principal_orishas
            ))[:3]

            core_en = (
                f"{yoruba_name} arises from the meeting of {left_meji.yoruba_name}'s energy "
                f"({left_meji.core_meaning_en[:80].rstrip()}…) with "
                f"{right_meji.yoruba_name}'s energy "
                f"({right_meji.core_meaning_en[:80].rstrip()}…). "
                f"Their interplay shapes the context of this reading."
            )
            core_zh = (
                f"{yoruba_name} 由 {left_meji.yoruba_name} 的能量"
                f"（{left_meji.core_meaning_zh[:40].rstrip()}……）"
                f"與 {right_meji.yoruba_name} 的能量"
                f"（{right_meji.core_meaning_zh[:40].rstrip()}……）交融而生。"
                f"兩者的交織塑造了此次占卜的脈絡。"
            )

            key_lessons = [
                {
                    "en": (
                        f"Integrate the qualities of {left_cap} ({left_meji.themes[0] if left_meji.themes else 'light'}) "
                        f"with those of {right_cap} ({right_meji.themes[0] if right_meji.themes else 'change'})."
                    ),
                    "zh": (
                        f"整合 {left_cap}（{left_meji.themes[0] if left_meji.themes else '光明'}）"
                        f"與 {right_cap}（{right_meji.themes[0] if right_meji.themes else '變化'}）的特質。"
                    ),
                },
                {
                    "en": left_meji.key_lessons[0]["en"] if left_meji.key_lessons else "",
                    "zh": left_meji.key_lessons[0]["zh"] if left_meji.key_lessons else "",
                },
                {
                    "en": right_meji.key_lessons[0]["en"] if right_meji.key_lessons else "",
                    "zh": right_meji.key_lessons[0]["zh"] if right_meji.key_lessons else "",
                },
            ]

            ebo_suggestions = (
                left_meji.ebo_suggestions[:1] + right_meji.ebo_suggestions[:1]
            )

            short_ese = {
                "en": (
                    f"{left_cap} and {right_cap} walked together —\n"
                    f"One carrying {left_meji.themes[0] if left_meji.themes else 'light'},\n"
                    f"The other bearing {right_meji.themes[0] if right_meji.themes else 'change'}.\n"
                    f"In their meeting, the oracle speaks."
                ),
                "zh": (
                    f"{left_cap} 與 {right_cap} 同行——\n"
                    f"一者攜帶{'、'.join(left_meji.themes[:2]) if left_meji.themes else '光明'}，\n"
                    f"另一者承載{'、'.join(right_meji.themes[:2]) if right_meji.themes else '變化'}。\n"
                    f"在它們的相遇中，神諕開口說話。"
                ),
            }

            composites.append(OduFull(
                id=odu_id,
                yoruba_name=yoruba_name,
                english_name=english_name,
                chinese_name=chinese_name,
                binary_pattern=binary_pattern,
                principal_orishas=orishas,
                core_meaning_en=core_en,
                core_meaning_zh=core_zh,
                key_lessons=key_lessons,
                ebo_suggestions=ebo_suggestions,
                short_ese_example=short_ese,
                left_parent_id=left_idx + 1,   # 1-based
                right_parent_id=right_idx + 1,
            ))
            odu_id += 1

    return composites


_COMPOSITE_DATA: List[OduFull] = _build_composite_odu()


# ===========================================================================
# Public collections
# ===========================================================================

# All 256 Odu in traditional order (16 Meji first, then 240 composites)
ODU_FULL_LIST: List[OduFull] = _MEJI_DATA + _COMPOSITE_DATA

# Lookup by 1-based ID (1–256)
ODU_FULL_BY_ID: Dict[int, OduFull] = {o.id: o for o in ODU_FULL_LIST}

# Lookup by lower-case Yoruba name  e.g. "eji ogbe", "ogbe oyeku"
ODU_FULL_BY_NAME: Dict[str, OduFull] = {
    o.yoruba_name.lower(): o for o in ODU_FULL_LIST
}

# Lookup by (left_parent_id, right_parent_id) — convenient for divination
ODU_FULL_BY_PARENTS: Dict[Tuple[int, int], OduFull] = {}
for _o in ODU_FULL_LIST:
    if _o.is_meji():
        ODU_FULL_BY_PARENTS[(_o.id, _o.id)] = _o
    else:
        assert _o.left_parent_id is not None and _o.right_parent_id is not None
        ODU_FULL_BY_PARENTS[(_o.left_parent_id, _o.right_parent_id)] = _o


# ===========================================================================
# Compatibility bridge: enrich legacy Odu objects with Chinese names
# ===========================================================================

def get_chinese_name(odu_number: int) -> str:
    """Return the Chinese name for one of the 16 principal Odu (1–16).

    Raises KeyError for out-of-range numbers.
    """
    return _MEJI_BY_NUMBER[odu_number].chinese_name


def get_odu_full_from_legacy(legacy_odu: Odu) -> OduFull:
    """Return the OduFull object that corresponds to a legacy Odu instance."""
    return ODU_FULL_BY_ID[legacy_odu.number]


# ===========================================================================
# Convenience: export a JSON-serialisable list of all 256 Odu
# ===========================================================================

def to_json_list() -> List[dict]:
    """Return all 256 Odu as a list of plain dicts (JSON-serialisable).

    Tuple fields are converted to lists for JSON compatibility.
    """
    result = []
    for o in ODU_FULL_LIST:
        d = {
            "id": o.id,
            "yoruba_name": o.yoruba_name,
            "english_name": o.english_name,
            "chinese_name": o.chinese_name,
            "binary_pattern": list(o.binary_pattern),
            "principal_orishas": list(o.principal_orishas),
            "core_meaning_en": o.core_meaning_en,
            "core_meaning_zh": o.core_meaning_zh,
            "key_lessons": o.key_lessons,
            "ebo_suggestions": o.ebo_suggestions,
            "ebo_caveat": o.ebo_caveat,
            "short_ese_example": o.short_ese_example,
            "is_meji": o.is_meji(),
            "left_parent_id": o.left_parent_id,
            "right_parent_id": o.right_parent_id,
        }
        result.append(d)
    return result
