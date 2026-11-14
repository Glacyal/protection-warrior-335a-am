"""
Test Kick Advisor — Class Warrior (Protection)
==============================================
Verifica la logica dell'interruzione cast integrata in 16 - Castbar warTank e 17 - Alerts:
Shield Bash vs Pummel vs notInterruptible check.
"""
import os
import sys

def run_tests():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, root_dir)
    from builder.tree import build_wa_tree

    tree = build_wa_tree()
    children_by_id = {c["id"]: c for c in tree["c"]}

    # 16 - Castbar warTank
    castbar = children_by_id["16 - Castbar warTank"]
    assert castbar["regionType"] == "aurabar"
    assert castbar["width"] == 278
    assert castbar["height"] == 20

    # Verifica presenza notInterruptible e kick advisor nel customText
    custom_text = castbar["triggers"][1]["trigger"]["customText"]
    assert "IMMUNE" in custom_text
    assert "KICKABLE" in custom_text
    assert "_G.PWHUD_GetKickInfo" in custom_text

    # Alert - Kick Now in 17 - Alerts warTank
    alert_kick = children_by_id["Alert - Kick Now"]
    assert alert_kick["regionType"] == "text"
    assert "INTERRUPT" in alert_kick["customText"]

    print("[OK] test_interrupts completato: Castbar 278px e Kick Advisor validati.")
    return True

if __name__ == "__main__":
    run_tests()
