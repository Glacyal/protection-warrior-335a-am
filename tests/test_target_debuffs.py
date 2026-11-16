"""
Test Target Debuff Trackers — Class Warrior (Protection 3.3.5a)
==============================================================
Verifica:
1. 01 - Procs warTank ha sort="none" per rispettare rigorosamente l'ordine visivo prioritario da sinistra a destra:
   [Emergency Low HP Alert] -> [Tank Buster Alert] -> [Revenge Ready] -> [Sword and Board] -> [Demo] -> [Clap] -> [Rend].
2. Se i debuff sono applicati sul bersaglio con durata abbondante (>10s per Demo/Clap, >5s per Rend), SCOMPAIONO (return false, "HEALTHY").
3. Quando i debuff applicati stanno per scadere (<=10s per Demo/Clap, <=5s per Rend), COMPAIONO CON TIMER e conto alla rovescia (return true, "EXPIRING").
4. Se i debuff MANCANO in combattimento su bersaglio attaccabile valido, compaiono con avviso MISS (return true, "MISS").
5. Rend filtra i bersagli immuni (Meccanici) sia in lingua inglese che italiana (return false, "IMMUNE").
6. Icone con texture dinamiche native C++ risolte tramite select(3, GetSpellInfo(spellId)) per prevenire question mark '?'.
7. Dual key subtext check (%c per timer/MISS in basso e acronimo al centro) con customText nel trigger.
"""
import os
import sys

def run_tests():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, root_dir)
    from builder.tree import build_wa_tree

    tree = build_wa_tree()
    children_by_id = {c["id"]: c for c in tree["c"]}

    # 1. 01 - Procs warTank configurazione di gruppo e priorità visiva
    procs_group = children_by_id["01 - Procs warTank"]
    assert procs_group["sort"] == "none", f"Expected sort 'none', got {procs_group.get('sort')}"
    ctrl = procs_group["controlledChildren"]

    expected_order = [
        "Emergency Low HP Alert",
        "Tank Buster Alert",
        "Revenge Ready warTank",
        "Sword and Board",
        "Demoralizing Shout Tracker warTank",
        "Thunder Clap Tracker warTank",
        "Rend Tracker warTank",
    ]
    assert ctrl == expected_order, f"Expected controlledChildren order {expected_order}, got {ctrl}"

    # 2. Demoralizing Shout Tracker
    demo = children_by_id["Demoralizing Shout Tracker warTank"]
    assert demo["width"] == 34 and demo["height"] == 34
    assert demo["cooldown"] is True
    assert demo["cooldownSwipe"] is True
    assert demo.get("desaturate", False) is False
    trig_demo = demo["triggers"][1]["trigger"]
    assert trig_demo["check"] == "update", f"Expected check 'update', got {trig_demo.get('check')}"
    assert "_G.PWHUD_CheckTargetDebuff" in trig_demo["custom"]
    assert "cache.demoFound" in trig_demo["custom"]
    assert 'rem <= 10.0' in trig_demo["custom"]
    assert 'return false, "HEALTHY"' in trig_demo["custom"]
    assert 'return true, "EXPIRING"' in trig_demo["custom"]
    assert 'return true, "MISS"' in trig_demo["custom"]
    # Check raid-aware spell IDs in shared logic
    custom_demo = trig_demo["custom"]
    assert "47437" in custom_demo  # Demo Shout Rank 8
    assert "48560" in custom_demo  # Demoralizing Roar Rank 8 (Druid)
    assert "50511" in custom_demo  # Curse of Weakness Rank 9 (Warlock)
    assert demo["customText"] != ""
    assert trig_demo["customText"] != ""
    assert trig_demo["customDuration"] != ""
    assert "GetSpellInfo(47437)" in trig_demo["customIcon"]

    # 3. Thunder Clap Tracker
    clap = children_by_id["Thunder Clap Tracker warTank"]
    assert clap["width"] == 34 and clap["height"] == 34
    assert clap["cooldown"] is True
    assert clap["cooldownSwipe"] is True
    trig_clap = clap["triggers"][1]["trigger"]
    assert trig_clap["check"] == "update"
    assert "_G.PWHUD_CheckTargetDebuff" in trig_clap["custom"]
    assert "cache.clapFound" in trig_clap["custom"]
    assert 'rem <= 10.0' in trig_clap["custom"]
    assert 'return false, "HEALTHY"' in trig_clap["custom"]
    assert 'return true, "EXPIRING"' in trig_clap["custom"]
    # Check raid-aware spell IDs in shared logic
    custom_clap = trig_clap["custom"]
    assert "47502" in custom_clap  # Thunder Clap Rank 9
    assert "55095" in custom_clap  # Frost Fever (DK)
    assert "53696" in custom_clap  # Judgements of the Just (Paladin)
    assert "48485" in custom_clap  # Infected Wounds (Druid)
    assert "GetSpellInfo(47502)" in trig_clap["customIcon"]

    # 4. Rend Tracker
    rend = children_by_id["Rend Tracker warTank"]
    assert rend["width"] == 34 and rend["height"] == 34
    assert rend["cooldown"] is True
    assert rend["cooldownSwipe"] is True
    trig_rend = rend["triggers"][1]["trigger"]
    assert trig_rend["check"] == "update"
    assert "_G.PWHUD_CheckTargetDebuff" in trig_rend["custom"]
    assert "cache.rendFound" in trig_rend["custom"]
    assert 'rem <= 5.0' in trig_rend["custom"]
    assert 'return false, "HEALTHY"' in trig_rend["custom"]
    assert 'return true, "EXPIRING"' in trig_rend["custom"]
    # Check mechanical immunity filter
    custom_rend = trig_rend["custom"]
    assert 'cType == "Mechanical"' in custom_rend
    assert 'cType == "Meccanico"' in custom_rend
    # Check player filter
    assert 'unitCaster == "player"' in custom_rend
    assert "47465" in custom_rend  # Rend Rank 10
    assert "GetSpellInfo(47465)" in trig_rend["customIcon"]

    # 5. Dual key subtext check
    for item in [demo, clap, rend]:
        subtexts = [sr for sr in item.get("subRegions", []) if sr.get("type") == "subtext"]
        assert len(subtexts) >= 1
        st = subtexts[0]
        assert st.get("text_text") == "%c"
        assert st.get("anchorPoint") == "INNER_BOTTOM"

    print("[OK] test_target_debuffs completato con successo (tutti i 3 debuff tracker verificati).")
    return True

if __name__ == "__main__":
    run_tests()
