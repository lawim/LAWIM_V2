# Category Details — Audit B.1R

## Source : 82 catégories

La source contient 82 catégories distinctes. Exemples :
- `rental_search` (20)
- `purchase_search` (15)
- `english_native_flow` (15)
- `pidgin_native_flow` (15)
- `restart_recovery` (25)
- `language_switch_fr_en_pcm` (20)
- ... (77 autres)

## Migré : 4 catégories

Le mapping `CATEGORY_MAP` dans le script de migration réduit 82 catégories
à 4 :

| Catégorie B.1 | Catégories source incluses | Nombre |
|---------------|---------------------------|--------|
| rental | rental_search, availability_negotiation, budget_negotiation, city_and_area_switch, ... | 950 |
| purchase | purchase_search, end_to_end_buy_journey, ... | 15 |
| idempotence | idempotence, duplicate_webhooks, ... | 15 |
| visit | visit_request, visit_planning, visit_scheduling, visit_after_search, ... | 10 |

## Problème

78 catégories source (95% de la diversité) sont perdues. Des catégories
comme `multilingual_pcm`, `pidgin_native_flow`, `restart_recovery`,
`correction_flow` sont toutes fondues dans "rental".

**La diversité réelle du corpus est masquée par le mapping.**

## Vérification

```python
# Dans migrate_gold_corpus.py :
CATEGORY_MAP = {
    "rental_search": "rental",
    "purchase_search": "purchase",
    # ... seulement 13 entrées pour 82 catégories
}
category = CATEGORY_MAP.get(category_raw, "rental")  # defaut = "rental"
```

Toute catégorie non listée devient "rental" par défaut.

## Contrôle

CAT-0001 : FAIL (82 catégories → 4, avec défaut "rental")
