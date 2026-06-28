# Sprint 006 Planning Report

- Sprint: Sprint 006
- Date: 2026-06-28
- Scope: Preparation only
- Statut propose: READY_FOR_DG_OPENING

## 1. Resume du Sprint 005 herite

Sprint 005 est cloture officiellement. Les trois tickets planifies sont couverts, le risque bloquant reste false et le PCC est coherent avec la trace de cloture. Le socle utilisateurs, roles, organisations et permissions est consolide et la suite peut se concentrer sur le coeur immobilier.

## 2. Objectif du Sprint 006

Construire le socle des biens, attributs et prix de LAWIM_V2. Ce sprint correspond au bloc S006 du plan directeur d'implementation et reste aligne avec les references `02-PROPERTY-REFERENCE.md`, `02H-ATTRIBUTE-CATALOG.md`, `02I-PRICING-REFERENCE.md`, `11-REPORTING-REFERENCE.md`, `05-WORKFLOW-REFERENCE.md` et `12-TESTS-REFERENCE.md`.

## 3. Liste des tickets

| Ticket | Titre | Entree | Sortie | Dependances |
| --- | --- | --- | --- | --- |
| T06.01 | Property domain schema | Sprint 005 cloture, PCC coherent, T05.03 valide, references property et attributes disponibles | Structure centrale des biens, statuts et relations de base | T05.03, 02-PROPERTY-REFERENCE.md, 02H-ATTRIBUTE-CATALOG.md |
| T06.02 | Pricing alignment | T06.01 ferme, modele des biens confirme | Regles de saisie, devises, plages de prix et variations | T06.01, 02I-PRICING-REFERENCE.md, 11-REPORTING-REFERENCE.md |
| T06.03 | Publication guardrails | T06.02 ferme, regles de prix confirmees | Controles pre-publication et statuts de publication | T06.02, 05-WORKFLOW-REFERENCE.md, 12-TESTS-REFERENCE.md |

## 4. Ordre recommande

1. T06.01 - Property domain schema.
2. T06.02 - Pricing alignment.
3. T06.03 - Publication guardrails.

T06.01 reste le gate dur du sprint. T06.02 et T06.03 ne peuvent pas demarrer avant la consolidation du modele des biens.

## 5. Dependances

- Decision DG d'ouverture du Sprint 006.
- Confirmation de cloture Sprint 005 et validation PCC.
- T05.03 comme gate technique.
- `02-PROPERTY-REFERENCE.md` pour le modele maître des biens.
- `02H-ATTRIBUTE-CATALOG.md` pour la normalisation des attributs.
- `02I-PRICING-REFERENCE.md` pour les prix et les variations.
- `11-REPORTING-REFERENCE.md` pour la lecture des prix et des indicateurs.
- `05-WORKFLOW-REFERENCE.md` pour les statuts et le cycle de publication.
- `12-TESTS-REFERENCE.md` pour les guardrails et la validation.

## 6. Chemin critique

Confirmation de cloture Sprint 005 -> Decision DG d'ouverture -> T06.01 -> T06.02 -> T06.03 -> cloture Sprint 006.

T06.01 est le gate dur. T06.02 et T06.03 ne peuvent pas demarrer avant lui et doivent tous deux etre disponibles avant qu'un lancement du sprint soit considere coherent.

## 7. Risques

- Des donnees incoherentes pourraient rendre les biens difficilement exploitables.
- Une confusion entre types de biens pourrait casser le modele maître.
- Une variation de prix non normalisee pourrait fausser les comparaisons et le reporting.
- Une publication incoherente pourrait exposer des biens incomplets ou invalides.

## 8. Recommandations

- Reutiliser les references property, attributes, pricing, workflow et tests avant toute creation de logique.
- Garder la normalisation des attributs comme socle du modele des biens.
- Conserver les guardrails de publication stricts et traces.
- Maintenir T06.01 comme gate dur pour la suite du sprint.

## 9. Etat du PCC

- Sprint 005: TERMINE.
- Tickets Sprint 005: 3/3 couverts.
- Blocking risk: false.
- PCC: coherent avec la cloture et les fondations heritees.
- Sprint 006: prepare, non ouvert.
- Aucun ticket Sprint 006 n existe encore.
- Les registres dependances et risques restent alignes avec l'ouverture preparee.

## 10. Decision proposee au Directeur General

GO AVEC RESERVES. Le Sprint 006 peut etre ouvert une fois la decision DG tracee, sous reserve de garder les biens, les attributs et les prix strictement alignes avec les references officielles.

```yaml
sprint: 006
status: READY_FOR_DG_OPENING
planning: PASS
dependencies: VERIFIED
risks: ACCEPTABLE
blocking_risk: false
next_ticket: T06.01
decision_required: true
```
