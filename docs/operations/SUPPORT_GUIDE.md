# LAWIM_V2 — Support Guide

**Document ID:** LAWIM-OPS-SUPPORT-V1
**Status:** OPERATIONAL
**Date:** 2026-07-15

---

## 1. Support Tiers

| Tier | Role | Responsibilities |
|------|------|------------------|
| L1 | Support Agent (AI) | Common issues, FAQ, routing |
| L2 | Human Support | Complex issues, handover from AI |
| L3 | Engineering | Bugs, incidents, escalations |

## 2. Common Issues

### User cannot log in
- Check credentials
- Verify session expiry
- Check database connectivity

### WhatsApp message not delivered
- Verify Green API token
- Check webhook endpoint
- Confirm phone number format (E.164)
- Review delivery logs in `communication_messages`

### Telegram message not delivered
- Verify bot token
- Check webhook is set: `GET /api/notifications/telegram/webhook`
- Confirm chat_id is valid
- Review telegram_messages table

### Payment not confirmed
- Check Campay callback was received
- Verify idempotency key
- Check payment status in Campay dashboard
- Review payment logs

### Agent not responding
- Check feature flag is enabled
- Verify agent is in ACTIVE status
- Check invocation logs
- Verify context builder has required data

## 3. Escalation Matrix

| Issue Type | L1 | L2 | L3 |
|-----------|-----|-----|-----|
| Login issues | ✅ | — | — |
| Conversation errors | ✅ | ✅ | — |
| Qualification failures | ✅ | ✅ | — |
| Payment failures | — | ✅ | ✅ |
| System downtime | — | — | ✅ |
| Data loss | — | — | ✅ |
| Security incident | — | ✅ | ✅ |
