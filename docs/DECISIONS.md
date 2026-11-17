# Architecture Decision Records (ADRs) — Protection Warrior 3.3.5a

Questo documento registra le decisioni architetturali e progettuali adottate nello sviluppo della suite **Class Warrior (Protection)**.

---

## ADR-001: Architettura Compiler-Driven Python per Generazione WeakAuras

- **Stato**: Approvato / Implementato
- **Contesto**: La modifica dell'albero WeakAuras all'interno del client di gioco tramite la GUI ufficiale dell'addon genera spesso sovrascritture accidentali, non offre controllo di versione (Git) e rende impraticabile il testing automatizzato.
- **Decisione**: Adottare una pipeline compiler-driven pura in Python (`builder/`), dove ogni elemento HUD è un componente modulare che genera dizionari Python, poi serializzati in AceSerializer-3.0, compressi con raw Deflate RFC 1951 e codificati in base64/LibDeflate.
- **Conseguenze**:
  - Controllo di versione granulare riga per riga su Git.
  - Possibilità di eseguire suite di test unitari e di integrazione in parallelo prima di generare la stringa.
  - Sincronizzazione automatica con il simulatore web tramite script.

---

## ADR-002: Sincronizzazione Orizzontale a 278 px per Barre Centrali

- **Stato**: Approvato / Implementato
- **Contesto**: L'HUD del Guerriero Tank richiede tre visualizzazioni centrali impilate: barra del potere (Rage Bar), barra di lancio target con kick advisor (Castbar) e swing timer (Rotational Bar). Incoerenze di larghezza creano rumore visivo e compromettono la concentrazione.
- **Decisione**: Fissare la larghezza di tutte e tre le barre orizzontali centrali esattamente a **278 px**:
  - `14 - Rage Bar`: 278 x 14 px (Y = -20 px)
  - `15 - Rotational Bar`: 278 x 7 px (Y = -7 px)
  - `16 - Castbar warTank`: 278 x 20 px (Y = +8 px)
- **Conseguenze**: Allineamento visivo perfetto 1:1 con `fury-warrior-335a-am` e `fire-mage-335a-am`.

---

## ADR-003: Gerarchia Prioritaria per l'Advisor Difensivo delle Emergenze

- **Stato**: Approvato / Implementato
- **Contesto**: Quando la salute del tank scende sotto la soglia critica (< 35% HP), premere un cooldown non ottimale o andare in panico porta al decesso. Serve una chiara raccomandazione gerarchica istantanea.
- **Decisione**: Stabilire la seguente catena di priorità per `Emergency Low HP Alert`:
  1. **Shield Wall** (se pronto e non attivo): -60% riduzione assoluta per 12s.
  2. **Last Stand** (se pronto e non attivo): +30% salute massima per 20s.
  3. **Shield Block** (se pronto e non attivo): +100% block chance e raddoppio block value per 10s.
  4. **Enraged Regeneration** (se pronto ed è attivo un effetto di Enrage/Berserker Rage): 30% cura nel tempo.
  5. **Healthstone** (Pietra della salute dello Stregone da inventario).
- **Conseguenze**: Il tank riceve immediatamente a schermo il suggerimento dell'abilità di salvezza più forte disponibile.

---

## ADR-004: Kick Advisor a Rilevamento Postura e Stato Scudo

- **Stato**: Approvato / Implementato
- **Contesto**: Il Guerriero in WotLK 3.3.5a ha due abilità di interruzione principali dipendenti dalla stance: `Shield Bash` (richiede Defensive o Battle Stance ed uno Scudo equipaggiato) e `Pummel` (richiede Berserker Stance). Inoltre, molti boss lanciano magie contrassegnate come non interrompibili (`notInterruptible == true`).
- **Decisione**: Integrare nella Castbar target un doppio controllo dinamico:
  - Ispezione del flag `notInterruptible` ritornato dall'API `UnitCastingInfo` / `UnitChannelInfo`.
  - Se non interrompibile, colorare la barra di Grigio scuro con la dicitura `[IMMUNE]`.
  - Se interrompibile, colorare di Ciano (`#00E5FF`) e indicare in tempo reale:
    - `[KICK: Shield Bash]` se in Stance 1 o 2 con scudo equipaggiato.
    - `[KICK: Pummel]` se in Stance 3 (Berserker).
    - `[STUN: Concussion Blow / Shockwave]` se l'interruzione standard è in cooldown e il bersaglio è stunnabile.
- **Conseguenze**: Eliminazione degli interrupt sprecati sui cast immuni e zero esitazione sull'abilità corretta da premere.

---

## ADR-005: Rilevamento Intelligente Sovrapposizioni di Raid per gli Shouts

- **Stato**: Approvato / Implementato
- **Contesto**: In un gruppo raid con Paladini o Warlock, lanciare Battle Shout o Commanding Shout quando già coperti da buff più forti (o equivalenti) genera spreco di Rabbia e GCD.
- **Decisione**: Implementare la logica zero-clutter:
  - `02 - Battle Shout`: Soppresso e nascosto se il player beneficia di *Blessing of Might* o *Greater Blessing of Might*.
  - `03 - Commanding Shout`: Soppresso e nascosto se nel raid è attivo *Blood Pact* dell'Imp del Warlock.
  - Se il buff del Guerriero è necessario, l'icona mostra il tempo rimanente solo quando `<= 30s`, oppure avverte con icona rossa desaturata `OFF` quando mancante.
- **Conseguenze**: Interfaccia pulita durante i combattimenti e chiamate puntuali solo quando serve rinnovare il grido.

---

## ADR-006: Rilevamento Debuff Letali (Tank Busters) e Boss Enrage

- **Stato**: Approvato / Implementato
- **Contesto**: Gli incontri di raid WotLK contengono abilità letali per i tank: Soul Reaper (Lich King), Impale (Gormok), Gastric Bloat (Festergut), Fusion Punch (XT-002), o abilità di Enrage/Frenzy dei boss.
- **Decisione**: Inserire nel modulo `01 - Procs warTank` due nodi di allerta specialistici:
  - `Tank Buster Alert`: Monitora le cariche critiche (Impale >= 2, Gastric Bloat >= 8, Soul Reaper attivo) e avvisa con testo e bordo rosso pulsante di chiamare il taunt swap o attivare un cooldown maggiore.
  - `Boss Enrage Alert`: Monitora il target per buff di tipo Enrage / Berserk / Frenzy avvisando il tank e il raid.
- **Conseguenze**: Elevata reattività senza necessità di affidarsi unicamente a timer generici di boss mod esterni.

---

## ADR-007: Chiavi Trigger Numeriche Intere e Risoluzione Blocco Import

- **Stato**: Risolto / Implementato
- **Contesto**: Durante i test di importazione in gioco, l'utente ha riscontrato il freeze della finestra di WeakAuras ("si è bloccato l'import").
- **Causa Primaria**: Nei moduli `05-13` (Utility Row), il dizionario dei trigger utilizzava la chiave stringa `"1": { ... }` anziché l'intero numerico `1: { ... }`, ed era omesso `"activeTriggerMode": -10`. In Lua, `triggers["1"]` è una chiave hash separata dall'indice numerico `triggers[1]`. L'iteratore `ipairs` di WeakAuras trovava `nil`, provocando un ciclo di migrazione infinito che congelava il client.
- **Decisione**:
  - Convertire tutte le chiavi dei trigger in interi `1, 2, ...`.
  - Introdurre un'asserzione vincolante permanente nel test `tests/test_components_integrity.py`.
- **Conseguenze**: Risolto completamente il blocco d'importazione, garantendo la conformità sia con versioni 4.0.0 che 5.21.8+.

---

## ADR-008: Adozione del SubRegion `subbackground` nelle Icone

- **Stato**: Approvato / Implementato
- **Contesto**: In WeakAuras per client 3.3.5a, le auras di tipo `icon` che contengono esclusivamente elementi `subtext` possono manifestare anomalie di contrasto o errori di rendering dello sfondo nativo dell'icona Blizzard.
- **Decisione**: Prependere l'elemento `{"type": "subbackground"}` come primo elemento (`index 0`) in `subRegions` di tutte le auras ad icona isolate (Shouts, Stance, Utility Row e Sunder Armor Tracker), uniformando la struttura al 100% con `fury-warrior-335a-am`.
- **Conseguenze**: Rendering estetico privo di artefatti e perfetta parità architetturale tra le suite.

---

## ADR-009: Banca Dati Completa WotLK 3.3.5a per Monili, Anelli, Incanti e Tier Set
- **Stato**: Approvato / Implementato
- **Contesto**: L'utente ha richiesto la parità funzionale completa con `fury-warrior-335a-am`, integrando tutti i monili da tank/threat, anelli reputazione Ashen Verdict, incanti arma (Blade Ward, Blood Draining con 5 stack e cura d'emergenza, Mongoose) e set bonus T7, T8, T9, T10 incluse combinazioni ibride.
- **Decisione**: Integrare tabelle di lookup globali complete in `_G.PWHUD_TrinketDB`, `_G.PWHUD_RingDB`, `_G.PWHUD_WeaponEnchantDB`, `_G.PWHUD_TierDB` gestite dal modulo `builder/components/utility.py`.
- **Conseguenze**: La suite rileva automaticamente e dinamizza gli slot equipaggiati (13, 14, 11/12, 15, 10, 8) senza configurazioni manuali.

---

## ADR-010: Self-Bootstrapping Lua e Risoluzione Crash 'Battle Shout - Active'
- **Stato**: Risolto / Implementato
- **Contesto**: Durante l'importazione in gioco, l'aura `Battle Shout - Active` generava un errore Lua: `This aura has caused a Lua error` provocando l'interruzione della pipeline di rendering di WeakAuras.
- **Causa**: La funzione `_G.PWHUD_GetPlayerBuffs` veniva invocata sul frame `OnUpdate` prima che l'azione `init` del root group fosse eseguita dal motore WeakAuras.
- **Decisione**:
  1. Aggiungere il self-bootstrapping immediato `_G.PWHUD_GetPlayerBuffs = _G.PWHUD_GetPlayerBuffs or {...}` nel corpo stesso del custom trigger.
  2. Convertire il trigger da polling su `update` a trigger reattivo guidato da eventi (`UNIT_AURA,PLAYER_ENTERING_WORLD,PWHUD_BS_THRESHOLD`).
  3. Migrare gli stati OFF di Shouts ad aure native `aura2` con `matchesShowOn: "showOnMissing"`.
- **Conseguenze**: Eliminazione totale dell'errore Lua in gioco e importazione fluida e immediata.

---

## ADR-011: Configurazione di [Devastate] (Talent ID 103) come Load Condition Univoca della Spec Protection
- **Stato**: Approvato / Implementato
- **Contesto**: L'utente ha richiesto esplicitamente che la WeakAura per il Guerriero Tank debba attivarsi esclusivamente se nella spec attiva è presente il talento **[Devastate]** (Devastazione, Spell ID 20243).
- **Decisione**:
  1. In WeakAuras per WoW 3.3.5a (`Prototypes.lua`), la funzione `WeakAuras.CheckTalentByIndex(index)` mappa:
     $$\text{tab} = \left\lceil \frac{\text{index}}{40} \right\rceil, \quad \text{num\_talent} = ((\text{index} - 1) \bmod 40) + 1$$
  2. Nel ramo Protezione (Tab 3), **Devastate** si trova al Tier 8, Colonna 1 (posizione 23).
  3. L'indice matematico lineare è: $(3 - 1) \times 40 + 23 = \mathbf{103}$.
  4. Aggiornata la costante `PROT_WARRIOR_LOAD` in `builder/core/constants.py` con:
     `"talent": {"single": 103, "multi": {103: True}}`, propagata a root e a tutti i nodi figli.
- **Conseguenze**: La suite si carica istantaneamente solo su Guerrieri Protezione talentati con Devastate, rimanendo invisibile su spec Arms, Fury o altre classi.

---

## ADR-012: Notifica Visiva Compatta Out-of-Stance ed Eliminazione Banner Testuali Ridondanti
- **Stato**: Aggiornato / Implementato (Banner testuale superato da filosofia Zero-Clutter)
- **Contesto**: Trovarsi fuori dalla Postura Difensiva durante il combattimento comporta la perdita di mitigazione e threat essenziali per il tank. Tuttavia, l'uso di banner testuali centrali duplicati genera clutter visivo non allineato con le suite Fury Warrior e Fire Mage.
- **Decisione**:
  1. Configurare `04 - Defensive Stance - OutOfStance warTank` (UID `PWHUD_STANCE_WARN`) nel gruppo `04 - Defensive Stance` con Pixel Glow rosso pulsante e label `STANCE` attivo istantaneamente su `UnitAffectingCombat("player") and (GetShapeshiftForm() ~= 2)`.
  2. Mantenere l'icona completamente invisibile quando il guerriero è in Defensive Stance (zero ingombro).
  3. **Eliminazione Banner Testuale**: Rimuovere definitivamente `Alert - Wrong Stance` dal gruppo `17 - Alerts warTank` per preservare il centro dello schermo libero e pulito, affidando l'allerta esclusivamente all'icona compatta reattiva.
  4. Gestire gli eventi tramite `PLAYER_REGEN_DISABLED`, `PLAYER_REGEN_ENABLED`, `UPDATE_SHAPESHIFT_FORM`, azzerando il carico CPU.
- **Conseguenze**: Allerta immediata a colpo d'occhio senza sacrificare la visibilità del terreno di gioco o creare allarmi duplicati.

---

## ADR-013: Riorganizzazione Pannello Statistiche Difensive Stile Fury Warrior e Motore Buff/Debuff
- **Stato**: Approvato / Implementato
- **Contesto**: L'utente ha richiesto di uniformare la resa grafica del pannello statistiche a quella di `fury-warrior-335a-am` (`|cFFFFFFFFLabel:|r <ValoreColorato>`), calcolando accuratamente tutti gli effetti di buff e debuff di boss, mob e raid in WotLK 3.3.5a e gestendo le regole di precedenza/sovrapposizione (non-stacking).
- **Decisione**:
  1. **Stile Tipografico**: Adozione delle etichette bianche su 5 righe: `Def:`, `Armor:`, `CTC:`, `Block:`, `Hit:` con valori colorati dinamicamente in base alle soglie di cap.
  2. **Motore Non-Stacking su Target**: Rilevamento di *Insect Swarm* e *Scorpid Sting* sul bersaglio per assegnare un massimo di +3.0% Miss al boss (evitando somme erronee di +6.0%).
  3. **Adattamento Livello Bersaglio**: Calcolo del Cap Difesa dinamico (540 per Boss Raid Lv.83, 535 per Eroiche Lv.82) e costante di riduzione armatura $K = 16635$.
  4. **Aura di Gruppo Draenei**: Rilevamento di *Heroic Presence* (+1.0% Hit fisico) nel party e verifica Soft Cap 26 ed Hard Cap 56 di Competenza.
  5. **Throttling e Ottimizzazione**: Aggiornamento vincolato a 10 Hz (0.1s) con caching su `_G.PWHUD_LastStatsText` per minimizzare l'impatto sulla CPU in raid.
- **Conseguenze**: Il tank dispone di un pannello completo, visivamente identico a Fury Warrior, con calcoli matematici rigorosi e affidabili contro qualunque boss.


---

## ADR-014: Architettura Riga Utility Auto-Adattiva a Centratura Dinamica con Filtri Selettivi Proc-Only (Parità 1:1 con Fire Mage e Fury Warrior)
- **Stato**: Approvato / Implementato
- **Contesto**: Nella suite Protection Warrior la riga inferiore (`05` - `13`, a $y = -45\text{ px}$) comprende monili, anello, mantello, bonus tier set, incanti arma, guanti d'ingegneria, i 3 cooldown difensivi maggiori del guerriero e stivali. Senza un algoritmo di centratura dinamica, slot non equipaggiati o soppressi genererebbero buchi visivi antiestetici o asimmetrie (icone spostate solo a destra). Inoltre, l'utente richiede una whitelist rigorosa che sopprima oggetti/incanti a statistiche statiche o non qualificati.
- **Decisione**:
  1. **Algoritmo di Centratura Dinamica**: Implementare la funzione globale `_G.PWHUD_UpdateUtilityRowPositions()` con formula matematica di calcolo $X$:
     $$\text{targetX} = \left\lfloor \left( i - \frac{N + 1}{2} \right) \times \text{step} + 0.5 \right\rfloor$$
     adattando il passo orizzontale $\text{step}$ ($25\text{ px}$ a $52\text{ px}$) e la dimensione icona ($24\text{ px}$ a $28\text{ px}$) in base alla cardinalità $N$ degli elementi attivi ($3 \le N \le 11$). Tutte le icone rimangono centrate sotto la barra rabbia da $278\text{ px}$.
  2. **Parità 1:1 con Fire Mage e Fury Warrior**: L'esperienza visiva, la fluidità di riposizionamento all'equipaggiamento/cambio item e l'assenza totale di buchi replicano al 100% l'architettura collaudata delle altre suite HUD.
  3. **Specifiche Tassative di Filtraggio Oggetti (Whitelist Rigorosa)**:
     - **Trinket 1 & 2 (Slot 13/14)**: Sempre visibili quando equipaggiati (database ICC/RS/ToC/Ulduar con tracciamento On-Use, ICD e procs).
     - **Anello (Slot 11/12)**: Solo *Ashen Band of Endless Courage* (Tank Armor proc) o *Endless Vengeance* (Melee AP proc con 60s ICD). Soppresso per anelli a statistiche statiche.
     - **Mantello (Slot 15)**: Solo incanti con proc da combattimento attivo (*Swordguard Embroidery* / Ricamo della Spada). Paracadute d'Ingegneria (*Flexweave Underlay*) e incanti a statistiche statiche (+22 Agi, +16 Def, +225 Armor) sono tassativamente soppressi.
     - **Tier Set (08)**: Solo con bonus 4 Pezzi Tier 10 attivo (*Ymirjar Lord's Battlegear* 4P: bonus Shield Block -20% danno subito). Soppresso in caso contrario.
     - **Incanti Arma (Slot 16)**: Solo incanti proccabili difensivi/offensivi (*Blade Ward*, *Blood Draining*, *Mongoose*, *Berserking*). Soppresso per incanti statici.
     - **Guanti (Slot 10)**: Solo se provvisti di tinker attivo d'Ingegneria (*Reticulated Armor Webbing* o *Hyperspeed Accelerators*).
     - **Cooldown Difensivi (`10b`, `11`, `12`)**: `Shield Block`, `Shield Wall` e `Last Stand` sempre integrati ordinatamente in `activeOrder`.
     - **Stivali (Slot 8)**: Solo se provvisti di tinker attivo d'Ingegneria (*Nitro Boosts*) o fallback su *Enraged Regeneration*.
  4. **Punto Unico di Inizializzazione Core**: Poiché WeakAuras 3.3.5a non esegue `actions.init` sul gruppo radice container, il bootstrap di `_G.PWHUD_InitCore` e la registrazione di `_G.PWHUD_UpdateUtilityRowPositions` risiedono perentoriamente nel trigger di `05 - Trinket 1 warTank` (`slot == 13`).
- **Conseguenze**: Riga perfettamente bilanciata, centrata e reattiva in ogni configurazione di gear, zero buchi visivi, zero spreco di CPU e conformità totale alle direttive dell'utente.
