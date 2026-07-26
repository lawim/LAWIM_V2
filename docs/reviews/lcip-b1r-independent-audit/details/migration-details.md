# Migration Details — Audit B.1R

## IDs migrés

- 990 IDs de B000001 à B000990
- Aucun ID dupliqué
- Aucun ID manquant dans la séquence
- **990 conversations** sur 990 sources (100%)

## Script de migration

Fichier : `tests/gold_corpus/import/migrate_gold_corpus.py`

### Problèmes identifiés

1. **Catégories écrasées** : 82 catégories source → 4 catégories via CATEGORY_MAP
2. **Langue par défaut** : `language: "UNSET"` dans 790 sources → `fr` par défaut
3. **expected_state généré** : entièrement déduit du dernier tour, pas du runtime
4. **expected_business** : `target_service` toujours `PropertySearchService`
5. **expected_assertions** : générées automatiquement, pas spécifiques
6. **rationale.md** : texte générique, pas d'analyse humaine
7. **expected_runtime** : `engine` toujours `ConversationJourneyOrchestrator` sans vérification

Aucune error d'import (990/990). Le script est fonctionnel mais génère des
fichiers expected_* par défaut, pas par certification réelle.

## Contrôle

MIG-0001 : STATIC_SCHEMA_VALID
