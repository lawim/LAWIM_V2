# Projets Et Dossiers

Version: 1.0
Date: 2026-07-14
Commit de reference: d30d61e1d89427ece9c180cec4639cce77fdcba3
Statut: CANONICAL

## Definition
Un projet represente un objectif immobilier persistant appartenant a un utilisateur ou une organisation. Un dossier represente le suivi operationnel d'un projet: faits confirmes, etapes, documents, recherches, propositions, relations, visites, offres et audit.

## Regles
- Un dossier n'est pas une session conversationnelle.
- Un dossier n'est pas cree pour chaque message.
- Un dossier ne doit jamais etre repris sans choix explicite lorsque plusieurs dossiers actifs sont possibles.
- Les etats conversationnels temporaires restent dans Conversation ou Qualification, pas dans Dossier.
- Les decisions engageantes sont historisees et attribuees a un acteur.

## Cycle de vie
`draft` -> `qualified` -> `active` -> `in_follow_up` -> `closed` ou `cancelled`. `suspended` peut interrompre le flux. Toute reouverture est auditee.
