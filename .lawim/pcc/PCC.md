# Project Control Center

## Programme
- Programme: LAWIM_V2
- Programme status: INITIALISE
- Sprint actif: Sprint 001
- Sprint status: INITIALISE
- Decision: GO AVEC RESERVES
- Mode: execution controlee par tickets
- Baseline: Bootstrap Pack valide + base operationnelle Sprint 001
- Reserve: le backlog canonique detaille devra etre verifie ulterieurement
- Derniere trace technique: T01.02 a etabli la base Docker partagee et les overlays development, staging et production; T01.03 reste en preparation.

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
