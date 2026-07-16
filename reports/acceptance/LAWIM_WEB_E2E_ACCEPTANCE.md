# LAWIM — Web E2E Acceptance Report

**Date:** 2026-07-15  
**QA Dataset Run ID:** QA-20260715-120000  

---

## E2E Scenario

| Step | Actor | Action | Result |
|------|-------|--------|--------|
| 1 | qa.user.01 | Login | ✅ Connected |
| 2 | qa.user.01 | Start conversation | ✅ Created |
| 3 | qa.user.01 | Qualification (10 steps) | ✅ Completed |
| 4 | qa.user.01 | Property search | ✅ Results displayed |
| 5 | qa.user.01 | Matching request | ✅ Score 92/100 |
| 6 | qa.user.01 | Visit request | ✅ Created (DEMO-Villa-DLA) |
| 7 | qa.agent.agency01.01 | Process visit | ✅ Scheduled |
| 8 | qa.agent.agency01.01 | Create transaction | ✅ Open |
| 9 | qa.user.01 | Payment (sandbox) | ✅ QA-PAY-001 SUCCESS |
| 10 | — | Conversion recorded | ✅ Created |
| 11 | — | Attribution (first-touch) | ✅ FB campaign |
| 12 | — | Analytics event | ✅ Delivered |
| 13 | — | Learning outcome | ✅ Recorded |

## Data Consistency

| Object | Created | Linked | Verified |
|--------|---------|--------|----------|
| Conversation | ✅ | → User, Agent | ✅ |
| Qualification | ✅ | → Conversation, Property | ✅ |
| Match | ✅ | → Qualification | ✅ |
| Visit | ✅ | → Match, Agent | ✅ |
| Transaction | ✅ | → Visit | ✅ |
| Payment | ✅ | → Transaction, Campay | ✅ |
| Conversion | ✅ | → Payment, Tracking | ✅ |
| Attribution | ✅ | → Conversion | ✅ |

## Decision

```
ACCEPTED — FULL WEB E2E FLOW
```
