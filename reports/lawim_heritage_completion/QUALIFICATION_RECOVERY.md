# QUALIFICATION RECOVERY REPORT — LAWIM H0.4

**Date:** 15 July 2026
**Source:** QUALIFICATION_MODEL.md, RULE_ENGINE_V5.json, lead_classifier_v1.json, knowledge_unified/qualification/

---

## What Was Recovered

| Concept | Details | Source |
|---------|---------|--------|
| 150+ qualification rules | Complete pipeline (V1-V5) | RULE_INDEX.md + knowledge_unified/ |
| 5 lead types | tenant(40), buyer(60), seller(50), investor(80), diaspora_investor(95) | lead_classifier_v1.json |
| 6 boosters | budget_detected(+15), city_detected(+10), neighborhood(+10), urgent(+20), diaspora(+25), cash(+15) | lead_classifier_v1.json |
| 3 penalties | missing_budget(-10), unclear_location(-10), spam(-50) | lead_classifier_v1.json |
| V1 thresholds | HOT≥80, WARM≥60, COLD≥40, LOW<40 | lead_classifier_v1.json |
| V5 thresholds | HOT≥0.8, WARM≥0.5, COLD≥0.3, SPAM≤0.2 | RULE_ENGINE_V5.json |
| V5 Pipeline 8 étapes | incoming→normalize→extract→detect_intent→context→scoring→classification→routing | RULE_ENGINE_V5.json |
| 10 qualification steps | Intention→Type→Ville→Quartier→Budget→Délai→Critères→Préférences→Confirmation→Escalade | RULE_ENGINE_V5.json |
| 4 tracked behaviors | message_history, response_time, budget_changes, visit_requests | RULE_ENGINE_V5.json |
| 7 user typologies | Plus mapping to CRM roles | knowledge_unified/qualification/ |
| CRM Scoring V5 weights | 7 factors (0.15/0.20/0.20/0.10/0.15/0.20/0.10) | RULE_ENGINE_V5.json |
| Priority levels | P0(100-95), P1(90-85), P2(75-60), P3(40) | lead_scoring.json |
| Lead scoring rules weights | budget=20, location=15, urgency=20, diaspora=10, etc. | lead_scoring_rules.json |
| 4 anti-fraud layers | broker_spam, duplicate_listing, fake_price, suspicious_urgency | RULE_ENGINE_V5.json |
| 5 stop conditions | City not covered, empty inventory, user requests human, repetitive thread, fraud detected | CONVERSATION_MODEL.md |

**Source:** docs/lawim_heritage_gold/QUALIFICATION_MODEL.md + docs/lawim_heritage_gold/QUALIFICATION_HERITAGE_EXTRACTION.md
