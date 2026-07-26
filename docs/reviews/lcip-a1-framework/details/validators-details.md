# Validators Details — LCIP A.1

## Scripts créés

### validate_schema.py

Valide les fichiers JSON d'une conversation contre les schémas correspondants.

- Entrée : chemin d'une conversation ou d'un fichier
- Vérifie : chaque fichier (conversation, expected_state, etc.) contre son schéma
- Sortie : PASS/FAIL par fichier, total global
- Dépendance : librairie `jsonschema`

### validate_conversation.py

Valide l'intégrité structurelle d'une conversation.

- Vérifie : id, messages (rôles, alternance, premier message user), category, level
- Détecte : doublons de rôles, messages vides
- Sortie : PASS/FAIL avec erreurs et avertissements détaillés

### validate_assertions.py

Évalue les assertions automatisées contre un état réel ou attendu.

- Opérateurs : eq, neq, contains, not_contains, exists, not_exists, gt, lt, regex
- Supporte les chemins JSON (ex: `state.intent`, `slots_filled.budget_xaf`)
- Sortie : PASS/FAIL par assertion, compteur global

### validate_business.py

Valide le comportement métier attendu.

- Vérifie : business_action, target_service, handover_required
- Compare avec un état réel optionnel
- Sortie : PASS/FAIL

## Tests exécutés

```bash
python tests/gold_corpus/validators/validate_schema.py tests/gold_corpus/examples/B000001/
python tests/gold_corpus/validators/validate_conversation.py tests/gold_corpus/examples/B000001/
python tests/gold_corpus/validators/validate_assertions.py tests/gold_corpus/examples/B000001/expected_assertions.json
python tests/gold_corpus/validators/validate_business.py tests/gold_corpus/examples/B000001/expected_business.json
```

Résultats : voir details/execution-details.md

## Contrôle

VALID-0001 : PASS
