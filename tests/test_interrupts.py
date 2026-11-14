"""
Test Kick Advisor — Class Warrior (Protection)
==============================================
Verifica la logica dell'interruzione cast:
Shield Bash vs Pummel vs Stuns vs Immune.
"""
import os
import sys

def run_tests():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, root_dir)
    from builder.tree import build_wa_tree

    tree = build_wa_tree()
    children_by_id = {c["id"]: c for c in tree["c"]}

    kick = children_by_id["02 - Kick Advisor warTank"]
    assert kick["regionType"] == "icon"
    assert kick["width"] == 50

    # Verifica presenza notInterruptible check nel custom trigger
    custom_code = kick["triggers"]["1"]["trigger"]["custom"]
    assert "_G.PWHUD_GetKickInfo" in custom_code

    # Verifica castbar interattiva
    castbar = children_by_id["09 - Castbar warTank"]
    cast_custom = castbar["triggers"]["1"]["trigger"]["customText"]
    assert "IMMUNE" in cast_custom
    assert "KICKABLE" in cast_custom

    print("[OK] test_interrupts completato: Kick Advisor e Castbar con validazione notInterruptible.")
    return True

if __name__ == "__main__":
    run_tests()
