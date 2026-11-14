"""
Modulo Componente: 05-13 - Utility Row (Warrior Protection)
===========================================================
Gestisce la riga orizzontale di utilità a y = -45 con riposizionamento dinamico
centrato naturale (da 3 a 10 icone) in base all'equipaggiamento e alle abilità:
1. 05 - Trinket 1 warTank (Slot 13: Fang, Indomitability, Coin, Scarab, Skeleton Key, Black Heart, ecc.)
2. 06 - Trinket 2 warTank (Slot 14: Fang, Indomitability, Coin, Scarab, Skeleton Key, Black Heart, ecc.)
3. 06b - Ring warTank (Slot 11/12: Ashen Band of Endless Courage +Armor/Dodge proc, 60s ICD)
4. 07 - Cloak warTank (Slot 15: Flexweave / Paracadute / Incanti)
5. 08 - Tier Set warTank (T9/T10 Prot: Ymirjar Lord 2P/4P, Triumph 2P/4P)
6. 09 - Enchants warTank (Slot 16/17: Blade Ward, Blood Draining, Mongoose con tracking)
7. 10 - Gloves warTank (Slot 10: Reticulated Armor Webbing +885 Armor / Acceleratori Ipersonici)
8. 11 - Shield Wall (Spell 871: durata attiva 12s, ricarica e glow emergenza)
9. 12 - Last Stand (Spell 12975: durata attiva 20s, ricarica e glow emergenza)
10. 13 - Boots warTank (Slot 8: Acceleratori a Nitro Boosts / Enraged Regeneration)
"""
from builder.core.helpers import make_subtext


# =============================================================================
# LOGICA LUA CONDIVISA CENTRALIZZATA (BOOTSTRAP UTILITY TANK WARRIOR)
# =============================================================================
SHARED_WARRIOR_CORE_BOOTSTRAP_LUA = r"""function()
    _G.PWHUD_GetPlayerBuffs = _G.PWHUD_GetPlayerBuffs or function()
        local now_b = GetTime()
        local c = _G.PWHUD_BuffCache
        if c and c.time == now_b then return c end
        c = { time = now_b, bySpellId = {}, byName = {}, list = {} }
        for i = 1, 40 do
            local name, rank, icon, count, debuffType, duration, expirationTime, unitCaster, isStealable, shouldConsolidate, spellId = UnitBuff("player", i)
            if not name then break end
            local b = {
                name = name,
                icon = icon,
                count = count or 0,
                duration = duration or 0,
                expirationTime = expirationTime or 0,
                spellId = spellId,
            }
            c.list[#c.list + 1] = b
            if spellId then c.bySpellId[spellId] = b end
            if name then c.byName[name] = b end
        end
        _G.PWHUD_BuffCache = c
        return c
    end

    _G.PWHUD_GetPlayerDebuffs = _G.PWHUD_GetPlayerDebuffs or function()
        local now_d = GetTime()
        local c = _G.PWHUD_PlayerDebuffCache
        if c and c.time == now_d then return c end
        c = { time = now_d, bySpellId = {}, byName = {}, list = {} }
        for i = 1, 40 do
            local name, rank, icon, count, debuffType, duration, expirationTime, unitCaster, isStealable, shouldConsolidate, spellId = UnitDebuff("player", i)
            if not name then break end
            local d = {
                name = name,
                icon = icon,
                count = count or 0,
                duration = duration or 0,
                expirationTime = expirationTime or 0,
                spellId = spellId,
            }
            c.list[#c.list + 1] = d
            if spellId then c.bySpellId[spellId] = d end
            if name then c.byName[name] = d end
        end
        _G.PWHUD_PlayerDebuffCache = c
        return c
    end

    _G.PWHUD_GetTargetBuffs = _G.PWHUD_GetTargetBuffs or function()
        local now_tb = GetTime()
        local c = _G.PWHUD_TargetBuffCache
        if c and c.time == now_tb then return c end
        c = { time = now_tb, hasEnrage = false, enrageName = nil, list = {} }
        if not UnitExists("target") then
            _G.PWHUD_TargetBuffCache = c
            return c
        end
        for i = 1, 40 do
            local name, rank, icon, count, debuffType, duration, expirationTime, unitCaster, isStealable, shouldConsolidate, spellId = UnitBuff("target", i)
            if not name then break end
            local lowerName = string.lower(name)
            if string.find(lowerName, "enrage") or string.find(lowerName, "frenzy") or string.find(lowerName, "berserk") or string.find(lowerName, "bloodlust") then
                c.hasEnrage = true
                c.enrageName = name
            end
        end
        _G.PWHUD_TargetBuffCache = c
        return c
    end

    _G.PWHUD_GetKickInfo = _G.PWHUD_GetKickInfo or function()
        local spell, rank, displayName, icon, startTime, endTime, isTradeSkill, castID, notInterruptible = UnitCastingInfo("target")
        if not spell then
            spell, rank, displayName, icon, startTime, endTime, isTradeSkill, notInterruptible = UnitChannelInfo("target")
        end
        if not spell then return nil end

        local form = GetShapeshiftForm() -- 1 = Battle, 2 = Defensive, 3 = Berserker
        local hasShield = (GetInventoryItemID("player", 17) ~= nil)
        local now = GetTime()
        local sStart, sDur = GetSpellCooldown("Shield Bash")
        local shieldBashReady = (sDur == nil or sDur <= 1.5 or (sStart + sDur <= now))
        local pStart, pDur = GetSpellCooldown("Pummel")
        local pummelReady = (pDur == nil or pDur <= 1.5 or (pStart + pDur <= now))

        local res = {
            spellName = spell,
            icon = icon,
            notInterruptible = notInterruptible,
            remaining = (endTime and (endTime / 1000 - now)) or 0,
            recommended = "SHIELD BASH",
            canKick = true,
        }

        if notInterruptible then
            res.canKick = false
            res.recommended = "IMMUNE"
            return res
        end

        if (form == 2 or form == 1) and hasShield and shieldBashReady then
            res.recommended = "SHIELD BASH"
        elseif form == 3 and pummelReady then
            res.recommended = "PUMMEL"
        elseif form == 2 and not shieldBashReady and pummelReady then
            res.recommended = "STANCE -> PUMMEL"
        else
            res.recommended = "STUN / CD"
        end
        return res
    end

    _G.PWHUD_GetEmergencyCD = _G.PWHUD_GetEmergencyCD or function()
        local curHP = UnitHealth("player") or 0
        local maxHP = UnitHealthMax("player") or 1
        local pct = (curHP / maxHP) * 100
        if pct > 35 then return nil end

        local now = GetTime()
        local function isReady(name)
            local s, d = GetSpellCooldown(name)
            return (d == nil or d <= 1.5 or (s + d <= now))
        end

        if isReady("Shield Wall") then
            return { action = "SHIELD WALL", icon = "Interface\\Icons\\Ability_Warrior_ShieldWall", pct = pct }
        elseif isReady("Last Stand") then
            return { action = "LAST STAND", icon = "Interface\\Icons\\Spell_Nature_ShamanRage", pct = pct }
        elseif isReady("Shield Block") then
            return { action = "SHIELD BLOCK", icon = "Interface\\Icons\\Ability_Defensive", pct = pct }
        elseif isReady("Enraged Regeneration") then
            return { action = "ENRAGED REGEN", icon = "Interface\\Icons\\Ability_Warrior_EnragedRegeneration", pct = pct }
        else
            return { action = "HEALTHSTONE / POT", icon = "Interface\\Icons\\INV_Stone_04", pct = pct }
        end
    end

    _G.PWHUD_CoreInitDone = true
end"""


def build_utility_auras() -> list[dict]:
    """Costruisce le 10 aure della riga di utilità (05-13)."""
    auras = []

    # 05 - Trinket 1 warTank (Slot 13)
    auras.append({
        "id": "05 - Trinket 1 warTank",
        "uid": "PWHUD_UTIL_TRINKET1",
        "parent": "Class Warrior (Protection)",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 28,
        "height": 28,
        "xOffset": -140,
        "yOffset": -45,
        "displayIcon": "Interface\\Icons\\INV_Misc_Ornament_02",
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
                        if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                        return (GetInventoryItemID("player", 13) ~= nil)
                    end""",
                    "customDuration": r"""function()
                        local start, duration = GetInventoryItemCooldown("player", 13)
                        if start and duration and duration > 1.5 then
                            return duration, start + duration
                        end
                        return 0, 0
                    end""",
                    "customIcon": r"""function()
                        return GetInventoryItemTexture("player", 13) or "Interface\\Icons\\INV_Misc_Ornament_02"
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            },
            "activeTriggerMode": -10,
        },
        "subRegions": [
            {"type": "subbackground"},
            make_subtext("%p", justify="CENTER", anchor_point="CENTER", font_size=11, y_offset=0),
            make_subtext("T1", justify="RIGHT", anchor_point="INNER_BOTTOMRIGHT", font_size=8, y_offset=-2, x_offset=2),
        ],
    })

    # 06 - Trinket 2 warTank (Slot 14)
    auras.append({
        "id": "06 - Trinket 2 warTank",
        "uid": "PWHUD_UTIL_TRINKET2",
        "parent": "Class Warrior (Protection)",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 28,
        "height": 28,
        "xOffset": -105,
        "yOffset": -45,
        "displayIcon": "Interface\\Icons\\INV_Misc_Ornament_02",
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
                        if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                        return (GetInventoryItemID("player", 14) ~= nil)
                    end""",
                    "customDuration": r"""function()
                        local start, duration = GetInventoryItemCooldown("player", 14)
                        if start and duration and duration > 1.5 then
                            return duration, start + duration
                        end
                        return 0, 0
                    end""",
                    "customIcon": r"""function()
                        return GetInventoryItemTexture("player", 14) or "Interface\\Icons\\INV_Misc_Ornament_02"
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            },
            "activeTriggerMode": -10,
        },
        "subRegions": [
            {"type": "subbackground"},
            make_subtext("%p", justify="CENTER", anchor_point="CENTER", font_size=11, y_offset=0),
            make_subtext("T2", justify="RIGHT", anchor_point="INNER_BOTTOMRIGHT", font_size=8, y_offset=-2, x_offset=2),
        ],
    })

    # 06b - Ring warTank (Slot 11/12)
    auras.append({
        "id": "06b - Ring warTank",
        "uid": "PWHUD_UTIL_RING",
        "parent": "Class Warrior (Protection)",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 28,
        "height": 28,
        "xOffset": -70,
        "yOffset": -45,
        "displayIcon": "Interface\\Icons\\INV_Jewelry_Ring_84",
        "cooldown": True,
        "cooldownSwipe": True,
        "triggers": {
            1: {
                "trigger": {
                    "type": "custom",
                    "custom_type": "status",
                    "check": "update",
                    "custom": r"""function()
                        local id1 = GetInventoryItemID("player", 11)
                        local id2 = GetInventoryItemID("player", 12)
                        return (id1 == 50403 or id1 == 50404 or id2 == 50403 or id2 == 50404)
                    end""",
                    "customIcon": r"""function()
                        return "Interface\\Icons\\INV_Jewelry_Ring_84"
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            },
            "activeTriggerMode": -10,
        },
        "subRegions": [
            {"type": "subbackground"},
            make_subtext("%p", justify="CENTER", anchor_point="CENTER", font_size=11, y_offset=0),
            make_subtext("RING", justify="RIGHT", anchor_point="INNER_BOTTOMRIGHT", font_size=8, y_offset=-2, x_offset=2),
        ],
    })

    # 07 - Cloak warTank (Slot 15)
    auras.append({
        "id": "07 - Cloak warTank",
        "uid": "PWHUD_UTIL_CLOAK",
        "parent": "Class Warrior (Protection)",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 28,
        "height": 28,
        "xOffset": -35,
        "yOffset": -45,
        "displayIcon": "Interface\\Icons\\INV_Misc_Cape_18",
        "cooldown": True,
        "cooldownSwipe": True,
        "triggers": {
            1: {
                "trigger": {
                    "type": "custom",
                    "custom_type": "status",
                    "check": "update",
                    "custom": r"""function()
                        return (GetInventoryItemID("player", 15) ~= nil)
                    end""",
                    "customDuration": r"""function()
                        local start, duration = GetInventoryItemCooldown("player", 15)
                        if start and duration and duration > 1.5 then
                            return duration, start + duration
                        end
                        return 0, 0
                    end""",
                    "customIcon": r"""function()
                        return GetInventoryItemTexture("player", 15) or "Interface\\Icons\\INV_Misc_Cape_18"
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            },
            "activeTriggerMode": -10,
        },
        "subRegions": [
            {"type": "subbackground"},
            make_subtext("%p", justify="CENTER", anchor_point="CENTER", font_size=11, y_offset=0),
            make_subtext("CLK", justify="RIGHT", anchor_point="INNER_BOTTOMRIGHT", font_size=8, y_offset=-2, x_offset=2),
        ],
    })

    # 08 - Tier Set warTank (T9/T10 Prot)
    auras.append({
        "id": "08 - Tier Set warTank",
        "uid": "PWHUD_UTIL_TIER",
        "parent": "Class Warrior (Protection)",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 28,
        "height": 28,
        "xOffset": 0,
        "yOffset": -45,
        "displayIcon": "Interface\\Icons\\INV_Chest_Plate_13",
        "cooldown": True,
        "cooldownSwipe": True,
        "triggers": {
            1: {
                "trigger": {
                    "type": "custom",
                    "custom_type": "status",
                    "check": "update",
                    "custom": r"""function()
                        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
                        return (buffs and (buffs.bySpellId[70844] or buffs.bySpellId[70843] or buffs.byName["Shield Block"]))
                    end""",
                    "customIcon": r"""function()
                        return "Interface\\Icons\\INV_Chest_Plate_13"
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            },
            "activeTriggerMode": -10,
        },
        "subRegions": [
            {"type": "subbackground"},
            make_subtext("T10", justify="RIGHT", anchor_point="INNER_BOTTOMRIGHT", font_size=8, y_offset=-2, x_offset=2),
        ],
    })

    # 09 - Enchants warTank (Blade Ward / Blood Draining / Mongoose)
    auras.append({
        "id": "09 - Enchants warTank",
        "uid": "PWHUD_UTIL_ENCHANTS",
        "parent": "Class Warrior (Protection)",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 28,
        "height": 28,
        "xOffset": 35,
        "yOffset": -45,
        "displayIcon": "Interface\\Icons\\Spell_Holy_BlessingOfProtection",
        "cooldown": True,
        "cooldownSwipe": True,
        "triggers": {
            1: {
                "trigger": {
                    "type": "custom",
                    "custom_type": "status",
                    "check": "update",
                    "custom": r"""function()
                        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
                        if not buffs then return false end
                        return (buffs.bySpellId[64440] or buffs.bySpellId[64568] or buffs.bySpellId[28093] or buffs.byName["Blade Ward"] or buffs.byName["Blood Draining"] or buffs.byName["Lightning Speed"])
                    end""",
                    "customDuration": r"""function()
                        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
                        local b = buffs and (buffs.bySpellId[64440] or buffs.bySpellId[64568] or buffs.bySpellId[28093])
                        if b and b.duration and b.duration > 0 then
                            return b.duration, b.expirationTime
                        end
                        return 0, 0
                    end""",
                    "customIcon": r"""function()
                        return "Interface\\Icons\\Spell_Holy_BlessingOfProtection"
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            },
            "activeTriggerMode": -10,
        },
        "subRegions": [
            {"type": "subbackground"},
            make_subtext("%p", justify="CENTER", anchor_point="CENTER", font_size=11, y_offset=0),
            make_subtext("ENC", justify="RIGHT", anchor_point="INNER_BOTTOMRIGHT", font_size=8, y_offset=-2, x_offset=2),
        ],
    })

    # 10 - Gloves warTank (Slot 10)
    auras.append({
        "id": "10 - Gloves warTank",
        "uid": "PWHUD_UTIL_GLOVES",
        "parent": "Class Warrior (Protection)",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 28,
        "height": 28,
        "xOffset": 70,
        "yOffset": -45,
        "displayIcon": "Interface\\Icons\\INV_Gauntlets_04",
        "cooldown": True,
        "cooldownSwipe": True,
        "triggers": {
            1: {
                "trigger": {
                    "type": "custom",
                    "custom_type": "status",
                    "check": "update",
                    "custom": r"""function()
                        return (GetInventoryItemID("player", 10) ~= nil)
                    end""",
                    "customDuration": r"""function()
                        local start, duration = GetInventoryItemCooldown("player", 10)
                        if start and duration and duration > 1.5 then
                            return duration, start + duration
                        end
                        return 0, 0
                    end""",
                    "customIcon": r"""function()
                        return GetInventoryItemTexture("player", 10) or "Interface\\Icons\\INV_Gauntlets_04"
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            },
            "activeTriggerMode": -10,
        },
        "subRegions": [
            {"type": "subbackground"},
            make_subtext("%p", justify="CENTER", anchor_point="CENTER", font_size=11, y_offset=0),
            make_subtext("GLV", justify="RIGHT", anchor_point="INNER_BOTTOMRIGHT", font_size=8, y_offset=-2, x_offset=2),
        ],
    })

    # 11 - Shield Wall (Spell 871)
    auras.append({
        "id": "11 - Shield Wall",
        "uid": "PWHUD_UTIL_SHIELD_WALL",
        "parent": "Class Warrior (Protection)",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 28,
        "height": 28,
        "xOffset": 105,
        "yOffset": -45,
        "displayIcon": "Interface\\Icons\\Ability_Warrior_ShieldWall",
        "cooldown": True,
        "cooldownSwipe": True,
        "triggers": {
            1: {
                "trigger": {
                    "type": "custom",
                    "custom_type": "status",
                    "check": "update",
                    "custom": r"""function() return true end""",
                    "customDuration": r"""function()
                        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
                        local b = buffs and (buffs.bySpellId[871] or buffs.byName["Shield Wall"])
                        if b and b.duration and b.duration > 0 then
                            return b.duration, b.expirationTime
                        end
                        local start, duration = GetSpellCooldown("Shield Wall")
                        if start and duration and duration > 1.5 then
                            return duration, start + duration
                        end
                        return 0, 0
                    end""",
                    "customIcon": r"""function()
                        return "Interface\\Icons\\Ability_Warrior_ShieldWall"
                    end""",
                    "customText": r"""function()
                        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
                        local b = buffs and (buffs.bySpellId[871] or buffs.byName["Shield Wall"])
                        if b then return "|cFF00FF00-60%|r" end
                        return ""
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            },
            "activeTriggerMode": -10,
        },
        "subRegions": [
            {"type": "subbackground"},
            make_subtext("%p", justify="CENTER", anchor_point="CENTER", font_size=11, y_offset=0),
            make_subtext("SW", justify="RIGHT", anchor_point="INNER_BOTTOMRIGHT", font_size=8, y_offset=-2, x_offset=2),
        ],
    })

    # 12 - Last Stand (Spell 12975)
    auras.append({
        "id": "12 - Last Stand",
        "uid": "PWHUD_UTIL_LAST_STAND",
        "parent": "Class Warrior (Protection)",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 28,
        "height": 28,
        "xOffset": 140,
        "yOffset": -45,
        "displayIcon": "Interface\\Icons\\Spell_Nature_ShamanRage",
        "cooldown": True,
        "cooldownSwipe": True,
        "triggers": {
            1: {
                "trigger": {
                    "type": "custom",
                    "custom_type": "status",
                    "check": "update",
                    "custom": r"""function() return true end""",
                    "customDuration": r"""function()
                        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
                        local b = buffs and (buffs.bySpellId[12975] or buffs.byName["Last Stand"])
                        if b and b.duration and b.duration > 0 then
                            return b.duration, b.expirationTime
                        end
                        local start, duration = GetSpellCooldown("Last Stand")
                        if start and duration and duration > 1.5 then
                            return duration, start + duration
                        end
                        return 0, 0
                    end""",
                    "customIcon": r"""function()
                        return "Interface\\Icons\\Spell_Nature_ShamanRage"
                    end""",
                    "customText": r"""function()
                        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
                        local b = buffs and (buffs.bySpellId[12975] or buffs.byName["Last Stand"])
                        if b then return "|cFF00FF00+30%|r" end
                        return ""
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            },
            "activeTriggerMode": -10,
        },
        "subRegions": [
            {"type": "subbackground"},
            make_subtext("%p", justify="CENTER", anchor_point="CENTER", font_size=11, y_offset=0),
            make_subtext("LS", justify="RIGHT", anchor_point="INNER_BOTTOMRIGHT", font_size=8, y_offset=-2, x_offset=2),
        ],
    })

    # 13 - Boots warTank (Slot 8 / Enraged Regeneration)
    auras.append({
        "id": "13 - Boots warTank",
        "uid": "PWHUD_UTIL_BOOTS",
        "parent": "Class Warrior (Protection)",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 28,
        "height": 28,
        "xOffset": 175,
        "yOffset": -45,
        "displayIcon": "Interface\\Icons\\Ability_Warrior_EnragedRegeneration",
        "cooldown": True,
        "cooldownSwipe": True,
        "triggers": {
            1: {
                "trigger": {
                    "type": "custom",
                    "custom_type": "status",
                    "check": "update",
                    "custom": r"""function() return true end""",
                    "customDuration": r"""function()
                        local start, duration = GetInventoryItemCooldown("player", 8)
                        if start and duration and duration > 1.5 then
                            return duration, start + duration
                        end
                        local s2, d2 = GetSpellCooldown("Enraged Regeneration")
                        if s2 and d2 and d2 > 1.5 then
                            return d2, s2 + d2
                        end
                        return 0, 0
                    end""",
                    "customIcon": r"""function()
                        local start, duration = GetInventoryItemCooldown("player", 8)
                        if start and duration and duration > 1.5 then
                            return GetInventoryItemTexture("player", 8) or "Interface\\Icons\\Ability_Warrior_EnragedRegeneration"
                        end
                        return "Interface\\Icons\\Ability_Warrior_EnragedRegeneration"
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            },
            "activeTriggerMode": -10,
        },
        "subRegions": [
            {"type": "subbackground"},
            make_subtext("%p", justify="CENTER", anchor_point="CENTER", font_size=11, y_offset=0),
            make_subtext("BOT", justify="RIGHT", anchor_point="INNER_BOTTOMRIGHT", font_size=8, y_offset=-2, x_offset=2),
        ],
    })

    return auras
