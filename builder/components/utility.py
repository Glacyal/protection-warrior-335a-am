"""
Modulo Componente: 11-13 - Utility, Trinkets & Core Bootstrap (Warrior Protection)
==================================================================================
Fornisce il bootstrap globale Lua (_G.PWHUD_*) e i tracker per:
1. 11 - Trinket 1 warTank (Slot 13: Sindragosa's Fang, Glyph of Indomitability, Coin, Scarab, ecc.)
2. 12 - Trinket 2 warTank (Slot 14: Corroded Skeleton Key, Black Heart, Onyxia Talisman, ecc.)
3. 13 - Gloves & Boots warTank (Slot 10: Reticulated Armor Webbing / Hyperspeed, Slot 8: Nitro Boosts)
"""
import copy
from builder.core.constants import PROT_WARRIOR_LOAD, FONT_EXPRESSWAY
from builder.core.helpers import make_subtext


# =============================================================================
# LOGICA LUA CONDIVISA CENTRALIZZATA (BOOTSTRAP TANK WARRIOR)
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
                rank = rank,
                icon = icon,
                count = count or 0,
                duration = duration or 0,
                expirationTime = expirationTime or 0,
                spellId = spellId
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
                count = count or 0,
                duration = duration or 0,
                expirationTime = expirationTime or 0,
                spellId = spellId,
                icon = icon
            }
            c.list[#c.list + 1] = d
            if spellId then c.bySpellId[spellId] = d end
            if name then c.byName[name] = d end
        end
        _G.PWHUD_PlayerDebuffCache = c
        return c
    end

    _G.PWHUD_GetTargetDebuffs = _G.PWHUD_GetTargetDebuffs or function()
        local now_td = GetTime()
        local c = _G.PWHUD_TargetDebuffCache
        if c and c.time == now_td then return c end
        c = { time = now_td, bySpellId = {}, byName = {}, list = {}, sunderCount = 0, sunderExp = 0, hasDemo = false, demoExp = 0, hasThunder = false, thunderExp = 0 }
        if not UnitExists("target") then
            _G.PWHUD_TargetDebuffCache = c
            return c
        end
        for i = 1, 40 do
            local name, rank, icon, count, debuffType, duration, expirationTime, unitCaster, isStealable, shouldConsolidate, spellId = UnitDebuff("target", i)
            if not name then break end
            local d = {
                name = name,
                count = count or 0,
                duration = duration or 0,
                expirationTime = expirationTime or 0,
                spellId = spellId
            }
            c.list[#c.list + 1] = d
            if spellId then c.bySpellId[spellId] = d end
            if name then c.byName[name] = d end

            -- Sunder Armor / Expose Armor check
            if name == "Sunder Armor" or spellId == 47437 or spellId == 7386 then
                c.sunderCount = count > 0 and count or 1
                c.sunderExp = expirationTime or 0
            elseif name == "Expose Armor" or spellId == 8647 then
                c.sunderCount = 5
                c.sunderExp = expirationTime or 0
            end

            -- Demoralizing Shout / Vindication check (-AP)
            if name == "Demoralizing Shout" or name == "Demoralizing Roar" or name == "Vindication" or spellId == 47436 then
                c.hasDemo = true
                c.demoExp = expirationTime or 0
            end

            -- Thunder Clap / Frost Fever / Judgements of the Just (-20% atk speed)
            if name == "Thunder Clap" or name == "Frost Fever" or name == "Judgements of the Just" or name == "Infected Wounds" or spellId == 47502 then
                c.hasThunder = true
                c.thunderExp = expirationTime or 0
            end
        end
        _G.PWHUD_TargetDebuffCache = c
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
            c.list[#c.list + 1] = { name = name, spellId = spellId }
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
        local isChannel = false
        if not spell then
            spell, rank, displayName, icon, startTime, endTime, isTradeSkill, notInterruptible = UnitChannelInfo("target")
            isChannel = (spell ~= nil)
        end
        if not spell then return nil end

        local form = GetShapeshiftForm() -- 1 = Battle, 2 = Defensive, 3 = Berserker
        local hasShield = (GetInventoryItemID("player", 17) ~= nil)
        local now = GetTime()
        local sStart, sDur = GetSpellCooldown("Shield Bash")
        local shieldBashReady = (sDur == nil or sDur <= 1.5 or (sStart + sDur <= now))
        local pStart, pDur = GetSpellCooldown("Pummel")
        local pummelReady = (pDur == nil or pDur <= 1.5 or (pStart + pDur <= now))
        local cStart, cDur = GetSpellCooldown("Concussion Blow")
        local concReady = (cDur == nil or cDur <= 1.5 or (cStart + cDur <= now))
        local swStart, swDur = GetSpellCooldown("Shockwave")
        local shockwaveReady = (swDur == nil or swDur <= 1.5 or (swStart + swDur <= now))

        local res = {
            spellName = spell,
            icon = icon,
            notInterruptible = notInterruptible,
            remaining = (endTime and (endTime / 1000 - now)) or 0,
            recommended = "Shield Bash",
            recommendedIcon = "Interface\\Icons\\Ability_Warrior_ShieldBash",
            canKick = true,
            reason = "OK"
        }

        if notInterruptible then
            res.canKick = false
            res.recommended = "IMMUNE (Reflect/Wall)"
            res.recommendedIcon = "Interface\\Icons\\Ability_Warrior_ShieldReflection"
            res.reason = "IMMUNE"
            return res
        end

        if (form == 2 or form == 1) and hasShield and shieldBashReady then
            res.recommended = "Shield Bash"
            res.recommendedIcon = "Interface\\Icons\\Ability_Warrior_ShieldBash"
        elseif form == 3 and pummelReady then
            res.recommended = "Pummel"
            res.recommendedIcon = "Interface\\Icons\\INV_Gauntlets_04"
        elseif form == 2 and not shieldBashReady and pummelReady then
            res.recommended = "Stance Dance -> Pummel"
            res.recommendedIcon = "Interface\\Icons\\INV_Gauntlets_04"
        elseif concReady then
            res.recommended = "Stun: Concussion Blow"
            res.recommendedIcon = "Interface\\Icons\\Ability_ThunderBolt"
        elseif shockwaveReady then
            res.recommended = "Stun: Shockwave"
            res.recommendedIcon = "Interface\\Icons\\Ability_Warrior_Shockwave"
        else
            res.recommended = "Kicks on Cooldown!"
            res.recommendedIcon = "Interface\\Icons\\Spell_Fire_SelfDestruct"
            res.canKick = false
            res.reason = "ON_CD"
        end
        return res
    end

    _G.PWHUD_GetEmergencyCD = _G.PWHUD_GetEmergencyCD or function()
        local curHP = UnitHealth("player")
        local maxHP = UnitHealthMax("player")
        if maxHP == 0 then return nil end
        local pct = (curHP / maxHP) * 100
        if pct > 35 then return nil end

        local now = GetTime()
        local function isReady(name)
            local s, d = GetSpellCooldown(name)
            return (d == nil or d <= 1.5 or (s + d <= now))
        end

        if isReady("Shield Wall") then
            return {
                action = "SHIELD WALL (-60% DR)",
                icon = "Interface\\Icons\\Ability_Warrior_ShieldWall",
                urgency = "CRITICAL",
                pct = pct
            }
        elseif isReady("Last Stand") then
            return {
                action = "LAST STAND (+30% HP)",
                icon = "Interface\\Icons\\Spell_Nature_ShamanRage",
                urgency = "HIGH",
                pct = pct
            }
        elseif isReady("Shield Block") then
            return {
                action = "SHIELD BLOCK (100% BLK)",
                icon = "Interface\\Icons\\Ability_Defensive",
                urgency = "MEDIUM",
                pct = pct
            }
        elseif isReady("Enraged Regeneration") then
            return {
                action = "ENRAGED REGEN (+30% HEAL)",
                icon = "Interface\\Icons\\Ability_Warrior_EnragedRegeneration",
                urgency = "MEDIUM",
                pct = pct
            }
        else
            return {
                action = "HEALTHSTONE / POTION!",
                icon = "Interface\\Icons\\INV_Stone_04",
                urgency = "PANIC",
                pct = pct
            }
        end
    end

    _G.PWHUD_GetTankStats = _G.PWHUD_GetTankStats or function()
        local baseDef, armorDef = UnitDefense("player")
        local totalDef = (baseDef or 0) + (armorDef or 0)
        local dodge = GetDodgeChance() or 0
        local parry = GetParryChance() or 0
        local block = GetBlockChance() or 0
        local miss = 5.0 + math.max(0, (totalDef - 400) * 0.04)
        local ctc = dodge + parry + block + miss
        local sbv = GetShieldBlock() or 0
        local baseArmor, effectiveArmor, armorVal, posBuff, negBuff = UnitArmor("player")
        effectiveArmor = effectiveArmor or baseArmor or 0
        local armorDR = (effectiveArmor / (effectiveArmor + 16635)) * 100
        local hitRating = GetCombatRating(6) or 0
        local hitBonus = GetCombatRatingBonus(6) or 0
        local exp = GetExpertise() or 0
        local hpMax = UnitHealthMax("player") or 1
        local ehp = hpMax / math.max(0.01, (1 - (armorDR / 100)))

        return {
            defense = totalDef,
            isCritImmune = (totalDef >= 540),
            dodge = dodge,
            parry = parry,
            block = block,
            miss = miss,
            ctc = ctc,
            sbv = sbv,
            armor = effectiveArmor,
            armorDR = armorDR,
            hitBonus = hitBonus,
            hitRating = hitRating,
            expertise = exp,
            hpMax = hpMax,
            ehp = ehp
        }
    end

    _G.PWHUD_CoreInitDone = true
end"""


def build_utility_auras() -> list[dict]:
    """Costruisce le aure per la riga di utilità (Trinkets, Gloves, Boots)."""
    auras = []

    # 11 - Trinket 1 warTank
    auras.append({
        "id": "11 - Trinket 1 warTank",
        "uid": "PWHUD_TRINKET_1",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 30,
        "height": 30,
        "xOffset": -60,
        "yOffset": -45,
        "anchorPoint": "CENTER",
        "selfPoint": "CENTER",
        "displayIcon": "Interface\\Icons\\INV_Jewelry_TrinketPVP_02",
        "load": copy.deepcopy(PROT_WARRIOR_LOAD),
        "triggers": {
            "1": {
                "trigger": {
                    "type": "custom",
                    "custom_type": "status",
                    "check": "update",
                    "custom": r"""function()
                        if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                        local itemID = GetInventoryItemID("player", 13)
                        return (itemID ~= nil)
                    end""",
                    "customDuration": r"""function()
                        local start, duration = GetInventoryItemCooldown("player", 13)
                        if start and duration and duration > 1.5 then
                            return duration, start + duration
                        end
                        return 0, 0
                    end""",
                    "customIcon": r"""function()
                        return GetInventoryItemTexture("player", 13) or "Interface\\Icons\\INV_Jewelry_TrinketPVP_02"
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            }
        },
        "subRegions": [
            make_subtext("%p", "CENTER", "CENTER", 11, 0, 0),
            make_subtext("T1", "RIGHT", "INNER_BOTTOMRIGHT", 9, 2, -2)
        ]
    })

    # 12 - Trinket 2 warTank
    auras.append({
        "id": "12 - Trinket 2 warTank",
        "uid": "PWHUD_TRINKET_2",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 30,
        "height": 30,
        "xOffset": -25,
        "yOffset": -45,
        "anchorPoint": "CENTER",
        "selfPoint": "CENTER",
        "displayIcon": "Interface\\Icons\\INV_Jewelry_TrinketPVP_02",
        "load": copy.deepcopy(PROT_WARRIOR_LOAD),
        "triggers": {
            "1": {
                "trigger": {
                    "type": "custom",
                    "custom_type": "status",
                    "check": "update",
                    "custom": r"""function()
                        if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                        local itemID = GetInventoryItemID("player", 14)
                        return (itemID ~= nil)
                    end""",
                    "customDuration": r"""function()
                        local start, duration = GetInventoryItemCooldown("player", 14)
                        if start and duration and duration > 1.5 then
                            return duration, start + duration
                        end
                        return 0, 0
                    end""",
                    "customIcon": r"""function()
                        return GetInventoryItemTexture("player", 14) or "Interface\\Icons\\INV_Jewelry_TrinketPVP_02"
                    end"""
                },
                "untrigger": {"type": "custom", "custom": "function() return false end"}
            }
        },
        "subRegions": [
            make_subtext("%p", "CENTER", "CENTER", 11, 0, 0),
            make_subtext("T2", "RIGHT", "INNER_BOTTOMRIGHT", 9, 2, -2)
        ]
    })

    # 13 - Gloves & Boots warTank
    auras.append({
        "id": "13 - Gloves & Boots warTank",
        "uid": "PWHUD_GLOVES_BOOTS",
        "regionType": "icon",
        "internalVersion": 90,
        "width": 30,
        "height": 30,
        "xOffset": 10,
        "yOffset": -45,
        "anchorPoint": "CENTER",
        "selfPoint": "CENTER",
        "displayIcon": "Interface\\Icons\\INV_Gauntlets_04",
        "load": copy.deepcopy(PROT_WARRIOR_LOAD),
        "triggers": {
            "1": {
                "trigger": {
                    "type": "custom",
                    "custom_type": "status",
                    "check": "update",
                    "custom": r"""function()
                        if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
                        local itemID = GetInventoryItemID("player", 10)
                        return (itemID ~= nil)
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
            }
        },
        "subRegions": [
            make_subtext("%p", "CENTER", "CENTER", 11, 0, 0),
            make_subtext("GLV", "RIGHT", "INNER_BOTTOMRIGHT", 9, 2, -2)
        ]
    })

    return auras
