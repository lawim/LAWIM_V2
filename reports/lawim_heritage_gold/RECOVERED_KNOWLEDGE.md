# RAPPORT DE RÉCUPÉRATION DES CONNAISSANCES MÉTIER LAWIM H0

**Date :** 2026-07-15  
**Mission :** Récupération des 6 connaissances oubliées et de toute connaissance métier absente  
**Sources :** `/media/abel/Doc/Drive/d/LAWIM_BACKUP_20260608_125026/LAWIMA/`

---

## Identifiant : KNW-FEATURE-FLAGS-001

### Titre : Feature Flags (État des fonctionnalités activées/désactivées)

### Description
Fichier JSON listant l'ensemble des feature flags du système LAWIM. Les flags contrôlent l'activation/désactivation des fonctionnalités métier. On distingue 3 groupes : les flags activés en production, les flags en attente d'activation, et les flags futurs/vision.

### Source
**Fichier :** `08_CONFIG/features/FEATURE_FLAGS.json`  
**Chemin :** `/media/abel/Doc/Drive/d/LAWIM_BACKUP_20260608_125026/LAWIMA/08_CONFIG/features/FEATURE_FLAGS.json`

### Extrait textuel
```json
{
  "whatsapp_core": true,
  "property_ingestion": true,
  "matching_simple": true,
  "lead_generation": true,

  "payments": false,
  "boost_system": false,
  "agent_subscription": false,
  "lead_scoring_ai": false,
  "dashboard": false,

  "diaspora_services": false,
  "advanced_matching": false,
  "subscriptions_complex": false,
  "data_engine": false,

  "auction_boost_system": false,
  "ai_pricing_estimator": false,
  "marketplace_payments": false,
  "escrow_system": false,
  "multi_city_expansion": false
}
```

### Niveau de confiance : ÉLEVÉ

### Valeurs et définitions

| Flag | Statut | Description |
|------|--------|-------------|
| `whatsapp_core` | `true` | Noyau WhatsApp (messagerie, réception/émission de messages) |
| `property_ingestion` | `true` | Ingestion de biens immobiliers |
| `matching_simple` | `true` | Matching simple propriétés/requêtes |
| `lead_generation` | `true` | Génération de leads |
| `payments` | `false` | Système de paiement |
| `boost_system` | `false` | Système de boost de visibilité |
| `agent_subscription` | `false` | Abonnement agent immobilier |
| `lead_scoring_ai` | `false` | Score IA des leads |
| `dashboard` | `false` | Tableau de bord |
| `diaspora_services` | `false` | Services diaspora |
| `advanced_matching` | `false` | Matching avancé (fuzzy + IA) |
| `subscriptions_complex` | `false` | Abonnements complexes récurrents |
| `data_engine` | `false` | Moteur de qualité de données |
| `auction_boost_system` | `false` | Système d'enchères boost |
| `ai_pricing_estimator` | `false` | Estimation de prix par IA |
| `marketplace_payments` | `false` | Paiements marketplace |
| `escrow_system` | `false` | Système d'entiercement |
| `multi_city_expansion` | `false` | Expansion multi-villes |

---

## Identifiant : KNW-ANTISPAM-001

### Titre : Anti-spam (Règles de limitation et blocage)

### Description
Système anti-spam intégré à WhatsApp. Limite le nombre de messages à 10 par minute par utilisateur. En cas de dépassement, l'utilisateur est bloqué pendant 60 minutes. Utilise Supabase pour le tracking.

### Source
**Fichier :** `03_ENGINE/anti_spam.py`  
**Chemin :** `/media/abel/Doc/Drive/d/LAWIM_BACKUP_20260608_125026/LAWIMA/03_ENGINE/anti_spam.py`

### Extrait textuel
```python
"""
Système anti-spam
Limite à 10 messages par minute par utilisateur
"""

class AntiSpam:
    def __init__(self):
        self.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.MAX_PER_MINUTE = 10
        self.BLOCK_DURATION = 60  # minutes
```

### Niveau de confiance : ÉLEVÉ

### Règles et valeurs

| Paramètre | Valeur | Description |
|-----------|--------|-------------|
| `MAX_PER_MINUTE` | **10** | Nombre max de messages par minute avant déclenchement |
| `BLOCK_DURATION` | **60 minutes** | Durée de blocage après détection de spam |
| `TABLE_SOURCE` | `whatsapp_logs` | Table des logs WhatsApp pour comptage |
| `TABLE_BLOCKED` | `blocked_users` | Table des utilisateurs bloqués |
| `MATCH_FIELD` | `phone` | Identification par numéro de téléphone |
| `REASON_FORMAT` | `"Spam: {count} msg/minute"` | Format de la raison de blocage |
| `is_blocked()` | Vérifie si le blocage est expiré | Débloque automatiquement après `BLOCK_DURATION` |
| `SUPABASE_URL` | `https://nfmgvjcpnyhigafwhqzj.supabase.co` | URL Supabase |
| `SUPABASE_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` | Clé Supabase |

---

## Identifiant : KNW-RULE-ENGINE-V2-002

### Titre : Rule Engine V2 - Normalisation et extraction d'intentions

### Description
Première version du moteur de règles LAWIM dédié à la normalisation des messages WhatsApp et à l'extraction d'intentions pour le marché immobilier camerounais.

### Source
**Fichier :** `08_CONFIG/rule_engine/RULE_ENGINE_V2.json`  
**Chemin :** `/media/abel/Doc/Drive/d/LAWIM_BACKUP_20260608_125026/LAWIMA/08_CONFIG/rule_engine/RULE_ENGINE_V2.json`

### Niveau de confiance : ÉLEVÉ

### Règles et valeurs

**Normalisation :**
- `case` → `lowercase_all_text`
- `remove_accents` → `true`
- `trim_spaces` → `true`

**Property Type Mapping (variantes orthographiques) :**
| Type canonique | Variantes |
|----------------|-----------|
| `studio` | `studio, stido, studia, stu, 1ch, single room` |
| `apartment` | `appartement, appart, apart, aprt, flat` |
| `villa` | `villa, vila, lux villa, haut standing` |
| `house` | `maison, house, mason, maisson` |
| `duplex` | `duplex, duplix, duplexe, dup` |
| `land` | `terrain, plot, land, m2, sqm` |

**Location Mapping :**
| Quartier canonique | Variantes |
|--------------------|-----------|
| `bastos` | `bastos, basto, bastoss, bastos village` |
| `essos` | `essos, esos, essoss` |
| `biyem_assi` | `biyem, biyem-assi, biyemassi, biem assi` |
| `odza` | `odza, odzaa, odja` |
| `akwa` | `akwa, aqua, akwah` |
| `bonamoussadi` | `bonamoussadi, bona moussadi, bonamussadi` |

**Intent Detection :**
| Intention | Déclencheurs |
|-----------|--------------|
| `search_property` | `je cherche, i need, looking for, besoin, recherche` |
| `sell_property` | `je vends, for sale, j'ai un terrain, proprio` |
| `visit_request` | `visite, visit, voir, check` |
| `price_signal` | `prix, budget, max, k, mille` |
| `urgency` | `urgent, asap, vite, rapide` |

**Price Parser :**
- `k_format` → `multiply_by_1000`
- `mille_format` → `multiply_by_1000`
- `range_detection` → `extract_min_max`

**Rule Priority :**
1. `normalize_text`
2. `detect_intent`
3. `extract_property_type`
4. `extract_location`
5. `extract_price`
- `fallback` → `send_to_ai`

---

## Identifiant : KNW-RULE-ENGINE-V3-003

### Titre : Rule Engine V3 - Moteur contextuel avec scoring de leads

### Description
Seconde évolution du moteur de règles. Architecture en 4 couches : nettoyage, fuzzy matching, extraction sémantique, et contexte métier. Introduction du scoring de leads pondéré et de la classification utilisateur (6 profils).

### Source
**Fichier :** `08_CONFIG/rule_engine/RULE_ENGINE_V3.json`  
**Chemin :** `/media/abel/Doc/Drive/d/LAWIM_BACKUP_20260608_125026/LAWIMA/08_CONFIG/rule_engine/RULE_ENGINE_V3.json`

### Niveau de confiance : ÉLEVÉ

### Règles et valeurs

**Layer 1 - Cleaning :**
- `lowercase`, `remove_accents`, `trim_spaces`, `remove_noise_words`

**Layer 2 - Fuzzy Matching (méthode : `levenshtein + dictionary boost`) :**
- Property types : `studio`, `apartment`, `villa`, `house`, `land`
- Locations : `bastos`, `essos`, `biyem_assi`, `bonamoussadi`, `odza`

**Layer 3 - Semantic Extraction :**
- Entités : `property_type`, `location`, `price`, `urgency`, `intent`, `transaction_type`
- `multi_intent_allowed` → `true`

**Intents :**
| Intention | Déclencheurs |
|-----------|--------------|
| `search` | `je cherche, looking for, need, besoin` |
| `sell` | `je vends, for sale, proprio, j'ai un` |
| `visit` | `visite, see, check` |
| `price` | `budget, max, prix, k, mille` |
| `urgent` | `urgent, asap, vite` |

**Layer 4 - Business Context Engine :**

**User Classification (6 profils) :**
| Profil | Signal |
|--------|--------|
| `property_seeker` | Search intent + budget mention |
| `agent` | Multiple listings + commission language |
| `owner` | Direct property ownership signals |
| `investor` | ROI + rendement + cashflow language |
| `diaspora` | Abroad + trust + verification signals |
| `broker` | Connection + transport fee + intermediary signals |

**Lead Scoring Weights :**
| Signal | Poids |
|--------|-------|
| `urgency` | **0.25** |
| `budget` | **0.25** |
| `visit` | **0.20** |
| `location` | **0.20** |
| `engagement` | **0.10** |

**Output Format :**
```json
{
  "normalized_text": "",
  "entities": {},
  "intent": [],
  "user_type": "",
  "lead_score": 0
}
```

---

## Identifiant : KNW-RULE-ENGINE-V4-004

### Titre : Rule Engine V4 - CRM Intelligence avec scoring et classes de leads

### Description
Troisième évolution. Introduction de la localisation intelligente (Yaoundé/Douala avec quartiers), des règles de pricing, et des classes de leads (hot/warm/cold) avec seuils.

### Source
**Fichier :** `08_CONFIG/rule_engine/RULE_ENGINE_V4.json`  
**Chemin :** `/media/abel/Doc/Drive/d/LAWIM_BACKUP_20260608_125026/LAWIMA/08_CONFIG/rule_engine/RULE_ENGINE_V4.json`

### Niveau de confiance : ÉLEVÉ

### Règles et valeurs

**Intent System :**
| Intention | Déclencheurs |
|-----------|--------------|
| `search_property` | `je cherche, je veux, need, looking for` |
| `sell_property` | `j'ai, je vends, proprio, available` |
| `investor_lead` | `investir, rentable, ROI, cash flow` |
| `broker_lead` | `je peux trouver, j'ai un contact` |
| `urgent_signal` | `urgent, asap, vite, rapidement` |
| `visit_request` | `visite, voir, visit, on passe` |

**Location Intelligence :**
| Ville | Quartiers |
|-------|-----------|
| `yaounde` | `bastos, essos, biyem assi, mvog, odza, nkoabang` |
| `douala` | `akwa, bonapriso, bonamoussadi, makepe, deido, bonaberi` |
| `fuzzy_locations` | `barrage, carrefour, derrière station, axe principal, non loin de` |

**Pricing Rules :**
- `k_conversion` → **1000**
- Patterns : `k`, `mille`, `000`
- Negotiation signals : `prix ferme`, `à débattre`, `dernier prix`

**Scoring V4 :**
| Critère | Poids |
|---------|-------|
| `base_interest` | **0.20** |
| `property_type_match` | **0.20** |
| `location_precision` | **0.20** |
| `budget_presence` | **0.10** |
| `urgency_context` | **0.20** |
| `visit_intent` | **0.20** |

**Lead Classes (seuils) :**
| Classe | Seuil min |
|--------|-----------|
| `hot` | **0.80** |
| `warm` | **0.50** |
| `cold` | **0.30** |

---

## Identifiant : KNW-RULE-ENGINE-V5-005

### Titre : Rule Engine V5 - Pipeline IA Ready complet avec anti-fraude

### Description
Version production finale du moteur de règles. Pipeline complet en 8 étapes, scoring enrichi (7 critères), classification à 4 niveaux (hot/warm/cold/spam), tracking comportemental, anti-fraude (4 détecteurs), couche IA Ready (mémoire, embeddings, LLM), et schéma de sortie CRM.

### Source
**Fichier :** `08_CONFIG/rule_engine/RULE_ENGINE_V5.json`  
**Chemin :** `/media/abel/Doc/Drive/d/LAWIM_BACKUP_20260608_125026/LAWIMA/08_CONFIG/rule_engine/RULE_ENGINE_V5.json`

### Niveau de confiance : ÉLEVÉ

### Règles et valeurs

**Pipeline Stages (8 étapes) :**
1. `incoming_message`
2. `normalize_text`
3. `extract_entities`
4. `detect_intent`
5. `context_enrichment`
6. `lead_scoring`
7. `lead_classification`
8. `crm_routing`

**Intent System :**
| Intention | Déclencheurs |
|-----------|--------------|
| `search_property` | `je cherche, looking for, need, besoin` |
| `sell_property` | `j'ai, je vends, available, proprio` |
| `investor_lead` | `investir, ROI, rentable, cash flow` |
| `broker_lead` | `je peux trouver, j'ai un contact` |
| `visit_request` | `visite, voir, visit` |
| `urgent_signal` | `urgent, asap, immediately, now, vite, rapidement` |

**Entity Extraction :**
- Property types : `studio, appartement, apartment, villa, house, maison, terrain, land, duplex, room, chambre, furnished, meublé`
- Locations : `bastos, essos, biyem assi, bonamoussadi, akwa, bonapriso`
- Fuzzy locations : `barrage, carrefour, derrière station, axe, non loin`
- Price patterns : `k, mille, 000, fcfa`

**CRM Scoring V5 :**
| Critère | Poids |
|---------|-------|
| `base_interest` | **0.15** |
| `property_type_match` | **0.20** |
| `location_precision` | **0.20** |
| `budget_presence` | **0.10** |
| `urgency_signal` | **0.15** |
| `visit_intent` | **0.20** |
| `trust_signal` | **0.10** |

**Lead Classification (seuils) :**
| Classe | Seuil min |
|--------|-----------|
| `hot` | **0.80** |
| `warm` | **0.50** |
| `cold` | **0.30** |
| `spam_risk` | **0.20** (en dessous) |

**Behavior Tracking :**
- `message_history` → `true`
- `response_time_tracking` → `true`
- `budget_changes_tracking` → `true`
- `visit_requests_tracking` → `true`

**Anti-Fraud (4 détecteurs) :**
- `broker_spam_detection` → `true`
- `duplicate_listing_detection` → `true`
- `fake_price_detection` → `true`
- `suspicious_urgency_detection` → `true`

**AI Ready Layer :**
- `memory_system` → `true`
- `conversation_context_window` → **10** (messages)
- Embedding fields : `normalized_text, intent, entities, location, budget_range`
- `future_llm_integration` → `true`

**CRM Output Schema :**
| Champ | Valeur |
|-------|--------|
| `lead_id` | `auto` |
| `score` | `0-1` |
| `status` | `hot\|warm\|cold\|spam` |
| `recommended_action` | `call_immediately, send_listings, request_budget, follow_up, ignore` |

---

## Identifiant : KNW-MONETISATION-006

### Titre : Monétisation (Modèle économique et services payants)

### Description
Module complet de monétisation LAWIM. Gère les services payants, achats unitaires, abonnements récurrents (mensuels), boosts de propriétés, plans agent (Pro/Business), premium demandeur, déblocage de coordonnées, leads payants (bronze/silver/gold), et services diaspora. Inclut la génération de factures, le cycle de vie complet (activation/expiration/renouvellement), et la vérification des services expirés.

### Sources
**Fichier 1 :** `core/monetisation.py`  
**Chemin :** `/media/abel/Doc/Drive/d/LAWIM_BACKUP_20260608_125026/LAWIMA/core/monetisation.py`

**Fichier 2 :** `core/monetisation_tables.sql`  
**Chemin :** `/media/abel/Doc/Drive/d/LAWIM_BACKUP_20260608_125026/LAWIMA/core/monetisation_tables.sql`

### Niveau de confiance : ÉLEVÉ

### Structure de données (SQL)

**Table `services` :** Catalogue des services payants
| Colonne | Type | Description |
|---------|------|-------------|
| `id` | SERIAL PK | Identifiant |
| `name` | TEXT UNIQUE | Nom du service |
| `description` | TEXT | Description |
| `price` | INTEGER | Prix en FCFA |
| `duration_days` | INTEGER DEFAULT 30 | Durée en jours (0 = achat unique) |
| `is_active` | BOOLEAN DEFAULT TRUE | Actif ou non |
| `created_at` | TIMESTAMP DEFAULT NOW() | Date de création |

**Table `purchases` :** Achats effectués
| Colonne | Type |
|---------|------|
| `id` | SERIAL PK |
| `user_id` | INTEGER FK→persons(id) |
| `service_name` | TEXT |
| `amount` | INTEGER |
| `status` | TEXT (pending, completed, failed, expired) |
| `payment_ref` | TEXT |
| `starts_at` | TIMESTAMP |
| `ends_at` | TIMESTAMP |
| `created_at` | TIMESTAMP |
| `completed_at` | TIMESTAMP |

**Table `invoices` :** Factures
| Colonne | Type |
|---------|------|
| `id` | SERIAL PK |
| `invoice_number` | TEXT UNIQUE |
| `user_id` | INTEGER FK→persons(id) |
| `service_name` | TEXT |
| `amount` | INTEGER |
| `tax` | INTEGER DEFAULT 0 |
| `total_amount` | INTEGER |
| `status` | TEXT DEFAULT pending |
| `payment_ref` | TEXT |
| `pdf_url` | TEXT |
| `created_at` | TIMESTAMP |
| `paid_at` | TIMESTAMP |

**Table `subscriptions` :** Abonnements récurrents
| Colonne | Type |
|---------|------|
| `id` | SERIAL PK |
| `user_id` | INTEGER FK→persons(id) |
| `service_name` | TEXT |
| `plan` | TEXT (monthly, quarterly, yearly) |
| `amount` | INTEGER |
| `status` | TEXT DEFAULT active |
| `starts_at` | TIMESTAMP |
| `ends_at` | TIMESTAMP |
| `auto_renew` | BOOLEAN DEFAULT TRUE |
| `last_payment_ref` | TEXT |
| `created_at` | TIMESTAMP |

### Catalogue des services (tarifs 2026)

| Service | Prix FCFA | Durée (jours) | Description |
|---------|-----------|---------------|-------------|
| `boost_7j` | **2 000** | 7 | Boost de visibilité 7 jours |
| `boost_30j` | **5 000** | 30 | Boost de visibilité 30 jours |
| `premium_listing` | **10 000** | 30 | Annonce premium |
| `agent_pro` | **10 000** | 30 | Abonnement Agent Pro (mensuel) |
| `agent_business` | **25 000** | 30 | Abonnement Agent Business (mensuel) |
| `lead_bronze` | **500** | 0 | Lead Bronze (score 40-60) |
| `lead_silver` | **1 500** | 0 | Lead Silver (score 60-80) |
| `lead_gold` | **3 000** | 0 | Lead Gold (score 80+) |
| `deblocage_coordonnees` | **500** | 0 | Déblocage coordonnées propriétaire |
| `demandeur_premium` | **1 000** | 30 | Compte Premium demandeur |
| `diaspora_simple` | **25 000** | 0 | Visite terrain diaspora |
| `diaspora_rapport` | **50 000** | 0 | Visite + rapport détaillé |
| `diaspora_complet` | **75 000** | 0 | Pack complet diaspora |

### Règles métier de monétisation

| Règle | Comportement |
|-------|-------------|
| `boost_*` | Active `boost_level=1` sur **toutes** les propriétés du user. Durée définie par `duration_days`. Expiration → `boost_level=0` |
| `agent_pro` | Plan `pro`, `subscription_active=true`, `subscription_plan='pro'` |
| `agent_business` | Plan `business`, `subscription_active=true`, `subscription_plan='business'` |
| `demandeur_premium` | `is_premium=true`, `premium_until` = now + duration |
| `lead_bronze/silver/gold` | Achat unique de lead, pas de durée |
| `deblocage_coordonnees` | Achat unique, pas de durée |
| `diaspora_*` | Services diaspora, achats uniques |
| `auto_renew` | Par défaut `true` pour les subscriptions. Renouvellement auto de 30 jours |
| `check_expired_services()` | Routine quotidienne : passe les achats en `expired` et désactive les services. Pour les subs : renouvelle si `auto_renew`, sinon expire |
| `Numéro de facture` | Format : `INV-YYYYMMDD-{token_hex_8}` |

---

## Identifiant : KNW-IDENTITY-RESOLUTION-007

### Titre : Identity Resolution (Détection et fusion des doublons)

### Description
Moteur de résolution d'identités. Détecte les personnes dupliquées dans la base selon 3 méthodes : téléphone (score 100%), email (score 95%), similarité de nom (score 40% base). Les candidats doublons sont stockés dans `duplicate_candidates` pour validation humaine. Score minimum pour similarité de nom : 40 points.

### Source
**Fichier :** `03_ENGINE/identity_resolution.py`  
**Chemin :** `/media/abel/Doc/Drive/d/LAWIM_BACKUP_20260608_125026/LAWIMA/03_ENGINE/identity_resolution.py`

### Niveau de confiance : ÉLEVÉ

### Règles et valeurs

**Normalisation téléphone :**
- `normalize_phone(phone)` → Supprime tout sauf chiffres
- Si `len(phone) == 9` → préfixe `237` (Cameroun)

**Méthodes de détection des doublons :**

| Méthode | Score | Raison | Logique |
|---------|-------|--------|---------|
| `find_duplicates_by_phone` | **100** | "Même numéro de téléphone" | Normalisation + matching exact |
| `find_duplicates_by_email` | **95** | "Même adresse email" | `lower()` + `strip()` + matching exact |
| `find_duplicates_by_name_similarity` | 40-90 | Cumul de raisons | Algorithme de similarité |

**Détail du scoring par similarité de nom :**
| Condition | Points | Raison |
|-----------|--------|--------|
| Même prénom (premier mot) | **+40** | "Même prénom" |
| 3 premières lettres du nom identiques | **+20** | "Nom similaire" |
| 6 derniers chiffres du téléphone identiques | **+30** | "Téléphone similaire" |
| **Seuil de validation** | **≥40** | Score minimum pour considérer comme doublon |

**Table des candidats doublons :**
| Colonne | Description |
|---------|-------------|
| `person_id_1` | Première personne |
| `person_id_2` | Seconde personne |
| `match_score` | Score de matching (0-100) |
| `match_reason` | Raison textuelle |
| `status` | `pending` (par défaut) |

**Fonctionnalités :**
- Déduplication des paires (si A_B et B_A, garde le meilleur score)
- Récupération des candidats en attente triés par `match_score` descendant
- Gestion d'erreur si table `duplicate_candidates` inexistante

---

## Identifiant : KNW-DATA-QUALITY-008

### Titre : Data Quality Engine (Score de qualité des données)

### Description
Moteur de scoring de qualité des données LAWIM. Évalue la complétude et la fiabilité des biens immobiliers et des leads. Score sur 100 basé sur : complétude des champs (60%) et fiabilité de la source (40%). Système de grading A+/A/B/C/D.

### Source
**Fichier :** `03_ENGINE/data_quality_engine.py`  
**Chemin :** `/media/abel/Doc/Drive/d/LAWIM_BACKUP_20260608_125026/LAWIMA/03_ENGINE/data_quality_engine.py`

### Niveau de confiance : ÉLEVÉ

### Règles et valeurs

**Fiabilité des sources (`SOURCE_RELIABILITY`) :**
| Source | Score (0-100) | Description |
|--------|---------------|-------------|
| `agent` | **90** | Agent partenaire vérifié |
| `google_form` | **85** | Formulaire structuré |
| `import` | **70** | Import CSV |
| `whatsapp` | **50** | Message libre |
| `unknown` | **30** | Source inconnue |

**Scoring propriété (`assess_property`) :**

*Complétude (60% du score total) :*

| Critère | Poids max | Condition de score |
|---------|-----------|-------------------|
| Titre | **10 points** | Présence de `title` |
| Description > 100 chars | **15 points** | `len(desc) > 100` |
| Description > 50 chars | **10 points** | `len(desc) > 50` |
| Description > 20 chars | **5 points** | `len(desc) > 20` |
| Prix | **15 points** | `price > 0` |
| Localisation | **15 points** | Présence de `location` |
| Type de bien | **15 points** | Présence de `property_type` |
| Images | **15 points** | `min(15, len(images) * 3)` |

*Fiabilité source (40% du score total) :*
- `quality_score = int(completeness * 0.6 + reliability * 0.4)`

**Scoring lead (`assess_lead`) :**
| Critère | Poids max | Condition |
|---------|-----------|-----------|
| Message | **30 points** | `len(message) > 20` |
| Budget | **25 points** | `budget > 0` |
| Localisation | **25 points** | Présence de `location` |
| Type de bien | **20 points** | Présence de `property_type` |

**Grades :**
| Score | Grade | Icône |
|-------|-------|-------|
| ≥ 80 | **A+ (Excellent)** | 🟢 |
| ≥ 60 | **A (Bon)** | 🟢 |
| ≥ 50 | (seuil d'affichage jaune) | 🟡 |
| ≥ 40 | **B (Moyen)** | 🟡 |
| ≥ 20 | **C (Faible)** | 🔴 |
| < 20 | **D (À vérifier)** | 🔴 |

**Métadonnées stockées (`data_quality` table) :**
- `entity_type` : `property` ou `lead`
- `entity_id` : ID de l'entité
- `quality_score` : Score global
- `completeness_score` : Score de complétude
- `source` : Source de la donnée
- `source_reliability` : Fiabilité de la source
- `has_images`, `has_price`, `has_location`, `has_description` : Flags booléens
- `last_assessed` : Timestamp de dernière évaluation

---

## Identifiant : KNW-LEAD-CLASSIFIER-009

### Titre : Lead Classifier V1 - Classification et scoring des leads

### Description
Classifieur de leads avec 5 types de profils, des boosters et pénalités de score, et des seuils de classification hot/warm/cold.

### Source
**Fichier :** `06_AI_MODELS/lead_classifier/lead_classifier_v1.json`  
**Chemin :** `/media/abel/Doc/Drive/d/LAWIM_BACKUP_20260608_125026/LAWIMA/06_AI_MODELS/lead_classifier/lead_classifier_v1.json`

### Niveau de confiance : ÉLEVÉ

### Règles et valeurs

**Lead Types et base scores :**
| Type | Intention | Base Score |
|------|-----------|------------|
| `tenant` | `RENT_PROPERTY` | **40** |
| `buyer` | `BUY_PROPERTY` | **60** |
| `seller` | `SELL_PROPERTY` | **50** |
| `investor` | `INVESTOR_INTENT` | **80** |
| `diaspora_investor` | `INVESTOR_INTENT` | **95** |

**Score Boosters :**
| Condition | Bonus |
|-----------|-------|
| `budget_detected` | **+15** |
| `city_detected` | **+10** |
| `neighborhood_detected` | **+10** |
| `urgent_request` | **+20** |
| `diaspora_detected` | **+25** |
| `cash_purchase` | **+15** |

**Score Penalties :**
| Condition | Pénalité |
|-----------|----------|
| `missing_budget` | **-10** |
| `unclear_location` | **-10** |
| `spam_like_message` | **-50** |

**Seuils de classification :**
| Classe | Seuil minimum |
|--------|---------------|
| `hot_lead` | ≥ **80** |
| `warm_lead` | ≥ **60** |
| `cold_lead` | ≥ **40** |

---

## Identifiant : KNW-PROPERTY-MATCHING-010

### Titre : Property Matching Engine V1 - Appariement propriété/requête

### Description
Moteur de matching entre les requêtes utilisateurs et les biens disponibles. Pondérations par critère, tolérances budgétaires par type de transaction, règles de priorité avec boosts, score minimum de 60% pour affichage, limite à 10 résultats.

### Source
**Fichier :** `06_AI_MODELS/matching_engine/property_matching_v1.json`  
**Chemin :** `/media/abel/Doc/Drive/d/LAWIM_BACKUP_20260608_125026/LAWIMA/06_AI_MODELS/matching_engine/property_matching_v1.json`

### Niveau de confiance : ÉLEVÉ

### Règles et valeurs

**Matching Weights :**
| Critère | Poids |
|---------|-------|
| `city` | **30** |
| `neighborhood` | **25** |
| `budget` | **25** |
| `property_type` | **15** |
| `title_status` | **5** |

**Budget Tolerance (par type de transaction) :**
| Transaction | Tolérance |
|-------------|-----------|
| `rent` | **±20%** |
| `buy` | **±15%** |
| `invest` | **±25%** |

**Priority Rules (boosts conditionnels) :**
| Condition | Boost |
|-----------|-------|
| `exact_neighborhood_match` | **+25** |
| `exact_city_match` | **+20** |
| `budget_within_range` | **+15** |
| `title_foncier` | **+10** |
| `diaspora_investor` | **+20** |

**Paramètres :**
| Paramètre | Valeur |
|-----------|--------|
| `minimum_match_score` | **60** (en dessous = non affiché) |
| `top_results_limit` | **10** (max résultats retournés) |

---

## Identifiant : KNW-CONVERSATION-FLOWS-011

### Titre : Conversation Flows V1 - Flux de dialogue WhatsApp

### Description
Définition des arbres de conversation WhatsApp pour chaque intention utilisateur. 4 flows distincts : location, achat, vente, investissement.

### Source
**Fichier :** `06_AI_MODELS/conversation_flows/conversation_flows_v1.json`  
**Chemin :** `/media/abel/Doc/Drive/d/LAWIM_BACKUP_20260608_125026/LAWIMA/06_AI_MODELS/conversation_flows/conversation_flows_v1.json`

### Niveau de confiance : ÉLEVÉ

### Règles et valeurs

**Flows :**
| Intention | Étapes |
|-----------|--------|
| `RENT_PROPERTY` | `ask_city` → `ask_neighborhood` → `ask_budget` → `show_properties` |
| `BUY_PROPERTY` | `ask_city` → `ask_budget` → `ask_property_type` → `show_properties` |
| `SELL_PROPERTY` | `ask_property_details` → `collect_contact` → `create_listing` |
| `INVESTOR_INTENT` | `ask_city` → `ask_budget` → `ask_investment_goal` → `show_opportunities` |

---

## Identifiant : KNW-MEMORY-RULES-012

### Titre : Memory Rules V1 - Règles de mémoire session et long terme

### Description
Système de mémoire pour LAWIM. Définit les champs à mémoriser en session, les préférences long terme, et la durée d'oubli (90 jours).

### Source
**Fichier :** `06_AI_MODELS/memory/memory_rules_v1.json`  
**Chemin :** `/media/abel/Doc/Drive/d/LAWIM_BACKUP_20260608_125026/LAWIMA/06_AI_MODELS/memory/memory_rules_v1.json`

### Niveau de confiance : ÉLEVÉ

### Règles et valeurs

**Session Memory (champs à retenir) :**
- `city`
- `neighborhood`
- `budget`
- `property_type`
- `user_role`
- `preferred_language`

**Long Term Memory :**
- `favorite_locations`
- `investment_preferences`
- `diaspora_country`

**Paramètres :**
| Paramètre | Valeur |
|-----------|--------|
| `session_memory` | **true** |
| `forget_after_days` | **90 jours** |

---

## Identifiant : KNW-REASONING-RULES-013

### Titre : Reasoning Rules V1 - Pipeline de raisonnement

### Description
Pipeline de raisonnement en 7 étapes pour le traitement des messages. Ordre de priorité des critères et seuil de confiance pour les décisions automatiques.

### Source
**Fichier :** `06_AI_MODELS/reasoning/reasoning_rules_v1.json`  
**Chemin :** `/media/abel/Doc/Drive/d/LAWIM_BACKUP_20260608_125026/LAWIMA/06_AI_MODELS/reasoning/reasoning_rules_v1.json`

### Niveau de confiance : ÉLEVÉ

### Règles et valeurs

**Reasoning Steps (7 étapes) :**
1. `detect_intent`
2. `detect_city`
3. `detect_neighborhood`
4. `detect_budget`
5. `classify_lead`
6. `match_properties`
7. `rank_results`

**Priority Order :**
1. `intent`
2. `location`
3. `budget`
4. `property_type`

**Paramètres :**
| Paramètre | Valeur |
|-----------|--------|
| `confidence_threshold` | **0.70** (70%) |

---

## Identifiant : KNW-SYSTEM-PROMPT-014

### Titre : System Prompt V1 - Prompt système LAWIM

### Description
Prompt système définissant le comportement, les objectifs, les types de clients, les intentions, les villes prioritaires, les règles, et le format de sortie structurée de l'assistant LAWIM.

### Source
**Fichier :** `06_AI_MODELS/prompts/system_prompt_v1.md`  
**Chemin :** `/media/abel/Doc/Drive/d/LAWIM_BACKUP_20260608_125026/LAWIMA/06_AI_MODELS/prompts/system_prompt_v1.md`

### Niveau de confiance : ÉLEVÉ

### Règles métier extraites

**Objectifs :**
1. Comprendre les intentions immobilières
2. Identifier automatiquement le type de client
3. Détecter la ville et le quartier recherchés
4. Déterminer le budget
5. Déterminer l'urgence
6. Identifier les investisseurs diaspora
7. Proposer les biens les plus pertinents

**Types de clients (7 profils) :**
`Locataire`, `Acheteur`, `Vendeur`, `Investisseur`, `Agence`, `Agent immobilier`, `Promoteur`

**Intentions :**
- `SEARCH_PROPERTY`
- `RENT_PROPERTY`
- `BUY_PROPERTY`
- `SELL_PROPERTY`
- `INVESTOR_INTENT`

**Villes prioritaires (10 villes) :**
`Douala`, `Yaoundé`, `Bafoussam`, `Bamenda`, `Buea`, `Limbe`, `Kribi`, `Nkongsamba`, `Garoua`, `Maroua`

**Règles obligatoires (8 règles) :**
1. Toujours détecter l'intention
2. Toujours calculer un score de lead
3. Toujours détecter la langue
4. Toujours tenter d'extraire : ville, quartier, budget, type de bien
5. Prioriser les leads investisseurs
6. Prioriser les clients diaspora
7. Préférer les biens avec documents valides
8. Ne jamais inventer un bien inexistant

**Format de sortie structurée :**
```json
{
  "intent": "",
  "lead_type": "",
  "city": "",
  "neighborhood": "",
  "budget": "",
  "property_type": "",
  "lead_score": 0,
  "urgency": ""
}
```

---

## Identifiant : KNW-IMMOBILIER-CAMEROUN-015

### Titre : Connaissances immobilières Cameroun

### Description
Base de connaissances du marché immobilier camerounais : villes et leurs quartiers, types de biens avec variantes orthographiques, intentions avec expressions WhatsApp camerounaises (pidgin, français, anglais), et vocabulaire d'urgence.

### Source
**Fichier :** `02_KNOWLEDGE/immobilier_cameroun.json`  
**Chemin :** `/media/abel/Doc/Drive/d/LAWIM_BACKUP_20260608_125026/LAWIMA/02_KNOWLEDGE/immobilier_cameroun.json`

### Niveau de confiance : ÉLEVÉ

### Règles et valeurs

**Villes et quartiers :**
| Ville | Quartiers |
|-------|-----------|
| `yaounde` | bastos, mvan, messa, etoudi, nlongkak, mokolo, biyemassi, oyer, mendong, odza, simbock |
| `douala` | bonapriso, akwa, bonamoussadi, makepe, logbessou, deido, ndokoti, bonaberi, bonanjo |
| `bafoussam` | domayo, banengo, toukour, famla |
| `bamenda` | upstation, downstation, nso, mankon |
| `garoua` | pete, canton, camp |
| `kribi` | plateau, mboa |
| `limbe` | down beach, middle farm, parliamentary |

**Types de biens et variantes :**
| Type | Variantes |
|------|-----------|
| `appartement` | appart, apart, flat, appt |
| `maison` | house, bungalow, villa |
| `terrain` | land, plot, parcelle |
| `studio` | studio, 1 piece, one bedroom |
| `bureau` | office, cabinet, bureau |
| `magasin` | shop, store, commerce |

**Intentions avec expressions camerounaises :**
| Intention | Déclencheurs |
|-----------|--------------|
| `buy` | cherche, recherche, veux, achète, acheter, trouver, acquérir, recherch |
| `rent` | loue, location, louer, locataire, loyer, looking for, i want to rent, need a house, rent a house, looking to rent, find house, dey find, need house, want house, i dey find, we dey find |
| `sell` | vends, vendre, propose, cède, cession |

**Urgence :**
`urgent`, `asap`, `rapidement`, `vite`, `prompt`, `urgence`, `dernier`, `dépêche`, `immédiat`, `ce week-end`

---

## Identifiant : KNW-LEAD-SCORING-RULES-016

### Titre : Lead Scoring Rules - Règles de scoring additionnelles

### Description
Deux fichiers de scoring de leads avec poids par attribut et profils utilisateurs avec scores et priorités.

### Sources
**Fichier 1 :** `02_KNOWLEDGE/scoring/lead_scoring_rules.json`  
**Chemin :** `/media/abel/Doc/Drive/d/LAWIM_BACKUP_20260608_125026/LAWIMA/02_KNOWLEDGE/scoring/lead_scoring_rules.json`

**Fichier 2 :** `02_KNOWLEDGE/lead_scoring/lead_scoring.json`  
**Chemin :** `/media/abel/Doc/Drive/d/LAWIM_BACKUP_20260608_125026/LAWIMA/02_KNOWLEDGE/lead_scoring/lead_scoring.json`

### Niveau de confiance : ÉLEVÉ

### Règles et valeurs

**Poids par attribut (`lead_scoring_rules.json`) :**
| Attribut | Poids |
|----------|-------|
| `budget` | **20** |
| `location` | **15** |
| `urgency` | **20** |
| `diaspora` | **10** |
| `phone` | **5** |
| `property_type` | **15** |
| `investment_profile` | **10** |

**Profils leads (`lead_scoring.json`) :**

| User Type | Intent | Budget Min | Score | Priorité |
|-----------|--------|------------|-------|----------|
| `diaspora_investor` | `INVESTOR_INTENT` | - | **100** | **P0** |
| `buyer` | `BUY_PROPERTY` | **50 000 000 FCFA** | **95** | **P0** |
| `seller` | `SELL_PROPERTY` | - | **90** | **P1** |
| `land_buyer` | `BUY_PROPERTY` | - | **85** | **P1** |
| `tenant` | `RENT_PROPERTY` | - | **40** | **P3** |

---

## Résumé des connaissances récupérées

| # | Identifiant | Connaissance | Fichiers source | Confiance |
|---|-------------|-------------|-----------------|-----------|
| 1 | KNW-FEATURE-FLAGS-001 | Feature Flags (18 flags, 4 actifs) | 1 | ÉLEVÉ |
| 2 | KNW-ANTISPAM-001 | Anti-spam (10 msg/min, blocage 60 min) | 1 | ÉLEVÉ |
| 3 | KNW-RULE-ENGINE-V2-002 | Rule Engine V2 (normalisation + mapping) | 1 | ÉLEVÉ |
| 4 | KNW-RULE-ENGINE-V3-003 | Rule Engine V3 (4 couches, scoring leads) | 1 | ÉLEVÉ |
| 5 | KNW-RULE-ENGINE-V4-004 | Rule Engine V4 (CRM intelligence, classes) | 1 | ÉLEVÉ |
| 6 | KNW-RULE-ENGINE-V5-005 | Rule Engine V5 (pipeline IA, anti-fraude) | 1 | ÉLEVÉ |
| 7 | KNW-MONETISATION-006 | Monétisation (13 services, 4 tables SQL) | 2 | ÉLEVÉ |
| 8 | KNW-IDENTITY-RESOLUTION-007 | Identity Resolution (3 méthodes) | 1 | ÉLEVÉ |
| 9 | KNW-DATA-QUALITY-008 | Data Quality Engine (scoring 0-100, grades) | 1 | ÉLEVÉ |
| 10 | KNW-LEAD-CLASSIFIER-009 | Lead Classifier V1 (5 types, boost/penalties) | 1 | ÉLEVÉ |
| 11 | KNW-PROPERTY-MATCHING-010 | Property Matching V1 (5 critères, tolérances) | 1 | ÉLEVÉ |
| 12 | KNW-CONVERSATION-FLOWS-011 | Conversation Flows V1 (4 flows) | 1 | ÉLEVÉ |
| 13 | KNW-MEMORY-RULES-012 | Memory Rules V1 (session + long terme, 90j) | 1 | ÉLEVÉ |
| 14 | KNW-REASONING-RULES-013 | Reasoning Rules V1 (7 étapes, seuil 70%) | 1 | ÉLEVÉ |
| 15 | KNW-SYSTEM-PROMPT-014 | System Prompt V1 (8 règles, 10 villes) | 1 | ÉLEVÉ |
| 16 | KNW-IMMOBILIER-CAMEROUN-015 | Connaissances immo Cameroun (7 villes, 6 types) | 1 | ÉLEVÉ |
| 17 | KNW-LEAD-SCORING-RULES-016 | Lead Scoring Rules (7 poids, 5 profils) | 2 | ÉLEVÉ |

**Total : 17 connaissances récupérées depuis 19 fichiers sources**
**Confidence globale : 100% ÉLEVÉ** (tous les fichiers étaient présents et intacts dans la backup)
