# Follow-up Execution Model

**Component of:** Knowledge Execution Architecture (H1)
**Domain:** Negotiation — Follow-up Execution
**Date:** 2026-07-15
**Status:** CANONICAL
**Prerequisite:** Heritage Gold NEGOTIATION_MODEL.md §4 (Follow-up Strategies), RULE_INDEX.md (NEGO-011), CRM_MODEL.md

---

**NEGO Reference:** NEGO-011 (follow-up calendar J1/J7/J30/J90), NEGO-007 (key moments for follow-up timing)

## 1. Follow-up Schedule

From Heritage Gold NEGOTIATION_MODEL §4.1 and RULE_INDEX.md NEGO-011.

| Interval | Label | Timer (hours) | Timer (ms) | Type | Goal |
|----------|-------|---------------|------------|------|------|
| **J1** | 24h follow-up | 24h | 86,400,000 | Capitalize | Capitalize on recent interest |
| **J7** | Weekly check | 168h | 604,800,000 | Maintain | Maintain engagement with new listings |
| **J30** | Monthly re-engagement | 720h | 2,592,000,000 | Strong value | Offer exclusive value to re-engage |
| **J90** | Quarterly reactivation | 2160h | 7,776,000,000 | Reactivate | Re-engage dormant leads with market data |

### 1.1 Timer Execution

```
Follow-up Timer Manager
    │
    ├── J1: Triggered 24h after: last_message, visit_completion, proposal_sent, relationship_created
    │
    ├── J7: Triggered 168h after: last_message (if no response), objection_raised (if unresolved)
    │
    ├── J30: Triggered 720h after: last_contact (if no response), dossier_creation
    │
    └── J90: Triggered 2160h after: dossier_creation (if still active), lead_becomes_cold
```

### 1.2 Timer Reset Rules

| Event | Timer Action |
|-------|-------------|
| User responds to follow-up | Reset all timers, restart from J1 |
| User explicitly opts out | Cancel all timers, archive dossier |
| Visit completed | Reset to J1 post-visit |
| Proposal sent | Reset to J1 post-proposal |
| Relationship created (mise en relation) | Reset to J1 post-connection |
| Objection raised (resolved) | Reset to J1 post-resolution |
| Objection raised (unresolved) | Continue existing timer |
| Dossier becomes HOT | Cancel all timers (active engagement) |
| Dossier is archived | Cancel all timers |

---

## 2. Follow-up Triggers

The follow-up system activates on the following triggers:

| Trigger Code | Trigger Event | Immediate Action | Follow-up Delay |
|-------------|---------------|-----------------|-----------------|
| `NO_RESPONSE` | Lead did not respond to last message | Schedule J1 follow-up | 24h |
| `OBJECTION_RAISED` | Lead raised an objection | Respond to objection, schedule J7 | 168h if unresolved |
| `VISIT_COMPLETED` | Physical or video visit finished | Send visit report, schedule J1 | 24h post-visit |
| `PROPOSAL_SENT` | Property proposal sent to lead | Wait for response, schedule J1 | 24h |
| `RELATIONSHIP_CREATED` | Double-consent connection established | Handoff to holder, schedule J1 | 24h |
| `INTENT_DETECTED` | Lead intent detected (buy/rent/sell) | Begin qualification, schedule J7 | 168h if not qualified |
| `DIASPORA_STEP` | Diaspora journey step completed | Move to next step, schedule J1 | 24h |
| `NEGOTIATION_SILENCE` | No response in negotiation > 72h | Send reminder, schedule J+3 | 72h |
| `MARKET_EVENT` | New matching property published | Immediate notification | Immediate |
| `PRICE_DROP` | Watched property price decreased | Immediate notification | Immediate |

---

## 3. Message Templates per Follow-up Type

### 3.1 No Response Follow-up

**FR — J1:**
```
Bonjour [nom], nous avons [N] nouveaux biens qui correspondent à votre recherche à [ville] dans votre budget. Souhaitez-vous les voir ?
```

**FR — J7:**
```
Bonjour [nom], cette semaine : 5 nouvelles annonces à [ville]. Dont une qui pourrait vous intéresser...
```

**FR — J30:**
```
Bonjour [nom], en exclusivité pour vous : un mois prioritaire pour voir les nouvelles annonces avant tout le monde. Gratuit.
```

**FR — J90:**
```
Bonjour [nom], votre recherche est toujours d'actualité ? Voici les tendances du marché à [ville] : [statistiques]. J'ai [N] biens à vous proposer.
```

**EN — J1:**
```
Hello [name], we have [N] new properties matching your search in [city] within your budget. Would you like to see them?
```

**EN — J7:**
```
Hello [name], this week: 5 new listings in [city]. Including one that might interest you...
```

**EN — J30:**
```
Hello [name], exclusively for you: one month of priority access to new listings before everyone else. Free.
```

**EN — J90:**
```
Hello [name], is your search still active? Here are market trends for [city]: [statistics]. I have [N] properties to propose.
```

### 3.2 Objection Raised Follow-up

**FR (Unresolved objection — J7):**
```
Bonjour [nom], je reviens vers vous suite à notre échange. Auriez-vous eu le temps de réfléchir à [objection] ? Je reste disponible pour toute question.
```

**FR (Resolved objection — J1):**
```
Suite à notre échange, voici les informations complémentaires sur le bien :
[information additionnelle]
Souhaitez-vous organiser une visite ?
```

### 3.3 Visit Completed Follow-up

**FR — J1 post-visit:**
```
Bonjour [nom], j'espère que la visite du bien à [adresse] vous a plu.
Avez-vous des questions sur le bien ou souhaitez-vous :
1. Discuter du prix ?
2. Voir les documents ?
3. Planifier une seconde visite ?
```

**FR — Diaspora visit report (J1):**
```
Bonjour [nom], voici le rapport de visite complet :

📋 Bien : [description]
📍 GPS : [lien]
📸 Photos : [N] photos jointes
📹 Vidéo : [lien vidéo]
📄 Statut documentaire : [vérifié/en cours]
📊 Avis de l'agent : [commentaire]

Souhaitez-vous procéder à la vérification juridique ou faire une proposition ?
```

**EN — J1 post-visit:**
```
Hello [name], I hope you enjoyed the visit to [address].
Do you have any questions about the property or would you like to:
1. Discuss the price?
2. See the documents?
3. Schedule a second visit?
```

### 3.4 Proposal Sent Follow-up

**FR — J1:**
```
Bonjour [nom], avez-vous eu le temps de consulter les biens que je vous ai proposés ? Je peux vous donner plus d'informations sur l'un d'eux si vous le souhaitez.
```

**FR — J7:**
```
Bonjour [nom], je voulais m'assurer que vous avez bien reçu ma proposition. Avez-vous des questions sur les biens présentés ?
```

### 3.5 Relationship Created Follow-up

**FR — J1 (to demandeur):**
```
Félicitations ! Vous êtes maintenant en contact direct avec le propriétaire/agent concernant le bien à [adresse].
N'hésitez pas à organiser une visite ou poser vos questions directement.

LAWIM reste disponible si vous avez besoin d'accompagnement.
```

**FR — J7 (post-connection check):**
```
Bonjour [nom], votre échange avec le propriétaire se passe bien ? Avez-vous besoin d'aide pour les documents, la visite, ou la négociation ?
```

### 3.6 Diaspora-Specific Follow-up

**FR — Step report (after each action):**
```
Bonjour [nom], mise à jour de votre dossier diaspora :

Action effectuée : [visite/vérification/document]
Résultat : [résultat détaillé]
Prochaine étape : [étape suivante]

Je vous tiens informé sous 48h de la suite.
```

**FR — Structured report template:**
```
RAPPORT DE VISITE — [date]

Bien : [adresse]
Type : [type]
Prix : [prix] FCFA

1. LOCALISATION
   • GPS : [coordonnées]
   • Quartier : [nom]
   • Accessibilité : [description]

2. ÉTAT DU BIEN
   • Intérieur : [description]
   • Extérieur : [description]
   • Travaux nécessaires : [oui/non]

3. DOCUMENTS
   • Titre foncier : [statut]
   • Conformité : [statut]

4. PHOTOS/VIDÉOS
   • [N] photos jointes
   • Vidéo disponible sur demande

5. AVIS
   • Points forts : [liste]
   • Points à vérifier : [liste]
```

---

## 4. NBA Integration

The Next Best Action engine integrates with the follow-up system to determine optimal timing and content.

### 4.1 NBA Priority for Follow-up

The Decision Engine prioritizes actions (from 04-DECISION-ENGINE-REFERENCE.md Ch88):

| Priority | Action | Precedes Follow-up? |
|----------|--------|---------------------|
| 1 | Correct an incoherence | YES — must fix before follow-up |
| 2 | Complete a critical field | YES — must qualify before follow-up |
| 3 | Matching | YES — match before following up |
| 4 | Present a property | YES — present before following up |
| 5 | Contact the holder | YES — contact before following up if applicable |
| 6 | Organize a visit | YES — visit before follow-up if applicable |
| **7** | **Follow up (relance)** | **NBA selected when no higher-priority action possible** |
| 8 | Notifications | Parallel to follow-up |
| 9 | Dossier optimization | Background, parallel to follow-up |

### 4.2 NBA Follow-up Selection Logic

```
IF dossier has no pending higher-priority action (1-6)
AND follow-up timer has elapsed
AND follow-up attempt count < MAX_ATTEMPTS (12)
THEN:
    SELECT follow-up type based on:
        - Last trigger event (NO_RESPONSE, VISIT_COMPLETED, etc.)
        - Lead profile (national, diaspora, investor, young_professional)
        - Current timer interval (J1, J7, J30, J90)
        - Available new inventory (new matches)
        - Market events (price drops, new listings)
    
    COMPOSE message using template + personalization
    SCHEDULE next follow-up if no response
```

### 4.3 NBA Event-Driven Follow-up

The following events can trigger a follow-up outside the scheduled cadence:

| Event | Follow-up Type | Delay |
|-------|---------------|-------|
| New property matching score > 80% | Immediate listing notification | < 5 min |
| Price drop on watched property | Price alert | < 5 min |
| Property becomes available again | Re-availability alert | < 15 min |
| Lead visits property page | Re-engagement follow-up | < 1h |
| Holder accepts contact | Connection notification | Immediate |

---

## 5. Opt-out Handling

### 5.1 Opt-out Detection

Detected through explicit user messages:

| Language | Opt-out Signals |
|----------|----------------|
| FR | ne plus m'écrire, stop, arrêtez, pas intéressé, supprimez mes données, ne me contactez plus |
| EN | stop, unsubscribe, don't write, not interested, delete my data |
| PID | no write me again, abeg stop, I don want |

### 5.2 Opt-out Process

```
User opt-out signal detected
    │
    ├── 1. Confirm opt-out: "Confirmez-vous ne plus être contacté ?" (FR)
    │       │
    │       ├── CONFIRMED → Stop all follow-ups, archive dossier
    │       │
    │       └── DENIED → Resume normal follow-up schedule
    │
    └── 2. If RGPD request ("SUPPRIMER MES DONNÉES"):
            ├── Initiate 7-day delay (CONV-009)
            ├── Stop all follow-ups immediately
            └── Schedule data deletion at day 7
```

### 5.3 Opt-out Confirmation Message

**FR:**
```
D'accord [nom], je prends note. Vous ne recevrez plus de messages de ma part concernant votre recherche.
Si vous changez d'avis, vous pouvez m'écrire à tout moment.
```

**EN:**
```
Noted [name]. You will no longer receive messages regarding your search.
If you change your mind, you can write to me at any time.
```

**FR (RGPD):**
```
J'ai bien pris note de votre demande de suppression de données.
Conformément à nos engagements, vos données seront supprimées sous 7 jours.
Vous recevrez un message de confirmation à l'issue.
```

---

## 6. Maximum Follow-up Attempts Before Archiving

### 6.1 Attempt Limits

| Lead Class | Max Follow-ups | Max Duration | Archive Action |
|------------|---------------|--------------|----------------|
| HOT | 6 attempts | 90 days | Archive with "lost_lead" reason |
| WARM | 8 attempts | 180 days | Archive with "cold_lead" reason |
| COLD | 10 attempts | 270 days | Archive with "dormant" reason |
| LOW | 12 attempts | 365 days | Archive with "inactive" reason |
| DIASPORA | 12 attempts | 365 days | Archive with "diaspora_pending" reason |

### 6.2 Attempt Counter

```
Each attempt = follow-up message sent
Max attempts per interval:
  • J1 → J7 → J30 → J90 = 4 complete cycles
  • Each interval resets if user responds
  • No response = increment counter + move to next interval
  • Counter persists across interval changes

Total possible: 
  J1(1) + J7(1) + J30(1) + J90(1) = 4 per cycle
  LOW leads: 3 complete cycles = 12 attempts → archive
```

### 6.3 Pre-archive Message

**FR — Before archiving (attempt 11/12):**
```
Bonjour [nom], je me permets un dernier message. Votre recherche est toujours d'actualité ?
Si je n'ai pas de réponse, je clôturerai temporairement votre dossier.
Vous pourrez me recontacter à tout moment pour le réactiver.
```

**FR — Archive notification:**
```
Votre dossier de recherche a été archivé faute d'activité. Vous pouvez me recontacter à tout moment pour le réactiver — je reprendrai votre recherche là où nous nous sommes arrêtés.
```

### 6.4 Reactivation

Archived dossiers can be reactivated (per NEGO-014, long-term memory retains data for 365 days):

| Reactivation Trigger | Action |
|---------------------|--------|
| User sends new message | Reopen dossier, restore context from memory |
| New matching property (score > 80%) | Reopen dossier, notify user |
| Market event (price change on watched property) | Notify user, reopen if they respond |

---

## 7. Audit Trail

Every follow-up action is recorded in the audit log.

### 7.1 Audit Event Schema

| Field | Type | Description |
|-------|------|-------------|
| `event` | String | `followup.sent` or `followup.archived` or `followup.optout` |
| `timestamp` | ISO8601 | When the follow-up was executed |
| `dossier_id` | UUID | Target dossier |
| `lead_id` | UUID | Target lead |
| `interval` | String | J1, J7, J30, J90 |
| `attempt_number` | Integer | Current attempt count (1-12) |
| `template_used` | String | Template identifier |
| `message_snippet` | String | First 100 chars of message sent |
| `response_received` | Boolean | Whether user responded |
| `next_followup_scheduled` | ISO8601 | Next scheduled follow-up time |
| `rule_references` | Array[String] | NEGO-011, CONV-016, etc. |

### 7.2 Audit Events Table

| Event Code | Trigger | Data Captured |
|------------|---------|---------------|
| `followup.sent` | Follow-up message dispatched | interval, attempt, template, recipient |
| `followup.response.received` | User replied to follow-up | response_text, sentiment, time_to_respond |
| `followup.optout.confirmed` | User opted out | optout_reason, timestamp |
| `followup.optout.rgpd` | RGPD deletion requested | 7-day_delay_activated, deletion_date |
| `followup.archived` | Dossier archived after max attempts | total_attempts, duration, reason |
| `followup.reactivated` | Archived dossier reopened | reactivation_trigger, context_restored |
| `followup.market.alert` | Market event triggered follow-up | event_type, property_id, match_score |

---

## 8. Diaspora-Specific Follow-up Rules

From Heritage Gold NEGOTIATION_MODEL §4.3 and §7:

| Rule | Implementation |
|------|---------------|
| Structured reports after each action | Every diaspora action triggers a written report with: action, result, next step |
| Precise timelines | Always include specific deadline: "I will send you the report within 48 hours" |
| Visual proof in each report | Photos, videos, geolocation in every diaspora communication |
| WhatsApp + email dual channel | Short updates via WhatsApp, full documents via email |
| 5 LAWIM diaspora rules | Always verify documents before proposing, structured report, video contact, no promises, local correspondent |

### 8.1 Diaspora Follow-up Cadence

| Phase | Cadence | Content |
|-------|---------|---------|
| Initial contact | Immediate | Welcome, diaspora service intro |
| Document verification | Within 48h | Verified documents report |
| Property proposal | Within 24h of verification | 3-5 matching properties with full data |
| Video visit | Within 72h of proposal | Live video or recorded walkthrough |
| Written report | Within 24h of video | Full written + photo + GPS report |
| Legal verification | Within 5 days | Title deed, litigation check, document status |
| Secured payment proposal | Within 24h of legal OK | Staggered payment plan, escrow options |
| Post-transaction | J1, J7, J30, J90 | Satisfaction check, key handover, registration follow-up |

---

## References

| Source | Section |
|--------|---------|
| Heritage Gold NEGOTIATION_MODEL.md | §4 Follow-up Strategies, §4.1 Relance Calendar, §4.3 Diaspora Follow-up |
| Heritage Gold RULE_INDEX.md | NEGO-011 (follow-up calendar), CONV-016 (follow-up intervals) |
| 05-WORKFLOW-REFERENCE.md | Part 7 (Negotiation Lifecycle), Ch79 (Surveillance continue) |
| 04-DECISION-ENGINE-REFERENCE.md | Ch83-88 (NBA priority), Ch11 (NBA core principle) |
| CRM_MODEL.md | Sec 1 (Pipeline), Sec 5 (Lead Priorities), Sec 6 (Behavior Tracking) |
| follow_up_system.py | Follow-up engine implementation |
| knowledge_unified/commercial/follow_up_strategies.md | Follow-up strategies, templates, cadence |
| conversation_memory.py | Conversation retention (365 days) |
| long_term_memory.py | Long-term lead storage and reactivation |
| RESPONSE_POLICY.md | CONV-009 (RGPD), CONV-016 (Relances) |
