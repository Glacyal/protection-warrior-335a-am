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
2. 16 - Castbar warTank (Gruppo 278x20px a y = +8):
   - Castbar - Target warTank (Aurabar 278x20px, y = 0, inverse = True, scorrimento da destra a sinistra).
     * Priorità assoluta sul cast del player in caso di sovrapposizione.
     * Advisor intelligente: Shield Bash vs Spell Reflection vs Immune.
     * Colori dinamici: Magenta/Viola [0.78, 0.25, 0.95] per Reflect, Ciano [0.0, 0.85, 1.0] per Kick, Grigio [0.55, 0.55, 0.55] per Immune.
     * Dicitura Opzione A: NomeSpell [SHIELD BASH] / NomeSpell [SPELL REFLECTION] / NomeSpell [IMMUNE].
   - Castbar - Player warTank (Aurabar 278x20px, y = 0, inverse = True, scorrimento da destra a sinistra).
     * Mostra lanci/canalizzazioni del giocatore con icona dinamica, soppressione su cast del bersaglio e stop immediato su interruzione.
"""
from builder.core.helpers import make_subtext
from builder.core.constants import (
    TEXTURE_STATUSBAR,
    COLOR_RAGE,
    COLOR_RAGE_DUMP,
    COLOR_RAGE_STARVED,
    COLOR_RAGE_BG,
    COLOR_CASTBAR,
    COLOR_CASTBAR_REFLECT,
    COLOR_CASTBAR_IMMUNE,
    COLOR_CASTBAR_BG,
)


SHARED_CASTBAR_LOGIC_LUA = r"""_G.PWHUD_GetTargetCastInfo = function()
    if not UnitExists("target") or not UnitCanAttack("player", "target") or UnitIsDead("target") then
        return nil
    end

    local spell, rank, displayName, icon, startTime, endTime, isTradeSkill, castID, notInterruptible = UnitCastingInfo("target")
    local isChannel = false
    if not spell then
        local cName, cRank, cText, cTexture, cStart, cEnd, cTrade, cNotInt = UnitChannelInfo("target")
        if cName then
            spell = cName
            displayName = cText
            icon = cTexture
            startTime = cStart
            endTime = cEnd
            isTradeSkill = cTrade
            notInterruptible = cNotInt
            isChannel = true
        end
    end
    if not spell then return nil end

    if not icon and spell and GetSpellTexture then
        icon = GetSpellTexture(spell)
    end

    local now = GetTime()
    local rem = (endTime and (endTime / 1000 - now)) or 0
    local dur = (startTime and endTime and ((endTime - startTime) / 1000)) or 0

    local hasShield = (GetInventoryItemID("player", 17) ~= nil)
    local isTargetingMe = UnitIsUnit("targettarget", "player")

    -- Check Cooldowns
    local sbStart, sbDur = GetSpellCooldown("Shield Bash")
    if not sbStart then sbStart, sbDur = GetSpellCooldown("Colpo di Scudo") end
    if not sbStart then sbStart, sbDur = GetSpellCooldown("Spaccatesta") end
    local sbReady = (sbDur == nil or sbDur <= 1.5 or (sbStart + sbDur <= now))

    local srStart, srDur = GetSpellCooldown("Spell Reflection")
    if not srStart then srStart, srDur = GetSpellCooldown("Riflessione degli Incantesimi") end
    local srReady = (srDur == nil or srDur <= 1.5 or (srStart + srDur <= now))

    local inMelee = (IsSpellInRange and (IsSpellInRange("Shield Bash", "target") == 1 or IsSpellInRange("Colpo di Scudo", "target") == 1 or IsSpellInRange("Spaccatesta", "target") == 1))
    if inMelee == nil or inMelee == false then
        inMelee = CheckInteractDistance("target", 3)
    end

    local res = {
        spell = spell,
        spellName = spell,
        icon = icon or "Interface\\Icons\\Temp",
        startTime = startTime,
        endTime = endTime,
        duration = dur,
        remaining = rem,
        notInterruptible = notInterruptible,
        canKick = not notInterruptible,
        isChannel = isChannel,
        action = "KICKABLE",
        recommended = "SHIELD BASH",
        actionType = "KICK",
    }

    if notInterruptible then
        if isTargetingMe and hasShield and srReady then
            res.action = "SPELL REFLECTION"
            res.recommended = "SPELL REFLECTION"
            res.actionType = "REFLECT"
        else
            res.action = "IMMUNE"
            res.recommended = "IMMUNE"
            res.actionType = "IMMUNE"
        end
        return res
    end

    -- Interruptible spell:
    if isTargetingMe and hasShield and srReady then
        if inMelee and sbReady then
            res.action = "SHIELD BASH / REFLECT"
            res.recommended = "SHIELD BASH"
            res.actionType = "BOTH"
        elseif not inMelee then
            res.action = "SPELL REFLECTION"
            res.recommended = "SPELL REFLECTION"
            res.actionType = "REFLECT"
        elseif sbReady then
            res.action = "SHIELD BASH"
            res.recommended = "SHIELD BASH"
            res.actionType = "KICK"
        else
            res.action = "SPELL REFLECTION"
            res.recommended = "SPELL REFLECTION"
            res.actionType = "REFLECT"
        end
    else
        if inMelee and sbReady and hasShield then
            res.action = "SHIELD BASH"
            res.recommended = "SHIELD BASH"
            res.actionType = "KICK"
        elseif not sbReady and hasShield and srReady and isTargetingMe then
            res.action = "SPELL REFLECTION"
            res.recommended = "SPELL REFLECTION"
            res.actionType = "REFLECT"
        elseif inMelee then
            local pStart, pDur = GetSpellCooldown("Pummel")
            if not pStart then pStart, pDur = GetSpellCooldown("Percossa") end
            if not pStart then pStart, pDur = GetSpellCooldown("Pestone") end
            local pummelReady = (pDur == nil or pDur <= 1.5 or (pStart + pDur <= now))
            if pummelReady then
                res.action = "PUMMEL"
                res.recommended = "PUMMEL"
                res.actionType = "KICK"
            else
                res.action = "STUN / CD"
                res.recommended = "STUN / CD"
                res.actionType = "KICK"
            end
        else
            res.action = "KICKABLE"
            res.recommended = "KICKABLE"
            res.actionType = "KICK"
        end
    end

    return res
end
_G.PWHUD_GetKickInfo = _G.PWHUD_GetTargetCastInfo"""


def build_bars_auras() -> list[dict]:
    """
    Costruisce e restituisce le barre dell'HUD:
    - 14 - Rage Bar warTank (Aurabar 278x14px a y = -20)
    - 16 - Castbar warTank (Gruppo 278x20px a y = +8)
    - Castbar - Target warTank (Aurabar 278x20px, inverse = True, scorrimento dx -> sx)
    - Castbar - Player warTank (Aurabar 278x20px, inverse = True, scorrimento dx -> sx)
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
        # 16 - CASTBAR WARTANK (GRUPPO CONTENITORE 278x20px a y = +8)
        # =====================================================================
        {
            "id": "16 - Castbar warTank",
            "uid": "PWHUD_CASTBAR",
            "parent": "Class Warrior (Protection)",
            "regionType": "group",
            "internalVersion": 90,
            "anchorPoint": "CENTER",
            "selfPoint": "CENTER",
            "xOffset": 0,
            "yOffset": 8,
            "controlledChildren": [
                "Castbar - Target warTank",
                "Castbar - Player warTank",
            ],
            "actions": {
                "init": {
                    "do_custom": True,
                    "custom": SHARED_CASTBAR_LOGIC_LUA,
                },
                "start": {},
                "finish": {},
            },
        },

        # =====================================================================
        # 16a - CASTBAR TARGET (SCORRIMENTO DA DESTRA VERSO SINISTRA - INVERSE)
        # =====================================================================
        {
            "id": "Castbar - Target warTank",
            "uid": "PWHUD_CASTBAR_TARGET",
            "parent": "16 - Castbar warTank",
            "regionType": "aurabar",
            "internalVersion": 90,
            "width": 278,
            "height": 20,
            "xOffset": 0,
            "yOffset": 0,
            "barColor": [0.0, 0.85, 1.0, 1.0],
            "backgroundColor": COLOR_CASTBAR_BG,
            "texture": TEXTURE_STATUSBAR,
            "inverse": True,
            "icon": True,
            "icon_side": "LEFT",
            "iconSource": 0,
            "auto": True,
            "displayIcon": "Interface\\Icons\\Temp",
            "customTextUpdate": "update",
            "customText": r"""function()
                if not _G.PWHUD_GetTargetCastInfo then
                    """ + SHARED_CASTBAR_LOGIC_LUA + r"""
                end
                local ki = _G.PWHUD_GetTargetCastInfo()
                if not ki then return "" end
                local reg = aura_env and aura_env.region
                local bar = reg and (reg.bar or (reg.SetVertexColor and reg))
                if reg and reg.icon and reg.icon.SetTexture and ki.icon then
                    reg.icon:SetTexture(ki.icon)
                end
                if ki.actionType == "REFLECT" then
                    if bar and bar.SetVertexColor then bar:SetVertexColor(0.78, 0.25, 0.95, 1.0) end
                    return string.format("|cFFFF55FF%s [%s]|r", ki.spell, ki.action)
                elseif ki.actionType == "IMMUNE" then
                    if bar and bar.SetVertexColor then bar:SetVertexColor(0.50, 0.50, 0.50, 0.85) end
                    return string.format("|cFF888888%s [%s]|r", ki.spell, ki.action)
                elseif ki.actionType == "BOTH" then
                    if bar and bar.SetVertexColor then bar:SetVertexColor(0.0, 0.85, 1.0, 1.0) end
                    return string.format("|cFF00FFFF%s [%s]|r", ki.spell, ki.action)
                else
                    if bar and bar.SetVertexColor then bar:SetVertexColor(0.0, 0.85, 1.0, 1.0) end
                    return string.format("|cFF00FFFF%s [%s]|r", ki.spell, ki.action)
                end
            end""",
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "custom": r"""function()
                            if not _G.PWHUD_GetTargetCastInfo then
                                """ + SHARED_CASTBAR_LOGIC_LUA + r"""
                            end
                            local ki = _G.PWHUD_GetTargetCastInfo()
                            return (ki ~= nil)
                        end""",
                        "customDuration": r"""function()
                            if not _G.PWHUD_GetTargetCastInfo then
                                """ + SHARED_CASTBAR_LOGIC_LUA + r"""
                            end
                            local ki = _G.PWHUD_GetTargetCastInfo()
                            if ki and ki.duration and ki.endTime then
                                return ki.duration, ki.endTime / 1000
                            end
                            local spell, rank, disp, icon, sTime, eTime = UnitCastingInfo("target")
                            if spell and sTime and eTime then
                                return (eTime - sTime) / 1000, eTime / 1000
                            end
                            local cName, cRank, cText, cTexture, cStart, cEnd = UnitChannelInfo("target")
                            if cName and cStart and cEnd then
                                return (cEnd - cStart) / 1000, cEnd / 1000
                            end
                            return 0, 0
                        end""",
                        "customIcon": r"""function()
                            if not _G.PWHUD_GetTargetCastInfo then
                                """ + SHARED_CASTBAR_LOGIC_LUA + r"""
                            end
                            local ki = _G.PWHUD_GetTargetCastInfo()
                            local icon = ki and ki.icon
                            if not icon then
                                local spell, rank, disp, tIcon = UnitCastingInfo("target")
                                if not spell then
                                    local cName, cRank, cText, cTexture = UnitChannelInfo("target")
                                    if cName then
                                        spell = cName
                                        tIcon = cTexture
                                    end
                                end
                                if not tIcon and spell and GetSpellTexture then
                                    tIcon = GetSpellTexture(spell)
                                end
                                icon = tIcon
                            end
                            if icon and aura_env and aura_env.region and aura_env.region.icon and aura_env.region.icon.SetTexture then
                                aura_env.region.icon:SetTexture(icon)
                            end
                            return icon or "Interface\\Icons\\Temp"
                        end""",
                    },
                    "untrigger": {
                        "type": "custom",
                        "custom": r"""function()
                            if not _G.PWHUD_GetTargetCastInfo then
                                """ + SHARED_CASTBAR_LOGIC_LUA + r"""
                            end
                            local ki = _G.PWHUD_GetTargetCastInfo()
                            return (ki == nil)
                        end"""
                    }
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                make_subtext("%c", justify="LEFT", anchor_point="INNER_LEFT", font_size=11, y_offset=0, x_offset=6),
                make_subtext("%p", justify="RIGHT", anchor_point="INNER_RIGHT", font_size=11, y_offset=0, x_offset=-6),
            ],
        },

        # =====================================================================
        # 16b - CASTBAR PLAYER (SCORRIMENTO DA DESTRA VERSO SINISTRA - INVERSE)
        # =====================================================================
        {
            "id": "Castbar - Player warTank",
            "uid": "PWHUD_CASTBAR_PLAYER",
            "parent": "16 - Castbar warTank",
            "regionType": "aurabar",
            "internalVersion": 90,
            "width": 278,
            "height": 20,
            "xOffset": 0,
            "yOffset": 0,
            "barColor": [0.0, 0.77, 1.0, 1.0],
            "backgroundColor": COLOR_CASTBAR_BG,
            "texture": TEXTURE_STATUSBAR,
            "inverse": True,
            "icon": True,
            "icon_side": "LEFT",
            "iconSource": 0,
            "auto": True,
            "displayIcon": "Interface\\Icons\\Temp",
            "customTextUpdate": "update",
            "customText": r"""function()
                local spell, rank, disp, icon = UnitCastingInfo("player")
                if not spell then
                    local cName, cRank, cText, cTexture = UnitChannelInfo("player")
                    if cName then
                        spell = cName
                        icon = cTexture
                    end
                end
                if not spell then return "" end
                if not icon and GetSpellTexture then
                    icon = GetSpellTexture(spell)
                end
                if icon and aura_env and aura_env.region and aura_env.region.icon and aura_env.region.icon.SetTexture then
                    aura_env.region.icon:SetTexture(icon)
                end
                return spell
            end""",
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "custom": r"""function()
                            -- Priorita 1: Se il target sta castando, sopprime completamente il cast del player
                            local targetSpell = UnitCastingInfo("target")
                            if not targetSpell then
                                targetSpell = UnitChannelInfo("target")
                            end
                            if targetSpell then return false end

                            -- Priorita 2: Cast del giocatore (lancio standard o incanalato)
                            local spell = UnitCastingInfo("player")
                            if not spell then
                                spell = UnitChannelInfo("player")
                            end
                            return (spell ~= nil)
                        end""",
                        "customDuration": r"""function()
                            local targetSpell = UnitCastingInfo("target")
                            if not targetSpell then
                                targetSpell = UnitChannelInfo("target")
                            end
                            if targetSpell then return 0, 0 end

                            local spell, rank, disp, icon, sTime, eTime = UnitCastingInfo("player")
                            if spell and sTime and eTime then
                                return (eTime - sTime) / 1000, eTime / 1000
                            end
                            local cName, cRank, cText, cTexture, csTime, ceTime = UnitChannelInfo("player")
                            if cName and csTime and ceTime then
                                return (ceTime - csTime) / 1000, ceTime / 1000
                            end
                            return 0, 0
                        end""",
                        "customIcon": r"""function()
                            local spell, rank, disp, icon = UnitCastingInfo("player")
                            if not spell then
                                local cName, cRank, cText, cTexture = UnitChannelInfo("player")
                                if cName then
                                    spell = cName
                                    icon = cTexture
                                end
                            end
                            if not icon and spell and GetSpellTexture then
                                icon = GetSpellTexture(spell)
                            end
                            if icon and aura_env and aura_env.region and aura_env.region.icon and aura_env.region.icon.SetTexture then
                                aura_env.region.icon:SetTexture(icon)
                            end
                            return icon or "Interface\\Icons\\Temp"
                        end""",
                    },
                    "untrigger": {
                        "type": "custom",
                        "custom": r"""function()
                            -- Se il target sta castando, nasconde il player cast
                            local targetSpell = UnitCastingInfo("target")
                            if not targetSpell then targetSpell = UnitChannelInfo("target") end
                            if targetSpell then return true end

                            -- Se il player ha interrotto o terminato il cast, untrigger immediato
                            local spell = UnitCastingInfo("player")
                            if not spell then spell = UnitChannelInfo("player") end
                            return (spell == nil)
                        end"""
                    }
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                make_subtext("%c", justify="LEFT", anchor_point="INNER_LEFT", font_size=11, y_offset=0, x_offset=6),
                make_subtext("%p", justify="RIGHT", anchor_point="INNER_RIGHT", font_size=11, y_offset=0, x_offset=-6),
            ],
        },
    ]
