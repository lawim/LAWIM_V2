# restart-details — B.2

## Contexte
Non testé spécifiquement dans cette campagne.
Non testé spécifiquement dans cette campagne.
200 échecs documentés dans le détail par conversation (tests/gold_corpus/certification/output/b2-runtime/). Voir evidence/normalized/failures.jsonl.
Cause racine: migration B.1 a généré des expected_* avec un modèle d'état qui ne correspond pas à la sortie du runtime réel.
Les expected_* doivent être mis à jour pour correspondre au modèle du runtime réel.

## Contrôle
N/A
