# Monitoring

Ce dossier porte la fondation documentaire de supervision de LAWIM_V2.

## Role
Reference pour la strategie de supervision, la disponibilite, les metriques techniques, les alertes, les health checks et les tableaux de bord.

## Perimetre
- disponibilite des services et des dependances;
- metriques techniques de runtime et de performance;
- alerting et escalation;
- health checks de type liveness, readiness et startup;
- tableaux de bord d'exploitation;
- integration conceptuelle avec Docker, Nginx, Logging, CI/CD et OVH.

## Signaux techniques
- latence, debit et taux d'erreur;
- reponses 5xx et timeouts;
- CPU, memoire, disque, reseau et redemarrages;
- disponibilite des dependances critiques;
- files d'attente, saturation et blocages quand le service les expose;
- succes ou echec des travaux d'exploitation relies au service.

## Disponibilite
- un service est considere disponible quand son health check liveness est OK et que ses dependances declarees repondent dans la fenetre attendue;
- aucune cible SLO ou SLA n'est figee ici;
- les seuils seront definis par ticket avant activation d'un outil.

## Alertes
- les alertes sont classees par info, warning et critical;
- une alerte critique doit pointer vers un incident ou une action claire;
- les alertes doivent etre actionnables et associees a un owner;
- aucun canal externe n'est configure dans ce dossier.

## Health checks
- liveness: le processus ou le conteneur repond;
- readiness: les dependances minimales sont disponibles;
- startup: l'initialisation est achevee;
- les checks doivent rester rapides, deterministes et sans effet de bord.

## Conventions
- aucun outil de monitoring reel n'est deploye ici;
- aucun secret, jeton, certificat ou identifiant externe;
- aucune configuration de service tiers;
- les dimensions communes sont `service`, `component`, `environment`, `severity`, `signal` et `ticket`;
- les seuils et les noms de signal doivent rester stables et documentes;
- la supervision doit rester compatible avec `logging/` et `docker/logging/`.

## Integration conceptuelle
- Docker: healthchecks de conteneurs, redemarrages et consommation de ressources;
- Nginx: disponibilite de l'amont, reponses HTTP, latence et erreurs d'edge;
- Logging: correlation des evenements, des incidents et des preuves d'exploitation;
- CI/CD: verification avant et apres deploiement, sans activer de pipeline reel ici;
- OVH: disponibilite host, saturation disque/reseau et etat des sauvegardes.

## TODO
- preciser les seuils d'alerte quand les services seront definis;
- figer la convention de dashboard au moment de l'activation d'un outil;
- garder les contrats de supervision separes des composants metier.
