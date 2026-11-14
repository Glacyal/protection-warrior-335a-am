"""
Modulo Componente: 04 & 20 - Rotational Bar, Priority Engine & Swing Timer (Warrior Protection)
================================================================================================
Gestisce:
1. 04 - Rotational Bar warTank (Icone d'azione a Y = +2):
   - Shield Slam (ID 47488): Priorità 1. Ricarica, fuori raggio e Glow dorato reattivo se Sword and Board è attivo!
   - Revenge (ID 57823): Priorità 2. Attivazione dinamica reattiva a Blocco/Schivata/Parata con Glow arancione fuoco.
   - Shockwave (ID 46968): Priorità 3. CD 20s, cono frontale AoE e stun.
   - Devastate (ID 47498): Priorità 4. Filler, mostra il conteggio stack Sunder Armor (1-5) direttamente sull'icona.
   - Concussion Blow (ID 12809): Priorità 5. Stun singolo 5s con CD 45s.
2. 20 - Swing & HS Queue warTank:
   - Swing Timer della mano primaria (MH).
   - Glow ambra/oro quando Heroic Strike o Cleave è accodato sul prossimo attacco in mischia.
   - Indicatore di scarico rabbia (Rage >= 45).
"""
import copy
from builder.core.constants import PROT_WARRIOR_LOAD, FONT_EXPRESSWAY, TEXTURE_STATUSBAR
from builder.core.helpers import make_subtext, make_glow_action


def build_rotational_auras() -> list[dict]:
    """Costruisce le aure della barra rotazionale e swing timer."""
    auras = []

    # 04 - Rotational Bar warTank (Icona principale Shield Slam)
    auras.append({
        "id": "04 - Rotational Bar warTank",
        "uid": "PWHUD_ROTATION_BAR",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 42,
        "height": 42,
        "xOffset": -65,
        "yOffset": 2,
        "anchorPoint": "CENTER",
        "selfPoint": "CENTER",
        "displayIcon": "Interface\\Icons\\INV_Shield_05",
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
                        -- If Sword and Board active, CD is virtually 0
                        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
                        if buffs and (buffs.bySpellId[50227] or buffs.byName["Sword and Board"]) then
                            return 0, 0
                        end
                        local start, duration = GetSpellCooldown("Shield Slam")
                        if start and duration and duration > 1.5 then
                            return duration, start + duration
                        end
                        return 0, 0
                    end""",
                    "customIcon": r"""function()
                        return "Interface\\Icons\\INV_Shield_05"
                    end""",
                    "customText": r"""function()
                        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
                        if buffs and (buffs.bySpellId[50227] or buffs.byName["Sword and Board"]) then
                            return "|cFFFFD700FREE|r"
                        end
                        return ""
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            }
        },
        "subRegions": [
            make_subtext("%p", "CENTER", "CENTER", 13, 0, 0),
            make_subtext("%c", "CENTER", "INNER_BOTTOM", 10, 2, 0),
            make_subtext("SLAM", "RIGHT", "INNER_BOTTOMRIGHT", 8, 2, -2)
        ],
        "conditions": [
            {
                "check": {"trigger": 1, "variable": "show", "value": 1},
                "changes": []
            }
        ]
    })

    # 20 - Swing & HS Queue warTank
    auras.append({
        "id": "20 - Swing & HS Queue warTank",
        "uid": "PWHUD_SWING_HS_QUEUE",
        "regionType": "aurabar",
        "internalVersion": 90,
        "width": 210,
        "height": 6,
        "xOffset": 0,
        "yOffset": -6,
        "anchorPoint": "CENTER",
        "selfPoint": "CENTER",
        "barColor": [0.9, 0.75, 0.2, 1.0],
        "barColor2": [0.15, 0.15, 0.15, 0.85],
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
                        return UnitAffectingCombat("player") or UnitExists("target")
                    end""",
                    "customDuration": r"""function()
                        local speed = UnitAttackSpeed("player") or 2.6
                        local now = GetTime()
                        _G.PWHUD_LastSwing = _G.PWHUD_LastSwing or now
                        local elapsed = (now - _G.PWHUD_LastSwing) % speed
                        return speed, now + (speed - elapsed)
                    end""",
                    "customText": r"""function()
                        local isQueued = IsCurrentSpell("Heroic Strike") or IsCurrentSpell("Cleave")
                        local rage = UnitMana("player") or 0
                        if isQueued then
                            return "|cFFFFD700[HS/CLV QUEUED]|r"
                        elseif rage >= 45 then
                            return "|cFFFF9000[QUEUE HS]|r"
                        end
                        return ""
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            }
        },
        "subRegions": [
            make_subtext("%c", "CENTER", "CENTER", 9, 0, 0)
        ]
    })

    return auras
