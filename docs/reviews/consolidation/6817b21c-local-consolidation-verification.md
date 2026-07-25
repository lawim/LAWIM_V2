# Verification de consolidation locale — 6817b21c

## Diff exact

| Metrique | Valeur |
|---|---|
| Fichiers ajoutes | 1 (docs/LAWIM_PROJECT_MASTER_CONTEXT.md) |
| Fichiers modifies | 0 |
| Fichiers supprimes | 0 |
| Lignes ajoutees | 126 |
| Lignes supprimees | 0 |
| Scripts supprimes | 0 |
| Modules supprimes | 0 |
| Compose supprimes | 0 |
| Documents archives | 0 |

**Conclusion :** Consolidation DOCUMENTAIRE uniquement. Aucun code, script, compose ou module obsolete n'a ete supprime.

## Moteurs encore actifs

| Moteur | Statut | Emplacement |
|---|---|---|
| ConversationJourneyOrchestrator | CANONIQUE (via ProgramFEngineAdapter) | lawim_runtime/conversation/journey.py |
| ProgramFEngineAdapter | CANONIQUE (runtime) | code/lawim_v2/conversation/program_f_adapter.py |
| ConversationStateEngine | **FALLBACK ENCORE ACTIF** | code/lawim_v2/communication/service.py ligne 8 |
| AIOrchestrator | ACTIF (AI providers) | code/lawim_v2/services.py ligne 157 |
| DialoguePlan | ACTIF (V2 policy) | code/lawim_v2/conversation/policy/ |
| ResponsePlan (Program F) | CANONIQUE | lawim_runtime/conversation/journey.py |
| InteractionResponsePlan (legacy) | **TOUJOURS PRESENT** | lawim_runtime/interaction/response_plan.py |

Deux classes `ResponsePlan` coexistent. `ConversationStateEngine` peut encore etre selectionne comme fallback.

## Repositories

| Repository | Technologie | Statut |
|---|---|---|
| _SQLiteJourneyRepository | SQLite | CANONIQUE (program_f_adapter.py) |
| _PostgresMarketplaceRepository | PostgreSQL | CANONIQUE (marketplace_adapter.py) |
| V2 ConversationStateRepository | SQLite | Fallback (toujours present) |

## Scripts concurrents

| Fonction | Scripts trouves | Canonique designe |
|---|---|---|
| Deploiement | deployment/scripts/deploy_program_f_acceptance.sh | Oui |
| Acceptance Web | deployment/scripts/acceptance_program_f_web.py | Oui |
| Validation corpus | scripts/g5_validate_corpus.py | Oui |
| Generation G.4 | scripts/g4_generate_corpus.py, scripts/g4_run_batch.py | Historique |
| Evaluation G.4R | scripts/g4r_evaluate.py | Historique |
| Generation G.0 | scripts/program_g_generate.py | Historique |
| Execution G.2 | scripts/g2_run_historical.py | Historique |

6 scripts historiques (G.0, G.2, G.4, G.4R) coexistent sans etre supprimes.

## References obsoletes

```bash
grep -RIn "ConversationStateEngine\|InteractionResponsePlan\|legacy\|deprecated" code lawim_runtime 2>/dev/null | head -10
```

| Reference | Fichier | Statut |
|---|---|---|
| ConversationStateEngine import | code/lawim_v2/communication/service.py:8 | Fallback actif |
| InteractionResponsePlan | lawim_runtime/interaction/response_plan.py | Legacy (non supprime) |

## Tests

| Suite | Resultat |
|---|---|
| python3 -m pytest lawim_runtime/conversation/tests/ | 118 PASS |
| python3 -m pytest --ignore=tests --ignore=code --ignore=docs --ignore=demo --ignore=deployment | 856 PASS |
| python3 scripts/g5_validate_corpus.py | 20 PASS / 10 FAIL |

## Recette locale minimale

Non executee (pas de changement de code necessitant verification).

## Verdict

```text
LAWIM_CONSOLIDATION_DOCUMENTATION_PASS
LAWIM_LOCAL_CONSOLIDATION_EXECUTION_PENDING
LAWIM_OVH_CONSOLIDATION_BLOCKED
LAWIM_CONSOLIDATION_PARTIAL
```

Le commit `6817b21c` est une consolidation **uniquement documentaire**. Aucun chemin obsolete n'a ete supprime, aucun script retire, aucun module archive.

Pour atteindre `LAWIM_LOCAL_CONSOLIDATION_PASS`, il faut au minimum :
1. Supprimer les 6 scripts historiques (G.0, G.2, G.4, G.4R) ou les archiver
2. Supprimer ou desactiver ConversationStateEngine fallback
3. Supprimer InteractionResponsePlan legacy
4. Archiver les rapports programmes F/G obsoletes
5. Reexecuter tous les tests
