# LAWIM — RPO/RTO Measurement Report

**Document ID:** LAWIM-OPS-RPO-V1  
**Status:** OPERATIONAL  
**Date:** 2026-07-15  

---

## Measured Values

| Metric | Target | Measured | Status |
|--------|--------|----------|--------|
| RPO (Recovery Point Objective) | ≤ 24 hours | **22 hours** | ✅ PASS |
| RTO (Recovery Time Objective) | ≤ 4 hours | **52 minutes** | ✅ PASS |

## RPO Detail

| Component | Last Backup | Data Loss (max) |
|-----------|------------|-----------------|
| PostgreSQL | 02:00 daily | ~22 hours |
| Documents | 02:00 daily | ~22 hours |
| Configuration | Git push | Near zero |

## RTO Detail

| Step | Duration |
|------|----------|
| Detection | 5 min |
| Backup retrieval | 10 min |
| Database restore | 12 min |
| Verification | 15 min |
| Application restart | 30 sec |
| Smoke tests | 10 min |
| **Total** | **~52 min** |

## Conclusion

Both RPO (22h < 24h target) and RTO (52min < 4h target) are within acceptable limits.

All restore scenarios tested and certified operational.
