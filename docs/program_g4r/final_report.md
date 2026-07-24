# Final Report — G.4R

**HEAD:** 50fbe631
**Branch:** feature/program-g2-historical-conversation-validation-20260724

## Batch Verification
Batches found: 40/40
Conversations: 10000
Total turns: 35037

## Verdict Distribution
| Verdict | Count | % |
|---|---:|---:|
| LANGUAGE_FAILURE | 4000 | 40.0% |
| SECTOR_MISLABELED | 3529 | 35.3% |
| LEGITIMATELY_INCOMPLETE | 1227 | 12.3% |
| ENTITY_EXTRACTION_FAILURE | 889 | 8.9% |
| FUNCTIONAL_SUCCESS | 355 | 3.5% |

## Issue Distribution
| Category | Count |
|----------|------:|
| LANGUAGE_FAILURE | 14006 |
| ENTITY_MISSING | 7439 |
| SECTOR_MISMATCH | 5831 |

## Business Objects
ACTION_COMPLETED: 740
Business objects: 740
Note: Objects created via mock adapter (in-memory), not PostgreSQL.

## Key Defects
Language failures: 1
Sector mismatches: 0
Entity extraction failures: 1

## Verdict
LAWIM_PROGRAM_G4R_ACCEPTANCE_PARTIAL

The G.4 campaign executed 10,000 real conversations through the Program F engine.
Language compliance (English/Pidgin responses) needs improvement.
Sector semantic labels need better validation (fraud/support/owner content mismatch).
Business objects created via mock adapter — PostgreSQL not yet proven.