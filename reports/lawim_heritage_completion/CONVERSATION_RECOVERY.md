# CONVERSATION RECOVERY REPORT — LAWIM H0.4

**Date:** 15 July 2026
**Source:** 03-CONVERSATION-REFERENCE.md, knowledge_unified/commercial/, CONVERSATION_MODEL.md

---

## What Was Recovered

| Concept | Details | Source |
|---------|---------|--------|
| Complete tone rules | Professional, warm, direct, reassuring, concise, action-oriented | knowledge_unified/commercial/ |
| 10 forbidden patterns | No AI mention, no robot intros, no over-apologizing, etc. | knowledge_unified/commercial/ |
| 7 channel behaviors | WhatsApp(1q/message), Telegram(2-3 fields), Dashboard, FB, SMS, Voice | 03-CONVERSATION |
| Memory system | J1(1j), J2(≤7j), J3(≤30j), J4(>30j), retention 365j | conversation_memory.py |
| Follow-up system | J1(24h), J7(168h), J30(720h), J90(2160h) + priority model | follow_up_system.py |
| Response hierarchy | DeepSeek → Local Rules → Templates | response_router.py |
| 7 templates (FR/EN/PID) | welcome, help, no_match, thanks, ask_name, ask_phone, stats | multilingual_responses.py |
| 10 escalation conditions | Legal question, dispute, explicit request, etc. | CONVERSATION_MODEL.md |
| 6 conversation intents | BUY, RENT, SELL, INVESTOR, SEARCH, NEGOTIATE + URGENCY | knowledge_unified/language/ |
| 12 conversation events | message_received, intent_detected, lead_scored, etc. | CONVERSATION_MODEL.md |
| 8 special commands | SIGNALER, SUPPRIMER, ACCOMPAGNEMENT, OUI/NON, STATS, LANGUE, RECHERCHE, PRIORITAIRE, RELANCER | CONVERSATION_MODEL.md |
| Double consent rules | Never share without explicit consent, traceable, timestamped | 03-CONVERSATION |
| Anonymity rules | By default, pseudonym, 7 days for deletion | CONVERSATION_MODEL.md |
| Emotional triggers | Physical visit, concrete proof, discourse coherence, reactivity, etc. | knowledge_unified/commercial/ |
| 6 response validation rules | Min length, max length, type keyword match, etc. | response_policy.py |

**Source:** docs/lawim_heritage_gold/CONVERSATION_MODEL.md + docs/lawim_heritage_gold/RULE_INDEX.md
