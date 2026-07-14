# LAWIM_V2 Mission 1 - Canonical Documentation Refoundation

Date: 2026-07-14
Initial commit: d30d61e1d89427ece9c180cec4639cce77fdcba3
Initial safety tag: pre-canonical-documentation-refoundation
Final tag target: lawim-v2-canonical-specification-v1

## 1. Resume executif
La documentation active de LAWIM_V2 a ete refondee autour d'une seule source de verite: `docs/canonical/`. Les anciens referentiels contradictoires de `docs/Directive`, `docs/platform`, `docs/PRODUCT_BIBLE`, `docs/strategy`, `docs/Specifications`, l'ADR historique et les rapports produit trompeurs ont ete supprimes du depot actif. Git conserve l'historique.

## 2. Etat Git initial
- Branche: `main`
- HEAD initial: `d30d61e1d89427ece9c180cec4639cce77fdcba3`
- Statut initial: worktree propre, branche en avance de 20 commits sur `origin/main`.
- Historique recent:
```text
d30d61e1 (HEAD -> main, tag: pre-canonical-documentation-refoundation, tag: lawim-v2-final-live-validation-2026-07-14) docs(product-review): record final live validation
31ba1fd0 (tag: lawim-v2-pre-live-validation-2026-07-13) fix(platform): stabilize backend before live conversation validation
62c11df1 (tag: lawim-v2-conversation-runtime-validation-2026-07-13) docs: finalize conversation core runtime validation report
993dadcd feat(conversation-core): validate runtime pipeline
c35db755 docs: finalize legacy cleanup report
```

## 3. Tag de securite
Tag cree avant modification: `pre-canonical-documentation-refoundation`.

## 4. Methode d'inventaire
Inventaire par `git ls-files`, `find`, `rg`, lecture des index, rapports, dossiers `docs`, `reports`, `OPS`, `scripts`, `prisma`, `frontend`, `code`, `tests` et fichiers de configuration. Les modules et routes ont ete cartographies depuis `code/lawim_v2/server.py`, `code/lawim_v2/*`, `prisma/schema.prisma` et les tests.

## 5. Nombre de documents analyses
609 fichiers documentaires et quasi-documentaires ont ete releves dans les perimetres principaux, hors dependances `node_modules` et artefacts generes.

## 6. Concepts recenses
Les concepts canoniques sont definis dans `docs/canonical/24_GLOSSARY.md`: LAWIM, utilisateur, visiteur, client, proprietaire, vendeur, bailleur, acheteur, locataire, investisseur, agents, agences, partenaires, professionnels, projet, dossier, conversation, message, fait, memoire, intention, qualification, recherche, bien, annonce, matching, proposition, consentement, relation, visite, offre, negociation, document, paiement, facture, commission, notification, feature flag, cockpit, evenement et audit.

## 7. Contradictions identifiees
- Product Bible et constitution anciennes se declaraient reference supreme.
- Directives conversation, matching, decision engine et IA entraient en concurrence avec les rapports Mission 10, 11, 15 et validation runtime.
- Plusieurs documents assimilaient tests techniques et validation metier.
- Brain, Conversation Core, Memory, Matching et Relation avaient des responsabilites chevauchantes.
- Les canaux et fournisseurs IA etaient parfois presentes comme porteurs d'une logique autonome.

## 8. Decisions canoniques
- `docs/canonical/` est superieur a tout ancien document.
- Conversation, qualification conversationnelle, search orchestration, matching, relationship, consentement, visites et suivi conversationnels sont `REBUILD_FROM_ZERO`.
- Identity, profiles, channels verified, CRM, properties/listings, GED, Financial Core, Campay, notifications, feature management, audit, monitoring, backup, PostgreSQL, Redis, Docker et deploiement sont conserves sous controle.

## 9. Domaines canoniques
La carte de domaines est dans `docs/canonical/03_DOMAIN_BOUNDARIES.md` avec statuts futurs, responsabilites, dependances autorisees et dependances interdites.

## 10. Modele de donnees canonique
`docs/canonical/04_CANONICAL_DATA_MODEL.md` definit User, Profile, ChannelIdentity, Organization, Project, Dossier, Property, Listing, Document, Conversation, Message, Fact, SearchRequest, Match, Proposal, Consent, Relationship, Visit, Offer, Payment, Invoice, Notification, FeatureFlag et AuditEvent.

## 11. Conversation
Ancien module: `DELETE`. Nouveau module: `REBUILD_FROM_ZERO`. Specification cible: `docs/canonical/07_CONVERSATION_TARGET_SPECIFICATION.md`.

## 12. Qualification
Qualification cible par matrices executables et faits traces: `docs/canonical/08_QUALIFICATION_TARGET_SPECIFICATION.md`.

## 13. Search
Search cible separe de Matching: `docs/canonical/09_SEARCH_AND_MATCHING_TARGET_SPECIFICATION.md`.

## 14. Matching
Moteur actuel classe `UNVALIDATED`, `TO_DELETE`, `TO_REBUILD` lorsqu'il depend d'etats non fiables.

## 15. Relationship
Moteur relationnel actuel classe `UNVALIDATED`, `TO_DELETE`, `TO_REBUILD`; consentement explicite obligatoire.

## 16. Visits et suivi
Visites, suivi commercial et transaction sont definis dans `docs/canonical/11_VISITS_COMMERCIAL_AND_TRANSACTION_FLOW.md`.

## 17. Documents
GED et information juridique sont definies dans `docs/canonical/12_DOCUMENTS_AND_LEGAL_INFORMATION.md`.

## 18. Financial Core et Campay
Fondations conservees sous controle dans `docs/canonical/13_FINANCIAL_CORE_AND_CAMPAY.md`.

## 19. Canaux
Web, WhatsApp, Telegram et Email sont adaptateurs techniques dans `docs/canonical/14_CHANNELS_AND_OMNICHANNEL.md`.

## 20. IA
OpenAI, DeepSeek et Gemini sont capacites linguistiques interchangeables dans `docs/canonical/15_AI_GOVERNANCE.md`.

## 21. Feature Management
Flags globaux, sous-flags, kill switches et audit sont definis dans `docs/canonical/16_FEATURE_MANAGEMENT.md`.

## 22. Cockpits
Cockpits definis comme surfaces de pilotage sans logique metier proprietaire dans `docs/canonical/17_ADMINISTRATION_AND_COCKPITS.md`.

## 23. Securite
Securite, confidentialite et consentement sont definis dans `docs/canonical/18_SECURITY_PRIVACY_AND_CONSENT.md`.

## 24. Tests
Le standard d'acceptation est defini dans `docs/canonical/20_TESTING_AND_ACCEPTANCE_STANDARD.md`.

## 25. Deploiement
Operations et reprise sont definies dans `docs/canonical/21_DEPLOYMENT_OPERATIONS_AND_RECOVERY.md`.

## 26. Modules a conserver
IAM, profiles, CRM, properties/listings sous nettoyage, GED, Financial Core, Campay, notifications, feature management, audit, monitoring, backup, PostgreSQL, Redis, Docker et deploiement.

## 27. Modules a nettoyer
`communication`, `real_estate_intelligence` pour separer biens/search/matching, `marketplace` pour separer partenaires/matching, routes et cockpits relies aux anciens contrats.

## 28. Modules a supprimer
`conversation_core`, `assistant`, elements conversationnels de `brain`, matching actuel, relation actuelle, consentement actuel, routes associees, DTO/tests/frontend associes selon Mission 2.

## 29. Modules a reconstruire
Conversation, qualification conversationnelle, search orchestration, matching, relationship, consent and introduction workflow, conversation-driven visits et conversation-driven commercial follow-up.

## 30. Documents crees
- `docs/canonical/00_LAWIM_VISION_AND_SCOPE.md`
- `docs/canonical/01_PRINCIPLES_AND_GOVERNANCE.md`
- `docs/canonical/02_USERS_ROLES_AND_ACTORS.md`
- `docs/canonical/03_DOMAIN_BOUNDARIES.md`
- `docs/canonical/04_CANONICAL_DATA_MODEL.md`
- `docs/canonical/05_PROJECTS_AND_DOSSIERS.md`
- `docs/canonical/06_PROPERTIES_AND_LISTINGS.md`
- `docs/canonical/07_CONVERSATION_TARGET_SPECIFICATION.md`
- `docs/canonical/08_QUALIFICATION_TARGET_SPECIFICATION.md`
- `docs/canonical/09_SEARCH_AND_MATCHING_TARGET_SPECIFICATION.md`
- `docs/canonical/10_RELATIONSHIP_TARGET_SPECIFICATION.md`
- `docs/canonical/11_VISITS_COMMERCIAL_AND_TRANSACTION_FLOW.md`
- `docs/canonical/12_DOCUMENTS_AND_LEGAL_INFORMATION.md`
- `docs/canonical/13_FINANCIAL_CORE_AND_CAMPAY.md`
- `docs/canonical/14_CHANNELS_AND_OMNICHANNEL.md`
- `docs/canonical/15_AI_GOVERNANCE.md`
- `docs/canonical/16_FEATURE_MANAGEMENT.md`
- `docs/canonical/17_ADMINISTRATION_AND_COCKPITS.md`
- `docs/canonical/18_SECURITY_PRIVACY_AND_CONSENT.md`
- `docs/canonical/19_EVENTS_OBSERVABILITY_AND_AUDIT.md`
- `docs/canonical/20_TESTING_AND_ACCEPTANCE_STANDARD.md`
- `docs/canonical/21_DEPLOYMENT_OPERATIONS_AND_RECOVERY.md`
- `docs/canonical/22_REBUILD_SCOPE_AND_DECOMMISSION_PLAN.md`
- `docs/canonical/23_TRACEABILITY_MATRIX.md`
- `docs/canonical/24_GLOSSARY.md`
- `docs/canonical/README.md`

## 31. Documents fusionnes
Les informations encore valables des directives, Product Bible, platform docs, specifications, financial docs, backup docs et rapports produit ont ete consolidees dans `docs/canonical/`.

## 32. Documents supprimes
276 documents remplaces sont indexes en suppression Git. Les principaux ensembles supprimes sont les anciennes directives, platform docs, Product Bible, strategies, specifications, financial docs, backup/disaster-recovery docs et anciens documents racine sous `docs`.

## 33. Rapports supprimes ou declasses
Rapports supprimes du depot actif car trompeurs ou remplacant une specification: Mission 10, Mission 11, Mission 12, Mission 15, Conversation Core Runtime Validation, Final Stabilization and Live Validation, Global Legacy Cleanup, Release 09 et readiness matrix. Les autres rapports historiques ne sont pas references comme specification active.

## 34. ADR crees
- `docs/adr/ADR-001-Canonical-Documentation.md`
- `docs/adr/ADR-002-Domain-Boundaries.md`
- `docs/adr/ADR-003-Conversation-Rebuild.md`
- `docs/adr/ADR-004-Search-Matching-Rebuild.md`
- `docs/adr/ADR-005-Relationship-Rebuild.md`
- `docs/adr/ADR-006-AI-As-Linguistic-Capability.md`
- `docs/adr/ADR-007-Omnichannel-Adapters.md`
- `docs/adr/ADR-008-Feature-Flag-Governance.md`
- `docs/adr/ADR-009-Behavioral-Acceptance-Standard.md`

## 35. Matrice de tracabilite
Creee dans `docs/canonical/23_TRACEABILITY_MATRIX.md` avec Requirement ID, domaine, objet, API cible, module cible, evenement, flag, test attendu, statut actuel et decision future.

## 36. Plan de decommissionnement
Cree dans `docs/canonical/22_REBUILD_SCOPE_AND_DECOMMISSION_PLAN.md` avec actions Mission 2 executables.

## 37. Controle automatise
Script cree: `scripts/validate_canonical_docs.py`.

## 38. Validations
A executer avant commit final:
```bash
python3 scripts/validate_canonical_docs.py
# Recherche ciblee effectuee sur les anciens chemins et titres supprimes.
```

## 39. Commit
Commit cible: `docs(canonical): refound LAWIM specification and remove obsolete references`.

## 40. Tag
Tag final cible: `lawim-v2-canonical-specification-v1`.

## 41. Etat Git final
A renseigner apres commit: worktree doit etre propre.

## 42. Reserves
Aucune reserve fonctionnelle n'est acceptee pour le verdict. Le code metier n'a pas ete modifie durant cette mission.

## 43. Verdict
VALIDE si le validateur documentaire est vert, les references residuelles sont corrigees, le commit est cree, le tag final est pose et le worktree est propre.

## 44. Entree de la Mission 2
Mission 2 doit supprimer le code conversationnel, matching et relation actuel selon `docs/canonical/22_REBUILD_SCOPE_AND_DECOMMISSION_PLAN.md`, puis reconstruire uniquement a partir des exigences de `docs/canonical/23_TRACEABILITY_MATRIX.md`.
