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

    # Rimozione Boss Enrage Alert da 01 - Procs warTank (Task 13)
    assert "Boss Enrage Alert" not in children_by_id
    assert "Boss Enrage Alert" not in children_by_id["01 - Procs warTank"]["controlledChildren"]

    # Tank Buster Alert in 01 - Procs
    buster = children_by_id["Tank Buster Alert"]
    assert buster["width"] == 34
    code = buster["triggers"][1]["trigger"]["custom"]
    assert "Soul Reaper" in code or "73797" in code

    # Alert - Emergency CD in 17 - Alerts
    alert_em = children_by_id["Alert - Emergency CD"]
    assert "CRIT HP" in alert_em["customText"]

    # Alert - Wrong Stance in 17 - Alerts warTank (Task 2)
    alert_stance = children_by_id["Alert - Wrong Stance"]
    assert "DEFENSIVE STANCE REQUIRED" in alert_stance["displayText"]
    assert "GetShapeshiftForm() ~= 2" in alert_stance["triggers"][1]["trigger"]["custom"]
    assert "PLAYER_REGEN_DISABLED" in alert_stance["triggers"][1]["trigger"]["events"]

    # 04 - Defensive Stance - OutOfStance (allineato a Fury Warrior: visibile solo out-of-stance in combat)
    stance_warn = children_by_id["04 - Defensive Stance - OutOfStance warTank"]
    assert "GetShapeshiftForm()" in stance_warn["triggers"][1]["trigger"]["custom"] and "form ~= 2" in stance_warn["triggers"][1]["trigger"]["custom"]
    assert stance_warn["width"] == 30 and stance_warn["height"] == 30
    assert "Defensive Stance - Active" not in children_by_id, "Defensive Stance - Active deve essere rimossa per non mostrare l'icona in postura corretta"

    print("[OK] test_danger_alerts completato: allarmi emergenza, tank buster e wrong stance conformi.")
    return True

if __name__ == "__main__":
    run_tests()
