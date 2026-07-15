# QUALIFICATION MODEL — Modèle de qualification LAWIM

**Sources :** LAWIMA `lead_scorer/`, `lead_classifier/`, `RULE_ENGINE_V*.json`, `data_quality_engine.py`, `pipeline_supabase_final.py`, LAWIM `KNOWLEDGE/qualification*`, `KNOWLEDGE/conversation-qualification-questions.md`
**Principe :** Documentation exhaustive des règles de qualification

---

## 1. Profils utilisateurs qualifiables

### 1.1 Types d'utilisateurs (classification)

**Source :** LAWIMA `06_AI_MODELS/lead_classifier/lead_classifier_v1.json`, `RULE_ENGINE_V3.json`

| Type | Base score | Description |
|------|-----------|-------------|
| tenant | 40 | Locataire potentiel |
| buyer | 60 | Acheteur potentiel |
| seller | 50 | Vendeur |
| investor | 80 | Investisseur |
| diaspora_investor | 95 | Investisseur diaspora |
| property_seeker | — | Chercheur de bien |
| agent | — | Agent immobilier |
| owner | — | Propriétaire |
| broker | — | Courtier/intermédiaire |

### 1.2 Informations par profil

**Source :** LAWIM `KNOWLEDGE/conversation-qualification-questions.md`

#### Acheteur (buyer)
**Obligatoire :** type de bien souhaité, ville, budget maximum
**Recommandé :** quartier, délai, nombre de pièces, usage (résidence principale/investissement)
**Optionnel :** source de financement, situation actuelle (locataire/propriétaire)

#### Locataire (tenant)
**Obligatoire :** type de bien, ville, budget mensuel
**Recommandé :** quartier, durée souhaitée, nombre de pièces
**Optionnel :** meublé/non meublé, animaux acceptés, parking

#### Vendeur (seller)
**Obligatoire :** type de bien, ville, prix souhaité
**Recommandé :** titre de propriété, surface, description détaillée, photos
**Optionnel :** motif de vente, disponibilité, historique du bien

#### Investisseur (investor)
**Obligatoire :** budget, type d'investissement (locatif/revente/terrain), ville
**Recommandé :** rendement attendu, horizon, zone préférée
**Optionnel :** expérience immobilière, autres investissements

### 1.3 Ordre conseillé de qualification

**Source :** LAWIMA `conversation_flows_v1.json`

Ordre général : Type de besoin → Ville → Budget → Type de bien → Quartier → Délai → Contact

### 1.4 Niveau minimal de complétude

**Source :** LAWIM `KNOWLEDGE/minimum-fields-request.md`

Pour qu'une requête soit qualifiée comme lead, elle doit contenir au minimum :
- Un type de bien (même implicite : "je cherche une maison")
- Une localisation (ville minimum)
- Un indicateur de budget (même approximatif : "pas trop cher")

## 2. Scoring des leads

### 2.1 Système de scores (V1)

**Source :** LAWIMA `03_ENGINE/lead_scorer/lead_scorer.py`, `06_AI_MODELS/lead_classifier/lead_classifier_v1.json`

#### Scores de base par type d'utilisateur

| Rôle | Score de base |
|------|--------------|
| Locataire (tenant) | 40 |
| Acheteur (buyer) | 60 |
| Vendeur (seller) | 50 |
| Investisseur (investor) | 80 |
| Investisseur diaspora (diaspora_investor) | 95 |

#### Boosters

| Signal | Bonus |
|--------|-------|
| Budget détecté | +15 |
| Ville détectée | +10 |
| Quartier détecté | +10 |
| Urgence exprimée | +20 |
| Diaspora détectée | +25 |
| Achat comptant | +15 |
| Message > 20 caractères | +30 |
| Budget présent | +25 |
| Localisation présente | +25 |
| Type de bien présent | +20 |

#### Pénalités

| Signal | Malus |
|--------|-------|
| Budget manquant | -10 |
| Localisation floue | -10 |
| Message suspect (spam) | -50 |

### 2.2 Seuils de classification

| Classe | Seuil V1 | Seuil V5 |
|--------|----------|----------|
| HOT | ≥ 80 | ≥ 0.8 |
| WARM | ≥ 60 | ≥ 0.5 |
| COLD | ≥ 40 | ≥ 0.3 |
| LOW / SPAM | < 40 | ≥ 0.2 (spam) |

### 2.3 Scoring V5 (CRM Intelligence)

**Source :** LAWIMA `08_CONFIG/rule_engine/RULE_ENGINE_V5.json`

#### Pondérations CRM V5

| Critère | Poids |
|---------|-------|
| Intérêt de base (base_interest) | 0.15 |
| Correspondance type de bien (property_type_match) | 0.20 |
| Précision de la localisation (location_precision) | 0.20 |
| Présence du budget (budget_presence) | 0.10 |
| Signal d'urgence (urgency_signal) | 0.15 |
| Intention de visite (visit_intent) | 0.20 |
| Signal de confiance (trust_signal) | 0.10 |

### 2.4 Actions recommandées par classe

| Classe | Action |
|--------|--------|
| HOT | call_immediately (appeler immédiatement) |
| WARM | send_listings (envoyer des annonces) |
| COLD | request_budget (demander budget) |
| LOW | follow_up (relance) |
| SPAM | ignore (ignorer) |

## 3. Qualification des utilisateurs

### 3.1 Champs extraits par KnowledgeBuilder

**Source :** LAWIMA `03_ENGINE/knowledge_builder.py`

32 champs de profil utilisateur (non listés exhaustivement ici, voir la source) :
- Nom, téléphone, email, ville, pays
- Type de bien recherché, budget, localisation
- Urgence, intention, source
- Satisfaction précédente, historique de recherche
- ... (25+ autres champs)

### 3.2 Champs de lead (7)

- message, intent, budget, location, property_type
- urgency, score

### 3.3 Complétude du profil

Calculée comme `X / total_champs` où X est le nombre de champs remplis.

## 4. Comportements traqués

**Source :** LAWIMA `08_CONFIG/rule_engine/RULE_ENGINE_V5.json`

- message_history
- response_time_tracking
- budget_changes_tracking
- visit_requests_tracking

## 5. Détection de la diaspora

**Source :** LAWIMA `03_ENGINE/diaspora_filter.py`, `02_KNOWLEDGE/whatsapp_language/diaspora_language.json`

### 5.1 Indicateurs de diaspora

**Pays/localisations :** france, paris, lyon, etats-unis, usa, canada, allemagne, belgique, suisse, uk, londres, diaspora, international

**Indicatifs téléphoniques :** +33, +1, +44, +49

### 5.2 Boost diaspora

- Score diaspora_investor : base 95 (le plus élevé)
- Boost matching : +20

### 5.3 Services diaspora

Table dédiée `diaspora_services` pour des offres spécifiques.

## 6. Anti-spam

**Source :** LAWIMA `03_ENGINE/anti_spam.py`

- Limite : 10 messages/minute
- Blocage : 60 minutes
- Table : blocked_users
- Pénalité scoring : -50 si spam détecté

## 7. Données de qualification (fichiers JSON)

**Source :** LAWIM `KNOWLEDGE/lead_scoring/lead_scoring.json`, LAWIMA `02_KNOWLEDGE/scoring/lead_scoring_rules.json`

Deux fichiers distincts contenant des règles de scoring :
- `lead_scoring.json` : Règles et poids de scoring
- `lead_scoring_rules.json` : Règles détaillées (scoring/ dossier)

Les contenus exacts sont dans les fichiers sources.

## 8. Pipeline de qualification (V5)

**Source :** LAWIMA `08_CONFIG/rule_engine/RULE_ENGINE_V5.json`

Pipeline complet en 8 étapes :
1. incoming_message → normalize_text
2. normalize_text → extract_entities
3. extract_entities → detect_intent
4. detect_intent → context_enrichment
5. context_enrichment → lead_scoring
6. lead_scoring → lead_classification
7. lead_classification → crm_routing
8. crm_routing → response

Couches additionnelles : anti-fraud (broker_spam_detection, duplicate_listing_detection, fake_price_detection, suspicious_urgency_detection)

---

*Document patrimonial — Aucune décision de reconstruction n'est prise ici.*
