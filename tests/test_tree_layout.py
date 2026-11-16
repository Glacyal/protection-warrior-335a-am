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
    rage = children_by_id["14 - Rage Bar"]
    assert rage["width"] == 278 and rage["height"] == 14
    assert rage["yOffset"] == -20

    cast = children_by_id["16 - Castbar warTank"]
    assert cast["width"] == 278 and cast["height"] == 20
    assert cast["yOffset"] == 8

    rot = children_by_id["15 - Rotational Bar"]
    assert rot["yOffset"] == -7

    # Verifiche gruppi e icone
    procs = children_by_id["01 - Procs warTank"]
    assert procs["yOffset"] == 52 and procs["regionType"] == "dynamicgroup"

    bs = children_by_id["02 - Battle Shout"]
    assert bs["xOffset"] == -222 and bs["yOffset"] == 0

    cs = children_by_id["03 - Commanding Shout"]
    assert cs["xOffset"] == -190 and cs["yOffset"] == 0

    ds = children_by_id["04 - Defensive Stance"]
    assert ds["xOffset"] == -158 and ds["yOffset"] == 0

    stats = children_by_id["18 - Stats Panel warTank"]
    assert stats["xOffset"] == -190 and stats["yOffset"] == -45

    sunder = children_by_id["19 - Sunder Armor Tracker warTank"]
    assert sunder["xOffset"] == 160 and sunder["yOffset"] == -7
    assert sunder["width"] == 32 and sunder["height"] == 32

    alerts = children_by_id["17 - Alerts warTank"]
    assert alerts["yOffset"] == 78

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
