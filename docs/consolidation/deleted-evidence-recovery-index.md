# Deleted Evidence Recovery Index

| Fichier supprimé | Type | Commit de suppression | Rôle | Moyen de récupération |
|---|---|---|---|---|
| `code/lawim_v2/conversation/state/engine.py` (42KB) | CODE_LEGACY | 1056ec68 | V2 ConversationStateEngine (obsolète, désactivé depuis consolidation) | `git show 21c31f62:code/lawim_v2/conversation/state/engine.py` |
| `code/lawim_v2/conversation/state/__init__.py` | CODE_LEGACY | 1056ec68 | V2 init de package | `git show 21c31f62:code/lawim_v2/conversation/state/__init__.py` |
| `scripts/g2_run_historical.py` | SCRIPT_HISTORICAL | 1056ec68 | Exécution corpus G.2 (486 conversations) | `git show 21c31f62:scripts/g2_run_historical.py` |
| `scripts/g3_evaluate.py` | SCRIPT_HISTORICAL | 1056ec68 | Évaluation G.3 | `git show 21c31f62:scripts/g3_evaluate.py` |
| `scripts/g4_generate_corpus.py` | SCRIPT_HISTORICAL | 1056ec68 | Génération 10 000 conversations G.4 | `git show 21c31f62:scripts/g4_generate_corpus.py` |
| `scripts/g4_run_batch.py` | SCRIPT_HISTORICAL | 1056ec68 | Exécution batch G.4 (40×250) | `git show 21c31f62:scripts/g4_run_batch.py` |
| `scripts/g4r_evaluate.py` | SCRIPT_HISTORICAL | 1056ec68 | Ré-évaluation G.4R | `git show 21c31f62:scripts/g4r_evaluate.py` |
| `docs/program_g2/*.md` (5 fichiers) | DOCUMENT_DUPLICATE | 1056ec68 | Rapports G.2 (486 conversations) | Synthèse dans master context + `git show 21c31f62:docs/program_g2/` |
| `docs/program_g3/*.md` (9 fichiers) | RAW_EVIDENCE | 1056ec68 | Baselines G.3, matrices de confusion | `git show 21c31f62:docs/program_g3/` |
| `docs/program_g3b/final_report.md` | DOCUMENT_DUPLICATE | 1056ec68 | Rapport G.3b | `git show 21c31f62:docs/program_g3b/` |
| `docs/program_g4/batch_*.json` (40 fichiers) | GENERATED_ARTIFACT | 1056ec68 | Batch data G.4 (10 000 conversations) | `git show 21c31f62:docs/program_g4/` (régénérable via script) |
| `docs/program_g4/generated_corpus.jsonl` | CORPUS | 1056ec68 | Corpus G.4 complet | `git show 21c31f62:docs/program_g4/generated_corpus.jsonl` |
| `docs/program_g4/run_manifest.json` | GENERATED_ARTIFACT | 1056ec68 | Manifest G.4 | `git show 21c31f62:docs/program_g4/run_manifest.json` |
| `docs/program_g4r/*.jsonl` (10 fichiers) | RAW_EVIDENCE | 1056ec68 | Évaluations G.4R (10 000 conversations, 14k linguistic failures) | `git show 21c31f62:docs/program_g4r/` |
| `docs/program_g4r/*.md` (4 fichiers) | DOCUMENT_DUPLICATE | 1056ec68 | Rapports G.4R | `git show 21c31f62:docs/program_g4r/` |
| `docs/program_g5/*` (3 fichiers) | RAW_EVIDENCE | 1056ec68 | Gold corpus G.5 (30 scenarios, baseline + runs) | `git show 21c31f62:docs/program_g5/` |
| `docker/compose/*.yml` (5 fichiers) | DOCUMENT_DUPLICATE | 1056ec68 | Compose files dupliqués | Archivés dans `docs/archive/compose/` |
| `compose/*.yml` (5 fichiers) | DOCUMENT_DUPLICATE | 1056ec68 | Compose files dupliqués | Archivés dans `docs/archive/compose/` |
| `tests/test_chantier5_*.py` (5 fichiers) | TEST_LEGACY | 1056ec68 | Tests obsolètes ConversationStateEngine | `git show 21c31f62:` prefix `tests/test_chantier5_` |
| `tests/test_conversation_architecture_*.py` (2 fichiers) | TEST_LEGACY | 1056ec68 | Tests obsolètes architecture V2 | `git show 21c31f62:test_conversation_architecture_` |
| `tests/test_conversation_*_baseline.py` (3 fichiers) | TEST_LEGACY | 1056ec68 | Tests obsolètes baselines V2 | `git show 21c31f62:` prefix `tests/test_conversation_` |
| `tests/test_greeting_comprehensive.py` | TEST_LEGACY | 1056ec68 | Test greeting obsolète | `git show 21c31f62:tests/test_greeting_comprehensive.py` |
| `tests/test_real_whatsapp_*` | TEST_LEGACY | 1056ec68 | Test WhatsApp régression obsolète | `git show 21c31f62:tests/test_real_whatsapp_*` |
| `tests/test_channel_runtime_*` | TEST_LEGACY | 1056ec68 | Test fallback canal obsolète | `git show 21c31f62:tests/test_channel_runtime_*` |
| `tests/test_conversation_journey.py` | TEST_LEGACY | 1056ec68 | Test journey obsolète (ConversationStateEngine) | `git show 21c31f62:tests/test_conversation_journey.py` |

## Garanties de récupération

- **A — Synthèse dans master context** : Tous les programmes G.0→G.5 sont documentés dans `docs/LAWIM_PROJECT_MASTER_CONTEXT.md`
- **B — Index précis** : Le commit `21c31f62` (lawim-v1-pre-cleanup-20260725-160240) contient TOUS les fichiers avant suppression
- **C — Archivage physique** : Les compose files sont dans `docs/archive/compose/`
- **D — Manifeste** : Ce fichier sert de manifeste (`docs/consolidation/deleted-evidence-recovery-index.md`)

## Commits de référence

| Tag | HEAD | Rôle |
|---|---|---|
| `lawim-v1-pre-cleanup-20260725-160240` | 21c31f62 | État complet AVANT cleanup (tous fichiers présents) |
| `lawim-v1-runtime-clean` | 1056ec68 | État APRÈS cleanup |
| `lawim-pre-runtime-consolidation-20260725-143856` | 14f8a64b | État AVANT consolidation runtime |
