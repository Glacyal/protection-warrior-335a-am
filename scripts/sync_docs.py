"""
Script di Sincronizzazione Stringa di Importazione in docs/index.html
=====================================================================
Legge 'IMPORT_STRING_v5.21.8.txt' e la inietta nel tag <textarea id="hiddenWaString">
all'interno di 'docs/index.html' per il simulatore web GitHub Pages.
"""
import re
import os

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import_path = os.path.join(root_dir, "IMPORT_STRING_v5.21.8.txt")
docs_path = os.path.join(root_dir, "docs", "index.html")

def sync():
    if not os.path.exists(import_path):
        print(f"[-] Errore: File {import_path} non trovato. Eseguire 'python generate.py'.")
        return False

    with open(import_path, "r", encoding="utf-8") as f:
        wa_str = f.read().strip()

    if not os.path.exists(docs_path):
        print(f"[-] Errore: {docs_path} non trovato.")
        return False

    with open(docs_path, "r", encoding="utf-8") as f:
        html = f.read()

    pattern = re.compile(r'(<textarea id="hiddenWaString"[^>]*>).*?(</textarea>)', re.DOTALL)
    new_html, count = pattern.subn(r'\g<1>' + wa_str + r'\g<2>', html)

    if count > 0:
        with open(docs_path, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"[OK] docs/index.html aggiornato con successo! Stringa v5: {len(wa_str)} caratteri.")
        return True
    else:
        print("[-] Attenzione: textarea id='hiddenWaString' non trovata in docs/index.html")
        return False

if __name__ == "__main__":
    sync()
