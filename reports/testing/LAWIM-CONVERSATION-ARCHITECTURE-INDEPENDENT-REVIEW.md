# LAWIM V2 — Conversation Architecture Independent Review

**HEAD :** `b2fe5e34`
**Reviewer :** Agent I
**Date :** 2026-07-20

## Runtime is Unique

`ConversationStateEngine.process_turn()` is the only entry point for response generation. Both WhatsApp and Telegram webhook handlers call `_generate_ai_reply()`, which routes through `ConversationStateEngine.process_turn()` as the primary path. The fallback (AIOrchestrator) is only reached when the state engine is `None` or raises an exception.

**Verified:** `process_green_api_webhook` (line 875) and `process_telegram_webhook` (line 1001) both call `_generate_ai_reply` (line 962 and 1120), which routes through `ConversationStateEngine` (line 628).

## No Channel Bypasses

Both WhatsApp and Telegram go through `_generate_ai_reply`, which uses `ConversationStateEngine` first. No channel has a direct LLM call path that skips the state engine.

**Verified:**
- WhatsApp: `_generate_ai_reply` → `ConversationStateEngine.process_turn()` → validator → `send_whatsapp`
- Telegram: `_generate_ai_reply` → `ConversationStateEngine.process_turn()` → validator → `send_telegram`
- Web (V3): persists only — no response generated (explicit scope exclusion)
- CRM: admin-only direct send (authorized, by design)

## ResponsePlan Mandatory

Every response path creates a `ResponsePlan`. The primary path generates one via `ConversationStateEngine._build_response_plan()`. The fallback path creates a synthetic `ResponsePlan(maximum_questions=1)`. Both pass through `ConversationResponseValidator.validate()`.

**Verified by architecture tests:**
- `test_response_plan_exists_before_provider_call` — PASS
- `test_turn_decision_exists_before_response_plan` — PASS
- `test_provider_cannot_add_second_question` — PASS

## Providers Constrained

Every provider response (primary or fallback) is checked by `ConversationResponseValidator.validate()` before delivery. The validator checks forbidden content (neutral assistant phrases, external referrals, unrequested translation, grammar correction) and enforces the maximum question count from the ResponsePlan.

## Validator Active

The following architecture contract tests confirm the validator is active and effective:

| Test | Status | What it verifies |
|------|--------|------------------|
| `test_provider_cannot_add_second_question` | PASS | Multiple questions trigger REPAIR |
| `test_neutral_assistant_phrase_is_rejected` | PASS | "I cannot make business decisions" blocked |
| `test_external_referral_is_rejected` | PASS | "Jumia", "SeLoger" etc. blocked |
| `test_translation_without_request_is_rejected` | PASS | Translation patterns blocked |
| `test_grammar_correction_without_request_is_rejected` | PASS | Grammar correction blocked |

## Dedup Active

- **Inbound dedup:** WhatsApp uses `event_key` (built via `build_event_key()` at `green_api.py`) checked against `communication_events` table. Telegram uses `update_key` (built via `build_telegram_event_key()` at `telegram_webhook.py`) checked against `telegram_updates` table.
- **Outbound dedup:** Provider `message_id` is stored and returned in delivery responses. Duplicate detection prevents re-processing same webhooks.

## Language Preserved

`ConversationState` has a `language` field (`state.py:26`). Language detection runs at `engine.py:91` via `_detect_language()`. If the detected language differs from the stored `state.language`, the state is updated. Architecture tests verify:
- `test_active_language_is_preserved` — PASS
- `test_english_conversation_stays_english` — PASS
- `test_foreign_word_does_not_change_language` — PASS

## No Tests Weakened

All pre-existing tests still pass:

| Suite | Status |
|-------|--------|
| Architecture contract | 13/13 PASS |
| Real failures | 8/8 PASS |
| Conversation baseline | 49/49 PASS |
| Communication delivery | 8/8 PASS |
| Webhooks | 6/6 PASS |
| AI fallback | 38/38 PASS |

**Total: 122 PASS, 0 XFAIL, 0 FAIL**

## Conclusion

**PASS** — The canonical conversation runtime is correctly implemented. `ConversationStateEngine` is the unique entry point, `ResponsePlan` is mandatory, `ConversationResponseValidator` is active, dedup is operational, language continuity is maintained, and all pre-existing tests pass without weakening.
