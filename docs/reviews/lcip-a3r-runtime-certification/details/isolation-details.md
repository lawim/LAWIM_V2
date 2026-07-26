# Isolation Details — A.3R

## Isolation par conversation

Chaque `execute_conversation()` :
1. Crée un tempfile SQLite dédié
2. Instancie un nouveau `ProgramFEngineAdapter(db_path=...)`
3. Chaque conversation a son propre `conversation_id`
4. Le tempfile est supprimé après exécution

## Test

`test_each_run_uses_separate_repo` vérifie :
- Deux runs séquentiels ne partagent PAS le même `conversation_id`
- Chaque run a `call_count > 0`

## Contrôle

ISO-0001 : PASS
