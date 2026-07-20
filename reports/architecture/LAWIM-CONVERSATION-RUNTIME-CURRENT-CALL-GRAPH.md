# LAWIM V2 — Current Call Graph (Conversation Runtime)

**Date :** 2026-07-20
**HEAD :** `b2fe5e34`

## WhatsApp Channel

```
server.py:2560 _handle_green_api_webhook
  → communication/service.py:875 process_green_api_webhook(payload)
    → normalization (GREEN_API_SUPPORTED_WEBHOOKS check)
    → duplicate detection (event_key + communication_events table)
    → if incomingMessageReceived and not duplicate:
      → communication/service.py:962 _generate_ai_reply(
           raw_text, channel="whatsapp", conversation_key, actor_id)
        → orphaned build_request call (line 612, result discarded)
        → handover detection (keywords)
        → communication/service.py:628 ConversationStateEngine.process_turn(
             actor_id, channel, conversation_key, message, language)
          → ConversationResolver.resolve()
          → ConversationStateRepository.load()
          → ConversationStateEngine._resolve_or_create_state()
          → wizard integration (ProgressiveWizard if configured)
          → ConversationStateEngine._build_response_plan()
          → ConversationStateEngine._generate_response()
          → ConversationStateRepository.save()
          → returns {state, response, response_plan, ...}
        → communication/service.py:641 ConversationResponseValidator.validate(
             response_text, plan)
          → detect_forbidden_content (neutral assistant, referrals, translation, grammar)
          → question count check (maximum_questions)
        → footer append (line 644-648)
      → communication/service.py:970 repository.send_whatsapp(
           to_number=normalized_number, body=reply_text)
      → delivery logged to whatsapp_delivery_logs
```

## Telegram Channel

```
server.py:2586 _handle_telegram_webhook
  → communication/service.py:1001 process_telegram_webhook(payload)
    → normalization (TELEGRAM_SUPPORTED_UPDATE_TYPES check)
    → duplicate detection (update_key + telegram_updates table)
    → if message/business_message/guest_message and not duplicate:
      → communication/service.py:1120 _generate_ai_reply(
           raw_text, channel="telegram", conversation_key, actor_id)
        → (same call graph as WhatsApp from this point)
      → communication/service.py:1128 repository.send_telegram(
           chat_id=chat_id, body=reply_text)
      → delivery logged to telegram_messages
```

## Web Channel (V3 API)

```
server.py:3760 _handle_v3_conversation_message_post(body, actor)
  → persist message to conversation_sessions + conversation_messages
  → return {status: "received", conversation_id, ...}
  → NO call to _generate_ai_reply
  → NO response generation
  → Only persist-and-acknowledge
```

## CRM Channel

```
server.py:2867 _handle_v2_api_post → path == "/api/v2/crm/whatsapp"
  → crm/service.py:211 send_whatsapp(actor, body)
    → _require_auth(actor)
    → repository.send_crm_whatsapp(contact_id, body, to_number)
    → direct send, no state engine, no ResponsePlan
  → Authorized admin action only
```

## Orphaned `build_request` Call

At `communication/service.py:612`, inside `_generate_ai_reply`:

```python
if self.ai is not None:
    try:
        self.ai.build_request(  # line 612
            channel=channel, text=raw_text,
            conversation_key=conversation_key, language=language,
        )
    except Exception:
        pass  # result discarded silently
```

This call builds an `AIRequest` object via `AIOrchestrator.build_request()` but discards the return value. The exception handler silently absorbs all errors. This appears to be a dead-code remnant or a warming call — no side effect beyond logging/metrics inside `build_request` itself (classify, continuity reconstruction, memory loading).

## AIOrchestrator Fallback Path

At `communication/service.py:656-681`, when `ConversationStateEngine` is `None` or raises an exception:

```python
if self.ai is not None:
    try:
        request = self.ai.build_request(  # line 658
            channel=channel, text=raw_text,
            conversation_key=conversation_key, language=language,
        )
        outcome = self.ai.generate(request)  # line 664
        response_text = outcome.response.content.strip()
        if response_text:
            plan = ResponsePlan(maximum_questions=1)
            validated, _ = ConversationResponseValidator().validate(
                response_text, plan)
            response_text = validated
            # footer appended
            return response_text
    except Exception as exc:
        # logged, returns empty string
```

This path:
1. Invokes the full `AIOrchestrator.build_request()` → `generate()` chain
2. Creates a synthetic `ResponsePlan(maximum_questions=1)` for validation
3. Runs `ConversationResponseValidator.validate()` on the output
4. Applies the AI footer

This means even the fallback path respects ResponsePlan constraints and validator rules.

## Summary

| Channel | Entry | Uses State Engine | Uses ResponsePlan | Uses Validator |
|---------|-------|-------------------|-------------------|----------------|
| WhatsApp | `_generate_ai_reply` | Yes (primary), AIOrchestrator (fallback) | Yes (engine or synthetic) | Yes |
| Telegram | `_generate_ai_reply` | Yes (primary), AIOrchestrator (fallback) | Yes (engine or synthetic) | Yes |
| Web (V3) | `_handle_v3_conversation_message_post` | No | No | No |
| CRM | `send_whatsapp` | No | No | No |
