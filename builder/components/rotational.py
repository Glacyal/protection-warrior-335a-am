"""
Modulo Componente: 15 - Rotational Bar warTank (Static Queue Indicator for Heroic Strike & Cleave)
==================================================================================================
Gestisce la barra orizzontale centrale a y = -7 (278x7px):
1. Background Frame (278x7px, scuro semitrasparente).
2. Base Bar (274x5px, barra statica a piena larghezza con texture Warrior copper/bronze).
   - Occupa l'intero spazio assegnato senza animazione di scorrimento/swipe.
   - Non visualizza alcun testo o conto alla rovescia del tempo rimanente.
3. Rotational Bar - HS Queued warTank (274x5px):
   - Rileva in tempo reale se Heroic Strike è accodato sul prossimo attacco in mischia tramite IsCurrentSpell().
   - Utilizza check="update" (valutazione OnUpdate ad ogni frame) e risoluzione universale del nome tramite GetSpellInfo(47450).
   - Retroilluminazione dinamica Gold (1.0, 0.84, 0.0) e Pixel Glow dedicato LibCustomGlow-1.0 / do_glow nativo.
4. Rotational Bar - Cleave Queued warTank (274x5px):
   - Rileva in tempo reale se Cleave è accodato sul prossimo attacco in mischia tramite IsCurrentSpell().
   - Utilizza check="update" e risoluzione del nome tramite GetSpellInfo(47520).
   - Retroilluminazione dinamica Verde Smeraldo (0.1, 0.95, 0.2) e Pixel Glow dedicato LibCustomGlow-1.0 / do_glow nativo.
"""
from builder.core.constants import TEXTURE_STATUSBAR, TEXTURE_WHITE8X8
from builder.core.helpers import make_glow_action


def build_rotational_auras() -> list[dict]:
    """
    Costruisce e restituisce le aure del gruppo Rotational Bar:
    - 15 - Rotational Bar warTank (Group 278x7px a y = -7)
    - Rotational Bar - Background warTank
    - Rotational Bar - Base Bar warTank
    - Rotational Bar - HS Queued warTank
    - Rotational Bar - Cleave Queued warTank
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
                "init": {},
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
        # Base Bar (274x5px statica, piena larghezza, nessun timer, nessuno scorrimento)
        {
            "id": "Rotational Bar - Base Bar warTank",
            "uid": "PWHUD_ROTCENTER_BASE",
            "parent": "15 - Rotational Bar warTank",
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
            "subRegions": [
                {"type": "subbackground"},
            ],
        },
        # Rotational Bar - HS Queued (Indicatore dinamico Heroic Strike: barra Oro vibrante + Pixel Glow dorato)
        {
            "id": "Rotational Bar - HS Queued warTank",
            "uid": "PWHUD_ROTCENTER_HSQ",
            "parent": "15 - Rotational Bar warTank",
            "regionType": "texture",
            "internalVersion": 90,
            "xOffset": 0,
            "yOffset": 0,
            "width": 274,
            "height": 5,
            "texture": TEXTURE_STATUSBAR,
            "color": [1.0, 0.84, 0.0, 1.0],
            "selfPoint": "CENTER",
            "anchorPoint": "CENTER",
            "actions": {
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
                            local isHS = (IsCurrentSpell and (IsCurrentSpell(hsName) or IsCurrentSpell("Heroic Strike") or IsCurrentSpell("Colpo Eroico")))
                            return (isHS == 1 or isHS == true)
                        end""",
                    },
                    "untrigger": {
                        "type": "custom",
                        "custom": r"""function()
                            local hsName = _G.PWHUD_HSName
                            if not hsName then
                                hsName = GetSpellInfo(47450) or "Heroic Strike"
                                _G.PWHUD_HSName = hsName
                            end
                            local isHS = (IsCurrentSpell and (IsCurrentSpell(hsName) or IsCurrentSpell("Heroic Strike") or IsCurrentSpell("Colpo Eroico")))
                            return not (isHS == 1 or isHS == true)
                        end""",
                    }
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
            ],
        },
        # Rotational Bar - Cleave Queued (Indicatore dinamico Cleave: barra Verde Smeraldo + Pixel Glow smeraldo)
        {
            "id": "Rotational Bar - Cleave Queued warTank",
            "uid": "PWHUD_ROTCENTER_CLQ",
            "parent": "15 - Rotational Bar warTank",
            "regionType": "texture",
            "internalVersion": 90,
            "xOffset": 0,
            "yOffset": 0,
            "width": 274,
            "height": 5,
            "texture": TEXTURE_STATUSBAR,
            "color": [0.1, 0.95, 0.2, 1.0],
            "selfPoint": "CENTER",
            "anchorPoint": "CENTER",
            "actions": {
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
                            local isCL = (IsCurrentSpell and (IsCurrentSpell(clName) or IsCurrentSpell("Cleave") or IsCurrentSpell("Fendente")))
                            return (isCL == 1 or isCL == true)
                        end""",
                    },
                    "untrigger": {
                        "type": "custom",
                        "custom": r"""function()
                            local clName = _G.PWHUD_CleaveName
                            if not clName then
                                clName = GetSpellInfo(47520) or "Cleave"
                                _G.PWHUD_CleaveName = clName
                            end
                            local isCL = (IsCurrentSpell and (IsCurrentSpell(clName) or IsCurrentSpell("Cleave") or IsCurrentSpell("Fendente")))
                            return not (isCL == 1 or isCL == true)
                        end""",
                    }
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
            ],
        },
    ]
