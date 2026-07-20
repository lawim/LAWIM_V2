# LAWIM V2 — VS Code Instruction Audit

**Date :** 2026-07-20
**HEAD initial :** `c2c5bf64`
**Branche locale observée :** `main`

## Baseline Git

La baseline locale est propre et synchronisée selon les références déjà présentes :

- branche : `main`
- `origin/main...HEAD` : `0 0`
- worktree : propre

Limite d'exécution : `git fetch origin --tags` a échoué car `.git/FETCH_HEAD` est en lecture seule dans la session. La création de branche et le push ne sont donc pas possibles depuis ce contexte.

## Synthèse interne du contexte canonique

| Axe | Synthèse |
| --- | --- |
| Identité de LAWIM | Plateforme immobilière intelligente et opérationnelle au Cameroun. |
| Périmètre métier | Recherche, location, vente, publication, matching, visites, transaction, documents, paiements, réclamations et suivi. |
| Architecture conversationnelle | Message entrant, normalisation, acteur, conversation, mémoire, langue, intention, critères, fusion, qualification, prochaine action, formulation, validation, rendu, persistance et livraison. |
| Rôle limité du LLM | Le LLM reformule et rédige. Il ne décide pas l'intention, l'état, la disponibilité, la prochaine action ou le handover. |
| Règles de mémoire | Les critères déjà fournis restent dans l'état conversationnel et ne doivent pas être redemandés. |
| Règles de qualification | La qualification métier et ProgressiveWizard déterminent la prochaine question utile, une seule à la fois. |
| Règles de preuve runtime | Aucun statut LIVE, VERIFIED, COMPLETE ou USER_ACCEPTED sans preuve réelle de bout en bout. |
| Règles relatives aux secrets | Ne jamais exposer, commettre, journaliser ou demander un secret déjà disponible dans l'environnement ou `deployment/secrets/*.env`. |
| Incident conversationnel actuel | ConversationStateEngine validé localement et ProgressiveWizard connecté au runtime ; déploiement OVH et recette utilisateur réelle encore requis. |

## Fichiers Audités

| Fichier | Résultat |
| --- | --- |
| `AGENTS.md` | Conforme au contexte canonique LAWIM. |
| `.opencode/AGENTS.md` | Conforme comme cadrage OpenCode, avec renvoi aux documents projet. |
| `frontend/docs/AGENTS.md` | Documentation runtime frontend, non spécifique VS Code. |

## Instructions VS Code Existantes

Aucun fichier VS Code existant n'a été trouvé avant intervention :

- `.github/copilot-instructions.md` absent ;
- `.github/instructions/*.instructions.md` absent ;
- `.github/prompts/*.prompt.md` absent.

## Contradictions Détectées

| Sujet | Observation | Traitement |
| --- | --- | --- |
| Footer IA | `LAWIM_CONVERSATION_CONTRACT.md` définit `ℹ️ LAWIM AI peut se tromper. Vérifiez les informations importantes.` alors que la mission demande `ℹ️ Réponse assistée par LAWIM AI.` pour VS Code. | Écart consigné. Les instructions VS Code suivent la mission sans modifier le document canonique. |

## Instructions Obsolètes Ou Duplications

Aucun ancien prompt VS Code ni ancienne instruction Copilot ne présente LAWIM comme assistant neutre.

Aucune instruction VS Code ne redirige vers des plateformes externes.

Aucune instruction VS Code ne donne au LLM le contrôle métier.

## Livrables Créés

- `.github/copilot-instructions.md`
- `.github/instructions/lawim-conversation.instructions.md`
- `.github/instructions/lawim-testing-evidence.instructions.md`
- `.github/prompts/lawim-preflight.prompt.md`
- `scripts/validation/validate_vscode_lawim_context.py`
- `scripts/validation/test_vscode_lawim_understanding.py`
