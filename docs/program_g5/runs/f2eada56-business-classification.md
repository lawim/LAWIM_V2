# Business Object Classification — f2eada56

## Summary
```
HEAD:            f2eada56
Branch:          feature/program-g5d-regression-recovery-20260724
Expected:        17 scenarios (expected_biz=True)
Created:         24 scenarios (business_object_ids present)
Matched:         13 (correctly create where expected)
Unexpected:      11 (create where not expected)
Missing:          4 (should create but don't)
```

## Formula
```
created_total (24) = matched (13) + unexpected (11) + duplicate (0) + unclassified (0)
expected_total (17) = matched (13) + missing (4)
```

## Per-Scenario Classification

| Scenario | Lang | Expected | Created | Classification | Cause |
|----------|------|---------:|-------:|---------------|-------|
| FR_RENT_001 | fr | Y | Y | MATCHED | |
| FR_RENT_002 | fr | N | Y | UNEXPECTED | awaiting=True, "Oui" matches confirmation during incomplete flow |
| FR_RENT_003 | fr | Y | Y | MATCHED | |
| FR_BUY_001 | fr | Y | Y | MATCHED | |
| FR_CORR_001 | fr | N | Y | UNEXPECTED | awaiting=True after correction, "Oui" triggers creation |
| FR_NEG_001 | fr | Y | Y | MATCHED | |
| FR_VISIT_001 | fr | Y | N | MISSING | awaiting never set, short messages don't trigger confirmation |
| FR_SHORT_001 | fr | Y | N | MISSING | Short message chain, awaiting never reaches True |
| EN_RENT_001 | en | Y | Y | MATCHED | |
| EN_RENT_002 | en | N | Y | UNEXPECTED | "Yes" matches confirmation, awaiting=True |
| EN_RENT_003 | en | Y | Y | MATCHED | |
| EN_BUY_001 | en | Y | Y | MATCHED | |
| EN_CORR_001 | en | N | N | CORRECT | correction, no biz |
| EN_NEG_001 | en | Y | Y | MATCHED | |
| EN_SHORT_001 | en | Y | N | MISSING | Short messages, awaiting not set |
| EN_ROOMS_001 | en | N | Y | UNEXPECTED | "Yes" after room clarification triggers creation |
| PCM_RENT_001 | pcm | Y | Y | MATCHED | |
| PCM_RENT_002 | pcm | N | Y | UNEXPECTED | PCM "Yes" match |
| PCM_BUY_001 | pcm | Y | Y | MATCHED | |
| PCM_NEG_001 | pcm | Y | Y | MATCHED | |
| PCM_CORR_001 | pcm | N | Y | UNEXPECTED | PCM correction + confirmation |
| PCM_SHORT_001 | pcm | Y | N | MISSING | Short PCM chain |
| PCM_ROOMS_001 | pcm | N | Y | UNEXPECTED | Room clarification |
| MIX_LANG_001 | fr | N | Y | UNEXPECTED | Mixed language, awaiting=True |
| MIX_LANG_002 | en | N | Y | UNEXPECTED | Mixed language, awaiting=True |
| LANG_SWITCH_001 | en | N | N | CORRECT | No biz intent |
| AMB_ROOMS_001 | en | N | Y | UNEXPECTED | Room ambiguity, awaiting=True |
| CORR_BUDGET_001 | fr | Y | Y | MATCHED | |
| CORR_AREA_001 | fr | Y | Y | MATCHED | |
| SHORT_CTX_001 | en | N | Y | UNEXPECTED | Short ctx + awaiting=True |

## Root Causes

### Unexpected (awaiting=True triggers premature creation)
- `awaiting_business_confirmation` stays True once set
- Not cleared by intermediate responses
- "Yes"/"Oui" after ANY question with all facts creates biz object
- Short contexts and mixed languages particularly affected

### Missing (awaiting never set or confirmation not recognized)
- Short message chains (FR_SHORT_001, EN_SHORT_001, PCM_SHORT_001)
- Visit flow (FR_VISIT_001 — visit_request intent not fully qualified)
- PCM_SHORT_001: "Yes" without "register" or "make i go"

## Verdict
```
LAWIM_PROGRAM_G5_BUSINESS_VALIDATION_FAIL
business_objects_expected = 17
business_objects_matched = 13
business_objects_missing = 4
business_objects_unexpected = 11
business_objects_duplicated = 0
business_objects_unclassified = 0
```
