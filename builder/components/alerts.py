"""
Modulo Componente: 17 - Alerts warTank
======================================
Gestisce gli avvisi testuali contestuali centrali (a y = 78, sopra Procs):
1. Alert - Sword and Board: Scritta singola centrata (|cFFFFFF00SHIELD SLAM READY!|r) con suono Drums.
2. Alert - Emergency CD: Allarme critico salute (< 35% HP) con raccomandazione cooldown difensivo e suono.
3. Alert - Kick Now: Avviso di interruzione cast prioritario.
4. Alert - Boss Enraged: Avviso Enrage boss per mitigazione immediata.
"""
from builder.core.constants import FONT_EXPRESSWAY


def build_alerts_auras() -> list[dict]:
    """
    Costruisce e restituisce l'aura del gruppo Alerts:
    - 17 - Alerts warTank (Group a y = 78)
    - Alert - Sword and Board (Text con suono Drums)
    - Alert - Emergency CD (Text con suono d'allarme)
    - Alert - Kick Now
    - Alert - Boss Enraged
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
                "Alert - Sword and Board",
                "Alert - Emergency CD",
                "Alert - Kick Now",
                "Alert - Boss Enraged",
                "Alert - Wrong Stance",
            ],
        },
        # 1. Alert - Sword and Board (SHIELD SLAM READY!)
        {
            "id": "Alert - Sword and Board",
            "uid": "PWHUD_ALERT_SAB",
            "parent": "17 - Alerts warTank",
            "regionType": "text",
            "internalVersion": 90,
            "displayText": "|cFFFFFF00SHIELD SLAM READY!|r",
            "fontSize": 20,
            "font": FONT_EXPRESSWAY,
            "outline": "OUTLINE",
            "justify": "CENTER",
            "color": [1, 1, 0, 1],
            "selfPoint": "CENTER",
            "anchorPoint": "CENTER",
            "xOffset": 0,
            "yOffset": 0,
            "actions": {
                "init": {"do_custom": False},
                "start": {
                    "do_sound": True,
                    "sound": "Interface\\AddOns\\WeakAuras\\Media\\Sounds\\Drums.ogg",
                    "sound_path": "Interface\\AddOns\\WeakAuras\\Media\\Sounds\\Drums.ogg",
                    "sound_channel": "Master",
                },
                "finish": {"do_sound": False},
            },
            "triggers": {
                1: {
                    "trigger": {
                        "type": "aura2",
                        "unit": "player",
                        "auranames": ["Sword and Board", "Spada e Scudo", "50227"],
                        "useName": True,
                        "debuffType": "HELPFUL",
                        "matchesShowOn": "showOnActive",
                    },
                    "untrigger": {}
                },
                "activeTriggerMode": -10,
            },
        },
        # 2. Alert - Emergency CD (< 35% HP)
        {
            "id": "Alert - Emergency CD",
            "uid": "PWHUD_ALERT_EMERGENCY",
            "parent": "17 - Alerts warTank",
            "regionType": "text",
            "internalVersion": 90,
            "displayText": "%c",
            "fontSize": 18,
            "font": FONT_EXPRESSWAY,
            "outline": "OUTLINE",
            "justify": "CENTER",
            "color": [1, 0.15, 0.15, 1],
            "selfPoint": "CENTER",
            "anchorPoint": "CENTER",
            "xOffset": 0,
            "yOffset": -24,
            "customTextUpdate": "update",
            "customText": r"""function()
                if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                local em = _G.PWHUD_GetEmergencyCD and _G.PWHUD_GetEmergencyCD()
                if em then
                    return string.format("|cFFFF1010CRIT HP (%.0f%%): USE %s!|r", em.pct, em.action)
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
                            if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                            local em = _G.PWHUD_GetEmergencyCD and _G.PWHUD_GetEmergencyCD()
                            return (em ~= nil)
                        end""",
                    },
                    "untrigger": {"type": "custom", "custom": "function() return false end"}
                },
                "activeTriggerMode": -10,
            },
        },
        # 3. Alert - Kick Now
        {
            "id": "Alert - Kick Now",
            "uid": "PWHUD_ALERT_KICK",
            "parent": "17 - Alerts warTank",
            "regionType": "text",
            "internalVersion": 90,
            "displayText": "%c",
            "fontSize": 16,
            "font": FONT_EXPRESSWAY,
            "outline": "OUTLINE",
            "justify": "CENTER",
            "color": [0.0, 0.9, 1.0, 1],
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
        # 4. Alert - Boss Enraged
        {
            "id": "Alert - Boss Enraged",
            "uid": "PWHUD_ALERT_ENRAGED",
            "parent": "17 - Alerts warTank",
            "regionType": "text",
            "internalVersion": 90,
            "displayText": "|cFFFF0000BOSS ENRAGED! POP CD!|r",
            "fontSize": 18,
            "font": FONT_EXPRESSWAY,
            "outline": "OUTLINE",
            "justify": "CENTER",
            "color": [1, 0, 0, 1],
            "selfPoint": "CENTER",
            "anchorPoint": "CENTER",
            "xOffset": 0,
            "yOffset": 44,
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "custom": r"""function()
                            local tb = _G.PWHUD_GetTargetBuffs and _G.PWHUD_GetTargetBuffs()
                            return (tb ~= nil and tb.hasEnrage)
                        end""",
                    },
                    "untrigger": {"type": "custom", "custom": "function() return false end"}
                },
                "activeTriggerMode": -10,
            },
        },
        # 5. Alert - Wrong Stance (DEFENSIVE STANCE REQUIRED!)
        {
            "id": "Alert - Wrong Stance",
            "uid": "PWHUD_ALERT_WRONG_STANCE",
            "parent": "17 - Alerts warTank",
            "regionType": "text",
            "internalVersion": 90,
            "displayText": "|cFFFF1010>> DEFENSIVE STANCE REQUIRED! <<|r",
            "fontSize": 20,
            "font": FONT_EXPRESSWAY,
            "outline": "OUTLINE",
            "justify": "CENTER",
            "color": [1, 0.1, 0.1, 1],
            "selfPoint": "CENTER",
            "anchorPoint": "CENTER",
            "xOffset": 0,
            "yOffset": 64,
            "actions": {
                "init": {"do_custom": False},
                "start": {
                    "do_sound": True,
                    "sound": "Interface\\AddOns\\WeakAuras\\Media\\Sounds\\RaidWarning.ogg",
                    "sound_path": "Interface\\AddOns\\WeakAuras\\Media\\Sounds\\RaidWarning.ogg",
                    "sound_channel": "Master",
                },
                "finish": {"do_sound": False},
            },
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "event",
                        "events": "PLAYER_REGEN_DISABLED,PLAYER_REGEN_ENABLED,UPDATE_SHAPESHIFT_FORM,PLAYER_ENTERING_WORLD",
                        "custom": r"""function()
                            return UnitAffectingCombat("player") and (GetShapeshiftForm() ~= 2)
                        end""",
                    },
                    "untrigger": {
                        "type": "custom",
                        "custom": r"""function()
                            return not UnitAffectingCombat("player") or (GetShapeshiftForm() == 2)
                        end""",
                    },
                },
                "activeTriggerMode": -10,
            },
        },
    ]
