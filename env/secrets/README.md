# Secrets

Ce dossier formalise la strategie de gestion des secrets de LAWIM_V2.

## Objectif

Separer strictement les variables d'environnement non secretes et les secrets, documenter le nommage, la rotation, le stockage et l'injection runtime, et preparer l'usage futur avec Docker Compose, OVH et CI/CD.

## Arborescence

- `development/.secrets.example`;
- `staging/.secrets.example`;
- `production/.secrets.example`;
- les fichiers runtime `.secrets.local` restent hors depot et ne sont jamais commits.

## Convention de nommage

- les noms de secrets utilisent le prefixe `LAWIM_SECRET_`;
- les noms restent explicites, stables et en majuscules;
- un secret correspond a une seule cle logique;
- aucune cle sensible ne doit apparaitre dans un fichier versionne.

## Separation variables / secrets

- `env/*/.env.example` documente les variables non secretes;
- `env/*/.secrets.example` documente la forme des secrets;
- les valeurs reelles sont injectees depuis l'exterieur;
- `SECRET_PROVIDER` reste externe et ne designe jamais un secret stocke dans Git.

## Stockage

- stockage prefere: coffre de secrets du fournisseur, store local protege ou fichier runtime hors depot;
- aucun secret dans le code, dans les images ou dans les journaux;
- aucune cle partagee entre environnements sans justification et validation explicites;
- les permissions d'acces restent les plus restrictives possibles.

## Rotation

- rotation planifiee;
- rotation apres incident;
- rotation apres changement d'operateur ou de role;
- rotation apres suspicion de fuite;
- verification de la nouvelle valeur avant retrait de l'ancienne.

## Integration Docker Compose

- Compose consomme les variables non secretes via les contrats d'environnement deja poses;
- les secrets sont montes ou injectes depuis l'exterieur, jamais depuis un fichier versionne;
- les overlays restent responsables du comportement, pas du stockage des valeurs;
- la couche Compose ne doit jamais devenir un registre de secrets.

## Integration OVH

- les serveurs OVH ne stockent pas les secrets comme source de verite;
- l'administration serveur consomme des secrets runtime, jamais des valeurs en clair dans les fichiers de depot;
- la continuite et la reprise doivent pouvoir recharger les secrets sans exposer leur contenu.

## Integration CI/CD

- les workflows consomment des secrets fournis par le fournisseur de CI/CD ou par un coffre externe;
- les valeurs doivent rester masquees dans les logs et les artefacts;
- aucun fichier YAML versionne ne doit contenir une valeur secrete;
- les secrets CI/CD doivent respecter le meme nommage que les secrets runtime quand cela est possible.

## Bonnes pratiques

- valider l'absence de secrets avant commit;
- conserver les templates comme modeles, pas comme sources de verite;
- separer les secrets de developpement, de staging et de production;
- documenter toute exception dans un ticket futur avec revue securite.
