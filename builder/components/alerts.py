"""
Modulo Componente: 01 & 19 - Alerts, Emergency CD Advisor & Boss Mechanics (Warrior Protection)
================================================================================================
Gestisce:
1. 01 - Emergency & Procs warTank:
   - Alert critico salute bassa (< 35% HP) con raccomandazione dinamica del miglior cooldown difensivo pronto:
     Shield Wall (-60% DR) > Last Stand (+30% HP) > Shield Block (100% BLK) > Enraged Regen (+30% Heal) > Potion/Stone.
   - Proc Sword and Board (ID 50227): reset Shield Slam e costo 0 rabbia con glow dorato ed effetto visivo centrale.
2. 19 - Boss Mechanics Alert warTank:
   - Alert Enrage/Frenzy boss (preparazione CD difensivo / chiamata Tranquilizing Shot).
   - Alert Tank Buster & debuff pericolosi sul tank (Soul Reaper, Impale, Necrotic Strike, Gastric Bloat).
"""
import copy
from builder.core.constants import PROT_WARRIOR_LOAD, FONT_EXPRESSWAY
from builder.core.helpers import make_subtext, make_glow_action


def build_alerts_auras() -> list[dict]:
    """Costruisce le aure dedicate agli allarmi centrali, proc e meccaniche boss."""
    auras = []

    # 01 - Emergency & Procs warTank
    auras.append({
        "id": "01 - Emergency & Procs warTank",
        "uid": "PWHUD_EMERGENCY_PROCS",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 54,
        "height": 54,
        "xOffset": 0,
        "yOffset": 65,
        "anchorPoint": "CENTER",
        "selfPoint": "CENTER",
        "displayIcon": "Interface\\Icons\\Ability_Warrior_ShieldWall",
        "load": copy.deepcopy(PROT_WARRIOR_LOAD),
        "triggers": {
            "1": {
                "trigger": {
                    "type": "custom",
                    "custom_type": "status",
                    "check": "update",
                    "custom": r"""function()
                        if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                        -- 1. Check Emergency Low HP
                        local em = _G.PWHUD_GetEmergencyCD and _G.PWHUD_GetEmergencyCD()
                        if em then return true end

                        -- 2. Check Sword and Board Proc (Spell ID 50227)
                        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
                        if buffs and (buffs.bySpellId[50227] or buffs.byName["Sword and Board"]) then
                            return true
                        end
                        return false
                    end""",
                    "customDuration": r"""function()
                        local em = _G.PWHUD_GetEmergencyCD and _G.PWHUD_GetEmergencyCD()
                        if em then return 0, 0 end
                        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
                        local b = buffs and (buffs.bySpellId[50227] or buffs.byName["Sword and Board"])
                        if b and b.duration and b.duration > 0 then
                            return b.duration, b.expirationTime
                        end
                        return 0, 0
                    end""",
                    "customIcon": r"""function()
                        local em = _G.PWHUD_GetEmergencyCD and _G.PWHUD_GetEmergencyCD()
                        if em then return em.icon end
                        return "Interface\\Icons\\Ability_Warrior_SwordandBoard"
                    end""",
                    "customText": r"""function()
                        local em = _G.PWHUD_GetEmergencyCD and _G.PWHUD_GetEmergencyCD()
                        if em then
                            return string.format("|cFFFF2020%s\n(%.0f%% HP)|r", em.action, em.pct)
                        end
                        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
                        local b = buffs and (buffs.bySpellId[50227] or buffs.byName["Sword and Board"])
                        if b then
                            local rem = math.max(0, b.expirationTime - GetTime())
                            return string.format("|cFFFFD700FREE SHIELD SLAM!\n(%.1fs)|r", rem)
                        end
                        return ""
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            }
        },
        "subRegions": [
            make_subtext("%c", "CENTER", "INNER_BOTTOM", 12, -22, 0, {
                "text_color": [1.0, 1.0, 0.2, 1.0]
            }),
            make_subtext("%p", "CENTER", "CENTER", 14, 0, 0)
        ],
        "conditions": [
            {
                "check": {"trigger": 1, "variable": "show", "value": 1},
                "changes": [
                    {"property": "glow", "value": True}
                ]
            }
        ]
    })

    # 19 - Boss Mechanics Alert warTank
    auras.append({
        "id": "19 - Boss Mechanics Alert warTank",
        "uid": "PWHUD_BOSS_MECHANICS",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 46,
        "height": 46,
        "xOffset": 0,
        "yOffset": 130,
        "anchorPoint": "CENTER",
        "selfPoint": "CENTER",
        "displayIcon": "Interface\\Icons\\Spell_Shadow_UnholyFrenzy",
        "load": copy.deepcopy(PROT_WARRIOR_LOAD),
        "triggers": {
            "1": {
                "trigger": {
                    "type": "custom",
                    "custom_type": "status",
                    "check": "update",
                    "custom": r"""function()
                        if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                        -- Check Boss Enrage
                        local tb = _G.PWHUD_GetTargetBuffs and _G.PWHUD_GetTargetBuffs()
                        if tb and tb.hasEnrage then return true end

                        -- Check Dangerous Debuffs on Player (Tank Busters)
                        local pd = _G.PWHUD_GetPlayerDebuffs and _G.PWHUD_GetPlayerDebuffs()
                        if pd then
                            -- Soul Reaper (73797 / 69409)
                            if pd.bySpellId[73797] or pd.bySpellId[69409] or pd.byName["Soul Reaper"] then
                                return true
                            end
                            -- Gastric Bloat high stacks (>= 8)
                            local gb = pd.byName["Gastric Bloat"] or pd.bySpellId[72219]
                            if gb and gb.count >= 8 then return true end
                            -- Gormok Impale (>= 2 stacks)
                            local imp = pd.byName["Impale"] or pd.bySpellId[67478]
                            if imp and imp.count >= 2 then return true end
                            -- Fusion Punch (67049)
                            if pd.byName["Fusion Punch"] or pd.bySpellId[67049] then return true end
                            -- Necrotic Strike
                            if pd.byName["Necrotic Strike"] or pd.bySpellId[73806] then return true end
                        end
                        return false
                    end""",
                    "customDuration": r"""function()
                        return 0, 0
                    end""",
                    "customIcon": r"""function()
                        local tb = _G.PWHUD_GetTargetBuffs and _G.PWHUD_GetTargetBuffs()
                        if tb and tb.hasEnrage then return "Interface\\Icons\\Spell_Shadow_UnholyFrenzy" end
                        local pd = _G.PWHUD_GetPlayerDebuffs and _G.PWHUD_GetPlayerDebuffs()
                        if pd then
                            local d = pd.byName["Soul Reaper"] or pd.byName["Gastric Bloat"] or pd.byName["Impale"] or pd.byName["Fusion Punch"]
                            if d and d.icon then return d.icon end
                        end
                        return "Interface\\Icons\\Spell_Shadow_UnholyFrenzy"
                    end""",
                    "customText": r"""function()
                        local tb = _G.PWHUD_GetTargetBuffs and _G.PWHUD_GetTargetBuffs()
                        if tb and tb.hasEnrage then
                            return string.format("|cFFFF0000BOSS %s!\nPOP DEFENSIVES / TRANQ!|r", string.upper(tb.enrageName or "ENRAGED"))
                        end
                        local pd = _G.PWHUD_GetPlayerDebuffs and _G.PWHUD_GetPlayerDebuffs()
                        if pd then
                            local sr = pd.byName["Soul Reaper"] or pd.bySpellId[73797] or pd.bySpellId[69409]
                            if sr then
                                local rem = math.max(0, sr.expirationTime - GetTime())
                                return string.format("|cFFFF1010SOUL REAPER (%.1fs)!\nSHIELD BLOCK / WALL!|r", rem)
                            end
                            local gb = pd.byName["Gastric Bloat"] or pd.bySpellId[72219]
                            if gb and gb.count >= 8 then
                                return string.format("|cFFFF4000GASTRIC BLOAT %d STACKS!\nCALL TAUNT SWAP!|r", gb.count)
                            end
                            local imp = pd.byName["Impale"] or pd.bySpellId[67478]
                            if imp and imp.count >= 2 then
                                return string.format("|cFFFF2000IMPALE %d STACKS!\nCALL TAUNT SWAP / POP CD!|r", imp.count)
                            end
                            local fp = pd.byName["Fusion Punch"] or pd.bySpellId[67049]
                            if fp then
                                return "|cFFFF1010FUSION PUNCH!\nPOP DEFENSIVE CD!|r"
                            end
                        end
                        return ""
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            }
        },
        "subRegions": [
            make_subtext("%c", "CENTER", "INNER_BOTTOM", 12, -22, 0, {
                "text_color": [1.0, 0.2, 0.2, 1.0]
            })
        ]
    })

    return auras
