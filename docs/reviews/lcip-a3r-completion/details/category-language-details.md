# Category/Language Details — A.3R-C

## Suppression des valeurs par défaut

Le pipeline de certification A.3R ne convertit plus silencieusement :
- catégorie absente → "rental" 
- langue absente → "fr"

Le RuntimeExecutor conserve les valeurs source ou utilise "unknown".

## Tests

| Test | Résultat |
|------|:--------:|
| test_missing_category_stays_unknown | PASS |
| test_missing_language_stays_unknown | PASS |
| test_category_not_defaulted_to_rental | PASS |
| test_language_not_defaulted_to_fr | PASS |

## Résultat

```
CATEGORY_DEFAULTS_REMOVED=YES
LANGUAGE_DEFAULTS_REMOVED=YES
```

**Contrôle :** CL-0001 : PASS
