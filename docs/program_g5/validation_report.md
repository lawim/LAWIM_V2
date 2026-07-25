# G.5-D Validation Report
**HEAD:** 1cc37bf4
**Branch:** feature/program-g5d-regression-recovery-20260724

## Baseline (d2502275)
**Expected:** 16 PASS / 14 FAIL, 17 business objects

## Current Results
**Scenarios:** 30
**PASS:** 20
**FAIL:** 10
**Business expected:** 24
**Business created:** 24
**Business unexpected:** 0
**Language drifts (scenarios):** 10

## Normalized Metrics
| Metric | Value |
|--------|------:|
| Scenarios PASS | 20 |
| Scenarios FAIL | 10 |
| Language drift turns | 26 |
| Entity false positives | 0 |
| Entity missed | 0 |
| Missing confirmations | 0 |
| Business objects created | 24 |
| Business objects expected | 24 |
| Business objects unexpected | 0 |

## Per-Scenario Results
| ID | Lang | Verdict | Issues | Biz | Status |
|---|---|--------|--------|-----|--------|
| FR_RENT_001 | fr | PASS | - | Y | ACTION_COMPLETED |
| FR_RENT_002 | fr | FAIL | LANGUAGE_DRIFT:turn=3,expected=fr,got=en; LANGUAGE_DRIFT:turn=4,expected=fr,got=en | Y | ACTION_COMPLETED |
| FR_RENT_003 | fr | PASS | - | Y | ACTION_COMPLETED |
| FR_BUY_001 | fr | PASS | - | Y | ACTION_COMPLETED |
| FR_CORR_001 | fr | FAIL | LANGUAGE_DRIFT:turn=3,expected=fr,got=en | Y | ACTION_COMPLETED |
| FR_NEG_001 | fr | PASS | - | Y | ACTION_COMPLETED |
| FR_VISIT_001 | fr | PASS | - | N | QUALIFYING |
| FR_SHORT_001 | fr | PASS | - | N | QUALIFYING |
| EN_RENT_001 | en | PASS | - | Y | ACTION_COMPLETED |
| EN_RENT_002 | en | PASS | - | Y | ACTION_COMPLETED |
| EN_RENT_003 | en | PASS | - | Y | ACTION_COMPLETED |
| EN_BUY_001 | en | PASS | - | Y | ACTION_COMPLETED |
| EN_CORR_001 | en | PASS | - | N | QUALIFYING |
| EN_NEG_001 | en | PASS | - | Y | ACTION_COMPLETED |
| EN_SHORT_001 | en | PASS | - | N | QUALIFYING |
| EN_ROOMS_001 | en | PASS | - | Y | ACTION_COMPLETED |
| PCM_RENT_001 | pcm | FAIL | LANGUAGE_DRIFT:turn=2,expected=pcm,got=en; LANGUAGE_DRIFT:turn=3,expected=pcm,got=en; LANGUAGE_DRIFT:turn=4,expected=pcm,got=en | Y | ACTION_COMPLETED |
| PCM_RENT_002 | pcm | FAIL | LANGUAGE_DRIFT:turn=2,expected=pcm,got=en; LANGUAGE_DRIFT:turn=3,expected=pcm,got=en; LANGUAGE_DRIFT:turn=4,expected=pcm,got=en | Y | ACTION_COMPLETED |
| PCM_BUY_001 | pcm | FAIL | LANGUAGE_DRIFT:turn=2,expected=pcm,got=en; LANGUAGE_DRIFT:turn=3,expected=pcm,got=en | Y | ACTION_COMPLETED |
| PCM_NEG_001 | pcm | FAIL | LANGUAGE_DRIFT:turn=2,expected=pcm,got=en; LANGUAGE_DRIFT:turn=3,expected=pcm,got=en; LANGUAGE_DRIFT:turn=4,expected=pcm,got=en | Y | ACTION_COMPLETED |
| PCM_CORR_001 | pcm | FAIL | LANGUAGE_DRIFT:turn=2,expected=pcm,got=en; LANGUAGE_DRIFT:turn=3,expected=pcm,got=en; LANGUAGE_DRIFT:turn=4,expected=pcm,got=en | Y | ACTION_COMPLETED |
| PCM_SHORT_001 | pcm | FAIL | LANGUAGE_DRIFT:turn=2,expected=pcm,got=en; LANGUAGE_DRIFT:turn=3,expected=pcm,got=en; LANGUAGE_DRIFT:turn=4,expected=pcm,got=en | N | QUALIFYING |
| PCM_ROOMS_001 | pcm | FAIL | LANGUAGE_DRIFT:turn=2,expected=pcm,got=en; LANGUAGE_DRIFT:turn=3,expected=pcm,got=en; LANGUAGE_DRIFT:turn=4,expected=pcm,got=en | Y | ACTION_COMPLETED |
| MIX_LANG_001 | fr | PASS | - | Y | ACTION_COMPLETED |
| MIX_LANG_002 | en | PASS | - | Y | ACTION_COMPLETED |
| LANG_SWITCH_001 | en | PASS | - | N | QUALIFYING |
| AMB_ROOMS_001 | en | PASS | - | Y | ACTION_COMPLETED |
| CORR_BUDGET_001 | fr | PASS | - | Y | ACTION_COMPLETED |
| CORR_AREA_001 | fr | FAIL | LANGUAGE_DRIFT:turn=4,expected=fr,got=en; LANGUAGE_DRIFT:turn=5,expected=fr,got=en | Y | ACTION_COMPLETED |
| SHORT_CTX_001 | en | PASS | - | Y | ACTION_COMPLETED |

## Failure Categories
| Category | Count |
|----------|------:|
| LANGUAGE_DRIFT | 26 |