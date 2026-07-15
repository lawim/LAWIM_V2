# DATASETS — Jeux de données LAWIM

**Sources :** LAWIM `KNOWLEDGE/`, LAWIMA `02_KNOWLEDGE/`, `01_DATABASE/`, `06_AI_MODELS/`, `08_CONFIG/`, `03_ENGINE/`, `07_DASHBOARD/`
**Principe :** Inventaire exhaustif des jeux de données sans validation

---

## 1. Datasets Knowledge (LAWIM)

**Chemin :** `LAWIM/KNOWLEDGE/`

### 1.1 Master Dataset

| Fichier | Description | Format |
|---------|-------------|--------|
| `LAWIM_MASTER_DATASET.json` | Dataset consolidé master (8765 lignes estimées) | JSON |

### 1.2 Géographie (11 fichiers)

| Fichier | Description |
|---------|-------------|
| `geography/cameroon_geography.json` | Géographie complète du Cameroun |
| `geography/cameroon_geography_v2_backup.json` | Backup V2 |
| `geography/district_aliases.json` | Alias des districts (v1) |
| `geography/district_aliases_v2.json` | Alias des districts (v2) |
| `geography/district_aliases_v3.json` | Alias des districts (v3) |
| `geography/district_hierarchy.json` | Hiérarchie des districts |
| `geography/gemini_recovered_gps.json` | GPS récupéré par IA Gemini |
| `geography/neighborhood_gps.json` | GPS des quartiers |
| `geography/neighborhood_inventory_clean.json` | Inventaire nettoyé des quartiers |
| `geography/neighborhood_inventory_final.json` | Inventaire final des quartiers |
| `geography/neighborhood_inventory.json` | Inventaire original des quartiers |

### 1.3 Quartiers (11 fichiers)

| Fichier | Description |
|---------|-------------|
| `neighborhoods/all_neighborhoods.json` | Tous les quartiers agrégés |
| `neighborhoods/douala.json` | Quartiers de Douala |
| `neighborhoods/yaounde.json` | Quartiers de Yaoundé |
| `neighborhoods/bamenda.json` | Quartiers de Bamenda |
| `neighborhoods/bafoussam.json` | Quartiers de Bafoussam |
| `neighborhoods/buea.json` | Quartiers de Buea |
| `neighborhoods/garoua.json` | Quartiers de Garoua |
| `neighborhoods/kribi.json` | Quartiers de Kribi |
| `neighborhoods/limbe.json` | Quartiers de Limbe |
| `neighborhoods/maroua.json` | Quartiers de Maroua |
| `neighborhoods/nkongsamba.json` | Quartiers de Nkongsamba |

### 1.4 Villes

| Fichier | Description |
|---------|-------------|
| `cities/cameroon_cities.json` | Liste des villes camerounaises |

### 1.5 Intentions (5 fichiers)

| Fichier | Description |
|---------|-------------|
| `intents/buy_property.json` | Intention d'achat |
| `intents/rent_property.json` | Intention de location |
| `intents/sell_property.json` | Intention de vente |
| `intents/search_property.json` | Intention de recherche |
| `intents/investor_intent.json` | Intention d'investissement |

### 1.6 Langage WhatsApp (7 fichiers)

| Fichier | Description |
|---------|-------------|
| `whatsapp_language/whatsapp_language.json` | Corpus langage WhatsApp |
| `whatsapp_language/diaspora_language.json` | Expressions diaspora |
| `whatsapp_language/investor_language.json` | Expressions investisseur |
| `whatsapp_language/negotiation.json` | Expressions négociation |
| `whatsapp_language/property_listing.json` | Expressions annonces |
| `whatsapp_language/property_search.json` | Expressions recherche |
| `whatsapp_language/urgency_signals.json` | Signaux d'urgence |

### 1.7 Correction orthographique (5 fichiers)

| Fichier | Description |
|---------|-------------|
| `typo_database/cities_typo.json` | Fautes villes |
| `typo_database/neighborhoods_typo.json` | Fautes quartiers |
| `typo_database/property_types_typo.json` | Fautes types de biens |
| `typo_database/whatsapp_typo.json` | Fautes WhatsApp |
| `typo_database/typo_database.json` | Base agrégée |

### 1.8 Autres fichiers knowledge

| Fichier | Description |
|---------|-------------|
| `entity_linking/entity_linking.json` | Liaison d'entités |
| `investor/investor_signals.json` | Signaux investisseur |
| `investors/investors.json` | Profils investisseurs |
| `lead_scoring/lead_scoring.json` | Règles de scoring |
| `scoring/lead_scoring_rules.json` | Règles de scoring détaillées |
| `pricing/pricing.json` | Données de prix |
| `pricing/pricing_expressions.json` | Expressions de prix |
| `pricing_expressions/pricing_expressions.json` | Expressions de prix (duplicata) |
| `property_types/property_types.json` | Types de biens |
| `real_estate/property_taxonomy.json` | Taxonomie immobilière v1 |
| `real_estate/property_taxonomy_v2.json` | Taxonomie immobilière v2 |
| `search/search_aliases.json` | Alias de recherche |
| `search_aliases/search_aliases.json` | Alias de recherche (duplicata) |
| `search_optimization/search_optimization.json` | Optimisation recherche |
| `title_status/title_status.json` | Statuts des titres |
| `user_roles/user_roles.json` | Rôles utilisateurs |
| `vocabulary/real_estate_vocabulary.json` | Vocabulaire immobilier |
| `crm/crm_schema.json` | Schéma CRM |
| `crm_schema/crm_schema.json` | Schéma CRM (duplicata) |

### 1.9 Documents de connaissance (15 fichiers)

**Chemin :** `KNOWLEDGE/master/`

Documents V1 séquentiels (01 à 15) couvrant : Architecture, CRM, Geography, Matching, Scoring, Actors, Tracking, Services, Learning Engine, Data Quality, Storage Architecture, Data Dictionary, Database Blueprint, Prisma Schema, Implementation Master Plan.

### 1.10 Documents de référence (10 fichiers)

**Chemin :** `KNOWLEDGE/REFERENCE/`

00-INDEX.md, 01-FUNCTIONAL-SPECIFICATION.md, 02-CONVERSATION.md, 03-PROPERTY-QUALIFICATION.md, 04-DASHBOARDS.md, 05-AUTHENTICATION.md, 06-WORKFLOWS.md, 07-BUSINESS-RULES.md, 08-ARCHITECTURE.md, 09-MIGRATION-GUIDE.md

## 2. Datasets Knowledge (LAWIMA)

**Chemin :** `LAWIMA/02_KNOWLEDGE/`

### 2.1 Contenu identique à LAWIM pour les dossiers communs

- `intents/` (5 fichiers) — mêmes fichiers que LAWIM
- `neighborhoods/` (11 fichiers) — mêmes fichiers que LAWIM
- `cities/` — mêmes fichiers
- `crm/`, `crm_schema/` — identiques
- `entity_linking/` — identique
- `investor/`, `investors/` — identiques
- `lead_scoring/`, `scoring/` — identiques
- `pricing/`, `pricing_expressions/` — identiques
- `property_types/` — identique
- `search/`, `search_aliases/` — identiques
- `search_optimization/` — identique
- `title_status/` — identique
- `user_roles/` — identique
- `typo_database/` (5 fichiers) — identiques
- `vocabulary/` — identique
- `whatsapp_language/` (7 fichiers) — identiques

### 2.2 Contenu supplémentaire LAWIMA

- `_archive/` — 61 fichiers d'archives (versions historiques, audits, diagnostics, enrichissements)
- `_archive_minimal/` — 16 fichiers d'archive minimale
- `_repair_backup/` — 84 fichiers de backup de réparation
- `generated/dataset_v1/` — Données générées v1
- `immobilier_cameroun.json` — Données marché

## 3. Datasets Knowledge (ancienne_structure)

**Chemin :** `ancienne_structure/02_KNOWLEDGE/`

Sous-ensemble de LAWIMA (sans `_archive/`, `_repair_backup/`, `generated/`). Les fichiers communs sont identiques.

## 4. Datasets Base de données (LAWIMA)

**Chemin :** `LAWIMA/01_DATABASE/`

### 4.1 CSV runtime
- `runtime/agents.csv`
- `runtime/events.csv`
- `runtime/leads.csv`
- `runtime/leads_corrupted_backup.csv`
- `runtime/properties.csv`
- `runtime/users.csv`

### 4.2 CSV ready for Supabase
- `ready_for_supabase/leads.csv`
- `ready_for_supabase/persons.csv`
- `ready_for_supabase/properties.csv`

### 4.3 CSV supabase_ready
- `supabase_ready/agents.csv`
- `supabase_ready/contact_channels.csv`
- `supabase_ready/events.csv`
- `supabase_ready/leads.csv`
- `supabase_ready/persons.csv`
- `supabase_ready/properties.csv`

### 4.4 Templates CSV
- `templates/AGENTS.csv`
- `templates/EVENTS.csv`
- `templates/LEADS.csv`
- `templates/PROPERTIES.csv`
- `templates/USERS.csv`

### 4.5 Backup CSV
- `backup_20260605/` — 8 fichiers (snapshot backup)

### 4.6 Event log
- `events_log.jsonl` — Log d'événements en format JSONL

## 5. Datasets IA (LAWIMA/ancienne_structure)

**Chemin :** `LAWIMA/06_AI_MODELS/`

### 5.1 Configurations IA (6 fichiers)

| Fichier | Description |
|---------|-------------|
| `conversation_flows/conversation_flows_v1.json` | Flows de conversation |
| `lead_classifier/lead_classifier_v1.json` | Classification des leads |
| `matching_engine/property_matching_v1.json` | Matching engine |
| `memory/memory_rules_v1.json` | Règles mémoire |
| `prompts/system_prompt_v1.md` | Prompt système (73 lignes) |
| `reasoning/reasoning_rules_v1.json` | Règles de raisonnement |

## 6. Datasets Configuration (LAWIMA/ancienne_structure)

**Chemin :** `LAWIMA/08_CONFIG/`

### 6.1 Rule Engine (5 versions)
- `rule_engine/RULE_ENGINE_V2.json`
- `rule_engine/RULE_ENGINE_V3.json`
- `rule_engine/RULE_ENGINE_V4.json`
- `rule_engine/RULE_ENGINE_V5.json` (version la plus aboutie)
- `rule_engine/RULE_ENGINE_V5.json.backup`

### 6.2 Autres configurations
- `features/FEATURE_FLAGS.json` — Feature flags
- `state_machine/USER_STATES.json` — États utilisateur (7 états)
- `state_machine/EVENT_TYPES.json` — Types d'événements (11 types)
- `action_engine/actions_v1.py` — Actions (48 lignes)
- `rule_engine_core/rules_v1.py` — Règles core (27 lignes)
- `payments/CAMPAY_CONFIG.json` — Configuration CamPay
- `whatsapp/GREEN_API_CONFIG.json` — Configuration WhatsApp

## 7. Structure des données SQL

**Source :** LAWIMA `05_AUTOMATIONS/scripts/implement_all.sql` (140 lignes), `setup_database.sql`

Tables créées par les scripts SQL :
- `role_permissions`
- `agent_routing`
- `disputes`
- `boosts`
- `diaspora_services`
- `agent_credits`
- `boost_purchases`
- `agent_zones`
- `agent_routing_history`
- `user_permissions`
- `pending_permission_changes`
- `system_logs`
- `training_conversations`
- `duplicate_candidates`
- `anonymization_requests`

## 8. Données géographiques additionnelles (LAWIM — racine)

| Fichier | Description |
|---------|-------------|
| `cameroon_geography_before_mass_gps_*.json` | Snapshot avant génération GPS |
| `buea_lookup.txt` | Données Buea |
| `listes_villes_camerounaises.md` | Liste des villes |
| `districts_missing_157.txt` | Districts manquants |
| `districts_not_found.txt` | Districts non trouvés |
| `districts_without_gps.txt` | Districts sans GPS |

## 9. Datasets générés

**Source :** LAWIM `scripts/` (10 scripts JS)

Scripts de génération de données :
- `build_cameroon_geography.js` (v1, v2)
- `build_inventory.js`
- `clean_inventory.js`
- `fix_inventory.js`
- `generate_city_gps.js`
- `generate_district_gps_test.js`
- `generate_neighborhood_gps.js`
- `apply_district_aliases.js`

## 10. Données géographiques LAWIM_V2 (pour référence — ne pas valider)

**Source :** LAWIM_V2 `code/lawim_v2/data/cameroon_locations.json`

Fichier de localisations présent dans l'implémentation actuelle.

---

*Document patrimonial — Aucune décision de reconstruction n'est prise ici.*
