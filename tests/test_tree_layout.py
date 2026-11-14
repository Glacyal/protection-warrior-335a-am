"""
Verifica Layout e Geometria dell'Albero — Class Warrior (Protection)
===================================================================
Verifica scale, offset e posizionamento delle barre e delle icone.
"""
import os
import sys

def run_tests():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, root_dir)
    from builder.tree import build_wa_tree

    tree = build_wa_tree()
    root = tree["d"]
    assert root["scale"] == 1.2
    assert root["yOffset"] == -190

    children_by_id = {c["id"]: c for c in tree["c"]}

    # Verifiche posizionali barre
    rage = children_by_id["07 - Rage Bar warTank"]
    assert rage["width"] == 210 and rage["height"] == 14
    assert rage["yOffset"] == -14

    hp = children_by_id["08 - Health Bar warTank"]
    assert hp["width"] == 210 and hp["height"] == 14
    assert hp["yOffset"] == -28

    stats = children_by_id["10 - Stats Panel warTank"]
    assert stats["width"] == 210 and stats["height"] == 26
    assert stats["yOffset"] == -120

    cast = children_by_id["09 - Castbar warTank"]
    assert cast["width"] == 210 and cast["height"] == 14
    assert cast["yOffset"] == -95

    # Verifiche icone
    em = children_by_id["01 - Emergency & Procs warTank"]
    assert em["width"] == 54 and em["height"] == 54
    assert em["yOffset"] == 65

    kick = children_by_id["02 - Kick Advisor warTank"]
    assert kick["width"] == 50 and kick["height"] == 50

    print("[OK] test_tree_layout completato: proporzioni e geometrie validate.")
    return True

if __name__ == "__main__":
    run_tests()
