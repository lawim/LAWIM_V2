# LAWIM_V2 Global Legacy Cleanup

## 1. Résumé exécutif
- Nettoyage ciblé du chemin conversationnel et des couches assistant legacy.
- Suppression du provider LLM optionnel côté assistant.
- Suppression du fallback direct vers `AIOrchestrator.generate` dans `CommunicationService`.
- Passage du `BrainService` et de l’assistant web vers `ConversationCoreService` comme point d’entrée effectif.
- Fallback conversationnel rendu déterministe et dépendant de l’état (`next_question`, `next_action`).

## 2. État Git initial
- Branche: `main`.
- HEAD initial: `983b4ffe` (`chore: snapshot pre-cleanup conversation audit state`).
- La branche locale était déjà en avance sur `origin/main`.
- Le worktree était propre au démarrage de cette phase de nettoyage.

## 3. Tag de sécurité
- Tag créé: `pre-cleanup-lawim-v2`.
- Objectif: point de retour stable avant suppressions effectives.

## 4. Méthode de détection
- Recherches `rg` sur les imports et symboles legacy.
- Lecture ciblée des services `assistant`, `communication`, `brain`, `conversation_core`, `ai`.
- Vérification de la compilation Python avec `compileall`.
- Exécution des tests unitaires ciblés autour du noyau conversationnel.

## 5. Cartographie initiale
- `code/lawim_v2/services.py` instancie `AIOrchestrator`, `ConversationCoreService`, `AssistantService`, `CommunicationService`, `BrainService`.
- `code/lawim_v2/conversation_core/service.py` pilote la qualification, la mémoire, la progression et l’émission finale.
- `code/lawim_v2/communication/service.py` exposait encore un fallback direct vers `AIOrchestrator`.
- `code/lawim_v2/assistant/repository.py` contenait un routage autonome et un moteur déterministe historique.
- `code/lawim_v2/brain/service.py` gardait une branche de secours legacy hors Conversation Core.
- `code/lawim_v2/ai/fallback.py` renvoyait encore un fallback générique par défaut.

## 6. Sources de vérité retenues
- `ConversationCoreService` comme autorité d’exécution conversationnelle.
- `ProgressionEngine` comme source de qualification et de prochaine étape.
- `BrainMemory` comme mémoire métier lue avant réponse.
- `AIOrchestrator` comme fournisseur de génération, mais plus comme décideur de stratégie.
- `ProjectService` et les moteurs métier existants comme sources canoniques de données et d’actions.

## 7. Conversation Core canonique
- La réponse déterministe est privilégiée pour les salutations, refus externes, questions de qualification et prochaine action connue.
- Quand la progression est suffisante, `next_action` est renvoyé sans appel LLM.
- Quand `direct_reply` existe, le LLM n’est plus invoqué.
- La progression et la mémoire sont toujours calculées avant la décision finale.

## 8. Legacy conversationnel supprimé
- `code/lawim_v2/assistant/providers.py` supprimé.
- `AgentRouterEngine` supprimé de `code/lawim_v2/assistant/engines.py`.
- `DeterministicAssistantEngine` supprimé de `code/lawim_v2/assistant/engines.py`.
- La branche de réponse autonome du stack assistant a été retirée.

## 9. Fallbacks supprimés
- Le fallback générique a été remplacé par un fallback état-aware.
- `compose_fallback()` retourne d’abord `next_question`, puis `next_action`.
- `FallbackEngine.resolve()` tente d’abord une réponse issue de la progression avant la phrase générique.
- Le message de secours a été réécrit pour ne plus sonner comme un assistant généraliste.

## 10. Appels IA directs supprimés
- `CommunicationService._dispatch_ai_reply()` ne contient plus de branche directe vers `AIOrchestrator.generate`.
- En absence de `conversation_core`, le chemin renvoie une erreur explicite et loggée.
- `AssistantService.chat()` ne possède plus de provider LLM optionnel local.
- `BrainService.process_chat()` passe uniquement par `ConversationCoreService`.

## 11. Mémoire nettoyée
- La mémoire métier continue d’être lue avant la réponse via `BrainMemory`.
- Aucune nouvelle couche mémoire parallèle n’a été ajoutée.
- Les données `hypothesis`/`pending` n’ont pas été modifiées dans cette phase.
- Le comportement de réutilisation dépend maintenant davantage de la progression que d’un texte de repli.

## 12. Brain nettoyé
- La branche legacy de `BrainService` hors Conversation Core a été retirée.
- `BrainService` dépend désormais d’un noyau conversationnel injecté.
- Les suggestions retournées par `BrainService` proviennent désormais de la progression du noyau, pas d’un assistant parallèle.

## 13. Assistant legacy supprimé
- Le provider LLM historique a disparu.
- Le routage autonome historique a disparu.
- `AssistantService` exige désormais un `conversation_core`.
- `AssistantRepository.chat_assistant()` exige désormais un `conversation_core` effectif.

## 14. Recherche et matching nettoyés
- Aucun changement fonctionnel dans ce lot.
- Les moteurs métiers existants restent en place.
- Le couplage conversationnel vers ces moteurs n’a pas été modifié ici.

## 15. Relation et consentement nettoyés
- Aucun changement fonctionnel dans ce lot.
- Aucun moteur relationnel n’a été recréé.

## 16. CRM nettoyé
- Aucun changement fonctionnel dans ce lot.

## 17. GED nettoyée
- Aucun changement fonctionnel dans ce lot.

## 18. Workflows nettoyés
- Aucun changement fonctionnel dans ce lot.

## 19. Financial Core et Campay nettoyés
- Aucun changement fonctionnel dans ce lot.
- Campay n’a pas été modifié.

## 20. Notifications nettoyées
- Aucun changement fonctionnel dans ce lot.

## 21. WhatsApp nettoyé
- Aucun changement de canal en dehors du retrait du fallback conversationnel direct.

## 22. Telegram nettoyé
- Aucun changement de canal en dehors du retrait du fallback conversationnel direct.

## 23. Email nettoyé
- Aucun changement fonctionnel dans ce lot.

## 24. Frontend nettoyé
- Aucun fichier frontend n’a été modifié dans ce lot.
- Le dépôt ne déclare pas de scripts frontend classiques dans `package.json`.

## 25. API nettoyée
- La route assistant continue d’exister, mais elle est maintenant alimentée par le Conversation Core.
- Le chemin de secours direct vers le LLM a été neutralisé.

## 26. SDK nettoyé
- Aucun SDK supprimé dans ce lot.

## 27. Base et migrations nettoyées
- Aucune migration ajoutée ou supprimée dans ce lot.

## 28. Configuration nettoyée
- La lecture du flag `LAWIM_LLM_ENABLED` a été retirée du service assistant.
- `CommunicationService` ne maintient plus de provider IA local.

## 29. Feature Flags nettoyés
- Aucun feature flag ajouté.
- Le flag assistant LLM local n’est plus consommé par le service assistant.

## 30. Dépendances supprimées
- Aucune dépendance npm ou Python supprimée dans ce lot.
- Le provider LLM local supprimé ne dépendait pas d’un package externe dédié.

## 31. Tests supprimés
- `tests/test_release_program_d.py` supprimé.
- Ce fichier validait principalement des comportements legacy de l’ancien stack assistant.

## 32. Tests ajoutés
- `tests/test_conversation_core_migration.py::test_communication_dispatch_without_conversation_core_returns_error`
- `tests/test_conversation_core_migration.py::test_conversation_core_uses_deterministic_next_action_without_llm`
- Ces tests prouvent l’absence de fallback direct et la non-invocation du LLM quand la prochaine action est déjà déterminée.

## 33. Documentation supprimée
- Aucune documentation supprimée dans ce lot.

## 34. Documentation mise à jour
- Aucun document produit n’a été modifié dans ce lot.

## 35. Artefacts supprimés
- Aucun artefact généré n’a été supprimé dans ce lot.

## 36. Fichiers créés
- `reports/product_reviews/LAWIM_V2_Global_Legacy_Cleanup.md`

## 37. Fichiers modifiés
- `code/lawim_v2/assistant/constants.py`
- `code/lawim_v2/assistant/engines.py`
- `code/lawim_v2/assistant/repository.py`
- `code/lawim_v2/assistant/service.py`
- `code/lawim_v2/brain/service.py`
- `code/lawim_v2/communication/service.py`
- `code/lawim_v2/conversation_core/response.py`
- `code/lawim_v2/conversation_core/service.py`
- `code/lawim_v2/ai/fallback.py`
- `code/lawim_v2/persona.py`
- `code/lawim_v2/services.py`
- `tests/test_conversation_core_migration.py`

## 38. Fichiers supprimés
- `code/lawim_v2/assistant/providers.py`
- Raison: provider LLM local legacy, uniquement utilisé par l’ancien assistant autonome.
- Remplacement canonique: aucun provider local dans l’assistant; Conversation Core injecté directement.
- Preuve d’absence de consommateur: recherche `rg` sans références restantes dans `code/` ou `tests/`.
- `tests/test_release_program_d.py`
- Raison: suite legacy orientée assistant historique et provider optionnel.
- Remplacement canonique: `tests/test_conversation_core_migration.py`.
- Preuve d’absence de consommateur: aucune référence runtime restante après suppression.

## 39. Routes supprimées
- Aucune route supprimée dans cette phase.
- La suppression a porté sur le chemin d’exécution, pas sur le routeur HTTP lui-même.

## 40. Variables supprimées
- `LAWIM_LLM_ENABLED` n’est plus consommée par `AssistantService`.
- Le flag de fallback direct à l’IA côté communication a été retiré du chemin runtime.

## 41. Packages supprimés
- Aucun package supprimé.

## 42. Migrations ajoutées
- Aucune migration ajoutée.

## 43. Compilation
- Commande exécutée: `PYTHONPYCACHEPREFIX=/tmp/lawim-pycache python3 -m compileall -q code tests`
- Résultat: succès.

## 44. Tests backend
- Commande exécutée: `PYTHONPATH=code python3 -m unittest tests.test_conversation_core_migration tests.test_ai_orchestrator lawim_v2.brain.tests`
- Résultat: `Ran 85 tests in 18.298s`, `OK`.

## 45. Tests frontend
- Aucun script frontend classique n’est défini dans `package.json`.
- La validation npm pertinente de ce dépôt est principalement Prisma.

## 46. Build
- Aucun build frontend n’a été exécuté.
- Aucun script `build` n’est défini dans `package.json`.

## 47. Déploiement
- Aucun déploiement effectué dans cette phase de nettoyage locale.

## 48. Tests runtime
- Non exécutés.

## 49. Tests Web
- Non exécutés.

## 50. Tests WhatsApp
- Non exécutés.

## 51. Tests Telegram
- Non exécutés.

## 52. Résidus trouvés après nettoyage
- Les documents de spécification contiennent encore des exemples historiques mentionnant des assistants généralistes et des plateformes externes.
- Les routes assistant d’appoint restent présentes par compatibilité, mais ne disposent plus de fallback direct vers le LLM.
- `npm run prisma:validate` n’a pas pu être exécuté dans cet environnement car le binaire `prisma` n’est pas installé.

## 53. Commit
- Commit de nettoyage à créer après ce rapport: `chore: decommission legacy assistant fallback paths`.

## 54. Tag
- Tag de sécurité: `pre-cleanup-lawim-v2`.
- Aucun tag de release final n’a encore été posé à ce stade du rapport.

## 55. État Git final
- État attendu après commit: worktree propre.
- L’état final sera confirmé après l’ajout du rapport et le commit de nettoyage.

## 56. Réserves
- La documentation historique n’a pas été purgée dans cette phase.
- Les couches assistant de compatibilité restent exposées, mais leur logique de réponse a été alignée sur le Conversation Core.
- La validation Prisma n’a pas été possible faute de binaire local.

## 57. Verdict
- `NON VALIDÉ`
- Motifs: validation locale incomplète côté Prisma, absence de déploiement runtime, et nettoyage documentaire non exécuté dans ce lot.
