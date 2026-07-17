# LAWIM — Google Drive Backup

## Identity
| Champ | Valeur |
|---|---|
| Projet | LAWIM_V2 |
| Commit | d793059c |
| Tag | lawim-v2-whatsapp-telegram-hotfix |
| Date de copie | 2026-07-17 |

## Structure
```
LAWIM/
├── PROJECT/       → Code source complet du projet
├── BACKUPS/       → Sauvegardes des versions certifiées
├── DATABASE/      → Dumps PostgreSQL
├── RELEASES/      → Manifestes de release
├── CONFIGURATION/ → Fichiers de configuration non sensibles
├── RESTORE/       → Instructions de restauration
├── MANIFESTS/     → Checksums et manifestes
└── CHECKSUMS/     → SHA-256 des données stockées
```

## Procédure de restauration
1. Cloner le dépôt depuis GitHub : `git clone git@github.com:lawim/LAWIM_V2.git`
2. Restaurer la base PostgreSQL à partir du dump dans `DATABASE/`
3. Restaurer les secrets depuis le gestionnaire de secrets de production
4. Construire et déployer avec Docker Compose

## Éléments exclus
- `.git/` — historique versionné sur GitHub
- `node_modules/` — reconstitué via `npm install`
- `__pycache__/`, `.pytest_cache/`, `dist/`, `build/` — artefacts générés
- `.env`, `secrets/`, `*.dump`, `*.tar.gz` — fichiers sensibles ou volumineux

## Avertissement
Ce dossier ne contient aucun secret de production. Les clés API, mots de passe et tokens
sont gérés exclusivement via le gestionnaire de secrets du serveur OVH.
