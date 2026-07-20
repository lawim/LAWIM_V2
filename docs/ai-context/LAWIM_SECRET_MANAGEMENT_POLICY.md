# LAWIM — Politique de Gestion des Secrets

## Sources autorisées

Les secrets sont chargés depuis :

1. Variables d'environnement du conteneur Docker
2. Fichier `/opt/lawim/secrets/.env` (production — jamais dans Git)
3. Fichiers `deployment/secrets/*.env` (développement local — jamais commit)
4. `CredentialVault` avec `LAWIM_VAULT_KEY` pour les credentials Google Drive

## Interdictions

- Ne jamais commettre de secret dans Git
- Ne jamais transmettre de secret dans un prompt d'agent
- Ne jamais écrire de secret dans un rapport
- Ne jamais journaliser de secret
- Ne jamais inclure le mot de passe principal Docker Hub
- Ne jamais inclure de clé privée SSH dans un fichier `.env`
- Ne jamais exposer de token dans une URL ou un log

## Format autorisé pour les fichiers d'environnement

Un fichier `.env` peut contenir :

```env
OVH_HOST=vps-6da158cc.vps.ovh.net
OVH_USER=ubuntu
OVH_SSH_KEY_PATH=~/.ssh/id_ed25519
DOCKER_USERNAME=laaawim
DOCKER_ACCESS_TOKEN=<token>
GITHUB_TOKEN=<token>
```

La clé privée SSH reste dans `~/.ssh/` avec les permissions `600`.

## Gestion des credentials

- Les credentials Google Drive sont stockés dans `CredentialVault` chiffré avec `LAWIM_VAULT_KEY`
- Les tokens API (Green API, Telegram, DeepSeek, OpenAI, Gemini) sont dans `/opt/lawim/secrets/.env`
- Les mots de passe base de données sont dans `/opt/lawim/secrets/.env`
- Le fichier `deployment/secrets/production.env` contient uniquement `LAWIM_VAULT_KEY`
