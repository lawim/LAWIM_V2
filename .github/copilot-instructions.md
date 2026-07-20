# LAWIM — Instructions permanentes pour VS Code

Avant toute intervention, lire :

- AGENTS.md
- docs/ai-context/LAWIM_CANONICAL_SCOPE.md
- docs/ai-context/LAWIM_CONVERSATION_CONTRACT.md
- docs/ai-context/LAWIM_ENGINEERING_RULES.md
- docs/ai-context/LAWIM_PRODUCTION_EVIDENCE_POLICY.md
- docs/ai-context/LAWIM_SECRET_MANAGEMENT_POLICY.md
- docs/ai-context/LAWIM_CURRENT_STATE.md

Règles permanentes :

1. LAWIM est une plateforme immobilière opérationnelle au Cameroun, pas un assistant généraliste neutre.

2. Ne jamais rediriger spontanément un utilisateur vers Jumia, Lamudi, SeLoger, Facebook, une agence externe ou une plateforme concurrente.

3. Le moteur métier décide de l’intention, des critères, de l’état, de la prochaine action et du handover. Le LLM formule uniquement la réponse déjà décidée.

4. Conserver les informations fournies au fil de la conversation. Ne jamais traiter isolément une réponse courte lorsqu’un parcours est actif.

5. ProgressiveWizard et les registres canoniques déterminent la prochaine question.

6. Poser une seule prochaine question utile.

7. Collecter les critères fondamentaux avant les exigences facultatives.

8. Ne pas suggérer spontanément le parking, la piscine, la climatisation ou d’autres options secondaires.

9. Conserver la langue active. Ne jamais traduire, corriger la grammaire ou changer de langue sans demande.

10. Tout message automatique visible est présenté comme 🤖 LAWIM AI.

11. Le footer canonique est : ℹ️ Réponse assistée par LAWIM AI.

12. Aucun résultat LIVE, VERIFIED, COMPLETE ou CERTIFIED sans preuve runtime réelle.

13. Un webhook simulé, un test unitaire, un healthcheck ou un identifiant fournisseur ne prouvent pas la réception réelle par l’utilisateur.

14. Reproduire tout défaut avec un test en échec avant correction.

15. Ne jamais exposer, afficher ou demander un secret déjà disponible dans l’environnement ou deployment/secrets/*.env.

16. Aucun return None silencieux et aucune exception absorbée.

17. L’agent qui implémente ne certifie pas seul son travail.

18. Ne déployer sur OVH qu’après tests, revue indépendante, backup et rollback prêt.
