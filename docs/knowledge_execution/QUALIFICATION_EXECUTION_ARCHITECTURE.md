# QUALIFICATION EXECUTION ARCHITECTURE — Moteur de Qualification LAWIM V5

**Mission :** LAWIM Heritage Gold
**Statut :** Architecture Validée — Standard d'implémentation pour le moteur de qualification
**Références :** QUALIFICATION_MODEL.md, RULE_INDEX.md (QUAL-001 à QUAL-019), DOMAIN_MODEL.md

---

## 1. Pipeline de Qualification V5 (8 étapes)

Pipeline séquentiel conforme à QUAL-006 :

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ 1.       │───→│ 2.       │───→│ 3.       │───→│ 4.       │
│ incoming │    │ normalize│    │ extract  │    │detect    │
│ _message │    │ _text    │    │ _entities│    │ _intent  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     │                                               │
     ↓                                               ↓
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ 5.       │───→│ 6.       │───→│ 7.       │───→│ 8.       │
│ context  │    │ lead     │    │ lead     │    │ crm      │
│enrichment│    │ _scoring │    │classification│  │ _routing │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
```

### 1.1 Étapes détaillées

| Étape | Entrée | Sortie | Responsabilité | Règles QUAL |
|-------|--------|--------|----------------|-------------|
| 1. `incoming_message` | Message brut (WhatsApp/Telegram/Dashboard) | `raw_message` structuré | Réception, canal detection, métadonnées (timestamp, source, session_id) | — |
| 2. `normalize_text` | `raw_message` | `normalized_text` | Nettoyage (typo, WhatsApp shortcuts, pidgin), normalisation orthographique, détection de langue | LANG-005, LANG-006, LANG-007 |
| 3. `extract_entities` | `normalized_text` | `extracted_fields` | Extraction de 25 USER_FIELDS (QUAL-010) : ville, quartier, budget, type_bien, surface, pieces, etage, urgence, cash, nom, telephone, email | QUAL-010, QUAL-011 |
| 4. `detect_intent` | `extracted_fields` | `intent` + `role` | Classification d'intention : RENT/BUY/SELL/INVESTOR. Mapping → rôle cible (QUAL-008). Détection multi-intention. | QUAL-008, QUAL-019 |
| 5. `context_enrichment` | `intent` + `extracted_fields` | `enriched_context` | Historique conversation (CONV-010), mémoire long terme (CONV-013), satisfaction précédente (CONV-015), préférences persistées | CONV-010, CONV-013, CONV-015 |
| 6. `lead_scoring` | `enriched_context` | `score` + `temperature` | Calcul score composite : base + boosters − pénalités. Puis normalisation V5. | QUAL-001, QUAL-002, QUAL-003, QUAL-005, QUAL-017 |
| 7. `lead_classification` | `score` | `classification` (HOT/WARM/COLD/SPAM) | Application des seuils V5 (QUAL-005), priorité P0-P3 (QUAL-018), température | QUAL-004, QUAL-005, QUAL-018 |
| 8. `crm_routing` | `classification` | `route` + `response` | Routage CRM, escalade humaine, file d'attente agent, génération réponse | QUAL-009, QUAL-015 |

### 1.2 Architecture composants internes

```
QualificationEngine
 ├── Normalizer (typo, shortcuts, lang detection)
 ├── EntityExtractor (NER, regex patterns, fuzzy matching)
 ├── IntentClassifier (LLM + rule-based fallback)
 ├── ContextEnricher (session, history, long-term memory)
 ├── ScoringEngine (base + boosters + penalties + weights)
 ├── Classifier (threshold gates → HOT/WARM/COLD/SPAM)
 ├── ReadinessCalculator (completeness → stages)
 ├── NextQuestionSelector (policy-based question picking)
 └── ResponseBuilder (channel-adaptive output)
```

---

## 2. Ordre de Qualification (10 étapes)

Ordre strict conforme à QUAL-007. Toutes les conversations suivent cette séquence :

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  1.         │────→│  2.         │────→│  3.         │────→│  4.         │
│ Intention   │     │ Type bien   │     │ Ville       │     │ Quartier    │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
     ↓                                                           ↓
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  5.         │────→│  6.         │────→│  7.         │────→│  8.         │
│ Budget      │     │ Délai       │     │ Critères    │     │ Préférences │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
     ↓                                                           ↓
┌─────────────┐     ┌─────────────┐
│  9.         │────→│ 10.         │
│ Confirmation│     │ Escalade    │
└─────────────┘     └─────────────┘
```

### 2.1 Détail des étapes

| # | Étape | Champs collectés | Canaux | Condition de progression |
|:-:|-------|------------------|--------|--------------------------|
| 1 | Intention | `intent` (RENT/BUY/SELL/INVESTOR) | Tous | Intent détectée avec confiance ≥ 0.70 |
| 2 | Type bien | `property_type` (studio/apartment/house/villa/duplex/land/commercial) | Tous | Type bien identifié |
| 3 | Ville | `city` | Tous | Ville reconnue dans inventory |
| 4 | Quartier | `neighborhood` | WhatsApp/Telegram | Ville connue ET quartier optionnel |
| 5 | Budget | `budget_min`, `budget_max`, `budget_type` (achat/mensuel) | Tous | Budget clair ou tolérance définie |
| 6 | Délai | `urgency`, `timeline` (urgent/1mois/3mois/flexible) | Tous | Temporalité exprimée |
| 7 | Critères | `surface`, `rooms`, `floor`, `parking`, `furnished`, `bedrooms` | Tous | Type bien connu |
| 8 | Préférences | `exposure`, `standing`, `animals`, `additional_features` | WhatsApp/Telegram | Critères de base collectés |
| 9 | Confirmation | Validation utilisateur du résumé | Tous | Résumé généré et présenté |
| 10 | Escalade | Décision : résultats/rendez-vous/transfert | Tous | Confirmation reçue |

### 2.2 Détection multi-intention

Un message peut exprimer plusieurs intentions (ex: "je veux acheter une maison et aussi investir dans un terrain"). Traitement :

1. **Extraction** : NER extrait tous les couples `(intent, property_type, location, budget)` distincts
2. **Scoring** : Chaque intention reçoit un score de confiance indépendant
3. **Priorisation** : L'intention avec le score le plus élevé est primaire
4. **Stockage** : Les intentions secondaires sont conservées dans `secondary_intents[]`
5. **Rebond** : La qualification principale terminée, le système propose de traiter l'intention secondaire

| Règle | Description | Source |
|-------|-------------|--------|
| `intent_primary` | Intention avec confiance max = intention active | QUAL-008 |
| `intent_secondary` | Intentions additionnelles stockées pour reprise | — |
| `intent_switch` | Changement d'intention → réinitialisation partielle, reprise étape 1 | QUAL-014, QUAL-015 |

### 2.3 Détection multi-intention — architecture de décision

```
multi_intent_detector(message)
 ├── extract all (intent, property_type, location, budget) pairs
 ├── score each pair independently
 ├── sort by confidence descending
 ├── if top confidence >= 0.70:
 │     set primary_intent = top
 │     set secondary_intents = remaining (confidence >= 0.40)
 │     store in session.secondary_intents
 └── if only one intent >= 0.70:
       standard single-intent qualification
```

---

## 3. Consommation des règles QUAL-001 à QUAL-019

### 3.1 Mapping règles → composants

| Rule ID | Composant | Comportement |
|---------|-----------|--------------|
| QUAL-001 | ScoringEngine → BaseScoreProvider | Assigne tenant=40, buyer=60, seller=50, investor=80, diaspora_investor=95 |
| QUAL-002 | ScoringEngine → BoosterProvider | +15 budget_detected, +10 city_detected, +10 neighborhood_detected, +20 urgent_request, +25 diaspora_detected, +15 cash_purchase |
| QUAL-003 | ScoringEngine → PenaltyProvider | −10 missing_budget, −10 unclear_location, −50 spam_like_message |
| QUAL-004 | Classifier → ThresholdGateV1 | Legacy : HOT≥80, WARM≥60, COLD≥40, LOW<40 |
| QUAL-005 | Classifier → ThresholdGateV5 | Production : HOT≥0.8, WARM≥0.5, COLD≥0.3, SPAM≤0.2 |
| QUAL-006 | QualificationEngine → PipelineOrchestrator | 8 étapes (incoming→normalize→extract→detect_intent→context→scoring→classification→routing) |
| QUAL-007 | QualificationEngine → StepSequencer | 10 étapes qualification (Intention→...→Escalade) |
| QUAL-008 | IntentClassifier → RoleMapper | RENT→tenant, BUY→buyer, SELL→seller, INVESTOR→investor/diaspora_investor |
| QUAL-009 | ResponseBuilder | call_immediately, send_listings, request_budget, follow_up, ignore |
| QUAL-010 | EntityExtractor → KnowledgeBuilder | 25 USER_FIELDS extraits |
| QUAL-011 | EntityExtractor → LeadFieldBuilder | 10 LEAD_FIELDS : message, intent, budget, location, property_type, urgency, score, status, priority, diaspora_flag |
| QUAL-012 | ContextEnricher → BehaviorTracker | 4 comportements : message_history, response_time, budget_changes, visit_requests |
| QUAL-013 | NextQuestionSelector → ChannelAdapter | WhatsApp : 1 message/question. Telegram : 2-3 champs/message |
| QUAL-014 | NextQuestionSelector → SupersessionEngine | Pas de redemande, pas de redémarrage, correction écrase contexte |
| QUAL-015 | PipelineOrchestrator → StopCondition | Arrêt si ville non couverte, inventaire vide, demande humain, 3 échanges sans progression |
| QUAL-016 | EntityExtractor → DiasporaDetector | 13 localisations + 4 indicatifs → diaspora_flag |
| QUAL-017 | ScoringEngine → CompositeScorer | budget=20%, location=15%, urgency=20%, diaspora=10%, phone=5%, property_type=15%, investment_profile=10% |
| QUAL-018 | Classifier → PriorityMapper | P0(100-95), P1(90-85), P2(75-60), P3(40) |
| QUAL-019 | IntentClassifier → ExtendedRoleMapper | Types additionnels : property_seeker, agent, owner, broker |

### 3.2 Exécution conditionnelle des règles

Chaque règle est exécutée seulement si sa condition de déclenchement est remplie :

```
rule_executor:
  load rule (QUAL-XXX)
  evaluate preconditions
  if all preconditions met:
    execute rule action
    log execution with confidence
    update lead state
  else:
    skip rule (log with reason)
```

---

## 4. Stratégie de Qualification Progressive

Conforme à QUAL-013 et QUAL-014. Principe : ne jamais submerger l'utilisateur.

### 4.1 Adaptation par canal

| Canal | Règle | Comportement |
|-------|-------|-------------|
| **WhatsApp** | 1 question par message | Une seule information demandée par message. Maximum 3 messages consécutifs avant pause. |
| **Telegram** | 2-3 champs par message | Groupe les questions connexes. Exemple : "Quel type de bien cherchez-vous et dans quelle ville ?" |
| **Dashboard** | Formulaire structuré | Affiche tous les champs manquants dans une interface structurée, validation par champ. |

### 4.2 Règles de progression

| Règle | Implémentation |
|-------|----------------|
| **Pas de redemande** | Chaque champ collecté est marqué `asked=false` dans le plan de questions. Vérification avant chaque envoi. |
| **Pas de redémarrage** | L'étape de qualification est persistée en session. Jamais remise à zéro sauf sur changement d'intention. |
| **Correction prioritaire** | Toute valeur corrective reçue écrase immédiatement la valeur précédente. Le plan de questions est recalculé. |
| **Extraction continue** | Même sans question explicite, tout message est analysé. Si un champ est extrait, il est marqué collecté. |

### 4.3 Conditions d'arrêt (QUAL-015)

| Condition | Détection | Action |
|-----------|-----------|--------|
| Ville non couverte | GEO-002 (10 villes prioritaires) | Stop qualification, message "Nous ne couvrons pas encore cette ville" |
| Inventaire vide | Aucun bien disponible pour les critères | Stop qualification, proposer alternatives |
| Demande humain | Message contenant "parler à un conseiller", "humain", etc. | Escalade immédiate |
| Thread répétitif | 3 échanges consécutifs sans progression (aucun nouveau champ) | Stop, offrir alternatives ou escalade |
| Changement d'intention | Nouvel intent détecté avec confiance > intention active | Réinitialisation partielle, reprise étape 1 |

---

## 5. Intégration Anti-Fraude

Conforme à QUAL-003 (pénalité spam) et SEC-004.

### 5.1 Architecture anti-fraude

```
AntiFraudEngine
 ├── Layer 1: BrokerSpamDetector
 │     Détection : messages type courtier non sollicités
 │     Action : penalty −50, flag `manual_review`
 │
 ├── Layer 2: DuplicateDetector
 │     Détection : même bien/même requête postée plusieurs fois
 │     Action : déduplication, avertissement
 │
 ├── Layer 3: FakePriceDetector
 │     Détection : prix anormalement bas ou haut (écart > 3σ de la médiane)
 │     Action : flag `price_verification`, réduction poids budget
 │
 └── Layer 4: UrgencyValidator
       Détection : urgence artificielle (pression temporelle sans fondement)
       Action : réduction poids urgency_signal de 50%
```

### 5.2 Intégration dans le pipeline

| Étape pipeline | Action anti-fraude |
|----------------|-------------------|
| normalize_text | Layer 1 : détection spam lexical |
| extract_entities | Layer 2 : déduplication entités |
| lead_scoring | Layer 3 : fake price → ajustement budget score |
| lead_classification | Layer 4 : urgency validation → ajustement température |

---

## 6. Température du Lead (HOT/WARM/COLD/SPAM)

### 6.1 Calcul de la température

```
temperature = normalize(lead_score)  → [0.0, 1.0]

lead_score = base_score + sum(boosters) + sum(penalties)
```

Où :
- `base_score` = score de base du rôle (QUAL-001)
- `boosters` = somme des bonus applicables (QUAL-002)
- `penalties` = somme des malus applicables (QUAL-003)

### 6.2 Normalisation V5

```
normalized_score = clamp(lead_score / 100.0, 0.0, 1.0)
```

### 6.3 Seuils de classification

| Température | Seuil V5 | Priorité | Action | Comportement CRM |
|-------------|:--------:|:--------:|--------|------------------|
| **HOT** | ≥ 0.80 | P0-P1 | `call_immediately` | Notification immédiate agent, SMS prioritaire |
| **WARM** | ≥ 0.50 | P2 | `send_listings` | Envoi des matching disponibles, relance J1 |
| **COLD** | ≥ 0.30 | P3 | `request_budget` | Demande budget, qualification complémentaire |
| **SPAM** | ≤ 0.20 | — | `ignore` | Archive silencieuse, pas de réponse |

### 6.4 Exemples de calcul

| Profil | Base | Boosters | Pénalités | Score brut | Normalisé | Classe |
|--------|:----:|:--------:|:---------:|:----------:|:---------:|:------:|
| Acheteur Douala, budget 50M, urgent | 60 | +10(city) +15(budget) +20(urgent)=+45 | 0 | 105 | 1.0 | HOT |
| Locataire Yaoundé, sans budget | 40 | +10(city)=+10 | −10(missing_budget)=−10 | 40 | 0.40 | COLD |
| Message "je vends ma villa" | 50 | 0 | 0 | 50 | 0.50 | WARM |
| "Achat appartement Paris, budget 200k€, urgent" | 95 | +10(city) +15(budget) +20(urgent) +25(diaspora)=+70 | 0 | 165 | 1.0 | HOT |
| "Appart pas cher stp" | 60 | 0 | −10(unclear_location)=−10 | 50 | 0.50 | WARM |
| "vendez moi maison" (courtier suspect) | 60 | 0 | −50(spam)=−50 | 10 | 0.10 | SPAM |

---

## 7. Moteur de Scoring

### 7.1 Architecture du ScoringEngine

```
ScoringEngine
 ├── BaseScoreProvider        → QUAL-001 : role → base score
 ├── BoosterProvider          → QUAL-002 : signals → bonuses
 ├── PenaltyProvider          → QUAL-003 : issues → malus
 ├── CompositeScorer          → QUAL-017 : weighted factors
 ├── Normalizer               → QUAL-005 : scale to [0.0, 1.0]
 └── ClassifierOutput         → temperature + priority
```

### 7.2 Scores de base (QUAL-001)

| Rôle | Score de base |
|------|:------------:|
| tenant | 40 |
| buyer | 60 |
| seller | 50 |
| investor | 80 |
| diaspora_investor | 95 |

### 7.3 Boosters (QUAL-002)

| Signal | Bonus | Condition de déclenchement |
|--------|:-----:|---------------------------|
| `budget_detected` | +15 | Budget extrait et validé (chiffres + devise ou plage) |
| `city_detected` | +10 | Ville reconnue dans GEO-002 |
| `neighborhood_detected` | +10 | Quartier valide pour la ville |
| `urgent_request` | +20 | Expression temporelle "urgent", "asap", "rapidement", "tout de suite" |
| `diaspora_detected` | +25 | QUAL-016 : localisation ou indicatif diaspora |
| `cash_purchase` | +15 | Mention "cash", "comptant", "pas de crédit" |

### 7.4 Pénalités (QUAL-003)

| Signal | Malus | Condition de déclenchement |
|--------|:-----:|---------------------------|
| `missing_budget` | −10 | Aucun budget exprimé après 2 relances |
| `unclear_location` | −10 | Localisation ambiguë ou non reconnue |
| `spam_like_message` | −50 | Pattern courtier, message générique, lien suspect |

### 7.5 Facteurs pondérés CRM V5 (QUAL-017, CRM-014)

| Facteur | Poids | Contribution au score |
|---------|:-----:|----------------------|
| `base_interest` | 0.15 | Intérêt de base exprimé |
| `property_type_match` | 0.20 | Correspondance type de bien |
| `location_precision` | 0.20 | Précision localisation (ville + quartier) |
| `budget_presence` | 0.10 | Présence et clarté du budget |
| `urgency_signal` | 0.15 | Signal d'urgence |
| `visit_intent` | 0.20 | Intention de visite exprimée |
| `trust_signal` | 0.10 | Signal de confiance |

### 7.6 Scores de priorité (QUAL-018)

| Priorité | Plage score | Délai de réponse cible |
|:--------:|:-----------:|------------------------|
| P0 | 100-95 | Immédiat (< 5 min) |
| P1 | 90-85 | < 30 min |
| P2 | 75-60 | < 2h |
| P3 | 40 | < 24h |

---

## 8. Calcul de Readiness (Complétude)

### 8.1 Principe

Le Readiness Score mesure le niveau de complétude de la qualification. Il détermine quelles actions sont possibles (search, matching, visit).

### 8.2 Formule

```
readiness_stage = f(completeness_pct)

completeness_pct = (collected_required + collected_recommended * 0.5) /
                   (total_required + total_recommended * 0.5) * 100
```

### 8.3 Seuils de readiness

| Stage | Seuil | Action possible | Comportement |
|-------|:-----:|----------------|--------------|
| **SEARCH_READY** | ≥ 40% | Recherche de biens correspondants | Déclenchement matching précoce (GOLD-DM-014, P5) |
| **MATCHING_READY** | ≥ 65% | Envoi de résultats de matching | Comparaison complète avec scoring pondéré |
| **VISIT_READY** | ≥ 85% | Proposition de visite | Qualification suffisante pour prise de rendez-vous |
| **RELATIONSHIP_READY** | 100% | Transfert à un agent/relation client | Qualification complète, escalade possible |

### 8.4 Intégration pipeline

```
ReadinessCalculator
 ├── Input : current qualified fields + role profile
 ├── Compute : completeness_pct
 ├── Map to stage : SEARCH_READY / MATCHING_READY / VISIT_READY / RELATIONSHIP_READY
 └── Output : readiness_stage + missing_critical_fields
```

---

## 9. Politique de Sélection de la Prochaine Question

### 9.1 Algorithme

```
next_question(qualified_context):
  missing = get_missing_fields(qualified_context)
  forbidden = get_forbidden_questions(qualified_context)  // QUAL-014
  deductible = get_deductible_fields(qualified_context)   // GOLD-DM-012, P3
  
  candidates = missing - forbidden - deductible
  
  if no candidates:
    if readiness >= MATCHING_READY:
      return PROPOSE_MATCHING
    else:
      return STOP_QUALIFICATION
  
  priority = sort_by_qualification_order(candidates)  // QUAL-007
  channel = detect_channel(qualified_context)
  batch = apply_channel_batching(priority, channel)   // QUAL-013
  
  return build_response(batch)
```

### 9.2 Détail dans NEXT_QUESTION_POLICY.md

Voir le document dédié pour la spécification complète de la politique de sélection, les templates, l'adaptation par canal, et la gestion d'ambiguïté.

---

---

## 10. NBA Integration

After qualification completes, the Decision Engine selects the Next Best Action (NBA) based on readiness stage and lead classification:

| Readiness Stage | Classification | NBA |
|-----------------|---------------|-----|
| SEARCH_READY | Any | `search.match` — begin matching with available criteria |
| MATCHING_READY | HOT/WARM | `search.match` — proceed to full matching |
| MATCHING_READY | COLD | `qualify.continue` — collect more data before matching |
| VISIT_READY | HOT | `search.match` → `schedule_visit` — prioritize visit scheduling |
| RELATIONSHIP_READY | Any | `relationship.introduce` — initiate mise en relation |

NBA is recalculated after each qualification step via the NBA Trigger (see WORKFLOW_EXECUTION_ARCHITECTURE.md §1.7).

---

*Document Architecture Gold — 2026-07-15 — Référence complète QUAL-001 à QUAL-019, GOLD-DM-001 à GOLD-DM-096.*
