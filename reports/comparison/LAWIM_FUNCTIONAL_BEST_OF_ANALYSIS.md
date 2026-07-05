# LAWIM - Analyse fonctionnelle croisee du meilleur de chaque depot

## Perimetre et methode
Analyse realisee en lecture seule sur les trois depots suivants :

- `LAWIM_V2` : `/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2`
- `LAWIM` : `/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM`
- `LAWIMA` : `/media/abel/Doc/Drive/d/LAWIM_BACKUP_20260608_125026/LAWIMA`

Le contenu applicatif n'a pas ete modifie. Les chiffres ci-dessous excluent les artefacts de cache, `node_modules`, les environnements virtuels, les dossiers `dist` et `build`.

## Resume executif

- `LAWIM_V2` est le meilleur depot pour servir de base produit. C'est le seul des trois qui presente une architecture runtime coherente, une vraie separation des couches, des services metiers, un schema relationnel executable, un sous-systeme de tests massif et une structure d'exploitation complete.
- `LAWIM` reste la meilleure source normative. Son interet principal est documentaire et fonctionnel : referentiels officiels, regles geographiques, regles de matching, de securite, de notifications, d'API, de deploiement, de tests et de gouvernance.
- `LAWIMA` est la meilleure reserve de matiere brute : packs de donnees, alias, typo dictionaries, heuristiques de langage, classifications de quartier, exemples WhatsApp, signaux lead scoring. En revanche, son code est trop fragmentaire et trop risqué pour etre reutilise tel quel.
- Le meilleur LAWIM final ne doit pas etre un collage de code. Il doit combiner :
  - le runtime propre de `LAWIM_V2`,
  - la doctrine fonctionnelle de `LAWIM`,
  - les donnees et heuristiques de `LAWIMA`.

## Comparaison Generale

| Depot | Volume utile | Nature dominante | Ce qu'il fait le mieux | Limites majeures |
|---|---:|---|---|---|
| `LAWIM_V2` | 1236 fichiers utiles | Produit executable, monolithe Python 3.12 + frontend + infra | Architecture, securite, CRM, communication, analytics, tests, deployment, observabilite | Geo encore trop peu semantique, beaucoup de documentation derivee de `LAWIM` |
| `LAWIM` | 500 fichiers utiles | Archive normative et referentiels officiels | Doctrine fonctionnelle, geo business model, security, notifications, API, deployment, tests, data dictionary | Tres peu de code executable, quasiment pas de tests de vrai runtime |
| `LAWIMA` | 585 fichiers utiles | Reservoir de donnees et prototypes | Packs de villes/quartiers, alias, typos, langage WhatsApp, lead scoring, prototypes de matching | Secrets codes en dur, duplication, scripts ad hoc, peu de structure produit |

Repere documentaire :

- `LAWIM_V2` : 219 fichiers dans `docs/`, 246 dans `reports/`, 7 knowledge packs.
- `LAWIM` : 83 documents dans `ARCHIVES/Directive/`, 40 documents dans `ARCHIVES/docs/`.
- `LAWIMA` : 14 fichiers dans `07_DOCUMENTATION/`, 2 dans `00_GLOBAL/doc_reference/`, 4 dans `00_GLOBAL/doc_projet/`.

## Tableau des Fonctionnalites

| Fonctionnalite | Etat dans `LAWIM_V2` | Etat dans `LAWIM` | Etat dans `LAWIMA` | Analyse / meilleur depot | Recommandation |
|---|---|---|---|---|---|
| Authentification | Auth locale, sessions, bootstrap, rate limiting, et scaffold AAD optionnel. Fichiers : `code/lawim_v2/security/service.py`, `code/lawim_v2/security/aad.py`, `code/lawim_v2/security/identity.py`, `tests/test_security_aad.py`, `reports/program/RELEASE-PROGRAM-AAD-CLOSURE.md`. | Principes clairs sur mot de passe, OTP, MFA, JWT, OAuth Google/Facebook, revocation et traçabilite. Fichier : `ARCHIVES/Directive/15-SECURITY-REFERENCE.md`. | Auth Flask / Telegram / magic-link et etat de conversation, mais avec logique dispersée. Fichiers : `core/auth_app.py`, `core/server_intelligent.py`, `core/config.py`. | `LAWIM_V2` gagne sur l'implementation. `LAWIM` gagne sur la politique. `LAWIMA` est trop fragile et trop couple a des secrets. | Conserver `LAWIM_V2`, importer la politique de `LAWIM`, re-ecrire le moindre pont AAD si besoin, ne pas reprendre `LAWIMA` tel quel. |
| Securite | IAM complet : roles, permissions, policies, sessions, audit, compliance, privacy, risk, incidents, analytics. Fichiers : `code/lawim_v2/security/service.py`, `code/lawim_v2/security/audit.py`, `code/lawim_v2/security/policies.py`, `code/lawim_v2/security/permissions.py`, `code/lawim_v2/security/session.py`. | Referentiel securite tres riche : moindre privilege, signatures webhook, anti-rejeu, secrets hors code, audit, anti-fraude, tests securite. Fichier : `ARCHIVES/Directive/15-SECURITY-REFERENCE.md`. | `core/config.py` contient des secrets en clair et des configurations dupliquees ; `core/payment.py` et `core/test_campay.py` manipulent des credentials directement. | `LAWIM_V2` est la seule base saine. `LAWIM` fournit les regles. `LAWIMA` est a proscrire pour toute reutilisation directe. | Conserver `LAWIM_V2`; faire remonter les principes de `LAWIM`; bannir tout secret ou token de `LAWIMA`. |
| AAD | Scaffold propre, optionnel et testable. Fichiers : `code/lawim_v2/security/aad.py`, `tests/test_security_aad.py`, `reports/program/RELEASE-PROGRAM-AAD-CLOSURE.md`. | Pas de brique AAD native de production, mais la doctrine securite couvre l'authentification et les providers externes. | Pas de vrai AAD, seulement des prototypes d'identite et d'auth. | `LAWIM_V2` a le seul scaffold explicite et non invasif. | Garder AAD comme option, jamais comme fondation de securite globale. |
| Utilisateurs / profils / permissions | Utilisateurs, organisations, sessions, roles et permissions sont modelises proprement. Fichiers : `prisma/schema.prisma`, `code/lawim_v2/project_service.py`, `code/lawim_v2/security/service.py`. | Le dictionnaire de donnees formalise contacts, roles, contact_roles, etc. Fichiers : `ARCHIVES/docs/LAWIM_DATA_DICTIONARY_V1.md`, `ARCHIVES/Directive/08-ROLE-REFERENCE.md`, `ARCHIVES/Directive/06-DATABASE-REFERENCE.md`. | `core/dashboard_master.py` gere `persons`, `agents`, `contestations`; `02_KNOWLEDGE/crm_schema/crm_schema.json` documente utilisateurs/agents/agences/investisseurs. | `LAWIM_V2` est le plus propre executablement, `LAWIM` a le meilleur modele conceptuel, `LAWIMA` a de bonnes donnees de terrain. | Conserver V2, enrichir le schema avec les entites documentaires de LAWIM, importer seulement les referentiels de LAWIMA. |
| CRM | CRM reel : contacts, leads, customers, opportunities, pipelines, communications, consent, customer 360. Fichiers : `code/lawim_v2/crm/service.py`, `code/lawim_v2/crm/repository.py`, `code/lawim_v2/crm/schema_v14_ddl.py`, `code/lawim_v2/source_intelligence/service.py`. | Le dictionnaire de donnees et les references conversation / matching couvrent deja les notions CRM essentielles. Fichiers : `ARCHIVES/docs/LAWIM_DATA_DICTIONARY_V1.md`, `ARCHIVES/Directive/03-CONVERSATION-REFERENCE.md`, `ARCHIVES/Directive/04-MATCHING-REFERENCE.md`. | Donnees CRM riches et prototypes utiles : `02_KNOWLEDGE/crm_schema/crm_schema.json`, `03_ENGINE/lead_scorer/lead_scorer.py`, `03_ENGINE/property_matcher/property_matcher.py`, `core/dashboard_master.py`. | `LAWIM_V2` gagne pour le produit. `LAWIM` est meilleur pour la structure conceptuelle. `LAWIMA` apporte des dictionnaires et des heuristiques. | Conserver le CRM V2, importer les champs manquants du dictionnaire LAWIM, re-exploiter les signaux LAWIMA uniquement comme donnees/heuristiques. |
| GED / documents / medias / stockage | Gestion medias et stockage mieux abstraite : `media_domain.py`, `storage_platform.py`, `BackupCenter`, `LocalMediaStorage`, `prisma/schema.prisma`. | Referentiel storage et backup tres clair : retention, sauvegarde, restauration, separation des supports. Fichiers : `ARCHIVES/Directive/14-STORAGE-REFERENCE.md`, `ARCHIVES/Directive/17-DEPLOYMENT-INFRASTRUCTURE-REFERENCE.md`. | Quelques scripts d'upload et de gestion, mais pas de vraie couche storage propre. Fichiers : `03_ENGINE/file_upload.py`, `core/gestion_biens.py`. | `LAWIM_V2` a la meilleure abstraction. `LAWIM` a la meilleure politique. `LAWIMA` est trop opportuniste. | Conserver V2, importer les regles de retention/backup de LAWIM, ne pas reutiliser les scripts de stockage de LAWIMA. |
| Workflow | Workflow automation complet : workflows, instances, tasks, approvals, queues, events, timers, notifications. Fichiers : `code/lawim_v2/workflow_automation/service.py`, `code/lawim_v2/workflow_automation/repository.py`. | Doctrine workflow tres mature : statuts, etapes, decisions, escalades, conditions de cloture. Fichier : `ARCHIVES/Directive/05-WORKFLOW-REFERENCE.md`. | Pipeline et follow-up scripts utiles mais non industrialises. Fichiers : `03_ENGINE/pipeline_complete.py`, `03_ENGINE/follow_up_system.py`, `core/matching_engine.py`. | `LAWIM_V2` gagne sur l'executable. `LAWIM` gagne sur les regles. `LAWIMA` ne doit servir qu'a inspirer certaines etapes. | Conserver V2, aligner les statuts et conditions sur LAWIM, re-ecrire les scripts LAWIMA si un besoin specifique subsiste. |
| Notifications | Multicanal propre : in-app, templates, preferences, queue, campaigns, analytics, integrations. Fichiers : `code/lawim_v2/communication/service.py`, `code/lawim_v2/communication/notifications.py`, `code/lawim_v2/communication/queue.py`, `code/lawim_v2/communication/templates.py`. | Referentiel officiel tres net sur la priorite, la source, le regroupement, les canaux et la tracabilite. Fichier : `ARCHIVES/Directive/10-NOTIFICATION-REFERENCE.md`. | Notifications pragmatiques mais dispersees : `core/notification_service.py`, `core/notification_manager.py`, `core/notifier.py`. | `LAWIM_V2` est meilleur en implementation, `LAWIM` en doctrine. `LAWIMA` reste un prototype. | Conserver V2, importer les regles de priorite / regroupement de LAWIM, re-ecrire toute logique ad hoc. |
| WhatsApp | Canal supporte nativement via `communication/whatsapp.py`, repository et schema. Fichiers : `code/lawim_v2/communication/whatsapp.py`, `code/lawim_v2/communication/repository.py`, `code/lawim_v2/communication/schema_v17_ddl.py`. | WhatsApp est un canal officiel du moteur de notification et de conversation. Fichiers : `ARCHIVES/Directive/10-NOTIFICATION-REFERENCE.md`, `ARCHIVES/Directive/03-CONVERSATION-REFERENCE.md`. | Tres riche en heuristiques et messages reels, mais code trop couple a Telegram/DeepSeek/Campay. Fichiers : `core/gateway_universal.py`, `core/config.py`, `02_KNOWLEDGE/whatsapp_language/*`, `02_KNOWLEDGE/whatsapp_language/whatsapp_language.json`. | `LAWIM_V2` gagne pour le canal. `LAWIMA` apporte de bonnes donnees linguistiques. | Conserver le canal V2, importer les lexiques et variantes LAWIMA, bannir les tokens et gateway scripts LAWIMA. |
| SMS | Support natif propre dans le moteur de communication. Fichiers : `code/lawim_v2/communication/sms.py`, `code/lawim_v2/communication/repository.py`. | SMS est officiel dans le referentiel notification. Fichier : `ARCHIVES/Directive/10-NOTIFICATION-REFERENCE.md`. | Pas de provider propre ; seulement des mentions et usages indirects. | `LAWIM_V2` gagne. | Conserver V2, garder LAWIM comme reference de politique, ne pas reutiliser de pseudo-provider LAWIMA. |
| Email | Support natif propre dans le moteur de communication. Fichiers : `code/lawim_v2/communication/email.py`, `code/lawim_v2/communication/repository.py`. | Email est un canal officiel du moteur de notification. Fichier : `ARCHIVES/Directive/10-NOTIFICATION-REFERENCE.md`. | Pas de vraie architecture d'email ; configuration dispersée. | `LAWIM_V2` gagne. | Conserver V2. |
| IA | IA structuree et plurielle : assistant, knowledge platform, cognition, analytics AI, source intelligence. Fichiers : `code/lawim_v2/assistant/service.py`, `code/lawim_v2/source_intelligence/service.py`, `code/lawim_v2/analytics/ai.py`, `code/lawim_v2/knowledge_platform/*`. | Doctrine IA et apprentissage continu tres presente dans les directives. Fichiers : `ARCHIVES/Directive/18-LAWIM-AI-REFERENCE.md`, `ARCHIVES/Directive/28-CONTINUOUS-LEARNING-REFERENCE.md`. | Prototypes IA nombreux mais fragiles : `core/deepseek_engine.py`, `core/gemini_engine.py`, `core/semantic_classifier.py`, `core/server_intelligent.py`. | `LAWIM_V2` gagne sur la structure. `LAWIM` fournit la gouvernance. `LAWIMA` apporte quelques heuristiques utiles, pas le code. | Conserver V2, importer les regles IA de LAWIM, ne reutiliser de LAWIMA que les dictionnaires / synonymes / prompts. |
| OCR | Pas d'implementation OCR veritable ; seulement des mentions documentaires. Fichiers : `docs/Directive/18-LAWIM-AI-REFERENCE.md`, `knowledge_packs/*`. | Meme constat : OCR mentionne comme possibilite, pas comme composant livre. Fichier : `ARCHIVES/Directive/18-LAWIM-AI-REFERENCE.md`. | Aucun sous-systeme OCR significatif trouve. | Aucune implementation gagnante. | A construire plus tard si le besoin devient prioritaire ; ne rien importer en l'etat. |
| Recherche | Recherche et filtrage coherents : requetes API, search locations, matching, geo search, frontend maps. Fichiers : `code/lawim_v2/api_query.py`, `code/lawim_v2/matching.py`, `code/lawim_v2/geo_domain.py`, `code/lawim_v2/db.py`, `frontend/packages/maps/src/index.ts`. | Les references matching / geo / multilingual search sont tres riches. Fichiers : `ARCHIVES/Directive/04-MATCHING-REFERENCE.md`, `ARCHIVES/Directive/09-GEOLOCATION-REFERENCE.md`, `ARCHIVES/Directive/30D-MULTILINGUAL-SEARCH-REFERENCE.md`. | Forte valeur sur les alias, typos, neighbourhood packs et classification : `core/matching_engine.py`, `core/semantic_classifier.py`, `02_KNOWLEDGE/search_aliases/*`, `02_KNOWLEDGE/typo_database/*`. | `LAWIM_V2` gagne sur l'implementation. `LAWIM` gagne sur la logique fonctionnelle. `LAWIMA` gagne sur les donnees de recherche. | Conserver le moteur V2, importer les alias / typos / market packs de LAWIMA et les regles de LAWIM. |
| Matching / proximite / geolocalisation | Moteur de scoring propre, Haversine, normalisation de localisation, geocoding provider local/external. Fichiers : `code/lawim_v2/matching.py`, `code/lawim_v2/geo_domain.py`, `code/lawim_v2/geocoding_provider.py`, `prisma/schema.prisma`. | Le modele geographique est le plus riche et le plus utile fonctionnellement. Fichiers : `ARCHIVES/Directive/09-GEOLOCATION-REFERENCE.md`, `ARCHIVES/GEO_REFERENCE_MODEL_CAMEROON_V4.md`, `ARCHIVES/GEO_MODEL_ALIGNMENT_PLAN.md`, `ARCHIVES/MATCHING_ENGINE_V1_SUMMARY.md`, `ARCHIVES/SEED_DATA_FINALIZATION_REPORT.md`. | Donnees locales et heuristiques tres utiles, mais code simple et direct. Fichiers : `core/geolocation.py`, `core/matching_engine.py`, `02_KNOWLEDGE/cities/cameroon_cities.json`, `02_KNOWLEDGE/neighborhoods/yaounde.json`, `02_KNOWLEDGE/neighborhoods/douala.json`. | Le meilleur resultat est hybride : `LAWIM` pour la logique metier, `LAWIM_V2` pour le runtime, `LAWIMA` pour les packs de donnees. | Voir la section geolocalisation detaillee. |
| Reporting / tableaux de bord / analytics | Suite analytique complete : KPI, dashboards, BI, datamarts, realtime, exports, AI insights, integrations. Fichiers : `code/lawim_v2/analytics/service.py`, `code/lawim_v2/analytics/reporting.py`, `code/lawim_v2/analytics/dashboards.py`, `code/lawim_v2/analytics/bi.py`, `code/lawim_v2/analytics/datamarts.py`, `code/lawim_v2/analytics/realtime.py`. | Referentiels de reporting et dashboard tres clairs. Fichiers : `ARCHIVES/Directive/11-REPORTING-REFERENCE.md`, `ARCHIVES/Directive/07-DASHBOARD-REFERENCE.md`. | Dashboards Streamlit et scripts de visualisation utiles mais non industrialises. Fichiers : `core/dashboard_master.py`, `core/dashboard_universel.py`, `07_DASHBOARD/*`. | `LAWIM_V2` gagne largement. | Conserver V2, importer les criteres de reporting de LAWIM, re-etalonner certains tableaux de bord avec les donnees LAWIMA. |
| API / integrations / webhooks | Serveur HTTP industriel, CORS, routes V2, health, metrics, bootstrap, uploads multipart, integrations transverses. Fichiers : `code/lawim_v2/server.py`, `code/lawim_v2/services.py`, `code/lawim_v2/source_intelligence/service.py`, `code/lawim_v2/communication/integrations.py`, `code/lawim_v2/analytics/integrations.py`. | API reference tres precise, versioning, webhooks signes, documentation, compatibilite ascendante. Fichiers : `ARCHIVES/Directive/16-API-REFERENCE.md`, `ARCHIVES/Directive/17-DEPLOYMENT-INFRASTRUCTURE-REFERENCE.md`. | Gateways Telegram / Flask / Supabase tres directes, mais heterogenes et dupliquees. Fichiers : `core/gateway_universal.py`, `core/server_intelligent.py`, `core/supabase_client.py`, `core/payment.py`. | `LAWIM_V2` gagne pour le produit. `LAWIM` gagne sur le contrat d'API. `LAWIMA` est trop fragile. | Conserver V2, aligner les contrats sur LAWIM, ne pas reprendre les gateways LAWIMA. |
| Migration / deployment / Docker / Nginx / monitoring / logs / performance | Stack d'exploitation la plus complete : compose, deployment, nginx, monitoring, health checks, logging, benchmarks, validations. Fichiers : `compose/README.md`, `deployment/health/health_checker.py`, `deployment/validator/index.ts`, `deployment/nginx/*`, `logging/README.md`, `scripts/benchmark_runtime.py`, `scripts/bench_hot_paths.py`, `reports/PRODUCTION-READINESS.md`. | Doctrine d'exploitation tres forte : OVH, Docker, Nginx, PostgreSQL, PostGIS, Redis, sauvegardes, monitoring, rollback. Fichiers : `ARCHIVES/Directive/17-DEPLOYMENT-INFRASTRUCTURE-REFERENCE.md`, `ARCHIVES/Directive/22-OPERATIONS-RUNBOOK.md`, `ARCHIVES/Directive/23-INSTALLATION-GUIDE.md`, `ARCHIVES/Directive/40-PRODUCTION-CHECKLIST.md`. | Existent, mais trop proches de prototypes ou de secrets en dur. Fichiers : `Dockerfile`, `docker-compose.yml`, `deploiement_ovh/*`, `sauvegardes/*`, `core/config.py`. | `LAWIM_V2` est le meilleur socle technique. `LAWIM` reste la meilleure doctrine. `LAWIMA` est a utiliser avec prudence extreme. | Conserver V2, importer les procedures LAWIM, ne jamais copier les secrets ni les scripts de LAWIMA. |
| Tests | Tres fort : harness partage, suites `unittest`, 2619 tests annoncees au 2026-07-04, tests runtime, migration, i18n, productization. Fichiers : `tests/README.md`, `tests/test_user_journeys.py`, `tests/test_product_depth.py`, `tests/test_security_aad.py`, `tests/test_runtime_smoke.py`. | Doctrine de qualite tres claire, mais pas de grande suite executable dans le depot. Fichier : `ARCHIVES/Directive/12-TESTS-REFERENCE.md`. | Quelques scripts de test ad hoc, souvent avec reseau et credentials. Fichiers : `core/test_admin_roles.py`, `core/test_campay.py`, `05_AUTOMATIONS/test_pipeline.py`. | `LAWIM_V2` gagne tres largement. | Conserver V2, importer la taxonomie de tests LAWIM, traiter les scripts LAWIMA comme des preuves historiques, pas comme une suite. |
| Documentation | Volume le plus important mais tres oriente execution et releases. Fichiers : `docs/README.md`, `docs/Directive/*`, `reports/*`, `knowledge_packs/*`, `release/*`. | Corpus le plus propre et le plus normatif : directives, guides, procedures, gouvernance, certification. Fichiers : `ARCHIVES/Directive/*`, `ARCHIVES/docs/*`, `ARCHIVES/TRANSMISSION/*`. | Documentation plus dispersee, melange de projets, references et archives. Fichiers : `07_DOCUMENTATION/*`, `00_GLOBAL/doc_reference/*`, `00_GLOBAL/doc_projet/*`, `99_ARCHIVES/*`. | `LAWIM` reste la meilleure source normative. `LAWIM_V2` a la meilleure couverture operationnelle. `LAWIMA` est la plus fragile. | Garder LAWIM comme reference documentaire canonique, utiliser V2 pour l'operationnel, ne conserver LAWIMA que pour les donnees et les signaux. |

## Geolocalisation Detaillee

### 1. `LAWIM_V2` : la meilleure base runtime

La geolocalisation runtime de `LAWIM_V2` est la plus propre des trois :

- normalisation pays / ville / region / code postal / adresse ;
- validation stricte des coordonnees ;
- cle de recherche geographique normalisee ;
- provider de geocodage local deterministic et provider externe optionnel ;
- scoring avec Haversine dans le moteur de matching ;
- stockage des coordonnees dans le schema relationnel ;
- presence d'une interface front map et de fichiers de recherche geographique.

Fichiers cles :

- `code/lawim_v2/geo_domain.py`
- `code/lawim_v2/geocoding_provider.py`
- `code/lawim_v2/matching.py`
- `prisma/schema.prisma`
- `frontend/packages/maps/src/index.ts`
- `frontend/apps/web/src/App.tsx`

Points faibles :

- le modele est encore trop plat ;
- la hierarchie territoriale est limitee a ville / region / pays ;
- les quartiers, clusters, sous-clusters, zones d'affinite et niveaux de confiance sont peu expresses dans le runtime.

### 2. `LAWIM` : la meilleure doctrine geo

`LAWIM` est nettement plus fort sur la logique geo-metier. Les textes de reference apportent :

- une hiérarchie market -> cluster -> subcluster -> neighborhood -> affinity -> GPS ;
- un principe explicite : le GPS ne doit jamais primer sur la logique metier ;
- des niveaux de precision distingues ;
- des regles de confidentialite sur la localisation ;
- des matrices d'affinite et des regles de rejet ;
- des modeles Geo Request / Opportunity et une alignement Prisma cible ;
- des segments de quartiers ambigus comme Bastos, Omnisports, Bonamoussadi, Akwa, Makepe, Odza, Mokolo, Logpom, Tsinga, Nkoabang.

Fichiers cles :

- `ARCHIVES/Directive/09-GEOLOCATION-REFERENCE.md`
- `ARCHIVES/GEO_REFERENCE_MODEL_CAMEROON_V4.md`
- `ARCHIVES/GEO_MODEL_ALIGNMENT_PLAN.md`
- `ARCHIVES/MATCHING_ENGINE_V1_SUMMARY.md`
- `ARCHIVES/REQUEST_ENGINE_VALIDATION_REPORT.md`
- `ARCHIVES/SEED_DATA_FINALIZATION_REPORT.md`
- `ARCHIVES/docs/LAWIM_DATA_DICTIONARY_V1.md`

Ce depot contient la meilleure definition du "bon" modele geographique pour LAWIM. Il ne contient pas la meilleure implementation executable.

### 3. `LAWIMA` : la meilleure reserve de donnees geo et de signaux

`LAWIMA` apporte une matiere brute tres utile :

- villes prioritaires avec aliases, typos et variantes sociales ;
- quartiers avec landmarks, references informelles et profils de marche ;
- mots-cles de recherche et formes typographiques ;
- scoring lead et signaux WhatsApp ;
- exemples de messages en francais, anglais et pidgin ;
- packs de donnees par ville et quartier.

Fichiers cles :

- `02_KNOWLEDGE/cities/cameroon_cities.json`
- `02_KNOWLEDGE/neighborhoods/yaounde.json`
- `02_KNOWLEDGE/neighborhoods/douala.json`
- `02_KNOWLEDGE/search_aliases/search_aliases.json`
- `02_KNOWLEDGE/typo_database/typo_database.json`
- `02_KNOWLEDGE/whatsapp_language/whatsapp_language.json`
- `02_KNOWLEDGE/lead_scoring/lead_scoring.json`
- `02_KNOWLEDGE/scoring/lead_scoring_rules.json`
- `02_KNOWLEDGE/crm_schema/crm_schema.json`

### Verdict geolocalisation

Le meilleur resultat n'est pas un seul depot. C'est une combinaison :

1. `LAWIM_V2` pour la couche runtime.
2. `LAWIM` pour la doctrine territoriale.
3. `LAWIMA` pour les datasets locaux, les alias et les heuristiques de langage.

La priorite produit doit etre :

- importer le referentiel geo de `LAWIM` dans un modele V2 propre ;
- injecter les packs `LAWIMA` comme donnees versionnees, pas comme code ;
- garder le geocoding local / externe de `LAWIM_V2` ;
- ajouter les niveaux quartier / cluster / sous-cluster / affinite / confiance.

## Modeles de Donnees

### `LAWIM_V2`

Le schema executable est propre et coherent :

- `Organization`
- `User`
- `Session`
- `Property`
- `Media`
- `Conversation`
- `Message`
- `Event`
- `Notification`
- `SchemaMeta`
- `Project`
- `ProjectStep`
- `ProjectChecklistItem`
- `ProjectStepHistory`

Le manifeste de persistance ajoute une vision transversale et aligne SQLite, PostgreSQL et Prisma. Fichiers cles :

- `code/lawim_v2/persistence.py`
- `prisma/schema.prisma`
- `code/lawim_v2/db.py`
- `code/lawim_v2/schema_ddl.py`

Limites :

- timestamps souvent stockes en `String` ;
- le modele metier de geographie est encore simplifie ;
- certaines entites metier du dictionnaire LAWIM ne sont pas encore representees.

### `LAWIM`

Le dictionnaire de donnees est plus riche conceptuellement. Il couvre :

- Contacts
- Roles
- Contact_Roles
- Client_Cases
- Opportunities
- Properties
- Property_Owners
- Property_Managers
- Listings
- Property_Features
- Property_Media
- Availability_History
- Verification_Records
- Matches
- Match_Scores
- Match_Feedbacks
- Conversations

Fichier cle :

- `ARCHIVES/docs/LAWIM_DATA_DICTIONARY_V1.md`

### `LAWIMA`

`LAWIMA` contient une reserve de schemas et de packs :

- `02_KNOWLEDGE/crm_schema/crm_schema.json`
- `02_KNOWLEDGE/cities/cameroon_cities.json`
- `02_KNOWLEDGE/neighborhoods/*.json`
- `02_KNOWLEDGE/property_types/property_types.json`
- `02_KNOWLEDGE/pricing/pricing.json`
- `02_KNOWLEDGE/search_aliases/search_aliases.json`
- `02_KNOWLEDGE/lead_scoring/lead_scoring.json`
- `02_KNOWLEDGE/typo_database/typo_database.json`
- `02_KNOWLEDGE/whatsapp_language/*.json`
- `02_KNOWLEDGE/entity_linking/entity_linking.json`

Mais ces donnees sont tres souvent dupliques, backuppees ou regroupees en archives de repair. Elles doivent etre normalisees avant toute industrialisation.

### Conclusion donnees

Le meilleur modele de donnees doit etre :

- executable comme `LAWIM_V2`,
- plus riche comme `LAWIM`,
- alimente par les packs de `LAWIMA`.

## Referentiels

### Ce que `LAWIM` apporte de meilleur

Les referentiels officiels de `LAWIM` sont la colonne vertebrale fonctionnelle du programme :

- `00-CONSTITUTION.md`
- `04-MATCHING-REFERENCE.md`
- `05-WORKFLOW-REFERENCE.md`
- `06-DATABASE-REFERENCE.md`
- `07-DASHBOARD-REFERENCE.md`
- `08-ROLE-REFERENCE.md`
- `09-GEOLOCATION-REFERENCE.md`
- `10-NOTIFICATION-REFERENCE.md`
- `11-REPORTING-REFERENCE.md`
- `12-TESTS-REFERENCE.md`
- `15-SECURITY-REFERENCE.md`
- `16-API-REFERENCE.md`
- `17-DEPLOYMENT-INFRASTRUCTURE-REFERENCE.md`
- `18-LAWIM-AI-REFERENCE.md`
- `23-INSTALLATION-GUIDE.md`
- `24-DEVELOPER-GUIDE.md`
- `25-USER-GUIDE.md`
- `27-TRACEABILITY-MATRIX.md`
- `30-I18N-L10N-REFERENCE.md`

Ces documents donnent la logique a respecter, les regles de priorite, les flux et les contraintes.

### Ce que `LAWIM_V2` apporte

`LAWIM_V2` a repris une partie de ces referentiels en copie figée dans `docs/Directive/`, puis les a enrichis avec :

- des plans de release,
- des rapports d'implementation,
- des knowledge packs,
- des matrices de traçabilite,
- des manifests de deploiement,
- des guides operationnels.

Cela en fait un meilleur depot d'execution, mais pas une meilleure source normative pure.

### Ce que `LAWIMA` apporte

`LAWIMA` n'a pas un corpus de referentiels centralise aussi propre. Il apporte surtout :

- des dictionnaires de donnees,
- des variations de termes,
- des packs de villes / quartiers / mots-cles,
- des archives de repair et de reconstruction.

Il faut le lire comme un reservoir de matiere premiere, pas comme un standard documentaire.

## Documentation

### `LAWIM`

`LAWIM` reste la meilleure base documentaire officielle :

- corpus de directives numerotees,
- architecture, gouvernance, procedures, installation, developpement, utilisateur,
- certification et matrice de traceabilite,
- vocabulaire metier et business dictionary.

La documentation est plus normative que volumique. C'est ce qui la rend utile.

### `LAWIM_V2`

`LAWIM_V2` a la plus grande masse documentaire exploitable :

- `docs/README.md` indique explicitement que le dossier est une copie figee depuis `LAWIM/Directive`,
- les `reports/` documentent les sprints, releases, validations et revues d'engineering,
- les `knowledge_packs/` centralisent les visions business, developer, director et full pack,
- les dossiers `deployment/`, `compose/`, `release/`, `logging/`, `implementation/` sont orientes exploitation.

Conclusion : excellente couverture operationnelle, mais documentation en partie derivee.

### `LAWIMA`

`LAWIMA` est le plus faible en documentation propre :

- quelques dossiers `07_DOCUMENTATION/`,
- quelques references sous `00_GLOBAL/`,
- beaucoup d'archives et de sauvegardes,
- peu de point d'entree central,
- un README racine peu utile comme porte d'entree.

## Tests

### `LAWIM_V2`

Le meilleur socle de test de loin :

- `tests/README.md` annonce 2619 tests au 2026-07-04 ;
- harness partage ;
- tests de parcours utilisateur, profondeur produit, stabilisation MVP, beta, release candidate, runtime smoke, i18n, migration framework ;
- integration Python `unittest`, validation Prisma, smoke runtime.

Fichiers cles :

- `tests/README.md`
- `tests/lawim_harness.py`
- `tests/test_user_journeys.py`
- `tests/test_product_depth.py`
- `tests/test_security_aad.py`
- `tests/test_runtime_smoke.py`
- `tests/test_migration_framework.py`

### `LAWIM`

`LAWIM` a une doctrine de tests tres propre :

- tests fonctionnels,
- techniques,
- integration,
- metier,
- securite,
- performance,
- regression,
- preproduction.

Mais le depot ne porte pas de grande suite executable equivalente.

Fichier cle :

- `ARCHIVES/Directive/12-TESTS-REFERENCE.md`

### `LAWIMA`

`LAWIMA` ne dispose que de tests ad hoc :

- `core/test_admin_roles.py`
- `core/test_campay.py`
- `05_AUTOMATIONS/test_pipeline.py`

Ce sont des scripts de verification ou de demonstration, pas une infrastructure de test industrielle.

## Analyse Des Fichiers

### Fichiers absents ou insuffisants

- `LAWIM` : quasi absence de runtime produit et de suite de tests executable.
- `LAWIMA` : absence de couche d'architecture stable, absence de gestion saine des secrets, absence de tests structurants.
- `LAWIM_V2` : profondeur geo encore insuffisante au regard de la doctrine de `LAWIM`.

### Fichiers plus complets

- Geo et matching de reference : `LAWIM/ARCHIVES/GEO_REFERENCE_MODEL_CAMEROON_V4.md`, `LAWIM/ARCHIVES/GEO_MODEL_ALIGNMENT_PLAN.md`, `LAWIM/ARCHIVES/MATCHING_ENGINE_V1_SUMMARY.md`.
- Dictionnaire de donnees : `LAWIM/ARCHIVES/docs/LAWIM_DATA_DICTIONARY_V1.md`.
- Runtime moderne : `LAWIM_V2/code/lawim_v2/security/service.py`, `LAWIM_V2/code/lawim_v2/communication/service.py`, `LAWIM_V2/code/lawim_v2/analytics/service.py`, `LAWIM_V2/code/lawim_v2/workflow_automation/service.py`.
- Packs de donnees : `LAWIMA/02_KNOWLEDGE/cities/cameroon_cities.json`, `LAWIMA/02_KNOWLEDGE/neighborhoods/yaounde.json`, `LAWIMA/02_KNOWLEDGE/whatsapp_language/whatsapp_language.json`.

### Fichiers plus modernes et plus propres

- `LAWIM_V2/code/lawim_v2/server.py`
- `LAWIM_V2/code/lawim_v2/persistence.py`
- `LAWIM_V2/prisma/schema.prisma`
- `LAWIM_V2/code/lawim_v2/geo_domain.py`
- `LAWIM_V2/code/lawim_v2/geocoding_provider.py`
- `LAWIM_V2/code/lawim_v2/matching.py`
- `LAWIM_V2/code/lawim_v2/security/aad.py`

Ces fichiers sont mieux isoles, plus lisibles, plus testables et mieux alignes avec un produit industrialisable.

### Fichiers obsoletes ou a traiter comme historiques

- `LAWIMA/core/config.py` : secrets et tokens en clair.
- `LAWIMA/core/gateway_universal.py` et les variantes `gateway_*` : duplication, etat global, logique hardcodee.
- `LAWIMA/core/dashboard_master.py` : UI admin utile historiquement, mais trop couplee a la base et a la presentation.
- `LAWIMA/core/test_campay.py` : test manuel avec credentials.
- `LAWIM/Downloads/*` : copies derivées de la documentation officielle.
- Tous les dossiers de backup/repair/archive de `LAWIMA` : utiles comme trace, pas comme source de runtime.

### Doublons

- `LAWIM_V2/docs/Directive/*` reprend la substance de `LAWIM/ARCHIVES/Directive/*`.
- `LAWIMA` contient plusieurs couches de duplications : `_archive`, `_archive_minimal`, `_repair_backup`, `sauvegardes`, `venv`, `venv_lawim`.
- `LAWIM` a aussi des copies et dossiers `Downloads/` qui doivent rester des archives, pas des sources actives.

### Meilleures implementations

- `LAWIM_V2/code/lawim_v2/security/service.py`
- `LAWIM_V2/code/lawim_v2/communication/service.py`
- `LAWIM_V2/code/lawim_v2/analytics/service.py`
- `LAWIM_V2/code/lawim_v2/workflow_automation/service.py`
- `LAWIM_V2/code/lawim_v2/matching.py`
- `LAWIM_V2/code/lawim_v2/geo_domain.py`
- `LAWIM_V2/code/lawim_v2/geocoding_provider.py`
- `LAWIM_V2/code/lawim_v2/source_intelligence/service.py`
- `LAWIM/ARCHIVES/GEO_REFERENCE_MODEL_CAMEROON_V4.md`
- `LAWIM/ARCHIVES/docs/LAWIM_DATA_DICTIONARY_V1.md`
- `LAWIMA/02_KNOWLEDGE/cities/cameroon_cities.json`
- `LAWIMA/02_KNOWLEDGE/neighborhoods/yaounde.json`
- `LAWIMA/02_KNOWLEDGE/lead_scoring/lead_scoring.json`

## Elements A Integrer Dans `LAWIM_V2`

Priorite haute :

- le modele geographique de `LAWIM` : market, cluster, subcluster, neighborhood, affinity, GPS confidence ;
- les packs geo et alias de `LAWIMA` : villes, quartiers, landmarks, typos, signaux sociaux ;
- le dictionnaire de donnees de `LAWIM` : ownership, management, verification, feedback, match score, history ;
- les regles de priorite, regroupement et criticite des notifications de `LAWIM` ;
- la taxonomie de tests de `LAWIM` ;
- les regles d'API, de webhook et de versioning de `LAWIM` ;
- les procedures de deployment, backup, rollback et monitoring de `LAWIM`.

Priorite moyenne :

- les signaux lead scoring de `LAWIMA`,
- les synonymes / alias de recherche / variations orthographiques,
- les exemples de messages WhatsApp / pidgin / anglais,
- les rules de matching locales, notamment sur Douala, Yaounde, Buea, Kribi, Bamenda, Bafoussam.

Priorite basse :

- les elements purement operationnels des archives si un equivalent V2 existe deja,
- les copies de documentation sans valeur supplementaire,
- les scripts de demonstration ou d'ancienne interface qui ne servent qu'a l'historique.

## Elements A Ne Jamais Reutiliser

- `LAWIMA/core/config.py` et tout fichier contenant des secrets, tokens ou cles en clair.
- `LAWIMA/core/gateway_universal.py` et les variantes `gateway_*` en tant que base de production.
- `LAWIMA/core/server_intelligent.py` en tant qu'architecture de serveur principale.
- `LAWIMA/core/test_campay.py` et tout test qui embarque des identifiants reels.
- Les environnements virtuels et paquets installes commits dans l'arborescence des trois depots.
- Les dumps, inventories, backups et repair artifacts comme source de runtime.
- Les dashboards Streamlit ad hoc comme socle applicatif final.
- Les appels directs non abstraits a Telegram, DeepSeek, Gemini, Supabase, Campay ou Nominatim quand ils contournent une couche metier propre.

## Priorisation Des Ameliorations

### P0

1. Fusionner la doctrine geo de `LAWIM` avec le runtime geo de `LAWIM_V2`.
2. Normaliser et versionner les packs d'aliases / quartiers / villes de `LAWIMA`.
3. Completer le modele de donnees V2 avec les entites manquantes du dictionnaire `LAWIM`.
4. Verrouiller la hygiene des secrets et supprimer toute tentation de reutiliser `LAWIMA/core/config.py`.
5. Couvrir les regles geo, matching, notifications et API par des tests de regression.

### P1

1. Importer la taxonomie de notifications et de workflows de `LAWIM`.
2. Renforcer le reporting avec les conventions officielles de `LAWIM`.
3. Integrer les signaux de lead scoring, de langue et de typo handling de `LAWIMA`.
4. Harmoniser les contrats d'API et les webhooks autour d'une specification unique.

### P2

1. Travailler l'OCR seulement si un besoin produit clair existe.
2. Enrichir les couches IA et source intelligence apres consolidation des donnees et du geo.
3. Nettoyer progressivement les artifacts et archives obsoletes en dehors du runtime.

## Conclusion Generale

### Ce que `LAWIM_V2` possede de meilleur

- la meilleure architecture executable ;
- la meilleure securite runtime ;
- le meilleur CRM exploitable ;
- la meilleure suite communication / notification ;
- la meilleure analytique ;
- la meilleure base de tests ;
- la meilleure industrialisation de deployment et d'observabilite.

### Ce que `LAWIM` apporte encore

- la meilleure doctrine fonctionnelle ;
- le meilleur modele geo business ;
- la meilleure specification des notifications, API, deployment et tests ;
- la meilleure base de reference pour les modeles de donnees et les roles.

### Ce que `LAWIMA` apporte encore

- la meilleure reserve de packs de donnees ;
- les meilleurs alias / typos / variantes locales ;
- les meilleures heuristiques de messages WhatsApp et de lead scoring ;
- quelques prototypes utiles pour comprendre le parcours terrain.

### Ce qu'il est pertinent d'integrer avant les prochaines releases

1. Le referentiel geo de `LAWIM` dans `LAWIM_V2`.
2. Les packs de donnees de `LAWIMA` dans un module versionne et propre.
3. Les entites donnees manquantes du dictionnaire `LAWIM`.
4. Les regles de notifications, reporting, API et tests de `LAWIM`.
5. La doctrine de deployment, backup, monitoring et rollback de `LAWIM`.

### Verdict final

`LAWIM_V2` doit rester la base cible. `LAWIM` doit rester la source normative. `LAWIMA` doit rester le reservoir de materiaux reutilisables apres nettoyage, normalisation et re-ecriture.
