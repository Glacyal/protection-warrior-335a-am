# Class Warrior (Protection) — WeakAuras Suite

[![WoW Version](https://img.shields.io/badge/World%20of%20Warcraft-3.3.5a%20(12340)-orange.svg)](https://github.com/Glacyal/protection-warrior-335a-am)
[![WeakAuras](https://img.shields.io/badge/WeakAuras-5.21.8+-blue.svg)](https://github.com/Glacyal/protection-warrior-335a-am)
[![Class](https://img.shields.io/badge/Class-Warrior%20(Protection%20Tank)-blue.svg)](https://github.com/Glacyal/protection-warrior-335a-am)
[![GitHub Pages](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-brightgreen.svg)](https://glacyal.github.io/protection-warrior-335a-am/)
[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-gray.svg?logo=paypal&logoColor=white&labelColor=0079c1)](https://www.paypal.me/AMantmar)

Suite WeakAuras completa, modulare e avanzata per **Warrior Protection (Tank) Livello 80** in World of Warcraft 3.3.5a (*Wrath of the Lich King - Build 12340*).  
Progettata per garantire la massima sopravvivenza in raid e dungeon, un monitoraggio impeccabile dei cooldown difensivi, gestione intelligente delle **Interruzioni (Kick / Shield Bash / Pummel / Stun)**, allarmi per colpi critici/tank buster, supporto automatico al **Taunt swap** e calcolo real-time di tutte le metriche tanking (CTC, Difesa 540, SBV, Armatura DR ed EHP).

---

## 🌐 Anteprima Online (Live Simulator)

Visualizza e interagisci con l'HUD direttamente dal browser senza installare nulla:  
👉 **[Apri il Simulatore Web su GitHub Pages](https://glacyal.github.io/protection-warrior-335a-am/)**  
- **Allerta Emergenza Salute Critica (&lt;35% HP)**: suggerimento dinamico prioritizzato del miglior cooldown difensivo pronto (*Shield Wall* > *Last Stand* > *Shield Block* > *Enraged Regen* > *Pozione/Pietra della Salute*).
- **Kick Advisor Dinamico**: monitoraggio del cast nemico con rilevamento nativo di cast interrompibili vs cast immuni/protetti (`notInterruptible`), con indicazione esatta dell'abilità da usare in base a postura e scudo.
- **Rotazione & Priorità con Sword and Board**: Glow dorato su Shield Slam a costo 0 rabbia e reset del CD; Revenge reattivo post-blocco/schivata/parata con Glow arancione fuoco.
- **Pannello Statistiche Tank Live**: calcolo real-time di Combat Table Coverage (CTC), immunità ai critici dei boss Lv.83 (**540 Difesa**), Armor DR%, Shield Block Value (SBV), Hit/Exp e Vita Effettiva (EHP).

---

## 🌟 Architettura dell'HUD (20 Nodi Ordinati)

La suite è strutturata in 20 nodi sequenziali controllati dal gruppo principale `Class Warrior (Protection)`:

### 1. Emergenza & Allarmi Centrali (`01 - Emergency & Procs warTank`)
- **Salute Critica (&lt;35% HP)**: Allarme visivo centrale e lampeggiante con raccomandazione contestuale dell'azione salvavita:
  1. *Shield Wall* (-60% danni subiti, priorità assoluta per mitigare colpi letali).
  2. *Last Stand* (+30% HP massimi e correnti se Shield Wall è in ricarica).
  3. *Shield Block* (+100% chance di blocco e +100% SBV per assorbire raffiche fisiche).
  4. *Enraged Regeneration* (+30% cura nel tempo se il tank è sotto effetto Enrage/Bloodrage).
  5. *Healthstone / Pozione* (se tutti i cooldown di classe sono in ricarica).
- **Sword and Board (Spell ID 50227)**: Icona centrale con bordo dorato pulsante e conto alla rovescia di 5 secondi: Shield Slam azzerato e a 0 costo di rabbia!

### 2. Interruzioni & Riflessione Magica (`02 - Kick Advisor` & `17 - Spell Reflect`)
- **Rilevamento Intelligente Cast Bersaglio**:
  - Intercetta i lanci nemici (`UNIT_SPELLCAST_START` e `CHANNEL`).
  - **Cast Interrompibile**:
    * Postura Difensiva o Battaglia con scudo: Suggerisce **`KICK: SHIELD BASH`** (Spell ID 72).
    * Postura Berserker: Suggerisce **`KICK: PUMMEL`** (Spell ID 6552).
    * Se Shield Bash è in ricarica: Suggerisce **`STANCE DANCE -> PUMMEL`** oppure gli stun **`STUN: CONCUSSION BLOW`** / **`STUN: SHOCKWAVE`**.
  - **Cast Protetto / Immune (`notInterruptible == true`)**:
    * Evidenzia chiaramente **`IMMUNE TO KICK!`** suggerendo di attivare **`SPELL REFLECT`** o un cooldown di mitigazione.
- **Spell Reflection (Spell ID 23920)**: Monitora il buff attivo (5s) e la ricarica rapida (8s con talento).

### 3. Cooldown Difensivi Maggiori (`03`, `14`, `15`, `16`)
- **14 - Shield Wall Alert warTank**: Spell ID 871 (-60% DR per 12s, CD 2m con talento/glifo).
- **15 - Last Stand Alert warTank**: Spell ID 12975 (+30% HP per 20s, CD 2m/3m).
- **16 - Shield Block Tracker warTank**: Spell ID 2565 (10s di durata con 100% blocco e ricarica rapida 30s/40s).
- **03 - Defensive Cooldowns warTank**: Monitoraggio di *Enraged Regeneration* (Spell ID 55694).

### 4. Barra Rotazionale & Swing Timer (`04` & `20`)
- **Shield Slam (Spell ID 47488)**: Priorità n. 1, cooldown swipe, raggio e Glow dorato reattivo a Sword and Board.
- **Revenge (Spell ID 57823)**: Priorità n. 2, si attiva con Glow arancione fuoco dopo aver parato, schivato o bloccato un colpo (gestione colpi doppi con *Improved Revenge*).
- **Shockwave (Spell ID 46968)**: Priorità n. 3, stun ad area frontale 4s e threat AoE massiccio.
- **Devastate (Spell ID 47498)**: Priorità n. 4, filler principale che mostra il conteggio stack Sunder Armor (1-5) direttamente sull'icona.
- **Concussion Blow (Spell ID 12809)**: Priorità n. 5, stun singolo 5s.
- **20 - Swing & HS Queue warTank**: Swing timer della mano primaria con Glow ambra/oro quando *Heroic Strike* o *Cleave* è accodato sul colpo successivo, e indicatore di scarico sicuro quando la rabbia supera i 45 punti.

### 5. Controllo Postura & Debuff Boss (`05` & `18`)
- **05 - Debuffs & Stance warTank**:
  - Verifica Postura Difensiva: allarme sonoro e visivo immediato se il tank entra in combattimento fuori da *Defensive Stance*.
  - Verifica *Thunder Clap* (-20% Attack Speed nemico) e *Demoralizing Shout* (-575 AP nemico): notifica se il boss non ha il debuff applicato!
- **18 - Sunder Armor Tracker warTank**:
  - Tracciamento delle cariche di Sunder Armor / Expose Armor (da 1 a 5 cariche) con barra durata e colorazione (Rosso = 0, Giallo = 1-4, Verde = 5/5).

### 6. Taunt & Threat Utility (`06`)
- Cooldown timer per *Taunt* (8s), *Mocking Blow* (2m) e *Challenging Shout* (10m).
- **Allarme Taunt Miss / Resist**: Intercetta tramite combat log i fallimenti del Taunt avvisando immediatamente il tank di usare il taunt di riserva (*Mocking Blow*) o coordinare lo swap.

### 7. Barre Centrali (`07`, `08`, `09`)
- **07 - Rage Bar**: Valore numerico esatto con colorazione a soglie: rosso scuro (<15 starvation), crimson (15-44 normale), ambra/oro (>=45 scarico sicuro).
- **08 - Health Bar**: Percentuale e vita numerica con soglie cromatiche (verde >65%, ambra 35-65%, rosso lampeggiante <35%).
- **09 - Castbar warTank**: Castbar del bersaglio con differenziazione cromatica ciano (interrompibile) vs grigio (protetto).

### 8. Pannello Statistiche Tanking (`10 - Stats Panel warTank`)
Visualizzazione a 3 righe a centro schermo ($y = -120$):
```text
DEF: 542/540 [IMMUNE]    CTC: 102.4% [FULL BLK]
ARM: 27.5k (68.2% DR)    SBV: 2,180
HIT: 8.2%   EXP: 26/26   EHP: 118k
```
- **DEF**: Verifica del raggiungimento del cap di **540 Difesa** per l'immunità dai colpi critici dei boss di raid livello 83.
- **CTC**: Combat Table Coverage (Schivata% + Parata% + Blocco% + Miss%) con indicazione di blocco totale / uncrushable.
- **ARM & DR%**: Armatura effettiva e percentuale di riduzione danno fisico calcolata con la formula ufficiale di WotLK 3.3.5a: $\text{DR} = \frac{\text{Armor}}{\text{Armor} + 16635}$.
- **SBV**: Shield Block Value per il calcolo del danno e del threat di Shield Slam.
- **HIT & EXP**: Controllo cap 8% Melee Hit (263 rating) e soft cap 26 Perizia (214 rating).
- **EHP**: Effective Health Pool $(\frac{\text{Max HP}}{1 - \text{DR}})$.

### 9. Monili & Equipaggiamento (`11`, `12`, `13`)
- Monitoraggio automatico di Monili Tanking nello Slot 13 e 14 (*Sindragosa's Flawless Fang*, *Glyph of Indomitability*, *Corpse Tongue Coin*, *Satrina's Impeding Scarab*, *Corroded Skeleton Key*, ecc.).
- Rilevamento di incanti Ingegneria su Guanti (*Reticulated Armor Webbing* +885 Armatura / *Hyperspeed Accelerators*) e Stivali (*Nitro Boosts*).

---

## 📥 Come Importare la Stringa WeakAuras

1. Apri il file [`IMPORT_STRING_v5.21.8.txt`](file:///d:/0Progetti/protection-warrior-335a-am/IMPORT_STRING_v5.21.8.txt) oppure copiala con un clic dal [Simulatore Web](https://glacyal.github.io/protection-warrior-335a-am/).
2. In gioco, apri l'interfaccia digitando `/wa`.
3. Clicca su **Importa** in alto a sinistra.
4. Incolla la stringa con `Ctrl + V` e premi **Importa Gruppo**.

---

## 🛠️ Manutenzione & Compilazione

La suite utilizza un compilatore Python deterministico:
- **Compilazione Stringa**:
  ```bash
  python generate.py
  ```
- **Sincronizzazione Simulatore Web**:
  ```bash
  python scripts/sync_docs.py
  ```
- **Suite di Test Paralleli**:
  ```bash
  python tests/run_parallel_tests.py
  ```

---

## 📄 Licenza
Rilasciato sotto licenza MIT. Sviluppato per la community WotLK 3.3.5a.
