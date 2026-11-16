"""
Modulo Componente: 01 - Procs warTank (Dynamic Group)
=====================================================
Gestisce la barra orizzontale dinamica superiore dei proc e allarmi (y = 52):
- Crescita orizzontale centrata (space = 6px, icone 34x34px).
- Include rigorosamente i proc chiave del tank e gli allarmi critici:
  1. Sword and Board (Buff 50227: Shield Slam a costo 0 con Pixel Glow dorato e timer 5s)
  2. Revenge Ready warTank (Attivo post Blocco/Schivata/Parata con finestra 5s, refresh dinamico e LibCustomGlow-1.0)
  3. Shield Block Active (Buff 2565: durata attiva 10s con countdown)
  4. Victory Rush (Proc Victorious con countdown durata 20s)
  5. Emergency Low HP Alert (Salute < 35% con allerta visiva del CD difensivo prioritario pronto)
  5. Tank Buster Alert (Debuff letali: Soul Reaper, Impale >= 2, Gastric Bloat >= 8, Fusion Punch)
"""
from builder.core.helpers import make_subtext, make_glow_action


def build_procs_auras() -> list[dict]:
    """
    Costruisce e restituisce le 8 aure del gruppo dinamico Procs:
    - 01 - Procs warTank (Dynamic Group)
    - Sword and Board, Revenge Ready warTank, Shield Block Active,
      Emergency Low HP Alert, Tank Buster Alert.
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
                "Revenge Ready warTank",
                "Shield Block Active",
                "Emergency Low HP Alert",
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
        # 2. Revenge Ready (5.0s window, dynamic refresh on avoid/block, LibCustomGlow-1.0)
        {
            "id": "Revenge Ready warTank",
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
                "init": {
                    "do_custom": True,
                    "custom": r"""if not _G.PWHUD_RevengeFrame then
    local f = CreateFrame("Frame")
    f:RegisterEvent("COMBAT_LOG_EVENT_UNFILTERED")
    f:RegisterEvent("PLAYER_ENTERING_WORLD")
    f:RegisterEvent("PLAYER_DEAD")
    _G.PWHUD_Revenge = _G.PWHUD_Revenge or { start = 0, duration = 5.0 }
    local pGUID = UnitGUID("player")
    f:SetScript("OnEvent", function(self, event, ...)
        if event == "PLAYER_ENTERING_WORLD" then
            pGUID = UnitGUID("player")
            _G.PWHUD_Revenge.start = 0
            return
        elseif event == "PLAYER_DEAD" then
            _G.PWHUD_Revenge.start = 0
            return
        end
        if event == "COMBAT_LOG_EVENT_UNFILTERED" then
            if not pGUID then pGUID = UnitGUID("player") end
            local _, ev, _, srcGUID, _, _, _, dstGUID = ...
            if dstGUID == pGUID then
                if ev == "SWING_MISSED" then
                    local mType = select(12, ...)
                    if mType == "DODGE" or mType == "PARRY" or mType == "BLOCK" then
                        _G.PWHUD_Revenge.start = GetTime()
                        _G.PWHUD_Revenge.duration = 5.0
                    end
                elseif ev == "RANGE_MISSED" or ev == "SPELL_MISSED" then
                    local mType = select(15, ...)
                    if mType == "DODGE" or mType == "PARRY" or mType == "BLOCK" then
                        _G.PWHUD_Revenge.start = GetTime()
                        _G.PWHUD_Revenge.duration = 5.0
                    end
                elseif ev == "SWING_DAMAGE" then
                    local blk = select(16, ...)
                    if blk and blk > 0 then
                        _G.PWHUD_Revenge.start = GetTime()
                        _G.PWHUD_Revenge.duration = 5.0
                    end
                elseif ev == "RANGE_DAMAGE" or ev == "SPELL_DAMAGE" then
                    local blk = select(19, ...)
                    if blk and blk > 0 then
                        _G.PWHUD_Revenge.start = GetTime()
                        _G.PWHUD_Revenge.duration = 5.0
                    end
                end
            end
            if srcGUID == pGUID and ev == "SPELL_CAST_SUCCESS" then
                local spId = select(12, ...)
                local spName = select(13, ...)
                if spId == 57823 or spId == 6572 or spId == 6574 or spId == 7379 or spId == 11601 or spId == 25288 or spId == 25269 or spId == 30357 or spName == "Revenge" or spName == "Ritorsione" then
                    _G.PWHUD_Revenge.start = 0
                end
            end
        end
    end)
    _G.PWHUD_RevengeFrame = f
end""",
                },
                "start": {
                    "do_custom": True,
                    "custom": r"""local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)
if LCG and aura_env and aura_env.region then
    LCG.PixelGlow_Start(aura_env.region, {0.95, 0.45, 0.10, 1.0}, 8, 0.25, 10, 2, 0, 0, false, "PWHUD_REVENGE_GLOW")
end""",
                },
                "finish": {
                    "do_custom": True,
                    "custom": r"""local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)
if LCG and aura_env and aura_env.region then
    LCG.PixelGlow_Stop(aura_env.region, "PWHUD_REVENGE_GLOW")
end""",
                },
            },
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "events": "COMBAT_LOG_EVENT_UNFILTERED,ACTIONBAR_UPDATE_USABLE,SPELL_UPDATE_USABLE,PLAYER_ENTERING_WORLD",
                        "custom": r"""function()
                            local usable = IsUsableSpell("Revenge") or IsUsableSpell("Ritorsione") or IsUsableSpell(57823)
                            if not (usable == 1 or usable == true) then
                                if _G.PWHUD_Revenge then _G.PWHUD_Revenge.start = 0 end
                                return false
                            end
                            local rev = _G.PWHUD_Revenge
                            local now = GetTime()
                            if not rev or not rev.start or rev.start == 0 then
                                _G.PWHUD_Revenge = _G.PWHUD_Revenge or {}
                                _G.PWHUD_Revenge.start = now
                                _G.PWHUD_Revenge.duration = 5.0
                                return true
                            end
                            if (now - rev.start) <= 5.0 then
                                return true
                            end
                            return false
                        end""",
                        "customDuration": r"""function()
                            local rev = _G.PWHUD_Revenge
                            if rev and rev.start and rev.start > 0 then
                                local dur = rev.duration or 5.0
                                return dur, rev.start + dur
                            end
                            return 0, 0
                        end""",
                    },
                    "untrigger": {
                        "type": "custom",
                        "custom": r"""function()
                            local usable = IsUsableSpell("Revenge") or IsUsableSpell("Ritorsione") or IsUsableSpell(57823)
                            if not (usable == 1 or usable == true) then
                                local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)
                                if LCG and aura_env and aura_env.region then
                                    LCG.PixelGlow_Stop(aura_env.region, "PWHUD_REVENGE_GLOW")
                                end
                                return true
                            end
                            local rev = _G.PWHUD_Revenge
                            if not rev or not rev.start or rev.start == 0 or (GetTime() - rev.start > 5.0) then
                                local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)
                                if LCG and aura_env and aura_env.region then
                                    LCG.PixelGlow_Stop(aura_env.region, "PWHUD_REVENGE_GLOW")
                                end
                                return true
                            end
                            return false
                        end""",
                    }
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("%p", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=10, y_offset=0),
                make_subtext("REV", justify="CENTER", anchor_point="CENTER", font_size=9, y_offset=0),
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
        # 5. Tank Buster Alert
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
