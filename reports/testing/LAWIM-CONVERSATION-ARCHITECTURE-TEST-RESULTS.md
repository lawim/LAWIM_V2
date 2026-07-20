# LAWIM V2 — Conversation Architecture Test Results

**HEAD :** `b2fe5e34`
**Date :** 2026-07-20

## Architecture Contract (`test_conversation_architecture_contract.py`)

| Test | Result |
|------|--------|
| `test_whatsapp_webhook_calls_runtime_not_llm_directly` | PASS |
| `test_telegram_webhook_calls_same_runtime_as_whatsapp` | PASS |
| `test_response_plan_exists_before_provider_call` | PASS |
| `test_turn_decision_exists_before_response_plan` | PASS |
| `test_one_inbound_message_produces_one_outbound_message` | PASS |
| `test_provider_cannot_add_second_question` | PASS |
| `test_neutral_assistant_phrase_is_rejected` | PASS |
| `test_external_referral_is_rejected` | PASS |
| `test_translation_without_request_is_rejected` | PASS |
| `test_grammar_correction_without_request_is_rejected` | PASS |
| `test_active_language_is_preserved` | PASS |
| `test_english_conversation_stays_english` | PASS |
| `test_foreign_word_does_not_change_language` | PASS |

**13/13 PASS**

## Real Failures (`test_conversation_architecture_real_failures.py`)

| Test | Result |
|------|--------|
| `test_studio_in_conversation_is_real_estate` | PASS |
| `test_residential_use_continues_studio_request` | PASS |
| `test_french_conversation_is_not_translated` | PASS |
| `test_i_dont_understand_rephrases_last_question` | PASS |
| `test_grammar_is_not_corrected_without_request` | PASS |
| `test_handover_requires_explicit_request` | PASS |
| `test_one_question_per_response` | PASS |
| `test_no_external_referral_in_greeting` | PASS |

**8/8 PASS**

## Conversation Baseline

| Suite | Tests | Result |
|-------|-------|--------|
| Intent and routing | 6 | 6/6 PASS |
| Handover policy | 5 | 5/5 PASS |
| Author identity | 5 | 5/5 PASS |
| AI footer policy | 7 | 7/7 PASS |
| Context baseline | 7 | 7/7 PASS |
| External referral policy | 11 | 11/11 PASS |
| Progressive wizard runtime | 8 | 8/8 PASS |

**49/49 PASS**

## Communication Delivery (`test_communication_delivery.py`)

| Test | Result |
|------|--------|
| `test_mask_delivery_recipient_masks_phone_and_chat_ids` | PASS |
| `test_sanitize_delivery_url_masks_provider_tokens` | PASS |
| `test_resolve_ipv4_prefers_ipv4` | PASS |
| `test_send_green_api_message_extracts_message_id` | PASS |
| `test_send_telegram_message_extracts_message_id` | PASS |
| `test_send_telegram_message_extracts_error_description` | PASS |
| `test_repository_send_whatsapp_records_sanitized_delivery` | PASS |
| `test_repository_send_telegram_records_sanitized_delivery` | PASS |

**8/8 PASS**

## Webhooks

| Suite | Tests | Result |
|-------|-------|--------|
| Green API webhook (`test_green_api_webhook.py`) | 3 | 3/3 PASS |
| Telegram webhook (`test_telegram_webhook.py`) | 3 | 3/3 PASS |

**6/6 PASS**

## AI Fallback (`test_ai_fallback_internal.py`)

| Class | Tests | Result |
|-------|-------|--------|
| `TestProviderFallbackChain` | 6 | 6/6 PASS |
| `TestInternalReasoningEngine` | 8 | 8/8 PASS |
| `TestDisclaimerManager` | 9 | 9/9 PASS |
| `TestPromptReconstructionEngine` | 7 | 7/7 PASS |
| `TestMemoryOptimizer` | 7 | 7/7 PASS |
| `TestOrchestrationOutcome` | 1 | 1/1 PASS |

**38/38 PASS**

## Summary

| Category | Pass | Total |
|----------|------|-------|
| Architecture contract | 13 | 13 |
| Real failures | 8 | 8 |
| Conversation baseline | 49 | 49 |
| Communication delivery | 8 | 8 |
| Webhooks | 6 | 6 |
| AI fallback | 38 | 38 |
| **Total** | **122** | **122** |
