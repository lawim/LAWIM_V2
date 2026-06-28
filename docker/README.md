# Docker

Ce dossier porte la fondation conteneurisee de LAWIM_V2.

Perimetres deja poses:
- T01.02 a fixe la base Docker partagee;
- T01.03 a fixe la fondation Docker Compose;
- T01.05 fixe maintenant la fondation Nginx;
- les prochains tickets doivent reutiliser ces contrats sans les dupliquer.

Principes:
- aucune logique metier dans les images;
- aucun secret en clair dans le depot;
- configuration injectee par variables d'environnement ou arguments de build;
- separation nette entre les couches base, developpement, staging et production;
- versions et tags explicites, reproductibles et tracables.

Arborescence:
- `Dockerfile.base` : base commune minimale et reutilisable;
- `images/` : overlays et conventions d'images par environnement;
- `compose/` : fondation Compose partagee, profils et conventions de nommage;
- `nginx/` : reverse proxy, TLS, headers, certificats et journalisation;
- `logging/` : strategie de journalisation;
- `monitoring/` : strategie de supervision.

Ordre de construction:
1. construire `Dockerfile.base`;
2. taguer l'image de base de maniere immuable;
3. construire l'overlay de developpement;
4. construire l'overlay de staging;
5. construire l'overlay de production;
6. brancher Compose sur les contrats d'environnement;
7. brancher Nginx sur les contrats d'environnement et les certificats montes;
8. promouvoir le meme digest du socle partage entre environnements quand c'est possible.
