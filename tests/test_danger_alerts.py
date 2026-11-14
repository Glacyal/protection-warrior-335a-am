"""
Test Allarmi Pericolo & Boss Mechanics — Class Warrior (Protection)
===================================================================
Verifica:
1. 01 - Emergency & Procs warTank (Salute < 35% e Sword and Board)
2. 19 - Boss Mechanics Alert warTank (Enrage Boss & Tank Busters)
"""
import os
import sys

def run_tests():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, root_dir)
    from builder.tree import build_wa_tree

    tree = build_wa_tree()
    children_by_id = {c["id"]: c for c in tree["c"]}

    em = children_by_id["01 - Emergency & Procs warTank"]
    assert em["width"] == 54
    assert "_G.PWHUD_GetEmergencyCD" in em["triggers"]["1"]["trigger"]["custom"]
    assert "50227" in em["triggers"]["1"]["trigger"]["custom"]

    boss = children_by_id["19 - Boss Mechanics Alert warTank"]
    assert boss["width"] == 46
    boss_code = boss["triggers"]["1"]["trigger"]["custom"]
    assert "hasEnrage" in boss_code
    assert "Soul Reaper" in boss_code or "73797" in boss_code
    assert "Gastric Bloat" in boss_code

    print("[OK] test_danger_alerts completato: rilevamento emergenza e tank buster validato.")
    return True

if __name__ == "__main__":
    run_tests()
