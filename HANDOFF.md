> 🇮🇹 **Versione Italiana**: [HANDOFF_IT.md](HANDOFF_IT.md)
>
> 🌐 **Live Web Simulator**: [https://glacyal.github.io/protection-warrior-335a-am/](https://glacyal.github.io/protection-warrior-335a-am/)

# Class Warrior (Protection) — Technical Handoff

Technical reference manual for the development, maintenance, and architectural extension of the **Class Warrior (Protection)** suite for World of Warcraft 3.3.5a (*WotLK Build 12340*).

---

## 1. Project Overview

The suite is distributed as a **standalone WeakAura** in compressed `!WA:1!` format (`AceSerializer-3.0` binary serialization + Deflate RFC 1951 level 9 compression + `LibDeflate` character print encoding).  
It features precision 278px visual geometry engineered specifically for the Protection Warrior, guaranteeing Zero Native Warnings on WeakAuras 5.21.8+ (`internalVersion = 90`).

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
│   └── components/                  # Component modules (modular builder architecture)
│       ├── procs.py                 # 01 - Procs warTank (Dynamic group 34x34 at y = 52: 1:1 visual parity SAB/REV, dynamic multi-proc refresh, cast consumption, >=500k HP target filter)
│       ├── buffs.py                 # 02 - Battle Shout warTank, 03 - Commanding Shout warTank, 04 - Defensive Stance warTank (x = -271, -216, -161, y = 0, 34x34px)
│       ├── utility.py               # 05-13 - Utility Row (Trinkets, Ring, Cloak, Tier, Enchants, Gloves, Shield Wall warTank, Last Stand warTank, Boots) at y = -45
│       ├── bars.py                  # 14 - Rage Bar & 16 - Castbar warTank (Dual specular Target dx->sx & Player sx->dx with Bash/Reflect advisor)
│       ├── rotational.py            # 15 - Rotational Bar warTank (Main-Hand swing timer 274x5px aurabar at y = -7 with synchronized HS/Cleave queue Pixel Glow)
│       ├── alerts.py                # 17 - Alerts warTank (Minimalist emergency text alerts: Emergency CD, Kick Now)
│       ├── stats.py                 # 18 - Stats Panel warTank (96x60px panel at x = -192, y = -45, perfectly adapted to 5-row text without % Armor or SBV)
│       └── sunder.py                # 19 - Sunder Armor Tracker warTank (32x32px at x = 160, y = -7)
│
├── docs/                            # Documentation and interactive preview for GitHub Pages
│   └── index.html                   # Interactive HTML/CSS/JS simulator (purely in English, standalone Protection Warrior HUD)
│
├── scripts/
│   └── sync_docs.py                 # Automatic sync script for v5 string into docs/index.html
│
└── tests/                           # Automated parallel test suite
    ├── run_parallel_tests.py        # Multi-core test runner (ProcessPoolExecutor)
    ├── test_components_integrity.py # Structural module integrity verification (20 sequential nodes & UIDs)
    ├── test_lua.py                  # Lua syntax validation (triggers, untriggers, custom scripts)
    ├── test_tree_layout.py          # Geometric layout and positioning verification
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

### 4.2 Out-of-Stance Alert in Combat (Zero-Clutter Model)
- In correct Defensive Stance (`GetShapeshiftForm() == 2`), the stance icon is **completely hidden** (zero visual clutter on screen).
- Dual-layer alert triggers whenever `UnitAffectingCombat("player") and GetShapeshiftForm() ~= 2`:
  1. Local indicator `04 - Defensive Stance - OutOfStance` (X: -158, Y: 0, 28x28px) with red alert color and `STANCE` subtext.
  2. Compact icon `04 - Defensive Stance - OutOfStance warTank` (X: -168, Y: 0) alongside shouts (central intrusive text banner removed in Task 29).

### 4.3 Protection Warrior Tanking Stats Engine & Non-Stacking Debuffs
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

### 4.11 T10 4P Defensive Cooldown & Bloodrage Icon Architecture (08 - Tier Set warTank)
- **Defensive Cooldown Transformation**: With T10 4P equipped (*Ymirjar Lord's Battlegear*), *Bloodrage* (Spell ID 2687) acts as an active defensive cooldown granting a 10s absorption shield equal to 20% max HP (*Blood Frenzy*, Spell ID 70844).
- **Triggering Ability Icon**: Standardized texture to *Bloodrage* (`Interface\Icons\Ability_Racial_BloodRage`), the exact ability that triggers the defensive shield.
- **Three-State Cooldown Engine**:
  1. `ACTIVE`: 10s countdown (`%.1fs`), circular swipe, and amber Pixel Glow (`LibCustomGlow-1.0`).
  2. `COOLDOWN`: Real-time tracking of Bloodrage spell cooldown (60s base or talent-reduced) with numeric countdown and recovery swipe.
  3. `READY`: Clean, ready Bloodrage icon ready to pop defensive shield.
- **Dynamic Centering & Edge Polish**: Strictly suppressed when T10 4P is not equipped; `cooldownEdge: False` ensures clean borders.

### 4.13 Shield Block Relocation to Utility Row (10b - Shield Block warTank)
- **Moved to Bottom Utility Row (Y: -45)**: Completely removed `Shield Block Active` from the upper procs dynamic group (`01 - Procs warTank`), placing it in the bottom utility row as `10b - Shield Block warTank` alongside `11 - Shield Wall warTank` and `12 - Last Stand warTank`.
- **Three-State Cooldown & Duration Engine**:
  1. `ACTIVE`: When *Shield Block* (Spell ID 2565) is active, tracks the 10-second duration with circular swipe, yellow countdown seconds (`|cFFFFFF00%.1fs|r`), and golden Pixel Glow (`LibCustomGlow-1.0`).
  2. `COOLDOWN`: When the buff expires, tracks remaining cooldown (base 60s, or 30s with *Shield Mastery* talent) with cooldown swipe, numeric countdown text, and clean borders (`cooldownEdge: False`).
  3. `READY`: When available, displays clean official icon (`Ability_Defensive`) without clutter.
- **Dynamic Row Auto-Centering**: Integrated into `_G.PWHUD_UpdateUtilityRowPositions()` preceding Shield Wall, supporting natural auto-centering for up to 11 utility icons.

### 4.12 Comprehensive Tank Buster Alert Database (WotLK 3.3.5a Raids & Deadly Trash)
- **All-Tier Boss & Trash Mechanics**: Full Spell ID database `_G.PWHUD_TankBustersDB` and bilingual name table `_G.PWHUD_TankBustersByName` in `builder/components/procs.py`:
  - **Icecrown Citadel (ICC)**: Soul Reaper (Lich King 10N/25N/10H/25H - 69409, 73797, 73798, 73799; `SWAP`), Gastric Bloat (Festergut 10N/25N/10H/25H >= 8 - 72219, 72551, 72552, 72553; `x8`), Rune of Blood (Deathbringer Saurfang - 72410; `SWAP`), Mystic Buffet (Sindragosa P3 >= 5 - 70127, 70128; `x5`), Delirious Slash (Blood-Queen Lana'thel >= 2 - 71623, 71624; `x2`), Mutated Plague (Putricide P3 >= 2 - 72451..72454; `x2`), Mutated Infection (Rotface - 69674..73023; `INFECT`), Corrosion (Valithria Zombie >= 3 - 70751, 71236; `x3`), Gut Spray (Valithria Abomination - 70633, 71232; `SPRAY`), Severed Flesh (Deathbound Ward / ICC Trash >= 3 - 71127; `x3`).
  - **Ruby Sanctum (RS)**: Fiery Combustion (Halion - 74562, 74567, 74795; `RUN`), Soul Consumption (Halion Twilight - 74792, 74793, 74799; `RUN`), Cleave Armor (General Zarithrian >= 2 - 74367; `x2`), Enervating Brand (Baltharus the Warborn - 74502; `BRAND`).
  - **Trial of the Crusader (TotC / ToGC)**: Impale (Gormok >= 2 - 67478, 67479, 66331; `x2`), Paralytic Toxin (Acidmaw - 66823, 67618; `TOXIN`), Incinerate Flesh (Jaraxxus - 66237, 67049..67051; `HEAL`), Expose Weakness (Anub'arak Burrower >= 2 - 67847..67849; `x2`).
  - **Ulduar**: Phase Punch (Algalon >= 3 - 64412, 64417; `x3`), Unbalancing Strike (Thorim - 62130, 62131; `SWAP`), Fusion Punch (Steelbreaker - 61903, 63493; `FUSION`), Overwhelming Power (Steelbreaker - 61888, 64637; `MELT`), Fuse Armor (Razorscale >= 2 - 64771, 64772; `x2`), Surge of Darkness (General Vezax - 62661, 62662; `CD!`), Plasma Blast (Mimiron - 62997, 64529; `PLASMA`), Crunch Armor (Kologarn >= 2 - 63355, 64002; `x2`), Slag Pot (Ignis - 62717, 63477; `POT`).
  - **Naxxramas, VoA, Sartharion**: Mortal Wound (Gluth >= 4 - 25646; `x4`), 4 Horsemen Marks (Blaumeux, Rivendare, Korth'azz, Zeliek >= 3 - 28832..28835; `x3`), Frostbite (Toravon the Ice Watcher >= 4 - 72098; `x4`), Twilight Torment (Sartharion - 57948; `SHADOW`).
- **Dynamic Graphical Polish**:
  - `customIcon`: dynamically commutates to the exact texture of the threatening debuff.
  - `customDuration`: circular countdown swipe with clean border (`cooldownEdge: False`).
  - `customText`: contextual tag or stack count (`SWAP`, `x8`, `HEAL`, `RUN`, `PLASMA`, etc.).
  - Intense red Pixel Glow via `LibCustomGlow-1.0` on start, automatic cleanup on expiration.

### 4.10 Vigilance Missing Alert (04b - Vigilance warTank — Pure Focus Magic Architecture)
- **1:1 Alignment with Focus Magic**: Removed talent inspection gates incompatible with 3.3.5a FrameXML; displays prominent desaturated `Ability_Warrior_Vigilance` icon with red `OFF` whenever no group/raid ally carries the buff (`not allyActive`).
- **Event-Driven Ally Lifecycle**:
  - `UNIT_SPELLCAST_SUCCEEDED`: Detects player casting Vigilance on a friendly target (`expires = now + 1800`).
  - `COMBAT_LOG_EVENT_UNFILTERED`: Tracks `SPELL_AURA_APPLIED`, `SPELL_AURA_REFRESH`, `SPELL_AURA_REMOVED`, `SPELL_AURA_BROKEN`, and instantly resets if the protected ally dies (`UNIT_DIED`).
  - Automatic fallback scanning across `target`, `focus`, `party1..4`, and `raid1..40`.
- **Anti-Clutter Visual Model**:
  - `Vigilance - OFF warTank`: Prominent desaturated icon with red `OFF` at `INNER_BOTTOM`, displayed whenever no group/raid ally carries the buff.
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
- Dynamic queueing logic for Heroic Strike and Cleave via `IsCurrentSpell()`:
  - Gold pixel glow (`LibCustomGlow-1.0`) and ADD vertex tint when *Heroic Strike* (`47450`) is queued.
  - Emerald Green pixel glow and ADD vertex tint when *Cleave* (`47520`) is queued.
  - Returns to neutral warrior copper/bronze static appearance when no ability is queued.

### 4.14 Dynamic Auto-Adapting Utility Row for War Tank
- **Natural Dynamic Centering**: The bottom utility row (`05` - `13`, at $y = -45\text{px}$) implements a dynamic auto-centering engine engineered specifically for the Protection Warrior.
- **Dynamic Centering Algorithm**: The engine dynamically evaluates `activeOrder` containing exclusively equipped and qualified items, positioning all active frames centered at $x = 0$ under the $278\text{px}$ rage bar via $\text{targetX} = \lfloor (i - \frac{N+1}{2}) \times \text{step} + 0.5 \rfloor$, dynamically scaling step ($25\text{px}-52\text{px}$) and frame width ($24\text{px}-28\text{px}$) for $N = 3 \dots 11$ active icons.
- **Strict Item Whitelist Enforcement**:
  1. **Trinkets 1 & 2 (Slot 13/14)**: Always visible when equipped (`itemID > 0`). Full database of WotLK mitigation and DPS trinkets with On-Use, ICD (45s–120s), and proc duration tracking.
  2. **Ring (Slot 11/12)**: Strictly limited to *Ashen Band of Endless Courage* (Tank Armor proc, Spell ID 72414) or *Ashen Band of Endless Vengeance* (Melee AP proc, Spell ID 72412). Static stat rings are completely suppressed.
  3. **Cloak (Slot 15)**: Strictly limited to combat proc enchants (Tailoring *Swordguard Embroidery* / *Ricamo della Spada* +400 AP, Spell ID 55775). Parachute tinker (*Flexweave Underlay*) and static enchants (+22 Agi, +16 Def, +225 Armor) are strictly suppressed.
  4. **Tier Set (08)**: Strictly limited to when **4 Pieces of Tier 10** (*Ymirjar Lord's Battlegear* 4P: bonus 20% magic DR during Shield Block) are equipped. Suppressed otherwise.
  5. **Weapon Enchants (Slot 16)**: Strictly limited to proccable weapon enchants (*Blade Ward*, *Blood Draining*, *Mongoose*, *Berserking*). Static enchants (+30 Stamina Titanguard, +20 Strength, etc.) are strictly suppressed.
  6. **Gloves (Slot 10)**: Strictly limited to active engineering tinkers (*Reticulated Armor Webbing* +885 Armor or *Hyperspeed Accelerators*).
  7. **Defensive Cooldowns (`10b`, `11`, `12`)**: `Shield Block` (10s duration, 30s/60s CD), `Shield Wall` (-60% DR for 12s, emergency glow <35% HP), and `Last Stand` (+30% max HP for 20s, emergency glow <35% HP) are permanently integrated into the active row preceding boots.
  8. **Boots (Slot 8)**: Active engineering *Nitro Boosts* tinker or utility fallback on *Enraged Regeneration*.
- **Core Initialization Bootstrap**: Due to WeakAuras 3.3.5a omitting execution of `actions.init` on container groups, global bootstrap (`_G.PWHUD_InitCore` and `_G.PWHUD_UpdateUtilityRowPositions`) is strictly located within the trigger of `05 - Trinket 1 warTank` (`slot == 13`).

---

### 4.15 Stats Panel Text Optimization (% Armor & SBV Removal) & 88x60px Geometric Adaptation with Top 4-Buff Cluster Harmony
- **Removal of Redundant Text**:
  - Cleaned line 2 (`Armor`) by removing `(%.1f%%)` $\rightarrow$ displays strictly `Armor: 25.3k` (retaining dynamic green coloration at $\ge 75\%$ DR hard cap).
  - Cleaned line 4 (`Block`) by removing `(%d SBV)` $\rightarrow$ displays strictly `Block: 21.7%`.
  - The resulting 5-row layout is ultra-clean, legible, and compact.
- **Compact 88x60px Stats Panel Geometry**:
  - Reconfigured group `18 - Stats Panel warTank` to $X = -190\text{px}, Y = -45\text{px}$.
  - Background `Stats Panel - Background warTank` sized to $88 \times 60\text{px}$.
  - Text `Stats Panel - Text warTank` centered with $X = 2$ and left-aligned, eliminating lateral wasted space.
- **Top 4-Buff Cluster Harmonization (20x20px with 2px gap)**:
  - Reconfigured the 4 icons directly above:
    1. `02 - Battle Shout warTank`: $X = -223\text{px}, Y = 0$, size $20 \times 20\text{px}$ (Active: font 9pt; OFF: font 8pt).
    2. `03 - Commanding Shout warTank`: $X = -201\text{px}, Y = 0$, size $20 \times 20\text{px}$ (Active: font 9pt; OFF: font 8pt).
    3. `04b - Vigilance warTank`: $X = -179\text{px}, Y = 0$, size $20 \times 20\text{px}$ (Active: font 9pt; OFF: font 8pt).
    4. `04 - Defensive Stance warTank`: $X = -157\text{px}, Y = 0$, size $20 \times 20\text{px}$ (OutOfStance: font 7pt).
  - Uniform $22\text{px}$ pitch ($20\text{px}$ width + $2\text{px}$ gap) spanning exactly $86\text{px}$ from $X = -233$ to $X = -147$, centered symmetrically over the $88\text{px}$ Stats Panel at $X = -190$ with $1\text{px}$ border margin.

---

### 4.16 Top 4-Buff Cluster Optimization to 24x24px & 96x60px Stats Panel Alignment
- **Top 4 Buff Icons Enlarged to 24x24px**:
  - Increased icon dimensions from 20x20px to 24x24px (+20% linear, +44% surface area), dramatically enhancing visual recognition of spell textures and readability of countdown / OFF text:
    1. `02 - Battle Shout warTank`: $X = -231\text{px}, Y = 0$, size $24 \times 24\text{px}$ (Active: font 10pt; OFF: font 9pt).
    2. `03 - Commanding Shout warTank`: $X = -205\text{px}, Y = 0$, size $24 \times 24\text{px}$ (Active: font 10pt; OFF: font 9pt).
    3. `04b - Vigilance warTank`: $X = -179\text{px}, Y = 0$, size $24 \times 24\text{px}$ (Active: font 10pt; OFF: font 9pt).
    4. `04 - Defensive Stance warTank`: $X = -153\text{px}, Y = 0$, size $24 \times 24\text{px}$ (OutOfStance: font 8pt).
  - Uniform $26\text{px}$ step ($24\text{px}$ width + $2\text{px}$ gap) spanning $102\text{px}$ from $X = -243$ to $X = -141$.
- **96x60px Stats Panel Geometric Alignment**:
  - Reconfigured `18 - Stats Panel warTank` to $X = -192, Y = -45$ with background $96 \times 60\text{px}$.
  - Perfectly balanced vertical column with 3px symmetrical margin relative to top icons, 5px clearance from Rage Bar, and 10px from Utility Row.

---

### 4.17 Castbar Optimization: Right-to-Left Player Fill, Dynamic Spell Icon, Target Priority & Instant Interrupt/Kick Untrigger
- **Unified Right-to-Left Direction (`inverse = True`)**:
  - `Castbar - Player warTank` inverted to flow smoothly from right to left (`inverse: True`), matching the visual convention of the HUD.
- **Dynamic Spell Icon Resolution**:
  - Fixed `iconSource: 0` (Trigger Icon) and eliminated the Lua multi-return truncation bug in `customIcon`. The bar displays the exact texture of the active player spell or channel.
- **Strict Target Priority & Immediate Kick Cancellation**:
  - `Castbar - Player warTank` automatically yields to `Castbar - Target warTank` whenever the target begins casting.
  - Replaced faulty `untrigger: function() return false end` with semantic `ki == nil` and `spell == nil` checks, ensuring both bars vanish instantaneously upon being kicked or interrupted.

---

### 4.18 Castbar Dynamic Icon Resolution: Auto Trigger Icon, 3.3.5a Channel Unpacking & Direct Frame Texture Update
- **Elimination of Red Question Mark (`INV_Misc_QuestionMark`)**:
  - Identified that `auto: False` forced WeakAuras to ignore `customIcon` and render `displayIcon` on every frame update. Enabled `auto: True` and removed `INV_Misc_QuestionMark`.
- **WotLK 3.3.5a `UnitChannelInfo` Compatibility**:
  - Corrected return unpacking for `UnitChannelInfo`: in 3.3.5a, channeled spells return `name, text, texture, startTimeMS, endTimeMS` (texture is 3rd argument, not 4th).
- **Direct Frame Texture Binding & Fallback**:
  - Added robust `GetSpellTexture(spell)` fallback and explicit `aura_env.region.icon:SetTexture(icon)` in both `customText` and `customIcon` ensuring instant, zero-latency icon updates on screen.

---

### 4.19 Alert - Kick Now Lua Error Elimination: Hostile Target Filter, Legacy Kick Logic Cleanup & Clean Untrigger
- **Elimination of Boolean Arithmetic Exception**:
  - Removed obsolete duplicate `_G.PWHUD_GetKickInfo` from `builder/components/utility.py` which incorrectly unpacked the 6th return value of `UnitChannelInfo` (`isTradeSkill`, boolean) into `endTime`, causing an irrecoverable `attempt to perform arithmetic on a boolean value` when party members channeled spells or crafted.
- **Strict Hostile Target Filtering (`UnitCanAttack`)**:
  - Enforced `UnitCanAttack("player", "target")` across `_G.PWHUD_GetTargetCastInfo()` and `Alert - Kick Now`. Completely prevents the interrupt engine from inspecting or attempting to interrupt friendly players and dungeon party members.
- **State Cleanup & Untrigger Fix**:
  - Replaced corrupted `untrigger: function() return false end` with immediate semantic cleanup returning `true` whenever target is missing, friendly, dead, or not casting an interruptible spell.
- **Italian Spell Localization Support**:
  - Added Italian client spell names (*Colpo di Scudo*, *Percossa*) alongside English names (*Shield Bash*, *Pummel*) for range and cooldown evaluation.

---

### 4.20 Player Castbar Channeled/Fishing Fix & Fishing Rod Auto-Suppression on Rotational Bar
- **Resolution of Channeled/Fishing Arithmetic String Error**:
  - Corrected `UnitChannelInfo("player")` return unpacking in `Castbar - Player warTank`. WotLK 3.3.5a returns 8 parameters including `rank`. Adding `cRank` ensures `csTime` and `ceTime` receive numeric millisecond timestamps, eliminating `attempt to perform arithmetic on a string value` when channeling Fishing or any trade skill.
- **Fishing Rod Auto-Suppression on 15 - Rotational Bar warTank**:
  - Added global detector `_G.PWHUD_IsFishingOrPole` checking active fishing channels and Main Hand slot 16 fishing pole equipment (`IsEquippedItemType("Fishing Poles")` / `"Canne da pesca"` / `GetItemInfo`).
  - Automatically suppresses and untriggers all 4 swing timer auras (`Background`, `Base Bar`, `HS Queued`, `Cleave Queued`) while a fishing rod is equipped or active, delegating fishing visual progress strictly to `16 - Castbar warTank`.

---

### 4.21 Emergency CD Alert Lua Error Resolution & 80% HP Recovery Hysteresis
- **Resolution of Table Method `:upper()` Lua Exception**:
  - `_G.PWHUD_GetEmergencyCD()` returns a table `{ action = "...", icon = "...", pct = ... }`. Fixed `customText` in `Alert - Emergency CD` to safely extract `cd.action` before formatting uppercase, preventing the `attempt to call method 'upper' (a nil value)` crash.
- **Dynamic 80% HP Recovery Hysteresis**:
  - Implemented requested persistence mechanic: the alert triggers when health drops below 35% in combat, but remains active until health recovers **above 80%** (`pct >= 80`), combat ends, or the player dies. This prevents annoying alert flickering when health hovers around the 35% threshold during active healing.
- **Multi-Language & Spell ID Cooldown Evaluation**:
  - `_G.PWHUD_GetEmergencyCD(maxThreshold)` supports dynamic threshold checking up to 80% HP and evaluates cooldowns via spell IDs (871, 12975, 2565, 55694) and Italian localization (*Muro di Scudo*, *Ultima Difesa*, *Blocco con lo Scudo*, *Rigenerazione Furente*).

---

### 4.22 Classic/TBC/WotLK 4-State Cast Advisor (`BOTH` / `KICK` / `REFLECT` / `IMMUNE`)
- **Full Cross-Expansion Audit & Classification**:
  - Completed comprehensive verification in [docs/CAST_ADVISOR_AUDIT.md](file:///d:/0Progetti/protection-warrior-335a-am/docs/CAST_ADVISOR_AUDIT.md) mapping Mob, Enemy Player (PvP), and Boss interactions across Classic, TBC, and WotLK 3.3.5a.
- **Event-Driven CLEU `spellId` & `spellSchool` Tracker (`_G.PWHUD_CastTracker`)**:
  - Anchored inside leaf aura `Castbar - Target warTank` (avoiding group-level `actions.init` per WotLK WeakAuras behavior) capturing `SPELL_CAST_START` & `SPELL_CAST_SUCCESS` to determine exact `spellId` and `spellSchool` (blocking physical castbars `spellSchool == 1` like *Steady Shot* / *Shattering Throw* / *Shoot* from ever triggering Spell Reflection).
- **Net 4-State Resolution Engine & Immunity Detection**:
  - Separates `canKick` and `canReflect`: enforces `isTradeSkill` suppression, scans target buffs without GC allocations for *Divine Shield*, *Hand of Protection* (blocking physical kicks), *Ice Block*, *Aura Mastery* + *Concentration Aura*, *Shroud of the Occult*, and boss *Spell Reflection*.
  - Enforces an O(1)-cached Anti-Reflect Blacklist (heals, rez, summons, ground/cone AoEs, *Mana Burn*, active channels, physical/boss mechanics) plus `worldboss` suppression with explicit Classic/TBC/WotLK Boss Reflect Whitelist (*Lord Jaraxxus Fel Fireball*, *Essence of Desire Deaden*, *Attumen Intangible Presence*, PvP-like council encounters) while keeping `Kel'Thuzad Frostbolt`, `General Vezax Searing Flames`, and `Lady Deathwhisper Frostbolt` strictly `KICK`-only.
  - Updated `Alert - Kick Now` to trigger strictly when `canKick == true`.

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
