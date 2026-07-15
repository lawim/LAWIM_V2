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
