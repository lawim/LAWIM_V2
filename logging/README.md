# Logging

Ce dossier reserve la strategie de journalisation de LAWIM_V2.

## Role
Squelette pour les conventions de logs, de correlation et de retention.

## Usage futur
- logs applicatifs et techniques;
- correlation des requetes et incidents;
- rotation ou retention hors logique metier;
- formats structures quand ils seront utiles.

## Conventions
- logs sur stdout et stderr quand c'est possible;
- aucun secret dans les journaux;
- pas de configuration metier ici;
- la structure devra rester compatible avec la supervision.

## TODO
- definir les formats cibles;
- documenter la correlation des evenements;
- fixer les regles de retention et de rotation.
