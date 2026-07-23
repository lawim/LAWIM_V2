# Programme E — Existing V2 Channel Audit

**Date:** 2026-07-23

## WhatsApp / Green API

| Aspect | Details |
|--------|---------|
| Entry point | `code/lawim_v2/server.py` — `/green-api/webhook` route |
| Normalization | Raw text extracted from `messageData.textMessageData.textMessage` |
| Identity | `senderData.chatId` + `senderData.sender` (phone number) |
| Conversation ID | `chatId` maps to conversation |
| Engine called | `CommunicationService.process_green_api_webhook()` |
| Provider called | Green API for delivery, AIOrchestrator for generation |
| Response delivery | Green API `sendMessage` via `WhatsAppSender` |
| Error handling | Webhook-level try/except, logged without secrets |

## Telegram Bot API

| Aspect | Details |
|--------|---------|
| Entry point | `code/lawim_v2/server.py` — `/telegram/webhook` route |
| Normalization | `message.text` with optional entity parsing |
| Identity | `message.chat.id` and `message.from.id` |
| Conversation ID | `chat_id` maps to conversation |
| Engine called | `CommunicationService.process_telegram_webhook()` |
| Provider called | Telegram Bot API, AIOrchestrator for generation |
| Response delivery | `bot.sendMessage()` with parse_mode |
| Error handling | Webhook try/except, IPv4/IPv6 handling |

## Web / API

| Aspect | Details |
|--------|---------|
| Entry point | `code/lawim_v2/server.py` — `/api/chat` |
| Authentication | Token-based (LAWIM_API_TOKEN env var) |
| Engine called | Direct `CommunicationService` call |
| Response | JSON with text and metadata |

## CommunicationService

The central V2 orchestrator. Performs: webhook validation → ConversationStateEngine → AIOrchestrator → response delivery.

## ConversationStateEngine

V2 state machine. Tracks intent, slots, conversation history. Not a project-centric store.

## ProgressiveWizard

Step-by-step field collection within V2 conversation state. Not wired to ProjectProfile.

## ResponsePlan / DialoguePlan

V2 contracts for response structure. Produced by ConversationStateEngine, consumed by AIOrchestrator.

## ProviderMemoryContext

Context passed to LLM providers with conversation history and extraction instructions.

## Key Findings for Programme E

1. V2 already has working webhook handlers for WhatsApp and Telegram
2. V2 identity resolution is per-channel (no cross-channel linking)
3. V2 state is conversation-scoped, not project-scoped
4. V2 response generation is LLM-driven (Programme F scope)
5. V2 has no deduplication at interaction level
6. V2 has no divergence analysis
7. V2 has no V3-compatible interaction envelope
