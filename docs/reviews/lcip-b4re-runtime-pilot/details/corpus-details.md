# Excluded Files Audit — LCIP B.4R-E

## Inventory

| Path | Type | Size | Git | Origin | Class | Action |
|------|------|------|-----|--------|-------|--------|
| ./how \\ | file | 3069 | No | Accidental | ACCIDENTAL_FILE | Remove |
| ./tests/gold_corpus/conversations/ | dir | 24576 | No | B.4 import | VALID_PROJECT_FILE | Keep |
| ./tests/gold_corpus/import/ | dir | 4096 | No | B.4 import | LEGACY_IMPORT | Keep |
| ./tests/gold_corpus/import/certification_output/ | dir | 24576 | No | B.4 output | GENERATED_TEMPORARY | Clean |

## Summary

| Class | Count |
|-------|------:|
| VALID_PROJECT_FILE | 1 |
| LEGACY_IMPORT | 6 |
| GENERATED_TEMPORARY | 1 |
| ACCIDENTAL_FILE | 1 |
