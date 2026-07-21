# LAWIM — État Actuel

**Dernière mise à jour :** 2026-07-21
**HEAD :** (branche `feature/controlled-response-generation-20260721`)

## Transport

Le transport WhatsApp et Telegram fonctionne actuellement.

- Green API : `authorized`
- Telegram Bot `@lawim_bot` : `ok: true`
- Webhooks configurés et endpoints opérationnels
- Footer IA non-bloquant (try/except protège la réponse principale)
- Footer réduit à ≤10 mots (FR/EN/PCM)
- Parse_mode HTML Telegram avec fallback texte brut

## Conversation Runtime

```
Conversation Memory : PERSISTANTE
Case Memory : ACTIVE
Cross-Channel Continuity : VALIDÉE LOCALEMENT
Identity Resolution : CONTRÔLÉE
Memory Context Builder : ACTIF
Handover Continuity : ACTIVE
Retention Policy : DOCUMENTÉE
Déploiement OVH : NON EFFECTUÉ
Recette réelle : EN ATTENTE
```

## Contrôle de Génération

```
ControlledGenerationRequest : OBLIGATOIRE
ProviderMemoryContext : LIMITÉ
Provider Orchestrator : ACTIF
DeepSeek : CONTRAINT
OpenAI : CONTRAINT
Gemini : CONTRAINT
Response Validation : ACTIVE
Internal Fallback : COMPLET
Deux XFAIL d'intégration : FERMÉS
Déploiement OVH : NON EFFECTUÉ
Recette réelle : EN ATTENTE
```

## Composants ajoutés (Chantier 3)

- LawimCase model (11 statuses, 8 types) + repository + service
- ActiveCaseResolver (6-level priority resolution)
- CaseConversationLink (conversation ↔ case binding)
- ConversationState versioning (optimistic locking with StateConflictError)
- SlotValueHistory (via Fact SUPERSEDED mechanism)
- CrossChannelIdentityResolver (5 confidence levels)
- CrossChannelConsent (full lifecycle: PENDING→GRANTED→REVOKED)
- MemoryContextBuilder (Business, Provider, HumanHandover contexts)
- ConversationSummaryService (structured summaries)
- MemoryCompactionService (turn window + important events)
- HandoverContinuityService (initiate → accept → resolve → return_to_lawim)
- MemoryRetentionService + MemoryDeletionService + MemoryAnonymizationService
- 22 observability events + 9 metrics
- 124 new tests, 335 total (0 regression)

## Composants ajoutés (Chantier 4)

- ControlledGenerationRequest/Response contract
- ProviderRegistry, ProviderSelectionPolicy, ProviderOrchestrator
- StructuralValidator, BusinessValidator, ConversationValidator
- RepairHandler (single repair attempt)
- ResponseQualityEvaluator
- Canonical system prompt (SYSTEM_PROMPT_V1)
- JSON response schema (strict, no additional properties)
- Circuit breaker (3 failures → OPEN for 60s)
- Retry (max 1, no new plan)
- 14 observability events + 12 metrics
- Two XFAILs closed: test_residential_use_continues_studio_request, test_i_dont_understand_rephrases_last_question

## Tests

- 385+ tests PASS (exact count depends on new tests)
- 0 XFAIL
- 0 régressions
