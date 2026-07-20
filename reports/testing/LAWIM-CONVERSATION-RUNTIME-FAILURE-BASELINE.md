# LAWIM V2 — Conversation Runtime Failure Baseline

**Date :** 2026-07-20
**HEAD :** `b8e0f6d2`
**Documents canoniques lus :** AGENTS.md, LAWIM_CANONICAL_SCOPE.md, LAWIM_CONVERSATION_CONTRACT.md, LAWIM_ENGINEERING_RULES.md, LAWIM_PRODUCTION_EVIDENCE_POLICY.md, LAWIM_SECRET_MANAGEMENT_POLICY.md, LAWIM_CURRENT_STATE.md

## Pipeline réellement actif

```
Webhook → _generate_ai_reply → AIOrchestrator.build_request + AIOrchestrator.generate
  → provider chain (deepseek, openai, gemini, ...)
  → InternalReasoningEngine fallback
```

**Composants NON câblés :** ProgressiveWizard, QualificationEngine, ReadinessEvaluator, NextQuestionResolver, ConversationService (domaine), Planner, GenerativeComposer

## Scénario reproduit

| Tour | Message | Problème |
|------|---------|----------|
| 1 | Bonjour | OK (static greeting) |
| 2 | Je cherche un appartement de deux chambres à Douala | Contexte perdu entre les tours |
| 3 | Mon budget est de 180 000 FCFA par mois | Aucun historique retenu |
| 4 | Je préfère Bonamoussadi | Aucun historique retenu |

## Défauts documentés (13 xfail)

| Test | Défaut | Sévérité |
|------|--------|----------|
| `test_rental_search_context_is_retained_across_four_turns` | Contexte multi-tour perdu | P0 |
| `test_short_response_is_contextualized` | Réponse courte non contextualisée | P0 |
| `test_quartier_updates_existing_search` | Quartier oublié | P0 |
| `test_criterion_modification_replaces_old_value` | Budget non remplacé | P1 |
| `test_no_criteria_are_reasked` | Critères redemandés | P1 |
| `test_one_single_next_question` | Questions multiples | P1 |
| `test_french_footer_has_ten_words_or_less` | Footer FR 23 mots (max 10) | P2 |
| `test_english_footer_has_ten_words_or_less` | Footer EN 26 mots (max 10) | P2 |
| `test_pcm_footer_has_ten_words_or_less` | Footer PCM 22 mots (max 10) | P2 |
| `test_progressive_wizard_exists_and_can_be_instantiated` | Mock setup | P3 |
| `test_human_handover_triggers` | Handover retourne message générique | P1 |
| `test_wizard_marks_completed` | Wizard ne marque pas completed après confirmation | P2 |
| `test_handover_requires_id_reason_target` | Handover incomplet | P2 |

## Causes racines probables

| Catégorie | Cause |
|-----------|-------|
| CONVERSATION_RESOLUTION | `conversation_key` est `str(message_row["id"])` — pas de session persistante |
| WIZARD_BYPASS | ProgressiveWizard jamais instancié dans le pipeline |
| LLM_FREEDOM | Le LLM choisit librement la prochaine question |
| SLOT_MERGE | Aucune fusion des critères entre les tours |
| PROMPT_CONSTRUCTION | Contexte chargé mais non utilisé pour décision métier |
