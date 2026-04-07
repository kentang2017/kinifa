#!/usr/bin/env python3
"""
ifa.py — Ifá Oracle: Command-Line Interface

Usage
-----
  python ifa.py                          # Interactive menu
  python ifa.py --method opele           # Quick Opele cast, no question
  python ifa.py --method ikin            # Quick Ikin cast, no question
  python ifa.py --question "..."         # Cast with a specific question
  python ifa.py --seed 42                # Reproducible cast
  python ifa.py --list                   # List all 16 principal Odu
  python ifa.py --odu 1                  # Show a specific Odu by number
  python ifa.py --intro                  # Print Ifá introduction text
  python ifa.py --no-colour              # Disable ANSI colour codes

Cultural note: This is an educational tool.  For authentic divination
consult a qualified Babalawo.

Requires Python 3.10+
"""

from __future__ import annotations

import argparse
import sys
from typing import Optional

import utils
from divination import IkinsOracle
from odu_data import ODU_LIST, ODU_BY_NUMBER


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _print_all_odu() -> None:
    """Print a compact summary table of all 16 principal Odu."""
    print(utils._c("\n  The 16 Principal Odu (Meji)\n", "cyan", "bold"))
    print(utils._c(
        f"  {'#':>2}  {'Meji Name':<20}  {'English Name':<35}  Orisha",
        "bold"
    ))
    print(utils._c("  " + "─" * 68, "dim"))
    for odu in ODU_LIST:
        num   = utils._c(f"  {odu.number:>2}", "yellow")
        name  = utils._c(f"  {odu.meji_name:<20}", "cyan")
        eng   = f"  {odu.english_name:<35}"
        oris  = utils._c(f"  {odu.orisha}", "magenta")
        print(f"{num}{name}{eng}{oris}")
    print()


def _run_divination(
    oracle: IkinsOracle,
    method: str,
    question: Optional[str],
    no_ebo: bool,
) -> None:
    """Execute a divination and print the formatted result."""
    result = oracle.divine(method=method, question=question)
    print(utils.render_result(result, show_ebo=not no_ebo))


# ---------------------------------------------------------------------------
# Interactive menu
# ---------------------------------------------------------------------------

def _interactive(oracle: IkinsOracle) -> None:
    """Run the interactive CLI session."""
    utils.print_banner()
    utils.print_disclaimer()

    while True:
        print(utils._c("\n  ╔══ MAIN MENU ══════════════════════════════╗", "cyan"))
        print(utils._c("  ║                                           ║", "cyan"))
        print(utils._c("  ║  1. Cast with Ọ̀pẹ̀lẹ̀ (chain)             ║", "cyan"))
        print(utils._c("  ║  2. Cast with Ikin (palm nuts)            ║", "cyan"))
        print(utils._c("  ║  3. List all 16 principal Odu             ║", "cyan"))
        print(utils._c("  ║  4. View a specific Odu                   ║", "cyan"))
        print(utils._c("  ║  5. About Ifá (introduction)              ║", "cyan"))
        print(utils._c("  ║  6. Cultural disclaimer                   ║", "cyan"))
        print(utils._c("  ║  Q. Quit                                  ║", "cyan"))
        print(utils._c("  ╚═══════════════════════════════════════════╝", "cyan"))

        choice = input(utils._c("\n  Your choice: ", "yellow")).strip().upper()

        if choice in ("1", "2"):
            method = "opele" if choice == "1" else "ikin"
            print(utils._c(
                "\n  Enter your question, or press Enter for general guidance:",
                "white"
            ))
            question = input(utils._c("  > ", "yellow")).strip() or None
            _run_divination(oracle, method, question, no_ebo=False)

        elif choice == "3":
            _print_all_odu()

        elif choice == "4":
            _print_all_odu()
            try:
                num_str = input(utils._c(
                    "  Enter Odu number (1–16): ", "yellow"
                )).strip()
                num = int(num_str)
                if num not in ODU_BY_NUMBER:
                    raise ValueError
                print(utils.render_odu_card(ODU_BY_NUMBER[num]))
            except ValueError:
                print(utils._c("  Invalid number.  Please enter 1–16.", "red"))

        elif choice == "5":
            utils.print_intro()

        elif choice == "6":
            utils.print_disclaimer()

        elif choice == "Q":
            print(utils._c(
                "\n  Ashe — may the blessings of Orunmila guide your path.\n",
                "yellow", "bold"
            ))
            break
        else:
            print(utils._c("  Unknown option.  Please choose 1–6 or Q.", "red"))


# ---------------------------------------------------------------------------
# Command-line argument parser
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="ifa",
        description="Ifá Oracle — Orunmila's Wisdom  (educational tool)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Cultural note: Ifá is a sacred tradition of the Yoruba people.\n"
            "This tool is for education and cultural appreciation only.\n"
            "For authentic divination, consult a qualified Babalawo."
        ),
    )
    p.add_argument(
        "--method", choices=["opele", "ikin"], default=None,
        help="Divination method: 'opele' (chain) or 'ikin' (palm nuts).",
    )
    p.add_argument(
        "--question", "-q", default=None, metavar="QUESTION",
        help="Your question for the oracle.",
    )
    p.add_argument(
        "--seed", "-s", type=int, default=None,
        help="RNG seed for reproducible results.",
    )
    p.add_argument(
        "--list", "-l", action="store_true",
        help="List all 16 principal Odu and exit.",
    )
    p.add_argument(
        "--odu", "-o", type=int, default=None, metavar="NUMBER",
        help="Show a specific Odu by number (1–16) and exit.",
    )
    p.add_argument(
        "--intro", action="store_true",
        help="Print the Ifá introduction text and exit.",
    )
    p.add_argument(
        "--no-colour", "--no-color", action="store_true",
        help="Disable ANSI colour codes.",
    )
    p.add_argument(
        "--no-ebo", action="store_true",
        help="Omit ebo (offering) suggestions from output.",
    )
    return p


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.no_colour:
        utils.disable_colour()

    oracle = IkinsOracle(seed=args.seed)

    # Non-interactive flags
    if args.list:
        utils.print_banner()
        _print_all_odu()
        return

    if args.odu is not None:
        if args.odu not in ODU_BY_NUMBER:
            print(utils._c(
                f"  Odu number must be between 1 and 16.  Got: {args.odu}", "red"
            ))
            sys.exit(1)
        utils.print_banner()
        print(utils.render_odu_card(ODU_BY_NUMBER[args.odu], show_ebo=not args.no_ebo))
        return

    if args.intro:
        utils.print_banner()
        utils.print_intro()
        return

    # Direct cast (non-interactive) if --method was given
    if args.method:
        utils.print_banner()
        utils.print_disclaimer()
        _run_divination(oracle, args.method, args.question, no_ebo=args.no_ebo)
        return

    # Default: interactive mode
    _interactive(oracle)


if __name__ == "__main__":
    main()
