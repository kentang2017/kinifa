"""
divination.py — Ifá Oracle: Core Divination Logic

Two traditional Ifá divination methods are simulated here:

  1. Ọ̀pẹ̀lẹ̀ (Opele) — a chain of eight half-seed pods, four on each side,
     cast in a single throw to produce one Odu instantly.

  2. Ikin — sacred palm nuts manipulated repeatedly until a complete figure
     of four mark-pairs is built up, one pair at a time.

Both methods produce one of the 16 principal Odu (Meji) for this simplified
educational system.  A full Ifá system can produce any of the 256 Odu.

Cultural note: Real Ifá divination is performed by a qualified Babalawo using
consecrated tools and accompanied by prayer, ritual, and deep knowledge of
the oral corpus (odù Ifá).  This simulation is for cultural education only.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from odu_data import Odu, ODU_LIST, ODU_BY_NUMBER


# ---------------------------------------------------------------------------
# Divination result container
# ---------------------------------------------------------------------------

@dataclass
class DivinationResult:
    """Holds the outcome of a single divination session."""

    method: str                        # "opele" or "ikin"
    odu: Odu
    question: Optional[str]            # User's question, if any
    timestamp: datetime = field(default_factory=datetime.now)
    seed: Optional[int] = None         # RNG seed used, for reproducibility
    cast_sequence: list[int] = field(default_factory=list)  # raw marks produced

    # Contextual interpretation hint (added by interpret())
    context_note: str = ""

    def interpret(self) -> str:
        """Return a contextually relevant interpretation note.

        If the user provided a question the note tries to orient the Odu
        meaning toward their stated concern.
        """
        if not self.question:
            return self.odu.advice

        q = self.question.lower()

        # Simple keyword-based contextual routing
        keywords = {
            "career": ["work", "job", "career", "business", "profession",
                       "money", "finance", "wealth", "success", "employment"],
            "love": ["love", "relationship", "marriage", "partner", "romance",
                     "heart", "spouse", "wedding", "family"],
            "health": ["health", "sick", "illness", "heal", "disease",
                       "medicine", "body", "pain", "doctor", "hospital"],
            "travel": ["travel", "journey", "move", "relocate", "abroad",
                       "trip", "migration"],
            "decision": ["decision", "choose", "choice", "should i", "which",
                         "option", "path"],
            "spiritual": ["spiritual", "orisha", "prayer", "ritual", "god",
                          "faith", "spirit", "divine"],
        }

        matched = None
        for category, words in keywords.items():
            if any(w in q for w in words):
                matched = category
                break

        theme_notes = {
            "career": (
                "Regarding your career/business question: "
                f"{self.odu.primary_meaning} "
                "Focus on the themes of "
                f"{', '.join(self.odu.themes[:3])}."
            ),
            "love": (
                "Regarding your relationship question: "
                f"{self.odu.primary_meaning} "
                "Consider how the themes of "
                f"{', '.join(self.odu.themes[:3])} "
                "are manifesting in your love life."
            ),
            "health": (
                "Regarding your health question: "
                f"{self.odu.primary_meaning} "
                "Pay attention to the positive aspects: "
                f"{self.odu.positive_aspects[0]}."
            ),
            "travel": (
                "Regarding your journey: "
                f"{self.odu.primary_meaning} "
                "Honour Ogun and Eshu before departing."
            ),
            "decision": (
                "Regarding your decision: "
                f"{self.odu.primary_meaning} "
                "Reflect on the moral teaching: "
                f'"{self.odu.moral_teaching}"'
            ),
            "spiritual": (
                "Regarding your spiritual path: "
                f"{self.odu.primary_meaning} "
                f"Connect with {self.odu.orisha} for guidance."
            ),
        }

        if matched and matched in theme_notes:
            self.context_note = theme_notes[matched]
        else:
            self.context_note = (
                f"Regarding your question — {self.odu.primary_meaning} "
                f"{self.odu.advice}"
            )

        return self.context_note


# ---------------------------------------------------------------------------
# Divination engine
# ---------------------------------------------------------------------------

class IkinsOracle:
    """
    Simulates Ifá divination using either Ọ̀pẹ̀lẹ̀ or Ikin method.

    Parameters
    ----------
    seed : int, optional
        RNG seed for reproducible results.
    """

    def __init__(self, seed: Optional[int] = None) -> None:
        self._seed = seed
        self._rng = random.Random(seed)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _random_mark(self) -> bool:
        """Return True (single |) or False (double ||) with equal probability.

        In a real Opele casting the chain falls with each side showing
        concave (open) or convex (closed), which Babalawo reads as single
        or double.  Here we simulate with a fair coin.
        """
        return self._rng.choice([True, False])

    def _marks_to_odu_number(self, marks: list[bool]) -> int:
        """Map 4 mark values to one of the 16 Meji Odu numbers (1–16).

        We use the traditional mapping where each combination of four
        binary marks corresponds to an Odu in the canonical ordering.
        """
        # Convert booleans to index 0-15 using big-endian binary
        idx = 0
        for m in marks:
            idx = (idx << 1) | (1 if m else 0)
        # idx is in range 0–15; map to 1–16
        return (idx % 16) + 1

    # ------------------------------------------------------------------
    # Public divination methods
    # ------------------------------------------------------------------

    def cast_opele(
        self,
        question: Optional[str] = None,
        seed: Optional[int] = None,
    ) -> DivinationResult:
        """Simulate an Ọ̀pẹ̀lẹ̀ (chain) casting.

        The Opele has eight half-pods (four on each side).  In a Meji
        reading both columns are identical, so we cast four marks for the
        left column and mirror them on the right.

        Parameters
        ----------
        question : str, optional
            The querent's question.
        seed : int, optional
            Override the instance seed for this cast.

        Returns
        -------
        DivinationResult
        """
        if seed is not None:
            self._rng.seed(seed)

        marks = [self._random_mark() for _ in range(4)]
        odu_number = self._marks_to_odu_number(marks)
        odu = ODU_BY_NUMBER[odu_number]

        result = DivinationResult(
            method="opele",
            odu=odu,
            question=question,
            seed=seed or self._seed,
            cast_sequence=marks,
        )
        result.interpret()
        return result

    def cast_ikin(
        self,
        question: Optional[str] = None,
        seed: Optional[int] = None,
        verbose: bool = False,
    ) -> DivinationResult:
        """Simulate Ikin (palm-nut) divination.

        The Babalawo passes sixteen Ikin between both hands multiple times.
        The number of nuts remaining in the right hand after the pass
        determines whether a single (I) or double (II) mark is made.
        The operation is repeated eight times to produce the full Odu figure
        (two columns of four marks each, with both columns identical for Meji).

        Parameters
        ----------
        question : str, optional
            The querent's question.
        seed : int, optional
            Override the instance seed for this cast.
        verbose : bool
            If True, return a list of intermediate steps in
            ``result.cast_sequence``.

        Returns
        -------
        DivinationResult
        """
        if seed is not None:
            self._rng.seed(seed)

        marks: list[bool] = []
        raw_sequence: list[int] = []

        for _ in range(4):
            # Simulate palm-nut pass: pick a random remainder (1 or 2)
            # 1 remaining → single mark (True)
            # 2 remaining → double mark (False)
            remainder = self._rng.choice([1, 2])
            raw_sequence.append(remainder)
            marks.append(remainder == 1)

        odu_number = self._marks_to_odu_number(marks)
        odu = ODU_BY_NUMBER[odu_number]

        result = DivinationResult(
            method="ikin",
            odu=odu,
            question=question,
            seed=seed or self._seed,
            cast_sequence=raw_sequence if verbose else marks,
        )
        result.interpret()
        return result

    def divine(
        self,
        method: str = "opele",
        question: Optional[str] = None,
        seed: Optional[int] = None,
    ) -> DivinationResult:
        """Convenience wrapper that dispatches to the appropriate method.

        Parameters
        ----------
        method : {"opele", "ikin"}
        question : str, optional
        seed : int, optional

        Returns
        -------
        DivinationResult
        """
        method = method.lower().strip()
        if method == "opele":
            return self.cast_opele(question=question, seed=seed)
        elif method == "ikin":
            return self.cast_ikin(question=question, seed=seed)
        else:
            raise ValueError(
                f"Unknown divination method '{method}'. Choose 'opele' or 'ikin'."
            )

    # ------------------------------------------------------------------
    # Utility: list all Odu
    # ------------------------------------------------------------------

    @staticmethod
    def all_odu() -> list[Odu]:
        """Return all 16 principal Odu in traditional order."""
        return ODU_LIST
