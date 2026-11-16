"""
Test di Integrità dei Componenti — Class Warrior (Protection)
============================================================
Verifica:
1. Root ID, UID, internalVersion.
2. Esatta corrispondenza dei 20 nodi in controlledChildren.
3. Univocità e prefisso PWHUD_ di tutti gli UID.
4. Conformità dual-key per WeakAuras 5.21.8+ in tutti i subtext.
5. Condizioni di caricamento classe Warrior su tutti i nodi.
"""
import os
import sys

def run_tests():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, root_dir)
    from builder.tree import build_wa_tree

    tree = build_wa_tree()
    root = tree["d"]
    assert root["id"] == "Class Warrior (Protection)", f"Invalid root id: {root.get('id')}"
    assert root["uid"] == "PWHUD_ROOT", f"Invalid root uid: {root.get('uid')}"
    assert root["internalVersion"] in (52, 90), f"Invalid internalVersion: {root.get('internalVersion')}"

    expected_children = [
        "01 - Procs warTank",
        "02 - Battle Shout warTank",
        "03 - Commanding Shout warTank",
        "04 - Defensive Stance warTank",
        "05 - Trinket 1 warTank",
        "06 - Trinket 2 warTank",
        "06b - Ring warTank",
        "07 - Cloak warTank",
        "08 - Tier Set warTank",
        "09 - Enchants warTank",
        "10 - Gloves warTank",
        "11 - Shield Wall warTank",
        "12 - Last Stand warTank",
        "13 - Boots warTank",
        "14 - Rage Bar warTank",
        "15 - Rotational Bar warTank",
        "16 - Castbar warTank",
        "17 - Alerts warTank",
        "18 - Stats Panel warTank",
        "19 - Sunder Armor Tracker warTank",
    ]

    ctrl = root["controlledChildren"]
    assert len(ctrl) == 20, f"Expected 20 controlled children, got {len(ctrl)}"
    for exp in expected_children:
        assert exp in ctrl, f"Missing child in root controlledChildren: {exp}"

    # Verify all children in tree['c']
    uids = set()

    for item in tree["c"]:
        cid = item.get("id")
        uid = item.get("uid")
        assert cid, "Item missing 'id'"
        assert uid, f"Item {cid} missing 'uid'"
        assert uid not in uids, f"Duplicate UID detected: {uid}"
        uids.add(uid)
        assert uid.startswith("PWHUD_"), f"UID {uid} does not start with 'PWHUD_'"
        assert item.get("internalVersion") in (52, 90), f"Item {cid} internalVersion not in (52, 90)"

        # Check triggers integrity (integer keys and activeTriggerMode)
        trigs = item.get("triggers", {})
        if trigs:
            assert "activeTriggerMode" in trigs, f"Item {cid} triggers dict missing activeTriggerMode"
            for k in trigs.keys():
                if k != "activeTriggerMode":
                    assert isinstance(k, int), f"Item {cid} has non-integer trigger key: {repr(k)} ({type(k)})"

        # Check subRegions dual-key structure for subtext
        for sr in item.get("subRegions", []):
            if sr.get("type") == "subtext":
                assert "anchor_point" in sr, f"Item {cid} missing anchor_point"
                assert "anchorPoint" in sr, f"Item {cid} missing anchorPoint"
                assert "text_anchorPoint" in sr, f"Item {cid} missing text_anchorPoint"
                assert "anchorXOffset" in sr, f"Item {cid} missing anchorXOffset"
                assert "anchorYOffset" in sr, f"Item {cid} missing anchorYOffset"
                assert "text_anchorXOffset" in sr, f"Item {cid} missing text_anchorXOffset"
                assert "text_anchorYOffset" in sr, f"Item {cid} missing text_anchorYOffset"

        # Check load conditions (Warrior Class)
        load = item.get("load", {})
        assert load.get("use_class") is True, f"Item {cid} load use_class is not True"

    print(f"[OK] test_components_integrity completato con successo ({len(tree['c'])} aure verificate).")
    return True

if __name__ == "__main__":
    run_tests()
