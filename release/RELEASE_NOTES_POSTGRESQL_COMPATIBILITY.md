# Release notes - correction PostgreSQL LAWIM_V2

## Résumé
Cette correction renforce la compatibilité PostgreSQL du runtime LAWIM_V2 en adaptant les appels SQL SQLite-spécifiques vers des équivalents PostgreSQL sûrs.

## Contenu
- Réécriture des fonctions SQL SQLite non prises en charge par PostgreSQL.
- Réécriture des instructions `INSERT OR IGNORE` / `INSERT OR REPLACE` via le connecteur PostgreSQL.
- Ajout d'une couverture de régression autour du connecteur SQL.

## Vérification
- Backend : tests unitaires Python
- Frontend : suite Vitest

## Limites connues
- Le déploiement OVH et la validation de production ne sont pas exécutable localement sans l'environnement cible, les secrets et les services distants.
