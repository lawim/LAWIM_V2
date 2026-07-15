# NEXT QUESTION POLICY — Politique de Sélection de la Prochaine Question

**Mission :** LAWIM Heritage Gold
**Statut :** Politique validée — Définit comment et quand le système pose des questions
**Références :** QUALIFICATION_MODEL.md §5, §8, RULE_INDEX.md QUAL-007, QUAL-013, QUAL-014, DOMAIN_MODEL.md GOLD-DM-010 à GOLD-DM-017

---

## 0. H0.5 Integration Layer — Data-Driven Question Selection

### 0.1 H0.5 Data Sources

The Next Question Policy is driven by four H0.5 data sources:

| Source | Usage | Location |
|--------|-------|----------|
| `field_dictionary.json` | Field definitions, validation rules, question templates, matching roles, privacy levels | `docs/lawim_heritage_gold/qualification_matrices/field_dictionary.json` |
| `readiness_rules.json` | Current readiness level, blocking conditions, allowed/forbidden actions per level | `docs/lawim_heritage_gold/qualification_matrices/readiness_rules.json` |
| `question_rules.json` | Conditional ask rules, never-ask list, deduce-from-context, defer-to rules, channel adaptations | `docs/lawim_heritage_gold/qualification_matrices/question_rules.json` |
| `matching_semantics.json` | Matching role per field (hard_constraint/soft_constraint/ranking_preference), weights, tolerances | `docs/lawim_heritage_gold/qualification_matrices/matching_semantics.json` |
| `qualification_matrices.json` | Matrix-specific field lists per readiness level (minimum_intake, minimum_search, etc.) | `docs/lawim_heritage_gold/qualification_matrices/qualification_matrices.json` |

### 0.2 H0.5 Question Selection Rules

The following rules from `question_rules.json` govern question selection:

**Rule 1 — Never re-ask confirmed facts** (`question_rules.json` RULE-001):
Once a field is collected and confirmed, it must never be asked again in the same qualification session.

**Rule 2 — Extract multiple fields from same message** (`question_rules.json` RULE-002):
When a user provides information containing multiple extractable fields, ALL must be extracted simultaneously.

**Rule 3 — One main question at a time** (`question_rules.json` RULE-003):
On WhatsApp, one question per message; on Telegram, 2-3 grouped fields; on Dashboard, full form.

**Rule 4 — Prioritize highest filtering power** (`question_rules.json` RULE-004):
Among missing fields, the one that most reduces search space is asked first. Priority is calculated as:
```
priority = base_priority - (impact_filtering * 10) + (sensitivity * 5) - (ambiguity * 3)
```

**Rule 5 — Launch search at MINIMUM_SEARCH_READY** (`question_rules.json` RULE-005):
As soon as minimum search fields are collected, launch search immediately. Do not continue asking.

**Rule 6 — Collect secondary preferences AFTER first search** (`question_rules.json` RULE-006):
Fields marked `defer_ask` in `question_rules.json` (balcon, jardin, climatisation, etc.) are collected post-search.

**Rule 7 — Ask confirmation only for real ambiguity** (`question_rules.json` RULE-007):
Never ask "is this correct?" for information the user explicitly provided. Only clarify when confidence < 0.70.

**Rule 8 — Never ask what can be deduced** (`question_rules.json` RULE-008):
Fields in `deduce_from_context` (e.g., chambres=0 for studio) are never asked directly.

### 0.3 H0.5 Priority Queue Construction

```
build_priority_queue(context, matrix):
  queue = []

  // 1. Determine current readiness level
  level = compute_readiness_level(context, matrix)

  // 2. Get matrix-specified fields for current and next level
  current_fields = matrix.fields["minimum_" + level.suffix]
  next_fields = matrix.fields["minimum_" + next_level(level).suffix]

  // 3. Add missing current-level fields first
  for field in current_fields:
    if field not in context.collected:
      queue.push(field, urgency="CRITICAL")

  // 4. Add missing next-level fields (lower priority)
  for field in next_fields:
    if field not in context.collected:
      queue.push(field, urgency="NORMAL")

  // 5. Add recommended fields (lowest priority, only post-search)
  if level >= MINIMUM_SEARCH_READY:
    for field in matrix.fields.recommended:
      if field not in context.collected:
        queue.push(field, urgency="LOW")

  // 6. Apply question_rules.json constraints
  queue = filter_never_ask(question_rules.never_ask, queue)
  queue = filter_deduced(question_rules.deduce_from_context, queue)
  queue = apply_defer(question_rules.defer_ask, queue, context)

  // 7. Apply conditional ask rules
  for rule in question_rules.conditional_ask:
    if eval_condition(rule.condition, context):
      if rule.field not in context.collected:
        queue.push(rule.field, priority=rule.priority)

  return sort_by_priority(queue)
```

### 0.4 Readiness-Gated Actions

From `readiness_rules.json` levels, each readiness level defines allowed and forbidden actions:

| Readiness Level | Allowed | Forbidden |
|-----------------|---------|-----------|
| INTENT_IDENTIFIED | detect_intent, confirm_intent, detect_property_type | launch_search, ask_contact_details, ask_detailed_criteria |
| MINIMUM_INTAKE_READY | confirm_city, confirm_budget, ask_neighborhood | launch_full_search, ask_contact_details, introduce_to_holders |
| MINIMUM_SEARCH_READY | **LAUNCH_FIRST_SEARCH**, present_top_results, ask_refinement | continue_asking_recommended_fields_before_search, withhold_results, ask_contact_before_results |
| MINIMUM_MATCHING_READY | rerank_results, filter_results, show_match_scores, ask_top_results, collect_introduction_fields | block_search_results, replace_results_without_user_request |
| INTRODUCTION_READY | **INTRODUCE_PARTIES**, share_property_details, contact_holder, schedule_introduction_call | share_contact_without_double_consent, force_introduction |
| VISIT_READY | schedule_and_confirm_visit, send_visit_confirmation, ask_feedback | share_exact_address_without_consent |
| TRANSACTION_READY | proceed_to_formal_transaction, engage_notary, facilitate_document_exchange, coordinate_payment | proceed_without_resolving_blockers, skip_legal_verification |

### 0.5 H0.5 Channel Adaptations

From `question_rules.json` `channel_adaptations`:

| Channel | Rules |
|---------|-------|
| WhatsApp | one_question_per_message=true, max_question_length=150, avoid_lists=true, defer_free_text=true, use_quick_replies=true |
| Telegram | batch_2_3_fields=true, use_formatting=true |
| Dashboard | full_form_one_page=true, group_by_category=true, inline_validation=true, save_draft=true |

---

## 1. H1 Heritage Layer — Algorithme de sélection

```
next_question(context):
  # 1. Collecter les champs manquants
  missing = get_missing_fields(context)
  
  # 2. Filtrer les interdits
  forbidden = get_forbidden_questions(context)
  deductible = get_deductible_fields(context)
  already_asked = get_already_asked(context)
  candidates = missing - forbidden - deductible - already_asked
  
  # 3. Sortir si aucun candidat
  if no candidates:
    if context.readiness >= MATCHING_READY:
      return propose_matching(context)
    return stop_qualification(context)
  
  # 4. Ordonner par priorité qualification (QUAL-007)
  ordered = sort_by_qualification_step(candidates)
  
  # 5. Adapter au canal (QUAL-013)
  response = channel_adapt(ordered, context.channel)
  
  return response
```

### 1.1 Diagramme de décision

```
                    ┌─────────────────────┐
                    │ Message entrant     │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │ Extraire champs     │
                    └──────────┬──────────┘
                               ↓
                    ┌─────────────────────┐
                    │ Mettre à jour       │
                    │ contexte session    │
                    └──────────┬──────────┘
                               ↓
              ┌────────────────────────────────┐
              │ Calculer readiness + température│
              └──────────┬─────────────────────┘
                         ↓
              ┌─────────────────────────────────┐
              │ Y a-t-il des champs manquants ? │
              └──────────┬──────────┬───────────┘
                    OUI  │          │  NON
                         ↓          ↓
              ┌──────────────────┐  ┌──────────────────┐
              │ Filtrer interdits│  │ Readiness ≥       │
              │ Ordonner par     │  │ MATCHING_READY ?  │
              │ priorité         │  └──────┬──────┬─────┘
              └───────┬──────────┘    OUI  │      │ NON
                      ↓                    ↓      ↓
              ┌──────────────────┐  ┌──────────┐  ┌──────────┐
              │ Adapter au canal │  │ Proposer  │  │ Stop     │
              │ Poser question   │  │ matching  │  │ qualif.  │
              └──────────────────┘  └──────────┘  └──────────┘
```

---

## 2. Priorité des champs manquants

### 2.1 Ordre strict de qualification (QUAL-007)

Les champs sont sélectionnés dans l'ordre des 10 étapes :

```
PRIORITY_QUEUE = [
  Step 1:  [intent],
  Step 2:  [property_type],
  Step 3:  [city],
  Step 4:  [neighborhood],
  Step 5:  [budget_min, budget_max, monthly_budget, cash_purchase],
  Step 6:  [urgency, timeline],
  Step 7:  [rooms, bedrooms, surface, min_surface, floor, parking, furnished],
  Step 8:  [usage, exposure, standing, pets_allowed, funding_source],
  Step 9:  [confirmation],
  Step 10: [escalation],
]
```

Règle : jamais de question d'une étape N+1 tant que tous les champs obligatoires de l'étape N ne sont pas collectés.

### 2.2 Priorité intra-étape

Au sein d'une même étape, les champs sont ordonnés par :

1. **Obligatoire > Recommandé > Optionnel**
2. **Extractible > Non extractible** (préférer les champs que le LLM peut déduire)
3. **Fort impact score > Faible impact**

### 2.3 Dérivation de priorité (Priorité composée)

```
field_priority(field, context):
  step = QUALIFICATION_ORDER[field]
  level = role_field_level(context.role, field)  // required=3, recommended=2, optional=1
  impact = scoring_impact(field)                 // poids dans QUAL-017
  
  composite = (7 - step) * 10 + level * 3 + impact
  return composite
```

Plus le composite est élevé, plus la question est posée tôt.

---

## 3. Adaptation par canal (QUAL-013)

### 3.1 WhatsApp — 1 question par message

| Règle | Détail |
|-------|--------|
| **Max questions par message** | 1 |
| **Format** | Question unique, naturelle, contexte préservé |
| **Exemple** | "Quel type de bien recherchez-vous ? (studio, appartement, maison...)" |
| **Comportement pièce jointe** | Si plusieurs champs manquants au même niveau, poser le plus prioritaire uniquement |
| **Limite consécutive** | Maximum 3 messages de questions consécutifs avant une réponse non-question |
| **Pause obligatoire** | Après 3 questions, envoyer un message informatif ou un résumé |

**Exemple WhatsApp :**
```
🤖: Merci ! Vous cherchez un appartement à Douala.
    Quel est votre budget maximum ?

👤: 50 millions

🤖: Parfait. Sous quel délai souhaitez-vous trouver ?
```

### 3.2 Telegram — 2-3 champs par message

| Règle | Détail |
|-------|--------|
| **Max questions par message** | 2-3 (champs connexes groupés) |
| **Principe de groupement** | Même étape ou étapes adjacentes |
| **Exemple** | "Quel type de bien et dans quelle ville ?" |
| **Validation** | Demander les champs compatibles ensemble |

**Règles de groupement :**

| Groupe autorisé | Champs | Exemple |
|-----------------|--------|---------|
| Type + Ville | property_type, city | "Quel type de bien et dans quelle ville ?" |
| Ville + Quartier | city, neighborhood | "Dans quelle ville et quel quartier ?" |
| Budget + Délai | budget, timeline | "Quel budget et sous quel délai ?" |
| Surface + Pièces | surface, rooms | "Quelle surface et combien de pièces ?" |
| Parking + Meublé | parking, furnished | "Avez-vous besoin de parking ? Meublé ou non ?" |

**Groupements interdits :**
| Groupe interdit | Raison |
|-----------------|--------|
| Intention + autre | L'intention doit être unique et claire |
| Budget + Quartier | Informations non connexes |
| Confirmation + autre | L'étape 9 est exclusive |

**Exemple Telegram :**
```
🤖: Quel type de bien cherchez-vous et dans quelle ville ?
  
👤: Appartement à Douala

🤖: Un budget à préciser ? Et sous quel délai ?
```

### 3.3 Dashboard — Formulaire structuré

| Règle | Détail |
|-------|--------|
| **Affichage** | Tous les champs manquants visibles dans un formulaire |
| **Validation** | Par champ, avec feedback immédiat |
| **Ordre** | Même priorité QUAL-007, mais l'utilisateur peut librement remplir |
| **Sauvegarde** | Sauvegarde automatique à chaque champ rempli |

---

## 4. Sélection contextuelle

### 4.1 Contexte utilisateur

La question est adaptée en fonction de :

| Contexte | Adaptation |
|----------|------------|
| **Nouvel utilisateur** | Ton plus guidé, explications, exemples dans la question |
| **Utilisateur existant** | Ton concis, référence à l'historique |
| **Diaspora** | Questions incluant la localisation internationale |
| **Après correction** | "Vous aviez dit [valeur], souhaitez-vous la corriger ?" |
| **Après incohérence** | Question de clarification avec mention de l'incohérence |

### 4.2 Ambiguïté détectée

Quand un champ extrait a une confiance basse (< 0.70), le système pose une question de clarification :

```
if entity.confidence < 0.70:
  question_type = CLARIFICATION
  template = "J'ai noté {entity.raw_value}, est-ce bien {entity.suggested} ?"
```

**Exemples :**

| Message ambigu | Question de clarification |
|----------------|--------------------------|
| "Je cherche à Buea" (Buea/Bafoussam ambiguity) | "Vous avez dit Buea, c'est bien Buea ou Bafoussam ?" |
| "Budget 5k" (5k = 5000 ou 5 millions ?) | "5k, c'est 5 000 ou 5 millions FCFA ?" |
| "3 pièces" (3 pièces = 3-chambres ?) | "3 pièces, c'est 3 chambres ou 3 pièces total ?" |

### 4.3 Proposition proactive

Quand un champ peut être déduit avec une confiance ≥ 0.85, le système propose plutôt que de demander :

```
if deduction.confidence >= 0.85:
  question_type = PROPOSAL
  template = "Vous cherchez un {deduced.value}, c'est bien ça ?"
```

**Exemples :**
- Déduction : `property_type=apartment` depuis "Je veux un 3 pièces" → "Vous cherchez un appartement, c'est bien ça ?"
- Déduction : `intent=buy` depuis "Budget 50M" sans intent explicite → "Vous cherchez à acheter ?"

### 4.4 Correction confirmation

Quand une correction est détectée :

```
if is_correction(new_value, previous_value):
  question_type = CONFIRMATION
  template = "D'accord, je note {new_value} au lieu de {previous_value}. C'est bien correct ?"
```

Exemple : "Ah non, c'est Yaoundé pas Douala" → "D'accord, je note Yaoundé au lieu de Douala. C'est bien correct ?"

---

## 5. Never-Ask List (Liste des questions interdites)

Conforme à QUAL-014 (GOLD-DM-010, GOLD-DM-012).

### 5.1 Questions déjà répondues (P1 — No re-ask)

Tout champ présent dans `context.collected_fields` ou dans `context.derived_fields` est interdit de question.

| Champ | Condition d'arrêt de question |
|-------|-------------------------------|
| Tous | `field in context.collected_fields` |
| Tous | `field in context.derived_fields` (calculé, pas besoin de demander) |

### 5.2 Questions déductibles (P3 — Deduction)

| Champ | Déduction | Condition |
|-------|-----------|-----------|
| `intent` | Depuis budget | budget_max → buy, monthly_budget → rent |
| `city` | Depuis quartier | neighborhood + GEO-003 → city |
| `budget_type` | Depuis intent | buy → budget_max, rent → monthly_budget |
| `urgency` | Depuis timeline et expressions | "asap" → urgent |

### 5.3 Questions bloquées par état

| Condition | Champs bloqués | Raison |
|-----------|----------------|--------|
| Ville non couverte | neighborhood, budget, délai... (tous) | Arrêt qualification (QUAL-015) |
| Inventaire vide | Confirmation, escalade | Arrêt qualification (QUAL-015) |
| Role=tenant | investment_type, expected_yield | Hors scope |

### 5.4 Questions déjà posées sans réponse

| Règle | Détail |
|-------|--------|
| Tolérance | Maximum 2 relances pour le même champ |
| Après 2 relances | Marquer le champ comme `user_silent`, passer au champ suivant |
| Comportement | "Je note que vous préférez ne pas répondre pour l'instant" |

---

## 6. Templates de questions

### 6.1 Templates par champ

| Champ | Template FR | Template EN |
|-------|-------------|-------------|
| `intent` | "Que cherchez-vous ? Louer, acheter, vendre ou investir ?" | "What are you looking for? Rent, buy, sell or invest?" |
| `property_type` | "Quel type de bien ? (studio, appartement, maison, villa, duplex, terrain, local)" | "What property type? (studio, apartment, house, villa, duplex, land, commercial)" |
| `city` | "Dans quelle ville ?" | "In which city?" |
| `neighborhood` | "Quel quartier préférez-vous à {city} ?" | "Which neighborhood in {city}?" |
| `budget_max` | "Quel est votre budget maximum pour l'achat ?" | "What's your maximum budget for purchase?" |
| `monthly_budget` | "Quel loyer maximum par mois ?" | "What's your maximum monthly rent?" |
| `desired_price` | "À quel prix souhaitez-vous vendre ?" | "At what price do you want to sell?" |
| `timeline` | "Sous quel délai ? (urgent, 1 mois, 3 mois, pas de presse)" | "What's your timeline? (urgent, 1 month, 3 months, no rush)" |
| `rooms` | "Combien de pièces ?" | "How many rooms?" |
| `bedrooms` | "Combien de chambres ?" | "How many bedrooms?" |
| `surface` | "Quelle surface minimale (m²) ?" | "What minimum surface (m²)?" |
| `parking` | "Avez-vous besoin d'un parking ?" | "Do you need parking?" |
| `furnished` | "Meublé ou non meublé ?" | "Furnished or unfurnished?" |
| `usage` | "C'est pour résidence principale ou investissement ?" | "Is it for primary residence or investment?" |

### 6.2 Templates contextuels

| Situation | Template |
|-----------|----------|
| **Après extraction partielle** | "J'ai noté que vous cherchez un {property_type}. Dans quelle ville ?" |
| **Nouvel utilisateur** | "Bonjour ! Je suis l'assistant LAWIM. Que cherchez-vous ?" |
| **Utilisateur connu** | "Bonjour ! Vous aviez cherché un {property_type} à {city} la dernière fois. Nouveau besoin ?" |
| **Diaspora** | "Bonjour ! LAWIM vous aide à investir au Cameroun depuis l'étranger. Quel type de bien ?" |
| **Correction enregistrée** | "J'ai bien noté {new_value} pour {field}. Continuons..." |
| **Ambiguïté** | "J'ai noté '{raw}'. Voulez-vous dire {suggestion1} ou {suggestion2} ?" |
| **Confirmation après complétude** | "Récapitulons : vous cherchez un {property_type} à {city} avec un budget de {budget}. C'est correct ?" |
| **Arrêt géographique** | "Désolé, nous ne couvrons pas encore {city}. Nous couvrons : Douala, Yaoundé, Bafoussam..." |

### 6.3 Templates de rebond

| Situation | Template |
|-----------|----------|
| **Intention secondaire détectée** | "Nous avons bien noté votre recherche de {primary_intent}. Souhaitez-vous aussi qu'on traite votre projet de {secondary_intent} ?" |
| **Changement d'intention** | "Je comprends que vous cherchez maintenant à {new_intent}. Je reprends votre nouvelle demande." |
| **Après matching refusé** | "Ces biens ne vous conviennent pas ? Puis-je ajuster les critères ?" |
| **Demande escalade humaine** | "Je vous mets en relation avec un conseiller LAWIM." |

---

## 7. Gestion des réponses utilisateur

### 7.1 Mapping réponse → champ

```
parse_user_response(message, context):
  # 1. Détection de correction explicite
  if is_correction_signal(message):
    return handle_correction(message, context)
    
  # 2. Extraction de valeur pour le champ en cours
  value = extract_field_value(message, context.current_question.field)
  
  if value and value.confidence >= 0.70:
    return FieldUpdate(context.current_question.field, value)
    
  # 3. Extraction de tout autre champ dans le message
  all_values = extract_all_fields(message)
  
  if all_values:
    return handle_multi_field_update(all_values, context)
    
  # 4. Aucune valeur extractible → clarification
  return ask_clarification(context.current_question)
```

### 7.2 Message hors-sujet

Si l'utilisateur répond hors-sujet (aucun champ extractible) :

| Comportement | Règle |
|--------------|-------|
| 1ère fois | Reformuler la question avec un exemple |
| 2ème fois | Proposer des choix ("Préférez-vous A ou B ?") |
| 3ème fois (consécutif) | Arrêt, proposer aide ou escalade humaine (QUAL-015) |

### 7.3 Réponse partielle

Quand l'utilisateur ne répond qu'à une partie d'une question groupée (Telegram) :

```
# Question groupée : "Quel type de bien et dans quelle ville ?"
# Réponse : "Appartement"
→ property_type = apartment
→ city = manquant → relance sur la ville uniquement
  "Merci ! Et dans quelle ville ?"
```

---

## 8. Règles avancées

### 8.1 Éviter les doublons de questions

Le système tient un registre de toutes les questions posées dans la session :

```
asked_questions: Set[{
  field: string,
  timestamp: datetime,
  response: any | null,
  attempts: number
}]
```

Règle : un champ ne peut être demandé que si `attempts < 3` dans la session active.

### 8.2 Détection de frustration

| Signal | Action |
|--------|--------|
| "Je l'ai déjà dit" | S'excuser, montrer la valeur collectée, proposer correction |
| "Je ne sais pas" | Passer au champ suivant, marquer comme `user_deferred` |
| "Trop de questions" | Arrêter qualification, proposer rappel plus tard |
| "Laissez-moi tranquille" | Arrêt immédiat, désactiver qualification pour 24h |

### 8.3 Réengagement après abandon

Si l'utilisateur quitte la conversation puis revient :

```
case REENGAGEMENT:
  if readiness >= MATCHING_READY:
    show_resume = "Nous cherchions un {property_type} à {city}. Vous voulez continuer ?"
  else:
    show_resume = "Nous étions en train de qualifier votre besoin. On continue ?"
  
  if user_confirms:
    resume_from_last_step()
  else:
    restart_qualification()
```

---

## 9. Métriques et monitoring

| Métrique | Objectif | Alerte si |
|----------|:--------:|-----------|
| Questions avant MATCHING_READY | ≤ 5 | > 8 |
| Questions totales avant VISIT_READY | ≤ 9 | > 12 |
| Taux d'abandon qualification | < 20% | > 30% |
| Taux de correction nécessaire | < 10% | > 20% |
| Temps moyen par question | < 30s | > 60s |
| Taux de frustration | < 5% | > 10% |

---

*Document Gold — Politique de sélection de questions validée — 2026-07-15*
