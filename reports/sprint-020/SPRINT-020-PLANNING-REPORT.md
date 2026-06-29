# Sprint 020 Planning Report

- Sprint: Sprint 020
- Date: 2026-06-29
- Scope: Mobile foundation
- Statut propose: EN COURS

## 1. Resume du Sprint 019 herite

Sprint 019 est cloture officiellement. Le cycle Continuous Learning est stabilise et le programme entre dans la base mobile.

## 2. Objectif du Sprint 020

preparer une application mobile legere et synchronisee. Ce sprint correspond au bloc S020 du plan directeur d implementation et reste aligne avec `20-MOBILE-REFERENCE.md`, `21-UX-UI-DESIGN-SYSTEM.md` et `29-CAMPAY-PAYMENT-REFERENCE.md`.

## 3. Liste des tickets

- T20.01 | Mobile shell | entree: S004-T03 | sortie: poser navigation, themes et architecture cliente | dependances: 20-MOBILE-REFERENCE.md, 21-UX-UI-DESIGN-SYSTEM.md
- T20.02 | Offline sync | entree: S020-T01 | sortie: preparer cache local et recuperation des donnees | dependances: 20-MOBILE-REFERENCE.md, 06-DATABASE-REFERENCE.md
- T20.03 | Push and payment handoff | entree: S020-T02 | sortie: relayer les alertes et redirections de paiement | dependances: 20-MOBILE-REFERENCE.md, 29-CAMPAY-PAYMENT-REFERENCE.md

## 4. Ordre recommande

1. T20.01 - Mobile shell.
2. T20.02 - Offline sync.
3. T20.03 - Push and payment handoff.

T20.01 est le gate du sprint. Les autres tickets ne peuvent pas demarrer avant la consolidation du cadre mobile.

## 5. Dependances

- Decision DG-0028 d ouverture du programme en implementation continue.
- Confirmation de cloture du Sprint 019 et validation PCC.
- S020-T01 comme gate technique.
- S004.
- S012.
- S014.
- S015.
- S016.

## 6. Chemin critique

DG-0028 -> T20.01 -> T20.02 -> T20.03 -> cloture Sprint 020.

T20.01 est le gate dur. Les autres tickets ne peuvent pas demarrer avant lui et doivent tous etre disponibles avant qu un lancement du sprint soit considere coherent.

## 7. Risques

- fragmentation device, latence, incoherence offline/online.

## 8. Recommandations

- garder le shell mobile minimal et lisible;
- expliciter la synchronisation locale et la reprise des donnees;
- isoler le handoff de paiement et les notifications;
- ne pas ouvrir le Sprint 021 avant la cloture du Sprint 020.

## 9. Etat du PCC

- Programme status: ACTIF.
- Sprint status: EN COURS.
- Sprint 020: ouvert.
- Tickets couverts: 0/3.
- Blocking risk: false.
- Le premier ticket a ete trace et la suite reste ouverte.

## 10. Decision proposee au Directeur General

GO AVEC RESERVES. Le Sprint 020 peut continuer sous Standard V2, sans ouvrir le sprint suivant.

```yaml
sprint: 020
status: EN_COURS
planning: PASS
dependencies: VERIFIED
risks: ACCEPTABLE
blocking_risk: false
next_ticket: T20.01
decision_required: false
```
