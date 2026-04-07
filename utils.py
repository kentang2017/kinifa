"""
utils.py — Ifá Oracle: Display & Formatting Utilities

All rich text formatting for the CLI lives here so that other modules
(and future web/Telegram front-ends) can import just the logic they need.
"""

from __future__ import annotations

import textwrap
from typing import Optional

from odu_data import Odu, SINGLE, DOUBLE

# ---------------------------------------------------------------------------
# Terminal colour helpers (no third-party library required)
# ---------------------------------------------------------------------------

_COLOURS = {
    "reset":  "\033[0m",
    "bold":   "\033[1m",
    "dim":    "\033[2m",
    "yellow": "\033[33m",
    "cyan":   "\033[36m",
    "green":  "\033[32m",
    "red":    "\033[31m",
    "blue":   "\033[34m",
    "magenta":"\033[35m",
    "white":  "\033[97m",
}

_USE_COLOUR = True   # set to False for plain-text output


def _c(text: str, *codes: str) -> str:
    """Wrap *text* in ANSI colour codes when colour is enabled."""
    if not _USE_COLOUR:
        return text
    prefix = "".join(_COLOURS.get(c, "") for c in codes)
    return f"{prefix}{text}{_COLOURS['reset']}"


def disable_colour() -> None:
    """Turn off ANSI colour codes (e.g., when piping output)."""
    global _USE_COLOUR
    _USE_COLOUR = False


# ---------------------------------------------------------------------------
# Width / wrapping
# ---------------------------------------------------------------------------

TERMINAL_WIDTH = 72
SECTION_SEP = _c("─" * TERMINAL_WIDTH, "dim")


def _wrap(text: str, indent: int = 0) -> str:
    prefix = " " * indent
    return textwrap.fill(text, width=TERMINAL_WIDTH, initial_indent=prefix,
                         subsequent_indent=prefix)


# ---------------------------------------------------------------------------
# Odu figure renderer
# ---------------------------------------------------------------------------

def render_odu_figure(odu: Odu) -> str:
    """Return an ASCII Odu figure as a multi-line string.

    Each row shows left and right columns (identical for Meji) plus
    a brief label on the first row.
    """
    lines = odu.figure_lines()
    label = _c(f"  ← {odu.meji_name} →", "dim")

    output_lines = []
    for i, line in enumerate(lines):
        row = _c(line, "yellow", "bold")
        if i == 1:
            row = f"{row}  {label}"
        output_lines.append(row)
    return "\n".join(output_lines)


def render_mark_legend() -> str:
    """Return a one-line legend explaining the mark symbols."""
    single = _c(SINGLE.strip(), "yellow")
    double = _c(DOUBLE.strip(), "cyan")
    return (
        f"  {single} = Single mark (I)  — odd count — 1\n"
        f"  {double} = Double mark (II) — even count — 0"
    )


# ---------------------------------------------------------------------------
# Full Odu card
# ---------------------------------------------------------------------------

def render_odu_card(odu: Odu, show_ebo: bool = True) -> str:
    """Return a fully formatted Odu information card."""
    parts: list[str] = []

    # ── Header ──────────────────────────────────────────────────────────
    parts.append(SECTION_SEP)
    header = f"  Odu #{odu.number:02d}  ✦  {odu.meji_name}  ✦  {odu.english_name}"
    parts.append(_c(header, "cyan", "bold"))
    if odu.alternate_spellings:
        alt = " / ".join(odu.alternate_spellings)
        parts.append(_c(f"  Also known as: {alt}", "dim"))
    parts.append(SECTION_SEP)

    # ── Figure ──────────────────────────────────────────────────────────
    parts.append("")
    parts.append(_c("  ⊕ ODU FIGURE", "yellow", "bold"))
    parts.append("")
    for line in render_odu_figure(odu).splitlines():
        parts.append(f"    {line}")
    parts.append("")
    parts.append(render_mark_legend())
    parts.append("")

    # ── Primary meaning ─────────────────────────────────────────────────
    parts.append(SECTION_SEP)
    parts.append(_c("  ✦ PRIMARY MEANING", "cyan", "bold"))
    parts.append("")
    parts.append(_wrap(odu.primary_meaning, indent=4))
    parts.append("")

    # ── Themes ──────────────────────────────────────────────────────────
    themes_str = "  •  ".join(t.title() for t in odu.themes)
    parts.append(_c(f"  Themes: ", "bold") + _c(themes_str, "green"))
    if odu.orisha:
        parts.append(_c(f"  Ruling Orisha: ", "bold") + _c(odu.orisha, "magenta"))
    if odu.colors:
        parts.append(_c(f"  Sacred colours: ", "bold") + ", ".join(odu.colors))
    parts.append("")

    # ── Positive aspects & challenges ───────────────────────────────────
    parts.append(SECTION_SEP)
    parts.append(_c("  ☀  POSITIVE ASPECTS", "green", "bold"))
    for item in odu.positive_aspects:
        parts.append(f"    ✓  {item}")
    parts.append("")
    parts.append(_c("  ⚡ CHALLENGES & CAUTIONS", "red", "bold"))
    for item in odu.challenges:
        parts.append(f"    !  {item}")
    parts.append("")

    # ── Story / ẹsẹ summary ──────────────────────────────────────────────
    parts.append(SECTION_SEP)
    parts.append(_c("  📖 TEACHING STORY (ẹsẹ)", "yellow", "bold"))
    parts.append("")
    parts.append(_wrap(odu.story_summary, indent=4))
    parts.append("")

    # ── Moral teaching ──────────────────────────────────────────────────
    parts.append(_c("  ❝ MORAL TEACHING ❞", "cyan", "bold"))
    parts.append("")
    parts.append(_wrap(odu.moral_teaching, indent=6))
    parts.append("")

    # ── Advice ──────────────────────────────────────────────────────────
    parts.append(SECTION_SEP)
    parts.append(_c("  🌿 ADVICE FOR THE QUERENT", "green", "bold"))
    parts.append("")
    parts.append(_wrap(odu.advice, indent=4))
    parts.append("")

    # ── Ebo suggestion ──────────────────────────────────────────────────
    if show_ebo:
        parts.append(SECTION_SEP)
        parts.append(_c("  🕯  EBO (OFFERING) SUGGESTION", "magenta", "bold"))
        parts.append("")
        parts.append(_wrap(odu.ebo_suggestion, indent=4))
        parts.append("")
        parts.append(_wrap(odu.ebo_caveat, indent=4))
        parts.append("")

    parts.append(SECTION_SEP)
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Divination result renderer
# ---------------------------------------------------------------------------

def render_result(result, show_ebo: bool = True) -> str:
    """Render a DivinationResult to a full formatted string.

    Parameters
    ----------
    result : DivinationResult
    show_ebo : bool
        Whether to include the ebo suggestion section.
    """
    parts: list[str] = []

    # ── Preamble ────────────────────────────────────────────────────────
    parts.append("")
    parts.append(SECTION_SEP)
    method_label = "Ọ̀pẹ̀lẹ̀ (Chain) Casting" if result.method == "opele" \
                   else "Ikin (Palm-Nut) Divination"
    parts.append(_c(f"  ✦ IFÁ ORACLE  —  {method_label}", "cyan", "bold"))
    ts = result.timestamp.strftime("%Y-%m-%d  %H:%M")
    parts.append(_c(f"  {ts}", "dim"))
    if result.seed is not None:
        parts.append(_c(f"  Seed: {result.seed}", "dim"))
    parts.append(SECTION_SEP)

    # ── Question ────────────────────────────────────────────────────────
    if result.question:
        parts.append("")
        parts.append(_c("  ❓ YOUR QUESTION", "yellow", "bold"))
        parts.append(_wrap(result.question, indent=4))
        parts.append("")

    # ── Main Odu card ───────────────────────────────────────────────────
    parts.append(render_odu_card(result.odu, show_ebo=show_ebo))

    # ── Contextual note if question was provided ─────────────────────────
    if result.question and result.context_note:
        parts.append(SECTION_SEP)
        parts.append(_c("  🔍 CONTEXTUAL GUIDANCE", "cyan", "bold"))
        parts.append("")
        parts.append(_wrap(result.context_note, indent=4))
        parts.append("")
        parts.append(SECTION_SEP)

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Banner & disclaimers
# ---------------------------------------------------------------------------

IFA_BANNER = r"""
  ___  __ _    ___  _ __ __ _  ___| | ___
 |_ / |  |_|  / _ \| '__/ _` |/ __| |/ _ \
  | |_| |_|  | (_) | | | (_| | (__| |  __/
 |___/\__, |  \___/|_|  \__,_|\___|_|\___|
      |___/

  I F Á   O R A C L E   —   Orunmila's Wisdom
"""

CULTURAL_DISCLAIMER = """
┌─────────────────────────────────────────────────────────────────────┐
│                     CULTURAL RESPECT NOTICE                         │
│                                                                     │
│  Ifá is a living, sacred oral tradition of the Yoruba people of     │
│  West Africa, inscribed on the UNESCO Intangible Cultural           │
│  Heritage list.                                                     │
│                                                                     │
│  This software is a respectful educational tool for learning        │
│  about Ifá philosophy and culture.  It is NOT a substitute for      │
│  authentic divination by a qualified Babalawo (Ifá priest).         │
│                                                                     │
│  For important life decisions, please consult a trained,            │
│  initiated Babalawo or Iyanifa.                                     │
│                                                                     │
│  Ifá emphasises: cause and consequence, not fatalism.               │
│  Every challenge has a remedy (ebo).  Every path can be improved.   │
└─────────────────────────────────────────────────────────────────────┘
"""

IFA_INTRO = """
  About Ifá
  ─────────
  Ifá is the divination system and body of spiritual wisdom of the
  Yoruba people of West Africa.  It is also practised widely in the
  African diaspora — in Brazil (as Candomblé / Umbanda), Cuba (as
  Lucumí / Santería), Haiti, Trinidad, and beyond.

  The system was bestowed upon humanity by Orunmila, the Orisha of
  wisdom and divination, acting as witness to human destiny (ayanmo).

  ● 256 Odù Ifá  —  the sacred corpus of knowledge, each with
    hundreds of  ẹsẹ (poetic verses), stories, proverbs, and prescriptions.

  ● 16 Principal Odù (Meji)  —  the 16 "mother" Odu from which all
    256 are derived.  Each Meji is named by doubling one of the 16 root
    signs (e.g., Ogbe + Ogbe = Ejiogbe).

  ● Babalawo / Iyanifa  —  initiated Ifá priests/priestesses who
    undergo years of training to memorise the vast oral corpus.

  ● Ẹbọ (Ebo)  —  offerings and prescribed actions that can alter or
    improve one's destiny path.  Ifá is emphatically NOT fatalistic:
    every negative sign has a prescribed remedy.

  ● Divination tools used in this system:
      • Ọ̀pẹ̀lẹ̀ (Opele) — a chain of eight half-seed pods, cast in
        one throw.  Fast and widely used for general consultations.
      • Ikin — sixteen consecrated palm nuts manipulated to generate
        a figure.  More solemn; used for deeper matters.
"""


def print_banner() -> None:
    """Print the application banner."""
    print(_c(IFA_BANNER, "yellow", "bold"))


def print_disclaimer() -> None:
    """Print the cultural disclaimer."""
    print(_c(CULTURAL_DISCLAIMER, "cyan"))


def print_intro() -> None:
    """Print the Ifá introduction text."""
    print(_c(IFA_INTRO, "white"))
