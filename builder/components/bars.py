"""
Modulo Componente: 14 - Rage Bar & 16 - Castbar warTank
========================================================
Gestisce le barre centrali sincronizzate a 278px di larghezza:
1. 14 - Rage Bar (278x14px a y = -20):
   - Barra della rabbia (powertype = 1) con texture statusbar.
   - Colore base: rosso sangue [0.78, 0.12, 0.12, 1.0].
   - Transizione cromatica dinamica ad ambra dorato [1.0, 0.65, 0.10, 1.0] a >= 45 Rage (soglia scarico sicuro Heroic Strike/Cleave).
   - Allerta starvation a < 25 Rage: colore rosso scuro [0.45, 0.05, 0.05, 1.0].
   - Testo centrale: valore numerico rabbia (%p).
2. 16 - Castbar warTank (Gruppo 278x20px a y = +8):
   - Castbar - Target warTank (Aurabar 278x20px, y = 0, inverse = True, scorrimento da destra a sinistra).
     * Priorità assoluta sul cast del player in caso di sovrapposizione.
     * Advisor intelligente a 4 stati (BOTH / KICK / REFLECT / IMMUNE) validato Classic/TBC/WotLK (Mob, PG, Boss): Shield Bash vs Spell Reflection vs Immune con tracker CLEU per spellId/spellSchool, filtri isTradeSkill/canali/fisici/cure/AoE e whitelist boss.
     * Colori dinamici: Magenta/Viola [0.78, 0.25, 0.95] per Reflect, Ciano [0.0, 0.85, 1.0] per Kick/Both, Grigio [0.50, 0.50, 0.50] per Immune.
     * Dicitura Opzione A: NomeSpell [SHIELD BASH] / [SHIELD BASH / REFLECT] / [SPELL REFLECTION] / [IMMUNE].
   - Castbar - Player warTank (Aurabar 278x20px, y = 0, inverse = True, scorrimento da destra a sinistra).
     * Mostra lanci/canalizzazioni del giocatore con icona dinamica, soppressione su cast del bersaglio e stop immediato su interruzione.
"""
from builder.core.helpers import make_subtext
from builder.core.constants import (
    TEXTURE_STATUSBAR,
    COLOR_RAGE,
    COLOR_RAGE_DUMP,
    COLOR_RAGE_STARVED,
    COLOR_RAGE_BG,
    COLOR_CASTBAR,
    COLOR_CASTBAR_REFLECT,
    COLOR_CASTBAR_IMMUNE,
    COLOR_CASTBAR_BG,
)


SHARED_CASTBAR_LOGIC_LUA = r"""_G.PWHUD_InitCastAdvisor = function()
    _G.PWHUD_CastTracker = _G.PWHUD_CastTracker or {}

    if not _G.PWHUD_CastTrackerFrame then
        local cf = CreateFrame("Frame")
        rawset(_G, "PWHUD_CastTrackerFrame", cf)
        cf:RegisterEvent("COMBAT_LOG_EVENT_UNFILTERED")
        cf:RegisterEvent("PLAYER_ENTERING_WORLD")
        cf:RegisterEvent("PLAYER_REGEN_ENABLED")
        cf:SetScript("OnEvent", function(self, event, ...)
            if event == "PLAYER_ENTERING_WORLD" or event == "PLAYER_REGEN_ENABLED" then
                if wipe then
                    wipe(_G.PWHUD_CastTracker)
                else
                    _G.PWHUD_CastTracker = {}
                end
                return
            end
            if event == "COMBAT_LOG_EVENT_UNFILTERED" then
                local _, subEvent, sourceGUID, _, _, destGUID, destName, _, spellId, spellName, spellSchool = ...
                if (subEvent == "SPELL_CAST_START" or subEvent == "SPELL_CAST_SUCCESS") and sourceGUID then
                    local tr = _G.PWHUD_CastTracker
                    local entry = tr[sourceGUID]
                    if not entry then
                        entry = {}
                        tr[sourceGUID] = entry
                    end
                    entry.spellId = spellId
                    entry.spellName = spellName
                    entry.spellSchool = spellSchool
                    entry.destGUID = destGUID
                    entry.destName = destName
                    entry.ts = GetTime()
                end
            end
        end)
    end

    if not _G.PWHUD_CastMeta then
        local noReflectIds = {
            -- Cure / Resurrezioni PG & NPC (Classic / TBC / WotLK)
            [635]=true, [639]=true, [647]=true, [1026]=true, [1042]=true, [3472]=true, [10328]=true, [10329]=true, [25292]=true, [27135]=true, [27136]=true, [48781]=true, [48782]=true,
            [19750]=true, [19939]=true, [19940]=true, [19941]=true, [19942]=true, [19943]=true, [27137]=true, [48784]=true, [48785]=true,
            [2050]=true, [2054]=true, [2055]=true, [6063]=true, [6064]=true, [2060]=true, [10963]=true, [10964]=true, [10965]=true, [25314]=true, [25210]=true, [25213]=true, [48062]=true, [48063]=true,
            [2061]=true, [9472]=true, [9473]=true, [9474]=true, [10915]=true, [10916]=true, [10917]=true, [25233]=true, [25235]=true, [48070]=true, [48071]=true,
            [32546]=true, [48119]=true, [48120]=true, [596]=true, [996]=true, [10960]=true, [10961]=true, [25316]=true, [25308]=true, [48072]=true,
            [331]=true, [332]=true, [547]=true, [913]=true, [939]=true, [959]=true, [8005]=true, [10395]=true, [10396]=true, [25357]=true, [25391]=true, [25396]=true, [49272]=true, [49273]=true,
            [8004]=true, [8008]=true, [8010]=true, [10466]=true, [10467]=true, [10468]=true, [25420]=true, [49275]=true, [49276]=true,
            [1064]=true, [10622]=true, [10623]=true, [25422]=true, [25423]=true, [55458]=true, [55459]=true,
            [5185]=true, [8936]=true, [50464]=true, [48378]=true, [48443]=true, [48447]=true, [740]=true,
            [2006]=true, [2008]=true, [7328]=true, [20484]=true, [50769]=true, [982]=true, [136]=true,
            [16588]=true, [23954]=true, [30878]=true,
            [65875]=true, [65876]=true, [67303]=true, [67304]=true, [67305]=true, [67306]=true, [67307]=true, [67308]=true,
            -- Specifici Anti-Reflect PvP & PvE (Mana Burn, Mass Dispel, AoE, Fisici)
            [8129]=true, [8131]=true, [10874]=true, [10875]=true, [10876]=true, [15800]=true,
            [32375]=true,
            [10]=true, [6141]=true, [8427]=true, [10185]=true, [10186]=true, [10187]=true, [27085]=true, [42940]=true,
            [2120]=true, [2121]=true, [8422]=true, [8423]=true, [10215]=true, [10216]=true, [27086]=true, [42925]=true, [42926]=true,
            [5740]=true, [6219]=true, [11677]=true, [11678]=true, [27212]=true, [47819]=true, [47820]=true,
            [16914]=true, [17401]=true, [17402]=true, [27012]=true, [48467]=true,
            [1949]=true, [11683]=true, [11684]=true, [27213]=true, [47823]=true,
            [1510]=true, [14294]=true, [14295]=true, [27022]=true, [58434]=true,
            [56641]=true, [34120]=true, [49051]=true, [49052]=true,
            [19434]=true, [20900]=true, [20901]=true, [20902]=true, [20903]=true, [20904]=true, [27065]=true, [49049]=true, [49050]=true,
            [64382]=true,
            [1464]=true, [8820]=true, [11604]=true, [11605]=true, [25241]=true, [25242]=true, [47474]=true, [47475]=true,
            -- Raid / Dungeon Boss Mechanics non riflettibili
            [28478]=true, [55802]=true,
            [71420]=true, [72007]=true, [72501]=true, [72502]=true,
            [62666]=true, [63276]=true,
            [71405]=true, [72804]=true, [72805]=true, [72806]=true, [71815]=true, [72809]=true, [72810]=true, [72811]=true,
            [69409]=true, [73797]=true, [73798]=true, [73799]=true,
            [68981]=true, [72259]=true, [74270]=true, [74271]=true,
            [70541]=true, [73779]=true, [73780]=true, [73781]=true,
            [72762]=true,
            [69057]=true, [70826]=true, [72088]=true, [72089]=true,
            [70768]=true, [70769]=true,
            [69051]=true,
            [66804]=true,
            [69167]=true,
            [52470]=true, [59348]=true,
            [52960]=true, [59835]=true,
        }

        local noReflectPatterns = {
            "heal", "cura", "curat", "holy light", "flash of light", "luce sacra", "lampo di luce",
            "mending", "ripar", "nourish", "nutrimento", "regrowth", "ricrescita", "renew", "rinnovamento",
            "resurrect", "risurre", "rebirth", "rinascita", "redemption", "redenzione", "revive", "rianima",
            "ancestral spirit", "spirito ancestrale", "summon", "evoca", "ritual", "rituale",
            "first aid", "primo soccorso", "bandage", "benda",
            "hearthstone", "pietra del focolare", "teleport", "portal", "teletrasporto", "portale",
            "tranquility", "tranquill", "divine hymn", "inno divino", "hymn of hope", "inno alla speranza",
            "evocation", "evocazione", "transformation", "trasformazione", "shroud", "velo dell'occulto",
            "spell reflection", "riflessione", "mirrored soul", "anima riflessa", "mirror image", "immagine speculare",
            "twin's pact", "patto dei gemelli",
            "blizzard", "bufera", "flamestrike", "colonna di fuoco", "rain of fire", "pioggia di fuoco",
            "hurricane", "uragano", "hellfire", "fuoco infernale", "volley", "raffica",
            "mass dispel", "dissipazione di massa", "arcane explosion", "esplosione arcana", "starfall", "pioggia di stelle",
            "consecration", "consacrazione", "death and decay", "morte e decadimento",
            "psychic scream", "urlo psichico", "howl of terror", "ululato del terrore", "shadowfury", "furia d'ombra",
            "defile", "profanazione", "infest", "infestazione", "remorseless winter", "inverno spietato",
            "bone spike", "spina d'ossa", "blight", "piaga", "slime spray", "spruzzo",
            "shock of sorrow", "urto del dolore", "soul shriek", "urlo dell'anima", "soulstorm", "tempesta d'anime",
            "searing flames", "fiamme ustionanti", "arcane vacuum", "vuoto arcano", "shockwave", "onda d'urto",
            "whirlwind", "turbine", "wailing souls", "anime piangenti", "smash", "slam", "bellowing roar",
            "lightning ring", "nova", "carrion swarm", "impale", "impalamento", "stomp", "breath", "soffio",
            "corrupt soul", "anima corrotta", "optic link", "void shift", "overlord's brand",
            "shadow lance", "lancia d'ombra", "frost tomb", "tomba di ghiaccio", "time warp", "explosive barrage",
            "mana burn", "bruciatura di mana", "steady shot", "tiro stabilizzato", "aimed shot", "tiro mirato",
            "multi-shot", "tiro multiplo", "shattering throw", "lancio frantumante",
            "shoot", "sparo", "throw", "lancio", "cursed arrow", "freccia maledetta", "soul reaper", "mietitura",
        }

        local bossReflectWhitelistIds = {
            [66532]=true, [66963]=true, [66964]=true, [66965]=true, -- Lord Jaraxxus: Fel Fireball
            [41410]=true, -- Essence of Desire: Deaden
            [29833]=true, -- Attumen: Intangible Presence
        }

        local bossReflectWhitelistNames = {
            ["fel fireball"]=true, ["palla di fuoco vile"]=true,
            ["deaden"]=true, ["intorpidimento"]=true,
            ["intangible presence"]=true, ["presenza intangibile"]=true,
            ["polymorph"]=true, ["metamorfosi"]=true,
            ["hex"]=true, ["maleficio"]=true,
            ["cyclone"]=true, ["ciclone"]=true,
            ["fear"]=true, ["paura"]=true,
            ["mind control"]=true, ["controllo mentale"]=true,
            ["chaos bolt"]=true, ["dardo del caos"]=true,
            ["lava burst"]=true, ["getto di lava"]=true,
            ["entangling roots"]=true, ["radici intrappolanti"]=true,
            ["repentance"]=true, ["penitenza"]=true,
        }

        local kickImmuneBuffIds = {
            [642]=true,
            [1022]=true, [5599]=true, [10278]=true,
            [45438]=true,
        }
        local kickImmuneBuffNames = {
            ["divine shield"]=true, ["scudo divino"]=true,
            ["hand of protection"]=true, ["mano di protezione"]=true,
            ["ice block"]=true, ["blocco di ghiaccio"]=true,
        }
        local selfReflectBuffIds = {
            [23920]=true, [36096]=true, [38599]=true,
        }
        local selfReflectBuffNames = {
            ["spell reflection"]=true, ["riflessione degli incantesimi"]=true,
        }
        local shroudBuffIds = {
            [70768]=true, [70769]=true,
        }
        local shroudBuffNames = {
            ["shroud of the occult"]=true, ["velo dell'occulto"]=true,
        }

        _G.PWHUD_CastMeta = {
            noReflectIds = noReflectIds,
            noReflectPatterns = noReflectPatterns,
            bossReflectWhitelistIds = bossReflectWhitelistIds,
            bossReflectWhitelistNames = bossReflectWhitelistNames,
            kickImmuneBuffIds = kickImmuneBuffIds,
            kickImmuneBuffNames = kickImmuneBuffNames,
            selfReflectBuffIds = selfReflectBuffIds,
            selfReflectBuffNames = selfReflectBuffNames,
            shroudBuffIds = shroudBuffIds,
            shroudBuffNames = shroudBuffNames,
            spellResultCache = {},
        }
    end

    _G.PWHUD_GetTargetCastInfo = function()
        if not UnitExists("target") or not UnitCanAttack("player", "target") or UnitIsDead("target") then
            return nil
        end

        local spell, rank, displayName, icon, startTime, endTime, isTradeSkill, castID, notInterruptible = UnitCastingInfo("target")
        local isChannel = false
        if not spell then
            local cName, cRank, cText, cTexture, cStart, cEnd, cTrade, cNotInt = UnitChannelInfo("target")
            if cName then
                spell = cName
                displayName = cText
                icon = cTexture
                startTime = cStart
                endTime = cEnd
                isTradeSkill = cTrade
                notInterruptible = cNotInt
                isChannel = true
            end
        end
        if not spell or isTradeSkill then return nil end

        if not icon and spell and GetSpellTexture then
            icon = GetSpellTexture(spell)
        end

        local now = GetTime()
        local rem = (endTime and (endTime / 1000 - now)) or 0
        local dur = (startTime and endTime and ((endTime - startTime) / 1000)) or 0

        local tGUID = UnitGUID("target")
        local pGUID = UnitGUID("player")
        local tracker = _G.PWHUD_CastTracker
        local cleuInfo = (tracker and tGUID) and tracker[tGUID] or nil
        if cleuInfo and ((cleuInfo.spellName and cleuInfo.spellName ~= spell) or (now - (cleuInfo.ts or 0) > 20)) then
            cleuInfo = nil
        end

        local spellId = cleuInfo and cleuInfo.spellId or nil
        local spellSchool = cleuInfo and cleuInfo.spellSchool or nil

        local isTargetingMe = UnitIsUnit("targettarget", "player")
        if cleuInfo and cleuInfo.destGUID == pGUID then
            isTargetingMe = true
        end

        local isPlayer = UnitIsPlayer("target")
        local tClassif = UnitClassification and UnitClassification("target") or "normal"
        local tLevel = UnitLevel and UnitLevel("target") or 80
        local isWorldBoss = (not isPlayer) and (tClassif == "worldboss" or tLevel == -1)

        local meta = _G.PWHUD_CastMeta
        local hasKickImmuneBuff = false
        local hasAuraMastery = false
        local hasConcAura = false
        local enemyHasReflect = false
        local enemyHasShroud = false

        for i = 1, 40 do
            local bName, _, _, _, _, _, _, _, _, _, bId = UnitBuff("target", i)
            if not bName then break end
            local bLower = string.lower(bName)
            if (bId and meta.kickImmuneBuffIds[bId]) or meta.kickImmuneBuffNames[bLower] then
                hasKickImmuneBuff = true
            end
            if bId == 31821 or bLower == "aura mastery" or bLower == "maestria nelle aure" then
                hasAuraMastery = true
            elseif bId == 19746 or bLower == "concentration aura" or bLower == "aura di concentrazione" then
                hasConcAura = true
            end
            if (bId and meta.selfReflectBuffIds[bId]) or meta.selfReflectBuffNames[bLower] then
                enemyHasReflect = true
            end
            if (bId and meta.shroudBuffIds[bId]) or meta.shroudBuffNames[bLower] then
                enemyHasShroud = true
            end
        end

        local lowerSpell = string.lower(spell)
        local isNoReflect = false
        if spellId and meta.noReflectIds[spellId] then
            isNoReflect = true
        else
            local cachedNoRef = meta.spellResultCache[lowerSpell]
            if cachedNoRef ~= nil then
                isNoReflect = cachedNoRef
            else
                for _, pat in ipairs(meta.noReflectPatterns) do
                    if string.find(lowerSpell, pat, 1, true) then
                        isNoReflect = true
                        break
                    end
                end
                meta.spellResultCache[lowerSpell] = isNoReflect
            end
        end

        -- Asse 1: Interrompibilita (Kick con Shield Bash / Pummel)
        local canKick = (not notInterruptible) and (not hasKickImmuneBuff) and (not enemyHasShroud) and (not (hasAuraMastery and hasConcAura))

        -- Asse 2: Riflettibilita (Spell Reflection)
        local isPhysical = (spellSchool == 1)
        local canReflect = (isTargetingMe == true) and (not isChannel) and (not isPhysical) and (not isNoReflect) and (not enemyHasReflect) and (not enemyHasShroud)
        if isWorldBoss and canReflect then
            local inBossWL = (spellId and meta.bossReflectWhitelistIds[spellId]) or meta.bossReflectWhitelistNames[lowerSpell]
            if not inBossWL then
                canReflect = false
            end
        end

        local hasShield = (GetInventoryItemID("player", 17) ~= nil)

        local sbStart, sbDur = GetSpellCooldown("Shield Bash")
        if not sbStart then sbStart, sbDur = GetSpellCooldown("Colpo di Scudo") end
        if not sbStart then sbStart, sbDur = GetSpellCooldown("Spaccatesta") end
        local sbReady = (sbDur == nil or sbDur <= 1.5 or (sbStart + sbDur <= now))

        local srStart, srDur = GetSpellCooldown("Spell Reflection")
        if not srStart then srStart, srDur = GetSpellCooldown("Riflessione degli Incantesimi") end
        local srReady = (srDur == nil or srDur <= 1.5 or (srStart + srDur <= now))

        local pStart, pDur = GetSpellCooldown("Pummel")
        if not pStart then pStart, pDur = GetSpellCooldown("Percossa") end
        if not pStart then pStart, pDur = GetSpellCooldown("Pestone") end
        local pummelReady = (pDur == nil or pDur <= 1.5 or (pStart + pDur <= now))

        local inMelee = (IsSpellInRange and (IsSpellInRange("Shield Bash", "target") == 1 or IsSpellInRange("Colpo di Scudo", "target") == 1 or IsSpellInRange("Spaccatesta", "target") == 1))
        if inMelee == nil or inMelee == false then
            inMelee = CheckInteractDistance("target", 3)
        end

        local res = {
            spell = spell,
            spellName = spell,
            spellId = spellId,
            spellSchool = spellSchool,
            icon = icon or "Interface\\Icons\\Temp",
            startTime = startTime,
            endTime = endTime,
            duration = dur,
            remaining = rem,
            notInterruptible = not canKick,
            canKick = canKick,
            canReflect = canReflect,
            isChannel = isChannel,
            isWorldBoss = isWorldBoss,
            isPlayer = isPlayer,
            enemyHasReflect = enemyHasReflect,
            action = "IMMUNE",
            recommended = "IMMUNE",
            actionType = "IMMUNE",
        }

        if canKick and canReflect then
            if hasShield and inMelee and sbReady then
                res.action = "SHIELD BASH / REFLECT"
                res.recommended = "SHIELD BASH"
                res.actionType = "BOTH"
            elseif hasShield and srReady then
                res.action = "SPELL REFLECTION"
                res.recommended = "SPELL REFLECTION"
                res.actionType = "REFLECT"
            elseif inMelee and pummelReady then
                res.action = "PUMMEL"
                res.recommended = "PUMMEL"
                res.actionType = "BOTH"
            elseif inMelee then
                res.action = "KICK (CD)"
                res.recommended = "STUN / KICK CD"
                res.actionType = "BOTH"
            else
                res.action = "KICKABLE"
                res.recommended = "KICKABLE"
                res.actionType = "BOTH"
            end
        elseif canKick and (not canReflect) then
            res.actionType = "KICK"
            if inMelee and hasShield and sbReady then
                res.action = "SHIELD BASH"
                res.recommended = "SHIELD BASH"
            elseif inMelee and pummelReady then
                res.action = "PUMMEL"
                res.recommended = "PUMMEL"
            elseif inMelee then
                res.action = "KICK (CD)"
                res.recommended = "STUN / KICK CD"
            else
                res.action = "KICKABLE"
                res.recommended = "KICKABLE"
            end
        elseif (not canKick) and canReflect then
            if hasShield and srReady then
                res.action = "SPELL REFLECTION"
                res.recommended = "SPELL REFLECTION"
                res.actionType = "REFLECT"
            else
                res.action = "IMMUNE (SR CD)"
                res.recommended = "IMMUNE"
                res.actionType = "IMMUNE"
            end
        else
            res.action = "IMMUNE"
            res.recommended = "IMMUNE"
            res.actionType = "IMMUNE"
        end

        return res
    end
    _G.PWHUD_GetKickInfo = _G.PWHUD_GetTargetCastInfo
end
_G.PWHUD_InitCastAdvisor()"""


def build_bars_auras() -> list[dict]:
    """
    Costruisce e restituisce le barre dell'HUD:
    - 14 - Rage Bar warTank (Aurabar 278x14px a y = -20)
    - 16 - Castbar warTank (Gruppo 278x20px a y = +8)
    - Castbar - Target warTank (Aurabar 278x20px, inverse = True, scorrimento dx -> sx)
    - Castbar - Player warTank (Aurabar 278x20px, inverse = True, scorrimento dx -> sx)
    """
    return [
        # =====================================================================
        # 14 - RAGE BAR
        # =====================================================================
        {
            "id": "14 - Rage Bar warTank",
            "uid": "PWHUD_RAGEBAR",
            "parent": "Class Warrior (Protection)",
            "regionType": "aurabar",
            "internalVersion": 90,
            "width": 278,
            "height": 14,
            "xOffset": 0,
            "yOffset": -20,
            "barColor": COLOR_RAGE,
            "backgroundColor": COLOR_RAGE_BG,
            "texture": TEXTURE_STATUSBAR,
            "displayText_format_1.percentpower_format": "Number",
            "displayText_format_1.percentpower_decimal_precision": 0,
            "triggers": {
                1: {
                    "trigger": {
                        "type": "unit",
                        "event": "Power",
                        "unit": "player",
                        "powertype": 1,
                        "use_unit": True,
                        "use_powertype": True,
                    },
                    "untrigger": {}
                },
                "activeTriggerMode": -10,
            },
            "conditions": [
                # Condizione 1: Rage >= 45 -> Colore ambra dorato (Rage Dump / Heroic Strike sicuro)
                {
                    "check": {
                        "trigger": 1,
                        "variable": "power",
                        "op": ">=",
                        "value": "45",
                    },
                    "changes": [
                        {
                            "property": "barColor",
                            "value": COLOR_RAGE_DUMP,
                        }
                    ],
                },
                # Condizione 2: Rage < 25 -> Colore scuro desaturato (Starvation)
                {
                    "check": {
                        "trigger": 1,
                        "variable": "power",
                        "op": "<",
                        "value": "25",
                    },
                    "changes": [
                        {
                            "property": "barColor",
                            "value": COLOR_RAGE_STARVED,
                        }
                    ],
                },
            ],
            "subRegions": [
                make_subtext("%p", justify="CENTER", anchor_point="CENTER", font_size=12, y_offset=0),
            ],
        },

        # =====================================================================
        # 16 - CASTBAR WARTANK (GRUPPO CONTENITORE 278x20px a y = +8)
        # =====================================================================
        {
            "id": "16 - Castbar warTank",
            "uid": "PWHUD_CASTBAR",
            "parent": "Class Warrior (Protection)",
            "regionType": "group",
            "internalVersion": 90,
            "anchorPoint": "CENTER",
            "selfPoint": "CENTER",
            "xOffset": 0,
            "yOffset": 8,
            "controlledChildren": [
                "Castbar - Target warTank",
                "Castbar - Player warTank",
            ],
        },

        # =====================================================================
        # 16a - CASTBAR TARGET (SCORRIMENTO DA DESTRA VERSO SINISTRA - INVERSE)
        # =====================================================================
        {
            "id": "Castbar - Target warTank",
            "uid": "PWHUD_CASTBAR_TARGET",
            "parent": "16 - Castbar warTank",
            "regionType": "aurabar",
            "internalVersion": 90,
            "width": 278,
            "height": 20,
            "xOffset": 0,
            "yOffset": 0,
            "barColor": [0.0, 0.85, 1.0, 1.0],
            "backgroundColor": COLOR_CASTBAR_BG,
            "texture": TEXTURE_STATUSBAR,
            "inverse": True,
            "icon": True,
            "icon_side": "LEFT",
            "iconSource": 0,
            "auto": True,
            "displayIcon": "Interface\\Icons\\Temp",
            "customTextUpdate": "update",
            "actions": {
                "init": {
                    "do_custom": True,
                    "custom": SHARED_CASTBAR_LOGIC_LUA,
                },
                "start": {},
                "finish": {},
            },
            "customText": r"""function()
                if not _G.PWHUD_GetTargetCastInfo then
                    if _G.PWHUD_InitCastAdvisor then _G.PWHUD_InitCastAdvisor() end
                    if not _G.PWHUD_GetTargetCastInfo then return "" end
                end
                local ki = _G.PWHUD_GetTargetCastInfo()
                if not ki then return "" end
                local reg = aura_env and aura_env.region
                local bar = reg and (reg.bar or (reg.SetVertexColor and reg))
                if reg and reg.icon and reg.icon.SetTexture and ki.icon then
                    reg.icon:SetTexture(ki.icon)
                end
                if ki.actionType == "REFLECT" then
                    if bar and bar.SetVertexColor then bar:SetVertexColor(0.78, 0.25, 0.95, 1.0) end
                    return string.format("|cFFFF55FF%s [%s]|r", ki.spell, ki.action or "SPELL REFLECTION")
                elseif ki.actionType == "IMMUNE" then
                    if bar and bar.SetVertexColor then bar:SetVertexColor(0.50, 0.50, 0.50, 0.85) end
                    return string.format("|cFF888888%s [%s]|r", ki.spell, ki.action or "IMMUNE")
                elseif ki.actionType == "BOTH" then
                    if bar and bar.SetVertexColor then bar:SetVertexColor(0.0, 0.85, 1.0, 1.0) end
                    return string.format("|cFF00FFFF%s [%s]|r", ki.spell, ki.action or "SHIELD BASH / REFLECT")
                else
                    if bar and bar.SetVertexColor then bar:SetVertexColor(0.0, 0.85, 1.0, 1.0) end
                    return string.format("|cFF00FFFF%s [%s]|r", ki.spell, ki.action or "SHIELD BASH")
                end
            end""",
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "custom": r"""function()
                            if not _G.PWHUD_GetTargetCastInfo then
                                """ + SHARED_CASTBAR_LOGIC_LUA + r"""
                            end
                            local ki = _G.PWHUD_GetTargetCastInfo and _G.PWHUD_GetTargetCastInfo()
                            return (ki ~= nil)
                        end""",
                        "customDuration": r"""function()
                            if not _G.PWHUD_GetTargetCastInfo and _G.PWHUD_InitCastAdvisor then
                                _G.PWHUD_InitCastAdvisor()
                            end
                            local ki = _G.PWHUD_GetTargetCastInfo and _G.PWHUD_GetTargetCastInfo()
                            if ki and ki.duration and ki.endTime then
                                return ki.duration, ki.endTime / 1000
                            end
                            local spell, rank, disp, icon, sTime, eTime = UnitCastingInfo("target")
                            if spell and sTime and eTime then
                                return (eTime - sTime) / 1000, eTime / 1000
                            end
                            local cName, cRank, cText, cTexture, cStart, cEnd = UnitChannelInfo("target")
                            if cName and cStart and cEnd then
                                return (cEnd - cStart) / 1000, cEnd / 1000
                            end
                            return 0, 0
                        end""",
                        "customIcon": r"""function()
                            if not _G.PWHUD_GetTargetCastInfo and _G.PWHUD_InitCastAdvisor then
                                _G.PWHUD_InitCastAdvisor()
                            end
                            local ki = _G.PWHUD_GetTargetCastInfo and _G.PWHUD_GetTargetCastInfo()
                            local icon = ki and ki.icon
                            if not icon then
                                local spell, rank, disp, tIcon = UnitCastingInfo("target")
                                if not spell then
                                    local cName, cRank, cText, cTexture = UnitChannelInfo("target")
                                    if cName then
                                        spell = cName
                                        tIcon = cTexture
                                    end
                                end
                                if not tIcon and spell and GetSpellTexture then
                                    tIcon = GetSpellTexture(spell)
                                end
                                icon = tIcon
                            end
                            if icon and aura_env and aura_env.region and aura_env.region.icon and aura_env.region.icon.SetTexture then
                                aura_env.region.icon:SetTexture(icon)
                            end
                            return icon or "Interface\\Icons\\Temp"
                        end""",
                    },
                    "untrigger": {
                        "type": "custom",
                        "custom": r"""function()
                            if not _G.PWHUD_GetTargetCastInfo and _G.PWHUD_InitCastAdvisor then
                                _G.PWHUD_InitCastAdvisor()
                            end
                            local ki = _G.PWHUD_GetTargetCastInfo and _G.PWHUD_GetTargetCastInfo()
                            return (ki == nil)
                        end"""
                    }
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                make_subtext("%c", justify="LEFT", anchor_point="INNER_LEFT", font_size=11, y_offset=0, x_offset=6),
                make_subtext("%p", justify="RIGHT", anchor_point="INNER_RIGHT", font_size=11, y_offset=0, x_offset=-6),
            ],
        },

        # =====================================================================
        # 16b - CASTBAR PLAYER (SCORRIMENTO DA DESTRA VERSO SINISTRA - INVERSE)
        # =====================================================================
        {
            "id": "Castbar - Player warTank",
            "uid": "PWHUD_CASTBAR_PLAYER",
            "parent": "16 - Castbar warTank",
            "regionType": "aurabar",
            "internalVersion": 90,
            "width": 278,
            "height": 20,
            "xOffset": 0,
            "yOffset": 0,
            "barColor": [0.0, 0.77, 1.0, 1.0],
            "backgroundColor": COLOR_CASTBAR_BG,
            "texture": TEXTURE_STATUSBAR,
            "inverse": True,
            "icon": True,
            "icon_side": "LEFT",
            "iconSource": 0,
            "auto": True,
            "displayIcon": "Interface\\Icons\\Temp",
            "customTextUpdate": "update",
            "customText": r"""function()
                local spell, rank, disp, icon = UnitCastingInfo("player")
                if not spell then
                    local cName, cRank, cText, cTexture = UnitChannelInfo("player")
                    if cName then
                        spell = cName
                        icon = cTexture
                    end
                end
                if not spell then return "" end
                if not icon and GetSpellTexture then
                    icon = GetSpellTexture(spell)
                end
                if icon and aura_env and aura_env.region and aura_env.region.icon and aura_env.region.icon.SetTexture then
                    aura_env.region.icon:SetTexture(icon)
                end
                return spell
            end""",
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "update",
                        "custom": r"""function()
                            -- Priorita 1: Se il target sta castando, sopprime completamente il cast del player
                            local targetSpell = UnitCastingInfo("target")
                            if not targetSpell then
                                targetSpell = UnitChannelInfo("target")
                            end
                            if targetSpell then return false end

                            -- Priorita 2: Cast del giocatore (lancio standard o incanalato)
                            local spell = UnitCastingInfo("player")
                            if not spell then
                                spell = UnitChannelInfo("player")
                            end
                            return (spell ~= nil)
                        end""",
                        "customDuration": r"""function()
                            local targetSpell = UnitCastingInfo("target")
                            if not targetSpell then
                                targetSpell = UnitChannelInfo("target")
                            end
                            if targetSpell then return 0, 0 end

                            local spell, rank, disp, icon, sTime, eTime = UnitCastingInfo("player")
                            if spell and sTime and eTime then
                                return (eTime - sTime) / 1000, eTime / 1000
                            end
                            local cName, cRank, cText, cTexture, csTime, ceTime = UnitChannelInfo("player")
                            if cName and csTime and ceTime then
                                return (ceTime - csTime) / 1000, ceTime / 1000
                            end
                            return 0, 0
                        end""",
                        "customIcon": r"""function()
                            local spell, rank, disp, icon = UnitCastingInfo("player")
                            if not spell then
                                local cName, cRank, cText, cTexture = UnitChannelInfo("player")
                                if cName then
                                    spell = cName
                                    icon = cTexture
                                end
                            end
                            if not icon and spell and GetSpellTexture then
                                icon = GetSpellTexture(spell)
                            end
                            if icon and aura_env and aura_env.region and aura_env.region.icon and aura_env.region.icon.SetTexture then
                                aura_env.region.icon:SetTexture(icon)
                            end
                            return icon or "Interface\\Icons\\Temp"
                        end""",
                    },
                    "untrigger": {
                        "type": "custom",
                        "custom": r"""function()
                            -- Se il target sta castando, nasconde il player cast
                            local targetSpell = UnitCastingInfo("target")
                            if not targetSpell then targetSpell = UnitChannelInfo("target") end
                            if targetSpell then return true end

                            -- Se il player ha interrotto o terminato il cast, untrigger immediato
                            local spell = UnitCastingInfo("player")
                            if not spell then spell = UnitChannelInfo("player") end
                            return (spell == nil)
                        end"""
                    }
                },
                "activeTriggerMode": -10,
            },
            "subRegions": [
                make_subtext("%c", justify="LEFT", anchor_point="INNER_LEFT", font_size=11, y_offset=0, x_offset=6),
                make_subtext("%p", justify="RIGHT", anchor_point="INNER_RIGHT", font_size=11, y_offset=0, x_offset=-6),
            ],
        },
    ]
