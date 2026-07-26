# Static Validation Details — LCIP B.4R-C

## Validation Checks Performed

### 1. Schema Validation
- Vérification que chaque fichier expected_*.json a une structure valide
- 20 conversations × 6 fichiers JSON = 120 fichiers validés

### 2. Provenance Validation
- Chaque champ attendu doit avoir une règle EXP source
- Toutes les provenances documentées dans expected_state.json

### 3. Transition Validation
- Les transitions d'intention sont cohérentes
- Pas de saut d'état invalide

### 4. Pending Validation
- Chaque pending est justifié par une question assistant
- Mapping explicite question → pending

### 5. Business Validation
- Action métier justifiée par consentement + faits complets
- Création unique vérifiée

### 6. Linguistic Validation
- Langue cohérente dans chaque conversation
- Pas de mélange de langues non justifié

### 7. Assertion Validation
- Assertions critiques documentées et vérifiables

## Results

| Check | Status |
|-------|--------|
| Schema validation | 20/20 PASS |
| Provenance validation | 20/20 PASS |
| Transition validation | 20/20 PASS |
| Pending validation | 20/20 PASS |
| Business validation | 20/20 PASS |
| Linguistic validation | 20/20 PASS |
| Assertion validation | 20/20 PASS |

## Summary

| Statut | Nombre |
|--------|-------:|
| SPEC_STATIC_APPROVED | 20 |
| SPEC_STATIC_REPAIR_REQUIRED | 0 |
| SPEC_STATIC_INVALID | 0 |
| Tautologie | 0 |
| Erreur normaliseur | 0 |
| Erreur comparateur | 0 |

## Evidence

- Normalized: `evidence/normalized/spec-validation-20.jsonl`
