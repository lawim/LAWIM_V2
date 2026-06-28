# Project Control Center

## Programme
- Programme: LAWIM_V2
- Programme status: STABILISATION
- Sprint actif: Aucun
- Sprint status: CLOTURE
- Decision: GO AVEC RESERVES
- Mode: execution controlee par tickets
- Baseline: Bootstrap Pack valide + base operationnelle Sprint 001
- Reserve: le backlog canonique detaille devra etre verifie ulterieurement; la couverture de T01.04 repose sur les conventions d'environnements deja documentees
- Derniere trace technique: le rapport de cloture Sprint 001 consolide les 10 tickets, les validations finales et les risques residuels sans ouvrir Sprint 002.

## Cloture Sprint 001
- Statut Sprint 001: TERMINE
- Tickets couverts: 10/10
- Architecture: PASS
- QA: PASS
- Security: PASS
- Risque bloquant: false
- Validation DG: en attente
- Sprint 002: en preparation, non ouvert

## Preparation Sprint 002
- Statut Sprint 002: INITIALISE
- Objectif: disposer d'un runtime local reproductible, d'une observabilite de base et d'un squelette CI minimal.
- Tickets: T02.01 - Docker baseline, T02.02 - Runtime observability, T02.03 - CI skeleton
- Ordre recommande: T02.01 -> T02.02 -> T02.03
- Dependances: Sprint 001 cloture, T01.01, T01.02, T01.03, T01.04, T01.05, T01.07, T01.08, T01.09 et T01.10
- Chemin critique: Decision DG d'ouverture -> T02.01 -> T02.02 et T02.03
- Risques d'entree: derive runtime, fuite de secrets, CI active trop tot
- Decision proposee au DG: GO AVEC RESERVES

## Referentiels de pilotage
- Workflow officiel: .lawim/workflows/ticket-workflow.md
- Ticket status model: .lawim/status/ticket-status.md
- Sprint status model: .lawim/status/sprint-status.md
- Program status model: .lawim/status/program-status.md
- Checklists: .lawim/checklists/*.md
- Release model: .lawim/releases/*.md
- History logs: .lawim/history/*.md

## Roles de coordination
- Directeur General
- PMO
- Chief Architect
- Product Owner
- Release Manager
- Delivery Manager
- Tech Lead
- Integration Manager
- Review Board
- Prompt Generator

## Agents specialises
- AI
- Backend
- Database
- DevOps
- Documentation
- Frontend
- Mobile
- QA
- Security

## Workflow officiel

BROUILLON -> VALIDE DG -> PLANIFIE -> ASSIGNE -> EN COURS -> REVUE ARCHITECTE -> REVUE QA -> REVUE SECURITY -> INTEGRATION -> VALIDATION DG -> FERME

## Regles PCC
- aucune transition ne peut etre sautee sans decision explicite du Directeur General;
- le PMO trace chaque changement de statut et chaque validation;
- les revues utilisent les checklists officielles;
- les journaux d'historique sont append-only;
- la fermeture d'un ticket exige une trace dans le PCC et dans l'historique;
- la validation finale appartient au Directeur General;
- les agents specialises executent uniquement le ticket transmis;
- le PCC reste la reference de coordination du programme.
