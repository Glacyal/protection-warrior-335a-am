"""
Verifica Allineamento Stringa Compilata — Class Warrior (Protection)
===================================================================
Confronta la stringa generata dal builder con IMPORT_STRING_v5.21.8.txt.
"""
import os
import sys

def run_tests():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, root_dir)
    from builder.core import generate_wa_string
    from builder.tree import build_wa_tree

    v5_path = os.path.join(root_dir, "IMPORT_STRING_v5.21.8.txt")
    v4_path = os.path.join(root_dir, "IMPORT_STRING_v4.0.0.txt")
    assert os.path.isfile(v5_path), f"File {v5_path} non trovato. Eseguire 'python generate.py'."
    assert os.path.isfile(v4_path), f"File {v4_path} non trovato. Eseguire 'python generate.py'."

    with open(v5_path, "r", encoding="utf-8") as f:
        stored_v5 = f.read().strip()
    with open(v4_path, "r", encoding="utf-8") as f:
        stored_v4 = f.read().strip()

    tree_v5 = build_wa_tree("5.21.8")
    gen_v5 = generate_wa_string(tree_v5).strip()
    assert stored_v5 == gen_v5, "IMPORT_STRING_v5.21.8.txt non corrisponde all'output del builder!"

    tree_v4 = build_wa_tree("4.0.0")
    gen_v4 = generate_wa_string(tree_v4).strip()
    assert stored_v4 == gen_v4, "IMPORT_STRING_v4.0.0.txt non corrisponde all'output del builder!"

    print(f"[OK] test_string_sync completato: v5 ({len(stored_v5)} car) e v4 ({len(stored_v4)} car) sincronizzati.")
    return True

if __name__ == "__main__":
    run_tests()
