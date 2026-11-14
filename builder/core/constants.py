"""
Costanti Globali & Configurazioni di Base per WeakAuras Suite — Warrior Protection 3.3.5a
========================================================================================
Contiene le condizioni di caricamento per Guerriero Protezione 3.3.5a (WotLK 12340)
e le impostazioni grafiche condivise (font, texture, palette colori, cap difensivi).
"""

# Condizioni di Caricamento (Load Conditions):
# Classe Guerriero (Class: WARRIOR) con opzione per talento Shield Slam / Shockwave
PROT_WARRIOR_LOAD = {
    "use_class": True,
    "class": {"single": "WARRIOR", "multi": {"WARRIOR": True}},
    "use_vehicle": False,
}

# Tipografia e Texture Standard
FONT_EXPRESSWAY = "Expressway"
TEXTURE_STATUSBAR = "Interface\\TargetingFrame\\UI-StatusBar"
TEXTURE_WHITE8X8 = "Interface\\Buttons\\WHITE8X8"

# Palette Colori RGBA
COLOR_RAGE = [0.78, 0.12, 0.12, 1.0]          # Crimson intenso base
COLOR_RAGE_DUMP = [1.0, 0.65, 0.10, 1.0]     # Oro/Ambra per soglia scarico sicuro (>= 45)
COLOR_RAGE_STARVED = [0.45, 0.05, 0.05, 1.0]  # Rosso scuro (< 15)
COLOR_RAGE_BG = [0.10, 0.04, 0.04, 0.85]     # Sfondo scuro barra rabbia

COLOR_HEALTH_HIGH = [0.15, 0.75, 0.15, 1.0]  # Verde salute ottimale (> 65%)
COLOR_HEALTH_MED = [0.95, 0.70, 0.10, 1.0]   # Ambra attenzione (35% - 65%)
COLOR_HEALTH_CRIT = [0.95, 0.10, 0.10, 1.0]  # Rosso allarme critico (< 35%)
COLOR_HEALTH_BG = [0.08, 0.08, 0.08, 0.90]   # Sfondo scuro barra salute

COLOR_GOLD_SAB = [1.0, 0.84, 0.0, 1.0]       # Oro per proc Sword and Board
COLOR_REVENGE = [0.95, 0.45, 0.10, 1.0]      # Arancione vivo per Revenge disponibile
COLOR_SHIELD_BLOCK = [0.20, 0.55, 1.00, 1.0] # Blu acciaio Shield Block
COLOR_KICK_READY = [0.0, 0.85, 1.0, 1.0]     # Ciano interrupt pronto
COLOR_KICK_IMMUNE = [0.55, 0.55, 0.55, 0.9]  # Grigio cast non interrompibile
COLOR_DANGER_ALERT = [1.0, 0.15, 0.15, 1.0]  # Rosso intenso pericolo / boss enrage

# Cap e Soglie Tank WotLK 3.3.5a (Raid Boss Livello 83)
DEFENSE_CAP_RAID = 540         # Immunità dai colpi critici dei boss livello 83 (5.6% crit reduction)
DEFENSE_CAP_DUNGEON = 535      # Immunità dai colpi critici nei dungeon eroici livello 82
HIT_CAP_MELEE = 8.0            # 8.0% (263 Hit Rating) per speciali fisici capped (Taunt, Shield Slam)
EXPERTISE_SOFT_CAP = 26        # 26 Expertise (214 Rating) elimina le Schivate dei boss (Dodge Cap)
EXPERTISE_HARD_CAP = 56        # 56 Expertise elimina anche le Parate dei boss (Parry Cap)
CRITICAL_HEALTH_PCT = 35       # Soglia salute critica per suggerimento cooldown difensivi d'emergenza
