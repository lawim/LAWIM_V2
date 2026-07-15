# Commercial Execution Architecture

**Component of:** Knowledge Execution Architecture (H1)
**Domain:** Negotiation — Commercial Knowledge Consumption
**Date:** 2026-07-15
**Status:** CANONICAL
**Prerequisite:** Heritage Gold NEGOTIATION_MODEL.md, RULE_INDEX.md (NEGO-001 to NEGO-014)

---

## 1. Commercial Knowledge Consumption Model

Commercial knowledge from Heritage Gold is consumed at runtime by the **Negotiation Engine**, **Conversation Engine**, and **Decision Engine** through a layered pipeline.

```
Heritage Gold (NEGOTIATION_MODEL.md, RULE_INDEX.md, SALES_PLAYBOOK)
        │
        ▼
Commercial Knowledge Registry (indexed NEGO rules, scripts, strategies)
        │
        ▼
Context Interpreter (lead profile, state, channel, language, urgency)
        │
        ▼
Strategy Selector (script, argument set, tone, closing technique)
        │
        ▼
Message Composer (template selection, personalization, NBA binding)
        │
        ▼
Channel Executor (WhatsApp, Telegram, Dashboard)
        │
        ▼
Audit Trail (decision trace, NEGO rule reference, outcome)
```

---

## 2. Commercial Action Types

The architecture distinguishes 10 commercial actions. Each maps to specific NEGO rules and engine behaviors.

| Action | Code | Description | NEGO Reference |
|--------|------|-------------|----------------|
| **Qualification commerciale** | `QUAL_COM` | Identify buyer/seller profile, budget, intent, urgency | NEGO-001, NEGO-002 |
| **Rassurance** | `RASSUR` | Address fears with proof, documents, transparency | NEGO-003, NEGO-004 |
| **Objection** | `OBJECT` | Handle 23 objection patterns with prescribed responses | NEGO-005, NEGO-006 |
| **Argumentation** | `ARGUE` | Deploy LAWIM arguments and property arguments | NEGO-005, NEGO-006 |
| **Négociation** | `NEGO` | Execute price negotiation strategy per profile | NEGO-008, NEGO-012 |
| **Relance** | `RELANCE` | Trigger follow-up at J1/J7/J30/J90 cadence | NEGO-011 |
| **Closing** | `CLOSING` | Execute 5-step trust sequence or visit-based closing | NEGO-010 |
| **Visite** | `VISIT` | Organize physical or video visit, post-visit follow-up | — (Workflow) |
| **Mise en relation** | `MER` | Double-consent contact between demandeur and holder | — (Workflow) |
| **Diaspora engagement** | `DIASP` | Execute 7-step diaspora trust journey | NEGO-014 |

### 2.1 Mise en Relation (Connection)

```
Matching → Demandeur interested → Holder contacted → Double consent → Connection
```

- Requires both parties to consent before coordinates are shared
- Never transmit holder data without explicit acceptance
- LAWIM AI remains the visible intermediary until connection is established

### 2.2 Buyer/Seller Roles

| Role | Code | Commercial Action Path |
|------|------|----------------------|
| Buyer | `ACHETEUR` | QUAL_COM → ARGUE → VISIT → NEGO → CLOSING |
| Seller | `VENDEUR` | QUAL_COM → ARGUE → MER → NEGO → CLOSING |
| Tenant | `LOCATAIRE` | QUAL_COM → VISIT → NEGO → CLOSING |
| Landlord | `BAILLEUR` | QUAL_COM → ARGUE → MER → NEGO → CLOSING |
| Professional | `PROFESSIONNEL` | QUAL_COM → ARGUE → VISIT → NEGO → CLOSING |

---

> **HUMAN_VALIDATION_REQUIRED:** Commercial scripts (especially objection handling, negotiation, and closing) must be validated by business stakeholders before deployment. Script content influences user trust and regulatory compliance.

## 3. NEGO Rules Consumption

All 14 NEGO rules are consumed by the commercial execution layer.

### 3.1 Buyer & Seller Profiles (NEGO-001, NEGO-002)

| Rule | Consumed By | Consumption Mechanism |
|------|-------------|----------------------|
| NEGO-001 (4 buyer profiles) | Qualification Engine, Negotiation Engine | Profile detector maps lead intent+behavior to `NATIONAL`, `DIASPORA`, `INVESTOR`, `YOUNG_PROFESSIONAL` |
| NEGO-002 (3 seller profiles) | Qualification Engine, Negotiation Engine | Profile detector maps seller type to `INDIVIDUAL`, `DEVELOPER`, `LANDLORD` |

**4 Buyer Profiles:**

| Profile | Characteristics | Primary Argument | Tone |
|---------|----------------|-----------------|------|
| **National** | Local buyer, price-sensitive, family involvement | Proximity, accessibility | Patient, pédagogique |
| **Diaspora** | Remote buyer, security-first, proof-driven | Zero commission, accompagnement, verified agents | Structured, transparent |
| **Investor** | ROI-focused, portfolio-building, data-driven | Rentabilité, matching intelligent, mise en relation | Technical, chiffré |
| **Young Professional** | First-time buyer, budget-conscious, digital-native | WhatsApp, zero commission, accompagnement | Encouraging, pédagogique |

**3 Seller Profiles:**

| Profile | Characteristics | Primary Argument | Tone |
|---------|----------------|-----------------|------|
| **Individual** | One property, emotional attachment, trust-sensitive | Mise en relation, réseau agents vérifiés | Patient, rassurant |
| **Developer** | Multiple properties, volume-driven, speed-focused | Matching intelligent, zero commission | Professional, efficient |
| **Landlord** | Rental income, tenant quality, management | Accompagnement, mise en relation | Expert, rentabilité |

### 3.2 Fear Management (NEGO-003, NEGO-004)

| Rule | Consumed By | Consumption Mechanism |
|------|-------------|----------------------|
| NEGO-003 (12 buyer fears) | Objection Handler, Rassurance Engine | Objection pattern matching → prescribed response from 23-pattern playbook |
| NEGO-004 (8 seller fears) | Objection Handler, Rassurance Engine | Seller fear detector → transparency response with proof |

### 3.3 Argument Deployment (NEGO-005, NEGO-006)

| Rule | Consumed By | Consumption Mechanism |
|------|-------------|----------------------|
| NEGO-005 (6 LAWIM arguments) | Argumentation Selector, Message Composer | Profile-based argument selection; deployed in objection response, proposition, closing |
| NEGO-006 (5 property arguments) | Argumentation Selector, Message Composer | Property-centric argument selection based on property features and prospect profile |

**6 LAWIM Arguments:**

| Argument | Code | Description | Trigger Keywords |
|----------|------|-------------|-----------------|
| Zero commission | `ZERO_COM` | LAWIM does not take commission on transactions | commission, frais, prix, combien |
| Mise en relation | `MER_ARG` | Direct buyer-seller matching | contact, proprio, directement |
| Intelligent matching | `MATCH_ARG` | Algorithm-based property matching | correspond, recherche, matching |
| Accompagnement | `ACCOMP` | 50k FCFA complete transaction support | aide, suivi, document, notaire |
| WhatsApp | `WHATSAPP` | Accessible via WhatsApp, Cameroon's primary channel | whatsapp, message, canal |
| Verified agents | `AGENTS_VERIF` | Selected and trained agent network | agent, arnaque, confiance, vérifié |

**5 Property Arguments:**

| Argument | Code | Description | Property Feature |
|----------|------|-------------|-----------------|
| Proximity | `PROXIMITE` | Near work, schools, markets, transport | Location data |
| Accessibility | `ACCESS` | Road condition, transport links, parking | Road/access data |
| Security | `SECURITE` | Guard, gated, neighborhood safety | Security features |
| Potential | `POTENTIEL` | Appreciation, development, rental yield | Market data |
| Living environment | `CADRE_VIE` | Green space, calm, community | Neighborhood data |

### 3.4 Timing & Rhythm (NEGO-007)

| Rule | Consumed By | Consumption Mechanism |
|------|-------------|----------------------|
| NEGO-007 (4 key moments) | NBA Engine, Follow-up Scheduler | Seasonal calendar triggers proactive commercial actions |

**4 Key Moments for Negotiation:**

| Moment | Period | Commercial Action | Leverage |
|--------|--------|-------------------|----------|
| **End of year** | Nov-Dec | Closing push, year-end deals | Sellers want to close before year-end; buyers have year-end bonuses |
| **Back-to-school** | Aug-Sep | Relance to families, proximity argument | Families prioritizing school location |
| **Dry season** | Nov-Mar | Visit acceleration, construction projects | Optimal visiting conditions; construction season |
| **Diaspora transfers** | Jun-Aug, Dec-Jan | Diaspora engagement, secured payment | Peak diaspora transfer periods; high purchasing power |

### 3.5 Tone Principles (NEGO-009)

| Rule | Consumed By | Consumption Mechanism |
|------|-------------|----------------------|
| NEGO-009 (5 tone principles) | Conversation Engine, Tone Selector | Tone selected based on profile + context + interaction stage |

**5 Tone Principles:**

| Principle | Application | Forbidden Opposite |
|-----------|-------------|-------------------|
| **Professional** | Always maintain business-level communication | Aggressive, vague |
| **Expertise** | Show market knowledge, data, precision | Defensive, uncertain |
| **Patience** | Allow client rhythm, no forcing | Forced, impatient |
| **Adaptation** | Adjust tone to client profile and responses | Rigid, uniform |
| **Validation** | Acknowledge client emotions and concerns | Condescending, dismissive |

### 3.6 Trust Sequence (NEGO-010)

| Rule | Consumed By | Consumption Mechanism |
|------|-------------|----------------------|
| NEGO-010 (5-step trust sequence) | Closing Engine, Conversation Engine | Step progression tracked per session; each step has input/output conditions |

**5-Step Trust Sequence:**

```
Step 1: Active Listening
  Input: User message, intent, context
  Action: Reformulate needs, show understanding
  Output: Validated understanding

Step 2: Information
  Input: Validated needs
  Action: Provide precise data (price, docs, neighborhood)
  Output: Informed prospect

Step 3: Proposition
  Input: Informed prospect
  Action: Present adapted solution (property, service)
  Output: Proposal delivered

Step 4: Objections
  Input: Proposal delivered
  Action: Respond point by point to resistance
  Output: Objections addressed

Step 5: Closing
  Input: Objections addressed
  Action: Propose action (visit, offer, contact)
  Output: Commitment or next action scheduled
```

### 3.7 Follow-up Cadence (NEGO-011)

| Rule | Consumed By | Consumption Mechanism |
|------|-------------|----------------------|
| NEGO-011 (follow-up calendar) | Follow-up Engine, NBA Engine | Cadence enforced by timer-based triggers at J1/J7/J30/J90 |

### 3.8 Signal Detection (NEGO-012, NEGO-013, NEGO-014)

| Rule | Consumed By | Consumption Mechanism |
|------|-------------|----------------------|
| NEGO-012 (urgency signals) | Signal Detector, Priority Router | Pattern matching on `urgent`, `asap`, `vite`, `besoin maintenant` → priority escalation |
| NEGO-013 (investor signals) | Signal Detector, Profile Enricher | Pattern matching on `investir`, `rentable`, `ROI`, `rendement` → investor profile boost |
| NEGO-014 (diaspora signals) | Signal Detector, Profile Enricher | Pattern matching on `diaspora`, `je vis à`, `l'étranger` + foreign dial codes → diaspora profile |

---

## 4. Integration with Decision Engine

The Decision Engine orchestrates commercial knowledge consumption through its priority framework (from 04-DECISION-ENGINE-REFERENCE.md Ch88):

| Priority | Action | Commercial Knowledge Required |
|----------|--------|------------------------------|
| 1 | Correct an incoherence | — |
| 2 | Complete a critical field | Qualification rules (NEGO-001, NEGO-002) |
| 3 | Matching | Profile data |
| 4 | Present a property | Arguments (NEGO-005, NEGO-006) |
| 5 | Contact the holder | Mise en relation rules |
| 6 | Organize a visit | Visit workflow |
| 7 | Follow up | Follow-up cadence (NEGO-011) |
| 8 | Notifications | Key moments (NEGO-007) |
| 9 | Dossier optimization | Profile enrichment |

The Decision Engine selects the **Next Best Action (NBA)** by evaluating the current dossier state and applicable NEGO rules.

---

## 5. Integration with Conversation Engine

The Conversation Engine consumes commercial knowledge to produce client-facing messages:

```
Conversation Engine receives:
  • User message + context
  • Applicable NEGO rules (resolved by Decision Engine)
  • Profile (buyer/seller type from NEGO-001/002)

Conversation Engine produces:
  • Tone-adapted response (NEGO-009)
  • Trust sequence step (NEGO-010)
  • Script selection (welcome, qualification, objection, closing)
  • Argument deployment (NEGO-005, NEGO-006)
  • Next commercial action
```

### 5.1 Channel-Specific Adaptation

| Channel | Characteristics | Commercial Adaptation |
|---------|----------------|----------------------|
| **WhatsApp** | Primary, informal, high open rate | Shorter messages, quick arguments, emoji-light, immediate next action |
| **Telegram** | Secondary, more structured | Longer messages, document sharing, structured updates |
| **Dashboard** | Back-office, agent-facing | Full data, statistics, dossier history, NBA recommendations |

---

## 6. Audit Events

Every commercial action generates an audit event:

| Event | Trigger | Data |
|-------|---------|------|
| `commercial.action.executed` | Commercial action performed | action_code, profile, rule_references, outcome |
| `commercial.profile.detected` | Buyer/seller profile identified | profile_type, confidence, signals_matched |
| `commercial.argument.deployed` | Argument used in message | argument_code, context, effectiveness |
| `commercial.objection.handled` | Objection response sent | objection_pattern, response_used, satisfaction |
| `commercial.closing.attempted` | Closing step executed | closing_type, trust_step, result |
| `commercial.followup.triggered` | Follow-up scheduled | interval, template, contact_method |
| `commercial.diaspora.step` | Diaspora journey step | step_number, documents_sent, verification_status |

---

## References

| Source | Section |
|--------|---------|
| Heritage Gold NEGOTIATION_MODEL.md | §1 Objection Handling, §2 Psychological Techniques, §5 Argumentation, §7 Diaspora |
| Heritage Gold RULE_INDEX.md | NEGO-001 to NEGO-014 |
| 48-LAWIM-SALES-PLAYBOOK.md | §Commercial Positioning, §Scripts, §Arguments |
| 04-DECISION-ENGINE-REFERENCE.md | Ch83-100 (Decision Engine), Ch86 (Authorized Actions) |
| 05-WORKFLOW-REFERENCE.md | Part 7 (Negotiation Lifecycle), Part 5 (Mise en Relation) |
| knowledge_unified/commercial/closing_techniques.md | Closing techniques & trust sequence |
| knowledge_unified/commercial/conversation_tone.md | Tone principles |
| knowledge_unified/commercial/objection_handling.md | 23 objection patterns |
