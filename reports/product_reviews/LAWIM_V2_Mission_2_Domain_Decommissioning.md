# LAWIM_V2 Mission 2 - Domain Decommissioning

Date: 2026-07-14
Branche: main
Commit canonique Mission 1: 54ec4c27ae7cfa6de457c17475be84799e0ed3e8
Tag de securite: pre-domain-decommission-mission-2

## 1. Résumé exécutif
Le bloc Conversation-Qualification-Search-Matching-Relationship legacy a ete decommissionne localement. Le runtime bascule vers un mode maintenance deterministe.

## 2. État Git initial
Worktree propre, branche `main`, HEAD Mission 1 `54ec4c27ae7cfa6de457c17475be84799e0ed3e8`, branche en avance sur `origin/main`.

## 3. Tag de sécurité
Tag cree: `pre-domain-decommission-mission-2`.

## 4. Mode maintenance
Service `MaintenanceService`, table `maintenance_messages`, routes `/api/v2/maintenance/status`, `/api/v2/maintenance/messages`, `/api/v2/maintenance/handover`.

## 5. Inventaire initial
Composants legacy identifies: `conversation_core`, `assistant`, `brain`, `matching.py`, AI fallback interne, routes assistant/matching, SDK Brain, panneaux frontend Advisor/Match.

## 6. Données à conserver
Users, profiles, properties, listings, documents, organizations, payments/invoices, communication messages et audit events.

## 7. Données migrées
Nouvelle table de reception brute `maintenance_messages`.

## 8. Données désactivées
Tables assistant/brain ciblees par migration destructive controlee; resultats de matching projet expires.

## 9. Conversation supprimée
`code/lawim_v2/conversation_core/` supprime.

## 10. Qualification supprimée
Progression Brain, intents, memory, next question et qualification conversationnelle supprimes.

## 11. Search orchestration supprimée
Routes `/api/matches` et `/api/v2/properties/search` retirees.

## 12. Matching supprimé
`matching.py`, `MatchingEngine2`, `MatchingEngine`, `RequestMatchingEngine`, SDK `getMatches` supprimes.

## 13. Relationship supprimé
`RelationEngine`, proposals, consentements et relations automatiques Brain supprimes.

## 14. Consentement supprimé
Routes consent request/grant et DTO associes supprimes.

## 15. Visites dépendantes supprimées
Les appels conversation/matching vers visites sont retires. Les visites REI independantes restent conservees.

## 16. Suivi commercial dépendant supprimé
Les suivis automatiques issus des moteurs supprimes ne sont plus appeles.

## 17. Brain nettoyé
`code/lawim_v2/brain/` supprime.

## 18. IA nettoyée
Fallback interne, prompts system/fallback et provider `internal` retires. L'IA reste une capacite fournisseur externe non appelee par les canaux en maintenance.

## 19. Routes supprimées
`/api/v2/assistant/*`, `/api/v2/matching`, `/api/v2/projects/*/matching*`, `/api/matches`, `/api/v2/properties/matching`, `/api/v2/properties/search`.

## 20. API nettoyée
Routes maintenance ajoutees; routes legacy tombent en 404.

## 21. SDK nettoyé
Types/methodes Brain, proposals, consent et `getMatches` retires. Methodes maintenance ajoutees.

## 22. Frontend nettoyé
`AdvisorPanel`, `MatchResultsPanel`, widgets Match supprimes. Page conversation remplacee par formulaire maintenance.

## 23. Web maintenance
Message web enregistre via `/api/v2/maintenance/messages`.

## 24. WhatsApp maintenance
Webhook conserve, message persiste, reponse maintenance envoyee sans LLM.

## 25. Telegram maintenance
Webhook conserve, message persiste, reponse maintenance envoyee sans LLM.

## 26. Email
Pas de reconstruction email. Adresse officielle conservee.

## 27. Feature Flags
`lawim_core_rebuild_maintenance_mode=true`; services conversation, qualification, search, matching, relationship `false`.

## 28. Événements
Evenements maintenance: `lawim.rebuild.maintenance_message_received`, `lawim.rebuild.human_handover_requested`, `lawim.rebuild.automated_processing_blocked`.

## 29. Métriques
Compteurs maintenance ajoutes via `METRICS.increment`.

## 30. Base de données
Schema runtime ajoute `maintenance_messages`; assistant/brain retires du schema d'initialisation.

## 31. Migrations
Migration ajoutee: `20260714120000_mission_2_domain_decommissioning`.

## 32. Tests supprimés
Tests conversation core, matching, REI matching, Marketplace matching et API SDK matching supprimes.

## 33. Tests créés
`tests/test_mission_2_maintenance_decommissioning.py`.

## 34. Compilation
`PYTHONPYCACHEPREFIX=/tmp/lawim-pycache python3 -m compileall -q code tests`: OK.

## 35. Backend
Tests cibles avec `LAWIM_TEST_MODE=1`: 873 tests OK; `test_lawim_v2.py`: 31 tests OK.

## 36. Frontend
`npm --prefix frontend test`: 30 fichiers, 125 tests OK.

## 37. Typecheck
`npm --prefix frontend run typecheck`: OK.

## 38. Build
`npm --prefix frontend run build`: OK.

## 39. Prisma
`npm run prisma:validate`: NON VALIDE localement, `prisma` absent du PATH (`sh: 1: prisma: not found`). `python3 scripts/validate_prisma_manifest.py`: OK, migration Mission 2 presente et coherente avec le manifeste runtime.

## 40. Déploiement
Non execute dans cette session: acces OVH et sauvegarde production non disponibles.

## 41. Commit runtime
Commit Mission 2: `refactor(platform): decommission conversation matching and relationship domains`.

## 42. Test live Web
Non execute, depend du deploiement.

## 43. Test live WhatsApp
Non execute, depend du deploiement et du canal reel.

## 44. Test live Telegram
Non execute, depend du deploiement et du canal reel.

## 45. Test handover humain
Valide localement par `handover_requested=true` dans maintenance message.

## 46. Recherche des résidus
Residus runtime interdits absents; anciennes routes presentes seulement dans tests explicites de decommissionnement.

## 47. Fichiers supprimés
Conversation Core, Assistant, Brain, matching, persona, fallback IA, panneaux frontend Advisor/Match, tests legacy.

## 48. Fichiers créés
`maintenance.py`, `maintenance_repository.py`, migration Mission 2, tests Mission 2, rapport Mission 2.

## 49. Fichiers modifiés
Runtime services/server/db/schema, communication, AI orchestration, frontend cockpit/SDK/static app, docs canoniques, validate_prisma_manifest.

## 50. Commit
Message: `refactor(platform): decommission conversation matching and relationship domains`.

## 51. Tag
Tag final: `lawim-v2-domain-decommission-mission-2`.

## 52. État Git final
Worktree propre apres commit et tag final; branche `main` en avance sur `origin/main`.

## 53. Réserves
Deploiement OVH et tests live non executes; Prisma CLI indisponible via npm script.

## 54. Verdict
NON VALIDÉ pour les criteres de deploiement/live. Decommissionnement local: conforme.

## 55. Entrée Mission 3
Reconstruire Conversation, Qualification, Search, Matching et Relationship a partir du canon, sur le socle maintenance propre.
