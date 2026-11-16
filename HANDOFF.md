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
│       ├── procs.py                 # 01 - Procs warTank (Horizontal 5-icon dynamic group 34x34 at y = 52)
│       ├── buffs.py                 # 02 - Battle Shout warTank, 03 - Commanding Shout warTank, 04 - Defensive Stance warTank (x = -271, -216, -161, y = 0, 34x34px)
│       ├── utility.py               # 05-13 - Utility Row (Trinkets, Ring, Cloak, Tier, Enchants, Gloves, Shield Wall warTank, Last Stand warTank, Boots) at y = -45
│       ├── bars.py                  # 14 - Rage Bar warTank (278x14px at y = -20) & 16 - Castbar warTank (278x20px at y = +8 with Kick Advisor)
│       ├── rotational.py            # 15 - Rotational Bar warTank (Static Queue Indicator 278x7px at y = -7 with HS/Cleave Pixel Glow)
│       ├── alerts.py                # 17 - Alerts warTank (Central text alerts at y = 78)
│       ├── stats.py                 # 18 - Stats Panel warTank (144x68px panel at x = -216, y = -53, perfectly adapted to 5-row text)
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

### 4.7 Left Column Harmonization (Stats Panel & Shouts Alignment)
- **Stats Panel Dimensions (144x68px at X: -216, Y: -53)**: Perfectly sized to enclose all 5 lines of defensive text (`Def: 541 (CAP)`, `Armor: 25.3k (62.4%)`, `CTC: 75.2%`, `Block: 21.7% (1800 SBV)`, `Hit: 9.1% | 25 Exp`) with 10px lateral and 6px vertical padding, eliminating label overflow.
- **Top Shouts & Stance Grid (34x34px at X: -271, -216, -161, Y: 0)**: Icon size standardized to 34x34px (matching procs row); left edge (-288) aligns with the left edge of the stats panel, center (-216) aligns with Commanding Shout, and right edge (-144) aligns with Defensive Stance.
- **Clean Vertical Separation**: 3px gap between icon labels (`OFF`, `STANCE` at Y: -17) and panel top edge (Y: -19.6), completely eliminating visual collisions.

### 4.10 Vigilance Missing Alert (04b - Vigilance warTank — Focus Magic Architecture)
- **Talent-Grounded Tracking**: Subscribed to spellbook/talent inspection for *Vigilance* (Spell ID 50720 / 59665). If not talented, the aura is completely dormant.
- **Event-Driven Ally Lifecycle**:
  - `UNIT_SPELLCAST_SUCCEEDED`: Detects player casting Vigilance on a friendly target (`expires = now + 1800`).
  - `COMBAT_LOG_EVENT_UNFILTERED`: Tracks `SPELL_AURA_APPLIED`, `SPELL_AURA_REFRESH`, `SPELL_AURA_REMOVED`, `SPELL_AURA_BROKEN`, and instantly resets if the protected ally dies (`UNIT_DIED`).
  - Automatic fallback scanning across `target`, `focus`, `party1..4`, and `raid1..40`.
- **Anti-Clutter Visual Model (Focus Magic Style)**:
  - `Vigilance - OFF warTank`: Prominent desaturated icon with red `OFF` at `INNER_BOTTOM`, displayed only when the warrior is talented into Vigilance and no group/raid ally carries the buff.
  - `Vigilance - Active warTank`: Only triggers if expiration is imminent (`rem <= 60s`).
- **Harmonized 4-Icon Row Geometry**: Standardized to 30x30px with 2px gap (step = 32px), spanning exactly 126px from $x = -279$ to $x = -153$:
  - `02 - Battle Shout warTank`: `X: -264, Y: 0`
  - `03 - Commanding Shout warTank`: `X: -232, Y: 0`
  - `04b - Vigilance warTank`: `X: -200, Y: 0`
  - `04 - Defensive Stance warTank`: `X: -168, Y: 0`

### 4.9 Compact Stats Panel Optimization (126x60px) & Tight 3px Icon Spacing
- **Snug 126x60px Stats Panel**: Resized from 144x68px to 126x60px at `X: -216, Y: -49`, eliminating redundant negative space on the right and bottom while preserving an exact 6px horizontal text margin on both sides without clipping.
- **Tight 3px Adjacent Shouts & Stance Grid**: Replaced the wide 21px gap with a crisp 3px margin between 34x34px icons (step = 37px):
  - `02 - Battle Shout warTank`: `X: -253, Y: 0`
  - `03 - Commanding Shout warTank`: `X: -216, Y: 0`
  - `04 - Defensive Stance warTank`: `X: -179, Y: 0`
- The 108px icon cluster is centered above the 126px Stats Panel with a clean 9px symmetrical margin on left and right and 2px vertical spacing.

### 4.8 Cloak Proc-Only Filtering (Slot 15) & Parachute/Static Suppression
- **Strict Cloak Proc-Only Visibility**: `07 - Cloak warTank` is exclusively displayed when an enchantment with actual combat procs is present on the Cloak (Slot 15), specifically Tailoring *Swordguard Embroidery* (*Ricamo della Spada*, +400 AP for 15s, 45s ICD, Spell ID 55775, Enchant ID 3730).
- **Parachute & Static Enchant Suppression**: The Engineering parachute tinker (*Flexweave Underlay*, Enchant ID 3605, Spell ID 55002) as well as static enchants (+22 Agility, +16 Defense, +225 Armor, resistances) or unenchanted cloaks strictly evaluate `_G.PWHUD_CheckSlotEquipped(15) == false`.
- **Dynamic Centering & Visual Polish**: When suppressed, `07 - Cloak warTank` is omitted from `activeOrder` in `_G.PWHUD_UpdateUtilityRowPositions()`, automatically re-centering remaining icons. Set `cooldownEdge: False` to avoid yellow tick artifacts.

### 4.7 Tier Set Proc-Only Filtering & Revenge Edge Polish
- **Strict Tier Set Proc-Only Visibility**: `08 - Tier Set warTank` is exclusively displayed when the equipped Tier set bonus possesses a genuine triggerable proc / active combat buff:
  - **T10 4P (*Blood Frenzy* / *Frenesia del Sangue*, Spell ID 70844)**: 20% max HP damage absorption for 10s triggered on Bloodrage.
  - **T8 4P (Magic Damage Reduction 20%, Spell ID 64938 / 2565)**: 20% magical DR for 10s triggered during Shield Block.
- **Suppression of Static Tier Bonuses**: Passive or static bonuses (T10 2P, T9 2P/4P, T8 2P, T7 2P/4P) or non-tier items strictly return `cache.isEquipped = false`.
- **Dynamic Utility Centering**: When suppressed, `08 - Tier Set warTank` is omitted from `activeOrder` in `_G.PWHUD_UpdateUtilityRowPositions()`, automatically re-centering the remaining utility icons without an empty gap.
- **Revenge Border Edge Polish**: Set `cooldownEdge: False` on `Revenge Ready warTank`, eliminating the yellow vertical line tick artifact at 12 o'clock while retaining the smooth circular cooldown swipe.

### 4.6 Weapon Proc Enchant Filtering (Slot 16)
- **Strict Proc-Only Visibility**: `09 - Enchants warTank` is exclusively displayed when an enchantment with actual combat procs is present on the Main-Hand weapon (Slot 16): *Blade Ward*, *Blood Draining* (stacks 1-5 & emergency heal), *Mongoose*, *Berserking*, *Executioner*, *Crusader*, *Lifeward*, *Black Magic*, *Icebreaker*, *Giant Slayer*, *Deathfrost*, *Unholy Weapon*, *Fiery Weapon*, *Lifestealing*.
- **Static Enchant Suppression**: Static enhancements (*Titanguard* +30 Stamina, *Accuracy* +25 Hit/+25 Crit, *Titanium Weapon Chain* +28 Hit/-50% Disarm, *Superior Potency* +65 AP, *Exceptional Agility* +26 Agi, *Major Defense* +12 Def, etc.) or weapons with no enchant strictly evaluate `_G.PWHUD_CheckEnchantsEquipped() == false`.
- **Seamless Row Auto-Centering**: When suppressed, `09 - Enchants warTank` is excluded from `activeOrder` in `_G.PWHUD_UpdateUtilityRowPositions()`, automatically re-centering the remaining utility icons without an empty gap.

### 4.5 Revenge Ready Engine & Dynamic Refresh
- **Internal 5.0s Window with CLEU Tracking**: Subscribed to `COMBAT_LOG_EVENT_UNFILTERED` detecting incoming `DODGE`, `PARRY`, and `BLOCK` (`blocked > 0`) on the player.
- **Dynamic Real-Time Refresh**: Each subsequent avoid or block immediately resets the internal timer back to full 5.0 seconds.
- **Reset on Cast**: `SPELL_CAST_SUCCESS` for Revenge (all spell IDs) immediately clears the active timer.
- **Visual Polish**: Circular cooldown swipe, `%p` countdown seconds text, centered `REV` tag, and amber Pixel Glow via `LibCustomGlow-1.0` with explicit `LCG.PixelGlow_Stop` in both `finish` and `untrigger` to eliminate stuck yellow line artifacts.

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
