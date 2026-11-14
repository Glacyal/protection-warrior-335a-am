"""
Modulo Componente: 19 - Sunder Armor Tracker
============================================
Gestisce il monitoraggio del debuff Sunder Armor / Expose Armor sul bersaglio corrente:
- Posizione: xOffset = 160, yOffset = -7 (sul lato destro rispetto alla barra centrale).
- Traccia:
  * Conteggio cariche (da 1 a 5 cariche, stack count %s).
  * Conto alla rovescia di scadenza (%p o timer formattato).
  * Segnalazione intelligente:
    - Se presenti 5 cariche: stack count centrato 'x5' in verde.
    - Se presente Expose Armor del Ladro: etichetta centrata 'EA' in ciano per non sovrascrivere.
    - Se mancante su target nemico: allerta rossa 'OFF' posizionata alla base del riquadro.
    - Timer di scadenza numerico centrato alla base, cariche centrate.
"""
from builder.core.helpers import make_subtext


def build_sunder_auras() -> list[dict]:
    """Costruisce e restituisce l'aura del componente Sunder Armor Tracker."""
    sunder_events = "UNIT_AURA,PLAYER_TARGET_CHANGED,PLAYER_REGEN_DISABLED,PLAYER_REGEN_ENABLED,PLAYER_ENTERING_WORLD"

    return [
        {
            "id": "19 - Sunder Armor Tracker",
            "uid": "PWHUD_SUNDER_TRACKER",
            "parent": "Class Warrior (Protection)",
            "regionType": "icon",
            "internalVersion": 90,
            "width": 32,
            "height": 32,
            "xOffset": 160,
            "yOffset": -7,
            "displayIcon": "Interface\\Icons\\Ability_Warrior_Sunder",
            "auto": False,
            "color": [1, 1, 1, 1],
            "cooldown": True,
            "cooldownSwipe": True,
            "cooldownEdge": True,
            "cooldownTextDisabled": True,
            "customTextUpdate": "update",
            "customText": r"""function()
                if not UnitExists("target") or UnitIsFriend("player", "target") or UnitIsDead("target") then
                    return "", ""
                end
                local sunderCount = 0
                local isExpose = false
                local sunderRem = 0
                local now = GetTime()
                for i = 1, 40 do
                    local name, _, _, count, _, dur, exp, _, _, _, spellId = UnitDebuff("target", i)
                    if not name then break end
                    if spellId == 47437 or spellId == 7386 or spellId == 11597 or name == "Sunder Armor" or name == "Fendente d'Armatura" then
                        sunderCount = (count and count > 0) and count or 1
                        if exp and exp > 0 then sunderRem = exp - now end
                        break
                    elseif spellId == 8647 or spellId == 48669 or name == "Expose Armor" or name == "Armatura Esclusa" then
                        isExpose = true
                        if exp and exp > 0 then sunderRem = exp - now end
                        break
                    end
                end

                if isExpose then
                    return "|cFF00FFFFEA|r", (sunderRem > 0 and string.format("%.0fs", sunderRem) or "")
                elseif sunderCount == 5 then
                    return "|cFF00FF00x5|r", (sunderRem > 0 and string.format("%.0fs", sunderRem) or "")
                elseif sunderCount > 0 then
                    return string.format("|cFFFFFF00x%d|r", sunderCount), (sunderRem > 0 and string.format("%.0fs", sunderRem) or "")
                else
                    return "|cFFFF2020OFF|r", ""
                end
            end""",
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "event",
                        "events": sunder_events,
                        "custom": r"""function(event, ...)
                            return UnitExists("target") and not UnitIsFriend("player", "target") and not UnitIsDead("target")
                        end""",
                        "customDuration": r"""function()
                            local now = GetTime()
                            for i = 1, 40 do
                                local name, _, _, _, _, dur, exp, _, _, _, spellId = UnitDebuff("target", i)
                                if not name then break end
                                if spellId == 47437 or spellId == 7386 or spellId == 8647 or name == "Sunder Armor" or name == "Expose Armor" then
                                    if exp and exp > 0 then
                                        return dur or 30, exp
                                    end
                                end
                            end
                            return 0, 0
                        end"""
                    },
                    "untrigger": {"type": "custom", "custom": "function(event, ...) return false end"}
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                make_subtext("%c1", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=10, y_offset=0),
                make_subtext("%c2", justify="CENTER", anchor_point="CENTER", font_size=12, y_offset=0),
            ],
        }
    ]
