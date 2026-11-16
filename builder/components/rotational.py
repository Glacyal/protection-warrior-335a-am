"""
Modulo Componente: 15 - Rotational Bar (Static Queue Indicator for Heroic Strike & Cleave)
========================================================================================
Gestisce la barra orizzontale centrale a y = -7 (278x7px):
1. Background Frame (278x7px, scuro semitrasparente).
2. Base Bar (274x5px, barra statica a piena larghezza con texture Warrior copper/bronze).
   - Occupa l'intero spazio assegnato senza animazione di scorrimento/swipe.
   - Non visualizza alcun testo o conto alla rovescia del tempo rimanente.
3. Queue Glow (278x7px, indicatore di accodamento analogo a Fury Warrior):
   - Rileva in tempo reale se Heroic Strike (47450) o Cleave (47520) è accodato tramite IsCurrentSpell().
   - Retroilluminazione additiva con blend mode ADD e Pixel Glow dedicato LibCustomGlow-1.0:
     * Oro (1.0, 0.84, 0.0) per Heroic Strike.
     * Verde Smeraldo (0.1, 0.95, 0.2) per Cleave.
   - Si spegne completamente quando nessuna abilità è accodata.
"""
from builder.core.helpers import make_subtext
from builder.core.constants import TEXTURE_STATUSBAR, TEXTURE_WHITE8X8


def build_rotational_auras() -> list[dict]:
    """
    Costruisce e restituisce le aure del gruppo Rotational Bar:
    - 15 - Rotational Bar (Group 278x7px a y = -7)
    - Rotational Bar - Background
    - Rotational Bar - Base Bar
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
                "Rotational Bar - Base Bar",
                "Rotational Bar - Queue Glow",
            ],
            "actions": {
                "init": {},
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
        # Base Bar (274x5px statica, piena larghezza, nessun timer, nessuno scorrimento)
        {
            "id": "Rotational Bar - Base Bar",
            "uid": "PWHUD_ROTCENTER_BASE",
            "parent": "15 - Rotational Bar",
            "regionType": "texture",
            "internalVersion": 90,
            "xOffset": 0,
            "yOffset": 0,
            "width": 274,
            "height": 5,
            "texture": TEXTURE_STATUSBAR,
            "color": [0.65, 0.35, 0.12, 0.90],
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
        # Rotational Bar - Queue Glow (Overlay dinamico additivo + LibCustomGlow-1.0 Pixel Glow per Heroic Strike / Cleave)
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
            "texture": TEXTURE_STATUSBAR,
            "blendMode": "ADD",
            "color": [1.0, 0.84, 0.0, 0.40],
            "selfPoint": "CENTER",
            "anchorPoint": "CENTER",
            "customTextUpdate": "update",
            "customText": r"""function()
                local isHS = IsCurrentSpell and (IsCurrentSpell(47450) or IsCurrentSpell("Heroic Strike") or IsCurrentSpell("Colpo Eroico"))
                local isCleave = IsCurrentSpell and (IsCurrentSpell(47520) or IsCurrentSpell("Cleave") or IsCurrentSpell("Fendente"))
                local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)
                local glowKey = "PWHUD_ROTCENTER_GLOW"
                local reg = aura_env and aura_env.region
                local tex = reg and (reg.texture or (reg.SetVertexColor and reg))
                if tex and tex.SetBlendMode then tex:SetBlendMode("ADD") end

                if isHS then
                    if aura_env and aura_env.lastQueuedState ~= "HS" then
                        aura_env.lastQueuedState = "HS"
                        if tex and tex.SetVertexColor then tex:SetVertexColor(1.0, 0.84, 0.0, 0.40) end
                        if LCG and reg then LCG.PixelGlow_Start(reg, {1.0, 0.84, 0.0, 1.0}, 8, 0.25, 10, 2, 0, 0, false, glowKey) end
                    end
                elseif isCleave then
                    if aura_env and aura_env.lastQueuedState ~= "CLEAVE" then
                        aura_env.lastQueuedState = "CLEAVE"
                        if tex and tex.SetVertexColor then tex:SetVertexColor(0.1, 0.95, 0.2, 0.40) end
                        if LCG and reg then LCG.PixelGlow_Start(reg, {0.1, 0.95, 0.2, 1.0}, 8, 0.25, 10, 2, 0, 0, false, glowKey) end
                    end
                else
                    if aura_env and aura_env.lastQueuedState ~= "NONE" then
                        aura_env.lastQueuedState = "NONE"
                        if LCG and reg then LCG.PixelGlow_Stop(reg, glowKey) end
                    end
                end
                return ""
            end""",
            "actions": {
                "start": {
                    "do_custom": True,
                    "custom": r"""if aura_env then aura_env.lastQueuedState = nil end
local isHS = IsCurrentSpell and (IsCurrentSpell(47450) or IsCurrentSpell("Heroic Strike") or IsCurrentSpell("Colpo Eroico"))
local isCleave = IsCurrentSpell and (IsCurrentSpell(47520) or IsCurrentSpell("Cleave") or IsCurrentSpell("Fendente"))
local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)
local glowKey = "PWHUD_ROTCENTER_GLOW"
local reg = aura_env and aura_env.region
local tex = reg and (reg.texture or (reg.SetVertexColor and reg))
if tex and tex.SetBlendMode then tex:SetBlendMode("ADD") end
if isHS then
    if aura_env then aura_env.lastQueuedState = "HS" end
    if tex and tex.SetVertexColor then tex:SetVertexColor(1.0, 0.84, 0.0, 0.40) end
    if LCG and reg then LCG.PixelGlow_Start(reg, {1.0, 0.84, 0.0, 1.0}, 8, 0.25, 10, 2, 0, 0, false, glowKey) end
elseif isCleave then
    if aura_env then aura_env.lastQueuedState = "CLEAVE" end
    if tex and tex.SetVertexColor then tex:SetVertexColor(0.1, 0.95, 0.2, 0.40) end
    if LCG and reg then LCG.PixelGlow_Start(reg, {0.1, 0.95, 0.2, 1.0}, 8, 0.25, 10, 2, 0, 0, false, glowKey) end
end""",
                },
                "finish": {
                    "do_custom": True,
                    "custom": r"""if aura_env then aura_env.lastQueuedState = nil end
local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)
if LCG and aura_env and aura_env.region then
    LCG.PixelGlow_Stop(aura_env.region, "PWHUD_ROTCENTER_GLOW")
end""",
                },
            },
            "subRegions": [
                make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=10, y_offset=0, extra_props={"text_color": [0, 0, 0, 0]}),
            ],
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "event",
                        "events": "CURRENT_SPELL_CAST_CHANGED,ACTIONBAR_UPDATE_STATE,START_AUTOREPEAT_SPELL,STOP_AUTOREPEAT_SPELL,UNIT_SPELLCAST_SUCCEEDED,PLAYER_ENTERING_WORLD",
                        "custom": r"""function()
                            local isHS = IsCurrentSpell and (IsCurrentSpell(47450) or IsCurrentSpell("Heroic Strike") or IsCurrentSpell("Colpo Eroico"))
                            local isCleave = IsCurrentSpell and (IsCurrentSpell(47520) or IsCurrentSpell("Cleave") or IsCurrentSpell("Fendente"))
                            return (isHS == true or isHS == 1 or isCleave == true or isCleave == 1)
                        end""",
                    },
                    "untrigger": {
                        "custom": r"""function()
                            local isHS = IsCurrentSpell and (IsCurrentSpell(47450) or IsCurrentSpell("Heroic Strike") or IsCurrentSpell("Colpo Eroico"))
                            local isCleave = IsCurrentSpell and (IsCurrentSpell(47520) or IsCurrentSpell("Cleave") or IsCurrentSpell("Fendente"))
                            return not (isHS or isCleave)
                        end""",
                    }
                },
                "activeTriggerMode": -10,
            },
        },
    ]
