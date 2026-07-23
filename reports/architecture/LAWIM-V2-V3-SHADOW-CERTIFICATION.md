# LAWIM V2/V3 Shadow Mode Certification

**Date:** 2026-07-23
**Certification:** Program E.5

## InteractionModeRouter

5 routing modes with deterministic resolution:

| Mode | V2 | V3 | Effect |
|------|----|----|--------|
| V2_ONLY | Full processing | No call | V2 only |
| V3_SHADOW | Full processing | Parallel processing | No V3 external effect |
| V3_CANARY | Full processing | For authorized users/channels | Canary only |
| V3_PRIMARY_WITH_V2_FALLBACK | Fallback only | Primary processing | V3 -> V2 if V3 fails |
| V3_ONLY | No call | Full processing | V3 only |

## Shadow Mode Guarantees

- No external API calls in shadow mode
- No profile modifications from shadow path
- No delivery from shadow path
- Divergences recorded for analysis

## Canary Mode

- Activation by user_id, channel, or project_id
- Non-canary traffic stays in V2_ONLY
- Immediate rollback by removing from canary set
- No user outside canary set affected

## Test Results

| Test | Result |
|------|--------|
| V2_ONLY mode | PASS |
| V3_SHADOW mode active | PASS |
| V3_SHADOW is_shadow() | PASS |
| V3_CANARY by user | PASS |
| V3_CANARY by channel | PASS |
| V3_PRIMARY_WITH_V2_FALLBACK | PASS |
| V3_ONLY mode | PASS |
| Divergence recording | PASS |
| Manual divergence record | PASS |
