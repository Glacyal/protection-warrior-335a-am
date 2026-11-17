> 🇬🇧 **English Version**: [HANDOFF.md](HANDOFF.md)
>
> 🌐 **Live Web Simulator**: [https://glacyal.github.io/protection-warrior-335a-am/](https://glacyal.github.io/protection-warrior-335a-am/)

# Class Warrior (Protection) — Handoff Tecnico

Manuale di riferimento tecnico per lo sviluppo, la manutenzione e l'estensione della suite **Class Warrior (Protection)** per World of Warcraft 3.3.5a (*WotLK Build 12340*).

---

## 1. Panoramica del Progetto

La suite è distribuita come **WeakAura autonoma** in formato compresso `!WA:1!` (serializzazione binaria `AceSerializer-3.0` + compressione Deflate RFC 1951 livello 9 + codifica di stampa `LibDeflate`).  
Adotta una geometria visiva a 278px ingegnerizzata specificamente per il Protection Warrior, garantendo Zero Warning nativa su WeakAuras 5.21.8+ (`internalVersion = 90`).

| Proprietà | Dettaglio |
| :--- | :--- |
| **Piattaforma Target** | World of Warcraft 3.3.5a (WotLK Build 12340) |
| **Engine WeakAuras Target** | **WeakAuras 5.21.8+** (`internalVersion = 90`, `w = "5.21.8"`). |
| **File di Distribuzione** | [`IMPORT_STRING_v5.21.8.txt`](IMPORT_STRING_v5.21.8.txt) (stringa ufficiale pronta per l'importazione) |
| **Simulatore Web** | [`docs/index.html`](docs/index.html) |
| **Live Demo Online** | [GitHub Pages Live Showcase](https://glacyal.github.io/protection-warrior-335a-am/) |
| **Controllo Versione** | Git su GitHub: [Glacyal/protection-warrior-335a-am](https://github.com/Glacyal/protection-warrior-335a-am) |

---

## 2. Struttura del Repository

```text
protection-warrior-335a-am/
├── IMPORT_STRING_v5.21.8.txt        # Stringa WeakAuras 5.21.8+ nativa (Zero warning, internalVersion: 90)
├── generate.py                      # Compilatore Python dell'albero WA
├── README.md                        # Documentazione utente primaria (Inglese)
├── README_IT.md                     # Documentazione utente secondaria (Italiano)
├── HANDOFF.md                       # Specifiche tecniche primarie per sviluppatori (Inglese)
├── HANDOFF_IT.md                    # Specifiche tecniche secondarie per sviluppatori (Italiano)
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
│   └── components/                  # Moduli dedicati ai singoli componenti dell'HUD
│       ├── procs.py                 # 01 - Procs warTank (Gruppo dinamico 34x34 a y = 52: parità visiva 1:1 SAB/REV, refresh multi-proc dinamico, consumo istantaneo, filtro >=500k HP)
│       ├── buffs.py                 # 02 - Battle Shout warTank, 03 - Commanding Shout warTank, 04 - Defensive Stance warTank (x = -271, -216, -161, y = 0, 34x34px)
│       ├── utility.py               # 05-13 - Utility Row (Monili, Anello, Mantello, Tier, Incanti, Guanti, Shield Wall warTank, Last Stand warTank, Boots) a y = -45
│       ├── bars.py                  # 14 - Rage Bar & 16 - Castbar warTank (Barra speculare Target dx->sx e Player sx->dx con advisor Bash/Reflect)
│       ├── rotational.py            # 15 - Rotational Bar warTank (Aurabar swing timer mano primaria 274x5px a y = -7 con Pixel Glow accodamento HS/Cleave)
│       ├── alerts.py                # 17 - Alerts warTank (Avvisi testuali di emergenza minimalisti: Emergency CD, Kick Now)
│       ├── stats.py                 # 18 - Stats Panel warTank (Pannello 96x60px a x = -192, y = -45, perfettamente adattato a 5 righe senza % Armor né SBV)
│       └── sunder.py                # 19 - Sunder Armor Tracker warTank (32x32px a x = 160, y = -7)
│
├── docs/                            # Documentazione e anteprima interattiva per GitHub Pages
│   └── index.html                   # Simulatore interattivo HTML/CSS/JS (puramente in Inglese, HUD War Tank nativo)
│
├── scripts/
│   └── sync_docs.py                 # Sincronizzazione automatica della stringa v5 in docs/index.html
│
└── tests/                           # Suite di test automatici e paralleli
    ├── run_parallel_tests.py        # Test runner parallelo multi-processore (ProcessPoolExecutor)
    ├── test_components_integrity.py # Verifica integrità strutturale moduli (20 nodi sequenziali e UIDs)
    ├── test_lua.py                  # Validazione sintassi codice Lua (trigger, untrigger, actions)
    ├── test_tree_layout.py          # Verifica conformità geometrica e posizionamento
    ├── test_string_sync.py          # Verifica corrispondenza tra builder e IMPORT_STRING_v5.21.8.txt
    ├── test_stats_panel.py          # Verifica formule tank (Armor DR contestuale, EHP, CTC, Defense 540)
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

### 4.2 Notifica Postura Errata in Combattimento (Wrong Stance Alert — Modello Zero-Clutter)
- In postura difensiva corretta (`GetShapeshiftForm() == 2`), l'icona è **completamente invisibile** (zero visual clutter a schermo).
- Doppio livello di allarme attivo quando `UnitAffectingCombat("player") and GetShapeshiftForm() ~= 2`:
  1. Indicatore locale `04 - Defensive Stance - OutOfStance` (X: -158, Y: 0, 28x28px) con colore rosso e label `STANCE`.
  2. Icona compatta `04 - Defensive Stance - OutOfStance warTank` (X: -168, Y: 0) a fianco degli urli (banner centrale invasivo rimosso nel Task 29).

### 4.3 Motore Statistiche Tanking del War Tank & Buff/Debuff Non-Stacking
- Formattazione a 5 righe con etichette bianche `|cFFFFFFFFLabel:|r <Valore>`:
  1. `Def:` (540 Cap per Lv.83, 535 per Lv.82).
  2. `Armor:` con Physical DR% contestuale ($K=15232.5$ a Lv.80 default pari a 62.4% come scheda PG; $K=16635$ su Raid Boss Lv.83 pari a 60.3%, hard cap 75%).
  3. `CTC:` Combat Table Coverage con motore non-stacking per *Insect Swarm* e *Scorpid Sting* (+3.0% Miss max).
  4. `Block:` con % di blocco e Shield Block Value (SBV).
  5. `Hit:` con Draenei *Heroic Presence* (+1.0%) ed `Exp:` con Soft Cap 26 ed Hard Cap 56.

### 4.7 Armonizzazione Colonna Sinistra (Allineamento Stats Panel e Shouts/Stance)
- **Dimensioni Stats Panel (144x68px a X: -216, Y: -53)**: Perfettamente dimensionato per racchiudere tutte le 5 righe di statistiche difensive (`Def: 541 (CAP)`, `Armor: 25.3k (62.4%)`, `CTC: 75.2%`, `Block: 21.7% (1800 SBV)`, `Hit: 9.1% | 25 Exp`) con 10px di margine laterale e 6px verticale, eliminando qualsiasi sbordamento a sinistra delle etichette.
- **Griglia Shouts e Stance Sovrastante (34x34px a X: -271, -216, -161, Y: 0)**: Icone standardizzate a 34x34px (identiche alla riga procs); bordo sinistro (-288) allineato a filo con il pannello, centro (-216) allineato a Commanding Shout, e bordo destro (-144) allineato a Defensive Stance.
- **Separazione Verticale Pulita**: Spazio di 3px tra le label inferiori delle icone (`OFF`, `STANCE` a Y: -17) e il bordo superiore del pannello (Y: -19.6), azzerando ogni sovrapposizione visiva.

### 4.12 Cooldown Difensivo T10 4P & Icona Bloodrage (08 - Tier Set warTank)
- **Trasformazione in Cooldown Difensivo**: Con il T10 4P (*Ymirjar Lord*), l'abilità *Bloodrage* (Spell ID 2687) funge da vero cooldown difensivo conferendo uno scudo del 20% della salute massima per 10s (*Blood Frenzy*, Spell ID 70844).
- **Icona Ufficiale dell'Abilità Attivatrice**: Standardizzata sull'icona di *Bloodrage* (`Interface\Icons\Ability_Racial_BloodRage`), l'abilità esatta che innesca l'effetto difensivo.
- **Engine a Tre Stati**:
  1. `ACTIVE`: Conto alla rovescia decrescente dello scudo da 10s (`%.1fs`), swipe e Pixel Glow dorato.
  2. `COOLDOWN`: Tracciamento del tempo di ricarica di Bloodrage (60s o ridotto) con swipe e secondi residui.
  3. `READY`: Icona Bloodrage pulita pronta all'uso.
- **Ricentratura Dinamica**: Soppressione totale se non si indossa il T10 4P con auto-centratura della riga utility; `cooldownEdge: False` per bordo pulito.

### 4.14 Riposizionamento Shield Block nella Riga Utility Inferiore (10b - Shield Block warTank)
- **Spostamento nella Riga Utility Inferiore (Y: -45)**: Rimosso completamente `Shield Block Active` dal gruppo dinamico procs superiore (`01 - Procs warTank`) e riposizionato sotto nella riga utility come `10b - Shield Block warTank` al fianco di `11 - Shield Wall warTank` e `12 - Last Stand warTank`.
- **Engine a Tre Stati (Durata, Ricarica, Pronto)**:
  1. `ACTIVE`: Quando *Shield Block* (Spell ID 2565) è attivo, traccia i 10 secondi di durata con swipe circolare, countdown in secondi gialli (`|cFFFFFF00%.1fs|r`) e Pixel Glow dorato (`LibCustomGlow-1.0`).
  2. `COOLDOWN`: Alla scadenza del buff, traccia la ricarica residua (base 60s, oppure 30s con il talento *Shield Mastery*) con swipe circolare di recupero, conto alla rovescia numerico e bordo pulito (`cooldownEdge: False`).
  3. `READY`: Quando disponibile, visualizza l'icona ufficiale pulita (`Ability_Defensive`) pronta all'uso senza testi spuri.
- **Ricentratura Dinamica Automatica**: Integrato in `_G.PWHUD_UpdateUtilityRowPositions()` prima di Shield Wall, garantendo una centratura fluida ed equilibrata fino a 11 icone di utilità.

### 4.13 Database Allarmi Tank Buster Completo (Raid WotLK 3.3.5a & Trash Pericolosi)
- **Meccaniche Tank Swap & Buster di Tutti i Tier**: Database completo per Spell ID `_G.PWHUD_TankBustersDB` e tabella nomi bilingue `_G.PWHUD_TankBustersByName` in `builder/components/procs.py`:
  - **Icecrown Citadel (ICC)**: Soul Reaper (Lich King 10N/25N/10H/25H - 69409, 73797, 73798, 73799; `SWAP`), Gastric Bloat (Festergut 10N/25N/10H/25H >= 8 - 72219, 72551, 72552, 72553; `x8`), Rune of Blood (Deathbringer Saurfang - 72410; `SWAP`), Mystic Buffet (Sindragosa P3 >= 5 - 70127, 70128; `x5`), Delirious Slash (Blood-Queen Lana'thel >= 2 - 71623, 71624; `x2`), Mutated Plague (Putricide P3 >= 2 - 72451..72454; `x2`), Mutated Infection (Rotface - 69674..73023; `INFECT`), Corrosion (Valithria Zombie >= 3 - 70751, 71236; `x3`), Gut Spray (Valithria Abomination - 70633, 71232; `SPRAY`), Severed Flesh (Deathbound Ward / Trash ICC >= 3 - 71127; `x3`).
  - **Ruby Sanctum (RS)**: Fiery Combustion (Halion - 74562, 74567, 74795; `RUN`), Soul Consumption (Halion Twilight - 74792, 74793, 74799; `RUN`), Cleave Armor (General Zarithrian >= 2 - 74367; `x2`), Enervating Brand (Baltharus the Warborn - 74502; `BRAND`).
  - **Trial of the Crusader (TotC / ToGC)**: Impale (Gormok >= 2 - 67478, 67479, 66331; `x2`), Paralytic Toxin (Acidmaw - 66823, 67618; `TOXIN`), Incinerate Flesh (Jaraxxus - 66237, 67049..67051; `HEAL`), Expose Weakness (Anub'arak Burrower >= 2 - 67847..67849; `x2`).
  - **Ulduar**: Phase Punch (Algalon >= 3 - 64412, 64417; `x3`), Unbalancing Strike (Thorim - 62130, 62131; `SWAP`), Fusion Punch (Steelbreaker - 61903, 63493; `FUSION`), Overwhelming Power (Steelbreaker - 61888, 64637; `MELT`), Fuse Armor (Razorscale >= 2 - 64771, 64772; `x2`), Surge of Darkness (General Vezax - 62661, 62662; `CD!`), Plasma Blast (Mimiron - 62997, 64529; `PLASMA`), Crunch Armor (Kologarn >= 2 - 63355, 64002; `x2`), Slag Pot (Ignis - 62717, 63477; `POT`).
  - **Naxxramas, VoA, Sartharion**: Mortal Wound (Gluth >= 4 - 25646; `x4`), 4 Horsemen Marks (Blaumeux, Rivendare, Korth'azz, Zeliek >= 3 - 28832..28835; `x3`), Frostbite (Toravon the Ice Watcher >= 4 - 72098; `x4`), Twilight Torment (Sartharion - 57948; `SHADOW`).
- **Dinamismo Grafico Avanzato**:
  - `customIcon`: commutazione dinamica della texture all'icona reale del debuff applicato.
  - `customDuration`: swipe di ricarica circolare con bordo pulito (`cooldownEdge: False`).
  - `customText`: etichetta di raccomandazione tattica o stack (`SWAP`, `x8`, `HEAL`, `RUN`, `PLASMA`, ecc.).
  - Pixel Glow rosso intenso via `LibCustomGlow-1.0` all'avvio con rimozione pulita allo scadere.

### 4.11 Allerta Mancanza Vigilanza (04b - Vigilance warTank — Architettura Focus Magic Pura)
- **Allineamento 1:1 a Focus Magic**: Rimosso il blocco incompatibile di scansione talenti; mostra l'icona desaturata `Ability_Warrior_Vigilance` con scritta rossa `OFF` non appena nessun alleato attivo nel raggio o nel party/raid possiede il buff (`not allyActive`).
- **Ciclo di Vita Event-Driven su Alleati**:
  - `UNIT_SPELLCAST_SUCCEEDED`: Rileva l'assegnazione di Vigilanza su alleato (`expires = now + 1800`).
  - `COMBAT_LOG_EVENT_UNFILTERED`: Traccia `SPELL_AURA_APPLIED`, `SPELL_AURA_REFRESH`, `SPELL_AURA_REMOVED`, `SPELL_AURA_BROKEN` e azzera il buff alla morte dell'alleato protetto (`UNIT_DIED`).
  - Scansione automatica di fallback su `target`, `focus`, `party1..4` e `raid1..40`.
- **Modello Visivo Anti-Clutter**:
  - `Vigilance - OFF warTank`: Icona desaturata con `OFF` rosso in basso, compare non appena nessun alleato ha il buff attivo.
  - `Vigilance - Active warTank`: Compare solo in prossimità di scadenza (`rem <= 60s`).
- **Geometria Armonizzata a 4 Icone (30x30px con gap 2px)**: Copre esattamente i 126px del pannello statistiche sottostante (da X: -279 a X: -153):
  - `02 - Battle Shout warTank`: `X: -264, Y: 0`
  - `03 - Commanding Shout warTank`: `X: -232, Y: 0`
  - `04b - Vigilance warTank`: `X: -200, Y: 0`
  - `04 - Defensive Stance warTank`: `X: -168, Y: 0`

### 4.10 Ottimizzazione Compatta Stats Panel (126x60px) & Ravvicinamento Icone a 3px
- **Pannello Statistiche Snello (126x60px)**: Riconfigurato a 126x60px (`X: -216, Y: -49`), eliminando il vuoto superfluo a destra e in basso, mantenendo un margine interno perfetto di 6px per lato sul testo difensivo.
- **Icone Sovrastanti Ravvicinate (Gap 3px)**: Sostituito l'eccessivo distacco di 21px con un passo compatto di 37px (34px icona + 3px gap):
  - `02 - Battle Shout warTank`: `X: -253, Y: 0`
  - `03 - Commanding Shout warTank`: `X: -216, Y: 0`
  - `04 - Defensive Stance warTank`: `X: -179, Y: 0`
- Il blocco icone (108px) risulta centrato sull'asse del pannello statistiche (126px) con 9px di respiro simmetrico a sinistra e a destra e 2px di distacco verticale.

### 4.9 Filtraggio Intelligente Mantello con Proc (Slot 15) & Soppressione Paracadute/Statici
- **Visibilità Esclusiva per Proc da Combattimento**: `07 - Cloak warTank` compare unicamente se il mantello (Slot 15) è dotato di un incanto proccabile da combattimento, specificamente *Swordguard Embroidery* (*Ricamo della Spada* di Sartoria, +400 AP per 15s con 45s ICD, Spell ID 55775, Enchant ID 3730).
- **Soppressione Totale Paracadute e Incanti Statici**: Il tinker del paracadute di Ingegneria (*Flexweave Underlay*, Incanto ID 3605, Spell ID 55002) così come tutti gli incanti statici (+22 Agilità, +16 Difesa, +225 Armatura) o mantelli senza incanto valutano rigorosamente `_G.PWHUD_CheckSlotEquipped(15) == false`.
- **Ricentratura Dinamica Senza Buchi**: In caso di soppressione, `07 - Cloak warTank` viene escluso da `activeOrder` in `_G.PWHUD_UpdateUtilityRowPositions()`, ricentrando perfettamente le restanti icone utility. Impostato `cooldownEdge: False` per prevenire artefatti grafici a spillo.

### 4.8 Filtraggio Intelligente Tier Set con Proc & Pulizia Bordo Revenge
- **Visibilità Esclusiva per Bonus Tier con Proc**: `08 - Tier Set warTank` compare esclusivamente se il bonus di set equipaggiato dispone di un vero proc / buff da tracciare:
  - **T10 4P (*Blood Frenzy* / *Frenesia del Sangue*, Spell ID 70844)**: Assorbimento pari al 20% della vita massima per 10s scatenato da Bloodrage.
  - **T8 4P (Riduzione Danno Magico 20%, Spell ID 64938 / 2565)**: 20% riduzione danno magico per 10s attivo durante Blocco con Scudo.
- **Soppressione Totale Bonus Statici**: Tutti i bonus puramente passivi o statici (T10 2P, T9 2P/4P, T8 2P, T7 2P/4P) restituiscono rigidamente `cache.isEquipped = false`.
- **Ricentratura Dinamica Senza Buchi**: In caso di soppressione, `08 - Tier Set warTank` viene escluso da `activeOrder` in `_G.PWHUD_UpdateUtilityRowPositions()`, ricentrando perfettamente le restanti icone utility.
- **Pulizia Bordo Icona Revenge**: Impostato `cooldownEdge: False` su `Revenge Ready warTank`, eliminando la linea/ago verticale gialla a ore 12 sul bordo superiore mantenendo lo swipe circolare.

### 4.6 Filtraggio Incanti Arma Proccabili (Slot 16)
- **Visibilità Esclusiva per Incanti con Proc**: `09 - Enchants warTank` compare solo se sull'arma principale (Slot 16) è presente un incantesimo con proc di combattimento attivo: *Blade Ward*, *Blood Draining* (stack 1-5 e cura d'emergenza), *Mongoose*, *Berserking*, *Executioner*, *Crusader*, *Lifeward*, *Black Magic*, *Icebreaker*, *Giant Slayer*, *Deathfrost*, *Unholy Weapon*, *Fiery Weapon*, *Lifestealing*.
- **Soppressione Integrale Incanti Statici**: Tutti gli incanti puramente statistici (*Titanguard* +30 Stamina, *Accuracy* +25 Hit/+25 Crit, *Titanium Weapon Chain* +28 Hit/-50% Disarm, *Superior Potency* +65 AP, *Exceptional Agility* +26 Agi, *Major Defense* +12 Def, ecc.) o armi prive di incanto valutano rigorosamente `_G.PWHUD_CheckEnchantsEquipped() == false`.
- **Ricentratura Dinamica Naturale**: In caso di soppressione, `09 - Enchants warTank` viene escluso da `activeOrder` in `_G.PWHUD_UpdateUtilityRowPositions()`, ricentrando simmetricamente le restanti icone utility senza lasciare spazi vuoti.

### 4.5 Motore Revenge Ready & Refresh Dinamico
- **Finestra Interna di 5.0s con Tracking CLEU**: Ascolto in tempo reale su `COMBAT_LOG_EVENT_UNFILTERED` per Schivata (`DODGE`), Parata (`PARRY`) e Blocco (`BLOCK` o `blocked > 0`) subiti dal giocatore.
- **Refresh Dinamico in Tempo Reale**: Ogni nuova schivata, parata o blocco mentre Revenge è utilizzabile ripristina istantaneamente il timer a 5,0 secondi pieni.
- **Azzeramento Immediato al Lancio**: L'evento `SPELL_CAST_SUCCESS` di Revenge (tutti i rank/spell ID) azzera immediatamente il timer.
- **Perfezionamento Grafico**: Swipe circolare, conto alla rovescia in secondi `%p`, label `REV` centrata e Pixel Glow ambra tramite `LibCustomGlow-1.0` con spegnimento esplicito `LCG.PixelGlow_Stop` sia in `actions.finish` che in `untrigger`, eliminando definitivamente i glitch grafici della linea gialla congelata.

### 4.4 Indicatore Statico di Accodamento Rotazionale (Heroic Strike & Cleave)
- Occupa l'intero spazio assegnato di 278x7px a $y = -7$ come barra statica e solida, senza animazione di scorrimento/swipe e senza numeri di tempo rimanente.
- Logica di queuing dinamico per Heroic Strike e Cleave tramite `IsCurrentSpell()`:
  - Pixel Glow dorato (`LibCustomGlow-1.0`) e tinta vertex ADD quando *Heroic Strike* (`47450`) è accodato.
  - Pixel Glow verde smeraldo e tinta vertex ADD quando *Cleave* (`47520`) è accodato.
  - Ritorno all'aspetto copper/bronze neutro quando nessuna abilità è accodata.

### 4.15 Riga Utility Auto-Adattiva a Centratura Dinamica per il War Tank
- **Centratura Dinamica Naturale**: La riga utility inferiore (`05` - `13`, a $y = -45\text{px}$) adotta un'architettura a centratura dinamica naturale ingegnerizzata appositamente per il War Tank.
- **Algoritmo di Centratura Dinamica**: Il motore calcola `activeOrder` contenente esclusivamente gli item equipaggiati e qualificati, ricentrando tutte le icone a $x = 0$ sotto la barra rabbia da $278\text{px}$ tramite $\text{targetX} = \lfloor (i - \frac{N+1}{2}) \times \text{step} + 0.5 \rfloor$, con scaling dinamico del passo ($25\text{px}-52\text{px}$) e della dimensione ($24\text{px}-28\text{px}$) per $N = 3 \dots 11$ icone attive.
- **Whitelist Rigorosa degli Oggetti**:
  1. **Trinket 1 & 2 (Slot 13/14)**: Sempre visibili quando equipaggiati (`itemID > 0`). Database completo ICC/RS/ToC/Ulduar con monitoraggio On-Use, ICD (45s–120s) e procs.
  2. **Anello (Slot 11/12)**: Rigorosamente limitato ad *Ashen Band of Endless Courage* (Tank Armor proc, Spell ID 72414) o *Ashen Band of Endless Vengeance* (Melee AP proc, Spell ID 72412). Anelli a sole statistiche statiche sono totalmente soppressi.
  3. **Mantello (Slot 15)**: Rigorosamente limitato a incanti da combattimento con proc attivo (Sartoria: *Swordguard Embroidery* / *Ricamo della Spada* +400 AP, Spell ID 55775). Il paracadute d'Ingegneria (*Flexweave Underlay*) e tutti gli incanti con statistiche statiche (+22 Agi, +16 Def, +225 Armor) sono tassativamente soppressi.
  4. **Tier Set (08)**: Rigorosamente limitato alla presenza di almeno **4 Pezzi Tier 10** (*Ymirjar Lord's Battlegear* 4P: bonus 20% magic DR durante Shield Block). Soppresso in caso contrario.
  5. **Incanti Arma (Slot 16)**: Rigorosamente limitati a incanti proccabili (*Blade Ward*, *Blood Draining*, *Mongoose*, *Berserking*). Incanti statici (+30 Stamina Titanguard, +20 Strength, ecc.) sono tassativamente soppressi.
  6. **Guanti (Slot 10)**: Rigorosamente limitati a tinker attivi d'Ingegneria (*Reticulated Armor Webbing* +885 Armatura o *Acceleratori Ipersonici*).
  7. **Cooldown Difensivi (`10b`, `11`, `12`)**: `Shield Block` (durata 10s, CD 30s/60s), `Shield Wall` (-60% DR per 12s, glow emergenza <35% HP) e `Last Stand` (+30% vita max per 20s, glow emergenza <35% HP) stabilmente integrati prima degli stivali.
  8. **Stivali (Slot 8)**: Tinker d'Ingegneria *Acceleratori a Nitro* o fallback su *Enraged Regeneration*.
- **Bootstrap Inizializzazione Core**: Poiché WeakAuras 3.3.5a non esegue `actions.init` sui nodi `group`, il bootstrap di `_G.PWHUD_InitCore` e `_G.PWHUD_UpdateUtilityRowPositions` risiede tassativamente nel trigger di `05 - Trinket 1 warTank` (`slot == 13`).

### 4.15 Ottimizzazione Testuale dello Stats Panel (Rimozione % Armor & SBV) e Riconfigurazione Geometrica Compatta (88x60px) con Armonizzazione del Cluster Buff Sovrastante
- **Rimozione Testo Superfluo**:
  - Pulita la riga 2 (`Armor`) rimuovendo `(%.1f%%)` $\rightarrow$ visualizza rigorosamente `Armor: 25.3k` (mantenendo la colorazione dinamica verde al raggiungimento del cap 75% DR).
  - Pulita la riga 4 (`Block`) rimuovendo `(%d SBV)` $\rightarrow$ visualizza rigorosamente `Block: 21.7%`.
  - Il layout finale a 5 righe risulta ultra-pulito, leggibile e privo di testo ridondante.
- **Geometria Compatta 88x60px dello Stats Panel**:
  - Riconfigurato il gruppo `18 - Stats Panel warTank` a $X = -190\text{px}, Y = -45\text{px}$.
  - Sfondo `Stats Panel - Background warTank` dimensionato a $88 \times 60\text{px}$.
  - Testo `Stats Panel - Text warTank` centrato con $X = 2$ e allineato a sinistra, eliminando ogni spazio laterale vuoto.
- **Armonizzazione del Cluster a 4 Buff Sovrastante (20x20px con gap 2px)**:
  - Riconfigurate le 4 icone sovrastanti:
    1. `02 - Battle Shout warTank`: $X = -223\text{px}, Y = 0$, dimensione $20 \times 20\text{px}$ (Active: font 9pt; OFF: font 8pt).
    2. `03 - Commanding Shout warTank`: $X = -201\text{px}, Y = 0$, dimensione $20 \times 20\text{px}$ (Active: font 9pt; OFF: font 8pt).
    3. `04b - Vigilance warTank`: $X = -179\text{px}, Y = 0$, dimensione $20 \times 20\text{px}$ (Active: font 9pt; OFF: font 8pt).
    4. `04 - Defensive Stance warTank`: $X = -157\text{px}, Y = 0$, dimensione $20 \times 20\text{px}$ (OutOfStance: font 7pt).
  - Passo uniforme di $22\text{px}$ ($20\text{px}$ larghezza + $2\text{px}$ gap) con estensione totale di $86\text{px}$ da $X = -233$ a $X = -147$, perfettamente centrato sull'asse $X = -190$ del pannello statistiche sottostante con $1\text{px}$ di margine simmetrico per lato.

---

### 4.16 Armonizzazione delle 4 Icone Sovrastanti a 24x24px e Allineamento Geometrico dello Stats Panel a 96x60px
- **4 Icone Sovrastanti Ingrandite a 24x24px**:
  - Incrementata la dimensione delle 4 icone da 20x20px a 24x24px (+20% in scala lineare, +44% in superficie), migliorando notevolmente il riconoscimento delle illustrazioni e la leggibilità delle scritte OFF e dei timer:
    1. `02 - Battle Shout warTank`: $X = -231\text{px}, Y = 0$, dimensione $24 \times 24\text{px}$ (Active: font 10pt; OFF: font 9pt).
    2. `03 - Commanding Shout warTank`: $X = -205\text{px}, Y = 0$, dimensione $24 \times 24\text{px}$ (Active: font 10pt; OFF: font 9pt).
    3. `04b - Vigilance warTank`: $X = -179\text{px}, Y = 0$, dimensione $24 \times 24\text{px}$ (Active: font 10pt; OFF: font 9pt).
    4. `04 - Defensive Stance warTank`: $X = -153\text{px}, Y = 0$, dimensione $24 \times 24\text{px}$ (OutOfStance: font 8pt).
  - Passo uniforme di $26\text{px}$ ($24\text{px}$ larghezza + $2\text{px}$ gap) con estensione di $102\text{px}$ da $X = -243$ a $X = -141$.
- **Allineamento Geometrico dello Stats Panel a 96x60px**:
  - Riconfigurato `18 - Stats Panel warTank` a $X = -192, Y = -45$ con sfondo $96 \times 60\text{px}$.
  - Perfetta simmetria visiva con 3px di margine per lato rispetto alle icone, 5px di distacco dalla Rage Bar e 10px dalla riga utility.

---

### 4.17 Ottimizzazione Castbar: Scorrimento Player dx->sx, Icona Dinamica della Spell, Priorità Target & Untrigger Istantaneo su Kick/Interruzione
- **Direzione Unificata da Destra a Sinistra (`inverse = True`)**:
  - `Castbar - Player warTank` convertita a riempimento da destra a sinistra (`inverse: True`), perfettamente allineata all'ergonomia dell'HUD.
- **Risoluzione Icona Dinamica della Spell**:
  - Configurato `iconSource: 0` (Trigger Icon) e risolto il troncamento dei ritorni multipli in Lua: l'icona mostra fedelmente la texture esatta dell'abilità o canalizzazione lanciata dal giocatore.
- **Priorità Assoluta del Bersaglio e Cancellazione Istantanea su Kick**:
  - La barra del giocatore si sopprime istantaneamente non appena il bersaglio nemico inizia un lancio.
  - Sostituito l'errato `untrigger: function() return false end` con controlli semantici immediati (`ki == nil` e `spell == nil`), garantendo la sparizione istantanea a schermo in caso di interruzione (kick da parte del player o di alleati, o movimento/stopcast del player).

---

### 4.18 Risoluzione Definitiva Icona Castbar: Auto Trigger Icon, Unpacking Canale 3.3.5a & Aggiornamento Diretto Texture Frame
- **Eliminazione Punto Interrogativo Rosso (`INV_Misc_QuestionMark`)**:
  - Identificato che `auto: False` costringeva WeakAuras a ignorare `customIcon` per visualizzare `displayIcon` su ogni frame. Impostato `auto: True` ed eliminato `INV_Misc_QuestionMark`.
- **Compatibilità API WotLK 3.3.5a per `UnitChannelInfo`**:
  - Corretto l'ordine dei ritorni per gli incantesimi canalizzati: in 3.3.5a restituisce `name, text, texture, startTimeMS, endTimeMS` (la texture è il 3° parametro, non il 4°).
- **Binding Diretto Texture Frame & Fallback**:
  - Integrato fallback con `GetSpellTexture(spell)` e mutazione diretta del frame `aura_env.region.icon:SetTexture(icon)` sia in `customText` che in `customIcon` per garantire l'aggiornamento immediato e privo di latenza dell'icona a schermo.

---

## 5. Glossario & Riferimento Sigle Tecniche Tanking (WotLK 3.3.5a)

| Sigla | Termine Completo | Descrizione Meccanica e Formule WotLK |
| :--- | :--- | :--- |
| **`DEF`** | **Defense Skill** | Skill di difesa (`base + rating`). Cap **540** per immunità dai colpi critici dei boss Lv.83 (-5.6% crit subito), **535** in Eroiche Lv.82. |
| **`ARM`** | **Effective Armor & Physical DR%** | Armatura effettiva del player. Calcola la riduzione del danno fisico contestuale: con costante Blizzard $K = 15232.5$ a Lv.80 default (25.253 armatura $\implies \mathbf{62.4\%}$, identico alla scheda PG in-game) e $K = 16635$ contro Raid Boss Lv.83 ($\implies \mathbf{60.3\%}$, mitigazione effettiva). Hard cap al 75.0%. |
| **`CTC`** | **Combat Table Coverage** | Copertura totale della tabella colpi: $\text{Dodge} + \text{Parry} + \text{Block} + \text{BossMiss}$. A $\ge \mathbf{102.4\%}$ il tank è *Unhittable* (nessun colpo normale subito). Include debuff non-stacking (*Insect Swarm* / *Scorpid Sting* max +3%). |
| **`Block`** | **Block Chance** | Percentuale di blocco con lo scudo. Raggiunge il 100% durante l'abilità attiva *Shield Block* (10s). |
| **`SBV`** | **Shield Block Value** | Quantità fissa di danno assorbito per singolo blocco. Moltiplicatore primario che scala danno e threat di *Shield Slam*. |
| **`Hit`** | **Melee Hit Chance** | Percentuale di colpo a segno con attacchi speciali e Taunt. Cap a **8.0%** (263 rating), ridotto al 7.0% con *Heroic Presence* Draenei. |
| **`Exp`** | **Expertise** | Riduce le schivate e parate del boss. **Soft Cap 26** (214 rating, azzera schivate frontali), **Hard Cap 56** (azzera parate frontali ed elimina il rischio *Parry-Haste*). |
| **`Avoid`** | **Avoidance Pura** | Somma di $\text{Dodge} + \text{Parry} + \text{Miss}$ (percentuale di colpi in cui si incassano **zero danni**). |
| **`DR%`** | **Damage Reduction %** | Percentuale passiva di mitigazione fisica garantita dall'armatura effettiva. |
| **`EHP`** | **Effective Health Pool** | Salute effettiva: $\text{Salute Massima} / (1 - \text{DR}\%)$. |
| **`GCD`** | **Global Cooldown** | Finestra standard di 1.5 secondi tra abilità. |
