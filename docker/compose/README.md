# Docker Compose

Ce dossier contient la fondation Compose canonique de LAWIM_V2.

Perimetre:
- definition du socle commun Compose;
- conventions de nommage des reseaux et volumes;
- contrat d'environnement par profil;
- structure d'extension pour les futurs services;
- documentation des profils development, staging et production.

Fichiers de reference:
- `docker-compose.base.yml` : base partagee, noms stables, contrat d'environnement et reseaux/volumes;
- `docker-compose.development.yml` : contrat de profil pour le developpement local;
- `docker-compose.staging.yml` : contrat de profil pour la preproduction;
- `docker-compose.production.yml` : contrat de profil pour la production.

Convention de nommage:
- les ressources Compose utilisent le prefixe stable `lawim_v2_`;
- les reseaux reserves sont `lawim_v2_public` et `lawim_v2_private`;
- les volumes reserves sont `lawim_v2_state`, `lawim_v2_shared` et `lawim_v2_cache`;
- les variables d'environnement suivent les noms explicites deja poses par `env/README.md` et ses exemples.

Contrat d'environnement:
- `APP_ENV` identifie l'environnement cible;
- `STACK_PROFILE` identifie le profil Compose actif;
- `LOG_LEVEL` reste `debug` en development et `info` en staging/production;
- `PUBLIC_BASE_URL` reste fourni de l'exterieur;
- `SECRET_PROVIDER` reste externe et aucun secret ne doit etre commite.

Contrat secrets:
- `env/development/.secrets.example`, `env/staging/.secrets.example` et `env/production/.secrets.example` documentent la forme des secrets;
- les fichiers runtime `.secrets.local` restent hors depot et sont montes ou injectes de l'exterieur;
- Compose ne doit jamais lire un secret reel depuis un fichier versionne;
- la separation variables / secrets reste visible dans les overlays et dans les futures definitions de services.

Ordre de couche recommande:
1. charger `docker-compose.base.yml`;
2. ajouter le profil `docker-compose.development.yml`, `docker-compose.staging.yml` ou `docker-compose.production.yml`;
3. ajouter ensuite, si necessaire, les fichiers de ticket suivants qui introduiront des services concrets.

Conventions d'extension:
- cette fondation utilise des fragments `x-` pour documenter les contrats reutilisables;
- `extends` reste reserve aux futurs services concrets quand ils existeront;
- les surcharges sont attendues par superposition de fichiers Compose avec `-f`;
- aucun service metier n'est implemente dans ce ticket.

Validation minimale:
- `docker-compose -f docker/compose/docker-compose.base.yml -f docker/compose/docker-compose.development.yml config`
- `docker-compose -f docker/compose/docker-compose.base.yml -f docker/compose/docker-compose.staging.yml config`
- `docker-compose -f docker/compose/docker-compose.base.yml -f docker/compose/docker-compose.production.yml config`

Preparation de T01.05:
- le prochain ticket doit reutiliser ce contrat sans redefinir les noms de ressources;
- les valeurs reelles d'environnement devront rester hors depot ou etre injectees par la mecanique officielle des environnements;
- Nginx devra consommer ce contrat sans redefinir `APP_ENV`, `STACK_PROFILE`, `LOG_LEVEL`, `PUBLIC_BASE_URL` ou `SECRET_PROVIDER`;
- aucune ouverture de T01.05 n'est requise pour conserver ce contexte.
