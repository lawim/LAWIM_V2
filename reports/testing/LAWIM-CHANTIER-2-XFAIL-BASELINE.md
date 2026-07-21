# Chantier 2 — XFAIL Baseline

| Test | Raison | Lien Chantier 2 | Fermable ici |
|------|--------|-----------------|--------------|
| test_residential_use_continues_studio_request | Residential use not retained as continuation | Slot merge + contextualisation | Oui |
| test_i_dont_understand_rephrases_last_question | Rephrase not implemented without state engine | Clarification action | Oui |
| test_short_response_is_contextualized | State engine not auto-created — requires explicit wiring | Fixture + slot merge | Oui |
| test_quartier_updates_existing_search | State engine not auto-created — requires explicit wiring | Fixture | Oui |
| test_criterion_modification_replaces_old_value | State engine not auto-created — requires explicit wiring | Fixture + correction | Oui |
| test_no_criteria_are_reasked | State engine not auto-created — requires explicit wiring | Priorité déterministe | Oui |
| test_one_single_next_question | State engine not auto-created — requires explicit wiring | ResponsePlan | Oui |
