        # Sprint 015 Planning Report

        - Sprint: Sprint 015
        - Date: 2026-06-28
        - Scope: Preparation only
        - Statut propose: READY_FOR_DG_OPENING

        ## 1. Resume du Sprint 014 herite

        Sprint 014 est cloture officiellement. Les trois tickets planifies sont couverts, le risque bloquant reste false et le PCC est coherent avec la trace de cloture. Le lot precedent est consolide et la suite peut se concentrer sur dashboard foundation.

        ## 2. Objectif du Sprint 015

        fournir les vues de pilotage essentielles. Ce sprint correspond au bloc S015 du plan directeur d implementation et reste aligne avec les references `07-DASHBOARD-REFERENCE.md`, `08-ROLE-REFERENCE.md`, `19-ADMINISTRATION-REFERENCE.md`, `21-UX-UI-DESIGN-SYSTEM.md`.

        ## 3. Liste des tickets

        - T15.01 | Dashboard shell | entree: S013-T03 | sortie: créer le cadre visuel de pilotage | dependances: 07-DASHBOARD-REFERENCE.md, 21-UX-UI-DESIGN-SYSTEM.md
- T15.02 | Admin views | entree: S015-T01 | sortie: afficher les métriques administratives | dependances: 07-DASHBOARD-REFERENCE.md, 19-ADMINISTRATION-REFERENCE.md
- T15.03 | Role-based views | entree: S015-T02 | sortie: adapter les vues selon les rôles | dependances: 08-ROLE-REFERENCE.md, 07-DASHBOARD-REFERENCE.md

        ## 4. Ordre recommande

        1. T15.01 - Dashboard shell.
2. T15.02 - Admin views.
3. T15.03 - Role-based views.

        T15.01 est le gate dur du sprint. Les autres tickets ne peuvent pas demarrer avant la consolidation du contrat precedent.

        ## 5. Dependances

        - Decision DG d'ouverture du Sprint 015.
        - Confirmation de cloture du sprint precedent et validation PCC.
        - S015-T01 comme gate technique.
        - `S013`.
- `S014.`.

        ## 6. Chemin critique

        Confirmation de cloture du sprint precedent -> Decision DG d'ouverture -> T15.01 -> T15.02 -> T15.03 -> cloture Sprint 015.

        T15.01 est le gate dur. Les autres tickets ne peuvent pas demarrer avant lui et doivent tous etre disponibles avant qu'un lancement du sprint soit considere coherent.

        ## 7. Risques

        - surcharge visuelle, incohérence entre rôles.

        ## 8. Recommandations

        - Reutiliser les references officielles avant toute creation de logique.
        - Garder le perimetre documentaire explicite et trace.
        - Conserver les secrets et les politiques hors depot.
        - Maintenir le gate dur comme condition de passage.

        ## 9. Etat du PCC

        - Sprint 014: TERMINE.
        - Tickets Sprint 014: 3/3 couverts.
        - Blocking risk: false.
        - PCC: coherent avec la cloture et les fondations heritees.
        - Sprint 015: prepare, non ouvert.
        - Aucun ticket Sprint 015 n existe encore.
        - Les registres dependances et risques restent alignes avec l'ouverture preparee.

        ## 10. Decision proposee au Directeur General

        GO AVEC RESERVES. Le Sprint 015 peut etre ouvert une fois la decision DG tracee, sous reserve de garder le perimetre strictement aligne avec les references officielles.

        ```yaml
        sprint: 015
        status: READY_FOR_DG_OPENING
        planning: PASS
        dependencies: VERIFIED
        risks: ACCEPTABLE
        blocking_risk: false
        next_ticket: T15.01
        decision_required: true
        ```
