> 🇬🇧 **English Version**: [HANDOFF.md](HANDOFF.md)
>
> 🌐 **Live Web Simulator**: [https://glacyal.github.io/protection-warrior-335a-am/](https://glacyal.github.io/protection-warrior-335a-am/)

# Class Warrior (Protection) — Handoff Tecnico

Manuale di riferimento tecnico per lo sviluppo, la manutenzione e l'estensione della suite **Class Warrior (Protection)** per World of Warcraft 3.3.5a (*WotLK Build 12340*).

---

## 1. Panoramica del Progetto

La suite è distribuita come **WeakAura autonoma** in formato compresso `!WA:1!` (serializzazione binaria `AceSerializer-3.0` + compressione Deflate RFC 1951 livello 9 + codifica di stampa `LibDeflate`).  
Rispetta l'identica geometria visiva a 278px introdotta con **Class Warrior (Fury)** e **Class Mage (TTW Fire)**, garantendo Zero Warning nativa su WeakAuras 5.21.8+ (`internalVersion = 90`).

| Proprietà | Dettaglio |
| :--- | :--- |
| **Piattaforma Target** | World of Warcraft 3.3.5a (WotLK Build 12340) |
| **Engine WeakAuras Target** | **WeakAuras 5.21.8+** (`internalVersion = 90`, `w = "5.21.8"`). |
| **File di Distribuzione** | [`IMPORT_STRING_v5.21.8.txt`](IMPORT_STRING_v5.21.8.txt) (stringa ufficiale pronta per l'importazione) |
| **Simulatore Web** | [`docs/index.html`](docs/index.html) |
| **Live Demo Online** | [GitHub Pages Live Showcase](https://glacyal.github.io/protection-warrior-335a-am/) |
| **Controllo Versione** | Git su GitHub: [Glacyal/protection-warrior-335a-am](https://github.com/Glacyal/protection-warrior-335a-am) |

---

## 2. Struttura del Repository

```text
protection-warrior-335a-am/
├── IMPORT_STRING_v5.21.8.txt        # Stringa WeakAuras 5.21.8+ nativa (Zero warning, internalVersion: 90)
├── generate.py                      # Compilatore Python dell'albero WA
├── README.md                        # Documentazione utente primaria (Inglese)
├── README_IT.md                     # Documentazione utente secondaria (Italiano)
├── HANDOFF.md                       # Specifiche tecniche primarie per sviluppatori (Inglese)
├── HANDOFF_IT.md                    # Specifiche tecniche secondarie per sviluppatori (Italiano)
├── .gitignore                       # Esclusioni virtualenv, cache e policy docs/*.md
│
├── builder/                         # Pacchetto Python modulare per la generazione dell'HUD
│   ├── tree.py                      # Assemblatore dell'albero gerarchico (20 nodi controllati)
│   ├── core/                        # Moduli core di serializzazione e codifica
│   │   ├── constants.py             # Load conditions (Warrior), texture, font Expressway, cap difensivi
│   │   ├── serializer.py            # Serializzatore AceSerializer-3.0 puro (^1...^^)
│   │   ├── deflate.py               # Compressione Deflate RFC 1951 + LibDeflate Print Encoding
│   │   ├── encoder.py               # Generatore stringa finale (!WA:1!...)
│   │   └── helpers.py               # Generatori di subtext dual-key e helper grafici
│   └── components/                  # Moduli dedicati ai singoli componenti dell'HUD (identici a Fury)
│       ├── procs.py                 # 01 - Procs warTank (Dynamic Group orizzontale a 7 icone 34x34 a y = 52)
│       ├── buffs.py                 # 02 - Battle Shout, 03 - Commanding Shout, 04 - Defensive Stance (x = -222, -190, -158, y = 0)
│       ├── utility.py               # 05-13 - Utility Row (Monili, Anello, Mantello, Tier, Incanti, Guanti, Shield Wall, Last Stand, Boots) a y = -45
│       ├── bars.py                  # 14 - Rage Bar (278x14px a y = -20) & 16 - Castbar warTank (278x20px a y = +8 con Kick Advisor)
│       ├── rotational.py            # 15 - Rotational Bar (Indicatore statico di accodamento 278x7px a y = -7 con Pixel Glow HS/Cleave)
│       ├── alerts.py                # 17 - Alerts warTank (Avvisi testuali centrali a y = 78)
│       ├── stats.py                 # 18 - Stats Panel warTank (Pannello 88x60px a x = -190, y = -45)
│       └── sunder.py                # 19 - Sunder Armor Tracker warTank (32x32px a x = 160, y = -7)
│
├── docs/                            # Documentazione e anteprima interattiva per GitHub Pages
│   └── index.html                   # Simulatore interattivo HTML/CSS/JS (puramente in Inglese, proporzioni 1:1 identico a Fury)
│
├── scripts/
│   └── sync_docs.py                 # Sincronizzazione automatica della stringa v5 in docs/index.html
│
└── tests/                           # Suite di test automatici e paralleli
    ├── run_parallel_tests.py        # Test runner parallelo multi-processore (ProcessPoolExecutor)
    ├── test_components_integrity.py # Verifica integrità strutturale moduli (20 nodi sequenziali e UIDs)
    ├── test_lua.py                  # Validazione sintassi codice Lua (trigger, untrigger, actions)
    ├── test_tree_layout.py          # Verifica conformità geometrica 1:1 con Fury Warrior
    ├── test_string_sync.py          # Verifica corrispondenza tra builder e IMPORT_STRING_v5.21.8.txt
    ├── test_stats_panel.py          # Verifica formule tank (Armor DR contestuale, EHP, CTC, Defense 540)
    ├── test_defensives.py           # Verifica cooldown di mitigazione (Shield Wall, Last Stand, Shield Block)
    ├── test_interrupts.py           # Verifica Kick Advisor (Shield Bash, Pummel, notInterruptible)
    └── test_danger_alerts.py        # Verifica allarmi salute critica e boss mechanics
```

---

## 3. Workflow di Sviluppo

1. **Modifica Componenti**:
   - Modifica i moduli in `builder/components/` o le formule in `builder/core/`.
2. **Esecuzione Test Paralleli**:
   - Lancia la suite di test completa sfruttando tutti i core della CPU:
     ```bash
     python tests/run_parallel_tests.py
     ```
   - Tutti gli 8 test devono risultare `[OK] PASSED` in circa 0.3 secondi.
3. **Compilazione Stringa di Importazione**:
   - Ricompila la stringa nativa WA 5.21.8+ eseguendo:
     ```bash
     python generate.py
     ```
4. **Sincronizzazione Simulatore Web**:
   - Sincronizza la stringa compilata all'interno del simulatore web:
     ```bash
     python scripts/sync_docs.py
     ```
5. **Commit & Push (`CP`)**:
   - Esegui lo staging e il commit dei file di codice e documentazione pubblica.

---

## 4. Specifiche Tecniche Recenti

### 4.1 Load Condition Specifica [Devastate]
- Indice lineare WeakAuras: **`103`** (calcolato come $(3 - 1) \times 40 + 23$, corrispondente al Tab 3 Protection, Tier 8 Colonna 1, Spell ID `20243`).
- Configurazione in `builder/core/constants.py`:
  ```python
  PROT_WARRIOR_LOAD = {
      "use_class": True,
      "class": {"single": "WARRIOR", "multi": {"WARRIOR": True}},
      "use_talent": True,
      "talent": {"single": 103, "multi": {103: True}},
      "use_vehicle": False,
  }
  ```
- Propagata uniformemente su root e su tutte le 43 aure figlie.

### 4.2 Notifica Postura Errata in Combattimento (Wrong Stance Alert — Modello Fury Warrior)
- In postura difensiva corretta (`GetShapeshiftForm() == 2`), l'icona è **completamente invisibile** (zero clutter a schermo, identico a Fury Warrior).
- Doppio livello di allarme attivo quando `UnitAffectingCombat("player") and GetShapeshiftForm() ~= 2`:
  1. Indicatore locale `04 - Defensive Stance - OutOfStance` (X: -158, Y: 0, 28x28px) con colore rosso e label `STANCE`.
  2. Banner centrale `Alert - Wrong Stance` (X: 0, Y: +64) a 20pt `>> DEFENSIVE STANCE REQUIRED! <<` con audio `RaidWarning.ogg`.

### 4.3 Motore Statistiche Tanking Stile Fury Warrior & Buff/Debuff Non-Stacking
- Formattazione a 5 righe con etichette bianche `|cFFFFFFFFLabel:|r <Valore>`:
  1. `Def:` (540 Cap per Lv.83, 535 per Lv.82).
  2. `Armor:` con Physical DR% contestuale ($K=15232.5$ a Lv.80 default pari a 62.4% come scheda PG; $K=16635$ su Raid Boss Lv.83 pari a 60.3%, hard cap 75%).
  3. `CTC:` Combat Table Coverage con motore non-stacking per *Insect Swarm* e *Scorpid Sting* (+3.0% Miss max).
  4. `Block:` con % di blocco e Shield Block Value (SBV).
  5. `Hit:` con Draenei *Heroic Presence* (+1.0%) ed `Exp:` con Soft Cap 26 ed Hard Cap 56.

### 4.4 Indicatore Statico di Accodamento Rotazionale (Heroic Strike & Cleave)
- Occupa l'intero spazio assegnato di 278x7px a $y = -7$ come barra statica e solida, senza animazione di scorrimento/swipe e senza numeri di tempo rimanente.
- Logica di queuing dinamico mutuata da Fury Warrior tramite `IsCurrentSpell()`:
  - Pixel Glow dorato (`LibCustomGlow-1.0`) e tinta vertex ADD quando *Heroic Strike* (`47450`) è accodato.
  - Pixel Glow verde smeraldo e tinta vertex ADD quando *Cleave* (`47520`) è accodato.
  - Ritorno all'aspetto copper/bronze neutro quando nessuna abilità è accodata.

---

## 5. Glossario & Riferimento Sigle Tecniche Tanking (WotLK 3.3.5a)

| Sigla | Termine Completo | Descrizione Meccanica e Formule WotLK |
| :--- | :--- | :--- |
| **`DEF`** | **Defense Skill** | Skill di difesa (`base + rating`). Cap **540** per immunità dai colpi critici dei boss Lv.83 (-5.6% crit subito), **535** in Eroiche Lv.82. |
| **`ARM`** | **Effective Armor & Physical DR%** | Armatura effettiva del player. Calcola la riduzione del danno fisico contestuale: con costante Blizzard $K = 15232.5$ a Lv.80 default (25.253 armatura $\implies \mathbf{62.4\%}$, identico alla scheda PG in-game) e $K = 16635$ contro Raid Boss Lv.83 ($\implies \mathbf{60.3\%}$, mitigazione effettiva). Hard cap al 75.0%. |
| **`CTC`** | **Combat Table Coverage** | Copertura totale della tabella colpi: $\text{Dodge} + \text{Parry} + \text{Block} + \text{BossMiss}$. A $\ge \mathbf{102.4\%}$ il tank è *Unhittable* (nessun colpo normale subito). Include debuff non-stacking (*Insect Swarm* / *Scorpid Sting* max +3%). |
| **`Block`** | **Block Chance** | Percentuale di blocco con lo scudo. Raggiunge il 100% durante l'abilità attiva *Shield Block* (10s). |
| **`SBV`** | **Shield Block Value** | Quantità fissa di danno assorbito per singolo blocco. Moltiplicatore primario che scala danno e threat di *Shield Slam*. |
| **`Hit`** | **Melee Hit Chance** | Percentuale di colpo a segno con attacchi speciali e Taunt. Cap a **8.0%** (263 rating), ridotto al 7.0% con *Heroic Presence* Draenei. |
| **`Exp`** | **Expertise** | Riduce le schivate e parate del boss. **Soft Cap 26** (214 rating, azzera schivate frontali), **Hard Cap 56** (azzera parate frontali ed elimina il rischio *Parry-Haste*). |
| **`Avoid`** | **Avoidance Pura** | Somma di $\text{Dodge} + \text{Parry} + \text{Miss}$ (percentuale di colpi in cui si incassano **zero danni**). |
| **`DR%`** | **Damage Reduction %** | Percentuale passiva di mitigazione fisica garantita dall'armatura effettiva. |
| **`EHP`** | **Effective Health Pool** | Salute effettiva: $\text{Salute Massima} / (1 - \text{DR}\%)$. |
| **`GCD`** | **Global Cooldown** | Finestra standard di 1.5 secondi tra abilità. |
