"""
Test Target Debuff Trackers — Class Warrior (Protection 3.3.5a)
==============================================================
Verifica:
1. 01 - Procs warTank ha sort="none" per rispettare rigorosamente l'ordine visivo prioritario da sinistra a destra:
   [Emergency Low HP Alert] -> [Tank Buster Alert] -> [Revenge Ready] -> [Sword and Board] -> [Demo] -> [Clap] -> [Rend].
2. Se i debuff sono applicati sul bersaglio con durata abbondante (>10s per Demo/Clap, >5s per Rend), SCOMPAIONO (return false, "HEALTHY").
3. Quando i debuff applicati stanno per scadere (<=10s per Demo/Clap, <=5s per Rend), COMPAIONO CON TIMER numerico decimale identico a Slam (return true, "EXPIRING").
4. Se non c'è un bersaglio attivo, se è morto o non attaccabile, o fuori combattimento: SCOMPAIONO ISTANTANEAMENTE (untrigger return not show).
5. Filtro Salute Bersaglio (Task 30): I debuff compaiono SOLO se UnitHealthMax("target") >= 500.000 HP (return false, "LOW_HP" per trash mob < 500k).
6. Rimozione etichette statiche "DEMO", "CLAP", "REND" all'interno delle icone debuff (solo %c attivo).
7. SLAM e REV centrati in alto (anchorPoint="INNER_TOP") con timer in basso (anchorPoint="INNER_BOTTOM").
8. Rend filtra i bersagli immuni (Meccanici) sia in lingua inglese che italiana (return false, "IMMUNE").
9. Icone con texture dinamiche native C++ risolte tramite select(3, GetSpellInfo(spellId)) per prevenire question mark '?'.
10. Architettura snella e ottimizzata: SHARED_TARGET_DEBUFFS_LUA centralizzata in actions.init senza duplicazioni nei trigger.
"""
import os
import sys

def run_tests():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, root_dir)
    from builder.tree import build_wa_tree
    from builder.components.procs import SHARED_TARGET_DEBUFFS_LUA

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

    # Verifica centralizzazione in root actions.init
    root_init = tree["d"]["actions"]["init"]["custom"]
    assert "_G.PWHUD_CheckTargetDebuff" in root_init
    assert "_G.PWHUD_CheckTankBusters" in root_init

    # Verifica logica globale SHARED_TARGET_DEBUFFS_LUA
    assert "cache.demoFound" in SHARED_TARGET_DEBUFFS_LUA
    assert "cache.clapFound" in SHARED_TARGET_DEBUFFS_LUA
    assert "cache.rendFound" in SHARED_TARGET_DEBUFFS_LUA
    assert 'rem <= 10.0' in SHARED_TARGET_DEBUFFS_LUA
    assert 'rem <= 5.0' in SHARED_TARGET_DEBUFFS_LUA
    assert 'return false, "HEALTHY"' in SHARED_TARGET_DEBUFFS_LUA
    assert 'return true, "EXPIRING"' in SHARED_TARGET_DEBUFFS_LUA
    assert 'return true, "MISS"' in SHARED_TARGET_DEBUFFS_LUA
    assert "47437" in SHARED_TARGET_DEBUFFS_LUA  # Demo Shout Rank 8
    assert "48560" in SHARED_TARGET_DEBUFFS_LUA  # Demoralizing Roar Rank 8 (Druid)
    assert "50511" in SHARED_TARGET_DEBUFFS_LUA  # Curse of Weakness Rank 9 (Warlock)
    assert "47502" in SHARED_TARGET_DEBUFFS_LUA  # Thunder Clap Rank 9
    assert "55095" in SHARED_TARGET_DEBUFFS_LUA  # Frost Fever (DK)
    assert "53696" in SHARED_TARGET_DEBUFFS_LUA  # Judgements of the Just (Paladin)
    assert "48485" in SHARED_TARGET_DEBUFFS_LUA  # Infected Wounds (Druid)
    assert "47465" in SHARED_TARGET_DEBUFFS_LUA  # Rend Rank 10
    assert 'cType == "Mechanical"' in SHARED_TARGET_DEBUFFS_LUA
    assert 'cType == "Meccanico"' in SHARED_TARGET_DEBUFFS_LUA
    assert 'unitCaster == "player"' in SHARED_TARGET_DEBUFFS_LUA
    assert 'UnitHealthMax("target")' in SHARED_TARGET_DEBUFFS_LUA
    assert '500000' in SHARED_TARGET_DEBUFFS_LUA
    assert 'return false, "LOW_HP"' in SHARED_TARGET_DEBUFFS_LUA

    # 2. Demoralizing Shout Tracker
    demo = children_by_id["Demoralizing Shout Tracker warTank"]
    assert demo["width"] == 34 and demo["height"] == 34
    assert demo["cooldown"] is True
    assert demo["cooldownSwipe"] is True
    assert demo.get("desaturate", False) is False
    trig_demo = demo["triggers"][1]["trigger"]
    assert trig_demo["check"] == "update", f"Expected check 'update', got {trig_demo.get('check')}"
    assert "_G.PWHUD_CheckTargetDebuff" in trig_demo["custom"]
    assert '"DEMO"' in trig_demo["custom"]
    untrig_demo = demo["triggers"][1]["untrigger"]
    assert "return not show" in untrig_demo["custom"], "Untrigger must return not show to hide when no target"
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
    assert '"CLAP"' in trig_clap["custom"]
    untrig_clap = clap["triggers"][1]["untrigger"]
    assert "return not show" in untrig_clap["custom"], "Untrigger must return not show to hide when no target"
    assert "GetSpellInfo(47502)" in trig_clap["customIcon"]

    # 4. Rend Tracker
    rend = children_by_id["Rend Tracker warTank"]
    assert rend["width"] == 34 and rend["height"] == 34
    assert rend["cooldown"] is True
    assert rend["cooldownSwipe"] is True
    trig_rend = rend["triggers"][1]["trigger"]
    assert trig_rend["check"] == "update"
    assert "_G.PWHUD_CheckTargetDebuff" in trig_rend["custom"]
    assert '"REND"' in trig_rend["custom"]
    untrig_rend = rend["triggers"][1]["untrigger"]
    assert "return not show" in untrig_rend["custom"], "Untrigger must return not show to hide when no target"
    assert "GetSpellInfo(47465)" in trig_rend["customIcon"]

    # 5. Subtext check per Demo, Clap, Rend (etichette rimosse, solo %c timer/MISS)
    for item in [demo, clap, rend]:
        subtexts = [sr for sr in item.get("subRegions", []) if sr.get("type") == "subtext"]
        assert len(subtexts) == 1, f"Expected exactly 1 subtext (%c) in {item['id']}, found {len(subtexts)}"
        st = subtexts[0]
        assert st.get("text_text") == "%c"
        assert st.get("anchorPoint") == "INNER_BOTTOM"

    demo_texts = [sr.get("text_text") for sr in demo.get("subRegions", [])]
    clap_texts = [sr.get("text_text") for sr in clap.get("subRegions", [])]
    rend_texts = [sr.get("text_text") for sr in rend.get("subRegions", [])]
    assert "DEMO" not in demo_texts, "Etichetta DEMO non deve essere presente"
    assert "CLAP" not in clap_texts, "Etichetta CLAP non deve essere presente"
    assert "REND" not in rend_texts, "Etichetta REND non deve essere presente"

    # 6. SLAM e REV centrati in alto (INNER_TOP) con timer in basso (INNER_BOTTOM)
    sab = children_by_id["Sword and Board"]
    sab_st = [sr for sr in sab.get("subRegions", []) if sr.get("type") == "subtext"]
    assert any(sr.get("text_text") == "SLAM" and sr.get("anchorPoint") == "INNER_TOP" for sr in sab_st), "SLAM deve avere anchorPoint INNER_TOP"
    assert any(sr.get("text_text") == "%p" and sr.get("anchorPoint") == "INNER_BOTTOM" for sr in sab_st), "%p su SAB deve avere anchorPoint INNER_BOTTOM"

    rev = children_by_id["Revenge Ready warTank"]
    rev_st = [sr for sr in rev.get("subRegions", []) if sr.get("type") == "subtext"]
    assert any(sr.get("text_text") == "REV" and sr.get("anchorPoint") == "INNER_TOP" for sr in rev_st), "REV deve avere anchorPoint INNER_TOP"
    assert any(sr.get("text_text") == "%p" and sr.get("anchorPoint") == "INNER_BOTTOM" for sr in rev_st), "%p su REV deve avere anchorPoint INNER_BOTTOM"

    print("[OK] test_target_debuffs completato con successo (filtro >=500k HP, etichette rimosse, SLAM/REV centrati in alto).")
    return True

if __name__ == "__main__":
    run_tests()
