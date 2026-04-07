# Kin Ifá 
# 堅伊法

**An educational Ifá divination system built with Python**

**以 Python 構建的伊法占卜系統**

---

## 中文簡介

伊法（Ifá）是西非約魯巴（Yoruba）民族的占卜系統與靈性智慧體系，已被列入
[聯合國教科文組織非物質文化遺產名錄](https://ich.unesco.org/en/RL/ifa-divination-system-00146)。
此系統由智慧與占卜之神 **奧倫米拉（Orunmila）** 傳授給人類，作為人類命運（*ayanmo*）的見證者。

### ⚠️ 文化尊重聲明

伊法是約魯巴民族**活的、神聖的口述傳統**。本軟體是一個**尊重文化的教育工具**，旨在：

- 學習伊法哲學、宇宙觀與文化實踐
- 文化欣賞與學術研究
- 探索 16 個主要神諕（Odù）及其智慧教導

本工具**不能**替代合格的 **巴巴拉沃（Babalawo，伊法祭司）** 或 **伊雅尼法（Iyanifa，女性伊法修行者）** 進行的真正占卜。重要的人生決定，請諮詢經過訓練與入門的修行者。

伊法強調的是**因果關係，而非宿命論**。每個挑戰都有對應的補救之道（ẹbọ / ebo），每條道路都可以改善。

### 功能特色

- 🌐 **中英雙語介面** — 可在中文與英文之間切換
- 🎴 **占卜功能** — 使用 Ọ̀pẹ̀lẹ̀（占卜鏈）或 Ikin（棕櫚果）進行占卜，支援中文顯示
- 📋 **瀏覽** — 以表格形式查看所有 16 個主要神諕
- 🔍 **查看** — 深入探索任何特定神諕的完整中文資料
- 📖 **關於伊法** — 中英雙語介紹
- 💻 **命令列模式** — 互動式 CLI 介面，適合終端用戶

### 快速開始

```bash
# Streamlit 網頁介面（推薦，支援中文）
pip install -r requirements.txt
streamlit run streamlit_app.py

# 命令列互動模式
python ifa.py
```

### 16 個主要神諕（Meji）

| # | Meji 名稱 | 中文名稱 | 主要神祇 |
|---|-----------|---------|---------|
| 1 | Ejiogbe | 光明之滿盈 | Obatala |
| 2 | Oyeku Meji | 重生前的黑暗 | Egungun / Oya |
| 3 | Iwori Meji | 內在的洞見 | Ori / Obatala |
| 4 | Odi Meji | 創造之母胎 | Yemoja / Osun |
| 5 | Irosun Meji | 生命之血的流動 | Osun / Sopona |
| 6 | Owonrin Meji | 變幻莫測之風 | Sango / Eshu |
| 7 | Obara Meji | 奧貢的王者風範 | Osun / Ogun |
| 8 | Okanran Meji | 衝突的火花 | Ogun / Sango |
| 9 | Ogunda Meji | 開路者 | Ogun |
| 10 | Osa Meji | 蛻變的風暴 | Oya |
| 11 | Ika Meji | 品德的盟約 | Obatala / Orunmila |
| 12 | Oturupon Meji | 深海之謎 | Yemoja / Olokun |
| 13 | Otura Meji | 和解之道 | Eshu / Orunmila |
| 14 | Irete Meji | 山的耐心 | Obatala / Orunmila |
| 15 | Ose Meji | 奧順的豐盛 | Osun |
| 16 | Ofun Meji | 圓滿循環的智慧 | Obatala / Orunmila |

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
├── ifa.py              ← CLI entry point (main programme)
├── streamlit_app.py    ← Streamlit web interface (中文/English bilingual)
├── odu_data.py         ← Data for all 16 principal Odu (Meji)
├── odu_data_zh.py      ← Chinese translations for all 16 Odu
├── divination.py       ← Opele & Ikin divination simulation classes
├── utils.py            ← ASCII display helpers, banners, disclaimers
├── requirements.txt    ← Python dependencies for Streamlit mode
└── README.md           ← This file
```

---

## Requirements

- **Python 3.10+**
- CLI mode: No third-party packages required (standard library only)
- Streamlit mode: `pip install -r requirements.txt`

---

## Usage

### Streamlit web interface (recommended for 中文 / Chinese)

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The Streamlit app provides:
- 🌐 **Bilingual interface** — toggle between 中文 and English
- 🎴 **Divination** — cast with Ọ̀pẹ̀lẹ̀ or Ikin, with Chinese display
- 📋 **Browse** — view all 16 principal Odu in a table
- 🔍 **View** — explore any specific Odu with full details in Chinese
- 📖 **About Ifá** — introduction in both languages

### Interactive CLI mode

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
- **Web interface**: `streamlit run streamlit_app.py` — bilingual Chinese/English Streamlit app (already included)
- **Telegram Bot**: Use `python-telegram-bot` with `IkinsOracle` as the backend
- **Multi-language**: Chinese translations are in `odu_data_zh.py` — add more languages following the same pattern

---

## Licence & Attribution

This project is provided for **educational and cultural appreciation purposes**.

The Ifá divination system belongs to the Yoruba people and their diaspora. Please
engage with this material respectfully and acknowledge its sacred origins.

If you use this code in academic or public work, please credit the Yoruba
cultural tradition from which Ifá originates.

---

*Àṣẹ — may the blessings of Orunmila guide your path.*
