"""
Modulo Componente: 17 - Alerts warTank
======================================
Gestisce gli avvisi testuali contestuali centrali (a y = 78, sopra Procs):
1. Alert - Emergency CD: Allarme critico salute (< 35% HP) con raccomandazione cooldown difensivo e suono.
2. Alert - Kick Now: Avviso di interruzione cast prioritario.
(Nota: Banner testuali invasivi per Boss Enraged, Wrong Stance e Sword and Board rimossi per garantire zero clutter).
"""
from builder.core.constants import FONT_EXPRESSWAY


def build_alerts_auras() -> list[dict]:
    """
    Costruisce e restituisce l'aura del gruppo Alerts:
    - 17 - Alerts warTank (Group a y = 78)
    - Alert - Emergency CD (Text con suono d'allarme)
    - Alert - Kick Now
    """
    return [
        {
            "id": "17 - Alerts warTank",
            "uid": "PWHUD_ALERTS_GRP",
            "parent": "Class Warrior (Protection)",
            "regionType": "group",
            "internalVersion": 90,
            "anchorPoint": "CENTER",
            "selfPoint": "CENTER",
            "xOffset": 0,
            "yOffset": 78,
            "controlledChildren": [
                "Alert - Emergency CD",
                "Alert - Kick Now",
            ],
        },
        # 1. Alert - Emergency CD (CRIT HP: POP CD!)
        {
            "id": "Alert - Emergency CD",
            "uid": "PWHUD_ALERT_EMERGENCY",
            "parent": "17 - Alerts warTank",
            "regionType": "text",
            "internalVersion": 90,
            "displayText": "%c",
            "fontSize": 22,
            "font": FONT_EXPRESSWAY,
            "outline": "OUTLINE",
            "justify": "CENTER",
            "color": [1, 0.2, 0.2, 1],
            "selfPoint": "CENTER",
            "anchorPoint": "CENTER",
            "xOffset": 0,
            "yOffset": -24,
            "customTextUpdate": "update",
            "customText": r"""function()
                local cd = _G.PWHUD_GetEmergencyCD and _G.PWHUD_GetEmergencyCD()
                if cd then
                    return string.format("|cFFFF0000CRIT HP: POP %s!|r", cd:upper())
                end
                local hp = UnitHealth("player")
                local maxHp = UnitHealthMax("player")
                local pct = maxHp > 0 and (hp / maxHp * 100) or 100
                if pct < 35 then
                    return "|cFFFF0000CRIT HP: POP DEFENSIVE!|r"
                end
                return ""
            end""",
            "actions": {
                "init": {"do_custom": False},
                "start": {
                    "do_sound": True,
                    "sound": "Interface\\AddOns\\WeakAuras\\Media\\Sounds\\AirHorn.ogg",
                    "sound_path": "Interface\\AddOns\\WeakAuras\\Media\\Sounds\\AirHorn.ogg",
                    "sound_channel": "Master",
                },
                "finish": {"do_sound": False},
            },
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "custom": r"""function()
                            local hp = UnitHealth("player")
                            local maxHp = UnitHealthMax("player")
                            local pct = maxHp > 0 and (hp / maxHp * 100) or 100
                            return pct < 35 and UnitAffectingCombat("player")
                        end""",
                    },
                    "untrigger": {"type": "custom", "custom": "function() return false end"}
                },
                "activeTriggerMode": -10,
            },
        },
        # 2. Alert - Kick Now (INTERRUPT TARGET!)
        {
            "id": "Alert - Kick Now",
            "uid": "PWHUD_ALERT_KICK",
            "parent": "17 - Alerts warTank",
            "regionType": "text",
            "internalVersion": 90,
            "displayText": "%c",
            "fontSize": 20,
            "font": FONT_EXPRESSWAY,
            "outline": "OUTLINE",
            "justify": "CENTER",
            "color": [0, 1, 1, 1],
            "selfPoint": "CENTER",
            "anchorPoint": "CENTER",
            "xOffset": 0,
            "yOffset": 24,
            "customTextUpdate": "update",
            "customText": r"""function()
                local ki = _G.PWHUD_GetKickInfo and _G.PWHUD_GetKickInfo()
                if ki and not ki.notInterruptible and ki.canKick then
                    return string.format("|cFF00FFFFINTERRUPT: %s!|r", ki.recommended)
                end
                return ""
            end""",
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "custom": r"""function()
                            local ki = _G.PWHUD_GetKickInfo and _G.PWHUD_GetKickInfo()
                            return (ki ~= nil and not ki.notInterruptible and ki.canKick)
                        end""",
                    },
                    "untrigger": {"type": "custom", "custom": "function() return false end"}
                },
                "activeTriggerMode": -10,
            },
        },
    ]
