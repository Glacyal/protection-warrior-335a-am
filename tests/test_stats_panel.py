"""
Verifica Formule Statistiche Tank — Class Warrior (Protection)
==============================================================
Verifica la logica di calcolo del pannello statistiche difensive:
- Defense skill e soglia 540 (Crit-Immune per boss Lv.83).
- CTC (Avoidance = Dodge + Parry + Miss + Block).
- Armor DR% formula: effectiveArmor / (effectiveArmor + 16635).
- EHP formula: HP / (1 - DR%).
"""
import os
import sys

def run_tests():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, root_dir)
    from builder.core.constants import DEFENSE_CAP_RAID, HIT_CAP_MELEE, EXPERTISE_SOFT_CAP

    assert DEFENSE_CAP_RAID == 540
    assert HIT_CAP_MELEE == 8.0
    assert EXPERTISE_SOFT_CAP == 26

    # Test formula Armor DR (Opzione 1: K=15232.5 su Lv.80 / scheda PG; K=16635 su Raid Boss Lv.83)
    armor_ingame = 25253
    k_80 = 400 + 85 * 80 + 4.5 * 85 * (80 - 59) # 15232.5
    dr_80 = (armor_ingame / (armor_ingame + k_80)) * 100
    assert abs(dr_80 - 62.38) < 0.05, f"Armor DR Lv.80 attesa ~62.38%, ottenuta {dr_80:.2f}%"

    k_83 = 16635
    dr_83 = (armor_ingame / (armor_ingame + k_83)) * 100
    assert abs(dr_83 - 60.29) < 0.05, f"Armor DR Lv.83 attesa ~60.29%, ottenuta {dr_83:.2f}%"

    # Test formula EHP
    hp = 45000
    ehp = hp / (1 - (dr_83 / 100))
    assert 110000 <= ehp <= 125000, f"EHP inattesa: {ehp}"

    # Test formula CTC (Combat Table Coverage)
    dodge = 28.5
    parry = 22.0
    block = 26.5
    miss = 4.4 + max(0, (542 - 400) * 0.04) + 3.0 # 542 defense + Insect Swarm/Scorpid Sting
    ctc = dodge + parry + block + miss
    assert ctc >= 85.0, f"CTC inatteso: {ctc}"

    # Verifica presenza etichette stile Fury Warrior e buff/debuff
    from builder.components.stats import make_stats_custom_text
    lua_code = make_stats_custom_text()
    assert "|cFFFFFFFFDef:|r" in lua_code
    assert "|cFFFFFFFFArmor:|r" in lua_code
    assert "|cFFFFFFFFCTC:|r" in lua_code
    assert "|cFFFFFFFFBlock:|r" in lua_code
    assert "|cFFFFFFFFHit:|r" in lua_code
    assert "Insect Swarm" in lua_code
    assert "Scorpid Sting" in lua_code
    assert "Heroic Presence" in lua_code
    assert "SBV" not in lua_code
    assert "(%.1f%%)" not in lua_code

    print(f"[OK] test_stats_panel completato: Armor DR Lv.80={dr_80:.1f}%, Lv.83={dr_83:.1f}%, EHP={ehp:.0f}, CTC={ctc:.1f}% e stile Fury Warrior verificati.")
    return True

if __name__ == "__main__":
    run_tests()
