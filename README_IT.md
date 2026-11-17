> 🇬🇧 **English Version**: [README.md](README.md)
>
> 🌐 **Live Web Simulator**: [https://glacyal.github.io/protection-warrior-335a-am/](https://glacyal.github.io/protection-warrior-335a-am/)

# Class Warrior (Protection) — WeakAuras Suite

[![WoW Version](https://img.shields.io/badge/World%20of%20Warcraft-3.3.5a%20(12340)-orange.svg)](https://github.com/Glacyal/protection-warrior-335a-am)
[![WeakAuras](https://img.shields.io/badge/WeakAuras-5.21.8+-blue.svg)](https://github.com/Glacyal/protection-warrior-335a-am)
[![Class](https://img.shields.io/badge/Class-Warrior%20(Protection%20Tank)-blue.svg)](https://github.com/Glacyal/protection-warrior-335a-am)
[![GitHub Pages](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-brightgreen.svg)](https://glacyal.github.io/protection-warrior-335a-am/)
[![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-gray.svg?logo=paypal&logoColor=white&labelColor=0079c1)](https://www.paypal.me/AMantmar)

Suite WeakAuras completa, modulare e avanzata per **Warrior Protection (Tank) Livello 80** in World of Warcraft 3.3.5a (*Wrath of the Lich King - Build 12340*).  
Progettata per garantire la massima conformità visiva, geometrica e prestazionale con le suite **Class Warrior (Fury)** e **Class Mage (TTW Fire)**: barre centrali sincronizzate a **278px**, riga utility dinamica a $y = -45$, gruppo procs orizzontale a $y = 52$, pannello statistiche $88 \times 60\text{px}$ a $x = -190$ e tracker Sunder Armor a $x = 160$.

La suite è condizionata al caricamento esclusivo su guerrieri con il talento **[Devastate]** (Devastazione, Indice WeakAuras `103`, Tab 3 Protezione, Posizione 23), disattivandosi automaticamente su spec Arms o Fury.

---

## 🌐 Anteprima Online (Live Simulator)

Visualizza e interagisci con l'HUD direttamente dal browser senza installare nulla:  
👉 **[Apri il Simulatore Web su GitHub Pages](https://glacyal.github.io/protection-warrior-335a-am/)**  
- **Visuale 1:1 Identica a Fury Warrior**: proporzioni native, barre a 278px, swing timer reattivo con Glow additivo e animazioni clock swipe.
- **Allerta Emergenza Salute Critica (<35% HP)**: suggerimento dinamico prioritizzato del miglior cooldown difensivo pronto (*Shield Wall* > *Last Stand* > *Shield Block* > *Enraged Regen* > *Pozione/Pietra della Salute*).
- **Kick Advisor Dinamico Integrato**: la castbar ($278 \times 20\text{px}$ a $y = +8$) rileva lo stato di interruzione (`notInterruptible`) e consiglia la spell ottimale (*Shield Bash*, *Pummel*, *Stun* o allerta cast *Immune*).
- **Pannello Statistiche Tank Live**: calcolo real-time di Combat Table Coverage (CTC), immunità ai critici dei boss Lv.83 (**540 Difesa**), Armor DR%, Shield Block Value (SBV), Hit/Exp ed EHP.

---

## 🌟 Architettura dell'HUD (20 Nodi Ordinati)

La suite è strutturata in 20 nodi sequenziali controllati dal gruppo principale `Class Warrior (Protection)` ($x = 0, y = -190$, scala $1.2$):

### 1. Gruppo Dinamico Procs (`01 - Procs warTank`)
Posizionato nella parte superiore dell'HUD ($y = 52$), configurato con `sort: "none"` per imporre rigorosamente una gerarchia visiva salvavita da sinistra verso destra:
1. **Emergency Low HP Alert**: Icona con Pixel Glow rosso lampeggiante quando la salute scende sotto il 35%, posizionata all'estrema sinistra (Posizione 1) mostrando l'icona del cooldown consigliato pronto (*Shield Wall* o *Last Stand*).
2. **Tank Buster Alert**: Allerta dinamica ad altissima priorità posizionata alla Posizione 2 per tutti i boss raid WotLK 3.3.5a e trash letali (*Soul Reaper*, *Phase Punch*, *Rune of Blood*, *Impale*, *Gastric Bloat*, *Fusion Punch*, *Fiery Combustion*, ecc.) con commutazione dinamica dell'icona del debuff, swipe circolare, etichette d'azione (`SWAP`, `x8`, `HEAL`, `RUN`, `PLASMA`), e Pixel Glow rosso intenso.
3. **Revenge Ready warTank**: Posizionato in Posizione 3, attivato da qualsiasi Schivata, Parata o Blocco (`blocked > 0`) con finestra temporale di 5.0 secondi, refresh dinamico ad ogni avoid/blocco, animazione swipe circolare, Pixel Glow ambra (`LibCustomGlow-1.0`), etichetta `REV` centrata in alto (`INNER_TOP`) e timer decimale in basso (`INNER_BOTTOM`).
4. **Sword and Board (Buff 50227)**: Posizionato in Posizione 4, proc di Shield Slam a costo 0 con azzeramento del cooldown, Pixel Glow dorato pulsante, conto alla rovescia di 5 secondi, etichetta `SLAM` centrata in alto (`INNER_TOP`) e timer decimale in basso (`INNER_BOTTOM`).
5. **Demoralizing Shout Tracker warTank**: Tracker debuff per riduzione danno fisico. Attivo esclusivamente su bersagli maggiori ($\ge 500.000	ext{ HP}$) per eliminare il disturbo sui trash mob. Raid-aware (soddisfatto da Warrior *Demoralizing Shout*, Feral Druid *Demoralizing Roar*, o Warlock *Curse of Weakness*). Icona pulita senza scritte di testo. Scompare automaticamente quando attivo con durata abbondante ($> 10	ext{s}$); ricompare con swipe circolare e timer decimale (`%.1f`, stile Slam) quando in scadenza ($\le 10	ext{s}$); proietta `MISS` in rosso se mancante.
6. **Thunder Clap Tracker warTank**: Tracker debuff per riduzione velocità d'attacco in mischia. Attivo esclusivamente su bersagli maggiori ($\ge 500.000	ext{ HP}$). Raid-aware (soddisfatto da Warrior *Thunder Clap*, DK *Frost Fever*, Paladin *Judgements of the Just*, o Feral Druid *Infected Wounds*). Icona pulita senza scritte di testo. Scompare quando sano ($> 10	ext{s}$); ricompare con swipe e timer decimale (`%.1f`) quando in scadenza ($\le 10	ext{s}$); proietta `MISS` se mancante.
7. **Rend Tracker warTank**: Tracker debuff sanguinamento del guerriero. Attivo esclusivamente su bersagli maggiori ($\ge 500.000	ext{ HP}$). Icona pulita senza scritte di testo. Scompare quando sano ($> 5	ext{s}$); ricompare con swipe e timer decimale (`%.1f`) quando in scadenza ($\le 5	ext{s}$); soppresso automaticamente sui bersagli meccanici immuni. Proietta `MISS` all'estrema destra se mancante.

### 2. Buff di Classe & Postura Difensiva (`02`, `03`, `04`)
Posizionati a sinistra direttamente sopra il pannello statistiche a $x = -264, -232, -200, -168$ e $y = 0$ (griglia a 4 icone da $30 \times 30\text{px}$ con 2px di spaziatura, combaciante con i 126px del pannello sottostante):
- **02 - Battle Shout warTank**: Timer attivo Battle Shout / allerta buff mancante (OFF).
- **03 - Commanding Shout warTank**: Timer attivo Commanding Shout / allerta buff mancante (OFF).
- **04b - Vigilance warTank**: Allerta Vigilanza mancante su alleato (OFF) su puro modello Focus Magic (icona desaturata con scritta OFF se nessun alleato ha la vigilanza; countdown quando $\le 60\text{s}$).
- **04 - Defensive Stance warTank**: Allerta postura errata fuori dalla Defensive Stance in combattimento (STANCE).
- **02 - Battle Shout warTank**: Compare con timer solo se in scadenza ($\le 30\text{s}$) o desaturato con scritta `OFF` se manca sia Battle Shout che *Blessing of Might* del Paladino.
- **03 - Commanding Shout warTank**: Compare con timer solo se in scadenza ($\le 30\text{s}$) o desaturato con scritta `OFF` se manca sia Commanding Shout che *Blood Pact* dell'Imp.
- **04 - Defensive Stance warTank**: Allineato al modello Fury Warrior (invisibile durante la corretta Defensive Stance; compare con allerta rossa e label `STANCE` solo fuori postura in combattimento tramite `04 - Defensive Stance - OutOfStance warTank`).

### 3. Riga Utility Inferiore (`05` - `13`, a $y = -45$)
Centratura automatica orizzontale adattiva sotto la barra della rabbia con icone $28 \times 28\text{px}$:
- **05 - Trinket 1 warTank** & **06 - Trinket 2 warTank**: Slot 13 e 14 con rilevamento automatico monili tank (*Sindragosa's Flawless Fang*, *Glyph of Indomitability*, *Corpse Tongue Coin*, *Satrina's Impeding Scarab*, *Corroded Skeleton Key*, ecc.).
- **06b - Ring warTank**: Rilevamento anello tanking (*Ashen Band of Endless Courage*).
- **07 - Cloak warTank**: Tracciamento incanti mantello con proc da combattimento (*Ricamo della Spada* +400 AP; il paracadute di Ingegneria e gli incanti statici come +22 Agilità o +16 Difesa vengono automaticamente soppressi per pulizia visiva).
- **08 - Tier Set warTank**: Cooldown difensivo T10 4P con icona *Bloodrage* (traccia lo scudo da 10s pari al 20% di HP di *Blood Frenzy*, il tempo di ricarica di Bloodrage, e si nasconde automaticamente se non si indossa il 4P).
- **09 - Enchants warTank**: Monitoraggio incanti arma proccabili (*Blade Ward*, *Blood Draining*, *Mongoose*, *Berserking*, ecc.). Visibile esclusivamente quando l'arma equipaggia un incanto che può realmente proccare; soppresso e nascosto automaticamente in presenza di incanti statici (+30 Stamina Titanguard, +25 Hit/+25 Crit Accuracy, Titanium Weapon Chain, +26 Agility, +65 AP) o nessun incanto, con ricalcolo e ricentratura automatica della barra utility.
- **10 - Gloves warTank**: *Reticulated Armor Webbing* (+885 Armatura) o *Acceleratori Ipersonici*.
- **10b - Shield Block warTank**: Tracciamento Shield Block a Y: -45 a fianco di Shield Wall (durata attiva 10s con swipe/timer, ricarica cooldown 30s/60s e stato pronto pulito).
- **11 - Shield Wall warTank**: Spell 871 (-60% DR per 12s, swipe durata e CD).
- **12 - Last Stand warTank**: Spell 12975 (+30% HP per 20s, swipe durata e CD).
- **13 - Boots warTank**: *Acceleratori a Nitro* (Ingegneria) o *Enraged Regeneration*.

### 4. Barre Centrali Sincronizzate a 278px (`14`, `15`, `16`)
- **14 - Rage Bar warTank ($278 \times 14\text{px}$ a $y = -20$)**: Valore numerico esatto al centro (%p) con colorazione a 3 stadi: rosso scuro sotto 25 punti (starvation), crimson pieno tra 25 e 44 punti e ambra/oro sopra i 45 punti (soglia scarico sicuro Heroic Strike/Cleave).
- **15 - Rotational Bar warTank ($278 \times 7\text{px}$ a $y = -7$)**: Indicatore statico di accodamento rotazionale a piena larghezza (278px) senza animazione di scorrimento/swipe e senza numeri di tempo rimanente. Gestito con polling frame-accurate `OnUpdate` e risoluzione universale `GetSpellInfo()`:
  - Barra solida copper/bronze (`[0.65, 0.35, 0.12, 0.90]`) a riposo.
  - Barra Oro brillante (`[1.0, 0.84, 0.0, 1.0]`) con Pixel Glow dorato `LibCustomGlow-1.0` all'accodamento di *Heroic Strike*.
  - Barra Verde Smeraldo brillante (`[0.1, 0.95, 0.2, 1.0]`) con Pixel Glow verde `LibCustomGlow-1.0` all'accodamento di *Cleave*.
  - Ritorno immediato all'aspetto neutro al rilascio del colpo o alla cancellazione.
- **16 - Castbar warTank ($278 \times 20\text{px}$ a $y = +8$)**: Barra di lancio speculare sincronizzata con intelligenza direzionale e priorità assoluta del target:
  - **Castbar Bersaglio (Destra &rarr; Sinistra, `inverse: true`)**: Scorrimento inverso di pericolo da destra verso sinistra per incantesimi di mob e boss. Icona a sinistra, tempo residuo a destra e advisor contestuale Opzione A:
    * `Spell [SHIELD BASH]` (Ciano `[0.0, 0.85, 1.0]`) per lanci interrompibili a raggio di mischia.
    * `Spell [SPELL REFLECTION]` (Magenta/Viola `[0.78, 0.25, 0.95]`) per magie dirette puntate sul tank con scudo equipaggiato, suggerito con priorità anche a distanza ($> 5\text{yd}$) o con Shield Bash in ricarica.
    * `Spell [IMMUNE]` (Grigio piombo `[0.50, 0.50, 0.50]`) per abilità protette non interrompibili.
  - **Castbar Giocatore (Sinistra &rarr; Destra, `inverse: false`)**: Scorrimento classico in avanti da sinistra a destra per lanci del player (Tiro, Lancio, professioni) in perfetto stile Fire Mage; si nasconde istantaneamente per cedere il passo ogni volta che il bersaglio inizia a castare.

### 5. Avvisi Testuali Centrali (`17 - Alerts warTank`)
Gruppo posizionato a $y = 78$ appena sopra i procs:
- **Alert - Sword and Board**: Scritta `SHIELD SLAM READY!` in giallo dorato con suono Tamburi di Guerra (*Drums*).
- **Alert - Emergency CD**: Notifica critica `CRIT HP: USE SHIELD WALL!` con allarme sonoro.
- **Alert - Kick Now**: Indicazione `INTERRUPT: SHIELD BASH!`.
*(Nota: I banner testuali invasivi per Boss Enraged e Wrong Stance sono stati rimossi per preservare la massima pulizia visiva centrale; gli errori di postura sono segnalati dall'icona compatta dedicata in `04 - Defensive Stance warTank`)*.

### 6. Pannello Statistiche Tanking Stile Fury Warrior (`18 - Stats Panel warTank`)
Box compatto $88 \times 60\text{px}$ a $x = -190, y = -45$ (sul lato sinistro della riga utility) con etichette bianche `Label:` e valori colorati con soglie dinamiche:
```text
Def:   541 (CAP)
Armor: 25.3k (62.4%)
CTC:   74.6%
Block: 21.7% (1800 SBV)
Hit:   9.1% | 25 Exp
```

#### 📖 Glossario & Spiegazione delle Sigle Statistiche Tank
| Sigla | Nome Esteso | Significato e Rilevanza Tattica in WotLK 3.3.5a |
| :--- | :--- | :--- |
| **`DEF`** | **Defense Skill** *(Abilità di Difesa)* | Punteggio totale di difesa (`base + bonus`). A livello 80 il valore base è 400. Raggiungere **540 Difesa** garantisce la completa **immunità ai colpi critici** dei Boss di Raid Lv.83 (-5.6% crit subito). In dungeon eroici (mob Lv.82) il cap è **535 Difesa**. |
| **`ARM`** | **Armor & Physical DR%** *(Armatura & Riduzione Danno)* | Quantità di armatura effettiva. La percentuale tra parentesi indica la riduzione del danno fisico contestuale: calcolata con costante Blizzard $K = 15232.5$ a Lv.80 (es. 25.253 armatura $\implies \mathbf{62.4\%}$, esattamente conforme al $62.38\%$ visualizzato nel tooltip in-game della scheda del personaggio) e con $K = 16635$ contro Raid Boss Lv.83 / Skull ($\implies \mathbf{60.3\%}$, mitigazione effettiva sul boss). L'hard cap è al **75.0%**. Include buff attivi (*Inspiration/Ancestral Fortitude* +25%) e debuff. |
| **`CTC`** | **Combat Table Coverage** *(Copertura Tabella Colpi)* | Somma di tutte le probabilità difensive: $\text{Dodge} + \text{Parry} + \text{Block} + \text{BossMiss}$. A $\ge \mathbf{102.4\%}$ il tank è **Unhittable**: nessun colpo bianco del boss può andare a segno come colpo normale (vengono tutti schivati, parati, bloccati o mancati). Include debuff non-stacking (*Insect Swarm* / *Scorpid Sting* +3%). |
| **`Block`** | **Block Chance** *(Probabilità di Blocco)* | Percentuale di parare un colpo con lo scudo. Durante l'abilità attiva *Shield Block* (+100%), il valore sale al 100%, portando istantaneamente il CTC oltre il 102.4%. |
| **`SBV`** | **Shield Block Value** *(Valore di Blocco con Scudo)* | Quantità netta di danno fisico assorbito da ciascun blocco riuscito. In WotLK 3.3.5a è anche il moltiplicatore primario che scala il danno e la minaccia generata da **Shield Slam** (Colpo di Scudo). |
| **`Hit`** | **Melee Hit Rating** *(Precisione Attacchi Fisici)* | Probabilità di colpire con colpi speciali e *Taunt*. Il cap contro boss Lv.83 è **8.0%** (263 rating), ridotto a 7.0% (230 rating) se nel gruppo è presente un Draenei (*Heroic Presence* +1%). |
| **`Exp`** | **Expertise** *(Perizia / Competenza)* | Riduce la probabilità che il boss schivi o pari gli attacchi del guerriero. **Soft Cap 26** (214 rating, elimina le Schivate del boss dal fronte). **Hard Cap 56** (elimina le Parate, azzerando il rischio di *Parry-Haste* su Sindragosa, Halion, Lady Deathwhisper). |
| **`Avoid`** | **Avoidance Pura** *(Evitamento Assoluto)* | Somma di $\text{Dodge} + \text{Parry} + \text{Miss}$: rappresenta la percentuale di colpi in cui il tank subisce **zero danni** (a differenza del blocco in cui il danno viene parzialmente mitigato). |
| **`DR%`** | **Damage Reduction %** *(Riduzione Danno)* | Percentuale di riduzione passiva del danno fisico calcolata in base all'armatura effettiva. |
| **`EHP`** | **Effective Health Pool** *(Salute Effettiva)* | Quantità di danno fisico grezzo che il tank può assorbire prima di morire: $\text{EHP} = \frac{\text{Salute Massima}}{1 - (\text{DR}\% / 100)}$. |
| **`GCD`** | **Global Cooldown** *(Tempo di Recupero Globale)* | Finestra standard di 1.5 secondi tra l'attivazione di un'abilità e la successiva. |
| **`ICD`** | **Internal Cooldown** *(Tempo di Ricarica Interno)* | Tempo di attesa obbligatorio (es. 45s o 50s) prima che l'effetto proc di un monile possa riattivarsi. |

### 7. Sunder Armor Tracker (`19 - Sunder Armor Tracker warTank`)
Posizionato sul lato destro delle barre ($x = 160, y = -7$, $32 \times 32\text{px}$):
- ID univoco `19 - Sunder Armor Tracker warTank` per prevenire collisioni di denominazione WeakAuras e suffissi automatici duplicati ` 2` in caso di coesistenza con la suite Fury Warrior o altre classi.
- Supporto completo ai debuff di riduzione armatura maggiori multi-classe e multi-spec: traccia *Sunder Armor* (tutti i rank 1-6 del Guerriero), *Expose Armor* del Ladro (`EA` in ciano) e *Acid Spit* del verme del Cacciatore.
- Conteggio cariche: `x5` in verde a 5 cariche, `x1`–`x4` in bianco, e cambio icona dinamico verso Expose Armor quando attivo.
- Timer di scadenza numerico alla base (%c1) e cariche centrate in alto (%c2).
- Allerta rossa visibile `OFF` alla base quando il debuff di armatura manca sul bersaglio ostile in combattimento.

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
