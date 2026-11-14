"""
Modulo Componente: 06 - Taunt & Threat Management (Warrior Protection)
======================================================================
Gestisce:
1. 06 - Taunt & Threat warTank:
   - Monitoraggio del tempo di ricarica di Taunt (ID 355, 8s CD).
   - Indicatore di disponibilità di Mocking Blow (ID 694) e Challenging Shout (ID 1161).
   - Allarme immediato in caso di Taunt Missed o Resisted per intervenire all'istante!
"""
import copy
from builder.core.constants import PROT_WARRIOR_LOAD, FONT_EXPRESSWAY
from builder.core.helpers import make_subtext, make_glow_action


def build_taunt_auras() -> list[dict]:
    """Costruisce le aure dedicate a Taunt e gestione aggro."""
    auras = []

    # 06 - Taunt & Threat warTank
    auras.append({
        "id": "06 - Taunt & Threat warTank",
        "uid": "PWHUD_TAUNT_THREAT",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 38,
        "height": 38,
        "xOffset": -25,
        "yOffset": 45,
        "anchorPoint": "CENTER",
        "selfPoint": "CENTER",
        "displayIcon": "Interface\\Icons\\Spell_Nature_Reincarnation",
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
                        local start, duration = GetSpellCooldown("Taunt")
                        if start and duration and duration > 1.5 then
                            return duration, start + duration
                        end
                        return 0, 0
                    end""",
                    "customIcon": r"""function()
                        return "Interface\\Icons\\Spell_Nature_Reincarnation"
                    end""",
                    "customText": r"""function()
                        local start, duration = GetSpellCooldown("Taunt")
                        if start and duration and duration > 1.5 then
                            local rem = (start + duration) - GetTime()
                            return string.format("%.1fs", rem)
                        end
                        return "|cFF00FF00READY|r"
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            }
        },
        "subRegions": [
            make_subtext("%c", "CENTER", "INNER_BOTTOM", 9, 2, 0),
            make_subtext("TAUNT", "RIGHT", "INNER_BOTTOMRIGHT", 8, 2, -2)
        ]
    })

    return auras
