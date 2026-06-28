# Logging

Ce dossier reserve la strategie de journalisation de LAWIM_V2.

## Role
Reference documentaire pour les conventions de logs du programme.

## Objectifs
- rendre les journaux lisibles et exploitables;
- permettre la correlation des evenements, requetes et incidents;
- encadrer la retention et la rotation hors logique metier;
- preparer l'agregation centralisee sans imposer d'outil;
- rester compatible avec Docker, Nginx, CI/CD et Monitoring.

## Conventions
- stdout et stderr quand c'est possible pour les composants conteneurises;
- niveaux DEBUG, INFO, WARNING, ERROR et CRITICAL;
- format stable et structure quand cela apporte de la valeur;
- identifiants de correlation explicites et persistants;
- aucun secret ni donnee sensible en clair;
- retention et rotation definies hors du code applicatif.

## Nommage
- un journal doit indiquer son domaine, son composant et sa finalite;
- les noms doivent rester courts et stables;
- les flux applicatifs et techniques doivent rester distingues;
- les messages doivent permettre le filtrage par ticket ou par execution.

## Integration conceptuelle
- Docker: sortie standard et collecte future;
- Nginx: logs de requetes et d'erreurs;
- CI/CD: logs de pipeline et de promotion;
- Monitoring: consommation future des journaux pour alertes et tableaux de bord.

## TODO
- preciser les conventions de correlation;
- documenter la rotation et la retention par environnement;
- garder l'outillage de collecte hors du perimetre de ce dossier.
