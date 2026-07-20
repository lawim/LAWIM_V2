# LAWIM V2 — Conversation State Engine Test Results

**Date :** 2026-07-20
**HEAD :** `8779e4a0`

## Baseline tests : 50 PASS, 7 XFAIL

### PASS (50) — Défauts corrigés

| Test | Défaut initial | Correction |
|------|---------------|------------|
| `test_wizard_marks_completed` | Wizard completed flag | `_advance_step` fix |
| `test_bonjour_does_not_route_to_support` | Routage incorrect | State engine routing |
| `test_human_handover_triggers` | Message générique | Handover keyword detection |
| `test_french_footer_has_ten_words_or_less` | 23 mots | Réduit à 10 |
| `test_english_footer_has_ten_words_or_less` | 26 mots | Réduit à 7 |
| `test_pcm_footer_has_ten_words_or_less` | 22 mots | Réduit à 8 |
| 44 autres tests | — | Inchangés |

### XFAIL (7) — Contexte multi-tour

| Test | Cause |
|------|-------|
| `test_rental_search_context_is_retained_across_four_turns` | Intégration LLM complète requise |
| `test_short_response_is_contextualized` | LLM non contraint |
| `test_quartier_updates_existing_search` | Slot extraction LLM |
| `test_criterion_modification_replaces_old_value` | Slot merge LLM |
| `test_no_criteria_are_reasked` | Double question LLM |
| `test_one_single_next_question` | LLM libre |
| `test_handover_requires_id_reason_target` | Objet handover persistant |

## Non-régression

| Suite | Résultat |
|-------|----------|
| Communication delivery | 8/8 PASS |
| Green API webhook | 3/3 PASS |
| Telegram webhook | 3/3 PASS |
