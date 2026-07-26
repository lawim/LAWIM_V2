# Runtime Execution Details — B.2

## Commande

```bash
python3 tests/gold_corpus/certification/campaigns/run_b2_campaign.py --max-conversations 200
```

## Résultats d'exécution

| Métrique | Valeur |
|----------|--------|
| Conversations | 200 |
| Runtime appelé | OUI (ProgramFEngineAdapter) |
| Appels runtime | 1 016 |
| Temps total | 18.6s |
| Temps moyen/conv | 88.2ms |
| p50 | 80.0ms |
| p95 | 162.3ms |
| p99 | 257.0ms |

## Classes runtime appelées

- `lawim_v2.conversation.program_f_adapter.ProgramFEngineAdapter`
- `lawim_runtime.conversation.journey.ConversationJourneyOrchestrator`

## Isolation

Chaque conversation a utilisé un tempfile SQLite dédié.

**Contrôle :** RUN-0001 : PASS
