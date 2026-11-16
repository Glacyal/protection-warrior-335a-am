"""
Verifica Layout e Geometria dell'Albero — Class Warrior (Protection)
===================================================================
Verifica scale, offset e posizionamento identico al layout di riferimento.
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

    # Verifiche barre centrali (278px sincronizzate)
    rage = children_by_id["14 - Rage Bar warTank"]
    assert rage["width"] == 278 and rage["height"] == 14
    assert rage["yOffset"] == -20

    cast = children_by_id["16 - Castbar warTank"]
    assert cast["yOffset"] == 8
    target_cast = children_by_id["Castbar - Target warTank"]
    assert target_cast["width"] == 278 and target_cast["height"] == 20
    player_cast = children_by_id["Castbar - Player warTank"]
    assert player_cast["width"] == 278 and player_cast["height"] == 20

    rot = children_by_id["15 - Rotational Bar warTank"]
    assert rot["yOffset"] == -7

    # Verifiche gruppi e icone
    procs = children_by_id["01 - Procs warTank"]
    assert procs["yOffset"] == 52 and procs["regionType"] == "dynamicgroup"
    assert "Revenge Ready warTank" in procs["controlledChildren"]
    assert "Revenge Ready warTank" in children_by_id
    assert children_by_id["Revenge Ready warTank"]["uid"] == "PWHUD_PROC_REVENGE"

    bs = children_by_id["02 - Battle Shout warTank"]
    assert bs["xOffset"] == -264 and bs["yOffset"] == 0

    cs = children_by_id["03 - Commanding Shout warTank"]
    assert cs["xOffset"] == -232 and cs["yOffset"] == 0

    vig = children_by_id["04b - Vigilance warTank"]
    assert vig["xOffset"] == -200 and vig["yOffset"] == 0

    ds = children_by_id["04 - Defensive Stance warTank"]
    assert ds["xOffset"] == -168 and ds["yOffset"] == 0

    stats = children_by_id["18 - Stats Panel warTank"]
    assert stats["xOffset"] == -216 and stats["yOffset"] == -49
    stats_bg = children_by_id["Stats Panel - Background warTank"]
    assert stats_bg["width"] == 126 and stats_bg["height"] == 60

    sunder = children_by_id["19 - Sunder Armor Tracker warTank"]
    assert sunder["xOffset"] == 160 and sunder["yOffset"] == -7
    assert sunder["width"] == 32 and sunder["height"] == 32

    alerts = children_by_id["17 - Alerts warTank"]
    assert alerts["yOffset"] == 78
    assert "10b - Shield Block warTank" in children_by_id

    # Verifica Load Conditions: Classe Warrior + Talento Devastate (ID 103)
    assert root["load"]["use_class"] is True
    assert root["load"]["class"]["single"] == "WARRIOR"
    assert root["load"]["use_talent"] is True
    assert root["load"]["talent"]["single"] == 103
    assert root["load"]["talent"]["multi"][103] is True

    for child in tree["c"]:
        assert child["load"]["use_talent"] is True
        assert child["load"]["talent"]["single"] == 103

    print("[OK] test_tree_layout completato: conformità geometrica 1:1 e Load Condition Devastate verificate.")
    return True

if __name__ == "__main__":
    run_tests()
