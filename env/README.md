# Environnements

Ce dossier reserve les conventions d'environnement de LAWIM_V2.

Arborescence attendue:
- `development/`;
- `staging/`;
- `production/`.

Principes:
- chaque environnement a ses variables et ses secrets distincts;
- les fichiers de reference restent non secrets;
- les valeurs reelles sont fournies hors depot ou par CI/CD;
- les noms de variables restent stables et explicites.

Modeles disponibles:
- `development/.env.example`;
- `staging/.env.example`;
- `production/.env.example`.

Aucun secret reel ne doit etre stocke ici.
