# Project Control Center

## Programme
- Programme: LAWIM_V2
- Programme status: STABILISATION
- Sprint actif: Sprint 005
- Sprint status: EN COURS
- Decision: GO AVEC RESERVES
- Mode: execution controlee par tickets
- Baseline: Bootstrap Pack valide + base operationnelle Sprint 001
- Reserve: le backlog canonique detaille devra etre verifie ulterieurement; la couverture de T01.04 repose sur les conventions d'environnements deja documentees; le socle utilisateurs, roles et organisations reste a consolider dans Sprint 005.
- Derniere trace technique: T05.03 est ferme; la matrice de permissions est stabilisee avant la cloture du Sprint 005, sans remettre en cause le socle Sprint 004.

## Cloture Sprint 001
- Statut Sprint 001: TERMINE
- Tickets couverts: 10/10
- Architecture: PASS
- QA: PASS
- Security: PASS
- Risque bloquant: false
- Validation DG: en attente
- Sprint 002: termine, cloture tracee

## Cloture Sprint 002
- Statut Sprint 002: TERMINE
- Objectif: disposer d'un runtime local reproductible, d'une observabilite de base et d'un squelette CI minimal.
- Tickets: T02.01 - Docker baseline, T02.02 - Runtime observability, T02.03 - CI skeleton
- Tickets couverts: 3/3
- Ordre recommande: T02.01 -> T02.02 -> T02.03
- Dependances: Sprint 001 cloture, T01.01, T01.02, T01.03, T01.04, T01.05, T01.07, T01.08, T01.09 et T01.10
- Chemin critique: Decision DG d'ouverture -> T02.01 -> T02.02 et T02.03 -> cloture Sprint 002
- Risques d'entree: derive runtime, fuite de secrets, CI active trop tot
- Risque bloquant: false
- Validation DG: en attente
- Sprint 003: termine, cloture tracee

## Cloture Sprint 003
- Statut Sprint 003: TERMINE
- Objectif: installer la persistance, la structure initiale et les capacites de sauvegarde.
- Tickets: T03.01 - PostgreSQL foundation, T03.02 - Prisma baseline, T03.03 - Backup primitives
- Tickets couverts: 3/3
- Ordre recommande: T03.01 -> T03.02 -> T03.03
- Dependances: Sprint 002 cloture, T02.03, `docs/Directive/06-DATABASE-REFERENCE.md` et `docs/Directive/14-STORAGE-REFERENCE.md`
- Chemin critique: Decision DG d'ouverture -> T03.01 -> T03.02 et T03.03 -> cloture Sprint 003
- Risques d'entree: derive de schema, derive de migration, restauration inverifiable
- Risque bloquant: false
- Validation DG: en attente
- T03.01: socle relationnel confirme
- T03.02: baseline Prisma confirmee
- T03.03: primitives de sauvegarde confirmee
- Sprint 004: termine, cloture tracee

## Ouverture Sprint 005
- Statut Sprint 005: EN COURS
- Objectif: organiser les utilisateurs, les roles, les organisations et la matrice de permissions de LAWIM_V2.
- Tickets: T05.01 - User lifecycle, T05.02 - Organization model, T05.03 - Permissions matrix
- Tickets couverts: 3/3
- T05.01: ferme
- T05.02: ferme
- T05.03: ferme
- Ordre recommande: T05.01 -> T05.02 -> T05.03
- Dependances: Sprint 004 cloture, T04.03, `docs/Directive/08-ROLE-REFERENCE.md`, `docs/Directive/19-ADMINISTRATION-REFERENCE.md`, `docs/Directive/13-ARCHITECTURE-GOVERNANCE-REFERENCE.md`, `docs/Directive/15-SECURITY-REFERENCE.md` et `docs/Directive/06-DATABASE-REFERENCE.md`
- Chemin critique: Decision DG d'ouverture -> T05.01 -> T05.02 -> T05.03 -> cloture Sprint 005
- Risques d'entree: duplication d identites, confusion sur les rattachements organisationnels, matrice de permissions trop large
- Risque bloquant: false
- Validation DG: en attente

## Cloture Sprint 004
- Statut Sprint 004: TERMINE
- Objectif: mettre en place l authentification et l identite de LAWIM_V2.
- Tickets: T04.01 - Auth service, T04.02 - Token strategy, T04.03 - MFA gate
- Tickets couverts: 3/3
- Ordre recommande: T04.01 -> T04.02 -> T04.03
- Dependances: Sprint 003 cloture, T03.02, `docs/Directive/15-SECURITY-REFERENCE.md`, `docs/Directive/16-API-REFERENCE.md`, `docs/Directive/24-DEVELOPER-GUIDE.md` et `docs/Directive/40-PRODUCTION-CHECKLIST.md`
- Chemin critique: Decision DG d'ouverture -> T04.01 -> T04.02 -> T04.03 -> cloture Sprint 004
- Risques d'entree: exposition d acces, gestion faible des secrets, strategie de jetons fragile, gate MFA incomplet
- Risque bloquant: false
- Validation DG: en attente
- T04.01: service d authentification confirme
- T04.02: strategie de jetons confirmee
- T04.03: gate MFA confirmee
- Sprint 005: ouvert

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
