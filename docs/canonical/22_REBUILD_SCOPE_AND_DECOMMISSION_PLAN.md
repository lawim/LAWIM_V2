# Plan De Reconstruction Et Decommissionnement

Version: 1.0
Date: 2026-07-14
Commit de reference: d30d61e1d89427ece9c180cec4639cce77fdcba3
Statut: CANONICAL

## Regle
Mission 1 ne supprime pas le runtime metier. Mission 2 executera la demolition controlee selon ce plan.

| Chemin | Responsabilite actuelle | Responsabilite canonique | Dependances | Donnees | Tests | Statut | Action Mission 2 | Raison |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| code/lawim_v2/conversation_core/ | Conversation runtime actuel | Conversation cible reconstruite | brain.memory, RelationEngine, AI | conversation, message, fact | tests/test_conversation_core_migration.py | DELETE | DELETE puis REBUILD | Architecture jugee non conforme aux parcours live. |
| code/lawim_v2/assistant/ | Assistant et RAG historiques | Adaptateur ou suppression | knowledge, brain | sessions, prompts | tests release assistant | DELETE | DELETE/REMOVE_ROUTE | Ancien assistant concurrent du futur Conversation. |
| code/lawim_v2/brain/ | Brain, memoire, relation | Aucun domaine unique canonique | conversation_core, repository | memory, relation | code/lawim_v2/brain/tests.py | SPLIT | DELETE/SPLIT | Melange memoire, dossier, relation et orchestration. |
| code/lawim_v2/matching.py | Matching simple | Matching cible explicable | properties | criteria | tests release | DELETE | DELETE | Non relie aux criteres canoniques. |
| code/lawim_v2/real_estate_intelligence/ | Biens, recherche, visites, transactions | Properties/Listings a conserver, search/matching a extraire | repository | property, listing, visit | tests release G | CLEAN | CLEAN/SPLIT | Fondation biens utile, matching a reconstruire. |
| code/lawim_v2/marketplace/ | Partenaires et request matching | Partenaires a conserver, matching a reconstruire | ecosystem | partner, provider | tests release I | CLEAN | CLEAN/SPLIT | Matching fournisseur non valide metier. |
| routes /api/v2/assistant/brain/* | Routes brain conversationnelles | API cible a redefinir | server.py | project, relation | tests conversation | REMOVE_ROUTE | REMOVE_ROUTE | Expose ancien Brain. |
| routes /api/v2/matching et /api/v2/projects/*/matching* | Routes matching historiques | API target search/matching v2 | server.py | match | tests ecosystem | REMOVE_ROUTE | REMOVE_ROUTE | Contrats non canoniques. |
| tests conversation/matching/relation historiques | Preuves techniques isolees | Nouveau standard comportemental | runtime actuel | fixtures | tests/* | REMOVE_TEST | REMOVE_TEST | Ne prouvent pas conformite metier. |
| frontend conversation/matching surfaces | UI historique | UI cible apres contrats | API SDK | state UI | frontend/tests | REBUILD | REBUILD | Couplee aux routes actuelles. |
| code/lawim_v2/security/ | IAM, audit, roles | Identity and Access | config, db | user, session | tests security | KEEP | CLEAN | Fondation independante. |
| code/lawim_v2/financial/ | Financial Core et Campay | Financial Core | providers | payment, invoice | tests financial | KEEP | CLEAN | Fondation conservee sous controle. |
| code/lawim_v2/communication/ | Notifications et canaux | Adaptateurs omnicanaux | AI optional | message, notification | tests webhooks | KEEP | CLEAN | A garder sans logique metier autonome. |
| code/lawim_v2/backup/ | Backup et recovery | Backup and DR | storage | bundle, schedule | tests backup | KEEP | CLEAN | Fondation operationnelle. |

## Documents associes supprimes en Mission 1
Les anciennes constitutions, Product Bible, directives, specifications conversationnelles, platform readiness, matrices de qualification, strategies IA, references matching/relation et rapports produit trompeurs sont remplaces par `docs/canonical/` et supprimes du depot actif lorsque leur maintien cree une confusion.

## Statut Apres Mission 2

Date: 2026-07-14

| Domaine | Statut apres Mission 2 | Preuve locale | Entrée Mission 3 |
| --- | --- | --- | --- |
| Conversation | DECOMMISSIONED / REBUILD_PENDING | `code/lawim_v2/conversation_core/` supprime, routes `/api/v2/assistant/*` supprimees | Reconstruire un nouveau runtime cible. |
| Qualification conversationnelle | DECOMMISSIONED / REBUILD_PENDING | Progression, next question et memoire Brain supprimees | Construire matrices executables. |
| Search orchestration | DECOMMISSIONED / REBUILD_PENDING | `/api/matches`, `/api/v2/properties/search` et orchestration de matching retirees | Construire Search v2. |
| Matching | DECOMMISSIONED / REBUILD_PENDING | `code/lawim_v2/matching.py`, MatchingEngine2, RequestMatchingEngine et MatchingEngine supprimes | Construire Matching v2 explicable. |
| Relationship | DECOMMISSIONED / REBUILD_PENDING | `code/lawim_v2/brain/relation.py` et routes consent/proposal/relations supprimees | Construire Relationship v2 avec consentements. |

Mode maintenance actif via `lawim_core_rebuild_maintenance_mode=true`; les sous-flags Conversation, Qualification, Search, Matching et Relationship restent `false`.
