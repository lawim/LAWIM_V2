# READINESS MODEL — Modèle de Maturité de Qualification

**Mission :** LAWIM Heritage Gold
**Statut :** Modèle validé — Calcule la complétude et détermine le niveau d'action possible
**Références :** QUALIFICATION_MODEL.md §5-6, QUALIFICATION_EXECUTION_ARCHITECTURE.md §8, DOMAIN_MODEL.md GOLD-DM-014 (P5)

---

> **ARCHITECTURE_DECISION_RETAINED:** The sections below (§1–§8) document the H1 heritage 4-level readiness model. This model is retained as an architectural reference but is **superseded by the H0.5 7-level model** defined in §0 above. H1 concepts still valid (completeness formula structure, readiness transitions, dynamical recalculation) are preserved; H0.5 contradictions are marked **RESOLVED_BY_H05** in §0.7.

## 1. Principe

Le Readiness Model mesure le niveau de complétude de la qualification d'un lead. Il détermine quelles actions sont disponibles et guide le NextQuestionSelector sur la prochaine question à poser.

Conforme à GOLD-DM-014 (P5 : Match early) : le matching commence dès que les informations critiques sont disponibles, les champs optionnels améliorent le score mais ne bloquent jamais.

---

## 2. Quatre niveaux de Readiness

```
SEARCH_READY      →    MATCHING_READY    →    VISIT_READY    →    RELATIONSHIP_READY
   ≥ 40%                  ≥ 65%                ≥ 85%                = 100%
```

### 2.1 SEARCH_READY (≥ 40%)

Le système peut commencer à chercher des biens correspondant aux critères de base.

| Condition | Détail |
|-----------|--------|
| Seuil | Complétude ≥ 40% |
| Déclencheur | Intent + property_type + city collectés |
| Action | Matching précoce activé (recherche interne, pas encore de présentation) |
| Principe | GOLD-DM-014 (P5) : "Match early — matching starts as soon as critical info is available" |

**Champs requis pour SEARCH_READY :**

| Profil | Champs requis |
|--------|---------------|
| buyer | intent, property_type, city |
| tenant | intent, property_type, city |
| seller | intent, property_type, city |
| investor | intent, city, budget |

### 2.2 MATCHING_READY (≥ 65%)

Le système peut présenter des résultats de matching à l'utilisateur.

| Condition | Détail |
|-----------|--------|
| Seuil | Complétude ≥ 65% |
| Déclencheur | Budget + délai collectés |
| Action | Envoi des résultats de matching (max 5 au premier matching — MATCH-010) |
| Principe | Le score de matching est fiable avec ces informations |

**Champs requis pour MATCHING_READY :**

| Profil | Champs additionnels requis (vs SEARCH_READY) |
|--------|---------------------------------------------|
| buyer | + budget_max, timeline |
| tenant | + monthly_budget, timeline, rooms |
| seller | + desired_price |
| investor | + budget, investment_type, horizon |

### 2.3 VISIT_READY (≥ 85%)

Le système peut proposer une visite physique.

| Condition | Détail |
|-----------|--------|
| Seuil | Complétude ≥ 85% |
| Déclencheur | Critères principaux + préférences collectés |
| Action | Proposition de rendez-vous de visite |
| Principe | L'agent a suffisamment d'information pour préparer une visite pertinente |

**Champs requis pour VISIT_READY :**
- Tous les champs de MATCHING_READY
- Critères : surface/rooms/bedrooms/parking/furnished selon property_type
- Préférences : usage, standing

### 2.4 RELATIONSHIP_READY (100%)

Qualification complète. Le lead peut être transféré à un agent.

| Condition | Détail |
|-----------|--------|
| Seuil | Complétude = 100% |
| Déclencheur | Confirmation utilisateur reçue |
| Action | Escalade agent, CRM routing |
| Principe | Tous les champs obligatoires + recommandés sont collectés et confirmés |

---

## 3. Calcul de la complétude

### 3.1 Formule générale

```
completeness_pct(fields_collected, profile) =
    (sum(required_collected) + sum(recommended_collected) * 0.5) /
    (count(required) + count(recommended) * 0.5) × 100
```

Où :
- `required_collected` = 1 si collecté, 0 sinon
- `recommended_collected` = 1 si collecté, 0 sinon (poids 0.5)
- `optional` = non comptés dans le calcul (améliorent le matching score mais pas la readiness)

### 3.2 Pondération des champs par profil

#### Buyer

| Champ | Niveau | Poids dans complétude |
|-------|--------|:---------------------:|
| intent | required | 1.0 |
| property_type | required | 1.0 |
| city | required | 1.0 |
| budget_max | required | 1.0 |
| timeline | recommended | 0.5 |
| neighborhood | recommended | 0.5 |
| rooms | recommended | 0.5 |
| usage | recommended | 0.5 |
| surface | optional | 0.0 |
| floor | optional | 0.0 |
| parking | optional | 0.0 |
| furnished | optional | 0.0 |
| **Total requis** | | **4.0** |
| **Total recommandé** | | **4 × 0.5 = 2.0** |
| **Dénominateur** | | **6.0** |

#### Tenant

| Champ | Niveau | Poids |
|-------|--------|:-----:|
| intent | required | 1.0 |
| property_type | required | 1.0 |
| city | required | 1.0 |
| monthly_budget | required | 1.0 |
| lease_duration | recommended | 0.5 |
| rooms | recommended | 0.5 |
| neighborhood | recommended | 0.5 |
| furnished | optional | 0.0 |
| **Dénominateur** | | **5.5** |

#### Seller

| Champ | Niveau | Poids |
|-------|--------|:-----:|
| intent | required | 1.0 |
| property_type | required | 1.0 |
| city | required | 1.0 |
| desired_price | required | 1.0 |
| title_deed | recommended | 0.5 |
| surface | recommended | 0.5 |
| description | recommended | 0.5 |
| photos | recommended | 0.5 |
| **Dénominateur** | | **6.0** |

#### Investor

| Champ | Niveau | Poids |
|-------|--------|:-----:|
| intent | required | 1.0 |
| city | required | 1.0 |
| budget | required | 1.0 |
| investment_type | required | 1.0 |
| expected_yield | recommended | 0.5 |
| horizon | recommended | 0.5 |
| preferred_zone | recommended | 0.5 |
| **Dénominateur** | | **5.5** |

### 3.3 Exemple de calcul — Buyer

Un acheteur a fourni : intent, property_type, city, budget_max, timeline, neighborhood.

```
completeness = (4 required + 2 recommended × 0.5) / (4 + 4 × 0.5) × 100
             = (4 + 1.0) / (4 + 2.0) × 100
             = 5.0 / 6.0 × 100
             = 83.3%
```

→ **VISIT_READY** (≥ 85%) — presque atteint, il manque rooms ou usage pour franchir le seuil.

### 3.4 Exemple — Tenant

Un locataire a fourni : intent, property_type, city, monthly_budget.

```
completeness = (4 required + 0 recommended) / (4 + 3 × 0.5) × 100
             = 4.0 / 5.5 × 100
             = 72.7%
```

→ **MATCHING_READY** (≥ 65%) — les résultats de matching peuvent être envoyés.

### 3.5 Exemple — Seller

Un vendeur a fourni : intent, property_type, city, desired_price, surface.

```
completeness = (4 required + 1 recommended × 0.5) / (4 + 4 × 0.5) × 100
             = 4.5 / 6.0 × 100
             = 75.0%
```

→ **MATCHING_READY** (≥ 65%) — le bien peut être estimé et mis en visibilité.

---

## 4. Readiness dynamique

### 4.1 Impact des nouvelles informations

La readiness est recalculée après chaque message. Tout nouveau champ collecté peut faire évoluer le niveau.

```
on_message_received(message, context):
  extract_fields(message)                          // Mise à jour des champs
  context = supersede(context, new_fields)         // Application QUAL-014
  new_readiness = compute_readiness(context)
  
  if new_readiness > context.previous_readiness:
    trigger_readiness_transition(new_readiness)
  elif new_readiness < context.previous_readiness:
    // Cas rare : changement d'intention ou correction qui réduit la complétude
    handle_readiness_regression(context)
    
  context.previous_readiness = new_readiness
```

### 4.2 Transitions de readiness

| Transition | Condition | Action déclenchée |
|------------|-----------|-------------------|
| SEARCH_READY → MATCHING_READY | Budget collecté | Déclencher matching, préparer premiers résultats |
| MATCHING_READY → VISIT_READY | Critères + préférences | Envoyer résultats si pas déjà fait, proposer visite |
| VISIT_READY → RELATIONSHIP_READY | Confirmation reçue | Transférer à l'agent, notifier CRM |
| Régression | Changement d'intention | Recalcul complet, notification "Je reprends votre nouveau besoin" |

### 4.3 Readiness décroissante (régression)

Dans certains cas, la readiness peut diminuer :

| Cause | Impact | Gestion |
|-------|--------|---------|
| Changement d'intention (ex: achat → location) | Tous les champs spécifiques à l'achat sont perdus | Réinitialisation partielle (QUAL-015) |
| Correction majeure (ex: ville → autre ville) | Les champs dépendants (quartier) sont perdus | Mise à jour, quartier remis à collecter |
| Annulation d'un champ | Retour à l'état précédent | Supersession avec historique |

---

## 5. Readiness et scoring — relation

```
Lead State
 ├── readiness_stage: SEARCH_READY | MATCHING_READY | VISIT_READY | RELATIONSHIP_READY
 ├── lead_temperature: HOT | WARM | COLD | SPAM
 └── completeness_pct: 0-100%
```

La readiness et la température sont orthogonales :

| Température \ Readiness | SEARCH_READY (40%) | MATCHING_READY (65%) | VISIT_READY (85%) | RELATIONSHIP_READY (100%) |
|:------------------------:|:------------------:|:--------------------:|:-----------------:|:-------------------------:|
| **HOT (≥ 0.8)** | Matching précoce déclenché | Envoi résultats IMMÉDIAT | Proposition visite prioritaire | Escalade agent URGENT |
| **WARM (≥ 0.5)** | Enrichissement requête | Envoi résultats standard | Proposition visite standard | Transfert agent normal |
| **COLD (≥ 0.3)** | Qualification continue | Qualification jusqu'à VISIT_READY | Qualification jusqu'à RELATIONSHIP_READY | Transfert si nécessaire |

---

## 6. Readiness par étape de qualification

Correspondance entre les 10 étapes (QUAL-007) et les niveaux de readiness :

| Étape qualification | Champs cumulés | Completeness approx. | Readiness |
|:-------------------:|----------------|:--------------------:|-----------|
| 1. Intention | intent | 15% | — |
| 2. Type bien | + property_type | 25% | — |
| 3. Ville | + city | 35% | SEARCH_READY |
| 4. Quartier | + neighborhood | 40% | SEARCH_READY |
| 5. Budget | + budget | 55% | MATCHING_READY (ou avant selon profil) |
| 6. Délai | + timeline | 65% | MATCHING_READY |
| 7. Critères | + surface/rooms/etc | 80% | VISIT_READY |
| 8. Préférences | + usage/standing/etc | 90% | VISIT_READY |
| 9. Confirmation | Validation | 100% | RELATIONSHIP_READY |
| 10. Escalade | — | 100% | RELATIONSHIP_READY |

## 0. H0.5 Integration Layer — 7-Level Readiness Model

### 0.1 RESOLVED_BY_H05 — 4-Level to 7-Level Migration

The H1 4-level model (SEARCH_READY → MATCHING_READY → VISIT_READY → RELATIONSHIP_READY) is **replaced** by the H0.5 7-level model. All H1 content below this section is retained as an `ARCHITECTURE_DECISION_RETAINED` reference but the canonical model is now the H0.5 7-level readiness system.

**Source Files:**
- `docs/lawim_heritage_gold/qualification_matrices/readiness_rules.json` — Canonical readiness definitions per level
- `docs/lawim_heritage_gold/qualification_matrices/READINESS_LEVELS.md` — Full documentation with examples

### 0.2 The 7 H0.5 Readiness Levels

```
Level 1: INTENT_IDENTIFIED
    ↓ (transaction + property_type known)
Level 2: MINIMUM_INTAKE_READY
    ↓ (city + budget known)
Level 3: MINIMUM_SEARCH_READY  ← FIRST SEARCH LAUNCHED HERE
    ↓ (neighborhood + basic criteria)
Level 4: MINIMUM_MATCHING_READY
    ↓ (field-specific criteria for ranking)
Level 5: INTRODUCTION_READY
    ↓ (contact info + willingness to connect)
Level 6: VISIT_READY
    ↓ (visit logistics confirmed)
Level 7: TRANSACTION_READY
    ↓ (legal/financial requirements met)
```

### 0.3 Mapping from H1 4-Level to H0.5 7-Level

| H1 Level | H0.5 Equivalent | Notes |
|----------|-----------------|-------|
| SEARCH_READY (40%) | MINIMUM_SEARCH_READY | Same threshold concept, H0.5 adds precise field requirements per matrix |
| MATCHING_READY (65%) | MINIMUM_MATCHING_READY | H0.5 requires property-type-specific criteria (chambres, douches, cuisine) |
| VISIT_READY (85%) | VISIT_READY | H0.5 adds visit logistics fields (date, time, participants) |
| RELATIONSHIP_READY (100%) | INTRODUCTION_READY → TRANSACTION_READY | H0.5 splits into introduction + visit + transaction stages |
| — | INTENT_IDENTIFIED | New: explicit intent + property type detection stage |
| — | MINIMUM_INTAKE_READY | New: city + budget collection stage |

### 0.4 H0.5 Completeness Weighted Formula

From `readiness_rules.json` and `READINESS_LEVELS.md`, the completeness calculation is level-aware with matrix-specific field requirements:

```
completeness(context, matrix):
  level = current_readiness_level(context, matrix)
  required = matrix.fields["minimum_" + level.suffix]
  conditional = readiness_rules.levels[level].conditional_requirements
  collected_required = count(f in context.collected for f in required)
  total_required = len(required) + len(conditional fields)

  recommended = matrix.fields.recommended
  collected_recommended = count(f in context.collected for f in recommended)
  total_recommended = len(recommended)

  // Weighted formula per H0.5 readiness_rules.json
  pct = (collected_required + collected_recommended * 0.5) /
        (total_required + total_recommended * 0.5) * 100

  // Apply penalty factors from readiness_rules.json penalty_factors_by_level
  for penalty in readiness_rules.penalty_factors_by_level[level]:
    if penalty_condition_met(context, penalty):
      pct -= penalty_value(penalty)

  return clamp(pct, 0, 100)
```

**Transition Rules** (from `readiness_rules.json transitions`):

| From | To | Trigger | Type |
|------|----|---------|------|
| INTENT_IDENTIFIED | MINIMUM_INTAKE_READY | Collect city + budget | auto |
| MINIMUM_INTAKE_READY | MINIMUM_SEARCH_READY | Collect neighborhood + validate | auto |
| MINIMUM_SEARCH_READY | MINIMUM_MATCHING_READY | Collect property-specific criteria | auto |
| MINIMUM_MATCHING_READY | INTRODUCTION_READY | Collect contact + confirm interest | semi_auto |
| INTRODUCTION_READY | VISIT_READY | Schedule visit + confirm access | manual |
| VISIT_READY | TRANSACTION_READY | Verify documents + legal + financing | manual |

### 0.5 H0.5 Boost and Penalty Factors by Level

From `readiness_rules.json`:

| Level | Boosts | Penalties |
|-------|--------|-----------|
| INTENT_IDENTIFIED | None | None |
| MINIMUM_INTAKE_READY | city_match +20, budget_within_range +15 | missing_budget -10, unclear_location -10 |
| MINIMUM_SEARCH_READY | exact_neighborhood +25, diaspora +20 | missing_neighborhood -5, spam_like -50 |
| MINIMUM_MATCHING_READY | property_type_match +15, amenities_match +10 | contradictory_criteria -15 |
| INTRODUCTION_READY | urgency +15, trust_signal +10 | refused_contact -20 |
| VISIT_READY | visit_intent +20 | missed_visit -25 |
| TRANSACTION_READY | financing_secured +15, documents_ready +10 | incomplete_documents -30 |

### 0.6 Cardinal Rule (from READINESS_LEVELS.md §4)

> **As soon as MINIMUM_SEARCH_READY is reached, LAWIM can launch a first search. It is forbidden to continue collecting recommended or optional fields before presenting initial results.**

### 0.7 H0.5 → H1 Contradiction Resolution

| H0.5 Rule | H1 (Heritage) | Resolution |
|-----------|---------------|------------|
| 7 readiness levels | 4 readiness levels | **RESOLVED_BY_H05** — 7-level model replaces 4-level |
| Matrix-specific field requirements per level | Static field lists per role | **RESOLVED_BY_H05** — Dynamic per-matrix field resolution |
| No regression allowed | Regressions possible (intent change) | **ARCHITECTURE_DECISION_RETAINED** — H1 regression handling kept for intent-change scenarios |
| TRANSACTION_READY as terminal | RELATIONSHIP_READY as terminal | **RESOLVED_BY_H05** — Transaction replaces relationship as terminal stage |
| Weighted formula per readiness level | Uniform formula | **RESOLVED_BY_H05** — H0.5 per-level weighting supersedes

---

## 7. Exemples complets par profil

### 7.1 Buyer — Jean cherche un appartement à Douala

| Message | Champs collectés | Readiness (H0.5) | Action |
|---------|-----------------|-------------------|--------|
| "Je cherche un appartement à Douala" | transaction=rent, property_type=apartment, city=douala | INTENT_IDENTIFIED | Confirmer intention |
| "Entre 30 et 50 millions" | + budget_max=50M, budget_min=30M | MINIMUM_INTAKE_READY | Demander quartier |
| "Bonapriso, urgent" | + neighborhood=bonapriso | MINIMUM_SEARCH_READY | **Lancer recherche** |
| Résultats présentés | — | MINIMUM_MATCHING_READY | Collecter chambres, douches |
| "3 pièces, 1 douche" | + chambres=3, douches=1 | INTRODUCTION_READY | Demander contact |
| "Jean, 691234567" | + nom=Jean, téléphone=691234567 | VISIT_READY | Proposer visite |
| "Vendredi à 10h" | + visit_date=vendredi | TRANSACTION_READY | Caution + charges |

### 7.2 Tenant — Marie cherche un studio à Yaoundé

| Message | Champs collectés | Readiness (H0.5) | Action |
|---------|-----------------|-------------------|--------|
| "Je cherche un studio à Yaoundé" | transaction=rent, property_type=studio, city=yaoundé | INTENT_IDENTIFIED | Confirmer |
| "Budget max 100k par mois" | + budget_max=100k | MINIMUM_INTAKE_READY | Demander quartier |
| "Au quartier Mfandena" | + neighborhood=mfandena | MINIMUM_SEARCH_READY | **Lancer recherche** |
| Résultats présentés | — | MINIMUM_MATCHING_READY | Cuisine, meublé |
| "Cuisine interne, meublé" | + cuisine=interne, meuble=oui | INTRODUCTION_READY | Demander contact |
| "Marie, 698765432" | + nom=Marie, téléphone=698765432 | VISIT_READY | Planifier visite |
| Confirmation | + visit_date | TRANSACTION_READY | Caution + charges |

### 7.3 Seller — Paul veut vendre sa villa à Buea

| Message | Champs collectés | Readiness (H0.5) | Action |
|---------|-----------------|-------------------|--------|
| "Je veux vendre ma villa à Buea" | transaction=sell, property_type=villa, city=buea | INTENT_IDENTIFIED | Confirmer |
| "Prix 150 millions" | + desired_price=150M | MINIMUM_INTAKE_READY | Quartier, surface |
| "Molyko, 200m2, 4 chambres" | + neighborhood=molyko, surface=200, chambres=4 | MINIMUM_SEARCH_READY | **Estimation + publication** |
| Résultats — estimation faite | + titre_foncier=oui | MINIMUM_MATCHING_READY | Affiner critères |
| "Paul, 695432198" | + nom=Paul, téléphone=695432198 | INTRODUCTION_READY | Proposer accompagnement |
| "Oui, accompagnement" | + accompagnement=oui | VISIT_READY | Planifier visites acheteurs |
| Photos + titre fournis | + photos, documents | TRANSACTION_READY | Publier + notaire |

### 7.4 Investor — Kwame veut investir depuis Paris

| Message | Champs collectés | Readiness (H0.5) | Action |
|---------|-----------------|-------------------|--------|
| "Je veux investir dans l'immobilier au Cameroun" | transaction=buy, property_type=land, diaspora=true | INTENT_IDENTIFIED | Détecter diaspora, qualifier |
| "Terrain à Douala" | + city=douala | MINIMUM_INTAKE_READY | Budget, surface |
| "Budget 100M, 500m2, usage prévu construction" | + budget_max=100M, surface=500, usage_prevu=construction | MINIMUM_SEARCH_READY | **Lancer recherche terrains** |
| Résultats terrains titrés | — | MINIMUM_MATCHING_READY | Type document, accessibilité |
| "Titre foncier requis" | + type_document=titre_foncier | INTRODUCTION_READY | Contact info |
| "Kwame, +33712345678" | + nom=Kwame, téléphone=+33712345678 | VISIT_READY | Proposer visite terrain |
| "Oui visite la semaine prochaine" | + visite_souhaitee=oui, disponibilite | TRANSACTION_READY | Notaire + financement |

---

## 8. Implémentation — ReadinessCalculator (H0.5)

The H0.5 ReadinessCalculator uses matrix-driven field resolution instead of hardcoded profiles:

```
class ReadinessCalculator:
    def __init__(self):
        self.matrices = load_json("qualification_matrices.json")
        self.rules = load_json("readiness_rules.json")
        self.fields = load_json("field_dictionary.json")

    def compute(self, context: QualificationContext) -> ReadinessResult:
        matrix = self._resolve_matrix(context)
        level = self._compute_level(context, matrix)

        required_fields = matrix.fields["minimum_" + level.suffix]
        collected_required = sum(1 for f in required_fields if f in context.collected)
        total_required = len(required_fields)

        recommended = matrix.fields.recommended
        collected_recommended = sum(1 for f in recommended if f in context.collected)
        total_recommended = len(recommended)

        numerator = collected_required + collected_recommended * 0.5
        denominator = total_required + total_recommended * 0.5
        completeness = (numerator / denominator * 100) if denominator > 0 else 0

        # Apply penalties from readiness_rules.json
        for penalty_def in self.rules.penalty_factors_by_level[level]:
            if self._penalty_applies(context, penalty_def):
                completeness -= self._penalty_value(penalty_def)

        return ReadinessResult(
            completeness_pct=round(max(0, completeness), 1),
            stage=level,
            matrix_id=matrix.matrix_id,
            collected=self._field_counts(context, matrix),
            missing=self._missing_by_level(context, matrix),
        )

    def _compute_level(self, context, matrix):
        levels = ["TRANSACTION_READY", "VISIT_READY", "INTRODUCTION_READY",
                  "MINIMUM_MATCHING_READY", "MINIMUM_SEARCH_READY",
                  "MINIMUM_INTAKE_READY", "INTENT_IDENTIFIED"]
        for level in levels:
            required = matrix.fields["minimum_" + self._level_suffix(level)]
            if all(f in context.collected for f in required):
                return level
        return "INTENT_IDENTIFIED"

    def _resolve_matrix(self, context):
        family = self._resolve_family(context)
        candidates = [m for m in self.matrices.matrices
                      if m.request_family == family
                      and context.transaction_type in m.transaction_type
                      and m.property_type == context.property_type]
        return candidates[0] if candidates else self.FALLBACK_MATRIX
```

**H1 compatibility shim** (maps H0.5 levels to legacy H1 stages for backward compatibility):

```
    def _legacy_stage(self, h05_level):
        mapping = {
            "INTENT_IDENTIFIED": "NOT_READY",
            "MINIMUM_INTAKE_READY": "NOT_READY",
            "MINIMUM_SEARCH_READY": "SEARCH_READY",
            "MINIMUM_MATCHING_READY": "MATCHING_READY",
            "INTRODUCTION_READY": "VISIT_READY",
            "VISIT_READY": "VISIT_READY",
            "TRANSACTION_READY": "RELATIONSHIP_READY",
        }
        return mapping.get(h05_level, "NOT_READY")
```

---

*Document Gold — Modèle de maturité validé — 2026-07-15*
