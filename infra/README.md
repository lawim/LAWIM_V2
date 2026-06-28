# Infra

Ce dossier regroupe la preparation d'infrastructure hors conteneurs de LAWIM_V2.

## Role

Point d'ancrage pour l'architecture OVH, les scripts operationnels et les conventions d'exploitation hors Docker.

## Arborescence

- `ovh/` : architecture cible OVH, reseau, DNS conceptuel, stockage et administration;
- `scripts/` : familles de scripts operationnels et conventions d'automatisation;
- `install.sh` : squelette de preparation d'hebergement;
- `check-env.sh` : squelette de verification des prerequis.

## Principes

- aucune ressource OVH reelle dans le depot;
- aucun identifiant, aucune cle et aucun certificat en clair;
- aucune configuration metier dans ce dossier;
- les scripts futurs doivent etre idempotents, explicites et traces;
- les conventions documentees ici doivent rester compatibles avec Docker, Docker Compose et Nginx.

## Integration

- Docker et Docker Compose consomment les contrats d'environnement;
- Nginx expose la partie publique de la stack;
- OVH porte l'hebergement cible et les points de reprise;
- les sauvegardes suivent le referentiel de stockage officiel;
- les futures automatisations doivent reutiliser ces conventions sans les redefinir.

## Preparation

- la fondation reste documentaire;
- les helpers racine servent de points d'entree futurs;
- les limites de secrets restent externes au depot;
- la reprise d'activite doit rester lisible et testable.
