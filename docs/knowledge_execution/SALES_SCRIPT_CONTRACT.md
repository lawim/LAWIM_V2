# Sales Script Contract

**Component of:** Knowledge Execution Architecture (H1)
**Domain:** Negotiation — Sales Script Execution
**Date:** 2026-07-15
**Status:** CANONICAL
**Prerequisite:** Heritage Gold NEGOTIATION_MODEL.md, RULE_INDEX.md (NEGO-001 to NEGO-014), 48-LAWIM-SALES-PLAYBOOK.md

---

## 1. Script Structure Contract

Every script in LAWIM must conform to this structure:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `trigger` | String | Yes | Event or condition that activates this script |
| `audience` | Array[String] | Yes | Target profile(s): `national`, `diaspora`, `investor`, `young_professional`, `individual`, `developer`, `landlord` |
| `context` | Object | Yes | Required context variables (lead state, dossier state, conversation history) |
| `preconditions` | Array[String] | Yes | Conditions that must be true before script can execute |
| `message_goal` | String | Yes | Single measurable objective of this message |
| `allowed_content` | Array[String] | Yes | Approved content types, arguments, tones |
| `forbidden_content` | Array[String] | Yes | Explicitly prohibited content |
| `next_action` | Object | Yes | Expected next commercial action after script execution |
| `escalation` | Object | Yes | Conditions under which the conversation escalates to human |
| `audit_event` | String | Yes | Audit event code emitted when script is used |

---

## 2. Script Definitions

### 2.1 Welcome Script

| Field | Value |
|-------|-------|
| **trigger** | First contact from new lead (message.received on new user) |
| **audience** | `[national, diaspora, investor, young_professional]` |
| **context** | `{ user_state: NEW_USER, channel: whatsapp/telegram, language: detected }` |
| **preconditions** | `[ "user has no prior conversation", "message is not spam" ]` |
| **message_goal** | Establish LAWIM positioning and begin qualification |

**FR:**
```
Bonjour [nom], bienvenue sur LAWIM. Je suis l'assistant LAWIM.

Nous mettons en relation acheteurs et vendeurs directement — zéro commission sur les transactions.
Avec nous, vous bénéficiez de :
• Mise en relation directe propriétaire-acquéreur
• Matching intelligent selon vos critères
• Accompagnement personnalisé à 50 000 FCFA seulement

Que recherchez-vous exactement ? Achat, location, ou vente ?
```

**EN:**
```
Hello [name], welcome to LAWIM. I am the LAWIM assistant.

We connect buyers and sellers directly — zero commission on transactions.
With us you benefit from:
• Direct owner-buyer connection
• Smart matching based on your criteria
• Personalized support at only 50,000 FCFA

What are you looking for exactly? Buying, renting, or selling?
```

| Field | Value |
|-------|-------|
| **allowed_content** | `[zero_commission, mise_en_relation, matching_intelligent, accompagnement]` |
| **forbidden_content** | `[price_guarantee, timeline_promise, document_commitment]` |
| **next_action** | `{ action: QUALIFY, field: intent, delay: immediate }` |
| **escalation** | `{ condition: "user asks for human", action: "transfer_to_advisor" }` |
| **audit_event** | `script.welcome.sent` |

---

### 2.2 Qualification Script

| Field | Value |
|-------|-------|
| **trigger** | Lead expressed intent (buy/rent/sell) but missing critical fields |
| **audience** | `[national, diaspora, investor, young_professional, individual, developer, landlord]` |
| **context** | `{ missing_fields: [budget, city, property_type, timeline], lead_score: score }` |
| **preconditions** | `[ "intent detected", "at least one critical field missing" ]` |
| **message_goal** | Collect missing qualification data without interrogation feeling |

**NEGO Reference:** NEGO-001 (buyer profiles), NEGO-007 (key moments), NEGO-009 (tone: patient, encouraging)

**FR (Buyer):**
```
Merci [nom]. Pour bien cibler les biens qui vous correspondent, pouvez-vous me préciser :

• Dans quelle ville ou quartier cherchez-vous ?
• Quel est votre budget approximatif ?
• Quel type de bien ? (appartement, maison, terrain, villa)

Je vous propose les meilleures options disponibles.
```

**FR (Seller):**
```
Merci [nom]. Pour présenter votre bien au bon acheteur, dites-m'en un peu plus :

• Dans quel quartier se trouve le bien ?
• À quel prix souhaitez-vous vendre/louer ?
• Quel type de bien ? (surface, pièces, état)

Je m'occupe de trouver des acquéreurs sérieux.
```

**EN (Buyer):**
```
Thank you [name]. To find the right properties for you, could you tell me:

• In which city or neighborhood are you looking?
• What is your approximate budget?
• What type of property? (apartment, house, land, villa)

I will propose the best available options.
```

**EN (Seller):**
```
Thank you [name]. To present your property to the right buyer, tell me more:

• In which neighborhood is the property located?
• At what price do you wish to sell/rent?
• What type of property? (size, rooms, condition)

I will find serious buyers for you.
```

| Field | Value |
|-------|-------|
| **allowed_content** | `[qualification_questions, intent_confirmation, value_proposition]` |
| **forbidden_content** | `[multiple_questions_in_one_message_for_whatsapp, pressure_for_immediate_answer, budget_outside_known_range]` |
| **next_action** | `{ action: MATCH, field: [city, budget, property_type], delay: < 24h }` |
| **escalation** | `{ condition: "user refuses to answer after 3 attempts", action: "mark_as_LOW_priority" }` |
| **audit_event** | `script.qualification.sent` |

---

### 2.3 Objection Handling Script

**NEGO Reference:** NEGO-003 (buyer fears), NEGO-004 (seller fears), NEGO-005 (LAWIM arguments), NEGO-009 (tone: patient, expertise, adaptation)

| Field | Value |
|-------|-------|
| **trigger** | User raised an objection from the 23-pattern set |
| **audience** | `[national, diaspora, investor, young_professional]` |
| **context** | `{ objection_pattern: pattern_id, buyer_fears: [fear_ids], dossier_state: state }` |
| **preconditions** | `[ "objection detected", "applicable response exists" ]` |
| **message_goal** | Address the specific objection and maintain trust |

**FR — "Trop cher" (Pattern #1):**
```
Je comprends. Voici des biens comparables dans le même quartier :
[listing 1] — [prix]
[listing 2] — [prix]

Le prix de ce bien reflète [contexte marché: offre/demande, emplacement, état].
Souhaitez-vous que je vous propose des options dans votre budget ?
```

**FR — "Je me méfie des agents" (Pattern #20):**
```
Je comprends votre méfiance. LAWIM fonctionne différemment :

✓ Zéro commission — nous ne vivons pas de vos transactions
✓ Agents vérifiés et notés par la communauté
✓ Accompagnement notaire à 50 000 FCFA pour sécuriser la transaction
✓ Tous les documents vous sont partagés avant tout engagement

Puis-je vous montrer un bien pour vous faire votre propre avis ?
```

**FR — "C'est négociable ?" (Pattern #3):**
```
Je suis transparent avec vous : sur ce bien, la marge de négociation est de [X]% selon le marché actuel.
Le prix affiché est [prix], et voici ce que des biens similaires ont été négociés récemment dans le quartier.

Souhaitez-vous faire une proposition ?
```

**EN — "Too expensive" (Pattern #1):**
```
I understand. Here are comparable properties in the same neighborhood:
[listing 1] — [price]
[listing 2] — [price]

The price of this property reflects [market context: supply/demand, location, condition].
Would you like me to suggest options within your budget?
```

| Field | Value |
|-------|-------|
| **allowed_content** | `[comparison_data, market_context, proof_documents, transparency_statement]` |
| **forbidden_content** | `[aggressive_closing, false_promises, vague_answers, defensive_tone]` |
| **next_action** | `{ action: DEPENDS_ON_OBJECTION, options: [VISIT_PROPOSE, PRICE_DISCUSS, DOCUMENT_SHARE], delay: immediate }` |
| **escalation** | `{ condition: "objection persists after 3 responses", action: "offer_human_advisor_call" }` |
| **audit_event** | `script.objection.handled` |

---

### 2.4 Price Negotiation Script

**NEGO Reference:** NEGO-008 (price expressions: prix ferme, à débattre, dernier prix), NEGO-012 (urgency signals), NEGO-009 (tone: professional, expertise, patience)

| Field | Value |
|-------|-------|
| **trigger** | User initiated price discussion ("dernier prix?", "c'est négociable?", "prix") |
| **audience** | `[national, diaspora, investor, young_professional]` |
| **context** | `{ price_expression: type, property_price: amount, market_context: object, profile: profile }` |
| **preconditions** | `[ "property presented", "price discussed", "no active negotiation" ]` |
| **message_goal** | Open transparent price discussion without aggression |

**FR — Prix négociable:**
```
Le bien est proposé à [prix]. Ce prix est négociable.
Sur ce type de bien dans [quartier], les transactions récentes se situent entre [fourchette_basse] et [fourchette_haute].
Quelle serait votre proposition ?
```

**FR — Prix ferme:**
```
Le prix de [prix] est ferme pour ce bien. Cela s'explique par [raison: emplacement, état, titre foncier].
Je peux vous montrer d'autres biens dans votre budget si celui-ci dépasse vos moyens.
```

**FR — À débattre:**
```
Le prix est à débattre. Le vendeur est ouvert aux propositions.
Avez-vous un montant en tête ? Je peux transmettre votre offre.
```

**EN — Negotiable:**
```
The property is offered at [price]. This price is negotiable.
For this type of property in [neighborhood], recent transactions range between [low_range] and [high_range].
What would your proposal be?
```

| Field | Value |
|-------|-------|
| **allowed_content** | `[market_data, price_context, negotiation_range, transparent_margin]` |
| **forbidden_content** | `[aggressive_closing, "take_it_or_leave_it", fake_urgency, price_manipulation]` |
| **next_action** | `{ action: PROPOSE_COUNTER_OR_ACCEPT, delay: 24h }` |
| **escalation** | `{ condition: "price gap > 20% or repeated impasse", action: "human_negotiator_assigned" }` |
| **audit_event** | `script.negotiation.price_opened` |

---

### 2.5 Closing Script

**NEGO Reference:** NEGO-010 (5-step trust sequence, step 5), NEGO-009 (tone: professional, validation)

| Field | Value |
|-------|-------|
| **trigger** | Trust sequence completed, objections handled, prospect ready |
| **audience** | `[national, diaspora, investor, young_professional]` |
| **context** | `{ trust_step: 5, objections: [resolved_ids], proposal: object }` |
| **preconditions** | `[ "proposal accepted in principle", "no active objections", "property available" ]` |
| **message_goal** | Move prospect to committed action (visit, offer, contact) |

**FR — Visit closing:**
```
Parfait ! Je propose une visite [jour] à [heure] ou [jour alternative].
Je prépare les documents et vous confirme par WhatsApp.

Aussi, je vous envoie la localisation exacte et les photos récentes.
```

**FR — Diaspora closing:**
```
Très bien. Voici la procédure :

1. Je vous envoie le rapport de visite complet (photos, vidéo, GPS) sous 24h
2. Vérification des documents par notre équipe juridique
3. Proposition sécurisée avec paiement échelonné

Souhaitez-vous commencer par la vérification documentaire ?
```

**EN — Visit closing:**
```
Perfect! I propose a visit on [day] at [time] or [alternative day].
I will prepare the documents and confirm via WhatsApp.

I will also send you the exact location and recent photos.
```

| Field | Value |
|-------|-------|
| **allowed_content** | `[visit_proposal, document_preparation, timeline, next_steps]` |
| **forbidden_content** | `[ultimatum, false_deadline, pressure_tactic, conditional_discount]` |
| **next_action** | `{ action: SCHEDULE_VISIT_OR_SEND_PROPOSAL, delay: < 2h }` |
| **escalation** | `{ condition: "user hesitates or requests more time", action: "reassure_and_reschedule" }` |
| **audit_event** | `script.closing.attempted` |

---

### 2.6 Follow-up Script

**NEGO Reference:** NEGO-011 (follow-up cadence J1/J7/J30/J90), CONV-016 (follow-up intervals)

| Field | Value |
|-------|-------|
| **trigger** | Follow-up timer elapsed (J1, J7, J30, J90) or trigger event |
| **audience** | `[national, diaspora, investor, young_professional]` |
| **context** | `{ interval: J1/J7/J30/J90, last_action: object, dossier_state: state }` |
| **preconditions** | `[ "no opt-out", "follow-up count < max_attempts (12)" ]` |
| **message_goal** | Re-engage lead with value-added content |

**FR — J1 (24h):**
```
Bonjour [nom], nous avons [N] nouveaux biens qui correspondent à votre recherche à [ville] dans votre budget.
Souhaitez-vous les voir ?
```

**FR — J7 (168h):**
```
Bonjour [nom], cette semaine : 5 nouvelles annonces à [ville].
Dont une qui pourrait vous intéresser : [description courte].
```

**FR — J30 (720h):**
```
Bonjour [nom], en exclusivité pour vous : un mois prioritaire pour voir les nouvelles annonces avant tout le monde. Gratuit.
```

**FR — J90 (2160h):**
```
Bonjour [nom], votre recherche est toujours d'actualité ? Voici les tendances du marché à [ville].
J'ai [N] biens à vous proposer.
```

**EN — J1 (24h):**
```
Hello [name], we have [N] new properties matching your search in [city] within your budget.
Would you like to see them?
```

| Field | Value |
|-------|-------|
| **allowed_content** | `[new_listings, market_updates, exclusive_offers, value_added_content]` |
| **forbidden_content** | `[begging_response, repeated_property_after_refusal, spam_same_message]` |
| **next_action** | `{ action: WAIT_FOR_RESPONSE_OR_NEXT_INTERVAL, delay: interval_ms }` |
| **escalation** | `{ condition: "no response after 12 attempts", action: "archive_dossier" }` |
| **audit_event** | `script.followup.sent` |

---

### 2.7 Diaspora Engagement Script

**NEGO Reference:** NEGO-014 (diaspora signals), NEGO-003 (buyer fears: credibility, documents), NEGO-013 (investor signals overlap for diaspora investors)

| Field | Value |
|-------|-------|
| **trigger** | Diaspora profile detected (NEGO-014), or diaspora service requested |
| **audience** | `[diaspora]` |
| **context** | `{ diaspora_step: 1-7, documents_verified: bool, payment_method: secured }` |
| **preconditions** | `[ "diaspora signal detected", "documents verified before property proposal" ]` |
| **message_goal** | Build credibility and structured remote trust journey |

**FR — Step 1 (Premier contact):**
```
Bonjour [nom], je comprends que vous êtes au [pays] et cherchez un bien au Cameroun.

Chez LAWIM, nous accompagnons spécifiquement la diaspora avec :
• Vérification documentaire complète avant toute proposition
• Rapports structurés avec photos, vidéos et géolocalisation
• Paiement sécurisé et échelonné
• Correspondant local pour les visites

Puis-je commencer par comprendre votre projet ?
```

**FR — Step 4 (Rapport écrit + photos):**
```
Voici le rapport de visite complet :

📋 Bien : [adresse/description]
📍 Localisation : [GPS link]
📸 Photos : [link gallery]
📹 Vidéo : [link]
📄 Documents vérifiés : [status]

Le bien est [disponible/réservé]. Souhaitez-vous :
1. Procéder à la vérification juridique complète ?
2. Organiser une visite vidéo en direct ?
3. Faire une proposition ?
```

**EN — Step 1 (First contact):**
```
Hello [name], I understand you are in [country] and looking for property in Cameroon.

At LAWIM, we specifically serve the diaspora with:
• Complete document verification before any proposal
• Structured reports with photos, videos, and geolocation
• Secured staggered payments
• Local correspondent for visits

May I start by understanding your project?
```

| Field | Value |
|-------|-------|
| **allowed_content** | `[structured_reports, verified_documents, geolocation, video_visit, secured_payment, local_correspondent]` |
| **forbidden_content** | `[timeline_promise, vague_document_claims, pressure_for_payment_before_verification]` |
| **next_action** | `{ action: DIASPORA_STEP_n+1, delay: < 48h }` |
| **escalation** | `{ condition: "diaspora requests human relationship manager", action: "assign_diaspora_advisor" }` |
| **audit_event** | `script.diaspora.step_executed` |

---

## 3. Script Selection Matrix

The Decision Engine selects the appropriate script based on lead profile and current state:

```
                   ┌────────────────────────────────────────────────────────────┐
                   │                     LEAD STATE                            │
                   ├──────────┬──────────┬──────────┬──────────┬───────────────┤
                   │  NEW     │ QUALIFIED│ OBJECTION│ PROPOSAL │   CLOSING     │
┌────────┐         ├──────────┼──────────┼──────────┼──────────┼───────────────┤
│PROFILE │ WELCOME │ QUALIFY  │ OBJECTION│ NEGOTIATE│ CLOSING  │ FOLLOW-UP     │
├────────┤─────────┼──────────┼──────────┼──────────┼──────────┼───────────────┤
│National│ Welcome │Qualify-FR│Object-FR │Negotiate │Close-FR  │Follow-up-FR   │
├────────┤─────────┼──────────┼──────────┼──────────┼──────────┼───────────────┤
│Diaspora│ Welcome │Qualify-FR│Object-FR │Negotiate │Close-DI  │Follow-up-FR   │
│        │         │/EN       │/EN       │/EN       │          │/EN            │
├────────┤─────────┼──────────┼──────────┼──────────┼──────────┼───────────────┤
│Investor│ Welcome │Qualify-FR│Object-FR │Negotiate │Close-FR  │Follow-up-FR   │
│        │         │/EN       │/EN       │/EN       │/EN       │/EN            │
├────────┤─────────┼──────────┼──────────┼──────────┼──────────┼───────────────┤
│Young   │ Welcome │Qualify-FR│Object-FR │Negotiate │Close-FR  │Follow-up-FR   │
│Professional       │          │          │          │          │               │
└────────┴─────────┴──────────┴──────────┴──────────┴──────────┴───────────────┘
```

### 3.1 Script Selection Rules

| Condition | Script Selected | Priority |
|-----------|----------------|----------|
| First message from new user | Welcome | HIGHEST |
| Intent detected + missing critical fields | Qualification | HIGH |
| Objection keyword matched | Objection Handling | HIGH |
| Price expression detected (prix ferme, à débattre, dernier prix) | Price Negotiation | HIGH |
| Trust step 5 reached + proposal accepted | Closing | HIGH |
| No response for interval duration | Follow-up | Scheduled |
| Diaspora profile detected + no active engagement | Diaspora Engagement | MEDIUM |

### 3.2 Script Escalation Rules

| Condition | Action |
|-----------|--------|
| 3 consecutive unanswered messages | Archive dossier (after 12 follow-up attempts total) |
| User explicitly asks for human | Transfer to LAWIM advisor |
| Price gap > 20% in negotiation | Offer human negotiator |
| Legal question beyond scope | Redirect to notary partner |
| Fraud suspicion | Suspend conversation, alert security |
| User requests data deletion | Execute RGPD workflow (7-day delay) |

---

## 4. Language Selection

Scripts are available in FR (default), EN, and PID (Pidgin) based on language detection (LANG-001 to LANG-003).

| Detection | Script Language | Fallback |
|-----------|----------------|----------|
| French keywords, 237 number | FR | FR |
| English keywords, non-237 number | EN | EN |
| Pidgin keywords | PID | EN |
| Mixed/unclear | FR (default) | FR |

---

## References

| Source | Section |
|--------|---------|
| Heritage Gold NEGOTIATION_MODEL.md | §1 Objections, §3 Closing, §4 Follow-up, §5 Arguments, §7 Diaspora |
| Heritage Gold RULE_INDEX.md | NEGO-001 to NEGO-014 |
| 48-LAWIM-SALES-PLAYBOOK.md | §Scripts, §Commercial Positioning |
| knowledge_unified/commercial/closing_techniques.md | 5-step trust sequence, closing techniques |
| knowledge_unified/commercial/conversation_tone.md | Tone principles, forbidden tones |
| knowledge_unified/commercial/follow_up_strategies.md | Follow-up templates and cadence |
| knowledge_unified/commercial/objection_handling.md | 23 objection patterns with responses |
| RESPONSE_POLICY.md | CONV-001 to CONV-009 (positioning, tone, channel) |
