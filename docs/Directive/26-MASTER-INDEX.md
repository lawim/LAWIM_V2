# LAWIM

# 26-MASTER-INDEX.md

# Index maître de la documentation

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le présent document récapitule l'ensemble de la documentation officielle de LAWIM.

Il constitue la référence unique pour :

* les modules ;
* les dépendances ;
* les moteurs ;
* les workflows ;
* les données ;
* les API ;
* les KPI ;
* les tests ;
* les modules de paiement.

---

# CHAPITRE 2 — CATALOGUE DES MODULES

| Module | Titre officiel | Rôle principal | Dépendances principales |
| --- | --- | --- | --- |
| 00 | CONSTITUTION | Source de vérité absolue | Tous les modules |
| 01 | GLOSSAIRE | Langage métier canonique | 00, 02, 03, 04, 06 |
| 02 | PROPERTY-REFERENCE | Référentiel maître des biens | 00, 01, 02A-02I |
| 02A | RESIDENTIAL-REFERENCE | Biens résidentiels | 02, 02H, 02I |
| 02B | COMMERCIAL-REFERENCE | Biens commerciaux | 02, 02H, 02I |
| 02C | INDUSTRIAL-REFERENCE | Biens industriels | 02, 02H, 02I |
| 02D | LAND-REFERENCE | Biens fonciers | 02, 02H, 02I |
| 02E | AGRICULTURAL-REFERENCE | Biens agricoles | 02, 02H, 02I |
| 02F | HOTEL-REFERENCE | Biens hôteliers | 02, 02H, 02I |
| 02G | PROJECT-REFERENCE | Projets immobiliers | 02, 02H, 02I |
| 02H | ATTRIBUTE-CATALOG | Normalisation des attributs | 01, 02, 02I |
| 02I | PRICING-REFERENCE | Référentiel officiel des prix | 02, 02H, 04, 06, 07, 11 |
| 03 | CONVERSATION-REFERENCE | Qualification conversationnelle | 00, 01, 02, 02H, 02I |
| 04 | MATCHING-REFERENCE | Matching officiel | 00, 01, 02, 02H, 02I, 03, 06, 09, 11 |
| 05 | WORKFLOW-REFERENCE | Cycles de vie métier | 00, 02, 03, 04, 10, 29 |
| 06 | DATABASE-REFERENCE | Modèle de données | 00, 01, 02, 02H, 02I, 03, 04, 05, 08, 09, 10, 11, 14, 29 |
| 07 | DASHBOARD-REFERENCE | Affichage de pilotage | 00, 02I, 03, 04, 05, 06, 08, 09, 10, 11, 29 |
| 08 | ROLE-REFERENCE | Rôles et permissions | 00, 01, 06, 13, 15, 19 |
| 09 | GEOLOCATION-REFERENCE | Géolocalisation | 00, 01, 02, 04, 06, 11 |
| 10 | NOTIFICATION-REFERENCE | Notifications | 00, 05, 06, 07, 08, 11, 14, 29 |
| 11 | REPORTING-REFERENCE | KPI et reporting | 00, 02I, 04, 06, 07, 10, 14, 29 |
| 12 | TESTS-REFERENCE | Stratégie qualité | Tous les modules |
| 13 | ARCHITECTURE-GOVERNANCE-REFERENCE | Gouvernance d'architecture | Tous les modules |
| 14 | STORAGE-REFERENCE | Stockage, archivage, sauvegardes | 00, 06, 13, 17, 22 |
| 15 | SECURITY-REFERENCE | Sécurité | 00, 06, 08, 10, 13, 14, 29 |
| 16 | API-REFERENCE | Contrats d'API | 00, 03, 04, 05, 06, 15, 29 |
| 17 | DEPLOYMENT-INFRASTRUCTURE-REFERENCE | Déploiement et infrastructure | 14, 15, 16, 22, 23, 29 |
| 18 | LAWIM-AI-REFERENCE | Assistance IA | 00, 01, 03, 04, 11, 13, 28 |
| 19 | ADMINISTRATION-REFERENCE | Administration | 08, 10, 13, 15, 17, 29 |
| 20 | MOBILE-REFERENCE | Expérience mobile | 15, 16, 29 |
| 21 | UX-UI-DESIGN-SYSTEM | Design system | 07, 10, 16, 20, 29 |
| 22 | OPERATIONS-RUNBOOK | Exploitation | 14, 17, 19, 29 |
| 23 | INSTALLATION-GUIDE | Installation | 14, 16, 17, 29 |
| 24 | DEVELOPER-GUIDE | Guide développeur | 00, 12, 13, 15, 16, 29 |
| 25 | USER-GUIDE | Guide utilisateur | 00, 03, 04, 07, 10, 29 |
| 26 | MASTER-INDEX | Index central | Tous les modules |
| 27 | TRACEABILITY-MATRIX | Traçabilité globale | Tous les modules |
| 28 | CONTINUOUS-LEARNING-REFERENCE | Amélioration continue | 04, 11, 18, 29 |
| 29 | CAMPAY-PAYMENT-REFERENCE | Paiement Campay | 05, 06, 07, 10, 11, 15, 16, 17, 19, 22, 23, 24 |
| 30 | I18N-L10N-REFERENCE | Internationalisation et localisation | 00, 01, 03, 04, 05, 06, 07, 10, 11, 12, 16, 18, 20, 21, 24, 25, 28, 29 |
| 30A | BUSINESS-DICTIONARY-REFERENCE | Dictionnaire métier | 01, 03, 04, 18, 28, 30 |
| 30B | TRANSLATION-REFERENCE | Traduction | 30, 16, 18, 20, 21, 25 |
| 30C | LANGUAGE-DETECTION-REFERENCE | Détection de langue | 30, 03, 04, 18, 20, 25 |
| 30D | MULTILINGUAL-SEARCH-REFERENCE | Recherche multilingue | 30, 01, 03, 04, 18, 25 |
| 31 | IMPLEMENTATION-ROADMAP | Plan d'implémentation | 00, 13, 26, 27, 31 |
| 32 | DEVELOPMENT-GOVERNANCE | Gouvernance de développement | 00, 13, 24, 31, 33 |
| 32F | FINAL-CERTIFICATION-REPORT | Rapport final de certification | 00, 13, 26, 27, 31, 32 |
| 33 | CODEX-IMPLEMENTATION-RULES | Règles Codex | 00, 13, 24, 31, 32 |
| 34 | IMPLEMENTATION-BACKLOG | Backlog d'implémentation | 31, 32, 33, 37 |
| 35 | MIGRATION-PLAN | Plan de migration | 14, 17, 22, 31, 39 |
| 36 | RELEASE-PLAN | Plan de release | 31, 32, 37, 39, 40 |
| 37 | QUALITY-ASSURANCE-PLAN | Assurance qualité | 12, 31, 32, 36, 40 |
| 38 | GIT-STRATEGY | Stratégie Git | 31, 32, 33, 36, 39 |
| 39 | CI-CD-REFERENCE | CI/CD | 17, 31, 32, 35, 38, 40 |
| 40 | PRODUCTION-CHECKLIST | Checklist de production | 17, 22, 31, 36, 39 |
| 41 | OPERATIONAL-PROCEDURES | Procédures opérationnelles maîtres | 00, 05, 06, 10, 11, 13, 15, 19, 22, 29 |
| 42 | PARTNER-ONBOARDING-PROCEDURE | Intégration partenaires | 00, 05, 06, 08, 13, 19, 41 |
| 43 | PROPERTY-VERIFICATION-PROCEDURE | Vérification des biens | 00, 02, 02H, 02I, 05, 06, 15, 41 |
| 44 | COMPLAINTS-AND-DISPUTES-PROCEDURE | Réclamations et litiges | 00, 05, 06, 10, 15, 19, 41 |
| 45 | AGENCY-CERTIFICATION-PROCEDURE | Certification agences | 00, 05, 06, 08, 13, 19, 41 |
| 46 | FRAUD-MANAGEMENT-PROCEDURE | Gestion fraude | 00, 06, 15, 19, 28, 41 |
| 47 | PARTNER-SUSPENSION-PROCEDURE | Suspension partenaires | 00, 05, 06, 08, 15, 19, 41, 46 |
| 48 | LAWIM-SALES-PLAYBOOK | Manuel commercial | 00, 01, 19, 24, 25, 41, 42, 45, 46, 47 |
| 49 | TICKET-EXECUTOR-REFERENCE | Point d'entree unique de traitement des tickets | 05, 33, 38, 41 |
| RPT | IMPLEMENTATION-READINESS-REPORT | Rapport de préparation | 26, 31, 32, 37 |
| MKT | MARKETING-TRACKING-CONSOLIDATION-REPORT | Tracking marketing, attribution, campaign, publication, lead attribution, redirect, conversion, KPI, analytics | 05, 06, 07, 11, 12, 16, 18, 19, 26, 27, 28, 29, 30A, 31, 32 |

---

# CHAPITRE 3 — MOTEURS OFFICIELS

Les moteurs officiels de LAWIM sont :

* Workflow Engine ;
* Conversation Engine ;
* Qualification Engine ;
* Matching Engine ;
* Dashboard Engine ;
* Notification Engine ;
* Geo Engine ;
* Role Engine ;
* Reporting Engine ;
* Storage Lifecycle Manager ;
* Security Engine ;
* API Gateway ;
* Administration Engine ;
* LAWIM AI ;
* Continuous Learning Engine ;
* Campay Payment Engine.

---

# CHAPITRE 4 — WORKFLOWS OFFICIELS

Les workflows centraux incluent notamment :

* qualification ;
* publication ;
* matching ;
* rematching ;
* conversation ;
* visite ;
* négociation ;
* transaction ;
* services payants ;
* paiement Campay ;
* archivage ;
* incident.

---

# CHAPITRE 5 — DONNÉES PRINCIPALES

Les données majeures couvrent notamment :

* utilisateurs ;
* rôles ;
* biens ;
* demandes ;
* leads ;
* conversations ;
* relations ;
* notifications ;
* rapports ;
* paiements ;
* archives ;
* journaux ;
* scores.

---

# CHAPITRE 6 — ÉVÉNEMENTS

Les événements clés incluent notamment :

* publication ;
* correction ;
* matching ;
* refus ;
* visite ;
* validation ;
* paiement initié ;
* paiement confirmé ;
* paiement échoué ;
* webhook Campay ;
* archivage ;
* alerte.

---

# CHAPITRE 7 — API PRINCIPALES

Les API principales doivent couvrir :

* authentification ;
* biens ;
* demandes ;
* matching ;
* workflows ;
* notifications ;
* reporting ;
* administration ;
* paiement Campay ;
* webhooks ;
* IA.

---

# CHAPITRE 8 — KPI MAJEURS

Les KPI principaux incluent :

* taux de matching ;
* taux de conversion ;
* taux de réponse ;
* taux de visite ;
* taux de service ;
* taux de confirmation de paiement ;
* volume de paiements ;
* taux de rapprochement ;
* taux d'archivage ;
* taux d'erreur.

---

# CHAPITRE 9 — TESTS MAJEURS

Les familles de tests principales sont :

* sécurité ;
* API ;
* matching ;
* workflows ;
* stockage ;
* paiements ;
* reporting ;
* mobile ;
* installation ;
* exploitation ;
* continuité ;
* IA.

---

# CHAPITRE 10 — MENTIONS SPÉCIALES

Les documents auxiliaires doivent être suivis dans l'écosystème documentaire, notamment :

* 04-DECISION-ENGINE-REFERENCE.md ;
* 13-CODEX-RULES.md ;
* 32-DEVELOPMENT-GOVERNANCE.md ;
* Plan_strategique_lancement.md ;
* IMPLEMENTATION-READINESS-REPORT.md ;
* MARKETING-TRACKING-CONSOLIDATION-REPORT.md ;
* OPERATIONAL-SALES-DOCUMENTS-REPORT.md ;
* Analyse __- marché immobilier camerounais_- groupe.md ;
* tout autre document d'analyse ou d'exploitation validé par LAWIM.

---

# CHAPITRE 11 — GEL DOCUMENTAIRE

Les documents de gel documentaire et de préparation V2 doivent être suivis comme références officielles complémentaires :

| Document | Rôle | Dépendances |
| --- | --- | --- |
| DOCUMENTATION-AUDIT-V1.md | Audit global du dossier Directive | 26, 27, 41-48 |
| LAWIM-DOCUMENTATION-V1.0.md | Socle documentaire figé | 00-48, plans, rapports, releases |
| CHANGELOG-V1.md | Historique officiel | 26, 31-48 |
| DOCUMENTATION-GOVERNANCE.md | Gouvernance documentaire | 26, 31-48 |
| DOCUMENTATION-STRUCTURE.md | Architecture documentaire | 26, 31-48 |
| LAWIM-BRAND-BOOK.md | Marque et communication | 00, 01, 19, 24, 25, 41, 48 |
| LAWIM-BUSINESS-PLAN.md | Business plan officiel | 00, 01, 19, 24, 25, 41, 48 |
| LAWIM-KNOWLEDGE-BASE-MASTER.md | Base de connaissances | 01, 03, 04, 18, 28, 30A, 30B, 30C, 30D |
| LAWIM-OPERATIONS-MANUAL.md | Manuel interne des opérations | 05, 06, 10, 11, 13, 15, 19, 22, 41 |
| LAWIM_V2_IMPLEMENTATION_READY.md | Préparation à l'implémentation | 26, 31, 32, 34, 37 |
| IMPLEMENTATION-MASTER-PLAN.md | Plan maître d'implémentation | 31, 32, 33, 34, 35, 36, 37, 38, 39, 40 |
| LAWIM-DOCUMENTATION-RELEASE-V1.0.md | Release documentaire officielle | 26, 27, 41-48, plans, rapports |
| LAWIM-DOCUMENTATION-V1.0-CERTIFICATION.md | Certification documentaire | 26, 27, release, audit, changelog |

---

# CHAPITRE 12 — OBJECTIF FINAL

L'index maître permet à LAWIM de retrouver immédiatement la documentation de référence, les dépendances critiques et la structure globale de gouvernance.

# FIN DU DOCUMENT
