# Product Requirements Document (PRD) — Protection Warrior 3.3.5a WeakAuras Suite

## 1. Visione del Prodotto

La suite **Class Warrior (Protection)** per World of Warcraft 3.3.5a (*Wrath of the Lich King - Build 12340*) è un HUD specialistico progettato per massimizzare la sopravvivenza, la generazione di minaccia (*Threat*) e la reattività tattica del Guerriero Tank nei raid di progressione (Icecrown Citadel, Ruby Sanctum, Trial of the Grand Crusader, Ulduar).

Il ruolo del Tank in WotLK 3.3.5a richiede decisioni istantanee di mitigazione: subire un picco di danno fisico da 40.000+ o un'abilità magica mortale senza cooldown attivo porta al wipe del raid in meno di 2 secondi. Questa suite fornisce al giocatore un'assistenza attiva in tempo reale:
1. **Advisor Difensivo delle Emergenze**: Rilevamento della salute critica (< 35% HP) con raccomandazione gerarchica rigorosa del cooldown migliore disponibile (Shield Wall > Last Stand > Shield Block > Enraged Regeneration > Healthstone).
2. **Allerta Debuff Letali (Tank Busters)**: Rilevamento immediato dei debuff d'accumulo e dei picchi mortali dei boss (Soul Reaper su Lich King, Impale >= 2 su Gormok, Gastric Bloat >= 8 su Festergut, Fusion Punch su XT-002) per segnalare il momento esatto del cooldown difensivo o del taunt swap del co-tank.
3. **Allerta Enrage / Frenzy del Boss**: Segnalazione tempestiva dei buff d'ira del boss per attivare mitigazioni o avvisare i cacciatori per Tranquilizing Shot.
4. **Kick Advisor Intelligente Stance & Shield Aware**: Rilevamento automatico delle spell del bersaglio, distinguendo lanci kiccabili da quelli immuni, indicando esattamente quale abilità usare in base alla postura e allo scudo equipaggiato (`Shield Bash` in Defensive/Battle con scudo, `Pummel` in Berserker, o stuns `Concussion Blow` / `Shockwave`).
5. **Zero Clutter & Prestazioni Estreme**: Carico CPU in combattimento inferiore allo **0.1%**, con cache unificate per buff, debuff e statistiche.

---

## 2. Meccaniche di Tanking del Guerriero Protezione (3.3.5a)

### 2.1 Statistiche e Soglie Critiche
- **Difesa (Defense Rating)**: La soglia minima non negoziabile per essere immune ai colpi critici dei boss di livello 83 (raid boss) è **540 Defense** (+140 rispetto al cap naturale di 400 a livello 80, corrispondente al 5.6% di riduzione crit). Sotto 540 il pannello avverte il tank in giallo.
- **Armatura (Armor)**: Mitigazione primaria del danno fisico. Il cap massimo di mitigazione armatura contro boss lv 83 è il **75%** (circa 49.905 Armor).
- **Valore di Blocco (Shield Block Value - SBV)**: In WotLK il valore di blocco assorbe una quantità fissa di danno per ogni colpo bloccato e scala direttamente con il danno e la minaccia generata da **Shield Slam**. Con il talento *Critical Block*, il valore assorbito raddoppia.
- **Evitamento Combinato (Total Avoidance)**: Somma di Miss (base 5% + Defense) + Dodge + Parry + Block. Con *Shield Block* attivo, la probabilità di blocco aumenta del 100%, spingendo i colpi normali fuori dalla tabella dei colpi (*Hit Table*).
- **Competenza (Expertise)**: 26 Expertise (214 rating) azzera la probabilità di Dodge del boss (6.5%). 56 Expertise azzera anche la Parry (14%), prevenendo il fenomeno del *Parry-Haste* sui boss che lo supportano.
- **Indice di Colpito (Hit Rating)**: 8% (263 rating) per le abilità fisiche speciali (Taunt, Shield Slam, Revenge).

### 2.2 Rotazione di Minaccia e Priorità
1. **Shield Slam** (CD: 6s): Massima priorità per generazione di minaccia su singolo bersaglio. Se *Sword and Board* proccha, il cooldown si azzera e il costo di rabbia diventa 0.
2. **Revenge** (Disponibile dopo Dodge, Parry o Block): Genera minaccia elevatissima a basso costo di rabbia; con il talento *Improved Revenge* colpisce 2 bersagli e stordisce.
3. **Shockwave** (CD: 20s): Abilità conica ad alta minaccia e stun di 4 secondi per 3 o più bersagli.
4. **Devastate**: Applica o rinnova Sunder Armor e infligge danno scalato sulle cariche e sull'arma.
5. **Heroic Strike / Cleave**: Accodato sui colpi d'arma bianca sopra i 45-50 Rage per evitare l'overcap e massimizzare il threat.
6. **Sunder Armor Tracker**: Mantenimento costante delle 5 cariche sul boss per garantire il 20% di riduzione armatura a favore dell'intero comparto fisico del raid (soppresso da Expose Armor se presente).

---

## 3. Requisiti Funzionali dei 20 Nodi WeakAuras

La suite è articolata in 20 nodi controllati direttamente sotto la radice `Class Warrior (Protection)`:

### Modulo 01 — `01 - Procs warTank` (Dynamic Group, Y = +52 px)
- Centrato orizzontalmente, ospita fino a 7 icone dinamiche (34x34 px):
  1. **Sword and Board** (Buff 50227): Resetta Shield Slam e rimuove il costo di rabbia per 5 secondi. Icona con pixel glow dorato.
  2. **Revenge Ready**: Disponibile al lancio (dopo un blocco, parata o schivata).
  3. **Shield Block Active** (Buff 2565): +100% block chance e raddoppio del block value per 10s.
  4. **Victory Rush**: Utilizzabile dopo aver ucciso un nemico.
  5. **Emergency Low HP Alert**: Attivo quando la salute del tank scende sotto il 35%. Suggerisce con priorità il cooldown difensivo da lanciare.
  6. **Boss Enrage Alert**: Segnala Enrage, Frenzy o Berserk sul bersaglio ostile.
  7. **Tank Buster Alert**: Allerta visiva e sonora per debuff pericolosi attivi sul tank (Soul Reaper, Impale, Gastric Bloat, Fusion Punch).

### Moduli 02, 03, 04 — Buffs & Stance (X = -222, -190, -158, Y = 0)
- `02 - Battle Shout`: Avvisa quando mancano meno di 30s o è assente. Soppresso da Blessing of Might.
- `03 - Commanding Shout`: Grido raccomandato primario del tank (+salute). Soppresso da Blood Pact.
- `04 - Defensive Stance`: Controllo postura. Se in combattimento il tank si trova fuori dalla Postura Difensiva (Stance 2), si attiva un allarme rosso con dicitura `STANCE` e glow perentorio.

### Moduli 05 - 13 — Utility Row Auto-Adattiva a Centratura Dinamica (Y = -45 px, da 3 a 11 Icone)
Parità architetturale 1:1 con `fire-mage-335a-am` e `fury-warrior-335a-am`: ricentratura automatica orizzontale a $x = 0$ sotto la barra rabbia da $278\text{ px}$ senza buchi visivi né sbilanciamenti a destra. Include una whitelist selettiva rigorosa per gli item equipaggiati:
- `05 - Trinket 1 warTank` (Slot 13): Sempre visibile se equipaggiato (On-Use, ICD 45s–120s, Procs).
- `06 - Trinket 2 warTank` (Slot 14): Sempre visibile se equipaggiato (On-Use, ICD 45s–120s, Procs).
- `06b - Ring warTank` (Slot 11/12): **SOLO** se *Ashen Band of Endless Courage* (Tank Armor proc) o *Endless Vengeance* (Melee AP proc, 60s ICD). Soppresso per anelli statici.
- `07 - Cloak warTank` (Slot 15): **SOLO** se provvisto di incanto da combattimento proccabile (*Swordguard Embroidery* / Ricamo della Spada). Paracadute e incanti a statistiche statiche (+22 Agi, +16 Def, +225 Armor) sono **tassativamente soppressi**.
- `08 - Tier Set warTank`: **SOLO** se attivo il bonus 4 Pezzi Tier 10 (*Ymirjar Lord's Battlegear* 4P: bonus Shield Block -20% danno subito). Soppresso con 0, 1, 2 o 3 pezzi.
- `09 - Enchants warTank` (Slot 16): **SOLO** se incanti arma proccabili (*Blade Ward*, *Blood Draining* 5 cariche + heal d'emergenza, *Mongoose*, *Berserking*). Soppresso per incanti statici.
- `10 - Gloves warTank` (Slot 10): **SOLO** se provvisti di tinker attivo d'Ingegneria (*Reticulated Armor Webbing* o *Hyperspeed Accelerators*).
- `10b - Shield Block warTank`: Cooldown difensivo attivo e ricarica (durata 10s, CD 30s/60s). Fissato in riga prima di Shield Wall.
- `11 - Shield Wall warTank`: Cooldown difensivo principale (-60% danno subito per 12s, ricarica e glow emergenza <35% HP).
- `12 - Last Stand warTank`: Cooldown vitale di sopravvivenza (+30% vita massima per 20s, ricarica e glow emergenza <35% HP).
- `13 - Boots warTank` (Slot 8): Tinker attivo d'Ingegneria (*Nitro Boosts*) o fallback di utilità su *Enraged Regeneration*.

### Moduli 14, 15, 16 — Barre Centrali Sincronizzate (278 px)
- `14 - Rage Bar` (278x14 px, Y = -20 px): Rosso scuro a < 45 Rage, Ambra dorato a >= 45 Rage.
- `15 - Rotational Bar` (278x7 px, Y = -7 px): Swing Timer Main Hand con glow per Heroic Strike / Cleave accodati.
- `16 - Castbar warTank` (278x20 px, Y = +8 px): Barra di lancio target con Kick Advisor integrato (Ciano interrompibile vs Grigio non interrompibile, e raccomandazione Shield Bash / Pummel / Stun).

### Moduli 17, 18, 19 — Alerts, Stats & Sunder Tracker
- `17 - Alerts warTank` (Y = +78 px): Testo 18-20pt ad alto impatto riservato unicamente ad avvisi critici di interrupt (`Alert - Kick Now`) ed emergenza difensiva estrema sotto il 35% HP (`Alert - Emergency CD`). Zero Clutter: banner testuali invasivi eliminati.
- `18 - Stats Panel warTank` (126x60 px a X = -216, Y = -49): Pannello difensivo a 5 righe stile Fury Warrior (Def 540 Cap, Armor DR%, CTC 102.4%, Block % & SBV, Hit & Exp).
- `19 - Sunder Armor Tracker` (32x32 px a X = +160, Y = -7): Monitoraggio cariche (1-5) e durata Sunder Armor o Expose Armor.

---

## 4. Requisiti Funzionali Aggiuntivi (Specifiche Tecniche)

### FR-LOAD-01: Load Condition Esclusiva [Devastate]
- La suite di WeakAuras deve attivarsi **soltanto** se il giocatore appartiene alla classe `WARRIOR` e possiede il talento **[Devastate]** (Indice WeakAuras `103`, Tab 3 Protezione, Posizione 23).
- Deve disattivarsi automaticamente in presenza di spec Arms o Fury o personaggi non guerrieri.

### FR-STANCE-01: Rilevamento Postura Errata in Combat (Zero-Clutter)
- Se il guerriero entra in combattimento (`UnitAffectingCombat("player") == true`) con postura diversa da Difensiva (`GetShapeshiftForm() ~= 2`):
  1. L'icona compatta `04 - Defensive Stance - OutOfStance warTank` (a $x = -158, y = 0$) attiva un Pixel Glow rosso perentorio con scritta `STANCE`.
  2. L'icona scompare istantaneamente al passaggio in Postura Difensiva o all'uscita dal combattimento.
  3. Per preservare la visibilità di gioco (stile Fury Warrior e Fire Mage), nessun banner testuale invasivo centrale viene proiettato a schermo.

### FR-STATS-01: Motore Statistiche Tank Stile Fury Warrior & Buff/Debuff Non-Stacking
- Il pannello statistiche `18 - Stats Panel warTank` deve visualizzare 5 righe con etichette bianche `|cFFFFFFFFLabel:|r <ValoreColorato>`:
  1. `Def:` (540 Cap Lv.83, 535 HC Lv.82).
  2. `Armor:` con Physical DR% contro boss Lv.83 ($K=16635$, hard cap 75%).
  3. `CTC:` Combat Table Coverage ($\text{Dodge} + \text{Parry} + \text{Block} + \text{BossMiss}$), con rilevamento non-stacking di *Insect Swarm* e *Scorpid Sting* (+3.0% max).
  4. `Block:` con percentuale di blocco e Shield Block Value (SBV).
  5. `Hit:` con bonus Draenei *Heroic Presence* (+1.0%) ed `Exp:` con Soft Cap 26 ed Hard Cap 56.
