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
| **File di Distribuzione** | [`IMPORT_STRING_v5.21.8.txt`](file:///d:/0Progetti/protection-warrior-335a-am/IMPORT_STRING_v5.21.8.txt) (stringa ufficiale pronta per l'importazione) |
| **Simulatore Web** | [`docs/index.html`](file:///d:/0Progetti/protection-warrior-335a-am/docs/index.html) |
| **Live Demo Online** | [GitHub Pages Live Showcase](https://glacyal.github.io/protection-warrior-335a-am/) |
| **Controllo Versione** | Git su GitHub: [Glacyal/protection-warrior-335a-am](https://github.com/Glacyal/protection-warrior-335a-am) |

---

## 2. Struttura del Repository

```text
protection-warrior-335a-am/
├── IMPORT_STRING_v5.21.8.txt        # Stringa WeakAuras 5.21.8+ nativa (Zero warning, internalVersion: 90)
├── generate.py                      # Compilatore Python dell'albero WA
├── README.md                        # Documentazione utente, guida installazione e compatibilità
├── HANDOFF.md                       # Specifiche tecniche per sviluppatori e manutentori
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
│       ├── rotational.py            # 15 - Rotational Bar (Composite Swing Timer 278x7px a y = -7 con retroilluminazione HS/Cleave)
│       ├── alerts.py                # 17 - Alerts warTank (Avvisi testuali centrali a y = 78)
│       ├── stats.py                 # 18 - Stats Panel warTank (Pannello 88x60px a x = -190, y = -45)
│       └── sunder.py                # 19 - Sunder Armor Tracker (32x32px a x = 160, y = -7)
│
├── docs/                            # Documentazione e anteprima interattiva per GitHub Pages
│   └── index.html                   # Simulatore interattivo HTML/CSS/JS (proporzioni 1:1 identico a Fury)
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
    ├── test_stats_panel.py          # Verifica formule tank (Armor DR, EHP, CTC, Defense 540)
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

### 4.2 Notifica Postura Errata in Combattimento (Wrong Stance Alert)
- Doppio livello di allarme attivo quando `UnitAffectingCombat("player") and GetShapeshiftForm() ~= 2`:
  1. Indicatore `Defensive Stance - Warning` (X: -158, Y: 0) con Pixel Glow rosso e label `STANCE`.
  2. Banner centrale `Alert - Wrong Stance` (X: 0, Y: +64) a 20pt `>> DEFENSIVE STANCE REQUIRED! <<` con audio `RaidWarning.ogg`.

### 4.3 Motore Statistiche Tanking Stile Fury Warrior & Buff/Debuff Non-Stacking
- Formattazione a 5 righe con etichette bianche `|cFFFFFFFFLabel:|r <Valore>`:
  1. `Def:` (540 Cap per Lv.83, 535 per Lv.82).
  2. `Armor:` con Physical DR% contro boss Lv.83 ($K=16635$, hard cap 75%).
  3. `CTC:` Combat Table Coverage con motore non-stacking per *Insect Swarm* e *Scorpid Sting* (+3.0% Miss max).
  4. `Block:` con % di blocco e Shield Block Value (SBV).
  5. `Hit:` con Draenei *Heroic Presence* (+1.0%) ed `Exp:` con Soft Cap 26 ed Hard Cap 56.
