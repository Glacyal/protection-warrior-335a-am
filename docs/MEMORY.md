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

### 2.5 Specifica Tassativa della Riga Utility Auto-Adattiva e Filtri Item Proc-Only per il War Tank
- **Direttiva Utente Tassativa**:
  "Quello che sta sotto come i due trinket, l'eventuale anello, mantello, solo se ha le specifiche indicate, e i cooldown difensivi devono adattarsi dinamicamente centrandosi in modo naturale sotto la barra della rabbia del War Tank."
- **Contratto Architetturale della Riga Utility (`05` - `13`, a $y = -45\text{ px}$)**:
  1. **Auto-Adattamento Dinamico Naturale per il War Tank**:
     - La riga non è una griglia statica: non deve MAI presentare buchi vuoti tra le icone o slittare a destra quando un elemento è assente o soppresso.
     - Tutte le icone qualificate vengono raccolte in `activeOrder` e centrate orizzontalmente a $x = 0$ sotto la barra rabbia ($278\text{ px}$) tramite la formula:
       $$\text{targetX} = \left\lfloor \left( i - \frac{N + 1}{2} \right) \times \text{step} + 0.5 \right\rfloor$$
     - Il passo (`step`) e la larghezza icona (`targetW`) scalano dinamicamente in base alla cardinalità $N$ ($3 \le N \le 11$):
       $N \ge 11 \implies 25\text{px} / 24\text{px}$, $N = 10 \implies 27\text{px} / 26\text{px}$, $N = 9 \dots 5 \implies 29\text{px} \dots 48\text{px} / 28\text{px}$, $N \le 4 \implies 52\text{px} / 28\text{px}$.
  2. **Whitelist Rigorosa di Filtraggio degli Oggetti**:
     - **Trinket 1 & 2 (Slot 13 e 14)**: Sempre visibili quando equipaggiati (`itemID > 0`). Tracciamento durata, CD on-use e ICD (45s–120s) da database ICC/RS/ToC/Ulduar.
     - **Anello (Slot 11/12)**: **SOLO ed esclusivamente** in presenza di *Ashen Band of Endless Courage* (Tank Armor proc, Spell ID 72414) o *Ashen Band of Endless Vengeance* (Melee AP proc, Spell ID 72412). Qualsiasi anello con sole statistiche statiche deve essere tassativamente soppresso.
     - **Mantello (Slot 15)**: **SOLO ed esclusivamente** se provvisto di incanto da combattimento con proc attivo (Sartoria: *Swordguard Embroidery* / *Ricamo della Spada*, Spell ID 55775, ID Incanto 3730). Il paracadute d'Ingegneria (*Flexweave Underlay*) e tutti gli incanti con statistiche passive statiche (+22 Agi, +16 Def, +225 Armor) sono **tassativamente soppressi e invisibili**.
     - **Tier Set (08)**: **SOLO ed esclusivamente** se il giocatore equipaggia almeno 4 Pezzi Tier 10 (*Ymirjar Lord's Battlegear* 4P: bonus *Shield Block* magico -20% danno subito). Soppresso con 0, 1, 2 o 3 pezzi.
     - **Incanti Arma (Slot 16)**: **SOLO ed esclusivamente** se l'arma monta incanti proccabili difensivi o offensivi (*Blade Ward*, *Blood Draining* 5 cariche + heal d'emergenza <35% HP, *Mongoose*, *Berserking*). Soppresso per incanti statici (+30 Stamina Titanguard, +20 Strength Potency, ecc.).
     - **Guanti (Slot 10)**: **SOLO ed esclusivamente** se provvisti di tinker attivo d'Ingegneria (*Reticulated Armor Webbing* o *Hyperspeed Accelerators*).
     - **Cooldown Difensivi Guerriero (`10b`, `11`, `12`)**: `Shield Block` (durata 10s e CD 30s/60s), `Shield Wall` (-60% danno, durata 12s, CD e glow emergenza <35% HP) e `Last Stand` (+30% vita max, durata 20s, CD e glow emergenza <35% HP) sono permanentemente integrati nella sequenza attiva prima degli stivali e partecipano alla centratura dinamica.
     - **Stivali (Slot 8)**: Provvisti di tinker attivo d'Ingegneria (*Nitro Boosts*) o fallback su *Enraged Regeneration*.
  3. **Punto Unico di Inizializzazione Core**:
     - `_G.PWHUD_InitCore` e la definizione di `_G.PWHUD_UpdateUtilityRowPositions` devono vivere nel trigger di `05 - Trinket 1 warTank` (`slot == 13`), perché `actions.init` sul gruppo radice non viene mai eseguito da WeakAuras 3.3.5a.

---

### 2.6 Parità Visiva Rigorosa e Multi-Proc Refresh SAB/REV con Offset CLEU 3.3.5a Tassativi
- **Direttiva Utente Tassativa**:
  *"Revenge Ready warTank" e "Sword and Board" devono essere simili nel modo in cui si mostrano, generare un task che crei questo fix, e inoltre, sia il primo che il secondo, oltre al fatto che giustamente spariscono se vengono usati, c'e da considerare che potrebbero proccare piu volte senza che io lo utilizzi, questo dovrebbe refresciare il tempo necessario per il lancio di una o del altra.*
- **Parità Visiva 1:1 Eseguita**:
  1. **Dimensioni & Forma**: Entrambe le icone sono $34 \times 34\text{ px}$ posizionate nel gruppo dinamico `01 - Procs warTank` ($y = +52\text{ px}$).
  2. **Texture Esplicita**: `auto: False` su entrambe con icone native `Ability_Warrior_SwordandBoard` e `Ability_Warrior_Revenge` (nessun flickering da texture dinamica).
  3. **Zero Lancetta Gialla Cooldown**: `cooldownEdge: False` su entrambe. Il valore `cooldownEdge: True` su Revenge creava una sgradevole lancetta verticale gialla che tagliava a metà l'icona; impostandolo a `False` la grafica rimane pulita.
  4. **Subregions a 3 Livelli Simmetriche**:
     - Indice 0: `{"type": "subbackground"}` (fondale opaco per contrasto).
     - Indice 1: Timer countdown decimale `%p` ancorato a `INNER_BOTTOM` (`font_size=11`, `y_offset=1`, formattazione `%.1f`).
     - Indice 2: Etichetta dell'abilità centrata in alto: `SLAM` su Sword and Board e `REV` su Revenge Ready, ancorata a `INNER_TOP` (`font_size=9`, `y_offset=-2`).
  5. **Effetto Glow Identico**: Gold Pixel Glow `LibCustomGlow-1.0` `[1.0, 0.84, 0.0, 1.0]` con 8 linee su `actions.start`, nascosto su `actions.finish`.
- **Offset Parametri CLEU in WotLK 3.3.5a (Build 12340)**:
  - In 3.3.5a gli 8 parametri base di `COMBAT_LOG_EVENT_UNFILTERED` sono:
    `timestamp, subEvent, sourceGUID, sourceName, sourceFlags, destGUID, destName, destFlags`.
  - Gli offset successivi a `destFlags` (indice 8) sono rigorosamente:
    - `SWING_MISSED`: `select(9, ...)` = `missType` (`"DODGE"`, `"PARRY"`, `"BLOCK"`).
    - `RANGE_MISSED` / `SPELL_MISSED`: `select(9, ...)` = `spellId`, `select(12, ...)` = `missType`.
    - `SWING_DAMAGE`: `select(9, ...)` = `amount`, `select(13, ...)` = `blocked`.
    - `RANGE_DAMAGE` / `SPELL_DAMAGE`: `select(9, ...)` = `spellId`, `select(16, ...)` = `blocked`.
    - `SPELL_CAST_SUCCESS`: `select(9, ...)` = `spellId`, `select(10, ...)` = `spellName`.
    - `SPELL_AURA_APPLIED` / `SPELL_AURA_REFRESH` / `SPELL_AURA_REMOVED`: `select(9, ...)` = `spellId`, `select(10, ...)` = `spellName`.
- **Logica Multi-Proc con Refresh Dinamico**:
  - Quando si verifica un nuovo evento valido (schivata, parata, blocco per Revenge; nuovo proc buff 50227 da Devastate/Revenge per Sword and Board) mentre l'icona è già visibile a schermo, la durata viene reimpostata a $5.0\text{ s}$ completi:
    ```lua
    _G.PWHUD_Revenge.start = GetTime()
    _G.PWHUD_Revenge.duration = 5.0
    ```
    ```lua
    _G.PWHUD_Sab.start = GetTime()
    _G.PWHUD_Sab.duration = 5.0
    ```
- **Consumo Istantaneo a 0 Latenza (Instant Cast Consumption)**:
  - Al lancio di *Shield Slam* o *Revenge*, il listener CLEU su `SPELL_CAST_SUCCESS` azzera immediatamente `start = 0`, facendo sparire l'icona istantaneamente senza attendere la latenza di rete del server o il successivo ciclo `UNIT_AURA`.

---

### 2.7 Swing Timer Mano Primaria & Accodamento Heroic Strike/Cleave (`15 - Rotational Bar warTank`)
- **Direttiva Utente Tassativa**:
  *"15 - Rotational Bar warTank" non funziona come la barra che mostra lo scorrimento tra un attacco ed il successivo, deve funzionare in modo identico, solo che nel War Tank l'arma è una sola invece di due, facciamo il task e il fix.*
- **Architettura Tecnica Adottata**:
  1. **Tipologia Region**: `Rotational Bar - Base Bar warTank`, `Rotational Bar - HS Queued warTank` e `Rotational Bar - Cleave Queued warTank` sono configurate come `regionType: "aurabar"` a piena larghezza ($274 \times 5\text{ px}$) anziché semplici texture statiche.
  2. **Tracciamento Singola Arma (Mano Primaria)**:
     - In quanto War Tank (arma 1H + scudo), il motore traccia unicamente la velocità della mano principale via `UnitAttackSpeed("player")`.
     - `_G.PWHUD_GetSwing()` intercetta via CLEU:
       - `SWING_DAMAGE` e `SWING_MISSED`: azzera e fa ripartire lo swing timer dall'istante corrente (`sw.mhStart = now`).
       - `SPELL_DAMAGE` e `SPELL_MISSED` per *Heroic Strike* (47450) o *Cleave* (47520): poiché sostituiscono l'attacco bianco successivo, all'impatto fanno ripartire lo swing timer da capo (`sw.mhStart = now`) e disattivano lo stato accodato.
       - `SPELL_EXTRA_ATTACKS` (es. proc Sword Specialization): riavvia il timer della mano primaria.
  3. **Visualizzazione Timer Centrato**: Mostra costantemente il tempo mancante in formato decimale (`%c`, es. `1.8s`) al centro esatto della barra.
  4. **Continuità Visiva dell'Accodamento**:
     - Quando il giocatore attiva *Heroic Strike* o *Cleave* durante un'oscillazione dell'arma (es. al 50% di caricamento), la barra non subisce glitch o reset a vuoto: la corrispondente aurabar accodata (`HS Queued` in Oro con Pixel Glow, o `Cleave Queued` in Verde Smeraldo con Pixel Glow) si sovrappone condividendo la medesima funzione di progresso (`customDuration`), proseguendo l'animazione di scorrimento senza soluzione di continuità fino all'impatto.

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
  - Tab 2 = Secondo ramo talenti (indici 41–80)
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

---

## 7. Regola Geometrica Vincolante: Stats Panel (88x60px) e Cluster Buff Sovrastante (20x20px con gap 2px)

A seguito della rimozione di `% armor` e `SBV` per garantire la massima pulizia visiva e compattezza dell'HUD, la geometria del blocco sinistro è standardizzata secondo i seguenti vincoli matematici:
1. **Stats Panel (`18 - Stats Panel warTank`)**:
   - Dimensioni: $88 \times 60\text{ px}$.
   - Coordinate: $X = -190\text{ px}, Y = -45\text{ px}$.
   - Contenuto a 5 righe: Def, Armor (in k), CTC, Block (%), Hit & Exp. Nessun testo superfluo di `% armor` né di `SBV`.
2. **Cluster 4 Icone Sovrastanti**:
   - `02 - Battle Shout warTank`: $X = -223\text{ px}, Y = 0$, dimensione $20 \times 20\text{ px}$.
   - `03 - Commanding Shout warTank`: $X = -201\text{ px}, Y = 0$, dimensione $20 \times 20\text{ px}$.
   - `04b - Vigilance warTank`: $X = -179\text{ px}, Y = 0$, dimensione $20 \times 20\text{ px}$.
   - `04 - Defensive Stance warTank`: $X = -157\text{ px}, Y = 0$, dimensione $20 \times 20\text{ px}$.
   - Spaziatura: passo di $22\text{ px}$ ($20\text{ px}$ larghezza + $2\text{ px}$ gap).
   - Estensione totale: da $X = -233\text{ px}$ a $X = -147\text{ px}$ (ampiezza $86\text{ px}$), perfettamente centrata su $X = -190\text{ px}$ con $1\text{ px}$ di margine simmetrico rispetto al pannello da $88\text{ px}$.
   - Dimensione font subtext: 9pt per timer countdown `%c`, 8pt per etichette `OFF`, 7pt per etichetta `STANCE`.
   - **Divieto Assoluto di Regressione**: Non allargare mai il pannello né le icone oltre queste dimensioni salvo esplicita richiesta dell'utente.
