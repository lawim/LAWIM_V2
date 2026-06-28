# Docker Compose

Ce dossier reserve l'organisation de la stack Compose.

Principes:
- socle commun unique;
- surcharges par environnement;
- profils d'execution explicites;
- reseaux et volumes nommes de facon stable;
- aucun port ou volume sensible sans justification.

Fichiers reserves:
- `compose.base.yml`;
- `compose.override.yml`;
- `compose.development.yml`;
- `compose.staging.yml`;
- `compose.production.yml`;
- `compose.observability.yml`.
