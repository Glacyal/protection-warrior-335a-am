"""
Modulo Componente: 01 - Procs warTank (Dynamic Group)
=====================================================
Gestisce la barra orizzontale dinamica superiore dei proc e allarmi (y = 52):
- Crescita orizzontale centrata (space = 6px, icone 34x34px).
- Include rigorosamente i proc chiave del tank e gli allarmi critici:
  1. Sword and Board (Buff 50227: Shield Slam a costo 0 con Pixel Glow dorato e timer 5s)
  2. Revenge Ready (Attivo post Blocco/Schivata/Parata con bordo arancione vivo)
  3. Shield Block Active (Buff 2565: durata attiva 10s con countdown)
  4. Victory Rush (Proc Victorious con countdown durata 20s)
  5. Emergency Low HP Alert (Salute < 35% con allerta visiva del CD difensivo prioritario pronto)
  6. Boss Enrage Alert (Allarme Enrage/Frenzy sul boss)
  7. Tank Buster Alert (Debuff letali: Soul Reaper, Impale >= 2, Gastric Bloat >= 8, Fusion Punch)
"""
from builder.core.helpers import make_subtext, make_glow_action


def build_procs_auras() -> list[dict]:
    """
    Costruisce e restituisce le 8 aure del gruppo dinamico Procs:
    - 01 - Procs warTank (Dynamic Group)
    - Sword and Board, Revenge Ready, Shield Block Active, Victory Rush,
      Emergency Low HP Alert, Boss Enrage Alert, Tank Buster Alert.
    """
    return [
        {
            "id": "01 - Procs warTank",
            "uid": "PWHUD_PROCS_DG",
            "parent": "Class Warrior (Protection)",
            "regionType": "dynamicgroup",
            "internalVersion": 90,
            "grow": "HORIZONTAL",
            "align": "CENTER",
            "space": 6,
            "xOffset": 0,
            "yOffset": 52,
            "controlledChildren": [
                "Sword and Board",
                "Revenge Ready",
                "Shield Block Active",
                "Victory Rush",
                "Emergency Low HP Alert",
                "Boss Enrage Alert",
                "Tank Buster Alert",
            ],
        },
        # 1. Sword and Board (Buff 50227)
        {
            "id": "Sword and Board",
            "uid": "PWHUD_PROC_SAB",
            "parent": "01 - Procs warTank",
            "regionType": "icon",
            "internalVersion": 90,
            "width": 34,
            "height": 34,
            "displayIcon": "Interface\\Icons\\Ability_Warrior_SwordandBoard",
            "auto": True,
            "color": [1, 1, 1, 1],
            "cooldown": True,
            "cooldownSwipe": True,
            "cooldownEdge": True,
            "actions": {
                "start": make_glow_action([1.0, 0.84, 0.0, 1.0]),
                "finish": {"do_glow": True, "glow_action": "hide"},
            },
            "triggers": {
                1: {
                    "trigger": {
                        "type": "aura2",
                        "unit": "player",
                        "auranames": ["Sword and Board", "Spada e Scudo", "50227"],
                        "useName": True,
                        "debuffType": "HELPFUL",
                        "matchesShowOn": "showOnActive",
                    },
                    "untrigger": {}
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                make_subtext("%p", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=12, y_offset=0),
                make_subtext("SLAM", justify="CENTER", anchor_point="CENTER", font_size=9, y_offset=0),
            ],
        },
        # 2. Revenge Ready
        {
            "id": "Revenge Ready",
            "uid": "PWHUD_PROC_REVENGE",
            "parent": "01 - Procs warTank",
            "regionType": "icon",
            "internalVersion": 90,
            "width": 34,
            "height": 34,
            "displayIcon": "Interface\\Icons\\Ability_Warrior_Revenge",
            "auto": False,
            "color": [1, 1, 1, 1],
            "cooldown": True,
            "cooldownSwipe": True,
            "cooldownEdge": True,
            "actions": {
                "start": make_glow_action([0.95, 0.45, 0.10, 1.0]),
                "finish": {"do_glow": True, "glow_action": "hide"},
            },
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "custom": r"""function()
                            local usable = IsUsableSpell("Revenge") or IsUsableSpell("Ritorsione")
                            return (usable == 1 or usable == true)
                        end""",
                        "customDuration": r"""function()
                            local start, duration = GetSpellCooldown("Revenge")
                            if start and duration and duration > 1.5 then
                                return duration, start + duration
                            end
                            return 0, 0
                        end""",
                    },
                    "untrigger": {"type": "custom", "custom": "function() return false end"}
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                make_subtext("REV", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=9, y_offset=0),
            ],
        },
        # 3. Shield Block Active (Buff 2565)
        {
            "id": "Shield Block Active",
            "uid": "PWHUD_PROC_SHIELDBLOCK",
            "parent": "01 - Procs warTank",
            "regionType": "icon",
            "internalVersion": 90,
            "width": 34,
            "height": 34,
            "displayIcon": "Interface\\Icons\\Ability_Defensive",
            "auto": True,
            "color": [1, 1, 1, 1],
            "cooldown": True,
            "cooldownSwipe": True,
            "cooldownEdge": True,
            "triggers": {
                1: {
                    "trigger": {
                        "type": "aura2",
                        "unit": "player",
                        "auranames": ["Shield Block", "Blocco con lo Scudo", "2565"],
                        "useName": True,
                        "debuffType": "HELPFUL",
                        "matchesShowOn": "showOnActive",
                    },
                    "untrigger": {}
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                make_subtext("%p", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=12, y_offset=0),
                make_subtext("100%", justify="CENTER", anchor_point="CENTER", font_size=9, y_offset=0),
            ],
        },
        # 4. Victory Rush
        {
            "id": "Victory Rush",
            "uid": "PWHUD_PROC_VICTORY_RUSH",
            "parent": "01 - Procs warTank",
            "regionType": "icon",
            "internalVersion": 90,
            "width": 34,
            "height": 34,
            "displayIcon": "Interface\\Icons\\Ability_Warrior_Devastate",
            "auto": True,
            "color": [1, 1, 1, 1],
            "cooldown": True,
            "cooldownSwipe": True,
            "cooldownEdge": True,
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "custom": r"""function()
                            local usable = IsUsableSpell("Victory Rush") or IsUsableSpell("Vittoria Imminente") or IsUsableSpell(34428)
                            return (usable == 1 or usable == true)
                        end""",
                    },
                    "untrigger": {"type": "custom", "custom": "function() return false end"}
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                make_subtext("VR", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=9, y_offset=0),
            ],
        },
        # 5. Emergency Low HP Alert (< 35% HP)
        {
            "id": "Emergency Low HP Alert",
            "uid": "PWHUD_PROC_EMERGENCY",
            "parent": "01 - Procs warTank",
            "regionType": "icon",
            "internalVersion": 90,
            "width": 34,
            "height": 34,
            "displayIcon": "Interface\\Icons\\Ability_Warrior_ShieldWall",
            "auto": False,
            "color": [1, 1, 1, 1],
            "cooldown": True,
            "actions": {
                "start": make_glow_action([1.0, 0.15, 0.15, 1.0]),
                "finish": {"do_glow": True, "glow_action": "hide"},
            },
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "custom": r"""function()
                            if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                            local em = _G.PWHUD_GetEmergencyCD and _G.PWHUD_GetEmergencyCD()
                            return (em ~= nil)
                        end""",
                        "customIcon": r"""function()
                            local em = _G.PWHUD_GetEmergencyCD and _G.PWHUD_GetEmergencyCD()
                            return em and em.icon or "Interface\\Icons\\Ability_Warrior_ShieldWall"
                        end""",
                        "customText": r"""function()
                            local cur = UnitHealth("player") or 0
                            local maxHP = UnitHealthMax("player") or 1
                            return string.format("%.0f%%", (cur / maxHP) * 100)
                        end"""
                    },
                    "untrigger": {"type": "custom", "custom": "function() return false end"}
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                make_subtext("%c", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=10, y_offset=0, extra_props={"text_color": [1.0, 0.2, 0.2, 1.0]}),
            ],
        },
        # 6. Boss Enrage Alert
        {
            "id": "Boss Enrage Alert",
            "uid": "PWHUD_PROC_BOSS_ENRAGE",
            "parent": "01 - Procs warTank",
            "regionType": "icon",
            "internalVersion": 90,
            "width": 34,
            "height": 34,
            "displayIcon": "Interface\\Icons\\Spell_Shadow_UnholyFrenzy",
            "auto": False,
            "color": [1, 1, 1, 1],
            "actions": {
                "start": make_glow_action([1.0, 0.0, 0.0, 1.0]),
                "finish": {"do_glow": True, "glow_action": "hide"},
            },
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "custom": r"""function()
                            if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                            local tb = _G.PWHUD_GetTargetBuffs and _G.PWHUD_GetTargetBuffs()
                            return (tb ~= nil and tb.hasEnrage)
                        end""",
                    },
                    "untrigger": {"type": "custom", "custom": "function() return false end"}
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                make_subtext("ENRAGE", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=8, y_offset=0, extra_props={"text_color": [1.0, 0.1, 0.1, 1.0]}),
            ],
        },
        # 7. Tank Buster Alert
        {
            "id": "Tank Buster Alert",
            "uid": "PWHUD_PROC_TANK_BUSTER",
            "parent": "01 - Procs warTank",
            "regionType": "icon",
            "internalVersion": 90,
            "width": 34,
            "height": 34,
            "displayIcon": "Interface\\Icons\\Spell_Shadow_SoulLeech_3",
            "auto": False,
            "color": [1, 1, 1, 1],
            "actions": {
                "start": make_glow_action([1.0, 0.2, 0.2, 1.0]),
                "finish": {"do_glow": True, "glow_action": "hide"},
            },
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "custom": r"""function()
                            if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                            local pd = _G.PWHUD_GetPlayerDebuffs and _G.PWHUD_GetPlayerDebuffs()
                            if not pd then return false end
                            if pd.byName["Soul Reaper"] or pd.bySpellId[73797] or pd.bySpellId[69409] then return true end
                            local gb = pd.byName["Gastric Bloat"] or pd.bySpellId[72219]
                            if gb and gb.count >= 8 then return true end
                            local imp = pd.byName["Impale"] or pd.bySpellId[67478]
                            if imp and imp.count >= 2 then return true end
                            return false
                        end""",
                        "customText": r"""function()
                            local pd = _G.PWHUD_GetPlayerDebuffs and _G.PWHUD_GetPlayerDebuffs()
                            if not pd then return "" end
                            local gb = pd.byName["Gastric Bloat"] or pd.bySpellId[72219]
                            if gb and gb.count >= 8 then return string.format("x%d", gb.count) end
                            local imp = pd.byName["Impale"] or pd.bySpellId[67478]
                            if imp and imp.count >= 2 then return string.format("x%d", imp.count) end
                            return "SWAP"
                        end"""
                    },
                    "untrigger": {"type": "custom", "custom": "function() return false end"}
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                make_subtext("%c", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=9, y_offset=0, extra_props={"text_color": [1.0, 0.3, 0.0, 1.0]}),
            ],
        },
    ]
