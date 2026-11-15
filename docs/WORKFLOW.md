# Developer Workflow — Protection Warrior 3.3.5a Suite

## 1. Ciclo di Sviluppo Standard

Il flusso di lavoro per qualsiasi modifica o estensione della suite segue rigorosamente il ciclo Compiler-Driven:

```mermaid
flowchart LR
    A[Modifica builder/components/*.py] --> B[python tests/run_parallel_tests.py]
    B -->|Se PASS| C[python generate.py]
    C --> D[python scripts/sync_docs.py]
    D --> E[Verifica docs/index.html nel Browser]
    E --> F[git commit -am 'feat/fix(...)']
```

---

## 2. Comandi Principali

### 2.1 Esecuzione Test Paralleli
Esegue tutti gli 8 test modulari sfruttando la CPU multi-core:
```powershell
python tests/run_parallel_tests.py
```

### 2.2 Ricompilazione Stringa di Import
Genera il file `IMPORT_STRING_v5.21.8.txt` compresso e codificato:
```powershell
python generate.py
```

### 2.3 Sincronizzazione Documentazione e Web Showcase
Aggiorna il blocco della stringa di importazione e la visualizzazione interattiva all'interno di `docs/index.html`:
```powershell
python scripts/sync_docs.py
```

### 2.4 Controllo di Versione Git
```powershell
git status
git add .
git commit -m "tipo(ambito): descrizione sintetica della modifica"
```

---

## 3. Guida alla Risoluzione Problemi Rapida

- **L'import in gioco non risponde o si blocca**:
  - Eseguire `python tests/run_parallel_tests.py`.
  - Il test `test_components_integrity.py` segnalerà immediatamente se un trigger ha accidentalmente una chiave stringa `"1"` anziché numerica `1`, o se manca `activeTriggerMode: -10`.
- **Il test `test_string_sync.py` fallisce**:
  - Significa che il codice in `builder/` è stato modificato ma non è stato ancora eseguito `python generate.py` per aggiornare `IMPORT_STRING_v5.21.8.txt`.
- **Un'etichetta non è allineata nel simulatore web o in WoW**:
  - Verificare che il subtext utilizzi la funzione ausiliaria `make_subtext` in `builder/core/helpers.py`, che inietta la doppia chiave (`anchor_point` + `anchorPoint` e `text_anchorPoint`).
