"""
Test Cooldown Difensivi — Class Warrior (Protection)
====================================================
Verifica i nodi dedicati ai cooldown di mitigazione:
Shield Wall, Last Stand, Shield Block, Enraged Regeneration.
"""
import os
import sys

def run_tests():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, root_dir)
    from builder.tree import build_wa_tree

    tree = build_wa_tree()
    children_by_id = {c["id"]: c for c in tree["c"]}

    # 11 - Shield Wall
    sw = children_by_id["11 - Shield Wall warTank"]
    assert sw["displayIcon"] == "Interface\\Icons\\Ability_Warrior_ShieldWall"

    # 12 - Last Stand
    ls = children_by_id["12 - Last Stand warTank"]
    assert ls["displayIcon"] == "Interface\\Icons\\Spell_Nature_ShamanRage"

    # 10b - Shield Block warTank (in Utility Row / Defensive CDs)
    sb = children_by_id["10b - Shield Block warTank"]
    assert sb["displayIcon"] == "Interface\\Icons\\Ability_Defensive"
    assert sb["cooldown"] is True and sb["cooldownSwipe"] is True
    assert sb["cooldownEdge"] is False
    assert "Shield Block Active" not in children_by_id["01 - Procs warTank"]["controlledChildren"]

    # 13 - Boots warTank (con fallback Enraged Regeneration)
    bot = children_by_id["13 - Boots warTank"]
    assert "Enraged Regeneration" in bot["displayIcon"] or "Ability_Warrior_EnragedRegeneration" in bot["displayIcon"]

    print("[OK] test_defensives completato: verificati cooldown di mitigazione.")
    return True

if __name__ == "__main__":
    run_tests()
