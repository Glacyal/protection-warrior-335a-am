"""
Costruttore dell'Albero Gerarchico Completo WeakAuras — Class Warrior (Protection)
==================================================================================
Assembla i moduli indipendenti sotto il gruppo master 'Class Warrior (Protection)',
applicando le condizioni di caricamento di classe Guerriero su tutti i nodi foglia.
"""
import copy
from builder.core.constants import PROT_WARRIOR_LOAD
from builder.components.utility import SHARED_WARRIOR_CORE_BOOTSTRAP_LUA
from builder.components import (
    build_alerts_auras,
    build_interrupt_auras,
    build_defensive_auras,
    build_rotational_auras,
    build_debuff_auras,
    build_taunt_auras,
    build_bars_auras,
    build_stats_auras,
    build_utility_auras,
)


def build_wa_tree(target_version: str = "5.21.8") -> dict:
    """
    Costruisce e restituisce l'albero gerarchico completo per WeakAuras Protection Warrior.
    Supporta:
    - target_version='5.21.8': WeakAuras 5.21.8+ nativo (internalVersion 90) [PREDETERMINATO]
    - target_version='4.0.0': WeakAuras 4.0.0 legacy (internalVersion 52)
    
    Assembla modularmente i 20 componenti:
    1. 01 - Emergency & Procs warTank (Suggerimento Cooldown Emergenza <35% HP & Sword and Board Proc)
    2. 02 - Kick Advisor warTank (Interruzione intelligente: Shield Bash vs Pummel vs Stun vs Immune)
    3. 03 - Defensive Cooldowns warTank (Enraged Regeneration CD/durata)
    4. 04 - Rotational Bar warTank (Shield Slam con Glow dorato SAB, Revenge reattivo, Devastate)
    5. 05 - Debuffs & Stance warTank (Check Postura Difensiva & debuff boss mancanti Demo/TC)
    6. 06 - Taunt & Threat warTank (Taunt CD & Allerta Taunt Miss/Resist)
    7. 07 - Rage Bar warTank (Rabbia con soglia scarico HS >= 45)
    8. 08 - Health Bar warTank (Salute real-time con soglie cromatiche <35% / 65%)
    9. 09 - Castbar warTank (Castbar nemica con indicatore kickable vs immune)
    10. 10 - Stats Panel warTank (Difesa vs 540, CTC, Armatura DR, SBV, Hit/Exp, EHP)
    11. 11 - Trinket 1 warTank
    12. 12 - Trinket 2 warTank
    13. 13 - Gloves & Boots warTank
    14. 14 - Shield Wall Alert warTank (-60% DR)
    15. 15 - Last Stand Alert warTank (+30% HP)
    16. 16 - Shield Block Tracker warTank (100% Blocco)
    17. 17 - Spell Reflect Advisor warTank
    18. 18 - Sunder Armor Tracker warTank (1-5 cariche sul target)
    19. 19 - Boss Mechanics Alert warTank (Enrage boss & Tank Buster su player)
    20. 20 - Swing & HS Queue warTank (Swing timer & Heroic Strike / Cleave Queued)
    """
    internal_ver = 90 if target_version == "5.21.8" else 52
    w_ver = "5.21.8" if target_version == "5.21.8" else "4.0.0"

    data = {
        "m": "d",
        "v": 2000,
        "w": w_ver,
        "d": {
            "id": "Class Warrior (Protection)",
            "uid": "PWHUD_ROOT",
            "regionType": "group",
            "internalVersion": internal_ver,
            "scale": 1.2,
            "xOffset": 0,
            "yOffset": -190,
            "anchorPoint": "CENTER",
            "selfPoint": "CENTER",
            "groupIcon": "Interface\\Icons\\Ability_Warrior_DefensiveStance",
            "displayIcon": "Interface\\Icons\\Ability_Warrior_DefensiveStance",
            "icon": "Interface\\Icons\\Ability_Warrior_DefensiveStance",
            "controlledChildren": [
                "01 - Emergency & Procs warTank",
                "02 - Kick Advisor warTank",
                "03 - Defensive Cooldowns warTank",
                "04 - Rotational Bar warTank",
                "05 - Debuffs & Stance warTank",
                "06 - Taunt & Threat warTank",
                "07 - Rage Bar warTank",
                "08 - Health Bar warTank",
                "09 - Castbar warTank",
                "10 - Stats Panel warTank",
                "11 - Trinket 1 warTank",
                "12 - Trinket 2 warTank",
                "13 - Gloves & Boots warTank",
                "14 - Shield Wall Alert warTank",
                "15 - Last Stand Alert warTank",
                "16 - Shield Block Tracker warTank",
                "17 - Spell Reflect Advisor warTank",
                "18 - Sunder Armor Tracker warTank",
                "19 - Boss Mechanics Alert warTank",
                "20 - Swing & HS Queue warTank",
            ],
            "load": copy.deepcopy(PROT_WARRIOR_LOAD),
            "actions": {
                "init": {
                    "do_custom": True,
                    "custom": f"_G.PWHUD_InitCore = {SHARED_WARRIOR_CORE_BOOTSTRAP_LUA}\n_G.PWHUD_InitCore()",
                },
                "start": {},
                "finish": {},
            },
        },
        "c": [],
    }

    # Assemblaggio ordinato dei componenti
    data["c"].extend(build_alerts_auras())
    data["c"].extend(build_interrupt_auras())
    data["c"].extend(build_defensive_auras())
    data["c"].extend(build_rotational_auras())
    data["c"].extend(build_debuff_auras())
    data["c"].extend(build_taunt_auras())
    data["c"].extend(build_bars_auras())
    data["c"].extend(build_stats_auras())
    data["c"].extend(build_utility_auras())

    # Applicazione dell'internalVersion a tutti i figli
    for item in data["c"]:
        item["internalVersion"] = internal_ver
        if "load" in item:
            item["load"] = copy.deepcopy(PROT_WARRIOR_LOAD)

    return data
