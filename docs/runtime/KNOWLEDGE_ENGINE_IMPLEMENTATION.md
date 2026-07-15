# Knowledge Runtime Engine — Qualification Runtime

## Overview

The Knowledge Runtime Engine (`code/lawim_v2/knowledge_runtime/engine/`) provides runtime
components that consume the H2.1 Knowledge Registries to drive the qualification process.

## Components

### ReadinessEvaluator

Evaluates the user's progress through the 7-level readiness scale (H0.5):

1. INTENT_IDENTIFIED → 2. MINIMUM_INTAKE_READY → 3. MINIMUM_SEARCH_READY →
4. MINIMUM_MATCHING_READY → 5. INTRODUCTION_READY → 6. VISIT_READY → 7. TRANSACTION_READY

```python
evaluator = ReadinessEvaluator(readiness_registry)
result = evaluator.evaluate(known_fields)
# -> {"current_level": "INTENT_IDENTIFIED", "current_score": 28.6, "next_level": "...", ...}
```

### NextQuestionResolver

Determines which field to ask next based on:
- always_ask rules (intent, transaction_type, city)
- Matrix field groups (intake → search → matching → ...)
- conditional_ask rules with priority ordering
- never_ask / deduce_from_context / defer_ask exclusions

```python
resolver = NextQuestionResolver(question_registry, matrix_registry)
result = resolver.resolve_next(known_fields, property_type="apartment")
# -> {"field": "neighborhood", "reason": "always_ask", ...}
```

### QualificationEngine

Orchestrates both evaluators:

```python
engine = QualificationEngine(knowledge_service)
result = engine.evaluate(known_fields, property_type="apartment")
# -> {"readiness": {...}, "next_question": {...}, "known_field_count": N}
```

### ProgressiveWizard

Implements the 10-step progressive qualification order (H2-W2-010):

| Step | Name | Mandatory Fields |
|------|------|-----------------|
| 1 | Intention | intent, transaction_type |
| 2 | Type | property_type |
| 3 | Ville | city |
| 4 | Quartier | neighborhood |
| 5 | Budget | budget_max |
| 6 | Delai | (none) |
| 7 | Criteres | surface, chambres |
| 8 | Preferences | (none) |
| 9 | Confirmation | confirmation |
| 10 | Escalade | (none) |

Manages sessions, step transitions, retry limits (max 3 per field), and escalation.

```python
wizard = ProgressiveWizard(readiness_evaluator, question_resolver)
session = wizard.create_session("sess-1", channel="whatsapp")
result = wizard.submit_answer("sess-1", "intent", "buy")
info = wizard.get_current_step_info("sess-1")
# -> {"step": 2, "name": "Type", "readiness": {...}, ...}
```
