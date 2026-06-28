# Docker

Ce dossier porte la fondation Docker de LAWIM_V2.

Perimetre T01.02:
- strategie Docker;
- image de base partagee;
- conventions de build;
- conventions de tagging;
- organisation des images de developpement, staging et production.

Principes:
- aucune logique metier dans les images;
- aucun secret en clair dans le depot;
- configuration injectee par variables d'environnement ou arguments de build;
- separation nette entre les couches base, developpement, staging et production;
- versions et tags explicites, reproductibles et tracables.

Arborescence:
- `Dockerfile.base` : base commune minimale et reutilisable;
- `images/` : overlays et conventions d'images par environnement;
- `compose/` : reserve a T01.03;
- `nginx/` : reserve a T01.05;
- `logging/` : strategie de journalisation;
- `monitoring/` : strategie de supervision.

Ordre de construction:
1. construire `Dockerfile.base`;
2. taguer l'image de base de maniere immuable;
3. construire l'overlay de developpement;
4. construire l'overlay de staging;
5. construire l'overlay de production;
6. promouvoir le meme digest du socle partage entre environnements quand c'est possible.
