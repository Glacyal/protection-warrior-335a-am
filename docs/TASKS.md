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
- [x] Documentazione tecnica e architetturale completa per il War Tank:
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
- [x] **Task 3: Refactoring Pannello Statistiche Difensive del War Tank & Motore Buff/Debuff WotLK**:
  - [x] Adozione dello stile grafico ad alto contrasto per il War Tank: etichette bianche `|cFFFFFFFFLabel:|r <ValoreColorato>`.
  - [x] Integrazione motore di calcolo non-stacking per debuff boss sul target: *Insect Swarm* (Druido) vs *Scorpid Sting* (Hunter) per un bonus Miss massimo di +3.0%.
  - [x] Gestione contestuale del livello bersaglio (Boss Raid Lv.83 = 540 Def, Eroica Lv.82 = 535 Def).
  - [x] Calcolo accurato Armor Physical DR% con costante $K = 16635$ e rilevamento automatico di *Inspiration* (+25%), *Stoneskin/Devotion* e debuff *Sunder/Acid/Faerie Fire/Melt Armor*.
  - [x] Calcolo CTC ($\text{Dodge} + \text{Parry} + \text{Block} + \text{BossMiss}$) con soglia Unhittable 102.4% e Block % con Shield Block Value (SBV).
  - [x] Rilevamento aura di gruppo Draenei *Heroic Presence* (+1.0% Hit) e Soft Cap 26 / Hard Cap 56 di Competenza (Expertise).
  - [x] Aggiornamento test di verifica in `tests/test_stats_panel.py`.
  - [x] Sincronizzazione in `docs/index.html` e rigenerazione `IMPORT_STRING_v5.21.8.txt`.
- [x] **Task 4: Riconfigurazione Icona Stance per il War Tank (Nascosta in Stance Corretta, Attiva solo Out-of-Stance in Combat)**:
  - [x] Rimozione di `Defensive Stance - Active` in `builder/components/buffs.py`: l'icona non deve essere mostrata quando il tank si trova nella postura difensiva corretta (`GetShapeshiftForm() == 2`).
  - [x] Riconfigurazione del gruppo `04 - Defensive Stance` con unico figlio `04 - Defensive Stance - OutOfStance` (UID `PWHUD_STANCE_WARN`) di dimensione 28x28px a $x = -158, y = 0$.
  - [x] Trigger condizionale reattivo: visibile esclusivamente in combattimento quando fuori postura difensiva (`GetShapeshiftForm() ~= 2 and UnitAffectingCombat("player")`).
  - [x] Ridimensionamento delle icone Shouts (`02 - Battle Shout`, `03 - Commanding Shout`) a 28x28px in `builder/components/buffs.py` per garantire perfetta coerenza geometrica del War Tank sopra lo Stats Panel (88px).
  - [x] Aggiornamento test di regressione (`tests/test_danger_alerts.py`, `tests/test_components_integrity.py`).
  - [x] Rigenerazione stringa WeakAuras `IMPORT_STRING_v5.21.8.txt` e verifica superamento suite 8/8 test paralleli.
  - [x] Aggiornamento simulatore web `docs/index.html`: icona stance nascosta di default e nel preset standard; visibile con bordo rosso pulsante solo nel preset `stance_fail`.
- [x] **Task 5: Calcolo Dinamico Armor Physical DR% Contestuale al Bersaglio (Opzione 1: Default Lv.80 Scheda PG, Lv.83 su Raid Boss/Skull)**:
  - [x] Aggiornamento logica Lua in `builder/components/stats.py`: se non esiste un target ostile attaccabile, il livello di riferimento predefinito diventa `UnitLevel("player") or 80` anziché 83 fisso.
  - [x] Allineamento matematico a $K_{80} = 15232.5$: in assenza di target (o contro bersagli Lv.80), la percentuale calcolata per 25.253 di armatura è $62.4\%$, esattamente corrispondente al $62.38\%$ visualizzato nel tooltip in-game della scheda del personaggio.
  - [x] Rilevamento dinamico Raid Boss / Skull ($lvl == -1$ o $lvl \ge 83$): adozione in tempo reale di $K_{83} = 16635$ per mostrare la mitigazione fisica effettiva sul boss ($60.3\%$).
  - [x] Aggiornamento test suite in `tests/test_stats_panel.py` con verifica formale sia di $K_{80} = 15232.5$ che di $K_{83} = 16635$.
  - [x] Rigenerazione stringa `IMPORT_STRING_v5.21.8.txt` e sincronizzazione in `docs/index.html`.
  - [x] Aggiornamento documentazione tecnica (`docs/ARCHITECTURE.md`, `docs/DESIGN.md`, `README.md`, `HANDOFF.md`).
- [x] **Task 6: Standard Bilingue Documentazione (Inglese Primario, Italiano Secondario) & Traduzione Integrale HTML**:
  - [x] Creazione di `README.md` (Inglese primario) e `README_IT.md` (Italiano secondario) con struttura e contenuti speculari 1:1 e link incrociati di testata.
  - [x] Creazione di `HANDOFF.md` (Inglese primario) e `HANDOFF_IT.md` (Italiano secondario) con identica architettura tecnica e glossario bilingue.
  - [x] Traduzione integrale in lingua inglese del simulatore web `docs/index.html` (interfaccia, controlli, preset di test, allarmi, slider e schede documentali/glossario).
  - [x] Istituzione della regola permanente non negoziabile in `docs/RULES.md` e memoria tecnica in `docs/MEMORY.md`.
- [x] **Task 7: Allineamento Componente 15 - Rotational Bar (Static Queue Indicator Senza Scorrimento e Senza Timer Rimanente, 278x7px)**:
  - [x] Riconfigurazione di `15 - Rotational Bar` in `builder/components/rotational.py`: la barra occupa l'intero spazio assegnato (278x7px a $y = -7$) senza animazione di scorrimento/swipe e senza testo del tempo rimanente (`%c` rimosso/invisibile).
  - [x] Implementazione del meccanismo di Queue Indicator per Heroic Strike e Cleave sul War Tank:
    - Rilevamento in tempo reale dell'accodamento di *Heroic Strike* (`47450`) o *Cleave* (`47520`) tramite `IsCurrentSpell()`.
    - Retroilluminazione additiva con blend mode `ADD` e Pixel Glow via `LibCustomGlow-1.0`: Oro (`1.0, 0.84, 0.0`) per Heroic Strike, Verde Smeraldo (`0.1, 0.95, 0.2`) per Cleave.
    - Spegnimento del glow e ripristino della barra base quando nessuna abilità è accodata.
  - [x] Aggiornamento simulatore web in `docs/index.html`: barra statica solida 278x7px, eliminazione dello scorrimento e del testo countdown dei secondi, aggiunta di controlli interattivi/toggle per simulare Heroic Strike Queued (Glow Oro) e Cleave Queued (Glow Verde).
  - [x] Rigenerazione stringa WeakAuras `IMPORT_STRING_v5.21.8.txt` e sincronizzazione automatica in `docs/index.html`.
  - [x] Aggiornamento sincronizzato di tutti i documenti bilingue: `README.md` & `README_IT.md`, `HANDOFF.md` & `HANDOFF_IT.md`, `docs/ARCHITECTURE.md`, `docs/DESIGN.md`.
  - [x] Esecuzione e superamento della suite di test (8/8 test paralleli).
  - [x] Commit Git con messaggio descrittivo.
- [x] **Task 8: Standardizzazione di 19 - Sunder Armor Tracker warTank (Prevenzione Collisioni Nomi & Ottimizzazione Funzionale War Tank)**:
  - [x] Ridenominazione univoca ID da `19 - Sunder Armor Tracker` a `19 - Sunder Armor Tracker warTank` in `builder/components/sunder.py` e `builder/tree.py` per prevenire sovrapposizioni e suffissi automatici ` 2` nell'importazione WeakAuras accanto ad altre configurazioni presenti nell'addon.
  - [x] Correzione typo storico sullo spell ID di Sunder Armor Rank 6 (`47467`, precedentemente `47437`) e supporto completo a tutti i rank di *Sunder Armor* (Warrior all-specs), *Expose Armor* (Rogue) e *Acid Spit* (Hunter Worm).
  - [x] Ottimizzazione del layout e gestione eventi per il War Tank:
    - Subtext `%c1` in basso (`INNER_BOTTOM`, font size 10) per timer di scadenza numerico o `OFF` in rosso in combattimento.
    - Subtext `%c2` in alto (`INNER_TOP`, font size 12, y=-1) per stack count (`x5` in verde, `x1`-`x4` in bianco, `EA` in ciano).
    - `customIcon` dinamica che commuta sull'icona di *Expose Armor* quando il debuff del ladro è attivo sul bersaglio.
    - Funzioni `customDuration`, `customStacks` e trigger reattivo `inCombat`.
  - [x] Aggiornamento test di regressione (`tests/test_tree_layout.py`, `tests/test_components_integrity.py`).
  - [x] Rigenerazione stringa WeakAuras `IMPORT_STRING_v5.21.8.txt` e sincronizzazione automatica in `docs/index.html`.
  - [x] Aggiornamento sincronizzato di tutti i documenti bilingue: `README.md` & `README_IT.md`, `HANDOFF.md` & `HANDOFF_IT.md`, `docs/ARCHITECTURE.md`, `docs/DESIGN.md`.
  - [x] Esecuzione e superamento della suite parallela multi-core (8/8 test).
  - [x] Commit Git con messaggio descrittivo.
- [x] **Task 9: Eliminazione Integrale Sovrapposizioni Nomi (Standardizzazione Suffisso warTank su tutte le Aure 01-19 e Figli)**:
  - [x] Standardizzazione globale dell'albero WeakAuras: applicazione del suffisso univoco `warTank` a tutti i nodi principali da 01 a 19 e ai relativi figli interni suscettibili di collisione multi-spec o multi-classe:
    - `02 - Battle Shout warTank` (e figli `Battle Shout - Active warTank`, `Battle Shout - OFF warTank`).
    - `03 - Commanding Shout warTank` (e figli `Commanding Shout - Active warTank`, `Commanding Shout - OFF warTank`).
    - `04 - Defensive Stance warTank` (e figlio `04 - Defensive Stance - OutOfStance warTank`).
    - `11 - Shield Wall warTank` & `12 - Last Stand warTank`.
    - `14 - Rage Bar warTank`.
    - `15 - Rotational Bar warTank` (e figli `Rotational Bar - Background warTank`, `Rotational Bar - Base Bar warTank`, `Rotational Bar - Queue Glow warTank`).
  - [x] Aggiornamento `builder/tree.py` e di tutti i moduli in `builder/components/`.
  - [x] Aggiornamento dei test di regressione (`tests/test_components_integrity.py`, `tests/test_tree_layout.py`, `tests/test_defensives.py`, `tests/test_danger_alerts.py`).
  - [x] Rigenerazione stringa WeakAuras `IMPORT_STRING_v5.21.8.txt` e sincronizzazione automatica in `docs/index.html`.
  - [x] Aggiornamento sincronizzato di tutti i documenti bilingue: `README.md` & `README_IT.md`, `HANDOFF.md` & `HANDOFF_IT.md`, `docs/ARCHITECTURE.md`, `docs/DESIGN.md`.
  - [x] Esecuzione e superamento della suite parallela multi-core (8/8 test).
  - [x] Commit Git con messaggio descrittivo.
- [x] **Task 10: Rimozione Completa di Victory Rush dal Pacchetto Tank (01 - Procs warTank)**:
  - [x] Rimozione dell'aura `Victory Rush warTank` da `builder/components/procs.py` e dalla lista `controlledChildren` del gruppo `01 - Procs warTank` (la riga procs passa da 7 a 6 icone dinamiche focalizzate sulla sopravvivenza del tank).
  - [x] Pulizia helper `_G.PWHUD_VRState` e `_G.PWHUD_CheckVictoryRush` in `builder/components/utility.py`.
  - [x] Rimozione dell'elemento `#procVR` dal simulatore web in `docs/index.html`.
  - [x] Rigenerazione stringa WeakAuras `IMPORT_STRING_v5.21.8.txt` e sincronizzazione automatica.
  - [x] Aggiornamento documentazione bilingue: `README.md` & `README_IT.md`, `HANDOFF.md` & `HANDOFF_IT.md`, `docs/ARCHITECTURE.md`.
  - [x] Esecuzione e superamento della suite parallela multi-core (8/8 test).
  - [x] Commit Git con messaggio descrittivo.
- [x] **Task 11: Fix e Perfezionamento di Revenge Ready (Timer Interno 5.0s, Refresh Dinamico Schivata/Parata/Blocco, Eliminazione Glitch Glow con LibCustomGlow-1.0 & Standardizzazione warTank)**:
  - [x] Ridenominazione e standardizzazione ID da `Revenge Ready` a `Revenge Ready warTank` (UID `PWHUD_PROC_REVENGE`) in `builder/components/procs.py`.
  - [x] Implementazione del motore event-driven `_G.PWHUD_Revenge` con listener `COMBAT_LOG_EVENT_UNFILTERED`:
    - Rilevamento in tempo reale di Schivata (`DODGE`), Parata (`PARRY`) o Blocco (`BLOCK` o `blocked > 0`) subiti dal giocatore con impostazione finestra `start = GetTime(), dur = 5.0`.
    - Meccanica di **Refresh Dinamico**: ogni nuova schivata/parata/blocco durante la disponibilità ricarica istantaneamente il timer a 5,0s.
    - Azzeramento immediato al lancio di Revenge (`SPELL_CAST_SUCCESS` per spell ID 57823, 6572, ecc.).
  - [x] Integrazione dello swipe circolare nativo (`customDuration` che ritorna `5.0, start + 5.0`) e visualizzazione del conto alla rovescia in secondi (`%p` a dimensione 10) con label `REV` centrata.
  - [x] Sostituzione definitiva del glow nativo difettoso (causa della linea gialla congelata) con **`LibCustomGlow-1.0` Pixel Glow arancione/ambra** (`0.95, 0.45, 0.10, 1.0`) e arresto garantito `LCG.PixelGlow_Stop` in `actions.finish`.
  - [x] Rigenerazione stringa WeakAuras `IMPORT_STRING_v5.21.8.txt` e sincronizzazione simulatore web `docs/index.html`.
  - [x] Aggiornamento sincronizzato della documentazione tecnica bilingue (`README.md` & `README_IT.md`, `HANDOFF.md` & `HANDOFF_IT.md`, `docs/ARCHITECTURE.md`, `docs/DESIGN.md`).
  - [x] Esecuzione e superamento di tutti gli 8 test paralleli multi-core.
  - [x] Commit Git con messaggio descrittivo.
- [x] **Task 12: Filtraggio Intelligente di 09 - Enchants warTank (Visibile Solo con Incanti Arma Proccabili, Soppressione Totale Incanti Statici)**:
  - [x] Riconfigurazione dell'engine di rilevamento `_G.PWHUD_CheckEnchantsEquipped` in `builder/components/utility.py`:
    - Verifica dell'incanto presente sull'arma principale (Slot 16) tramite ID esatto contro il database incanti con proc `_G.PWHUD_WeaponEnchantDB` (*Blade Ward*, *Blood Draining*, *Mongoose*, *Berserking*, *Executioner*, *Crusader*, *Lifeward*, *Black Magic*, ecc.).
    - Soppressione esplicita e immediata (`cache.hasEnchant = false`) per tutti gli incanti statici censiti in `_G.PWHUD_StaticWeaponEnchants` (*Titanguard* +30 Stamina, *Accuracy* +25 Hit/+25 Crit, *Titanium Weapon Chain* +28 Hit/-50% Disarm, *Superior Potency* +65 AP, *Exceptional Agility* +26 Agi, *Major Defense* +12 Def, ecc.) e in assenza di incanto (`enchantID == 0`).
    - Ispezione fallback dei buff proccati attivi sul giocatore e scansione del tooltip per keyword di proc sul testo verde dell'incanto (`chance on`, `probabilità`, `proc`, `blade ward`, `blood draining`, `mongoose`, ecc.).
    - Impostazione del fallback predefinito a `false` (invece di `true`), eliminando la comparsa non voluta dell'aura con incanti statici.
  - [x] Allineamento della barra utility dinamica `_G.PWHUD_UpdateUtilityRowPositions`: in presenza di incanti statici, `09 - Enchants warTank` non viene inserito nella lista `activeOrder`, ricentrando armoniosamente le restanti icone utility senza lasciare spazi vuoti.
  - [x] Icona dinamica `defIcon` in `_G.PWHUD_CheckEnchants` sincronizzata con la texture specifica dell'incanto proccabile equipaggiato.
  - [x] Rigenerazione stringa WeakAuras `IMPORT_STRING_v5.21.8.txt` e sincronizzazione simulatore web `docs/index.html`.
  - [x] Aggiornamento sincronizzato della documentazione tecnica bilingue (`README.md` & `README_IT.md`, `HANDOFF.md` & `HANDOFF_IT.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md`).
  - [x] Esecuzione e superamento di tutti gli 8 test paralleli multi-core.
  - [x] Commit Git con messaggio descrittivo.
- [x] **Task 13: Rimozione Completa di Boss Enrage Alert dal Gruppo Procs (01 - Procs warTank)**:
  - [x] Rimozione dell'aura `Boss Enrage Alert` (UID `PWHUD_PROC_BOSS_ENRAGE`) da `builder/components/procs.py` e dalla lista `controlledChildren` di `01 - Procs warTank` (la riga procs dinamica superiore gestisce ora 5 icone focalizzate sulla sopravvivenza del tank: Sword & Board, Revenge Ready warTank, Shield Block Active, Emergency Low HP Alert, Tank Buster Alert).
  - [x] Aggiornamento dei test di regressione in `tests/test_danger_alerts.py` verificando l'assenza permanente dell'aura e del relativo child.
  - [x] Rimozione dell'elemento `#procEnrage` dal simulatore web in `docs/index.html`.
  - [x] Rigenerazione stringa WeakAuras `IMPORT_STRING_v5.21.8.txt` e sincronizzazione simulatore web `docs/index.html`.
  - [x] Aggiornamento sincronizzato della documentazione tecnica bilingue (`README.md` & `README_IT.md`, `HANDOFF.md` & `HANDOFF_IT.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md`).
  - [x] Esecuzione e superamento di tutti gli 8 test paralleli multi-core.
  - [x] Commit Git con messaggio descrittivo.
- [x] **Task 14: Adattamento Perfetto di Stats Panel - Text warTank (144x68px) e Armonizzazione Componenti Sovrastanti (Shouts & Stance a 34x34px)**:
  - [x] Riconfigurazione geometrica di `18 - Stats Panel warTank` in `builder/components/stats.py`:
    - Espansione del background `Stats Panel - Background warTank` a **144x68px** (precedentemente 88x60px), dimensionato con precisione per racchiudere tutte le 5 righe di testo difensivo (`Def`, `Armor DR%`, `CTC`, `Block % (SBV)`, `Hit | Exp`) con 10px di margine orizzontale e 6px verticale, eliminando qualsiasi debordamento all'esterno del box scuro.
    - Riposizionamento del centro del pannello a **X: -216, Y: -53**, azzerando `xOffset` a 0 per centratura interna uniforme del testo `%c`.
  - [x] Armonizzazione e allineamento geometrico 1:1 delle 3 componenti sovrastanti in `builder/components/buffs.py`:
    - Dimensione icone standardizzata a **34x34px** (precedentemente 28x28px, coerente con le icone 34x34px dei procs):
      - `02 - Battle Shout warTank`: centro a **X: -271, Y: 0** (il bordo sinistro a -288 combacia perfettamente al pixel con il bordo sinistro dello stats panel).
      - `03 - Commanding Shout warTank`: centro a **X: -216, Y: 0** (il centro combacia perfettamente con l'asse centrale dello stats panel).
      - `04 - Defensive Stance warTank`: centro a **X: -161, Y: 0** (il bordo destro a -144 combacia perfettamente al pixel con il bordo destro dello stats panel).
    - Risoluzione dell'interferenza verticale: creato un margine pulito di 3px tra la base delle icone e delle etichette `OFF`/`STANCE` (Y: -17) e la cima del pannello statistiche (Y: -19), eliminando ogni sovrapposizione visiva.
  - [x] Aggiornamento dei test di regressione in `tests/test_tree_layout.py` con le nuove coordinate e dimensioni sincronizzate.
  - [x] Aggiornamento del simulatore web in `docs/index.html` (colonna sinistra allineata a 144px con icone `size-34` e box statistiche 144x68px).
  - [x] Rigenerazione stringa WeakAuras `IMPORT_STRING_v5.21.8.txt` e sincronizzazione simulatore web `docs/index.html`.
  - [x] Aggiornamento sincronizzato della documentazione tecnica bilingue (`README.md` & `README_IT.md`, `HANDOFF.md` & `HANDOFF_IT.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md`).
  - [x] Esecuzione e superamento di tutti gli 8 test paralleli multi-core.
  - [x] Commit Git con messaggio descrittivo.

- [x] **Task 15: Filtraggio Rigoroso di 08 - Tier Set warTank (Visibile Solo con Bonus Set con Proc Attivo: T10 4P / T8 4P, Soppressione Totale Bonus Statici) & Pulizia Bordo Revenge**:
  - [x] Riconfigurazione del motore di rilevamento Tier `_G.PWHUD_CheckTierSetEquipped` e `_G.PWHUD_CheckTierSet` in `builder/components/utility.py`:
    - Censimento dettagliato delle meccaniche di set Protection Warrior in WotLK 3.3.5a:
      - **T10 4P (*Blood Frenzy* / *Frenesia del Sangue*, Spell ID 70844)**: Proc attivo garantito dall'attivazione di Bloodrage (assorbimento danni pari al 20% della salute massima per 10s) -> **PROC ATTIVO / TRACKED**.
      - **T8 4P (Riduzione Danno Magico 20%, Spell ID 64938 / 2565)**: Proc attivo scatenato durante Blocco con Scudo (20% riduzione danno magico per 10s) -> **PROC ATTIVO / TRACKED**.
      - **T10 2P, T9 2P/4P, T8 2P, T7 2P/4P**: Bonus interamente passivi e statici (+20% danno Shield Slam/Devastate, -2s CD Taunt, -10s CD Shield Block, +10% crit Shield Slam, +3s durata Shield Wall). Nessun proc dinamico o buff da tracciare -> **SOPPRESSIONE TOTALE**.
    - `_G.PWHUD_CheckTierSetEquipped()` restituisce `true` solo se il giocatore ha equipaggiato un set con proc attivo (`t10 >= 4 or t8 >= 4`) o ha il buff del proc attivo (`Spell 70844`). In tutti gli altri casi restituisce `false`.
    - La riga utility dinamica `_G.PWHUD_UpdateUtilityRowPositions` esclude `08 - Tier Set warTank` da `activeOrder` quando `hasTier` è `false`, ricentrando armoniosamente le restanti icone senza spazi vuoti.
  - [x] Pulizia dell'artefatto grafico su `Revenge Ready warTank` in `builder/components/procs.py`:
    - Impostato `"cooldownEdge": False` (mantenendo `"cooldownSwipe": True`), eliminando la linea/ago verticale gialla a ore 12 sul bordo superiore dell'icona mostrata a riposo.
  - [x] Rigenerazione stringa WeakAuras `IMPORT_STRING_v5.21.8.txt` e sincronizzazione simulatore web `docs/index.html`.
  - [x] Aggiornamento sincronizzato della documentazione tecnica bilingue (`README.md` & `README_IT.md`, `HANDOFF.md` & `HANDOFF_IT.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md`).
  - [x] Esecuzione e superamento di tutti gli 8 test paralleli multi-core.
  - [x] Commit Git con messaggio descrittivo.

- [x] **Task 16: Filtraggio Rigoroso di 07 - Cloak warTank (Soppressione Totale Paracadute/Flexweave e Incanti Statici, Visibilità Esclusiva per Proc Attivi come Swordguard)**:
  - [x] Riconfigurazione dei filtri Mantello (Slot 15) in `builder/components/utility.py`:
    - **Soppressione Totale Paracadute (Ingegneria)**: Rimosso completamente il tracciamento del paracadute (*Flexweave Underlay*, incanto ID 3605, spell IDs 55002 e 54865, keyword "flexweave", "parachute", "flessibile", "paracadute"). L'uso del paracadute è un'utility di movimento/caduta e non deve occupare uno slot nella riga utility di combattimento del tank.
    - **Soppressione Totale Incanti Statici**: Tutti gli incanti statici da mantello (+22 Agilità, +16 Difesa, +225 Armatura, resistenze magiche) o mantelli senza incanto valutano rigorosamente `cache.isEquipped = false`.
    - **Tracciamento Esclusivo Proc da Combattimento**: `07 - Cloak warTank` compare unicamente se sul mantello è presente un vero incanto proccabile da combattimento, specificamente *Swordguard Embroidery* (*Ricamo della Spada* di Sartoria, incanto ID 3730, spell ID 55775, buff +400 AP per 15s con 45s ICD) o se il relativo buff è attivo.
  - [x] Allineamento della barra utility dinamica `_G.PWHUD_UpdateUtilityRowPositions`: in presenza di paracadute o incanti statici, `07 - Cloak warTank` viene escluso da `activeOrder`, ricentrando armoniosamente le restanti icone utility senza lasciare spazi vuoti.
  - [x] Rimozione artefatto grafico: impostato `"cooldownEdge": False` su `07 - Cloak warTank`.
  - [x] Rigenerazione stringa WeakAuras `IMPORT_STRING_v5.21.8.txt` e sincronizzazione simulatore web `docs/index.html`.
  - [x] Aggiornamento sincronizzato della documentazione tecnica bilingue (`README.md` & `README_IT.md`, `HANDOFF.md` & `HANDOFF_IT.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md`).
  - [x] Esecuzione e superamento di tutti gli 8 test paralleli multi-core.
  - [x] Commit Git con messaggio descrittivo.

- [x] **Task 17: Ottimizzazione Compatta Stats Panel (126x60px) & Ravvicinamento 1:1 delle Tre Componenti Sovrastanti (Shouts & Stance con Spaziatura 3px)**:
  - [x] Riconfigurazione geometrica ad alta precisione di `18 - Stats Panel warTank` in `builder/components/stats.py`:
    - Adattamento del background `Stats Panel - Background warTank` a **126x60px** (precedentemente 144x68px), eliminando gli eccessi di spazio vuoto a destra e sul fondo:
      - Larghezza 126px: testo difensivo centrato con 6px di margine laterale pulito sia a sinistra che a destra, senza clipping.
      - Altezza 60px: 5 righe di testo racchiuse perfettamente con 4px di padding verticale superiore e inferiore.
      - Centro riposizionato a **X: -216, Y: -49** per mantenere il bordo superiore perfettamente a Y: -19 (2px di distacco verticale dalla base delle icone superiori a Y: -17).
  - [x] Ravvicinamento compatto delle 3 componenti sovrastanti in `builder/components/buffs.py`:
    - Eliminata la spaziatura eccessiva (21px di gap): le icone (34x34px) sono ora adiacenti e compatte con un margine pulito di **3px** tra loro (step di 37px):
      - `02 - Battle Shout warTank`: centro a **X: -253, Y: 0** (span da -270 a -236).
      - `03 - Commanding Shout warTank`: centro a **X: -216, Y: 0** (span da -233 a -199; gap di 3px rispetto a Battle Shout).
      - `04 - Defensive Stance warTank`: centro a **X: -179, Y: 0** (span da -196 a -162; gap di 3px rispetto a Commanding Shout).
    - Il gruppo delle 3 icone (span totale 108px) risulta ora perfettamente centrato rispetto all'asse del pannello statistiche (126px), con 9px di respiro simmetrico a sinistra e a destra.
  - [x] Aggiornamento test di regressione in `tests/test_tree_layout.py` con le nuove coordinate sincronizzate.
  - [x] Aggiornamento del simulatore web in `docs/index.html` (colonna sinistra 126px, gap 3px, box 126x60px).
  - [x] Rigenerazione stringa WeakAuras `IMPORT_STRING_v5.21.8.txt` e sincronizzazione simulatore web `docs/index.html`.
  - [x] Aggiornamento sincronizzato della documentazione tecnica bilingue (`README.md` & `README_IT.md`, `HANDOFF.md` & `HANDOFF_IT.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md`).
  - [x] Esecuzione e superamento di tutti gli 8 test paralleli multi-core.
  - [x] Esecuzione CP (Commit & Push su `origin/master`).

- [x] **Task 18: Integrazione Componente 04b - Vigilance warTank (Allerta 'OFF' su Mancanza Buff Vigilanza su Alleato)**:
  - [x] Implementazione del modulo e della logica event-driven `SHARED_VIGILANCE_CHECK_LUA` in `builder/components/buffs.py`:
    - Verifica del talento appreso: `_G.PWHUD_CheckVigilance` controlla in tempo reale se il giocatore ha appreso il talento *Vigilance* (Spell ID 50720 / 59665) tramite `IsSpellKnown` e scansione spellbook. Se il talento non è presente, il componente rimane totalmente inattivo.
    - Tracciamento dinamico su alleati:
      - Listener `UNIT_SPELLCAST_SUCCEEDED`: registra l'assegnazione di Vigilanza sull'alleato target (`expires = now + 1800`).
      - Listener `COMBAT_LOG_EVENT_UNFILTERED`: gestisce `SPELL_AURA_APPLIED`, `SPELL_AURA_REFRESH`, `SPELL_AURA_REMOVED`, `SPELL_AURA_BROKEN` e azzera il tracciamento alla morte dell'alleato registrato (`UNIT_DIED`).
      - Scansione reattiva automatica su `target`, `focus`, `party1..4` e `raid1..40` al login, reload o cambio zona.
    - Sotto-aura `Vigilance - OFF warTank` (UID `PWHUD_VIGILANCE_OFF`): compare con icona desaturata e label `OFF` rossa in basso solo quando il guerriero ha appreso il talento ma nessun alleato del gruppo/raid possiede il buff attivo.
    - Sotto-aura `Vigilance - Active warTank` (UID `PWHUD_VIGILANCE_ACTIVE`): attiva solo durante l'avviso di scadenza imminente (`rem <= 60s`). A durata piena rimane invisibile per evitare clutter.
  - [x] Riorganizzazione geometrica della riga a 4 componenti (30x30px con gap di 2px, passo 32px):
    - `02 - Battle Shout warTank`: `X: -264, Y: 0` (span da -279 a -249).
    - `03 - Commanding Shout warTank`: `X: -232, Y: 0` (span da -247 a -217, gap 2px).
    - `04b - Vigilance warTank`: `X: -200, Y: 0` (span da -215 a -185, gap 2px).
    - `04 - Defensive Stance warTank`: `X: -168, Y: 0` (span da -183 a -153, gap 2px).
    - La riga delle 4 componenti combacia al singolo pixel con i 126px di larghezza del pannello statistiche sottostante (da X: -279 a X: -153).
  - [x] Aggiornamento albero master in `builder/tree.py` (21 nodi controllati) e test di regressione (`tests/test_components_integrity.py`, `tests/test_tree_layout.py`, `tests/test_danger_alerts.py`).
  - [x] Aggiornamento simulatore web in `docs/index.html` (aggiunto `#iconVigilance` e classe `.size-30`).
  - [x] Rigenerazione stringa WeakAuras `IMPORT_STRING_v5.21.8.txt` e sincronizzazione simulatore web `docs/index.html`.
  - [x] Aggiornamento sincronizzato della documentazione tecnica bilingue (`README.md` & `README_IT.md`, `HANDOFF.md` & `HANDOFF_IT.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md`).
  - [x] Esecuzione e superamento di tutti gli 8 test paralleli multi-core.
  - [x] Esecuzione CP (Commit & Push su `origin/master`).

- [x] **Task 19: Allineamento '08 - Tier Set warTank' al Cooldown Difensivo Bloodrage T10 4P (Icona Bloodrage, Swipe Cooldown e Timer Scudo 20% HP)**:
  - [x] Riconfigurazione dell'icona e della logica di `08 - Tier Set warTank` in `builder/components/utility.py`:
    - Con il bonus T10 4P (*Ymirjar Lord*), l'abilità *Bloodrage* (*Ira Sanguinaria*, Spell ID 2687) si trasforma in un potente CD difensivo a tempo, garantendo un assorbimento danni del 20% della salute massima per 10 secondi (*Blood Frenzy*, Spell ID 70844).
    - **Icona Dinamica Appropriata**: Sostituita la generica texture scudo con l'icona ufficiale dell'abilità che attiva l'effetto difensivo: *Bloodrage* (`Interface\Icons\Ability_Racial_BloodRage`).
    - **Tre Stati di Tracciamento Cooldown**:
      1. **Attivo (`ACTIVE`)**: Durante i 10s dello scudo *Blood Frenzy*, visualizza timer di durata decrescente `%p` (es. `10.0s`), swipe circolare e Pixel Glow dorato (`LibCustomGlow-1.0`).
      2. **In Ricarica (`COOLDOWN`)**: Alla scadenza del buff difensivo, traccia istantaneamente il tempo di ricarica residuo di *Bloodrage* (60s o ridotto dai talenti) con swipe e countdown numerico in secondi/minuti.
      3. **Pronto (`READY`)**: Quando Bloodrage è disponibile, mostra l'icona pulita pronta all'uso difensivo.
    - **Soppressione Automatica**: Se il giocatore non indossa il T10 4P, il componente viene escluso e la barra utility ricentra fluidamente le restanti icone.
    - **Pulizia Bordo**: Impostato `"cooldownEdge": False` per eliminare qualsiasi artefatto a spillo giallo a riposo.
  - [x] Rigenerazione stringa WeakAuras `IMPORT_STRING_v5.21.8.txt` e sincronizzazione simulatore web `docs/index.html`.
  - [x] Aggiornamento sincronizzato della documentazione tecnica bilingue (`README.md` & `README_IT.md`, `HANDOFF.md` & `HANDOFF_IT.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md`).
  - [x] Esecuzione e superamento di tutti gli 8 test paralleli multi-core.
  - [x] Esecuzione CP (Commit & Push su `origin/master`).

- [x] **Task 20: Espansione Massiva Database Tank Buster Alert (Tutti i Boss Raid WotLK 3.3.5a & Trash Pericolosi) e Perfezionamento Vigilance (Allineamento 1:1 a Focus Magic)**:
  - [x] Database completo dei debuff letali e meccaniche tank swap in `builder/components/procs.py`:
    - Definita la tabella `_G.PWHUD_TankBustersDB` per Spell ID e `_G.PWHUD_TankBustersByName` per nomi bilingue (EN / IT) con soglie stack (`min`) e tag d'azione (`SWAP`, `STACK`, `HEAL`, `RUN`, `PLASMA`, `FUSION`, `MELT`, `BRAND`, `TOXIN`, `INFECT`, `SPRAY`, `CD!`, `POT`, `SHADOW`).
    - **Icecrown Citadel (ICC)**: Soul Reaper (Lich King 10N/25N/10H/25H - 69409, 73797, 73798, 73799), Gastric Bloat (Festergut 10N/25N/10H/25H >= 8 - 72219, 72551, 72552, 72553), Rune of Blood (Saurfang - 72410), Mystic Buffet (Sindragosa P3 >= 5 - 70127, 70128), Delirious Slash (Lana'thel >= 2 - 71623, 71624), Mutated Plague (Putricide P3 >= 2 - 72451..72454), Mutated Infection (Rotface - 69674..73023), Corrosion (Valithria Zombie >= 3 - 70751, 71236), Gut Spray (Valithria Abomination - 70633, 71232), Severed Flesh (Deathbound Ward / Trash ICC >= 3 - 71127).
    - **Ruby Sanctum (RS)**: Fiery Combustion (Halion - 74562, 74567, 74795), Soul Consumption (Halion - 74792, 74793, 74799), Cleave Armor (Zarithrian >= 2 - 74367), Enervating Brand (Baltharus - 74502).
    - **Trial of the Crusader (TotC / ToGC)**: Impale (Gormok >= 2 - 67478, 67479, 66331), Paralytic Toxin (Acidmaw - 66823, 67618), Incinerate Flesh (Jaraxxus - 66237, 67049..67051), Expose Weakness (Anub'arak Nerubian Burrower >= 2 - 67847..67849).
    - **Ulduar**: Phase Punch (Algalon >= 3 - 64412, 64417), Unbalancing Strike (Thorim - 62130, 62131), Fusion Punch (Steelbreaker - 61903, 63493), Overwhelming Power (Steelbreaker - 61888, 64637), Fuse Armor (Razorscale >= 2 - 64771, 64772), Surge of Darkness (General Vezax - 62661, 62662), Plasma Blast (Mimiron - 62997, 64529), Crunch Armor (Kologarn >= 2 - 63355, 64002), Slag Pot (Ignis - 62717, 63477).
    - **Naxxramas, VoA, Sartharion**: Mortal Wound (Gluth >= 4 - 25646), 4 Horsemen Marks (Blaumeux, Rivendare, Korth'azz, Zeliek >= 3 - 28832..28835), Frostbite (Toravon - 72098), Twilight Torment (Sartharion - 57948).
  - [x] Dinamismo grafico completo in `Tank Buster Alert`:
    - Funzione `_G.PWHUD_CheckTankBusters(force)` condivisa con caching per frame.
    - Texture dinamica `customIcon`: adotta all'istante l'icona del debuff critico attivo sul giocatore.
    - Conto alla rovescia e swipe circolare `customDuration` con `"cooldownEdge": False`.
    - Etichetta dinamica `%c` (`customText`) che visualizza l'azione consigliata o il conteggio stack (`SWAP`, `x8`, `HEAL`, `RUN`, `PLASMA`, ecc.).
    - Azione `actions.start` con red Pixel Glow e `actions.finish` con rimozione glow al termine del debuff.
  - [x] Perfezionamento architettura `04b - Vigilance warTank` in `builder/components/buffs.py`:
    - Rimossa la verifica bloccante `IsSpellKnown` (non supportata nativamente nell'ambiente FrameXML 3.3.5a), allineando il trigger di `Vigilance - OFF warTank` direttamente al modello collaudato di Focus Magic (`not allyActive`).
    - L'icona compare desaturata con `OFF` rosso non appena nessun alleato attivo nel raggio o nel party/raid possiede la vigilanza.
  - [x] Aggiornamento dei test in `tests/test_danger_alerts.py` a copertura di tutti i nuovi Spell ID e meccaniche.
  - [x] Rigenerazione stringa WeakAuras `IMPORT_STRING_v5.21.8.txt` e sincronizzazione simulatore web `docs/index.html`.
  - [x] Aggiornamento sincronizzato della documentazione tecnica bilingue (`README.md` & `README_IT.md`, `HANDOFF.md` & `HANDOFF_IT.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md`).
  - [x] Esecuzione e superamento di tutti gli 8 test paralleli multi-core.
  - [x] Esecuzione CP (Commit & Push su `origin/master`).

- [x] **Task 21: Riposizionamento 'Shield Block Active' nella Riga Utility Inferiore ('10b - Shield Block warTank') con Tracciamento Cooldown e Durata Attiva**:
  - [x] Rimozione di `Shield Block Active` da `01 - Procs warTank` in `builder/components/procs.py`:
    - Rimosso `Shield Block Active` dai nodi controllati (`controlledChildren`) del gruppo dinamico superiore.
    - Eliminata la visualizzazione limitata al solo buff attivo a Y: +52.
  - [x] Creazione di `10b - Shield Block warTank` (UID `PWHUD_UTIL_SHIELDBLOCK`) in `builder/components/utility.py`:
    - Posizionamento a **Y: -45** a fianco di `11 - Shield Wall warTank` e `12 - Last Stand warTank`.
    - **Engine a Tre Stati (Durata, Ricarica, Pronto)**:
      1. **Attivo (`ACTIVE`)**: Durante i 10 secondi del buff *Shield Block* (Spell ID 2565), visualizza il conto alla rovescia decrescente della durata residua (`|cFFFFFF00%.1fs|r`, es. `9.8s`), swipe circolare e Pixel Glow dorato (`LibCustomGlow-1.0`).
      2. **In Ricarica (`COOLDOWN`)**: Alla scadenza del buff, traccia in tempo reale il tempo di ricarica residuo (base 60s, oppure 30s con il talento *Shield Mastery*) con conto alla rovescia numerico e swipe circolare di recupero con `"cooldownEdge": False` (bordo pulito).
      3. **Pronto (`READY`)**: Quando Shield Block è disponibile, visualizza l'icona ufficiale pulita (`Interface\Icons\Ability_Defensive`) pronta all'uso senza clutter numerico.
  - [x] Integrazione nel riposizionamento dinamico automatico `_G.PWHUD_UpdateUtilityRowPositions()`:
    - Inserito `10b - Shield Block warTank` nell'ordine naturale `activeOrder` prima di `11 - Shield Wall warTank`.
    - Calibrato lo scaling automatico della riga utility fino a 11 icone contemporanee (step 25px, larghezza 24-28px) per preservare la centratura naturale entro i 278px.
  - [x] Aggiornamento dei nodi controllati in `builder/tree.py` (22 nodi controllati).
  - [x] Aggiornamento del simulatore web in `docs/index.html` (rimosso `#procSB` da `.procs-bar`, aggiunto `#iconSB` a `.utility-bar`).
  - [x] Aggiornamento dei test di regressione (`tests/test_components_integrity.py`, `tests/test_defensives.py`, `tests/test_tree_layout.py`).
  - [x] Rigenerazione stringa WeakAuras `IMPORT_STRING_v5.21.8.txt` e sincronizzazione simulatore web `docs/index.html`.
  - [x] Aggiornamento sincronizzato della documentazione tecnica bilingue (`README.md` & `README_IT.md`, `HANDOFF.md` & `HANDOFF_IT.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md`).
  - [x] Esecuzione e superamento di tutti gli 8 test paralleli multi-core.
  - [x] Esecuzione CP (Commit & Push su `origin/master`).

- [x] **Task 22: Target Debuff Trackers in '01 - Procs warTank' (Demoralizing Shout, Thunder Clap, Rend) con Ordinamento Ascending per Scadenza, Filtro Meccanici e Caching Unificato**:
  - [x] Architettura e configurazione dinamica di `01 - Procs warTank`:
    - Impostato `"sort": "ascending"` nel gruppo dinamico: le icone vengono posizionate automaticamente da sinistra verso destra in base al tempo di scadenza (`expirationTime`). I debuff mancanti (`MISS`) restituiscono il timestamp corrente `now` (il valore minimo possibile), garantendo il loro piazzamento prioritario all'estrema sinistra.
  - [x] Implementazione dei 3 Target Debuff Tracker (34x34px):
    1. **Demoralizing Shout Tracker warTank** (UID `PWHUD_PROC_DEMO`, icona `Ability_Warrior_WarCry`):
       - **Raid-Aware (Opzione A)**: riconosce Warrior *Demoralizing Shout* (tutti i rank), Druid *Demoralizing Roar* (tutti i rank) e Warlock *Curse of Weakness* (tutti i rank).
       - **Soglia Visibilità (Opzione B modificata)**: compare solo se mancante (`MISS`) o in scadenza entro <= 10s (`%.1f` secondi). Completamente nascosto se applicato con durata > 10s, fuori combattimento o target non valido.
    2. **Thunder Clap Tracker warTank** (UID `PWHUD_PROC_TC`, icona `Spell_Nature_ThunderClap`):
       - **Raid-Aware (Opzione A)**: riconosce Warrior *Thunder Clap* (tutti i rank), Death Knight *Frost Fever* (Spell 55095), Paladin *Judgements of the Just* (Spell 53695, 53696) e Druid *Infected Wounds* (Spell 48483, 48484, 48485).
       - **Soglia Visibilità (Opzione B modificata)**: compare solo se mancante (`MISS`) o in scadenza entro <= 10s (`%.1f` secondi). Completamente nascosto se applicato con durata > 10s.
    3. **Rend Tracker warTank** (UID `PWHUD_PROC_REND`, icona `Ability_Gouge`):
       - **Player Filter**: traccia esclusivamente il debuff *Rend* applicato dal Warrior giocatore (`unitCaster == "player"`).
       - **Filtro Immunità Meccanici**: soppressione totale dell'avviso (`return false, "IMMUNE"`) se `UnitCreatureType("target") == "Mechanical"` o `"Meccanico"`, evitando falsi allarmi su mob e boss immuni ai sanguinamenti.
       - **Soglia Visibilità (Opzione B modificata)**: compare solo se mancante (`MISS`) o in scadenza entro <= 5s (`%.1f` secondi).
  - [x] Ottimizzazione Lua e Caching Unificato per frame (`_G.PWHUD_TargetDebuffScanCache`):
    - La scansione dei debuff sul target viene eseguita una sola volta per frame tick condividendo lo stato tra i 3 tracker, azzerando l'overhead computazionale e prevenendo spike di GC.
  - [x] Suite di Test Dedicata `tests/test_target_debuffs.py` e aggiornamento runner parallelo `tests/run_parallel_tests.py` (9/9 test superati con successo in 0.37s).
  - [x] Rigenerazione stringa WeakAuras `IMPORT_STRING_v5.21.8.txt` (66880 caratteri) e sincronizzazione simulatore web `docs/index.html`.
  - [x] Aggiornamento sincronizzato della documentazione tecnica bilingue (`README.md` & `README_IT.md`, `HANDOFF.md` & `HANDOFF_IT.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md`).
  - [x] Esecuzione CP (Commit & Push su `origin/master`).

- [x] **Task 23: Fix e Rifattorizzazione Architetturale '15 - Rotational Bar warTank' (Accodamento Reattivo Heroic Strike & Cleave con Frame-Rate Update e Pixel Glow)**:
  - [x] Root cause analysis del malfunzionamento:
    - In WotLK 3.3.5a, `IsCurrentSpell` accetta esclusivamente il nome stringa dell'abilità (`"Heroic Strike"`, `"Cleave"`) e non lo Spell ID numerico (interpretato dal client come slot dell'indice del grimorio, risultando in `nil`).
    - Il controllo ad eventi (`check: "event"`) su abilità "al prossimo colpo in mischia" non riceveva eventi immediati (`CURRENT_SPELL_CAST_CHANGED` non scatta per incantesimi on-next-swing).
    - Tentativo di gestione bifronte in un'unica aura tramite customText su subregion nascosta, che impediva le transizioni reattive tra Heroic Strike e Cleave.
  - [x] Nuova architettura modulare reattiva in `builder/components/rotational.py`:
    - **Rotational Bar - Background warTank** (`PWHUD_ROTCENTER_BG`, 278x7px): cornice scura di base semitrasparente.
    - **Rotational Bar - Base Bar warTank** (`PWHUD_ROTCENTER_BASE`, 274x5px): barra statica piena larghezza in texture warrior copper/bronze (`[0.65, 0.35, 0.12, 0.90]`) sempre visibile come riposo neutro (zero swipe, zero timer numerici).
    - **Rotational Bar - HS Queued warTank** (`PWHUD_ROTCENTER_HSQ`, 274x5px):
      - Trigger con `check: "update"` (valutazione OnUpdate frame-accurate) e risoluzione universale del nome tramite `GetSpellInfo(47450)` con fallback bilingue EN/IT.
      - Barra piena larghezza color Oro vibrante (`[1.0, 0.84, 0.0, 1.0]`).
      - Azione di Pixel Glow dorata (`LibCustomGlow-1.0` con chiave `PWHUD_HS_GLOW` e `do_glow: True` nativo di WeakAuras).
    - **Rotational Bar - Cleave Queued warTank** (`PWHUD_ROTCENTER_CLQ`, 274x5px):
      - Trigger con `check: "update"` e risoluzione universale tramite `GetSpellInfo(47520)`.
      - Barra piena larghezza color Verde Smeraldo vibrante (`[0.1, 0.95, 0.2, 1.0]`).
      - Azione di Pixel Glow verde smeraldo (`LibCustomGlow-1.0` con chiave `PWHUD_CLEAVE_GLOW` e `do_glow: True` nativo).
  - [x] Creazione unit test dedicato `tests/test_rotational.py` e integrazione nella test suite parallela `tests/run_parallel_tests.py` (10/10 test superati in 0.39s).
  - [x] Rigenerazione stringa WeakAuras `IMPORT_STRING_v5.21.8.txt` (66692 caratteri) e sincronizzazione `docs/index.html`.
  - [x] Aggiornamento sincronizzato della documentazione tecnica bilingue (`README.md` & `README_IT.md`, `HANDOFF.md` & `HANDOFF_IT.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md`).
  - [x] Esecuzione CP (Commit & Push su `origin/master`).

- [x] **Task 24: Castbar Speculare Intelligente '16 - Castbar warTank' (Player sx->dx vs Target dx->sx con Priorità Assoluta, Shield Bash & Spell Reflection Advisor)**:
  - [x] Riorganizzazione architetturale del modulo `16 - Castbar warTank` (`builder/components/bars.py`) come gruppo contenitore $278 	imes 20\text{px}$ a $y = +8$ con 2 aurabar speculari:
    1. **Castbar - Target warTank** (UID `PWHUD_CASTBAR_TARGET`, $278 	imes 20\text{px}$, `inverse: True`):
       - **Scorrimento inverso da destra verso sinistra**: effetto visivo di pericolo e conto alla rovescia del cast in arrivo.
       - **Priorità Assoluta sul Player Cast**: in caso di sovrapposizione temporale con un cast del giocatore, il cast del target prende immediatamente possesso della barra.
       - **Advisor Intelligente Dicitura Opzione A**:
         - *Shield Bash*: `NomeSpell [SHIELD BASH]` o `[BASH / REFLECT]` se a raggio di mischia ($\le 5\text{yd}$) con barra ciano viva (`[0.0, 0.85, 1.0]`).
         - *Spell Reflection*: `NomeSpell [SPELL REFLECTION]` se il target sta mirando al tank (`UnitIsUnit("targettarget", "player")`), il tank ha lo scudo e Spell Reflection è pronto (consigliato prioritariamente anche a distanza $> 5\text{yd}$ o con Shield Bash in CD), con barra magenta/viola (`[0.78, 0.25, 0.95]`).
         - *Immune*: `NomeSpell [IMMUNE]` con barra grigio piombo (`[0.50, 0.50, 0.50]`) se il cast è non interrompibile e non riflettibile.
    2. **Castbar - Player warTank** (UID `PWHUD_CASTBAR_PLAYER`, $278 	imes 20\text{px}$, `inverse: False`):
       - **Scorrimento standard da sinistra verso destra**: visualizza i lanci e le canalizzazioni del giocatore (Shoot, Throw, professioni, Slam, ecc.) con icona a sinistra, nome incantesimo e tempo residuo a destra.
       - Soppressione automatica se il bersaglio sta lanciando un incantesimo (`if targetSpell then return false end`).
  - [x] Aggiornamento delle costanti grafiche (`COLOR_CASTBAR_REFLECT = [0.78, 0.25, 0.95, 1.0]` in `builder/core/constants.py`).
  - [x] Aggiornamento dei test di regressione (`tests/test_interrupts.py` e `tests/test_tree_layout.py`) a copertura del gruppo, delle due barre speculari, dell'inversione e dell'advisor.
  - [x] Aggiornamento del simulatore web interattivo in `docs/index.html` (nuovi preset per Target Kick dx->sx, Target Reflect dx->sx, Target Immune dx->sx e Player Cast sx->dx).
  - [x] Rigenerazione stringa WeakAuras `IMPORT_STRING_v5.21.8.txt` (69073 caratteri) e sincronizzazione `docs/index.html`.
  - [x] Aggiornamento sincronizzato della documentazione tecnica bilingue (`README.md` & `README_IT.md`, `HANDOFF.md` & `HANDOFF_IT.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md`).
  - [x] Esecuzione CP (Commit & Push su `origin/master`).


- [x] **Task 25: Risoluzione Texture Question Mark '?', Soppressione Completa Debuff Applicati e Priorità Gerarchica Emergenze > Procs > Debuff in '01 - Procs warTank'**:
  - [x] **Risoluzione Texture Question Mark '?'**:
    - Risolto il problema delle icone rosse con punto interrogativo '?' visualizzate in gioco su WotLK 3.3.5a, causato dall'escape di backslash non raw nelle stringhe Lua `customIcon`.
    - Implementata la risoluzione dinamica nativa tramite chiamata C++ `select(3, GetSpellInfo(spellId))` per Demoralizing Shout (47437), Thunder Clap (47502) e Rend (47465), garantendo il recupero immediato e corretto della texture client per qualsiasi lingua e server core.
  - [x] **Soppressione Totale dei Debuff se Applicati ("se applicate devono sparire")**:
    - I tracker debuff (`DEMO`, `CLAP`, `REND`) ora si nascondono istantaneamente se il debuff è presente sul bersaglio (`return false, "ACTIVE"`).
    - Compaiono esclusivamente durante il combattimento su bersaglio ostile valido quando sono MANCANTI (`return true, "MISS"`), con dicitura visibile `|cFFFF2020MISS|r`.
    - Mantenuto il filtro immunità meccanica per Rend (`cType == "Mechanical"` o `"Meccanico"`) con soppressione completa (`return false, "IMMUNE"`).
    - Lookup table precalcolata globale `_G.PWHUD_DebuffLookup` con ID raid-aware, nomi localizzati e pattern substring su icona (`warcry`, `thunderclap`, `gouge`) per scansione per-frame senza fallimenti.
  - [x] **Ordinamento e Priorità Visiva da Sinistra verso Destra (`sort: "none"`)**:
    - Riconfigurato `"sort": "none"` nel gruppo dinamico `01 - Procs warTank` per disattivare l'ordinamento dinamico per durata residua (che forzava i debuff MISS all'estrema sinistra) e imporre l'ordine fisso e gerarchico di `controlledChildren`:
      1. `Emergency Low HP Alert` (Salute critica < 35%, allarme prioritario all'estrema sinistra).
      2. `Tank Buster Alert` (Debuff letali raid/dungeon 3.3.5a: Soul Reaper, Impale, Fusion Punch...).
      3. `Revenge Ready warTank` (Proc offensivo/difensivo Ritorsione, 5s).
      4. `Sword and Board` (Proc Spada e Scudo, Shield Slam istantaneo).
      5. `Demoralizing Shout Tracker warTank` (Debuff mancante sul target).
      6. `Thunder Clap Tracker warTank` (Debuff mancante sul target).
      7. `Rend Tracker warTank` (Debuff mancante sul target, estrema destra).
  - [x] **Test Suite e Documentazione**:
    - Aggiornato `tests/test_target_debuffs.py` per verificare `sort == "none"`, la lista ordinata dei figli, la soppressione ad applicazione e le icone C++.
    - Suite parallela multi-core: 10/10 test superati in 0.39s.
    - Rigenerata la stringa WeakAuras `IMPORT_STRING_v5.21.8.txt` e sincronizzato `docs/index.html`.
    - Documentazione tecnica bilingue allineata (`README.md`, `README_IT.md`, `HANDOFF.md`, `HANDOFF_IT.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md`).
    - Esecuzione CP (Commit & Push su `origin/master`).

- [x] **Task 26: Integrazione Timer Conto alla Rovescia & Soppressione Dinamica per Target Debuffs in '01 - Procs warTank' (Scomparsa con Durata Abbondante, Timer <=10s / <=5s, e Allerta MISS)**:
  - [x] **Logica di Visibilità e Timer per Debuff Applicati**:
    - Se applicati con durata abbondante (>10s per Demoralizing Shout e Thunder Clap, >5s per Rend), le icone **scompaiono completamente** (`return false, "HEALTHY"`), garantendo zero ingombro visivo.
    - Se applicati e in fase di scadenza ($\le 10\text{s}$ per Demo/Clap, $\le 5\text{s}$ per Rend), le icone **compaiono con il timer** e lo swipe circolare attivo (`return true, "EXPIRING"`). Il subtext `%c` mostra il countdown numerico in secondi (giallo `%.1fs`, rosso `%.1fs` a $\le 3\text{s}$).
    - Se mancanti in combattimento su bersaglio attaccabile valido, compaiono con dicitura rossa `MISS` (`return true, "MISS"`).
  - [x] **Attivazione Frame-Accurate OnUpdate & Subtext %c**:
    - Impostato `check: "update"` sui trigger dei 3 tracker per consentire la comparsa istantanea non appena il debuff scende sotto la soglia di 10s/5s senza dipendere da eventi discontinui.
    - Registrato `customText` sia all'interno di `trigger.customText` che nella root dell'aura, garantendo la risoluzione infallibile di `%c` in `subRegions`.
  - [x] **Test Suite & Documentazione Sincronizzata**:
    - Aggiornato [`tests/test_target_debuffs.py`](file:///d:/0Progetti/protection-warrior-335a-am/tests/test_target_debuffs.py) con test dedicati a soglie temporali, swipe, stati `HEALTHY`, `EXPIRING`, `MISS` e `IMMUNE`.
    - 10/10 test paralleli superati con successo in 0.45s.
    - Rigenerata la stringa di importazione `IMPORT_STRING_v5.21.8.txt` (72252 caratteri) e aggiornato `docs/index.html`.
    - Documentazione tecnica allineata (`README.md`, `README_IT.md`, `HANDOFF.md`, `HANDOFF_IT.md`, `docs/ARCHITECTURE.md`, `docs/TASKS.md`).
    - Esecuzione CP (Commit & Push su `origin/master`).

- [x] **Task 27: Fix Untrigger Reattivo Target Debuffs (Scomparsa Immediata Senza Target / Target Morto e Reattività al Cambio Target)**:
  - [x] **Causa del Blocco Visivo Senza Target**:
    - La funzione `untrigger` nei 3 tracker restituiva `false` staticamente (`function() return false end`), impedendo al motore di WeakAuras di disattivare l'aura una volta attivata, anche in assenza di target o a target morto.
  - [x] **Implementazione Untrigger Dinamico Reattivo**:
    - Creata la funzione `make_target_debuff_untrigger(kind)` che valuta `return not show`: non appena `show` diventa `false` (nessun bersaglio attivo `not UnitExists("target")`, bersaglio morto `UnitIsDead("target")`, non attaccabile `not UnitCanAttack` o fuori combattimento), l'aura riceve segnale `true` di untrigger e **scompare istantaneamente**.
    - Inserito lo svuotamento cache `_G.PWHUD_TargetDebuffScanCache = nil` ad ogni deselezione bersaglio per azzerare lo stato.
  - [x] **Aggiornamento Istantaneo al Cambio Target (`PLAYER_TARGET_CHANGED`)**:
    - La scansione frame-accurate confronta `cache.targetGUID ~= tGUID`: non appena si seleziona un nuovo mob o boss, la cache viene ricalcolata al primo tick, mostrando i debuff mancanti sul nuovo target o nascondendo quelli già presenti con durata >10s/5s.
  - [x] **Test Suite & Documentazione**:
    - Aggiornato [`tests/test_target_debuffs.py`](file:///d:/0Progetti/protection-warrior-335a-am/tests/test_target_debuffs.py) a verifica di `untrigger` reattivo (`return not show`).
    - Suite parallela: 10/10 test superati in 0.41s.
    - Rigenerata `IMPORT_STRING_v5.21.8.txt` (72672 caratteri) e aggiornato `docs/index.html`.
    - Esecuzione CP (Commit & Push su `origin/master`).


- [x] **Task 28: Ottimizzazione e Deduplicazione Architetturale Stringa WeakAuras (Riduzione del 33.3% da 72.672 a 48.502 Caratteri a Parità Funzionale 1:1)**:
  - [x] **Audit e Root Cause Analysis delle Duplicazioni**:
    1. **Trinket 1 Duplicate Bootstrap (67.065 caratteri uncompressed eliminati)**:
       - Rilevata la duplicazione ridondante dell'intero blocco `SHARED_WARRIOR_CORE_BOOTSTRAP_LUA` dentro il trigger di `05 - Trinket 1 warTank` (già presente e inizializzato nativamente in `actions.init` del master group).
       - Sostituito con chiamata snella `if (not _G.PWHUD_CoreInitDone or _G.PWHUD_BUILD_VER ~= 48) and _G.PWHUD_InitCore then _G.PWHUD_InitCore() end`.
    2. **Target Debuffs Template Duplication (~100.000 caratteri uncompressed eliminati)**:
       - `SHARED_TARGET_DEBUFFS_LUA` (6.7 KB) era interpolato 15 volte (trigger, untrigger, customDuration, customText in trigger, customText in aura root per 3 auras).
       - Centralizzata l'inizializzazione in `_G.PWHUD_CheckTargetDebuff` all'interno di `actions.init` del root group. I trigger invocano ora semplicemente la funzione globale in 2 righe.
    3. **Tank Buster Alert Duplication (~46.000 caratteri uncompressed eliminati)**:
       - `TANK_BUSTER_CHECK_LUA` (11.7 KB contenente il database raid WotLK) era interpolato 4 volte (custom, customText, customIcon, customDuration).
       - Centralizzato in `_G.PWHUD_CheckTankBusters` in `actions.init`. I trigger sono ora semplici consumatori della funzione globale.
  - [x] **Metriche di Riduzione**:
    - **Dimensione Uncompressed AceSerialized**: ridotta da **627.447 caratteri a 363.851 caratteri** (risparmio netto di **263.596 caratteri**, riduzione del **42.0%** del payload in memoria).
    - **Stringa di Importazione (`IMPORT_STRING_v5.21.8.txt`)**: ridotta da **72.672 caratteri a 48.502 caratteri** (risparmio netto di **24.170 caratteri**, riduzione del **33.3%**).
  - [x] **Integrità Funzionale al 100%**:
    - Zero modifiche logiche: rilevamento debuff (Demoralizing Shout, Thunder Clap, Rend con filtro meccanici), allerta MISS, scomparsa con durata abbondante (>10s/5s), conto alla rovescia timer ($\le 10\text{s}$/$\le 5\text{s}$) e reattività al cambio o deselezione target rimangono identici.
    - Test Suite Parallela: 10/10 test superati con successo in 0.41s.
    - Rigenerazione di `IMPORT_STRING_v5.21.8.txt` e sincronizzazione simulatore web `docs/index.html`.
    - Esecuzione CP (Commit & Push su `origin/master`).

- [x] **Task 29: Rimozione di Alert - Boss Enraged e Alert - Wrong Stance da 17 - Alerts warTank**:
  - [x] **Contesto e De-cluttering su Richiesta Utente**:
    - Rimossi gli allarmi testuali centrali `Alert - Boss Enraged` (notifica enrage boss) e `Alert - Wrong Stance` (scritta centrale ad alta priorità `>> DEFENSIVE STANCE REQUIRED! <<` con audio `RaidWarning.ogg` a $y = 64$) per eliminare elementi testuali non desiderati ed evitare sovrapposizioni e allarmi invasivi.
    - L'icona compatta `04 - Defensive Stance - OutOfStance warTank` (30x30px a fianco degli urli ad $x = -168, y = 0$) rimane attiva e funzionante per segnalare chiaramente quando si è fuori postura difensiva in combattimento garantendo massima reattività e zero clutter sul War Tank.
  - [x] **Aggiornamento Componente Alerts (`builder/components/alerts.py`)**:
    - Aggiornato `controlledChildren` del gruppo `17 - Alerts warTank` a 3 elementi: `Alert - Sword and Board`, `Alert - Emergency CD`, `Alert - Kick Now`.
    - Eliminate integralmente le strutture dati dizionario per `Alert - Boss Enraged` e `Alert - Wrong Stance`.
  - [x] **Aggiornamento Simulatore Web & Test Suite**:
    - Rimosse le classi CSS, gli elementi DOM `#alertWrongStance` e `#alertEnrage`, i pulsanti preset e la gestione JS in `docs/index.html`. Aggiornata la pillola informativa su Defensive Stance.
    - Aggiornato `tests/test_danger_alerts.py` con asserzioni negative a garanzia che entrambi gli allarmi siano assenti sia dall'albero complessivo che da `controlledChildren`.
    - Esecuzione Test Suite Parallela: 10/10 superati con successo in 0.37s.
    - Stringa di importazione WeakAuras rigenerata a **48.237 caratteri** e sincronizzata in `docs/index.html`.
    - Esecuzione CP (Commit & Push su `origin/master`).

- [x] **Task 30: Ottimizzazione Visiva Procs Bar — Rimozione Label Debuff, Timer Decimale Stile Slam, SLAM/REV Centrati in Alto e Filtro Bersaglio >= 500k HP**:
  - [x] **Filtro Salute Bersaglio (>= 500.000 HP)**:
    - Inserito in `_G.PWHUD_CheckTargetDebuff` il controllo `UnitHealthMax("target") < 500000`: se il bersaglio attivo ha salute totale inferiore a 500k HP (trash mob, add secondari, mob generici), il tracciamento dei debuff non si attiva mai (`return false, "LOW_HP"`), garantendo zero ingombro visivo.
    - Su boss ed élite maggiori ($\ge 500	ext{k}$ HP), i debuff (Demoralizing Shout, Thunder Clap, Rend) continuano a funzionare regolarmente con tutte le logiche di controllo (allarme MISS, scomparsa se sani $>10	ext{s}$/$>5	ext{s}$, timer se in scadenza).
  - [x] **Rimozione Label Statiche da Rend, Demo e Clap**:
    - Rimosse le etichette di testo interne `DEMO`, `CLAP` e `REND` per non coprire le illustrazioni delle icone.
    - All'interno di ciascuna icona rimane esclusivamente il subtext dinamico `%c`: in stato `EXPIRING` proietta il timer decimale (`%.1f`, es. `3.7`, `5.2`) identico a Slam; in stato `MISS` proietta `MISS`.
  - [x] **Riallineamento SLAM e REV Centrati in Alto (`INNER_TOP`)**:
    - Aggiornati i subtext `SLAM` (Sword and Board) e `REV` (Revenge Ready) con ancoraggio `anchor_point="INNER_TOP"` e `y_offset=-2`, posizionando le scritte dentro l'icona centrate in alto.
    - I rispettivi timer `%p` rimangono ancorati in basso a `INNER_BOTTOM` (`font_size=11`, `y_offset=1`), garantendo una separazione visiva perfetta (etichetta in alto, timer in basso).
  - [x] **Test Suite & Documentazione**:
    - Aggiornato [`tests/test_target_debuffs.py`](file:///d:/0Progetti/protection-warrior-335a-am/tests/test_target_debuffs.py) a verifica del filtro $\ge 500	ext{k}$ HP, dell'assenza di etichette statiche nei debuff e del posizionamento `INNER_TOP` di `SLAM` e `REV`.
    - Suite parallela: 10/10 test superati con successo in 0.43s.
    - Stringa WeakAuras rigenerata a 48.248 caratteri e sincronizzata in `docs/index.html`.
    - Esecuzione CP (Commit & Push su `origin/master`).

- [x] **Task 31: Risoluzione Definitiva Regressione Banner "SHIELD SLAM READY!" e Rimozione Completa di Alert - Sword and Board**:
  - [x] **Root Cause Analysis della Regressione**:
    - L'utente ha riscontrato a schermo la comparsa fissa della scritta gialla a 20pt `SHIELD SLAM READY!` al centro della visuale anche da fermi in città con 0 rabbia.
    - Causa 1: Esistenza di `Alert - Sword and Board` dentro `17 - Alerts warTank`, ridondante rispetto all'icona del proc in `01 - Procs warTank`.
    - Causa 2: Lo Spell ID `46953` inserito nel trigger era l'ID del talento passivo (Rango 1) nel ramo Protezione. Avendo il talento appreso, l'aura risultava perennemente attiva e non scompariva mai.
  - [x] **Risoluzione & Pulizia**:
    - Rimossa completamente l'aura `Alert - Sword and Board` da `builder/components/alerts.py` e da `controlledChildren` di `17 - Alerts warTank`.
    - `17 - Alerts warTank` controlla ora solo `Alert - Emergency CD` e `Alert - Kick Now`.
    - Rimossi `#alertSab` e `.alert-text-sab` da `docs/index.html`.
    - Aggiornato `tests/test_danger_alerts.py` con asserzioni negative che certificano l'assenza totale di `Alert - Sword and Board`.
    - Salvata la regola tassativa in `docs/MEMORY.md` (Sezione 2.3).
    - Test Suite Parallela: 10/10 superati con successo in 0.47s.
    - Stringa WeakAuras rigenerata a 48.017 caratteri e sincronizzata in `docs/index.html`.
    - Esecuzione CP (Commit & Push su `origin/master`).

- [x] **Task 32: Risoluzione Regressione Sparizione Trinket & Auto-Adattamento Barra Utility**:
  - [x] **Root Cause**:
    - In WeakAuras 3.3.5a, `actions.init` sul gruppo radice `Class Warrior (Protection)` (`regionType: "group"`) non viene mai eseguito dal motore dell'addon.
    - Nel Task 28, credendo che `actions.init` del gruppo eseguisse il bootstrap, era stato rimosso `bootstrap` dal trigger di `05 - Trinket 1 warTank`.
    - Non venendo mai definito `_G.PWHUD_InitCore`: `_G.PWHUD_CheckSlotEquipped` risultava `nil`, facendo restituire `false` a tutti gli slot (trinket, anello, mantello, guanti) e impedendo a `_G.PWHUD_UpdateUtilityRowPositions` di auto-adattare e centrare le icone.
  - [x] **Risoluzione Definitiva**:
    - Ripristinata l'inizializzazione tassativa `_G.PWHUD_InitCore` all'interno del trigger di `05 - Trinket 1 warTank` (`slot == 13`), includendo anche la definizione centralizzata di `_G.PWHUD_CheckTargetDebuff` e `_G.PWHUD_CheckTankBusters`.
    - Inserito fallback difensivo in `_G.PWHUD_UpdateUtilityRowPositions` (`group = getRegion(...) or rage:GetParent()`).
    - Rigenerata `IMPORT_STRING_v5.21.8.txt` (72.749 caratteri) e sincronizzato `docs/index.html`.
    - Suite parallela: 10/10 test superati in 0.49s.
    - Aggiornata memoria tecnica in `docs/MEMORY.md` (Sezione 2.4).
    - Esecuzione CP (Commit & Push su `origin/master`).

- [x] **Task 33: Allineamento Globale Documentazione DOCS su Riga Utility Auto-Adattiva e Specifiche Filtri Item per il War Tank**:
  - [x] **Direttiva Utente**:
    - "Quello che sta sotto come i due trinket, l'eventuale anello, mantello, solo se ha le specifiche indicate, e i cooldown difensivi devono adattarsi dinamicamente centrandosi in modo naturale sotto la barra della rabbia del War Tank."
  - [x] **Allineamento File di Documentazione Eseguito**:
    - **`docs/ARCHITECTURE.md`**:
      - Aggiornata la tabella riassuntiva dei componenti per la riga utility (`05` - `13`).
      - Aggiunta la Sezione 4.1 dedicata con descrizione dell'architettura auto-adattiva a centratura dinamica naturale, formula matematica $X$ ($\lfloor (i - rac{N+1}{2}) 	imes 	ext{step} + 0.5 
floor$), tabella di scaling $N = 3 \dots 11$ (step $25	ext{px} \dots 52	ext{px}$, larghezza $24	ext{px} \dots 28	ext{px}$) e specifiche di filtraggio whitelist per ogni slot.
      - Bonificata la Sezione 7: rimosso il riferimento al banner `Alert - Wrong Stance` a favore della sola icona compatta `04 - Defensive Stance - OutOfStance warTank`.
    - **`docs/DESIGN.md`**:
      - Aggiornata la Sezione 4.5 con la formula di centratura orizzontale, la tabella di passo/dimensione e le regole tassative per trinket, anello (solo Ashen Band), mantello (solo ricamo Swordguard, soppressione totale del paracadute e statici), tier set (solo T10 4P), incanti arma (solo proc, statici soppressi), guanti (solo tinker), cooldown difensivi (fissi e integrati) e stivali.
      - Aggiornata la Sezione 4.6 con la filosofia Zero-Clutter ed eliminazione definitiva dei banner centrali `Alert - Sword and Board`, `Alert - Boss Enraged` e `Alert - Wrong Stance`.
    - **`docs/DECISIONS.md`**:
      - Aggiornato ADR-012 (filosofia Zero-Clutter su allarme postura con eliminazione del banner testuale).
      - Redatto e integrato **ADR-014**: "Architettura Riga Utility Auto-Adattiva a Centratura Dinamica con Filtri Selettivi Proc-Only per il War Tank".
    - **`docs/PRD.md`**:
      - Aggiornata la specifica dei Moduli 05 - 13 per la riga utility dinamica e la whitelist selettiva rigorosa.
      - Aggiornati i requisiti `FR-STANCE-01` e `17 - Alerts warTank` (zero banner invasivi per abilità rotazionali o postura).
    - **`docs/MEMORY.md`**:
      - Aggiunta la **Sezione 2.5**: "Specifica Tassativa della Riga Utility Auto-Adattiva e Filtri Item Proc-Only per il War Tank".
    - **`README.md` & `README_IT.md`**:
      - Formalizzata la riga utility dinamica ad auto-centratura e dettagliate le regole di whitelist (parità 1:1 bilingue).
    - **`HANDOFF.md` & `HANDOFF_IT.md`**:
      - Aggiornato lo stato dell'architettura della riga utility e registrata la conformità alle direttive utente.
  - [x] **Verifica e Compilazione**:
    - `python generate.py`: compilazione eseguita con successo.
    - `python scripts/sync_docs.py`: documentazione web sincronizzata.
    - `python tests/run_parallel_tests.py`: 10/10 test superati.
    - Esecuzione CP (Commit & Push su `origin/master`).

- [x] **Task 34: Parità Visiva Rigorosa e Multi-Proc Refresh Dinamico con Consumo Istantaneo per "Revenge Ready warTank" e "Sword and Board"**:
  - [x] **Direttiva Utente**:
    - *"Revenge Ready warTank" e "Sword and Board" devono essere simili nel modo in cui si mostrano, generare un task che crei questo fix, e inoltre, sia il primo che il secondo, oltre al fatto che giustamente spariscono se vengono usati, c'e da considerare che potrebbero proccare piu volte senza che io lo utilizzi, questo dovrebbe refresciare il tempo necessario per il lancio di una o del altra.*
  - [x] **Parità Visiva 1:1 tra Sword and Board e Revenge Ready**:
    - **Dimensioni & Layout**: Entrambe le icone dimensionate rigorosamente a $34 \times 34\text{ px}$ nel gruppo `01 - Procs warTank` (a $y = +52\text{ px}$, `space = 6`).
    - **Texture Fisse**: `auto: False` su entrambe con texture esplicite (`Interface\Icons\Ability_Warrior_SwordandBoard` e `Interface\Icons\Ability_Warrior_Revenge`).
    - **Opzioni Cooldown Uniformi**: `cooldown: True`, `cooldownSwipe: True`, `cooldownEdge: False` su entrambe (eliminata la lancetta gialla / bordo orologio da Revenge).
    - **Architettura Subregions a 3 Livelli Identica**:
      1. Sotto-sfondo: `{"type": "subbackground"}` su entrambe.
      2. Timer countdown decimale `%p`: ancorato a `INNER_BOTTOM`, dimensione font 11, `y_offset = 1`.
      3. Etichetta dell'abilità: `SLAM` (per Sword and Board) e `REV` (per Revenge Ready) ancorate a `INNER_TOP`, dimensione font 9, `y_offset = -2`.
    - **Effetto Glow Identico**: Gold Pixel Glow `[1.0, 0.84, 0.0, 1.0]` (8 linee, frequenza 0.25, lunghezza 10, spessore 2) configurato via `make_glow_action` su `actions.start`, nascosto su `actions.finish`.
  - [x] **Risoluzione Bug Offset Parametri CLEU in WotLK 3.3.5a**:
    - Risolto grave disallineamento nei parametri CLEU: in 3.3.5a il prefisso base contiene 8 argomenti (`timestamp, subEvent, sourceGUID, sourceName, sourceFlags, destGUID, destName, destFlags`).
    - Il codice precedente usava offset errati da Cataclysm (`select(12, ...)` per `missType`, `select(16, ...)` per `blocked`, `select(12, ...)` per `spellId`), rendendo inefficace il listener CLEU.
    - Corretti gli indici ufficiali 3.3.5a:
      - `SWING_MISSED`: `select(9, ...)` per `missType` (`"DODGE"`, `"PARRY"`, `"BLOCK"`).
      - `RANGE_MISSED` / `SPELL_MISSED`: `select(12, ...)` per `missType`.
      - `SWING_DAMAGE`: `select(13, ...)` per `blocked`.
      - `RANGE_DAMAGE` / `SPELL_DAMAGE`: `select(16, ...)` per `blocked`.
      - `SPELL_CAST_SUCCESS`: `select(9, ...)` per `spellId`.
  - [x] **Gestione Multi-Proc con Refresh Dinamico**:
    - **Revenge Ready**: Ad ogni successiva schivata, parata o blocco mentre Revenge è già attivo a schermo, il listener CLEU reimposta `_G.PWHUD_Revenge.start = GetTime()` e `duration = 5.0`, riavviando lo swipe da 5.0s completi.
    - **Sword and Board**: Ad ogni successivo proc di Devastate o Revenge (`SPELL_AURA_APPLIED` o `SPELL_AURA_REFRESH` su buff `50227`), il listener CLEU e il trigger reimpostano `_G.PWHUD_Sab.start = GetTime()` e `duration = 5.0`, riavviando lo swipe da 5.0s completi.
  - [x] **Consumo Istantaneo a 0 Latenza (Instant Cast Consumption)**:
    - Al lancio di *Shield Slam* (`SPELL_CAST_SUCCESS` su spell IDs `47486`, `47485`, `30356`, `25258`, `23925`, `23924`, `23923`, `23922`), `_G.PWHUD_Sab.start = 0` viene impostato istantaneamente, facendo sparire l'icona prima ancora della propagazione di `UNIT_AURA`.
    - Al lancio di *Revenge* (`SPELL_CAST_SUCCESS` su spell IDs `57823`, `6572`, `6574`, `7379`, `11601`, `25288`, `25269`, `30357`), `_G.PWHUD_Revenge.start = 0` viene impostato istantaneamente, facendo sparire l'icona con zero ritardo.
  - [x] **Simulatore Web & Test Suite**:
    - Aggiornato `docs/index.html`: `#procRev` uniformato con `pixel-glow-gold` e tooltip dettagliato sul multi-proc refresh.
    - Aggiornato `tests/test_target_debuffs.py` con test rigorosi di parità visiva (34x34px, auto=False, cooldownEdge=False, subbackground, timer %p, etichette SLAM/REV, gold pixel glow, CLEU 3.3.5a offsets).
    - Suite parallela: 10/10 test superati con successo in 0.46s.
    - Rigenerata stringa master `IMPORT_STRING_v5.21.8.txt` (73.198 caratteri).
    - Esecuzione CP (Commit & Push su `origin/master`).

- [x] **Task 35: Swing Timer Mano Primaria ad Animazione Progressiva e Accodamento Sincronizzato per 15 - Rotational Bar warTank**:
  - [x] **Direttiva Utente**:
    - *"15 - Rotational Bar warTank" non funziona come la barra che mostra lo scorrimento tra un attacco ed il successivo, deve funzionare in modo identico, solo che nel War Tank l'arma è una sola invece di due, facciamo il task e il fix.*
  - [x] **Architettura Aurabar con Swing Timer a Piena Larghezza ($274 \times 5\text{ px}$)**:
    - Trasformata `Rotational Bar - Base Bar warTank` da semplice texture statica ad `aurabar` reattiva ad aggiornamento `OnUpdate`.
    - Tracciamento della singola arma da mischia del tank (Main Hand) tramite `_G.PWHUD_GetSwing()`, con aggancio agli eventi CLEU (`SWING_DAMAGE`, `SWING_MISSED`, `SPELL_DAMAGE`, `SPELL_MISSED`, `SPELL_EXTRA_ATTACKS`) e `UNIT_ATTACK_SPEED`.
    - Mostra lo scorrimento continuo e fluido della barra (da 0% al 100%) tra ciascun attacco bianco e il successivo, con timer decimale residuo centrato (`%c`, es. `1.8s`).
    - Texture standard Warrior copper/bronze (`[0.65, 0.35, 0.12, 0.90]`).
  - [x] **Sincronizzazione Dinamica di Accodamento Heroic Strike & Cleave**:
    - `Rotational Bar - HS Queued warTank` e `Rotational Bar - Cleave Queued warTank` convertite in `aurabar` sincronizzate:
      - Condividono la medesima funzione di durata (`customDuration`) calcolata su `_G.PWHUD_Swing.mhStart + dur`.
      - Quando Heroic Strike o Cleave viene accodato a metà oscillazione, la barra non si blocca né riparte da zero: commuta istantaneamente colore (Oro per HS, Verde Smeraldo per Cleave) continuando lo scorrimento in perfetta continuità.
      - Attivazione istantanea del rispettivo Pixel Glow perimetrale (`PWHUD_HS_GLOW` o `PWHUD_CLEAVE_GLOW`).
      - All'esecuzione dell'attacco (`SPELL_DAMAGE` di HS o Cleave), lo swing timer si riavvia dallo 0% e l'effetto di accodamento svanisce istantaneamente.
  - [x] **Simulatore Web & Test Suite**:
    - Aggiornato `docs/index.html` con animazione continua del Main-Hand swing timer a 60fps (`requestAnimationFrame`) e timer numerico `%c` centrato.
    - Aggiornato `tests/test_rotational.py` con verifiche vincolanti sulla tipologia `aurabar`, tracciamento `UnitAttackSpeed` e timer `%c` centrato.
    - Suite parallela: 10/10 test superati con successo in 0.46s.
    - Rigenerata stringa master `IMPORT_STRING_v5.21.8.txt` (75.114 caratteri).
    - Esecuzione CP (Commit & Push su `origin/master`).
- [x] **Task 36: Ottimizzazione Testuale dello Stats Panel (Rimozione % Armor & SBV) e Riconfigurazione Geometrica Compatta (88x60px) con Armonizzazione del Cluster Buff Sovrastante (20x20px)**:
  - [x] **Direttiva Utente**:
    - *"fammi vedere % armor e di SBV non devono piu comparire riadatta le componenti in base a questa riduzione di testo, incluse le 4 componenti che stanno sopra task e fix"*
  - [x] **Rimozione Stringhe `% armor` e `SBV`**:
    - In `builder/components/stats.py` (`make_stats_custom_text`):
      - Rimosso `|cFF80D0FF(%.1f%%)|r` dalla riga Armatura: la stringa è ora semplicemente `Armor: %s%.1fk|r` (es. `Armor: 25.3k`). Mantenuta la colorazione dinamica in verde al raggiungimento del cap 75% DR.
      - Rimosso `|cFFFFD700(%d SBV)|r` dalla riga Blocco: la stringa è ora semplicemente `Block: |cFF80D0FF%.1f%%|r` (es. `Block: 21.7%`).
      - Risultato visivo: 5 righe ultra-pulite, compatte e prive di testo ridondante.
  - [x] **Riconfigurazione Geometrica Compatta dello Stats Panel ($88 \times 60\text{ px}$)**:
    - Riconfigurato il gruppo `18 - Stats Panel warTank` da $X = -216, Y = -49$ a $X = -190, Y = -45$.
    - Ridotto lo sfondo `Stats Panel - Background warTank` da $126 \times 60\text{ px}$ a $88 \times 60\text{ px}$.
    - Ancoraggio testo `Stats Panel - Text warTank` centrato con `xOffset = 2` e `justify = "LEFT"`, garantendo un margine interno perfetto senza clipping o spazi vuoti laterali.
  - [x] **Armonizzazione Geometrica delle 4 Componenti Sovrastanti ($20 \times 20\text{ px}$ con gap $2\text{ px}$)**:
    - Riconfigurati i 4 gruppi e icone sovrastanti:
      1. `02 - Battle Shout warTank`: $X = -223\text{ px}, Y = 0$, dimensione $20 \times 20\text{ px}$ (Active: font 9pt; OFF: font 8pt).
      2. `03 - Commanding Shout warTank`: $X = -201\text{ px}, Y = 0$, dimensione $20 \times 20\text{ px}$ (Active: font 9pt; OFF: font 8pt).
      3. `04b - Vigilance warTank`: $X = -179\text{ px}, Y = 0$, dimensione $20 \times 20\text{ px}$ (Active: font 9pt; OFF: font 8pt).
      4. `04 - Defensive Stance warTank`: $X = -157\text{ px}, Y = 0$, dimensione $20 \times 20\text{ px}$ (OutOfStance: font 7pt).
    - Passo uniforme di $22\text{ px}$ per icona ($20\text{ px}$ + $2\text{ px}$ spaziatura).
    - Estensione orizzontale complessiva: $86\text{ px}$ (da $X = -233$ a $X = -147$), perfettamente centrata sull'asse $X = -190$ del pannello statistiche sottostante con $1\text{ px}$ di margine simmetrico per lato.
  - [x] **Aggiornamento Simulatore Web & Test Suite**:
    - Aggiornato `docs/index.html`: `.left-col` e `.stats-panel-box` ridotti a $88\text{ px}$, icone convertite a `.size-20`, rimossi i frammenti `(62.4%)` e `(1800 SBV)`.
    - Aggiornati i test `tests/test_tree_layout.py`, `tests/test_stats_panel.py` e `tests/test_danger_alerts.py`.
    - Suite parallela: 10/10 test superati con successo in 0.38s.
    - Rigenerata stringa master `IMPORT_STRING_v5.21.8.txt` (75.077 caratteri).
    - Esecuzione CP (Commit & Push su `origin/master`).
- [x] **Task 37: Armonizzazione delle 4 Icone Sovrastanti a 24x24px e Riconfigurazione Geometrica dello Stats Panel a 96x60px**:
  - [x] **Direttiva Utente**:
    - *"leggermenti piu grandi è meglio le 4 icone di sopra"* (con allegato screenshot in-game del pannello compatto).
  - [x] **Ingrandimento Visivo delle 4 Icone Sovrastanti ($24 \times 24\text{ px}$ con gap $2\text{ px}$)**:
    - Incrementata la dimensione delle 4 icone da $20 \times 20\text{ px}$ a $24 \times 24\text{ px}$ (+20% in scala lineare, +44% in superficie visibile), rendendo i volti e le illustrazioni dei buff nitidi e perfettamente leggibili:
      1. `02 - Battle Shout warTank`: $X = -231\text{ px}, Y = 0$, dimensione $24 \times 24\text{ px}$ (Active: font 10pt; OFF: font 9pt).
      2. `03 - Commanding Shout warTank`: $X = -205\text{ px}, Y = 0$, dimensione $24 \times 24\text{ px}$ (Active: font 10pt; OFF: font 9pt).
      3. `04b - Vigilance warTank`: $X = -179\text{ px}, Y = 0$, dimensione $24 \times 24\text{ px}$ (Active: font 10pt; OFF: font 9pt).
      4. `04 - Defensive Stance warTank`: $X = -153\text{ px}, Y = 0$, dimensione $24 \times 24\text{ px}$ (OutOfStance: font 8pt).
    - Passo regolare a $26\text{ px}$ ($24\text{ px}$ + $2\text{ px}$ spaziatura) con ampiezza totale di $102\text{ px}$ (da $X = -243$ a $X = -141$).
  - [x] **Allineamento Geometrico dello Stats Panel ($96 \times 60\text{ px}$ a $X = -192, Y = -45$)**:
    - Riconfigurato `18 - Stats Panel warTank` a $X = -192, Y = -45$ con sfondo $96 \times 60\text{ px}$ (da $X = -240$ a $X = -144$).
    - Garantisce una perfetta simmetria visiva con le icone sovrastanti (3px di margine per lato), 5px di respiro rispetto alla barra della rabbia e 10px rispetto alla riga utility.
    - Offre eccellente respiro alla riga più lunga `Hit: 9.1% | 25 Exp` senza alcuna compressione visiva sui bordi.
  - [x] **Aggiornamento Simulatore Web & Test Suite**:
    - Aggiornato `docs/index.html` con classi `.size-24` e colonna a $96\text{ px}$.
    - Aggiornati i test `tests/test_tree_layout.py` e `tests/test_danger_alerts.py`.
    - Suite parallela: 10/10 test superati con successo in 0.44s.
    - Rigenerata stringa master `IMPORT_STRING_v5.21.8.txt` (75.080 caratteri).
    - Esecuzione CP (Commit & Push su `origin/master`).
- [x] **Task 38: Revisione Castbar warTank (Scorrimento Player dx->sx, Icona Dinamica della Spell, Priorità Assoluta del Target e Untrigger Immediato su Kick/Interruzione)**:
  - [x] **Direttiva Utente**:
    - *"dobbiamo generare un task che vada a fixxare '16 - Castbar warTank': questa barra deve riportare la spell che io sto lanciando, mostrando il caricamento da destra verso sinistra, e se io la interrompo questa deve fermarsi pure, anche l'icona che viene mostrata deve essere la spell di riferimento, se invece il target sta per castarmi qualcosa questa è prioritaria e deve nascondere quella secondaria, se avviene il kick da parte mia o di qualcunaltro allora anche la primaria che scorre da destra verso sinistra deve annullarsi, riusciamo a fare questa modifica?"*
  - [x] **Scorrimento Unificato da Destra verso Sinistra (`inverse = True`)**:
    - `Castbar - Player warTank`: convertita da `inverse: False` a `inverse: True`, garantendo la medesima direzione di riempimento naturale da destra a sinistra richiesta per l'HUD.
  - [x] **Risoluzione Bug Icona Dinamica della Spell del Player (`iconSource = 0` & Multi-Return Lua Fix)**:
    - Risolto il blocco statico dell'icona: `iconSource` impostato a `0` (Trigger Icon) anziché `-1` (Manual Icon).
    - Risolto il troncamento dei valori multipli in Lua (`local a, b, c, d = func1() or func2()` che scartava i ritorni successivi al primo): ora `UnitCastingInfo("player")` estrae correttamente il 4° parametro `icon`, con fallback condizionale pulito su `UnitChannelInfo("player")`.
    - L'icona visualizzata corrisponde all'istante e fedelmente all'incantesimo o canalizzazione in esecuzione dal tank.
  - [x] **Priorità Assoluta del Target & Soppressione Istantanea**:
    - Quando il target nemico inizia un lancio (`UnitCastingInfo("target")` o `UnitChannelInfo("target")`), la castbar secondaria del giocatore si auto-sopprime immediatamente, cedendo il 100% dell'area alla barra primaria del bersaglio con l'advisor di kick/reflect.
  - [x] **Risoluzione Bug Untrigger su Kick e Interruzioni**:
    - Risolto il blocco del mancato untrigger (`untrigger: function() return false end`): in precedenza la barra rimaneva visibile a schermo anche dopo un kick o l'interruzione del movimento perché l'untrigger restituiva `false`.
    - In `Castbar - Target warTank`: `untrigger` verifica `ki == nil`, cancellando e nascondendo istantaneamente la barra nel momento esatto in cui il bersaglio viene interrotto (da un kick del giocatore o di qualsiasi alleato nel gruppo/raid).
    - In `Castbar - Player warTank`: `untrigger` verifica `spell == nil` o `targetSpell ~= nil`, interrompendo all'istante la barra se il giocatore si muove, salta o annulla il lancio, oppure se il bersaglio nemico inizia un cast prioritario.
  - [x] **Aggiornamento Simulatore Web & Test Suite**:
    - Aggiornato `docs/index.html` con gradiente e riempimento `player` da destra verso sinistra (`float: right`).
    - Aggiornato `tests/test_interrupts.py` con verifiche vincolanti su `inverse = True` per entrambe le barre, `iconSource = 0` e presenza del controllo `ki == nil` e `spell == nil` negli untrigger.
    - Suite parallela: 10/10 test superati con successo in 0.46s.
    - Rigenerata stringa master `IMPORT_STRING_v5.21.8.txt` (75.792 caratteri).
    - Esecuzione CP (Commit & Push su `origin/master`).
- [x] **Task 39: Risoluzione Definitiva Icona Castbar warTank (Eliminazione Punto Interrogativo Rosso, Abilitazione `auto = True`, Unpacking API WotLK 3.3.5a per `UnitChannelInfo` e Override Diretto Frame)**:
  - [x] **Direttiva Utente**:
    - *"questo va risolto"* (screenshot con icona a punto interrogativo rosso `INV_Misc_QuestionMark` su castbar attiva).
  - [x] **Causa Radice Identificata**:
    1. WeakAuras gestisce l'icona dell'aurabar verificando `if not data.auto and data.displayIcon then icon = data.displayIcon end`. Avendo impostato `auto: False` con `displayIcon: "Interface\Icons\INV_Misc_QuestionMark"`, WeakAuras ignorava il valore calcolato da `customIcon` e forzava su ogni fotogramma il punto interrogativo rosso (`INV_Misc_QuestionMark`).
    2. Nelle chiamate canalizzate (`UnitChannelInfo`), la firma API di WotLK 3.3.5a restituisce `name, text, texture, startTimeMS, endTimeMS` (la texture è il 3° parametro, senza `rank`). La precedente estrazione trattava il 4° parametro come texture, che corrispondeva a `startTimeMS` (un timestamp numerico), provocando fallback errati o errori aritmetici nei calcoli di durata.
  - [x] **Implementazione Fix**:
    - `auto: True`: abilitato il recupero automatico dell'icona dal trigger per entrambe le castbar (`Castbar - Target warTank` e `Castbar - Player warTank`).
    - Eliminato qualsiasi riferimento a `INV_Misc_QuestionMark`, impostando `displayIcon: "Interface\Icons\Temp"`.
    - Integrato fallback robusto via `GetSpellTexture(spell)` sia in target che in player castbar.
    - Gestione distinta e sicura dei parametri di `UnitChannelInfo` conforme alle API WotLK 3.3.5a (`cName, cText, cTexture, cStart, cEnd`).
    - Applicazione diretta a livello di frame UI: `aura_env.region.icon:SetTexture(icon)` in `customText` e `customIcon` per garantire l'aggiornamento immediato e senza latenza dell'icona a schermo.
  - [x] **Validazione & Collaudo**:
    - Aggiornati test in `tests/test_interrupts.py` con verifiche vincolanti su `auto == True`, assenza di `INV_Misc_QuestionMark`, presenza di `GetSpellTexture` e `SetTexture`.
    - Test Suite parallela: 10/10 PASS in 0.51s.
    - Rigenerata stringa master `IMPORT_STRING_v5.21.8.txt` (76.253 caratteri).
    - Commit & push su `origin/master`.

- [x] **Task 40: Risoluzione Errore Lua in "Alert - Kick Now" (Filtro Bersaglio Ostile `UnitCanAttack`, Eliminazione Duplicate Kick Logic Obsoleta in `utility.py` con Mismatch Signature `UnitChannelInfo`, Supporto Spell Localizzate IT e Untrigger Pulito)**:
  - [x] **Direttiva Utente**:
    - *"cosa sarebbe e come si potrebbe fixxare?"* (screenshot in-game con errore `WeakAuras: Aura 'Alert - Kick Now': This aura has caused a Lua error` subito dopo che i membri del gruppo Spaktut e Cattiva hanno confermato il ruolo per il dungeon).
  - [x] **Analisi Cause Radice**:
    1. **Errore Aritmetico su Boolean (`UnitChannelInfo`)**: `builder/components/utility.py` conteneva una vecchia definizione duplicata di `_G.PWHUD_GetKickInfo` (risalente a versioni precedenti del builder) che scompattava `UnitChannelInfo` con un offset errato, assegnando il 6° valore di ritorno (`isTradeSkill`, di tipo booleano) a `endTime`. Nel calcolo del tempo residuo `(endTime / 1000 - now)`, l'interprete Lua 5.1 di WoW 3.3.5a sollevava l'eccezione irreversibile `attempt to perform arithmetic on a boolean value` non appena un alleato o compagno di gruppo avviava un channel o un craft.
    2. **Assenza Filtro di Ostilità (`UnitCanAttack`)**: Né `_G.PWHUD_GetTargetCastInfo` né `Alert - Kick Now` verificavano l'ostilità del bersaglio (`UnitCanAttack("player", "target")`). Se il tank selezionava un membro del party o un NPC alleato intento a castare (cura, buff, pietra del focolare, craft), l'aura tentava di calcolare l'avviso di kick su un alleato.
    3. **Untrigger Corrotto (`return false`)**: Il trigger dell'avviso `Alert - Kick Now` definiva `"untrigger": {"type": "custom", "custom": "function() return false end"}`. In WeakAuras per 3.3.5a, restituire `false` nell'untrigger impedisce la disattivazione e il ciclo di cleanup dell'aura, lasciandola in uno stato orfano in cui il codice `customText` riceveva parametri `nil`.
    4. **Mancanza Localizzazione Nomi Spell IT**: Le chiamate ad `IsSpellInRange` controllavano solo i nomi in inglese (*Shield Bash*, *Pummel*), mancando le denominazioni del client italiano (*Colpo di Scudo*, *Percossa*).
  - [x] **Implementazione Soluzione**:
    - `builder/components/bars.py`: aggiunto controllo perentorio `if not UnitExists("target") or not UnitCanAttack("player", "target") or UnitIsDead("target") then return nil end` nella funzione globale `_G.PWHUD_GetTargetCastInfo()`. Integrati i nomi italiani (*Colpo di Scudo*, *Percossa*) nelle tuple di interrupt.
    - `builder/components/utility.py`: rimossa definitivamente la definizione obsoleta e ridondante di `_G.PWHUD_GetKickInfo`, delegando in modo centralizzato ed ermetico a `_G.PWHUD_GetTargetCastInfo()`.
    - `builder/components/alerts.py`: aggiunto controllo `UnitCanAttack("player", "target")` in `customText`, e aggiornato l'untrigger per restituire `true` (immediato cleanup e disattivazione) non appena il bersaglio non esiste, è morto, è amichevole o non presenta cast interrompibili.
  - [x] **Validazione & Collaudo**:
    - Aggiornati test in `tests/test_interrupts.py` con verifiche vincolanti su `UnitCanAttack` in `customText` e `ki == nil` nell'untrigger di `Alert - Kick Now`.
    - Test Suite parallela: 10/10 test superati con successo in 0.40s.
    - Rigenerata stringa master `IMPORT_STRING_v5.21.8.txt` (76.853 caratteri).
    - Esecuzione CP (Commit & Push su `origin/master`).
