# DOMAIN MODEL — Modèle de domaines LAWIM

**Source :** LAWIM + LAWIMA + ancienne_structure
**Principe :** Documentation des domaines métier, entités et relations — sans validation

---

## 1. Domaines métier identifiés

### 1.1 Domaines principaux

| Domaine | Description | Sources |
|---------|-------------|---------|
| **Immobilier** | Gestion des biens immobiliers, types, cycles de vie, transactions | LAWIM Directive/02*, LAWIMA property_lifecycle_engine |
| **Géographie** | Référentiel géographique Cameroun, villes, quartiers, zones | LAWIM KNOWLEDGE/geography, LAWIMA location_normalizer |
| **Qualification** | Scoring des leads, classification, profils utilisateurs | LAWIMA lead_scorer, lead_classifier, RULE_ENGINE |
| **Conversation** | Dialogue utilisateur, intentions, réponses multilingues | LAWIM Directive/03, LAWIMA engine conversation |
| **Matching** | Appariement offre-demande, scoring, recommandations | LAWIMA property_matcher, LAWIM matching docs |
| **CRM** | Gestion des relations clients, agents, organisations | LAWIMA user_roles, agent_optin, SQL schemas |
| **Négociation** | Techniques commerciales, objections, closing | LAWIM sales-playbook, negotiation-patterns |
| **Communication** | Canaux (WhatsApp, Telegram, Email, Dashboard) | LAWIMA gateways, LAWIM notification docs |
| **Paiement** | Monétisation, abonnements, boosts | LAWIMA monetisation, CAMPAY_CONFIG |
| **Knowledge** | Base de connaissance, apprentissage continu | LAWIM KNOWLEDGE/, LAWIMA knowledge_enricher |
| **Fraude / Confiance** | Détection fraude, vérification, scoring confiance | LAWIM fraud-signals, LAWIMA anti_spam |
| **Workflow** | Processus métier, états, transitions | LAWIM Directive/05, LAWIMA state_machine |

### 1.2 Domaines support

| Domaine | Description | Sources |
|---------|-------------|---------|
| **Identity Resolution** | Détection et fusion des doublons | LAWIMA identity_resolution |
| **Data Quality** | Score de qualité des données et sources | LAWIMA data_quality_engine |
| **Mémoire** | Conversation memory, long-term memory | LAWIMA conversation_memory, long_term_memory |
| **Anti-spam** | Rate limiting et blocage | LAWIMA anti_spam |
| **Feedback** | Évaluation utilisateur (thumbs up/down, notes) | LAWIMA feedback_handler |
| **Relance** | Follow-up multi-échéances | LAWIMA follow_up_system |
| **Agent Opt-In** | Permission partage contact agent | LAWIMA agent_optin |
| **Agent Rating** | Notation des agents | LAWIMA agent_rating |
| **Phone Formatting** | Normalisation numéros téléphone internationaux | LAWIMA phone_formatter |
| **Diaspora** | Détection et services diaspora | LAWIMA diaspora_filter |
| **File Upload** | Gestion des uploads (photos, CNI) | LAWIMA file_upload |
| **Event Logging** | Journalisation des événements | LAWIMA event_logger |
| **Gouvernance** | Rapports, transmission, inventaire | LAWIMA governance scripts |

## 2. Entités métier principales

### 2.1 Personne (Person)

Acteur du système (demandeur, vendeur, agent, etc.)

**Champs identifiés :**
- id, name, phone, email, city, country
- status
- tracking_code (follow-up tracking)
- max_role_level (niveau de rôle maximum atteint)
- max_role (rôle maximum : demandeur, vendeur, agent, assistant, master, etc.)
- is_admin (booléen)
- is_vendor (booléen)
- diaspora_flag (booléen, détection diaspora)

**Sources :** LAWIMA `persons` table (SQL), LAWIMA pipeline_supabase

### 2.2 Canal de contact (ContactChannel)

Moyen de contacter une personne

**Types de canal :** whatsapp, telegram, email, phone, sms
**Champs :** id, person_id, channel_type, value, is_primary

**Sources :** LAWIMA `contact_channels` table (SQL)

### 2.3 Agent

Professionnel de l'immobilier

**Champs :** id, person_id, company, license, speciality, zone
**Attributs additionnels :** lead_price (défaut 500 FCFA), rating (1-5), credits

**Sources :** LAWIMA `agents` table, agent_rating, agent_dashboard

### 2.4 Propriété (Property)

Bien immobilier mis en vente ou location

**Champs identifiés :**
- id, owner_id, type, price, location, description
- surface, rooms, bedrooms, bathrooms, floor
- has_elevator, is_furnished (logement)
- is_agricultural, is_constructible, has_water, has_electricity (terrain)
- front_window, parking_spots, has_signage (commerce)
- status (available/pending/rented/sold/archived)
- images (tableau d'URLs)
- source, quality_score (0-100)
- boost_level, verification_status
- diaspora_ready (booléen)
- title_status

**Sources :** LAWIMA `properties` table, property_lifecycle_engine, property_types.py

### 2.5 Lead

Opportunité commerciale générée par une conversation

**Champs :** id, person_id, message, intent, budget, location, property_type, urgency, score, status, priority, diaspora_flag

**Sources :** LAWIMA `leads` table, lead_scorer, lead_classifier

### 2.6 Source de données (DataSource)

Source d'import des propriétés

**Types :** agent, google_form, import, whatsapp
**Attributs :** name, type, reliability (score de fiabilité)

**Sources :** LAWIMA data_quality_engine

### 2.7 Entrée de connaissance (KnowledgeEntry)

Connaissance apprise ou importée

**Types :** location, synonym, property_type, intent
**Champs :** id, type, value, synonyms[], confidence, source

**Sources :** LAWIMA knowledge_enricher

### 2.8 Événement (Event)

Trace d'activité dans le système

**Types :** message.received, intent.detected, user.created, user.state_changed, property.created, lead.created, match.generated, payment.success, subscription.renewed, boost.applied, access.granted

**Sources :** LAWIMA EVENT_TYPES, event_logger

### 2.9 Litige (Dispute)

Réclamation utilisateur

**Champs :** id, person_id, reason, status (open/resolved)

**Sources :** LAWIMA `disputes` table, RESPONSE_POLICY

### 2.10 Demande d'anonymisation (AnonymizationRequest)

Demande RGPD de suppression des données

**Sources :** LAWIMA `anonymization_requests` table, RESPONSE_POLICY

## 3. Relations entre entités

```
Personne (1) ──── a plusieurs ────► Canal de contact (N)
Personne (1) ──── peut être ─────► Agent (0..1)
Personne (1) ──── possède ───────► Propriété (N)
Personne (1) ──── génère ────────► Lead (N)
Personne (1) ──── peut avoir ─────► Litige (N)
Personne (1) ──── peut demander ──► Anonymisation (0..1)
Propriété (1) ──── a un ──────────► Cycle de vie (N états)
Lead (1) ───────── est lié à ─────► Propriété (N) via matching
Agent (1) ──────── reçoit ────────► Lead (N) via matching
Propriété (1) ──── a une ─────────► Source (1)
Agent (1) ──────── a des ─────────► Credits (N)
```

## 4. Règles métier globales

### 4.1 Règles fondamentales (Constitution LAWIM)

**Source :** LAWIM `Directive/00-CONSTITUTION.md`

1. LAWIM est un intermédiaire de mise en relation — zéro commission sur transactions
2. Le cœur du système est la donnée, pas WhatsApp
3. WhatsApp est l'interface principale mais pas exclusive
4. Toutes les interactions doivent pouvoir basculer sur n'importe quel canal
5. Le matching est le cœur de la proposition de valeur
6. La qualification est la fondation de la confiance
7. Les agents sont des clients, pas des ressources
8. Le système doit fonctionner avec ou sans connexion permanente (offline-first)

### 4.2 Règles commerciales

**Sources :** LAWIMA RESPONSE_POLICY, LAWIM Constitution

- Service gratuit : mise en relation, matching, recherche de biens
- Service payant : accompagnement personnalisé (50 000 FCFA)
- Zéro commission sur les transactions finales
- Les agents paient pour les leads (500 FCFA/lead par défaut)
- Les boosts sont optionnels et payants
- Les abonnements premium sont désactivés (feature flag)

### 4.3 Règles de protection

**Sources :** LAWIMA RESPONSE_POLICY, LAWIM Constitution

- RGPD : droit à l'effacement sous 7 jours (commande `SUPPRIMER MES DONNÉES`)
- Opt-in obligatoire avant partage de contact agent
- Signalement des litiges : commande `SIGNALER`
- Pas de garantie sur les biens (score indicatif seulement)
- Orientation vers notaire pour les questions juridiques

### 4.4 Feature flags

**Source :** LAWIMA `08_CONFIG/features/FEATURE_FLAGS.json`

**Activés :** whatsapp_core, property_ingestion, matching_simple, lead_generation
**Désactivés :** payments, boost_system, agent_subscription, lead_scoring_ai, dashboard, diaspora_services, advanced_matching, subscriptions_complex, data_engine, auction_boost_system, ai_pricing_estimator, marketplace_payments, escrow_system, multi_city_expansion

### 4.5 Anti-spam

**Source :** LAWIMA `03_ENGINE/anti_spam.py`

- Maximum 10 messages/minute par utilisateur
- Blocage automatique pour 60 minutes
- Table `blocked_users`

---

*Document patrimonial — Aucune décision de reconstruction n'est prise ici.*
