"""
WeakAuras String Generator — Class Warrior (Protection)
=======================================================
Genera le stringhe di importazione WeakAuras per:
1. 'IMPORT_STRING_v5.21.8.txt': WeakAuras 5.21.8+ nativo (internalVersion 90)
2. 'IMPORT_STRING_v4.0.0.txt': WeakAuras 4.0.0 legacy 3.3.5a (internalVersion 52)
3. 'IMPORT_STRING_TEST_ON_MAGE.txt': Versione di test abilitata anche per Mago/qualsiasi classe
"""
import os
from builder.core import generate_wa_string
from builder.tree import build_wa_tree

TARGET_V5_FILE = "IMPORT_STRING_v5.21.8.txt"
TARGET_V4_FILE = "IMPORT_STRING_v4.0.0.txt"
TARGET_TEST_MAGE_FILE = "IMPORT_STRING_TEST_ON_MAGE.txt"

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    v5_path = os.path.join(base_dir, TARGET_V5_FILE)
    v4_path = os.path.join(base_dir, TARGET_V4_FILE)
    test_mage_path = os.path.join(base_dir, TARGET_TEST_MAGE_FILE)

    # 1. Target v5.21.8 (internalVersion 90)
    print(f"[BUILD] Generazione di '{TARGET_V5_FILE}' (internalVersion 90)...")
    tree_v5 = build_wa_tree(target_version="5.21.8")
    str_v5 = generate_wa_string(tree_v5)
    with open(v5_path, "w", encoding="utf-8") as f:
        f.write(str_v5)
    print(f"[SUCCESS] '{TARGET_V5_FILE}': {len(str_v5)} caratteri.")

    # 2. Target v4.0.0 (internalVersion 52)
    print(f"[BUILD] Generazione di '{TARGET_V4_FILE}' (internalVersion 52)...")
    tree_v4 = build_wa_tree(target_version="4.0.0")
    str_v4 = generate_wa_string(tree_v4)
    with open(v4_path, "w", encoding="utf-8") as f:
        f.write(str_v4)
    print(f"[SUCCESS] '{TARGET_V4_FILE}': {len(str_v4)} caratteri.")

    # 3. Target Test on Mage (senza restrizione di classe, per test immediato sul Mago)
    print(f"[BUILD] Generazione di '{TARGET_TEST_MAGE_FILE}'...")
    load_test_mage = {
        "use_class": True,
        "class": {"single": "WARRIOR", "multi": {"WARRIOR": True, "MAGE": True}},
        "use_vehicle": False,
    }
    tree_test_mage = build_wa_tree(target_version="5.21.8", load_override=load_test_mage)
    str_test_mage = generate_wa_string(tree_test_mage)
    with open(test_mage_path, "w", encoding="utf-8") as f:
        f.write(str_test_mage)
    print(f"[SUCCESS] '{TARGET_TEST_MAGE_FILE}': {len(str_test_mage)} caratteri.")
