# Sprint 003 Planning Report

- Sprint: Sprint 003
- Date: 2026-06-28
- Scope: Preparation only
- Statut propose: READY_FOR_DG_OPENING

## 1. Resume du Sprint 002 herite

Sprint 002 est cloture officiellement. Les trois tickets planifies sont couverts, le risque bloquant reste false et le PCC est coherent avec la trace de cloture. Le socle Docker, l'observabilite runtime et le squelette CI restent la reference technique immediate.

## 2. Objectif du Sprint 003

Installer la base de donnees et le stockage de LAWIM_V2: PostgreSQL, Prisma, Redis, sauvegardes, restauration et archivage. Ce sprint correspond au bloc S003 du plan directeur d'implementation et reste aligne avec les references `06-DATABASE-REFERENCE.md` et `14-STORAGE-REFERENCE.md`.

## 3. Liste des tickets

| Ticket | Titre | Entree | Sortie | Dependances |
| --- | --- | --- | --- | --- |
| T03.01 | PostgreSQL foundation | Sprint 002 cloture, PCC coherent, T02.03 valide, references data et storage disponibles | Socle relationnel, contraintes de base et conventions de connexion | T02.03, 06-DATABASE-REFERENCE.md, 14-STORAGE-REFERENCE.md |
| T03.02 | Prisma baseline | T03.01 ferme, schema relationnel confirme | Premiere couche ORM et conventions de migration | T03.01, 06-DATABASE-REFERENCE.md, 24-DEVELOPER-GUIDE.md |
| T03.03 | Backup primitives | T03.01 ferme, contrat de stockage confirme | Snapshot, checksum, restauration et trace de reprise | T03.01, 14-STORAGE-REFERENCE.md, 22-OPERATIONS-RUNBOOK.md |

## 4. Ordre recommande

1. T03.01 - PostgreSQL foundation.
2. T03.02 - Prisma baseline.
3. T03.03 - Backup primitives.

T03.02 et T03.03 peuvent etre prepares apres T03.01, mais T03.01 reste le gate dur du sprint.

## 5. Dependances

- Decision DG d'ouverture du Sprint 003.
- Confirmation de cloture Sprint 002 et validation PCC.
- T02.03 comme gate d'entree technique.
- `06-DATABASE-REFERENCE.md` pour le modele de donnees.
- `14-STORAGE-REFERENCE.md` pour la persistance, l'archivage et la reprise.
- `24-DEVELOPER-GUIDE.md` pour les conventions Prisma.
- `22-OPERATIONS-RUNBOOK.md` pour les primitives de sauvegarde et de restauration.

## 6. Chemin critique

Confirmation de cloture Sprint 002 -> Decision DG d'ouverture -> T03.01 -> T03.02 et T03.03 -> cloture Sprint 003.

T03.01 est le gate dur. T03.02 et T03.03 ne peuvent pas demarrer avant lui et doivent tous deux etre disponibles avant qu'un lancement du sprint soit considere coherent.

## 7. Risques

- Une derive entre le schéma PostgreSQL et le modele canonique pourrait creer des ecarts de persistance. Mitigation: reutiliser les references officielles et limiter le perimetre de T03.01.
- Une baseline Prisma mal alignee pourrait introduire des migrations fragiles. Mitigation: garder les conventions de migration explicites et derivables des documents de reference.
- Des primitives de sauvegarde insuffisantes pourraient laisser une restauration inverifiable. Mitigation: documenter checksum, snapshot et procedure de restauration avant toute activation.

## 8. Recommandations

- Ouvrir Sprint 003 uniquement apres la decision DG tracee.
- Reutiliser les references officielles avant toute creation de schema ou de convention de migration.
- Garder PostgreSQL, Prisma et les sauvegardes dans un perimetre strictement documentaire et traçable tant qu'aucun ticket d'implementation ne l'ouvre explicitement.
- Conserver T03.01 comme gate dur pour la suite du sprint.

## 9. Etat du PCC

- Sprint 002: TERMINE.
- Tickets Sprint 002: 3/3 couverts.
- Blocking risk: false.
- PCC: coherent avec la cloture et les fondations heritees.
- Sprint 003: prepare, non ouvert.
- Aucun ticket Sprint 003 n'existe encore.
- Les registres dependances et risques restent alignes avec l'ouverture preparee.

## 10. Decision proposee au Directeur General

GO AVEC RESERVES. Le Sprint 003 peut etre ouvert une fois la decision DG tracee, sous reserve de conserver les contrats PostgreSQL, Prisma, stockage, sauvegardes et restauration strictement alignes avec les references officielles.

```yaml
sprint: 003
status: READY_FOR_DG_OPENING
planning: PASS
dependencies: VERIFIED
risks: ACCEPTABLE
blocking_risk: false
next_ticket: T03.01
decision_required: true
```
