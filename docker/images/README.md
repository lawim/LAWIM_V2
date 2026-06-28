# Docker Images

Ce dossier porte les overlays d'images derives de `docker/Dockerfile.base`.

Perimetre T01.02:
- organisation des images de developpement, staging et production;
- conventions de build;
- conventions de tagging;
- promotion du digest du socle partage entre environnements.

Principes:
- images minimales et reproductibles;
- versions figees et tags explicites;
- separation runtime, build et outils;
- aucun secret dans une image;
- build previsible, documente et reutilisable.

Arborescence reservee:
- `development/Dockerfile`;
- `staging/Dockerfile`;
- `production/Dockerfile`.

Ordre de build:
1. construire l'image de base;
2. taguer la base avec un tag immuable;
3. construire l'overlay developpement a partir de cette base;
4. construire l'overlay staging a partir de la meme base;
5. construire l'overlay production a partir de la meme base.

Conventions de tagging:
- `lawim/base:local` pour le bootstrapping local et les boucles de travail;
- `lawim/base:<version>` pour la base partagee;
- `lawim/dev:<version>-dev.<gitsha>` pour le developpement;
- `lawim/staging:<version>-rc.<n>` pour la preproduction;
- `lawim/prod:<version>` pour la production.

Regle de promotion:
- ne pas reconstruire un socle deja valide si son digest peut etre promu tel quel;
- ne pas utiliser `latest` comme reference de promotion;
- conserver un tag lisible pour chaque environnement.
