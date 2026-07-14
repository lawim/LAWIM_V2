# Specification Cible Conversation

Version: 1.0
Date: 2026-07-14
Commit de reference: d30d61e1d89427ece9c180cec4639cce77fdcba3
Statut: CANONICAL

## Statut
Ancien module conversationnel: DELETE. Nouveau module: REBUILD_FROM_ZERO.

## Role
Le domaine Conversation gere les conversations, messages, identites d'interlocuteurs, continuites de canal, ambiguites, handover humain et appels controles aux actions metier. Il ne possede ni matching, ni relation, ni regles financieres.

## Etats cibles
`new`, `identifying_actor`, `selecting_project`, `qualifying`, `waiting_clarification`, `ready_for_search`, `waiting_consent`, `handover_requested`, `closed`.

## Memoire et faits
La memoire canonique est une collection de faits structures avec provenance, statut (`hypothesis`, `pending_confirmation`, `confirmed`, `superseded`) et portee (`conversation`, `project`, `dossier`). Un fait confirme n'est jamais redemande sauf demande de correction ou expiration.

## Comportements
- Reponses courtes par defaut, avec detail sur demande.
- Anti-boucle: pas plus de deux clarifications identiques sans escalade ou reformulation deterministe.
- Fallback deterministe en cas de panne IA.
- Selection explicite du projet si plusieurs projets actifs existent.
- Les actions annoncees doivent etre executees ou marquees comme non executees.
- Le changement de canal conserve l'etat via ChannelIdentity et Project/Dossier.

## Role limite du LLM
Le LLM reformule, extrait, classe linguistiquement et propose des brouillons. Le runtime LAWIM valide, decide, autorise et execute.

## Validation
Le module cible est valide seulement par corpus comportemental multicanal, tests d'integration, tests live et preuve de version deployee selon [20_TESTING_AND_ACCEPTANCE_STANDARD.md](20_TESTING_AND_ACCEPTANCE_STANDARD.md).
