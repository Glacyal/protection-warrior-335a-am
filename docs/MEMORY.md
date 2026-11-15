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
