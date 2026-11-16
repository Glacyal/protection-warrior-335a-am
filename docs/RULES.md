# Development Rules & Coding Standards — Protection Warrior 3.3.5a Suite

## 1. Principi di Sviluppo Non Negoziabili

1. **Compiler-Driven Source of Truth**:
   - I file Python in `builder/` sono l'unica fonte di verità.
   - Nessuna modifica deve essere apportata manualmente esportando da WoW: ogni cambiamento si effettua nel codice Python, si verifica con i test e si compila tramite `python generate.py`.

2. **Isolamento e Integrità dei Nomi Globali Lua**:
   - Tutte le funzioni e variabili Lua globali registrate in `_G` **devono** avere il prefisso riservato `PWHUD_` (es. `_G.PWHUD_InitCore`, `_G.PWHUD_BuffCache`, `_G.PWHUD_DebuffCache`).
   - È severamente vietato sovrascrivere o inquinare variabili globali Blizzard o di altri addon (es. non usare mai `buffCache`, `t1`, `calcStats` come globali non prefissate).

3. **Integrità delle Mappe Trigger (Regola Vincente Antigravity)**:
   - All'interno del dizionario `"triggers"` di ogni aura WeakAuras, le chiavi dei trigger devono essere **interi numerici** (`1: { ... }`) e **mai stringhe** (`"1": { ... }`).
   - Le chiavi stringa provocano il blocco irreversibile dell'importatore di WeakAuras in gioco perché AceSerializer le serializza come hash map `^S1` anziché come array index `^N1`, rendendo inaccessibile l'elemento tramite `ipairs` o `triggers[1]`.
   - Ogni aura dotata di triggers deve includere `"activeTriggerMode": -10`.

4. **Conformità Dual-Key per SubRegions**:
   - Ogni elemento di tipo `subtext` in `subRegions` deve implementare la sintassi a doppia chiave (snake_case + camelCase) per garantire interoperabilità trasparente tra i fork 4.0.0 e 5.21.8+ di WeakAuras:
     - `anchor_point` e `anchorPoint`
     - `text_anchorPoint`
     - `anchorXOffset` e `text_anchorXOffset`
     - `anchorYOffset` e `text_anchorYOffset`
   - Le auras ad icona devono includere `{"type": "subbackground"}` come primo elemento (`index 0`) per assicurare il rendering corretto dello sfondo Blizzard.

5. **Vincolo Dimensionale delle Barre Orizzontali**:
   - La larghezza delle tre barre orizzontali (`14 - Rage Bar`, `15 - Rotational Bar`, `16 - Castbar warTank`) deve essere **esattamente 278 px**. Nessun componente centrale può violare questa metrica di simmetria.

---

## 2. Standard Lua per WotLK 3.3.5a (Client Build 12340)

1. **Nessun Impiego di API Moderne non Retrocompatibili**:
   - È vietato l'uso di API introdotte nelle espansioni successive (es. `C_Timer.After`, `C_Spell.*`, `GetSpecialization`, `UnitAura` con filtri moderni non supportati).
   - Impiegare esclusivamente le API native 3.3.5a:
     - `UnitBuff(unit, index)` e `UnitDebuff(unit, index)`
     - `UnitCastingInfo("target")` e `UnitChannelInfo("target")`
     - `GetInventoryItemID("player", slot)` e `GetInventoryItemCooldown("player", slot)`
     - `GetSpellCooldown(spellName)`
     - `GetShapeshiftForm()`
     - `UnitAffectingCombat("player")`
     - `UnitHealth("player")` e `UnitHealthMax("player")`

2. **Garbage Collection e Prestazioni a 60 FPS**:
   - In funzioni a frequenza elevata (`check: "update"`), evitare la creazione continua di tabelle anonime temporanee.
   - Utilizzare il throttling temporale (`GetTime() - lastUpdate > 0.1`) per le scansioni del pannello statistiche (frequenza massima 10 Hz).
   - Riutilizzare le tabelle di cache globale anziché ricrearle ad ogni frame.

---

## 3. Standard di Test ed Esecuzione Locale

1. Prima di ogni commit Git, è obbligatorio eseguire la test suite parallela completa:
   ```powershell
   python tests/run_parallel_tests.py
   ```
2. Tutti gli 8 script di test devono superare le asserzioni con esito `PASS`:
   - `test_components_integrity.py`
   - `test_tree_layout.py`
   - `test_stats_panel.py`
   - `test_lua.py`
   - `test_defensives.py`
   - `test_interrupts.py`
   - `test_string_sync.py`
   - `test_danger_alerts.py`
3. Dopo ogni modifica al modello dei componenti, sincronizzare la stringa di importazione nel simulatore web:
   ```powershell
   python generate.py
   python scripts/sync_docs.py
   ```

---

## 4. Standard Bilingue Documentazione & HTML in Inglese (Regola Non Negoziabile)

1. **Doppia Lingua Obbligatoria per Documentazione Radice**:
   - **`README.md`** (Inglese, primario) e **`README_IT.md`** (Italiano, secondario).
   - **`HANDOFF.md`** (Inglese, primario) e **`HANDOFF_IT.md`** (Italiano, secondario).
   - I file devono mantenere **rigorosa coerenza e parità 1:1** in termini di struttura gerarchica, sezioni, tabelle, badge, code snippet e metadati, differendo unicamente per la lingua.
   - Ogni modifica futura a `README` o `HANDOFF` deve essere applicata **contemporaneamente a entrambe le versioni** prima del commit.
2. **HTML Esclusivamente in Inglese**:
   - [`docs/index.html`](file:///D:/0Progetti/protection-warrior-335a-am/docs/index.html) (Live Web Simulator) deve essere **puramente in lingua inglese** in ogni sua componente testuale: titoli, sottotitoli, pulsanti, scenari/preset, controlli slider, messaggi toast, allarmi e tabelle documentali/glossario.
