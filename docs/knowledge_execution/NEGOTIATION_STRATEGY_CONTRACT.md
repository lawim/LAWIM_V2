# Negotiation Strategy Contract

**Component of:** Knowledge Execution Architecture (H1)
**Domain:** Negotiation — Strategy Execution
**Date:** 2026-07-15
**Status:** CANONICAL
**Prerequisite:** Heritage Gold NEGOTIATION_MODEL.md §6 (Price Negotiation), RULE_INDEX.md (NEGO-008, NEGO-012, NEGO-013, NEGO-014)

---

## 1. Price Negotiation Expressions

Expressions extracted from Heritage Gold, mapped to detectable keywords and response strategies.

| Expression | Code | Detection Keywords | Meaning | Response Strategy |
|------------|------|-------------------|---------|-------------------|
| **Prix ferme** | `PRIX_FERME` | ferme, fixe, non-négociable, final | Fixed price, no negotiation | Explain rationale, propose alternative properties if budget mismatch |
| **À débattre** | `A_DEBATTRE` | débattre, discuter, voir, proposer, offre | Open to negotiation | Elicit buyer's offer, counter with market context |
| **Dernier prix** | `DERNIER_PRIX` | dernier prix, last price, final offer | Buyer seeking floor price | Give price in context (market + history), explain margin, no aggressive closing |
| **Prix négociable** | `PRIX_NEGO` | négociable, negotiable, marge, arrangement | Negotiation expected | Confirm margin range, propose discussion, elicit offer |

### 1.1 Expression Detection Rules

| Expression | Confidence | Required Context |
|------------|-----------|-----------------|
| `PRIX_FERME` | HIGH (explicit keyword match) | Property price, seller confirmation |
| `A_DEBATTRE` | MEDIUM (may be implicit) | Property state, market data |
| `DERNIER_PRIX` | HIGH (buyer signal) | Buyer profile, price history |
| `PRIX_NEGO` | MEDIUM (may be explicit or implicit) | Seller profile, margin range |

### 1.2 Six Price Levels (from NEGOTIATION_MODEL §6.1)

| Level | Definition | Storage | Usage |
|-------|-----------|---------|-------|
| **Prix affiché** | Published listing price | `property.price_display` | Point de départ visible |
| **Prix négociable** | Real negotiation margin | `property.negotiable_range` | To determine with seller |
| **Prix final** | Effective transaction price | `negotiation.final_price` | Result of negotiation |
| **Prix estimation** | Estimated market price | `market.estimated_price` | To advise seller |
| **Fourchette de prix** | High-low interval | `search.price_range` | To frame search |
| **Prix historique** | Historical prices | `property.price_history` | To justify evolution |

---

## 2. Negotiation State Machine

```
                     ┌──────────────────────────────────────────────────────────┐
                     │                  NEGOTIATION LIFECYCLE                    │
                     │         (05-WORKFLOW-REFERENCE Part 7 Ch109-127)         │
                     └──────────────────────────────────────────────────────────┘

                              PROPOSED
                                 │
                                 ▼
                            DISCUSSION
                                 │
                                 ▼
                              COUNTER
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
                    ▼            ▼            ▼
                 ACCEPTED    REJECTED    RENEGOTIATE
                    │            │            │
                    ▼            │            │
              FINAL_AGREEMENT    │            │
                    │            │            │
                    ▼            ▼            ▼
              TRANSACTION    FAILURE      COUNTER (new cycle)
                                 │
                                 ▼
                           REMATCHING
```

### 2.1 State Definitions

| State | Code | Description | Entry Condition |
|-------|------|-------------|-----------------|
| **Proposed** | `PROPOSED` | Initial offer submitted | Positive visit OR both parties agree to negotiate |
| **Discussion** | `DISCUSSION` | Parties exchanging views | Offer submitted, response pending |
| **Counter** | `COUNTER` | Counter-offer submitted | Party responds with modified terms |
| **Accepted** | `ACCEPTED` | Agreement in principle | Both parties agree on price and terms |
| **Rejected** | `REJECTED` | Offer refused without counter | Clear refusal signal |
| **Renegotiate** | `RENEGOTIATE` | New offer cycle started | Gap exists but parties willing to continue |
| **Final agreement** | `FINAL_AGREEMENT` | Binding agreement reached | Signed agreement or confirmed commitment |
| **Transaction** | `TRANSACTION` | Transaction in progress | Payment initiated |
| **Failure** | `FAILURE` | Negotiation ended without agreement | No further engagement possible |

### 2.2 State Transitions

| From | To | Trigger | Condition |
|------|----|---------|-----------|
| PROPOSED | DISCUSSION | Offer submitted | Valid offer data present |
| DISCUSSION | COUNTER | Counter-offer received | Counter differs from original |
| DISCUSSION | ACCEPTED | Offer accepted | Explicit acceptance |
| DISCUSSION | REJECTED | Offer refused | Clear refusal, no counter |
| COUNTER | ACCEPTED | Counter accepted | Acceptance signal |
| COUNTER | REJECTED | Counter refused | Refusal signal |
| COUNTER | RENEGOTIATE | New counter proposed | Gap remains, engagement continues |
| ACCEPTED | FINAL_AGREEMENT | Terms confirmed | Both parties confirm |
| FINAL_AGREEMENT | TRANSACTION | Payment process starts | Agreement signed |
| REJECTED | FAILURE | No further action | Max attempts exceeded |
| RENEGOTIATE | COUNTER | New proposal made | Engagement continues |
| FAILURE | REMATCHING | System action | Post-failure diagnostic |

### 2.3 Negotiable Elements (per transaction type)

| Transaction Type | Negotiable Elements |
|-----------------|-------------------|
| **Sale (Vente)** | Price, payment terms, deadlines, included furniture, equipment, release date |
| **Rental (Location)** | Rent, deposit, advance, lease duration, entry date, possible works |
| **Land (Terrain)** | Price, boundary marking, documents, deadlines |
| **Commercial** | Rent, key money, equipment, duration |

---

## 3. Strategy per Buyer Profile

**NEGO Reference:** NEGO-001 (4 buyer profiles), NEGO-005 (LAWIM arguments), NEGO-006 (property arguments), NEGO-009 (tone per profile), NEGO-010 (trust sequence)

### 3.1 National Buyer

| Aspect | Strategy |
|--------|----------|
| **Primary argument** | Proximity to work/family/school, accessibility, living environment |
| **Price approach** | Compare with neighborhood market, emphasize value for money |
| **Objection response** | Family involvement (cousin, parent) → respect timeline, keep active |
| **Tone** | Patient, pédagogique, rassurant |
| **Closing** | Visit-based closing, family visit encouraged |
| **Key leverage** | Cash payment discount, proximity argument |

**Strategy FR:**
```
Ce bien est idéalement situé près de [école/marché/transport].
Dans ce quartier, les biens comparables se vendent entre [X] et [Y].
Je vous propose une visite pour vous faire votre propre avis.
```

### 3.2 Diaspora Buyer

| Aspect | Strategy |
|--------|----------|
| **Primary argument** | Security, ROI, document verification, structured reports |
| **Price approach** | Emphasize ROI, property appreciation potential, secured payment |
| **Objection response** | Distant trust → proof before commitment, video visit, GPS reports |
| **Tone** | Structured, transparent, patient |
| **Closing** | Diaspora trust journey step-by-step, secured escrow payment |
| **Key leverage** | Document verification before proposal, local correspondent |

**Strategy FR (ROI-focused):**
```
Ce bien présente un potentiel de rendement locatif de [X]% par an.
Dans [quartier], les prix ont augmenté de [Y]% sur les 3 dernières années.
Je vous propose un rapport complet avec photos, vidéo et vérification documentaire.
```

**Strategy EN:**
```
This property offers a rental yield potential of [X]% per year.
In [neighborhood], prices have increased by [Y]% over the last 3 years.
I propose a complete report with photos, video, and document verification.
```

### 3.3 Investor

| Aspect | Strategy |
|--------|----------|
| **Primary argument** | ROI, rentabilité, plus-value, market data, matching intelligent |
| **Price approach** | Data-driven: market comparables, yield calculations, projection |
| **Objection response** | Technical questions → data, projections, market analysis |
| **Tone** | Technique, chiffré, professionnel |
| **Closing** | Document-based: title deed verification, notary accompaniment |
| **Key leverage** | Rental yield data, market tension index, appreciation history |

**Strategy FR:**
```
Analyse du bien :
• Prix : [X] FCFA
• Loyer estimé : [Y] FCFA/mois
• Rendement brut : [Z]%
• Tension marché dans le quartier : [indice]/100
• Appréciation 3 ans : [W]%

Souhaitez-vous que je prépare le dossier de vérification ?
```

### 3.4 Young Professional

| Aspect | Strategy |
|--------|----------|
| **Primary argument** | Primo-accession, budget maîtrisé, WhatsApp, accompagnement |
| **Price approach** | Budget-friendly options, payment flexibility, explain total cost |
| **Objection response** | Budget concerns → alternative options, progressive budget expansion |
| **Tone** | Encouraging, pédagogique, digital-native |
| **Closing** | Simple, fast, digital-first; WhatsApp-based closing |
| **Key leverage** | Zero commission (significant for first purchase), matching intelligence |

**Strategy FR:**
```
Premier achat ? LAWIM vous accompagne de A à Z pour seulement 50 000 FCFA.
Pas de commission cachée — vous payez le prix que vous voyez.
Voici 3 biens dans votre budget à [ville] :
```

---

## 4. Strategy per Seller Profile

**NEGO Reference:** NEGO-002 (3 seller profiles), NEGO-004 (seller fears), NEGO-005 (LAWIM arguments), NEGO-009 (tone per profile)

### 4.1 Individual Seller

| Aspect | Strategy |
|--------|----------|
| **Primary concern** | Trust, fair price, serious buyer |
| **Argument** | Mise en relation directe, réseau agents vérifiés |
| **Price approach** | Market estimation + historical data to justify recommended price |
| **Tone** | Patient, rassurant, transparent |
| **Key leverage** | Qualification des acheteurs, visites ciblées |

### 4.2 Developer (Promoteur)

| Aspect | Strategy |
|--------|----------|
| **Primary concern** | Speed, volume, rotation |
| **Argument** | Matching intelligent, zéro commission, visibilité |
| **Price approach** | Competitive positioning, bulk listing options |
| **Tone** | Professional, efficient, results-oriented |
| **Key leverage** | Number of qualified buyers, match rate statistics |

### 4.3 Landlord (Bailleur)

| Aspect | Strategy |
|--------|----------|
| **Primary concern** | Tenant quality, rent regularity, management |
| **Argument** | Accompagnement, mise en relation, agent verification |
| **Price approach** | Market rent analysis, tenant solvency focus |
| **Tone** | Expert, rentabilité, conseil |
| **Key leverage** | Tenant qualification, rental guarantee |

---

## 5. Signal Detection and Handling

### 5.1 Urgency Signals (NEGO-012)

| Signal | Keywords | Priority Impact | Response |
|--------|----------|----------------|----------|
| **Véritable urgence** | urgent, asap, vite, immédiat, besoin maintenant, date butoir | P0/P1 escalation | Fast-track matching, immediate visit proposal, priority processing |
| **Urgence artificielle** | last chance, aujourd'hui seulement, limited offer | Flag as suspicious | Verify legitimacy, do not create false pressure |

**Detection:**
```
TRUE_URGENCY keywords: urgent, asap, vite, immédiat, date butoir, avant [date]
ARTIFICIAL_URGENCY keywords: today only, last chance, limited, dépêchez-vous
Pattern: Real urgency = specific deadline + concrete action context
         Artificial urgency = vague time pressure + no specific deadline
```

**Response to real urgency:**
```
FR: Je comprends l'urgence. Je priorise votre dossier et vous propose les biens disponibles immédiatement dans [ville].
Souhaitez-vous une visite dans les prochaines 24h ?

EN: I understand the urgency. I prioritize your dossier and propose immediately available properties in [city].
Would you like a visit within the next 24 hours?
```

### 5.2 Investor Signals (NEGO-013)

| Signal | Keywords | Profile Impact | Data Sent |
|--------|----------|----------------|-----------|
| **Investor intent** | investir, investissement, placement | Profile → INVESTOR (score +80) | Rentabilité, ROI, plus-value, tension marché |
| **ROI focus** | rentable, ROI, rendement, rentabilité | Profile → INVESTOR | Yield projections, comparables |
| **Portfolio** | portefeuille, patrimoine, diversification | Profile → INVESTOR | Market analysis, portfolio suggestions |

**Detection confidence matrix:**
| Signal | Single Occurrence | Repeated (2+) | With budget > 50M |
|--------|------------------|---------------|-------------------|
| investir | MEDIUM | HIGH | HIGHEST |
| rentable | MEDIUM | HIGH | HIGHEST |
| ROI | MEDIUM | HIGH | HIGHEST |
| rendement | LOW | MEDIUM | HIGH |

### 5.3 Diaspora Signals (NEGO-014)

| Signal | Keywords | Profile Impact | Action |
|--------|----------|----------------|--------|
| **Self-identification** | diaspora, je vis à l'étranger, je suis à | Profile → DIASPORA | Initiate 7-step trust journey |
| **Foreign location** | à Paris, en France, en Europe, à Londres, USA, Canada | Profile → DIASPORA | Language adaptation (EN/FR) |
| **Foreign dial code** | +33, +1, +44, +49, +32, +41 | Profile → DIASPORA | Document verification before proposal |
| **Money transfer** | transfert, envoyer, Western Union, MoneyGram | Profile → DIASPORA | Secured payment proposal |

**13 diaspora locations (from diaspora_filter.py):** France, UK, USA, Canada, Germany, Belgium, Switzerland, Italy, Spain, South Africa, UAE, China, other African countries

**4 dial codes:** +33 (France), +1 (US/Canada), +44 (UK), +49 (Germany)

**Diaspora response:**
```
FR: Je comprends que vous êtes à l'étranger. LAWIM a conçu un service spécial diaspora :
    • Vérification documentaire avant toute proposition
    • Visite vidéo en direct du bien
    • Rapports avec photos, vidéos et localisation GPS
    • Paiement sécurisé et échelonné
    • Correspondant local pour les visites
```

---

## 6. Escalation Criteria

The system escalates to human negotiation when automated negotiation cannot resolve the situation.

| Level | Condition | Escalation Action | Target |
|-------|-----------|-------------------|--------|
| **L1** | Price gap > 20% after 3 exchanges | Offer human negotiator | LAWIM Conseiller |
| **L2** | Legal/document dispute | Redirect to notary | Notaire partenaire |
| **L3** | Fraud suspicion (any SEC signal) | Suspend + alert security | LAWIM Administrateur |
| **L4** | Repeated impasse (5+ counters) | Human mediator assigned | Médiateur LAWIM |
| **L5** | User explicitly demands human | Transfer immediately | Conseiller LAWIM |
| **L6** | User requests data deletion | Execute RGPD workflow | Automated (7-day delay) |

### 6.1 Escalation State Machine

```
AUTO_NEGOTIATION (active)
    │
    ├── Escalation condition met → ESCALATION_REQUESTED
    │       │
    │       ├── Human accepts → HUMAN_NEGOTIATION
    │       │       │
    │       │       ├── Resolved → COMPLETED
    │       │       └── Unresolved → MEDIATION
    │       │
    │       └── Human unavailable → SYSTEM_HOLD (re-evaluate in 24h)
    │
    └── No escalation condition → Continue AUTO_NEGOTIATION
```

### 6.2 Escalation Message

**FR:**
```
Je vous propose de mettre un conseiller LAWIM en contact avec vous pour discuter de ce dossier plus en détail.
[Conseiller] pourra vous aider à trouver la meilleure solution.

Souhaitez-vous que je transmette votre dossier ?
```

**EN:**
```
I suggest connecting you with a LAWIM advisor to discuss this matter in more detail.
[Advisor] will help you find the best solution.

Would you like me to transfer your dossier?
```

---

## 7. Cultural Dynamics Reference

From Heritage Gold NEGOTIATION_MODEL §6.3 — Applied in automated negotiation:

| Cultural Rule | Implementation |
|---------------|---------------|
| Le vendeur fixe un prix ambitieux | Assume negotiation margin in displayed price |
| Le vendeur attend la première offre | Do not demand seller's floor price upfront |
| Remise pour transaction rapide | Offer discount lever for quick cash payment |
| Offre basse = ouverture | Treat low offers as entry point, not insult |
| L'acheteur négocie tôt | Prepare for price discussion from first contact |
| Contre-offre = test | Counter-offers are often still negotiable |
| Preuve comme levier | Use comparables to justify price position |

---

## References

| Source | Section |
|--------|---------|
| Heritage Gold NEGOTIATION_MODEL.md | §6 Price Negotiation, §6.3 Cultural Dynamics, §7 Diaspora |
| Heritage Gold RULE_INDEX.md | NEGO-008, NEGO-012, NEGO-013, NEGO-014 |
| 05-WORKFLOW-REFERENCE.md | Part 7 (Negotiation Lifecycle Ch109-127) |
| 04-DECISION-ENGINE-REFERENCE.md | Ch88 (Decision Priority), Ch90 (Transaction Success Score) |
| knowledge_unified/commercial/negotiation_techniques.md | Cameroon market negotiation techniques |
| knowledge_unified/commercial/objection_handling.md | Price objections (#1, #2, #3) |
| negotiation.json | Price expressions data |
| investor_intent.json | Investor/diaspora signal patterns |
| conversation-patterns.md | Urgency signal patterns |
