# Class Warrior (Protection) — WeakAuras Suite

[![WoW Version](https://img.shields.io/badge/World%20of%20Warcraft-3.3.5a%20(12340)-orange.svg)](https://github.com/Glacyal/protection-warrior-335a-am)
[![WeakAuras](https://img.shields.io/badge/WeakAuras-5.21.8+-blue.svg)](https://github.com/Glacyal/protection-warrior-335a-am)
[![Class](https://img.shields.io/badge/Class-Warrior%20(Protection%20Tank)-blue.svg)](https://github.com/Glacyal/protection-warrior-335a-am)
[![GitHub Pages](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-brightgreen.svg)](https://glacyal.github.io/protection-warrior-335a-am/)
[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-gray.svg?logo=paypal&logoColor=white&labelColor=0079c1)](https://www.paypal.me/AMantmar)

Suite WeakAuras completa, modulare e avanzata per **Warrior Protection (Tank) Livello 80** in World of Warcraft 3.3.5a (*Wrath of the Lich King - Build 12340*).  
Progettata per garantire la massima conformità visiva, geometrica e prestazionale con le suite **Class Warrior (Fury)** e **Class Mage (TTW Fire)**: barre centrali sincronizzate a **278px**, riga utility dinamica a $y = -45$, gruppo procs orizzontale a $y = 52$, pannello statistiche $88 \times 60\text{px}$ a $x = -190$ e tracker Sunder Armor a $x = 160$.

---

## 🌐 Anteprima Online (Live Simulator)

Visualizza e interagisci con l'HUD direttamente dal browser senza installare nulla:  
👉 **[Apri il Simulatore Web su GitHub Pages](https://glacyal.github.io/protection-warrior-335a-am/)**  
- **Visuale 1:1 Identica a Fury Warrior**: proporzioni native, barre a 278px, swing timer reattivo con Glow additivo e animazioni clock swipe.
- **Allerta Emergenza Salute Critica (&lt;35% HP)**: suggerimento dinamico prioritizzato del miglior cooldown difensivo pronto (*Shield Wall* > *Last Stand* > *Shield Block* > *Enraged Regen* > *Pozione/Pietra della Salute*).
- **Kick Advisor Dinamico Integrato**: la castbar ($278 \times 20\text{px}$ a $y = +8$) rileva lo stato di interruzione (`notInterruptible`) e consiglia la spell ottimale (*Shield Bash*, *Pummel*, *Stun* o allerta cast *Immune*).
- **Pannello Statistiche Tank Live**: calcolo real-time di Combat Table Coverage (CTC), immunità ai critici dei boss Lv.83 (**540 Difesa**), Armor DR%, Shield Block Value (SBV), Hit/Exp ed EHP.

---

## 🌟 Architettura dell'HUD (20 Nodi Ordinati)

La suite è strutturata in 20 nodi sequenziali controllati dal gruppo principale `Class Warrior (Protection)` ($x = 0, y = -190$, scala $1.2$):

### 1. Gruppo Dinamico Procs (`01 - Procs warTank`)
Posizionato nella parte superiore dell'HUD ($y = 52$), gestisce fino a 7 icone ($34 \times 34\text{px}$, space $6\text{px}$) con riposizionamento orizzontale centrato:
1. **Sword and Board (Buff 50227)**: Shield Slam a costo 0 rabbia e azzeramento del CD, con Pixel Glow dorato pulsante e conto alla rovescia di 5 secondi.
2. **Revenge Ready**: Si attiva con bordo luminoso arancione vivo post Schivata/Parata/Blocco.
3. **Shield Block Active (Buff 2565)**: Durata attiva di 10 secondi con conto alla rovescia ed etichetta `100%`.
4. **Victory Rush**: Proc *Victorious* con countdown di 20 secondi.
5. **Emergency Low HP Alert**: Icona con Pixel Glow rosso lampeggiante quando la salute scende sotto il 35%, mostrando l'icona del cooldown consigliato pronto (*Shield Wall* o *Last Stand*).
6. **Boss Enrage Alert**: Segnalazione immediata con Glow rosso quando il boss entra in Enrage/Frenzy/Berserk per attivare mitigazioni pesanti o chiamare il Tranq Shot.
7. **Tank Buster Alert**: Notifica con Glow rosso in caso di debuff letali sul tank (*Soul Reaper*, *Impale* $\ge 2$ stacks, *Gastric Bloat* $\ge 8$ stacks) per coordinare lo swap del Taunt.

### 2. Buff di Classe & Postura Difensiva (`02`, `03`, `04`)
Posizionati a sinistra a $x = -222, -190, -158$ e $y = 0$:
- **02 - Battle Shout**: Compare con timer solo se in scadenza ($\le 30\text{s}$) o desaturato con scritta `OFF` se manca sia Battle Shout che *Blessing of Might* del Paladino.
- **03 - Commanding Shout**: Compare con timer solo se in scadenza ($\le 30\text{s}$) o desaturato con scritta `OFF` se manca sia Commanding Shout che *Blood Pact* dell'Imp.
- **04 - Defensive Stance**: Allerta immediata ad alta visibilità con Glow rosso ed etichetta `STANCE` se il guerriero si trova fuori dalla *Defensive Stance* durante il combattimento.

### 3. Riga Utility Inferiore (`05` - `13`, a $y = -45$)
Centratura automatica orizzontale adattiva sotto la barra della rabbia con icone $28 \times 28\text{px}$:
- **05 - Trinket 1 warTank** & **06 - Trinket 2 warTank**: Slot 13 e 14 con rilevamento automatico monili tank (*Sindragosa's Flawless Fang*, *Glyph of Indomitability*, *Corpse Tongue Coin*, *Satrina's Impeding Scarab*, *Corroded Skeleton Key*, ecc.).
- **06b - Ring warTank**: Rilevamento anello tanking (*Ashen Band of Endless Courage*).
- **07 - Cloak warTank**: Paracadute/Flexweave e incanti mantello.
- **08 - Tier Set warTank**: Tracciamento bonus set T9 e T10 Prot (*Ymirjar Lord* 2P/4P).
- **09 - Enchants warTank**: Incanti arma tanking (*Blade Ward*, *Blood Draining*, *Mongoose*).
- **10 - Gloves warTank**: *Reticulated Armor Webbing* (+885 Armatura) o *Acceleratori Ipersonici*.
- **11 - Shield Wall**: Spell 871 (-60% DR per 12s, swipe durata e CD).
- **12 - Last Stand**: Spell 12975 (+30% HP per 20s, swipe durata e CD).
- **13 - Boots warTank**: *Acceleratori a Nitro* (Ingegneria) o *Enraged Regeneration*.

### 4. Barre Centrali Sincronizzate a 278px (`14`, `15`, `16`)
- **14 - Rage Bar ($278 \times 14\text{px}$ a $y = -20$)**: Valore numerico esatto al centro (%p) con colorazione a 3 stadi: rosso scuro sotto 25 punti (starvation), crimson pieno tra 25 e 44 punti e ambra/oro sopra i 45 punti (soglia scarico sicuro Heroic Strike/Cleave).
- **15 - Rotational Bar ($278 \times 7\text{px}$ a $y = -7$)**: Barra centrale con swing timer della mano primaria e retroilluminazione dinamica additiva (Pixel Glow dorato quando *Heroic Strike* è accodato, verde smeraldo quando *Cleave* è accodato).
- **16 - Castbar warTank ($278 \times 20\text{px}$ a $y = +8$)**: Barra di lancio sincronizzata con il bersaglio (o player). Mostra icona a sinistra, nome incantesimo con **Kick Advisor** integrato a sinistra (es. `Frostbolt [KICK: SHIELD BASH]` in ciano, o `[IMMUNE]` in grigio) e tempo residuo a destra (%p).

### 5. Avvisi Testuali Centrali (`17 - Alerts warTank`)
Gruppo posizionato a $y = 78$ appena sopra i procs:
- **Alert - Sword and Board**: Scritta `SHIELD SLAM READY!` in giallo dorato con suono Tamburi di Guerra (*Drums*).
- **Alert - Emergency CD**: Notifica critica `CRIT HP: USE SHIELD WALL!` con allarme sonoro.
- **Alert - Kick Now**: Indicazione `INTERRUPT: SHIELD BASH!`.
- **Alert - Boss Enraged**: Notifica `BOSS ENRAGED! POP CD!`.

### 6. Pannello Statistiche Tanking (`18 - Stats Panel warTank`)
Box compatto $88 \times 60\text{px}$ a $x = -190, y = -45$ (sul lato sinistro della riga utility):
```text
DEF: 542 (CAP)
CTC: 102.4% (MAX)
ARM: 27.5k (68.2%)
SBV: 2,180
H: 8.2%  E: 26
```
- **DEF**: Verifica del raggiungimento del cap di **540 Difesa** per l'immunità dai colpi critici dei boss di raid livello 83.
- **CTC**: Combat Table Coverage (Schivata% + Parata% + Blocco% + Miss%) con indicazione di copertura totale.
- **ARM**: Armatura effettiva e percentuale di riduzione danno fisico ($\text{DR} = \frac{\text{Armor}}{\text{Armor} + 16635}$).
- **SBV**: Shield Block Value per il calcolo del danno e del threat di Shield Slam.
- **H/E**: Cap 8% Melee Hit (263 rating) e soft cap 26 Perizia (214 rating).

### 7. Sunder Armor Tracker (`19 - Sunder Armor Tracker`)
Posizionato sul lato destro delle barre ($x = 160, y = -7$, $32 \times 32\text{px}$):
- Tracciamento delle cariche di Sunder Armor (1-5 cariche, stack count verde `x5`) o *Expose Armor* del Ladro (`EA` in ciano).
- Timer numerico di scadenza alla base.
- Allerta rossa `OFF` quando il debuff manca sul bersaglio corrente in combattimento.

---

## 📥 Come Importare la Stringa WeakAuras

1. Apri il file [`IMPORT_STRING_v5.21.8.txt`](file:///d:/0Progetti/protection-warrior-335a-am/IMPORT_STRING_v5.21.8.txt) oppure copiala con un clic dal [Simulatore Web](https://glacyal.github.io/protection-warrior-335a-am/).
2. In gioco, apri l'interfaccia digitando `/wa`.
3. Clicca su **Importa** in alto a sinistra.
4. Incolla la stringa con `Ctrl + V` e premi **Importa Gruppo**.

---

## 🛠️ Manutenzione & Compilazione

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
