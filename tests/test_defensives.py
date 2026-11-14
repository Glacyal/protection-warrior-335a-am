"""
Test Cooldown Difensivi — Class Warrior (Protection)
====================================================
Verifica i nodi dedicati ai cooldown di mitigazione:
Shield Wall, Last Stand, Shield Block, Enraged Regeneration, Spell Reflection.
"""
import os
import sys

def run_tests():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, root_dir)
    from builder.tree import build_wa_tree

    tree = build_wa_tree()
    children_by_id = {c["id"]: c for c in tree["c"]}

    # 14 - Shield Wall
    sw = children_by_id["14 - Shield Wall Alert warTank"]
    assert sw["displayIcon"] == "Interface\\Icons\\Ability_Warrior_ShieldWall"

    # 15 - Last Stand
    ls = children_by_id["15 - Last Stand Alert warTank"]
    assert ls["displayIcon"] == "Interface\\Icons\\Spell_Nature_ShamanRage"

    # 16 - Shield Block
    sb = children_by_id["16 - Shield Block Tracker warTank"]
    assert sb["displayIcon"] == "Interface\\Icons\\Ability_Defensive"

    # 17 - Spell Reflection
    sr = children_by_id["17 - Spell Reflect Advisor warTank"]
    assert sr["displayIcon"] == "Interface\\Icons\\Ability_Warrior_ShieldReflection"

    # 03 - Enraged Regeneration
    er = children_by_id["03 - Defensive Cooldowns warTank"]
    assert er["displayIcon"] == "Interface\\Icons\\Ability_Warrior_EnragedRegeneration"

    print("[OK] test_defensives completato: verificati 5 nodi di mitigazione.")
    return True

if __name__ == "__main__":
    run_tests()
