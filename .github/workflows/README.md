# GitHub Workflows

Ce dossier documente les workflows GitHub Actions de LAWIM_V2.

## Role
Point d'ancrage des futures chaines CI et CD, sans execution active dans T01.08.

## Sources de verite
- `.lawim/releases/branching-model.md`
- `.lawim/releases/versioning.md`
- `.lawim/workflows/ticket-workflow.md`
- `docs/Directive/39-CI-CD-REFERENCE.md`
- `docs/Directive/17-DEPLOYMENT-INFRASTRUCTURE-REFERENCE.md`
- `docs/Directive/15-SECURITY-REFERENCE.md`
- `docs/Directive/37-QUALITY-ASSURANCE-PLAN.md`
- `docs/Directive/40-PRODUCTION-CHECKLIST.md`
- `docker/README.md`
- `docker/compose/README.md`
- `env/README.md`
- `env/secrets/README.md`
- `.github/workflows/ci.yml.example`
- `.github/workflows/cd.yml.example`
- `templates/validation-template.md`

## Portee T01.08
- documenter la separation CI et CD;
- fixer les validations de branches;
- documenter les etapes build, test, analyse, publication et deploiement;
- documenter les variables et secrets attendus;
- documenter la promotion et le versioning;
- rester conceptuel: aucun workflow actif, aucune image publiee, aucun secret reel.

## Strategie CI
- la CI valide les contrats de depot, les fichiers Docker, les overlays Compose et les conventions de secrets;
- la CI couvre les branches `ticket/*`, `sprint/*`, `release/*`, `hotfix/*` et `main` selon les regles de protection;
- la CI reste en lecture seule vis-a-vis des environnements de livraison;
- la CI produit des preuves de qualite, jamais des changements de production.

## Strategie CD
- la CD ne s'active qu'apres une validation de version et de promotion;
- la CD documente les etapes de preparation, de promotion, de validation post-deploiement et de rollback;
- la CD doit reutiliser le meme digest lorsque cela est possible;
- la CD ne publie aucune image Docker dans ce ticket.

## Validation des branches
- `ticket/*`: controle rapide du contrat de branche, du format et des fichiers de support;
- `sprint/*`: consolidation des validations techniques avant integration;
- `release/*`: gel de la version candidate et gates completes;
- `hotfix/*`: correction courte avec les memes gates critiques;
- `main`: promotion finale et controle de lisibilite de la livraison.

## Etapes de validation
| Etape | Objectif | Preuve attendue |
| --- | --- | --- |
| Preflight | Verifier le nommage, les fichiers requis et le contexte de branche | Contrat du depot et de la branche |
| Build | Valider la construction conceptuelle des artefacts et des images | Socle Docker et overlays Compose |
| Test | Valider les tests et les controles de non-regression | Resultats de tests ou de verifications documentaires |
| Analyse | Valider la qualite, la securite et la coherence des contrats | Rapports d'analyse et checklists |
| Migration | Valider le contrat de migration de schema avant la livraison | Contrat de migration documente et reutilisable |
| Publication | Preparation de la livraison sans publication d'image Docker dans T01.08 | Metadonnees de version et preuves de promotion |
| Deploiement | Documenter la promotion et le controle post-deploiement | Gates de staging et de production conceptuels |
| Rollback | Garder le chemin de retour lisible et reversible | Procedure de retour arriere documentee |

## Variables CI/CD
- `APP_ENV` identifie le contexte d'execution;
- `STACK_PROFILE` aligne le profil Compose;
- `LOG_LEVEL` fixe le niveau de verbosite;
- `PUBLIC_BASE_URL` reste fourni de l'exterieur;
- `SECRET_PROVIDER` reste externe;
- `LAWIM_SECRET_*` suit la convention des secrets runtime;
- `GITHUB_TOKEN` reste un jeton fourni par GitHub avec permissions minimales;
- `GITHUB_REF`, `GITHUB_SHA` et `GITHUB_EVENT_NAME` servent uniquement au contexte de pipeline.

## Integration Docker et Compose
- la CI doit valider `docker/Dockerfile.base` et les overlays d'images;
- la CI doit valider les contrats `docker/compose/*.yml` avec `docker compose config`;
- les noms de reseaux et de volumes restent stables;
- aucun secret reel ne doit etre injecte depuis un fichier versionne;
- les promotions reutilisent le socle partage et evitent les tags `latest` pour la promotion.

## Integration Secrets
- les secrets restent externes au depot;
- les workflows ne contiennent aucune valeur sensible;
- les logs et les artefacts doivent rester masques;
- la convention `LAWIM_SECRET_` reste la reference commune avec les tickets de secrets et de livraison;
- les valeurs reelles sont fournies par le coffre du fournisseur ou par un store runtime autorise.

## Versionnement et promotion
- le versioning suit `vMAJOR.MINOR.PATCH`;
- chaque promotion cite les tickets inclus;
- la promotion se fait sur des tags lisibles et des digests immuables;
- `latest` ne sert pas de reference de promotion;
- les branches de release restent gelees sauf correction approuvee.

## Conventions
- un workflow par objectif;
- secrets externalises;
- permissions minimales;
- exemples suffixes `.example` non actifs;
- aucune logique metier dans les fichiers de workflow.

## Preparation de T01.09
- T01.09 pourra reutiliser cette separation CI/CD sans redefinir les branches ou les permissions;
- les futures activations devront rester alignees sur la strategie de logs et de secrets;
- aucun ticket suivant n'est ouvert ici.
