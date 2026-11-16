# System Architecture — Class Warrior (Protection) WeakAuras Suite

## 1. Panoramica Architetturale

La suite **Class Warrior (Protection)** per World of Warcraft 3.3.5a (*Wrath of the Lich King - Build 12340*) è progettata secondo un'architettura **Compiler-Driven Component-Based**: l'intero albero dati gerarchico di WeakAuras non viene manipolato manualmente in Lua né esportato empiricamente in gioco, ma viene modellato e generato programmaticamente da una pipeline Python dedicata (`builder/`).

Il compilatore serializza l'albero nel formato binario di **AceSerializer-3.0**, comprime il payload con l'algoritmo **Deflate** (RFC 1951, compressione raw senza header zlib) e codifica il risultato tramite il charset di stampa a 64 caratteri sicuri di **LibDeflate**, producendo la stringa standard `!WA:1!...` pronta per l'importazione diretta con `Ctrl+V` in gioco.

```mermaid
flowchart TD
    subgraph Python Compiler
        A[builder/components/*.py] --> B[builder/tree.py: build_wa_tree]
        C[builder/core/constants.py] --> B
        B --> D[builder/core/serializer.py: AceSerializer-3.0]
        D --> E[builder/core/deflate.py: Raw Deflate RFC1951]
        E --> F[builder/core/encoder.py: LibDeflate Print Encoding]
        F --> G[IMPORT_STRING_v5.21.8.txt]
    end

    subgraph World of Warcraft 3.3.5a
        G -->|Ctrl+V into /wa| H[WeakAuras Addon]
        H --> I[Class Warrior Protection HUD]
    end

    subgraph Web Ecosystem
        G --> J[scripts/sync_docs.py]
        J --> K[docs/index.html: Web Showcase Simulator]
    end
```

---

## 2. Struttura del Package Python `builder/`

La cartella sorgente `builder/` è articolata in moduli indipendenti e riutilizzabili:

```text
builder/
├── core/                        # Motore di serializzazione, codifica e costanti
│   ├── constants.py             # Condizioni di caricamento, palette RGB, metriche grafiche e spell IDs
│   ├── serializer.py            # Implementazione pura Python di AceSerializer-3.0 (^1...^^)
│   ├── deflate.py               # Compressione Deflate senza header zlib e tabella caratteri LibDeflate
│   ├── encoder.py               # Assemblatore finale stringa !WA:1!
│   ├── helpers.py               # Funzioni ausiliarie per subtext, subbackground e glow
│   └── __init__.py              # Export pubblico del modulo core
│
├── components/                  # Moduli verticali dei 20 componenti HUD
│   ├── procs.py                 # 01 - Procs warTank (Dynamic Group: Sword & Board, Revenge Ready warTank, Shield Block, Emergency HP, Tank Buster)
│   ├── buffs.py                 # 02 - Battle Shout, 03 - Commanding Shout, 04b - Vigilance (Focus Magic model), 04 - Defensive Stance
│   ├── utility.py               # 05-13 - Riga Utility Adattiva (Trinket 1/2, Ring, Cloak Proc-Only, Tier Set Proc-Only, Enchants Proc-Only, Gloves, Shield Wall warTank, Last Stand warTank, Boots)
│   ├── bars.py                  # 14 - Rage Bar warTank & 16 - Castbar warTank (con Kick Advisor integrato)
│   ├── rotational.py            # 15 - Rotational Bar warTank (Indicatore statico di accodamento 278x7px per HS/Cleave con Pixel Glow)
│   ├── alerts.py                # 17 - Alerts warTank (Gruppo avvisi sonori e visivi per emergenze difensive e interrupt)
│   ├── stats.py                 # 18 - Stats Panel warTank (Pannello 126x60px difensivo: Armor, Def, Block, Parry/Dodge, HP)
│   ├── sunder.py                # 19 - Sunder Armor Tracker warTank (32x32px a x=160, y=-7 con supporto Expose Armor & Acid Spit)
│   └── __init__.py              # Export aggregato dei builder dei componenti
│
└── tree.py                      # Assemblatore dell'albero gerarchico master (Root Group + 20 children controllati)
```

---

## 3. Specifiche del Protocollo di Serializzazione & Compressione

WeakAuras per World of Warcraft 3.3.5a impiega un protocollo standardizzato a tre livelli per l'interscambio delle tabelle dati:

1. **AceSerializer-3.0**:
   - Marcatore di apertura: `^1`
   - Marcatore di chiusura: `^^`
   - Tipi supportati e codifica binaria:
     - Tabelle associative / dizionari: `^T...^t`
     - Numeri interi: `^N<valore>` (es. `^N1` per array index 1, `^N90` per internalVersion)
     - Stringhe: `^S<valore>` con sequenze di escape per caratteri di controllo (es. `~z` per byte 30, `~}` per `^`, `~|` per `~`).
     - Booleani: `^B` per `true`, `^b` per `false`.
     - Valori nulli: `^Z`.
   - **Regola Vincolante per i Trigger**: Le mappe dei trigger WeakAuras **devono** avere chiavi numeriche intere (`1: { ... }` $\rightarrow$ `^N1`) e **non** stringhe (`"1": { ... }` $\rightarrow$ `^S1`). Le chiavi stringa impediscono la scansione con `ipairs` e provocano il blocco totale del deserializzatore durante l'importazione. Inoltre ogni mappa trigger deve contenere `"activeTriggerMode": -10`.

2. **Compressione RFC 1951 (Raw Deflate)**:
   - Stream compresso generato con `zlib.compressobj(level=9, method=zlib.DEFLATED, wbits=-15)` (finestra raw a 15 bit senza wrapper o checksum zlib/gzip).

3. **LibDeflate Print Encoding**:
   - Tabella di conversione a 64 caratteri sicuri per la chat e le editbox di WoW (`a-z`, `A-Z`, `0-9`, `(`, `)`).
   - Prefisso di compatibilità globale: `!WA:1!`.

---

## 4. Griglia Coordinate a Schermo e Layout HUD

L'HUD è ancorato al centro dello schermo (`anchorPoint: "CENTER"`, `selfPoint: "CENTER"`) con un offset base verticale di `yOffset = -190`, posizionandosi esattamente sotto il modello del personaggio per garantire piena visibilità delle pozze e dei debuff a terra.

Le tre barre orizzontali condividono la larghezza calibrata di **278 px**:

```text
                  [ 17 - Alerts warTank (y = +78) ]
           [ 01 - Procs warTank (Dynamic Group, y = +52) ]

================== [ 16 - Castbar warTank (278x20px, y = +8) ] ==================
---------------- [ 15 - Rotational Bar (Swing Timer 278x7px, y = -7) ] ----------  [ 19 - Sunder ]
==================== [ 14 - Rage Bar (278x14px, y = -20) ] =====================

[ Shouts & Stance ]                                            [ Utility Row ]
(x = -222, -190, -158, y = 0)                                  (y = -45, 10 icone)
[ 18 - Stats Panel ]
(x = -190, y = -45, 88x60px)
```

| ID Modulo | Nome Componente | Dimensioni | Coordinate (X, Y) | Comportamento e Funzionalità |
| :--- | :--- | :--- | :--- | :--- |
| **Root** | `Class Warrior (Protection)` | Scale 1.2 | X: 0, Y: -190 | Gruppo master contenitore con icona Defensive Stance e bootstrap core |
| **01** | `01 - Procs warTank` | 34x34 px (icone) | X: 0, Y: +52 | Dynamic group orizzontale centrato a 4 icone: Sword & Board, Revenge Ready warTank (finestra 5s con refresh dinamico su Schivata/Parata/Blocco e LibCustomGlow-1.0), Low HP Alert, Tank Buster (Database completo WotLK 3.3.5a: Soul Reaper, Phase Punch, Rune of Blood, Impale, ecc.) |
| **02** | `02 - Battle Shout warTank` | 30x30 px | X: -264, Y: 0 | Monitoraggio buff; soppresso intelligentemente da Blessing of Might del Paladino |
| **03** | `03 - Commanding Shout warTank`| 30x30 px | X: -232, Y: 0 | Buff salute; soppresso intelligentemente da Blood Pact dell'Imp del Warlock |
| **04b** | `04b - Vigilance warTank` | 30x30 px | X: -200, Y: 0 | Allerta Vigilanza mancante su alleato (OFF stile Focus Magic) e timer scadenza (<= 60s) |
| **04** | `04 - Defensive Stance warTank`| 30x30 px | X: -168, Y: 0 | Allerta visiva immediata e glow rosso se in combat fuori dalla Postura Difensiva |
| **05-13**| Utility Row (11 Icone) | 28x28 px | Y: -45, X centrato | Trinket 1/2, Ring, Cloak (Proc-Only: Swordguard), Tier 10 (Bloodrage CD), Enchants (Proc-Only), Gloves, Shield Block warTank (Durata 10s & CD 30s/60s), Shield Wall warTank (-60%), Last Stand warTank (+30%), Boots/Enraged Regen |
| **14** | `14 - Rage Bar warTank` | 278x14 px | X: 0, Y: -20 | Barra risorsa con cambio colore a soglia Heroic Strike/Cleave (>= 45 Rage) |
| **15** | `15 - Rotational Bar warTank` | 278x7 px | X: 0, Y: -7 | Indicatore statico di accodamento rotazionale a 278x7px senza scorrimento e senza timer numerico; Pixel Glow LibCustomGlow-1.0 oro per Heroic Strike e verde smeraldo per Cleave |
| **16** | `16 - Castbar warTank` | 278x20 px | X: 0, Y: +8 | Barra di lancio target con **Kick Advisor integrato**: rileva lanci interrompibili vs immuni e suggerisce Shield Bash, Pummel o Stun in base a stance e scudo |
| **17** | `17 - Alerts warTank` | Testo 20pt | X: 0, Y: +78 | Avvisi sonori e testuali per emergenza difensiva, debuff letali e richiesta interrupt |
| **18** | `18 - Stats Panel warTank` | 126x60 px | X: -216, Y: -49 | Pannello difensivo compatto a 5 righe stile Fury Warrior (Def 540 Cap, Armor DR%, CTC 102.4%, Block % & SBV, Hit & Exp) |
| **19** | `19 - Sunder Armor Tracker warTank` | 32x32 px | X: +160, Y: -7 | Monitoraggio cariche (1-5) e durata Sunder Armor (Warrior), Expose Armor (Rogue) o Acid Spit (Hunter); nome univoco anti-conflitto |

---

## 5. Caching Lua e Ottimizzazione Prestazionale

In combattimento raid ad alta intensità (es. Lich King 25HC), il motore Lua di World of Warcraft 3.3.5a è suscettibile a picchi di garbage collection. Per mantenere il carico della CPU inferiore allo **0.1%**, la suite implementa due cache globali isolate:

1. **`_G.PWHUD_BuffCache`**:
   - Cache unificata dei buff del giocatore indicizzati per `spellId` e `name`.
   - Aggiornata al massimo una volta per frame (`GetTime() == c.time`).
   - Rileva istantaneamente sovrapposizioni di raid (`hasBoM`, `hasBloodPact`).

2. **`_G.PWHUD_DebuffCache`**:
   - Cache dei debuff target/player per monitorare i colpi letali dei boss (Soul Reaper, Impale, Gastric Bloat, Fusion Punch) senza eseguire scansioni ripetute dell'API `UnitDebuff`.

3. **Motore di Calcolo e Glossario Sigle Statistiche Tank (`_G.PWHUD_LastStatsText`)**:
   - Caching a 10 Hz (0.1s) per evitare ricalcoli costosi su ogni frame.
   - **`DEF` (Defense Skill)**: Cap **540** per immunità critici boss Lv.83 (-5.6% crit subito), **535** in Eroiche Lv.82.
   - **`ARM` (Armor & Physical DR% Contestuale)**: Armatura effettiva dinamica: calcolo a pari livello (Lv.80 con costante Blizzard $K = 15232.5 \implies 62.4\%$, esattamente conforme al tooltip della scheda PG in-game) in assenza di target; scalatura automatica in tempo reale a $K = 16635 \implies 60.3\%$ su Raid Boss / Skull Lv.83 (mitigazione fisica effettiva in raid). Hard Cap 75.0%.
   - **`CTC` (Combat Table Coverage)**: Copertura tabella colpi: $\text{Dodge} + \text{Parry} + \text{Block} + \text{BossMiss}$. A $\ge \mathbf{102.4\%}$ il tank è *Unhittable*. Include debuff non-stacking (*Insect Swarm* / *Scorpid Sting* max +3%).
   - **`Block` & `SBV` (Shield Block Value)**: Probabilità di blocco e assorbimento netto; scala danno e minaccia di *Shield Slam*.
   - **`Hit` & `Exp` (Expertise)**: Melee Hit (Cap 8% con *Heroic Presence* Draenei +1%), Soft Cap 26 (0% dodge del boss) ed Hard Cap 56 (0% parry del boss per azzerare *Parry-Haste*).

---

## 6. Condizioni di Caricamento (Load Conditions) — Spec Protection Only

Per garantire che la suite si attivi **esclusivamente** quando il personaggio è specializzato Guerriero Protezione (Protection Warrior) con il talento **[Devastate]** appreso, le condizioni di caricamento sono definite a livello di master group e propagate uniformemente a tutte le 43 aure figlie:

```python
PROT_WARRIOR_LOAD = {
    "use_class": True,
    "class": {"single": "WARRIOR", "multi": {"WARRIOR": True}},
    "use_talent": True,
    "talent": {"single": 103, "multi": {103: True}},
    "use_vehicle": False,
}
```

### Calcolo Matematico dell'Indice Talento in WeakAuras 3.3.5a:
In WeakAuras per la build 12340, `WeakAuras.CheckTalentByIndex(index)` mappa l'albero tramite:
$$\text{tab} = \left\lceil \frac{\text{index}}{40} \right\rceil, \quad \text{num\_talent} = ((\text{index} - 1) \bmod 40) + 1$$
- **Tab 1**: Arms (indici 1–31)
- **Tab 2**: Fury (indici 41–67, con Rampage = 64)
- **Tab 3**: Protection (indici 81–107)
All'interno del Tab 3 (Protection), **Devastate** (Spell ID: `20243`) si trova al Tier 8, Colonna 1, occupando l'ordinale **23**. L'indice WeakAuras risulta quindi:
$$\text{Index} = (3 - 1) \times 40 + 23 = \mathbf{103}$$

---

## 7. Rilevamento e Alerting Postura Errata (Out-of-Stance) in Combattimento

La gestione della postura è critica per la sopravvivenza del Protection Warrior in raid e dungeon. Un guerriero che affronta il combattimento fuori da *Defensive Stance* perde il 10% di mitigazione passiva, il bonus di Threat moltiplicato e l'accesso ad abilità salvavita (*Shield Block*, *Shield Wall*, *Revenge*).

L'architettura adotta un **doppio livello di allerta reattiva**:
1. **Indicatore Locale su Slot Postura (`04 - Defensive Stance - OutOfStance`, UID `PWHUD_STANCE_WARN`)**:
   - Posizionato a $x = -158, y = 0$ (dimensione 28x28px, allineato alle shout e al pannello statistiche).
   - In postura difensiva corretta (`GetShapeshiftForm() == 2`) l'icona è **completamente invisibile** (allineamento 1:1 al modello Fury Warrior: zero clutter a schermo).
   - Dotato di colore rosso allerta e label visiva `STANCE`.
   - Si attiva istantaneamente in combattimento quando `UnitAffectingCombat("player") and (GetShapeshiftForm() ~= 2)`.
2. **Allarme Centrale ad Alta Priorità (`Alert - Wrong Stance`, UID `PWHUD_ALERT_WRONG_STANCE`)**:
   - Posizionato nel gruppo `17 - Alerts warTank` a $y = +64$ (sopra il castbar, centro visivo del giocatore).
   - Testo a 20pt con contorno: `|cFFFF1010>> DEFENSIVE STANCE REQUIRED! <<|r`.
   - Audio di emergenza `RaidWarning.ogg` attivato all'ingresso in combat o al cambio accidentale di stance.
   - Entrambe le aure utilizzano trigger event-driven basati su `PLAYER_REGEN_DISABLED`, `PLAYER_REGEN_ENABLED`, `UPDATE_SHAPESHIFT_FORM`, azzerando il consumo CPU a zero durante la normale postura difensiva.
