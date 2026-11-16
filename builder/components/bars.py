"""
Modulo Componente: 14 - Rage Bar & 16 - Castbar warTank
========================================================
Gestisce le barre centrali sincronizzate a 278px di larghezza:
1. 14 - Rage Bar (278x14px a y = -20):
   - Barra della rabbia (powertype = 1) con texture statusbar.
   - Colore base: rosso sangue [0.78, 0.12, 0.12, 1.0].
   - Transizione cromatica dinamica ad ambra dorato [1.0, 0.65, 0.10, 1.0] a >= 45 Rage (soglia scarico sicuro Heroic Strike/Cleave).
   - Allerta starvation a < 25 Rage: colore rosso scuro [0.45, 0.05, 0.05, 1.0].
   - Testo centrale: valore numerico rabbia (%p).
2. 16 - Castbar warTank (278x20px a y = +8):
   - Barra di lancio sincronizzata con il bersaglio corrente (o player per lanci Slam/tiro).
   - Mostra icona a sinistra, nome incantesimo con advisor kick interattivo a sinistra (%c1) e tempo residuo a destra (%p).
   - Ciano vivo per spell interrompibili, grigio piombo per spell immuni/protette.
"""
from builder.core.helpers import make_subtext
from builder.core.constants import (
    TEXTURE_STATUSBAR,
    COLOR_RAGE,
    COLOR_RAGE_DUMP,
    COLOR_RAGE_STARVED,
    COLOR_RAGE_BG,
    COLOR_CASTBAR,
    COLOR_CASTBAR_BG,
)


def build_bars_auras() -> list[dict]:
    """
    Costruisce e restituisce le 2 barre principali dell'HUD:
    - 14 - Rage Bar warTank (Aurabar 278x14px a y = -20)
    - 16 - Castbar warTank (Aurabar 278x20px a y = +8)
    """
    return [
        # =====================================================================
        # 14 - RAGE BAR
        # =====================================================================
        {
            "id": "14 - Rage Bar warTank",
            "uid": "PWHUD_RAGEBAR",
            "parent": "Class Warrior (Protection)",
            "regionType": "aurabar",
            "internalVersion": 90,
            "width": 278,
            "height": 14,
            "xOffset": 0,
            "yOffset": -20,
            "barColor": COLOR_RAGE,
            "backgroundColor": COLOR_RAGE_BG,
            "texture": TEXTURE_STATUSBAR,
            "displayText_format_1.percentpower_format": "Number",
            "displayText_format_1.percentpower_decimal_precision": 0,
            "triggers": {
                1: {
                    "trigger": {
                        "type": "unit",
                        "event": "Power",
                        "unit": "player",
                        "powertype": 1,
                        "use_unit": True,
                        "use_powertype": True,
                    },
                    "untrigger": {}
                },
                "activeTriggerMode": -10,
            },
            "conditions": [
                # Condizione 1: Rage >= 45 -> Colore ambra dorato (Rage Dump / Heroic Strike sicuro)
                {
                    "check": {
                        "trigger": 1,
                        "variable": "power",
                        "op": ">=",
                        "value": "45",
                    },
                    "changes": [
                        {
                            "property": "barColor",
                            "value": COLOR_RAGE_DUMP,
                        }
                    ],
                },
                # Condizione 2: Rage < 25 -> Colore scuro desaturato (Starvation)
                {
                    "check": {
                        "trigger": 1,
                        "variable": "power",
                        "op": "<",
                        "value": "25",
                    },
                    "changes": [
                        {
                            "property": "barColor",
                            "value": COLOR_RAGE_STARVED,
                        }
                    ],
                },
            ],
            "subRegions": [
                make_subtext("%p", justify="CENTER", anchor_point="CENTER", font_size=12, y_offset=0),
            ],
        },

        # =====================================================================
        # 16 - CASTBAR WARTANK (CON KICK ADVISOR INTEGRATO)
        # =====================================================================
        {
            "id": "16 - Castbar warTank",
            "uid": "PWHUD_CASTBAR",
            "parent": "Class Warrior (Protection)",
            "regionType": "aurabar",
            "internalVersion": 90,
            "width": 278,
            "height": 20,
            "xOffset": 0,
            "yOffset": 8,
            "barColor": COLOR_CASTBAR,
            "backgroundColor": COLOR_CASTBAR_BG,
            "texture": TEXTURE_STATUSBAR,
            "icon": True,
            "icon_side": "LEFT",
            "iconSource": -1,
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "custom": r"""function()
                            if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                            local spell = UnitCastingInfo("target") or UnitChannelInfo("target")
                            if spell then return true end
                            spell = UnitCastingInfo("player") or UnitChannelInfo("player")
                            return (spell ~= nil)
                        end""",
                        "customDuration": r"""function()
                            local spell, rank, disp, icon, sTime, eTime, isTrade, castID, notInt = UnitCastingInfo("target")
                            if not spell then
                                spell, rank, disp, icon, sTime, eTime, isTrade, notInt = UnitChannelInfo("target")
                            end
                            if not spell then
                                spell, rank, disp, icon, sTime, eTime = UnitCastingInfo("player")
                            end
                            if not spell then
                                spell, rank, disp, icon, sTime, eTime = UnitChannelInfo("player")
                            end
                            if sTime and eTime then
                                local dur = (eTime - sTime) / 1000
                                return dur, eTime / 1000
                            end
                            return 0, 0
                        end""",
                        "customIcon": r"""function()
                            local spell, rank, disp, icon = UnitCastingInfo("target") or UnitChannelInfo("target")
                            if not spell then
                                spell, rank, disp, icon = UnitCastingInfo("player") or UnitChannelInfo("player")
                            end
                            return icon or "Interface\\Icons\\Temp"
                        end""",
                        "customText": r"""function()
                            local spell, rank, disp, icon, sTime, eTime, isTrade, castID, notInt = UnitCastingInfo("target")
                            local isTarget = true
                            if not spell then
                                spell, rank, disp, icon, sTime, eTime, isTrade, notInt = UnitChannelInfo("target")
                            end
                            if not spell then
                                spell, rank, disp, icon, sTime, eTime = UnitCastingInfo("player") or UnitChannelInfo("player")
                                isTarget = false
                            end
                            if not spell then return "" end

                            if isTarget then
                                local ki = _G.PWHUD_GetKickInfo and _G.PWHUD_GetKickInfo()
                                if notInt then
                                    return string.format("|cFF888888%s [IMMUNE]|r", spell)
                                elseif ki and ki.recommended then
                                    return string.format("|cFF00FFFF%s [%s]|r", spell, ki.recommended)
                                else
                                    return string.format("|cFF00FFFF%s [KICKABLE]|r", spell)
                                end
                            else
                                return spell
                            end
                        end"""
                    },
                    "untrigger": {"type": "custom", "custom": "function() return false end"}
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                make_subtext("%c", justify="LEFT", anchor_point="INNER_LEFT", font_size=11, y_offset=0, x_offset=4),
                make_subtext("%p", justify="RIGHT", anchor_point="INNER_RIGHT", font_size=11, y_offset=0, x_offset=-4),
            ],
        },
    ]
