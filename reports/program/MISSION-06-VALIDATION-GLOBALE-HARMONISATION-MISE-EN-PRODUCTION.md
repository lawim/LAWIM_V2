# MISSION 06 - VALIDATION GLOBALE, HARMONISATION ET MISE EN PRODUCTION

## Resume executif

La mission 06 a finalise la coherence de LAWIM_V2 en production. Le frontend livre precedemment reste la source runtime officielle, la page d acces conserve le logo LAWIM et le slogan officiel, et le login admin/agent/owner fonctionne de nouveau sur OVH sans exposer de role a la connexion.

Un correctif de bootstrap a ete ajoute pour synchroniser les comptes demo de production avec le secret `LAWIM_ADMIN_PASSWORD`, puis le compose OVH a ete ajuste pour transmettre ce secret au conteneur `lawim-app`. Le resultat est verifie en production.

## References de livraison

- Commit code principal: `41d4812e`
- Commit precedent frontend/UX: `a38b05ae`
- Artifact de release: `/tmp/lawim_v2_release_41d4812e.tar.gz`
- SHA256 artifact: `c81f9588e15671d9e734f8f94c177c71b089042bb7740c9a82d269a9a895d857`
- Release OVH active: `/opt/lawim/releases/41d4812e`
- Symlink actif: `/opt/lawim/current -> /opt/lawim/releases/41d4812e`

## Source frontend officielle de production

Decision reconfirmee: `code/lawim_v2/static`

Motifs:

- `code/lawim_v2/server.py` sert directement la page d accueil et les assets statiques depuis cette arborescence.
- Le runtime OVH reconstruit `lawim-app` depuis la release versionnee.
- `frontend/apps/web` et `frontend/dist` restent des surfaces de developpement et de validation, pas la source runtime de production.

## Travaux realises

- Synchronisation du bootstrap des credentials demo en fonction de `LAWIM_ADMIN_PASSWORD`.
- Injection de `LAWIM_ADMIN_PASSWORD` dans le conteneur `lawim-app` OVH.
- Recration du conteneur applicatif avec prise en compte du secret.
- Validation de la connexion prod pour:
  - `admin@lawim.app`
  - `agent@lawim.app`
  - `owner@lawim.app`
- Harmonisation documentaire du guide de production.

## Validation locale

Validation cible executee avant la promotion:

- `PYTHONPATH=tests python3 -m unittest tests.test_lawim_v2`
  - 25 tests passes

Validations deja consolidees sur la release precedente:

- `npm run build`
- `npm run test -- --run`

## Validation production

Services:

- `lawim-app` healthy
- `lawim-postgres` healthy
- `lawim-redis` healthy

Health:

- `https://lawim.app/api/health` -> `200`

Authentification:

- `admin@lawim.app` -> `201`, role `admin`
- `agent@lawim.app` -> `201`, role `agent`
- `owner@lawim.app` -> `201`, role `owner`

Controle environnement:

- `LAWIM_ADMIN_PASSWORD` est bien present dans l environnement du conteneur `lawim-app`.
- Le bootstrap a pu synchroniser les comptes demo au demarrage.

## Deploiement OVH

Sequence executee:

1. Construction de la release locale a partir de `HEAD`.
2. Copie de l archive verifiee vers OVH.
3. Extraction dans `/opt/lawim/releases/41d4812e`.
4. Bascule de `/opt/lawim/current`.
5. Recreate du conteneur `lawim-app`.
6. Verifications de services et de login.

## Procedure de rollback

Rollback release:

1. Rebasculer `/opt/lawim/current` vers la release precedente.
2. Recreate `lawim-app`.
3. Revalider `https://lawim.app/` et `https://lawim.app/api/health`.

Rollback credentials:

1. Retirer ou modifier `LAWIM_ADMIN_PASSWORD` cote environnement OVH.
2. Recreate `lawim-app` pour que le bootstrap reapplique les credentials souhaites.

## Rapport de coherence

La coherence globale est maintenue:

- fonctionnelle
- technique
- ergonomique
- documentaire
- operationnelle
- strategique
- deploiement

## Notes

- Les changements hors perimetre deja presents dans le worktree local ont ete conserves sans ecrasement.
- Aucun secret n a ete commit dans Git.
