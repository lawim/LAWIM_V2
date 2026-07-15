# RELATIONSHIP LIFECYCLE

**Domain:** Relationship State Machine — Mise en Relation
**Version:** 1.0
**Status:** CANONICAL
**Source:** Heritage Gold — WORKFLOW_EXTRACTION_COMPLETE.md §5, §25, §26
**Prerequisite:** RELATIONSHIP_EXECUTION_ARCHITECTURE.md, CONSENT_EXECUTION_CONTRACT.md

---

## 1. State Machine Overview

### 1.1 Entity

`relationship` — Represents a Mise en Relation between a demandeur and a holder for a specific property.

### 1.2 States

```
                    ┌───────────────────────────────────────────────────────────────┐
                    │                       PROPOSED                                │
                    │  (Match selected, proposition created)                        │
                    └───────────────────────┬───────────────────────────────────────┘
                                            │
                                            ▼
                    ┌───────────────────────────────────────────────────────────────┐
                    │                 CONSENT_DEMANDEUR_PENDING                     │
                    │  (Demandeur asked to confirm interest)                        │
                    └───────┬───────────────────────────────────────────┬───────────┘
                            │                                           │
                     consented │                                    declined │
                            ▼                                           ▼
                    ┌──────────────────┐                       ┌──────────────────┐
                    │ CONSENT_DEMANDEUR │                       │     CLOSED       │
                    │     _GRANTED     │                       │ (Demandeur       │
                    └───────┬──────────┘                       │  declined)       │
                            │                                  └──────────────────┘
                            ▼
                    ┌───────────────────────────────────────────────────────────────┐
                    │                 CONSENT_HOLDER_PENDING                        │
                    │  (Holder contacted, asked to accept)                          │
                    └───┬───────┬───────┬───────┬──────────────────────┬────────────┘
                        │       │       │       │                      │
                   accept │ refuse │ delay │ alt   │            unavailable
                        ▼       ▼       ▼       ▼                      ▼
                    ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐    ┌───────────────┐
                    │ ACTIVE│ │CLOSED │ │PENDING│ │ACTIVE │    │PROPERTY       │
                    │       │ │(Holder│ │ (timer│ │ (alt  │    │UNAVAILABLE →  │
                    │       │ │refused│ │  set) │ │ prop) │    │CLOSED         │
                    └───┬───┘ └───────┘ └───────┘ └───────┘    └───────────────┘
                        │
                        ├────────────────────────────────┬──────────────────────┐
                        │                                │                      │
                        ▼                                ▼                      ▼
                    ┌──────────┐                   ┌──────────┐          ┌──────────┐
                    │ FOLLOWUP │                   │ EXPIRED  │          │ REVOKED  │
                    │ (NBA     │                   │ (SLA     │          │ (Party   │
                    │  driven) │                   │  passed) │          │  request)│
                    └──────────┘                   └──────────┘          └──────────┘
                        │                                                    │
                        ▼                                                    │
                    ┌──────────┐                                              │
                    │  ACTIVE  │◄─────────────────────────────────────────────┘
                    │ (re-     │
                    │  engaged)│
                    └────┬─────┘
                         │
                         ▼ (objective achieved / abandoned)
                    ┌──────────┐
                    │  CLOSED  │
                    └────┬─────┘
                         │
                         ▼
                    ┌──────────┐
                    │ ARCHIVED │
                    └──────────┘
```

### 1.3 State Definitions

| State | Code | Description | Type |
|---|---|---|---|
| `proposed` | `PROPOSED` | Match selected by demandeur, proposition created | Active |
| `consent_demandeur_pending` | `C_DEMANDEUR_PENDING` | Awaiting demandeur interest confirmation | Active |
| `consent_demandeur_granted` | `C_DEMANDEUR_GRANTED` | Demandeur consented, holder contact initiated | Active |
| `consent_holder_pending` | `C_HOLDER_PENDING` | Awaiting holder response | Active |
| `active` | `ACTIVE` | Double consent obtained, relationship live | Active |
| `follow_up` | `FOLLOW_UP` | NBA-driven follow-up phase | Active |
| `expired` | `EXPIRED` | SLA exceeded without activity | Terminal |
| `revoked` | `REVOKED` | Party withdrew consent | Terminal |
| `closed` | `CLOSED` | Objective achieved or abandoned | Terminal |
| `archived` | `ARCHIVED` | Final archival state | Terminal |

---

## 2. State Transitions

### 2.1 Transition Table

| From | To | Event | Guard | Action | Side Effect | Audit Event |
|---|---|---|---|---|---|---|
| `PROPOSED` | `C_DEMANDEUR_PENDING` | `demandeur_interest_declared` | Dossier active, property available | Create consent request for demandeur | Schedule demandeur consent SLA timer | `relationship.demandeur_consent_requested` |
| `C_DEMANDEUR_PENDING` | `C_DEMANDEUR_GRANTED` | `demandeur_consent_granted` | Demandeur is authorized party | Record demandeur consent | Initiate holder contact, mask demandeur identity | `relationship.demandeur_consent_granted` |
| `C_DEMANDEUR_PENDING` | `CLOSED` | `demandeur_consent_declined` | Demandeur is authorized party | Record refusal | Trigger rematching | `relationship.demandeur_consent_declined` |
| `C_DEMANDEUR_PENDING` | `EXPIRED` | `demandeur_consent_timeout` | SLA exceeded | Auto-close consent request | Notify demandeur | `relationship.demandeur_consent_expired` |
| `C_DEMANDEUR_GRANTED` | `C_HOLDER_PENDING` | `holder_contact_initiated` | Demandeur consent valid | Send holder notification | Schedule holder SLA timer | `relationship.holder_contacted` |
| `C_HOLDER_PENDING` | `ACTIVE` | `holder_consent_granted` | Holder is authorized party | Record holder consent, lift anonymity | Set interlocutor to holder, notify both parties, compute NBA | `relationship.created` |
| `C_HOLDER_PENDING` | `CLOSED` | `holder_consent_refused` | Holder is authorized party | Record refusal | Notify demandeur, trigger rematching | `relationship.holder_consent_refused` |
| `C_HOLDER_PENDING` | `C_HOLDER_PENDING` | `holder_consent_delayed` | Holder is authorized party | Set timer per holder request | Schedule follow-up reminder | `relationship.holder_consent_delayed` |
| `C_HOLDER_PENDING` | `ACTIVE` | `holder_alternative_proposed` | Holder proposes different property | Create new proposition | Initiate new relationship on alternative property | `relationship.alternative_proposed` |
| `C_HOLDER_PENDING` | `CLOSED` | `holder_declared_unavailable` | Holder confirms unavailability | Mark property unavailable | Notify demandeur, trigger rematching | `relationship.holder_unavailable` |
| `C_HOLDER_PENDING` | `EXPIRED` | `holder_consent_timeout` | SLA exceeded, silence workflow exhausted | Auto-close | Mark property "to confirm", trigger rematching, notify LAWIM | `relationship.holder_consent_expired` |
| `ACTIVE` | `FOLLOW_UP` | `follow_up_due` | NBA triggers follow-up | Schedule follow-up action | Execute NBA: send message, request feedback | `relationship.follow_up_started` |
| `FOLLOW_UP` | `ACTIVE` | `party_responded` | Party engages with follow-up | Reset activity timer | Compute next NBA | `relationship.re_engaged` |
| `FOLLOW_UP` | `EXPIRED` | `inactivity_timeout` | No response within follow-up SLA | Auto-close | Notify parties | `relationship.expired` |
| `ACTIVE` | `REVOKED` | `consent_revoked` | Party requests revocation | Revoke consent, close relationship | Notify other party, archive relationship | `relationship.revoked` |
| `FOLLOW_UP` | `REVOKED` | `consent_revoked` | Party requests revocation | Revoke consent, close relationship | Notify other party, archive relationship | `relationship.revoked` |
| `ACTIVE` | `CLOSED` | `objective_achieved` | Transaction or negotiation completed | Record successful outcome | Trigger satisfaction survey, update stats | `relationship.closed_success` |
| `ACTIVE` | `CLOSED` | `objective_abandoned` | Party ends pursuit | Record abandonment | Trigger rematching | `relationship.closed_abandoned` |
| `FOLLOW_UP` | `CLOSED` | `objective_achieved` | Transaction or negotiation completed | Same as above | Same as above | `relationship.closed_success` |
| `FOLLOW_UP` | `CLOSED` | `objective_abandoned` | Party ends pursuit | Same as above | Same as above | `relationship.closed_abandoned` |
| `EXPIRED` | `ARCHIVED` | `archival_timer_elapsed` | 90 days in expired state | Archive record | Remove from active indexes | `relationship.archived` |
| `REVOKED` | `ARCHIVED` | `archival_timer_elapsed` | 90 days in revoked state | Archive record | Remove from active indexes | `relationship.archived` |
| `CLOSED` | `ARCHIVED` | `archival_timer_elapsed` | 90 days in closed state | Archive record | Remove from active indexes | `relationship.archived` |
| `ARCHIVED` | `ACTIVE` | `reactivation_requested` | Admin authorization obtained | Reactivate relationship | Restore to active workflows | `relationship.reactivated` |

### 2.2 Transition Rules

| Rule | Description |
|---|---|
| **Irreversibility** | Terminal states (`EXPIRED`, `REVOKED`, `CLOSED`) are irreversible except `ARCHIVED → ACTIVE` (admin only) |
| **State order** | States MUST progress forward; no skipping or reversion without explicit transition event |
| **Concurrent transitions** | Only one transition at a time per relationship (optimistic locking via version field) |
| **Transition authorization** | Each transition must be authorized by the correct party role or system |
| **Audit every transition** | Every transition produces an immutable audit event |

---

## 3. Duration & SLA Per State

### 3.1 State Duration Limits

| State | Max Duration | Timer Starts | Timer Resets | Escalation |
|---|---|---|---|---|
| `PROPOSED` | 7 days | On proposition creation | N/A | Reminder at J+3, close at J+7 |
| `C_DEMANDEUR_PENDING` | 48h | On consent request | N/A | Reminder at 24h, close at 48h |
| `C_DEMANDEUR_GRANTED` | 24h | On demandeur consent | N/A | Auto-transition to holder contact |
| `C_HOLDER_PENDING` | Per property type (see §3.2) | On holder contact | On `delay` response | Silence workflow (§4) |
| `ACTIVE` | 90 days without activity | On last party activity | On any party activity | Follow-up cadence (§5) |
| `FOLLOW_UP` | 7 days | On follow-up trigger | On party response | Escalation to LAWIM at J+7 |

### 3.2 Holder SLA by Property Type

Per Heritage Gold SLA tables (WORKFLOW_EXTRACTION_COMPLETE.md §24):

| Property Type | First Holder Contact SLA | First Reminder | Second Reminder | Last Reminder |
|---|---|---|---|---|
| Chambre / Chambre moderne | 24h | +24h | +48h | +72h |
| Studio | 48h | +48h | +72h | +96h |
| Appartement | 72h | +72h | +5 days | +7 days |
| Maison | 5 days | +5 days | +7 days | +10 days |
| Villa / Duplex | 7 days | +7 days | +10 days | +14 days |
| Terrain résidentiel | 10 days | +10 days | +15 days | +20 days |
| Terrain agricole | 15 days | +15 days | +20 days | +25 days |
| Terrain industriel | 20 days | +20 days | +30 days | +40 days |
| Commerce | 7 days | +7 days | +10 days | +14 days |
| Bureau | 10 days | +10 days | +15 days | +20 days |
| Entrepôt | 15 days | +15 days | +20 days | +30 days |
| Hôtel / Immeuble | 30 days | +30 days | +45 days | +60 days |

### 3.3 Active Relationship Inactivity SLA

| Tier | Inactivity Period | Action |
|---|---|---|
| Green | < 7 days | No action |
| Yellow | 7-14 days | Automated follow-up message |
| Orange | 14-21 days | Second follow-up, suggest next action |
| Red | > 21 days | LAWIM collaborator notified, relationship at risk of expiry |
| Expired | 90 days | Automatic expiry |

---

## 4. Holder Silence Workflow

Per Heritage Gold WORKFLOW_EXTRACTION_COMPLETE.md §5:

### 4.1 Silence Timeline

```
Day 0:  Holder contacted
Day D:  First SLA point reached → First reminder sent
Day 2D: Second SLA point reached → Second reminder sent
Day 3D: Third SLA point reached → Last reminder sent
Day 4D: SLA exhausted → Property marked "to confirm"
                             → Rematching triggered for demandeur
                             → LAWIM collaborator notified
```

Where `D` = property-type-specific SLA from §3.2.

### 4.2 Reminder Template

```
First reminder:
  "Bonjour, une personne est intéressée par votre bien [ref].
   Avez-vous eu le temps de considérer la demande ?
   - ✅ Accepter   - ❌ Refuser   - ⏳ Plus tard"

Second reminder:
  "Dernière relance concernant la demande pour [ref].
   Sans réponse sous 48h, le bien sera marqué 'à confirmer'.
   - ✅ Accepter   - ❌ Refuser   - ⏳ Plus tard"

Last reminder:
  "Dernière chance : confirmez-vous la disponibilité de [ref] ?
   Sans réponse sous 24h, nous procédons au re-matching.
   - ✅ Accepter   - ❌ Refuser   - ⏳ Plus tard"
```

### 4.3 Post-Silence Side Effects

| Effect | Description |
|---|---|
| Property status | Marked `À confirmer` |
| Holder reliability score | Decreased |
| Demandeur proposition | Closed, rematching triggered |
| LAWIM notification | Collaborator assigned to follow up manually |

---

## 5. Follow-Up Triggers During Active Relationship

### 5.1 Follow-Up Cadence

Per Heritage Gold follow-up calendar (NEGO-011):

| Follow-Up | Timing | Trigger | Channel |
|---|---|---|---|
| J1 | 24h after relationship creation | No visit scheduled | WhatsApp/Telegram |
| J7 | 7 days after relationship creation | No activity | WhatsApp |
| J30 | 30 days after relationship creation | Low engagement | WhatsApp |
| J90 | 90 days after relationship creation | No transaction progress | Telegram + LAWIM review |

### 5.2 Follow-Up NBA

| State | NBA Action | Priority |
|---|---|---|
| `ACTIVE` (no visit) | "Souhaitez-vous organiser une visite ?" | High |
| `ACTIVE` (visit done, no negotiation) | "Êtes-vous satisfait de la visite ? Souhaitez-vous négocier ?" | High |
| `ACTIVE` (negotiation stalled) | "Besoin d'aide pour la négociation ?" | Medium |
| `ACTIVE` (all quiet) | "Comment se passe votre recherche ?" | Low |
| `FOLLOW_UP` (no response) | Escalate to LAWIM collaborator | Urgent |

### 5.3 Follow-Up Templates

```
J1 follow-up:
  "Félicitations ! Vous êtes maintenant en contact avec [holder_name]
   pour le bien [property_ref]. Souhaitez-vous planifier une visite ?"

J7 follow-up:
  "Comment se passe votre échange concernant [property_ref] ?
   Avez-vous besoin d'aide pour organiser une visite ?"

J30 follow-up:
  "Cela fait un mois que vous êtes en relation pour [property_ref].
   Où en êtes-vous ? Puis-je vous aider à avancer ?"

J90 follow-up:
  "Cela fait 3 mois. Si votre projet a abouti, félicitations !
   Sinon, souhaitez-vous explorer d'autres options ?"
```

---

## 6. NBA Integration for Relationship Management

### 6.1 NBA Triggers

| Event | NBA Triggered | Priority |
|---|---|---|
| Relationship created | Organize visit | 6 |
| Visit completed (satisfied) | Open negotiation | 7 |
| Visit completed (unsatisfied) | Propose another property | 4 |
| Negotiation opened | Follow up | 7 |
| Negotiation successful | Prepare transaction | 6 |
| Hold response timeout | Rematching | 3 |
| Demandeur inactive 7 days | Follow up | 7 |
| Demandeur inactive 21 days | Escalate to LAWIM | - |

### 6.2 NBA Priority Enforcement

Per Heritage Gold Decision Engine Priority (Ch88):

| Priority | Action | When |
|---|---|---|
| 4 | Present a property | After relationship creation, if no visit |
| 5 | Contact the holder | If holder has not responded |
| 6 | Organize a visit | If both parties engaged |
| 7 | Follow up | If no activity within SLA |

---

## 7. Escalation Rules for Stalled Relationships

### 7.1 Escalation Conditions

| Condition | Metrics | Escalation Target |
|---|---|---|
| Holder unresponsive | No response within 3x property SLA | LAWIM collaborator |
| Demandeur unreachable | No response after 3 follow-ups (J1+J7+J30) | LAWIM collaborator |
| Both parties disengaged | 21+ days without interaction | LAWIM collaborator |
| Consent request expired | SLA exceeded without consent | LAWIM collaborator |
| Dispute declared | Any party reports issue | Mediation workflow |

### 7.2 Escalation Process

```
Step 1: System detects stalled condition
Step 2: System attempts automated resolution (last reminder, alternative property)
Step 3: If automated resolution fails → LAWIM collaborator assigned
Step 4: Collaborator attempts manual resolution within 48h
Step 5: If manual resolution fails → Relationship closed, full diagnostic logged
```

### 7.3 LAWIM Collaborator Dashboard

| Metric | Display |
|---|---|
| Stalled relationships count | Total count with SLA exceeded |
| By state | `C_HOLDER_PENDING`, `FOLLOW_UP`, `ACTIVE` (inactive) |
| By priority | Calculated from property type, lead score, time stalled |
| By duration | Hours/days since last activity |
| Action needed | Recommended next action |

---

## 8. Audit Events Per Lifecycle State

### 8.1 Event Catalog

| Lifecycle State | Event | Description | Mandatory Fields |
|---|---|---|---|
| `PROPOSED` | `relationship.proposed` | Relationship proposition created | match_id, dossier_id, property_id |
| `C_DEMANDEUR_PENDING` | `relationship.demandeur_consent_requested` | Demandeur consent asked | consent_id, method |
| `C_DEMANDEUR_GRANTED` | `relationship.demandeur_consent_granted` | Demandeur consented | consent_id, channel |
| `C_DEMANDEUR_PENDING` | `relationship.demandeur_consent_declined` | Demandeur refused | consent_id, reason (opt) |
| `C_DEMANDEUR_PENDING` | `relationship.demandeur_consent_expired` | Demandeur consent timeout | consent_id, sla_exceeded |
| `C_HOLDER_PENDING` | `relationship.holder_contacted` | Holder contacted | property_id, method |
| `C_HOLDER_PENDING` | `relationship.holder_consent_granted` | Holder accepted | consent_id, channel |
| `C_HOLDER_PENDING` | `relationship.holder_consent_refused` | Holder refused | consent_id, reason (opt) |
| `C_HOLDER_PENDING` | `relationship.holder_consent_delayed` | Holder requested delay | delay_duration |
| `C_HOLDER_PENDING` | `relationship.holder_alternative_proposed` | Holder proposed alternative | alternative_property_id |
| `C_HOLDER_PENDING` | `relationship.holder_unavailable` | Holder declared unavailable | new_property_status |
| `C_HOLDER_PENDING` | `relationship.holder_consent_expired` | Holder consent timeout | sla_level, reminders_sent |
| `C_HOLDER_PENDING` | `relationship.holder_reminder_sent` | Reminder sent | reminder_number (1-3) |
| `ACTIVE` | `relationship.created` | Relationship activated | anonymity_lifted_at, interlocutor |
| `ACTIVE` | `relationship.visit_scheduled` | Visit scheduled | visit_id |
| `ACTIVE` | `relationship.negotiation_opened` | Negotiation started | negotiation_id |
| `ACTIVE` | `relationship.activity_recorded` | Party activity | party_id, activity_type |
| `FOLLOW_UP` | `relationship.follow_up_started` | Follow-up initiated | nba_action, template_used |
| `FOLLOW_UP` | `relationship.follow_up_completed` | Follow-up resolved | outcome |
| `FOLLOW_UP` | `relationship.re_engaged` | Party responded | response_type |
| `ACTIVE` | `relationship.consent_revoked` | Consent revoked | party_id, reason |
| `ACTIVE` | `relationship.expired` | Relationship expired | inactivity_duration |
| `ACTIVE` | `relationship.closed_success` | Relationship succeeded | outcome, satisfaction_score |
| `ACTIVE` | `relationship.closed_abandoned` | Relationship abandoned | reason, rematching_triggered |
| `REVOKED` | `relationship.revoked` | Relationship revoked | revoking_party, reason |
| `EXPIRED` | `relationship.expired` | Relationship expired | state_at_expiry |
| `CLOSED` | `relationship.closed` | Relationship closed | final_state, reason |
| `ARCHIVED` | `relationship.archived` | Relationship archived | previous_state |
| `ARCHIVED` | `relationship.reactivated` | Relationship reactivated | admin_id, reason |

### 8.2 Audit Event Structure

```json
{
  "audit_id": "UUID",
  "event_type": "relationship.created",
  "timestamp": "2026-07-15T10:30:00Z",
  "relationship_id": "UUID",
  "old_status": "C_HOLDER_PENDING",
  "new_status": "ACTIVE",
  "actor_id": "UUID",
  "actor_role": "holder",
  "consent_ids": ["UUID_demandeur", "UUID_holder"],
  "metadata": {
    "property_type": "appartement",
    "property_id": "UUID",
    "demandeur_id": "UUID",
    "holder_id": "UUID",
    "anonymity_lifted": true,
    "interlocutor": "proprietaire"
  },
  "nba_resolved": "organize_visit",
  "state_snapshot": {
    "relationship_status": "ACTIVE",
    "demandeur_consent": "granted",
    "holder_consent": "granted",
    "data_sharing": "not_requested",
    "visit_count": 0,
    "last_activity": "2026-07-15T10:30:00Z"
  }
}
```

---

## 9. Health Score Per Relationship

### 9.1 Health Score Components

| Component | Weight | Metric | Calculation |
|---|---|---|---|
| Engagement | 35% | Party activity | Days since last interaction (inverse) |
| Progress | 25% | Lifecycle progression | Current state vs expected progression |
| Responsiveness | 20% | Response time | Average response time vs SLA |
| Satisfaction | 10% | Feedback | Latest satisfaction score (if any) |
| Consent health | 10% | Consent validity | Days until consent expiry |

### 9.2 Health Levels

| Level | Score | Label | Action |
|---|---|---|---|
| 🟢 | ≥ 80 | Excellent | No action needed |
| 🟡 | 60-79 | Normal | Standard follow-up cadence |
| 🟠 | 40-59 | To monitor | Increased follow-up frequency |
| 🔴 | < 40 | Critical | Escalation to LAWIM collaborator |

---

## 10. References

| Reference | File |
|---|---|
| Heritage Gold — Mise en Relation Lifecycle | `docs/lawim_heritage_gold/WORKFLOW_EXTRACTION_COMPLETE.md` §5 |
| Heritage Gold — State Machine Diagrams | `docs/lawim_heritage_gold/WORKFLOW_EXTRACTION_COMPLETE.md` §26 |
| Heritage Gold — SLA Tables | `docs/lawim_heritage_gold/WORKFLOW_EXTRACTION_COMPLETE.md` §24 |
| Heritage Gold — Dossier Lifecycle | `docs/lawim_heritage_gold/WORKFLOW_EXTRACTION_COMPLETE.md` §3 |
| Heritage Gold — NBA Rules | `docs/lawim_heritage_gold/WORKFLOW_EXTRACTION_COMPLETE.md` §20 |
| Heritage Gold — Health Scores | `docs/lawim_heritage_gold/WORKFLOW_EXTRACTION_COMPLETE.md` §23 |
| Relationship Execution Architecture | `docs/knowledge_execution/RELATIONSHIP_EXECUTION_ARCHITECTURE.md` |
| Consent Execution Contract | `docs/knowledge_execution/CONSENT_EXECUTION_CONTRACT.md` |
| Data Sharing Policy | `docs/knowledge_execution/DATA_SHARING_POLICY.md` |
| State Machine Catalog | `docs/knowledge_execution/STATE_MACHINE_CATALOG.md` |
| SLA Execution Model | `docs/knowledge_execution/SLA_EXECUTION_MODEL.md` |
