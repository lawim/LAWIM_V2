# LAWIM AIOS v1.0

Ce dossier contient le referentiel officiel de pilotage de LAWIM_V2. AIOS v1.0 est fige et sert de base de travail pour la production de developpement.

## Comment utiliser les agents

- Utiliser le Ticket Executor comme point d'entree unique pour chaque ticket.
- Les autres agents servent d'experts internes de reference par domaine.
- Confier au Ticket Executor le ticket, les regles, le PCC et le workflow.
- Attendre un livrable trace, pas une interpretation libre du besoin.
- Utiliser les agents comme references specialisees, pas comme arbitres de gouvernance.
- Faire remonter tout blocage au PMO et au Directeur General si une decision est requise.

Referentiel utile:

- [AIOS Manifest](./AIOS-MANIFEST.md)
- [Ticket workflow](./workflows/ticket-workflow.md)
- [Ticket Executor reference](../docs/Directive/49-TICKET-EXECUTOR-REFERENCE.md)

## Comment utiliser le PMO

- Le PMO est le point d'entree operationnel du programme.
- Il tient le PCC, trace les statuts et prepare les validations.
- Il controle que chaque ticket a un owner, un statut, des dependances et des preuves.
- Il alerte sur les ecarts, les oublis et les incoherences documentaires.
- Il ne remplace pas la decision DG, il l'execute et la trace.

Referentiel utile:

- [PCC](./pcc/PCC.md)
- [Program status](./status/program-status.md)
- [Ticket status](./status/ticket-status.md)
- [Sprint status](./status/sprint-status.md)

## Comment utiliser le PCC

- Le PCC est la source de verite de coordination du programme.
- Il centralise decisions, risques, dependances, validations et references.
- Toute transition de workflow doit y laisser une trace.
- Toute exception doit y etre consignee.
- Toute fermeture doit y etre visible avant d'etre consideree comme definitive.

Referentiel utile:

- [PCC](./pcc/PCC.md)
- [Decisions](./pcc/decisions.md)
- [Risks](./pcc/risks.md)
- [Dependencies](./pcc/dependencies.md)
- [Validations](./pcc/validations.md)

## Comment utiliser les tickets

- Un ticket est l'unite unique de travail.
- Un ticket doit decrire son objectif, son perimetre, ses dependances et ses criteres d'acceptation.
- Un ticket suit le workflow officiel sans saut d'etat.
- Un ticket ne se ferme qu'apres les validations requises.
- Un ticket doit conserver des traces exploitables pour l'archivage et la revue.

Referentiel utile:

- [Ticket workflow](./workflows/ticket-workflow.md)
- [Ticket status](./status/ticket-status.md)
- [Sprint status](./status/sprint-status.md)

## Comment utiliser les sprints

- Un sprint regroupe un ensemble de tickets dans une fenetre de livraison controlee.
- Sprint 001 est la premiere base d'execution officielle.
- Un sprint doit rester coherent avec le programme, le PCC et les dependances confirmees.
- Le sprint ne peut pas masquer des tickets non traces.
- La cloture du sprint exige un bilan, des validations et une archive lisible.

Referentiel utile:

- [Sprint 001](./sprints/sprint-001.md)
- [Sprint status](./status/sprint-status.md)
- [Program status](./status/program-status.md)

## Comment utiliser les workflows

- Le workflow officiel des tickets est la reference obligatoire.
- Aucun role ne peut le renommer ou le court-circuiter sans decision DG.
- Les revues architecture, QA, security et integration sont des portes de controle, pas des formalites.
- Les refus renvoient vers la correction avec justification tracee.
- La validation finale appartient au Directeur General.

Referentiel utile:

- [Ticket workflow](./workflows/ticket-workflow.md)
- [AIOS Manifest](./AIOS-MANIFEST.md)
- [Baseline v1](./BASELINE-v1.md)

## Regles d'utilisation

- Ne pas creer de nouveaux agents hors Ticket Executor, approuve comme point d'entree unique.
- Ne pas demarrer de ticket applicatif sans PCC et sans planification.
- Ne pas modifier les referentiels fondateurs sans decision explicite.
- Ne pas considerer un travail comme termine sans validation officielle.
- Ne pas detacher les livrables de leur trace documentaire.

## Demarrage recommande

1. Lire `VERSION` et `BASELINE-v1.md`.
2. Verifier le `PCC`.
3. Ouvrir le sprint et le ticket concerne.
4. Lancer le Ticket Executor sur le ticket concerne.
5. Executer le travail avec trace PMO.
6. Enchainer les validations dans l'ordre du workflow.
7. Fermer le ticket dans le PCC et archiver la preuve.
