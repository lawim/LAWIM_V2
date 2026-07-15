# QUALIFICATION MATRIX CONTRACT — Matrice de Qualification

**Mission :** LAWIM Heritage Gold
**Statut :** Contrat validé — Définit les champs, validations et règles de la qualification
**Références :** QUALIFICATION_MODEL.md §6-7, RULE_INDEX.md QUAL-007, QUAL-010, QUAL-011, QUAL-013, QUAL-014, DOMAIN_MODEL.md §8

---

> **DEPENDENCY_H05:** Detailed field matrices per property type and transaction type require H0.5 qualification deliverables. The contracts defined here specify the EXPECTED INTERFACE for H0.5 integration. Actual field lists, priorities, and validation rules must be sourced from H0.5.

## 1. Champs par type de transaction

### 1.1 Achat (buy)

| Niveau | Champs | Source QUAL |
|--------|--------|-------------|
| **Obligatoire** | `property_type`, `city`, `budget_max` | QUALIFICATION_MODEL.md §6.1 |
| **Recommandé** | `neighborhood`, `timeline`, `rooms`, `usage` (résidence principale / investissement) | QUALIFICATION_MODEL.md §6.1 |
| **Optionnel** | `funding_source`, `current_situation` (locataire / propriétaire), `floor`, `parking`, `furnished` | QUALIFICATION_MODEL.md §6.1 |

### 1.2 Location (rent)

| Niveau | Champs | Source QUAL |
|--------|--------|-------------|
| **Obligatoire** | `property_type`, `city`, `monthly_budget` | QUALIFICATION_MODEL.md §6.2 |
| **Recommandé** | `neighborhood`, `lease_duration`, `rooms`, `furnished` | QUALIFICATION_MODEL.md §6.2 |
| **Optionnel** | `furnished`, `pets_allowed`, `parking`, `floor` | QUALIFICATION_MODEL.md §6.2 |

### 1.3 Vente (sell)

| Niveau | Champs | Source QUAL |
|--------|--------|-------------|
| **Obligatoire** | `property_type`, `city`, `desired_price` | QUALIFICATION_MODEL.md §6.3 |
| **Recommandé** | `title_deed`, `surface`, `description`, `photos` | QUALIFICATION_MODEL.md §6.3 |
| **Optionnel** | `sell_reason`, `availability`, `property_history` | QUALIFICATION_MODEL.md §6.3 |

### 1.4 Investissement (invest)

| Niveau | Champs | Source QUAL |
|--------|--------|-------------|
| **Obligatoire** | `budget`, `investment_type` (locatif / revente / terrain), `city` | QUALIFICATION_MODEL.md §6.4 |
| **Recommandé** | `expected_yield`, `horizon`, `preferred_zone` | QUALIFICATION_MODEL.md §6.4 |
| **Optionnel** | `real_estate_experience`, `other_investments`, `diaspora_status` | QUALIFICATION_MODEL.md §6.4 |

---

## 2. Champs obligatoires par type de bien

| Type de bien | Champs obligatoires | Source |
|-------------|---------------------|--------|
| **studio** | `city`, `budget`, `min_surface` | QUALIFICATION_MODEL.md §7 |
| **apartment** | `city`, `budget`, `rooms` | QUALIFICATION_MODEL.md §7 |
| **house** | `city`, `budget`, `surface`, `bedrooms` | QUALIFICATION_MODEL.md §7 |
| **villa** | `city`, `budget`, `land_surface`, `bedrooms` | QUALIFICATION_MODEL.md §7 |
| **duplex** | `city`, `budget`, `surface`, `floor` | QUALIFICATION_MODEL.md §7 |
| **land** | `city`, `budget`, `surface`, `land_type` (constructible / agricole) | QUALIFICATION_MODEL.md §7 |
| **commercial** | `city`, `budget`, `surface`, `commerce_type` | QUALIFICATION_MODEL.md §7 |

### 2.1 Matrice croisée transaction × type

Cette matrice détermine les champs exacts requis pour chaque combinaison :

| Transaction | Type bien | Champs obligatoires spécifiques |
|-------------|-----------|--------------------------------|
| buy | apartment | property_type, city, budget_max, rooms |
| buy | house | property_type, city, budget_max, surface, bedrooms |
| buy | land | property_type, city, budget_max, surface, land_type |
| rent | apartment | property_type, city, monthly_budget, rooms |
| rent | studio | property_type, city, monthly_budget, min_surface |
| sell | house | property_type, city, desired_price, surface, title_deed |
| invest | land | budget, investment_type, city, surface, land_type |
| invest | commercial | budget, investment_type, city, surface, commerce_type |

---

## 3. Modèle de données — 25 USER_FIELDS (QUAL-010)

### 3.1 Catalogue complet des champs de qualification

| # | Champ | Type | Catégorie | Extraction | Priorité qualification |
|:-:|-------|------|-----------|------------|:---------------------:|
| 1 | `intent` | enum | Intention | IntentClassifier | 1 |
| 2 | `property_type` | enum | Bien | NER | 2 |
| 3 | `city` | string | Localisation | NER + GeoEngine | 3 |
| 4 | `neighborhood` | string | Localisation | NER + GeoEngine | 4 |
| 5 | `budget_min` | number | Budget | NER | 5 |
| 6 | `budget_max` | number | Budget | NER | 5 |
| 7 | `monthly_budget` | number | Budget | NER (rent) | 5 |
| 8 | `currency` | enum | Budget | Devise detection | 5 |
| 9 | `urgency` | enum | Temporalité | Expression temporelle | 6 |
| 10 | `timeline` | enum | Temporalité | Délai explicite | 6 |
| 11 | `rooms` | integer | Critères | NER | 7 |
| 12 | `bedrooms` | integer | Critères | NER (house/villa) | 7 |
| 13 | `surface` | number | Critères | NER | 7 |
| 14 | `min_surface` | number | Critères | NER (studio/land) | 7 |
| 15 | `floor` | integer | Critères | NER | 7 |
| 16 | `parking` | boolean | Critères | Expression booléenne | 7 |
| 17 | `furnished` | boolean | Critères | Expression booléenne | 7 |
| 18 | `usage` | enum | Préférences | Résidence principale / investissement | 8 |
| 19 | `exposure` | enum | Préférences | NER | 8 |
| 20 | `standing` | enum | Préférences | NER | 8 |
| 21 | `pets_allowed` | boolean | Préférences | Expression booléenne | 8 |
| 22 | `funding_source` | string | Profil | NER | 8 |
| 23 | `diaspora_flag` | boolean | Profil | QUAL-016 | 1 (automatique) |
| 24 | `cash_purchase` | boolean | Profil | Expression "cash" | 5 (automatique) |
| 25 | `name` | string | Identité | NER | — (continu) |
| 26 | `phone` | string | Identité | NER | — (continu) |
| 27 | `email` | string | Identité | NER | — (continu) |

### 3.2 10 LEAD_FIELDS (QUAL-011)

| # | Champ | Source | Description |
|:-:|-------|--------|-------------|
| 1 | `message` | raw input | Message brut de l'utilisateur |
| 2 | `intent` | intent_classifier | Intention détectée |
| 3 | `budget` | entity_extractor | Budget extrait (min/max/mensuel) |
| 4 | `location` | entity_extractor + GeoEngine | Localisation extraite (ville, quartier) |
| 5 | `property_type` | entity_extractor | Type de bien extrait |
| 6 | `urgency` | entity_extractor | Niveau d'urgence |
| 7 | `score` | scoring_engine | Score composite calculé |
| 8 | `status` | classifier | Statut qualification (in_progress/complete/paused/abandoned) |
| 9 | `priority` | classifier | Priorité P0-P3 |
| 10 | `diaspora_flag` | diaspora_detector | Flag diaspora (booléen) |

---

## 4. Règles de validation par champ

### 4.1 Validation de présence

| Champ | Règle de validation | Message d'erreur |
|-------|---------------------|------------------|
| `intent` | Doit être RENT/BUY/SELL/INVESTOR | "Je n'ai pas bien compris votre besoin. Cherchez-vous à louer, acheter, vendre ou investir ?" |
| `property_type` | Doit être studio/apartment/house/villa/duplex/land/commercial | "Quel type de bien recherchez-vous ? (studio, appartement, maison, villa, duplex, terrain, local commercial)" |
| `city` | Doit être dans GEO-002 (10 villes) + extensions | "Désolé, nous ne couvrons pas encore cette ville." |
| `neighborhood` | Doit être valide pour la ville (GEO-003) | "Je n'ai pas reconnu ce quartier. Voici les quartiers disponibles à [ville] : ..." |
| `budget` | Doit être > 0, avec devise (FCFA par défaut) | "Pouvez-vous préciser votre budget ? (ex: 50 millions FCFA)" |

### 4.2 Validation de plage

| Champ | Validation | Source |
|-------|-----------|--------|
| `budget_max` | Écart type OK si budget_min < budget_max | — |
| `surface` | > 0 m² | — |
| `rooms` | ≥ 1 | — |
| `bedrooms` | ≥ 1, ≤ rooms | — |
| `floor` | ≥ 0 | — |
| `urgency` | Enum : urgent / 1mois / 3mois / flexible | QUALIFICATION_MODEL.md §5 |

### 4.3 Validation de cohérence

| Règle | Condition | Action |
|-------|-----------|--------|
| Budget location vs achat | Si intent=rent, budget doit être mensuel | Conversion auto si "50k" et rent → monthly_budget |
| Type terrain → land_type | Si property_type=land, land_type requis | Question complémentaire obligatoire |
| Type studio → min_surface | Si property_type=studio, min_surface recommandé | Question complémentaire recommandée |
| Maison/Villa → bedrooms | Si property_type=house/villa, bedrooms requis | Question complémentaire obligatoire |

### 4.4 Validation de couverture géographique

```
is_city_covered(city):
  if city in GEO_002_PRIORITY_CITIES: return COVERED
  if city in GEO_002_EXTENDED: return COVERED
  if city_affinity_exists(city): return AFFINITY  // GOLD-DM-008
  return NOT_COVERED  // → arrêt qualification (QUAL-015)
```

---

## 5. Priorité des champs dans l'ordre de qualification

Conforme à QUAL-007 : ordre strict de qualification.

```
PRIORITY_ORDER = [
  1:  intent,              // Intention
  2:  property_type,       // Type de bien
  3:  city,                // Ville
  4:  neighborhood,        // Quartier
  5:  budget_min,          // Budget (min/max/mensuel)
      budget_max,
      monthly_budget,
  6:  urgency,             // Délai
      timeline,
  7:  rooms,               // Critères
      bedrooms,
      surface,
      min_surface,
      floor,
      parking,
      furnished,
  8:  usage,               // Préférences
      exposure,
      standing,
      pets_allowed,
      funding_source,
  9:  confirmation,        // Confirmation (étape synthèse)
  10: escalation,          // Escalade (décision finale)
]
```

### 5.1 Règles de priorité relative

1. **Intention toujours en premier** : Aucune question avant d'avoir `intent` avec confiance ≥ 0.70
2. **Type bien avant ville** : Le type de bien influence les questions de localisation (ex: terrain ≠ appartement)
3. **Ville avant quartier** : Les quartiers sont dépendants de la ville
4. **Budget selon transaction** : Achat → budget_max, Location → monthly_budget, Vente → desired_price
5. **Délai après budget** : La temporalité est contextuelle au budget
6. **Critères après type bien** : Les critères varient selon le type (surface pour maison, étage pour duplex)
7. **Préférences en dernier** : Standing, exposition — affinent le matching mais ne bloquent pas

---

## 6. Règles de supersession

Conforme à QUAL-014 (GOLD-DM-011, P2).

### 6.1 Principe

La correction de l'utilisateur écrase toujours le contexte obsolète. Aucune valeur n'est définitive tant que la qualification n'est pas confirmée.

### 6.2 Mécanisme

```
supersede(current_value, new_value):
  if new_value is None: return current_value          // Pas de mise à jour
  if new_value.confidence < 0.40: return current_value  // Confiance trop basse
  if new_value is correction to previous answer:
    store old_value in history[current_field].previous_values[]
    current_value = new_value
    recalculate_derived_fields(current_field)
    mark_confirmation_needed(current_field)            // Demander validation à l'étape 9
    return new_value
```

### 6.3 Cas particuliers

| Scénario | Règle | Exemple |
|----------|-------|---------|
| Correction explicite | "Non, je parlais de Yaoundé, pas Douala" → écrase city | City passe de Douala → Yaoundé |
| Affinement | "Plutôt entre 40 et 50 millions" → écrase budget | Budget max passe de 60M → 50M |
| Changement d'avis | "Finalement je cherche plutôt un terrain" → écrase property_type | Type passe de apartment → land |
| Rétractation | "Non en fait je cherche à louer pas à acheter" → réinitialisation partielle, reprise étape 1 | Intent change → historique conservé mais contexte réinitialisé |

### 6.4 Historique des valeurs

Chaque champ conserve un historique des valeurs précédentes :

```
FieldHistory {
  field_name: string
  current_value: any
  previous_values: [
    { value: any, timestamp: datetime, source: "user" | "extraction" | "deduction" }
  ]
  supersession_count: number
  last_updated: datetime
}
```

### 6.5 Détection de boucle de correction

Si un champ est modifié plus de 3 fois, le système :
1. Marque le champ comme `unstable`
2. Réduit son poids dans le scoring de 50%
3. Propose une confirmation renforcée à l'étape 9

---

## 7. Questions interdites (Never-Ask / Forbidden)

Conforme à QUAL-014 (GOLD-DM-010, P1), GOLD-DM-012 (P3).

### 7.1 Catégories de questions interdites

| Catégorie | Règle | Exemple interdit |
|-----------|-------|------------------|
| **Déjà répondu** | Ne jamais demander un champ déjà collecté (historique ou session en cours) | "Quel type de bien ?" alors que déjà dit "appartement" |
| **Déductible** | Ne jamais demander ce qui peut être déduit d'autres champs | "Cherchez-vous à acheter ?" alors que budget_max > monthly_budget possible |
| **Incohérent avec contexte** | Ne pas demander un champ qui contreditait les réponses précédentes | "Quel quartier ?" si ville non couverte |
| **Hors scope du rôle** | Ne pas demander des champs non applicables au rôle détecté | "Quel rendement attendu ?" à un locataire |
| **Déjà en cours de confirmation** | Ne pas redemander à l'étape 9 un champ déjà listé dans le résumé | Demander le budget alors qu'il est dans le récapitulatif |

### 7.2 Matrice des questions interdites par rôle

| Champ | tenant | buyer | seller | investor | Raison |
|-------|:------:|:-----:|:------:|:--------:|--------|
| `investment_type` | ❌ | ✓ | ❌ | ✓ | Hors scope locataire/vendeur |
| `expected_yield` | ❌ | ❌ | ❌ | ✓ | Spécifique investisseur |
| `sell_reason` | ❌ | ❌ | ✓ | ❌ | Spécifique vendeur |
| `lease_duration` | ✓ | ❌ | ❌ | ❌ | Spécifique locataire |
| `title_deed` | ❌ | ❌ | ✓ | ❌ | Spécifique vendeur |
| `monthly_budget` | ✓ | ❌ | ❌ | ❌ | Achat = budget_max, pas mensuel |
| `funding_source` | ❌ | ✓ | ❌ | ✓ | Pertinent achat/investissement |

### 7.3 Détection de déductibilité

```
is_deductible(field, context):
  match field:
    case "intent" if context.budget_max > 0 AND context.monthly_budget == 0:
      return True  // budget_max → intent=buy
    case "property_type" if context.surface AND context.bedrooms:
      return True  // surface + bedrooms → house probable
    case "city" if context.neighborhood:
      return True  // quartier → ville déduite
    case "urgency" if context.timeline == "urgent":
      return True  // timeline urgent déjà exprimé
    case _:
      return False
```

### 7.4 Vérification avant envoi

```
before_asking(question, context):
  if question.field in context.collected_fields:
    return REJECT_ALREADY_COLLECTED
  if is_deductible(question.field, context):
    return REJECT_DEDUCTIBLE
  if context.role not in question.allowed_roles:
    return REJECT_ROLE_MISMATCH
  if context.city_status == NOT_COVERED:
    return REJECT_GEOGRAPHY_BLOCK
  return APPROVED
```

---

## 8. Comportements traqués (QUAL-012)

| Comportement | Données collectées | Usage |
|-------------|-------------------|-------|
| `message_history` | Timestamps, length, field_delta | Analyse cohérence, détection changements intention |
| `response_time` | Avg, min, max response time (seconds) | Mesure engagement, priorisation |
| `budget_changes` | Valeurs précédentes, amplitude | Détection indécision, mise à jour |
| `visit_requests` | Nombre demandes, biens ciblés | Signal fort intention d'achat (boost visit_intent) |

---

## 9. Champs composites et dérivés

Certains champs sont calculés à partir d'autres champs, jamais demandés directement :

| Champ dérivé | Formule | Usage |
|-------------|---------|-------|
| `budget_range_ok` | `budget_min <= budget_max` | Validation budgétaire |
| `diaspora_flag` | QUAL-016 : localisation OU indicatif | Score booster |
| `lead_temperature` | normalisation score QUAL-004/005 | Classification |
| `readiness_stage` | Completeness % → stage | Progression |
| `budget_type` | `monthly_budget ? "rent" : budget_max ? "buy" : "invest"` | Typage budget |

---

*Document Gold — Contrat de qualification validé — 2026-07-15*
