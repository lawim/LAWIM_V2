# LAWIM

# LAWIM_V2_MASTER_IMPLEMENTATION_PLAN.md

# Plan directeur d'implémentation LAWIM_V2

Version 1.0

Date : 2026-06-27

---

# 1. Vision générale

## 1.1 Philosophie de développement

LAWIM_V2 doit être développé selon une logique contract-first, doc-first, data-first, test-first et security-first.

Les règles fondatrices sont les suivantes :

* la documentation LAWIM Documentation Version 1.0 reste la source de vérité ;
* aucun développement ne peut contredire les référentiels figés ;
* chaque sprint doit produire un incrément vérifiable ;
* chaque ticket doit être isolable ;
* toute décision sensible doit être validée par un humain ;
* toute évolution doit être traçable, testée et réversible.

## 1.2 Objectifs du programme

LAWIM_V2 doit permettre de construire une plateforme :

* cohérente ;
* industrialisable ;
* multilingue ;
* sécurisée ;
* mesurable ;
* migrable ;
* maintenable ;
* évolutive ;
* compatible avec le modèle économique sans commission immobilière.

## 1.3 Règles de gouvernance

Le développement doit respecter :

* la séparation stricte entre code, données, connaissance, migration, legacy et documentation ;
* la validation humaine sur les sujets métier, paiement, sécurité, conformité et IA ;
* la revue systématique avant merge ;
* les releases balisées ;
* l'absence de changement silencieux ;
* l'obligation de tests avant validation.

---

# 2. Architecture cible

| Bloc | Rôle | Dépendances principales | Priorité |
| --- | --- | --- | --- |
| Backend | Implémenter les services et contrats métier officiels, exposer les API, orchestrer les domaines. | Infra, DB, auth, sécurité, docs | P0 |
| Frontend | Consommer les API, afficher les parcours web, dashboards et vues d'administration. | API, auth, dashboard, tracking | P1 |
| Mobile | Offrir une expérience légère, synchronisée et multilingue. | API, auth, notifications, Campay | P2 |
| IA | Fournir assistance, résumé, détection de langue, recherche intelligente et suggestions. | Knowledge base, data, tracking, API | P2 |
| Base de données | Héberger les données métier, les historiques, les journaux et les agrégats. | Migration, sécurité, backup, API | P0 |
| Matching | Qualifier, scorer, classer et rapprocher les besoins et les biens. | Property, conversation, geo, pricing, tracking | P1 |
| Decision Engine | Prendre les décisions de workflow et de rematching selon les règles validées. | Matching, workflow, notifications | P1 |
| Conversation Engine | Gérer les échanges, l'historique, la qualification et les pièces jointes. | Auth, property, roles, notifications | P1 |
| Campay | Gérer le paiement, les webhooks, la réconciliation, les reçus et le reporting paiement. | Security, auth, notifications, reporting | P1 |
| Dashboard | Offrir la lecture opérationnelle, administrative et analytique. | Tracking, reporting, roles, API | P1 |
| Reporting | Calculer KPI, rapports, agrégats et exports périodiques. | DB, tracking, Campay, matching, conversation | P1 |
| Continuous Learning | Apprendre à partir des usages et proposer des améliorations validées. | Reporting, AI, tracking, knowledge | P2 |
| Tracking | Suivre campagnes, publications, redirections, leads, conversions et attribution. | DB, API, events, reporting, dashboard | P1 |
| Notifications | Diffuser les messages métier, opérationnels et de suivi. | Workflow, Campay, tracking, API | P1 |
| API | Exposer les contrats stables à tous les clients. | Backend, auth, DB, docs | P0 |
| Knowledge Base | Centraliser les connaissances marché, métier, juridique et IA. | Docs, migration, curation, AI | P1 |

---

# 3. Découpage officiel en sprints

## 3.1 Vue d'ensemble

| Sprint | Nom | Thème principal | Durée estimée |
| --- | --- | --- | --- |
| S001 | Bootstrap et contrat de dépôt | Socle de projet | 2 semaines |
| S002 | Infrastructure et environnements | Exécution locale et CI initiale | 2 semaines |
| S003 | Base de données et stockage | Schéma et persistance | 2 semaines |
| S004 | Authentification et identité | Accès et sessions | 2 semaines |
| S005 | Utilisateurs, rôles, organisations | Gouvernance des acteurs | 2 semaines |
| S006 | Cœur immobilier | Biens, attributs, prix | 2 semaines |
| S007 | Médias, documents, géolocalisation | Vérification et contexte | 2 semaines |
| S008 | Conversation Engine | Échanges et historique | 2 semaines |
| S009 | Matching foundation | Qualification et scoring | 2 semaines |
| S010 | Decision Engine et rematching | Arbitrage et requalification | 2 semaines |
| S011 | Workflows et visites | Orchestration métier | 2 semaines |
| S012 | Notifications | Diffusion et templates | 2 semaines |
| S013 | Tracking et attribution | Campagnes, publications, redirections | 2 semaines |
| S014 | Campay | Paiement, webhooks, réconciliation | 2 semaines |
| S015 | Dashboard foundation | Vues, KPI et pilotage | 2 semaines |
| S016 | Reporting foundation | Rapports, agrégats, exports | 2 semaines |
| S017 | Knowledge Base | Savoir métier et curation | 2 semaines |
| S018 | LAWIM AI | Assistance, langue, recherche | 2 semaines |
| S019 | Continuous Learning | Boucle d'amélioration | 2 semaines |
| S020 | Mobile foundation | App mobile, offline, sync | 2 semaines |
| S021 | Security hardening | Zero trust, audit, fraude | 2 semaines |
| S022 | Migration tooling | Préparation des flux de migration | 2 semaines |
| S023 | Migration execution | Reprises et validation | 2 semaines |
| S024 | Beta et production readiness | Stabilité et mise en production | 2 semaines |

## 3.2 Sprint catalogue détaillé

### Sprint S001 - Bootstrap et contrat de dépôt

Objectif : créer une base de travail propre, séparer les espaces de travail et aligner le dépôt sur la documentation figée.

Durée estimée : 2 semaines

Modules concernés : structure de dépôt, documentation, gouvernance, conventions de nommage.

Dépendances : aucune.

Livrables : arborescence initiale, conventions de dépôt, inventaire des sources officielles, journal de démarrage.

Risques : confusion entre source officielle et legacy, dérive de structure.

Critères d'acceptation : le projet est vide de code métier, les chemins sont stables, la documentation de référence est liée au projet.

Critères de sortie : le dépôt est prêt à recevoir les couches techniques sans ambiguïté.

Tickets :

* S001-T01 - Repository scaffold | objectif: établir la structure racine et les frontières du projet | description: créer les dossiers, conventions et points d'entrée de la livraison | docs: LAWIM_V2_BOOTSTRAP_REPORT.md, LAWIM-DOCUMENTATION-V1.0.md | composants: `code/`, `data/`, `tests/`, `prompts/`, `docs/` | dépendances: aucune | estimation: 1 jour | risque: faible | priorité: P0
* S001-T02 - Reference inventory | objectif: inventorier les documents sources de LAWIM V1.0 | description: produire la cartographie des documents, familles et dépendances | docs: 26-MASTER-INDEX.md, 27-TRACEABILITY-MATRIX.md, LAWIM-DOCUMENTATION-RELEASE-V1.0.md | composants: index, traçabilité, release | dépendances: S001-T01 | estimation: 1 jour | risque: faible | priorité: P0
* S001-T03 - Governance seed | objectif: installer les règles de travail initiales | description: poser les règles de revue, validation et gestion des changements | docs: DOCUMENTATION-GOVERNANCE.md, 32-DEVELOPMENT-GOVERNANCE.md, 33-CODEX-IMPLEMENTATION-RULES.md | composants: gouvernance, changelog, revues | dépendances: S001-T01, S001-T02 | estimation: 1 jour | risque: faible | priorité: P0

### Sprint S002 - Infrastructure et environnements

Objectif : disposer d'un environnement d'exécution local et reproductible.

Durée estimée : 2 semaines

Modules concernés : Docker, Nginx, environnements, monitoring, logs, secrets.

Dépendances : S001.

Livrables : environnement local, base de stack, conventions de secrets, premier pipeline.

Risques : configuration instable, divergence entre environnements.

Critères d'acceptation : la stack démarre de manière reproductible, les logs sont visibles.

Critères de sortie : l'équipe peut exécuter, observer et redémarrer l'environnement.

Tickets :

* S002-T01 - Docker baseline | objectif: poser la base conteneurisée du projet | description: définir les services de base et les fichiers de déploiement locaux | docs: 17-DEPLOYMENT-INFRASTRUCTURE-REFERENCE.md, 39-CI-CD-REFERENCE.md | composants: Docker, Nginx, environnements | dépendances: S001-T01 | estimation: 2 jours | risque: faible | priorité: P0
* S002-T02 - Runtime observability | objectif: exposer logs et health checks | description: rendre visibles l'état, les erreurs et les points de contrôle | docs: 22-OPERATIONS-RUNBOOK.md, 40-PRODUCTION-CHECKLIST.md | composants: monitoring, logs, checks | dépendances: S002-T01 | estimation: 2 jours | risque: faible | priorité: P0
* S002-T03 - CI skeleton | objectif: préparer le premier pipeline technique | description: créer les étapes minimales de build, lint et smoke test | docs: 37-QUALITY-ASSURANCE-PLAN.md, 39-CI-CD-REFERENCE.md | composants: CI, lint, build, smoke tests | dépendances: S002-T01 | estimation: 2 jours | risque: faible | priorité: P0

### Sprint S003 - Base de données et stockage

Objectif : installer la persistance, la structure initiale et les capacités de sauvegarde.

Durée estimée : 2 semaines

Modules concernés : PostgreSQL, Prisma, Redis, storage, sauvegardes, archivage.

Dépendances : S002.

Livrables : base initiale, schéma de démarrage, primitives de backup/restore.

Risques : corruption de schéma, mauvaise migration, restauration incomplète.

Critères d'acceptation : lecture/écriture fonctionnelles, sauvegarde vérifiée.

Critères de sortie : la persistance est stable et testable.

Tickets :

* S003-T01 - PostgreSQL foundation | objectif: créer le socle relationnel | description: définir l'instance, les connexions et les contraintes de base | docs: 06-DATABASE-REFERENCE.md, 14-STORAGE-REFERENCE.md | composants: PostgreSQL, schema, constraints | dépendances: S002-T03 | estimation: 2 jours | risque: moyen | priorité: P0
* S003-T02 - Prisma baseline | objectif: aligner les modèles de données sur la documentation | description: générer la première couche ORM et les conventions de migration | docs: 06-DATABASE-REFERENCE.md, 24-DEVELOPER-GUIDE.md | composants: Prisma, schema, migrations | dépendances: S003-T01 | estimation: 2 jours | risque: moyen | priorité: P0
* S003-T03 - Backup primitives | objectif: préparer les sauvegardes et restaurations de base | description: définir les mécanismes de snapshot, checksum et restauration | docs: 14-STORAGE-REFERENCE.md, 22-OPERATIONS-RUNBOOK.md | composants: backups, restore, checksums | dépendances: S003-T01 | estimation: 2 jours | risque: moyen | priorité: P0

### Sprint S004 - Authentification et identité

Objectif : sécuriser l'entrée dans le système et préparer les sessions.

Durée estimée : 2 semaines

Modules concernés : authentification, sessions, JWT, OAuth, MFA.

Dépendances : S003.

Livrables : login, logout, sessions, permissions techniques de base.

Risques : exposition d'accès, gestion faible des secrets.

Critères d'acceptation : l'accès est maîtrisé et les refus sont corrects.

Critères de sortie : les comptes peuvent être authentifiés de manière sûre.

Tickets :

* S004-T01 - Auth service | objectif: implémenter le service d'authentification | description: préparer login, logout et gestion de session | docs: 15-SECURITY-REFERENCE.md, 16-API-REFERENCE.md | composants: auth, sessions, tokens | dépendances: S003-T02 | estimation: 2 jours | risque: moyen | priorité: P0
* S004-T02 - Token strategy | objectif: définir les tokens et flux d'accès | description: cadrer JWT, refresh et gestion de session | docs: 15-SECURITY-REFERENCE.md, 24-DEVELOPER-GUIDE.md | composants: JWT, OAuth, session storage | dépendances: S004-T01 | estimation: 2 jours | risque: moyen | priorité: P0
* S004-T03 - MFA gate | objectif: durcir les accès sensibles | description: ajouter l'étape de validation additionnelle sur les flux critiques | docs: 15-SECURITY-REFERENCE.md, 40-PRODUCTION-CHECKLIST.md | composants: MFA, recovery, access policy | dépendances: S004-T02 | estimation: 2 jours | risque: moyen | priorité: P0

### Sprint S005 - Utilisateurs, rôles, organisations

Objectif : organiser les acteurs, les agences, les partenaires et les permissions.

Durée estimée : 2 semaines

Modules concernés : users, organizations, roles, permissions, profiles.

Dépendances : S004.

Livrables : modèle utilisateur, arborescence organisationnelle, matrice de rôles.

Risques : duplication des identités, incohérence des droits.

Critères d'acceptation : les rôles sont stables et les permissions cohérentes.

Critères de sortie : l'écosystème de comptes est gouvernable.

Tickets :

* S005-T01 - User lifecycle | objectif: gérer la création et la maintenance des comptes | description: définir les statuts, profils et transitions utilisateur | docs: 08-ROLE-REFERENCE.md, 06-DATABASE-REFERENCE.md | composants: users, profiles, statuses | dépendances: S004-T03 | estimation: 2 jours | risque: moyen | priorité: P0
* S005-T02 - Organization model | objectif: structurer agences, partenaires et équipes | description: poser l'arbre organisationnel et les rattachements | docs: 19-ADMINISTRATION-REFERENCE.md, 13-ARCHITECTURE-GOVERNANCE-REFERENCE.md | composants: organizations, agencies, partners, teams | dépendances: S005-T01 | estimation: 2 jours | risque: moyen | priorité: P0
* S005-T03 - Permissions matrix | objectif: traduire les rôles en droits applicables | description: aligner permissions, visibilité et accès aux ressources | docs: 08-ROLE-REFERENCE.md, 15-SECURITY-REFERENCE.md | composants: RBAC, ABAC, policy engine | dépendances: S005-T02 | estimation: 2 jours | risque: moyen | priorité: P0

### Sprint S006 - Coeur immobilier

Objectif : construire le socle des biens, attributs et prix.

Durée estimée : 2 semaines

Modules concernés : Property, pricing, attribut catalog, publication guardrails.

Dépendances : S003, S005.

Livrables : modèle bien, normalisation des attributs, règles de prix.

Risques : données incohérentes, confusion entre types de biens.

Critères d'acceptation : les biens sont décrits, classés et validés.

Critères de sortie : le moteur immobilier est exploitable pour la suite.

Tickets :

* S006-T01 - Property domain schema | objectif: définir la structure centrale des biens | description: implémenter les entités, statuts et relations du bien | docs: 02-PROPERTY-REFERENCE.md, 02H-ATTRIBUTE-CATALOG.md | composants: property, attributes, statuses | dépendances: S003-T02, S005-T03 | estimation: 2 jours | risque: moyen | priorité: P0
* S006-T02 - Pricing alignment | objectif: aligner les prix, loyers et cautions | description: préparer les règles de saisie et de variation | docs: 02I-PRICING-REFERENCE.md, 11-REPORTING-REFERENCE.md | composants: pricing, currencies, ranges | dépendances: S006-T01 | estimation: 2 jours | risque: moyen | priorité: P0
* S006-T03 - Publication guardrails | objectif: empêcher les publications incohérentes | description: définir les contrôles pré-publication et les statuts | docs: 05-WORKFLOW-REFERENCE.md, 12-TESTS-REFERENCE.md | composants: publication guards, validation rules | dépendances: S006-T01, S006-T02 | estimation: 2 jours | risque: moyen | priorité: P0

### Sprint S007 - Médias, documents, géolocalisation

Objectif : associer les médias, les preuves et le contexte géographique aux biens.

Durée estimée : 2 semaines

Modules concernés : media, documents, geo, addresses, zoning.

Dépendances : S006.

Livrables : pipeline média, preuve documentaire, géolocalisation utile.

Risques : médias trompeurs, localisation inexacte.

Critères d'acceptation : les photos, documents et zones sont rattachés correctement.

Critères de sortie : les biens sont contextualisés et vérifiables.

Tickets :

* S007-T01 - Media pipeline | objectif: gérer photos et vidéos des biens | description: définir ingestion, stockage et association média | docs: 14-STORAGE-REFERENCE.md, 21-UX-UI-DESIGN-SYSTEM.md | composants: media storage, thumbnails, attachments | dépendances: S006-T03 | estimation: 2 jours | risque: moyen | priorité: P1
* S007-T02 - Document pipeline | objectif: gérer les pièces et preuves liées aux biens | description: standardiser les documents acceptés et leur statut | docs: 43-PROPERTY-VERIFICATION-PROCEDURE.md, 15-SECURITY-REFERENCE.md | composants: documents, verification, archives | dépendances: S007-T01 | estimation: 2 jours | risque: moyen | priorité: P1
* S007-T03 - Geo integration | objectif: relier le bien à sa localisation réelle | description: intégrer villes, quartiers, zones et coordonnées | docs: 09-GEOLOCATION-REFERENCE.md, 27-TRACEABILITY-MATRIX.md | composants: geo, city, neighborhood, zone | dépendances: S007-T02 | estimation: 2 jours | risque: moyen | priorité: P1

### Sprint S008 - Conversation Engine

Objectif : permettre les échanges traçables entre utilisateurs et partenaires.

Durée estimée : 2 semaines

Modules concernés : Conversation Engine, chat, messages, attachments, history.

Dépendances : S005, S006, S007.

Livrables : conversation de base, historique, pièces jointes.

Risques : spam, perte de contexte, conversations orphelines.

Critères d'acceptation : une conversation peut être ouverte, suivie et archivée.

Critères de sortie : les échanges servent de base au matching et au support.

Tickets :

* S008-T01 - Conversation model | objectif: poser la structure de conversation | description: définir threads, participants et statuts | docs: 03-CONVERSATION-REFERENCE.md, 06-DATABASE-REFERENCE.md | composants: conversations, threads, participants | dépendances: S005-T01, S006-T03 | estimation: 2 jours | risque: moyen | priorité: P1
* S008-T02 - Messaging flow | objectif: gérer l'envoi et la réception des messages | description: brancher le flux de messages et les états de lecture | docs: 03-CONVERSATION-REFERENCE.md, 10-NOTIFICATION-REFERENCE.md | composants: messages, read states, delivery | dépendances: S008-T01 | estimation: 2 jours | risque: moyen | priorité: P1
* S008-T03 - Attachments and history | objectif: conserver les pièces jointes et l'historique | description: tracer les échanges et les fichiers liés | docs: 14-STORAGE-REFERENCE.md, 12-TESTS-REFERENCE.md | composants: attachments, history, audit trail | dépendances: S008-T02 | estimation: 2 jours | risque: moyen | priorité: P1

### Sprint S009 - Matching foundation

Objectif : construire la qualification et le classement des besoins.

Durée estimée : 2 semaines

Modules concernés : Matching, qualification, scoring, ranking, search.

Dépendances : S006, S007, S008.

Livrables : recherche initiale, scoring, règles de qualification.

Risques : faux positifs, faux négatifs, biais de score.

Critères d'acceptation : les correspondances restent cohérentes et explicables.

Critères de sortie : le moteur peut proposer des rapprochements utiles.

Tickets :

* S009-T01 - Search and ranking | objectif: établir la recherche et le classement | description: implémenter les critères de tri et de pertinence | docs: 04-MATCHING-REFERENCE.md, 02I-PRICING-REFERENCE.md | composants: search, ranking, filters | dépendances: S006-T01, S007-T03 | estimation: 2 jours | risque: moyen | priorité: P1
* S009-T02 - Qualification and scoring | objectif: qualifier les besoins et noter les correspondances | description: traduire les règles métier en scores exploitables | docs: 04-MATCHING-REFERENCE.md, 03-CONVERSATION-REFERENCE.md | composants: qualification, scoring, rules | dépendances: S009-T01 | estimation: 2 jours | risque: moyen | priorité: P1
* S009-T03 - Availability and preferences | objectif: tenir compte de la disponibilité et des préférences | description: filtrer par contexte, langue, zone et disponibilité | docs: 04-MATCHING-REFERENCE.md, 09-GEOLOCATION-REFERENCE.md | composants: availability, preferences, filters | dépendances: S009-T02 | estimation: 2 jours | risque: moyen | priorité: P1

### Sprint S010 - Decision Engine et rematching

Objectif : arbitrer les décisions et relancer le matching quand nécessaire.

Durée estimée : 2 semaines

Modules concernés : Decision Engine, rematching, recommendation, explainability.

Dépendances : S008, S009.

Livrables : règles de décision, rematching, motifs d'exclusion.

Risques : décision opaque, boucles de relance, incohérence métier.

Critères d'acceptation : les décisions sont justifiables et réversibles.

Critères de sortie : la chaîne de décision est opérationnelle.

Tickets :

* S010-T01 - Decision orchestration | objectif: exécuter les règles de décision métier | description: connecter le matching aux étapes de décision | docs: 04-DECISION-ENGINE-REFERENCE.md, 05-WORKFLOW-REFERENCE.md | composants: decision rules, orchestrator | dépendances: S009-T02 | estimation: 2 jours | risque: moyen | priorité: P1
* S010-T02 - Rematching flow | objectif: relancer le matching quand le contexte change | description: gérer les rejets, changements et nouvelles suggestions | docs: 04-DECISION-ENGINE-REFERENCE.md, 12-TESTS-REFERENCE.md | composants: rematching, retry logic | dépendances: S010-T01 | estimation: 2 jours | risque: moyen | priorité: P1
* S010-T03 - Recommendation trace | objectif: rendre les recommandations explicables | description: conserver les raisons de décision et de suggestion | docs: 04-DECISION-ENGINE-REFERENCE.md, 27-TRACEABILITY-MATRIX.md | composants: explanation trail, recommendation metadata | dépendances: S010-T02 | estimation: 2 jours | risque: moyen | priorité: P1

### Sprint S011 - Workflows, visites, notifications

Objectif : orchestrer les étapes métier, les visites et les événements.

Durée estimée : 2 semaines

Modules concernés : Workflow Engine, visits, notifications, events.

Dépendances : S008, S010.

Livrables : orchestration de workflow, visite, notifications métier.

Risques : séquence cassée, notifications mal déclenchées.

Critères d'acceptation : les événements métier sont déclenchés au bon moment.

Critères de sortie : les workflows clés sont pilotables.

Tickets :

* S011-T01 - Workflow orchestration | objectif: lier les étapes métier en séquence | description: implémenter l'état des workflows et les transitions | docs: 05-WORKFLOW-REFERENCE.md, 13-ARCHITECTURE-GOVERNANCE-REFERENCE.md | composants: workflow states, transitions | dépendances: S010-T01 | estimation: 2 jours | risque: moyen | priorité: P1
* S011-T02 - Visits and follow-up | objectif: gérer les visites et le suivi | description: brancher la prise de rendez-vous, le suivi et les statuts | docs: 05-WORKFLOW-REFERENCE.md, 44-COMPLAINTS-AND-DISPUTES-PROCEDURE.md | composants: visits, scheduling, follow-up | dépendances: S011-T01 | estimation: 2 jours | risque: moyen | priorité: P1
* S011-T03 - Event markers | objectif: marquer les événements de workflow | description: préparer les hooks de notification et de reporting | docs: 05-WORKFLOW-REFERENCE.md, 27-TRACEABILITY-MATRIX.md | composants: events, hooks, markers | dépendances: S011-T02 | estimation: 2 jours | risque: moyen | priorité: P1

### Sprint S012 - Notifications

Objectif : diffuser les messages au bon moment et par le bon canal.

Durée estimée : 2 semaines

Modules concernés : Notification Engine, templates, channels, preferences.

Dépendances : S011, S004.

Livrables : notifications in-app, email, SMS, WhatsApp, Telegram.

Risques : bruit, doublons, mauvaise priorité.

Critères d'acceptation : la notification est fiable, tracée et conforme.

Critères de sortie : les canaux officiels sont fonctionnels.

Tickets :

* S012-T01 - Notification model | objectif: structurer les notifications et leur trace | description: définir le schéma, les statuts et les origines | docs: 10-NOTIFICATION-REFERENCE.md, 06-DATABASE-REFERENCE.md | composants: notifications, delivery states | dépendances: S011-T03 | estimation: 2 jours | risque: moyen | priorité: P1
* S012-T02 - Channel adapters | objectif: brancher les canaux officiels | description: préparer les connecteurs e-mail, SMS, WhatsApp et Telegram | docs: 10-NOTIFICATION-REFERENCE.md, 29-CAMPAY-PAYMENT-REFERENCE.md | composants: email, sms, WhatsApp, Telegram | dépendances: S012-T01 | estimation: 2 jours | risque: moyen | priorité: P1
* S012-T03 - Templates and preferences | objectif: centraliser les gabarits et préférences | description: gérer la langue active, les modèles et les priorités | docs: 10-NOTIFICATION-REFERENCE.md, 30-I18N-L10N-REFERENCE.md | composants: templates, preferences, localization | dépendances: S012-T02 | estimation: 2 jours | risque: moyen | priorité: P1

### Sprint S013 - Tracking et attribution

Objectif : rendre la traçabilité marketing transverse et immuable.

Durée estimée : 2 semaines

Modules concernés : Tracking, campaigns, publications, redirects, attribution.

Dépendances : S005, S006, S011.

Livrables : tracking code, campagnes, publications, redirections, attribution.

Risques : dérive d'attribution, doublons, code recalculé par erreur.

Critères d'acceptation : chaque clic et chaque conversion restent traçables.

Critères de sortie : le tracking devient une source transverse partagée.

Tickets :

* S013-T01 - Tracking code generator | objectif: générer un code stable et unique | description: formaliser la logique d'identifiant de traçabilité immuable | docs: MARKETING-TRACKING-CONSOLIDATION-REPORT.md, 06-DATABASE-REFERENCE.md | composants: tracking code, uniqueness, sequencing | dépendances: S005-T01, S006-T03 | estimation: 2 jours | risque: élevé | priorité: P1
* S013-T02 - Campaign and publication model | objectif: poser campagnes et publications marketing | description: représenter les campagnes, canaux, acteurs et biens | docs: 06-DATABASE-REFERENCE.md, 07-DASHBOARD-REFERENCE.md | composants: campaigns, publications, actors, channels | dépendances: S013-T01 | estimation: 2 jours | risque: élevé | priorité: P1
* S013-T03 - Redirect logging and attribution | objectif: enregistrer les redirections et les attributions | description: loguer les clics, sessions et conversions associées | docs: 27-TRACEABILITY-MATRIX.md, 11-REPORTING-REFERENCE.md | composants: redirects, attribution, analytics events | dépendances: S013-T02 | estimation: 2 jours | risque: élevé | priorité: P1

### Sprint S014 - Campay

Objectif : intégrer les paiements, les webhooks et la réconciliation.

Durée estimée : 2 semaines

Modules concernés : Campay, payments, webhooks, receipts, reconciliation.

Dépendances : S004, S011, S012, S013.

Livrables : sandbox paiement, webhooks, reçus, rapprochement.

Risques : doublons, faux positifs, divergence de statut.

Critères d'acceptation : la transaction est confirmée, tracée et réconciliée.

Critères de sortie : les paiements opérationnels peuvent être suivis.

Tickets :

* S014-T01 - Sandbox integration | objectif: connecter Campay en environnement de test | description: préparer les appels, statuts et retours de sandbox | docs: 29-CAMPAY-PAYMENT-REFERENCE.md, 15-SECURITY-REFERENCE.md | composants: Campay sandbox, payments | dépendances: S004-T01 | estimation: 2 jours | risque: élevé | priorité: P1
* S014-T02 - Webhook integrity | objectif: sécuriser les retours de paiement | description: gérer signature, idempotence et contrôle de cohérence | docs: 29-CAMPAY-PAYMENT-REFERENCE.md, 16-API-REFERENCE.md | composants: webhooks, signature, idempotence | dépendances: S014-T01 | estimation: 2 jours | risque: élevé | priorité: P1
* S014-T03 - Reconciliation and receipts | objectif: gérer le rapprochement et les reçus | description: aligner paiement, reporting et suivi comptable | docs: 11-REPORTING-REFERENCE.md, 29-CAMPAY-PAYMENT-REFERENCE.md | composants: reconciliation, receipts, finance trail | dépendances: S014-T02 | estimation: 2 jours | risque: élevé | priorité: P1

### Sprint S015 - Dashboard foundation

Objectif : fournir les vues de pilotage essentielles.

Durée estimée : 2 semaines

Modules concernés : Dashboard Engine, admin views, KPI cards, role-based views.

Dépendances : S013, S014.

Livrables : shell de dashboard, vues admin, cartes KPI.

Risques : surcharge visuelle, incohérence entre rôles.

Critères d'acceptation : les tableaux de bord affichent des données cohérentes.

Critères de sortie : les écrans de pilotage sont prêts à recevoir les métriques.

Tickets :

* S015-T01 - Dashboard shell | objectif: créer le cadre visuel de pilotage | description: poser la navigation, les cartes et les zones de contenu | docs: 07-DASHBOARD-REFERENCE.md, 21-UX-UI-DESIGN-SYSTEM.md | composants: dashboard shell, layout, cards | dépendances: S013-T03 | estimation: 2 jours | risque: moyen | priorité: P1
* S015-T02 - Admin views | objectif: afficher les métriques administratives | description: exposer campagnes, publications, clics et conversions | docs: 07-DASHBOARD-REFERENCE.md, 19-ADMINISTRATION-REFERENCE.md | composants: admin dashboard, metrics, filters | dépendances: S015-T01 | estimation: 2 jours | risque: moyen | priorité: P1
* S015-T03 - Role-based views | objectif: adapter les vues selon les rôles | description: filtrer la visibilité des sections selon les permissions | docs: 08-ROLE-REFERENCE.md, 07-DASHBOARD-REFERENCE.md | composants: role views, visibility rules | dépendances: S015-T02 | estimation: 2 jours | risque: moyen | priorité: P1

### Sprint S016 - Reporting foundation

Objectif : produire les premiers agrégats et rapports périodiques.

Durée estimée : 2 semaines

Modules concernés : Reporting Engine, aggregates, exports, KPI catalog.

Dépendances : S013, S014, S015.

Livrables : rapports, KPI, exports programmés.

Risques : chiffres incohérents, agrégats incomplets.

Critères d'acceptation : les rapports reflètent les mêmes données que les dashboards.

Critères de sortie : la couche reporting est exploitable et stable.

Tickets :

* S016-T01 - Reporting engine | objectif: calculer les agrégats métier | description: brancher les sources et les calculs périodiques | docs: 11-REPORTING-REFERENCE.md, 06-DATABASE-REFERENCE.md | composants: reporting, aggregates, jobs | dépendances: S013-T03, S014-T03 | estimation: 2 jours | risque: moyen | priorité: P1
* S016-T02 - Periodic reports | objectif: produire les rapports récurrents | description: générer quotidien, hebdo, mensuel et trimestriel | docs: 11-REPORTING-REFERENCE.md, MARKETING-TRACKING-CONSOLIDATION-REPORT.md | composants: scheduled reports, exports | dépendances: S016-T01 | estimation: 2 jours | risque: moyen | priorité: P1
* S016-T03 - KPI catalog | objectif: figer les indicateurs suivis | description: lister les KPI, définitions et sources | docs: 11-REPORTING-REFERENCE.md, 32-FINAL-CERTIFICATION-REPORT.md | composants: KPI catalog, definitions, metadata | dépendances: S016-T02 | estimation: 2 jours | risque: moyen | priorité: P1

### Sprint S017 - Knowledge Base

Objectif : structurer la connaissance métier et les contenus utiles à l'IA.

Durée estimée : 2 semaines

Modules concernés : Knowledge Base, glossary sync, FAQ, legal, market, business.

Dépendances : S006, S008, S013, S016.

Livrables : taxonomie connaissance, ingestion, curation.

Risques : qualité inégale, redondance, contenus non validés.

Critères d'acceptation : la connaissance est versionnée et reliée à ses sources.

Critères de sortie : la base peut alimenter l'IA et le support.

Tickets :

* S017-T01 - Knowledge taxonomy | objectif: définir les catégories de savoir | description: structurer marché, quartiers, droit, FAQ, business, prompts | docs: LAWIM-KNOWLEDGE-BASE-MASTER.md, 30A-BUSINESS-DICTIONARY-REFERENCE.md | composants: taxonomy, categories, tags | dépendances: S006-T01 | estimation: 2 jours | risque: moyen | priorité: P1
* S017-T02 - Ingestion and curation | objectif: alimenter la base de connaissances | description: définir la collecte, la validation et la version | docs: DOCUMENTATION-GOVERNANCE.md, LAWIM-KNOWLEDGE-BASE-MASTER.md | composants: ingestion, curation, versioning | dépendances: S017-T01 | estimation: 2 jours | risque: moyen | priorité: P1
* S017-T03 - FAQ and business content | objectif: préparer les contenus opérationnels | description: intégrer FAQ, guides, dossiers métier et cas terrain | docs: 41-OPERATIONAL-PROCEDURES.md, 48-LAWIM-SALES-PLAYBOOK.md | composants: FAQ, guides, business content | dépendances: S017-T02 | estimation: 2 jours | risque: moyen | priorité: P1

### Sprint S018 - LAWIM AI

Objectif : brancher l'assistance IA sur les données, la langue et la connaissance.

Durée estimée : 2 semaines

Modules concernés : LAWIM AI, language detection, search, summarization.

Dépendances : S017, S013, S016.

Livrables : réponses assistées, détection de langue, recherche intelligente.

Risques : hallucinations, mauvaise langue, sur-automatisation.

Critères d'acceptation : l'IA répond dans la langue attendue et cite ses sources.

Critères de sortie : l'assistance IA est utilisable sans décision autonome sensible.

Tickets :

* S018-T01 - AI service scaffold | objectif: poser la structure d'assistance IA | description: préparer les services de base et les contrats d'appel | docs: 18-LAWIM-AI-REFERENCE.md, LAWIM-KNOWLEDGE-BASE-MASTER.md | composants: AI service, prompt routing | dépendances: S017-T02 | estimation: 2 jours | risque: élevé | priorité: P2
* S018-T02 - Language and search intelligence | objectif: comprendre la langue et la requête | description: brancher détection de langue, synonymes et recherche intelligente | docs: 30C-LANGUAGE-DETECTION-REFERENCE.md, 30D-MULTILINGUAL-SEARCH-REFERENCE.md | composants: language detection, semantic search | dépendances: S018-T01 | estimation: 2 jours | risque: élevé | priorité: P2
* S018-T03 - Source-grounded responses | objectif: produire des réponses fondées sur les référentiels | description: limiter les réponses aux données validées et traçables | docs: 18-LAWIM-AI-REFERENCE.md, 27-TRACEABILITY-MATRIX.md | composants: answer generation, citation trail | dépendances: S018-T02 | estimation: 2 jours | risque: élevé | priorité: P2

### Sprint S019 - Continuous Learning

Objectif : organiser la boucle d'amélioration avec validation humaine.

Durée estimée : 2 semaines

Modules concernés : Continuous Learning, feedback, validation, versioning.

Dépendances : S016, S017, S018.

Livrables : boucle mensuelle, suggestions, validation humaine.

Risques : auto-optimisation non contrôlée, biais, dérive métier.

Critères d'acceptation : aucune amélioration sensible n'est appliquée sans validation.

Critères de sortie : le cycle d'apprentissage est exploitable et gouverné.

Tickets :

* S019-T01 - Feedback loop | objectif: collecter les signaux utiles | description: capter retours, performances et événements d'apprentissage | docs: 28-CONTINUOUS-LEARNING-REFERENCE.md, 11-REPORTING-REFERENCE.md | composants: feedback, trend capture, metrics | dépendances: S016-T03 | estimation: 2 jours | risque: moyen | priorité: P2
* S019-T02 - Human validation gate | objectif: exiger une validation humaine | description: bloquer toute application automatique sensible | docs: DOCUMENTATION-GOVERNANCE.md, 28-CONTINUOUS-LEARNING-REFERENCE.md | composants: review gate, approvals | dépendances: S019-T01 | estimation: 2 jours | risque: moyen | priorité: P2
* S019-T03 - Versioned recommendations | objectif: versionner les recommandations | description: historiser les propositions et les retours | docs: 28-CONTINUOUS-LEARNING-REFERENCE.md, LAWIM-DOCUMENTATION-V1.0.md | composants: recommendation versioning, rollback | dépendances: S019-T02 | estimation: 2 jours | risque: moyen | priorité: P2

### Sprint S020 - Mobile foundation

Objectif : préparer une application mobile légère et synchronisée.

Durée estimée : 2 semaines

Modules concernés : Mobile, offline cache, sync, push notifications, payment handoff.

Dépendances : S004, S012, S014, S015, S016.

Livrables : shell mobile, cache local, synchronisation, notifications push.

Risques : fragmentation device, latence, incohérence offline/online.

Critères d'acceptation : l'application fonctionne en mode connecté et déconnecté.

Critères de sortie : la base mobile est prête pour l'expérience métier.

Tickets :

* S020-T01 - Mobile shell | objectif: créer le cadre applicatif mobile | description: poser navigation, thèmes et architecture cliente | docs: 20-MOBILE-REFERENCE.md, 21-UX-UI-DESIGN-SYSTEM.md | composants: mobile shell, navigation, UI kit | dépendances: S004-T03 | estimation: 2 jours | risque: moyen | priorité: P2
* S020-T02 - Offline sync | objectif: gérer la synchronisation locale | description: préparer cache local et récupération des données | docs: 20-MOBILE-REFERENCE.md, 06-DATABASE-REFERENCE.md | composants: offline cache, sync engine | dépendances: S020-T01 | estimation: 2 jours | risque: moyen | priorité: P2
* S020-T03 - Push and payment handoff | objectif: brancher notifications push et parcours de paiement | description: relayer les alertes et redirections de paiement | docs: 20-MOBILE-REFERENCE.md, 29-CAMPAY-PAYMENT-REFERENCE.md | composants: push, mobile payment flow | dépendances: S020-T02 | estimation: 2 jours | risque: moyen | priorité: P2

### Sprint S021 - Security hardening

Objectif : renforcer la sécurité, l'audit et la détection de fraude.

Durée estimée : 2 semaines

Modules concernés : Security Engine, privacy, audit, fraud controls.

Dépendances : S004, S014, S018, S020.

Livrables : durcissement des accès, logs d'audit, contrôles fraude.

Risques : faux positifs, trop de friction, surface d'attaque résiduelle.

Critères d'acceptation : les contrôles critiques sont en place et testés.

Critères de sortie : la plateforme est apte à l'audit de préproduction.

Tickets :

* S021-T01 - Zero trust hardening | objectif: durcir l'accès et les privilèges | description: aligner auth, rôles et segmentation | docs: 15-SECURITY-REFERENCE.md, 08-ROLE-REFERENCE.md | composants: zero trust, policies, segmentation | dépendances: S004-T03, S005-T03 | estimation: 2 jours | risque: élevé | priorité: P1
* S021-T02 - Audit and privacy | objectif: tracer et protéger les données sensibles | description: consolider logs, niveaux de sensibilité et rétention | docs: 15-SECURITY-REFERENCE.md, 06-DATABASE-REFERENCE.md | composants: audit logs, privacy controls, retention | dépendances: S021-T01 | estimation: 2 jours | risque: élevé | priorité: P1
* S021-T03 - Fraud controls | objectif: mettre en place les garde-fous anti-fraude | description: surveiller signaux, anomalies et abus | docs: 46-FRAUD-MANAGEMENT-PROCEDURE.md, 47-PARTNER-SUSPENSION-PROCEDURE.md | composants: fraud controls, alerts, suspensions | dépendances: S021-T02 | estimation: 2 jours | risque: élevé | priorité: P1

### Sprint S022 - Migration tooling

Objectif : préparer l'extraction et la transformation des données utiles de l'ancien LAWIM.

Durée estimée : 2 semaines

Modules concernés : migration scripts, mappings, staging, validation.

Dépendances : S003, S006, S007, S017, S021.

Livrables : inventaire source, mapping, staging, checks de validation.

Risques : données hétérogènes, qualité source faible, pertes pendant transformation.

Critères d'acceptation : chaque objet migrable a un mapping et un contrôle.

Critères de sortie : la migration peut être répétée à blanc.

Tickets :

* S022-T01 - Source inventory | objectif: inventorier les données migrables | description: lister utilisateurs, biens, médias, partenaires, stats et historiques | docs: LAWIM_V2_BOOTSTRAP_REPORT.md, DOCUMENTATION-AUDIT-V1.md | composants: inventory, source catalog | dépendances: S003-T01, S017-T01 | estimation: 2 jours | risque: élevé | priorité: P1
* S022-T02 - Mapping and transformation | objectif: cartographier les champs et transformations | description: définir les règles de transfert vers LAWIM_V2 | docs: 35-MIGRATION-PLAN.md, 27-TRACEABILITY-MATRIX.md | composants: mappings, transformations, staging | dépendances: S022-T01 | estimation: 2 jours | risque: élevé | priorité: P1
* S022-T03 - Validation rehearsal | objectif: préparer les essais de migration | description: construire le cadre de validation et de contrôle | docs: 35-MIGRATION-PLAN.md, LAWIM_V2_BOOTSTRAP_REPORT.md | composants: rehearsal, validation, checksums | dépendances: S022-T02 | estimation: 2 jours | risque: élevé | priorité: P1

### Sprint S023 - Migration execution

Objectif : exécuter les migrations préparées et valider les reconcilations.

Durée estimée : 2 semaines

Modules concernés : users migration, property migration, partner migration, media migration, stats migration, knowledge migration.

Dépendances : S022.

Livrables : données reprises, historiques alignés, écarts traités.

Risques : perte de données, divergence de comptes, doublons.

Critères d'acceptation : les volumes et échantillons concordent avec les sources.

Critères de sortie : la migration est réconciliée et documentée.

Tickets :

* S023-T01 - Users and partners migration | objectif: migrer les comptes utiles | description: reprendre les utilisateurs, partenaires et organisations | docs: 35-MIGRATION-PLAN.md, 06-DATABASE-REFERENCE.md | composants: users, partners, organizations | dépendances: S022-T03 | estimation: 2 jours | risque: élevé | priorité: P1
* S023-T02 - Property and media migration | objectif: migrer biens, médias et documents | description: transférer les annonces, photos, vidéos et preuves | docs: 35-MIGRATION-PLAN.md, 43-PROPERTY-VERIFICATION-PROCEDURE.md | composants: property, media, documents | dépendances: S023-T01 | estimation: 2 jours | risque: élevé | priorité: P1
* S023-T03 - Stats and history migration | objectif: migrer les statistiques et historiques utiles | description: reprendre les agrégats, événements et bases de reporting | docs: 11-REPORTING-REFERENCE.md, 28-CONTINUOUS-LEARNING-REFERENCE.md | composants: stats, history, analytics, knowledge | dépendances: S023-T02 | estimation: 2 jours | risque: élevé | priorité: P1

### Sprint S024 - Beta et production readiness

Objectif : stabiliser, tester et préparer la mise en production.

Durée estimée : 2 semaines

Modules concernés : QA, performance, regression, release readiness, cutover, support.

Dépendances : S023.

Livrables : beta interne, beta privée, release candidate, checklist de production.

Risques : régression tardive, performance insuffisante, bug bloquant.

Critères d'acceptation : la version candidate passe les tests et la revue finale.

Critères de sortie : le projet est prêt pour le lancement contrôlé.

Tickets :

* S024-T01 - Internal beta QA | objectif: valider l'expérience interne | description: exécuter les scénarios de bout en bout avec les équipes | docs: 12-TESTS-REFERENCE.md, 37-QUALITY-ASSURANCE-PLAN.md | composants: QA, user journeys, internal feedback | dépendances: S023-T03 | estimation: 2 jours | risque: moyen | priorité: P1
* S024-T02 - Performance and regression | objectif: contrôler la stabilité et les performances | description: lancer les tests de charge, de non-régression et de robustesse | docs: 12-TESTS-REFERENCE.md, 40-PRODUCTION-CHECKLIST.md | composants: performance, regression, stability | dépendances: S024-T01 | estimation: 2 jours | risque: élevé | priorité: P1
* S024-T03 - Release candidate and go-live | objectif: préparer la version candidate et la mise en production | description: finaliser la checklist, les retours et le plan de rollback | docs: LAWIM-DOCUMENTATION-RELEASE-V1.0.md, LAWIM_V2_BOOTSTRAP_REPORT.md | composants: release candidate, cutover, rollback | dépendances: S024-T02 | estimation: 2 jours | risque: élevé | priorité: P0

---

# 4. Dépendances

## 4.1 Dépendances sprint vers sprint

La règle générale est séquentielle :

* S002 dépend de S001 ;
* S003 dépend de S002 ;
* S004 dépend de S003 ;
* S005 dépend de S004 ;
* S006 dépend de S005 et S003 ;
* S007 dépend de S006 ;
* S008 dépend de S005, S006 et S007 ;
* S009 dépend de S006, S007 et S008 ;
* S010 dépend de S009 ;
* S011 dépend de S010 et S008 ;
* S012 dépend de S011 et S004 ;
* S013 dépend de S011 et S006 ;
* S014 dépend de S004, S011, S012 et S013 ;
* S015 dépend de S013 et S014 ;
* S016 dépend de S013, S014 et S015 ;
* S017 dépend de S006, S008, S013 et S016 ;
* S018 dépend de S017 et S016 ;
* S019 dépend de S016, S017 et S018 ;
* S020 dépend de S004, S012, S014, S015 et S016 ;
* S021 dépend de S004, S014, S018 et S020 ;
* S022 dépend de S003, S006, S007, S017 et S021 ;
* S023 dépend de S022 ;
* S024 dépend de S023.

## 4.2 Dépendances ticket vers ticket

Les tickets d'un sprint suivent la logique :

* T01 ouvre le sprint ;
* T02 dépend de T01 ;
* T03 dépend de T02 ;
* les tickets critiques transverses ne peuvent démarrer qu'après les tickets qui fournissent leurs données, leurs contrats ou leurs règles.

## 4.3 Dépendances module vers module

| Module source | Module cible | Nature de la dépendance |
| --- | --- | --- |
| Base de données | API | Les API consomment les données et les contrats persistants. |
| API | Frontend | Le frontend consomme les contrats API. |
| API | Mobile | Le mobile consomme les contrats API. |
| Knowledge Base | IA | L'IA exploite le savoir curé et validé. |
| Tracking | Dashboard | Le dashboard lit les événements et agrégats de tracking. |
| Tracking | Reporting | Le reporting agrège les événements de tracking. |
| Campay | Reporting | Le reporting financier dépend des confirmations Campay. |
| Matching | Decision Engine | La décision consomme les résultats de matching. |
| Conversation | Matching | La conversation enrichit la qualification et le rapprochement. |
| Backend | Mobile | Le mobile consomme les services backend. |
| Backend | Frontend | Le frontend consomme les services backend. |
| Continuous Learning | Knowledge Base | L'apprentissage réutilise le savoir et les retours curés. |

---

# 5. Critères de validation

## 5.1 Validation technique

* build vert ;
* lint vert ;
* tests unitaires et d'intégration verts ;
* absence de régression critique ;
* logs et monitoring en place.

## 5.2 Validation fonctionnelle

* scénario métier validé ;
* comportement conforme aux référentiels ;
* statuts cohérents ;
* transitions attendues ;
* cas d'erreur gérés.

## 5.3 Validation documentaire

* document de référence mis à jour ;
* ticket relié aux bonnes sources ;
* dépendances listées ;
* matrice de traçabilité cohérente.

## 5.4 Validation sécurité

* accès autorisés seulement ;
* secrets protégés ;
* journaux d'audit actifs ;
* contrôles d'entrée et de sortie ;
* aucun contournement de sécurité.

## 5.5 Validation métier

* le produit owner ou le validateur métier accepte ;
* le modèle économique reste inchangé ;
* aucune commission immobilière n'est introduite ;
* les règles de service sont respectées.

## 5.6 Validation UX

* parcours lisible ;
* feedback clair ;
* cohérence visuelle ;
* accessibilité de base ;
* adaptation mobile.

## 5.7 Validation performance

* temps de réponse acceptable ;
* charge supportable ;
* stabilité sous usage normal ;
* démarrage et rafraîchissement corrects.

## 5.8 Validation conformité

* conformité documentaire ;
* conformité données ;
* conformité paiement ;
* conformité confidentialité ;
* conformité des messages utilisateurs.

---

# 6. Stratégie de tests

| Type de test | Quand | Objectif | Gate |
| --- | --- | --- | --- |
| Unitaires | Pendant chaque ticket | Valider la logique isolée. | Avant merge du ticket. |
| Intégration | Fin de ticket et fin de sprint | Valider les interactions entre composants. | Avant fermeture du sprint. |
| API | Chaque changement de contrat | Valider entrées, sorties et erreurs. | Avant merge et avant release. |
| UI | Chaque évolution d'écran | Valider les parcours et le rendu. | Avant merge frontend/mobile. |
| Performance | Fin des sprints clés et avant beta | Vérifier les temps et la charge. | Avant beta et release candidate. |
| Sécurité | En continu et avant release | Contrôler l'exposition, les accès et les données sensibles. | Avant release et production. |
| Régression | Chaque merge vers develop/release | Empêcher les cassures fonctionnelles. | Avant merge et avant tag. |
| Migration | Sprints 22 et 23 | Vérifier la reprise et la cohérence des données. | Avant cutover. |
| IA | Sprints 18 et 19 | Tester la qualité des réponses et l'absence d'automatisation sensible. | Avant exposition interne. |
| Matching | Sprints 9 et 10 | Vérifier les scores, les règles et les rematchs. | Avant beta et release. |
| Campay | Sprints 14 et 16 | Vérifier paiement, webhooks et réconciliation. | Avant staging et production. |

Le principe général est simple :

* chaque ticket doit avoir ses tests ;
* chaque sprint doit avoir ses preuves ;
* chaque release doit avoir une régression complète ;
* aucune validation ne passe sans preuves.

---

# 7. Stratégie Git

## 7.1 Branches

* `main` : branche protégée de production ;
* `develop` : branche d'intégration ;
* `feature/*` : branches de travail isolées ;
* `release/*` : branches de stabilisation ;
* `hotfix/*` : branches de correction urgente.

## 7.2 Règles de merge

* aucun développement direct sur `main` ;
* chaque ticket passe par une branche dédiée ;
* chaque merge se fait via pull request ;
* au moins une revue est requise, deux pour les sujets sensibles ;
* les sujets sécurité, paiement, migration et IA nécessitent une revue renforcée.

## 7.3 Tags et releases

* les tags doivent être explicites ;
* les versions candidates doivent être balisées ;
* la release finale doit être taguée ;
* les hotfix doivent repartir d'une base connue et stable.

## 7.4 Rollback

* le rollback se fait par revert ou hotfix ;
* aucun force push n'est autorisé sur les branches protégées ;
* tout rollback doit être documenté et lié à un ticket.

---

# 8. Stratégie CI/CD

Pipeline recommandé :

1. lint ;
2. build ;
3. tests unitaires ;
4. tests d'intégration ;
5. tests API ;
6. analyse qualité ;
7. analyse sécurité ;
8. validation documentaire ;
9. déploiement development ;
10. déploiement staging ;
11. recette ;
12. déploiement production ;
13. contrôle post-déploiement ;
14. rollback si nécessaire.

Règles :

* aucun merge sans pipeline vert ;
* aucun déploiement sans gate humain sur les sujets sensibles ;
* aucune release sans artefacts versionnés ;
* aucun artefact sans journalisation.

---

# 9. Stratégie de migration

## 9.1 Objets migrés

* utilisateurs ;
* biens ;
* partenaires ;
* médias ;
* base de connaissances ;
* statistiques ;
* historiques.

## 9.2 Méthode

1. inventaire ;
2. mapping ;
3. extraction ;
4. transformation ;
5. chargement en staging ;
6. validation ;
7. répétition à blanc ;
8. cutover ;
9. réconciliation.

## 9.3 Critères de validation par objet

| Objet | Validation |
| --- | --- |
| Utilisateurs | Comptage, correspondance des identités, statuts et rôles. |
| Biens | Comptage, attributs, photos, documents, géolocalisation. |
| Partenaires | Comptage, certificats, suspensions, affiliations. |
| Médias | Intégrité, taille, disponibilité, association aux biens. |
| Base de connaissances | Catégories, versions, validations, liens IA. |
| Statistiques | Agrégats, cohérence temporelle, traçabilité des sources. |
| Historiques | Ordre, horodatage, conservation et auditabilité. |

## 9.4 Règles

* toute migration doit être testée avant production ;
* toute migration doit être réversible ;
* tout écart doit être documenté ;
* toute reprise doit être validée humainement.

---

# 10. Stratégie Knowledge

La connaissance de LAWIM_V2 doit être intégrée progressivement à partir de :

* études ;
* FAQ ;
* droit immobilier ;
* quartiers ;
* villes ;
* guides ;
* procédures ;
* prompts ;
* analyses ;
* retours utilisateurs ;
* retours partenaires ;
* données marketing.

## 10.1 Cycle de vie

1. collecte ;
2. normalisation ;
3. curation ;
4. validation ;
5. versioning ;
6. publication ;
7. consommation par l'IA ;
8. retour d'expérience ;
9. révision.

## 10.2 Lien avec LAWIM AI

LAWIM AI consomme la base de connaissances pour :

* comprendre les termes ;
* traduire ;
* répondre ;
* proposer des synonymes ;
* assister la recherche ;
* améliorer la pertinence du matching et du support.

La connaissance ne doit jamais alimenter une automatisation sensible sans validation humaine.

---

# 11. Stratégie Legacy

L'ancien LAWIM est une source d'inspiration, pas la base du nouveau code.

## 11.1 Peut être réutilisé

* le vocabulaire validé ;
* les documents de référence figés ;
* les schémas de compréhension marché ;
* les contenus de connaissance ;
* certains patterns UX ou opérationnels validés après revue.

## 11.2 Doit être réécrit

* le code métier ;
* les API métier ;
* les modèles techniques ;
* les intégrations sensibles ;
* les parcours qui dépendent d'anciennes hypothèses non figées.

## 11.3 Doit être abandonné

* les duplications ;
* les logiques ambiguës ;
* les traces de commission immobilière ;
* les comportements obsolètes ;
* les composants non alignés avec la documentation figée.

## 11.4 Référence uniquement

* les analyses historiques ;
* les preuves de marché ;
* les supports de comparaison ;
* les données utiles à la migration.

---

# 12. Gouvernance du développement

## 12.1 Fréquence des revues

* daily courte ;
* revue technique hebdomadaire ;
* revue architecture hebdomadaire ;
* revue documentaire hebdomadaire ;
* revue sécurité à chaque sprint ;
* revue release avant tout tag.

## 12.2 Validation documentaire

Chaque ticket doit pointer vers :

* les documents de référence ;
* la matrice de traçabilité ;
* le sprint concerné ;
* le livrable attendu.

## 12.3 Validation métier

Les sujets métier sensibles nécessitent :

* acceptation produit ;
* acceptation métier ;
* confirmation de non-contradiction avec les référentiels ;
* clôture formelle.

## 12.4 Validation sécurité

Les sujets sécurité, paiement, migration, IA et confidentialité exigent :

* revue dédiée ;
* journaux d'audit ;
* tests de sécurité ;
* approbation avant release.

## 12.5 Gestion des changements

Tout changement doit :

* être lié à un ticket ;
* être justifié ;
* être testé ;
* être documenté ;
* être réversible ;
* être validé avant propagation.

---

# 13. Jalons (Milestones)

| Jalon | Déclencheur | Sprint(s) associé(s) | Critère de sortie |
| --- | --- | --- | --- |
| M0 | Bootstrap validé | S001 | Dépôt, gouvernance et sources clarifiées. |
| M1 | Infrastructure validée | S002 | Environnements stables et observables. |
| M2 | Authentification validée | S004 | Accès maîtrisé. |
| M3 | Utilisateurs validés | S005 | Acteurs et permissions alignés. |
| M4 | Immobilier validé | S006-S007 | Biens, prix, médias et geo exploitables. |
| M5 | Matching validé | S009-S010 | Rapprochement et décisions opérationnels. |
| M6 | IA validée | S017-S018 | Base de connaissances et assistance prêtes. |
| M7 | Campay validé | S014 | Paiement et réconciliation fiables. |
| M8 | Dashboards validés | S015-S016 | Pilotage et reporting disponibles. |
| M9 | Migration validée | S022-S023 | Reprise contrôlée des données utiles. |
| M10 | Beta interne | S024 | Usage interne complet. |
| M11 | Beta privée | S024 | Validation d'un cercle restreint. |
| M12 | Release Candidate | S024 | Version stabilisée. |
| M13 | Production | S024 | Déploiement officiel. |

---

# 14. Indicateurs de pilotage

| KPI | Définition | Cible de pilotage |
| --- | --- | --- |
| Avancement | Tickets terminés / tickets planifiés. | Suivre à chaque sprint. |
| Couverture de tests | Tests passés / tests attendus. | Suivre à chaque merge et sprint. |
| Bugs | Nombre d'anomalies ouvertes par sévérité. | Réduire à chaque sprint. |
| Dette technique | Points de dette ou backlog technique. | Réduire continuellement. |
| Qualité | Score de conformité fonctionnelle et documentaire. | Maintenir au vert. |
| Vélocité | Tickets livrés par sprint. | Stabiliser après 3 sprints. |
| Stabilité | Taux d'incidents et de régressions. | Maintenir bas. |
| Performance | Temps de réponse et charge supportée. | Mesurer à partir des sprints clés. |
| Conformité documentaire | Documents, liens et matrices à jour. | 100 pour cent avant release. |

---

# 15. Gestion des risques

| Risque | Probabilité | Impact | Mitigation |
| --- | --- | --- | --- |
| Migration incomplète | Moyen | Élevé | Dry-runs, checksums, réconciliation, rollback. |
| Sécurité insuffisante | Moyen | Élevé | Sprint 21, revues sécurité, audit. |
| Campay incohérent | Moyen | Élevé | Sandbox, idempotence, signatures, reconciliation. |
| Qualité des données | Élevé | Élevé | Validation, curation, déduplication, scoring. |
| Legacy contamination | Moyen | Élevé | Legacy en lecture, tickets isolés, revue architecture. |
| AI hallucination | Moyen | Élevé | Knowledge grounded, human validation, citations. |
| Scope creep | Élevé | Moyen | Ticketing strict, change control, release gating. |
| Dérive documentaire | Moyen | Élevé | Release figée, index maître, changelog. |
| Performance insuffisante | Moyen | Moyen | Profiling, tests charge, optimisation ciblée. |
| UX incohérente | Moyen | Moyen | Design system, review UX, tests utilisateurs. |

---

# 16. Checklists officielles

## 16.1 Avant Sprint

* confirmer l'objectif ;
* confirmer les dépendances ;
* confirmer les références documentaires ;
* confirmer la capacité de l'équipe ;
* confirmer le périmètre du ticket ;
* confirmer les risques ;
* confirmer les critères d'acceptation.

## 16.2 Pendant Sprint

* tenir le board à jour ;
* vérifier les tests au fil de l'eau ;
* valider les changements de scope ;
* documenter les hypothèses ;
* journaliser les décisions importantes ;
* escalader les blocages.

## 16.3 Avant Merge

* build vert ;
* lint vert ;
* tests verts ;
* documentation alignée ;
* revue effectuée ;
* sécurité vérifiée si sensible.

## 16.4 Avant Release

* régression complète ;
* validation documentaire ;
* validation métier ;
* validation sécurité ;
* plan de rollback prêt ;
* release notes prêtes.

## 16.5 Avant Production

* staging stable ;
* monitoring actif ;
* sauvegardes vérifiées ;
* performance acceptable ;
* Campay validé si concerné ;
* approbation humaine signée.

## 16.6 Après Production

* surveillance renforcée ;
* correction rapide des incidents ;
* revue post-release ;
* mise à jour du changelog ;
* archivage des preuves ;
* retour d'expérience.

---

# 17. Règles absolues

* la documentation V1.0 est la seule source de vérité ;
* toute évolution documentaire passe par le versioning ;
* aucun code ne peut contredire les référentiels sans décision formelle ;
* les procédures opérationnelles doivent être respectées ;
* les tests sont obligatoires avant toute validation ;
* aucune commission immobilière ne peut être introduite ;
* aucun nouveau moteur métier ne peut être créé sans décision formelle ;
* aucun changement silencieux n'est autorisé.

---

# 18. Ordre d'implémentation recommandé

1. Bootstrap et contrat de dépôt.
2. Infrastructure et environnements.
3. Base de données et stockage.
4. Authentification et identité.
5. Utilisateurs, rôles, organisations.
6. Immobilier, médias, documents, géolocalisation.
7. Conversation.
8. Matching.
9. Decision Engine et rematching.
10. Workflows, visites, notifications.
11. Tracking et attribution.
12. Campay.
13. Dashboards.
14. Reporting.
15. Knowledge Base.
16. LAWIM AI.
17. Continuous Learning.
18. Mobile.
19. Security hardening.
20. Migration.
21. Beta et production readiness.

---

# 19. Conclusion

Ce plan maître est la référence unique de planification et de gouvernance technique pour LAWIM_V2 jusqu'à la mise en production.

# FIN DU DOCUMENT
