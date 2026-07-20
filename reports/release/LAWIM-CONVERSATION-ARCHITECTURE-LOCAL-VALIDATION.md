# LAWIM V2 — Conversation Architecture Local Validation

**Chantier :** 1 — Canonical Conversation Runtime
**HEAD :** `b2fe5e34`
**Date :** 2026-07-20

## Validation Results

### ConversationState

**Status: EXISTING AND CONSOLIDATED**

`ConversationState` dataclass at `conversation/state/state.py:21` is fully operational with 25 fields including `conversation_id`, `actor_id`, `channel`, `channel_session_id`, `language`, `current_intent`, `intent_confidence`, `known_slots`, `missing_slots`, `changed_slots`, `last_user_message`, `last_lawim_message`, `last_question_key`, `last_question_slot`, `qualification_status`, `qualification_step`, `selected_agent`, `handover_status`, `wizard_session_id`, `created_at`, `updated_at`, `version`.

Persistence via `ConversationStateRepository` (SQLite). Resolution via `ConversationResolver` by channel + session ID.

### ConversationTurnDecision

**Status: EXISTING**

`ConversationTurnDecision` dataclass at `conversation/state/state.py:108` with fields: `intent`, `known_slots`, `missing_slots`, `qualification_ready`, `next_action`, `next_question_key`, `next_question_text`, `selected_agent`, `handover_required`, `allowed_response_content`, `forbidden_response_content`.

Used within the state engine decision logic to produce the `ResponsePlan`.

### ResponsePlan

**Status: OBLIGATORY**

`ResponsePlan` dataclass at `conversation/state/state.py:85` is mandatory for every response. It controls:
- `speaker`, `language`, `response_type`
- `next_action`, `next_question_key`, `next_question_text`
- `maximum_questions` (default 1)
- `maximum_length` (default 500)
- `forbidden_content`, `allowed_content`
- `handover_required`, `handover_reason`, `handover_target_team`, `handover_id`

Every code path (primary via engine, fallback via AIOrchestrator) creates a ResponsePlan before generating or validating output.

Test: `test_response_plan_exists_before_provider_call` — PASS

### AIOrchestrator

**Status: CONSTRAINED**

`AIOrchestrator` at `ai/orchestrator.py:68` is still available as the LLM provider but is now constrained:
- Primary path: used by `ConversationStateEngine._generate_response()` under the direction of `ResponsePlan`
- Fallback path: used only when `ConversationStateEngine` is None or fails; creates a synthetic `ResponsePlan(maximum_questions=1)` and validates output

Pre-existing fallback protection (provider chain, circuit breakers, InternalReasoningEngine) remains intact.

### ResponseValidator

**Status: ACTIVE**

`ConversationResponseValidator` at `conversation/state/validator.py:41` is active on every response:
- Forbidden content detection (neutral assistant, referrals, translation, grammar)
- Question count enforcement
- Returns `PASS`, `REPAIR`, `FALLBACK_INTERNAL`, or `BLOCK`

All 5 validator tests in architecture contract suite pass.

### Internal Engine (ConversationStateEngine)

**Status: READY**

`ConversationStateEngine.process_turn()` at `conversation/state/engine.py:71` handles:
- Session resolution and state loading
- Greeting / handover / rephrase detection
- Short-answer contextualization
- Slot extraction and merge
- Wizard integration
- Response plan generation
- LLM formulation via AIOrchestrator
- State persistence

### WhatsApp

**Status: CONNECTED**

Webhook at `server.py:2560` → `process_green_api_webhook` (line 875) → `_generate_ai_reply` (line 962) → `ConversationStateEngine.process_turn()` → validator → `send_whatsapp` (line 970).

### Telegram

**Status: CONNECTED**

Webhook at `server.py:2586` → `process_telegram_webhook` (line 1001) → `_generate_ai_reply` (line 1120) → `ConversationStateEngine.process_turn()` → validator → `send_telegram` (line 1128).

### Web (V3)

**Status: PERSIST-ONLY (no response yet)**

`_handle_v3_conversation_message_post` at `server.py:3760` persists to `conversation_sessions` + `conversation_messages` tables. Returns `{status: "received"}`. No `_generate_ai_reply` call. Response generation will be added in Chantier 2.

## Deployment

**OVH: NOT DEPLOYED**

This validation is local only. The updated conversation runtime has not been deployed to the OVH production environment.

## Next Steps

| Item | Owner | Target |
|------|-------|--------|
| Chantier 2: Wire Web V3 into canonical runtime | Pipeline | TBD |
| Chantier 2: Add response generation to Web channel | Pipeline | TBD |
| OVH deployment of canonical runtime | DevOps | After Chantier 2 |
| Real user acceptance testing | QA | After OVH deployment |
