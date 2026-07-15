# STATE MACHINE CATALOG

**Domain:** Workflow and State Machine Architecture  
**Version:** 1.0  
**Source:** Heritage Gold Extraction — 21 workflows from 05-WORKFLOW-REFERENCE.md, 04-MATCHING-REFERENCE.md, 04-DECISION-ENGINE-REFERENCE.md, CRM_MODEL.md, 08-ROLE-REFERENCE.md

---

## Machine 01: Property Lifecycle

- **Entity:** `property`
- **Initial state:** `Création`
- **Terminal states:** `Archivé`
- **States:**

| State | Description |
|---|---|
| `Création` | Property record created, minimal fields populated |
| `Qualification` | Progressive enrichment of property details |
| `Validation` | Coherence, conformity, uniqueness, availability checks |
| `Publié` | Property published and visible on platform |
| `Disponible` | Actively available for matching |
| `Matching` | System computing compatible dossiers |
| `Visites` | Property is being visited by demandeurs |
| `Négociation` | Property under active negotiation |
| `Réservé` | Agreement in principle reached |
| `Transaction` | Sale/rental transaction in progress |
| `Indisponible` | Sold or rented (Vendu/Loué) |
| `Réactivation éventuelle` | Possible return to availability |
| `Archivé` | End of life, not modifiable, audit only |

- **Transitions:**

| From | To | Event | Guard | Action | Side Effect | Audit Event |
|---|---|---|---|---|---|---|
| `Création` | `Qualification` | `field_completion` | Required fields present | Update status | None | `property.qualified` |
| `Qualification` | `Validation` | `enrichment_complete` | Property Health Score calculated | Validate coherence | Score persisted | `property.validation_started` |
| `Validation` | `Publié` | `validation_success` | Coherence, conformity, uniqueness, availability checks pass | Publish listing | SIE publication workflow triggered | `property.published` |
| `Publié` | `Disponible` | `availability_declared` | Status explicitly set | Set status to Disponible | None | `property.available` |
| `Disponible` | `Matching` | `matching_triggered` | Dossier exists for matching | Compute scores | Match Count, Avg Score, Attractiveness Score calculated | `property.matching` |
| `Matching` | `Visites` | `demandeur_accepts` | Double consent obtained | Create visit record | Visit lifecycle initialized | `property.visit_scheduled` |
| `Visites` | `Négociation` | `positive_visit` | Visitor satisfaction recorded | Open negotiation channel | Negotiation lifecycle initialized | `property.negotiation_open` |
| `Négociation` | `Réservé` | `agreement_in_principle` | Price/terms agreed | Set status to Réservé | None | `property.reserved` |
| `Réservé` | `Transaction` | `finalization` | Sale/rental finalized | Set status | Transaction lifecycle initialized | `property.in_transaction` |
| `Transaction` | `Indisponible` | `sold_or_rented` | Transaction completed | Set status to Vendu/Loué | Payment tracking updated | `property.unavailable` |
| `Indisponible` | `Disponible` | `reactivation` | End of lease, cancellation, withdrawal of compromise | Set status to Disponible | Rematching triggered | `property.reactivated` |
| `Indisponible` | `Archivé` | `archival_request` | Owner request, obsolescence, archival rules reached | Archive entity | Remove from matching, retain for stats | `property.archived` |

- **SLA Rules:**

| State | Metric | Threshold | Action |
|---|---|---|---|
| `Disponible` | Time in state | Per property type (see SLA_EXECUTION_MODEL.md) | Diagnostic: price, photos, description, availability |
| `Création` | Time to qualification | 24h | Reminder to complete fields |
| `Indisponible` | Auto-archival | 90 days inactivity | Automatic archival |

- **NBA Consequences per State:**

| State | NBA |
|---|---|
| `Création` | Complete required fields |
| `Qualification` | Enrich property data, request photos |
| `Publié` | Confirm availability |
| `Disponible` | Suggest price reduction, recommend new photos, broaden matching, propose premium visibility |
| `Matching` | None (system computes) |
| `Visites` | Follow up after visit |
| `Négociation` | Support negotiation process |
| `Réservé` | Prepare transaction documents |
| `Transaction` | Track payment, verify identity |
| `Indisponible` | Propose reactivation if applicable |
| `Réactivation éventuelle` | Confirm availability status |
| `Archivé` | None (terminal) |

- **Escalation Rules:**

If a property remains in `Disponible` beyond the normal rotation duration for its type, the system automatically triggers a diagnostic analyzing: price, photo quality, description, real availability, owner activity, match count, visit count, refusal count. After diagnostic, NBA adjusts accordingly (price reduction suggestion, premium visibility proposal, or archival recommendation).

---

## Machine 02: Dossier/Case Lifecycle

- **Entity:** `dossier`
- **Initial state:** `Création`
- **Terminal states:** `Archivage`
- **States:**

| State | Description |
|---|---|
| `Création` | Dossier created when user expresses real estate need |
| `Qualification` | Progressive collection of criteria (never as a form) |
| `Matching` | Computing compatible properties |
| `Présentation` | Top matches presented to demandeur |
| `Attente décision demandeur` | Waiting for demandeur response |
| `Contact détenteur` | Establishing contact with holder |
| `Attente décision détenteur` | Waiting for holder response |
| `Mise en relation` | Double consent obtained, contact established |
| `Visite` | Visit underway |
| `Négociation` | Negotiation in progress |
| `Accord` | Agreement reached |
| `Transaction` | Transaction in progress |
| `Clôture` | Closing phase |
| `Archivage` | End of life |

- **Transitions:**

| From | To | Event | Guard | Action | Side Effect | Audit Event |
|---|---|---|---|---|---|---|
| `Création` | `Qualification` | `criteria_initiated` | Minimum fields present | Progressive criteria collection | NBA calculated | `dossier.qualifying` |
| `Qualification` | `Matching` | `critical_fields_known` | Type, budget, location known | Launch matching engine | Matching lifecycle starts | `dossier.matching` |
| `Matching` | `Présentation` | `match_complete` | Score >= 60% | Present top 5 properties | NBA = present property | `dossier.presented` |
| `Présentation` | `Attente décision demandeur` | `properties_presented` | Properties shown | Await demandeur choice | Follow-up timer set | `dossier.awaiting_decision` |
| `Attente décision demandeur` | `Contact détenteur` | `demandeur_interested` | Demandeur confirms interest | Contact holder | Holder silence workflow if no response | `dossier.contacting_holder` |
| `Attente décision demandeur` | `Matching` | `demandeur_refuses` | All presented refused | Rematch (exclude refused) | Learning from refusal | `dossier.rematching` |
| `Contact détenteur` | `Attente décision détenteur` | `holder_contacted` | Contact initiated | Await holder response | Follow-up timer set | `dossier.awaiting_holder` |
| `Attente décision détenteur` | `Mise en relation` | `double_consent` | Demandeur interested AND holder favorable | Establish contact, change interlocutor visibility | Interlocutor changes from 🤖 LAWIM AI to 👤 Holder | `dossier.contact_established` |
| `Attente décision détenteur` | `Matching` | `holder_refuses` | Holder refuses | Rematch | Holder refusal recorded | `dossier.rematching` |
| `Mise en relation` | `Visite` | `visit_scheduled` | Both parties agree on date | Schedule visit | Visit lifecycle starts, reminders set | `dossier.visit_scheduled` |
| `Visite` | `Négociation` | `positive_visit` | Visitor satisfied | Open negotiation | Negotiation lifecycle starts | `dossier.negotiating` |
| `Négociation` | `Accord` | `agreement_reached` | Final agreement | Document agreement | NBA = prepare transaction | `dossier.agreement` |
| `Accord` | `Transaction` | `transaction_initiated` | Parties confirm intention | Start transaction | Transaction lifecycle starts | `dossier.in_transaction` |
| `Transaction` | `Clôture` | `transaction_complete` | Transaction finalized | Close dossier | Satisfaction confirmation | `dossier.closed` |
| `Clôture` | `Archivage` | `archival_triggered` | Cleanup verified (no pending visits, negotiations, payments, incidents) | Archive | Remove from active workflows | `dossier.archived` |

- **SLA Rules:**

| State | Metric | Threshold | Action |
|---|---|---|---|
| `Matching` | Processing time | Immediate | None (system) |
| `Attente décision demandeur` | Response time | Based on urgency level | Follow-up reminder |
| `Attente décision détenteur` | Response time | Based on property type | Holder silence workflow |
| `Visite` | Realization | Until visit occurs | Automatic follow-up |
| Any non-terminal state | Significant event gap | Per property type SLA | Launch rematching, follow up party, propose adjustment, escalate to LAWIM collaborator |

- **NBA per State:**

| State | NBA |
|---|---|
| `Création` | Ask qualifying questions |
| `Qualification` | Complete critical fields |
| `Matching` | Launch matching |
| `Présentation` | Present properties |
| `Attente décision demandeur` | Wait for response / Follow up |
| `Contact détenteur` | Contact holder |
| `Attente décision détenteur` | Wait for response / Follow up |
| `Mise en relation` | Organize a visit |
| `Visite` | Register result / Propose negotiation |
| `Négociation` | Open negotiation / Follow up |
| `Accord` | Launch transaction |
| `Transaction` | Close dossier |
| `Clôture` | Close |
| `Archivage` | None (terminal) |

- **Escalation Rules:**

A dossier must never remain without a significant event beyond the applicable SLA. If exceeded, the system MUST: launch rematching, follow up a party, propose an adjustment, or escalate to a LAWIM collaborator.

- **Reopening Conditions:** New search, cancelled transaction, return of need.

---

## Machine 03: Matching Lifecycle

- **Entity:** `match`
- **Initial state:** `Load Dossier`
- **Terminal states:** `Learn & Recalculate`
- **States:**

| State | Description |
|---|---|
| `Load Dossier` | Load dossier criteria |
| `Check Critical Fields` | Verify mandatory fields present |
| `Select Compatible Properties` | Filter property pool |
| `Eliminate Incompatible` | Remove incompatible results |
| `Calculate Scores` | Score dimensions: Real Estate, Availability, Document, Holder Reliability, Transaction Success |
| `Rank Properties` | Sort by composite score |
| `Propose Best` | Present top results (max 5 first pass, max 10 V1) |
| `Wait for Decision` | Await demandeur response |
| `Learn` | Record acceptance/refusal, update model |
| `Recalculate if Necessary` | Adjust parameters and re-run if no acceptance |

- **Transitions:**

| From | To | Event | Guard | Action |
|---|---|---|---|---|
| `Load Dossier` | `Check Critical Fields` | `dossier_loaded` | Dossier exists | Verify field completeness |
| `Check Critical Fields` | `Select Compatible Properties` | `critical_fields_ok` | Type, budget, location, operation present | Query property pool |
| `Select Compatible Properties` | `Eliminate Incompatible` | `pool_selected` | Pool non-empty | Apply exclusion rules |
| `Eliminate Incompatible` | `Calculate Scores` | `incompatibles_removed` | Remaining properties > 0 | Score: RE(25/20/15/15/15/10) + Availability + Document + Holder |
| `Calculate Scores` | `Rank Properties` | `scores_calculated` | Scores computed | Sort descending, apply diversity rule |
| `Rank Properties` | `Propose Best` | `ranking_done` | Ranked list non-empty | Present (max 5) |
| `Propose Best` | `Wait for Decision` | `proposals_sent` | Properties presented | Await response |
| `Wait for Decision` | `Learn` | `decision_received` | Accept or refuse | Record outcome |
| `Learn` | `Recalculate if Necessary` | `learning_done` | Acceptance rate < threshold | Adjust weights, re-run |

- **SLA:** Immediate — matching is computed synchronously upon trigger.

- **Trigger Events:** Dossier creation, correction, budget modification, city change, property type change, new property publication, property becomes available, refusal, visit, failed negotiation.

- **NBA:** Matching itself IS the NBA for a dossier. Once matching completes, NBA transitions to `PRESENT_PROPERTY`.

---

## Machine 04: Mise en Relation / Contact Lifecycle

- **Entity:** `contact`
- **Initial state:** `Matching Complete`
- **Terminal states:** `Mise en relation established` / `Refused` / `Abandoned`
- **States:**

| State | Description |
|---|---|
| `Matching Complete` | Demandeur shown compatible properties |
| `Demandeur Interested` | Demandeur expresses interest in property |
| `Holder Contacted` | System contacts holder for permission |
| `Holder Decision` | Holder responds (accept/refuse/delay/alternative/unavailable) |
| `Double Consent Obtained` | Both parties agree to contact |
| `Mise en Relation Established` | Contact information shared, interlocutor changes |

- **Transitions:**

| From | To | Event | Guard | Action |
|---|---|---|---|---|
| `Matching Complete` | `Demandeur Interested` | `demandeur_confirms_interest` | Dossier active, property available | Record interest |
| `Demandeur Interested` | `Holder Contacted` | `interest_recorded` | None | Notify holder |
| `Holder Contacted` | `Holder Decision` | `holder_responds` | Response received within SLA | Process response |
| `Holder Decision` | `Double Consent Obtained` | `holder_accepts` | Holder favorable | Record double consent |
| `Double Consent Obtained` | `Mise en Relation Established` | `consent_confirmed` | Both consents valid | Share contact, change interlocutor |
| `Holder Decision` | `Matching` | `holder_refuses` | Holder refuses | Rematch, record reason |
| `Demandeur Interested` | `Matching` | `demandeur_abandons` | Demandeur changes mind | Rematch |

- **Guard:** Double consent is MANDATORY — demandeur interested AND holder favorable. No exceptions.

- **Holder Silence Escalation:**
  1. First reminder
  2. Second reminder
  3. Last reminder
  4. Property marked "to confirm"
  5. Rematching

- **SLA:** Holder response time based on property type (see SLA_EXECUTION_MODEL.md).

- **Interlocutor Shift:** After Mise en Relation, interlocutor changes from 🤖 LAWIM AI to 👤 Propriétaire/🏢 Agence/🤝 Introduceur.

---

## Machine 05: Visit Lifecycle

- **Entity:** `visit`
- **Initial state:** `Demandée`
- **Terminal states:** `Réalisée` / `Refusée` / `Annulée`
- **States:**

| State | Description |
|---|---|
| `Demandée` | Visit requested by demandeur |
| `En attente de confirmation` | Awaiting holder confirmation |
| `Confirmée` | Both parties confirmed |
| `Reportée` | Visit postponed to later date |
| `Réalisée` | Visit actually took place |
| `Refusée` | Holder refused visit |
| `Annulée` | Visit cancelled by either party |
| `Absence du demandeur` | Demandeur did not show |
| `Absence du détenteur` | Holder did not show |

- **Transitions:**

| From | To | Event | Guard | Action |
|---|---|---|---|---|
| `Demandée` | `En attente de confirmation` | `visit_requested` | Property available, dossier active | Notify holder |
| `En attente de confirmation` | `Confirmée` | `holder_confirms` | Holder accepts | Schedule, set reminders |
| `En attente de confirmation` | `Refusée` | `holder_refuses` | Holder declines | Record reason, propose alternatives |
| `Confirmée` | `Reportée` | `postponement_requested` | Valid reason | Reschedule |
| `Confirmée` | `Réalisée` | `visit_realized` | Visit occurred | Register result |
| `Confirmée` | `Annulée` | `cancellation` | Party cancels | Record reason, decrease reliability if applicable |
| `Confirmée` | `Absence du demandeur` | `demandeur_no_show` | Demandeur absent | Inform holder, propose new date |
| `Confirmée` | `Absence du détenteur` | `holder_no_show` | Holder absent | Inform demandeur, decrease holder reliability, propose alternatives |
| `Réalisée` | (terminal) | `satisfaction_recorded` | Result registered | NBA: open negotiation / second visit / propose another / rematch |

- **SLA:**

| Event | Timing |
|---|---|
| Reminder before visit | 24h before, 2h before |
| Configurable additional reminders | As configured |

- **NBA per Post-Visit Satisfaction:**

| Satisfaction | NBA |
|---|---|
| Très satisfait / Satisfait | Open negotiation |
| Mitigé | Schedule second visit |
| Insatisfait | Propose another property / Launch rematching |

- **Indicators:** Time before first visit, confirmation rate, cancellation rate, absence rate, satisfaction rate, transformation rate to negotiation.

---

## Machine 06: Negotiation Lifecycle

- **Entity:** `negotiation`
- **Initial state:** `Ouverte`
- **Terminal states:** `Transaction` / `Échec`
- **States:**

| State | Description |
|---|---|
| `Ouverte` | Negotiation channel opened |
| `En discussion` | Active exchange between parties |
| `Offre` | Formal offer submitted |
| `Contre-offre` | Counter-offer submitted |
| `Accord de principe` | Agreement in principle on key terms |
| `Accord final` | Final agreement documented |
| `Transaction` | Moves to transaction workflow |
| `Échec` | Negotiation failed |

- **Transitions:**

| From | To | Event | Guard | Action |
|---|---|---|---|---|
| `Ouverte` | `En discussion` | `discussion_started` | Both parties present | Open channel |
| `En discussion` | `Offre` | `offer_made` | Valid offer (amount, terms) | Register offer |
| `Offre` | `Contre-offre` | `counter_offer_made` | Valid counter-offer | Register counter-offer |
| `Contre-offre` | `Offre` | `new_offer` | Iteration continues | Register new offer |
| `Contre-offre` | `Accord de principe` | `agreement_in_principle` | Key terms agreed | Document terms |
| `Accord de principe` | `Accord final` | `final_agreement` | All terms finalized | Document final agreement |
| `Accord final` | `Transaction` | `transaction_initiated` | Both parties confirm | Launch transaction lifecycle |
| Any | `Échec` | `negotiation_failed` | Max delay, party withdrawal, property unavailable, parties end exchanges | Diagnostic, rematch |

- **Negotiable Elements:**
  - **Sale:** Price, payment terms, deadlines, included furniture, equipment, release date
  - **Rental:** Rent, deposit, advance, lease duration, entry date, possible works
  - **Land:** Price, boundary marking, documents, deadlines
  - **Commercial:** Rent, key money, equipment, duration

- **Silence Escalation:**
  1. First reminder
  2. Second reminder
  3. Last reminder
  4. Automatic closure of negotiation
  5. Possible rematching

- **SLA:** Follow-up intervals: J1, J7, J30, J90 (from NEGO-011).

- **Indicators:** Average duration, number of offers, number of counter-offers, agreement rate, failure rate, average gap between initial and final price.

---

## Machine 07: Transaction Lifecycle

- **Entity:** `transaction`
- **Initial state:** `Accord`
- **Terminal states:** `Transaction terminée` / `Échec`
- **States:**

| State | Description |
|---|---|
| `Accord` | Agreement documented, transaction ready |
| `Préparation` | Document preparation phase |
| `Documents` | Document collection and verification |
| `Paiement` | Payment processing |
| `Signature` | Contract signing |
| `Remise des clés` | Key handover |
| `Confirmation` | Post-transaction confirmation |
| `Transaction terminée` | Transaction completed |
| `Archivage` | Archival of transaction records |
| `Échec` | Transaction failed |

- **Transitions:**

| From | To | Event | Guard | Action |
|---|---|---|---|---|
| `Accord` | `Préparation` | `transaction_kickoff` | Agreement exists, property available, parties confirm | Start prep |
| `Préparation` | `Documents` | `documents_ready` | Documents collected | Verify documents |
| `Documents` | `Paiement` | `documents_verified` | All docs valid | Initiate payment flow |
| `Paiement` | `Signature` | `payment_confirmed` | Payment successful | Schedule signing |
| `Signature` | `Remise des clés` | `signature_complete` | All signatures obtained | Schedule handover |
| `Remise des clés` | `Confirmation` | `keys_handed` | Keys transferred | Send satisfaction survey |
| `Confirmation` | `Transaction terminée` | `satisfaction_confirmed` | Both parties satisfied | Update stats, improve reliability scores |
| `Transaction terminée` | `Archivage` | `archival_triggered` | Post-transaction follow-up complete | Archive |
| Any | `Échec` | `transaction_failed` | Payment abandoned, docs impossible, party withdrawal | Rollback, return to negotiation |

- **Transaction Types:** Location (Rental), Vente (Sale), Achat (Purchase), Bail professionnel, Bail commercial, Location saisonnière.

- **Document Requirements:**
  - **Sale:** Land title, ID, power of attorney
  - **Rental:** Contract, deposit, inventory of fixtures

- **Post-Transaction:** Satisfaction confirmation, remaining commitments follow-up, statistics update, reliability score improvement.

---

## Machine 08: Paid Services & Payment Lifecycle

- **Entity:** `paid_service`
- **Initial state:** `Création`
- **Terminal states:** `Archivage` / `Expiration`
- **Service states:**

| State | Description |
|---|---|
| `Création` | Service record created |
| `Proposition` | Service offered to user |
| `Acceptation` | User accepts service |
| `Paiement` | Payment in progress |
| `Activation` | Service activated after payment |
| `Utilisation` | Service being delivered |
| `Expiration` | Service period ended |
| `Archivage` | Service record archived |

- **Payment sub-states (10 states):**

| State | Description |
|---|---|
| `PAYMENT_CREATED` | Payment record created |
| `PAYMENT_INITIATED` | Payment session initiated |
| `PAYMENT_PENDING` | Awaiting confirmation |
| `PAYMENT_CONFIRMED` | Payment received |
| `PAYMENT_FAILED` | Payment declined/error |
| `PAYMENT_CANCELLED` | Payment cancelled |
| `PAYMENT_EXPIRED` | Payment session expired |
| `PAYMENT_REFUNDED` | Payment returned |
| `PAYMENT_RECONCILED` | Payment reconciled with ledger |
| `PAYMENT_DISPUTED` | Payment contested |

- **Transitions (Service):**

| From | To | Event | Guard | Action |
|---|---|---|---|---|
| `Création` | `Proposition` | `service_offered` | User eligible | Present service details |
| `Proposition` | `Acceptation` | `user_accepts` | Terms accepted | Create payment session |
| `Acceptation` | `Paiement` | `payment_initiated` | Payment session created | Await payment confirmation |
| `Paiement` | `Activation` | `payment.success` | Payment confirmed | Activate service (e.g., boost listing, unlock contact) |
| `Paiement` | `Paiement` | `payment.failed` | Retry allowed | Notify user, offer retry |
| `Activation` | `Utilisation` | `service_started` | Service active | Track usage |
| `Utilisation` | `Expiration` | `service_period_end` | Duration elapsed | Deactivate, archive |
| `Expiration` | `Archivage` | `archival_triggered` | Cleanup done | Archive |

- **13 Monetized Services:** See Heritage Gold section 9 for complete list with prices (Boost, Premium, Agent Pro/Business, Leads, Diaspora packages, etc.)

- **Key Rule:** LAWIM never deducts a percentage from transactions — revenue comes exclusively from platform services.

---

## Machine 09: Disputes, Claims & Incidents Lifecycle

- **Entity:** `incident`
- **Initial state:** `Signalement`
- **Terminal states:** `Archivage`
- **Priority Levels:**
  - 🔴 Critique — Immediate handling
  - 🟠 Élevée — < 24 hours
  - 🟡 Normale — < 72 hours
  - 🟢 Faible — According to support availability

- **States:**

| State | Description |
|---|---|
| `Signalement` | Incident reported |
| `Qualification` | Incident categorized and prioritized |
| `Analyse` | Root cause analysis |
| `Collecte des informations` | Evidence gathering |
| `Décision` | Resolution decision made |
| `Résolution` | Remediation actions executed |
| `Clôture` | Incident closed |
| `Archivage` | Record archived |

- **Transitions:**

| From | To | Event | Guard | Action |
|---|---|---|---|---|
| `Signalement` | `Qualification` | `incident_reported` | Valid report | Set priority, categorize |
| `Qualification` | `Analyse` | `qualified` | Category determined | Begin analysis |
| `Analyse` | `Collecte des informations` | `analysis_begun` | Analysis scope defined | Gather evidence |
| `Collecte des informations` | `Décision` | `info_collected` | Sufficient evidence | Decide resolution |
| `Décision` | `Résolution` | `decision_made` | Valid decision | Execute remediation |
| `Résolution` | `Clôture` | `remediated` | Resolution confirmed | Close incident |
| `Clôture` | `Archivage` | `archival_triggered` | Retention period met | Archive |
| Any | `Clôture` | `dismissed` | No action needed | Close without resolution |

- **Incident Types:** Property unavailable, inaccurate info, visit cancellation, participant absence, post-visit disagreement, non-respect of commitment, contested payment, inappropriate behavior, identity theft, presumed fraud, fake documents, platform abuse.

- **Fraud Actions:** Temporarily suspend account/property/listing/contact (all motivated, historized, reversible after verification).

- **User Actions:** Send warning, request supporting docs, limit functionality, temporarily suspend, forward to administrator.

- **SLA by Priority:**

| Priority | SLA |
|---|---|
| 🔴 Critique | Immediate |
| 🟠 Élevée | < 24h |
| 🟡 Normale | < 72h |
| 🟢 Faible | Per support availability |

---

## Machine 10: Closure, Archiving & Retention Lifecycle

- **Entity:** `archived_object`
- **Initial state:** `Active`
- **Terminal states:** `Long-term archiving`
- **Principle:** No business data is ever deleted in LAWIM.

- **States:**

| State | Description |
|---|---|
| `Active` | Entity is active and modifiable |
| `Closed` | Entity closed (objective achieved, abandoned, or admin decision) |
| `Archived (Operational)` | Not modifiable, not in active workflows, available for audit/statistics/reporting/learning |
| `Long-term Archiving` | Same as archived, removed from matching; reactivation only via authorized admin procedure |

- **Transitions:**

| From | To | Event | Guard | Action |
|---|---|---|---|---|
| `Active` | `Closed` | `closure_requested` | Objective achieved, abandoned, or admin decision; no pending visits/negotiations/payments/incidents | Close entity |
| `Closed` | `Archived (Operational)` | `archival_requested` | Closure verified | Archive, retain for audit/stats/learning |
| `Archived (Operational)` | `Long-term Archiving` | `time_elapsed_3_years` | 3 years since archival | Move to long-term, remove from matching |

- **Objects Concerned:** Dossiers, properties, conversations, visits, negotiations, transactions, service payments, incidents, notifications, workflows.

- **Reopening:** Cancelled sale, end of lease, new request, administrative decision.

---

## Machine 11: Mediation Workflow

- **Entity:** `mediation`
- **Initial state:** `Incident Reported`
- **Terminal states:** `Clôture` (amicable agreement, disagreement, abandonment, or referral)
- **States:**

| State | Description |
|---|---|
| `Incident` | Incident identified as requiring mediation |
| `Proposition de médiation` | Mediation proposed to all parties |
| `Acceptation des parties` | All parties agree to mediation |
| `Nomination du Médiateur LAWIM` | Mediator assigned |
| `Échanges` | Facilitated dialogue |
| `Proposition de solution` | Mediator proposes solution |
| `Acceptation` | Solution accepted |
| `Clôture` | Mediation closed |

- **Transitions:**

| From | To | Event | Guard | Action |
|---|---|---|---|---|
| `Incident` | `Proposition de médiation` | `mediation_recommended` | Suitable for mediation | Contact parties |
| `Proposition de médiation` | `Acceptation des parties` | `all_parties_accept` | All parties agree | Proceed to nomination |
| `Acceptation des parties` | `Nomination du Médiateur LAWIM` | `mediator_assigned` | Qualified mediator available | Assign mediator |
| `Nomination du Médiateur LAWIM` | `Échanges` | `mediation_started` | Parties ready | Facilitate exchange |
| `Échanges` | `Proposition de solution` | `solution_proposed` | Sufficient exchange | Document proposal |
| `Proposition de solution` | `Acceptation` | `solution_accepted` | All parties agree | Record agreement |
| `Proposition de solution` | `Clôture` | `solution_refused` | Party refuses | Close, refer if needed |
| `Proposition de médiation` | `Clôture` | `mediation_declined` | Party declines | Close incident |

- **Mediator Role:** Listen, facilitate, explain procedures, seek amicable solution, document exchanges.
  NEVER: impose decision, represent a party, modify dossier history, render legal judgment.

- **Possible Endings:** Amicable agreement, disagreement, abandonment, referral to competent authority.

---

## Machine 12: User Identity Lifecycle

- **Entity:** `user`
- **Initial state:** `NEW_USER`
- **Terminal states:** `INACTIVE`
- **States:**

| State | Description |
|---|---|
| `NEW_USER` | Account created, minimal fields |
| `SEARCHING_PROPERTY` | Demandeur actively searching |
| `PROPERTY_OWNER` | User owns listed property |
| `AGENT` | Registered real estate agent |
| `PREMIUM_AGENT` | Agent with active subscription |
| `LEAD_CREATED` | Qualified lead generated from user |
| `INACTIVE` | User inactive (can reactivate) |

- **Transitions:**

| From | To | Event | Guard | Action |
|---|---|---|---|---|
| `NEW_USER` | `SEARCHING_PROPERTY` | `intent_to_search` | Minimum fields complete | Create dossier |
| `NEW_USER` | `PROPERTY_OWNER` | `property_registered` | Valid property | Onboard as owner |
| `NEW_USER` | `AGENT` | `agent_registration` | Professional docs validated | Create agent profile |
| `NEW_USER` | `INACTIVE` | `inactivity_timeout` | No activity for threshold | Mark inactive |
| `SEARCHING_PROPERTY` | `LEAD_CREATED` | `lead_qualified` | Lead score >= threshold | Route to CRM |
| `SEARCHING_PROPERTY` | `INACTIVE` | `inactivity_timeout` | No activity | Mark inactive |
| `PROPERTY_OWNER` | `LEAD_CREATED` | `lead_qualified` | Lead score >= threshold | Route to CRM |
| `PROPERTY_OWNER` | `INACTIVE` | `inactivity_timeout` | No activity | Mark inactive |
| `AGENT` | `PREMIUM_AGENT` | `subscription_activated` | Payment successful | Upgrade features |
| `AGENT` | `INACTIVE` | `inactivity_timeout` | No activity | Mark inactive |
| `PREMIUM_AGENT` | `AGENT` | `subscription_expired` | Subscription period ends | Downgrade features |
| `INACTIVE` | `NEW_USER` | `reactivation` | User returns | Restore account |

- **Registration Minimum Fields:** Full name, unique email, unique username, WhatsApp number (mandatory), password + confirmation, preferred language, terms acceptance.

- **Identity Verification Documents:** National ID Card (CNI), Passport, Residence permit.

- **Trust Score Levels (6):** New account → Phone verified → Identity verified → Professional docs validated → Verified professional/partner → Reference account.

- **Automatic Evolution Paths:**
  - Demandeur → Publication of property → Propriétaire
  - Demandeur → Property management declaration → Détenteur
  - Détenteur → Professional validation → Agent immobilier
  - Agent → Creation of validated agency → Responsable d'agence

---

## Machine 13: Organization/Agency Lifecycle

- **Entity:** `organization`
- **Initial state:** `Demande`
- **Terminal states:** `Organisation active` / `Dissoute`
- **States:**

| State | Description |
|---|---|
| `Demande` | Agency creation request submitted |
| `Saisie des informations` | Information entry phase |
| `Téléversement des justificatifs` | Document upload |
| `Contrôle automatique` | Automated verification |
| `Contrôle LAWIM` | Manual LAWIM review |
| `Validation` | Agency validated |
| `Organisation active` | Fully operational agency |
| `Dissoute` | Agency dissolved |

- **Transitions:**

| From | To | Event | Guard | Action |
|---|---|---|---|---|
| `Demande` | `Saisie des informations` | `request_submitted` | Valid request | Enable info entry |
| `Saisie des informations` | `Téléversement des justificatifs` | `info_complete` | All fields filled | Enable document upload |
| `Téléversement des justificatifs` | `Contrôle automatique` | `docs_uploaded` | Required docs present | Auto-verify |
| `Contrôle automatique` | `Contrôle LAWIM` | `auto_check_passed` | Auto-checks pass | Queue for manual review |
| `Contrôle automatique` | `Saisie des informations` | `auto_check_failed` | Issues found | Request corrections |
| `Contrôle LAWIM` | `Validation` | `manual_approval` | LAWIM approves | Grant agency status |
| `Contrôle LAWIM` | `Saisie des informations` | `manual_rejection` | Issues found | Request corrections |
| `Validation` | `Organisation active` | `activation` | Minimum effective (3 agents) | Activate agency |

- **Minimum Requirements:** CNI of responsible person, verified phone number, email, physical address. Optional: RCCM, tax ID, business license, logo, headquarters proof.

- **Minimum Effective:** 3 active agents for "fully operational" status.

- **Dissolution Checks:** Open dossiers, managed properties, services in progress, payments, legal obligations.

---

## Machine 14: Agent Invitation Workflow

- **Entity:** `agent_invitation`
- **Initial state:** `Invitation`
- **Terminal states:** `Agent actif`
- **States:**

| State | Description |
|---|---|
| `Invitation` | Invitation sent to prospective agent |
| `Secure Link` | Secure registration link generated |
| `Account Creation` | Agent creates account |
| `Phone Verified` | Phone number confirmed |
| `CNI Uploaded` | Identity document uploaded |
| `LAWIM Validation` | LAWIM reviews and validates |
| `Agent actif` | Agent fully onboarded |

- **Transitions:**

| From | To | Event | Guard | Action |
|---|---|---|---|---|
| `Invitation` | `Secure Link` | `invitation_sent` | Valid email/phone | Generate secure link |
| `Secure Link` | `Account Creation` | `link_clicked` | Link valid, not expired | Create account |
| `Account Creation` | `Phone Verified` | `phone_confirmed` | OTP validated | Confirm phone |
| `Phone Verified` | `CNI Uploaded` | `cni_submitted` | Valid ID document | Verify document |
| `CNI Uploaded` | `LAWIM Validation` | `cni_verified` | Auto-checks pass | Queue for LAWIM |
| `LAWIM Validation` | `Agent actif` | `manual_approval` | LAWIM approves | Activate agent |

- **Member Departure:** Remove org permissions, keep personal history and audit traces, transfer open dossiers per defined rules, user account remains active.

---

## Machine 15: Publication (SIE-Enriched)

- **Entity:** `publication`
- **Initial state:** `Création de la publication`
- **Terminal states:** `Disponibilité des dashboards`
- **States:**

| State | Description |
|---|---|
| `Création de la publication` | Publication record created |
| `Validation` | Content validated |
| `Génération Reference Code` | SIE reference code assigned |
| `Association Campagne` | Linked to campaign if applicable |
| `Association Acteur` | Linked to actor (agent/owner) |
| `Association Biens` | Linked to properties |
| `Association Services` | Linked to services (optional) |
| `Publication sur le canal` | Published to channel |
| `Journalisation` | Logging completed |
| `Mise à jour des statistiques` | Analytics updated |
| `Disponibilité des dashboards` | Available in reporting |

- **Transitions:** Strictly sequential through all states.

- **SIE Integration:** Reference code generation is a SIE (System d'Information Externalisé) call.

---

## Machine 16: Redirection (SIE-Enriched)

- **Entity:** `redirection`
- **Initial state:** `Utilisateur`
- **Terminal states:** `Événement envoyé au Continuous Learning`
- **States:**

| State | Description |
|---|---|
| `Utilisateur` | User initiates action |
| `Clic sur le lien` | Link clicked |
| `Validation du Reference Code` | Reference code validated |
| `Contrôle d'intégrité` | Integrity check |
| `Détection bot` | Bot detection |
| `Détection doublon` | Duplicate detection |
| `Journalisation` | Logging |
| `Création éventuelle d'une session` | Session creation if needed |
| `Redirection` | User redirected |
| `Mise à jour des statistiques` | Stats updated |
| `Événement envoyé au Reporting` | Event sent to reporting |
| `Événement envoyé au Continuous Learning` | Event sent to learning system |

- **Transitions:** Strictly sequential.

---

## Machine 17: Conversion & Attribution (SIE-Enriched)

- **Entity:** `conversion`
- **Initial state:** `Publication`
- **Terminal states:** `Historisation`
- **States:**

| State | Description |
|---|---|
| `Publication` | Content published |
| `Clic` | User clicks |
| `Redirection` | User redirected to LAWIM |
| `Visite` | User browses platform |
| `Création éventuelle du compte` | Account creation |
| `Conversation` | User engages in conversation |
| `Matching` | Matching initiated |
| `Visite terrain` | Physical visit |
| `Service LAWIM` | Paid service used |
| `Paiement Campay confirmé` | Payment confirmed via Campay |
| `Conversion` | Conversion registered |
| `Historisation` | Conversion recorded for analytics |

- **Transitions:** Strictly sequential — represents the full attribution pipeline from ad click to revenue.

- **Attribution Model:** Last-touch (final conversion step before Historisation is the attributed source).

---

## Machine 18: CRM Pipeline (8 Stages)

- **Entity:** `lead`
- **Initial state:** `incoming_message`
- **Terminal states:** `crm_routing`
- **States (Stages):**

| Stage | Input | Processing | Output |
|---|---|---|---|
| `1. incoming_message` | Raw WhatsApp/Telegram message | Reception and formatting | Normalized message |
| `2. normalize_text` | Normalized message | Orthographic normalization, typo, slang correction | Cleaned text |
| `3. extract_entities` | Cleaned text | Entity extraction (budget, city, type, phone) | Structured entities |
| `4. detect_intent` | Entities + text | Intent classification (buy/rent/sell/invest) | Intent + confidence |
| `5. context_enrichment` | Intent + entities | History, profile, behavior enrichment | Full context |
| `6. lead_scoring` | Full context | Score = base + boosters - penalties | Numeric score |
| `7. lead_classification` | Numeric score | HOT(>=80)/WARM(>=60)/COLD(>=40)/LOW(<40)/SPAM | Class + priority |
| `8. crm_routing` | Class + priority | Route to agent, dashboard, or auto-response | CRM action |

- **Lead Types with Base Scores:** tenant(40), buyer(60), seller(50), investor(80), diaspora_investor(95).

- **Score Boosters:** Budget detected(+15), City detected(+10), Neighborhood(+10), Urgency(+20), Diaspora(+25), Cash purchase(+15), etc.

- **Score Penalties:** Missing budget(-10), Unclear location(-10), Spam-like(-50), Too short(-20), External links(-30), etc.

- **SLA by Priority:**

| Priority | Types | SLA |
|---|---|---|
| P0 | diaspora_investor, buyer > 50M FCFA | < 30 min |
| P1 | seller, land_buyer | < 2h |
| P2 | standard buyer, standard investor | < 24h |
| P3 | tenant, non-qualified prospect | J+1 to J+7 |

- **Classification SLAs:**

| Class | Delay | Action |
|---|---|---|
| HOT | < 1h | call_immediately (Phone + WhatsApp) |
| WARM | < 24h | send_listings (WhatsApp) |
| COLD | < 48h | request_budget (WhatsApp) |
| LOW | J+7 / J+30 / J+90 | follow_up (WhatsApp) |
| SPAM | Immediate | ignore + block if persistent |

---

## Machine 19: Agent Opt-In Workflow

- **Entity:** `agent_opt_in`
- **Initial state:** `Detection`
- **Terminal states:** `Sharing Active`
- **Source:** CRM_MODEL.md — Sec 11

- **States:**

| State | Description |
|---|---|
| `Detection` | System detects agent from message patterns (e.g., "je suis agent") |
| `Opt-In Request` | System asks "Voulez-vous recevoir des leads?" |
| `Opt-In Response Logged` | Agent accepts/declines |
| `Sharing Active` | Lead sharing activated for this agent |

- **Transitions:**

| From | To | Event | Guard | Action |
|---|---|---|---|---|
| `Detection` | `Opt-In Request` | `agent_pattern_detected` | Confidence > threshold | Send opt-in message |
| `Opt-In Request` | `Opt-In Response Logged` | `agent_responds` | Valid response | Record preference |
| `Opt-In Response Logged` | `Sharing Active` | `agent_accepted` | Acceptance | Start lead routing |

- **4 Steps:** Detection → Request → Log → Share.

---

## Machine 20: Identity Resolution Workflow

- **Entity:** `identity_resolution`
- **Initial state:** `Potential Match Detected`
- **Terminal states:** `Merged` / `False Positive Discarded`
- **Source:** CRM_MODEL.md — Sec 8

- **States:**

| State | Description |
|---|---|
| `Potential Match Detected` | System identifies possible duplicate user |
| `Confidence Evaluation` | Score match based on phone, email, name, device |
| `Human Review (if needed)` | Manual review for medium confidence |
| `Merged` | Identities consolidated |
| `False Positive Discarded` | Match rejected |

- **Transitions:**

| From | To | Event | Guard | Action |
|---|---|---|---|---|
| `Potential Match Detected` | `Confidence Evaluation` | `match_candidate` | Match found | Score similarity |
| `Confidence Evaluation` | `Merged` | `high_confidence` | Score > threshold | Merge records, keep audit |
| `Confidence Evaluation` | `Human Review` | `medium_confidence` | Score in gray zone | Flag for manual review |
| `Confidence Evaluation` | `False Positive Discarded` | `low_confidence` | Score < threshold | Discard, log |
| `Human Review` | `Merged` | `manual_merge` | Reviewer confirms | Merge |
| `Human Review` | `False Positive Discarded` | `manual_reject` | Reviewer rejects | Discard |

---

## Machine 21: Main Cross-Cutting Workflow

- **Entity:** `real_estate_project`
- **Initial state:** `Projet immobilier`
- **Terminal states:** `Archivage`
- **This is the top-level orchestrator** that spans the entire client journey from initial need to archival. It does NOT execute business logic itself — it delegates to sub-workflows.

- **States:**

| Stage | Description | Sub-Workflow Delegated |
|---|---|---|
| `Projet immobilier` | Real estate project identified | None |
| `Création du dossier` | Dossier created | Dossier Lifecycle |
| `Qualification` | Needs qualified | Dossier Lifecycle |
| `Matching` | Properties matched | Matching Lifecycle |
| `Mise en relation` | Contact established | Contact Lifecycle |
| `Visite` | Property visited | Visit Lifecycle |
| `Négociation` | Deal negotiated | Negotiation Lifecycle |
| `Transaction` | Transaction executed | Transaction Lifecycle |
| `Clôture` | Project closed | Closure workflow |
| `Archivage` | Project archived | Archiving workflow |

- **Transitions:**

| From | To | Event | Delegated To |
|---|---|---|---|
| `Projet immobilier` | `Création du dossier` | `need_expressed` | Dossier Lifecycle |
| `Création du dossier` | `Qualification` | `dossier.created` | Dossier Lifecycle |
| `Qualification` | `Matching` | `dossier.qualified` | Matching Lifecycle |
| `Matching` | `Mise en relation` | `match.accepted` | Contact Lifecycle |
| `Mise en relation` | `Visite` | `contact.established` | Visit Lifecycle |
| `Visite` | `Négociation` | `visit.positive` | Negotiation Lifecycle |
| `Négociation` | `Transaction` | `negotiation.agreement` | Transaction Lifecycle |
| `Transaction` | `Clôture` | `transaction.complete` | Closure |
| `Clôture` | `Archivage` | `closure.verified` | Archiving |

- **States run in parallel:** Visit, Negotiation, Transaction can all have active sub-workflows simultaneously.
- **If any sub-workflow enters a failure terminal,** the cross-cutting workflow can either retry, skip to rematching, or close depending on failure type.

---

## Machine Index

| # | Machine | Entity | States | Initial | Terminal |
|---|---|---|---|---|---|
| 01 | Property Lifecycle | property | 13 | Création | Archivé |
| 02 | Dossier/Case Lifecycle | dossier | 14 | Création | Archivage |
| 03 | Matching Lifecycle | match | 10 | Load Dossier | Learn & Recalculate |
| 04 | Mise en Relation / Contact | contact | 6 | Matching Complete | Established / Refused |
| 05 | Visit Lifecycle | visit | 9 | Demandée | Réalisée / Refusée / Annulée |
| 06 | Negotiation Lifecycle | negotiation | 8 | Ouverte | Transaction / Échec |
| 07 | Transaction Lifecycle | transaction | 10 | Accord | Terminée / Échec |
| 08 | Paid Services & Payment | paid_service | 8 + 10 payment sub-states | Création | Archivage / Expiration |
| 09 | Disputes, Claims & Incidents | incident | 8 | Signalement | Archivage |
| 10 | Closure, Archiving & Retention | archived_object | 4 | Active | Long-term Archiving |
| 11 | Mediation Workflow | mediation | 8 | Incident | Clôture |
| 12 | User Identity Lifecycle | user | 7 | NEW_USER | INACTIVE |
| 13 | Organization/Agency Lifecycle | organization | 8 | Demande | Active / Dissoute |
| 14 | Agent Invitation | agent_invitation | 7 | Invitation | Agent actif |
| 15 | Publication (SIE) | publication | 11 | Création | Dashboards |
| 16 | Redirection (SIE) | redirection | 12 | Utilisateur | Continuous Learning |
| 17 | Conversion & Attribution | conversion | 12 | Publication | Historisation |
| 18 | CRM Pipeline | lead | 8 | incoming_message | crm_routing |
| 19 | Agent Opt-In | agent_opt_in | 4 | Detection | Sharing Active |
| 20 | Identity Resolution | identity_resolution | 5 | Potential Match Detected | Merged / Discarded |
| 21 | Main Cross-cutting Workflow | real_estate_project | 9 | Projet immobilier | Archivage |

**Total: 21 machines, ~175+ states** (including payment sub-states and visit statuses).
