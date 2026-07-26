# Runtime Execution Details — LCIP B.4R-C

## Pipeline

```
ExpectedSpecLoader
→ ExpectedNormalizer
→ RuntimeExecutor
  → ProgramFEngineAdapter
  → ConversationJourneyOrchestrator
  → ActualNormalizer
→ CanonicalComparator
```

## Status

NON EXÉCUTÉ

L'infrastructure ConversationJourneyOrchestrator et ProgramFEngineAdapter ne sont pas disponibles dans cet environnement de test. Les spécifications sont statiquement validées mais non exécutées contre le runtime.

## Action Recommandée

1. Déployer l'infrastructure runtime
2. Exécuter les 20 conversations via le pipeline ci-dessus
3. Capturer expected brut, actual brut, diff, violations
4. Classer chaque résultat
