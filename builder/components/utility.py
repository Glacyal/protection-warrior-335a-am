"""
Modulo Componente: 05-13 - Utility Row (Warrior Protection)
===========================================================
Gestisce la riga orizzontale di utilità a y = -45 con riposizionamento dinamico
centrato naturale (da 3 a 10 icone) in base all'equipaggiamento e alle abilità:
1. 05 - Trinket 1 warTank (Slot 13: Fang, Indomitability, Coin, Scarab, Skeleton Key, Black Heart, DBW, STS, ecc.)
2. 06 - Trinket 2 warTank (Slot 14: Fang, Indomitability, Coin, Scarab, Skeleton Key, Black Heart, DBW, STS, ecc.)
3. 06b - Ring warTank (Slot 11/12: Ashen Band of Endless Courage +Armor proc / Endless Vengeance +AP, 60s ICD)
4. 07 - Cloak warTank (Slot 15: Flexweave / Paracadute / Incanti)
5. 08 - Tier Set warTank (T10 Ymirjar Lord 2P/4P, T9 Wrynn/Hellscream 2P/4P, T8 Siegebreaker, T7 Dreadnaught)
6. 09 - Enchants warTank (Slot 16: Blade Ward parry proc, Blood Draining con 5 stack e heal emergenza, Mongoose, Berserking)
7. 10 - Gloves warTank (Slot 10: Reticulated Armor Webbing +885 Armor / Acceleratori Ipersonici)
8. 11 - Shield Wall (Spell 871: durata attiva 12s, ricarica e glow emergenza <35% HP)
9. 12 - Last Stand (Spell 12975: durata attiva 20s, ricarica e glow emergenza <35% HP)
10. 13 - Boots warTank (Slot 8: Acceleratori a Nitro Boosts / Enraged Regeneration fallback)
"""
from builder.core.helpers import make_subtext


# =============================================================================
# LOGICA LUA CONDIVISA CENTRALIZZATA (BOOTSTRAP UTILITY TANK WARRIOR)
# =============================================================================
SHARED_WARRIOR_CORE_BOOTSTRAP_LUA = r"""function()
    _G.PWHUD_GetPlayerBuffs = _G.PWHUD_GetPlayerBuffs or function()
        local now_b = GetTime()
        local c = _G.PWHUD_BuffCache
        if c and c.time == now_b then
            return c
        end
        c = { time = now_b, bySpellId = {}, byName = {}, list = {} }
        for i = 1, 40 do
            local name, rank, icon, count, debuffType, duration, expirationTime, unitCaster, isStealable, shouldConsolidate, spellId = UnitBuff("player", i)
            if not name then break end
            local b = {
                name = name,
                rank = rank,
                icon = icon,
                count = count or 0,
                debuffType = debuffType,
                duration = duration or 0,
                expirationTime = expirationTime or 0,
                unitCaster = unitCaster,
                isStealable = isStealable,
                shouldConsolidate = shouldConsolidate,
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

    local CURRENT_BUILD_VER = 48
    if _G.PWHUD_CoreInitDone and _G.PWHUD_BUILD_VER == CURRENT_BUILD_VER then return end
    _G.PWHUD_BUILD_VER = CURRENT_BUILD_VER
    _G.PWHUD_SlotCache = {}
    _G.PWHUD_BuffCache = nil

    if _G.PWHUD_ICD then
        for _, state in pairs(_G.PWHUD_ICD) do
            if state then state.isProc = false end
        end
    else
        _G.PWHUD_ICD = {
            [8]  = { lastStart = 0, lastEnd = 0, isProc = false, lastItemID = 0 },
            [10] = { lastStart = 0, lastEnd = 0, isProc = false, lastItemID = 0 },
            [13] = { lastStart = 0, lastEnd = 0, isProc = false, lastItemID = 0 },
            [14] = { lastStart = 0, lastEnd = 0, isProc = false, lastItemID = 0 },
            [15] = { lastStart = 0, lastEnd = 0, isProc = false, lastItemID = 0 },
        }
    end


    -- =========================================================================
    -- BANCA DATI MONILI WOTLK 3.3.5A (TANK & PHYSICAL DPS / THREAT)
    -- =========================================================================
    _G.PWHUD_TrinketDB = {
        -- ====================================================================
        -- TANK MITIGATION & SURVIVAL TRINKETS
        -- ====================================================================
        -- Corroded Skeleton Key (50356 - 60 Emblem of Frost)
        [50356] = { keywords = { "corroded", "skeleton", "key", "chiave", "scheletro", "corroso", "hardened", "skin" }, spellIds = { [71586] = true }, icd = 120, dur = 30, onUse = true },

        -- Sindragosa's Flawless Fang (Normal 50361, Heroic 50364 - ICC 25 Sindragosa)
        [50361] = { keywords = { "flawless", "fang", "zanna", "impeccabile", "sindragosa", "ward", "protezione" }, spellIds = { [71635] = true, [71638] = true }, icd = 60, dur = 10, onUse = true },
        [50364] = { keywords = { "flawless", "fang", "zanna", "impeccabile", "sindragosa", "ward", "protezione" }, spellIds = { [71635] = true, [71638] = true }, icd = 60, dur = 10, onUse = true },

        -- Satrina's Impeding Scarab / Juggernaut's Vitality (ToC 25: 47080, 47088, 47451, 47290)
        [47080] = { keywords = { "impeding", "scarab", "scarabeo", "satrina", "juggernaut", "vitality", "vitalita", "fortitude" }, spellIds = { [67751] = true, [67753] = true }, icd = 180, dur = 15, onUse = true },
        [47088] = { keywords = { "impeding", "scarab", "scarabeo", "satrina", "juggernaut", "vitality", "vitalita", "fortitude" }, spellIds = { [67751] = true, [67753] = true }, icd = 180, dur = 15, onUse = true },
        [47451] = { keywords = { "impeding", "scarab", "scarabeo", "satrina", "juggernaut", "vitality", "vitalita", "fortitude" }, spellIds = { [67751] = true, [67753] = true }, icd = 180, dur = 15, onUse = true },
        [47290] = { keywords = { "impeding", "scarab", "scarabeo", "satrina", "juggernaut", "vitality", "vitalita", "fortitude" }, spellIds = { [67751] = true, [67753] = true }, icd = 180, dur = 15, onUse = true },

        -- Unidentifiable Organ (Normal 50341, Heroic 50344 - ICC 10 Putricide)
        [50341] = { keywords = { "unidentifiable", "organ", "organo", "nonidentificabile", "putricide", "armor", "armatura" }, spellIds = { [71570] = true, [71571] = true, [71572] = true }, icd = 0, dur = 10 },
        [50344] = { keywords = { "unidentifiable", "organ", "organo", "nonidentificabile", "putricide", "armor", "armatura" }, spellIds = { [71570] = true, [71571] = true, [71572] = true }, icd = 0, dur = 10 },

        -- The Black Heart (47216 - ToC 5 Normal)
        [47216] = { keywords = { "black", "heart", "cuore", "nero", "hardened", "indurito" }, spellIds = { [67744] = true }, icd = 45, dur = 10 },

        -- Onyxia Blood Talisman (49487 - Onyxia 25)
        [49487] = { keywords = { "onyxia", "blood", "talisman", "sangue", "talismano" }, spellIds = { [67596] = true }, icd = 45, dur = 10 },

        -- Glyph of Indomitability (47735 - 50 Emblem of Triumph)
        [47735] = { keywords = { "glyph", "indomitability", "glifo", "indomabilita", "dodge", "schivata" }, spellIds = { [67694] = true }, icd = 120, dur = 20, onUse = true },

        -- Heart of Iron (45158 - Ulduar 10 XT-002)
        [45158] = { keywords = { "heart", "iron", "cuore", "ferro", "dodge" }, spellIds = { [64792] = true }, icd = 120, dur = 20, onUse = true },

        -- Lavanthor's Talisman (40683 - Violet Hold)
        [40683] = { keywords = { "lavanthor", "talisman", "talismano", "blocco", "block" }, spellIds = { [60527] = true }, icd = 120, dur = 20, onUse = true },

        -- Baza's / Ick's Rotten Thumb (50235 - Pit of Saron Heroic)
        [50235] = { keywords = { "rotten", "thumb", "pollice", "marcio", "ick" }, spellIds = { [71490] = true }, icd = 180, dur = 15, onUse = true },

        -- Figurine - Monarch Crab (44063 - Jewelcrafting)
        [44063] = { keywords = { "monarch", "crab", "granchio", "reale" }, spellIds = { [59672] = true }, icd = 120, dur = 20, onUse = true },

        -- Seal of the Pantheon (36993 - Halls of Lightning)
        [36993] = { keywords = { "pantheon", "sigillo", "seal" }, spellIds = { [51433] = true }, icd = 45, dur = 10 },

        -- Offering of Sacrifice (37800 - Gundrak)
        [37800] = { keywords = { "offering", "sacrifice", "offerta", "sacrificio" }, spellIds = { [54808] = true }, icd = 120, dur = 20, onUse = true },

        -- Defender's Code (40257 - Naxxramas 25)
        [40257] = { keywords = { "defender", "code", "codice", "difensore" }, spellIds = { [60488] = true }, icd = 120, dur = 20, onUse = true },

        -- Super-Charged Iron Core (40373 - Naxxramas 25)
        [40373] = { keywords = { "iron", "core", "nucleo", "ferro" }, spellIds = { [60492] = true }, icd = 120, dur = 20, onUse = true },

        -- Fervor of the Frostborn / Eitrigg's Oath (47084, 47087 - ToC 25)
        [47084] = { keywords = { "fervor", "frostborn", "eitrigg", "oath", "giuramento" }, spellIds = { [67756] = true }, icd = 120, dur = 20, onUse = true },
        [47087] = { keywords = { "fervor", "frostborn", "eitrigg", "oath", "giuramento" }, spellIds = { [67756] = true }, icd = 120, dur = 20, onUse = true },

        -- Petrified Twilight Scale (Normal 54571, Heroic 54591 - RS 25 Halion)
        [54571] = { keywords = { "petrified", "twilight", "scale", "pietrificata", "crepuscolare" }, spellIds = { [75480] = true, [75482] = true }, icd = 45, dur = 10 },
        [54591] = { keywords = { "petrified", "twilight", "scale", "pietrificata", "crepuscolare" }, spellIds = { [75480] = true, [75482] = true }, icd = 45, dur = 10 },

        -- ====================================================================
        -- PHYSICAL DPS / THREAT TRINKETS (USED BY OFF-TANKS / AGGRO ROTATIONS)
        -- ====================================================================
        -- Deathbringer's Will (Normal 50362, Heroic 50363 - ICC 25 Saurfang)
        [50362] = { keywords = { "taunka", "vrykul", "irondwarf", "deathbringer", "nanodiferro", "forzadel", "forzadei", "agilitadel", "miradel", "volonta" }, spellIds = { [71484] = true, [71485] = true, [71486] = true, [71491] = true, [71492] = true, [71487] = true, [71556] = true, [71557] = true, [71558] = true, [71559] = true, [71560] = true, [71561] = true }, icd = 105, dur = 30 },
        [50363] = { keywords = { "taunka", "vrykul", "irondwarf", "deathbringer", "nanodiferro", "forzadel", "forzadei", "agilitadel", "miradel", "volonta" }, spellIds = { [71484] = true, [71485] = true, [71486] = true, [71491] = true, [71492] = true, [71487] = true, [71556] = true, [71557] = true, [71558] = true, [71559] = true, [71560] = true, [71561] = true }, icd = 105, dur = 30 },

        -- Sharpened Twilight Scale (Normal 54569, Heroic 54590 - RS 25 Halion)
        [54569] = { keywords = { "twilightprecision", "sharpenedtwilight", "twilight", "crepuscolare", "precisione" }, spellIds = { [75473] = true, [75474] = true, [75466] = true, [75456] = true }, icd = 45, dur = 15 },
        [54590] = { keywords = { "twilightprecision", "sharpenedtwilight", "twilight", "crepuscolare", "precisione" }, spellIds = { [75473] = true, [75474] = true, [75466] = true, [75456] = true }, icd = 45, dur = 15 },

        -- Death's Choice / Verdict (47115, 47131, 47303, 47464 - ToC 25 Twins)
        [47115] = { keywords = { "paragon", "choice", "verdict", "scelta", "verdetto", "esempio", "forza", "strength" }, spellIds = { [67708] = true, [67703] = true, [67707] = true }, icd = 45, dur = 15 },
        [47131] = { keywords = { "paragon", "choice", "verdict", "scelta", "verdetto", "esempio", "forza", "strength" }, spellIds = { [67773] = true, [67772] = true, [67771] = true }, icd = 45, dur = 15 },
        [47303] = { keywords = { "paragon", "choice", "verdict", "scelta", "verdetto", "esempio", "forza", "strength" }, spellIds = { [67708] = true, [67703] = true, [67707] = true }, icd = 45, dur = 15 },
        [47464] = { keywords = { "paragon", "choice", "verdict", "scelta", "verdetto", "esempio", "forza", "strength" }, spellIds = { [67773] = true, [67772] = true, [67771] = true }, icd = 45, dur = 15 },

        -- Whispering Fanged Skull (Normal 50342, Heroic 50343 - ICC 10 Lady Deathwhisper)
        [50342] = { keywords = { "whisperingfangedskull", "fanged", "skull", "teschio", "sussurrante" }, spellIds = { [71541] = true, [71540] = true }, icd = 45, dur = 15 },
        [50343] = { keywords = { "whisperingfangedskull", "fanged", "skull", "teschio", "sussurrante" }, spellIds = { [71541] = true, [71540] = true }, icd = 45, dur = 15 },

        -- Herkuml War Token (50355 - 60 Frost Emblems)
        [50355] = { keywords = { "herkuml", "token" }, spellIds = { [71396] = true }, icd = 0, dur = 10 },

        -- Needle-Encrusted Scorpion (50198 - Forge of Souls Heroic)
        [50198] = { keywords = { "nowisthetime", "oraeilmomento", "needleencrusted", "scorpion", "scorpione" }, spellIds = { [71403] = true, [71401] = true }, icd = 45, dur = 10 },

        -- Mjolnir Runestone (45931, 45866 - Ulduar 10 Thorim)
        [45931] = { keywords = { "mjolnirrunestone", "runestone", "mjolnir", "pietrarunica" }, spellIds = { [65019] = true, [65014] = true }, icd = 45, dur = 10 },
        [45866] = { keywords = { "mjolnirrunestone", "runestone", "mjolnir", "pietrarunica" }, spellIds = { [65019] = true, [65014] = true }, icd = 45, dur = 10 },

        -- Comet's Trail (45609 - Ulduar 25 Algalon)
        [45609] = { keywords = { "cometstrail", "comet", "cometa" }, spellIds = { [64772] = true }, icd = 45, dur = 10 },

        -- Darkmoon Card: Greatness (44253, 44254, 44255, 42987)
        [44253] = { keywords = { "greatness", "nobilt", "grandezza", "forza", "strength" }, spellIds = { [60229] = true, [60233] = true, [60234] = true, [60235] = true }, icd = 45, dur = 15 },
        [44254] = { keywords = { "greatness", "nobilt", "grandezza", "forza", "strength" }, spellIds = { [60229] = true, [60233] = true, [60234] = true, [60235] = true }, icd = 45, dur = 15 },
        [44255] = { keywords = { "greatness", "nobilt", "grandezza", "forza", "strength" }, spellIds = { [60229] = true, [60233] = true, [60234] = true, [60235] = true }, icd = 45, dur = 15 },
        [42987] = { keywords = { "greatness", "nobilt", "grandezza", "forza", "strength" }, spellIds = { [60229] = true, [60233] = true, [60234] = true, [60235] = true }, icd = 45, dur = 15 },

        -- Grim Toll (40256 - Naxxramas 25)
        [40256] = { keywords = { "grimtoll", "toll", "rintocco" }, spellIds = { [60486] = true, [60485] = true }, icd = 45, dur = 10 },

        -- Mirror of Truth (40684 - 40 Emblem of Heroism)
        [40684] = { keywords = { "reflection", "torment", "riflesso", "tormento", "mirroroftruth", "mirror", "truth", "specchio" }, spellIds = { [60065] = true, [60064] = true }, icd = 45, dur = 10 },

        -- PvP Medallions / Battlemaster
        [42122] = { keywords = { "medallion", "medaglione" }, icd = 120, dur = 0, onUse = true },
        [42123] = { keywords = { "medallion", "medaglione" }, icd = 120, dur = 0, onUse = true },
        [51377] = { keywords = { "medallion", "medaglione" }, icd = 120, dur = 0, onUse = true },
        [51378] = { keywords = { "medallion", "medaglione" }, icd = 120, dur = 0, onUse = true },
        [42133] = { keywords = { "battlemaster" }, spellIds = { [59754] = true }, icd = 180, dur = 15, onUse = true },
        [44064] = { keywords = { "battlemaster" }, spellIds = { [59754] = true }, icd = 180, dur = 15, onUse = true },
    }

    _G.PWHUD_RingDB = {
        -- Ashen Band of Endless Courage (Exalted Tank - 277)
        [50404] = { keywords = { "frostforgeddefender", "defender", "difensore", "armor of the ashen", "armatura del verdetto", "armatura" }, spellIds = { [72414] = true, [72412] = true }, icd = 60, dur = 10 },
        -- Ashen Band of Unmatched Courage (Revered Tank - 268)
        [50403] = { keywords = { "frostforgeddefender", "defender", "difensore", "armor of the ashen", "armatura del verdetto", "armatura" }, spellIds = { [72414] = true, [72412] = true }, icd = 60, dur = 10 },
        -- Ashen Band of Greater Courage (Honored Tank - 259)
        [50402] = { keywords = { "frostforgeddefender", "defender", "difensore", "armor of the ashen", "armatura del verdetto", "armatura" }, spellIds = { [72414] = true, [72412] = true }, icd = 60, dur = 10 },
        -- Ashen Band of Courage (Friendly Tank - 251)
        [50401] = { keywords = { "frostforgeddefender", "defender", "difensore", "armor of the ashen", "armatura del verdetto", "armatura" }, spellIds = { [72414] = true, [72412] = true }, icd = 60, dur = 10 },

        -- Ashen Band of Endless Vengeance (Exalted Melee DPS - 277)
        [50402] = { keywords = { "frostforgedchampion", "champion", "campione" }, spellIds = { [72412] = true, [72414] = true }, icd = 60, dur = 10 },
        [50401] = { keywords = { "frostforgedchampion", "champion", "campione" }, spellIds = { [72412] = true, [72414] = true }, icd = 60, dur = 10 },
        [50398] = { keywords = { "frostforgedchampion", "champion", "campione" }, spellIds = { [72412] = true, [72414] = true }, icd = 60, dur = 10 },
        [50397] = { keywords = { "frostforgedchampion", "champion", "campione" }, spellIds = { [72412] = true, [72414] = true }, icd = 60, dur = 10 },

        -- Band of the Eternal Champion (TBC Hyjal Exalted Melee DPS - 152)
        [29301] = { keywords = { "eternalchampion" }, spellIds = { [35081] = true }, icd = 60, dur = 10 },
    }
    _G.PWHUD_RingState = _G.PWHUD_RingState or { lastStart = 0, lastEnd = 0, isProc = false, lastItemID = 0 }

    _G.PWHUD_WeaponEnchantDB = {
        [3870] = { name = "Blood Draining", spellId = 64440, dur = 20, icon = "Interface\\Icons\\Spell_Shadow_BloodBoil" },
        [3869] = { name = "Blade Ward", spellId = 64442, dur = 10, icon = "Interface\\Icons\\Ability_Warrior_WeaponMastery" },
        [2673] = { name = "Mongoose", spellId = 28093, dur = 15, icon = "Interface\\Icons\\Spell_Nature_Possess" },
        [3789] = { name = "Berserking", spellId = 59620, dur = 15, icon = "Interface\\Icons\\Spell_Nature_BloodLust" },
        [3225] = { name = "Executioner", spellId = 42976, dur = 15, icon = "Interface\\Icons\\INV_Sword_48" },
        [1900] = { name = "Crusader", spellId = 20007, dur = 15, icon = "Interface\\Icons\\Spell_Holy_BlessingOfProtection" },
        [3830] = { name = "Lifeward", spellId = 60691, dur = 10, icon = "Interface\\Icons\\Spell_Holy_Restoration" },
        [3790] = { name = "Black Magic", spellId = 59626, dur = 10, icon = "Interface\\Icons\\Spell_Shadow_ShadowBolt" },
        [3239] = { name = "Icebreaker", spellId = 44525, dur = 5, icon = "Interface\\Icons\\Spell_Frost_FrostNova" },
        [3251] = { name = "Giant Slayer", spellId = 44578, dur = 10, icon = "Interface\\Icons\\Ability_Racial_Avatar" },
        [3273] = { name = "Deathfrost", spellId = 46578, dur = 8, icon = "Interface\\Icons\\Spell_Frost_FrostArmor" },
        [1898] = { name = "Unholy Weapon", spellId = 20004, dur = 10, icon = "Interface\\Icons\\Spell_Shadow_ShadowWordDominate" },
        [803]  = { name = "Fiery Weapon", spellId = 13897, dur = 5, icon = "Interface\\Icons\\Spell_Fire_FlameBlades" },
        [1899] = { name = "Lifestealing", spellId = 20005, dur = 5, icon = "Interface\\Icons\\Spell_Shadow_LifeDrain02" },
    }
    _G.PWHUD_StaticWeaponEnchants = {
        [3851] = true, -- Titanguard (+30 Stamina)
        [195]  = true, -- Titanguard legacy
        [3788] = true, -- Accuracy (+25 Hit & +25 Crit)
        [3731] = true, -- Titanium Weapon Chain (+28 Hit & -50% Disarm)
        [2667] = true, -- Superior Potency (+65 Attack Power 1H)
        [1103] = true, -- Exceptional Agility (+26 Agility)
        [1944] = true, -- Major Defense (+12 Defense)
        [3834] = true, -- Mighty Spellpower (+63 SP)
        [3827] = true, -- Massacre (+110 AP 2H)
        [3247] = true, -- Scourgebane (+140 AP vs Undead)
        [2674] = true, -- Greater Savagery (+85 AP 2H)
        [2666] = true, -- Potency (+20 Strength)
        [805]  = true, -- Major Striking (+7 Damage)
        [1897] = true, -- Superior Striking (+5 Damage)
        [249]  = true, -- Greater Striking (+4 Damage)
        [0]    = true, -- Nessun incanto
    }
    _G.PWHUD_WeaponState = _G.PWHUD_WeaponState or {
        [16] = { lastStart = 0, lastEnd = 0, isProc = false },
        [17] = { lastStart = 0, lastEnd = 0, isProc = false }
    }

    -- Cloak (Slot 15): Parachute tinker (Flexweave Underlay) and static enchants (+22 Agi, +16 Def, +225 Armor) are strictly suppressed.
    -- Only active combat proc enchants (Tailoring Swordguard Embroidery / Ricamo della Spada) are tracked.
    _G.PWHUD_CloakKeywords = { "swordguard", "ricamo della spada" }
    _G.PWHUD_CloakSpellIds = { [55775] = true }
    _G.PWHUD_CloakEnchantIDs = { [3730] = true }

    _G.PWHUD_GlovesSpellIds = { [54758] = true, [54998] = true }
    _G.PWHUD_GlovesKeywords = { "armor webbing", "reticulated", "corazza reticolare", "hyperspeed", "accelerat" }

    _G.PWHUD_BootsEnchantIDs = {
        [3606] = true,
        [3601] = true,
        [55016] = true,
        [54861] = true,
        [55004] = true,
        [54858] = true,
    }
    _G.PWHUD_BootsSpellIds = {
        [54861] = true,
        [55016] = true,
        [55004] = true,
        [54858] = true,
    }
    _G.PWHUD_BootsKeywords = { "nitro", "acceleratori a nitro", "acceleratori di nitro" }

    _G.PWHUD_T10_Pieces = {
        [50115] = true, [50116] = true, [50117] = true, [50118] = true, [50119] = true,
        [50859] = true, [50860] = true, [50861] = true, [50862] = true, [50863] = true,
        [51220] = true, [51221] = true, [51222] = true, [51223] = true, [51224] = true,
    }
    _G.PWHUD_T9_Pieces = {
        -- Alliance T9 Protection (232, 245, 258)
        [48590] = true, [48591] = true, [48592] = true, [48593] = true, [48594] = true,
        [48588] = true, [48587] = true, [48564] = true, [48589] = true, [48586] = true,
        [48584] = true, [48583] = true, [48581] = true, [48585] = true, [48582] = true,
        -- Horde T9 Protection (232, 245, 258)
        [48595] = true, [48596] = true, [48597] = true, [48598] = true, [48599] = true,
        [48571] = true, [48572] = true, [48573] = true, [48574] = true, [48575] = true,
        [48578] = true, [48577] = true, [48576] = true, [48579] = true, [48580] = true,
    }
    _G.PWHUD_T8_Pieces = {
        [46162] = true, [46163] = true, [46164] = true, [46166] = true, [46167] = true,
        [45424] = true, [45425] = true, [45426] = true, [45427] = true, [45428] = true,
    }
    _G.PWHUD_T7_Pieces = {
        [39638] = true, [39639] = true, [39640] = true, [39641] = true, [39642] = true,
        [40544] = true, [40545] = true, [40546] = true, [40547] = true, [40548] = true,
    }

    _G.PWHUD_CheckSlotEquipped = function(s)
        local now_t = GetTime()
        _G.PWHUD_SlotEquipCache = _G.PWHUD_SlotEquipCache or {}
        local cache = _G.PWHUD_SlotEquipCache[s]
        if cache and (now_t - cache.time < 0.25) then
            return cache.isEquipped
        end
        if not cache then
            cache = { time = 0, isEquipped = false }
            _G.PWHUD_SlotEquipCache[s] = cache
        end
        cache.time = now_t

        local itemID = GetInventoryItemID and GetInventoryItemID("player", s)
        if not itemID then
            local link = GetInventoryItemLink("player", s)
            if link then itemID = tonumber(link:match("item:(%d+)")) end
        end

        if s == 13 or s == 14 then
            local eq = (itemID ~= nil and itemID > 0)
            cache.isEquipped = eq
            return eq
        end

        if not itemID or itemID == 0 then
            cache.isEquipped = false
            return false
        end

        local itemLink = GetInventoryItemLink("player", s)
        local enchantID = nil
        if itemLink then
            enchantID = tonumber(itemLink:match("item:%d+:(%d+)"))
        end

        local function scanTT(keywords)
            local tt = _G.PWHUD_ScanTT
            if not tt then
                tt = CreateFrame("GameTooltip", "PWHUD_ScanTT", UIParent, "GameTooltipTemplate")
                tt:SetOwner(UIParent, "ANCHOR_NONE")
                for i = 1, 30 do
                    if not _G["PWHUD_ScanTTTextLeft"..i] then
                        local l = tt:CreateFontString("PWHUD_ScanTTTextLeft"..i, "ARTWORK", "GameTooltipText")
                        local r = tt:CreateFontString("PWHUD_ScanTTTextRight"..i, "ARTWORK", "GameTooltipText")
                        tt:AddFontStrings(l, r)
                    end
                end
                rawset(_G, "PWHUD_ScanTT", tt)
            end
            tt:ClearLines()
            tt:SetInventoryItem("player", s)
            for j = 1, (tt:NumLines() or 0) do
                local line = _G["PWHUD_ScanTTTextLeft"..j]
                local text = line and line:GetText()
                if text then
                    local lt = text:lower()
                    for _, kw in ipairs(keywords) do
                        if lt:find(kw, 1, true) then return true end
                    end
                end
            end
            return false
        end

        if s == 10 then
            local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
            if buffs and (buffs.bySpellId[54758] or buffs.bySpellId[54998]) then
                cache.isEquipped = true
                return true
            end
            if enchantID == 3604 or enchantID == 3859 then
                cache.isEquipped = true
                return true
            end
            if scanTT(_G.PWHUD_GlovesKeywords) then
                cache.isEquipped = true
                return true
            end
            local itemStart, itemDur = GetInventoryItemCooldown("player", 10)
            if itemDur and itemDur >= 45 then
                cache.isEquipped = true
                return true
            end
            cache.isEquipped = false
            return false
        end

        if s == 8 then
            local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
            if buffs then
                if (_G.PWHUD_BootsSpellIds and (buffs.bySpellId[54861] or buffs.bySpellId[54858] or buffs.bySpellId[55016])) then
                    cache.isEquipped = true
                    return true
                end
            end
            if enchantID and _G.PWHUD_BootsEnchantIDs and _G.PWHUD_BootsEnchantIDs[enchantID] then
                cache.isEquipped = true
                return true
            end
            local itemStart, itemDur = GetInventoryItemCooldown("player", 8)
            if itemDur and itemDur >= 60 then
                cache.isEquipped = true
                return true
            end
            if scanTT(_G.PWHUD_BootsKeywords) then
                cache.isEquipped = true
                return true
            end
            -- Fallback prot warrior: Enraged Regeneration
            local erStart, erDur = GetSpellCooldown("Enraged Regeneration")
            if erDur and erDur > 0 then
                cache.isEquipped = true
                return true
            end
            cache.isEquipped = true
            return true
        end

        if s == 15 then
            local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
            if buffs then
                for id, _ in pairs(_G.PWHUD_CloakSpellIds) do
                    if buffs.bySpellId[id] then
                        cache.isEquipped = true
                        return true
                    end
                end
            end
            if enchantID and _G.PWHUD_CloakEnchantIDs[enchantID] then
                cache.isEquipped = true
                return true
            end
            if scanTT(_G.PWHUD_CloakKeywords) then
                cache.isEquipped = true
                return true
            end
            cache.isEquipped = false
            return false
        end

        cache.isEquipped = true
        return true
    end

    _G.PWHUD_CheckSlot = function(slot)
        local now = GetTime()
        _G.PWHUD_SlotCache = _G.PWHUD_SlotCache or {}
        if _G.PWHUD_SlotCache[slot] and _G.PWHUD_SlotCache[slot].time == now then
            local c = _G.PWHUD_SlotCache[slot]
            return c.state, c.rem, c.dur, c.icon, c.spellId, c.buffName
        end

        local function finish(st, r, d, ic, spId, bNm)
            local c = _G.PWHUD_SlotCache[slot]
            if not c then
                c = {}
                _G.PWHUD_SlotCache[slot] = c
            end
            c.time = now
            c.state = st
            c.rem = r
            c.dur = d
            c.icon = ic
            c.spellId = spId
            c.buffName = bNm
            return st, r, d, ic, spId, bNm
        end

        local itemID = nil
        if GetInventoryItemID then itemID = GetInventoryItemID("player", slot) end
        if not itemID then
            local link = GetInventoryItemLink("player", slot)
            if link then itemID = tonumber(link:match("item:(%d+)")) end
        end
        local icdState = _G.PWHUD_ICD and _G.PWHUD_ICD[slot]
        if not icdState then
            _G.PWHUD_ICD = _G.PWHUD_ICD or {}
            icdState = { lastStart = 0, lastEnd = 0, isProc = false, lastItemID = 0 }
            _G.PWHUD_ICD[slot] = icdState
        end
        if icdState.lastItemID and itemID and icdState.lastItemID ~= itemID then
            icdState.lastStart = 0
            icdState.lastEnd = 0
            icdState.isProc = false
        end
        if itemID then icdState.lastItemID = itemID end

        local entry = itemID and _G.PWHUD_TrinketDB and _G.PWHUD_TrinketDB[itemID]
        if not entry and itemID and (slot == 13 or slot == 14) then
            local itemName = GetItemInfo and GetItemInfo(itemID)
            if not itemName then
                local link = GetInventoryItemLink("player", slot)
                if link then itemName = link:match("%[(.-)%]") end
            end
            if itemName then
                local inClean = itemName:lower():gsub("[%s%p%c]", "")
                for dbID, dbEntry in pairs(_G.PWHUD_TrinketDB or {}) do
                    if dbEntry.keywords then
                        for _, kw in ipairs(dbEntry.keywords) do
                            local kwClean = kw:lower():gsub("[%s%p%c]", "")
                            if inClean:find(kwClean, 1, true) then
                                entry = dbEntry
                                break
                            end
                        end
                    end
                    if entry then break end
                end
            end
        end
        local targetICD = (entry and entry.icd) or (slot == 10 and 60) or (slot == 8 and 180) or (slot == 15 and 45) or 45
        local defaultDur = (entry and entry.dur) or (slot == 10 and 12) or (slot == 8 and 5) or (slot == 15 and 15) or 15

        local itemStart, itemDur = GetInventoryItemCooldown("player", slot)
        if slot == 8 then
            if itemStart and itemDur and itemDur < 60 then itemStart, itemDur = 0, 0 end
            if not itemStart or itemDur == 0 or itemDur <= 1.5 then
                local sStart, sDur = GetSpellCooldown(54861)
                if sStart and sDur and sDur >= 60 then itemStart, itemDur = sStart, sDur end
            end
        elseif slot == 10 then
            if itemStart and itemDur and itemDur < 45 then itemStart, itemDur = 0, 0 end
            if not itemStart or itemDur == 0 or itemDur <= 1.5 then
                local sStart, sDur = GetSpellCooldown(54758)
                if sStart and sDur and sDur >= 45 then itemStart, itemDur = sStart, sDur end
            end
        end

        local isOnUseCooldown = false
        local remItemCD = 0
        if itemStart and itemDur and itemStart > 0 and itemDur > 1.5 then
            remItemCD = (itemStart + itemDur) - now
            if remItemCD > 0.1 then isOnUseCooldown = true end
        end

        local baseIcon = GetInventoryItemTexture("player", slot)
        if not baseIcon then
            baseIcon = (slot == 13 and "Interface\\Icons\\INV_Misc_Ornament_02") or
                       (slot == 14 and "Interface\\Icons\\INV_Misc_RubySanctum1") or
                       (slot == 15 and "Interface\\Icons\\INV_Misc_Cape_19") or
                       (slot == 10 and "Interface\\Icons\\INV_Gauntlets_26") or
                       (slot == 8  and "Interface\\Icons\\Ability_Kick") or nil
        end

        local foundBuff = false
        local remBuff = 0
        local durBuff = 0
        local buffIcon = nil
        local matchedSpellId = nil
        local matchedBuffName = nil

        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
        local buffList = buffs and buffs.list or {}

        for _, b in ipairs(buffList) do
            local isMatch = false
            if slot == 10 then
                if b.spellId == 54758 or (b.name and b.name:find("Hyperspeed")) then isMatch = true end
            elseif slot == 8 then
                if b.spellId == 54861 or (b.name and b.name:find("Nitro")) then isMatch = true end
            elseif slot == 15 then
                if b.spellId == 55775 or (b.name and (b.name:find("Swordguard") or b.name:find("Spada"))) then isMatch = true end
            elseif slot == 13 or slot == 14 then
                if entry and entry.spellIds and b.spellId and entry.spellIds[b.spellId] then
                    isMatch = true
                else
                    local bName = b.name
                    if bName then
                        local cName = string.lower(bName):gsub("[%s%p%c]", "")
                        if entry and entry.keywords then
                            for _, kw in ipairs(entry.keywords) do
                                local kwClean = kw:lower():gsub("[%s%p%c]", "")
                                if cName:find(kwClean, 1, true) then isMatch = true break end
                            end
                        end
                    end
                end
            end

            if isMatch then
                durBuff = (b.duration and b.duration > 0) and b.duration or defaultDur
                remBuff = (b.expirationTime and b.expirationTime > 0) and (b.expirationTime - now) or 0
                if remBuff > 0.05 then
                    foundBuff = true
                    buffIcon = b.icon
                    matchedSpellId = b.spellId
                    matchedBuffName = b.name
                    break
                end
            end
        end

        if foundBuff then
            if not icdState.isProc or (now - icdState.lastStart > durBuff + 2) then
                icdState.lastStart = now - (durBuff - remBuff)
                icdState.lastEnd = icdState.lastStart + targetICD
                icdState.isProc = true
            end
            return finish("ACTIVE", remBuff, durBuff, buffIcon or baseIcon, matchedSpellId, matchedBuffName)
        end

        if icdState.isProc then
            icdState.isProc = false
        end

        if isOnUseCooldown then
            return finish("COOLDOWN", remItemCD, itemDur, baseIcon)
        end

        if icdState.lastStart > 0 and targetICD > 0 then
            local elapsed = now - icdState.lastStart
            if elapsed < targetICD then
                local remICD = targetICD - elapsed
                return finish("ICD", remICD, targetICD, baseIcon)
            else
                icdState.lastStart = 0
            end
        end

        return finish("READY", 0, 0, baseIcon)
    end

    _G.PWHUD_CheckRingEquipped = function()
        local now_r = GetTime()
        local cache = _G.PWHUD_RingEquipCache
        if cache and (now_r - cache.time < 0.25) then
            return cache.isEquipped, cache.slot, cache.itemID
        end
        if not cache then
            cache = { time = 0, isEquipped = false, slot = nil, itemID = nil }
            _G.PWHUD_RingEquipCache = cache
        end
        cache.time = now_r

        for _, s in ipairs({ 11, 12 }) do
            local id = GetInventoryItemID("player", s)
            if not id then
                local link = GetInventoryItemLink("player", s)
                if link then id = tonumber(link:match("item:(%d+)")) end
            end
            if id and _G.PWHUD_RingDB and _G.PWHUD_RingDB[id] then
                cache.isEquipped = true
                cache.slot = s
                cache.itemID = id
                return true, s, id
            end
        end

        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
        if buffs then
            if buffs.bySpellId[72414] or buffs.bySpellId[72412] or buffs.bySpellId[72410] or buffs.bySpellId[72408] then
                cache.isEquipped = true
                cache.slot = 11
                cache.itemID = 50404
                return true, 11, 50404
            end
        end

        cache.isEquipped = false
        cache.slot = nil
        cache.itemID = nil
        return false, nil, nil
    end

    _G.PWHUD_CheckRing = function()
        local isEquipped, ringSlot, ringItemID = _G.PWHUD_CheckRingEquipped()
        local defIcon = (ringItemID and GetItemIcon(ringItemID)) or "Interface\\Icons\\INV_Jewelry_Ring_84"
        if not isEquipped then return "NONE", 0, 0, defIcon, false end

        local now_rk = GetTime()
        local state = _G.PWHUD_RingState
        local entry = ringItemID and _G.PWHUD_RingDB and _G.PWHUD_RingDB[ringItemID]
        local targetICD = (entry and entry.icd) or 60
        local defaultDur = (entry and entry.dur) or 10

        if state.lastItemID and ringItemID and state.lastItemID ~= ringItemID then
            state.lastStart = 0
            state.lastEnd = 0
            state.isProc = false
        end
        if ringItemID then state.lastItemID = ringItemID end

        local foundBuff = false
        local remBuff = 0
        local durBuff = defaultDur
        local buffIcon = nil

        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
        local bList = buffs and buffs.list or {}

        for _, b in ipairs(bList) do
            local isMatch = false
            if entry and entry.spellIds and b.spellId and entry.spellIds[b.spellId] then
                isMatch = true
            else
                local bName = b.name
                if bName then
                    local cName = string.lower(bName):gsub("[%s%p%c]", "")
                    if entry and entry.keywords then
                        for _, kw in ipairs(entry.keywords) do
                            local kwClean = kw:lower():gsub("[%s%p%c]", "")
                            if cName:find(kwClean, 1, true) then isMatch = true break end
                        end
                    end
                end
            end

            if isMatch then
                durBuff = (b.duration and b.duration > 0) and b.duration or defaultDur
                remBuff = (b.expirationTime and b.expirationTime > 0) and (b.expirationTime - now_rk) or 0
                if remBuff > 0.05 then
                    foundBuff = true
                    buffIcon = b.icon
                    break
                end
            end
        end

        if foundBuff then
            if not state.isProc or (now_rk - state.lastStart > durBuff + 2) then
                state.lastStart = now_rk - (durBuff - remBuff)
                state.lastEnd = state.lastStart + targetICD
                state.isProc = true
            end
            return "ACTIVE", remBuff, durBuff, buffIcon or defIcon, true
        end

        if state.isProc then
            state.isProc = false
        end

        if state.lastStart > 0 and targetICD > 0 then
            local elapsed = now_rk - state.lastStart
            if elapsed < targetICD then
                local remICD = targetICD - elapsed
                return "ICD", remICD, targetICD, defIcon, false
            else
                state.lastStart = 0
            end
        end

        return "READY", 0, 0, defIcon, false
    end

    _G.PWHUD_CheckTierSetEquipped = function()
        local now = GetTime()
        local cache = _G.PWHUD_TierEquipCache
        if cache and (now - cache.time < 0.25) then
            return cache.isEquipped, cache.t10, cache.t9, cache.t8, cache.t7
        end
        if not cache then
            cache = { time = 0, isEquipped = false, t10 = 0, t9 = 0, t8 = 0, t7 = 0 }
            _G.PWHUD_TierEquipCache = cache
        end
        cache.time = now

        local t10, t9, t8, t7 = 0, 0, 0, 0
        local tierSlots = { 1, 3, 5, 7, 10 } -- Head, Shoulder, Chest, Legs, Hands

        for _, s in ipairs(tierSlots) do
            local id = GetInventoryItemID("player", s)
            if not id then
                local link = GetInventoryItemLink("player", s)
                if link then id = tonumber(link:match("item:(%d+)")) end
            end
            if id then
                if _G.PWHUD_T10_Pieces[id] then t10 = t10 + 1
                elseif _G.PWHUD_T9_Pieces[id] then t9 = t9 + 1
                elseif _G.PWHUD_T8_Pieces[id] then t8 = t8 + 1
                elseif _G.PWHUD_T7_Pieces[id] then t7 = t7 + 1
                end
            end
        end

        cache.t10 = t10
        cache.t9 = t9
        cache.t8 = t8
        cache.t7 = t7

        -- In WotLK 3.3.5a, only Tier set bonuses with genuine triggerable procs / active tracking buffs are displayed:
        -- 1. T10 4P (Blood Frenzy: Bloodrage grants 20% max HP damage absorption for 10s - Spell ID 70844)
        -- 2. T8 4P (Magic DR: Shield Block grants 20% magical damage reduction for 10s - Spell ID 64938 / 2565)
        -- Purely static/passive bonuses (T10 2P, T9 2P/4P, T8 2P, T7 2P/4P) do NOT have procs and are hidden.
        local hasProcTier = (t10 >= 4 or t8 >= 4)

        if not hasProcTier then
            local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
            if buffs then
                local bList = buffs.list or {}
                for _, b in ipairs(bList) do
                    if b.spellId == 70844 or (b.name and (b.name == "Blood Frenzy" or b.name == "Frenesia del Sangue")) then
                        hasProcTier = true
                        break
                    end
                end
            end
        end

        cache.isEquipped = hasProcTier
        return cache.isEquipped, t10, t9, t8, t7
    end

    _G.PWHUD_CheckTierSet = function()
        local isEquipped, t10, t9, t8, t7 = _G.PWHUD_CheckTierSetEquipped()
        if not isEquipped then
            return "NONE", 0, 0, 0, "Interface\\Icons\\Ability_Warrior_DefensiveStance", "No Proc Tier"
        end

        local now_tk = GetTime()
        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()

        -- T10 Prot 4P: Blood Frenzy from Bloodrage (Spell 70844 / "Blood Frenzy" / "Frenesia del Sangue")
        -- Bloodrage (Spell 2687) acts as a powerful active defensive CD granting 20% max HP absorption for 10s
        if t10 >= 4 or (buffs and buffs.bySpellId and buffs.bySpellId[70844]) then
            local t10_4P_Buff = buffs and (buffs.bySpellId[70844] or buffs.byName["Blood Frenzy"] or buffs.byName["Frenesia del Sangue"])
            if t10_4P_Buff and t10_4P_Buff.expirationTime and t10_4P_Buff.expirationTime > now_tk then
                local rem = t10_4P_Buff.expirationTime - now_tk
                local dur = (t10_4P_Buff.duration and t10_4P_Buff.duration > 0) and t10_4P_Buff.duration or 10
                return "ACTIVE", rem, dur, 1, "Interface\\Icons\\Ability_Racial_BloodRage", "T10 (4P)"
            end

            -- Bloodrage Cooldown tracking (Spell 2687)
            local brStart, brDur = GetSpellCooldown(2687)
            if not brStart or brDur == 0 or brDur <= 1.5 then
                local brName = (GetSpellInfo and select(1, GetSpellInfo(2687))) or "Bloodrage"
                brStart, brDur = GetSpellCooldown(brName)
            end
            if brStart and brDur and brDur > 1.5 then
                local remCD = (brStart + brDur) - now_tk
                if remCD > 0.1 then
                    return "COOLDOWN", remCD, brDur, 0, "Interface\\Icons\\Ability_Racial_BloodRage", "T10 (4P)"
                end
            end

            if t10 >= 4 then
                return "READY", 0, 0, 0, "Interface\\Icons\\Ability_Racial_BloodRage", "T10 (4P)"
            end
        end

        -- T8 Prot 4P: Shield Block magic reduction active (Spell 64938 / 2565)
        if t8 >= 4 then
            local sbBuff = buffs and (buffs.bySpellId[64938] or buffs.bySpellId[2565] or buffs.byName["Shield Block"] or buffs.byName["Blocco con Scudo"])
            if sbBuff and sbBuff.expirationTime and sbBuff.expirationTime > now_tk then
                local rem = sbBuff.expirationTime - now_tk
                local dur = (sbBuff.duration and sbBuff.duration > 0) and sbBuff.duration or 10
                return "ACTIVE", rem, dur, 1, "Interface\\Icons\\Ability_Defensive", "T8 (4P)"
            end
            return "READY", 0, 0, 0, "Interface\\Icons\\Spell_Nature_BloodLust", "T8 (4P)"
        end

        return "NONE", 0, 0, 0, "Interface\\Icons\\INV_Shield_05", "No Proc Tier"
    end

    _G.PWHUD_CheckEnchantsEquipped = function()
        local now = GetTime()
        local cache = _G.PWHUD_EnchantEquipCache
        if cache and (now - cache.time < 0.25) then return cache.hasEnchant end
        if not cache then cache = { time = 0, hasEnchant = false }; _G.PWHUD_EnchantEquipCache = cache end
        cache.time = now

        local itemLink = GetInventoryItemLink("player", 16)
        if not itemLink then
            cache.hasEnchant = false
            return false
        end

        local enchantID = tonumber(itemLink:match("item:%d+:(%d+)"))
        if enchantID and enchantID > 0 then
            if _G.PWHUD_WeaponEnchantDB and _G.PWHUD_WeaponEnchantDB[enchantID] then
                cache.hasEnchant = true
                return true
            end
            if _G.PWHUD_StaticWeaponEnchants and _G.PWHUD_StaticWeaponEnchants[enchantID] then
                cache.hasEnchant = false
                return false
            end
        elseif not enchantID or enchantID == 0 then
            cache.hasEnchant = false
            return false
        end

        -- Check active player buffs for known weapon proc auras
        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
        local bList = buffs and buffs.list or {}
        for _, b in ipairs(bList) do
            local sId = b.spellId
            local name = b.name or ""
            if sId == 64440 or sId == 64442 or sId == 64568 or sId == 28093 or sId == 59620 or sId == 42976 or sId == 20007 or sId == 60691 or sId == 59626 or
               name:find("Blade Ward") or name:find("Guardiano") or
               name:find("Blood Reserve") or name:find("Riserva") or
               name:find("Blood Draining") or name:find("Drenaggio") or
               name:find("Lightning Speed") or name:find("Velocit") or name:find("Mongoose") or name:find("Mangusta") or
               name:find("Berserk") or name:find("Executioner") or name:find("Boia") or
               name:find("Holy Strength") or name:find("Forza Sacra") or name:find("Crusader") or
               name:find("Lifeward") or name:find("Salvavita") or
               name:find("Black Magic") or name:find("Magia Nera") then
                cache.hasEnchant = true
                return true
            end
        end

        -- Tooltip scanning fallback for dynamic proc enchant detection on green text
        if not _G.PWHUD_EnchantScanTooltip then
            local tt = CreateFrame("GameTooltip", "PWHUD_EnchantScanTooltip", nil, "GameTooltipTemplate")
            tt:SetOwner(WorldFrame, "ANCHOR_NONE")
            _G.PWHUD_EnchantScanTooltip = tt
        end
        local tt = _G.PWHUD_EnchantScanTooltip
        tt:ClearLines()
        tt:SetInventoryItem("player", 16)
        for i = 1, tt:NumLines() do
            local fontString = _G["PWHUD_EnchantScanTooltipTextLeft" .. i]
            if fontString then
                local text = fontString:GetText()
                local r, g, b = fontString:GetTextColor()
                if text and r and g and b and (g > 0.7 and r < 0.3 and b < 0.3) then
                    local t = text:lower()
                    if t:find("chance") or t:find("probabilit") or t:find("proc") or
                       t:find("blade ward") or t:find("guardiano") or
                       t:find("blood draining") or t:find("drenaggio") or
                       t:find("mongoose") or t:find("mangusta") or
                       t:find("berserk") or t:find("executioner") or t:find("boia") or
                       t:find("crusader") or t:find("crociato") or
                       t:find("lifeward") or t:find("salvavita") or
                       t:find("black magic") or t:find("magia nera") then
                        cache.hasEnchant = true
                        return true
                    end
                end
            end
        end

        cache.hasEnchant = false
        return false
    end

    _G.PWHUD_CheckEnchants = function()
        local now = GetTime()
        local defIcon = "Interface\\Icons\\Spell_Holy_BlessingOfProtection"

        local buffs = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
        local bList = buffs and buffs.list or {}

        -- 1. Check Blood Draining (Spell 64568: emergency heal active)
        local bdHeal = buffs and (buffs.bySpellId[64568] or buffs.byName["Blood Draining"])
        if bdHeal and bdHeal.expirationTime and bdHeal.expirationTime > now then
            local rem = bdHeal.expirationTime - now
            local dur = (bdHeal.duration and bdHeal.duration > 0) and bdHeal.duration or 20
            return "ACTIVE", rem, dur, 1, "Interface\\Icons\\Spell_Shadow_BloodBoil"
        end

        -- 2. Check Blade Ward (+200 Parry active)
        local bw = buffs and (buffs.bySpellId[64442] or buffs.bySpellId[64440] or buffs.byName["Blade Ward"])
        if bw and bw.expirationTime and bw.expirationTime > now then
            local rem = bw.expirationTime - now
            local dur = (bw.duration and bw.duration > 0) and bw.duration or 10
            return "ACTIVE", rem, dur, 1, "Interface\\Icons\\Ability_Warrior_WeaponMastery"
        end

        -- 3. Check Mongoose
        local mg = buffs and (buffs.bySpellId[28093] or buffs.byName["Lightning Speed"])
        if mg and mg.expirationTime and mg.expirationTime > now then
            local rem = mg.expirationTime - now
            local dur = (mg.duration and mg.duration > 0) and mg.duration or 15
            return "ACTIVE", rem, dur, 1, "Interface\\Icons\\Spell_Nature_Possess"
        end

        -- 4. Check Berserking
        local bz = buffs and (buffs.bySpellId[59620] or buffs.byName["Berserking"])
        if bz and bz.expirationTime and bz.expirationTime > now then
            local rem = bz.expirationTime - now
            local dur = (bz.duration and bz.duration > 0) and bz.duration or 15
            return "ACTIVE", rem, dur, 1, "Interface\\Icons\\Spell_Nature_BloodLust"
        end

        -- 5. Check Blood Reserve Stacks (1 to 5)
        local br = buffs and (buffs.bySpellId[64440] or buffs.byName["Blood Reserve"] or buffs.byName["Riserva di Sangue"])
        if br and br.count and br.count > 0 then
            return "STACKS", 0, 0, br.count, "Interface\\Icons\\Spell_Shadow_BloodBoil"
        end

        local itemLink = GetInventoryItemLink("player", 16)
        local enchantID = itemLink and tonumber(itemLink:match("item:%d+:(%d+)"))
        if enchantID and _G.PWHUD_WeaponEnchantDB and _G.PWHUD_WeaponEnchantDB[enchantID] then
            defIcon = _G.PWHUD_WeaponEnchantDB[enchantID].icon or defIcon
        end

        return "READY", 0, 0, 0, defIcon
    end

    _G.PWHUD_CheckWarriorSpell = function(spellId, buffId)
        local now = GetTime()
        local defIcon = select(3, GetSpellInfo(spellId))
        if not defIcon then
            if spellId == 871 then defIcon = "Interface\\Icons\\Ability_Warrior_ShieldWall"
            elseif spellId == 12975 then defIcon = "Interface\\Icons\\Spell_Nature_ShamanRage"
            elseif spellId == 2565 then defIcon = "Interface\\Icons\\Ability_Defensive"
            elseif spellId == 55694 then defIcon = "Interface\\Icons\\Ability_Warrior_EnragedRegeneration"
            end
        end

        if buffId then
            for i = 1, 40 do
                local name, _, icon, count, _, duration, expirationTime, _, _, _, sId = UnitBuff("player", i)
                if not name then break end
                local isMatch = (sId == buffId or sId == spellId)
                if not isMatch and name then
                    if spellId == 2565 and (name == "Shield Block" or name == "Blocco con lo Scudo") then isMatch = true
                    elseif spellId == 871 and (name == "Shield Wall" or name == "Muro di Scudi") then isMatch = true
                    elseif spellId == 12975 and (name == "Last Stand" or name == "Ultima Difesa") then isMatch = true
                    end
                end
                if isMatch then
                    local rem = (expirationTime and expirationTime > 0) and (expirationTime - now) or 0
                    local dur = (duration and duration > 0) and duration or 0
                    return "ACTIVE", rem, dur, count or 1, icon or defIcon
                end
            end
        end

        local start, duration = GetSpellCooldown(spellId)
        if (not start or duration == 0) and GetSpellInfo then
            local spName = GetSpellInfo(spellId)
            if spName then start, duration = GetSpellCooldown(spName) end
        end
        if start and duration and start > 0 and duration > 1.5 then
            local remCD = (start + duration) - now
            if remCD > 0.1 then
                return "COOLDOWN", remCD, duration, 0, defIcon
            end
        end

        local curHP = UnitHealth("player") or 100
        local maxHP = UnitHealthMax("player") or 100
        local isEmergency = (curHP / maxHP) < 0.35 and (spellId == 871 or spellId == 12975)

        return (isEmergency and "EMERGENCY" or "READY"), 0, 0, 0, defIcon
    end

    -- =========================================================================
    -- RIPOSIZIONAMENTO DINAMICO NATURALE (CENTRATURA DINAMICA 1-10 ICONE)
    -- =========================================================================
    local lastRowUpdate = 0
    _G.PWHUD_UpdateUtilityRowPositions = function(force)
        local now = GetTime()
        if not force and (now - lastRowUpdate < 0.15) then return end
        lastRowUpdate = now

        local function getRegion(id)
            if not WeakAuras then return end
            if WeakAuras.GetRegion then
                local obj = WeakAuras.GetRegion(id)
                if obj then return obj.region or (obj.GetPoint and obj) end
            end
            if WeakAuras.regions then
                local regObj = WeakAuras.regions[id]
                return regObj and (regObj.region or (regObj.GetPoint and regObj))
            end
        end

        local group = getRegion("Class Warrior (Protection)")
        if not group then return end

        local hasT1 = _G.PWHUD_CheckSlotEquipped and _G.PWHUD_CheckSlotEquipped(13)
        local hasT2 = _G.PWHUD_CheckSlotEquipped and _G.PWHUD_CheckSlotEquipped(14)
        local hasRing = _G.PWHUD_CheckRingEquipped and _G.PWHUD_CheckRingEquipped()
        local hasCloak = _G.PWHUD_CheckSlotEquipped and _G.PWHUD_CheckSlotEquipped(15)
        local hasTier = _G.PWHUD_CheckTierSetEquipped and _G.PWHUD_CheckTierSetEquipped()
        local hasEnchant = _G.PWHUD_CheckEnchantsEquipped and _G.PWHUD_CheckEnchantsEquipped()
        local hasGloves = _G.PWHUD_CheckSlotEquipped and _G.PWHUD_CheckSlotEquipped(10)
        local hasBoots = _G.PWHUD_CheckSlotEquipped and _G.PWHUD_CheckSlotEquipped(8)

        local activeOrder = {}
        if hasT1 then table.insert(activeOrder, "05 - Trinket 1 warTank") end
        if hasT2 then table.insert(activeOrder, "06 - Trinket 2 warTank") end
        if hasRing then table.insert(activeOrder, "06b - Ring warTank") end
        if hasCloak then table.insert(activeOrder, "07 - Cloak warTank") end
        if hasTier then table.insert(activeOrder, "08 - Tier Set warTank") end
        if hasEnchant then table.insert(activeOrder, "09 - Enchants warTank") end
        if hasGloves then table.insert(activeOrder, "10 - Gloves warTank") end
        table.insert(activeOrder, "10b - Shield Block warTank")
        table.insert(activeOrder, "11 - Shield Wall warTank")
        table.insert(activeOrder, "12 - Last Stand warTank")
        if hasBoots then table.insert(activeOrder, "13 - Boots warTank") end

        local N = #activeOrder
        local step = 38
        local targetW = 28
        if N >= 11 then step = 25; targetW = 24
        elseif N == 10 then step = 27; targetW = 26
        elseif N == 9 then step = 29; targetW = 28
        elseif N == 8 then step = 32; targetW = 28
        elseif N == 7 then step = 38; targetW = 28
        elseif N == 6 then step = 44; targetW = 28
        elseif N == 5 then step = 48; targetW = 28
        else step = 52; targetW = 28 end

        for i, id in ipairs(activeOrder) do
            local targetX = math.floor(((i - (N + 1) / 2) * step) + 0.5)
            local r = getRegion(id)
            if r and r.ClearAllPoints and r.SetPoint then
                r:ClearAllPoints()
                r:SetPoint("CENTER", group, "CENTER", targetX, -45)
                if r.SetWidth and r.SetHeight then
                    r:SetWidth(targetW)
                    r:SetHeight(targetW)
                end
            end
        end
    end

    -- =========================================================================
    -- EVENT FRAME PER COMBAT LOG & GESTIONE ICD / REFRESH
    -- =========================================================================
    local f = _G.PWHUD_CoreFrame
    if not f then
        f = CreateFrame("Frame")
        rawset(_G, "PWHUD_CoreFrame", f)

        f:RegisterEvent("COMBAT_LOG_EVENT_UNFILTERED")
        f:RegisterEvent("PLAYER_EQUIPMENT_CHANGED")
        f:RegisterEvent("UNIT_INVENTORY_CHANGED")
        f:RegisterEvent("PLAYER_ENTERING_WORLD")
        f:RegisterEvent("ZONE_CHANGED_NEW_AREA")
        f:RegisterEvent("UNIT_AURA")
        f.pendingUpdates = 0

        local playerGUID = nil
        f:SetScript("OnEvent", function(self, event, ...)
            if event == "COMBAT_LOG_EVENT_UNFILTERED" then
                local timestamp, subEvent, sourceGUID, sourceName, sourceFlags, destGUID, destName, destFlags, spellId, spellName = ...
                if not playerGUID then playerGUID = UnitGUID("player") end
                local isPlayer = (destGUID == playerGUID or sourceGUID == playerGUID)
                if isPlayer then
                    local now = GetTime()
                    if subEvent == "SPELL_CAST_SUCCESS" or subEvent == "SPELL_AURA_APPLIED" or subEvent == "SPELL_AURA_REFRESH" then
                        for _, s in ipairs({ 13, 14 }) do
                            local tID = GetInventoryItemID and GetInventoryItemID("player", s)
                            local tEntry = tID and _G.PWHUD_TrinketDB and _G.PWHUD_TrinketDB[tID]
                            local isTMatch = false
                            if tEntry then
                                if spellId and tEntry.spellIds and tEntry.spellIds[spellId] then
                                    isTMatch = true
                                elseif spellName and tEntry.keywords then
                                    local snClean = spellName:lower():gsub("[%s%p%c]", "")
                                    for _, kw in ipairs(tEntry.keywords) do
                                        if snClean:find(kw:lower():gsub("[%s%p%c]", ""), 1, true) then
                                            isTMatch = true
                                            break
                                        end
                                    end
                                end
                            end
                            if isTMatch then
                                local sICD = _G.PWHUD_ICD and _G.PWHUD_ICD[s]
                                if sICD then
                                    sICD.lastStart = now
                                    sICD.lastEnd = now + (tEntry.icd or 45)
                                    sICD.isProc = true
                                    if WeakAuras and WeakAuras.ScanEvents then
                                        WeakAuras.ScanEvents("PWHUD_ROW_UPDATE")
                                    end
                                end
                            end
                        end

                        -- Boots & Gloves ICD
                        if spellId == 54861 or spellName == "Nitro Boosts" then
                            _G.PWHUD_ICD[8].lastStart = now
                            _G.PWHUD_ICD[8].lastEnd = now + 180
                            _G.PWHUD_ICD[8].isProc = true
                            if WeakAuras and WeakAuras.ScanEvents then WeakAuras.ScanEvents("PWHUD_ROW_UPDATE") end
                        elseif spellId == 54758 or spellName == "Hyperspeed Acceleration" then
                            _G.PWHUD_ICD[10].lastStart = now
                            _G.PWHUD_ICD[10].lastEnd = now + 60
                            _G.PWHUD_ICD[10].isProc = true
                            if WeakAuras and WeakAuras.ScanEvents then WeakAuras.ScanEvents("PWHUD_ROW_UPDATE") end
                        end

                        -- Ring Proc
                        if spellId == 72414 or spellId == 72412 or spellName == "Armor of the Ashen Verdict" or spellName == "Armatura del Verdetto Cinereo" then
                            _G.PWHUD_RingState.lastStart = now
                            _G.PWHUD_RingState.lastEnd = now + 60
                            _G.PWHUD_RingState.isProc = true
                            if WeakAuras and WeakAuras.ScanEvents then WeakAuras.ScanEvents("PWHUD_ROW_UPDATE") end
                        end
                    elseif subEvent == "SPELL_AURA_REMOVED" then
                        for _, s in ipairs({ 13, 14 }) do
                            local sICD = _G.PWHUD_ICD and _G.PWHUD_ICD[s]
                            if sICD then sICD.isProc = false end
                        end
                        if WeakAuras and WeakAuras.ScanEvents then WeakAuras.ScanEvents("PWHUD_ROW_UPDATE") end
                    end
                end
                return
            end

            _G.PWHUD_BuffCache = nil
            _G.PWHUD_SlotEquipCache = nil
            _G.PWHUD_TierEquipCache = nil
            _G.PWHUD_EnchantEquipCache = nil
            if WeakAuras and WeakAuras.ScanEvents then
                WeakAuras.ScanEvents("PWHUD_ROW_UPDATE")
            end
            _G.PWHUD_UpdateUtilityRowPositions(true)
            self.pendingUpdates = 5
            self:SetScript("OnUpdate", function(sf, el)
                if sf.pendingUpdates and sf.pendingUpdates > 0 then
                    sf.pendingUpdates = sf.pendingUpdates - 1
                    _G.PWHUD_UpdateUtilityRowPositions(true)
                else
                    sf:SetScript("OnUpdate", nil)
                end
            end)
        end)
    end

    _G.PWHUD_CoreInitDone = true
end"""


def make_slot_custom_text(slot: int) -> str:
    """Testo descrittivo del monile/mantello/guanti/scarpe (%c), con pixel glow su proc attivo e timer ICD."""
    return f"""function()
    if (not _G.PWHUD_CoreInitDone or _G.PWHUD_BUILD_VER ~= 48) and _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
    if _G.PWHUD_UpdateUtilityRowPositions then
        _G.PWHUD_UpdateUtilityRowPositions()
    end
    if not _G.PWHUD_CheckSlot then return "" end
    local state, rem, dur, icon = _G.PWHUD_CheckSlot({slot})
    local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)
    local glowKey = "PWHUD_SLOT_{slot}_GLOW"
    if state == "ACTIVE" then
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Start(aura_env.region, {{1, 0.85, 0.1, 1}}, 8, 0.25, 10, 2, 0, 0, false, glowKey)
        end
        return string.format("|cFFFFFF00%.1fs|r", rem)
    else
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Stop(aura_env.region, glowKey)
        end
        if (state == "ICD" or state == "COOLDOWN") and rem > 0.1 then
            if rem >= 60 then
                local m = math.floor(rem / 60)
                local s = math.floor(rem % 60)
                return string.format("%d:%02d", m, s)
            else
                return string.format("%.0f", rem)
            end
        end
        return ""
    end
end"""


def make_slot_custom_duration(slot: int) -> str:
    """Durata e scadenza dello swipe di ricarica per lo slot indicato."""
    return f"""function()
    if not _G.PWHUD_CheckSlot then return 0, 0 end
    local state, rem, dur = _G.PWHUD_CheckSlot({slot})
    if (state == "ACTIVE" or state == "ICD" or state == "COOLDOWN") and rem > 0 and dur > 0 then
        return dur, GetTime() + rem
    end
    return 0, 0
end"""


def make_slot_custom_icon(slot: int, default_icon: str) -> str:
    """Restituisce dinamicamente l'icona dell'oggetto equipaggiato o del proc attivo."""
    return f"""function()
    if _G.PWHUD_CheckSlot then
        local state, rem, dur, icon = _G.PWHUD_CheckSlot({slot})
        if state == "ACTIVE" and icon then
            return icon
        end
        if icon then return icon end
    end
    return GetInventoryItemTexture("player", {slot}) or "{default_icon}"
end"""


def make_slot_trigger_custom(slot: int) -> str:
    """Trigger custom per verificare se lo slot è equipaggiato."""
    bootstrap = f"""    _G.PWHUD_InitCore = {SHARED_WARRIOR_CORE_BOOTSTRAP_LUA}
    if not _G.PWHUD_CoreInitDone or _G.PWHUD_BUILD_VER ~= 48 then _G.PWHUD_InitCore() end""" if slot == 13 else ""
    return f"""function(event, ...)
{bootstrap}
    if not _G.PWHUD_CheckSlotEquipped then return false end
    return _G.PWHUD_CheckSlotEquipped({slot})
end"""


def make_slot_untrigger_custom(slot: int) -> str:
    """Untrigger custom quando lo slot non è equipaggiato."""
    return f"""function(event, ...)
    if not _G.PWHUD_CheckSlotEquipped then return true end
    return not _G.PWHUD_CheckSlotEquipped({slot})
end"""


def make_ring_custom_text() -> str:
    """Testo descrittivo dell'anello (%c) con pixel glow e timer ICD 60s."""
    return """function()
    if (not _G.PWHUD_CoreInitDone or _G.PWHUD_BUILD_VER ~= 48) and _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
    if _G.PWHUD_UpdateUtilityRowPositions then
        _G.PWHUD_UpdateUtilityRowPositions()
    end
    if not _G.PWHUD_CheckRing then return "" end
    local state, rem, dur, icon = _G.PWHUD_CheckRing()
    local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)
    local glowKey = "PWHUD_RING_GLOW"
    if state == "ACTIVE" then
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Start(aura_env.region, {1, 0.85, 0.1, 1}, 8, 0.25, 10, 2, 0, 0, false, glowKey)
        end
        return string.format("|cFFFFFF00%.1fs|r", rem)
    else
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Stop(aura_env.region, glowKey)
        end
        if state == "ICD" and rem > 0.1 then
            if rem >= 60 then
                local m = math.floor(rem / 60)
                local s = math.floor(rem % 60)
                return string.format("%d:%02d", m, s)
            else
                return string.format("%.0f", rem)
            end
        end
        return ""
    end
end"""


def make_ring_custom_duration() -> str:
    return """function()
    if not _G.PWHUD_CheckRing then return 0, 0 end
    local state, rem, dur = _G.PWHUD_CheckRing()
    if (state == "ACTIVE" or state == "ICD") and rem > 0 and dur > 0 then
        return dur, GetTime() + rem
    end
    return 0, 0
end"""


def make_ring_custom_icon() -> str:
    return """function()
    if _G.PWHUD_CheckRing then
        local state, rem, dur, icon = _G.PWHUD_CheckRing()
        if icon then return icon end
    end
    return "Interface\\Icons\\INV_Jewelry_Ring_84"
end"""


def make_ring_trigger_custom() -> str:
    return """function(event, ...)
    if not _G.PWHUD_CheckRingEquipped then return false end
    return _G.PWHUD_CheckRingEquipped()
end"""


def make_ring_untrigger_custom() -> str:
    return """function(event, ...)
    if not _G.PWHUD_CheckRingEquipped then return true end
    return not _G.PWHUD_CheckRingEquipped()
end"""


def make_tierset_custom_text() -> str:
    return """function()
    if (not _G.PWHUD_CoreInitDone or _G.PWHUD_BUILD_VER ~= 48) and _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
    if _G.PWHUD_UpdateUtilityRowPositions then
        _G.PWHUD_UpdateUtilityRowPositions()
    end
    if not _G.PWHUD_CheckTierSet then return "" end
    local state, rem, dur, count, icon, label = _G.PWHUD_CheckTierSet()
    local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)
    local glowKey = "PWHUD_TIER_GLOW"
    if state == "ACTIVE" then
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Start(aura_env.region, {1, 0.85, 0.1, 1}, 8, 0.25, 10, 2, 0, 0, false, glowKey)
        end
        if rem > 0 then
            return string.format("|cFFFFFF00%.1fs|r", rem)
        end
        return "|cFFFFFF00ON|r"
    else
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Stop(aura_env.region, glowKey)
        end
        if state == "COOLDOWN" and rem > 0.1 then
            if rem >= 60 then
                local m = math.floor(rem / 60)
                local s = math.floor(rem % 60)
                return string.format("%d:%02d", m, s)
            else
                return string.format("%.0f", rem)
            end
        end
        return ""
    end
end"""


def make_tierset_custom_duration() -> str:
    return """function()
    if not _G.PWHUD_CheckTierSet then return 0, 0 end
    local state, rem, dur = _G.PWHUD_CheckTierSet()
    if (state == "ACTIVE" or state == "COOLDOWN") and rem > 0 and dur > 0 then
        return dur, GetTime() + rem
    end
    return 0, 0
end"""


def make_tierset_custom_icon() -> str:
    return """function()
    if _G.PWHUD_CheckTierSet then
        local state, rem, dur, count, icon = _G.PWHUD_CheckTierSet()
        if icon then return icon end
    end
    return "Interface\\Icons\\Ability_Racial_BloodRage"
end"""


def make_tierset_trigger_custom() -> str:
    return """function(event, ...)
    if not _G.PWHUD_CheckTierSetEquipped then return false end
    return _G.PWHUD_CheckTierSetEquipped()
end"""


def make_tierset_untrigger_custom() -> str:
    return """function(event, ...)
    if not _G.PWHUD_CheckTierSetEquipped then return true end
    return not _G.PWHUD_CheckTierSetEquipped()
end"""


def make_enchants_custom_text() -> str:
    return """function()
    if (not _G.PWHUD_CoreInitDone or _G.PWHUD_BUILD_VER ~= 48) and _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
    if _G.PWHUD_UpdateUtilityRowPositions then
        _G.PWHUD_UpdateUtilityRowPositions()
    end
    if not _G.PWHUD_CheckEnchants then return "" end
    local state, rem, dur, count, icon = _G.PWHUD_CheckEnchants()
    local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)
    local glowKey = "PWHUD_ENCHANT_GLOW"
    if state == "ACTIVE" then
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Start(aura_env.region, {1, 0.85, 0.1, 1}, 8, 0.25, 10, 2, 0, 0, false, glowKey)
        end
        return string.format("|cFFFFFF00%.1fs|r", rem)
    elseif state == "STACKS" then
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Stop(aura_env.region, glowKey)
        end
        return string.format("|cFF00FF00x%d|r", count)
    else
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Stop(aura_env.region, glowKey)
        end
        return ""
    end
end"""


def make_enchants_custom_duration() -> str:
    return """function()
    if not _G.PWHUD_CheckEnchants then return 0, 0 end
    local state, rem, dur = _G.PWHUD_CheckEnchants()
    if state == "ACTIVE" and rem > 0 and dur > 0 then
        return dur, GetTime() + rem
    end
    return 0, 0
end"""


def make_enchants_custom_icon() -> str:
    return """function()
    if _G.PWHUD_CheckEnchants then
        local state, rem, dur, count, icon = _G.PWHUD_CheckEnchants()
        if icon then return icon end
    end
    return "Interface\\Icons\\Spell_Holy_BlessingOfProtection"
end"""


def make_enchants_trigger_custom() -> str:
    return """function(event, ...)
    if not _G.PWHUD_CheckEnchantsEquipped then return false end
    return _G.PWHUD_CheckEnchantsEquipped()
end"""


def make_enchants_untrigger_custom() -> str:
    return """function(event, ...)
    if not _G.PWHUD_CheckEnchantsEquipped then return true end
    return not _G.PWHUD_CheckEnchantsEquipped()
end"""


def make_warrior_spell_custom_text(spell_id: int, buff_id: int, glow_key: str) -> str:
    return f"""function()
    if (not _G.PWHUD_CoreInitDone or _G.PWHUD_BUILD_VER ~= 48) and _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
    if _G.PWHUD_UpdateUtilityRowPositions then
        _G.PWHUD_UpdateUtilityRowPositions()
    end
    if not _G.PWHUD_CheckWarriorSpell then return "" end
    local state, rem, dur, count, icon = _G.PWHUD_CheckWarriorSpell({spell_id}, {buff_id or "nil"})
    local LCG = LibStub and LibStub("LibCustomGlow-1.0", true)
    if state == "ACTIVE" then
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Start(aura_env.region, {{1, 0.85, 0.1, 1}}, 8, 0.25, 10, 2, 0, 0, false, "{glow_key}")
        end
        return string.format("|cFFFFFF00%.1fs|r", rem)
    elseif state == "EMERGENCY" then
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Start(aura_env.region, {{1, 0.2, 0.1, 1}}, 10, 0.35, 12, 2, 0, 0, false, "{glow_key}")
        end
        return "|cFFFF2020USE!|r"
    else
        if LCG and aura_env and aura_env.region then
            LCG.PixelGlow_Stop(aura_env.region, "{glow_key}")
        end
        if state == "COOLDOWN" and rem > 0.1 then
            if rem >= 60 then
                local m = math.floor(rem / 60)
                local s = math.floor(rem % 60)
                return string.format("%d:%02d", m, s)
            else
                return string.format("%.0f", rem)
            end
        end
        return ""
    end
end"""


def make_warrior_spell_custom_duration(spell_id: int, buff_id: int) -> str:
    return f"""function()
    if not _G.PWHUD_CheckWarriorSpell then return 0, 0 end
    local state, rem, dur = _G.PWHUD_CheckWarriorSpell({spell_id}, {buff_id or "nil"})
    if (state == "ACTIVE" or state == "COOLDOWN") and rem > 0 and dur > 0 then
        return dur, GetTime() + rem
    end
    return 0, 0
end"""


def make_warrior_spell_custom_icon(spell_id: int, default_icon: str) -> str:
    return f"""function()
    if _G.PWHUD_CheckWarriorSpell then
        local state, rem, dur, count, icon = _G.PWHUD_CheckWarriorSpell({spell_id})
        if icon then return icon end
    end
    return select(3, GetSpellInfo({spell_id})) or "{default_icon}"
end"""


def make_warrior_spell_trigger_custom(spell_id: int) -> str:
    return f"""function(event, ...)
    return IsSpellKnown({spell_id}) or (GetSpellCooldown({spell_id}) ~= nil)
end"""


def build_utility_auras() -> list[dict]:
    events_list = "PLAYER_EQUIPMENT_CHANGED,UNIT_INVENTORY_CHANGED,PLAYER_ENTERING_WORLD,ZONE_CHANGED_NEW_AREA,UNIT_AURA,COMBAT_LOG_EVENT_UNFILTERED,PWHUD_ROW_UPDATE"

    return [
        # 05 - Trinket 1 warTank (Slot 13)
        {
            "id": "05 - Trinket 1 warTank",
            "uid": "PWHUD_UTIL_TRINKET1",
            "parent": "Class Warrior (Protection)",
            "regionType": "icon",
            "internalVersion": 90,
            "xOffset": -140,
            "yOffset": -45,
            "width": 28,
            "height": 28,
            "displayIcon": "Interface\\Icons\\INV_Misc_Ornament_02",
            "cooldown": True,
            "cooldownSwipe": True,
            "cooldownEdge": True,
            "cooldownTextDisabled": True,
            "inverse": False,
            "customTextUpdate": "update",
            "customText": make_slot_custom_text(13),
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "events": events_list,
                        "custom": make_slot_trigger_custom(13),
                        "customDuration": make_slot_custom_duration(13),
                        "customIcon": make_slot_custom_icon(13, "Interface\\Icons\\INV_Misc_Ornament_02")
                    },
                    "untrigger": {
                        "custom": make_slot_untrigger_custom(13)
                    }
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=10),
            ],
        },

        # 06 - Trinket 2 warTank (Slot 14)
        {
            "id": "06 - Trinket 2 warTank",
            "uid": "PWHUD_UTIL_TRINKET2",
            "parent": "Class Warrior (Protection)",
            "regionType": "icon",
            "internalVersion": 90,
            "xOffset": -112,
            "yOffset": -45,
            "width": 28,
            "height": 28,
            "displayIcon": "Interface\\Icons\\INV_Misc_RubySanctum1",
            "cooldown": True,
            "cooldownSwipe": True,
            "cooldownEdge": True,
            "cooldownTextDisabled": True,
            "inverse": False,
            "customTextUpdate": "update",
            "customText": make_slot_custom_text(14),
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "events": events_list,
                        "custom": make_slot_trigger_custom(14),
                        "customDuration": make_slot_custom_duration(14),
                        "customIcon": make_slot_custom_icon(14, "Interface\\Icons\\INV_Misc_RubySanctum1")
                    },
                    "untrigger": {
                        "custom": make_slot_untrigger_custom(14)
                    }
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=10),
            ],
        },

        # 06b - Ring warTank (Slot 11/12)
        {
            "id": "06b - Ring warTank",
            "uid": "PWHUD_UTIL_RING",
            "parent": "Class Warrior (Protection)",
            "regionType": "icon",
            "internalVersion": 90,
            "xOffset": -84,
            "yOffset": -45,
            "width": 28,
            "height": 28,
            "displayIcon": "Interface\\Icons\\INV_Jewelry_Ring_84",
            "cooldown": True,
            "cooldownSwipe": True,
            "cooldownEdge": True,
            "cooldownTextDisabled": True,
            "inverse": False,
            "customTextUpdate": "update",
            "customText": make_ring_custom_text(),
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "events": events_list,
                        "custom": make_ring_trigger_custom(),
                        "customDuration": make_ring_custom_duration(),
                        "customIcon": make_ring_custom_icon()
                    },
                    "untrigger": {
                        "custom": make_ring_untrigger_custom()
                    }
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=10),
            ],
        },

        # 07 - Cloak warTank (Slot 15)
        {
            "id": "07 - Cloak warTank",
            "uid": "PWHUD_UTIL_CLOAK",
            "parent": "Class Warrior (Protection)",
            "regionType": "icon",
            "internalVersion": 90,
            "xOffset": -56,
            "yOffset": -45,
            "width": 28,
            "height": 28,
            "displayIcon": "Interface\\Icons\\INV_Misc_Cape_19",
            "cooldown": True,
            "cooldownSwipe": True,
            "cooldownEdge": False,
            "cooldownTextDisabled": True,
            "inverse": False,
            "customTextUpdate": "update",
            "customText": make_slot_custom_text(15),
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "events": events_list,
                        "custom": make_slot_trigger_custom(15),
                        "customDuration": make_slot_custom_duration(15),
                        "customIcon": make_slot_custom_icon(15, "Interface\\Icons\\INV_Misc_Cape_19")
                    },
                    "untrigger": {
                        "custom": make_slot_untrigger_custom(15)
                    }
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=10),
            ],
        },

        # 08 - Tier Set warTank (T10 / T9 / T8 / T7)
        {
            "id": "08 - Tier Set warTank",
            "uid": "PWHUD_UTIL_TIER",
            "parent": "Class Warrior (Protection)",
            "regionType": "icon",
            "internalVersion": 90,
            "xOffset": -28,
            "yOffset": -45,
            "width": 28,
            "height": 28,
            "displayIcon": "Interface\\Icons\\Ability_Racial_BloodRage",
            "cooldown": True,
            "cooldownSwipe": True,
            "cooldownEdge": False,
            "cooldownTextDisabled": True,
            "inverse": False,
            "customTextUpdate": "update",
            "customText": make_tierset_custom_text(),
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "events": events_list,
                        "custom": make_tierset_trigger_custom(),
                        "customDuration": make_tierset_custom_duration(),
                        "customIcon": make_tierset_custom_icon()
                    },
                    "untrigger": {
                        "custom": make_tierset_untrigger_custom()
                    }
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=10),
            ],
        },

        # 09 - Enchants warTank (Slot 16)
        {
            "id": "09 - Enchants warTank",
            "uid": "PWHUD_UTIL_ENCHANTS",
            "parent": "Class Warrior (Protection)",
            "regionType": "icon",
            "internalVersion": 90,
            "xOffset": 0,
            "yOffset": -45,
            "width": 28,
            "height": 28,
            "displayIcon": "Interface\\Icons\\Spell_Holy_BlessingOfProtection",
            "cooldown": True,
            "cooldownSwipe": True,
            "cooldownEdge": True,
            "cooldownTextDisabled": True,
            "inverse": False,
            "customTextUpdate": "update",
            "customText": make_enchants_custom_text(),
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "events": events_list,
                        "custom": make_enchants_trigger_custom(),
                        "customDuration": make_enchants_custom_duration(),
                        "customIcon": make_enchants_custom_icon()
                    },
                    "untrigger": {
                        "custom": make_enchants_untrigger_custom()
                    }
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=10),
            ],
        },

        # 10 - Gloves warTank (Slot 10)
        {
            "id": "10 - Gloves warTank",
            "uid": "PWHUD_UTIL_GLOVES",
            "parent": "Class Warrior (Protection)",
            "regionType": "icon",
            "internalVersion": 90,
            "xOffset": 28,
            "yOffset": -45,
            "width": 28,
            "height": 28,
            "displayIcon": "Interface\\Icons\\INV_Gauntlets_26",
            "cooldown": True,
            "cooldownSwipe": True,
            "cooldownEdge": True,
            "cooldownTextDisabled": True,
            "inverse": False,
            "customTextUpdate": "update",
            "customText": make_slot_custom_text(10),
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "events": events_list,
                        "custom": make_slot_trigger_custom(10),
                        "customDuration": make_slot_custom_duration(10),
                        "customIcon": make_slot_custom_icon(10, "Interface\\Icons\\INV_Gauntlets_26")
                    },
                    "untrigger": {
                        "custom": make_slot_untrigger_custom(10)
                    }
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=10),
            ],
        },

        # 10b - Shield Block warTank (Spell 2565: Durata Attiva 10s & Cooldown 30s/60s)
        {
            "id": "10b - Shield Block warTank",
            "uid": "PWHUD_UTIL_SHIELDBLOCK",
            "parent": "Class Warrior (Protection)",
            "regionType": "icon",
            "internalVersion": 90,
            "xOffset": 28,
            "yOffset": -45,
            "width": 28,
            "height": 28,
            "displayIcon": "Interface\\Icons\\Ability_Defensive",
            "cooldown": True,
            "cooldownSwipe": True,
            "cooldownEdge": False,
            "cooldownTextDisabled": True,
            "inverse": False,
            "customTextUpdate": "update",
            "customText": make_warrior_spell_custom_text(2565, 2565, "PWHUD_SHIELDBLOCK_GLOW"),
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "events": events_list,
                        "custom": make_warrior_spell_trigger_custom(2565),
                        "customDuration": make_warrior_spell_custom_duration(2565, 2565),
                        "customIcon": make_warrior_spell_custom_icon(2565, "Interface\\Icons\\Ability_Defensive")
                    },
                    "untrigger": {
                        "custom": "function() return false end"
                    }
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=10),
            ],
        },

        # 11 - Shield Wall (Spell 871)
        {
            "id": "11 - Shield Wall warTank",
            "uid": "PWHUD_UTIL_SHIELDWALL",
            "parent": "Class Warrior (Protection)",
            "regionType": "icon",
            "internalVersion": 90,
            "xOffset": 56,
            "yOffset": -45,
            "width": 28,
            "height": 28,
            "displayIcon": "Interface\\Icons\\Ability_Warrior_ShieldWall",
            "cooldown": True,
            "cooldownSwipe": True,
            "cooldownEdge": True,
            "cooldownTextDisabled": True,
            "inverse": False,
            "customTextUpdate": "update",
            "customText": make_warrior_spell_custom_text(871, 871, "PWHUD_SHIELDWALL_GLOW"),
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "events": events_list,
                        "custom": make_warrior_spell_trigger_custom(871),
                        "customDuration": make_warrior_spell_custom_duration(871, 871),
                        "customIcon": make_warrior_spell_custom_icon(871, "Interface\\Icons\\Ability_Warrior_ShieldWall")
                    },
                    "untrigger": {
                        "custom": "function() return false end"
                    }
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=10),
            ],
        },

        # 12 - Last Stand (Spell 12975)
        {
            "id": "12 - Last Stand warTank",
            "uid": "PWHUD_UTIL_LASTSTAND",
            "parent": "Class Warrior (Protection)",
            "regionType": "icon",
            "internalVersion": 90,
            "xOffset": 84,
            "yOffset": -45,
            "width": 28,
            "height": 28,
            "displayIcon": "Interface\\Icons\\Spell_Nature_ShamanRage",
            "cooldown": True,
            "cooldownSwipe": True,
            "cooldownEdge": True,
            "cooldownTextDisabled": True,
            "inverse": False,
            "customTextUpdate": "update",
            "customText": make_warrior_spell_custom_text(12975, 12975, "PWHUD_LASTSTAND_GLOW"),
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "events": events_list,
                        "custom": make_warrior_spell_trigger_custom(12975),
                        "customDuration": make_warrior_spell_custom_duration(12975, 12975),
                        "customIcon": make_warrior_spell_custom_icon(12975, "Interface\\Icons\\Spell_Nature_ShamanRage")
                    },
                    "untrigger": {
                        "custom": "function() return false end"
                    }
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=10),
            ],
        },

        # 13 - Boots warTank (Slot 8)
        {
            "id": "13 - Boots warTank",
            "uid": "PWHUD_UTIL_BOOTS",
            "parent": "Class Warrior (Protection)",
            "regionType": "icon",
            "internalVersion": 90,
            "xOffset": 112,
            "yOffset": -45,
            "width": 28,
            "height": 28,
            "displayIcon": "Interface\\Icons\\Ability_Warrior_EnragedRegeneration",
            "cooldown": True,
            "cooldownSwipe": True,
            "cooldownEdge": True,
            "cooldownTextDisabled": True,
            "inverse": False,
            "customTextUpdate": "update",
            "customText": make_slot_custom_text(8),
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "events": events_list,
                        "custom": make_slot_trigger_custom(8),
                        "customDuration": make_slot_custom_duration(8),
                        "customIcon": make_slot_custom_icon(8, "Interface\\Icons\\Ability_Warrior_EnragedRegeneration")
                    },
                    "untrigger": {
                        "custom": make_slot_untrigger_custom(8)
                    }
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="CENTER", font_size=10),
            ],
        },
    ]
