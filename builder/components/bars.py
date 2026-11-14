"""
Modulo Componente: 07, 08, 09 - Bars: Rage, Health & Castbar (Warrior Protection)
=================================================================================
Gestisce:
1. 07 - Rage Bar warTank (Y = -14, larghezza 210, altezza 14):
   - Valore esatto di Rabbia (0-100) con colorazione cromatica:
     * < 15: Rosso scuro (Rabbia insufficiente per abilità primarie)
     * 15 - 44: Crimson intenso (Fascia operativa di mitigazione)
     * >= 45: Oro/Ambra (Soglia di scarico sicuro con Heroic Strike/Cleave)
2. 08 - Health Bar warTank (Y = -28, larghezza 210, altezza 14):
   - Monitoraggio real-time della salute del tank con soglie cromatiche dinamiche:
     * > 65%: Verde salvezza
     * 35% - 65%: Ambra cautela
     * < 35%: Rosso lampeggiante allerta emergenza cooldown
3. 09 - Castbar warTank (Y = -95, larghezza 210, altezza 14):
   - Castbar del target con differenziazione immediata di interruzione:
     * Ciano brillante: Cast interrompibile (kickable)
     * Grigio piombo: Cast protetto / immune ai kick
"""
import copy
from builder.core.constants import (
    PROT_WARRIOR_LOAD,
    FONT_EXPRESSWAY,
    TEXTURE_STATUSBAR,
    COLOR_RAGE,
    COLOR_RAGE_BG,
    COLOR_HEALTH_HIGH,
    COLOR_HEALTH_BG,
)
from builder.core.helpers import make_subtext


def build_bars_auras() -> list[dict]:
    """Costruisce le barre grafiche di rabbia, salute ed esecuzione cast del bersaglio."""
    auras = []

    # 07 - Rage Bar warTank
    auras.append({
        "id": "07 - Rage Bar warTank",
        "uid": "PWHUD_RAGE_BAR",
        "regionType": "aurabar",
        "internalVersion": 90,
        "width": 210,
        "height": 14,
        "xOffset": 0,
        "yOffset": -14,
        "anchorPoint": "CENTER",
        "selfPoint": "CENTER",
        "barColor": COLOR_RAGE,
        "barColor2": COLOR_RAGE_BG,
        "texture": TEXTURE_STATUSBAR,
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
                        local cur = UnitMana("player") or 0
                        local maxRage = UnitManaMax("player") or 100
                        return cur, maxRage
                    end""",
                    "customText": r"""function()
                        local cur = UnitMana("player") or 0
                        if cur >= 45 then
                            return string.format("|cFFFFD700%d (DUMP)|r", cur)
                        elseif cur < 15 then
                            return string.format("|cFFFF4040%d|r", cur)
                        else
                            return tostring(cur)
                        end
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            }
        },
        "subRegions": [
            make_subtext("%c", "CENTER", "CENTER", 11, 0, 0),
            make_subtext("RAGE", "LEFT", "INNER_LEFT", 9, 0, 4)
        ]
    })

    # 08 - Health Bar warTank
    auras.append({
        "id": "08 - Health Bar warTank",
        "uid": "PWHUD_HEALTH_BAR",
        "regionType": "aurabar",
        "internalVersion": 90,
        "width": 210,
        "height": 14,
        "xOffset": 0,
        "yOffset": -28,
        "anchorPoint": "CENTER",
        "selfPoint": "CENTER",
        "barColor": COLOR_HEALTH_HIGH,
        "barColor2": COLOR_HEALTH_BG,
        "texture": TEXTURE_STATUSBAR,
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
                        local cur = UnitHealth("player") or 0
                        local maxHP = UnitHealthMax("player") or 1
                        return cur, maxHP
                    end""",
                    "customText": r"""function()
                        local cur = UnitHealth("player") or 0
                        local maxHP = UnitHealthMax("player") or 1
                        local pct = (cur / maxHP) * 100
                        if pct <= 35 then
                            return string.format("|cFFFF2020%d / %d (%.0f%%) [CRIT!]|r", cur, maxHP, pct)
                        elseif pct <= 65 then
                            return string.format("|cFFFFD000%d / %d (%.0f%%)|r", cur, maxHP, pct)
                        else
                            return string.format("|cFF40FF40%d / %d (%.0f%%)|r", cur, maxHP, pct)
                        end
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            }
        },
        "subRegions": [
            make_subtext("%c", "CENTER", "CENTER", 10, 0, 0),
            make_subtext("HP", "LEFT", "INNER_LEFT", 9, 0, 4)
        ]
    })

    # 09 - Castbar warTank
    auras.append({
        "id": "09 - Castbar warTank",
        "uid": "PWHUD_CASTBAR",
        "regionType": "aurabar",
        "internalVersion": 90,
        "width": 210,
        "height": 14,
        "xOffset": 0,
        "yOffset": -95,
        "anchorPoint": "CENTER",
        "selfPoint": "CENTER",
        "barColor": [0.0, 0.85, 1.0, 1.0],
        "barColor2": [0.05, 0.08, 0.12, 0.85],
        "texture": TEXTURE_STATUSBAR,
        "load": copy.deepcopy(PROT_WARRIOR_LOAD),
        "triggers": {
            "1": {
                "trigger": {
                    "type": "custom",
                    "custom_type": "status",
                    "check": "update",
                    "custom": r"""function()
                        if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                        local spell = UnitCastingInfo("target") or UnitChannelInfo("target")
                        return (spell ~= nil)
                    end""",
                    "customDuration": r"""function()
                        local spell, rank, disp, icon, sTime, eTime, isTrade, castID, notInt = UnitCastingInfo("target")
                        if not spell then
                            spell, rank, disp, icon, sTime, eTime, isTrade, notInt = UnitChannelInfo("target")
                        end
                        if sTime and eTime then
                            local dur = (eTime - sTime) / 1000
                            return dur, eTime / 1000
                        end
                        return 0, 0
                    end""",
                    "customText": r"""function()
                        local spell, rank, disp, icon, sTime, eTime, isTrade, castID, notInt = UnitCastingInfo("target")
                        if not spell then
                            spell, rank, disp, icon, sTime, eTime, isTrade, notInt = UnitChannelInfo("target")
                        end
                        if spell then
                            if notInt then
                                return string.format("|cFF808080[IMMUNE] %s|r", spell)
                            else
                                return string.format("|cFF00FFFF[KICKABLE] %s|r", spell)
                            end
                        end
                        return ""
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            }
        },
        "subRegions": [
            make_subtext("%c", "CENTER", "CENTER", 10, 0, 0)
        ]
    })

    return auras
