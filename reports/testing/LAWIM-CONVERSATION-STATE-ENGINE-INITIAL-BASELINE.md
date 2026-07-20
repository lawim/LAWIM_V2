# LAWIM V2 — Conversation State Engine Initial Baseline

**Date :** 2026-07-20
**HEAD :** `c38e16ce`
**Branche de travail :** `feature/conversation-state-engine-20260720`

## Résultat des 57 tests de baseline

| Résultat | Nombre |
|----------|--------|
| PASS | 44 |
| XFAIL strict | 13 |
| FAIL | 0 |
| XPASS | 0 |

## Défauts à corriger (13 XFAIL)

| Test | Catégorie |
|------|-----------|
| `test_rental_search_context_is_retained_across_four_turns` | Contexte perdu |
| `test_short_response_is_contextualized` | Réponse courte non contextualisée |
| `test_quartier_updates_existing_search` | Quartier oublié |
| `test_criterion_modification_replaces_old_value` | Budget non remplacé |
| `test_no_criteria_are_reasked` | Critères redemandés |
| `test_one_single_next_question` | Questions multiples |
| `test_bonjour_does_not_route_to_support` | Routage défaillant |
| `test_human_handover_triggers` | Handover retourne message générique |
| `test_handover_requires_id_reason_target` | Handover incomplet |
| `test_french_footer_has_ten_words_or_less` | Footer FR >10 mots |
| `test_english_footer_has_ten_words_or_less` | Footer EN >10 mots |
| `test_pcm_footer_has_ten_words_or_less` | Footer PCM >10 mots |
| `test_wizard_marks_completed` | Wizard completed bug |
