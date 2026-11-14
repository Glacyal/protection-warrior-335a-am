"""
Modulo Componente: 02 - Battle Shout, 03 - Commanding Shout, 04 - Defensive Stance
===================================================================================
Gestisce i buff di classe e la postura a x = -222, -190, -158 a y = 0:
1. 02 - Battle Shout:
   - Gruppo a x = -222, y = 0
   - Active: visibile SOLO quando il buff (Battle Shout o BoM/GBoM del Paladino) sta per scadere (<= 30s).
   - OFF: visibile quando manca SIA Battle Shout CHE BoM/GBoM (desaturato + 'OFF').
2. 03 - Commanding Shout:
   - Gruppo a x = -190, y = 0
   - Active: visibile SOLO quando il buff (Commanding Shout o Blood Pact dell'Imp) sta per scadere (<= 30s).
   - OFF: visibile quando manca SIA Commanding Shout CHE Blood Pact (desaturato + 'OFF').
3. 04 - Defensive Stance:
   - Gruppo a x = -158, y = 0
   - Allerta immediata con glow rosso e scritta 'STANCE' se in combattimento il tank si trova fuori dalla Postura Difensiva (Stance 2).
"""
from builder.core.helpers import make_subtext, make_glow_action


SHARED_GET_PLAYER_BUFFS_LUA = r"""function(force)
    local now_b = GetTime()
    local c = _G.PWHUD_BuffCache
    if not force and c and c.time == now_b then
        return c
    end
    c = {
        time = now_b,
        bySpellId = {},
        byName = {},
        list = {},
        hasBoM = false,
        hasBloodPact = false,
        hasBattleShout = false,
        hasCommandingShout = false,
    }

    for i = 1, 40 do
        local name, rank, icon, count, debuffType, duration, expirationTime, unitCaster, isStealable, shouldConsolidate, spellId = UnitBuff("player", i)
        if not name then break end
        local b = {
            name = name,
            icon = icon,
            duration = duration,
            expirationTime = expirationTime,
            spellId = spellId,
        }
        c.list[#c.list + 1] = b
        if spellId then c.bySpellId[spellId] = b end
        if name then c.byName[name] = b end

        if spellId == 48934 or spellId == 48932 or spellId == 19740 or name == "Blessing of Might" or name == "Greater Blessing of Might" then
            c.hasBoM = true
        end
        if spellId == 47982 or spellId == 47440 or name == "Blood Pact" then
            c.hasBloodPact = true
        end
        if spellId == 47436 or spellId == 25289 or name == "Battle Shout" then
            c.hasBattleShout = true
        end
        if spellId == 47440 or spellId == 469 or name == "Commanding Shout" then
            c.hasCommandingShout = true
        end
    end
    _G.PWHUD_BuffCache = c
    return c
end"""


def build_buffs_auras() -> list[dict]:
    """Costruisce le aure per Battle Shout, Commanding Shout e Defensive Stance."""
    return [
        # =====================================================================
        # 02 - BATTLE SHOUT (Gruppo a x = -222, y = 0)
        # =====================================================================
        {
            "id": "02 - Battle Shout",
            "uid": "PWHUD_BS_GRP",
            "parent": "Class Warrior (Protection)",
            "regionType": "group",
            "internalVersion": 90,
            "xOffset": -222,
            "yOffset": 0,
            "controlledChildren": [
                "Battle Shout - Active",
                "Battle Shout - OFF",
            ],
            "actions": {
                "init": {"do_custom": True, "custom": f"_G.PWHUD_GetPlayerBuffs = {SHARED_GET_PLAYER_BUFFS_LUA}"},
                "start": {},
                "finish": {},
            },
        },
        {
            "id": "Battle Shout - Active",
            "uid": "PWHUD_BS_ACTIVE",
            "parent": "02 - Battle Shout",
            "regionType": "icon",
            "internalVersion": 90,
            "width": 34,
            "height": 34,
            "xOffset": 0,
            "yOffset": 0,
            "displayIcon": "Interface\\Icons\\Ability_Warrior_BattleShout",
            "cooldown": True,
            "cooldownSwipe": True,
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "custom": r"""function()
                            if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                            local c = _G.PWHUD_GetPlayerBuffs()
                            local b = c.bySpellId[47436] or c.byName["Battle Shout"]
                            if b and b.expirationTime and b.expirationTime > 0 then
                                local rem = b.expirationTime - GetTime()
                                return (rem > 0 and rem <= 30)
                            end
                            return false
                        end""",
                        "customDuration": r"""function()
                            local c = _G.PWHUD_GetPlayerBuffs()
                            local b = c.bySpellId[47436] or c.byName["Battle Shout"]
                            if b and b.duration and b.duration > 0 then
                                return b.duration, b.expirationTime
                            end
                            return 0, 0
                        end"""
                    },
                    "untrigger": {"type": "custom", "custom": "function() return false end"}
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("%p", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=12, y_offset=0),
            ],
        },
        {
            "id": "Battle Shout - OFF",
            "uid": "PWHUD_BS_OFF",
            "parent": "02 - Battle Shout",
            "regionType": "icon",
            "internalVersion": 90,
            "width": 34,
            "height": 34,
            "xOffset": 0,
            "yOffset": 0,
            "displayIcon": "Interface\\Icons\\Ability_Warrior_BattleShout",
            "desaturate": True,
            "color": [0.6, 0.6, 0.6, 0.85],
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "custom": r"""function()
                            if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                            local c = _G.PWHUD_GetPlayerBuffs()
                            return (not c.hasBattleShout and not c.hasBoM)
                        end""",
                    },
                    "untrigger": {"type": "custom", "custom": "function() return false end"}
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("OFF", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=11, y_offset=0, extra_props={"text_color": [1, 0.2, 0.2, 1]}),
            ],
        },

        # =====================================================================
        # 03 - COMMANDING SHOUT (Gruppo a x = -190, y = 0)
        # =====================================================================
        {
            "id": "03 - Commanding Shout",
            "uid": "PWHUD_CS_GRP",
            "parent": "Class Warrior (Protection)",
            "regionType": "group",
            "internalVersion": 90,
            "xOffset": -190,
            "yOffset": 0,
            "controlledChildren": [
                "Commanding Shout - Active",
                "Commanding Shout - OFF",
            ],
            "actions": {
                "init": {"do_custom": True, "custom": f"_G.PWHUD_GetPlayerBuffs = {SHARED_GET_PLAYER_BUFFS_LUA}"},
                "start": {},
                "finish": {},
            },
        },
        {
            "id": "Commanding Shout - Active",
            "uid": "PWHUD_CS_ACTIVE",
            "parent": "03 - Commanding Shout",
            "regionType": "icon",
            "internalVersion": 90,
            "width": 34,
            "height": 34,
            "xOffset": 0,
            "yOffset": 0,
            "displayIcon": "Interface\\Icons\\Ability_Warrior_RallyingCry",
            "cooldown": True,
            "cooldownSwipe": True,
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "custom": r"""function()
                            if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                            local c = _G.PWHUD_GetPlayerBuffs()
                            local b = c.bySpellId[47440] or c.byName["Commanding Shout"]
                            if b and b.expirationTime and b.expirationTime > 0 then
                                local rem = b.expirationTime - GetTime()
                                return (rem > 0 and rem <= 30)
                            end
                            return false
                        end""",
                        "customDuration": r"""function()
                            local c = _G.PWHUD_GetPlayerBuffs()
                            local b = c.bySpellId[47440] or c.byName["Commanding Shout"]
                            if b and b.duration and b.duration > 0 then
                                return b.duration, b.expirationTime
                            end
                            return 0, 0
                        end"""
                    },
                    "untrigger": {"type": "custom", "custom": "function() return false end"}
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("%p", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=12, y_offset=0),
            ],
        },
        {
            "id": "Commanding Shout - OFF",
            "uid": "PWHUD_CS_OFF",
            "parent": "03 - Commanding Shout",
            "regionType": "icon",
            "internalVersion": 90,
            "width": 34,
            "height": 34,
            "xOffset": 0,
            "yOffset": 0,
            "displayIcon": "Interface\\Icons\\Ability_Warrior_RallyingCry",
            "desaturate": True,
            "color": [0.6, 0.6, 0.6, 0.85],
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "custom": r"""function()
                            if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                            local c = _G.PWHUD_GetPlayerBuffs()
                            return (not c.hasCommandingShout and not c.hasBloodPact)
                        end""",
                    },
                    "untrigger": {"type": "custom", "custom": "function() return false end"}
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("OFF", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=11, y_offset=0, extra_props={"text_color": [1, 0.2, 0.2, 1]}),
            ],
        },

        # =====================================================================
        # 04 - DEFENSIVE STANCE (Gruppo a x = -158, y = 0)
        # =====================================================================
        {
            "id": "04 - Defensive Stance",
            "uid": "PWHUD_STANCE_GRP",
            "parent": "Class Warrior (Protection)",
            "regionType": "group",
            "internalVersion": 90,
            "xOffset": -158,
            "yOffset": 0,
            "controlledChildren": [
                "Defensive Stance - Active",
                "Defensive Stance - Warning",
            ],
        },
        {
            "id": "Defensive Stance - Active",
            "uid": "PWHUD_STANCE_ACTIVE",
            "parent": "04 - Defensive Stance",
            "regionType": "icon",
            "internalVersion": 90,
            "width": 34,
            "height": 34,
            "xOffset": 0,
            "yOffset": 0,
            "displayIcon": "Interface\\Icons\\Ability_Warrior_DefensiveStance",
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "custom": r"""function()
                            return (GetShapeshiftForm() == 2)
                        end""",
                    },
                    "untrigger": {"type": "custom", "custom": "function() return false end"}
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("DEF", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=9, y_offset=0),
            ],
        },
        {
            "id": "Defensive Stance - Warning",
            "uid": "PWHUD_STANCE_WARN",
            "parent": "04 - Defensive Stance",
            "regionType": "icon",
            "internalVersion": 90,
            "width": 34,
            "height": 34,
            "xOffset": 0,
            "yOffset": 0,
            "displayIcon": "Interface\\Icons\\Ability_Warrior_DefensiveStance",
            "actions": {
                "start": make_glow_action([1.0, 0.1, 0.1, 1.0]),
                "finish": {"do_glow": True, "glow_action": "hide"},
            },
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "custom": r"""function()
                            return UnitAffectingCombat("player") and (GetShapeshiftForm() ~= 2)
                        end""",
                    },
                    "untrigger": {"type": "custom", "custom": "function() return false end"}
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("STANCE", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=8, y_offset=0, extra_props={"text_color": [1.0, 0.1, 0.1, 1.0]}),
            ],
        },
    ]
