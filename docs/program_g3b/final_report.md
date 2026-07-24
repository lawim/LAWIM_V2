# Final Report — Programme G.3B

## Provenance
```
HEAD initial:       15d93cb9 (feature/program-g2-historical-conversation-validation-20260724)
HEAD final:         cb2ec2fc (feature/program-g2-historical-conversation-validation-20260724)
G.3 rapports:       15d93cb9 (baseline preserved in docs/program_g3/)
SHA-256 baselines:  preserved in docs/program_g3/baseline/
Tests:              118 conversation, 856 full suite — 0 failures
```

## Corrections appliquées

| Domaine | Avant | Après | Fichier |
|---------|-------|-------|---------|
| city_is_non_geographic_term | 37 | 0 | entity/__init__.py |
| safety_failure | 12 | 5 | intent (hierarchical priority) |
| intent_mismatch | 23 | 22 | intent engine + qualification |
| CONVERSATIONAL_FAILURE | 11 | 5 | journey.py |
| Intent engine | Flat keyword, greeting discount | Priority-based hierarchy, safety override, 25+ new intents | intent/__init__.py |
| Qualification | 3 intents | 18 intents | qualification/__init__.py |
| NON_BUSINESS_INTENTS | Hardcoded tuple | Configurable constant | journey.py |

## Résultats de la reclassification (486 conversations)

| Métrique | Valeur |
|----------|-------:|
| LEGITIMATELY_INCOMPLETE | 444 |
| INTENT_FAILURE | 21 |
| FUNCTIONAL_SUCCESS | 16 |
| CONVERSATIONAL_FAILURE | 5 |
| language_mismatch | 325 |
| intent_mismatch | 22 |
| unknown_city | 19 |
| safety_failure | 5 |
| studio_with_bedrooms | 2 |

## Défauts résiduels
1. **language_mismatch (325)**: Le moteur répond toujours en français. Une couche de réponse multilingue est nécessaire.
2. **unknown_city (19)**: Certaines villes du corpus ne sont pas dans le dictionnaire CITIES.
3. **safety_failure (5)**: Les réponses de sécurité sont génériques au lieu d'être spécifiques au contexte.
4. **studio_with_bedrooms (2)**: Incohérence entre type de bien et nombre de chambres non détectée.

## Verdict
```
LAWIM_PROGRAM_G3B_ACCEPTANCE_PARTIAL

Les corrections critiques sont appliquées (city_is_non_geographic_term=0,
safety amélioré, hiérarchie d'intentions, tests 118+856 verts).
Les défauts résiduels (langues, villes, réponses sécurité) nécessitent
une couche supplémentaire de traitement du langage et de localisation.
```
