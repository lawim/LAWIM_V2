# Logging

Ce dossier reserve la strategie de journalisation de LAWIM_V2.

## Role
Squelette pour les conventions de logs, de correlation, de retention et de supervision cote Docker.

## Portee
- logs applicatifs et techniques;
- niveau, format et structure des messages;
- correlation des executions, requetes et incidents;
- retention, rotation et archivage hors logique metier;
- preparation de l'agregation centralisee;
- integration conceptuelle avec Docker, Nginx, CI/CD et Monitoring.

## Conventions
- stdout et stderr restent la cible par defaut quand c'est possible;
- les niveaux supportes sont DEBUG, INFO, WARNING, ERROR et CRITICAL;
- les identifiants de correlation doivent rester stables et lisibles;
- aucun secret, mot de passe, jeton ou donnee sensible en clair;
- aucune configuration d'outil de collecte ici;
- la structure devra rester compatible avec la supervision future.

## Reutilisation
- reutiliser les conventions communes du dossier `logging/`;
- aligner les noms de flux sur les composants et les tickets;
- garder la rotation et la retention en dehors de la logique metier.

## TODO
- definir les conventions de nommage des flux;
- preciser les regles de retention par environnement;
- documenter le pont avec le Monitoring futur.
