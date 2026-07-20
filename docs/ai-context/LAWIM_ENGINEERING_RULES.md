# LAWIM — Règles Techniques Permanentes

## Règles d'exécution

1. **Reproduire le défaut avant toute correction.**
   Ne jamais modifier le code sans avoir reproduit et observé le comportement défaillant.

2. **Créer un test qui échoue avant de modifier le code.**
   Écrire d'abord un test qui capture le défaut, vérifier qu'il échoue, puis corriger.

3. **Identifier la cause racine, pas seulement le symptôme.**
   Creuser jusqu'à la cause profonde. Ne pas se contenter du premier niveau d'erreur.

4. **Réutiliser les services canoniques.**
   Ne pas créer de nouveaux chemins parallèles. Utiliser les services, modules et packages existants.

5. **Éviter les nouveaux chemins parallèles.**
   Toute nouvelle fonctionnalité doit emprunter le pipeline existant ou l'étendre, jamais le contourner.

6. **Aucun `return None` silencieux.**
   Toute fonction qui retourne `None` doit le faire explicitement avec documentation.

7. **Aucun `except Exception: pass`.**
   Toute exception capturée doit être journalisée (sans secret) et traité.

8. **Toute erreur doit être journalisée sans secret.**
   Les logs ne doivent jamais contenir de mots de passe, tokens, clés ou données personnelles.

9. **Une erreur de footer ne doit jamais empêcher la réponse principale.**
   Le rendu du footer est décoratif. En cas d'échec, la réponse principale est envoyée sans footer.

10. **Une erreur d'un fournisseur IA doit déclencher le fallback.**
    L'échec du fournisseur primaire passe au suivant dans la chaîne de fallback configurée.

11. **Les tests simulés ne remplacent pas les tests réels.**
    Un mock ou un webhook simulé prouve le code, pas le fonctionnement réel.

12. **L'agent qui exécute ne certifie pas seul son propre travail.**
    Toute certification doit être validée par un pair ou un réviseur indépendant.

13. **Les tags Git ne constituent pas une preuve runtime.**
    Un tag `verified` ne remplace pas une vérification réelle sur canal.

14. **Le code métier décide ; le LLM formule.**
    Le moteur détermine l'intention, l'état, la prochaine action. Le LLM rédige la réponse.

15. **Toute modification doit avoir un rollback documenté.**
    Avant tout déploiement, la procédure de retour arrière doit être identifiée et écrite.

## Politique Git

- une mission = une branche
- commits ciblés (un commit par changement logique)
- tests avant fusion
- worktree propre à la clôture
- `origin/main...HEAD = 0 0`
