# Task & Milestone Tracking — Protection Warrior 3.3.5a Suite

## Milestone 1: Architettura Compiler & Struttura Core
- [x] Inizializzazione repository Git `protection-warrior-335a-am`.
- [x] Creazione pacchetto `builder/core/`:
  - [x] `constants.py`: Colori, texture, load conditions classe Warrior.
  - [x] `serializer.py`: Encoder puro Python AceSerializer-3.0.
  - [x] `deflate.py`: Compressione Raw Deflate (RFC 1951) e charset LibDeflate.
  - [x] `encoder.py`: Generatore della stringa standard `!WA:1!`.
  - [x] `helpers.py`: `make_subtext` (dual-key), `make_subbackground`, `make_glow_action`.
- [x] Definizione dell'albero master in `builder/tree.py`:
  - [x] Root group `Class Warrior (Protection)` con UID `PWHUD_ROOT`.
  - [x] Registrazione controllata dei 20 nodi in `controlledChildren`.
  - [x] Inizializzazione globale con bootstrap isolato `_G.PWHUD_InitCore()`.

---

## Milestone 2: Implementazione Componenti HUD Specializzati
- [x] **01 - Procs warTank** (`builder/components/procs.py`):
  - [x] Sword & Board (Buff 50227).
  - [x] Revenge Ready.
  - [x] Shield Block Active (Buff 2565).
  - [x] Victory Rush.
  - [x] Emergency Low HP Advisor (< 35% HP con priorità cooldown).
  - [x] Boss Enrage Alert.
  - [x] Tank Buster Debuff Alert (Soul Reaper, Impale, Gastric Bloat, Fusion Punch).
- [x] **02 - Battle Shout**, **03 - Commanding Shout**, **04 - Defensive Stance** (`builder/components/buffs.py`):
  - [x] Logica zero-clutter e soppressione con Blessing of Might e Blood Pact.
  - [x] Allarme rosso fuori postura difensiva in combattimento.
- [x] **05 - 13 Riga Utility Adattiva** (`builder/components/utility.py`):
  - [x] Slot 13 & 14 (Trinket 1 e Trinket 2).
  - [x] Slot 11/12 (Ashen Band of Endless Courage).
  - [x] Slot 15 (Mantello Ingegneria/Ricamo).
  - [x] Bonus Tier 10 Protection.
  - [x] Incantesimi arma (Blade Ward, Blood Draining, Mongoose).
  - [x] Slot 10 (Guanti Ingegneria).
  - [x] Shield Wall (Spell 871 con timer e `-60%`).
  - [x] Last Stand (Spell 12975 con timer e `+30%`).
  - [x] Slot 8 (Nitro Boosts o Enraged Regeneration).
- [x] **14 - Rage Bar** & **16 - Castbar con Kick Advisor** (`builder/components/bars.py`):
  - [x] Rage bar 278x14px con transizione cromatica a >= 45 Rage.
  - [x] Castbar target 278x20px con rilevamento lanci interrompibili vs immuni.
  - [x] Raccomandazione dinamica Shield Bash / Pummel / Stuns.
- [x] **15 - Rotational Bar** (`builder/components/rotational.py`):
  - [x] Main-Hand Swing Timer a 278x7px con glow oro per Heroic Strike / Cleave accodati.
- [x] **17 - Alerts warTank** (`builder/components/alerts.py`):
  - [x] Avvisi testuali e sonori per emergenze e chiamate di interruzione.
- [x] **18 - Stats Panel warTank** (`builder/components/stats.py`):
  - [x] Pannello 88x60px a 5 righe (Armor, Def 540 Cap, Block Value, Parry/Dodge, HP).
- [x] **19 - Sunder Armor Tracker** (`builder/components/sunder.py`):
  - [x] Monitoraggio cariche 1-5 e durata di Sunder Armor / Expose Armor.

---

## Milestone 3: Risoluzione Bug Import & Compatibilità
- [x] Diagnosi dell'errore "si è bloccato l'import".
- [x] Conversione delle chiavi dei trigger da stringa `"1"` a intero `1` in tutta la barra utility.
- [x] Aggiunta di `"activeTriggerMode": -10` nei trigger.
- [x] Aggiunta di `{"type": "subbackground"}` in `subRegions` di tutte le auras ad icona.
- [x] Verifica del superamento del test di integrità.

---

## Milestone 4: Test Suite & Documentazione Completa
- [x] Suite di test automatizzati paralleli multi-core:
  - [x] `test_components_integrity.py` (PASS)
  - [x] `test_tree_layout.py` (PASS)
  - [x] `test_stats_panel.py` (PASS)
  - [x] `test_lua.py` (PASS)
  - [x] `test_defensives.py` (PASS)
  - [x] `test_interrupts.py` (PASS)
  - [x] `test_string_sync.py` (PASS)
  - [x] `test_danger_alerts.py` (PASS)
- [x] Simulatore web interattivo in `docs/index.html`.
- [x] Documentazione completa allineata a Fury e Fire:
  - [x] `docs/ARCHITECTURE.md`
  - [x] `docs/DESIGN.md`
  - [x] `docs/PRD.md`
  - [x] `docs/RULES.md`
  - [x] `docs/DECISIONS.md`
  - [x] `docs/MEMORY.md`
  - [x] `docs/TASKS.md`
  - [x] `docs/TEST_PLAN.md`
  - [x] `docs/WORKFLOW.md`

---

## Milestone 5: Load Condition Specifica [Devastate] & Controllo Postura Difensiva in Combat
- [x] **Task 1: Load Condition Specifica per Warrior Tank**:
  - [x] Calcolo matematico dell'indice lineare di WeakAuras 3.3.5a: Tab 3 (Protection), Posizione 23 (Tier 8, Colonna 1) $\rightarrow$ `(3 - 1) * 40 + 23 = 103`.
  - [x] Aggiornamento della costante `PROT_WARRIOR_LOAD` in `builder/core/constants.py` con `"use_talent": True` e `"talent": {"single": 103, "multi": {103: True}}`.
  - [x] Propagazione automatica della condizione su Root `Class Warrior (Protection)` e su tutte le 43 aure figlie.
  - [x] Aggiornamento test di verifica in `tests/test_tree_layout.py`.
- [x] **Task 2: Rilevamento e Notifica Postura Errata (Out-of-Stance) in Combattimento**:
  - [x] Livello 1: Riconfigurazione dell'indicatore `Defensive Stance - Warning` (UID `PWHUD_STANCE_WARN`) nel gruppo `04 - Defensive Stance` con Pixel Glow rosso e label `STANCE` attivo su `UnitAffectingCombat("player") and (GetShapeshiftForm() ~= 2)`.
  - [x] Livello 2: Creazione dell'allarme centrale ad alta priorità `Alert - Wrong Stance` (UID `PWHUD_ALERT_WRONG_STANCE`) in `17 - Alerts warTank` a $y = 64$ con avviso `|cFFFF1010>> DEFENSIVE STANCE REQUIRED! <<|r` e riproduzione sonora `RaidWarning.ogg`.
  - [x] Trigger event-driven immediato basato su `PLAYER_REGEN_DISABLED`, `PLAYER_REGEN_ENABLED`, `UPDATE_SHAPESHIFT_FORM`, `PLAYER_ENTERING_WORLD`.
  - [x] Aggiornamento test di verifica in `tests/test_danger_alerts.py`.
  - [x] Rigenerazione stringa finale `IMPORT_STRING_v5.21.8.txt` e verifica superamento 8/8 test paralleli.
- [x] **Task 3: Refactoring Pannello Statistiche Difensive Stile Fury Warrior & Motore Buff/Debuff WotLK**:
  - [x] Adozione dello stile grafico uniforme a Fury Warrior: etichette bianche `|cFFFFFFFFLabel:|r <ValoreColorato>`.
  - [x] Integrazione motore di calcolo non-stacking per debuff boss sul target: *Insect Swarm* (Druido) vs *Scorpid Sting* (Hunter) per un bonus Miss massimo di +3.0%.
  - [x] Gestione contestuale del livello bersaglio (Boss Raid Lv.83 = 540 Def, Eroica Lv.82 = 535 Def).
  - [x] Calcolo accurato Armor Physical DR% con costante $K = 16635$ e rilevamento automatico di *Inspiration* (+25%), *Stoneskin/Devotion* e debuff *Sunder/Acid/Faerie Fire/Melt Armor*.
  - [x] Calcolo CTC ($\text{Dodge} + \text{Parry} + \text{Block} + \text{BossMiss}$) con soglia Unhittable 102.4% e Block % con Shield Block Value (SBV).
  - [x] Rilevamento aura di gruppo Draenei *Heroic Presence* (+1.0% Hit) e Soft Cap 26 / Hard Cap 56 di Competenza (Expertise).
  - [x] Aggiornamento test di verifica in `tests/test_stats_panel.py`.
  - [x] Sincronizzazione in `docs/index.html` e rigenerazione `IMPORT_STRING_v5.21.8.txt`.
- [x] **Task 4: Allineamento 1:1 Icona Stance al Modello Fury Warrior (Nascosta in Stance Corretta, Attiva solo Out-of-Stance in Combat)**:
  - [x] Rimozione di `Defensive Stance - Active` in `builder/components/buffs.py`: l'icona non deve essere mostrata quando il tank si trova nella postura difensiva corretta (`GetShapeshiftForm() == 2`).
  - [x] Riconfigurazione del gruppo `04 - Defensive Stance` con unico figlio `04 - Defensive Stance - OutOfStance` (UID `PWHUD_STANCE_WARN`) di dimensione 28x28px a $x = -158, y = 0$.
  - [x] Trigger condizionale reattivo identico a Fury Warrior: visibile esclusivamente in combattimento quando fuori postura difensiva (`GetShapeshiftForm() ~= 2 and UnitAffectingCombat("player")`).
  - [x] Ridimensionamento delle icone Shouts (`02 - Battle Shout`, `03 - Commanding Shout`) a 28x28px in `builder/components/buffs.py` per garantire perfetta coerenza geometrica con Fury Warrior sopra lo Stats Panel (88px).
  - [x] Aggiornamento test di regressione (`tests/test_danger_alerts.py`, `tests/test_components_integrity.py`).
  - [x] Rigenerazione stringa WeakAuras `IMPORT_STRING_v5.21.8.txt` e verifica superamento suite 8/8 test paralleli.
  - [x] Aggiornamento simulatore web `docs/index.html`: icona stance nascosta di default e nel preset standard; visibile con bordo rosso pulsante solo nel preset `stance_fail`.
