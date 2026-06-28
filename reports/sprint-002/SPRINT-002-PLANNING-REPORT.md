# Sprint 002 Planning Report

- Sprint: Sprint 002
- Date: 2026-06-28
- Scope: Preparation only
- Statut propose: READY_FOR_DG_OPENING

## 1. Resume du Sprint 001 herite

Sprint 001 est cloture officiellement. Les 10 tickets planifies sont couverts, le risque bloquant reste false et le PCC est coherent avec la trace de cloture. T01.04 reste couvert par `env/README.md` et les fichiers `*.env.example` / `*.secrets.example`.

## 2. Objectif du Sprint 002

Mettre en place un runtime local reproductible, une observabilite de base et un squelette CI minimal pour preparer l'execution controlee du programme, sans ouvrir de ticket et sans modifier la gouvernance.

## 3. Liste des tickets

| Ticket | Titre | Entree | Sortie | Dependances |
| --- | --- | --- | --- | --- |
| T02.01 | Docker baseline | Sprint 001 cloture, PCC coherent, contrat d'environnement confirme | Base runtime reproductible, stack locale stable, conventions de build et de tag reutilisables | T01.01, T01.02, T01.03, T01.04, T01.05 |
| T02.02 | Runtime observability | T02.01 ferme, conventions logging et monitoring disponibles | Logs visibles, health checks exposes, signaux de degradation lisibles | T02.01, T01.09, T01.10 |
| T02.03 | CI skeleton | T02.01 ferme, conventions secrets et CI/CD disponibles | Pipeline minimal build, lint et smoke tests, branches gatees, aucun secret reel | T02.01, T01.07, T01.08 |

## 4. Ordre recommande

1. T02.01 - Docker baseline.
2. T02.02 - Runtime observability.
3. T02.03 - CI skeleton.
4. T02.02 et T02.03 peuvent etre prepares en parallele apres T02.01 si le DG autorise une execution parallele, mais T02.01 reste le gate obligatoire.

## 5. Dependances

- Decision DG d'ouverture du Sprint 002.
- Confirmation de cloture Sprint 001 et validation PCC.
- T01.01, T01.02, T01.03, T01.04 et T01.05 pour la base runtime.
- T01.09 et T01.10 pour l'observabilite.
- T01.07 et T01.08 pour le squelette CI.
- T02.01 comme gate commun pour T02.02 et T02.03.

## 6. Chemin critique

Confirmation de cloture Sprint 001 -> Decision DG d'ouverture -> T02.01 -> gate commun T02.02 / T02.03 -> Sprint 002 pret pour execution.

T02.01 est le gate dur. T02.02 et T02.03 ne peuvent pas demarrer avant lui et doivent tous deux etre disponibles avant qu'un lancement de Sprint 002 soit considere coherent.

## 7. Risques

- Ouvrir Sprint 002 avant que la trace de cloture du Sprint 001 soit pleinement prise en compte creerait un ecart de gouvernance. Mitigation: rester en preparation uniquement jusqu'a la decision DG.
- Un drift entre la base runtime et les conventions heritees pourrait reintroduire des comportements non reproductibles. Mitigation: reutiliser la base partagee et valider les overlays de maniere deterministe.
- L'activation trop precoce de l'observabilite ou du CI pourrait exposer des secrets ou masquer des defauts. Mitigation: garder les secrets externes et valider le masquage des logs ainsi que les health checks avant activation.

## 8. Recommandations

- Ne pas ouvrir de ticket Sprint 002 avant la decision DG d'ouverture.
- Limiter T02.01 a la reproductibilite du runtime et aux conventions de base.
- Reutiliser les conventions Sprint 001 sans renommage des contrats Docker, Compose, environnements, secrets et CI/CD.
- Traiter observabilite et CI skeleton comme de la preparation non destructive.
- Maintenir le freeze PCC jusqu'a la validation DG.

## 9. Etat du PCC

- Sprint 001: TERMINE.
- Tickets Sprint 001: 10/10 couverts.
- Blocking risk: false.
- PCC: coherent avec la cloture et les fondations heritees.
- Sprint 002: prepare, non ouvert.
- Aucun ticket Sprint 002 n'existe encore.
- Les registres dependances et risques sont alignes avec l'ouverture preparee.

## 10. Decision proposee au Directeur General

GO AVEC RESERVES. Le Sprint 002 peut etre ouvert une fois la decision DG tracee, sous reserve de conserver les contrats runtime, secrets et observabilite herites du Sprint 001 sans derive.

```yaml
sprint: 002
status: READY_FOR_DG_OPENING
planning: PASS
dependencies: VERIFIED
risks: ACCEPTABLE
blocking_risk: false
next_ticket: T02.01
decision_required: true
```
