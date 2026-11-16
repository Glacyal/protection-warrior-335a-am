> 🇮🇹 **Versione Italiana**: [HANDOFF_IT.md](HANDOFF_IT.md)
>
> 🌐 **Live Web Simulator**: [https://glacyal.github.io/protection-warrior-335a-am/](https://glacyal.github.io/protection-warrior-335a-am/)

# Class Warrior (Protection) — Technical Handoff

Technical reference manual for the development, maintenance, and architectural extension of the **Class Warrior (Protection)** suite for World of Warcraft 3.3.5a (*WotLK Build 12340*).

---

## 1. Project Overview

The suite is distributed as a **standalone WeakAura** in compressed `!WA:1!` format (`AceSerializer-3.0` binary serialization + Deflate RFC 1951 level 9 compression + `LibDeflate` character print encoding).  
It strictly complies with the synchronized 278px visual geometry established with **Class Warrior (Fury)** and **Class Mage (TTW Fire)**, guaranteeing Zero Native Warnings on WeakAuras 5.21.8+ (`internalVersion = 90`).

| Property | Detail |
| :--- | :--- |
| **Target Platform** | World of Warcraft 3.3.5a (WotLK Build 12340) |
| **Target WeakAuras Engine** | **WeakAuras 5.21.8+** (`internalVersion = 90`, `w = "5.21.8"`). |
| **Distribution File** | [`IMPORT_STRING_v5.21.8.txt`](IMPORT_STRING_v5.21.8.txt) (official import string ready for production) |
| **Web Simulator** | [`docs/index.html`](docs/index.html) |
| **Online Live Demo** | [GitHub Pages Live Showcase](https://glacyal.github.io/protection-warrior-335a-am/) |
| **Version Control** | Git on GitHub: [Glacyal/protection-warrior-335a-am](https://github.com/Glacyal/protection-warrior-335a-am) |

---

## 2. Repository Layout

```text
protection-warrior-335a-am/
├── IMPORT_STRING_v5.21.8.txt        # Native WeakAuras 5.21.8+ string (Zero warnings, internalVersion: 90)
├── generate.py                      # Python compiler for the WeakAuras tree
├── README.md                        # Primary user documentation (English)
├── README_IT.md                     # Secondary user documentation (Italian)
├── HANDOFF.md                       # Primary technical developer manual (English)
├── HANDOFF_IT.md                    # Secondary technical developer manual (Italian)
├── .gitignore                       # Virtualenv, cache, and policy ignore rules
│
├── builder/                         # Modular Python package for HUD generation
│   ├── tree.py                      # Master hierarchical tree assembler (20 controlled nodes)
│   ├── core/                        # Core serialization and encoding modules
│   │   ├── constants.py             # Load conditions (Warrior), textures, Expressway font, defensive caps
│   │   ├── serializer.py            # Pure Python AceSerializer-3.0 serializer (^1...^^)
│   │   ├── deflate.py               # Deflate RFC 1951 compression + LibDeflate Print Encoding
│   │   ├── encoder.py               # Final string generator (!WA:1!...)
│   │   └── helpers.py               # Dual-key subtext generators and UI helpers
│   └── components/                  # Component modules (identical architecture to Fury)
│       ├── procs.py                 # 01 - Procs warTank (Horizontal 7-icon dynamic group 34x34 at y = 52)
│       ├── buffs.py                 # 02 - Battle Shout, 03 - Commanding Shout, 04 - Defensive Stance (x = -222, -190, -158, y = 0)
│       ├── utility.py               # 05-13 - Utility Row (Trinkets, Ring, Cloak, Tier, Enchants, Gloves, Shield Wall, Last Stand, Boots) at y = -45
│       ├── bars.py                  # 14 - Rage Bar (278x14px at y = -20) & 16 - Castbar warTank (278x20px at y = +8 with Kick Advisor)
│       ├── rotational.py            # 15 - Rotational Bar (Static Queue Indicator 278x7px at y = -7 with HS/Cleave Pixel Glow)
│       ├── alerts.py                # 17 - Alerts warTank (Central text alerts at y = 78)
│       ├── stats.py                 # 18 - Stats Panel warTank (Compact panel 88x60px at x = -190, y = -45)
│       └── sunder.py                # 19 - Sunder Armor Tracker warTank (32x32px at x = 160, y = -7)
│
├── docs/                            # Documentation and interactive preview for GitHub Pages
│   └── index.html                   # Interactive HTML/CSS/JS simulator (purely in English, 1:1 Fury layout)
│
├── scripts/
│   └── sync_docs.py                 # Automatic sync script for v5 string into docs/index.html
│
└── tests/                           # Automated parallel test suite
    ├── run_parallel_tests.py        # Multi-core test runner (ProcessPoolExecutor)
    ├── test_components_integrity.py # Structural module integrity verification (20 sequential nodes & UIDs)
    ├── test_lua.py                  # Lua syntax validation (triggers, untriggers, custom scripts)
    ├── test_tree_layout.py          # Geometric 1:1 layout verification with Fury Warrior
    ├── test_string_sync.py          # String consistency check between builder and IMPORT_STRING_v5.21.8.txt
    ├── test_stats_panel.py          # Tank formulas verification (Contextual Armor DR, EHP, CTC, 540 Defense)
    ├── test_defensives.py           # Defensive mitigation cooldown verification (Shield Wall, Last Stand, Shield Block)
    ├── test_interrupts.py           # Contextual Kick Advisor check (Shield Bash, Pummel, notInterruptible)
    └── test_danger_alerts.py        # Critical HP alerts and lethal boss mechanics verification
```

---

## 3. Development Workflow

1. **Component Modification**:
   - Edit modules in `builder/components/` or core formulas in `builder/core/`.
2. **Execute Parallel Test Suite**:
   - Run the multi-core parallel test runner:
     ```bash
     python tests/run_parallel_tests.py
     ```
   - All 8 tests must report `[✓] PASS` in under 0.4 seconds.
3. **Compile Import String**:
   - Recompile the native WA 5.21.8+ string:
     ```bash
     python generate.py
     ```
4. **Synchronize Web Simulator**:
   - Inject the compiled string into the web simulator:
     ```bash
     python scripts/sync_docs.py
     ```
5. **Commit & Push (`CP`)**:
   - Stage and commit code, test, and documentation files simultaneously.

---

## 4. Key Architectural Specifications

### 4.1 Exclusive Load Condition: [Devastate]
- Linear WeakAuras Index: **`103`** (calculated as $(3 - 1) \times 40 + 23$, corresponding to Tab 3 Protection, Tier 8 Column 1, Spell ID `20243`).
- Configuration in `builder/core/constants.py`:
  ```python
  PROT_WARRIOR_LOAD = {
      "use_class": True,
      "class": {"single": "WARRIOR", "multi": {"WARRIOR": True}},
      "use_talent": True,
      "talent": {"single": 103, "multi": {103: True}},
      "use_vehicle": False,
  }
  ```
- Uniformly inherited by the root group and all 43 child auras.

### 4.2 Out-of-Stance Alert in Combat (Fury Warrior Model)
- In correct Defensive Stance (`GetShapeshiftForm() == 2`), the stance icon is **completely hidden** (zero visual clutter on screen, identical to Fury Warrior).
- Dual-layer alert triggers whenever `UnitAffectingCombat("player") and GetShapeshiftForm() ~= 2`:
  1. Local indicator `04 - Defensive Stance - OutOfStance` (X: -158, Y: 0, 28x28px) with red alert color and `STANCE` subtext.
  2. Master banner `Alert - Wrong Stance` (X: 0, Y: +64) at 20pt `>> DEFENSIVE STANCE REQUIRED! <<` accompanied by `RaidWarning.ogg`.

### 4.3 Fury Warrior-Style Tanking Stats Engine & Non-Stacking Debuffs
- Clean 5-row presentation with white labels `|cFFFFFFFFLabel:|r <Value>`:
  1. `Def:` (540 Cap for Lv.83 raid bosses, 535 for Lv.82 heroic dungeon bosses).
  2. `Armor:` with contextual Physical DR% ($K=15232.5$ at Lv.80 default showing 62.4% identical to in-game character sheet; $K=16635$ on Lv.83 raid bosses showing 60.3% actual raid mitigation, hard cap 75.0%).
  3. `CTC:` Combat Table Coverage with non-stacking engine for *Insect Swarm* and *Scorpid Sting* (+3.0% max Miss).
  4. `Block:` with block chance % and Shield Block Value (SBV).
  5. `Hit:` with Draenei *Heroic Presence* (+1.0%) and `Exp:` with Soft Cap 26 and Hard Cap 56.

### 4.4 Static Rotational Queue Indicator (Heroic Strike & Cleave)
- Occupies the allocated 278x7px space at $y = -7$ as a static, solid bar without swipe animation and without remaining time countdown numbers.
- Dynamic queueing logic inherited from Fury Warrior via `IsCurrentSpell()`:
  - Gold pixel glow (`LibCustomGlow-1.0`) and ADD vertex tint when *Heroic Strike* (`47450`) is queued.
  - Emerald Green pixel glow and ADD vertex tint when *Cleave* (`47520`) is queued.
  - Returns to neutral warrior copper/bronze static appearance when no ability is queued.

---

## 5. Technical Glossary & Tanking Acronyms (WotLK 3.3.5a)

| Acronym | Full Name | Mechanics & Formulas |
| :--- | :--- | :--- |
| **`DEF`** | **Defense Skill** | Defense skill rating (`base + rating`). Cap **540** for raid boss Lv.83 crit immunity (-5.6% incoming crit chance), **535** in Lv.82 heroics. |
| **`ARM`** | **Effective Armor & Physical DR%** | Instantaneous effective armor. Evaluates contextual physical mitigation: Blizzard constant $K = 15232.5$ at Lv.80 default (25,253 armor $\implies \mathbf{62.4\%}$, matching in-game paperdoll) and $K = 16635$ against Lv.83 Raid Bosses ($\implies \mathbf{60.3\%}$, actual raid mitigation). Hard cap at 75.0%. |
| **`CTC`** | **Combat Table Coverage** | Total attack table coverage: $\text{Dodge} + \text{Parry} + \text{Block} + \text{BossMiss}$. At $\ge \mathbf{102.4\%}$, the tank is **Unhittable** (zero unmitigated hits). Includes non-stacking debuffs (*Insect Swarm* / *Scorpid Sting* max +3%). |
| **`Block`** | **Block Chance** | Shield block probability. Reaches 100% during active *Shield Block* (10s). |
| **`SBV`** | **Shield Block Value** | Fixed amount of damage absorbed per block. Primary scaling multiplier for *Shield Slam* damage and threat. |
| **`Hit`** | **Melee Hit Chance** | Hit accuracy for melee special attacks and Taunt. Cap is **8.0%** (263 rating), reduced to 7.0% with Draenei *Heroic Presence*. |
| **`Exp`** | **Expertise** | Reduces enemy chance to dodge and parry. **Soft Cap 26** (214 rating, eliminates frontal dodges), **Hard Cap 56** (eliminates frontal parries and negates *Parry-Haste*). |
| **`Avoid`** | **Pure Avoidance** | Sum of $\text{Dodge} + \text{Parry} + \text{Miss}$ (percentage of attacks dealing **zero damage**). |
| **`DR%`** | **Damage Reduction %** | Passive physical damage reduction percentage provided by effective armor. |
| **`EHP`** | **Effective Health Pool** | Raw physical damage pool: $\text{Max HP} / (1 - \text{DR}\%)$. |
| **`GCD`** | **Global Cooldown** | Standard 1.5-second ability recovery window. |
