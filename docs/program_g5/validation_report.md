# G.5-B Validation Report
**HEAD:** 1956e312
**Branch:** feature/program-g5-multilingual-semantic-postgres-20260724
**Scenarios:** 30
**PASS:** 16
**FAIL:** 14

## Results by Language
| fr | 11 | 6 | 54.5% |
| en | 12 | 10 | 83.3% |
| pcm | 7 | 0 | 0.0% |
| mixed | 0 | 0 | N/A |

## Failure Categories
| Category | Count |
|----------|------:|
| LANGUAGE_DRIFT | 28 |
| MISSING_CONFIRMATION | 4 |
| ENTITY_FALSE_POSITIVE | 1 |

## Business Actions
Business objects created: 24/17
Language drifts: 10/30

## Per-Scenario Results
| ID | Lang | Verdict | Issues | Biz | Status |
|---|---|--------|--------|-----|--------|
| FR_RENT_001 | fr | FAIL | LANGUAGE_DRIFT:turn=3,expected=fr,got=en; LANGUAGE_DRIFT:turn=4,expected=fr,got=en | Y | ACTION_COMPLETED |
| FR_RENT_002 | fr | FAIL | LANGUAGE_DRIFT:turn=3,expected=fr,got=en; LANGUAGE_DRIFT:turn=4,expected=fr,got=en | Y | ACTION_COMPLETED |
| FR_RENT_003 | fr | PASS | - | Y | ACTION_COMPLETED |
| FR_BUY_001 | fr | PASS | - | Y | ACTION_COMPLETED |
| FR_CORR_001 | fr | PASS | - | Y | ACTION_COMPLETED |
| FR_NEG_001 | fr | FAIL | LANGUAGE_DRIFT:turn=2,expected=fr,got=en; LANGUAGE_DRIFT:turn=3,expected=fr,got=en; LANGUAGE_DRIFT:turn=4,expected=fr,got=en | Y | ACTION_COMPLETED |
| FR_VISIT_001 | fr | FAIL | MISSING_CONFIRMATION:business_action_expected_but_not_executed | N | QUALIFYING |
| FR_SHORT_001 | fr | FAIL | MISSING_CONFIRMATION:business_action_expected_but_not_executed | N | QUALIFYING |
| EN_RENT_001 | en | PASS | - | Y | ACTION_COMPLETED |
| EN_RENT_002 | en | PASS | - | Y | ACTION_COMPLETED |
| EN_RENT_003 | en | PASS | - | Y | ACTION_COMPLETED |
| EN_BUY_001 | en | PASS | - | Y | ACTION_COMPLETED |
| EN_CORR_001 | en | PASS | - | N | QUALIFYING |
| EN_NEG_001 | en | FAIL | ENTITY_FALSE_POSITIVE:transaction_type=expected=buy,got=rent | Y | ACTION_COMPLETED |
| EN_SHORT_001 | en | FAIL | MISSING_CONFIRMATION:business_action_expected_but_not_executed | N | QUALIFYING |
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
| CORR_AREA_001 | fr | PASS | - | Y | ACTION_COMPLETED |
| SHORT_CTX_001 | en | PASS | - | Y | ACTION_COMPLETED |