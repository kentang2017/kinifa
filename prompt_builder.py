"""
prompt_builder.py — Ifá Oracle: Enhanced Interpretation Prompt Builder

Generates structured, bilingual (English + 繁體中文) prompt strings for
Ifá-style poetic interpretation.  The prompts are designed to be passed
to a local or cloud LLM when the user opts in; until then, the generated
string is displayed directly in the UI as a "ready-to-use" template.

═══════════════════════════════════════════════════════════════════════
⚠️ Educational note — This module produces educational, culturally
respectful prompt text.  It does NOT call any external AI service.
Real Ifá interpretation requires a trained Babalawo or Iyanifa.
═══════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

from typing import Optional


# ---------------------------------------------------------------------------
# System prompt (bilingual)
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT_EN = """\
You are a respectful scholar of Ifá tradition, conveying the wisdom of \
Orunmila to a seeker.  Your tone is wise, poetic, and balanced.

Rules:
• Honour the sacred nature of the Odu.  Avoid trivialising the tradition.
• Emphasise free will, ebo (remedy), and personal responsibility — \
never fatalism.
• Structure every interpretation with: Positive Potential, Challenges, \
and Suggested Actions.
• End with a strong reminder that this is for educational purposes only \
and that real Ifá divination requires a qualified Babalawo or Iyanifa.
• Avoid modern "self-help" or motivational-poster language.  Maintain \
cultural accuracy and poetic depth."""

_SYSTEM_PROMPT_ZH = """\
你是一位尊重伊法傳統的學者，正在傳遞來自奧倫米拉（Orunmila）的智慧。
你的語調智慧、詩意、平衡。

規則：
• 敬重神諕（Odu）的神聖本質，不可輕率對待傳統。
• 強調自由意志、ebo（補救）與個人責任——絕不宿命論。
• 每次解讀必須包含：正面潛力、挑戰、建議行動。
• 結尾必須強烈提醒：此解讀僅供教育用途，真正的伊法占卜需要合格的 \
Babalawo 或 Iyanifa。
• 避免現代心靈雞湯式語言，保持文化準確性與詩意深度。"""


# ---------------------------------------------------------------------------
# Question-category labels (bilingual)
# ---------------------------------------------------------------------------

QUESTION_CATEGORIES = {
    "love":      {"en": "Love & Relationships", "zh": "感情與關係"},
    "career":    {"en": "Career & Wealth",       "zh": "事業與財富"},
    "health":    {"en": "Health & Wellbeing",     "zh": "健康與身心"},
    "family":    {"en": "Family & Home",          "zh": "家庭與居所"},
    "spiritual": {"en": "Spiritual Growth",       "zh": "靈性成長"},
    "general":   {"en": "General Guidance",        "zh": "整體指引"},
}


# ---------------------------------------------------------------------------
# Core builder
# ---------------------------------------------------------------------------

def build_enhanced_prompt(
    *,
    odu_name: str,
    odu_english_name: str,
    odu_chinese_name: str,
    core_meaning_en: str,
    core_meaning_zh: str,
    key_lessons_en: list[str],
    key_lessons_zh: list[str],
    orishas: list[str],
    ese_en: str = "",
    ese_zh: str = "",
    question: str = "",
    question_category: str = "general",
    lang: str = "en",
) -> str:
    """Return a rich, formatted prompt string for Ifá-style interpretation.

    Parameters
    ----------
    odu_name : str          Yoruba name, e.g. "Eji Ogbe".
    odu_english_name : str  English translation.
    odu_chinese_name : str  Chinese translation.
    core_meaning_en/zh      Core meaning paragraphs.
    key_lessons_en/zh       Lists of lesson strings.
    orishas                 List of associated Orisha names.
    ese_en / ese_zh         Short ese (poem) example.
    question                User's question (may be empty).
    question_category       One of QUESTION_CATEGORIES keys.
    lang                    "en" or "zh" — determines which system prompt
                            appears first, but both languages are always
                            included in the output.

    Returns
    -------
    str   A ready-to-use prompt string (no external API call is made).
    """
    cat_label = QUESTION_CATEGORIES.get(question_category, QUESTION_CATEGORIES["general"])

    # ── Assemble prompt sections ──────────────────────────────────────
    lines: list[str] = []

    # System instruction
    lines.append("═" * 60)
    lines.append("SYSTEM PROMPT / 系統指令")
    lines.append("═" * 60)
    if lang == "zh":
        lines.append(_SYSTEM_PROMPT_ZH)
        lines.append("")
        lines.append(_SYSTEM_PROMPT_EN)
    else:
        lines.append(_SYSTEM_PROMPT_EN)
        lines.append("")
        lines.append(_SYSTEM_PROMPT_ZH)

    lines.append("")
    lines.append("═" * 60)
    lines.append("CONTEXT / 背景")
    lines.append("═" * 60)
    lines.append("")

    # Odu identity
    lines.append(f"Odu:  {odu_name}")
    lines.append(f"English name:  {odu_english_name}")
    lines.append(f"中文名稱:  {odu_chinese_name}")
    lines.append(f"Associated Orishas:  {', '.join(orishas) if orishas else 'N/A'}")
    lines.append("")

    # Core meaning
    lines.append("── Core Meaning (English) ──")
    lines.append(core_meaning_en)
    lines.append("")
    lines.append("── 核心含義（中文）──")
    lines.append(core_meaning_zh)
    lines.append("")

    # Key lessons
    if key_lessons_en:
        lines.append("── Key Lessons (English) ──")
        for i, lesson in enumerate(key_lessons_en, 1):
            lines.append(f"  {i}. {lesson}")
        lines.append("")
    if key_lessons_zh:
        lines.append("── 重點教導（中文）──")
        for i, lesson in enumerate(key_lessons_zh, 1):
            lines.append(f"  {i}. {lesson}")
        lines.append("")

    # Ese example
    if ese_en:
        lines.append("── Ese Verse Example ──")
        lines.append(ese_en)
        lines.append("")
    if ese_zh:
        lines.append("── 詩節範例 ──")
        lines.append(ese_zh)
        lines.append("")

    # User context
    lines.append("═" * 60)
    lines.append("USER QUERY / 使用者提問")
    lines.append("═" * 60)
    lines.append(f"Category / 類別:  {cat_label['en']}  ({cat_label['zh']})")
    if question:
        lines.append(f"Question / 問題:  {question}")
    else:
        lines.append("Question / 問題:  (No specific question — general guidance requested)")
    lines.append("")

    # Expected output structure
    lines.append("═" * 60)
    lines.append("REQUESTED OUTPUT STRUCTURE / 輸出結構")
    lines.append("═" * 60)
    lines.append("""
Please produce a bilingual interpretation with the following sections:

1. 🌅 Positive Potential / 正面潛力
   — What blessings or opportunities does this Odu illuminate?

2. ⚡ Challenges / 挑戰與警示
   — What obstacles or pitfalls should the seeker be mindful of?

3. 🌿 Suggested Actions / 建議行動
   — Practical and spiritual steps (including ebo if appropriate).

4. ✦ Poetic Reflection / 詩意省思
   — A short poetic paragraph in the voice of the Odu.

5. ⚠️ Disclaimer / 免責聲明
   — Remind the user this is educational only.  Real divination
     requires a qualified Babalawo or Iyanifa.

Each section must appear in BOTH English and 繁體中文.
""")

    lines.append("═" * 60)
    lines.append("⚠️ DISCLAIMER / 免責聲明")
    lines.append("═" * 60)
    lines.append(
        "This prompt and any text generated from it are for EDUCATIONAL "
        "purposes only.  They do not constitute authentic Ifá divination.  "
        "For genuine spiritual guidance, consult a qualified Babalawo or Iyanifa."
    )
    lines.append(
        "此提示及由其產生的任何文字僅供教育用途，不構成真正的伊法占卜。"
        "如需真正的靈性指引，請諮詢合格的 Babalawo 或 Iyanifa。"
    )

    return "\n".join(lines)
