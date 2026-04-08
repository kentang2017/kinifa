"""
streamlit_app.py — KinIfá 堅伊法 — Sacred Ifá Learning Interface

A bilingual (繁體中文 + English) Streamlit application for respectful,
educational exploration of the Ifá divination tradition.

Usage:
    streamlit run streamlit_app.py

⚠️ Cultural note — This tool is for education only.  It does NOT replace
authentic divination by a qualified Babalawo or Iyanifa.
"""

from __future__ import annotations

import time
from datetime import datetime
from typing import Optional

import streamlit as st

from divination import IkinsOracle, DivinationResult
from odu_data import Odu, ODU_LIST, ODU_BY_NUMBER, SINGLE, DOUBLE
from odu_data_zh import ODU_ZH_BY_NUMBER, ZH_UI, OduZh
from odu_data_full import ODU_FULL_BY_ID, OduFull
from prompt_builder import build_enhanced_prompt, QUESTION_CATEGORIES


# ═══════════════════════════════════════════════════════════════════════════
# Page configuration
# ═══════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="KinIfá 堅伊法",
    page_icon="🔮",
    layout="wide",
)


# ═══════════════════════════════════════════════════════════════════════════
# Custom CSS — sacred earth-tone theme
# ═══════════════════════════════════════════════════════════════════════════

_SACRED_CSS = """
<style>
/* ── Global palette ─────────────────────────────────────────────────── */
:root {
    --kf-bg:         #1a1a12;
    --kf-bg-card:    #252518;
    --kf-gold:       #d4af37;
    --kf-gold-dim:   #a68928;
    --kf-green:      #3a6b35;
    --kf-green-dim:  #2d5229;
    --kf-brown:      #5c4033;
    --kf-cream:      #f5f0e1;
    --kf-text:       #e8e0cc;
    --kf-text-dim:   #a09880;
    --kf-border:     #3a3828;
}

/* ── Main area ──────────────────────────────────────────────────────── */
.stApp, [data-testid="stAppViewContainer"] {
    background-color: var(--kf-bg) !important;
    color: var(--kf-text) !important;
}

/* ── Sidebar ────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #1e1e14 !important;
    border-right: 1px solid var(--kf-border) !important;
}
[data-testid="stSidebar"] * {
    color: var(--kf-text) !important;
}

/* ── Headings ───────────────────────────────────────────────────────── */
h1, h2, h3, h4, h5, h6 {
    color: var(--kf-gold) !important;
    font-family: Georgia, 'Noto Serif TC', serif !important;
}

/* ── Text ───────────────────────────────────────────────────────────── */
p, li, span, label, .stMarkdown {
    color: var(--kf-text) !important;
}

/* ── Cards / containers ─────────────────────────────────────────────── */
[data-testid="stExpander"],
.stAlert,
[data-testid="stMetric"] {
    background-color: var(--kf-bg-card) !important;
    border: 1px solid var(--kf-border) !important;
    border-radius: 8px !important;
}

/* ── Tabs ───────────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background-color: var(--kf-bg-card) !important;
    border-radius: 8px 8px 0 0;
    gap: 0px;
}
.stTabs [data-baseweb="tab"] {
    color: var(--kf-text-dim) !important;
    background-color: transparent !important;
    border: none !important;
    padding: 0.75rem 1.25rem !important;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    color: var(--kf-gold) !important;
    border-bottom: 2px solid var(--kf-gold) !important;
    background-color: rgba(212, 175, 55, 0.08) !important;
}

/* ── Primary button ─────────────────────────────────────────────────── */
.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"] {
    background-color: var(--kf-green) !important;
    color: var(--kf-cream) !important;
    border: 1px solid var(--kf-gold-dim) !important;
    border-radius: 8px !important;
    font-size: 1.1rem !important;
    padding: 0.6rem 2rem !important;
    transition: all 0.3s ease;
}
.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="stBaseButton-primary"]:hover {
    background-color: var(--kf-gold-dim) !important;
    color: #1a1a12 !important;
}

/* ── Text input / select ────────────────────────────────────────────── */
input, textarea, [data-baseweb="select"] {
    background-color: var(--kf-bg-card) !important;
    color: var(--kf-text) !important;
    border: 1px solid var(--kf-border) !important;
    border-radius: 6px !important;
}

/* ── Code blocks (Odu figures) ──────────────────────────────────────── */
code, pre {
    background-color: #1e1e14 !important;
    color: var(--kf-gold) !important;
    font-family: 'Courier New', 'Noto Sans Mono', monospace !important;
    font-size: 1.25rem !important;
    line-height: 1.8 !important;
}

/* ── Disclaimer banner ──────────────────────────────────────────────── */
.disclaimer-banner {
    background: linear-gradient(135deg, #2d2210, #1e1e14);
    border: 1px solid var(--kf-gold-dim);
    border-left: 4px solid var(--kf-gold);
    border-radius: 6px;
    padding: 1rem 1.25rem;
    margin: 1rem 0;
    color: var(--kf-text-dim);
    font-size: 0.9rem;
    line-height: 1.6;
}

/* ── Sacred header ──────────────────────────────────────────────────── */
.sacred-header {
    text-align: center;
    padding: 1.5rem 0 1rem;
    border-bottom: 1px solid var(--kf-border);
    margin-bottom: 1.5rem;
}
.sacred-header h1 {
    font-size: 2.2rem !important;
    letter-spacing: 0.15em;
    margin-bottom: 0.2rem;
}
.sacred-header .odu-symbols {
    font-family: 'Courier New', monospace;
    color: var(--kf-gold-dim);
    font-size: 1rem;
    letter-spacing: 0.4em;
}
.sacred-header .subtitle {
    color: var(--kf-text-dim);
    font-size: 0.95rem;
    margin-top: 0.3rem;
}

/* ── Odu large figure ───────────────────────────────────────────────── */
.odu-figure-large {
    font-family: 'Courier New', monospace;
    font-size: 1.5rem;
    line-height: 2;
    color: var(--kf-gold);
    text-align: center;
    padding: 1rem;
    background: #1e1e14;
    border-radius: 8px;
    border: 1px solid var(--kf-border);
}

/* ── Divider ────────────────────────────────────────────────────────── */
.sacred-divider {
    text-align: center;
    color: var(--kf-gold-dim);
    font-size: 0.85rem;
    letter-spacing: 0.5em;
    margin: 1rem 0;
}

/* ── Mobile-friendly adjustments ────────────────────────────────────── */
@media (max-width: 768px) {
    .sacred-header h1 { font-size: 1.6rem !important; }
    .odu-figure-large { font-size: 1.2rem; }
    code, pre { font-size: 1.05rem !important; }
}
</style>
"""

st.markdown(_SACRED_CSS, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════
# Session state
# ═══════════════════════════════════════════════════════════════════════════

if "lang" not in st.session_state:
    st.session_state.lang = "zh"

if "oracle" not in st.session_state:
    st.session_state.oracle = IkinsOracle()


# ═══════════════════════════════════════════════════════════════════════════
# Language helpers
# ═══════════════════════════════════════════════════════════════════════════

def is_zh() -> bool:
    return st.session_state.lang == "zh"


# Bilingual UI strings
_EN_UI = {
    "app_title": "KinIfá 堅伊法",
    "app_subtitle": "Orunmila's Wisdom · Sacred Learning Tool",
    "divination": "Divination",
    "browse_odu": "Browse Odu",
    "view_odu": "View Odu",
    "about": "About Ifá",
    "disclaimer": "Cultural Disclaimer",
    "method_opele": "Ọ̀pẹ̀lẹ̀ (Chain) Casting",
    "method_ikin": "Ikin (Palm Nuts) Divination",
    "enter_question": "Enter your question (optional):",
    "cast_button": "🎴  Cast Divination",
    "odu_number": "Odu #",
    "meji_name": "Meji Name",
    "english_name": "English Name",
    "chinese_name": "Chinese Name",
    "orisha": "Ruling Orisha",
    "primary_meaning": "Primary Meaning",
    "themes": "Themes",
    "positive_aspects": "Positive Aspects",
    "challenges": "Challenges & Cautions",
    "story": "Teaching Story",
    "moral": "Moral Teaching",
    "advice": "Advice",
    "ebo": "Ebo (Offering) Suggestion",
    "ebo_caveat": (
        "⚠️ Ebo guidance here is simplified for educational purposes only. "
        "Actual ebo prescription requires consultation with a qualified Babalawo."
    ),
    "figure": "Odu Figure",
    "mark_single": "Single mark (I) — odd count — 1",
    "mark_double": "Double mark (II) — even count — 0",
    "select_odu": "Select an Odu to view details:",
    "general_guidance": "General Guidance",
    "contextual_guidance": "🔍 Contextual Guidance",
    "cultural_notice_title": "⚠️ Cultural Respect Notice",
    "cultural_notice": (
        "Ifá is a living, sacred oral tradition of the Yoruba people of "
        "West Africa, inscribed on the UNESCO Intangible Cultural Heritage list.\n\n"
        "This software is a respectful educational tool for learning about Ifá "
        "philosophy and culture. It is **NOT** a substitute for authentic divination "
        "by a qualified Babalawo (Ifá priest) or Iyanifa (female Ifá practitioner).\n\n"
        "Ifá emphasises: **cause and consequence, not fatalism**. Every challenge has "
        "a prescribed remedy (ebo). Every path can be improved."
    ),
    "about_ifa_title": "About Ifá",
    "about_ifa": (
        "Ifá is the divination system and body of spiritual wisdom of the Yoruba people "
        "of West Africa. It is also practised widely in the African diaspora — in Brazil "
        "(as Candomblé / Umbanda), Cuba (as Lucumí / Santería), Haiti, Trinidad, and beyond.\n\n"
        "The system was bestowed upon humanity by Orunmila, the Orisha of wisdom and "
        "divination, acting as witness to human destiny (ayanmo).\n\n"
        "● **256 Odù Ifá** — the sacred corpus of knowledge, each with hundreds of ẹsẹ "
        "(poetic verses), stories, proverbs, and prescriptions.\n\n"
        "● **16 Principal Odù (Meji)** — the 16 'mother' Odu from which all 256 are derived.\n\n"
        "● **Babalawo / Iyanifa** — initiated Ifá priests/priestesses who undergo years "
        "of training to memorise the vast oral corpus.\n\n"
        "● **Ẹbọ (Ebo)** — offerings and prescribed actions that can alter or improve "
        "one's destiny path.\n\n"
        "● **Divination tools:**\n"
        "  - Ọ̀pẹ̀lẹ̀ (Opele) — a chain of eight half-seed pods, cast in one throw. "
        "Fast and widely used for general consultations.\n"
        "  - Ikin — sixteen consecrated palm nuts manipulated to generate a figure. "
        "More solemn; used for deeper matters."
    ),
    "language": "Language / 語言",
    "lang_zh": "中文",
    "lang_en": "English",
    "sacred_colors": "Sacred Colours",
    "also_known_as": "Also known as",
    "your_question": "❓ Your Question",
    "casting_result": "Divination Result",
    "method_label_opele": "Ọ̀pẹ̀lẹ̀ (Chain) Casting",
    "method_label_ikin": "Ikin (Palm Nut) Divination",
    "footer": "Àṣẹ — may the blessings of Orunmila guide your path.",
    "question_category": "Question Focus",
    "casting_animation": "The sacred instruments are speaking…",
    "tab_core": "✦ Core Message",
    "tab_details": "📖 Details & Ese",
    "tab_orisha": "🌿 Orisha & Ebo",
    "tab_culture": "📝 Cultural Notes",
    "tab_enhanced": "🔮 Enhanced Interpretation",
    "enhanced_toggle": "Enable Enhanced Interpretation (Prompt Preview)",
    "enhanced_note": (
        "This generates a structured prompt template for Ifá-style interpretation. "
        "No external AI is called — the prompt is displayed for review."
    ),
}


def t(key: str) -> str:
    """Translate UI key to current language text."""
    if is_zh() and key in ZH_UI:
        return ZH_UI[key]
    return _EN_UI.get(key, key)


# ═══════════════════════════════════════════════════════════════════════════
# Rendering helpers
# ═══════════════════════════════════════════════════════════════════════════

def get_zh(odu_number: int) -> Optional[OduZh]:
    """Get Chinese data for an Odu by number."""
    return ODU_ZH_BY_NUMBER.get(odu_number)


def _disclaimer_html(lang: str = "en") -> str:
    """Return the disclaimer as an HTML banner."""
    if lang == "zh":
        return (
            '<div class="disclaimer-banner">'
            "⚠️ <b>文化尊重聲明</b> — 伊法（Ifá）是約魯巴人活的、神聖的口述傳統，"
            "已被聯合國教科文組織列入非物質文化遺產名錄。本工具僅供教育與學習使用，"
            "<b>絕對不能取代</b>合格的 Babalawo 或 Iyanifa 進行的真正占卜。"
            "</div>"
        )
    return (
        '<div class="disclaimer-banner">'
        "⚠️ <b>Cultural Respect Notice</b> — Ifá is a living, sacred oral tradition "
        "of the Yoruba people, inscribed on the UNESCO Intangible Cultural Heritage list. "
        "This tool is for <b>educational purposes only</b> and is NOT a substitute for "
        "authentic divination by a qualified Babalawo or Iyanifa."
        "</div>"
    )


def render_disclaimer() -> None:
    """Render the bilingual disclaimer banner."""
    st.markdown(_disclaimer_html("zh" if is_zh() else "en"), unsafe_allow_html=True)


def render_odu_figure_large(odu: Odu) -> None:
    """Render the Odu figure with large monospace symbols."""
    lines = odu.figure_lines()
    figure_html = "<br>".join(
        line.replace(" ", "&nbsp;") for line in lines
    )
    st.markdown(
        f'<div class="odu-figure-large">{figure_html}</div>',
        unsafe_allow_html=True,
    )
    st.caption(f"  |   = {t('mark_single')}  ·   | |  = {t('mark_double')}")


def render_sacred_divider() -> None:
    """Render a decorative divider."""
    st.markdown(
        '<div class="sacred-divider">✦ ─── ✦ ─── ✦</div>',
        unsafe_allow_html=True,
    )


def _get_odu_full(odu_number: int) -> Optional[OduFull]:
    """Get the OduFull record for a principal Odu by its 1-16 number."""
    return ODU_FULL_BY_ID.get(odu_number)


# ═══════════════════════════════════════════════════════════════════════════
# Odu display — tabbed layout
# ═══════════════════════════════════════════════════════════════════════════

def display_odu_tabs(
    odu: Odu,
    *,
    question: str = "",
    question_category: str = "general",
    context_note: str = "",
    show_enhanced: bool = False,
) -> None:
    """Display Odu information using st.tabs for clean, layered presentation."""
    zh = get_zh(odu.number)
    full = _get_odu_full(odu.number)

    # ── Header ────────────────────────────────────────────────────────
    header_text = f"✦ Odu #{odu.number:02d} — {odu.meji_name}"
    if zh and is_zh():
        header_text += f" — {zh.chinese_name}"
    st.markdown(f"### {header_text}")

    if is_zh() and zh:
        st.markdown(f"**{odu.english_name}** · {zh.english_name_zh}")
    else:
        st.markdown(f"**{odu.english_name}**")

    if odu.alternate_spellings:
        st.caption(f"{t('also_known_as')}: {' / '.join(odu.alternate_spellings)}")

    # ── Tabs ──────────────────────────────────────────────────────────
    tab_labels = [
        t("tab_core"),
        t("tab_details"),
        t("tab_orisha"),
        t("tab_culture"),
    ]
    if show_enhanced:
        tab_labels.append(t("tab_enhanced"))

    tabs = st.tabs(tab_labels)

    # ── Tab 1: Core message + Odu symbol ──────────────────────────────
    with tabs[0]:
        render_odu_figure_large(odu)
        render_sacred_divider()

        st.markdown(f"#### ✦ {t('primary_meaning')}")
        if is_zh() and zh:
            st.info(zh.primary_meaning)
            with st.expander("English"):
                st.write(odu.primary_meaning)
        else:
            st.info(odu.primary_meaning)

        # Key lessons from OduFull (if available)
        if full and full.key_lessons:
            st.markdown("#### 🔑 Key Lessons / 重點教導" if is_zh() else "#### 🔑 Key Lessons")
            for lesson in full.key_lessons:
                if is_zh():
                    st.markdown(f"- {lesson.get('zh', lesson.get('en', ''))}")
                else:
                    st.markdown(f"- {lesson.get('en', '')}")

        # Contextual guidance (from divination)
        if context_note:
            render_sacred_divider()
            st.markdown(f"#### {t('contextual_guidance')}")
            st.info(context_note)

    # ── Tab 2: Detailed meaning & Ese ─────────────────────────────────
    with tabs[1]:
        # Themes
        if is_zh() and zh:
            st.markdown(f"**{t('themes')}:** {' · '.join(zh.themes)}")
        else:
            st.markdown(f"**{t('themes')}:** {' · '.join(theme.title() for theme in odu.themes)}")

        # Positive aspects & Challenges
        col_pos, col_chal = st.columns(2)
        with col_pos:
            st.markdown(f"#### ☀ {t('positive_aspects')}")
            items = zh.positive_aspects if (is_zh() and zh) else odu.positive_aspects
            for item in items:
                st.markdown(f"- ✓ {item}")
        with col_chal:
            st.markdown(f"#### ⚡ {t('challenges')}")
            items = zh.challenges if (is_zh() and zh) else odu.challenges
            for item in items:
                st.markdown(f"- ⚠ {item}")

        render_sacred_divider()

        # Story
        st.markdown(f"#### 📖 {t('story')}")
        if is_zh() and zh:
            st.write(zh.story_summary)
            with st.expander("English"):
                st.write(odu.story_summary)
        else:
            st.write(odu.story_summary)

        # Moral teaching
        st.markdown(f"#### ❝ {t('moral')} ❞")
        if is_zh() and zh:
            st.success(zh.moral_teaching)
            with st.expander("English"):
                st.write(odu.moral_teaching)
        else:
            st.success(odu.moral_teaching)

        # Ese (poem) from OduFull
        if full and full.short_ese_example:
            render_sacred_divider()
            st.markdown("#### ✦ Ese (Sacred Verse) / 神聖詩節")
            ese = full.short_ese_example
            if is_zh() and ese.get("zh"):
                st.markdown(f"```\n{ese['zh']}\n```")
                with st.expander("English"):
                    st.markdown(f"```\n{ese.get('en', '')}\n```")
            elif ese.get("en"):
                st.markdown(f"```\n{ese['en']}\n```")

    # ── Tab 3: Orisha & Ebo ───────────────────────────────────────────
    with tabs[2]:
        # Orisha
        if odu.orisha:
            st.markdown(f"#### 🌿 {t('orisha')}")
            st.markdown(f"**{odu.orisha}**")
        if full and full.principal_orishas:
            st.markdown("**Associated Orishas:** " + " · ".join(full.principal_orishas))

        if odu.colors:
            st.markdown(f"**{t('sacred_colors')}:** {', '.join(odu.colors)}")

        render_sacred_divider()

        # Advice
        st.markdown(f"#### 🌿 {t('advice')}")
        if is_zh() and zh:
            st.write(zh.advice)
            with st.expander("English"):
                st.write(odu.advice)
        else:
            st.write(odu.advice)

        render_sacred_divider()

        # Ebo
        st.markdown(f"#### 🕯 {t('ebo')}")
        if is_zh() and zh:
            st.write(zh.ebo_suggestion)
            with st.expander("English"):
                st.write(odu.ebo_suggestion)
        else:
            st.write(odu.ebo_suggestion)

        # Ebo from OduFull (list format)
        if full and full.ebo_suggestions:
            st.markdown("**Specific suggestions / 具體建議：**")
            for suggestion in full.ebo_suggestions:
                st.markdown(f"- {suggestion}")

        st.caption(t("ebo_caveat"))

    # ── Tab 4: Cultural Notes ─────────────────────────────────────────
    with tabs[3]:
        st.markdown("#### 📝 Cultural Context / 文化脈絡")
        st.markdown(t("cultural_notice"))

        render_sacred_divider()

        about_heading = "#### About Ifá Divination / 關於伊法占卜" if is_zh() else "#### About Ifá Divination"
        st.markdown(about_heading)
        st.markdown(
            "Ifá is a **living, sacred oral tradition** of the Yoruba people. "
            "The 256 Odù Ifá form one of humanity's most complex knowledge systems. "
            "Each Odu contains hundreds of *ẹsẹ* (verses), proverbs, and prescriptions.\n\n"
            "The divination tools simulated here — Ọ̀pẹ̀lẹ̀ (chain) and Ikin (palm nuts) — "
            "are consecrated instruments used by trained Babalawo. This simulation "
            "is for cultural education only."
        )
        if is_zh():
            st.markdown(
                "伊法是約魯巴人**活的、神聖的口述傳統**。256 個神諕構成了人類最複雜的知識體系之一。"
                "每個 Odu 包含數百首 *ẹsẹ*（詩節）、諺語和處方。\n\n"
                "此處模擬的占卜工具——Ọ̀pẹ̀lẹ̀（占卜鏈）和 Ikin（棕櫚果）——"
                "是受過訓練的 Babalawo 使用的神聖器具。此模擬僅供文化教育之用。"
            )

    # ── Tab 5: Enhanced Interpretation (optional) ─────────────────────
    if show_enhanced and len(tabs) > 4:
        with tabs[4]:
            st.markdown("#### 🔮 Enhanced Interpretation Prompt / 增強解讀提示")
            if is_zh():
                st.caption(
                    "此功能產生結構化提示範本，供伊法風格的詩意解讀使用。"
                    "目前不呼叫任何外部 AI 服務——僅顯示提示文字。"
                )
            else:
                st.caption(t("enhanced_note"))

            # Build prompt from OduFull / OduZh data
            if full:
                key_lessons_en = [l.get("en", "") for l in full.key_lessons]
                key_lessons_zh = [l.get("zh", "") for l in full.key_lessons]
                orishas = full.principal_orishas
                ese_en = full.short_ese_example.get("en", "")
                ese_zh = full.short_ese_example.get("zh", "")
                chinese_name = full.chinese_name
            else:
                key_lessons_en = []
                key_lessons_zh = []
                orishas = []
                ese_en = ""
                ese_zh = ""
                chinese_name = zh.chinese_name if zh else ""

            prompt_text = build_enhanced_prompt(
                odu_name=odu.meji_name,
                odu_english_name=odu.english_name,
                odu_chinese_name=chinese_name,
                core_meaning_en=odu.primary_meaning,
                core_meaning_zh=zh.primary_meaning if zh else odu.primary_meaning,
                key_lessons_en=key_lessons_en,
                key_lessons_zh=key_lessons_zh,
                orishas=orishas,
                ese_en=ese_en,
                ese_zh=ese_zh,
                question=question,
                question_category=question_category,
                lang=st.session_state.lang,
            )
            st.code(prompt_text, language=None)


# ═══════════════════════════════════════════════════════════════════════════
# Casting animation
# ═══════════════════════════════════════════════════════════════════════════

def _casting_animation(method: str) -> None:
    """Show a brief animation simulating the divination casting."""
    if method == "opele":
        steps = [
            "🔗 The Ọ̀pẹ̀lẹ̀ chain is lifted…" if not is_zh()
            else "🔗 占卜鏈被拿起……",
            "🌿 Prayers to Orunmila…" if not is_zh()
            else "🌿 向奧倫米拉祈禱……",
            "🎴 The chain falls…" if not is_zh()
            else "🎴 鏈條落下……",
        ]
    else:
        steps = [
            "🌴 Sixteen Ikin are gathered…" if not is_zh()
            else "🌴 十六顆棕櫚果被聚攏……",
            "🙏 Prayers to Orunmila…" if not is_zh()
            else "🙏 向奧倫米拉祈禱……",
            "✋ The palm nuts are passed…" if not is_zh()
            else "✋ 棕櫚果在雙手間傳遞……",
            "📿 Marks are recorded…" if not is_zh()
            else "📿 標記被記錄……",
        ]

    progress_bar = st.progress(0)
    status_text = st.empty()
    total_steps = len(steps)
    for i, step_text in enumerate(steps):
        status_text.markdown(f"*{step_text}*")
        progress_bar.progress((i + 1) / total_steps)
        time.sleep(0.6)
    status_text.empty()
    progress_bar.empty()


# ═══════════════════════════════════════════════════════════════════════════
# Sacred header
# ═══════════════════════════════════════════════════════════════════════════

def render_header() -> None:
    """Render the sacred application header with Odu symbols."""
    st.markdown(
        '<div class="sacred-header">'
        '<h1>🔮 KinIfá 堅伊法</h1>'
        '<div class="odu-symbols">|&nbsp;&nbsp;|&nbsp;&nbsp;||&nbsp;&nbsp;|&nbsp;&nbsp;||&nbsp;&nbsp;|&nbsp;&nbsp;|&nbsp;&nbsp;||</div>'
        '<div class="subtitle">Orunmila\'s Wisdom · 奧倫米拉的智慧 · Sacred Learning Tool</div>'
        '</div>',
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Sidebar
# ═══════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🔮 KinIfá 堅伊法")

    # Language toggle
    lang_options = ["中文", "English"]
    lang_idx = 0 if st.session_state.lang == "zh" else 1
    selected_lang = st.radio(
        t("language"),
        lang_options,
        index=lang_idx,
        horizontal=True,
    )
    st.session_state.lang = "zh" if selected_lang == "中文" else "en"

    st.divider()

    # Navigation
    page_options = {
        "divination": f"🎴 {t('divination')}",
        "browse": f"📋 {t('browse_odu')}",
        "view": f"🔍 {t('view_odu')}",
        "about": f"📖 {t('about')}",
        "disclaimer": f"⚠️ {t('disclaimer')}",
    }
    page = st.radio(
        "Navigation" if not is_zh() else "導航",
        list(page_options.keys()),
        format_func=lambda x: page_options[x],
    )

    st.divider()
    st.caption(t("footer"))


# ═══════════════════════════════════════════════════════════════════════════
# Pages
# ═══════════════════════════════════════════════════════════════════════════

if page == "divination":
    render_header()
    render_disclaimer()

    # ── Method + question category + question ─────────────────────────
    col_method, col_cat = st.columns([1, 1])

    with col_method:
        method = st.radio(
            "Method" if not is_zh() else "占卜方式",
            ["opele", "ikin"],
            format_func=lambda x: t("method_opele") if x == "opele" else t("method_ikin"),
        )

    with col_cat:
        cat_keys = list(QUESTION_CATEGORIES.keys())
        cat_labels = [
            f"{QUESTION_CATEGORIES[k]['zh']}  ({QUESTION_CATEGORIES[k]['en']})"
            if is_zh()
            else QUESTION_CATEGORIES[k]["en"]
            for k in cat_keys
        ]
        cat_label = "問題類別" if is_zh() else "Question Focus"
        selected_cat_label = st.selectbox(cat_label, cat_labels)
        selected_cat = cat_keys[cat_labels.index(selected_cat_label)]

    question = st.text_input(
        t("enter_question"),
        placeholder="例如：我應該接受這份新工作嗎？" if is_zh() else "e.g., Should I accept this new job offer?",
    )

    # Enhanced interpretation toggle
    enhanced = st.toggle(
        "🔮 Enhanced Interpretation / 增強解讀" if is_zh() else "🔮 Enhanced Interpretation",
        value=False,
        help=t("enhanced_note") if not is_zh() else (
            "產生結構化提示範本，供伊法風格的詩意解讀使用。不呼叫外部 AI。"
        ),
    )

    render_sacred_divider()

    # ── Cast button ───────────────────────────────────────────────────
    if st.button(t("cast_button"), type="primary", use_container_width=True):
        _casting_animation(method)

        oracle: IkinsOracle = st.session_state.oracle
        result = oracle.divine(method=method, question=question if question else None)

        render_sacred_divider()

        # Method & time
        if result.method == "opele":
            method_label = t("method_label_opele")
        else:
            method_label = t("method_label_ikin")

        st.markdown(f"### ✦ {t('casting_result')} — {method_label}")
        st.caption(result.timestamp.strftime("%Y-%m-%d  %H:%M"))

        # Question echo
        if result.question:
            st.markdown(f"#### {t('your_question')}")
            st.write(result.question)

        render_sacred_divider()

        # Tabbed Odu display
        display_odu_tabs(
            result.odu,
            question=question,
            question_category=selected_cat,
            context_note=result.context_note,
            show_enhanced=enhanced,
        )

        # Bottom disclaimer
        render_sacred_divider()
        render_disclaimer()


elif page == "browse":
    render_header()
    st.title(f"📋 {t('browse_odu')}")
    if is_zh():
        st.markdown("所有 16 個主要神諕（Meji）一覽表")
    else:
        st.markdown("All 16 Principal Odu (Meji)")

    # Build table data
    table_data = []
    for odu in ODU_LIST:
        zh = get_zh(odu.number)
        row = {
            "#": odu.number,
            "Meji": odu.meji_name,
        }
        if is_zh() and zh:
            row["中文名稱"] = zh.chinese_name
        row["English Name"] = odu.english_name
        row["Orisha"] = odu.orisha
        table_data.append(row)

    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True,
    )


elif page == "view":
    render_header()
    st.title(f"🔍 {t('view_odu')}")

    # Selector
    odu_options = {
        odu.number: f"#{odu.number:02d} — {odu.meji_name} — {odu.english_name}"
        + (f" — {get_zh(odu.number).chinese_name}" if (is_zh() and get_zh(odu.number)) else "")
        for odu in ODU_LIST
    }

    selected = st.selectbox(
        t("select_odu"),
        list(odu_options.keys()),
        format_func=lambda x: odu_options[x],
    )

    if selected:
        st.divider()
        display_odu_tabs(ODU_BY_NUMBER[selected], show_enhanced=False)


elif page == "about":
    render_header()
    st.title(f"📖 {t('about_ifa_title')}")
    st.markdown(t("about_ifa"))


elif page == "disclaimer":
    render_header()
    st.title(t("cultural_notice_title"))
    st.markdown(t("cultural_notice"))
