"""
Test Kick & Spell Reflection Advisor — Class Warrior (Protection 3.3.5a)
========================================================================
Verifica:
1. 16 - Castbar warTank (Gruppo contenitore 278x20px a y = 8 con 2 barre speculari).
2. Castbar - Target warTank:
   - aurabar 278x20px, inverse = True (scorrimento da destra verso sinistra).
   - logica intelligente: Shield Bash vs Spell Reflection vs Immune.
   - customText Opzione A: NomeSpell [SHIELD BASH] / [SPELL REFLECTION] / [IMMUNE].
3. Castbar - Player warTank:
   - aurabar 278x20px, inverse = True (scorrimento da destra verso sinistra).
   - priorità assoluta del target: il cast del player viene soppresso se il target casta.
4. Alert - Kick Now in 17 - Alerts warTank.
"""
import os
import sys

def run_tests():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, root_dir)
    from builder.tree import build_wa_tree

    tree = build_wa_tree()
    children_by_id = {c["id"]: c for c in tree["c"]}

    # 1. 16 - Castbar warTank (Gruppo)
    cast_grp = children_by_id["16 - Castbar warTank"]
    assert cast_grp["regionType"] == "group"
    assert cast_grp["yOffset"] == 8
    ctrl = cast_grp["controlledChildren"]
    assert len(ctrl) == 2
    assert "Castbar - Target warTank" in ctrl
    assert "Castbar - Player warTank" in ctrl

    # 2. Castbar - Target warTank
    target_cast = children_by_id["Castbar - Target warTank"]
    assert target_cast["regionType"] == "aurabar"
    assert target_cast["width"] == 278
    assert target_cast["height"] == 20
    assert target_cast["inverse"] is True, "Target castbar must have inverse=True (scorrimento dx -> sx)"
    assert target_cast["icon"] is True
    assert target_cast["icon_side"] == "LEFT"

    custom_text = target_cast["customText"]
    assert "SHIELD BASH" in custom_text
    assert "SPELL REFLECTION" in custom_text
    assert "IMMUNE" in custom_text
    assert "_G.PWHUD_GetTargetCastInfo" in custom_text

    # Verifica colorazione dinamica in customText
    assert "0.78, 0.25, 0.95" in custom_text  # Magenta/Viola per Reflect
    assert "0.0, 0.85, 1.0" in custom_text    # Ciano per Kick

    # 3. Castbar - Player warTank
    player_cast = children_by_id["Castbar - Player warTank"]
    assert player_cast["regionType"] == "aurabar"
    assert player_cast["width"] == 278
    assert player_cast["height"] == 20
    assert player_cast["inverse"] is True, "Player castbar must have inverse=True (scorrimento dx -> sx)"
    assert player_cast["icon"] is True
    assert player_cast["icon_side"] == "LEFT"

    # Verifica soppressione prioritaria
    player_trigger = player_cast["triggers"][1]["trigger"]["custom"]
    assert 'UnitCastingInfo("target")' in player_trigger
    assert 'UnitChannelInfo("target")' in player_trigger
    assert 'if targetSpell then return false end' in player_trigger

    # Verifiche Untrigger immediato su Kick / Interruzione e Trigger Icon
    assert target_cast["iconSource"] == 0
    assert player_cast["iconSource"] == 0
    assert target_cast["auto"] is True, "Target castbar must have auto=True for dynamic trigger icon"
    assert player_cast["auto"] is True, "Player castbar must have auto=True for dynamic trigger icon"
    assert "INV_Misc_QuestionMark" not in target_cast.get("displayIcon", ""), "Target castbar must not fallback to QuestionMark"
    assert "INV_Misc_QuestionMark" not in player_cast.get("displayIcon", ""), "Player castbar must not fallback to QuestionMark"
    assert "ki == nil" in target_cast["triggers"][1]["untrigger"]["custom"]
    assert "spell == nil" in player_cast["triggers"][1]["untrigger"]["custom"]
    assert "GetSpellTexture" in player_cast["customText"]
    assert "SetTexture" in player_cast["customText"]

    # 4. Alert - Kick Now in 17 - Alerts warTank
    alert_kick = children_by_id["Alert - Kick Now"]
    assert alert_kick["regionType"] == "text"
    assert "INTERRUPT" in alert_kick["customText"]
    assert "UnitCanAttack" in alert_kick["customText"]
    assert "ki == nil" in alert_kick["triggers"][1]["untrigger"]["custom"]

    # 5. Verifica unpacking con cRank per UnitChannelInfo in Player Castbar (previene errore aritmetico su stringa durante canalizzazioni/pesca)
    assert "cRank" in player_cast["triggers"][1]["trigger"]["customDuration"], "customDuration deve scompattare cRank per calcolare (ceTime - csTime)"
    assert "cRank" in player_cast["customText"], "customText deve scompattare cRank per assegnare correttamente cTexture"
    assert "cRank" in player_cast["triggers"][1]["trigger"]["customIcon"], "customIcon deve scompattare cRank per assegnare cTexture all'icona"

    print("[OK] test_interrupts completato con successo (Castbar Target e Player entrambe dx->sx con Kick/Reflect, icone dinamiche, canale 3.3.5a e untrigger immediato validati).")
    return True

if __name__ == "__main__":
    run_tests()
