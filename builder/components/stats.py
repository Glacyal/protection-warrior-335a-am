"""
Modulo Componente: 18 - Stats Panel warTank (Warrior Protection)
================================================================
Gestisce il pannello delle statistiche in tempo reale (88x60px a x = -190, y = -45):
- Mostra 5 righe di statistiche dinamiche di mitigazione e threat per WotLK 3.3.5a:
  1. Skill Difesa & Immunità Critici (DEF 540 Cap per raid boss Lv.83)
  2. Combat Table Coverage (CTC: Schivata + Parata + Blocco + Miss)
  3. Armatura effettiva & Riduzione Danno Fisico % (Armor DR)
  4. Shield Block Value (SBV: danno/threat di Shield Slam)
  5. Melee Hit (Cap 8% / 263 rating) ed Expertise (Soft Cap 26 / 214 rating)
"""
from builder.core.constants import TEXTURE_WHITE8X8, FONT_EXPRESSWAY


def make_stats_custom_text() -> str:
    """Funzione Lua che calcola in tempo reale le statistiche del Protection Warrior con logica WotLK 3.3.5a completa."""
    return r"""function()
    local now = GetTime()
    if _G.PWHUD_LastStatsText and (now - (_G.PWHUD_LastStatsTime or 0)) < 0.1 then
        return _G.PWHUD_LastStatsText
    end

    -- 0. CONTESTO BERSAGLIO & DEBUFFS (Insect Swarm, Scorpid Sting -> Non-stacking +3.0% Boss Miss)
    -- Opzione 1: Default Lv.80 (allineato alla scheda del personaggio in-game)
    -- e scalatura automatica a Lv.83 su Raid Boss / Skull in tempo reale
    local pLvl = UnitLevel("player") or 80
    local targetLevel = pLvl
    local targetMissBonus = 0
    local hasHostileTarget = false
    if UnitExists("target") and not UnitIsDead("target") and UnitCanAttack("player", "target") then
        hasHostileTarget = true
        local lvl = UnitLevel("target")
        if lvl and lvl > 0 then
            targetLevel = lvl
        elseif lvl == -1 or UnitClassification("target") == "worldboss" then
            targetLevel = 83
        end

        for i = 1, 40 do
            local name, _, _, _, _, _, _, _, _, _, spellId = UnitDebuff("target", i)
            if not name then break end
            -- Insect Swarm (Druido: -3% hit) o Scorpid Sting (Cacciatore: -3% hit)
            -- Regola di precedenza WotLK: NON STACKANO! Massimo +3.0%
            if spellId == 5570 or spellId == 27013 or spellId == 24974 or spellId == 24975 or
               spellId == 24976 or spellId == 24977 or spellId == 48468 or spellId == 3043 or
               name == "Insect Swarm" or name == "Sciame d'Insetti" or
               name == "Scorpid Sting" or name == "Puntura dello Scorpide" then
                targetMissBonus = 3.0
                break
            end
        end
    end

    -- 1. DEFENSE SKILL & CRIT IMMUNITY (Cap: 540 per Boss Raid Lv.83, 535 per Eroiche Lv.82)
    local baseDef, armorDef = UnitDefense("player")
    local totalDef = (baseDef or 0) + (armorDef or 0)
    local reqDef = (hasHostileTarget and targetLevel == 82) and 535 or 540
    local defStr
    if totalDef >= reqDef then
        defStr = string.format("|cFF22C55E%d (CAP)|r", totalDef)
    elseif totalDef >= 535 then
        defStr = string.format("|cFFFFD700%d (HC)|r", totalDef)
    else
        defStr = string.format("|cFFFF2020%d/%d|r", totalDef, reqDef)
    end

    -- 2. ARMOR & PHYSICAL DAMAGE REDUCTION (DR%)
    -- EffectiveArmor include tutti i buff attivi (Inspiration/Ancestral Fortitude +25%, Stoneskin/Devotion)
    -- e i debuff (Sunder, Acid Spit, Faerie Fire, Melt Armor)
    local baseArmor, effectiveArmor = UnitArmor("player")
    effectiveArmor = effectiveArmor or baseArmor or 0
    local k = (targetLevel >= 83) and 16635 or (400 + 85 * targetLevel + 4.5 * 85 * (targetLevel - 59))
    local armorDR = math.min(75.0, (effectiveArmor / (effectiveArmor + k)) * 100)
    local armColor = armorDR >= 75.0 and "|cFF22C55E" or "|cFFFFFFFF"
    local armStr = string.format("%s%.1fk|r |cFF80D0FF(%.1f%%)|r", armColor, effectiveArmor / 1000, armorDR)

    -- 3. COMBAT TABLE COVERAGE (CTC = Dodge + Parry + Block + BossMiss)
    local dodge = GetDodgeChance() or 0
    local parry = GetParryChance() or 0
    local block = GetBlockChance() or 0
    local baseBossMiss = (targetLevel >= 83) and 4.4 or (5.0 - (targetLevel - 80) * 0.2)
    local miss = math.max(0, baseBossMiss + math.max(0, (totalDef - 400) * 0.04) + targetMissBonus)
    local ctc = dodge + parry + block + miss
    local ctcStr
    if ctc >= 102.4 then
        ctcStr = string.format("|cFF00FFFF%.1f%% (MAX)|r", ctc)
    else
        ctcStr = string.format("|cFFFFD700%.1f%%|r", ctc)
    end

    -- 4. BLOCK & SHIELD BLOCK VALUE (SBV)
    local sbv = GetShieldBlock() or 0
    local blockStr = string.format("|cFF80D0FF%.1f%%|r |cFFFFD700(%d SBV)|r", block, sbv)

    -- 5. HIT & EXPERTISE (Melee Hit: CR 6, Draenei Heroic Presence +1%; Soft Cap 26, Hard Cap 56)
    local hasHeroicPresence = false
    for i = 1, 40 do
        local name, _, _, _, _, _, _, _, _, _, spellId = UnitBuff("player", i)
        if not name then break end
        if spellId == 28878 or spellId == 6562 or name == "Heroic Presence" or name == "Presenza Eroica" then
            hasHeroicPresence = true
            break
        end
    end

    local hitBonus = GetCombatRatingBonus(6) or 0
    local totalHit = hitBonus + (hasHeroicPresence and 1.0 or 0.0)
    local exp = GetExpertise and GetExpertise() or 0

    local hitColor = (totalHit >= 8.0) and "|cFF22C55E" or "|cFFFFFFFF"
    local expColor = (exp >= 56) and "|cFF00FFFF" or ((exp >= 26) and "|cFF22C55E" or "|cFFFFFFFF")
    local hitExpStr = string.format("%s%.1f%%|r | %s%d Exp|r", hitColor, totalHit, expColor, exp)

    -- FORMATTAZIONE FINALE A 5 RIGHE CON STILE FURY WARRIOR (|cFFFFFFFFLabel:|r <Valore>)
    local res = string.format(
        "|cFFFFFFFFDef:|r %s\n|cFFFFFFFFArmor:|r %s\n|cFFFFFFFFCTC:|r %s\n|cFFFFFFFFBlock:|r %s\n|cFFFFFFFFHit:|r %s",
        defStr, armStr, ctcStr, blockStr, hitExpStr
    )
    _G.PWHUD_LastStatsText = res
    _G.PWHUD_LastStatsTime = now
    return res
end"""


def build_stats_auras() -> list[dict]:
    """Costruisce il gruppo 18 - Stats Panel warTank."""
    stats_events = "PLAYER_ENTERING_WORLD,UNIT_STATS,UNIT_AURA,PLAYER_EQUIPMENT_CHANGED,COMBAT_RATING_UPDATE,PLAYER_TARGET_CHANGED,UNIT_TARGET,RAID_ROSTER_UPDATE,PARTY_MEMBERS_CHANGED"

    return [
        {
            "id": "18 - Stats Panel warTank",
            "uid": "PWHUD_STATS_GRP",
            "parent": "Class Warrior (Protection)",
            "regionType": "group",
            "internalVersion": 90,
            "anchorPoint": "CENTER",
            "selfPoint": "CENTER",
            "xOffset": -190,
            "yOffset": -45,
            "controlledChildren": [
                "Stats Panel - Background warTank",
                "Stats Panel - Text warTank",
            ],
        },
        {
            "id": "Stats Panel - Background warTank",
            "uid": "PWHUD_STATS_BG",
            "parent": "18 - Stats Panel warTank",
            "regionType": "texture",
            "internalVersion": 90,
            "width": 88,
            "height": 60,
            "xOffset": 0,
            "yOffset": 0,
            "texture": TEXTURE_WHITE8X8,
            "color": [0.06, 0.04, 0.04, 0.85],
            "selfPoint": "CENTER",
            "anchorPoint": "CENTER",
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "event",
                        "events": "PLAYER_ENTERING_WORLD,PLAYER_ALIVE",
                        "custom": "function() return true end",
                    },
                    "untrigger": {"type": "custom", "custom": "function() return false end"}
                },
                "activeTriggerMode": -10,
            },
        },
        {
            "id": "Stats Panel - Text warTank",
            "uid": "PWHUD_STATS_TEXT",
            "parent": "18 - Stats Panel warTank",
            "regionType": "text",
            "internalVersion": 90,
            "fontSize": 9,
            "font": FONT_EXPRESSWAY,
            "outline": "OUTLINE",
            "justify": "LEFT",
            "color": [1, 1, 1, 1],
            "selfPoint": "CENTER",
            "anchorPoint": "CENTER",
            "xOffset": 2,
            "yOffset": 0,
            "displayText": "%c",
            "customTextUpdate": "update",
            "customText": make_stats_custom_text(),
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "event",
                        "events": stats_events,
                        "custom": "function(event, ...) return true end",
                    },
                    "untrigger": {"type": "custom", "custom": "function(event, ...) return false end"}
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [],
        },
    ]
