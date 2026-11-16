"""
Modulo Componente: 19 - Sunder Armor Tracker warTank
===================================================
Gestisce il monitoraggio del debuff Sunder Armor / Expose Armor sul bersaglio corrente:
- Nome univoco: '19 - Sunder Armor Tracker warTank' (previene conflitti/suffisso ' 2' con Fury Warrior o altre classi).
- Posizione: xOffset = 160, yOffset = -7 (sul lato destro rispetto alla barra centrale, 32x32px).
- Traccia:
  * Sunder Armor (Warrior all-specs: 47467, 25225, 11597, 7386, 485, 7340).
  * Expose Armor (Rogue all-specs: 48669, 11198, 11197, 8650, 8649, 8647).
  * Acid Spit (Hunter Exotic Worm: 55754, 55753, 55752, 55751, 55750, 55749, 55748, 55747).
- Segnalazione intelligente 1:1 identica a Fury Warrior:
  * %c1 (INNER_BOTTOM, font 10): timer esatto di scadenza (es. 27s) o 'OFF' in rosso quando mancante in combat.
  * %c2 (INNER_TOP, font 12, y=-1): stack count ('x5' in verde, 'x1'-'x4' in bianco) o 'EA' in ciano.
  * customIcon: commuta dinamicamente all'icona di Expose Armor se presente sul bersaglio.
  * customDuration & customStacks per animazione swipe coerente.
"""
from builder.core.helpers import make_subtext


def build_sunder_auras() -> list[dict]:
    """Costruisce e restituisce l'aura del componente Sunder Armor Tracker warTank."""
    sunder_events = "UNIT_AURA,PLAYER_TARGET_CHANGED,PLAYER_REGEN_DISABLED,PLAYER_REGEN_ENABLED,PLAYER_ENTERING_WORLD"

    return [
        {
            "id": "19 - Sunder Armor Tracker warTank",
            "uid": "PWHUD_SUNDER_TRACKER",
            "parent": "Class Warrior (Protection)",
            "regionType": "icon",
            "internalVersion": 90,
            "width": 32,
            "height": 32,
            "xOffset": 160,
            "yOffset": -7,
            "displayIcon": "Interface\\Icons\\ability_warrior_sunder",
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
        if spellId == 47467 or spellId == 25225 or spellId == 11597 or spellId == 7386 or spellId == 485 or spellId == 7340 or name == "Sunder Armor" or name == "Fendente d'Armatura" then
            sunderCount = (count and count > 0) and count or 1
            if exp and exp > 0 then sunderRem = exp - now end
            break
        elseif spellId == 8647 or spellId == 8649 or spellId == 8650 or spellId == 11197 or spellId == 11198 or spellId == 48669 or name == "Expose Armor" or name == "Armatura Esclusa" then
            isExpose = true
            if exp and exp > 0 then sunderRem = exp - now end
            break
        elseif spellId == 55754 or spellId == 55753 or spellId == 55752 or spellId == 55751 or spellId == 55750 or spellId == 55749 or spellId == 55748 or spellId == 55747 or name == "Acid Spit" or name == "Sputo Acido" then
            isExpose = true
            if exp and exp > 0 then sunderRem = exp - now end
            break
        end
    end

    local timerText = ""
    local centerText = ""

    if isExpose then
        centerText = "|cFF00FFFFEA|r"
        if sunderRem > 0.1 then
            timerText = string.format("%.0fs", sunderRem)
        end
    elseif sunderCount > 0 then
        local stackColor = (sunderCount >= 5) and "|cFF00FF00" or "|cFFFFFFFF"
        centerText = string.format("%sx%d|r", stackColor, sunderCount)
        if sunderRem > 0.1 then
            timerText = string.format("%.0fs", sunderRem)
        end
    else
        -- Solo 'OFF' in rosso alla base quando manca Sunder Armor (nessuna scritta al centro)
        timerText = "|cFFFF0000OFF|r"
        centerText = ""
    end

    return timerText, centerText
end""",
            "subRegions": [
                {"type": "subbackground"},
                # 1. Timer / Status alla base (%c1): timer esatto (es. 27s) o 'OFF' in rosso quando mancante
                make_subtext("%c1", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=10, y_offset=0),
                # 2. Cariche al centro (%c2): cariche centrate (x1, x2, x3, x4, x5 o EA)
                make_subtext("%c2", justify="CENTER", anchor_point="INNER_TOP", font_size=12, y_offset=-1),
            ],
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "events": sunder_events,
                        "custom": r"""function(event, ...)
    if not UnitExists("target") or UnitIsFriend("player", "target") or UnitIsDead("target") then
        return false
    end
    local inCombat = UnitAffectingCombat("player")
    local found = false
    for i = 1, 40 do
        local name, _, _, _, _, _, _, _, _, _, spellId = UnitDebuff("target", i)
        if not name then break end
        if spellId == 47467 or spellId == 25225 or spellId == 11597 or spellId == 7386 or spellId == 485 or spellId == 7340 or name == "Sunder Armor" or name == "Fendente d'Armatura"
           or spellId == 8647 or spellId == 8649 or spellId == 8650 or spellId == 11197 or spellId == 11198 or spellId == 48669 or name == "Expose Armor" or name == "Armatura Esclusa"
           or spellId == 55754 or spellId == 55753 or spellId == 55752 or spellId == 55751 or spellId == 55750 or spellId == 55749 or spellId == 55748 or spellId == 55747 or name == "Acid Spit" or name == "Sputo Acido" then
            found = true
            break
        end
    end
    if found or inCombat then
        return true
    end
    return false
end""",
                        "customDuration": r"""function()
    if not UnitExists("target") or UnitIsFriend("player", "target") or UnitIsDead("target") then return 0, 0 end
    for i = 1, 40 do
        local name, _, _, _, _, dur, exp, _, _, _, spellId = UnitDebuff("target", i)
        if not name then break end
        if spellId == 47467 or spellId == 25225 or spellId == 11597 or spellId == 7386 or spellId == 485 or spellId == 7340 or name == "Sunder Armor" or name == "Fendente d'Armatura"
           or spellId == 8647 or spellId == 8649 or spellId == 8650 or spellId == 11197 or spellId == 11198 or spellId == 48669 or name == "Expose Armor" or name == "Armatura Esclusa"
           or spellId == 55754 or spellId == 55753 or spellId == 55752 or spellId == 55751 or spellId == 55750 or spellId == 55749 or spellId == 55748 or spellId == 55747 or name == "Acid Spit" or name == "Sputo Acido" then
            if dur and dur > 0 and exp and exp > 0 then
                return dur, exp
            end
        end
    end
    return 0, 0
end""",
                        "customStacks": r"""function()
    if not UnitExists("target") or UnitIsFriend("player", "target") or UnitIsDead("target") then return 0 end
    for i = 1, 40 do
        local name, _, _, count, _, _, _, _, _, _, spellId = UnitDebuff("target", i)
        if not name then break end
        if spellId == 47467 or spellId == 25225 or spellId == 11597 or spellId == 7386 or spellId == 485 or spellId == 7340 or name == "Sunder Armor" or name == "Fendente d'Armatura" then
            return (count and count > 0) and count or 1
        end
    end
    return 0
end""",
                        "customIcon": r"""function()
    if UnitExists("target") and not UnitIsFriend("player", "target") then
        for i = 1, 40 do
            local name, _, icon, _, _, _, _, _, _, _, spellId = UnitDebuff("target", i)
            if not name then break end
            if spellId == 8647 or spellId == 8649 or spellId == 8650 or spellId == 11197 or spellId == 11198 or spellId == 48669 or name == "Expose Armor" or name == "Armatura Esclusa" then
                return icon or (GetSpellInfo and select(3, GetSpellInfo(8647))) or "Interface\\Icons\\Ability_Warrior_Riposte"
            elseif spellId == 47467 or spellId == 25225 or spellId == 11597 or spellId == 7386 or spellId == 485 or spellId == 7340 or name == "Sunder Armor" or name == "Fendente d'Armatura" then
                return icon or (GetSpellInfo and select(3, GetSpellInfo(7386))) or "Interface\\Icons\\ability_warrior_sunder"
            end
        end
    end
    return (GetSpellInfo and select(3, GetSpellInfo(7386))) or (GetSpellInfo and select(3, GetSpellInfo(47467))) or "Interface\\Icons\\ability_warrior_sunder"
end""",
                    },
                    "untrigger": {
                        "custom": r"""function(event, ...)
    if not UnitExists("target") or UnitIsFriend("player", "target") or UnitIsDead("target") then
        return true
    end
    local inCombat = UnitAffectingCombat("player")
    local found = false
    for i = 1, 40 do
        local name, _, _, _, _, _, _, _, _, _, spellId = UnitDebuff("target", i)
        if not name then break end
        if spellId == 47467 or spellId == 25225 or spellId == 11597 or spellId == 7386 or spellId == 485 or spellId == 7340 or name == "Sunder Armor" or name == "Fendente d'Armatura"
           or spellId == 8647 or spellId == 8649 or spellId == 8650 or spellId == 11197 or spellId == 11198 or spellId == 48669 or name == "Expose Armor" or name == "Armatura Esclusa"
           or spellId == 55754 or spellId == 55753 or spellId == 55752 or spellId == 55751 or spellId == 55750 or spellId == 55749 or spellId == 55748 or spellId == 55747 or name == "Acid Spit" or name == "Sputo Acido" then
            found = true
            break
        end
    end
    return not (found or inCombat)
end"""
                    }
                },
                "activeTriggerMode": -10,
            },
        },
    ]
