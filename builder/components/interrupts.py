"""
Modulo Componente: 02 & 17 - Kick & Spell Reflect Advisor (Warrior Protection)
=============================================================================
Gestisce:
1. 02 - Kick Advisor warTank:
   - Monitoraggio real-time del cast del target (UNIT_SPELLCAST_START/CHANNEL).
   - Analisi di interruzione nativa (notInterruptible check 3.3.5a).
   - Suggerimento intelligente dell'abilità ottimale in base alla postura e ai cooldown:
     * Postura Difensiva / Battaglia + Scudo: "KICK: SHIELD BASH" (ID 72)
     * Postura Berserker: "KICK: PUMMEL" (ID 6552)
     * Shield Bash in CD ma Pummel pronto: "STANCE DANCE -> PUMMEL"
     * Se kick fisici in CD: "STUN: CONCUSSION BLOW" o "STUN: SHOCKWAVE"
     * Se immune ai kick (cast protetto): "IMMUNE TO KICK (REFLECT / CD)"
2. 17 - Spell Reflect Advisor warTank:
   - Monitoraggio dello stato di Spell Reflection (ID 23920, buff attivo 5s o cooldown pronto).
"""
import copy
from builder.core.constants import PROT_WARRIOR_LOAD, FONT_EXPRESSWAY
from builder.core.helpers import make_subtext, make_glow_action


def build_interrupt_auras() -> list[dict]:
    """Costruisce le aure per l'interruzione intelligente dei cast nemici."""
    auras = []

    # 02 - Kick Advisor warTank
    auras.append({
        "id": "02 - Kick Advisor warTank",
        "uid": "PWHUD_KICK_ADVISOR",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 50,
        "height": 50,
        "xOffset": 0,
        "yOffset": 2,
        "anchorPoint": "CENTER",
        "selfPoint": "CENTER",
        "displayIcon": "Interface\\Icons\\Ability_Warrior_ShieldBash",
        "load": copy.deepcopy(PROT_WARRIOR_LOAD),
        "triggers": {
            "1": {
                "trigger": {
                    "type": "custom",
                    "custom_type": "status",
                    "check": "update",
                    "custom": r"""function()
                        if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                        local ki = _G.PWHUD_GetKickInfo and _G.PWHUD_GetKickInfo()
                        return (ki ~= nil)
                    end""",
                    "customDuration": r"""function()
                        local ki = _G.PWHUD_GetKickInfo and _G.PWHUD_GetKickInfo()
                        if ki and ki.remaining > 0 then
                            return ki.remaining, GetTime() + ki.remaining
                        end
                        return 0, 0
                    end""",
                    "customIcon": r"""function()
                        local ki = _G.PWHUD_GetKickInfo and _G.PWHUD_GetKickInfo()
                        if ki then return ki.recommendedIcon end
                        return "Interface\\Icons\\Ability_Warrior_ShieldBash"
                    end""",
                    "customText": r"""function()
                        local ki = _G.PWHUD_GetKickInfo and _G.PWHUD_GetKickInfo()
                        if ki then
                            if ki.notInterruptible then
                                return "|cFF808080IMMUNE TO KICK!\nREFLECT / CD|r"
                            else
                                return string.format("|cFF00E0FF%s\n[%.1fs]|r", ki.recommended, ki.remaining)
                            end
                        end
                        return ""
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            }
        },
        "subRegions": [
            make_subtext("%c", "CENTER", "INNER_TOP", 11, 20, 0, {
                "text_color": [0.0, 0.9, 1.0, 1.0]
            }),
            make_subtext("%p", "CENTER", "CENTER", 14, 0, 0)
        ],
        "conditions": [
            {
                "check": {"trigger": 1, "variable": "show", "value": 1},
                "changes": [
                    {"property": "glow", "value": True}
                ]
            }
        ]
    })

    # 17 - Spell Reflect Advisor warTank
    auras.append({
        "id": "17 - Spell Reflect Advisor warTank",
        "uid": "PWHUD_SPELL_REFLECT",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 36,
        "height": 36,
        "xOffset": 150,
        "yOffset": -45,
        "anchorPoint": "CENTER",
        "selfPoint": "CENTER",
        "displayIcon": "Interface\\Icons\\Ability_Warrior_ShieldReflection",
        "load": copy.deepcopy(PROT_WARRIOR_LOAD),
        "triggers": {
            "1": {
                "trigger": {
                    "type": "custom",
                    "custom_type": "status",
                    "check": "update",
                    "custom": r"""function()
                        if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                        return true
                    end""",
                    "customDuration": r"""function()
                        -- Check if buff active on player
                        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
                        local b = buffs and (buffs.bySpellId[23920] or buffs.byName["Spell Reflection"])
                        if b and b.duration and b.duration > 0 then
                            return b.duration, b.expirationTime
                        end
                        -- Cooldown
                        local start, duration = GetSpellCooldown("Spell Reflection")
                        if start and duration and duration > 1.5 then
                            return duration, start + duration
                        end
                        return 0, 0
                    end""",
                    "customIcon": r"""function()
                        return "Interface\\Icons\\Ability_Warrior_ShieldReflection"
                    end""",
                    "customText": r"""function()
                        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
                        local b = buffs and (buffs.bySpellId[23920] or buffs.byName["Spell Reflection"])
                        if b then
                            return "|cFF00FF00ACTIVE|r"
                        end
                        return ""
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            }
        },
        "subRegions": [
            make_subtext("%p", "CENTER", "CENTER", 12, 0, 0),
            make_subtext("%c", "CENTER", "INNER_BOTTOM", 9, 2, 0)
        ]
    })

    return auras
