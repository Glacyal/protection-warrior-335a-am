# Design System & UI Specifications — Class Warrior (Protection) HUD

## 1. Principi di Design per Tank

L'interfaccia utente è fondata su tre principi chiave per la gestione sicura del tanking in WotLK 3.3.5a:
1. **Chiarezza Decisionale Immediata**: Il tank deve prendere decisioni critiche in frazioni di secondo (un Soul Reaper su Lich King o un Impale su Gormok richiede un cooldown difensivo o un taunt swap istantaneo). I segnali di allarme utilizzano contrasti cromatici netti (Rosso Letale, Oro Block, Ciano Interruzione).
2. **Zero Clutter (Disordine Zero)**: Niente elementi superflui a schermo. I buff con durata residua confortevole (> 30s) o coperti da altri membri del raid rimangono invisibili o attenuati. Solo le emergenze difensive e le finestre d'azione attiva saltano all'occhio.
3. **Gerarchia Visiva Concentrica a Barre Sincronizzate**: Al centro esatto si trovano le risorse vitali e i tempi d'azione (Castbar target con Kick Advisor a +8px, Swing Timer a -7px, Rage Bar a -20px, tutte a larghezza **278 px**). Subito sopra la riga dei Procs attivi (y = +52px) e l'allerta testuale (y = +78px). Ai lati esterni il pannello statistico difensivo (x = -190px) e il monitoraggio Sunder Armor (x = +160px).

---

## 2. Palette Colori

| Nome Token | Hex / RGBA | Ruolo / Utilizzo |
| :--- | :--- | :--- |
| **Shield Azure** | `#0088FF` / `[0.0, 0.53, 1.0, 1.0]` | Colore primario del guerriero protezione e Shield Slam |
| **Rage Crimson** | `#C71E1E` / `[0.78, 0.12, 0.12, 1.0]` | Barra della Rabbia base (0 - 44 Rage) |
| **Heroic Amber** | `#FFA500` / `[1.0, 0.65, 0.10, 1.0]` | Barra della Rabbia a soglia scarico sicuro (>= 45 Rage) e glow HS |
| **Emergency Red**| `#FF1100` / `[1.0, 0.07, 0.0, 1.0]` | Allerta vita bassa (< 35% HP) e Tank Buster letali |
| **Shield Wall Green**| `#00FF00` / `[0.0, 1.0, 0.0, 1.0]` | Cooldown maggiore attivo (-60% danno subito) o difesa al cap |
| **Boss Enrage Magenta**| `#FF0088` / `[1.0, 0.0, 0.53, 1.0]` | Allerta Enrage / Frenzy del boss |
| **Kick Cyan** | `#00E5FF` / `[0.0, 0.9, 1.0, 1.0]` | Lancio nemico interrompibile e advisor Shield Bash / Pummel |
| **Immune Grey** | `#888888` / `[0.53, 0.53, 0.53, 1.0]` | Lancio nemico non interrompibile (`notInterruptible == true`) |
| **Stance Bronze**| `#8B3A0F` / `[0.55, 0.23, 0.06, 1.0]` | Bordo e indicatore Postura Difensiva |
| **Dark HUD Base** | `#0C0E14` / `[0.05, 0.06, 0.08, 0.85]`| Sfondo opaco delle barre e del pannello statistiche |

---

## 3. Tipografia e Texture

- **Font di Riferimento**: `Expressway` (standard esportato per garantire massima leggibilità anche in situazioni di movimento frenetico della telecamera).
- **Font Secondario**: `Friz Quadrata TT` o `Arial Narrow`.
- **Texture Barre di Stato**: `Interface\\TargetingFrame\\UI-StatusBar` (sfumatura Blizzard pulita con bordi netti) e `Interface\\Buttons\\WHITE8X8` per cornici e fondali.
- **Icone**: Icone native Blizzard con bordi zoomati (zoom: 0.05) per eliminare il bordo grigio predefinito e massimizzare l'area visiva utile.

---

## 4. Componenti UI Dettagliati

### 4.1 Barra della Rabbia (`14 - Rage Bar`)
- **Dimensioni**: 278 x 14 px
- **Posizione**: X = 0, Y = -20 px
- **Testo**: `%p` (valore corrente) centrato.
- **Comportamento Cromatico**:
  - `0 - 44 Rage`: Rosso scuro/sangue (Rabbia riservata a Shield Slam, Revenge, Shockwave e Shield Block).
  - `>= 45 Rage`: Transizione istantanea ad ambra dorato (Rabbia in eccedenza: via libera per accodare Heroic Strike o Cleave senza rischiare di prosciugare la risorsa per le abilità di mitigazione e minaccia primaria).

### 4.2 Barra Rotazionale Swing Timer (`15 - Rotational Bar`)
- **Dimensioni**: 278 x 7 px
- **Posizione**: X = 0, Y = -7 px
- **Funzione**: Timer del colpo bianco dell'arma primaria (Main Hand).
- **Pixel Glow**: Bordo dorato pulsante attivo durante l'accodamento di Heroic Strike o Cleave, confermando visivamente al tank che il prossimo swing consumerà rabbia per generare minaccia extra.

### 4.3 Castbar con Kick Advisor Integrato (`16 - Castbar warTank`)
- **Dimensioni**: 278 x 20 px
- **Posizione**: X = 0, Y = +8 px
- **Funzionalità Unica**:
  - Mostra il tempo di lancio o canalizzazione del target corrente.
  - **Interrompibile**: Colore Ciano (`#00E5FF`). Mostra l'etichetta dell'abilità raccomandata in base alla postura e allo scudo:
    - In Defensive o Battle Stance con Scudo: `[KICK: Shield Bash]`
    - In Berserker Stance: `[KICK: Pummel]`
    - Se l'interruzione standard è in cooldown: `[STUN: Concussion Blow / Shockwave]`
  - **Non Interrompibile**: Colore Grigio scuro con testo rosso `[IMMUNE]`, evitando al tank di sprecare il cooldown di Shield Bash o Pummel su spell non kiccabili.

### 4.4 Pannello Statistiche Difensive (`18 - Stats Panel warTank`)
- **Dimensioni**: 88 x 60 px
- **Posizione**: X = -190 px, Y = -45 px
- **Stile Tipografico**: Allineato al 100% con `fury-warrior-335a-am` (`|cFFFFFFFFLabel:|r <ValoreColorato>`).
- **Layout a 5 Righe (Throttle a 10 Hz)**:
  1. `|cFFFFFFFFDef:|r |cFF22C55E540 (CAP)|r` (o `|cFFFFD700535 (HC)|r` / `|cFFFF2020%d/540|r`)
  2. `|cFFFFFFFFArmor:|r |cFFFFFFFF32.4k|r |cFF80D0FF(66.1%)|r` (Physical DR% contro boss Lv.83, Cap 75%)
  3. `|cFFFFFFFFCTC:|r |cFF00FFFF102.4% (MAX)|r` (o `|cFFFFD700%.1f%%|r`, Avoidance totale con non-stacking debuffs)
  4. `|cFFFFFFFFBlock:|r |cFF80D0FF38.2%|r |cFFFFD700(2450 SBV)|r` (Percentuale di blocco e Shield Block Value)
  5. `|cFFFFFFFFHit:|r |cFF22C55E8.0%|r | |cFF22C55E26 Exp|r` (Melee Hit con Draenei +1% e Soft Cap 26 / Hard Cap 56)

#### Legenda & Significato delle Sigle del Pannello
- **`Def` (Defense Skill)**: Abilità di difesa del personaggio (`base + rating`). A livello 80 il cap di immunità dai colpi critici dei boss Lv.83 è **540** (riduce del 5.6% il crit subito). In dungeon eroici il cap è **535**.
- **`Armor` (Armatura)**: Armatura effettiva del player; tra parentesi la percentuale di riduzione danno fisico contro boss Lv.83 ($\text{DR}\% = \frac{\text{Armor}}{\text{Armor} + 16635} \times 100$). Hard cap a 49.905 armatura (75% DR).
- **`CTC` (Combat Table Coverage)**: Copertura totale della tabella colpi: $\text{Dodge} + \text{Parry} + \text{Block} + \text{BossMiss}$. A $\ge 102.4\%$ il tank è *Unhittable* (tutti i colpi bianchi vengono mitigati o evitati). Include debuff non-stacking (*Insect Swarm* o *Scorpid Sting* max +3%).
- **`Block`**: Percentuale di parare un colpo con lo scudo (durante *Shield Block* sale al 100%).
- **`SBV` (Shield Block Value)**: Quantità netta di danno fisico assorbito da ciascun blocco; scala anche il danno e la minaccia di *Shield Slam*.
- **`Hit`**: Melee Hit Rating; cap speciale all'**8.0%** (263 rating), ridotto al 7.0% con *Heroic Presence* Draenei.
- **`Exp` (Expertise)**: Competenza/Perizia; **Soft Cap 26** (elimina le schivate del boss dal fronte), **Hard Cap 56** (elimina le parate e scongiura il *Parry-Haste*).

### 4.5 Riga Utility Adattiva (`05 - 13`)
- **Dimensioni**: Icone standardizzate 28 x 28 px a Y = -45 px.
- **Composizione**:
  - `05 - Trinket 1` e `06 - Trinket 2`: Auto-rilevamento slot 13 e 14.
  - `06b - Ring`: Ashen Band of Endless Courage (proc armor/def).
  - `07 - Cloak`: Incanto Ingegneria / paracadute o proc ricamo.
  - `08 - Tier Set`: Bonus Tier 10 Prot (Shield Block).
  - `09 - Enchants`: Blade Ward, Blood Draining, Mongoose.
  - `10 - Gloves`: Razzo o armatura Ingegneria.
  - `11 - Shield Wall`: Cooldown difensivo maggiore (-60% danno, con timer e testo verde `-60%`).
  - `12 - Last Stand`: Cooldown vitale (+30% salute massima, con timer e testo verde `+30%`).
  - `13 - Boots`: Turbo Ingegneria o Enraged Regeneration.

### 4.6 Allerte Centrali & Rilevamento Postura Errata (`17 - Alerts warTank` & `04 - Defensive Stance`)
- **Gruppo Allerte Centrali (`17 - Alerts warTank`)**:
  - Posizione: X = 0, Y = +78 px (ancorato al centro HUD sopra la Castbar).
  - Componenti:
    - `Alert - Sword and Board`: `|cFFFFFF00SHIELD SLAM READY!|r` (20pt, suono *Drums*).
    - `Alert - Emergency CD`: `|cFFFF1010CRIT HP (%.0f%%): USE %s!|r` (18pt, prioritizzazione Shield Wall / Last Stand).
    - `Alert - Kick Now`: `|cFF00FFFFINTERRUPT: %s!|r` (16pt, Ciano).
    - `Alert - Boss Enraged`: `|cFFFF0000BOSS ENRAGED! POP CD!|r` (18pt, Rosso vivo).
    - `Alert - Wrong Stance`: `|cFFFF1010>> DEFENSIVE STANCE REQUIRED! <<|r` (20pt, Rosso vivido lampeggiante con allarme audio *RaidWarning.ogg* a $y = 64$ px, attivo solo se `UnitAffectingCombat("player") and GetShapeshiftForm() ~= 2`).
- **Indicatore Icona Postura Difensiva (`04 - Defensive Stance`)**:
  - Posizione: X = -158 px, Y = 0 px.
  - `Defensive Stance - Active`: Icona standard con label `DEF` in verde quando in Stance 2.
  - `Defensive Stance - Warning`: Icona con Pixel Glow rosso vivo (spessore 2px, 8 linee) e label `|cFFFF2020STANCE|r` in combattimento fuori da Stance 2.
