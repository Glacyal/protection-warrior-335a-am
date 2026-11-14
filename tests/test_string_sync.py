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
    assert os.path.isfile(v5_path), f"File {v5_path} non trovato. Eseguire 'python generate.py'."

    with open(v5_path, "r", encoding="utf-8") as f:
        stored_string = f.read().strip()

    tree = build_wa_tree("5.21.8")
    generated_string = generate_wa_string(tree).strip()

    assert stored_string == generated_string, (
        "La stringa in IMPORT_STRING_v5.21.8.txt non corrisponde all'output del builder! Eseguire 'python generate.py'."
    )
    print(f"[OK] test_string_sync completato: stringa sincronizzata ({len(stored_string)} caratteri).")
    return True

if __name__ == "__main__":
    run_tests()
