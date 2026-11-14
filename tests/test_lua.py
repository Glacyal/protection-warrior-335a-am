"""
Validazione Sintassi Codice Lua — Class Warrior (Protection)
============================================================
Analizza e valida tutti i blocchi Lua embedded (trigger, customDuration,
customIcon, customText, actions.init, actions.start, actions.finish).
"""
import os
import re
import sys

def strip_lua(code):
    code = re.sub(r'--\[\[.*?\]\]', '', code, flags=re.DOTALL)
    code = re.sub(r'--.*$', '', code, flags=re.MULTILINE)
    code = re.sub(r'\[\[.*?\]\]', '""', code, flags=re.DOTALL)
    code = re.sub(r'"(\\.|[^"])*"', '""', code)
    code = re.sub(r"'(\\.|[^'])*'", "''", code)
    return code

def verify_lua(code, name):
    stripped = strip_lua(code)
    tokens = re.findall(r'\b(function|if|do|while|repeat|end|until)\b', stripped)
    depth = 0
    for t in tokens:
        if t in ('function', 'if', 'do', 'while', 'repeat'):
            depth += 1
        elif t in ('end', 'until'):
            depth -= 1
        if depth < 0:
            print(f"[-] Errore di sintassi in {name}: terminatore inatteso '{t}'")
            return False
    if depth != 0:
        print(f"[-] Errore di sintassi in {name}: blocchi non bilanciati (depth = {depth})")
        return False
    return True

def run_tests():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    all_passed = True

    sys.path.insert(0, root_dir)
    from builder.tree import build_wa_tree
    tree = build_wa_tree()

    count = 0

    # Check root actions
    root_act = tree.get("d", {}).get("actions", {})
    init_custom = root_act.get("init", {}).get("custom")
    if init_custom and isinstance(init_custom, str):
        count += 1
        ok = verify_lua(init_custom, "Root -> actions.init.custom")
        if not ok: all_passed = False

    all_items = [tree["d"]] + tree["c"]
    for child in all_items:
        cid = child.get("id", "Unknown")
        actions = child.get("actions", {})
        for act_name in ("init", "start", "finish"):
            act_c = actions.get(act_name, {}).get("custom")
            if act_c and isinstance(act_c, str):
                count += 1
                assert not act_c.strip().startswith("function"), (
                    f"{cid} -> actions.{act_name}.custom cannot start with 'function'"
                )
                wrapped_code = f"function()\n{act_c}\nend"
                ok = verify_lua(wrapped_code, f"{cid} -> actions.{act_name}.custom")
                if not ok: all_passed = False

        triggers = child.get("triggers", {})
        for k, v in triggers.items():
            if isinstance(v, dict):
                trig = v.get("trigger", {})
                for field in ("custom", "customDuration", "customIcon", "customText", "customOverlay"):
                    code = trig.get(field)
                    if code and isinstance(code, str):
                        count += 1
                        ok = verify_lua(code, f"{cid} -> trigger.{k}.{field}")
                        if not ok: all_passed = False

                untrig = v.get("untrigger", {})
                ucode = untrig.get("custom")
                if ucode and isinstance(ucode, str):
                    count += 1
                    ok = verify_lua(ucode, f"{cid} -> untrigger.{k}.custom")
                    if not ok: all_passed = False

    assert all_passed, "Rilevati errori di sintassi nei blocchi Lua"
    print(f"[OK] test_lua completato con successo ({count} blocchi Lua verificati senza errori).")
    return True

if __name__ == "__main__":
    run_tests()
