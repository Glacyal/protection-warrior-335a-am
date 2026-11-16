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


# =============================================================================
# LOGICA LUA CONDIVISA: TANK BUSTER ALERT (WotLK 3.3.5a Complete Raid DB)
# =============================================================================
TANK_BUSTER_DB_LUA = r"""
_G.PWHUD_TankBustersDB = {
    -- Icecrown Citadel (ICC)
    [69409] = { min = 1, tag = "SWAP", desc = "Soul Reaper (Lich King 10N)" },
    [73797] = { min = 1, tag = "SWAP", desc = "Soul Reaper (Lich King 25N)" },
    [73798] = { min = 1, tag = "SWAP", desc = "Soul Reaper (Lich King 10H)" },
    [73799] = { min = 1, tag = "SWAP", desc = "Soul Reaper (Lich King 25H)" },
    [72219] = { min = 8, tag = "STACK", desc = "Gastric Bloat (Festergut 10N)" },
    [72551] = { min = 8, tag = "STACK", desc = "Gastric Bloat (Festergut 25N)" },
    [72552] = { min = 8, tag = "STACK", desc = "Gastric Bloat (Festergut 10H)" },
    [72553] = { min = 8, tag = "STACK", desc = "Gastric Bloat (Festergut 25H)" },
    [72410] = { min = 1, tag = "SWAP", desc = "Rune of Blood (Deathbringer Saurfang)" },
    [70127] = { min = 5, tag = "STACK", desc = "Mystic Buffet (Sindragosa Phase 3)" },
    [70128] = { min = 5, tag = "STACK", desc = "Mystic Buffet (Sindragosa Phase 3 25)" },
    [71623] = { min = 2, tag = "STACK", desc = "Delirious Slash (Blood-Queen Lana'thel)" },
    [71624] = { min = 2, tag = "STACK", desc = "Delirious Slash (Blood-Queen Lana'thel 25)" },
    [72451] = { min = 2, tag = "STACK", desc = "Mutated Plague (Professor Putricide Phase 3)" },
    [72452] = { min = 2, tag = "STACK", desc = "Mutated Plague (Professor Putricide 25N)" },
    [72453] = { min = 2, tag = "STACK", desc = "Mutated Plague (Professor Putricide 10H)" },
    [72454] = { min = 2, tag = "STACK", desc = "Mutated Plague (Professor Putricide 25H)" },
    [69674] = { min = 1, tag = "INFECT", desc = "Mutated Infection (Rotface 10N)" },
    [71224] = { min = 1, tag = "INFECT", desc = "Mutated Infection (Rotface 25N)" },
    [73022] = { min = 1, tag = "INFECT", desc = "Mutated Infection (Rotface 10H)" },
    [73023] = { min = 1, tag = "INFECT", desc = "Mutated Infection (Rotface 25H)" },
    [70751] = { min = 3, tag = "STACK", desc = "Corrosion (Valithria Zombie)" },
    [71236] = { min = 3, tag = "STACK", desc = "Corrosion (Valithria Zombie 25)" },
    [70633] = { min = 1, tag = "SPRAY", desc = "Gut Spray (Valithria Abomination)" },
    [71232] = { min = 1, tag = "SPRAY", desc = "Gut Spray (Valithria Abomination 25)" },
    [71127] = { min = 3, tag = "STACK", desc = "Severed Flesh (Deathbound Ward / ICC Trash)" },

    -- Ruby Sanctum (RS)
    [74562] = { min = 1, tag = "RUN", desc = "Fiery Combustion (Halion Physical 10)" },
    [74567] = { min = 1, tag = "RUN", desc = "Fiery Combustion (Halion Physical 25)" },
    [74795] = { min = 1, tag = "RUN", desc = "Fiery Combustion (Halion Heroic)" },
    [74792] = { min = 1, tag = "RUN", desc = "Soul Consumption (Halion Twilight 10)" },
    [74793] = { min = 1, tag = "RUN", desc = "Soul Consumption (Halion Twilight 25)" },
    [74799] = { min = 1, tag = "RUN", desc = "Soul Consumption (Halion Heroic)" },
    [74367] = { min = 2, tag = "STACK", desc = "Cleave Armor (General Zarithrian)" },
    [74502] = { min = 1, tag = "BRAND", desc = "Enervating Brand (Baltharus the Warborn)" },

    -- Trial of the Crusader (TotC / ToGC)
    [67478] = { min = 2, tag = "STACK", desc = "Impale (Gormok 25N/H)" },
    [67479] = { min = 2, tag = "STACK", desc = "Impale (Gormok 25H)" },
    [66331] = { min = 2, tag = "STACK", desc = "Impale (Gormok 10N)" },
    [66823] = { min = 1, tag = "TOXIN", desc = "Paralytic Toxin (Acidmaw 10)" },
    [67618] = { min = 1, tag = "TOXIN", desc = "Paralytic Toxin (Acidmaw 25)" },
    [66237] = { min = 1, tag = "HEAL", desc = "Incinerate Flesh (Lord Jaraxxus 10N)" },
    [67049] = { min = 1, tag = "HEAL", desc = "Incinerate Flesh (Lord Jaraxxus 25N)" },
    [67050] = { min = 1, tag = "HEAL", desc = "Incinerate Flesh (Lord Jaraxxus 10H)" },
    [67051] = { min = 1, tag = "HEAL", desc = "Incinerate Flesh (Lord Jaraxxus 25H)" },
    [67847] = { min = 2, tag = "STACK", desc = "Expose Weakness (Anub'arak Burrower 10)" },
    [67848] = { min = 2, tag = "STACK", desc = "Expose Weakness (Anub'arak Burrower 25)" },
    [67849] = { min = 2, tag = "STACK", desc = "Expose Weakness (Anub'arak Burrower H)" },

    -- Ulduar
    [64412] = { min = 3, tag = "STACK", desc = "Phase Punch (Algalon 10)" },
    [64417] = { min = 3, tag = "STACK", desc = "Phase Punch (Algalon 25)" },
    [62130] = { min = 1, tag = "SWAP", desc = "Unbalancing Strike (Thorim 10)" },
    [62131] = { min = 1, tag = "SWAP", desc = "Unbalancing Strike (Thorim 25)" },
    [61903] = { min = 1, tag = "FUSION", desc = "Fusion Punch (Steelbreaker 10)" },
    [63493] = { min = 1, tag = "FUSION", desc = "Fusion Punch (Steelbreaker 25)" },
    [61888] = { min = 1, tag = "MELT", desc = "Overwhelming Power (Steelbreaker 10)" },
    [64637] = { min = 1, tag = "MELT", desc = "Overwhelming Power (Steelbreaker 25)" },
    [64771] = { min = 2, tag = "STACK", desc = "Fuse Armor (Razorscale 10)" },
    [64772] = { min = 2, tag = "STACK", desc = "Fuse Armor (Razorscale 25)" },
    [62661] = { min = 1, tag = "CD!", desc = "Surge of Darkness (General Vezax 10)" },
    [62662] = { min = 1, tag = "CD!", desc = "Surge of Darkness (General Vezax 25)" },
    [62997] = { min = 1, tag = "PLASMA", desc = "Plasma Blast (Mimiron 10)" },
    [64529] = { min = 1, tag = "PLASMA", desc = "Plasma Blast (Mimiron 25)" },
    [63355] = { min = 2, tag = "STACK", desc = "Crunch Armor (Kologarn 10)" },
    [64002] = { min = 2, tag = "STACK", desc = "Crunch Armor (Kologarn 25)" },
    [62717] = { min = 1, tag = "POT", desc = "Slag Pot (Ignis 10)" },
    [63477] = { min = 1, tag = "POT", desc = "Slag Pot (Ignis 25)" },

    -- Naxxramas, VoA, Sartharion
    [25646] = { min = 4, tag = "STACK", desc = "Mortal Wound (Gluth)" },
    [28832] = { min = 3, tag = "STACK", desc = "Mark of Blaumeux (4 Horsemen)" },
    [28833] = { min = 3, tag = "STACK", desc = "Mark of Rivendare (4 Horsemen)" },
    [28834] = { min = 3, tag = "STACK", desc = "Mark of Korth'azz (4 Horsemen)" },
    [28835] = { min = 3, tag = "STACK", desc = "Mark of Zeliek (4 Horsemen)" },
    [72098] = { min = 4, tag = "STACK", desc = "Frostbite (Toravon the Ice Watcher - VoA)" },
    [57948] = { min = 1, tag = "SHADOW", desc = "Twilight Torment (Sartharion)" },
}

_G.PWHUD_TankBustersByName = {
    ["Soul Reaper"] = { min = 1, tag = "SWAP" },
    ["Mietitura d'Anime"] = { min = 1, tag = "SWAP" },
    ["Gastric Bloat"] = { min = 8, tag = "STACK" },
    ["Gonfiore Gastrico"] = { min = 8, tag = "STACK" },
    ["Rune of Blood"] = { min = 1, tag = "SWAP" },
    ["Runa del Sangue"] = { min = 1, tag = "SWAP" },
    ["Mystic Buffet"] = { min = 5, tag = "STACK" },
    ["Raffica Mistica"] = { min = 5, tag = "STACK" },
    ["Delirious Slash"] = { min = 2, tag = "STACK" },
    ["Squarcio Delirante"] = { min = 2, tag = "STACK" },
    ["Mutated Plague"] = { min = 2, tag = "STACK" },
    ["Peste Mutata"] = { min = 2, tag = "STACK" },
    ["Mutated Infection"] = { min = 1, tag = "INFECT" },
    ["Infezione Mutata"] = { min = 1, tag = "INFECT" },
    ["Corrosion"] = { min = 3, tag = "STACK" },
    ["Corrosione"] = { min = 3, tag = "STACK" },
    ["Gut Spray"] = { min = 1, tag = "SPRAY" },
    ["Spruzzo Viscerale"] = { min = 1, tag = "SPRAY" },
    ["Severed Flesh"] = { min = 3, tag = "STACK" },
    ["Carne Recisa"] = { min = 3, tag = "STACK" },
    ["Fiery Combustion"] = { min = 1, tag = "RUN" },
    ["Combustione Fiammeggiante"] = { min = 1, tag = "RUN" },
    ["Soul Consumption"] = { min = 1, tag = "RUN" },
    ["Consunzione d'Anime"] = { min = 1, tag = "RUN" },
    ["Cleave Armor"] = { min = 2, tag = "STACK" },
    ["Fendente Corazzato"] = { min = 2, tag = "STACK" },
    ["Enervating Brand"] = { min = 1, tag = "BRAND" },
    ["Marchio Snervante"] = { min = 1, tag = "BRAND" },
    ["Impale"] = { min = 2, tag = "STACK" },
    ["Impalamento"] = { min = 2, tag = "STACK" },
    ["Paralytic Toxin"] = { min = 1, tag = "TOXIN" },
    ["Tossina Paralizzante"] = { min = 1, tag = "TOXIN" },
    ["Incinerate Flesh"] = { min = 1, tag = "HEAL" },
    ["Incenerimento della Carne"] = { min = 1, tag = "HEAL" },
    ["Expose Weakness"] = { min = 2, tag = "STACK" },
    ["Scoperta del Punto Debole"] = { min = 2, tag = "STACK" },
    ["Phase Punch"] = { min = 3, tag = "STACK" },
    ["Pugno di Fase"] = { min = 3, tag = "STACK" },
    ["Unbalancing Strike"] = { min = 1, tag = "SWAP" },
    ["Colpo Sbilanciante"] = { min = 1, tag = "SWAP" },
    ["Fusion Punch"] = { min = 1, tag = "FUSION" },
    ["Pugno a Fusione"] = { min = 1, tag = "FUSION" },
    ["Overwhelming Power"] = { min = 1, tag = "MELT" },
    ["Potere Sovrastante"] = { min = 1, tag = "MELT" },
    ["Fuse Armor"] = { min = 2, tag = "STACK" },
    ["Fusione dell'Armatura"] = { min = 2, tag = "STACK" },
    ["Surge of Darkness"] = { min = 1, tag = "CD!" },
    ["Ondata di Tenebra"] = { min = 1, tag = "CD!" },
    ["Plasma Blast"] = { min = 1, tag = "PLASMA" },
    ["Esplosione di Plasma"] = { min = 1, tag = "PLASMA" },
    ["Crunch Armor"] = { min = 2, tag = "STACK" },
    ["Schiaccia-Armatura"] = { min = 2, tag = "STACK" },
    ["Slag Pot"] = { min = 1, tag = "POT" },
    ["Crogiolo di Scorie"] = { min = 1, tag = "POT" },
    ["Mortal Wound"] = { min = 4, tag = "STACK" },
    ["Ferita Mortale"] = { min = 4, tag = "STACK" },
    ["Mark of Blaumeux"] = { min = 3, tag = "STACK" },
    ["Marchio di Blaumeux"] = { min = 3, tag = "STACK" },
    ["Mark of Rivendare"] = { min = 3, tag = "STACK" },
    ["Marchio di Rivendare"] = { min = 3, tag = "STACK" },
    ["Mark of Korth'azz"] = { min = 3, tag = "STACK" },
    ["Marchio di Korth'azz"] = { min = 3, tag = "STACK" },
    ["Mark of Zeliek"] = { min = 3, tag = "STACK" },
    ["Marchio di Zeliek"] = { min = 3, tag = "STACK" },
    ["Frostbite"] = { min = 4, tag = "STACK" },
    ["Congelamento"] = { min = 4, tag = "STACK" },
    ["Twilight Torment"] = { min = 1, tag = "SHADOW" },
    ["Tormento del Crepuscolo"] = { min = 1, tag = "SHADOW" },
}
"""

TANK_BUSTER_CHECK_LUA = f"""function(force)
    local now = GetTime()
    local cached = _G.PWHUD_TankBusterCache
    if not force and cached and cached.time == now then
        return cached.isAlert, cached.name, cached.count, cached.icon, cached.dur, cached.exp, cached.tag
    end
    if not _G.PWHUD_TankBustersDB then
        {TANK_BUSTER_DB_LUA}
    end
    if _G.PWHUD_InitCore then _G.PWHUD_InitCore() end
    local pd = _G.PWHUD_GetPlayerDebuffs and _G.PWHUD_GetPlayerDebuffs()
    if not pd or not pd.list then
        return false, nil, 0, nil, 0, 0, ""
    end

    local db = _G.PWHUD_TankBustersDB
    local dbNames = _G.PWHUD_TankBustersByName

    for i = 1, #pd.list do
        local debuff = pd.list[i]
        local info = (debuff.spellId and db[debuff.spellId]) or (debuff.name and dbNames[debuff.name])
        if info then
            local count = debuff.count or 1
            if count == 0 then count = 1 end
            if count >= info.min then
                local tag = info.tag
                if tag == "STACK" then
                    tag = string.format("x%d", count)
                end
                local res = {{
                    time = now,
                    isAlert = true,
                    name = debuff.name,
                    count = count,
                    icon = debuff.icon or "Interface\\\\Icons\\\\Spell_Shadow_SoulLeech_3",
                    dur = debuff.duration or 0,
                    exp = debuff.expirationTime or 0,
                    tag = tag
                }}
                _G.PWHUD_TankBusterCache = res
                return true, debuff.name, count, res.icon, res.dur, res.exp, res.tag
            end
        end
    end

    _G.PWHUD_TankBusterCache = {{ time = now, isAlert = false, name = nil, count = 0, icon = nil, dur = 0, exp = 0, tag = "" }}
    return false, nil, 0, nil, 0, 0, ""
end"""

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
            "cooldownEdge": False,
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
                # 5. Tank Buster Alert (Comprehensive WotLK 3.3.5a Raid & Trash Database)
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
            "cooldown": True,
            "cooldownSwipe": True,
            "cooldownEdge": False,
            "actions": {
                "start": make_glow_action([1.0, 0.2, 0.2, 1.0]),
                "finish": {"do_glow": True, "glow_action": "hide"},
            },
            "triggers": {
                1: {
                    "trigger": {
                        "type": "custom",
                        "custom_type": "status",
                        "check": "event",
                        "events": "UNIT_AURA,PLAYER_TARGET_CHANGED,COMBAT_LOG_EVENT_UNFILTERED,PLAYER_ENTERING_WORLD",
                        "custom": f"""function(event, ...)
                            _G.PWHUD_CheckTankBusters = _G.PWHUD_CheckTankBusters or {TANK_BUSTER_CHECK_LUA}
                            local isAlert = _G.PWHUD_CheckTankBusters(true)
                            return isAlert
                        end""",
                        "customText": f"""function()
                            _G.PWHUD_CheckTankBusters = _G.PWHUD_CheckTankBusters or {TANK_BUSTER_CHECK_LUA}
                            local isAlert, name, count, icon, dur, exp, tag = _G.PWHUD_CheckTankBusters()
                            if isAlert then return tag or "SWAP" end
                            return ""
                        end""",
                        "customIcon": f"""function()
                            _G.PWHUD_CheckTankBusters = _G.PWHUD_CheckTankBusters or {TANK_BUSTER_CHECK_LUA}
                            local isAlert, name, count, icon = _G.PWHUD_CheckTankBusters()
                            if isAlert and icon then return icon end
                            return "Interface\\Icons\\Spell_Shadow_SoulLeech_3"
                        end""",
                        "customDuration": f"""function()
                            _G.PWHUD_CheckTankBusters = _G.PWHUD_CheckTankBusters or {TANK_BUSTER_CHECK_LUA}
                            local isAlert, name, count, icon, dur, exp = _G.PWHUD_CheckTankBusters()
                            if isAlert and exp and exp > 0 then
                                return dur or 0, exp
                            end
                            return 0, 0
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
