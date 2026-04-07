# Ifá Oracle — Orunmila's Wisdom

**An educational Ifá divination system built with Python**

---

## ⚠️ Cultural Respect Notice

Ifá is a **living, sacred oral tradition** of the Yoruba people of West Africa,
inscribed on the [UNESCO Intangible Cultural Heritage list](https://ich.unesco.org/en/RL/ifa-divination-system-00146).

This software is a **respectful educational tool** intended for:
- Learning about Ifá philosophy, cosmology, and cultural practices
- Cultural appreciation and academic study
- Exploring the 16 principal Odù and their wisdom teachings

It is **NOT** a substitute for authentic divination by a qualified **Babalawo**
(Ifá priest) or **Iyanifa** (female Ifá practitioner). For important life
decisions, please consult a trained, initiated practitioner.

Ifá emphasises **cause and consequence, not fatalism**. Every challenge has a
prescribed remedy (ẹbọ / ebo). Every path can be improved.

---

## About Ifá

Ifá is the divination system and body of spiritual wisdom of the Yoruba people
of West Africa. It is practised widely in the African diaspora — in Brazil
(Candomblé / Umbanda), Cuba (Lucumí / Santería), Haiti, Trinidad, and beyond.

The system was bestowed upon humanity by **Orunmila**, the Orisha of wisdom
and divination, acting as witness to human destiny (*ayanmo*).

| Concept | Description |
|---------|-------------|
| **256 Odù Ifá** | The sacred corpus of knowledge; each Odù contains hundreds of *ẹsẹ* (poetic verses), stories, and prescriptions |
| **16 Principal Odù (Meji)** | The 16 "mother" Odu from which all 256 are derived |
| **Babalawo / Iyanifa** | Initiated Ifá priests who memorise the vast oral corpus |
| **Ẹbọ (Ebo)** | Offerings and prescribed actions that can improve one's destiny |
| **Ọ̀pẹ̀lẹ̀ (Opele)** | A chain of eight half-seed pods, cast in one throw |
| **Ikin** | Sixteen consecrated palm nuts manipulated to generate a figure |

---

## Project Structure

```
kinifa/
├── ifa.py          ← CLI entry point (main programme)
├── odu_data.py     ← Data for all 16 principal Odu (Meji)
├── divination.py   ← Opele & Ikin divination simulation classes
├── utils.py        ← ASCII display helpers, banners, disclaimers
└── README.md       ← This file
```

---

## Requirements

- **Python 3.10+**
- No third-party packages required (standard library only)

---

## Usage

### Interactive mode (recommended)

```bash
python ifa.py
```

This opens the full interactive menu where you can:
1. Cast with Ọ̀pẹ̀lẹ̀ (chain) — fast, general consultations
2. Cast with Ikin (palm nuts) — more deliberate consultations
3. Browse all 16 principal Odu
4. View any specific Odu by number
5. Read the Ifá introduction
6. Review the cultural disclaimer

### Command-line flags

```bash
# Quick Opele cast without a question
python ifa.py --method opele

# Cast with a specific question
python ifa.py --method ikin --question "Should I accept this new job offer?"

# Reproducible cast with a seed
python ifa.py --method opele --seed 42

# List all 16 principal Odu
python ifa.py --list

# View a specific Odu (e.g., Ejiogbe = #1)
python ifa.py --odu 1

# Print Ifá introduction
python ifa.py --intro

# Disable colour output (for piping / logging)
python ifa.py --no-colour --method opele

# Omit ebo suggestions
python ifa.py --no-ebo --method opele
```

### Full options

```
usage: ifa [--method {opele,ikin}] [--question QUESTION] [--seed SEED]
           [--list] [--odu NUMBER] [--intro] [--no-colour] [--no-ebo]

Options:
  --method {opele,ikin}   Divination method
  --question, -q TEXT     Your question for the oracle
  --seed, -s INT          RNG seed for reproducible results
  --list, -l              List all 16 principal Odu and exit
  --odu, -o NUMBER        Show a specific Odu by number (1–16)
  --intro                 Print the Ifá introduction text and exit
  --no-colour             Disable ANSI colour codes
  --no-ebo                Omit ebo suggestions from output
```

---

## The 16 Principal Odu (Meji)

| # | Meji Name | English Name | Ruling Orisha |
|---|-----------|--------------|---------------|
| 1 | Ejiogbe | The Fullness of Light | Obatala |
| 2 | Oyeku Meji | The Darkness Before Renewal | Egungun / Oya |
| 3 | Iwori Meji | The Inner Vision | Ori / Obatala |
| 4 | Odi Meji | The Womb of Creation | Yemoja / Osun |
| 5 | Irosun Meji | The Flow of Life Blood | Osun / Sopona |
| 6 | Owonrin Meji | The Unpredictable Wind | Sango / Eshu |
| 7 | Obara Meji | The Royalty of Ogun | Osun / Ogun |
| 8 | Okanran Meji | The Spark of Conflict | Ogun / Sango |
| 9 | Ogunda Meji | The Path-Opener | Ogun |
| 10 | Osa Meji | The Storm of Transformation | Oya |
| 11 | Ika Meji | The Covenant of Character | Obatala / Orunmila |
| 12 | Oturupon Meji | The Mystery of the Deep | Yemoja / Olokun |
| 13 | Otura Meji | The Reconciliation | Eshu / Orunmila |
| 14 | Irete Meji | The Patience of the Mountain | Obatala / Orunmila |
| 15 | Ose Meji | The Abundance of Osun | Osun |
| 16 | Ofun Meji | The Wisdom of the Completed Cycle | Obatala / Orunmila |

---

## Odu Figure Symbols

Each Odu is represented by four pairs of marks (from the Ọ̀pẹ̀lẹ̀ casting):

```
  |   = Single mark (I)  — odd count  — 1
 | |  = Double mark (II) — even count — 0
```

Example — Ejiogbe (all single marks):

```
  |      |
  |      |
  |      |
  |      |
```

Example — Oyeku Meji (all double marks):

```
 | |    | |
 | |    | |
 | |    | |
 | |    | |
```

---

## Extending the System

The codebase is designed for future expansion:

- **256 full Odu**: Add remaining Odu data to `odu_data.py` using the same `Odu` dataclass
- **ẹsẹ verse database**: Extend the `Odu` dataclass with a `verses: List[str]` field
- **AI-assisted interpretation**: Wrap `DivinationResult.interpret()` with an LLM call
- **Web interface**: Import `divination.py` and `utils.py` into a Streamlit or Gradio app
- **Telegram Bot**: Use `python-telegram-bot` with `IkinsOracle` as the backend
- **Multi-language**: Add `meaning_zh_tw` (Traditional Chinese) fields to `Odu`

---

## Licence & Attribution

This project is provided for **educational and cultural appreciation purposes**.

The Ifá divination system belongs to the Yoruba people and their diaspora. Please
engage with this material respectfully and acknowledge its sacred origins.

If you use this code in academic or public work, please credit the Yoruba
cultural tradition from which Ifá originates.

---

*Àṣẹ — may the blessings of Orunmila guide your path.*
