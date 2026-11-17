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

### 4.0 Gruppo Dinamico Proc & Debuff (`01 - Procs warTank`)
- **Dimensioni & Layout**: Icone $34 \times 34\text{ px}$, posizionate a $Y = +52\text{ px}$ sopra la Castbar, crescita orizzontale centrata con spaziatura di $6\text{ px}$.
- **Parità Visiva Rigorosa tra Sword and Board e Revenge Ready**:
  - Entrambe le icone adottano la medesima struttura visiva:
    - `width: 34`, `height: 34`, `auto: False` con texture fisse Blizzard.
    - `cooldown: True`, `cooldownSwipe: True`, `cooldownEdge: False` (nessun bordo o lancetta gialla orologio).
    - Subregions a 3 livelli simmetriche:
      1. Sotto-sfondo semitrasparente: `{"type": "subbackground"}` per contrasto visivo elevato.
      2. Timer decimale `%p`: ancorato a `INNER_BOTTOM` (`font_size=11`, `y_offset=1`), formattazione `%.1f` (es. `4.8`, `3.2`).
      3. Etichetta abilità centrata in alto: `SLAM` (per Sword and Board) e `REV` (per Revenge Ready) ancorate a `INNER_TOP` (`font_size=9`, `y_offset=-2`).
    - Effetto Glow: Identico Gold Pixel Glow LibCustomGlow-1.0 `[1.0, 0.84, 0.0, 1.0]` (8 linee, frequenza 0.25, lunghezza 10, spessore 2) su `actions.start`, nascosto su `actions.finish`.
- **Comportamento Multi-Proc Dinamico**:
  - Se un'abilità procca più volte consecutive senza essere utilizzata, la durata non si interrompe né scade prematuramente: il timer e l'animazione di swipe si reimpostano istantaneamente a $5.0\text{ s}$ pieni (ad ogni schivata/parata/blocco per Revenge e ad ogni proc da Devastate/Revenge per Sword and Board).
- **Consumo Istantaneo a 0 Latenza**:
  - Al momento esatto del lancio (`SPELL_CAST_SUCCESS`) di *Shield Slam* o *Revenge*, la rispettiva icona scompare immediatamente dallo schermo, evitando visualizzazioni fantasma.
- **Debuff su Bersaglio (Demoralizing Shout, Thunder Clap, Rend)**:
  - **Filtro Vita Bersaglio**: Compaiono esclusivamente se `UnitHealthMax("target") >= 500.000` HP (boss ed élite maggiori). Su trash mob e bersagli secondari rimangono completamente invisibili.
  - **Zero-Clutter**: Etichette interne `DEMO`, `CLAP` e `REND` rimosse; all'interno dell'icona compare solo il timer decimale `%c` in fase `EXPIRING` o `MISS` in caso di debuff assente.

### 4.1 Barra della Rabbia (`14 - Rage Bar warTank`)
- **Dimensioni**: 278 x 14 px
- **Posizione**: X = 0, Y = -20 px
- **Testo**: `%p` (valore corrente) centrato.
- **Comportamento Cromatico**:
  - `0 - 44 Rage`: Rosso scuro/sangue (Rabbia riservata a Shield Slam, Revenge, Shockwave e Shield Block).
  - `>= 45 Rage`: Transizione istantanea ad ambra dorato (Rabbia in eccedenza: via libera per accodare Heroic Strike o Cleave senza rischiare di prosciugare la risorsa per le abilità di mitigazione e minaccia primaria).

### 4.2 Barra Rotazionale Swing Timer & Indicatore di Accodamento (`15 - Rotational Bar warTank`)
- **Dimensioni**: 278 x 7 px (cornice esterna), 274 x 5 px (area utile barra)
- **Posizione**: X = 0, Y = -7 px
- **Swing Timer Mano Primaria ad Animazione Progressiva**:
  - `Base Bar` ($274 \times 5\text{ px}$, `regionType: "aurabar"`): Barra progressiva fluida a piena larghezza che mostra in tempo reale lo scorrimento del tempo tra un attacco in mischia e il successivo (Swing Timer). Calibrata sulla velocità effettiva dell'arma principale (`UnitAttackSpeed("player")`).
  - **Timer Decimale Centrato**: Mostra il tempo residuo in secondi (`%c`, es. `1.8s`) centrato sulla barra.
  - **Colore Base**: Rame/bronzo Warrior (`[0.65, 0.35, 0.12, 0.90]`).
- **Sistema di Accodamento Dinamico Sincronizzato per il War Tank**:
  - **Heroic Strike accodato (`47450`)**: Barra aurabar sincronizzata in Oro brillante (`[1.0, 0.84, 0.0, 1.0]`) che prosegue lo scorrimento progressivo dello swing timer, corredata da Gold Pixel Glow `LibCustomGlow-1.0` (`PWHUD_HS_GLOW`).
  - **Cleave accodato (`47520`)**: Barra aurabar sincronizzata in Verde Smeraldo (`[0.1, 0.95, 0.2, 1.0]`) che prosegue lo scorrimento progressivo dello swing timer, corredata da Emerald Green Pixel Glow `LibCustomGlow-1.0` (`PWHUD_CLEAVE_GLOW`).
  - Al reset del colpo (lancio di HS/Cleave o auto-attacco normale tramite `SWING_DAMAGE`/`SWING_MISSED`), lo swing timer riparte istantaneamente dallo 0% e l'effetto di accodamento svanisce.

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
- **Stile Tipografico**: Visualizzazione ad alta leggibilità con etichette bianche (`|cFFFFFFFFLabel:|r <ValoreColorato>`) e valori colorati dinamicamente in base alle soglie di cap difensive del War Tank.
- **Layout a 5 Righe (Throttle a 10 Hz)**:
  1. `|cFFFFFFFFDef:|r |cFF22C55E540 (CAP)|r` (o `|cFFFFD700535 (HC)|r` / `|cFFFF2020%d/540|r`)
  2. `|cFFFFFFFFArmor:|r |cFFFFFFFF32.4k|r |cFF80D0FF(66.1%)|r` (Physical DR% contro boss Lv.83, Cap 75%)
  3. `|cFFFFFFFFCTC:|r |cFF00FFFF102.4% (MAX)|r` (o `|cFFFFD700%.1f%%|r`, Avoidance totale con non-stacking debuffs)
  4. `|cFFFFFFFFBlock:|r |cFF80D0FF38.2%|r |cFFFFD700(2450 SBV)|r` (Percentuale di blocco e Shield Block Value)
  5. `|cFFFFFFFFHit:|r |cFF22C55E8.0%|r | |cFF22C55E26 Exp|r` (Melee Hit con Draenei +1% e Soft Cap 26 / Hard Cap 56)

#### Legenda & Significato delle Sigle del Pannello
- **`Def` (Defense Skill)**: Abilità di difesa del personaggio (`base + rating`). A livello 80 il cap di immunità dai colpi critici dei boss Lv.83 è **540** (riduce del 5.6% il crit subito). In dungeon eroici il cap è **535**.
- **`Armor` (Armatura & DR% Contestuale)**: Armatura effettiva del player; tra parentesi la percentuale di riduzione danno fisico contestuale: calcolata con costante Blizzard $K = 15232.5$ a Lv.80 (es. 25.253 armatura $\implies \mathbf{62.4\%}$, identico al $62.38\%$ visualizzato nel tooltip in-game della scheda personaggio) e con $K = 16635$ contro Raid Boss Lv.83 / Skull ($\implies \mathbf{60.3\%}$, mitigazione effettiva sul boss). Hard cap al 75.0% DR.
- **`CTC` (Combat Table Coverage)**: Copertura totale della tabella colpi: $\text{Dodge} + \text{Parry} + \text{Block} + \text{BossMiss}$. A $\ge 102.4\%$ il tank è *Unhittable* (tutti i colpi bianchi vengono mitigati o evitati). Include debuff non-stacking (*Insect Swarm* o *Scorpid Sting* max +3%).
- **`Block`**: Percentuale di parare un colpo con lo scudo (durante *Shield Block* sale al 100%).
- **`SBV` (Shield Block Value)**: Quantità netta di danno fisico assorbito da ciascun blocco; scala anche il danno e la minaccia di *Shield Slam*.
- **`Hit`**: Melee Hit Rating; cap speciale all'**8.0%** (263 rating), ridotto al 7.0% con *Heroic Presence* Draenei.
- **`Exp` (Expertise)**: Competenza/Perizia; **Soft Cap 26** (elimina le schivate del boss dal fronte), **Hard Cap 56** (elimina le parate e scongiura il *Parry-Haste*).

### 4.5 Riga Utility Adattiva (`05 - 13`) — Auto-Centratura Dinamica per il War Tank
- **Principio Architetturale**:
  La riga inferiore (`05` - `13`, posizionata a $y = -45\text{ px}$ sotto la barra della rabbia da $278\text{ px}$) adotta un'architettura a **centratura dinamica naturale** appositamente studiata per il War Tank: gli slot non equipaggiati o non qualificati vengono completamente soppressi, e le icone attive vengono ricentrate orizzontalmente attorno a $x = 0$ senza buchi, spazi vuoti o slittamenti asimmetrici a destra.
- **Formula di Calcolo delle Coordinate Orizzontali**:
  $$\text{targetX} = \left\lfloor \left( i - \frac{N + 1}{2} \right) \times \text{step} + 0.5 \right\rfloor$$
  dove $i$ è l'indice dell'elemento qualificato all'interno della lista `activeOrder`, ed $N = \#\text{activeOrder}$ è il numero totale di icone attualmente attive (variabile dinamicamente tra $3$ e $11$).
- **Tabella di Scaling Dinamico di Passo e Dimensione**:
  | Numero Icone Attive ($N$) | Passo Orizzontale (`step`) | Dimensione Icona (`targetW`) | Larghezza Totale Riga |
  | :--- | :--- | :--- | :--- |
  | **$N \ge 11$** | $25\text{ px}$ | $24 \times 24\text{ px}$ | $\approx 250\text{ px}$ (sotto i $278\text{ px}$ della Rage Bar) |
  | **$N = 10$** | $27\text{ px}$ | $26 \times 26\text{ px}$ | $\approx 243\text{ px}$ |
  | **$N = 9$** | $29\text{ px}$ | $28 \times 28\text{ px}$ | $\approx 232\text{ px}$ |
  | **$N = 8$** | $32\text{ px}$ | $28 \times 28\text{ px}$ | $\approx 224\text{ px}$ |
  | **$N = 7$** | $38\text{ px}$ | $28 \times 28\text{ px}$ | $\approx 228\text{ px}$ |
  | **$N = 6$** | $44\text{ px}$ | $28 \times 28\text{ px}$ | $\approx 220\text{ px}$ |
  | **$N = 5$** | $48\text{ px}$ | $28 \times 28\text{ px}$ | $\approx 192\text{ px}$ |
  | **$N \le 4$** | $52\text{ px}$ | $28 \times 28\text{ px}$ | $\le 156\text{ px}$ |

- **Specifiche Tassative di Filtraggio degli Oggetti (Whitelist Rigorosa)**:
  1. **Trinket 1 & 2 (`05 - Trinket 1 warTank` & `06 - Trinket 2 warTank`)**:
     - *Slot 13 e 14*. Sempre visibili quando equipaggiati. Tracciano durata attiva, tempo di recupero on-use ed Internal Cooldown (ICD) da 45s a 120s (database completo ICC/RS/ToC/Ulduar/Naxxramas).
  2. **Anello (`06b - Ring warTank`)**:
     - *Slot 11/12*. **SOLO ed esclusivamente** se equipaggiato con:
       - *Ashen Band of Endless Courage* (anello tank reputazione Ashen Verdict con proc +Armor / Defensivo, Spell ID `72414`/`72412`).
       - *Ashen Band of Endless Vengeance* (anello melee DPS con proc +480 AP, 60s ICD).
     - *Soppressione Totale*: qualsiasi anello a sole statistiche passive statiche viene ignorato ed escluso da `activeOrder`.
  3. **Mantello (`07 - Cloak warTank`)**:
     - *Slot 15*. **SOLO ed esclusivamente** se provvisto di incanto da combattimento con proc attivo (Sartoria: *Swordguard Embroidery* / *Ricamo della Spada*, Spell ID `55775`, ID Incanto `3730`).
     - *Soppressione Tassativa*: il paracadute d'Ingegneria (*Flexweave Underlay*) e tutti gli incanti con statistiche statiche (+22 Agility, +16 Defense, +225 Armor) sono **rigorosamente soppressi e invisibili**.
  4. **Tier Set (`08 - Tier Set warTank`)**:
     - **SOLO ed esclusivamente** se il giocatore indossa almeno **4 Pezzi Tier 10** (*Ymirjar Lord's Battlegear* 4P: bonus *Shield Block* che riduce il danno magico subito del 20% per 10s, Spell ID `70844`).
     - *Soppressione Totale*: con 0, 1, 2 o 3 pezzi T10 l'icona è completamente nascosta e rimossa da `activeOrder`.
  5. **Incanti Arma (`09 - Enchants warTank`)**:
     - *Slot 16*. **SOLO ed esclusivamente** se l'arma principale monta un incanto proccabile difensivo o offensivo (*Blade Ward* per parry proc, *Blood Draining* con 5 stack e cura automatica d'emergenza <35% HP, *Mongoose*, *Berserking*).
     - *Soppressione Totale*: incanti statici (+30 Stamina Titanguard, +20 Strength Potency, ecc.) sono ignorati.
  6. **Guanti (`10 - Gloves warTank`)**:
     - *Slot 10*. **SOLO ed esclusivamente** se provvisti di tinker attivo d'Ingegneria (*Reticulated Armor Webbing* per +885 Armor attiva o *Hyperspeed Accelerators*).
  7. **Cooldown Difensivi Guerriero (`10b - Shield Block`, `11 - Shield Wall`, `12 - Last Stand`)**:
     - Fissi ed integrati armonicamente all'interno di `activeOrder` prima degli stivali:
       - `10b - Shield Block warTank`: durata attiva 10s con bonus block rating/value e CD di 30s/60s.
       - `11 - Shield Wall warTank`: cooldown maggiore di riduzione del danno subito (-60%), con durata attiva di 12s, ricarica e glow di emergenza a <35% HP.
       - `12 - Last Stand warTank`: cooldown vitale di sopravvivenza (+30% salute massima per 20s), con ricarica e glow di emergenza a <35% HP.
  8. **Stivali (`13 - Boots warTank`)**:
     - *Slot 8*. **SOLO** se provvisti di tinker attivo d'Ingegneria (*Nitro Boosts* / Acceleratori a Nitro) oppure fallback di utilità su *Enraged Regeneration*.

### 4.6 Allerte Centrali & Rilevamento Postura Errata (`17 - Alerts warTank` & `04 - Defensive Stance`)
- **Filosofia Zero-Clutter Centrale**:
  Coerentemente con la filosofia Zero-Clutter del War Tank per massimizzare la visibilità delle meccaniche dei boss in raid, al centro dello schermo non compare alcun banner testuale per abilità ordinarie o proc rotazionali.
  - **Banner Testuali Eliminati**: `Alert - Sword and Board`, `Alert - Boss Enraged` e `Alert - Wrong Stance` sono stati **definitivamente rimossi** dal gruppo `17 - Alerts warTank`.
  - **Proc Rotazionali in Gruppo Dedicato (`01 - Procs warTank`)**: *Sword and Board*, *Revenge Ready*, *Shield Slam* e i debuff su target vivono esclusivamente come icone compatte con timer e bordi dedicati sopra la barra di cast.
- **Allarmi Critici di Sopravvivenza Residui (`17 - Alerts warTank`)**:
  - Posizione: X = 0, Y = +78 px (centro visivo, sopra la Castbar).
  - Componenti:
    - `Alert - Emergency CD`: `|cFFFF1010CRIT HP (%.0f%%): USE %s!|r` (18pt, prioritizzazione salvavita Shield Wall / Last Stand / Shield Block / Pot quando il tank è sotto il 35% HP).
    - `Alert - Kick Now`: `|cFF00FFFFINTERRUPT: %s!|r` (16pt, ciano brillante quando il target ostile sta canalizzando o lanciando un'abilità interrompibile).
- **Indicatore Compatto Postura Difensiva Errata (`04 - Defensive Stance warTank`)**:
  - Posizione: X = -158 px, Y = 0 px (icona 28x28px, allineata alle shout e al pannello statistiche).
  - In postura corretta (*Defensive Stance*, Stance 2): **completamente invisibile** (zero distrazioni in combattimento).
  - Fuori postura difensiva in combattimento: si attiva istantaneamente con icona `04 - Defensive Stance - OutOfStance warTank`, pixel glow rosso perentorio e label visiva `STANCE`. Event-driven su `PLAYER_REGEN_DISABLED`, `PLAYER_REGEN_ENABLED` e `UPDATE_SHAPESHIFT_FORM`.

### 4.7 Tracker Debuff Armatura (`19 - Sunder Armor Tracker warTank`)
- **Dimensioni**: 32 x 32 px
- **Posizione**: X = +160 px, Y = -7 px (lato destro centrale)
- **Denominazione Univoca Anti-Conflitto**: Identificatore `19 - Sunder Armor Tracker warTank` con suffisso protetto `warTank` per scongiurare collisioni e rinomine automatiche a suffisso ` 2` nell'import WeakAuras accanto ad altre configurazioni presenti nell'addon.
- **Rilevamento Intelligente Sovrapposizioni (All-Specs & Cross-Class)**:
  - *Sunder Armor* (Guerriero all-specs, rank 1-6): contatore cariche `x1`–`x4` in bianco, `x5` in verde smeraldo, e timer di scadenza alla base.
  - *Expose Armor* (Ladro): etichetta `EA` in ciano con icona dinamica di Expose Armor, riconoscendo la sovrapposizione al 100% (-20% armor).
  - *Acid Spit* (Hunter Worm): rilevamento automatico del debuff esotico del verme (-20% armor).
  - **Mancanza Debuff in Combattimento**: testo visibile `OFF` in rosso vivo alla base dell'icona.
