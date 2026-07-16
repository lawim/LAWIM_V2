# LAWIM — QA Data Acceptance Report

**Date:** 2026-07-15  
**Dataset Run ID:** QA-20260715-120000  

---

| Object | Count | Created | Coherent | Isolated | Resettable |
|--------|-------|---------|----------|----------|------------|
| Agencies | 2 | ✅ | ✅ | ✅ agence 1 ≠ agence 2 | ✅ |
| Properties | 10 | ✅ | ✅ | ✅ by agency | ✅ |
| Leads | 4 | ✅ | ✅ | ✅ by agency | ✅ |
| Conversations | 4 | ✅ | ✅ | ✅ multi-channel | ✅ |
| Qualifications | 3 | ✅ | ✅ | ✅ completed/partial/abandoned | ✅ |
| Matchings | 3 | ✅ | ✅ | ✅ exact/partial/none | ✅ |
| Sandbox payments | 3 | ✅ | ✅ | ✅ success/failed/pending | ✅ |
| Tracking campaigns | 2 | ✅ | ✅ | ✅ FB + WA | ✅ |
| Analytics events | ✅ | ✅ | ✅ | ✅ metrics recorded | ✅ |
| Learning events | ✅ | ✅ | ✅ | ✅ outcomes + feedback | ✅ |

## Data Quality

- No real personal data used
- All QA data prefixed (QA-, DEMO-, QA-PAY-)
- Isolated by `dataset_run_id`
- Full reset possible: `python3 scripts/qa/seed_qa_data.py --reset QA-20260715-120000`
- Seeder is idempotent
- Production environment blocked

## Decision

```
ACCEPTED — QA DATA VALIDATED
```
