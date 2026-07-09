# MISSION-08-3-AUTH-ACCESS-DEMO-ACCOUNTS

## Résumé Exécutif

Cette mission a corrigé le blocage d’authentification constaté en recette réelle et a remis la page d’accès et les comptes de démonstration en conformité avec la convention officielle LAWIM.

Le problème racine provenait de deux écarts côté production :

- la base PostgreSQL distante était restée sur un schéma ancien sans `username` ni `phone_e164` ;
- le bootstrap de démarrage ne synchronisait qu’un seul compte démo et un override `LAWIM_ADMIN_PASSWORD` écrasait le mot de passe standard du compte admin en production.

La correction finale a :

- appliqué la migration de compatibilité PostgreSQL au démarrage ;
- synchronisé automatiquement les 5 comptes de démonstration standards ;
- accepté la connexion par email, username ou téléphone ;
- neutralisé l’override admin en production pour préserver les identifiants démo officiels ;
- validé la production avec `/api/health` et les 5 comptes standards.

## Problèmes Détectés

1. Le login admin échouait en production.
2. Le schéma PostgreSQL de production n’avait pas encore les colonnes `username` et `phone_e164`.
3. La base de production contenait seulement 3 utilisateurs au lieu des 5 comptes standards.
4. L’override `LAWIM_ADMIN_PASSWORD` modifiait le compte admin en production et cassait la convention de démonstration.

## Corrections Réalisées

### Authentification

- Acceptation du login par `identifier` unique.
- Résolution du compte via email, username ou téléphone.
- Maintien du formulaire d’accès simplifié.

### Bootstrap de production

- Ajout de la migration PostgreSQL de compatibilité sur l’initialisation du repository.
- Ajout d’une synchronisation déterministe des 5 comptes démo standards au démarrage.
- Conservation des mots de passe standards en production.
- Ignorance de `LAWIM_ADMIN_PASSWORD` en production pour ne pas casser les comptes de démonstration officiels.

### Documentation et gouvernance

- Mise à jour du journal des décisions.
- Mise à jour de la documentation d’exploitation.
- Mise à jour des tests de non-régression auth.

## Fichiers Modifiés

- [code/lawim_v2/bootstrap.py](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/code/lawim_v2/bootstrap.py)
- [code/lawim_v2/db.py](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/code/lawim_v2/db.py)
- [code/lawim_v2/persistence.py](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/code/lawim_v2/persistence.py)
- [code/lawim_v2/postgresql_repository.py](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/code/lawim_v2/postgresql_repository.py)
- [code/lawim_v2/repository_contract.py](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/code/lawim_v2/repository_contract.py)
- [docs/PRODUCTION.md](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/docs/PRODUCTION.md)
- [docs/WORKFLOWS.md](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/docs/WORKFLOWS.md)
- [.lawim/history/decision-log.md](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/.lawim/history/decision-log.md)
- [tests/test_lawim_v2.py](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/tests/test_lawim_v2.py)
- [tests/test_rc_postgresql.py](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/tests/test_rc_postgresql.py)
- [frontend/dist/index.html](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/frontend/dist/index.html)
- [frontend/dist/sw.js](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/frontend/dist/sw.js)

## Comptes De Démonstration

Les comptes standards validés en production sont :

| Usage | Identifiant | Username | Téléphone | Mot de passe |
| --- | --- | --- | --- | --- |
| Administrateur | `admin@lawim.app` | `admin` | `+237686822667` | `LAWIM@Demo2026µ` |
| Manager | `manager@lawim.app` | `manager` | `+237686822668` | `LAWIM@Demo2026µ` |
| Agent LAWIM | `agent@lawim.app` | `agent` | `+237686822669` | `LAWIM@Demo2026` |
| Utilisateur propriétaire | `owner@lawim.app` | `owner` | `+237686822670` | `LAWIM@Demo2026µ` |
| Investisseur / Banque | `investor@lawim.app` | `investor` | `+237686822671` | `LAWIM@Demo2026µ` |

## Tests Exécutés

### Backend

- `PYTHONPATH=code:tests python3 -m unittest tests.test_lawim_v2`
- Résultat: `Ran 31 tests in 89.012s OK`
- `PYTHONPATH=code:tests python3 -m unittest tests.test_rc_postgresql`
- Résultat: `0 tests` exécutés, `1 skipped` car `LAWIM_TEST_POSTGRES_URL` n’était pas défini localement

### Manifest / Schéma

- `PYTHONPATH=code python3 scripts/validate_prisma_manifest.py`
- Résultat: PASS

### Frontend

- `npm run build`
- `npm run test -- --run tests/api-sdk.test.ts tests/i18n.test.tsx tests/static-runtime-login.test.ts tests/frontend-shell.test.tsx`
- Résultat: build OK, 25 tests frontend OK

## Validation Production

Date de validation: `2026-07-09`

### Santé des services

- `/api/health` OK
- `lawim-app` healthy
- `lawim-postgres` healthy
- `lawim-redis` healthy

### Authentification validée

- Login admin par email OK
- Login admin par username OK
- Login admin par téléphone OK
- Login manager OK
- Login agent OK
- Login owner OK
- Login investor OK
- Le dashboard reste accessible après connexion
- Le formulaire de login disparaît après authentification

### Résultat d’état observé

- `organizations: 2`
- `users: 5`

## Commit Et Tag

### Release code

- Commit: `14e00163` puis correction finale `3465e89e`
- Message principal: `fix(auth): support identifier login and repair access screen`
- Correction finale: `fix(auth): preserve standard demo passwords in production`

### Tag officiel

- `mission-08-3-auth-access-demo-accounts`
- Pointe sur `3465e89e`

## Artefact Et SHA256

- Artefact: `/tmp/lawim_v2_release_mission-08-3-auth-access-demo-accounts.tar.gz`
- SHA256: `666d8750cb92c5127fd9963a995433c08424df141a7ba5f072b810b2608ae61c`

## Déploiement OVH

- Release extrait sur OVH: `/opt/lawim/releases/3465e89e`
- Release active: `/opt/lawim/current`
- Sauvegarde avant bascule: `/opt/lawim/backups/pre-3465e89e-20260709091324.tar.gz`

### Note d’exploitation

Le build Docker distant n’a pas pu reconstruire l’image à cause de l’absence de `python:3.11-slim` dans le cache OVH et d’un accès registry/DNS dégradé. Le package Python réellement importé par le conteneur a donc été synchronisé directement après extraction du release. Cette opération a été vérifiée par redémarrage du conteneur `lawim-app` et par validation fonctionnelle des comptes standards.

## Procédure De Rollback

1. Rebasculer `/opt/lawim/current` vers le release précédent.
2. Restaurer le backup correspondant dans `/opt/lawim/backups/`.
3. Redémarrer `lawim-app`.
4. Revalider `/api/health` et les trois comptes critiques: admin, agent, owner.

## Réserves

- Aucune réserve fonctionnelle bloquante après validation finale.
- `LAWIM_ADMIN_PASSWORD` est désormais ignoré en production pour préserver les identifiants de démonstration standards.
- Le cache d’image Docker OVH doit être surveillé car la reconstruction distante dépend d’une image base qui n’était pas présente localement sur le serveur au moment du déploiement.

