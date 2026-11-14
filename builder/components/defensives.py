"""
Modulo Componente: 03, 14, 15, 16 - Defensive Cooldowns & Uptime Tracker (Warrior Protection)
=============================================================================================
Gestisce i cooldown difensivi maggiori del Guerriero Protezione:
1. 03 - Defensive Cooldowns warTank (Riga orizzontale o gruppo icone)
2. 14 - Shield Wall Alert warTank (Spell ID 871: durata attiva 12s e ricarica)
3. 15 - Last Stand Alert warTank (Spell ID 12975: durata attiva 20s e ricarica)
4. 16 - Shield Block Tracker warTank (Spell ID 2565: durata attiva 10s e ricarica rapida 30s/40s)
"""
import copy
from builder.core.constants import PROT_WARRIOR_LOAD, FONT_EXPRESSWAY
from builder.core.helpers import make_subtext, make_glow_action


def build_defensive_auras() -> list[dict]:
    """Costruisce le aure per la mitigazione e i cooldown difensivi maggiori."""
    auras = []

    # 03 - Defensive Cooldowns warTank (Icona Cooldown Enraged Regeneration / Utility Difensiva)
    auras.append({
        "id": "03 - Defensive Cooldowns warTank",
        "uid": "PWHUD_DEFENSIVE_ROW",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 36,
        "height": 36,
        "xOffset": 110,
        "yOffset": -45,
        "anchorPoint": "CENTER",
        "selfPoint": "CENTER",
        "displayIcon": "Interface\\Icons\\Ability_Warrior_EnragedRegeneration",
        "load": copy.deepcopy(PROT_WARRIOR_LOAD),
        "triggers": {
            "1": {
                "trigger": {
                    "type": "custom",
                    "custom_type": "status",
                    "check": "update",
                    "custom": r"""function()
                        if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                        return true
                    end""",
                    "customDuration": r"""function()
                        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
                        local b = buffs and (buffs.bySpellId[55694] or buffs.byName["Enraged Regeneration"])
                        if b and b.duration and b.duration > 0 then
                            return b.duration, b.expirationTime
                        end
                        local start, duration = GetSpellCooldown("Enraged Regeneration")
                        if start and duration and duration > 1.5 then
                            return duration, start + duration
                        end
                        return 0, 0
                    end""",
                    "customIcon": r"""function()
                        return "Interface\\Icons\\Ability_Warrior_EnragedRegeneration"
                    end""",
                    "customText": r"""function()
                        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
                        local b = buffs and (buffs.bySpellId[55694] or buffs.byName["Enraged Regeneration"])
                        if b then return "|cFF00FF00HEAL|r" end
                        return ""
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            }
        },
        "subRegions": [
            make_subtext("%p", "CENTER", "CENTER", 12, 0, 0),
            make_subtext("ER", "RIGHT", "INNER_BOTTOMRIGHT", 9, 2, -2)
        ]
    })

    # 14 - Shield Wall Alert warTank
    auras.append({
        "id": "14 - Shield Wall Alert warTank",
        "uid": "PWHUD_SHIELD_WALL",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 36,
        "height": 36,
        "xOffset": -150,
        "yOffset": -45,
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
                        return true
                    end""",
                    "customDuration": r"""function()
                        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
                        local b = buffs and (buffs.bySpellId[871] or buffs.byName["Shield Wall"])
                        if b and b.duration and b.duration > 0 then
                            return b.duration, b.expirationTime
                        end
                        local start, duration = GetSpellCooldown("Shield Wall")
                        if start and duration and duration > 1.5 then
                            return duration, start + duration
                        end
                        return 0, 0
                    end""",
                    "customIcon": r"""function()
                        return "Interface\\Icons\\Ability_Warrior_ShieldWall"
                    end""",
                    "customText": r"""function()
                        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
                        local b = buffs and (buffs.bySpellId[871] or buffs.byName["Shield Wall"])
                        if b then
                            return "|cFF00FF00-60%|r"
                        end
                        return ""
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            }
        },
        "subRegions": [
            make_subtext("%p", "CENTER", "CENTER", 12, 0, 0),
            make_subtext("%c", "CENTER", "INNER_BOTTOM", 9, 2, 0),
            make_subtext("SW", "RIGHT", "INNER_BOTTOMRIGHT", 9, 2, -2)
        ],
        "conditions": [
            {
                "check": {"trigger": 1, "variable": "show", "value": 1},
                "changes": []
            }
        ]
    })

    # 15 - Last Stand Alert warTank
    auras.append({
        "id": "15 - Last Stand Alert warTank",
        "uid": "PWHUD_LAST_STAND",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 36,
        "height": 36,
        "xOffset": -110,
        "yOffset": -45,
        "anchorPoint": "CENTER",
        "selfPoint": "CENTER",
        "displayIcon": "Interface\\Icons\\Spell_Nature_ShamanRage",
        "load": copy.deepcopy(PROT_WARRIOR_LOAD),
        "triggers": {
            "1": {
                "trigger": {
                    "type": "custom",
                    "custom_type": "status",
                    "check": "update",
                    "custom": r"""function()
                        if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                        return true
                    end""",
                    "customDuration": r"""function()
                        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
                        local b = buffs and (buffs.bySpellId[12975] or buffs.byName["Last Stand"])
                        if b and b.duration and b.duration > 0 then
                            return b.duration, b.expirationTime
                        end
                        local start, duration = GetSpellCooldown("Last Stand")
                        if start and duration and duration > 1.5 then
                            return duration, start + duration
                        end
                        return 0, 0
                    end""",
                    "customIcon": r"""function()
                        return "Interface\\Icons\\Spell_Nature_ShamanRage"
                    end""",
                    "customText": r"""function()
                        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
                        local b = buffs and (buffs.bySpellId[12975] or buffs.byName["Last Stand"])
                        if b then
                            return "|cFF00FF00+30%HP|r"
                        end
                        return ""
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            }
        },
        "subRegions": [
            make_subtext("%p", "CENTER", "CENTER", 12, 0, 0),
            make_subtext("%c", "CENTER", "INNER_BOTTOM", 9, 2, 0),
            make_subtext("LS", "RIGHT", "INNER_BOTTOMRIGHT", 9, 2, -2)
        ]
    })

    # 16 - Shield Block Tracker warTank
    auras.append({
        "id": "16 - Shield Block Tracker warTank",
        "uid": "PWHUD_SHIELD_BLOCK",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 36,
        "height": 36,
        "xOffset": 60,
        "yOffset": -45,
        "anchorPoint": "CENTER",
        "selfPoint": "CENTER",
        "displayIcon": "Interface\\Icons\\Ability_Defensive",
        "load": copy.deepcopy(PROT_WARRIOR_LOAD),
        "triggers": {
            "1": {
                "trigger": {
                    "type": "custom",
                    "custom_type": "status",
                    "check": "update",
                    "custom": r"""function()
                        if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                        return true
                    end""",
                    "customDuration": r"""function()
                        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
                        local b = buffs and (buffs.bySpellId[2565] or buffs.byName["Shield Block"])
                        if b and b.duration and b.duration > 0 then
                            return b.duration, b.expirationTime
                        end
                        local start, duration = GetSpellCooldown("Shield Block")
                        if start and duration and duration > 1.5 then
                            return duration, start + duration
                        end
                        return 0, 0
                    end""",
                    "customIcon": r"""function()
                        return "Interface\\Icons\\Ability_Defensive"
                    end""",
                    "customText": r"""function()
                        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
                        local b = buffs and (buffs.bySpellId[2565] or buffs.byName["Shield Block"])
                        if b then
                            return "|cFF00D0FF100%|r"
                        end
                        return ""
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            }
        },
        "subRegions": [
            make_subtext("%p", "CENTER", "CENTER", 12, 0, 0),
            make_subtext("%c", "CENTER", "INNER_BOTTOM", 9, 2, 0),
            make_subtext("SB", "RIGHT", "INNER_BOTTOMRIGHT", 9, 2, -2)
        ]
    })

    return auras
