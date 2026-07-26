# Schema Details — LCIP A.1

## Schémas créés

| Fichier | Description | Contrôle |
|---------|-------------|----------|
| conversation.schema.json | Structure complète d'une conversation Gold | id, category, level, channel, language, messages, business_object |
| expected_state.schema.json | État conversationnel attendu | intent, qualification_status, slots_filled, next_action, memory_retained |
| expected_business.schema.json | Comportement métier attendu | business_action, target_service, parameters, handover_required |
| expected_questions.schema.json | Questions attendues dans le dialogue | max 1 question/tour, required_questions, forbidden_questions |
| expected_language.schema.json | Comportement linguistique attendu | primary_language, responses_language, footer_required, identity |
| expected_runtime.schema.json | Comportement runtime attendu | engine, expected_services, expected_repositories, fallback_chain |
| assertions.schema.json | Assertions automatisées | 8 types (state, memory, business, language, channel, runtime, questions, intent) |

## Utilisation

Tous les schémas sont en format JSON Schema draft-07, avec $id unique, title,
description, required, properties et contraintes de validation.

## Validation

Les schémas sont appelés par `validate_schema.py` via la librairie `jsonschema`.

## Contrôle

SCHEMA-0001 : PASS
