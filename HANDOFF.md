# Class Warrior (Protection) — Handoff Tecnico

Manuale di riferimento tecnico per lo sviluppo, la manutenzione e l'estensione della suite **Class Warrior (Protection)** per World of Warcraft 3.3.5a (*WotLK Build 12340*).

---

## 1. Panoramica del Progetto

La suite è distribuita come **WeakAura autonoma** in formato compresso `!WA:1!` (serializzazione binaria `AceSerializer-3.0` + compressione Deflate RFC 1951 livello 9 + codifica di stampa `LibDeflate`).  
Include un simulatore web interattivo per la visualizzazione e il testing dei preset ospitato su GitHub Pages, una suite completa di test deterministici in Python con runner multi-core parallelo e una conformità nativa per WeakAuras 5.21.8+ (Zero Warning nativa).

| Proprietà | Dettaglio |
| :--- | :--- |
| **Piattaforma Target** | World of Warcraft 3.3.5a (WotLK Build 12340) |
| **Engine WeakAuras Target** | **WeakAuras 5.21.8+** (`internalVersion = 90`, `w = "5.21.8"`, Zero Warning nativa). |
| **File di Distribuzione** | [`IMPORT_STRING_v5.21.8.txt`](file:///d:/0Progetti/protection-warrior-335a-am/IMPORT_STRING_v5.21.8.txt) (stringa ufficiale pronta per l'importazione) |
| **Simulatore Web** | [`docs/index.html`](file:///d:/0Progetti/protection-warrior-335a-am/docs/index.html) |
| **Live Demo Online** | [GitHub Pages Live Showcase](https://glacyal.github.io/protection-warrior-335a-am/) |
| **Controllo Versione** | Git su GitHub: [Glacyal/protection-warrior-335a-am](https://github.com/Glacyal/protection-warrior-335a-am) |
| **Politica Documentazione** | `docs/*.md` esclusi dal controllo versione via `.gitignore` per preservare il contesto locale senza appesantire il repository Git. |

---

## 2. Struttura del Repository

```text
protection-warrior-335a-am/
├── IMPORT_STRING_v5.21.8.txt        # Stringa WeakAuras 5.21.8+ nativa (Zero warning, internalVersion: 90)
├── generate.py                      # Compilatore Python dell'albero WA
├── README.md                        # Documentazione utente, guida installazione e compatibilità
├── HANDOFF.md                       # Specifiche tecniche per sviluppatori e manutentori
├── .gitignore                       # Esclusioni per virtualenv, cache e policy docs/*.md
│
├── builder/                         # Pacchetto Python modulare per la generazione dell'HUD
│   ├── tree.py                      # Assemblatore dell'albero gerarchico (20 nodi controllati)
│   ├── core/                        # Moduli core di serializzazione e codifica
│   │   ├── constants.py             # Load conditions (Warrior), texture, font Expressway, cap difensivi
│   │   ├── serializer.py            # Serializzatore AceSerializer-3.0 puro (^1...^^)
│   │   ├── deflate.py               # Compressione Deflate RFC 1951 + LibDeflate Print Encoding
│   │   ├── encoder.py               # Generatore stringa finale (!WA:1!...)
│   │   └── helpers.py               # Generatori di subtext dual-key e helper grafici
│   └── components/                  # Moduli dedicati ai singoli componenti dell'HUD
│       ├── alerts.py                # 01 - Emergency & Procs warTank & 19 - Boss Mechanics Alert
│       ├── interrupts.py            # 02 - Kick Advisor warTank & 17 - Spell Reflect Advisor
│       ├── defensives.py            # 03 - Defensive Row, 14 - Shield Wall, 15 - Last Stand, 16 - Shield Block
│       ├── rotational.py            # 04 - Rotational Bar (Shield Slam, Revenge, Devastate) & 20 - Swing & HS Queue
│       ├── debuffs.py               # 05 - Debuffs & Stance (Check Defensive Stance, Demo/TC) & 18 - Sunder Tracker
│       ├── taunts.py                # 06 - Taunt & Threat warTank (Taunt, Mocking, Challenging + Miss Alert)
│       ├── bars.py                  # 07 - Rage Bar, 08 - Health Bar warTank & 09 - Castbar warTank
│       ├── stats.py                 # 10 - Stats Panel warTank (Defense 540, CTC, Armor DR, SBV, Hit/Exp, EHP)
│       └── utility.py               # 11 - Trinket 1, 12 - Trinket 2, 13 - Gloves/Boots & Core Bootstrap Lua
│
├── docs/                            # Documentazione e anteprima interattiva per GitHub Pages
│   └── index.html                   # Simulatore interattivo HTML/CSS/JS (proporzioni 1:1, tracciato in Git)
│
├── scripts/
│   └── sync_docs.py                 # Sincronizzazione automatica della stringa v5 in docs/index.html
│
└── tests/                           # Suite di test automatici e paralleli
    ├── run_parallel_tests.py        # Test runner parallelo multi-processore (ProcessPoolExecutor)
    ├── test_components_integrity.py # Verifica integrità strutturale moduli (20 nodi sequenziali e UIDs)
    ├── test_lua.py                  # Validazione sintassi codice Lua (trigger, untrigger, actions)
    ├── test_tree_layout.py          # Verifica gerarchia e proporzioni albero WA
    ├── test_string_sync.py          # Verifica corrispondenza tra builder e IMPORT_STRING_v5.21.8.txt
    ├── test_stats_panel.py          # Verifica formule tank (Armor DR, EHP, CTC, Defense 540)
    ├── test_defensives.py           # Verifica cooldown di mitigazione (Shield Wall, Last Stand, Shield Block)
    ├── test_interrupts.py           # Verifica Kick Advisor (Shield Bash, Pummel, Stun, notInterruptible)
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

## 4. Logica Lua Centralizzata (`_G.PWHUD_*`)

Tutti i componenti attingono a un namespace centralizzato idempotente iniettato in `actions.init`:
- `_G.PWHUD_GetPlayerBuffs()`: scansione e cache dei buff del giocatore.
- `_G.PWHUD_GetPlayerDebuffs()`: monitoraggio debuff pericolosi (Soul Reaper, Impale, Gastric Bloat, Fusion Punch).
- `_G.PWHUD_GetTargetDebuffs()`: conteggio stack Sunder Armor (1-5), Demo Shout e Thunder Clap.
- `_G.PWHUD_GetTargetBuffs()`: rilevamento Enrage, Frenzy, Berserk e Bloodlust sul boss.
- `_G.PWHUD_GetKickInfo()`: analisi del cast nemico con `notInterruptible`, postura (`GetShapeshiftForm()`), scudo equipaggiato e disponibilità di Shield Bash vs Pummel vs Stuns.
- `_G.PWHUD_GetEmergencyCD()`: algoritmo di raccomandazione del miglior cooldown di mitigazione disponibile quando la salute scende sotto il 35%.
- `_G.PWHUD_GetTankStats()`: calcolo istantaneo di Difesa (cap 540), CTC, SBV, Armor DR%, Hit/Exp ed EHP.
