"""
Modulo Componente: 02 - Battle Shout, 03 - Commanding Shout, 04 - Defensive Stance
===================================================================================
Gestisce i buff di classe e la postura a x = -231, -205, -179, -153 a y = 0 (24x24px con gap 2px):
1. 02 - Battle Shout:
   - Gruppo a x = -231, y = 0
   - Active: visibile SOLO quando il buff (Battle Shout o BoM/GBoM del Paladino) sta per scadere (<= 30s).
   - OFF: visibile quando manca SIA Battle Shout CHE BoM/GBoM (desaturato + 'OFF' con native aura2).
2. 03 - Commanding Shout:
   - Gruppo a x = -205, y = 0
   - Active: visibile SOLO quando il buff (Commanding Shout o Blood Pact dell'Imp) sta per scadere (<= 30s).
   - OFF: visibile quando manca SIA Commanding Shout CHE Blood Pact (desaturato + 'OFF' con native aura2).
3. 04 - Defensive Stance:
   - Gruppo a x = -153, y = 0
   - Active: icona postura difensiva.
   - Warning: allerta immediata con glow rosso e scritta 'STANCE' se in combattimento fuori dalla Postura Difensiva (Stance 2).
"""
from builder.core.helpers import make_subtext, make_glow_action


# =============================================================================
# LOGICA LUA CONDIVISA: CACHE BUFF GUERRIERO & VERIFICA SOVRAPPOSIZIONI RAID
# =============================================================================
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
        bomDuration = 0,
        bomExpiration = 0,
        hasBloodPact = false,
        bpDuration = 0,
        bpExpiration = 0,
        hasBattleShout = false,
        bsDuration = 0,
        bsExpiration = 0,
        hasCommandingShout = false,
        csDuration = 0,
        csExpiration = 0,
    }

    local bsNameLocal = (GetSpellInfo and select(1, GetSpellInfo(47436))) or "Battle Shout"
    local csNameLocal = (GetSpellInfo and select(1, GetSpellInfo(47440))) or "Commanding Shout"
    local bomNameLocal1 = (GetSpellInfo and select(1, GetSpellInfo(48934))) or "Greater Blessing of Might"
    local bomNameLocal2 = (GetSpellInfo and select(1, GetSpellInfo(19740))) or "Blessing of Might"
    local bpNameLocal = (GetSpellInfo and select(1, GetSpellInfo(47982))) or "Blood Pact"

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

        local lowerName = string.lower(name)
        local lowerIcon = icon and string.lower(icon) or ""

        -- Paladin Blessing of Might / Greater Blessing of Might
        if spellId == 48934 or spellId == 48933 or spellId == 48932 or spellId == 48931 or
           spellId == 27141 or spellId == 27140 or spellId == 25916 or spellId == 25782 or
           spellId == 25291 or spellId == 19838 or spellId == 19837 or spellId == 19836 or
           spellId == 19835 or spellId == 19834 or spellId == 19740 or
           (bomNameLocal1 and name == bomNameLocal1) or (bomNameLocal2 and name == bomNameLocal2) or
           string.find(lowerName, "might") or string.find(lowerName, "potenza") or
           string.find(lowerIcon, "spell_holy_greaterblessingofkings") or string.find(lowerIcon, "spell_holy_fistofjustice") then
            c.hasBoM = true
            c.bomDuration = duration or 1800
            c.bomExpiration = (expirationTime and expirationTime > 0) and expirationTime or (now_b + 1800)
        end

        -- Warlock Imp Blood Pact
        if spellId == 47982 or spellId == 47981 or spellId == 27268 or spellId == 11767 or
           spellId == 11766 or spellId == 6307 or (bpNameLocal and name == bpNameLocal) or
           string.find(lowerName, "blood pact") or string.find(lowerName, "patto di sangue") or
           string.find(lowerIcon, "spell_shadow_bloodboil") then
            c.hasBloodPact = true
            c.bpDuration = duration or 1800
            c.bpExpiration = (expirationTime and expirationTime > 0) and expirationTime or (now_b + 1800)
        end

        -- Battle Shout
        if spellId == 47436 or spellId == 25289 or spellId == 11551 or spellId == 11550 or
           spellId == 11549 or spellId == 6192 or spellId == 5242 or spellId == 2048 or spellId == 6673 or
           (bsNameLocal and name == bsNameLocal) or string.find(lowerName, "battle shout") or string.find(lowerName, "urlo di battaglia") or
           string.find(lowerIcon, "ability_warrior_battleshout") then
            c.hasBattleShout = true
            c.bsDuration = duration or 120
            c.bsExpiration = (expirationTime and expirationTime > 0) and expirationTime or (now_b + 120)
        end

        -- Commanding Shout
        if spellId == 47440 or spellId == 47439 or spellId == 469 or spellId == 45517 or
           (csNameLocal and name == csNameLocal) or string.find(lowerName, "commanding shout") or string.find(lowerName, "urlo di comando") or
           string.find(lowerIcon, "ability_warrior_commandingshout") or string.find(lowerIcon, "ability_warrior_rallyingcry") then
            c.hasCommandingShout = true
            c.csDuration = duration or 120
            c.csExpiration = (expirationTime and expirationTime > 0) and expirationTime or (now_b + 120)
        end
    end
    _G.PWHUD_BuffCache = c
    return c
end"""


BS_BUFF_LOOKUP_LUA = """local b = c.bySpellId[47436] or c.bySpellId[25289] or c.bySpellId[11551] or c.bySpellId[11550] or c.bySpellId[11549] or c.bySpellId[6192] or c.bySpellId[5242] or c.bySpellId[2048] or c.bySpellId[6673]
        or c.bySpellId[48934] or c.bySpellId[48933] or c.bySpellId[48932] or c.bySpellId[48931] or c.bySpellId[27141] or c.bySpellId[27140] or c.bySpellId[25916] or c.bySpellId[25782] or c.bySpellId[25291] or c.bySpellId[19838] or c.bySpellId[19837] or c.bySpellId[19836] or c.bySpellId[19835] or c.bySpellId[19834] or c.bySpellId[19740]
        or c.byName["Battle Shout"] or c.byName["Urlo di Battaglia"]
        or c.byName["Greater Blessing of Might"] or c.byName["Blessing of Might"]
        or c.byName["Benedizione della Potenza Superiore"] or c.byName["Benedizione della Potenza"]"""


CS_BUFF_LOOKUP_LUA = """local b = c.bySpellId[47440] or c.bySpellId[47439] or c.bySpellId[469] or c.bySpellId[45517]
        or c.bySpellId[47982] or c.bySpellId[47981] or c.bySpellId[27268] or c.bySpellId[11767] or c.bySpellId[11766] or c.bySpellId[6307]
        or c.byName["Commanding Shout"] or c.byName["Urlo di Comando"]
        or c.byName["Blood Pact"] or c.byName["Patto di Sangue"]"""


def make_bs_custom_text() -> str:
    return f"""function()
    _G.PWHUD_GetPlayerBuffs = _G.PWHUD_GetPlayerBuffs or {SHARED_GET_PLAYER_BUFFS_LUA}
    local c = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
    if not c then return "" end
    {BS_BUFF_LOOKUP_LUA}
    if b and b.expirationTime and b.expirationTime > 0 then
        local rem = b.expirationTime - GetTime()
        if rem > 60 then
            local m = math.floor(rem / 60)
            local s = math.floor(rem % 60)
            return string.format("|cFFFFFF00%d:%02d|r", m, s)
        elseif rem > 0 then
            return string.format("|cFFFF4444%.0fs|r", rem)
        end
    end
    return ""
end"""


def make_bs_trigger() -> str:
    return f"""function(event, ...)
    _G.PWHUD_GetPlayerBuffs = _G.PWHUD_GetPlayerBuffs or {SHARED_GET_PLAYER_BUFFS_LUA}
    local now = GetTime()
    local c = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
    if not c then return false end
    {BS_BUFF_LOOKUP_LUA}
    if b and b.expirationTime and b.expirationTime > 0 then
        local rem = b.expirationTime - now
        if rem > 30 then
            local delay = rem - 30
            if _G.PWHUD_BS_ScheduledExp ~= b.expirationTime then
                _G.PWHUD_BS_ScheduledExp = b.expirationTime
                _G.PWHUD_BS_TimerSeq = (_G.PWHUD_BS_TimerSeq or 0) + 1
                local mySeq = _G.PWHUD_BS_TimerSeq
                local timerAfter = (C_Timer and C_Timer.After) or (_G.C_Timer and _G.C_Timer.After)
                if timerAfter then
                    timerAfter(delay, function()
                        if _G.PWHUD_BS_TimerSeq == mySeq and WeakAuras and WeakAuras.ScanEvents then
                            WeakAuras.ScanEvents("PWHUD_BS_THRESHOLD")
                        end
                    end)
                elseif WeakAuras and WeakAuras.timer and WeakAuras.timer.ScheduleTimer then
                    WeakAuras.timer:ScheduleTimer(function()
                        if _G.PWHUD_BS_TimerSeq == mySeq and WeakAuras and WeakAuras.ScanEvents then
                            WeakAuras.ScanEvents("PWHUD_BS_THRESHOLD")
                        end
                    end, delay)
                end
            end
            return false
        elseif rem > 0 then
            _G.PWHUD_BS_ScheduledExp = nil
            return true
        end
    end
    _G.PWHUD_BS_ScheduledExp = nil
    _G.PWHUD_BS_TimerSeq = (_G.PWHUD_BS_TimerSeq or 0) + 1
    return false
end"""


def make_bs_custom_duration() -> str:
    return f"""function()
    _G.PWHUD_GetPlayerBuffs = _G.PWHUD_GetPlayerBuffs or {SHARED_GET_PLAYER_BUFFS_LUA}
    local c = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
    if not c then return 0, 0 end
    {BS_BUFF_LOOKUP_LUA}
    if b then
        return b.duration or 120, b.expirationTime
    end
    return 0, 0
end"""


def make_bs_untrigger() -> str:
    return f"""function(event, ...)
    _G.PWHUD_GetPlayerBuffs = _G.PWHUD_GetPlayerBuffs or {SHARED_GET_PLAYER_BUFFS_LUA}
    local now = GetTime()
    local c = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
    if not c then return true end
    {BS_BUFF_LOOKUP_LUA}
    if b and b.expirationTime and b.expirationTime > 0 then
        local rem = b.expirationTime - now
        return not (rem > 0 and rem <= 30)
    end
    return true
end"""


def make_cs_custom_text() -> str:
    return f"""function()
    _G.PWHUD_GetPlayerBuffs = _G.PWHUD_GetPlayerBuffs or {SHARED_GET_PLAYER_BUFFS_LUA}
    local c = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
    if not c then return "" end
    {CS_BUFF_LOOKUP_LUA}
    if b and b.expirationTime and b.expirationTime > 0 then
        local rem = b.expirationTime - GetTime()
        if rem > 60 then
            local m = math.floor(rem / 60)
            local s = math.floor(rem % 60)
            return string.format("|cFFFFFF00%d:%02d|r", m, s)
        elseif rem > 0 then
            return string.format("|cFFFF4444%.0fs|r", rem)
        end
    end
    return ""
end"""


def make_cs_trigger() -> str:
    return f"""function(event, ...)
    _G.PWHUD_GetPlayerBuffs = _G.PWHUD_GetPlayerBuffs or {SHARED_GET_PLAYER_BUFFS_LUA}
    local now = GetTime()
    local c = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
    if not c then return false end
    {CS_BUFF_LOOKUP_LUA}
    if b and b.expirationTime and b.expirationTime > 0 then
        local rem = b.expirationTime - now
        if rem > 30 then
            local delay = rem - 30
            if _G.PWHUD_CS_ScheduledExp ~= b.expirationTime then
                _G.PWHUD_CS_ScheduledExp = b.expirationTime
                _G.PWHUD_CS_TimerSeq = (_G.PWHUD_CS_TimerSeq or 0) + 1
                local mySeq = _G.PWHUD_CS_TimerSeq
                local timerAfter = (C_Timer and C_Timer.After) or (_G.C_Timer and _G.C_Timer.After)
                if timerAfter then
                    timerAfter(delay, function()
                        if _G.PWHUD_CS_TimerSeq == mySeq and WeakAuras and WeakAuras.ScanEvents then
                            WeakAuras.ScanEvents("PWHUD_CS_THRESHOLD")
                        end
                    end)
                elseif WeakAuras and WeakAuras.timer and WeakAuras.timer.ScheduleTimer then
                    WeakAuras.timer:ScheduleTimer(function()
                        if _G.PWHUD_CS_TimerSeq == mySeq and WeakAuras and WeakAuras.ScanEvents then
                            WeakAuras.ScanEvents("PWHUD_CS_THRESHOLD")
                        end
                    end, delay)
                end
            end
            return false
        elseif rem > 0 then
            _G.PWHUD_CS_ScheduledExp = nil
            return true
        end
    end
    _G.PWHUD_CS_ScheduledExp = nil
    _G.PWHUD_CS_TimerSeq = (_G.PWHUD_CS_TimerSeq or 0) + 1
    return false
end"""


def make_cs_custom_duration() -> str:
    return f"""function()
    _G.PWHUD_GetPlayerBuffs = _G.PWHUD_GetPlayerBuffs or {SHARED_GET_PLAYER_BUFFS_LUA}
    local c = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
    if not c then return 0, 0 end
    {CS_BUFF_LOOKUP_LUA}
    if b then
        return b.duration or 120, b.expirationTime
    end
    return 0, 0
end"""


def make_cs_untrigger() -> str:
    return f"""function(event, ...)
    _G.PWHUD_GetPlayerBuffs = _G.PWHUD_GetPlayerBuffs or {SHARED_GET_PLAYER_BUFFS_LUA}
    local now = GetTime()
    local c = _G.PWHUD_GetPlayerBuffs and _G.PWHUD_GetPlayerBuffs()
    if not c then return true end
    {CS_BUFF_LOOKUP_LUA}
    if b and b.expirationTime and b.expirationTime > 0 then
        local rem = b.expirationTime - now
        return not (rem > 0 and rem <= 30)
    end
    return true
end"""



# =============================================================================
# LOGICA LUA CONDIVISA: VIGILANCE (VIGILANZA - MODELLO FOCUS MAGIC)
# =============================================================================
SHARED_VIGILANCE_CHECK_LUA = r"""function(event, ...)
    local state = _G.PWHUD_VigilanceState
    if not state then
        state = { targetGUID = nil, targetName = nil, expires = 0, playerGUID = UnitGUID("player") }
        _G.PWHUD_VigilanceState = state
    end
    local playerGUID = state.playerGUID
    if not playerGUID then
        playerGUID = UnitGUID("player")
        state.playerGUID = playerGUID
    end

    local now = GetTime()

    -- 1. Gestione Eventi Assegnazione, Rimozione e Morte
    if event == "UNIT_SPELLCAST_SUCCEEDED" then
        local unit, spell = ...
        if unit == "player" and (spell == "Vigilance" or spell == "Vigilanza" or spell == 50720 or spell == 59665) then
            state.targetName = UnitName("target")
            state.targetGUID = UnitGUID("target")
            state.expires = now + 1800
        end
    elseif event == "COMBAT_LOG_EVENT_UNFILTERED" or event == "CLEU" then
        local _, subEvent, sourceGUID, _, _, destGUID, destName, _, spellId, spellName = ...
        local isRelevant = false
        if sourceGUID == playerGUID and (spellId == 50720 or spellId == 59665 or spellName == "Vigilance" or spellName == "Vigilanza") then
            isRelevant = true
            if subEvent == "SPELL_AURA_APPLIED" or subEvent == "SPELL_AURA_REFRESH" or subEvent == "SPELL_CAST_SUCCESS" then
                state.targetName = destName
                state.targetGUID = destGUID
                state.expires = now + 1800
            elseif subEvent == "SPELL_AURA_REMOVED" or subEvent == "SPELL_AURA_BROKEN" then
                state.targetName = nil
                state.targetGUID = nil
                state.expires = 0
            end
        elseif subEvent == "UNIT_DIED" then
            if (state.targetGUID and destGUID == state.targetGUID) or (state.targetName and destName == state.targetName) then
                isRelevant = true
                state.targetName = nil
                state.targetGUID = nil
                state.expires = 0
            end
        end
        if not isRelevant then
            local isAllyActive = (state.expires and state.expires > now) or false
            return isAllyActive, (isAllyActive and (state.expires - now) or 0), 1800, (state.expires or 0)
        end
    end

    -- 2. Verifica se l'alleato registrato ha ancora il buff ed e vivo
    if state.expires and state.expires > now then
        if state.targetName and UnitExists(state.targetName) and UnitIsDead(state.targetName) then
            state.targetName = nil
            state.targetGUID = nil
            state.expires = 0
        else
            return true, (state.expires - now), 1800, state.expires
        end
    end

    -- 3. Scansione attiva su target, focus, raid o party (utile al login, reload o cambio zona)
    local allyActive = false
    local expTime = 0
    local function checkUnit(u)
        if UnitExists(u) and UnitIsFriend("player", u) and not UnitIsDead(u) then
            for i = 1, 40 do
                local n, _, _, _, _, dur, exp, c, _, _, spellId = UnitBuff(u, i)
                if not n then break end
                if (spellId == 50720 or spellId == 59665 or n == "Vigilance" or n == "Vigilanza") and (c == "player" or not c) then
                    state.targetName = UnitName(u)
                    state.targetGUID = UnitGUID(u)
                    expTime = (exp and exp > 0) and exp or (now + 1800)
                    state.expires = expTime
                    return true
                end
            end
        end
        return false
    end

    if checkUnit("target") or checkUnit("focus") then
        allyActive = true
    else
        local nr = (GetNumRaidMembers and GetNumRaidMembers()) or 0
        if nr > 0 then
            for r = 1, nr do
                if checkUnit("raid" .. r) then
                    allyActive = true
                    break
                end
            end
        else
            local np = (GetNumPartyMembers and GetNumPartyMembers()) or 0
            if np > 0 then
                for p = 1, np do
                    if checkUnit("party" .. p) then
                        allyActive = true
                        break
                    end
                end
            end
        end
    end

    local rem = allyActive and (expTime > now and (expTime - now) or 1800) or 0
    return allyActive, rem, 1800, expTime
end"""


def make_vigilance_off_trigger() -> str:
    """Trigger Lua per Vigilance OFF (visibile se nessun alleato ha il buff - modello Focus Magic)."""
    return f"""function(event, ...)
    _G.PWHUD_CheckVigilance = _G.PWHUD_CheckVigilance or {SHARED_VIGILANCE_CHECK_LUA}
    local allyActive = _G.PWHUD_CheckVigilance(event, ...)
    return not allyActive
end"""


def make_vigilance_off_untrigger() -> str:
    """Untrigger Lua per Vigilance OFF."""
    return f"""function(event, ...)
    _G.PWHUD_CheckVigilance = _G.PWHUD_CheckVigilance or {SHARED_VIGILANCE_CHECK_LUA}
    local allyActive = _G.PWHUD_CheckVigilance(event, ...)
    return allyActive
end"""


def make_vigilance_active_trigger() -> str:
    """Trigger Lua per Vigilance Active (visibile solo se sta per scadere <= 60s)."""
    return f"""function(event, ...)
    _G.PWHUD_CheckVigilance = _G.PWHUD_CheckVigilance or {SHARED_VIGILANCE_CHECK_LUA}
    local allyActive, rem = _G.PWHUD_CheckVigilance(event, ...)
    return allyActive and rem > 0 and rem <= 60
end"""


def make_vigilance_active_untrigger() -> str:
    """Untrigger Lua per Vigilance Active."""
    return f"""function(event, ...)
    _G.PWHUD_CheckVigilance = _G.PWHUD_CheckVigilance or {SHARED_VIGILANCE_CHECK_LUA}
    local allyActive, rem = _G.PWHUD_CheckVigilance(event, ...)
    return (not allyActive) or rem > 60 or rem <= 0
end"""


def make_vigilance_custom_duration() -> str:
    """Durata e scadenza dello swipe di ricarica per Vigilance."""
    return """function()
    if not _G.PWHUD_CheckVigilance then return 0, 0 end
    local allyActive, rem, dur, exp = _G.PWHUD_CheckVigilance()
    if allyActive and rem > 0 and rem <= 60 then
        return dur or 1800, exp or (GetTime() + rem)
    end
    return 0, 0
end"""


def make_vigilance_custom_text() -> str:
    """Conto alla rovescia formattato per Vigilance (visibile quando rem <= 60)."""
    return """function()
    if not _G.PWHUD_CheckVigilance then return "" end
    local allyActive, rem = _G.PWHUD_CheckVigilance()
    if allyActive and rem > 0 and rem <= 60 then
        return string.format("|cFFFF4444%.0fs|r", rem)
    end
    return ""
end"""


def build_buffs_auras() -> list[dict]:
    return [
        # =====================================================================
        # 02 - BATTLE SHOUT (Gruppo Madre a x = -222, y = 0)
        # =====================================================================
        {
            "id": "02 - Battle Shout warTank",
            "uid": "PWHUD_BS_GRP",
            "parent": "Class Warrior (Protection)",
            "regionType": "group",
            "internalVersion": 90,
            "xOffset": -231,
            "yOffset": 0,
            "controlledChildren": [
                "Battle Shout - Active warTank",
                "Battle Shout - OFF warTank",
            ],
        },
        # 02 - Active (mostra timer solo se il buff o BoM è attivo ma con <= 30 secondi)
        {
            "id": "Battle Shout - Active warTank",
            "uid": "PWHUD_BS_ACTIVE",
            "parent": "02 - Battle Shout warTank",
            "regionType": "icon",
            "internalVersion": 90,
            "xOffset": 0,
            "yOffset": 0,
            "width": 24,
            "height": 24,
            "displayIcon": "Interface\\Icons\\Ability_Warrior_BattleShout",
            "auto": False,
            "color": [1, 1, 1, 1],
            "cooldown": True,
            "cooldownSwipe": True,
            "cooldownEdge": True,
            "cooldownTextDisabled": True,
            "inverse": False,
            "customTextUpdate": "update",
            "customText": make_bs_custom_text(),
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "event",
                        "events": "UNIT_AURA,PLAYER_ENTERING_WORLD,PWHUD_BS_THRESHOLD",
                        "custom": make_bs_trigger(),
                        "customDuration": make_bs_custom_duration(),
                    },
                    "untrigger": {
                        "custom": make_bs_untrigger(),
                    },
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=10, y_offset=0),
            ],
        },
        # 02 - OFF (Architettura nativa aura2 con showOnMissing e controllo sovrapposizioni BoM/GBoM)
        {
            "id": "Battle Shout - OFF warTank",
            "uid": "PWHUD_BS_OFF",
            "parent": "02 - Battle Shout warTank",
            "regionType": "icon",
            "internalVersion": 90,
            "xOffset": 0,
            "yOffset": 0,
            "width": 24,
            "height": 24,
            "displayIcon": "Interface\\Icons\\Ability_Warrior_BattleShout",
            "auto": False,
            "desaturate": True,
            "color": [0.6, 0.6, 0.6, 0.8],
            "triggers": {
                1: {
                    "trigger": {
                        "type": "aura2",
                        "unit": "player",
                        "auranames": [
                            "Battle Shout",
                            "Urlo di Battaglia",
                            "Greater Blessing of Might",
                            "Blessing of Might",
                            "Benedizione della Potenza Superiore",
                            "Benedizione della Potenza",
                        ],
                        "useName": True,
                        "debuffType": "HELPFUL",
                        "matchesShowOn": "showOnMissing",
                    },
                    "untrigger": {},
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("|cFFFF4444OFF|r", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=9, y_offset=1),
            ],
        },

        # =====================================================================
        # 03 - COMMANDING SHOUT (Gruppo Madre a x = -190, y = 0)
        # =====================================================================
        {
            "id": "03 - Commanding Shout warTank",
            "uid": "PWHUD_CS_GRP",
            "parent": "Class Warrior (Protection)",
            "regionType": "group",
            "internalVersion": 90,
            "xOffset": -205,
            "yOffset": 0,
            "controlledChildren": [
                "Commanding Shout - Active warTank",
                "Commanding Shout - OFF warTank",
            ],
        },
        # 03 - Active (mostra timer solo se il buff o Blood Pact è attivo ma con <= 30 secondi)
        {
            "id": "Commanding Shout - Active warTank",
            "uid": "PWHUD_CS_ACTIVE",
            "parent": "03 - Commanding Shout warTank",
            "regionType": "icon",
            "internalVersion": 90,
            "xOffset": 0,
            "yOffset": 0,
            "width": 24,
            "height": 24,
            "displayIcon": "Interface\\Icons\\Ability_Warrior_RallyingCry",
            "auto": False,
            "color": [1, 1, 1, 1],
            "cooldown": True,
            "cooldownSwipe": True,
            "cooldownEdge": True,
            "cooldownTextDisabled": True,
            "inverse": False,
            "customTextUpdate": "update",
            "customText": make_cs_custom_text(),
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "event",
                        "events": "UNIT_AURA,PLAYER_ENTERING_WORLD,PWHUD_CS_THRESHOLD",
                        "custom": make_cs_trigger(),
                        "customDuration": make_cs_custom_duration(),
                    },
                    "untrigger": {
                        "custom": make_cs_untrigger(),
                    },
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=10, y_offset=0),
            ],
        },
        # 03 - OFF (Architettura nativa aura2 con showOnMissing e controllo sovrapposizioni Blood Pact)
        {
            "id": "Commanding Shout - OFF warTank",
            "uid": "PWHUD_CS_OFF",
            "parent": "03 - Commanding Shout warTank",
            "regionType": "icon",
            "internalVersion": 90,
            "xOffset": 0,
            "yOffset": 0,
            "width": 24,
            "height": 24,
            "displayIcon": "Interface\\Icons\\Ability_Warrior_RallyingCry",
            "auto": False,
            "desaturate": True,
            "color": [0.6, 0.6, 0.6, 0.8],
            "triggers": {
                1: {
                    "trigger": {
                        "type": "aura2",
                        "unit": "player",
                        "auranames": [
                            "Commanding Shout",
                            "Urlo di Comando",
                            "Blood Pact",
                            "Patto di Sangue",
                        ],
                        "useName": True,
                        "debuffType": "HELPFUL",
                        "matchesShowOn": "showOnMissing",
                    },
                    "untrigger": {},
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("|cFFFF4444OFF|r", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=9, y_offset=1),
            ],
        },

        # =====================================================================
        # 04b - VIGILANCE (Gruppo Madre a x = -200, y = 0 - Modello Focus Magic)
        # =====================================================================
        {
            "id": "04b - Vigilance warTank",
            "uid": "PWHUD_VIGILANCE_GRP",
            "parent": "Class Warrior (Protection)",
            "regionType": "group",
            "internalVersion": 90,
            "xOffset": -179,
            "yOffset": 0,
            "controlledChildren": [
                "Vigilance - Active warTank",
                "Vigilance - OFF warTank",
            ],
        },
        # 04b - Active (mostra timer solo se il buff su alleato ha <= 60 secondi rimanenti)
        {
            "id": "Vigilance - Active warTank",
            "uid": "PWHUD_VIGILANCE_ACTIVE",
            "parent": "04b - Vigilance warTank",
            "regionType": "icon",
            "internalVersion": 90,
            "xOffset": 0,
            "yOffset": 0,
            "width": 24,
            "height": 24,
            "displayIcon": "Interface\\Icons\\Ability_Warrior_Vigilance",
            "auto": False,
            "color": [1, 1, 1, 1],
            "cooldown": True,
            "cooldownSwipe": True,
            "cooldownEdge": False,
            "cooldownTextDisabled": True,
            "inverse": False,
            "customTextUpdate": "update",
            "customText": make_vigilance_custom_text(),
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "event",
                        "events": "CLEU:SPELL_AURA_APPLIED:SPELL_AURA_REFRESH:SPELL_AURA_REMOVED:SPELL_AURA_BROKEN:UNIT_DIED,UNIT_SPELLCAST_SUCCEEDED,UNIT_AURA,PLAYER_TARGET_CHANGED,PLAYER_FOCUS_CHANGED,RAID_ROSTER_UPDATE,PARTY_MEMBERS_CHANGED,PLAYER_ENTERING_WORLD,ZONE_CHANGED_NEW_AREA",
                        "custom": make_vigilance_active_trigger(),
                        "customDuration": make_vigilance_custom_duration(),
                        "customIcon": """function()
    return "Interface\\\\Icons\\\\Ability_Warrior_Vigilance"
end""",
                    },
                    "untrigger": {
                        "custom": make_vigilance_active_untrigger(),
                    }
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("%c", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=10),
            ],
        },
        # 04b - OFF (allerta prominente con icona desaturata e testo rosso 'OFF' se nessun alleato ha il buff)
        {
            "id": "Vigilance - OFF warTank",
            "uid": "PWHUD_VIGILANCE_OFF",
            "parent": "04b - Vigilance warTank",
            "regionType": "icon",
            "internalVersion": 90,
            "xOffset": 0,
            "yOffset": 0,
            "width": 24,
            "height": 24,
            "displayIcon": "Interface\\Icons\\Ability_Warrior_Vigilance",
            "desaturate": True,
            "color": [0.6, 0.6, 0.6, 0.8],
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "event",
                        "events": "CLEU:SPELL_AURA_APPLIED:SPELL_AURA_REFRESH:SPELL_AURA_REMOVED:SPELL_AURA_BROKEN:UNIT_DIED,UNIT_SPELLCAST_SUCCEEDED,UNIT_AURA,PLAYER_TARGET_CHANGED,PLAYER_FOCUS_CHANGED,RAID_ROSTER_UPDATE,PARTY_MEMBERS_CHANGED,PLAYER_ENTERING_WORLD,ZONE_CHANGED_NEW_AREA,CHARACTER_POINTS_CHANGED,PLAYER_TALENT_UPDATE",
                        "custom": make_vigilance_off_trigger(),
                    },
                    "untrigger": {
                        "custom": make_vigilance_off_untrigger(),
                    }
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("|cFFFF4444OFF|r", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=9),
            ],
        },

        # =====================================================================
        # 04 - DEFENSIVE STANCE (Gruppo Madre a x = -158, y = 0)
        # =====================================================================
        {
            "id": "04 - Defensive Stance warTank",
            "uid": "PWHUD_STANCE_GRP",
            "parent": "Class Warrior (Protection)",
            "regionType": "group",
            "internalVersion": 90,
            "xOffset": -153,
            "yOffset": 0,
            "controlledChildren": [
                "04 - Defensive Stance - OutOfStance warTank",
            ],
        },
        {
            "id": "04 - Defensive Stance - OutOfStance warTank",
            "uid": "PWHUD_STANCE_WARN",
            "parent": "04 - Defensive Stance warTank",
            "regionType": "icon",
            "internalVersion": 90,
            "width": 24,
            "height": 24,
            "displayIcon": "Interface\\Icons\\Ability_Warrior_DefensiveStance",
            "auto": False,
            "color": [1, 0.2, 0.1, 1],
            "desaturate": False,
            "subRegions": [
                {"type": "subbackground"},
                make_subtext("STANCE", justify="CENTER", anchor_point="INNER_BOTTOM", font_size=8, y_offset=1),
            ],
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "custom": """function()
    local form = GetShapeshiftForm()
    return form ~= 2 and UnitAffectingCombat("player")
end""",
                    },
                    "untrigger": {},
                },
                "activeTriggerMode": -10,
            },
        },
    ]
