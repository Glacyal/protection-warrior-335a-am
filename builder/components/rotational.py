"""
Modulo Componente: 15 - Rotational Bar warTank (Single Main-Hand Swing Timer & Queued Indicator)
=================================================================================================
Gestisce la barra orizzontale centrale composita a y = -7 (278x7px):
1. Background Frame (278x7px, scuro semitrasparente).
2. Base Bar (274x5px a piena larghezza, aurabar OnUpdate):
   - Monitora e visualizza in tempo reale lo scorrimento del tempo tra un attacco in mischia e il successivo (Swing Timer).
   - In quanto War Tank con arma a una mano e scudo, traccia unicamente la mano primaria (Main Hand).
   - Mostra il timer numerico decimale residuo in secondi (%c, es. 1.8s) centrato sulla barra.
   - Colore base rame/bronzo Warrior ([0.65, 0.35, 0.12, 0.90]).
3. Rotational Bar - HS Queued warTank (274x5px, aurabar OnUpdate sincronizzata):
   - Rileva in tempo reale se Heroic Strike (47450) è accodato sul prossimo attacco in mischia tramite IsCurrentSpell().
   - Barra aurabar sincronizzata in Oro brillante ([1.0, 0.84, 0.0, 1.0]) che prosegue lo scorrimento dello swing timer.
   - Pixel Glow dorato LibCustomGlow-1.0 dedicato (PWHUD_HS_GLOW).
4. Rotational Bar - Cleave Queued warTank (274x5px, aurabar OnUpdate sincronizzata):
   - Rileva in tempo reale se Cleave (47520) è accodato sul prossimo attacco in mischia tramite IsCurrentSpell().
   - Barra aurabar sincronizzata in Verde Smeraldo ([0.1, 0.95, 0.2, 1.0]) che prosegue lo scorrimento dello swing timer.
   - Pixel Glow verde smeraldo LibCustomGlow-1.0 dedicato (PWHUD_CLEAVE_GLOW).
"""
from builder.core.constants import TEXTURE_STATUSBAR, TEXTURE_WHITE8X8
from builder.core.helpers import make_subtext


# =============================================================================
# LOGICA LUA CONDIVISA: SWING TIMER MANO PRIMARIA & HEROIC STRIKE / CLEAVE QUEUING
# =============================================================================
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
            local mhSpeed = select(1, UnitAttackSpeed("player")) or 2.6

            if ev == "SWING_DAMAGE" or ev == "SWING_MISSED" then
                sw.mhStart = now
                sw.mhDur = mhSpeed
            elseif ev == "SPELL_DAMAGE" or ev == "SPELL_MISSED" then
                local sId = select(9, ...)
                local sName = select(10, ...)
                if sId == 47450 or sId == 25286 or sId == 11567 or sId == 11566 or sId == 11565 or sId == 11564 or sId == 1608 or sId == 284 or sId == 285 or sName == "Heroic Strike" or sName == "Colpo Eroico" then
                    sw.mhStart = now
                    sw.mhDur = mhSpeed
                    sw.hsQueued = false
                elseif sId == 47520 or sId == 25231 or sId == 11585 or sId == 11584 or sId == 845 or sName == "Cleave" or sName == "Fendente" then
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
        f:RegisterEvent("START_AUTOREPEAT_SPELL")
        f:RegisterEvent("STOP_AUTOREPEAT_SPELL")
        f:SetScript("OnEvent", function(self, event, ...)
            if event == "COMBAT_LOG_EVENT_UNFILTERED" then
                handleCLEU(...)
            elseif event == "UNIT_ATTACK_SPEED" then
                local u = select(1, ...)
                if u == "player" then
                    local mh = select(1, UnitAttackSpeed("player"))
                    if mh and mh > 0 then sw.mhDur = mh end
                end
            elseif event == "PLAYER_ENTERING_WORLD" then
                local mh = select(1, UnitAttackSpeed("player"))
                if mh and mh > 0 then sw.mhDur = mh end
            end
        end)
    end

    local hsName = _G.PWHUD_HSName
    if not hsName then
        hsName = GetSpellInfo(47450) or "Heroic Strike"
        _G.PWHUD_HSName = hsName
    end
    local clName = _G.PWHUD_CleaveName
    if not clName then
        clName = GetSpellInfo(47520) or "Cleave"
        _G.PWHUD_CleaveName = clName
    end
    local isHS = IsCurrentSpell and (IsCurrentSpell(hsName) or IsCurrentSpell(47450) or IsCurrentSpell("Heroic Strike") or IsCurrentSpell("Colpo Eroico"))
    local isCleave = IsCurrentSpell and (IsCurrentSpell(clName) or IsCurrentSpell(47520) or IsCurrentSpell("Cleave") or IsCurrentSpell("Fendente"))
    sw.hsQueued = (isHS == true or isHS == 1)
    sw.cleaveQueued = (isCleave == true or isCleave == 1)

    return sw
end"""


def build_rotational_auras() -> list[dict]:
    """
    Costruisce e restituisce le 4 aure del gruppo Rotational Bar:
    - 15 - Rotational Bar warTank (Group 278x7px a y = -7)
    - Rotational Bar - Background warTank
    - Rotational Bar - Base Bar warTank (Aurabar 274x5px OnUpdate con scorrimento dello swing timer e timer %c)
    - Rotational Bar - HS Queued warTank (Aurabar 274x5px sincronizzata in Oro con Pixel Glow)
    - Rotational Bar - Cleave Queued warTank (Aurabar 274x5px sincronizzata in Verde Smeraldo con Pixel Glow)
    """
    return [
        # Gruppo contenitore (278x7px a y = -7)
        {
            "id": "15 - Rotational Bar warTank",
            "uid": "PWHUD_ROTCENTER_GRP",
            "parent": "Class Warrior (Protection)",
            "regionType": "group",
            "internalVersion": 90,
            "anchorPoint": "CENTER",
            "selfPoint": "CENTER",
            "xOffset": 0,
            "yOffset": -7,
            "controlledChildren": [
                "Rotational Bar - Background warTank",
                "Rotational Bar - Base Bar warTank",
                "Rotational Bar - HS Queued warTank",
                "Rotational Bar - Cleave Queued warTank",
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
            "id": "Rotational Bar - Background warTank",
            "uid": "PWHUD_ROTCENTER_BG",
            "parent": "15 - Rotational Bar warTank",
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
            "subRegions": [
                {"type": "subbackground"},
            ],
        },
        # Base Bar (274x5px aurabar OnUpdate, swing timer scorrimento mano primaria con timer %c)
        {
            "id": "Rotational Bar - Base Bar warTank",
            "uid": "PWHUD_ROTCENTER_BASE",
            "parent": "15 - Rotational Bar warTank",
            "regionType": "aurabar",
            "internalVersion": 90,
            "xOffset": 0,
            "yOffset": 0,
            "width": 274,
            "height": 5,
            "barColor": [0.65, 0.35, 0.12, 0.90],
            "backgroundColor": [0.12, 0.06, 0.04, 0.60],
            "texture": TEXTURE_STATUSBAR,
            "color": [0.65, 0.35, 0.12, 0.90],
            "inverse": False,
            "selfPoint": "CENTER",
            "anchorPoint": "CENTER",
            "customTextUpdate": "update",
            "customText": r"""function()
                if _G.PWHUD_GetSwing then _G.PWHUD_GetSwing() end
                local now = GetTime()
                local sw = _G.PWHUD_Swing
                if sw and sw.mhStart and sw.mhStart > 0 then
                    local rem = (sw.mhStart + (sw.mhDur or 2.6)) - now
                    if rem > 0 then
                        return string.format("%.1fs", rem)
                    end
                end
                local spd = select(1, UnitAttackSpeed("player")) or 2.6
                return string.format("%.1fs", spd)
            end""",
            "actions": {
                "init": {
                    "do_custom": True,
                    "custom": SHARED_SWING_TIMER_LUA,
                },
                "start": {},
                "finish": {},
            },
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
                            local dur = sw and sw.mhDur or select(1, UnitAttackSpeed("player")) or 2.6
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
                            if sw and sw.mhStart and sw.mhStart > 0 then
                                local rem = (sw.mhStart + (sw.mhDur or 2.6)) - now
                                if rem > 0 then
                                    return string.format("%.1fs", rem)
                                end
                            end
                            local spd = select(1, UnitAttackSpeed("player")) or 2.6
                            return string.format("%.1fs", spd)
                        end""",
                        "customTextUpdate": "update",
                    },
                    "untrigger": {
                        "custom": "function() return false end",
                    }
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=9, y_offset=0, extra_props={"text_color": [1.0, 1.0, 1.0, 1.0]}),
            ],
        },
        # Rotational Bar - HS Queued (Aurabar 274x5px sincronizzata in Oro con Pixel Glow dorato)
        {
            "id": "Rotational Bar - HS Queued warTank",
            "uid": "PWHUD_ROTCENTER_HSQ",
            "parent": "15 - Rotational Bar warTank",
            "regionType": "aurabar",
            "internalVersion": 90,
            "xOffset": 0,
            "yOffset": 0,
            "width": 274,
            "height": 5,
            "barColor": [1.0, 0.84, 0.0, 1.0],
            "backgroundColor": [0.12, 0.06, 0.04, 0.60],
            "texture": TEXTURE_STATUSBAR,
            "color": [1.0, 0.84, 0.0, 1.0],
            "inverse": False,
            "selfPoint": "CENTER",
            "anchorPoint": "CENTER",
            "customTextUpdate": "update",
            "customText": r"""function()
                if _G.PWHUD_GetSwing then _G.PWHUD_GetSwing() end
                local now = GetTime()
                local sw = _G.PWHUD_Swing
                if sw and sw.mhStart and sw.mhStart > 0 then
                    local rem = (sw.mhStart + (sw.mhDur or 2.6)) - now
                    if rem > 0 then
                        return string.format("%.1fs", rem)
                    end
                end
                local spd = select(1, UnitAttackSpeed("player")) or 2.6
                return string.format("%.1fs", spd)
            end""",
            "actions": {
                "init": {
                    "do_custom": True,
                    "custom": SHARED_SWING_TIMER_LUA,
                },
                "start": {
                    "do_custom": True,
                    "custom": r"""local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)
if LCG and aura_env and aura_env.region then
    LCG.PixelGlow_Start(aura_env.region, {1.0, 0.84, 0.0, 1.0}, 8, 0.25, 10, 2, 0, 0, false, "PWHUD_HS_GLOW")
end""",
                    "do_glow": True,
                    "glow_action": "show",
                    "glow_type": "Pixel",
                    "glow_color": [1.0, 0.84, 0.0, 1.0],
                    "glow_lines": 8,
                    "glow_frequency": 0.25,
                    "glow_length": 10,
                    "glow_thickness": 2,
                },
                "finish": {
                    "do_custom": True,
                    "custom": r"""local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)
if LCG and aura_env and aura_env.region then
    LCG.PixelGlow_Stop(aura_env.region, "PWHUD_HS_GLOW")
end""",
                    "do_glow": True,
                    "glow_action": "hide",
                },
            },
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "custom": r"""function()
                            local hsName = _G.PWHUD_HSName
                            if not hsName then
                                hsName = GetSpellInfo(47450) or "Heroic Strike"
                                _G.PWHUD_HSName = hsName
                            end
                            local isHS = (IsCurrentSpell and (IsCurrentSpell(hsName) or IsCurrentSpell(47450) or IsCurrentSpell("Heroic Strike") or IsCurrentSpell("Colpo Eroico")))
                            return (isHS == 1 or isHS == true)
                        end""",
                        "customDuration": r"""function()
                            if _G.PWHUD_GetSwing then _G.PWHUD_GetSwing() end
                            local sw = _G.PWHUD_Swing
                            local now = GetTime()
                            local start = sw and sw.mhStart or 0
                            local dur = sw and sw.mhDur or select(1, UnitAttackSpeed("player")) or 2.6
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
                            if sw and sw.mhStart and sw.mhStart > 0 then
                                local rem = (sw.mhStart + (sw.mhDur or 2.6)) - now
                                if rem > 0 then
                                    return string.format("%.1fs", rem)
                                end
                            end
                            local spd = select(1, UnitAttackSpeed("player")) or 2.6
                            return string.format("%.1fs", spd)
                        end""",
                        "customTextUpdate": "update",
                    },
                    "untrigger": {
                        "type": "custom",
                        "custom": r"""function()
                            local hsName = _G.PWHUD_HSName
                            if not hsName then
                                hsName = GetSpellInfo(47450) or "Heroic Strike"
                                _G.PWHUD_HSName = hsName
                            end
                            local isHS = (IsCurrentSpell and (IsCurrentSpell(hsName) or IsCurrentSpell(47450) or IsCurrentSpell("Heroic Strike") or IsCurrentSpell("Colpo Eroico")))
                            return not (isHS == 1 or isHS == true)
                        end""",
                    }
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=9, y_offset=0, extra_props={"text_color": [1.0, 1.0, 1.0, 1.0]}),
            ],
        },
        # Rotational Bar - Cleave Queued (Aurabar 274x5px sincronizzata in Verde Smeraldo con Pixel Glow)
        {
            "id": "Rotational Bar - Cleave Queued warTank",
            "uid": "PWHUD_ROTCENTER_CLQ",
            "parent": "15 - Rotational Bar warTank",
            "regionType": "aurabar",
            "internalVersion": 90,
            "xOffset": 0,
            "yOffset": 0,
            "width": 274,
            "height": 5,
            "barColor": [0.1, 0.95, 0.2, 1.0],
            "backgroundColor": [0.12, 0.06, 0.04, 0.60],
            "texture": TEXTURE_STATUSBAR,
            "color": [0.1, 0.95, 0.2, 1.0],
            "inverse": False,
            "selfPoint": "CENTER",
            "anchorPoint": "CENTER",
            "customTextUpdate": "update",
            "customText": r"""function()
                if _G.PWHUD_GetSwing then _G.PWHUD_GetSwing() end
                local now = GetTime()
                local sw = _G.PWHUD_Swing
                if sw and sw.mhStart and sw.mhStart > 0 then
                    local rem = (sw.mhStart + (sw.mhDur or 2.6)) - now
                    if rem > 0 then
                        return string.format("%.1fs", rem)
                    end
                end
                local spd = select(1, UnitAttackSpeed("player")) or 2.6
                return string.format("%.1fs", spd)
            end""",
            "actions": {
                "init": {
                    "do_custom": True,
                    "custom": SHARED_SWING_TIMER_LUA,
                },
                "start": {
                    "do_custom": True,
                    "custom": r"""local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)
if LCG and aura_env and aura_env.region then
    LCG.PixelGlow_Start(aura_env.region, {0.1, 0.95, 0.2, 1.0}, 8, 0.25, 10, 2, 0, 0, false, "PWHUD_CLEAVE_GLOW")
end""",
                    "do_glow": True,
                    "glow_action": "show",
                    "glow_type": "Pixel",
                    "glow_color": [0.1, 0.95, 0.2, 1.0],
                    "glow_lines": 8,
                    "glow_frequency": 0.25,
                    "glow_length": 10,
                    "glow_thickness": 2,
                },
                "finish": {
                    "do_custom": True,
                    "custom": r"""local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)
if LCG and aura_env and aura_env.region then
    LCG.PixelGlow_Stop(aura_env.region, "PWHUD_CLEAVE_GLOW")
end""",
                    "do_glow": True,
                    "glow_action": "hide",
                },
            },
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "custom": r"""function()
                            local clName = _G.PWHUD_CleaveName
                            if not clName then
                                clName = GetSpellInfo(47520) or "Cleave"
                                _G.PWHUD_CleaveName = clName
                            end
                            local isCL = (IsCurrentSpell and (IsCurrentSpell(clName) or IsCurrentSpell(47520) or IsCurrentSpell("Cleave") or IsCurrentSpell("Fendente")))
                            return (isCL == 1 or isCL == true)
                        end""",
                        "customDuration": r"""function()
                            if _G.PWHUD_GetSwing then _G.PWHUD_GetSwing() end
                            local sw = _G.PWHUD_Swing
                            local now = GetTime()
                            local start = sw and sw.mhStart or 0
                            local dur = sw and sw.mhDur or select(1, UnitAttackSpeed("player")) or 2.6
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
                            if sw and sw.mhStart and sw.mhStart > 0 then
                                local rem = (sw.mhStart + (sw.mhDur or 2.6)) - now
                                if rem > 0 then
                                    return string.format("%.1fs", rem)
                                end
                            end
                            local spd = select(1, UnitAttackSpeed("player")) or 2.6
                            return string.format("%.1fs", spd)
                        end""",
                        "customTextUpdate": "update",
                    },
                    "untrigger": {
                        "type": "custom",
                        "custom": r"""function()
                            local clName = _G.PWHUD_CleaveName
                            if not clName then
                                clName = GetSpellInfo(47520) or "Cleave"
                                _G.PWHUD_CleaveName = clName
                            end
                            local isCL = (IsCurrentSpell and (IsCurrentSpell(clName) or IsCurrentSpell(47520) or IsCurrentSpell("Cleave") or IsCurrentSpell("Fendente")))
                            return not (isCL == 1 or isCL == true)
                        end""",
                    }
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=9, y_offset=0, extra_props={"text_color": [1.0, 1.0, 1.0, 1.0]}),
            ],
        },
    ]
