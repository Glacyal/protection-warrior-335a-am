"""
Modulo Componente: 05 & 18 - Debuffs, Stance & Sunder Tracker (Warrior Protection)
==================================================================================
Gestisce:
1. 05 - Debuffs & Stance warTank:
   - Controllo Postura Difensiva (GetShapeshiftForm() == 2): alert sonoro/visivo se il tank entra in combattimento fuori da Defensive Stance.
   - Monitoraggio Demoralizing Shout / Vindication (-575 AP) sul target con notifica debuff mancante.
   - Monitoraggio Thunder Clap / Frost Fever (-20% Attack Speed) sul target con notifica debuff mancante.
2. 18 - Sunder Armor Tracker warTank:
   - Conteggio cariche Sunder Armor / Expose Armor (1-5) sul boss con timer di scadenza e colorazione reattiva.
"""
import copy
from builder.core.constants import PROT_WARRIOR_LOAD, FONT_EXPRESSWAY
from builder.core.helpers import make_subtext


def build_debuff_auras() -> list[dict]:
    """Costruisce le aure per il controllo della postura e dei debuff sul target."""
    auras = []

    # 05 - Debuffs & Stance warTank (Allerta Postura Difensiva / Debuff Boss)
    auras.append({
        "id": "05 - Debuffs & Stance warTank",
        "uid": "PWHUD_STANCE_DEBUFFS",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 38,
        "height": 38,
        "xOffset": -65,
        "yOffset": 45,
        "anchorPoint": "CENTER",
        "selfPoint": "CENTER",
        "displayIcon": "Interface\\Icons\\Ability_Racial_Avatar",
        "load": copy.deepcopy(PROT_WARRIOR_LOAD),
        "triggers": {
            "1": {
                "trigger": {
                    "type": "custom",
                    "custom_type": "status",
                    "check": "update",
                    "custom": r"""function()
                        if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                        -- 1. Check if NOT in Defensive Stance while in combat
                        local inCombat = UnitAffectingCombat("player")
                        local form = GetShapeshiftForm() -- 2 = Defensive Stance
                        if inCombat and form ~= 2 then return true end

                        -- 2. Check missing Thunder Clap / Demo Shout on target in combat
                        if inCombat and UnitExists("target") and not UnitIsDead("target") and UnitCanAttack("player", "target") then
                            local td = _G.PWHUD_GetTargetDebuffs and _G.PWHUD_GetTargetDebuffs()
                            if td and (not td.hasThunder or not td.hasDemo) then
                                return true
                            end
                        end
                        return false
                    end""",
                    "customDuration": r"""function()
                        return 0, 0
                    end""",
                    "customIcon": r"""function()
                        local form = GetShapeshiftForm()
                        if form ~= 2 then
                            return "Interface\\Icons\\Ability_Racial_Avatar"
                        end
                        local td = _G.PWHUD_GetTargetDebuffs and _G.PWHUD_GetTargetDebuffs()
                        if td and not td.hasThunder then
                            return "Interface\\Icons\\Spell_Nature_ThunderClap"
                        elseif td and not td.hasDemo then
                            return "Interface\\Icons\\Ability_Warrior_WarCry"
                        end
                        return "Interface\\Icons\\Ability_Racial_Avatar"
                    end""",
                    "customText": r"""function()
                        local form = GetShapeshiftForm()
                        if form ~= 2 then
                            return "|cFFFF1010DEFENSIVE STANCE\nMISSING!|r"
                        end
                        local td = _G.PWHUD_GetTargetDebuffs and _G.PWHUD_GetTargetDebuffs()
                        if td and not td.hasThunder then
                            return "|cFFFF8000TC MISSING (-20% ATK)|r"
                        elseif td and not td.hasDemo then
                            return "|cFFFFB000DEMO MISSING (-AP)|r"
                        end
                        return ""
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            }
        },
        "subRegions": [
            make_subtext("%c", "CENTER", "INNER_BOTTOM", 10, -18, 0, {
                "text_color": [1.0, 0.4, 0.0, 1.0]
            })
        ]
    })

    # 18 - Sunder Armor Tracker warTank
    auras.append({
        "id": "18 - Sunder Armor Tracker warTank",
        "uid": "PWHUD_SUNDER_TRACKER",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 38,
        "height": 38,
        "xOffset": 65,
        "yOffset": 45,
        "anchorPoint": "CENTER",
        "selfPoint": "CENTER",
        "displayIcon": "Interface\\Icons\\Ability_Warrior_Sunder",
        "load": copy.deepcopy(PROT_WARRIOR_LOAD),
        "triggers": {
            "1": {
                "trigger": {
                    "type": "custom",
                    "custom_type": "status",
                    "check": "update",
                    "custom": r"""function()
                        if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                        return UnitExists("target") and not UnitIsDead("target") and UnitCanAttack("player", "target")
                    end""",
                    "customDuration": r"""function()
                        local td = _G.PWHUD_GetTargetDebuffs and _G.PWHUD_GetTargetDebuffs()
                        if td and td.sunderExp and td.sunderExp > 0 then
                            local rem = td.sunderExp - GetTime()
                            return 30, td.sunderExp
                        end
                        return 0, 0
                    end""",
                    "customIcon": r"""function()
                        return "Interface\\Icons\\Ability_Warrior_Sunder"
                    end""",
                    "customText": r"""function()
                        local td = _G.PWHUD_GetTargetDebuffs and _G.PWHUD_GetTargetDebuffs()
                        local count = (td and td.sunderCount) or 0
                        if count == 0 then
                            return "|cFFFF2020SUNDER: 0/5|r"
                        elseif count < 5 then
                            return string.format("|cFFFFD700SUNDER: %d/5|r", count)
                        else
                            return "|cFF00FF00SUNDER: 5/5|r"
                        end
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            }
        },
        "subRegions": [
            make_subtext("%c", "CENTER", "INNER_BOTTOM", 10, -18, 0),
            make_subtext("%p", "CENTER", "CENTER", 12, 0, 0)
        ]
    })

    return auras
