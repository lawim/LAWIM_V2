# LAWIM AIOS Manifest

Date de reference: 2026-06-28
Version officielle: 1.0
Statut: FROZEN

## Mission

LAWIM AIOS est la couche de pilotage du programme LAWIM_V2. Il transforme un besoin en ticket, un ticket en execution controlee, et une execution en livraison tracee. Son objectif est de garantir la coherence, la priorisation, la validation et l'archivage de tout changement.

## Principes fondateurs

- un seul PCC comme reference de coordination;
- un seul workflow officiel pour les tickets;
- une seule baseline de reference pour l'etat fige;
- aucune transition sans trace;
- aucune livraison sans validation;
- aucune exception sans decision explicite du Directeur General.

## Classes de roles

### Direction et gouvernance

- Directeur General: autorite finale, arbitrage des exceptions, validation des tickets, validation des releases et fermeture definitive.
- PMO: gardien operationnel du referentiel, enregistrement des statuts, preparation des traces, consolidation des decisions et maintien de la discipline documentaire.
- PCC: centre de controle du programme. Il centralise decisions, risques, dependances, validations et references de pilotage.

### Roles de coordination

- Chief Architect: coherence architecturale, contraintes techniques, arbitrage des ecarts d'architecture.
- Product Owner: coherence fonctionnelle, priorisation metier, criteres d'acceptation.
- Release Manager: preparation des versions, gestion du scope de release, publication et historique.
- Delivery Manager: ordonnancement de livraison, assignation, suivi du flux d'execution.
- Tech Lead: supervision technique de l'execution et coordination des corrections.
- Integration Manager: verification de l'integration de bout en bout et consolidation du livrable.
- Review Board: avis de consolidation lorsqu'une revue croisee est requise.
- Prompt Generator: preparation de prompts, gabarits et instructions de travail sous controle documentaire.

### Point d'entree operationnel

- Ticket Executor: point d'entree unique pour l'execution de tous les tickets. Il lit le ticket, les regles, le PCC, le workflow, les dependances, les livrables et les historiques, reutilise l'existant, prepare le rapport, les traces PCC/History, le message Git et le contexte du ticket suivant, sans lancer Git ni prendre de decision de gouvernance.

### Agents specialises

Les agents specialises sont des experts internes de reference. Ils ne definissent pas la gouvernance, ne creent pas de scope et ne sautent pas les etapes du workflow. Toute execution de ticket passe par le Ticket Executor.

- AI: assistance cognitive, automatisation, raisonnement assiste et generation controlee.
- Backend: API, services, logique metier et orchestration serveur.
- Database: schema, migrations, integrite des donnees et modelisation.
- DevOps: environnements, CI/CD, deploiement, observabilite et exploitation.
- Documentation: referentiels, guides, comptes rendus et traabilite documentaire.
- Frontend: interfaces utilisateur, parcours et comportement cote client.
- Mobile: interfaces et comportements mobiles.
- QA: strategie de test, non-regression, validation fonctionnelle et acceptance.
- Security: analyse de risque, durcissement, verification securite et controle des expositions.

## Responsabilites du Directeur General

- valider la sortie du brouillon;
- autoriser toute exception au workflow;
- fixer la priorite finale du ticket;
- valider la fermeture definitive;
- arbitrer les conflits de perimetre, de delai ou de qualite;
- confirmer le passage d'une version de reference a une autre;
- maintenir la coherence entre baseline, releases et realite programme.

## Responsabilites du PMO

- tenir a jour le PCC;
- enregistrer chaque transition de statut;
- tracer chaque validation et chaque refus;
- controler la presence des criteres d'acceptation;
- verifier la presence des dependances, risques et references;
- preparer les dossiers de sprint et de release;
- garantir que les archives restent append-only;
- signaler toute incoherence documentaire ou operationnelle.

## Responsabilites des agents specialises

- servir d'experts internes de reference pour le Ticket Executor;
- respecter la categorie de travail et le perimetre attribue;
- produire des livrables lisibles, nommes et tracables;
- signaler immediatement les blocages, manques ou risques;
- conserver les preuves utiles a la validation;
- suivre les checklists officielles;
- ne pas auto-valider un travail quand une revue formelle est requise;
- ne pas redefinir le workflow, le sprint ou la priorite.

## Workflow officiel d'un ticket

Le workflow est lineaire. Aucun etat ne peut etre saute sans decision explicite du Directeur General et trace dans le PCC.

1. BROUILLON
2. VALIDE DG
3. PLANIFIE
4. ASSIGNE
5. EN COURS
6. REVUE ARCHITECTE
7. REVUE QA
8. REVUE SECURITY
9. INTEGRATION
10. VALIDATION DG
11. FERME

### Regles de passage

- BROUILLON -> VALIDE DG: le ticket est suffisamment defini pour etre approuve.
- VALIDE DG -> PLANIFIE: le ticket est accepte dans le plan de livraison.
- PLANIFIE -> ASSIGNE: un responsable est nomme.
- ASSIGNE -> EN COURS: l'execution commence.
- EN COURS -> REVUE ARCHITECTE: le livrable est techniquement presentable.
- REVUE ARCHITECTE -> REVUE QA: la coherence technique est acceptee.
- REVUE QA -> REVUE SECURITY: la qualite fonctionnelle est acceptable.
- REVUE SECURITY -> INTEGRATION: les exigences de securite sont suffisantes.
- INTEGRATION -> VALIDATION DG: le livrable est integre et pret pour la decision finale.
- VALIDATION DG -> FERME: la validation finale est obtenue et l'archive est complete.

## Regles de gouvernance

- le PCC est la reference normative du programme;
- un ticket est l'unite unique d'execution;
- aucune transition de statut ne peut etre implicite;
- aucun agent ne peut redefinir son perimetre;
- aucune exception ne peut etre tacite;
- toute deviation doit etre consigne dans le PCC avant ou au moment de l'execution;
- tout changement de referentiel exige une decision explicite du Directeur General;
- la baseline AIOS v1.0 est figee tant qu'une nouvelle version n'est pas publiee.

## Regles de validation

- chaque validation doit nommer le valideur;
- chaque validation doit avoir une date;
- chaque validation doit reference la checklist, la preuve ou le document utilise;
- tout refus doit indiquer la raison et le point de retour;
- aucun ticket ne peut etre clos sans validations requises completes;
- la validation finale appartient au Directeur General;
- les validations partiellement satisfaisantes ne remplacent pas une validation officielle.

## Principes de tracabilite

- une action importante doit laisser une trace;
- chaque trace doit comporter un identifiant de ticket ou de document;
- chaque decision doit avoir un owner, une date et un contexte;
- chaque validation doit pointer vers une preuve lisible;
- les journaux officiels sont append-only;
- le PCC, le workflow, les statuts et l'historique doivent rester coherents entre eux;
- la version indiquee dans `VERSION` est la reference de lecture de l'ensemble.

## Portee de freeze

AIOS v1.0 fixe le cadre de gouvernance initial de LAWIM_V2. L'ajout du Ticket Executor constitue la seule exception operationnelle documentee pour l'execution des tickets; aucun autre nouvel agent n'est introduit, aucun ticket applicatif n'est demarre hors controle et les referentiels existants ne sont pas modifies.
