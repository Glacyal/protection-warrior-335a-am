"""
Modulo Componente: 15 - Rotational Bar (Swing Timer & Heroic Strike Queued)
===========================================================================
Gestisce la barra orizzontale centrale composita a y = -7 (278x7px):
1. Background Frame (278x7px, scuro semitrasparente).
2. Swing Timer Melee Mano Primaria (MH) con timing %c (es. 1.8s) e avanzamento swipe.
3. Indicatore Heroic Strike / Cleave Queued:
   - Rileva in tempo reale se Heroic Strike (47450) o Cleave (47520) è accodato tramite IsCurrentSpell().
   - Illuminazione cromatica dinamica su tutta la barra (278x7px) e Pixel Glow dedicato (Oro per Heroic Strike, Verde Smeraldo per Cleave).
"""
from builder.core.helpers import make_subtext
from builder.core.constants import TEXTURE_STATUSBAR, TEXTURE_WHITE8X8


SHARED_SWING_TIMER_LUA = r"""_G.PWHUD_GetSwing = function()
    _G.PWHUD_Swing = _G.PWHUD_Swing or {
        mhStart = 0,
        mhDur = 2.6,
        hsQueued = false,
        cleaveQueued = false,
    }
    local sw = _G.PWHUD_Swing

    local f = _G.PWHUD_SwingFrame
    if not f then
        f = CreateFrame("Frame")
        rawset(_G, "PWHUD_SwingFrame", f)

        local playerGUID = nil
        local function handleCLEU(...)
            local ts, ev, srcGUID = select(1, ...), select(2, ...), select(3, ...)
            if not playerGUID then playerGUID = UnitGUID("player") end
            if srcGUID ~= playerGUID then return end

            local now = GetTime()
            local mhSpeed = UnitAttackSpeed("player") or 2.6

            if ev == "SWING_DAMAGE" or ev == "SWING_MISSED" then
                sw.mhStart = now
                sw.mhDur = mhSpeed
            elseif ev == "SPELL_DAMAGE" or ev == "SPELL_MISSED" then
                local sId = select(9, ...)
                local sName = select(10, ...)
                if sId == 47450 or sName == "Heroic Strike" or sName == "Colpo Eroico" then
                    sw.mhStart = now
                    sw.mhDur = mhSpeed
                    sw.hsQueued = false
                elseif sId == 47520 or sName == "Cleave" or sName == "Fendente" then
                    sw.mhStart = now
                    sw.mhDur = mhSpeed
                    sw.cleaveQueued = false
                end
            elseif ev == "SPELL_EXTRA_ATTACKS" then
                sw.mhStart = now
                sw.mhDur = mhSpeed
            end
        end

        f:RegisterEvent("COMBAT_LOG_EVENT_UNFILTERED")
        f:RegisterEvent("UNIT_ATTACK_SPEED")
        f:RegisterEvent("PLAYER_ENTERING_WORLD")
        f:SetScript("OnEvent", function(self, event, ...)
            if event == "COMBAT_LOG_EVENT_UNFILTERED" then
                handleCLEU(...)
            elseif event == "UNIT_ATTACK_SPEED" then
                local u = select(1, ...)
                if u == "player" then
                    local mh = UnitAttackSpeed("player")
                    if mh and mh > 0 then sw.mhDur = mh end
                end
            elseif event == "PLAYER_ENTERING_WORLD" then
                local mh = UnitAttackSpeed("player")
                if mh and mh > 0 then sw.mhDur = mh end
            end
        end)
    end

    local isHS = IsCurrentSpell(47450) or IsCurrentSpell("Heroic Strike") or IsCurrentSpell("Colpo Eroico")
    local isCL = IsCurrentSpell(47520) or IsCurrentSpell("Cleave") or IsCurrentSpell("Fendente")
    sw.hsQueued = isHS
    sw.cleaveQueued = isCL
    return sw
end"""


def build_rotational_auras() -> list[dict]:
    """
    Costruisce e restituisce le aure del gruppo Rotational Bar:
    - 15 - Rotational Bar (Group 278x7px a y = -7)
    - Rotational Bar - Background
    - Rotational Bar - MH Swing
    - Rotational Bar - Queue Glow
    """
    return [
        # Gruppo contenitore (278x7px a y = -7)
        {
            "id": "15 - Rotational Bar",
            "uid": "PWHUD_ROTCENTER_GRP",
            "parent": "Class Warrior (Protection)",
            "regionType": "group",
            "internalVersion": 90,
            "anchorPoint": "CENTER",
            "selfPoint": "CENTER",
            "xOffset": 0,
            "yOffset": -7,
            "controlledChildren": [
                "Rotational Bar - Background",
                "Rotational Bar - MH Swing",
                "Rotational Bar - Queue Glow",
            ],
            "actions": {
                "init": {
                    "do_custom": True,
                    "custom": SHARED_SWING_TIMER_LUA,
                },
                "start": {},
                "finish": {},
            },
        },
        # Background Frame (278x7px)
        {
            "id": "Rotational Bar - Background",
            "uid": "PWHUD_ROTCENTER_BG",
            "parent": "15 - Rotational Bar",
            "regionType": "texture",
            "internalVersion": 90,
            "xOffset": 0,
            "yOffset": 0,
            "width": 278,
            "height": 7,
            "texture": TEXTURE_WHITE8X8,
            "color": [0.08, 0.04, 0.04, 0.85],
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
                    "untrigger": {
                        "custom": "function() return false end",
                    }
                },
                "activeTriggerMode": -10,
            },
        },
        # MH Swing (278x5px a x = 0) con etichetta timing %c
        {
            "id": "Rotational Bar - MH Swing",
            "uid": "PWHUD_ROTCENTER_MH",
            "parent": "15 - Rotational Bar",
            "regionType": "aurabar",
            "internalVersion": 90,
            "width": 274,
            "height": 5,
            "xOffset": 0,
            "yOffset": 0,
            "barColor": [0.85, 0.45, 0.15, 1.0],
            "backgroundColor": [0.12, 0.06, 0.04, 0.6],
            "texture": TEXTURE_STATUSBAR,
            "inverse": False,
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "custom": "function() return true end",
                        "customDuration": r"""function()
                            if _G.PWHUD_GetSwing then _G.PWHUD_GetSwing() end
                            local sw = _G.PWHUD_Swing
                            local now = GetTime()
                            local start = sw and sw.mhStart or 0
                            local dur = sw and sw.mhDur or UnitAttackSpeed("player") or 2.6
                            local exp = start + dur
                            if exp > now and start > 0 then
                                return dur, exp
                            end
                            return dur, now + dur
                        end""",
                        "customText": r"""function()
                            if _G.PWHUD_GetSwing then _G.PWHUD_GetSwing() end
                            local now = GetTime()
                            local sw = _G.PWHUD_Swing
                            local remStr = ""
                            if sw and sw.mhStart and sw.mhStart > 0 then
                                local rem = (sw.mhStart + (sw.mhDur or 2.6)) - now
                                if rem > 0 then remStr = string.format("%.1fs", rem) end
                            end
                            if sw and sw.hsQueued then
                                return string.format("|cFFFFD700[HS QUEUED] %s|r", remStr)
                            elseif sw and sw.cleaveQueued then
                                return string.format("|cFF00FF00[CLEAVE QUEUED] %s|r", remStr)
                            end
                            return remStr
                        end"""
                    },
                    "untrigger": {"type": "custom", "custom": "function() return false end"}
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=9, y_offset=0),
            ],
        },
        # Rotational Bar - Queue Glow (Retroilluminazione additiva quando HS o Cleave è accodato)
        {
            "id": "Rotational Bar - Queue Glow",
            "uid": "PWHUD_ROTCENTER_GLOW",
            "parent": "15 - Rotational Bar",
            "regionType": "texture",
            "internalVersion": 90,
            "xOffset": 0,
            "yOffset": 0,
            "width": 278,
            "height": 7,
            "texture": TEXTURE_WHITE8X8,
            "color": [1.0, 0.84, 0.0, 0.35],
            "selfPoint": "CENTER",
            "anchorPoint": "CENTER",
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "custom": r"""function()
                            local isHS = IsCurrentSpell(47450) or IsCurrentSpell("Heroic Strike") or IsCurrentSpell("Colpo Eroico")
                            local isCL = IsCurrentSpell(47520) or IsCurrentSpell("Cleave") or IsCurrentSpell("Fendente")
                            return (isHS or isCL)
                        end""",
                    },
                    "untrigger": {"type": "custom", "custom": "function() return false end"}
                },
                "activeTriggerMode": -10,
            },
            "conditions": [
                {
                    "check": {"trigger": 1, "variable": "show", "value": 1},
                    "changes": [
                        {"property": "color", "value": [1.0, 0.84, 0.0, 0.45]}
                    ]
                }
            ],
        },
    ]
