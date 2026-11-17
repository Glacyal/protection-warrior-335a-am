"""
Test Componente: 15 - Rotational Bar warTank (Static Queue Indicator for HS & Cleave)
=====================================================================================
Verifica:
1. Gruppo contenitore a y = -7 con i 4 figli controllati.
2. Background Frame a 278x7px.
3. Base Bar statica a 274x5px con colorazione copper/bronze Warrior.
4. HS Queued con texture Oro (1.0, 0.84, 0.0), check='update', GetSpellInfo(47450), IsCurrentSpell e Pixel Glow oro.
5. Cleave Queued con texture Verde Smeraldo (0.1, 0.95, 0.2), check='update', GetSpellInfo(47520), IsCurrentSpell e Pixel Glow verde.
6. Pulizia garantita all'untrigger e actions.finish con rimozione glow.
"""
import os
import sys

def run_tests():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, root_dir)
    from builder.tree import build_wa_tree

    tree = build_wa_tree()
    children_by_id = {c["id"]: c for c in tree["c"]}

    # 1. Gruppo Contenitore
    rot_grp = children_by_id["15 - Rotational Bar warTank"]
    assert rot_grp["yOffset"] == -7, f"yOffset inatteso: {rot_grp.get('yOffset')}"
    assert rot_grp["regionType"] == "group"
    ctrl = rot_grp["controlledChildren"]
    assert len(ctrl) == 4, f"Previsti 4 nodi controllati in 15 - Rotational Bar, trovati {len(ctrl)}"
    assert "Rotational Bar - Background warTank" in ctrl
    assert "Rotational Bar - Base Bar warTank" in ctrl
    assert "Rotational Bar - HS Queued warTank" in ctrl
    assert "Rotational Bar - Cleave Queued warTank" in ctrl

    # 2. Background Frame
    bg = children_by_id["Rotational Bar - Background warTank"]
    assert bg["width"] == 278 and bg["height"] == 7
    assert bg["uid"] == "PWHUD_ROTCENTER_BG"

    # 3. Base Bar (Aurabar Swing Timer Mano Primaria)
    base = children_by_id["Rotational Bar - Base Bar warTank"]
    assert base["width"] == 274 and base["height"] == 5
    assert base["uid"] == "PWHUD_ROTCENTER_BASE"
    assert base["regionType"] == "aurabar", "Base Bar deve essere aurabar per mostrare lo scorrimento dello swing timer"
    assert base["color"] == [0.65, 0.35, 0.12, 0.90]
    assert base["barColor"] == [0.65, 0.35, 0.12, 0.90]
    assert "UnitAttackSpeed" in base["triggers"][1]["trigger"]["customDuration"], "customDuration deve tracciare la velocità d'attacco"
    assert "PWHUD_Swing" in base["triggers"][1]["trigger"]["customDuration"], "customDuration deve agganciarsi a PWHUD_Swing"
    base_subtexts = [sr for sr in base.get("subRegions", []) if sr.get("type") == "subtext"]
    assert any(sr.get("text_text") == "%c" and sr.get("anchorPoint") == "CENTER" for sr in base_subtexts), "Base bar deve avere timer %c centrato"

    # 4. HS Queued Indicator
    hsq = children_by_id["Rotational Bar - HS Queued warTank"]
    assert hsq["width"] == 274 and hsq["height"] == 5
    assert hsq["uid"] == "PWHUD_ROTCENTER_HSQ"
    assert hsq["color"] == [1.0, 0.84, 0.0, 1.0]

    # Triggers HS
    trig_hs = hsq["triggers"][1]["trigger"]
    assert trig_hs["check"] == "update", "HS trigger check must be 'update' for frame-accurate responsiveness"
    assert "GetSpellInfo(47450)" in trig_hs["custom"]
    assert "IsCurrentSpell" in trig_hs["custom"]
    untrig_hs = hsq["triggers"][1]["untrigger"]
    assert "GetSpellInfo(47450)" in untrig_hs["custom"]
    assert "IsCurrentSpell" in untrig_hs["custom"]

    # Actions HS (Pixel Glow + Native Glow)
    act_start_hs = hsq["actions"]["start"]
    assert act_start_hs.get("do_glow") is True
    assert act_start_hs.get("glow_color") == [1.0, 0.84, 0.0, 1.0]
    assert "PixelGlow_Start" in act_start_hs.get("custom", "")
    assert "PWHUD_HS_GLOW" in act_start_hs.get("custom", "")
    act_fin_hs = hsq["actions"]["finish"]
    assert act_fin_hs.get("do_glow") is True
    assert act_fin_hs.get("glow_action") == "hide"
    assert "PixelGlow_Stop" in act_fin_hs.get("custom", "")
    assert "PWHUD_HS_GLOW" in act_fin_hs.get("custom", "")

    # 5. Cleave Queued Indicator
    clq = children_by_id["Rotational Bar - Cleave Queued warTank"]
    assert clq["width"] == 274 and clq["height"] == 5
    assert clq["uid"] == "PWHUD_ROTCENTER_CLQ"
    assert clq["color"] == [0.1, 0.95, 0.2, 1.0]

    # Triggers Cleave
    trig_cl = clq["triggers"][1]["trigger"]
    assert trig_cl["check"] == "update", "Cleave trigger check must be 'update' for frame-accurate responsiveness"
    assert "GetSpellInfo(47520)" in trig_cl["custom"]
    assert "IsCurrentSpell" in trig_cl["custom"]
    untrig_cl = clq["triggers"][1]["untrigger"]
    assert "GetSpellInfo(47520)" in untrig_cl["custom"]
    assert "IsCurrentSpell" in untrig_cl["custom"]

    # Actions Cleave (Pixel Glow + Native Glow)
    act_start_cl = clq["actions"]["start"]
    assert act_start_cl.get("do_glow") is True
    assert act_start_cl.get("glow_color") == [0.1, 0.95, 0.2, 1.0]
    assert "PixelGlow_Start" in act_start_cl.get("custom", "")
    assert "PWHUD_CLEAVE_GLOW" in act_start_cl.get("custom", "")
    act_fin_cl = clq["actions"]["finish"]
    assert act_fin_cl.get("do_glow") is True
    assert act_fin_cl.get("glow_action") == "hide"
    assert "PixelGlow_Stop" in act_fin_cl.get("custom", "")
    assert "PWHUD_CLEAVE_GLOW" in act_fin_cl.get("custom", "")

    print("[OK] test_rotational completato con successo (tutti i componenti di 15 - Rotational Bar verificati).")
    return True

if __name__ == "__main__":
    run_tests()
