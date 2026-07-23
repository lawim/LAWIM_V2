# V2/V3 Interaction Migration

**Date:** 2026-07-23
**Status:** COMPLETE
**File:** `lawim_runtime/interaction/routing.py`

## Purpose

Safely migrate from LAWIM V2 conversational runtime to V3 project-centric runtime without disrupting production.

## Modes

| Mode | V2 Behavior | V3 Behavior | Effects |
|------|-------------|-------------|---------|
| V2_ONLY | Processes normally | Not called | V2 only |
| V3_SHADOW | Processes normally | Processes in parallel | No V3 external effects |
| V3_CANARY | Processes normally | Processes for allowed users/channels | No V3 external effects for non-canary |
| V3_PRIMARY_WITH_V2_FALLBACK | Fallback only | Processes primarily | V3 sent, V2 if V3 fails |
| V3_ONLY | Not called | Processes normally | V3 only |

## Router

```python
class InteractionModeRouter:
    mode: InteractionMode
    canary_users: set[str]
    canary_channels: set[str]
    canary_projects: set[str]

    def resolve_mode(envelope, user_id, project_id) -> InteractionMode
    def is_v3_active(envelope, user_id, project_id) -> bool
    def is_shadow(envelope, user_id, project_id) -> bool
```

## Shadow Mode

In `V3_SHADOW` mode:
- V2 processes the interaction and sends the real response
- V3 processes in parallel but sends nothing
- All V3 results are discarded (no external API calls, no side effects)
- Divergences are recorded via `InteractionDivergenceAnalyzer`

## Canary Mode

In `V3_CANARY` mode:
- V3 is active only for explicitly whitelisted users, channels, or projects
- All other traffic continues in V2_ONLY
- Rollback is immediate (remove from canary set)
- Dedicated metrics for canary traffic

## Divergence Analyzer

**File:** `lawim_runtime/interaction/divergence.py`

Compares V2 and V3 results on:
- resolved_identity
- resolved_project
- intent
- next_action
- response_type
- handover

Divergences are recorded with severity and are auditable by correlation_id.

## Default Configuration

```yaml
interaction_gateway_enabled: false
whatsapp_adapter_enabled: false
telegram_adapter_enabled: false
web_interaction_enabled: false
whatsapp_shadow_mode: true
telegram_shadow_mode: true
```

## Rollback

Rollback from V3 to V2_ONLY is always safe:
1. Set mode to V2_ONLY
2. No V3 code runs
3. All traffic returns to V2 pipeline
4. Existing V3 sessions continue in V2

## Validation

- 6 routing tests for all mode transitions
- Shadow mode tested with divergence recording
- Canary mode tested with user/channel/project whitelist
- Rollback test: mode change mid-session
