"""
streamlit_app.py — 伊法神諕 Streamlit 版本（中英雙語）

Ifá Oracle — Orunmila's Wisdom — Bilingual Streamlit Interface

Usage:
    streamlit run streamlit_app.py
"""

from __future__ import annotations

import streamlit as st
from datetime import datetime

from divination import IkinsOracle, DivinationResult
from odu_data import Odu, ODU_LIST, ODU_BY_NUMBER, SINGLE, DOUBLE
from odu_data_zh import ODU_ZH_BY_NUMBER, ZH_UI, OduZh


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="KinIfá 堅伊法",
    page_icon="🔮",
    layout="wide",
)


# ---------------------------------------------------------------------------
# Language state
# ---------------------------------------------------------------------------

if "lang" not in st.session_state:
    st.session_state.lang = "zh"

if "oracle" not in st.session_state:
    st.session_state.oracle = IkinsOracle()


def is_zh() -> bool:
    return st.session_state.lang == "zh"


def t(key: str) -> str:
    """Translate UI key to current language text."""
    if is_zh() and key in ZH_UI:
        return ZH_UI[key]
    # English fallbacks
    en_ui = {
        "app_title": "Ifá Oracle — Orunmila's Wisdom",
        "app_subtitle": "伊法神諕 — 奧倫米拉的智慧",
        "divination": "Divination",
        "browse_odu": "Browse Odu",
        "view_odu": "View Odu",
        "about": "About Ifá",
        "disclaimer": "Cultural Disclaimer",
        "method_opele": "Ọ̀pẹ̀lẹ̀ (Chain) Casting",
        "method_ikin": "Ikin (Palm Nuts) Divination",
        "enter_question": "Enter your question (optional):",
        "cast_button": "Cast Divination",
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
    }
    return en_ui.get(key, key)


# ---------------------------------------------------------------------------
# Odu rendering helpers
# ---------------------------------------------------------------------------

def get_zh(odu_number: int) -> OduZh | None:
    """Get Chinese data for an Odu by number."""
    return ODU_ZH_BY_NUMBER.get(odu_number)


def display_odu_card(odu: Odu, show_ebo: bool = True) -> None:
    """Display a full Odu card in the Streamlit UI."""
    zh = get_zh(odu.number)

    # Header
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

    # Figure
    st.markdown(f"#### ⊕ {t('figure')}")
    st.code(odu.figure_str(), language=None)
    st.caption(f"  |   = {t('mark_single')}  ·   | |  = {t('mark_double')}")

    # Primary meaning
    st.markdown(f"#### ✦ {t('primary_meaning')}")
    if is_zh() and zh:
        st.info(zh.primary_meaning)
        with st.expander("English"):
            st.write(odu.primary_meaning)
    else:
        st.info(odu.primary_meaning)

    # Themes & Orisha
    col1, col2 = st.columns(2)
    with col1:
        if is_zh() and zh:
            st.markdown(f"**{t('themes')}:** {' · '.join(zh.themes)}")
        else:
            st.markdown(f"**{t('themes')}:** {' · '.join(theme.title() for theme in odu.themes)}")
    with col2:
        if odu.orisha:
            st.markdown(f"**{t('orisha')}:** {odu.orisha}")
        if odu.colors:
            st.markdown(f"**{t('sacred_colors')}:** {', '.join(odu.colors)}")

    # Positive aspects & challenges
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

    # Advice
    st.markdown(f"#### 🌿 {t('advice')}")
    if is_zh() and zh:
        st.write(zh.advice)
        with st.expander("English"):
            st.write(odu.advice)
    else:
        st.write(odu.advice)

    # Ebo
    if show_ebo:
        st.markdown(f"#### 🕯 {t('ebo')}")
        if is_zh() and zh:
            st.write(zh.ebo_suggestion)
            with st.expander("English"):
                st.write(odu.ebo_suggestion)
        else:
            st.write(odu.ebo_suggestion)
        st.caption(t("ebo_caveat"))


def display_result(result: DivinationResult) -> None:
    """Display a divination result."""
    zh = get_zh(result.odu.number)

    # Preamble
    if result.method == "opele":
        method_label = t("method_label_opele")
    else:
        method_label = t("method_label_ikin")

    st.markdown(f"### ✦ {t('casting_result')} — {method_label}")
    st.caption(result.timestamp.strftime("%Y-%m-%d  %H:%M"))

    # Question
    if result.question:
        st.markdown(f"#### {t('your_question')}")
        st.write(result.question)

    st.divider()

    # Full Odu card
    display_odu_card(result.odu, show_ebo=True)

    # Contextual guidance
    if result.question and result.context_note:
        st.divider()
        st.markdown(f"#### {t('contextual_guidance')}")
        st.info(result.context_note)


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("## 🔮 伊法神諕 / Ifá Oracle")

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


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

if page == "divination":
    st.title(f"🎴 {t('divination')}")
    st.markdown(t("cultural_notice"))

    col_method, col_question = st.columns([1, 2])

    with col_method:
        method = st.radio(
            "Method" if not is_zh() else "占卜方式",
            ["opele", "ikin"],
            format_func=lambda x: t("method_opele") if x == "opele" else t("method_ikin"),
        )

    with col_question:
        question = st.text_input(
            t("enter_question"),
            placeholder="例如：我應該接受這份新工作嗎？" if is_zh() else "e.g., Should I accept this new job offer?",
        )

    if st.button(t("cast_button"), type="primary", use_container_width=True):
        oracle = st.session_state.oracle
        result = oracle.divine(method=method, question=question if question else None)

        st.divider()
        display_result(result)


elif page == "browse":
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
        display_odu_card(ODU_BY_NUMBER[selected])


elif page == "about":
    st.title(f"📖 {t('about_ifa_title')}")
    st.markdown(t("about_ifa"))


elif page == "disclaimer":
    st.title(t("cultural_notice_title"))
    st.markdown(t("cultural_notice"))
