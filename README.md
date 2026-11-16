> 🇮🇹 **Versione Italiana**: [README_IT.md](README_IT.md)
>
> 🌐 **Live Web Simulator**: [https://glacyal.github.io/protection-warrior-335a-am/](https://glacyal.github.io/protection-warrior-335a-am/)

# Class Warrior (Protection) — WeakAuras Suite

[![WoW Version](https://img.shields.io/badge/World%20of%20Warcraft-3.3.5a%20(12340)-orange.svg)](https://github.com/Glacyal/protection-warrior-335a-am)
[![WeakAuras](https://img.shields.io/badge/WeakAuras-5.21.8+-blue.svg)](https://github.com/Glacyal/protection-warrior-335a-am)
[![Class](https://img.shields.io/badge/Class-Warrior%20(Protection%20Tank)-blue.svg)](https://github.com/Glacyal/protection-warrior-335a-am)
[![GitHub Pages](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-brightgreen.svg)](https://glacyal.github.io/protection-warrior-335a-am/)
[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-gray.svg?logo=paypal&logoColor=white&labelColor=0079c1)](https://www.paypal.me/AMantmar)

Complete, modular, and high-performance WeakAuras suite for **Level 80 Protection Warrior (Tank)** in World of Warcraft 3.3.5a (*Wrath of the Lich King - Build 12340*).  
Designed to guarantee 100% visual, geometric, and performance conformity with the **Class Warrior (Fury)** and **Class Mage (TTW Fire)** suites: synchronized **278px** center bars, dynamic utility row at $y = -45$, horizontal procs group at $y = 52$, compact $88 \times 60\text{px}$ stats panel at $x = -190$, and Sunder Armor tracker at $x = 160$.

The suite features an exclusive load condition bound to warriors with the **[Devastate]** talent learned (Talent Index `103`, Tab 3 Protection, Tier 8 Position 23), automatically remaining disabled and consuming zero CPU on Arms or Fury specs.

---

## 🌐 Live Web Simulator

Explore and interact with the HUD directly inside your browser without installing anything:  
👉 **[Open Live Web Simulator on GitHub Pages](https://glacyal.github.io/protection-warrior-335a-am/)**  
- **1:1 Visual Alignment with Fury Warrior**: Native proportions, 278px bars, responsive swing timer with additive glow, and clock swipe cooldown overlays.
- **Critical Health Emergency Advisor (<35% HP)**: Dynamic prioritized recommendation of the best ready defensive cooldown (*Shield Wall* > *Last Stand* > *Shield Block* > *Enraged Regen* > *Healthstone/Potion*).
- **Integrated Contextual Kick Advisor**: Castbar ($278 \times 20\text{px}$ at $y = +8$) evaluates spell interruptibility (`notInterruptible`) and prompts the optimal ability (*Shield Bash*, *Pummel*, *Stun*, or cast *Immune* notice).
- **Live Tanking Stats Panel**: Real-time evaluation of Combat Table Coverage (CTC), raid boss Lv.83 crit immunity (**540 Defense**), contextual Armor DR%, Shield Block Value (SBV), Hit/Exp, and EHP.

---

## 🌟 HUD Architecture (20 Ordered Nodes)

The suite is structured into 20 sequential nodes controlled by the master group `Class Warrior (Protection)` ($x = 0, y = -190$, scale $1.2$):

### 1. Dynamic Procs Group (`01 - Procs warTank`)
Positioned at the upper region of the HUD ($y = 52$), configured with `sort: "ascending"` to order active icons from left to right by expiration time (missing or soonest-expiring icons automatically sort to the far left):
1. **Sword and Board (Buff 50227)**: Zero-rage Shield Slam proc with instant CD reset, pulsing golden Pixel Glow, and a 5-second countdown.
2. **Revenge Ready warTank**: Triggered by any Dodge, Parry, or Block (`blocked > 0`) with an internal 5.0-second window, dynamic real-time refresh upon subsequent avoids/blocks, circular swipe animation, `%p` seconds countdown, and amber Pixel Glow (`LibCustomGlow-1.0`).
3. **Demoralizing Shout Tracker warTank**: Target debuff tracker for physical damage reduction. Raid-aware (satisfied by Warrior *Demoralizing Shout*, Feral Druid *Demoralizing Roar*, or Warlock *Curse of Weakness*). Displays `MISS` or countdown when expiring ($\le 10\text{s}$); hidden when $> 10\text{s}$.
4. **Thunder Clap Tracker warTank**: Target debuff tracker for melee attack speed reduction. Raid-aware (satisfied by Warrior *Thunder Clap*, Death Knight *Frost Fever*, Paladin *Judgements of the Just*, or Feral Druid *Infected Wounds*). Displays `MISS` or countdown when expiring ($\le 10\text{s}$); hidden when $> 10\text{s}$.
5. **Rend Tracker warTank**: Player bleed debuff tracker. Displays `MISS` or countdown when expiring ($\le 5\text{s}$); automatically suppressed and hidden on mechanical targets immune to bleed effects.
6. **Emergency Low HP Alert**: Flashing red Pixel Glow icon when health drops below 35%, surfacing the icon of the optimal ready cooldown (*Shield Wall* or *Last Stand*).
7. **Tank Buster Alert**: Dynamic high-priority alert covering all WotLK 3.3.5a raid bosses and dangerous trash mechanics (*Soul Reaper*, *Phase Punch*, *Rune of Blood*, *Impale*, *Gastric Bloat*, *Fusion Punch*, *Fiery Combustion*, etc.) with dynamic debuff icon commutation, circular swipe, action tags (`SWAP`, `x8`, `HEAL`, `RUN`, `PLASMA`), and intense red Pixel Glow.

### 2. Class Buffs & Defensive Stance (`02`, `03`, `04`)
Positioned on the left side directly above the Stats Panel at $x = -264, -232, -200, -168$ and $y = 0$ ($30 \times 30\text{px}$, 4-icon grid perfectly spanning the 126px width of the stats panel with 2px spacing):
- **02 - Battle Shout warTank**: Battle Shout active timer / missing alert (OFF).
- **03 - Commanding Shout warTank**: Commanding Shout active timer / missing alert (OFF).
- **04b - Vigilance warTank**: Vigilance missing alert on ally (OFF) using pure Focus Magic model (displays desaturated icon with red OFF whenever no group/raid ally carries Vigilance; countdown timer when $\le 60\text{s}$).
- **04 - Defensive Stance warTank**: Wrong stance combat warning (STANCE).
- **02 - Battle Shout warTank**: Displays countdown timer only when expiring ($\le 30\text{s}$) or desaturated with red `OFF` label when neither Battle Shout nor Paladin *Blessing of Might* is present.
- **03 - Commanding Shout warTank**: Displays countdown timer only when expiring ($\le 30\text{s}$) or desaturated with red `OFF` label when neither Commanding Shout nor Warlock *Blood Pact* is present.
- **04 - Defensive Stance warTank**: Aligned 1:1 with Fury Warrior (completely hidden during correct Defensive Stance; visible with red alert border and `STANCE` subtext only when out-of-stance during combat via `04 - Defensive Stance - OutOfStance warTank`).

### 3. Bottom Utility Row (`05` - `13`, at $y = -45$)
Adaptive horizontal centering below the rage bar featuring $28 \times 28\text{px}$ icons:
- **05 - Trinket 1 warTank** & **06 - Trinket 2 warTank**: Slot 13 & 14 auto-detection for tank trinkets (*Sindragosa's Flawless Fang*, *Glyph of Indomitability*, *Corpse Tongue Coin*, *Satrina's Impeding Scarab*, *Corroded Skeleton Key*, etc.).
- **06b - Ring warTank**: Tank ring tracker (*Ashen Band of Endless Courage*).
- **07 - Cloak warTank**: Proccable cloak combat enchant tracking (*Swordguard Embroidery* +400 AP; parachute tinker and static enchants like +22 Agility or +16 Defense are automatically suppressed to avoid clutter).
- **08 - Tier Set warTank**: T10 4P defensive cooldown tracker with *Bloodrage* icon (tracks 10s 20% max HP *Blood Frenzy* shield, Bloodrage recovery cooldown, and suppresses automatically when T10 4P is not equipped).
- **09 - Enchants warTank**: Main-Hand weapon proc enchant tracker (*Blade Ward*, *Blood Draining*, *Mongoose*, *Berserking*, etc.). Exclusively visible when an enchant capable of proccing is equipped; automatically suppressed and hidden when static enchants (+30 Stamina Titanguard, +25 Hit/+25 Crit Accuracy, Titanium Weapon Chain, +26 Agility, +65 AP) or no enchants are present, with seamless dynamic re-centering of the utility row.
- **10 - Gloves warTank**: *Reticulated Armor Webbing* (+885 Armor) or *Hyperspeed Accelerators*.
- **10b - Shield Block warTank**: Shield Block tracking at Y: -45 alongside Shield Wall (10s active duration swipe/countdown, recovery cooldown tracking 30s/60s, and clean ready state).
- **11 - Shield Wall warTank**: Spell 871 (-60% DR for 12s, duration swipe and CD).
- **12 - Last Stand warTank**: Spell 12975 (+30% HP for 20s, duration swipe and CD).
- **13 - Boots warTank**: Engineering *Nitro Boosts* or *Enraged Regeneration*.

### 4. Synchronized 278px Center Bars (`14`, `15`, `16`)
- **14 - Rage Bar warTank ($278 \times 14\text{px}$ at $y = -20$)**: Precise numeric value centered with 3-tier dynamic color shifts: dark red under 25 points (starvation), deep crimson between 25 and 44 points, and bright amber/gold above 45 points (safe rage-dumping threshold for Heroic Strike / Cleave).
- **15 - Rotational Bar warTank ($278 \times 7\text{px}$ at $y = -7$)**: Static rotational queue indicator occupying the full 278px width without scroll/swipe animation and without remaining time countdown. Features dynamic additive illumination and LibCustomGlow-1.0 Pixel Glow (Gold for *Heroic Strike*, Emerald Green for *Cleave*), fully aligned with the Fury Warrior queueing mechanics.
- **16 - Castbar warTank ($278 \times 20\text{px}$ at $y = +8$)**: Target (or player) castbar. Features left spell icon, contextual **Kick Advisor** spell label (e.g. `Frostbolt [KICK: SHIELD BASH]` in cyan, or `[IMMUNE]` in dark gray), and remaining cast time on the right.

### 5. Central Text Alerts (`17 - Alerts warTank`)
Alert group positioned at $y = 78$ directly above the procs:
- **Alert - Sword and Board**: Golden `SHIELD SLAM READY!` notification with War Drums sound.
- **Alert - Emergency CD**: Critical notification `CRIT HP: USE SHIELD WALL!` with audio cue.
- **Alert - Kick Now**: Clear interrupt prompt `INTERRUPT: SHIELD BASH!`.
- **Alert - Boss Enraged**: High-visibility notice `BOSS ENRAGED! POP CD!`.
- **Alert - Wrong Stance**: Priority warning banner at $y = 64$ `>> DEFENSIVE STANCE REQUIRED! <<` with `RaidWarning.ogg` audio trigger when out of Stance 2 during combat.

### 6. Fury Warrior-Style Tanking Stats Panel (`18 - Stats Panel warTank`)
Compact $88 \times 60\text{px}$ frame at $x = -190, y = -45$ (left of the utility row) featuring clean white labels `Label:` and color-coded values with dynamic thresholds:
```text
Def:   541 (CAP)
Armor: 25.3k (62.4%)
CTC:   74.6%
Block: 21.7% (1800 SBV)
Hit:   9.1% | 25 Exp
```

#### 📖 Glossary & Tanking Acronyms Reference
| Acronym | Full Name | Mechanical Meaning & WotLK 3.3.5a Relevance |
| :--- | :--- | :--- |
| **`DEF`** | **Defense Skill** | Total defense skill rating (`base + bonus`). Base at Lv.80 is 400. Reaching **540 Defense** (+140 from rating/talents) guarantees complete **Crit Immunity** against Lv.83 Raid Bosses (-5.6% incoming crit chance). Heroic Dungeon cap (Lv.82 mobs) is **535 Defense**. |
| **`ARM`** | **Armor & Physical DR%** | Instantaneous effective armor. The percentage in parentheses represents contextual Physical Damage Reduction: evaluated with Blizzard constant $K = 15232.5$ at Lv.80 default (e.g. 25,253 armor $\implies \mathbf{62.4\%}$, matching in-game character sheet tooltip 62.38%) and with $K = 16635$ against Lv.83 Raid Bosses / Skull ($\implies \mathbf{60.3\%}$, actual raid mitigation). Hard cap at **75.0%**. Includes active buffs (*Inspiration/Ancestral Fortitude* +25%) and debuffs. |
| **`CTC`** | **Combat Table Coverage** | Total combat table coverage: $\text{Dodge} + \text{Parry} + \text{Block} + \text{BossMiss}$. At $\ge \mathbf{102.4\%}$, the tank is **Unhittable**: no incoming boss melee swing can land as a normal unmitigated hit (they are all dodged, parried, blocked, or missed). Incorporates non-stacking boss hit debuffs (*Insect Swarm* / *Scorpid Sting* max +3% Miss). |
| **`Block`** | **Block Chance** | Probability to block an incoming melee swing with the shield. During active *Shield Block* (+100%), this value caps at 100%, instantly pushing total CTC well above 102.4%. |
| **`SBV`** | **Shield Block Value** | Fixed amount of physical damage absorbed by each successful shield block. In WotLK 3.3.5a, it is also the primary damage multiplier scaling **Shield Slam** damage and threat. |
| **`Hit`** | **Melee Hit Rating** | Accuracy for special melee abilities and *Taunt*. Cap against Lv.83 raid bosses is **8.0%** (263 rating), reduced to 7.0% (230 rating) with Draenei *Heroic Presence* (+1%). |
| **`Exp`** | **Expertise** | Reduces enemy chance to dodge and parry. **Soft Cap 26** (214 rating, eliminates boss frontal dodges). **Hard Cap 56** (eliminates boss frontal parries, negating *Parry-Haste* risks on Sindragosa, Halion, Lady Deathwhisper). |
| **`Avoid`** | **Pure Avoidance** | Sum of $\text{Dodge} + \text{Parry} + \text{Miss}$: percentage of attacks where the tank suffers **zero damage** (unlike blocking where damage is partially absorbed). |
| **`DR%`** | **Damage Reduction %** | Passive physical mitigation percentage provided by effective armor. |
| **`EHP`** | **Effective Health Pool** | Raw physical damage pool required to kill the tank without healing: $\text{EHP} = \frac{\text{Max HP}}{1 - (\text{DR}\% / 100)}$. |
| **`GCD`** | **Global Cooldown** | Standard 1.5-second recovery window between ability activations. |
| **`ICD`** | **Internal Cooldown** | Required cooldown interval (e.g. 45s or 50s) before a trinket proc effect can trigger again. |

### 7. Sunder Armor Tracker (`19 - Sunder Armor Tracker warTank`)
Positioned on the right side of the bars ($x = 160, y = -7$, $32 \times 32\text{px}$):
- Unique ID `19 - Sunder Armor Tracker warTank` preventing WeakAuras naming collisions and automated ` 2` duplicate suffixes when coexisting with Fury Warrior or other class suites.
- Full multi-class and multi-spec armor debuff support: tracks *Sunder Armor* (Warrior all-specs ranks 1-6), Rogue *Expose Armor* (`EA` in cyan), and Hunter Worm *Acid Spit*.
- Stack tracking: green `x5` at 5 stacks, white `x1`–`x4`, and dynamic icon shift to Expose Armor when rogue debuff is active.
- Numeric expiration countdown timer at base (%c1) and centered stacks (%c2).
- Prominent red `OFF` alert at base when major armor reduction is missing on the active hostile combat target.

---

## 📥 How to Import the WeakAuras String

1. Open [`IMPORT_STRING_v5.21.8.txt`](IMPORT_STRING_v5.21.8.txt) or copy it with one click from the [Live Web Simulator](https://glacyal.github.io/protection-warrior-335a-am/).
2. In-game, open WeakAuras by typing `/wa`.
3. Click **Import** at the top left.
4. Paste the string with `Ctrl + V` and press **Import Group**.

---

## 🛠️ Build & Development Workflow

- **Compile WA String**:
  ```bash
  python generate.py
  ```
- **Sync Web Simulator**:
  ```bash
  python scripts/sync_docs.py
  ```
- **Run Parallel Test Suite**:
  ```bash
  python tests/run_parallel_tests.py
  ```

---

## 📄 License
Released under the MIT License. Developed for the WotLK 3.3.5a community.
