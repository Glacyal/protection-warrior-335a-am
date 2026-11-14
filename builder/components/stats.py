"""
Modulo Componente: 10 - Stats Panel warTank (Warrior Protection)
================================================================
Pannello informativo avanzato a Y = -120 con statistiche tanking real-time WotLK 3.3.5a:
1. Difesa & Immunità Critici: Skill Difesa reale vs Cap 540 (Boss Raid Lv.83).
2. Combat Table Coverage (CTC): Schivata% + Parata% + Blocco% + Miss% (Soglia uncrushable/full block).
3. Armatura & Riduzione Danno Fisico % (Armor DR%).
4. Shield Block Value (SBV): Valore di blocco scudo (danno e threat di Shield Slam).
5. Hit & Expertise: Hit % (Cap 8% / 263 rating) e Perizia (Soft Cap 26 / 214 rating).
6. Effective Health Pool (EHP): Vita massima effettiva ponderata con l'assorbimento dell'armatura.
"""
import copy
from builder.core.constants import PROT_WARRIOR_LOAD, FONT_EXPRESSWAY, TEXTURE_STATUSBAR
from builder.core.helpers import make_subtext


def build_stats_auras() -> list[dict]:
    """Costruisce l'aura per il pannello statistiche tank."""
    auras = []

    # 10 - Stats Panel warTank
    auras.append({
        "id": "10 - Stats Panel warTank",
        "uid": "PWHUD_STATS_PANEL",
        "regionType": "aurabar",
        "internalVersion": 90,
        "width": 210,
        "height": 26,
        "xOffset": 0,
        "yOffset": -120,
        "anchorPoint": "CENTER",
        "selfPoint": "CENTER",
        "barColor": [0.12, 0.16, 0.22, 0.90],
        "barColor2": [0.06, 0.08, 0.12, 0.95],
        "texture": TEXTURE_STATUSBAR,
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
                        return 0, 0
                    end""",
                    "customText": r"""function()
                        local st = _G.PWHUD_GetTankStats and _G.PWHUD_GetTankStats()
                        if not st then return "" end

                        local defColor = st.isCritImmune and "|cFF40FF40" or "|cFFFF2020"
                        local ctcColor = (st.ctc >= 102.4) and "|cFF00FFFF" or "|cFFFFD700"

                        local line1 = string.format("%sDEF: %d/540|r  %sCTC: %.1f%%|r", defColor, st.defense, ctcColor, st.ctc)
                        local line2 = string.format("|cFFFFFFFFARM: %.1fk (%.1f%% DR)|r  |cFF80D0FFSBV: %d|r", st.armor / 1000, st.armorDR, st.sbv)
                        local line3 = string.format("|cFFFFA000HIT: %.1f%%|r  |cFFFFCC00EXP: %d/26|r  |cFF20FF20EHP: %.0fk|r", st.hitBonus, st.expertise, st.ehp / 1000)

                        return string.format("%s\n%s\n%s", line1, line2, line3)
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            }
        },
        "subRegions": [
            make_subtext("%c", "CENTER", "CENTER", 8, 0, 0, {
                "text_justify": "CENTER"
            })
        ]
    })

    return auras
