# Test Plan & Quality Assurance — Protection Warrior 3.3.5a Suite

## 1. Strategia di Collaudo

La qualità e l'affidabilità della suite WeakAuras per il Guerriero Protezione sono garantite da una strategia di test piramidale a tre livelli:

1. **Test Statici e di Struttura (Livello 1)**:
   - Validazione della correttezza dei nodi, univocità degli UID (`PWHUD_*`), consistenza dell'albero gerarchico e appartenenza a `controlledChildren`.
   - Verifica della sintassi dual-key dei `subRegions` e presenza di `subbackground`.
   - Verifica rigorosa che tutte le chiavi dei trigger siano **interi** numerici e che `activeTriggerMode == -10` sia sempre presente.

2. **Test di Sintassi Lua Embedded (Livello 2)**:
   - Parser ad albero per tokenizzare e verificare il bilanciamento di tutti i blocchi Lua custom (`trigger`, `untrigger`, `customDuration`, `customIcon`, `customText`, `actions.init/start/finish`).
   - Verifica che nessun blocco in `actions.*.custom` inizi con la parola chiave `function` (requisito stringente di WeakAuras).

3. **Test Funzionali di Logica di Gioco (Livello 3)**:
   - Simulazione delle condizioni di combattimento: salute bassa (< 35%), debuff letali (Soul Reaper, Impale, Gastric Bloat), spell del boss interrompibili vs protette, e calcolo statistiche difensive.

---

## 2. Dettaglio dei Test Modulari

Tutti gli 8 test vengono eseguiti in parallelo sfruttando i core multipli della CPU tramite il runner `tests/run_parallel_tests.py`:

| Script di Test | Scopo del Test | Asserzioni Chiave Verificate |
| :--- | :--- | :--- |
| **`test_components_integrity.py`** | Integrità strutturale dell'albero | Root ID `Class Warrior (Protection)`, 20 figli in `controlledChildren`, UID univoci `PWHUD_`, chiavi trigger integer `1`, `activeTriggerMode == -10`, conformità dual-key. |
| **`test_tree_layout.py`** | Geometria e simmetria a schermo | Barre a larghezza **278 px**, yOffset sincronizzati (-20px Rage, -7px Swing, +8px Castbar), riga utility a Y = -45px, procs a Y = +52px, alerts a Y = +78px. **Verifica Load Conditions**: classe `WARRIOR`, `use_talent == True`, `talent["single"] == 103` (Devastate) estesa a root e a tutte le 43 aure figlie. |
| **`test_stats_panel.py`** | Logica pannello difensivo | 5 righe formattate in stile Fury Warrior (`|cFFFFFFFFLabel:|r <ValoreColorato>`). Verifica formule Armor DR ($K=16635$), CTC con non-stacking debuff (*Insect Swarm*, *Scorpid Sting*), Shield Block Value (SBV), Draenei *Heroic Presence* (+1% Hit), e Soft Cap 26 / Hard Cap 56 Expertise. |
| **`test_lua.py`** | Validazione sintattica blocchi Lua | Tutti i 90+ blocchi di codice Lua compilano senza terminatori inattesi né parentesi o blocchi non bilanciati (`depth == 0`). |
| **`test_defensives.py`** | Logica advisor difensivo | Priorità gerarchica corretta sotto il 35% HP (Shield Wall > Last Stand > Shield Block > Enraged Regeneration > Healthstone). |
| **`test_interrupts.py`** | Kick Advisor target | Rilevamento `notInterruptible`, colorazione Ciano vs Grigio, suggerimento corretto di Shield Bash, Pummel o Stun. |
| **`test_string_sync.py`** | Allineamento output binario | `IMPORT_STRING_v5.21.8.txt` corrisponde al 100% all'output ricompilato dal builder. |
| **`test_danger_alerts.py`** | Rilevamento Tank Busters & Enrage & Stance | Allarmi attivi su Soul Reaper, Impale >= 2, Gastric Bloat >= 8, Fusion Punch, Enrage del boss e **Wrong Stance** (`Alert - Wrong Stance` + `Defensive Stance - Warning` attivi in combat con Stance ~= 2). |

---

## 3. Istruzioni per l'Esecuzione

Per avviare la suite di collaudo automatizzata in locale:

```powershell
python tests/run_parallel_tests.py
```

Output atteso:
```text
==============================================================================
🚀 AVVIO TEST SUITE PARALLELA MULTI-CORE — CLASS WARRIOR (PROTECTION 3.3.5A)
Directory Progetto : D:\0Progetti\protection-warrior-335a-am
Script Rilevati    : 8
==============================================================================
[✓] test_components_integrity.py     |  0.09s |  PASS 
[✓] test_tree_layout.py              |  0.09s |  PASS 
[✓] test_stats_panel.py              |  0.08s |  PASS 
[✓] test_lua.py                      |  0.11s |  PASS 
[✓] test_defensives.py               |  0.07s |  PASS 
[✓] test_interrupts.py               |  0.08s |  PASS 
[✓] test_string_sync.py              |  0.10s |  PASS 
[✓] test_danger_alerts.py            |  0.07s |  PASS 
------------------------------------------------------------------------------
Riepilogo: 8/8 superati con successo in 0.37s
==============================================================================
🎉 TUTTI I TEST PARALLELI SONO STATI SUPERATI CON SUCCESSO!
```
