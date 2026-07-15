# HERITAGE INDEX — Patrimoine Métier LAWIM

**Mission :** H0 — LAWIM Business Heritage Recovery
**Date :** 15 juillet 2026
**Sources explorées :** LAWIM, LAWIMA, ancienne_structure
**Principe :** Documentation exclusive — aucune décision de reconstruction

---

## 1. Présentation du patrimoine

Ce dossier constitue la mémoire fonctionnelle complète de LAWIM.

Il documente l'intégralité des connaissances métier accumulées dans les trois branches historiques, sans aucune modification, sans aucune sélection, sans aucune validation par rapport à LAWIM_V2.

Chaque document liste exhaustivement les concepts, règles, définitions, classifications et processus découverts, avec leur source exacte (branche + fichier).

## 2. Branches explorées

| Branche | Chemin racine | Nature | Volume exploré |
|---------|---------------|--------|----------------|
| **LAWIM** | `LAWIM_BACKUP/LAWIM/` | Documentation + Knowledge JSON + Scripts | ~290 fichiers |
| **LAWIMA** | `LAWIM_BACKUP/LAWIMA/` | Engine Python + Dashboards + Knowledge + Config | ~400 fichiers |
| **ancienne_structure** | `LAWIM_BACKUP/ancienne_structure/` | Engine Python (sous-ensemble LAWIMA) | ~300 fichiers |

## 3. Documents du patrimoine

| Document | Contenu | Sources principales |
|----------|---------|-------------------|
| `PROPERTY_MODEL.md` | Types de biens, attributs, cycles de vie, transactions, titres | LAWIM Directive/02*, LAWIMA property_types, ancienne property_lifecycle_engine |
| `GEOGRAPHY_MODEL.md` | Villes, quartiers, hiérarchie territoriale, alias, scoring géographique | LAWIM KNOWLEDGE/geography, neighborhoods, LAWIMA location_normalizer |
| `QUALIFICATION_MODEL.md` | Profils utilisateurs, scoring, champs obligatoires/recommandés, seuils | LAWIMA lead_scorer, lead_classifier, RULE_ENGINE, LAWIM qualification docs |
| `INTENT_MODEL.md` | Intentions, sous-intentions, mots-clés, poids, flux de qualification | LAWIMA intents/*.json, intent_detector, LAWIM intents/ |
| `CONVERSATION_MODEL.md` | Règles de dialogue, langues, relances, objections, commandes, feedback | LAWIMA response_policy, conversation_memory, follow_up_system, LAWIM conversation docs |
| `MATCHING_MODEL.md` | Dimensions de matching, poids, tolérances, exclusions, scoring | LAWIMA property_matcher_v5, matching_engine configs, LAWIM matching docs |
| `CRM_MODEL.md` | Rôles, acteurs, permissions, agents, organisations, états | LAWIMA user_roles, RULE_ENGINE, agent_optin, agent_rating, SQL scripts |
| `NEGOTIATION_MODEL.md` | Techniques, objections, argumentaires, signaux de négociation | LAWIM conversation-patterns, negotiation-patterns, WhatsApp language |
| `LANGUAGE_MODEL.md` | Langues, synonymes, alias, fautes courantes, expressions camerounaises | LAWIM typo_database, whatsapp_language, vocabulary, entity_linking |
| `ROLE_MODEL.md` | Rôles détaillés, hiérarchie, permissions, niveaux | LAWIMA user_roles, agent_rating, dashboard, LAWIM role docs |
| `DOMAIN_MODEL.md` | Domaines métier, entités, relations, règles globales | LAWIM Constitution, LAWIMA RULE_ENGINE, SQL schemas |
| `DATASETS.md` | Tous les jeux de données, structures, formats, volumes | LAWIM KNOWLEDGE/, LAWIMA 02_KNOWLEDGE/, LAWIMA 01_DATABASE/ |
| `KNOWLEDGE_COVERAGE_MATRIX.md` | Matrice de couverture des connaissances par branche et domaine | Toutes les sources |
| `HERITAGE_GLOSSARY.md` | Glossaire complet des termes métier LAWIM | Toutes les sources |

## 4. Domaines couverts

| Domaine | Niveau de couverture | Source la plus riche |
|---------|---------------------|---------------------|
| Immobilier (types de biens) | Exhaustif | LAWIM Directive/02* (9 docs de référence) |
| Géographie (Cameroun) | Exhaustif | LAWIM KNOWLEDGE/geography/ (11 fichiers) |
| Qualification (scoring) | Exhaustif | LAWIMA lead_classifier + RULE_ENGINE (5 versions) |
| Intentions | Exhaustif | LAWIMA 02_KNOWLEDGE/intents/ (5 fichiers) |
| Conversation | Exhaustif | LAWIM Directive + LAWIMA engine (multiples sources) |
| Matching | Exhaustif | LAWIMA property_matcher (3 versions) + LAWIM docs |
| CRM / Rôles | Exhaustif | LAWIMA user_roles + SQL scripts (multiples tables) |
| Négociation | Partiel | LAWIM conversation-patterns + whatsapp_language |
| Langage | Exhaustif | LAWIM typo_database + whatsapp_language (12+ fichiers) |
| Datasets | Exhaustif | LAWIMA 02_KNOWLEDGE (200+ fichiers) |
| Règles métier | Exhaustif | LAWIMA RULE_ENGINE V2-V5 + LAWIM Constitution |
| Workflows | Exhaustif | LAWIM workflow docs + LAWIMA state_machine |
| Fraude / Confiance | Partiel | LAWIM fraud docs + LAWIMA anti_spam |
| Monétisation | Partiel | LAWIMA FEATURE_FLAGS + monetisation scripts |

## 5. Fichiers clés par branche

### LAWIM — Fichiers à valeur métier principale

| Fichier | Domaine |
|---------|---------|
| `Directive/00-CONSTITUTION.md` | Règles fondamentales du projet |
| `Directive/02-PROPERTY-REFERENCE.md` | Référence complète propriétés |
| `Directive/02A-RESIDENTIAL-REFERENCE.md` à `02I-PRICING-REFERENCE.md` | Types de biens détaillés |
| `Directive/03-CONVERSATION-REFERENCE.md` | Design conversation |
| `Directive/04-MATCHING-REFERENCE.md` | Moteur de matching |
| `Directive/04-DECISION-ENGINE-REFERENCE.md` | Moteur de décision |
| `Directive/05-WORKFLOW-REFERENCE.md` | Workflows |
| `Directive/06-DATABASE-REFERENCE.md` | Schéma de données |
| `Directive/08-ROLE-REFERENCE.md` | Rôles et permissions |
| `Directive/09-GEOLOCATION-REFERENCE.md` | Géolocalisation |
| `Directive/10-NOTIFICATION-REFERENCE.md` | Notifications |
| `Directive/15-SECURITY-REFERENCE.md` | Sécurité |
| `Directive/16-API-REFERENCE.md` | API |
| `Directive/18-LAWIM-AI-REFERENCE.md` | IA |
| `Directive/48-LAWIM-SALES-PLAYBOOK.md` | Ventes et négociation |
| `KNOWLEDGE/LAWIM_MASTER_DATASET.json` | Dataset master consolidé |
| `KNOWLEDGE/geography/` (11 fichiers) | Données géographiques |
| `KNOWLEDGE/neighborhoods/` (10 fichiers ville) | Quartiers par ville |
| `KNOWLEDGE/intents/` (5 fichiers) | Définitions d'intentions |
| `KNOWLEDGE/whatsapp_language/` (7 fichiers) | Langage WhatsApp |
| `KNOWLEDGE/typo_database/` (5 fichiers) | Corrections orthographiques |
| `KNOWLEDGE/conversation-patterns.md` | Patterns de conversation |
| `KNOWLEDGE/negotiation-patterns.md` | Patterns de négociation |
| `KNOWLEDGE/qualification-implementation-backlog.md` | Backlog qualification |
| `KNOWLEDGE/master/` (15 docs V1) | Documents V1 complets |

### LAWIMA — Fichiers à valeur métier principale

| Fichier | Domaine |
|---------|---------|
| `02_KNOWLEDGE/intents/*.json` | Intentions (5 fichiers) |
| `02_KNOWLEDGE/lead_scoring/lead_scoring.json` | Règles de scoring |
| `02_KNOWLEDGE/scoring/lead_scoring_rules.json` | Règles de scoring détaillées |
| `02_KNOWLEDGE/cities/cameroon_cities.json` | Villes du Cameroun |
| `02_KNOWLEDGE/neighborhoods/*.json` | Quartiers (11 fichiers) |
| `02_KNOWLEDGE/crm_schema/crm_schema.json` | Schéma CRM |
| `02_KNOWLEDGE/property_types/property_types.json` | Types de biens |
| `02_KNOWLEDGE/pricing/pricing.json` | Prix et expressions |
| `02_KNOWLEDGE/vocabulary/real_estate_vocabulary.json` | Vocabulaire immobilier |
| `02_KNOWLEDGE/entity_linking/entity_linking.json` | Lien d'entités |
| `02_KNOWLEDGE/whatsapp_language/*.json` | Langage WhatsApp |
| `06_AI_MODELS/lead_classifier/lead_classifier_v1.json` | Classification leads |
| `06_AI_MODELS/matching_engine/property_matching_v1.json` | Matching engine |
| `06_AI_MODELS/conversation_flows/conversation_flows_v1.json` | Flows conversation |
| `06_AI_MODELS/memory/memory_rules_v1.json` | Règles mémoire |
| `06_AI_MODELS/reasoning/reasoning_rules_v1.json` | Règles raisonnement |
| `06_AI_MODELS/prompts/system_prompt_v1.md` | Prompt système IA |
| `08_CONFIG/rule_engine/RULE_ENGINE_V5.json` | Règles moteur V5 |
| `08_CONFIG/features/FEATURE_FLAGS.json` | Feature flags |
| `08_CONFIG/state_machine/USER_STATES.json` | États utilisateur |
| `08_CONFIG/state_machine/EVENT_TYPES.json` | Types d'événements |
| `03_ENGINE/lawim_engine_v1.py` | Orchestrateur engine |
| `03_ENGINE/conversation_memory.py` | Mémoire conversation |
| `03_ENGINE/long_term_memory.py` | Mémoire long-terme |
| `03_ENGINE/follow_up_system.py` | Système de relance |
| `03_ENGINE/anti_spam.py` | Anti-spam |
| `03_ENGINE/identity_resolution.py` | Résolution d'identité |
| `03_ENGINE/data_quality_engine.py` | Qualité des données |
| `03_ENGINE/property_lifecycle_engine.py` | Cycle de vie propriétés |
| `03_ENGINE/location_normalizer.py` | Normalisation localisation |
| `03_ENGINE/phone_formatter.py` | Formatage téléphone |
| `03_ENGINE/knowledge_builder.py` | Profils utilisateurs |
| `03_ENGINE/knowledge_enricher.py` | Enrichissement connaissance |
| `03_ENGINE/multilingual_responses.py` | Réponses multilingues |
| `03_ENGINE/diaspora_filter.py` | Filtre diaspora |
| `03_ENGINE/response_router.py` | Routeur de réponses |
| `00_GLOBAL/rules/RESPONSE_POLICY.md` | Politique de réponse |
| `05_AUTOMATIONS/scripts/implement_all.sql` | SQL d'implémentation |
| `05_AUTOMATIONS/scripts/setup_database.sql` | SQL base de données |
| `core/monetisation.py` | Logique de monétisation |
| `core/data_quality_engine.py` | Qualité des données core |

## 6. Concepts transversaux

Les documents suivants contiennent des concepts qui traversent plusieurs domaines :

| Concept | Présent dans |
|---------|-------------|
| Zéro commission | LAWIM Constitution, LAWIMA RESPONSE_POLICY |
| Accompagnement payant (50k FCFA) | LAWIMA response_policy, RESPONSE_POLICY |
| Diaspora (détection et services) | LAWIMA diaspora_filter, entity_linking, LAWIM diaspora-behavior-model |
| Anti-fraud (25 signaux) | LAWIM fraud-signals-and-verification, LAWIMA RULE_ENGINE_V5 |
| RGPD / Protection des données | LAWIMA RESPONSE_POLICY, SQL scripts |
| Feature flags (whatsapp_core activé, payments désactivé) | LAWIMA FEATURE_FLAGS.json |
| Architecture data-first | LAWIMA 00_GLOBAL/doc_reference/ARCHITECTURE.md |
| Multi-canal (WhatsApp, Telegram, Facebook, Dashboard) | LAWIM omnichannel-playbook, LAWIMA gateways |

## 7. Notes sur les duplications

Certaines connaissances sont présentes dans plusieurs branches, parfois avec des variations :

| Connaissance | LAWIM | LAWIMA | ancienne_structure | Notes |
|-------------|-------|--------|-------------------|-------|
| Intentions (buy/rent/sell/search/investor) | KNOWLEDGE/intents/*.json | 02_KNOWLEDGE/intents/*.json | 02_KNOWLEDGE/intents/*.json | Contenu similaire, vérifier les variations |
| Quartiers | KNOWLEDGE/neighborhoods/ (10 villes) | 02_KNOWLEDGE/neighborhoods/ (11 villes) | 02_KNOWLEDGE/neighborhoods/ | Légères différences de contenu |
| Géographie | KNOWLEDGE/geography/ (11 fichiers) | 02_KNOWLEDGE/geography/ | 02_KNOWLEDGE/geography/ | LAWIM a plus de fichiers |
| Scoring leads | KNOWLEDGE/lead_scoring/lead_scoring.json | 02_KNOWLEDGE/scoring/ + lead_scoring/ | 02_KNOWLEDGE/ | LAWIMA a 2 dossiers de scoring |
| WhatsApp language | KNOWLEDGE/whatsapp_language/ (7 fichiers) | 02_KNOWLEDGE/whatsapp_language/ (7 fichiers) | 02_KNOWLEDGE/whatsapp_language/ | Similaires |
| Entity linking | KNOWLEDGE/entity_linking/entity_linking.json | 02_KNOWLEDGE/entity_linking/entity_linking.json | 02_KNOWLEDGE/entity_linking/entity_linking.json | Identique |
| Moteur de matching | 4 docs MATCHING_ENGINE_*.md | property_matcher/ (3 versions) + matching_engine config | property_matcher/ (3 versions) | Différents niveaux de détail |
| Règles moteur | Absent | RULE_ENGINE V2-V5 | RULE_ENGINE V2-V5 | 5 versions évolutives |
| Flows conversation | conversation-patterns.md | conversation_flows_v1.json | conversation_flows_v1.json | Format différent (MD vs JSON) |

## 8. Connaissances potentiellement uniques

Les connaissances suivantes n'ont été trouvées que dans une seule branche :

| Connaissance | Branche | Fichier |
|-------------|---------|---------|
| Constitution LAWIM (23 articles) | LAWIM | Directive/00-CONSTITUTION.md |
| Référence propriété complète (9 docs) | LAWIM | Directive/02*.md |
| Workflows et state machines | LAWIM | Directive/05-WORKFLOW-REFERENCE.md |
| Référence API legacy | LAWIM | Directive/16-API-REFERENCE.md |
| Sales playbook | LAWIM | Directive/48-LAWIM-SALES-PLAYBOOK.md |
| Brand book | LAWIM | Directive/LAWIM-BRAND-BOOK.md |
| Business plan | LAWIM | Directive/LAWIM-BUSINESS-PLAN.md |
| Operations manual | LAWIM | Directive/LAWIM-OPERATIONS-MANUAL.md |
| Marketing plan | LAWIM | Directive/Plan_strategique_lancement.md |
| Master dataset consolidé | LAWIM | KNOWLEDGE/LAWIM_MASTER_DATASET.json |
| Prompt système IA (73 lignes) | LAWIMA/ancienne | 06_AI_MODELS/prompts/system_prompt_v1.md |
| Rule engine V5 (version la plus aboutie) | LAWIMA | 08_CONFIG/rule_engine/RULE_ENGINE_V5.json |
| Data quality engine (scores complets) | LAWIMA | 03_ENGINE/data_quality_engine.py |
| Knowledge builder (32 champs profil) | LAWIMA | 03_ENGINE/knowledge_builder.py |
| Monétisation détaillée | LAWIMA | core/monetisation.py |
| Identity resolution | LAWIMA | 03_ENGINE/identity_resolution.py |
| Feature flags complets | LAWIMA | 08_CONFIG/features/FEATURE_FLAGS.json |
| Documents financiers (.docx) | LAWIMA | 07_DOCUMENTATION/finance/ |
| Documents marketing (.odt) | LAWIMA | 07_DOCUMENTATION/marketing/ |
| Documents techniques (.docx) | LAWIMA/ancienne | 07_DOCUMENTATION/technical/ |
| Analyse marché immobilier camerounais | LAWIM | Directive/Analyse *marché immobilier*.md |
| Étude de marché complète | LAWIM | KNOWLEDGE/market-research-real-estate-cameroon.md |
| Modèle comportement diaspora | LAWIM | KNOWLEDGE/diaspora-behavior-model.md |
| Signaux de fraude (25 détails) | LAWIM | KNOWLEDGE/fraud-signals-and-verification.md |
| Matrice d'affinité des villes | LAWIM | KNOWLEDGE/city-affinity-matrix.md |

---

*Document patrimonial — Aucune décision de reconstruction n'est prise ici.*
