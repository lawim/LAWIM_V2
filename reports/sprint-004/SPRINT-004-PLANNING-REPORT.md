# Sprint 004 Planning Report

- Sprint: Sprint 004
- Date: 2026-06-28
- Scope: Preparation only
- Statut propose: READY_FOR_DG_OPENING

## 1. Resume du Sprint 003 herite

Sprint 003 est cloture officiellement. Les trois tickets planifies sont couverts, le risque bloquant reste false et le PCC est coherent avec la trace de cloture. Le socle PostgreSQL, Prisma et les primitives de sauvegarde restent la reference technique immediate.

## 2. Objectif du Sprint 004

Mettre en place l authentification et l identite de LAWIM_V2: service d authentification, strategie de jetons, sessions et gate MFA. Ce sprint correspond au bloc S004 du plan directeur d implementation et reste aligne avec les references `15-SECURITY-REFERENCE.md`, `16-API-REFERENCE.md`, `24-DEVELOPER-GUIDE.md` et `40-PRODUCTION-CHECKLIST.md`.

## 3. Liste des tickets

| Ticket | Titre | Entree | Sortie | Dependances |
| --- | --- | --- | --- | --- |
| T04.01 | Auth service | Sprint 003 cloture, PCC coherent, T03.02 valide, references security et API disponibles | Service d authentification, login, logout, sessions et tokens techniques | T03.02, 15-SECURITY-REFERENCE.md, 16-API-REFERENCE.md |
| T04.02 | Token strategy | T04.01 ferme, contrat auth/session confirme | Strategie JWT, refresh et stockage de session | T04.01, 15-SECURITY-REFERENCE.md, 24-DEVELOPER-GUIDE.md |
| T04.03 | MFA gate | T04.02 ferme, strategie de jetons confirmee | Gate MFA, recovery et politique d acces | T04.02, 15-SECURITY-REFERENCE.md, 40-PRODUCTION-CHECKLIST.md |

## 4. Ordre recommande

1. T04.01 - Auth service.
2. T04.02 - Token strategy.
3. T04.03 - MFA gate.

T04.02 et T04.03 peuvent etre prepares apres T04.01, mais T04.01 reste le gate dur du sprint.

## 5. Dependances

- Decision DG d ouverture du Sprint 004.
- Confirmation de cloture Sprint 003 et validation PCC.
- T03.02 comme gate technique.
- `15-SECURITY-REFERENCE.md` pour le contrat de securite et d acces.
- `16-API-REFERENCE.md` pour les contrats d appel et de session.
- `24-DEVELOPER-GUIDE.md` pour les conventions de jetons et de configuration.
- `40-PRODUCTION-CHECKLIST.md` pour le durcissement MFA et les flux critiques.

## 6. Chemin critique

Confirmation de cloture Sprint 003 -> Decision DG d ouverture -> T04.01 -> T04.02 -> T04.03 -> cloture Sprint 004.

T04.01 est le gate dur. T04.02 et T04.03 ne peuvent pas demarrer avant lui et doivent tous deux etre disponibles avant qu un lancement du sprint soit considere coherent.

## 7. Risques

- Une derive entre le contrat d authentification et les references API ou securite pourrait exposer l acces.
- Une strategie de jetons mal alignee pourrait introduire des sessions fragiles ou difficiles a invalider.
- Un gate MFA insuffisamment precise pourrait laisser des flux critiques mal proteges.
- Des secrets reels ou des flux de recovery non traces ne sont pas acceptables dans ce sprint.

## 8. Recommandations

- Reutiliser les references securite et API avant toute creation de logique d acces.
- Garder les jetons, refresh et sessions strictement documentes avant toute implementation.
- Conserver les secrets et les politiques MFA hors depot et hors perimetre non trace.
- Maintenir T04.01 comme gate dur pour la suite du sprint.

## 9. Etat du PCC

- Sprint 003: TERMINE.
- Tickets Sprint 003: 3/3 couverts.
- Blocking risk: false.
- PCC: coherent avec la cloture et les fondations heritees.
- Sprint 004: prepare, non ouvert.
- Aucun ticket Sprint 004 n existe encore.
- Les registres dependances et risques restent alignes avec l ouverture preparee.

## 10. Decision proposee au Directeur General

GO AVEC RESERVES. Le Sprint 004 peut etre ouvert une fois la decision DG tracee, sous reserve de conserver les contrats d authentification, de jetons et de MFA strictement alignes avec les references officielles.

```yaml
sprint: 004
status: READY_FOR_DG_OPENING
planning: PASS
dependencies: VERIFIED
risks: ACCEPTABLE
blocking_risk: false
next_ticket: T04.01
decision_required: true
```
