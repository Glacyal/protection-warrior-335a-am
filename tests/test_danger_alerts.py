"""
Test Allarmi Pericolo & Boss Mechanics — Class Warrior (Protection)
===================================================================
Verifica:
1. Emergency Low HP Alert (< 35% HP con suggerimento dinamico CD)
2. Boss Enrage Alert
3. Tank Buster Alert (Soul Reaper, Gastric Bloat, Impale)
"""
import os
import sys

def run_tests():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, root_dir)
    from builder.tree import build_wa_tree

    tree = build_wa_tree()
    children_by_id = {c["id"]: c for c in tree["c"]}

    # Emergency Low HP Alert in 01 - Procs
    em = children_by_id["Emergency Low HP Alert"]
    assert em["width"] == 34
    assert "_G.PWHUD_GetEmergencyCD" in em["triggers"][1]["trigger"]["custom"]

    # Boss Enrage Alert in 01 - Procs
    enrage = children_by_id["Boss Enrage Alert"]
    assert enrage["width"] == 34
    assert "hasEnrage" in enrage["triggers"][1]["trigger"]["custom"]

    # Tank Buster Alert in 01 - Procs
    buster = children_by_id["Tank Buster Alert"]
    assert buster["width"] == 34
    code = buster["triggers"][1]["trigger"]["custom"]
    assert "Soul Reaper" in code or "73797" in code

    # Alert - Emergency CD in 17 - Alerts
    alert_em = children_by_id["Alert - Emergency CD"]
    assert "CRIT HP" in alert_em["customText"]

    print("[OK] test_danger_alerts completato: allarmi emergenza e tank buster conformi.")
    return True

if __name__ == "__main__":
    run_tests()
