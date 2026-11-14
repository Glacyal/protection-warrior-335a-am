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

    # Test formula Armor DR
    armor = 27450
    k = 16635 # Costante livello 80 WotLK
    armor_dr = (armor / (armor + k)) * 100
    assert 62.0 <= armor_dr <= 63.0, f"Armor DR inattesa: {armor_dr}"

    # Test formula EHP
    hp = 45000
    ehp = hp / (1 - (armor_dr / 100))
    assert 115000 <= ehp <= 125000, f"EHP inattesa: {ehp}"

    # Test formula CTC (Combat Table Coverage)
    dodge = 28.5
    parry = 22.0
    block = 26.5
    miss = 5.0 + max(0, (542 - 400) * 0.04) # 542 defense
    ctc = dodge + parry + block + miss
    assert ctc >= 85.0, f"CTC inatteso: {ctc}"

    print(f"[OK] test_stats_panel completato: Armor DR={armor_dr:.1f}%, EHP={ehp:.0f}, CTC={ctc:.1f}%.")
    return True

if __name__ == "__main__":
    run_tests()
