# Infra

Ce dossier regroupe les elements d'infrastructure hors conteneurs.

## Role
Base documentaire des futurs points d'entree techniques hors Docker.

## Usage futur
- preparation des environnements;
- scripts d'installation et de verification;
- conventions de reprise et de controle;
- references operationnelles rattachees aux autres dossiers.

## Conventions
- aucun secret dans le depot;
- aucune configuration metier ici;
- scripts idempotents et traces quand ils seront ajoutes;
- chaque sous-dossier doit garder un perimetre clair.

## TODO
- brancher les scripts `install.sh` et `check-env.sh`;
- documenter les prerequis techniques par environnement;
- garder les integrations externes dans leurs dossiers dedies.
