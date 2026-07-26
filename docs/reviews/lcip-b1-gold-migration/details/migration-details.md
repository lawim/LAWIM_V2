# Migration Details — LCIP B.1

## Script

`tests/gold_corpus/import/migrate_gold_corpus.py`

## Pipeline

1. Lecture des ZIPs
2. Détection des doublons par SHA256
3. Pour chaque conversation : conversion au format Gold Corpus
4. Écriture de 8 fichiers : conversation.json, expected_state.json, expected_business.json, expected_questions.json, expected_language.json, expected_runtime.json, expected_assertions.json, rationale.md

## Résultats

| Métrique | Valeur |
|----------|--------|
| Conversations importées | 990 |
| Erreurs d'import | 0 |
| Durée | 6.18s |

## Format de sortie

Chaque conversation produit un dossier `B######/` avec 8 fichiers.

## Script de certification batch

`tests/gold_corpus/import/batch_certify.py`

## Contrôle

MIG-0001 : PASS
