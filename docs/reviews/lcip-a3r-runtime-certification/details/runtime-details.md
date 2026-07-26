# Runtime Execution Details — A.3R

## Classes appelées

- `lawim_v2.conversation.program_f_adapter.ProgramFEngineAdapter` — réel, importé
- `ConversationJourneyOrchestrator` — réel, instancié en interne par l'adaptateur

## Preuve d'appel

Les tests positifs vérifient :
```python
self.assertTrue(result.get("runtime_called", False))
self.assertGreater(result.get("call_count", 0), 0)
```

Test `test_each_run_uses_separate_repo` vérifie :
- Deux conversations séquentielles utilisent des DB SQLite isolées (tempfiles)
- Chaque conversation a son propre `conversation_id`

## Isolation

Chaque `execute_conversation()` crée un fichier SQLite temporaire :
```python
db_fd, db_path = tempfile.mkstemp(suffix="_lawim_test.sqlite3")
```

## Runtime trace

Pour chaque exécution, `runtime-trace.json` contient :
- turn_index, user_input, assistant_output
- intent_detected, facts_after, pending_after, business_actions
- duration_ms, error

## Contrôle

RT-0001 : PASS
