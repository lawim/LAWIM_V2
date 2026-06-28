# Docker

Ce dossier regroupe la base conteneurisee de LAWIM_V2.

Principes:
- aucune logique metier dans les images;
- configuration injectee par variables d'environnement;
- separation nette entre development, staging et production;
- aucun secret en clair dans le depot.

Sous-dossiers:
- `images/` : conventions des images, des versions et du tagging;
- `compose/` : organisation de la stack et des profils d'execution;
- `nginx/` : reverse proxy, TLS, headers et routage;
- `logging/` : strategie de journalisation;
- `monitoring/` : strategie de supervision.
