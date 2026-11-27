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

    # Rimozione Alert - Boss Enraged e Alert - Wrong Stance da 17 - Alerts warTank (Task 29)
    assert "Alert - Boss Enraged" not in children_by_id
    assert "Alert - Boss Enraged" not in children_by_id["17 - Alerts warTank"]["controlledChildren"]
    assert "Alert - Wrong Stance" not in children_by_id
    assert "Alert - Wrong Stance" not in children_by_id["17 - Alerts warTank"]["controlledChildren"]

    # Rimozione Alert - Sword and Board da 17 - Alerts warTank (Task 31 - Regression Fix)
    assert "Alert - Sword and Board" not in children_by_id, "Alert - Sword and Board (banner testuale) non deve essere presente"
    assert "Alert - Sword and Board" not in children_by_id["17 - Alerts warTank"]["controlledChildren"]
    assert children_by_id["17 - Alerts warTank"]["controlledChildren"] == ["Alert - Emergency CD", "Alert - Kick Now"]

    # Tank Buster Alert in 01 - Procs (Task 20 - WotLK 3.3.5a Database)
    buster = children_by_id["Tank Buster Alert"]
    assert buster["width"] == 34
    assert buster["cooldown"] is True
    assert buster["cooldownSwipe"] is True
    assert buster["cooldownEdge"] is False
    trig = buster["triggers"][1]["trigger"]
    assert "_G.PWHUD_CheckTankBusters" in trig["custom"]
    assert "customIcon" in trig and "customDuration" in trig and "customText" in trig
    from builder.components.procs import TANK_BUSTER_DB_LUA
    assert "69409" in TANK_BUSTER_DB_LUA and "73797" in TANK_BUSTER_DB_LUA  # Soul Reaper
    assert "64412" in TANK_BUSTER_DB_LUA  # Phase Punch (Algalon)
    assert "72410" in TANK_BUSTER_DB_LUA  # Rune of Blood (Saurfang)
    assert "62130" in TANK_BUSTER_DB_LUA  # Unbalancing Strike (Thorim)
    assert "74562" in TANK_BUSTER_DB_LUA  # Fiery Combustion (Halion)
    assert "67478" in TANK_BUSTER_DB_LUA  # Impale (Gormok)
    assert "72219" in TANK_BUSTER_DB_LUA  # Gastric Bloat (Festergut)

    # Vigilance Missing Alert (04b - Vigilance warTank — Focus Magic Architecture)
    vig_off = children_by_id["Vigilance - OFF warTank"]
    assert vig_off["desaturate"] is True
    assert "not allyActive" in vig_off["triggers"][1]["trigger"]["custom"]

    # Alert - Emergency CD in 17 - Alerts (Hysteresis a 80% HP e fix table index/upper)
    alert_em = children_by_id["Alert - Emergency CD"]
    assert "CRIT HP" in alert_em["customText"]
    assert "cd.action" in alert_em["customText"], "customText deve estrarre cd.action da tabella senza invocare :upper() direttamente sulla tabella"
    assert "80" in alert_em["triggers"][1]["untrigger"]["custom"], "untrigger deve rimanere attivo fino al ritorno oltre 80% HP"
    assert "UnitAffectingCombat" in alert_em["triggers"][1]["untrigger"]["custom"], "untrigger deve disattivarsi fuori combat"

    # 04 - Defensive Stance - OutOfStance (allineato a Fury Warrior: visibile solo out-of-stance in combat)
    stance_warn = children_by_id["04 - Defensive Stance - OutOfStance warTank"]
    assert "GetShapeshiftForm()" in stance_warn["triggers"][1]["trigger"]["custom"] and "form ~= 2" in stance_warn["triggers"][1]["trigger"]["custom"]
    assert stance_warn["width"] == 24 and stance_warn["height"] == 24
    assert "Defensive Stance - Active" not in children_by_id, "Defensive Stance - Active deve essere rimossa per non mostrare l'icona in postura corretta"

    print("[OK] test_danger_alerts completato: allarmi emergenza, tank buster e rimozione banner testuali conformi.")
    return True

if __name__ == "__main__":
    run_tests()
