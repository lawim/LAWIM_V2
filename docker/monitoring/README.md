# Monitoring

Ce dossier reserve le contrat de supervision cote Docker.

## Role
Squelette pour les health checks conteneur, la disponibilite des services Compose, les metriques runtime et la preparation des tableaux de bord.

## Portee
- health checks des conteneurs et des services Compose;
- signaux de redemarrage, saturation et indisponibilite;
- exposition future de metriques par conteneur, sans outillage ici;
- relation avec les journaux techniques et les alertes;
- integration conceptuelle avec Nginx, Logging, CI/CD et OVH.

## Conventions
- aucun exporter, agent, sidecar ou demon de supervision n'est active ici;
- aucune configuration d'outil tiers n'est figee;
- les health checks doivent etre deterministes, rapides et sans effet de bord;
- un health check Compose doit refleter l'etat d'exploitation utile, pas seulement le fait que le processus tourne;
- l'echec doit signaler une indisponibilite reelle, pas un detail interne;
- un `healthy` local n'est pas une validation fonctionnelle complete.

## Utilisation future
- distinguer liveness, readiness et startup quand les services applicatifs l'exigeront;
- relier les checks aux noms de services, aux profils Compose et aux environnements;
- garder les identifiants de metriques stables pour la correlation avec logging.

## Integration conceptuelle
- Docker/Compose: healthcheck, ordre de demarrage et relance de services;
- Nginx: verification de l'amont et de la reponse HTTP;
- Logging: correlation des incidents et preuves de diagnostic;
- CI/CD: smoke checks et gates de livraison;
- OVH: etat du host, espace disque et disponibilite reseau.

## TODO
- definir les endpoints de health pour les services applicatifs quand ils seront ouverts;
- formaliser le modele de dashboard et d'alerte;
- garder l'outillage hors du perimetre.
