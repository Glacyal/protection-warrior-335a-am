"""
Test Target Debuff Trackers — Class Warrior (Protection 3.3.5a)
==============================================================
Verifica:
1. 01 - Procs warTank ha sort="ascending" per ordinare da sinistra a destra (scadenza minore o MISS a sinistra).
2. Presenza dei 3 tracker in controlledChildren:
   - Demoralizing Shout Tracker warTank (soglia <= 10s o MISS, raid-aware con Roar e Curse of Weakness)
   - Thunder Clap Tracker warTank (soglia <= 10s o MISS, raid-aware con Frost Fever, Judgements of the Just, Infected Wounds)
   - Rend Tracker warTank (soglia <= 5s o MISS, solo player, filtro immunità Meccanici)
3. Struttura trigger custom, customDuration, customText e per-frame caching (_G.PWHUD_ScanTargetDebuffs).
"""
import os
import sys

def run_tests():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, root_dir)
    from builder.tree import build_wa_tree

    tree = build_wa_tree()
    children_by_id = {c["id"]: c for c in tree["c"]}

    # 1. 01 - Procs warTank configurazione di gruppo
    procs_group = children_by_id["01 - Procs warTank"]
    assert procs_group["sort"] == "ascending", f"Expected sort 'ascending', got {procs_group.get('sort')}"
    ctrl = procs_group["controlledChildren"]

    assert "Demoralizing Shout Tracker warTank" in ctrl, "Missing Demoralizing Shout Tracker in 01 - Procs"
    assert "Thunder Clap Tracker warTank" in ctrl, "Missing Thunder Clap Tracker in 01 - Procs"
    assert "Rend Tracker warTank" in ctrl, "Missing Rend Tracker in 01 - Procs"

    # 2. Demoralizing Shout Tracker
    demo = children_by_id["Demoralizing Shout Tracker warTank"]
    assert demo["width"] == 34 and demo["height"] == 34
    assert demo["cooldown"] is True
    assert demo["cooldownSwipe"] is True
    assert demo.get("desaturate", False) is False
    trig_demo = demo["triggers"][1]["trigger"]
    assert "_G.PWHUD_CheckTargetDebuff" in trig_demo["custom"]
    assert "cache.demoFound" in trig_demo["custom"]
    assert "<= 10.0" in trig_demo["custom"]
    # Check raid-aware spell IDs in shared logic
    custom_demo = trig_demo["custom"]
    assert "47437" in custom_demo  # Demo Shout Rank 8
    assert "48560" in custom_demo  # Demoralizing Roar Rank 8 (Druid)
    assert "50511" in custom_demo  # Curse of Weakness Rank 9 (Warlock)
    assert demo["customText"] != ""
    assert trig_demo["customDuration"] != ""

    # 3. Thunder Clap Tracker
    clap = children_by_id["Thunder Clap Tracker warTank"]
    assert clap["width"] == 34 and clap["height"] == 34
    assert clap["cooldown"] is True
    assert clap["cooldownSwipe"] is True
    trig_clap = clap["triggers"][1]["trigger"]
    assert "_G.PWHUD_CheckTargetDebuff" in trig_clap["custom"]
    assert "cache.clapFound" in trig_clap["custom"]
    assert "<= 10.0" in trig_clap["custom"]
    # Check raid-aware spell IDs in shared logic
    custom_clap = trig_clap["custom"]
    assert "47502" in custom_clap  # Thunder Clap Rank 9
    assert "55095" in custom_clap  # Frost Fever (DK)
    assert "53696" in custom_clap  # Judgements of the Just (Paladin)
    assert "48485" in custom_clap  # Infected Wounds (Druid)

    # 4. Rend Tracker
    rend = children_by_id["Rend Tracker warTank"]
    assert rend["width"] == 34 and rend["height"] == 34
    assert rend["cooldown"] is True
    assert rend["cooldownSwipe"] is True
    trig_rend = rend["triggers"][1]["trigger"]
    assert "_G.PWHUD_CheckTargetDebuff" in trig_rend["custom"]
    assert "cache.rendFound" in trig_rend["custom"]
    assert "<= 5.0" in trig_rend["custom"]
    # Check mechanical immunity filter
    custom_rend = trig_rend["custom"]
    assert 'cType == "Mechanical"' in custom_rend
    assert 'cType == "Meccanico"' in custom_rend
    # Check player filter
    assert 'unitCaster == "player"' in custom_rend
    assert "47465" in custom_rend  # Rend Rank 10

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
