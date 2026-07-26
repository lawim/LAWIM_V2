# Discrepancies — LCIP B.5G

5 minor discrepancies found. None affect the validity of the corpus certification.

| # | Severity | Description | Fix |
|--|----------|-------------|-----|
| D1 | LOW | FULLY_CERTIFIED=165 reported (remaining only) vs 185 (corpus) | Clarify scope in report |
| D2 | LOW | Language counts exclude 20 pilot conversations | Add pilot breakdown |
| D3 | MINOR | RUNTIME_VERDICT says PROVEN_RUNTIME_ERRORS_FOUND (contradiction) | Fix verdict |
| D4 | MINOR | Idempotence counts overlap (200 creation + 2 no-action) | Split to 198+2 |
| D5 | MINOR | SHA256SUMS verification from wrong directory | Run from evidence/ |

All 5 are reporting issues only. No functional or certification issues.
