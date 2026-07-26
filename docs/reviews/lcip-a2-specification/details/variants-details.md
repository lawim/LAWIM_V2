# Variants Details — LCIP A.2

## Fichier créé

`tests/gold_corpus/specification/variants/variants_policy.json`

## Types de variantes

| Type | Description | Condition |
|------|-------------|-----------|
| lexical | Synonymes | equals_state |
| syntactic | Reformulations | equals_state |
| semantic | Sens équivalent | equals_business_decision |
| language_switch | Même intention autre langue | equals_intent |
| partial_input | Entrée partielle | equals_extracted_entities |

## Règle de certification

Une conversation est certifiée si elle satisfait les assertions pour AU MOINS
UNE formulation de chaque tour.

## Contrôle

VARIANTS-0001 : PASS
