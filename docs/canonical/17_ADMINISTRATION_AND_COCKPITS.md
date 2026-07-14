# Administration Et Cockpits

Version: 1.0
Date: 2026-07-14
Commit de reference: d30d61e1d89427ece9c180cec4639cce77fdcba3
Statut: CANONICAL

## Role
Les Cockpits sont des surfaces de pilotage: utilisateur, agent, manager, admin, investisseur, partenaire et financier. Ils affichent l'etat canonique et declenchent des actions autorisees.

## Regles
- Un cockpit ne possede pas la logique metier; il consomme des API de domaine.
- Les actions sensibles exigent role, permission, contexte et audit.
- Les vues doivent distinguer cible, implemente, verifie et a reconstruire.
