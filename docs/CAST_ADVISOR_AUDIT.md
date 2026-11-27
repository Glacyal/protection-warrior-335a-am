# Audit Completo WotLK 3.3.5a (Classic, TBC, WotLK) — Interrompibilità vs Riflettibilità per il War Tank

**Stato**: Task 43 — Censimento Completo Classic + TBC + WotLK 3.3.5a Completato (Pre-requisito per Task 44)  
**Target Client**: World of Warcraft: Wrath of the Lich King (3.3.5a, Build 12340)  
**Specializzazione**: Guerriero Protezione (War Tank)  
**Componenti Coinvolti**: [`bars.py`](file:///d:/0Progetti/protection-warrior-335a-am/builder/components/bars.py) (`16 - Castbar warTank`) e [`alerts.py`](file:///d:/0Progetti/protection-warrior-335a-am/builder/components/alerts.py) (`17 - Alerts warTank`)

---

## 1. Perché l'attuale Advisor Sbaglia (Gap Analysis)

Nell'attuale implementazione (`_G.PWHUD_GetTargetCastInfo()`), i cast nemici vengono valutati in modo quasi binario, generando continui falsi positivi:
1. **`notInterruptible == true` + `targettarget == player` $\to$ consiglia sempre `SPELL REFLECTION`**:
   - Falso su quasi tutti i Raid Boss (*Soul Reaper*, *Frost Breath*, *Defile*, *Whirlwind*, *Flame Breath*, *Pungent Blight*), su attacchi fisici con barra cast (*Dark Smash*, *Boulder Toss*), su AoE non targettate e su *Aura Mastery* + cura.
2. **`notInterruptible == false` + `targettarget == player` $\to$ consiglia `SHIELD BASH / REFLECT` (o fallback `REFLECT`)**:
   - Falso su **Cure/Buff** (*Greater Heal*, *Dark Mending*, *Holy Light*), **Evocazioni** (*Summon*), **AoE a terra** (*Blizzard*, *Flamestrike*, *Rain of Fire*, *Volley*), **Cast Fisici** (*Steady Shot*, *Shattering Throw*, *Slam*, *Shoot*), ***Mana Burn***, **Canali già in esecuzione** (*Mind Flay*, *Drain Life*) e cast specifici di Raid Boss immuni a reflect (*Kel'Thuzad Frostbolt*, *Lady Deathwhisper Frostbolt*).
3. **Mancano**: filtro `isTradeSkill`, controllo `spellSchool` (fisico `0x1` vs magico `>1`), rilevamento immunità PvP/PvE via `UnitBuff` e differenziazione tra **PG**, **Mob** e **Boss (`worldboss` / `-1`)**.

---

## 2. Classificazione Ufficiale a 4 Stati Operativi

Ogni lancio o canalizzazione rilevata su un bersaglio ostile in WotLK 3.3.5a appartiene esattamente a uno di **4 gruppi operativi**:

| Stato | Colore UI | Azione War Tank | Esempi Tipici |
| :--- | :--- | :--- | :--- |
| **`BOTH`** | Ciano (`SHIELD BASH`) / Magenta (`SPELL REFLECTION`) se fuori melee o SB in CD | **Interrompibile E Riflettibile** | Magie offensive/CC single-target lanciate sul tank (*Polymorph*, *Fear*, *Shadow Bolt*, *Frostbolt* trash/PG, *Fel Fireball*, *Deathchill Bolt*). |
| **`KICK`** | Ciano brillante (`SHIELD BASH` / `PUMMEL` / `KICK (CD)`) | **SOLO Interrompibile** *(Mai Reflect!)* | Tutte le **Cure**, **Resurrezioni**, **Evocazioni**, **AoE a terra/cono**, ***Mana Burn***, **Cast Fisici** (*Steady Shot*, *Shoot*, *Slam*), **Canali già avviati**, *Kel'Thuzad Frostbolt*, *General Vezax Searing Flames*, *Deathwhisper Frostbolt*, *Moorabi Transformation*. |
| **`REFLECT`** | Magenta (`SPELL REFLECTION`) | **SOLO Riflettibile** *(Immune al Kick!)* | Magia offensiva/CC single-target diretta sul tank quando l'interrupt fisico è immune: es. PG sotto *Aura Mastery*, *Essence of Desire — Deaden* (BT), *Attumen — Intangible Presence* (Karazhan), rari mob élite con magia protetta da scudo grigio. |
| **`IMMUNE`** | Grigio neutro (`IMMUNE`) | **NESSUNA DELLE DUE** *(Né Kick né Reflect!)* | ~95% meccaniche Raid Boss (*Soul Reaper*, *Infest*, *Defile*, *Frost Breath*, *Bone Spike*, *Pungent Blight*, *Lightning Nova*, *Shadow Nova*, *Whirlwind*, *Dark Smash*), Cure sotto *Divine Shield*/*Aura Mastery*/*BoP*, `isTradeSkill`. |

---

## 3. Censimento Completo per Espansione: CLASSIC, TBC e WOTLK (3.3.5a)

### 3.1 ERA CLASSIC (Lv. 15–60 Dungeons & Lv. 60 Raids in 3.3.5a)

#### A. Dungeons Classic (*Deadmines, Wailing Caverns, SFK, Stockade, BFD, Gnomeregan, RFK/RFD, Scarlet Monastery, Uldaman, Zul'Farrak, Maraudon, Sunken Temple, BRD, LBRS/UBRS, Dire Maul, Scholomance, Stratholme*)
- **Mob Trash & Boss Caster Standard (`BOTH` / `KICK`)**:
  - *Single-Target Offensive Magic* (Shadowcasters in SFK/BFD/Stratholme/Scholomance, Pyromancers in BRD, Highborne in Dire Maul, *Archmage Arugal* *Void Bolt*, *Ras Frostwhisper* *Frostbolt*, *Darkmaster Gandling* *Arcane Missiles*, *Jammal'an* *Hex*): **`BOTH`** (interrompibile e riflettibile se targetta te).
  - *Cure / Buff / Evocazioni / AoE* (*Druid of the Fang Healing Touch*, *Scarlet Clerics / High Inquisitor Whitemane* *Heal/Flash Heal*, *BRD Anvilrage Medics*, *Crimson Priests*, *Stratholme Dark Mending*, *Flamestrike* / *Blizzard* / *Rain of Fire*): **`KICK` SOLO** (critico interromperle; mai riflettibili!).
  - *Ranged/Melee Fisici con Cast* (*Defias Riflemen*, *Scholomance/Stratholme Riflemen* *Shoot*, *Scarlet Myrmidon/Herod* *Whirlwind*): *Shoot* = **`KICK` (fisico, no Reflect)**; *Whirlwind* / *Cleave* non interrompibile = **`IMMUNE`**.
  - *UBRS Draghi* (*General Drakkisath* *Conflagration*/*Flame Breath*, *Gyth* breath, *Rend Blackhand*): **`IMMUNE`**.

#### B. Raids Classic (*Molten Core, Blackwing Lair, Zul'Gurub, AQ20, AQ40*)
| Istanza | Boss / Mob | Cast Noti | Puoi Kick? | Puoi Reflect? | Gruppo |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Molten Core** | *Flamewaker Priests* (add Sulfuron) | *Dark Mending*, *Shadow Word: Pain* | **SÌ** (su *Dark Mending*) | **NO** | **`KICK`** *(critico!)* |
| **Molten Core** | *Trash Casters* (*Firewalker*, *Lava Spawn*) | *Fireball* / *Pyroblast* | Sì | Sì *(se singolo su te)* | **`BOTH`** |
| **Molten Core** | *Lucifron, Magmadar, Gehennas, Geddon, Shazzrah, Ragnaros* | *Panic*, *Inferno*, *Living Bomb*, *Arcane Explosion*, *Wrath of Ragnaros*, *Magma Blast* | **NO** | **NO** *(AoE/script boss)* | **`IMMUNE`** |
| **Blackwing Lair** | *Razorgore, Vaelastrasz, Broodlord, Firemaw, Ebonroc, Flamegor, Chromaggus, Nefarian* | *Flame Breath*, *Shadow Flame*, *Wing Buffet*, *Blast Wave*, *Brood Affliction*, *Bellowing Roar* | **NO** | **NO** *(coni/AoE draconici)* | **`IMMUNE`** |
| **Blackwing Lair** | *Blackwing Spellbinder / Mage / Technicians* (Trash) | *Greater Heal*, *Flamestrike*, *Shadow Bolt* | **SÌ** | Solo *Shadow Bolt* | **`KICK`** / **`BOTH`** |
| **Zul'Gurub** | *High Priestess Jeklik*, *Zealot Lor'Khan (Thekal)* | ***Great Heal*** (*Grande Cura*) | **SÌ (Critico!)** | **NO** | **`KICK`** |
| **Zul'Gurub** | *High Priestess Mar'li* | *Drain Life*, *Poison Bolt Volley* | **SÌ** *(Drain)* | **NO** *(canale/AoE)* | **`KICK`** / **`IMMUNE`** |
| **Zul'Gurub** | *Hakkar*, *Jin'do*, *Arlokk*, *Venoxis* | *Blood Siphon*, *Cause Insanity*, *Holy Fire* (AoE/boss) | **NO** *(o limitato)* | **NO** | **`IMMUNE`** |
| **AQ20 & AQ40** | *The Prophet Skeram* (e Cloni) | *Arcane Explosion* (cast), *True Fulfillment* | **SÌ** *(Arcane Exp.)* | **NO** *(AoE)* | **`KICK`** / **`IMMUNE`** |
| **AQ20 & AQ40** | *Twin Emperors (Vek'lor)*, *Viscidus*, *C'Thun*, *Fankriss*, *Huhuran*, *Ouro* | *Eye Beam*, *Dark Glare*, *Poison Bolt Volley*, *Acid Spit*, *Blizzard* | **NO** | **NO** *(AoE/Boss)* | **`IMMUNE`** |
| **AQ40 Trash** | *Qiraji Mindslayers*, *Anubisath Defenders/Sentinels* | *Mind Flay*, *Mana Burn*, *Plague*, *Thunderclap*, *Shadow Storm* | **SÌ** *(Mind Flay/Mana Burn)* | **NO** *(channel/Mana Burn/AoE)* | **`KICK`** / **`IMMUNE`** |

---

### 3.2 ERA TBC — THE BURNING CRUSADE (Lv. 60–70 Dungeons & Lv. 70 Raids in 3.3.5a)

#### A. Dungeons TBC (*Hellfire Ramparts, Blood Furnace, Shattered Halls, Slave Pens, Underbog, Steamvault, Mana-Tombs, Auchenai Crypts, Sethekk Halls, Shadow Labyrinth, Old Hillsbrad, Black Morass, Mechanar, Botanica, Arcatraz, Magisters' Terrace*)
- **Eccezioni Riflettibili / Interrompibili Celebri in TBC 5-man**:
  - **The Black Morass**: *Rift Keepers / Rift Lords* $\to$ *Pyroblast*, *Frostbolt*, *Shadow Bolt* (**`BOTH` / `REFLECT`** — danno riflesso enorme).
  - **Magisters' Terrace**:
    - *Blood Elf Trash* (*Magistrix*, *Mage Guard*): *Polymorph*, *Fireball*, *Frostbolt* $\to$ **`BOTH`**.
    - *Priestess Delrissa + 4 Adds PvP*: Mago/Warlock casts $\to$ **`BOTH`**; Cure/Shield (*Flash Heal*, *Lesser Healing Wave*) $\to$ **`KICK`**; Hunter (*Steady Shot*) $\to$ **`KICK` (fisico, no Reflect)**.
    - *Kael'thas Sunstrider (5-man)*: *Fireball* $\to$ **`KICK` / `REFLECT`**; *Pyroblast* (quando scudo assente) $\to$ **`KICK`**; *Flame Strike* / *Gravity Lapse* $\to$ **`IMMUNE`**.
  - **The Steamvault**: *Warlord Kalithresh* attiva *Spell Reflection* proprio su di sé (**NON** attaccare con magie!); *Coilfang Sorceress* (*Heal*, *Frostbolt*) $\to$ **`KICK`** / **`BOTH`**.
  - **Sethekk Halls**: *Talon King Ikiss* (*Arcane Explosion* = **`IMMUNE`** AoE, *Polymorph* = **`BOTH`**); *Darkweavers* (*Shadow Bolt* / *Heal* = **`BOTH`** / **`KICK`**).
  - **Shadow Labyrinth**: *Shadow Council Cabalists / Malicious Instructors* (*Shadow Bolt*, *Rain of Fire*, *Heal*) $\to$ **`BOTH`** / **`KICK`**; *Murmur* (*Sonic Boom*, *Murmur's Touch*) $\to$ **`IMMUNE`**.
  - **Old Hillsbrad Foothills**: *Captain Skarloc* (*Holy Light* = **`KICK` Critico!**), *Epoch Hunter* (*Sand Breath* = **`IMMUNE`**).
  - **Shattered Halls / Blood Furnace / Arcatraz / Botanica / Mechanar / Mana-Tombs**: Tutti i caster trash hanno cure/AoE (**`KICK`**, mai Reflect) e bolt singoli (**`BOTH`**); i bruti fisici (*Kargath*, *O'mrogg*, *Porung*, *Dalliah* *Whirlwind*, *Broggok*) sono **`IMMUNE`**.

#### B. Raids TBC (*Karazhan, Gruul, Magtheridon, SSC, Tempest Keep, Mount Hyjal, Black Temple, Zul'Aman, Sunwell Plateau*)
| Istanza | Boss / Mob | Cast Noti | Puoi Kick? | Puoi Reflect? | Gruppo |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Karazhan** | *Attumen the Huntsman* | ***Intangible Presence*** (curse) | **NO** | **SÌ!** | **`REFLECT`** *(Whitelist!)* |
| **Karazhan** | *Moroes (4 Ospiti)* | *Greater Heal* (Catriona), *Holy Light* (Keira), *Mana Burn* (Dorothea) | **SÌ (Critico!)** | **NO** *(cure/Mana Burn)* | **`KICK`** |
| **Karazhan** | *Opera — Julianne* | *Eternal Affection* (Cura) | **SÌ (Critico!)** | **NO** | **`KICK`** |
| **Karazhan** | *Shade of Aran* | *Fireball*, *Frostbolt*, *Arcane Missiles* | **SÌ (Critico!)** | **NO** *(o limitato; Flame Wreath/Blizzard/AE = no)* | **`KICK`** *(Super AE / Blizzard = `IMMUNE`)* |
| **Karazhan** | *Curator, Maiden, Netherspite, Malchezaar* | *Evocation*, *Repentance*, *Nether Breath*, *Shadow Nova* | **NO** | **NO** | **`IMMUNE`** |
| **Gruul's Lair** | *Maulgar — Blindeye the Seer* | ***Prayer of Healing*** (dopo Shield) | **SÌ (Critico!)** | **NO** | **`KICK`** |
| **Gruul's Lair** | *Krosh Firehand*, *Gruul* | *Greater Fireball* (Krosh), *Ground Slam* / *Shatter* | **NO** | **NO** *(Krosh = Spellsteal Mage)* | **`IMMUNE`** |
| **Magtheridon** | *Hellfire Channelers* | ***Dark Mending*** (Cura) | **SÌ (Critico!)** | **NO** | **`KICK`** |
| **Magtheridon** | *Magtheridon* | *Blast Nova* (solo Cubi!), *Quake* | **NO** | **NO** | **`IMMUNE`** |
| **SSC** | *Fathom-Guard Caribdis* (Karathress), *Coilfang Priestess* | *Healing Wave* / *Heal* | **SÌ (Critico!)** | **NO** | **`KICK`** |
| **SSC** | *Hydross, Lurker, Leotheras, Morogrim, Lady Vashj* | *Spout*, *Whirlwind*, *Watery Grave*, *Static Charge* | **NO** | **NO** | **`IMMUNE`** |
| **Tempest Keep** | *Kael'thas Sunstrider* (Fase 4/5) | ***Fireball*** (critico!), *Pyroblast* (dopo rottura Shock Barrier) | **SÌ (Critico!)** | **NO** *(boss immune)* | **`KICK`** |
| **Tempest Keep** | *Al'ar, Void Reaver, Solarian, Advisors* | *Flame Quills*, *Pounding*, *Arcane Missiles* | **NO** *(o add stun)* | **NO** | **`IMMUNE`** |
| **Mount Hyjal** | *Ondate Trash* (*Necromancers, Banshees*) | *Shadow Bolt*, *Unholy Frenzy*, *Heal*, *Curse* | **SÌ** | Solo bolt singoli | **`BOTH` / `KICK`** |
| **Mount Hyjal** | *Winterchill, Anetheron, Kaz'rogal, Azgalor, Archimonde* | *Death & Decay*, *Carrion Swarm*, *Rain of Fire*, *Doom*, *Finger of Death* | **NO** | **NO** | **`IMMUNE`** |
| **Black Temple** | ***Reliquary of Souls P2 (Essence of Desire)*** | ***Deaden*** (*Intorpidimento*, +100% dmg taken!) | **NO** | **SÌ (OBBLIGATORIO!)** | **`REFLECT`** *(Whitelist!)* |
| **Black Temple** | ***Reliquary of Souls P2 (Essence of Desire)*** | ***Spirit Shock*** (stun sul tank) | **SÌ (OBBLIGATORIO!)** | **NO** | **`KICK`** |
| **Black Temple** | *Illidari Council (Lady Malande)* | ***Circle of Healing*** (o cura), *Divine Wrath* | **SÌ (Critico!)** | **NO** | **`KICK`** |
| **Black Temple** | *Naj'entus, Supremus, Gorefiend, Bloodboil, Shahraz, Illidan* | *Shear*, *Dark Barrage*, *Flame Crash*, *Fatal Attraction* | **NO** | **NO** | **`IMMUNE`** |
| **Zul'Aman** | *Amani'shi Medicine Man / Trash*, *Malacrass Adds* | *Chain Heal*, *Healing Ward*, *Fireball* | **SÌ (Critico!)** | Solo *Fireball* | **`KICK` / `BOTH`** |
| **Zul'Aman** | *Akil'zon, Nalorakk, Jan'alai, Halazzi, Zul'jin* | *Electrical Storm*, *Flame Breath*, *Shock* | **NO** | **NO** | **`IMMUNE`** |
| **Sunwell** | *Trash* (*Shadowsword Priests / Mages*), *Sathrovarr* | *Greater Heal*, *Renew*, *Fireball*, *Polymorph* | **SÌ** | Solo single nuke | **`KICK` / `BOTH`** |
| **Sunwell** | *Kalecgos, Brutallus, Felmyst, Twins, M'uru, Kil'jaeden* | *Gas Nova*, *Conflagration*, *Darkness of a Thousand Souls* | **NO** | **NO** | **`IMMUNE`** |

---

### 3.3 ERA WOTLK 3.3.5a (Tutti i 16 Dungeon Lv.70–80 & Tutti i 9 Raid Lv.80)

#### A. Tutti i 16 Dungeon WotLK 3.3.5a (Normal & Heroic 5-man)

| Dungeon | Boss & Trash Principali | Cast Noti | Kick (`Shield Bash`) | Reflect (`Spell Reflect`) | Gruppo Netto |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **1. Utgarde Keep** | *Dalronn the Controller* | *Shadow Bolt*, *Debilitate* | Sì | Sì *(se su te)* | **`BOTH` / `KICK`** |
| | *Ingvar the Plunderer* | *Dark Smash*, *Dreadful Roar*, *Staggering Roar* | **NO** | **NO** *(fisico/AoE)* | **`IMMUNE`** |
| **2. The Nexus** | *Grand Magus Telestra* (& Cloni) | *Fireball*, *Frostbolt* / *Arcane* | Sì *(Fuoco/Gelo)* | Sì *(singolo)* | **`BOTH` / `KICK`** |
| | *Keristrasza, Ormorok, Stoutbeard* | *Frost Breath*, *Crystal Spikes*, *Whirlwind* | **NO** | **NO** | **`IMMUNE`** |
| | *Mage Hunters* (Trash) | *Arcane Bolt*, *Polymorph*, *Cone of Cold* | Sì | Solo *Bolt/Poly* | **`BOTH` / `KICK`** |
| **3. Azjol-Nerub** | *Krik'thir Adds* (*Watcher*, *Shadowcaster*) | *Shadow Bolt*, *Mind Flay*, *Curse* | Sì | Solo *Bolt/Curse* | **`BOTH` / `KICK`** |
| | *Hadronox*, *Anub'arak* | *Acid Cloud*, *Pound*, *Impale* | **NO** | **NO** | **`IMMUNE`** |
| **4. Ahn'kahet** | *Ahn'kahar Spell Flinger* (Trash!) | ***Shadow Blast*** (~90% HP sul tank!) | **SÌ** | **SÌ (Mortale riflesso!)** | **`BOTH`** *(Critico!)* |
| | *Prince Taldaram* / *Jedoga* / *Volazj* | *Conjure Flame*, *Insanity*, *Cyclone Strike* | **NO** | **NO** | **`IMMUNE`** *(Add = `KICK`)* |
| **5. Drak'Tharon** | *Novos the Summoner* (P2) & Adds | *Frostbolt*, *Arcane Blast*, *Shadow Bolt* | Sì *(P2)* | Sì *(se su te)* | **`BOTH` / `KICK`** |
| | *Trollgore, King Dred, Tharon'ja* | *Consume*, *Rain of Fire*, *Shadow Volley* | **NO** | **NO** | **`IMMUNE`** |
| **6. Violet Hold** | *Portal Guardians / Bosses* (*Lavanthor*, ecc.) | *Arcane Lightning*, *Shadow Bolt*, *Firebolt* | Sì *(trash/alcuni)* | Sì *(trash)* | **`KICK` / `BOTH`** |
| | *Cyanigosa*, *Moragg*, *Erekem* | *Arcane Vacuum*, *Blizzard*, *Optic Link* | **NO** | **NO** | **`IMMUNE`** |
| **7. Gundrak** | *Moorabi* | ***Transformation*** (*Trasformazione Mammut*) | **SÌ (Achievement!)** | **NO** *(self-buff!)* | **`KICK`** |
| | *Slad'ran*, *Colossus*, *Gal'darah*, *Eck* | *Poison Nova*, *Whirlwind*, *Impale* | **NO** | **NO** | **`IMMUNE`** |
| **8. Halls of Stone** | *Maiden of Grief* | *Shock of Sorrow* (AoE), *Parting Sorrow* | **NO** | **NO** *(AoE stun)* | **`IMMUNE`** |
| | *Krystallus*, *Sjonnir* + Adds Tribunal | *Shatter*, *Lightning Ring* / *Chain Lightning* | Sì *(Adds/Chain)* | Solo Adds singoli | **`KICK` / `IMMUNE`** |
| **9. Halls of Lightning** | *General Bjarngrim* | **Attiva *Spell Reflection* su di sé** / *Whirlwind* | **NO** | **NO** | **`IMMUNE`** *(No cast su boss!)* |
| | *Volkhan*, *Ionar*, *Loken* | *Heat*, *Lightning Nova*, *Pulsing Shockwave* | **NO** | **NO** | **`IMMUNE`** |
| | *Stormforged Mender* (Trash) | *Greater Heal*, *Arc Weld* | **SÌ (Critico!)** | **NO** | **`KICK`** |
| **10. The Oculus** | *Mage-Lord Urom* | *Empowered Arcane Explosion* (AoE LoS!), *Frostbolt* | Sì *(Frostbolt)* | **NO** *(Arc. Exp. = AoE)* | **`KICK` / `IMMUNE`** |
| | *Drakos*, *Varos*, *Eregos* | *Thundering Stomp*, combattimento su drago | **NO** | **NO** | **`IMMUNE`** |
| **11. Utgarde Pinnacle** | *Svala*, *Gortok*, *Skadi*, *King Ymiron* | *Ritual*, *Impale*, *Whirlwind*, *Bane* (reflect dmg), *Dark Slash* | **NO** | **NO** | **`IMMUNE`** |
| **12. Culling of Strat.** | *Cultists / Necromancers* + *Salramm* | *Dark Mending*, *Shadow Bolt*, *Curse*, *Rain of Fire* | **SÌ** | Solo *Bolt/Curse* | **`KICK` / `BOTH`** |
| | *Meathook*, *Epoch*, *Mal'Ganis* | *Carrion Swarm* (cono), *Sleep* | **NO** | **NO** | **`IMMUNE`** |
| **13. Trial of Champ.** | ***Grand Champions*** (PvP-Boss!) | Cure (*Holy Light*/*Flash Heal*) = `KICK`; CC/Bolt (*Poly*/*Lava Burst*) = `BOTH`; *Steady Shot* = `KICK` fisico | **SÌ** | Solo magie offensive/CC su te | **`KICK` / `BOTH`** |
| | *Paletress*, *Eadric*, *Black Knight* | *Renew*/*Holy Fire* (`KICK`), *Radiance* (`IMMUNE`), *Desecration* (`IMMUNE`) | Sì *(Paletress)* | **NO** | **`KICK` / `IMMUNE`** |
| **14. Forge of Souls** | ***Devourer of Souls*** | ***Phantom Blast*** (*Esplosione Fantasma*, 2.0s) | **SÌ (Achievement!)** | Sì *(cautela con Mirrored Soul!)* | **`KICK` / `BOTH`** |
| | *Devourer* / *Bronjahm* | *Mirrored Soul*, *Wailing Souls*, *Corrupt Soul*, *Soulstorm* | **NO** | **NO** | **`IMMUNE`** |
| **15. Pit of Saron** | *Krick* & *Deathwhisperer Trash* | *Shadow Bolt*, *Shadow Bolt Volley*, *Hellfire*, *Icebolt* | **SÌ** | Solo single bolt | **`KICK` / `BOTH`** |
| | *Garfrost*, *Ick*, *Tyrannus* | *Throw Saronite* (fisico), *Poison Nova*, *Overlord's Brand*, *Icy Blast* | **NO** | **NO** | **`IMMUNE`** |
| **16. Halls of Reflection** | *Wave Trash* (*Priests, Mages, Riflemen*) | *Flash Heal*/*Heal* (`KICK`), *Flamestrike* (`KICK`), *Shoot/Cursed Arrow* (`KICK` fisico), *Fireball/Frostbolt* (`BOTH`) | **SÌ** | Solo single magic bolt | **`KICK` / `BOTH`** |
| | *Falric*, *Marwyn*, *Lich King Escape* | *Impending Doom*, *Corrupted Flesh*, *Well of Corruption*, *Remorseless Winter* | **NO** | **NO** | **`IMMUNE`** |

#### B. Tutti i 9 Raid WotLK 3.3.5a (Lv. 80)

| Raid | Boss / Incontro | Cast Noti | Puoi Kick? | Puoi Reflect? | Gruppo Netto |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Naxxramas** | ***Kel'Thuzad*** | ***Frostbolt*** (singolo sul tank) | **SÌ (OBBLIGATORIO!)** | **NO** *(Boss immune a reflect!)* | **`KICK`** |
| | *Kel'Thuzad* | *Frostbolt Volley*, *Frost Blast*, *Shadow Fissure* | **NO** | **NO** | **`IMMUNE`** |
| | *Altri 14 Boss Naxxramas* | *Locust Swarm*, *Poison Volley*, *Disrupting Shout*, *Breath*, *Polarity Shift* | **NO** | **NO** | **`IMMUNE`** |
| **OS / EoE / Onyxia** | *Sartharion + Drakes, Malygos, Onyxia 80* | *Flame Breath*, *Shadow Breath*, *Arcane Breath*, *Deep Breath*, *Bellowing Roar* | **NO** | **NO** | **`IMMUNE`** |
| **Vault of Archavon** | *Archavon, Emalon, Koralon, Toravon* | *Rock Shards*, *Lightning Nova*, *Meteor Fists*, *Burning Breath*, *Freezing Ground* | **NO** | **NO** | **`IMMUNE`** |
| **Ulduar** | ***General Vezax*** | ***Searing Flames*** (*Fiamme Ustionanti*) | **SÌ (OBBLIGATORIO!)** | **NO** | **`KICK`** |
| | *Assembly of Iron — Brundir* | *Chain Lightning* (Kick), *Overload* (Immune) | **Sì** *(Chain L.)* | **NO** | **`KICK` / `IMMUNE`** |
| | *Freya (Lashers)* / *Yogg Tentacles* | *Healing Wave* / *Storm Bolt*, *Apathy*, *Curse of Doom* | **Sì** *(adds)* | Solo se singolo diretto | **`KICK` / `BOTH`** |
| | *Leviathan, Ignis, XT-002, Kologarn, Hodir, Mimiron, Algalon, Yogg* | *Slag Pot*, *Tantrum*, *Eyebeam*, *Plasma Blast*, *Big Bang*, *Induce Madness* | **NO** | **NO** | **`IMMUNE`** |
| **ToC / ToGC** | ***Lord Jaraxxus*** | ***Fel Fireball*** (*Palla di Fuoco Vile*) | **SÌ** | **SÌ (Annulla dmg/DoT!)** | **`BOTH`** *(Whitelist!)* |
| | ***Faction Champions*** | Encounter stile PG PvP completo (vedi Tabella PG) | **Sì** | Solo magie single-target su te | **`KICK` / `BOTH`** |
| | *Twin Val'kyr* | *Twin's Pact* (solo **dopo** aver rotto lo scudo!) | **Sì** *(post-shield)* | **NO** | **`KICK` / `IMMUNE`** |
| | *Northrend Beasts, Anub'arak* | *Arctic Breath*, *Fire Bomb*, *Impale*, *Leeching Swarm*, *Penetrating Cold* | **NO** | **NO** | **`IMMUNE`** |
| **Icecrown Citadel** | ***Lady Deathwhisper P2*** | ***Frostbolt*** (singolo sul tank!) | **SÌ (OBBLIGATORIO!)** | **NO** | **`KICK`** |
| | *Lady Deathwhisper P1 Adds* (*Cult Adherent*) | *Deathchill Bolt*, *Curse* (ATTENZIONE: *Shroud of the Occult*!) | Sì *(senza Shroud)* | **NO** *(con Shroud attivo)* | **`BOTH` / `IMMUNE`** |
| | *Valithria Adds* (*Risen Archmage*, *Suppresser*) | *Frostbolt Volley* | Sì / No | **NO** | **`KICK` / `IMMUNE`** |
| | *Prince Keleseth* (BPC) | *Shadow Lance* / *Empowered Shadow Lance* | **NO** | **NO** *(serve soak Dark Nuclei)* | **`IMMUNE`** |
| | *Marrowgar, Saurfang, Festergut, Rotface, Putricide, Lana'thel, Sindragosa, Lich King* | *Bone Spike*, *Bone Storm*, *Pungent Blight*, *Inhale*, *Frost Breath*, *Blistering Cold*, *Soul Reaper*, *Infest*, *Defile*, *Remorseless Winter*, *Soul Shriek* | **NO** | **NO** | **`IMMUNE`** |
| **Ruby Sanctum** | *Baltharus, Saviana, Zarithrian, Halion* | *Flame Breath*, *Dark Breath*, *Blade Tempest*, *Meteor Strike* | **NO** | **NO** | **`IMMUNE`** |

---

### 3.4 ERA PG — GIOCATORI NEMICI (PvP, Arena, Battleground, Duelli)

| Tipologia Cast PG | Esempi / Immunità | Kick (`Shield Bash`/`Pummel`) | Reflect (`Spell Reflection`) | Gruppo Netto |
| :--- | :--- | :---: | :---: | :--- |
| **Magia Offensiva / CC Single-Target sul War Tank** | *Polymorph*, *Cyclone*, *Fear*, *Hex*, *Chaos Bolt*, *Lava Burst*, *Mind Control*, *Entangling Roots*, *Repentance*, *Unstable Affliction*, *Vampiric Touch*, *Frostbolt* | **SÌ** | **SÌ** *(se target = te)* | **`BOTH`** |
| **Cure, Resurrezioni, Evocazioni Pet** | *Holy Light*, *Flash of Light*, *Flash Heal*, *Greater Heal*, *Chain Heal*, *Lesser Healing Wave*, *Nourish*, *Regrowth*, *Rebirth*, *Redemption*, *Summon Felhunter* | **SÌ** | **NO** | **`KICK`** |
| **AoE a Terra & Dispel di Massa** | *Blizzard*, *Flamestrike*, *Rain of Fire*, *Hurricane*, *Hellfire*, *Mass Dispel*, *Tranquility*, *Divine Hymn* | **SÌ** | **NO** | **`KICK`** |
| ***Mana Burn*** (*Bruciatura di Mana*) | Priest cast (flag blizzard non riflettibile in 3.3.5a) | **SÌ** | **NO** | **`KICK`** |
| **Cast Fisici PvP (`spellSchool == 1`)** | *Steady Shot*, *Shattering Throw*, *Slam*, *Revive Pet* | **SÌ** | **NO** | **`KICK`** |
| **Canali PvP già avviati** | *Penance* (offensivo), *Mind Flay*, *Drain Life*, *Drain Mana*, *Drain Soul* | **SÌ** | **NO** *(tick successivi non fermati)* | **`KICK`** |
| **Magia Offensiva sotto *Aura Mastery*** (`31821` + `19746`) | Paladino/Caster alleato protetto da *Aura Mastery* che lancia nuke/CC su di te | **NO** *(immune a kick)* | **SÌ** | **`REFLECT`** |
| **Cure sotto *Aura Mastery* / *Divine Shield* / *Hand of Protection*** | *Divine Shield* (642), *Hand of Protection* (1022 — blocca kick fisico!), *Aura Mastery* (31821) | **NO** | **NO** | **`IMMUNE`** |

---

## 4. Architettura della Soluzione per il Task 44

Per rendere il sistema a prova di errore su **Classic, TBC e WotLK (Mob, PG e Boss)** senza creare migliaia di righe rigide soggette a errori di localizzazione:

1. **Rilevatore Event-Driven `SPELL_CAST_START` (`_G.PWHUD_CastTracker`)**:
   - Intercetta `COMBAT_LOG_EVENT_UNFILTERED` sul singolo subevento `SPELL_CAST_START` e indicizza per `sourceGUID` $\to$ `{ spellId, spellSchool, spellName, destGUID, ts }`.
   - **Vantaggio chiave**: identifica istantaneamente **`spellSchool == 1` (Fisico)** e gli **`spellId`** nativi indipendentemente dalla lingua del client (EN/IT/ES/DE/FR), con costo CPU praticamente nullo.
2. **Albero Decisionale a 4 Stati Netti (`canKick` × `canReflect`)**:
   - **Step 0 — Filtro Pre-Check**: Se `isTradeSkill == true` o `not UnitCanAttack("player", "target")` $\to$ ritorna `nil` (`Castbar Target` e `Alert Kick` spenti).
   - **Step 1 — Valutazione `canKick`**:
     - `false` se `notInterruptible == true`.
     - `false` se `UnitBuff("target", ...)` rileva immunità fisiche/interrupt (*Divine Shield* `642`, *Hand of Protection* `1022`, *Ice Block* `45438`, o *Aura Mastery* `31821` + *Concentration Aura* `19746`).
     - `false` se Boss protetto (scudo *Shock Barrier* / *Shroud of the Occult*).
   - **Step 2 — Valutazione `canReflect`**:
     - Richiede `isTargetingMe == true` (o whitelist speciale raid) e nessuna aura auto-riflettente attiva sul nemico (*Shroud of the Occult* `70768`, Boss *Spell Reflection*).
     - Negato se `spellSchool == 1` (Fisico).
     - Negato se `isChannel == true` (i canali già iniziati richiedono **KICK**, non Reflect).
     - Negato se la spell è nella **Blacklist Bilingue EN/IT + Spell ID Anti-Reflect**:
       - Tutte le Cure & Resurrezioni (*Heal*, *Flash*, *Light*, *Wave*, *Nourish*, *Regrowth*, *Mending*, *Tranquility*, *Renew*, *Pact*, *Cura*, *Luce*, *Lampo*, *Onda*, *Rinascita*, *Resurrezione*...).
       - Tutte le Evocazioni & Self-Buff (*Summon*, *Evoca*, *Transformation*, *Trasformazione*, *Mirrored Soul*).
       - Tutte le AoE / Coni / Soffi / Nova (*Blizzard*, *Flamestrike*, *Rain of Fire*, *Hurricane*, *Hellfire*, *Volley*, *Mass Dispel*, *Breath*, *Soffio*, *Nova*, *Storm*, *Blight*, *Infest*, *Defile*, *Explos*, *Searing Flames*, *Arcane Vacuum*, *Shriek*).
       - Specifica anti-reflect: *Mana Burn* / *Bruciatura di Mana*, *Steady Shot*, *Shattering Throw*, *Slam*, *Shoot*, *Throw*.
     - **Regola Boss (`unitKind == "WORLDBOSS"`)**:
       - Su World Boss / Raid Boss (`UnitClassification == "worldboss"` o `UnitLevel == -1`), `canReflect` è **`false` di default** (protegge automaticamente contro falsi Reflect su *Kel'Thuzad Frostbolt*, *Keleseth Shadow Lance*, *Kael'thas*, *Deathwhisper*, *Lich King*, *Nefarian*, *Ragnaros*, *Halion*), **A MENO CHE** non compaia nella **Whitelist Boss Riflettibili** (*Fel Fireball* / `66532` Jaraxxus, *Deaden* / `41410` Essence of Desire, *Intangible Presence* / `29833` Attumen, *Shadow Blast* / `57620`, o incontri Council/PvP-like come *Faction Champions* / *Delrissa*).
   - **Step 3 — Assegnazione Stati UI (`BOTH`, `KICK`, `REFLECT`, `IMMUNE`)**:
     - `canKick and canReflect` $\to$ `BOTH` (`[SHIELD BASH / REFLECT]` ciano se pronto in melee, oppure `[SPELL REFLECTION]` magenta se fuori melee/SB in CD).
     - `canKick and not canReflect` $\to$ `KICK` (`[SHIELD BASH]` / `[PUMMEL]` / `[KICK CD]`, **MAI** magenta Reflect!).
     - `not canKick and canReflect` $\to$ `REFLECT` (`[SPELL REFLECTION]` magenta se SR+Scudo pronti, altrimenti `[REFLECT CD]` / `[IMMUNE]`; `Alert - Kick Now` resta spento!).
     - `not canKick and not canReflect` $\to$ `IMMUNE` (`[IMMUNE]` grigio; `Alert - Kick Now` spento!).
