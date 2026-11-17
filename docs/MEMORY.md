# Project Memory & Knowledge Base — Protection Warrior 3.3.5a

Questo documento raccoglie la memoria tecnica, le particolarità delle API WotLK 3.3.5a (Build 12340) e le soluzioni ai problemi noti scoperti durante lo sviluppo della suite.

---

## 1. Caratteristiche e Peculiarità delle API WotLK 3.3.5a

### 1.1 `UnitCastingInfo` e `UnitChannelInfo`
- **Firma di Ritorno**:
  ```lua
  local name, subText, text, texture, startTime, endTime, isTradeSkill, castID, notInterruptible = UnitCastingInfo(unit)
  ```
- **Peculiarità del nono parametro (`notInterruptible`)**:
  - Se `notInterruptible == true` o `1`, il cast del boss **non può essere interrotto** (es. abilità speciali scripted, Soul Reaper di LK, ecc.).
  - Se `notInterruptible == false` o `nil`, il cast è **interrompibile**.
  - In WotLK 3.3.5a, `UnitChannelInfo` ritorna una firma equivalente. La nostra Castbar controlla entrambi i canali e adatta istantaneamente il colore (Ciano se kiccabile, Grigio scuro con `[IMMUNE]` se protetto).

### 1.2 Gestione degli Slot d'Inventario e Cooldown
- Gli slot rilevanti per il Guerriero Protezione sono:
  - `Slot 8`: Scarpe (Boots / Nitro Boosts Ingegneria).
  - `Slot 10`: Guanti (Gloves / Pyro-Rocket / Hyperspeed / Armatura).
  - `Slot 11 & 12`: Anelli (Ring / Ashen Band).
  - `Slot 13 & 14`: Monili (Trinkets).
  - `Slot 15`: Mantello (Cloak / Paracadute o ricami).
  - `Slot 17`: Mano Secondaria (Shield).
- **Controllo dello Scudo Equipaggiato**:
  ```lua
  local itemLink = GetInventoryItemLink("player", 17)
  -- Per verificare se è uno scudo:
  local _, _, _, _, _, itemType, itemSubType = GetItemInfo(itemLink)
  -- itemSubType == "Shields" o "Scudi"
  ```
  In alternativa per le macro veloci in combattimento:
  ```lua
  local hasShield = (GetInventoryItemID("player", 17) ~= nil)
  ```
  Se il tank ha disequipaggiato per sbaglio lo scudo o sta impugnando un'arma 2H, `Shield Bash` non è utilizzabile; il Kick Advisor suggerisce automaticamente `Pummel` se in Berserker Stance o segnala la mancanza dello scudo.

### 1.3 `GetShapeshiftForm()` per il Guerriero
- In WotLK 3.3.5a:
  - `GetShapeshiftForm() == 1`: Battle Stance (Postura di Battaglia).
  - `GetShapeshiftForm() == 2`: **Defensive Stance (Postura Difensiva)**.
  - `GetShapeshiftForm() == 3`: Berserker Stance (Postura Berserker).
- Il tank deve rimanere in **Stance 2** per beneficiare del -10% danno subito, +threat e abilitare Revenge e Shield Wall. Il nostro modulo `04 - Defensive Stance` si attiva con allarme rosso e scritta `STANCE` appena il tank si trova in combattimento in Stance 1 o 3.

---

## 2. Risoluzione dei Bug Noti

### 2.1 Freeze dell'Importazione WeakAuras ("si è bloccato l'import")
- **Sintomo**: Copiando la stringa e incollandola nella casella di import di WeakAuras in gioco, la finestra si bloccava senza aprire il popup di conferma ("Import / Upgrade / Ignore").
- **Causa Analizzata**:
  In `builder/components/utility.py`, i dizionari `triggers` utilizzavano `"1": { ... }` con chiave stringa anziché intero `1: { ... }`.
  - AceSerializer codificava `"1"` come `^S1`.
  - WeakAuras internamente fa affidamento su tabelle indicizzate come array per i trigger: `for i, trigData in ipairs(auraData.triggers) do`.
  - Trovando un buco all'indice numerico `1`, la migrazione dei trigger falliva entrando in un loop infinito o tentando di accedere a campi di un oggetto `nil`.
- **Risoluzione Definitiva**:
  1. Tutti i componenti usano la chiave numerica intera `1:` nei dizionari `triggers`.
  2. Aggiunto `"activeTriggerMode": -10` obbligatorio in ogni blocco trigger.
  3. Aggiunta asserzione bloccante in `tests/test_components_integrity.py`.

### 2.2 Sincronizzazione SubRegions Dual-Key
- **Sintomo**: Nelle versioni moderne o biforcate di WeakAuras (es. 5.21.8+ per 3.3.5a), le etichette di testo dei cooldown e dei nomi apparivano posizionate erroneamente nell'angolo in basso a sinistra anziché centrate.
- **Causa**: WeakAuras 5.21.8+ richiede proprietà camelCase con prefisso `text_` (es. `text_anchorPoint`, `text_anchorXOffset`), mentre versioni più vecchie leggevano `anchor_point`, `anchorXOffset`.
- **Soluzione**: La funzione ausiliaria `make_subtext` in `builder/core/helpers.py` inietta contemporaneamente entrambe le chiavi:
  ```python
  {
      "type": "subtext",
      "text_text": text,
      "text_font": font,
      "text_fontSize": font_size,
      "text_fontType": font_type,
      "text_justify": justify,
      "text_anchorPoint": anchor_point,
      "anchor_point": anchor_point,
      "anchorPoint": anchor_point,
      "text_anchorXOffset": x_offset,
      "anchorXOffset": x_offset,
      "text_anchorYOffset": y_offset,
      "anchorYOffset": y_offset,
      "text_visible": True,
  }
  ```

---


### 2.3 Divieto Assoluto di Banner Testuali Centrali per Proc e Divieto di Spell ID Talenti Passivi
- **Regressione Analizzata (Sintomo)**:
  Nella schermata di gioco compariva una gigantesca scritta testuale gialla **`SHIELD SLAM READY!`** fissa al centro dello schermo anche da fermi in città, fuori combattimento e con 0 rabbia.
- **Root Cause Tecniche**:
  1. **Duplicazione Invasiva**: Esisteva un'aura testuale centrale ridondante `Alert - Sword and Board` dentro `17 - Alerts warTank` che stampava testo a 20pt al centro dello schermo. Il proc di Sword and Board è già tracciato in modo pulito e completo dall'icona compatta con timer in `01 - Procs warTank`.
  2. **Spell ID di Talento Passivo (`46953`)**: Il trigger `aura2` conteneva `spellIds: [46953, 50227]`. In WotLK 3.3.5a, `46953` è lo Spell ID del **talento passivo** (Rango 1) nel ramo Protezione. Avendo il talento appreso nell'albero, il motore di WeakAuras rilevava il talento permanentemente attivo sul giocatore, mantenendo la scritta `SHIELD SLAM READY!` sempre visibile a schermo.
- **Regole Architetturali Tassative (DA NON RIPETERE MAI)**:
  1. **Nessun Banner Testuale per Proc Rotazionali**: Tutti i proc del giocatore (`Sword and Board`, `Revenge Ready`, `Shield Block`, ecc.) devono vivere **esclusivamente come icone compatte** all'interno del gruppo dinamico `01 - Procs warTank`. È severamente vietato creare o mantenere banner testuali invasivi centrali per abilità rotazionali.
  2. **Divieto di Spell ID di Talenti Passivi nei Trigger Buff**: Nei trigger `aura2` o nei controlli `UnitBuff` / `UnitDebuff`, verificare sempre che gli ID corrispondano esclusivamente al **buff temporaneo** applicato dal proc (es. `50227` per il proc Sword and Board) e MAI agli ID del talento passivo (es. `46953`).
  3. **Zero Clutter Centrale**: Il gruppo `17 - Alerts warTank` è riservato unicamente ad allarmi critici di raid/sopravvivenza estrema (`Alert - Emergency CD`, `Alert - Kick Now`); tutti i banner testuali non essenziali (`Alert - Boss Enraged`, `Alert - Wrong Stance`, `Alert - Sword and Board`) sono stati eliminati definitivamente.

---


### 2.4 Il Gruppo Radice WeakAuras NON Esegue `actions.init`: Inizializzazione Core Tassativa nel Trigger di Trinket 1
- **Regressione Analizzata (Sintomo)**:
  Tutti i trinket (Slot 13 e 14), l'anello, il mantello, i bonus tier e i guanti della riga utility erano **completamente spariti** a schermo, e la riga non si auto-adattava più: rimanevano solo le 3 icone dei difensivi guerriero (`Shield Block`, `Shield Wall`, `Last Stand`) sbilanciate e bloccate a destra ($x = 28, 56, 84$).
- **Root Cause Tecnica**:
  In WeakAuras per WotLK 3.3.5a, i nodi di tipo `group` (come il master group `Class Warrior (Protection)`) **NON sono regioni visive attive** e il motore di WeakAuras **NON esegue mai il loro blocco `actions.init`**.
  Tentando di deduplicare il codice inserendo `_G.PWHUD_InitCore` dentro `tree["d"]["actions"]["init"]`:
  - `_G.PWHUD_InitCore` non veniva mai definito in memoria WoW.
  - Di conseguenza `_G.PWHUD_CheckSlotEquipped` era `nil`, facendo restituire `false` a tutti gli slot equipaggiati (facendo sparire trinket, anello, mantello, ecc.).
  - Di conseguenza `_G.PWHUD_UpdateUtilityRowPositions` era `nil`, impedendo alla barra di calcolare `activeOrder` e di auto-centrarsi.
- **Regola Architetturale Tassativa (DA NON RIPETERE MAI)**:
  1. **MAI affidare l'inizializzazione del core globale ad `actions.init` di un gruppo container**: in WeakAuras 3.3.5a l'inizializzazione deve essere compilata ed eseguita all'interno della prima aura reattiva garantita, nello specifico il trigger di **`05 - Trinket 1 warTank` (`slot == 13`)**.
  2. In questo modo, appena WeakAuras compila il trigger di Trinket 1 all'avvio:
     - `_G.PWHUD_InitCore` viene compilato ed eseguito immediatamente.
     - Tutte le funzioni di scansione slot (`_G.PWHUD_CheckSlotEquipped`, `_G.PWHUD_CheckSlot`, `_G.PWHUD_UpdateUtilityRowPositions`, `_G.PWHUD_CheckTargetDebuff`, `_G.PWHUD_CheckTankBusters`) vengono registrate istantaneamente in `_G`.
     - Tutti i trinket ricompaiono e la riga si auto-adatta fluidamente centrandosi sotto la barra rabbia.

---

## 3. Catalogo Debuff Letali dei Boss Monitorati

| Nome Debuff | Spell ID | Incontro Raid | Soglia Allarme / Azione Richiesta |
| :--- | :--- | :--- | :--- |
| **Soul Reaper** | `69409`, `73797`, `73798`, `73799` | The Lich King (ICC 10/25) | Allerta immediata: infligge 50.000 danno ombra dopo 5s. Attivare Shield Wall o chiamare Taunt Swap. |
| **Impale** | `67477`, `67478`, `67479` | Gormok the Impaler (ToC) | Allerta a cariche `>= 2`. Danno emorragia cumulativo letale. Chiamare Taunt Swap. |
| **Gastric Bloat** | `72219`, `72551`, `72552`, `72553` | Festergut (ICC 10/25) | Allerta a cariche `>= 8` (esplosione a 10 cariche). Taunt Swap obbligatorio prima della 10ª carica. |
| **Fusion Punch** | `62876`, `64597` | XT-002 Deconstructor (Ulduar) | Allerta immediata: colpo da 35k-40k fisico + 20k fuoco al secondo. Attivare Shield Block / Shield Wall. |
| **Enrage / Berserk / Frenzy** | Varie | Varie (Saurfang, Halion, ecc.) | Allarme sonoro e visivo magenta per attivazione difensiva immediata o Tranquilizing Shot. |

---

## 4. Memoria Tecnica: Indici Talenti e Condizioni di Caricamento

### 4.1 Mappatura Matematica Indice Talento WotLK 3.3.5a
In WeakAuras 3.3.5a, la funzione `WeakAuras.CheckTalentByIndex(index)` non usa spell ID ma un indice lineare:
- Formula: $\text{tab} = \lceil \text{index} / 40 \rceil$, $\text{num\_talent} = ((\text{index} - 1) \bmod 40) + 1$.
- Per il Guerriero:
  - Tab 1 = Arms
  - Tab 2 = Fury (es. Rampage = 64, ovvero $(2-1)*40 + 24$)
  - Tab 3 = Protection (27 talenti totali)
- Nel ramo Protection (Tab 3), **Devastate** (Spell ID: `20243`) si trova al Tier 8, Colonna 1, occupando l'ordinale **23**.
- Indice lineare WeakAuras: $(3 - 1) \times 40 + 23 = \mathbf{103}$.
- Configurazione vincolante: `"talent": {"single": 103, "multi": {103: True}}`.

### 4.2 Controllo Postura Difensiva (Stance Check)
- Postura Difensiva = Form 2 (`GetShapeshiftForm() == 2`).
- Doppio allarme implementato:
  1. Icona `04 - Defensive Stance - Warning` (X: -158, Y: 0) con Pixel Glow rosso e label `STANCE`.
  2. Testo centrale `Alert - Wrong Stance` (Y: +64) con `>> DEFENSIVE STANCE REQUIRED! <<` e suono `RaidWarning.ogg`.
- Trigger event-driven su `PLAYER_REGEN_DISABLED, PLAYER_REGEN_ENABLED, UPDATE_SHAPESHIFT_FORM`. Zero polling su `OnUpdate`.

---

## 5. Glossario Dettagliato delle Sigle Statistiche Tank (WotLK 3.3.5a)

| Sigla | Termine Esteso | Definizione Meccanica & Ruolo nel Tanking WotLK |
| :--- | :--- | :--- |
| **`DEF`** | **Defense Skill** | Abilità di difesa del personaggio (`base + rating`). Base a Lv.80 = 400. Raggiungere **540 Difesa** (+140 da rating/talenti) garantisce la completa **immunità ai colpi critici** dei Boss Raid Lv.83 (-5.6% crit subito). In Dungeon Eroici (mob Lv.82) il cap è **535**. |
| **`ARM`** | **Effective Armor & Physical DR%** | Armatura effettiva istantanea del guerriero. La percentuale tra parentesi è il **Physical Damage Reduction** contro boss Lv.83: $\text{DR}\% = \min(75.0, \frac{\text{Armor}}{\text{Armor} + 16635} \times 100)$. Hard cap al 75% (49.905 armatura). Include buff (*Inspiration/Ancestral Fortitude* +25%, *Stoneskin/Devotion*) e debuff (*Sunder/Acid/Faerie Fire/Melt Armor*). |
| **`CTC`** | **Combat Table Coverage** | Copertura totale della tabella colpi: $\text{Dodge} + \text{Parry} + \text{Block} + \text{BossMiss}$. A $\ge \mathbf{102.4\%}$ il tank è **Unhittable**: nessun colpo bianco del boss può andare a segno normale (vengono tutti schivati, parati, bloccati o mancati). Gestisce debuff non-stacking (*Insect Swarm* o *Scorpid Sting* max +3% Miss). |
| **`Block`** | **Block Chance** | Probabilità di bloccare un attacco fisico con lo scudo. Durante l'abilità attiva *Shield Block* (10s) raggiunge il 100%, portando istantaneamente il CTC oltre il 102.4%. |
| **`SBV`** | **Shield Block Value** | Quantità di danno fisico assorbito da ciascun blocco riuscito. In WotLK 3.3.5a è anche il moltiplicatore primario che scala il danno e la minaccia generata da **Shield Slam** (Colpo di Scudo). |
| **`Hit`** | **Melee Hit Chance** | Precisione degli attacchi speciali e di *Taunt*. Cap contro boss Lv.83 a **8.0%** (263 rating), ridotto al 7.0% con *Heroic Presence* Draenei (+1%). |
| **`Exp`** | **Expertise** | Perizia/Competenza: **Soft Cap 26** (214 rating, azzera le Schivate del boss dal fronte). **Hard Cap 56** (azzera le Parate del boss dal fronte, fondamentale per eliminare il rischio di *Parry-Haste* su Sindragosa, Halion, Lady Deathwhisper). |
| **`Avoid`** | **Avoidance Pura** | Somma di $\text{Dodge} + \text{Parry} + \text{Miss}$: percentuale di colpi in cui il tank incassa **zero danni** (a differenza del blocco dove il danno viene solo assorbito parzialmente). |
| **`DR%`** | **Damage Reduction %** | Percentuale passiva di mitigazione fisica garantita dall'armatura effettiva. |
| **`EHP`** | **Effective Health Pool** | Salute effettiva: $\text{EHP} = \frac{\text{Max HP}}{1 - (\text{DR}\% / 100)}$. |
| **`GCD`** | **Global Cooldown** | Finestra standard di recupero tra abilità (1.5s). |
| **`ICD`** | **Internal Cooldown** | Tempo di ricarica interno dei proc dei monili (tipicamente 45s o 50s). |

---

## 6. Standard di Bilinguismo della Documentazione & Lingua del Simulatore Web

- **Lingua Principale**: **Inglese**. I file radice principali per gli utenti e per gli sviluppatori sono scritti in inglese:
  - `README.md` (Inglese)
  - `HANDOFF.md` (Inglese)
- **Lingua Secondaria**: **Italiano**. Devono sempre esistere i corrispettivi file in lingua italiana:
  - `README_IT.md` (Italiano)
  - `HANDOFF_IT.md` (Italiano)
- **Regola di Parità 1:1**: I file in inglese e in italiano devono mantenere la medesima struttura gerarchica, sezioni, badge, tabelle e comandi di compilazione, differendo esclusivamente per la lingua del testo. Ogni volta che viene modificato un `README` o un `HANDOFF`, è **obbligatorio** aggiornare entrambi contemporaneamente.
- **Simulatore Web (`docs/index.html`)**: Deve essere **puramente in lingua inglese** in tutta l'interfaccia (titoli, sottotitoli, pulsanti, scenari di test, etichette dei preset, slider dei parametri, allarmi, avvisi toast e tabelle di documentazione/glossario).
