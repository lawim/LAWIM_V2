# Nginx

Ce dossier porte la fondation reverse proxy de LAWIM_V2.

Perimetre T01.05:
- architecture du reverse proxy;
- conventions de configuration;
- structure des virtual hosts;
- organisation des certificats;
- preparation HTTPS;
- integration avec Docker Compose;
- conventions de journalisation Nginx;
- preparation de la production.

Principes:
- aucun domaine reel;
- aucun certificat reel;
- aucune logique metier;
- aucun deploiement;
- un `default.conf` de base et des reperes reutilisables;
- les virtual hosts futurs vivent dans `conf.d/`;
- les fragments reutilisables vivent dans `snippets/`;
- les certificats sont documentes mais jamais commites.

Arborescence:
- `default.conf` : serveur par defaut, redirection HTTP vers HTTPS, proxy d'amont et health check;
- `conf.d/` : futurs virtual hosts et surcharges de routage;
- `snippets/` : fragments reutilisables pour headers, proxy et TLS;
- `certs/` : politique de stockage des certificats et des cles;
- journalisation : logs d'acces et d'erreur envoyes vers stdout/stderr.

Integration Docker Compose:
- le service Nginx devra monter ce dossier en lecture seule;
- `default.conf` sera la base commune;
- les valeurs d'environnement proviennent du contrat etabli par T01.04;
- les services amonts restent definis par Compose.

Preparation HTTPS:
- les ports 80 et 443 sont reserves;
- 80 redirige vers 443;
- 443 attend des chemins de certificats montes depuis l'exterieur;
- les certificats locaux de developpement restent hors depot.

Preparation de production:
- `server_name` final sera injecte par l'environnement ou par une surcharge future;
- la journalisation doit rester exploitable;
- les en-tetes de securite sont poses au niveau du reverse proxy;
- aucun point d'entree metier ne doit etre expose directement.
