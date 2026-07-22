# LAWIM — Règles Permanentes des Agents

## 1. Lecture obligatoire avant modification

Avant toute intervention, un agent DOIT lire les documents suivants dans leur
dernière version à jour :

- `LAWIM_CONTEXT.md` — contexte complet du projet, architecture, programmes
- `AGENTS.md` — presentes regles
- `lawim_program_status.yaml` — etat courant des programmes
- `docs/canonical/24_GLOSSARY.md` — glossaire canonique
- `docs/ai-context/LAWIM_CANONICAL_SCOPE.md` — perimetre LAWIM
- `docs/ai-context/LAWIM_CONVERSATION_CONTRACT.md` — contrat conversationnel
- `docs/ai-context/LAWIM_ENGINEERING_RULES.md` — regles techniques permanentes
- `docs/ai-context/LAWIM_PRODUCTION_EVIDENCE_POLICY.md` — politique de preuve
- `docs/ai-context/LAWIM_SECRET_MANAGEMENT_POLICY.md` — gestion des secrets
- `docs/canonical/01_PRINCIPLES_AND_GOVERNANCE.md` — principes et gouvernance
- `docs/canonical/15_AI_GOVERNANCE.md` — gouvernance IA
- Toute ADR applicable au composant concerne
- Toute specification de programme applicable

## 2. Verification pre-modification

Avant TOUTE modification du code, du schema ou de la configuration, un agent
DOIT executer les etapes suivantes :

1. Verifier l'etat Git (branche, HEAD, fichiers modifies non commites)
2. Lire les documents canoniques du composant concerne
3. Inspecter le code existant du composant
4. Rechercher les composants similaires existants
5. Identifier les contrats publics (APIs, evenements, modeles)
6. Executer les tests de reference pour etablir la ligne de base
7. Resumer sa comprehension du changement propose
8. Signaler toute contradiction trouvee dans le code ou la documentation
9. Identifier les risques du changement propose

## 3. Perimetre LAWIM

LAWIM traite directement les demandes immobilieres de son perimetre.

Ne jamais rediriger spontanement vers une plateforme, une agence ou un service
immobilier externe, notamment :

- Jumia House, SeLoger, Leboncoin, Facebook, Lamudi
- agences immobilieres externes
- plateformes concurrentes
- services immobiliers externes

LAWIM utilise exclusivement ses propres biens, services, moteur de recherche,
moteur de matching, CRM, agents, workflows et ressources documentaires.

## 4. Separation metier / LLM

Le moteur metier determine l'intention, l'etat et la prochaine action.

Le LLM formule uniquement la reponse.

- Le LLM peut extraire, classifier, reformuler, resumer, traduire et rediger
- Le LLM ne peut pas decider de l'intention metier, de l'etat de la
  conversation, de la prochaine etape metier, de la disponibilite d'un bien,
  du statut d'une visite, du statut d'un paiement ou de la creation d'un
  handover
- Le code metier decide ; le LLM formule

## 5. Signature des messages

Tous les messages automatiques visibles sont signes `🤖 LAWIM AI`.

Le footer canonique est :

- Francais : `ℹ️ LAWIM AI peut se tromper. Verifiez les informations importantes.`
- Anglais : `ℹ️ LAWIM AI may make mistakes. Verify important information.`
- Pidgin : `ℹ️ LAWIM AI fit mistake. Check important info.`

Le footer doit comporter au maximum dix mots. Il doit etre discret, non
bloquant et separe du contenu principal.

Une erreur de footer ne doit jamais empecher la reponse principale.

## 6. Handover

Aucun handover sans `handover_id` persistant et raison valide.

Un handover humain necessite obligatoirement :

- `handover_required = true`
- `handover_id` persistant
- raison explicite
- equipe cible
- statut persistant
- audit

Aucune salutation ou demande ordinaire ne doit provoquer automatiquement un
handover.

## 7. Preuve de production

Aucun resultat LIVE, VERIFIED ou COMPLETE sans preuve runtime reelle.

Les elements suivants ne permettent PAS de declarer une fonctionnalite
operationnelle sur un canal reel :

- code present dans le depot
- tests unitaires reussis
- build reussi
- conteneur Docker healthy
- healthz retourne 200
- readyz retourne 200
- webhook configure dans l'API
- payload simule accepte par l'endpoint
- Green API retourne authorized
- Telegram getMe retourne ok
- tag Git cree
- rapport redige

Pour declarer un canal reel operationnel, fournir pour chaque message de test :

1. message reel envoye par un utilisateur
2. webhook reel recu et horodate
3. correlation_id ou identifiant de bout en bout
4. pipeline conversationnel execute (intention, qualification, agent)
5. reponse generee avec contenu contextuel
6. adaptateur sortant appele avec identifiant fournisseur
7. identifiant fournisseur obtenu (idMessage WhatsApp, message_id Telegram)
8. reponse recue sur le terminal utilisateur
9. contenu de la reponse verifie (identite, footer, contexte)
10. logs complets sans secret

## 8. Secrets

Ne jamais exposer ni demander un secret deja disponible dans l'environnement
ou `deployment/secrets/*.env`.

Interdictions absolues :

- Ne jamais commettre de secret dans Git
- Ne jamais transmettre de secret dans un prompt d'agent
- Ne jamais ecrire de secret dans un rapport
- Ne jamais journaliser de secret
- Ne jamais inclure le mot de passe principal Docker Hub
- Ne jamais inclure de cle privee SSH dans un fichier .env
- Ne jamais exposer de token dans une URL ou un log

## 9. Gestion des erreurs

Aucun `return None` silencieux et aucune exception absorbee.

- Toute fonction qui retourne `None` doit le faire explicitement
- Toute exception capturee doit etre journalisee (sans secret) et traitee
- Les logs ne doivent jamais contenir de mots de passe, tokens, cles ou
  donnees personnelles
- Un `except Exception: pass` est strictement interdit

## 10. Certification

L'executeur ne certifie pas seul son propre travail.

Toute certification doit etre validee par un pair ou un reviseur independant.

Les tests simules (mocks, webhooks simules) prouvent le code, pas le
fonctionnement reel.

Les tags Git ne constituent pas une preuve runtime.

## 11. Tests et reproduction

Reproduire chaque defaut avec un test en echec avant correction.

- Ecrire d'abord un test qui echoue et capture le defaut
- Verifier que le test echoue
- Corriger le code
- Verifier que le test passe
- Verifier qu'aucun test existant n'est regresse

## 12. Developpement

- Conserver tous les criteres deja fournis dans l'etat conversationnel
- Poser une seule prochaine question utile par reponse
- Utiliser les services, modules et packages existants
- Ne pas creer de nouveaux chemins paralleles
- Toute nouvelle fonctionnalite doit emprunter le pipeline existant ou
  l'etendre, jamais le contourner

## 13. Politique Git

- une mission = une branche
- commits cibles (un commit par changement logique)
- tests avant fusion
- worktree propre a la cloture
- `origin/main...HEAD = 0 0`

## 14. Rappels

- LAWIM n'est pas un chatbot. LAWIM est une plateforme immobiliere
  intelligente et operationnelle.
- Une conversation ne constitue pas un projet.
- Un message ne constitue pas une decision.
- Une decision ne constitue pas une execution.
- Une execution automatisee ne constitue pas necessairement une preuve reelle.
- Un test unitaire ne prouve pas une integration reelle.
- Un commit ne prouve pas un deploiement.
- Un service sain ne prouve pas le fonctionnement du parcours metier.
