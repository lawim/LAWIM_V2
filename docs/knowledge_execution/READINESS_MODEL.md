# READINESS MODEL — Modèle de Maturité de Qualification

**Mission :** LAWIM Heritage Gold
**Statut :** Modèle validé — Calcule la complétude et détermine le niveau d'action possible
**Références :** QUALIFICATION_MODEL.md §5-6, QUALIFICATION_EXECUTION_ARCHITECTURE.md §8, DOMAIN_MODEL.md GOLD-DM-014 (P5)

---

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

> **DEPENDENCY_H05:** Detailed readiness thresholds per property type and transaction type require H0.5 qualification matrices. The 4-level staging model (SEARCH → MATCHING → VISIT → RELATIONSHIP) is an `ARCHITECTURE_DECISION` awaiting refinement from H0.5.

---

## 7. Exemples complets par profil

### 7.1 Buyer — Jean cherche un appartement à Douala

| Message | Champs collectés | Completeness | Readiness | Action |
|---------|-----------------|:-----------:|-----------|--------|
| "Je cherche un appartement à Douala" | intent=buy, property_type=apartment, city=douala | 3/4 req = 75% of req = 50% overall | SEARCH_READY | Démarrer matching précoce |
| "Entre 30 et 50 millions" | + budget_max=50M, budget_min=30M | 4/4 req = 100% of req = 66.7% overall | MATCHING_READY | Envoyer premiers résultats |
| "Urgent, je veux visiter cette semaine" | + timeline=urgent | 4/4 + 1/4 rec = 4.5/6 = 75% | MATCHING_READY | Affiner matching |
| "3 pièces, premier étage si possible" | + rooms=3, floor=1 | 4/4 + 2/4 rec = 5.0/6 = 83% | VISIT_READY | Proposer visite |
| "Résidence principale" | + usage=primary | 4/4 + 3/4 rec = 5.5/6 = 91.7% | VISIT_READY | Qualification quasi-complète |
| Confirmation | intent confirmé | 100% | RELATIONSHIP_READY | Escalade agent |

### 7.2 Tenant — Marie cherche un studio à Yaoundé

| Message | Champs collectés | Completeness | Readiness | Action |
|---------|-----------------|:-----------:|-----------|--------|
| "Je cherche un studio à Yaoundé" | intent=rent, property_type=studio, city=yaoundé | 3/4 req = 75% of req | SEARCH_READY | Préparer recherche |
| "Budget max 100k par mois" | + monthly_budget=100k | 4/4 req = 100% of req = 72.7% | MATCHING_READY | Envoyer studios disponibles |
| "Au quartier Mfandena" | + neighborhood=mfandena | 4/4 + 1/3 rec = 4.5/5.5 = 81.8% | VISIT_READY | Filtrer par quartier |
| "Je préfère meublé" | + furnished=true | 4/4 + 1/3 rec = 4.5/5.5 = 81.8% | VISIT_READY | Proposer visite |
| Confirmation | | 100% | RELATIONSHIP_READY | Mise en relation |

### 7.3 Seller — Paul veut vendre sa villa à Buea

| Message | Champs collectés | Completeness | Readiness | Action |
|---------|-----------------|:-----------:|-----------|--------|
| "Je veux vendre ma villa à Buea" | intent=sell, property_type=villa, city=buea | 3/4 req | SEARCH_READY | Préparer estimation |
| "Prix 150 millions" | + desired_price=150M | 4/4 req = 66.7% | MATCHING_READY | Proposer mise en ligne |
| "J'ai le titre foncier" | + title_deed=true | 4/4 + 1/4 rec = 4.5/6 = 75% | MATCHING_READY | Accélérer publication |
| "Surface 200m2, 4 chambres" | + surface=200, bedrooms=4 | 4/4 + 2/4 rec = 5.0/6 = 83% | VISIT_READY | Proposer accompagnement |
| Confirmation + photos | + photos | 100% | RELATIONSHIP_READY | Publier + agent |

### 7.4 Investor — Kwame veut investir depuis Paris

| Message | Champs collectés | Completeness | Readiness | Action |
|---------|-----------------|:-----------:|-----------|--------|
| "Je veux investir dans l'immobilier au Cameroun" | intent=invest, diaspora_flag=true | 1/4 req | — | Détecter diaspora, qualifier |
| "Je suis à Paris" | diaspora confirmé | 1/4 req | — | Booster diaspora |
| "Terrain à Douala" | + city=douala, property_type=land | 2/4 req = 50% req = 36.4% | SEARCH_READY | Recherche terrains |
| "Budget 100 millions" | + budget=100M | 3/4 req = 75% req = 54.5% | SEARCH_READY | Matching précoce |
| "Pour construire et revendre" | + investment_type=revente | 4/4 req = 100% req = 72.7% | MATCHING_READY | Envoyer résultats terrains |
| "Rendement 15% attendu" | + expected_yield=15 | 4/4 + 1/3 rec = 4.5/5.5 = 81.8% | VISIT_READY | Proposer visite terrain |
| Confirmation | | 100% | RELATIONSHIP_READY | Agent + services diaspora |

---

## 8. Implémentation — ReadinessCalculator

```
class ReadinessCalculator:
    PROFILES = {
        "buyer": {"required": 4, "recommended": 4},
        "tenant": {"required": 4, "recommended": 3},
        "seller": {"required": 4, "recommended": 4},
        "investor": {"required": 4, "recommended": 3},
    }

    def compute(self, context: QualificationContext) -> ReadinessResult:
        profile = self._get_profile(context.role)
        required_collected = self._count_required_collected(context, profile)
        recommended_collected = self._count_recommended_collected(context, profile)

        numerator = required_collected + recommended_collected * 0.5
        denominator = profile.required + profile.recommended * 0.5
        completeness = (numerator / denominator) * 100 if denominator > 0 else 0

        return ReadinessResult(
            completeness_pct=round(completeness, 1),
            stage=self._map_stage(completeness),
            missing_required=self._missing_required(context, profile),
            missing_recommended=self._missing_recommended(context, profile),
        )

    def _map_stage(self, pct: float) -> ReadinessStage:
        if pct >= 100: return RELATIONSHIP_READY
        if pct >= 85:  return VISIT_READY
        if pct >= 65:  return MATCHING_READY
        if pct >= 40:  return SEARCH_READY
        return NOT_READY
```

---

*Document Gold — Modèle de maturité validé — 2026-07-15*
