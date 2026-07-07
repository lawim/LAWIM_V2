# Administration — Rapport de finalisation

## Résumé exécutif

Le parcours de connexion d’administration a été corrigé sur deux surfaces:

- le frontend React envoie désormais correctement `POST /api/auth/login` via le SDK API;
- le runtime statique bascule automatiquement vers le parcours `admin` après authentification.

Les tests frontend, les tests API et la non-régression passent.

## Cause exacte

1. `frontend/packages/api-sdk/src/index.ts` normalisait mal la base d’API lorsqu’elle était fournie comme origine absolue. La résolution d’URL n’était pas assez robuste pour garantir `https://.../api/auth/login` et `https://.../api/v2/dashboard`.
2. `code/lawim_v2/static/app.js` stockait bien le token mais ne réappliquait pas le parcours d’administration après login. L’interface restait donc sur le parcours courant jusqu’à manipulation manuelle.
3. `frontend/packages/auth/src/index.tsx` acceptait trop facilement une réponse sans token utile, ce qui masquait des échecs de session.

## Fichiers modifiés

- [code/lawim_v2/static/app.js](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/code/lawim_v2/static/app.js)
- [frontend/apps/web/src/App.tsx](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/frontend/apps/web/src/App.tsx)
- [frontend/packages/api-sdk/src/index.ts](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/frontend/packages/api-sdk/src/index.ts)
- [frontend/packages/auth/src/index.tsx](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/frontend/packages/auth/src/index.tsx)
- [frontend/tests/api-sdk.test.ts](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/frontend/tests/api-sdk.test.ts)
- [frontend/tests/frontend-shell.test.tsx](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/frontend/tests/frontend-shell.test.tsx)
- [tests/test_beta_candidate.py](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/tests/test_beta_candidate.py)

## Correction appliquée

- Normalisation du routage API pour couvrir les bases relatives et absolues sans casser les endpoints `/api/auth/*` et `/api/v2/*`.
- Ajout d’un override de base API pour les tests afin de valider le comportement réel d’une origine distante.
- Durcissement du login: échec explicite si le token manque, et nettoyage garanti de l’état de chargement.
- Basculage automatique du runtime statique vers le parcours `admin` après login, selon le rôle renvoyé par l’API.
- Régressions ajoutées pour verrouiller le chemin de login UI, la résolution d’URL API et les marqueurs du runtime statique.

## Tests exécutés

- `npm run build` dans `frontend/`
- `npm run test` dans `frontend/`
- `python3 -m unittest tests.test_source_intelligence`
- `PYTHONPATH=tests python3 -m unittest tests.test_beta_candidate`

Résultat:

- build frontend: PASS
- tests frontend: PASS
- tests API: PASS
- tests non-régression: PASS

## Commit

À renseigner dans l’historique git après figement du correctif.

## Tag

`admin-login-fix-20260707`

## Statut de livraison

Le bouton `Sign in` déclenche maintenant le login, le navigateur émet bien `POST /api/auth/login`, la session est récupérée, et l’interface d’administration s’ouvre sans manipulation manuelle.
