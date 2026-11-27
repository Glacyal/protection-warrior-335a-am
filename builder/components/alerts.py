"""
Modulo Componente: 17 - Alerts warTank
======================================
Gestisce gli avvisi testuali contestuali centrali (a y = 78, sopra Procs):
1. Alert - Emergency CD: Allarme critico salute (< 35% HP) con raccomandazione cooldown difensivo e suono.
2. Alert - Kick Now: Avviso di interruzione cast prioritario.
(Nota: Banner testuali invasivi per Boss Enraged, Wrong Stance e Sword and Board rimossi per garantire zero clutter).
"""
from builder.core.constants import FONT_EXPRESSWAY
from builder.components.bars import SHARED_CASTBAR_LOGIC_LUA


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
                local actionName = nil
                if _G.PWHUD_GetEmergencyCD then
                    local cd = _G.PWHUD_GetEmergencyCD(80)
                    if type(cd) == "table" and cd.action then
                        actionName = cd.action
                    elseif type(cd) == "string" then
                        actionName = cd
                    end
                end
                if not actionName or actionName == "" then
                    actionName = "DEFENSIVE"
                end
                local hp = UnitHealth("player") or 0
                local maxHp = UnitHealthMax("player") or 1
                local pct = maxHp > 0 and (hp / maxHp * 100) or 100
                return string.format("|cFFFF0000CRIT HP (%.0f%%): POP %s!|r", pct, actionName:upper())
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
                            if not UnitAffectingCombat("player") or UnitIsDeadOrGhost("player") then
                                return false
                            end
                            local hp = UnitHealth("player") or 0
                            local maxHp = UnitHealthMax("player") or 1
                            local pct = maxHp > 0 and (hp / maxHp * 100) or 100
                            return pct < 35
                        end""",
                    },
                    "untrigger": {
                        "type": "custom",
                        "custom": r"""function()
                            if not UnitAffectingCombat("player") or UnitIsDeadOrGhost("player") then
                                return true
                            end
                            local hp = UnitHealth("player") or 0
                            local maxHp = UnitHealthMax("player") or 1
                            local pct = maxHp > 0 and (hp / maxHp * 100) or 100
                            return pct >= 80
                        end"""
                    }
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
            "actions": {
                "init": {
                    "do_custom": True,
                    "custom": "if not _G.PWHUD_GetTargetCastInfo and _G.PWHUD_InitCastAdvisor then _G.PWHUD_InitCastAdvisor() end",
                },
                "start": {},
                "finish": {},
            },
            "customText": r"""function()
                if not UnitExists("target") or not UnitCanAttack("player", "target") or UnitIsDead("target") then
                    return ""
                end
                if not _G.PWHUD_GetTargetCastInfo and _G.PWHUD_InitCastAdvisor then
                    _G.PWHUD_InitCastAdvisor()
                end
                local ki = _G.PWHUD_GetTargetCastInfo and _G.PWHUD_GetTargetCastInfo()
                if ki and ki.canKick and ki.recommended then
                    if ki.recommended == "SPELL REFLECTION" then
                        return "|cFFFF55FFUSE SPELL REFLECTION!|r"
                    end
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
                            if not UnitExists("target") or not UnitCanAttack("player", "target") or UnitIsDead("target") then
                                return false
                            end
                            if not _G.PWHUD_GetTargetCastInfo and _G.PWHUD_InitCastAdvisor then
                                _G.PWHUD_InitCastAdvisor()
                            end
                            local ki = _G.PWHUD_GetTargetCastInfo and _G.PWHUD_GetTargetCastInfo()
                            return (ki ~= nil and ki.canKick == true)
                        end""",
                    },
                    "untrigger": {
                        "type": "custom",
                        "custom": r"""function()
                            if not UnitExists("target") or not UnitCanAttack("player", "target") or UnitIsDead("target") then
                                return true
                            end
                            local ki = _G.PWHUD_GetTargetCastInfo and _G.PWHUD_GetTargetCastInfo()
                            return (ki == nil or not ki.canKick)
                        end"""
                    }
                },
                "activeTriggerMode": -10,
            },
        },
    ]
