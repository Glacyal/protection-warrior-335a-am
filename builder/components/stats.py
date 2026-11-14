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
    """Funzione Lua che calcola in tempo reale le statistiche del Protection Warrior."""
    return r"""function()
    local now = GetTime()
    if _G.PWHUD_LastStatsText and (now - (_G.PWHUD_LastStatsTime or 0)) < 0.1 then
        return _G.PWHUD_LastStatsText
    end

    -- 1. DEFENSE SKILL & CRIT IMMUNITY (540 Cap per Lv.83 boss)
    local baseDef, armorDef = UnitDefense("player")
    local totalDef = (baseDef or 0) + (armorDef or 0)
    local defStr = ""
    if totalDef >= 540 then
        defStr = string.format("|cFF40FF40DEF: %d (CAP)|r", totalDef)
    else
        defStr = string.format("|cFFFF2020DEF: %d/540|r", totalDef)
    end

    -- 2. COMBAT TABLE COVERAGE (CTC = Dodge + Parry + Block + Miss)
    local dodge = GetDodgeChance() or 0
    local parry = GetParryChance() or 0
    local block = GetBlockChance() or 0
    local miss = 5.0 + math.max(0, (totalDef - 400) * 0.04)
    local ctc = dodge + parry + block + miss
    local ctcStr = ""
    if ctc >= 102.4 then
        ctcStr = string.format("|cFF00FFFFCTC: %.1f%% (MAX)|r", ctc)
    else
        ctcStr = string.format("|cFFFFD700CTC: %.1f%%|r", ctc)
    end

    -- 3. ARMOR & PHYSICAL DR% (Formula WotLK: Armor / (Armor + 16635))
    local baseArmor, effectiveArmor = UnitArmor("player")
    effectiveArmor = effectiveArmor or baseArmor or 0
    local armorDR = (effectiveArmor / (effectiveArmor + 16635)) * 100
    local armStr = string.format("ARM: %.1fk (%.1f%%)", effectiveArmor / 1000, armorDR)

    -- 4. SHIELD BLOCK VALUE (SBV)
    local sbv = GetShieldBlock() or 0
    local sbvStr = string.format("|cFF80D0FFSBV: %d|r", sbv)

    -- 5. HIT & EXPERTISE
    local hitBonus = GetCombatRatingBonus(6) or 0
    local exp = GetExpertise() or 0
    local hitColor = (hitBonus >= 8.0) and "|cFF40FF40" or "|cFFFFD700"
    local expColor = (exp >= 26) and "|cFF40FF40" or "|cFFFFD700"
    local capStr = string.format("%sH:%.1f%%|r %sE:%d|r", hitColor, hitBonus, expColor, exp)

    local res = string.format("%s\n%s\n%s\n%s\n%s", defStr, ctcStr, armStr, sbvStr, capStr)
    _G.PWHUD_LastStatsText = res
    _G.PWHUD_LastStatsTime = now
    return res
end"""


def build_stats_auras() -> list[dict]:
    """Costruisce il gruppo 18 - Stats Panel warTank."""
    stats_events = "PLAYER_ENTERING_WORLD,UNIT_STATS,UNIT_AURA,PLAYER_EQUIPMENT_CHANGED,COMBAT_RATING_UPDATE"

    return [
        {
            "id": "18 - Stats Panel warTank",
            "uid": "PWHUD_STATS_GRP",
            "parent": "Class Warrior (Protection)",
            "regionType": "group",
            "internalVersion": 90,
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
