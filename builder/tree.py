"""
Costruttore dell'Albero Gerarchico Completo WeakAuras — Class Warrior (Protection)
==================================================================================
Assembla modularmente i componenti sotto il gruppo master 'Class Warrior (Protection)',
conformandosi al layout grafico, visivo e dimensionale (278px) di Fury Warrior e Fire Mage.
"""
import copy
from builder.core.constants import PROT_WARRIOR_LOAD
from builder.components.utility import SHARED_WARRIOR_CORE_BOOTSTRAP_LUA
from builder.components import (
    build_procs_auras,
    build_buffs_auras,
    build_utility_auras,
    build_bars_auras,
    build_rotational_auras,
    build_alerts_auras,
    build_stats_auras,
    build_sunder_auras,
)


def build_wa_tree(target_version: str = "5.21.8") -> dict:
    """
    Costruisce e restituisce l'albero gerarchico completo per WeakAuras Protection Warrior.
    Supporta WeakAuras 5.21.8+ nativo (internalVersion 90, Zero Warning).
    
    Assembla modularmente i 20 nodi controllati principali:
    1. 01 - Procs warTank (Dynamic Group con Sword & Board, Revenge, Shield Block, Emergency CD, Boss Enrage, Tank Buster)
    2. 02 - Battle Shout, 03 - Commanding Shout, 04 - Defensive Stance (x = -222, -190, -158, y = 0)
    3. 05-13 - Utility Row (Monili Slot 13/14, Ring, Cloak, Tier, Enchants, Gloves, Shield Wall, Last Stand, Boots) a y = -45
    4. 14 - Rage Bar (278x14px a y = -20)
    5. 15 - Rotational Bar (Composite Swing Timer 278x7px a y = -7 con retroilluminazione HS/Cleave Queue)
    6. 16 - Castbar warTank (278x20px a y = +8 con Kick Advisor integrato)
    7. 17 - Alerts warTank (Gruppo avvisi testuali e sonori a y = 78)
    8. 18 - Stats Panel warTank (Pannello difensivo 88x60px a x = -190, y = -45)
    9. 19 - Sunder Armor Tracker (32x32px a x = 160, y = -7)
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
                "01 - Procs warTank",
                "02 - Battle Shout",
                "03 - Commanding Shout",
                "04 - Defensive Stance",
                "05 - Trinket 1 warTank",
                "06 - Trinket 2 warTank",
                "06b - Ring warTank",
                "07 - Cloak warTank",
                "08 - Tier Set warTank",
                "09 - Enchants warTank",
                "10 - Gloves warTank",
                "11 - Shield Wall",
                "12 - Last Stand",
                "13 - Boots warTank",
                "14 - Rage Bar",
                "15 - Rotational Bar",
                "16 - Castbar warTank",
                "17 - Alerts warTank",
                "18 - Stats Panel warTank",
                "19 - Sunder Armor Tracker",
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
    data["c"].extend(build_procs_auras())
    data["c"].extend(build_buffs_auras())
    data["c"].extend(build_utility_auras())
    data["c"].extend(build_bars_auras())
    data["c"].extend(build_rotational_auras())
    data["c"].extend(build_alerts_auras())
    data["c"].extend(build_stats_auras())
    data["c"].extend(build_sunder_auras())

    # Applicazione uniforme delle condizioni di caricamento e versione interna
    for item in data["c"]:
        item["load"] = copy.deepcopy(PROT_WARRIOR_LOAD)
        item["internalVersion"] = internal_ver

    return data
