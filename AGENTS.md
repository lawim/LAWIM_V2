# LAWIM — Règles Permanentes des Agents

1. Lire les documents de `docs/ai-context/` avant toute intervention.

2. LAWIM traite directement les demandes immobilières de son périmètre.
   Ne jamais rediriger spontanément vers une plateforme, une agence ou
   un service immobilier externe.

3. Le moteur métier détermine l'intention, l'état et la prochaine action.
   Le LLM formule uniquement la réponse.

4. Conserver tous les critères déjà fournis dans l'état conversationnel.

5. Poser une seule prochaine question utile.

6. Tous les messages automatiques visibles sont signés 🤖 LAWIM AI.

7. Aucun handover sans `handover_id` persistant et raison valide.

8. Aucun résultat LIVE, VERIFIED ou COMPLETE sans preuve runtime réelle.

9. Reproduire chaque défaut avec un test en échec avant correction.

10. Ne jamais exposer ni demander un secret déjà disponible dans
    l'environnement ou `deployment/secrets/*.env`.

11. Aucun `return None` silencieux et aucune exception absorbée.

12. L'exécuteur ne certifie pas seul son propre travail.
