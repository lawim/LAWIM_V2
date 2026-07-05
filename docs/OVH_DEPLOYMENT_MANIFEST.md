# OVH_DEPLOYMENT_MANIFEST

## Objectif

Ce document resume la projection minimale de LAWIM_V2 destinee a OVH. Le manifeste detaille et la version de release vivent dans `release/manifests/DEPLOYMENT_MANIFEST.md`.

## Deployed on OVH

Le paquet OVH doit contenir uniquement ce qui est necessaire a l'execution:

- `Dockerfile`, `sitecustomize.py`, `pyproject.toml`, `requirements.txt`, `requirements-postgresql.txt`;
- le runtime de [`code/lawim_v2/`](../code/lawim_v2/), y compris `i18n.py`, le geo runtime (`geo_domain.py`, `geo_reference.py`, `geocoding_provider.py`, `services.py`, `dto.py`) et le curated bundle [`code/lawim_v2/data/cameroon_locations.json`](../code/lawim_v2/data/cameroon_locations.json), mais sans `migration.py`;
- le frontend de [`frontend/`](../frontend/) sans `docs/`, `reports/`, `tests/`, `node_modules/` ni `dist/`;
- les contrats de base de donnees et les migrations necessaires dans [`prisma/`](../prisma/);
- les manifests de deploiement dans [`compose/`](../compose/) et [`deployment/compose/`](../deployment/compose/);
- les images et scripts de deployment dans [`deployment/docker/`](../deployment/docker/), [`deployment/nginx/`](../deployment/nginx/), [`deployment/systemd/`](../deployment/systemd/), [`deployment/health/`](../deployment/health/), [`deployment/server/scripts/`](../deployment/server/scripts/), [`deployment/scripts/`](../deployment/scripts/) et [`deployment/backup/`](../deployment/backup/), y compris les gabarits PostgreSQL `postgres-init.sql` et `postgresql.conf` montes par la compose prod;
- les exemples de configuration dans [`env/`](../env/) et [`deployment/environments/production/`](../deployment/environments/production/);
- les scripts de lancement validés pour la production, par exemple [`scripts/run-compose-prod.sh`](../scripts/run-compose-prod.sh).

## Conserved on distributed servers

Les serveurs distribues conservent uniquement les donnees d'execution:

- volumes applicatifs;
- medias et fichiers utilisateur;
- journaux de production;
- sauvegardes planifiees;
- secrets d'execution injectes par l'environnement;
- certificats TLS et parametres reseau propres au serveur.

## Stays local in the master repository

Le depot maitre conserve tout ce qui sert a la certification, a l'analyse et a la gouvernance:

- [`docs/`](../docs/), hors manifestes de deploiement;
- [`reports/`](../reports/);
- [`prompts/`](../prompts/);
- [`implementation/`](../implementation/);
- [`legacy/`](../legacy/);
- [`tests/`](../tests/);
- [`release/`](../release/), qui porte la projection et la documentation de release;
- les scripts de validation, de benchmark et de generation de tests;
- le scaffold local de migration dans [`code/lawim_v2/migration.py`](../code/lawim_v2/migration.py) et sa documentation [`docs/MIGRATION_FRAMEWORK.md`](../docs/MIGRATION_FRAMEWORK.md), tant que la phase AAF n'est pas lancee.

## Archived on external disk

L'archivage externe conserve les elements qui ne doivent pas encombrer le serveur de production:

- dumps de base de donnees;
- sauvegardes froides;
- exports historiques;
- journaux archives;
- preuves de validation et rapports de certification;
- artefacts volumineux generes pendant les repetitions de migration.

## Governance rules

- Aucun secret reel ne doit etre commite dans le depot maitre.
- Aucun artefact de test ne doit etre inclus dans le paquet OVH.
- Aucun schema de base de donnees n'est modifie par ce document.
- Aucune migration n'est lancee par ce manifest.
