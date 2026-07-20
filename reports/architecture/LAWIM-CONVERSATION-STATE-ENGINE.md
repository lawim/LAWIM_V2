# LAWIM V2 — Conversation State Engine

**Date :** 2026-07-20

## Architecture

```
message entrant
→ ConversationResolver (résolution session par canal)
→ ConversationStateRepository.load() (chargement état persistant)
→ ConversationStateEngine.process_turn()
    → Détection greeting/handover
    → ConversationStateEngine._merge_update() (fusion slots)
    → ProgressiveWizard.submit_answer() (qualification)
    → AIOrchestrator.generate() (formulation réponse)
    → ConversationResponseValidator (validation)
→ ConversationStateRepository.save() (persistance)
→ Channel formatting + delivery
```

## Composants

| Composant | Fichier | Rôle |
|-----------|---------|------|
| `ConversationState` | `conversation/state/state.py` | Modèle d'état |
| `ConversationStateRepository` | `conversation/state/repository.py` | Persistance SQLite |
| `ConversationResolver` | `conversation/state/resolver.py` | Résolution session |
| `ConversationStateEngine` | `conversation/state/engine.py` | Ordonnanceur |
| `ResponsePlan` | `conversation/state/state.py` | Plan de réponse |
| `ProgressiveWizard` | `knowledge_runtime/engine/wizard.py` | Qualification |
| `ReadinessEvaluator` | `knowledge_runtime/engine/readiness.py` | Évaluation |
| `NextQuestionResolver` | `knowledge_runtime/engine/resolver.py` | Prochaine question |

## Intégration runtime

- `CommunicationService._generate_ai_reply()` → `ConversationStateEngine.process_turn()`
- Fallback: AIOrchestrator → _greeting_response()
- Handover détecté avant tout traitement
- Footer ≤10 mots, non bloquant
