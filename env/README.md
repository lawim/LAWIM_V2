# Environnements

Ce dossier reserve les conventions d'environnement de LAWIM_V2.

Arborescence attendue:
- `development/`;
- `staging/`;
- `production/`;
- `secrets/` pour la strategie des secrets et les modeles generiques.

Principes:
- chaque environnement a ses variables non secretes et ses secrets distincts;
- les fichiers `.env.example` documentent uniquement les variables;
- les fichiers `.secrets.example` documentent uniquement la forme des secrets;
- les valeurs reelles restent hors depot;
- les noms de variables restent stables, explicites et sans doublon;
- `SECRET_PROVIDER` reste externe et ne doit jamais pointer vers un secret commite.

Modeles disponibles:
- `development/.env.example`;
- `staging/.env.example`;
- `production/.env.example`.

Modeles secrets:
- `development/.secrets.example`;
- `staging/.secrets.example`;
- `production/.secrets.example`;
- `secrets/README.md` pour la convention centrale.

Integration:
- Docker Compose consomme les variables d'environnement non secretes;
- les secrets sont injectes a l'execution depuis l'exterieur;
- CI/CD peut fournir des secrets via un coffre du fournisseur, jamais via des fichiers versionnes;
- OVH et les futurs serveurs ne deviennent jamais des coffres a secrets.

Aucun secret reel ne doit etre stocke ici.
