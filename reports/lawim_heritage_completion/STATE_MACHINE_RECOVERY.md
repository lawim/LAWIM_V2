# STATE MACHINE RECOVERY REPORT — LAWIM H0.4

**Date:** 15 July 2026
**Source:** 05-WORKFLOW-REFERENCE.md, 04-DECISION-ENGINE-REFERENCE.md, knowledge_unified/

---

## 1. Property State Machine

```
                     ┌─────────────────────────────────────────┐
                     │                                         │
                     v                                         │
Creation → Qualification → Validation → Published → Available →┤
                     │                                         │
                     │         ┌───────────────────────────────┘
                     │         │
                     v         v
                  Matching → Visits → Negotiation → Reserved → Transaction → Unavailable
                                                                                │
                                                                                v
                                                                         Archived
                                                                                │
                                                                                v
                                                                         Reactivation
```

**Transitions:** 12 states, 15+ transitions
**Auto-archiving:** After 90 days inactivity
**Events:** publication, modification, matching, visit, negotiation, signature, payment, closure, archiving

## 2. Dossier State Machine

```
Creation → Qualification → InProgress → Matching → Proposal → UnderReview
                                                                     │
                                              ┌──────────────────────┤
                                              v                      v
                                         Accepted               Refused
                                              │                      │
                                              v                      v
                                         Transaction          Rematching
                                              │                 ┌─────┘
                                              v                 v
                                         Closed            Proposal (new)
```

**7 states:** CREATED, QUALIFYING, MATCHING, PROPOSED, UNDER_REVIEW, CLOSED, REOPENED
**Events:** creation, qualification_complete, match_found, proposal_accepted, proposal_refused, time_expired, manual_reopen

## 3. User State Machine (CRM)

```
                    NEW_USER
                        │
                        v
              SEARCHING_PROPERTY
                   │        │
                   v        v
          PROPERTY_OWNER  LEAD_CREATED
                   │        │
                   v        v
                 AGENT  ──→ PREMIUM_AGENT
                   │
                   v
               INACTIVE
```

**7 states:** NEW_USER, SEARCHING_PROPERTY, PROPERTY_OWNER, AGENT, LEAD_CREATED, PREMIUM_AGENT, INACTIVE
**Events:** message.received, intent.detected, user.created, user.state_changed, property.created, lead.created, match.generated

## 4. Matching State Machine

```
Need → CriteriaDefinition → SearchActive → MatchFound → ProposalSent → AwaitingDecision
                                                                              │
                                     ┌────────────────────────────────────────┤
                                     v                                        v
                                Accepted                                  Refused
                                     │                                        │
                                     v                                     ┌──┘
                                ContactHolder                          Learning
                                     │                             ┌──────┘
                                     v                             v
                                VisitOrganized               RematchingTriggered
                                     │                             │
                                     v                             v
                                NegotiationOpen               NewSearch (adjusted)
                                     │
                                     v
                                Transaction → Closed
```

## 5. Visit State Machine

```
Requested → ToSchedule → Scheduling → Proposed → AwaitingConfirmation → Confirmed
                                                                              │
                                                                              v
                                                                         Prepared
                                                                              │
                                                                              v
                                                                         Realized
                                                                              │
                                                                   ┌─────────┴────────┐
                                                                   v                  v
                                                              Satisfied        NotSatisfied
                                                                   │                  │
                                                                   v                  v
                                                              FollowUp           ReProposal
```

**Source:** docs/lawim_heritage_gold/WORKFLOW_EXTRACTION_COMPLETE.md §6
