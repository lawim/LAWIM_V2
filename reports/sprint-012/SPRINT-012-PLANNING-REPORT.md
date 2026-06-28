        # Sprint 012 Planning Report

        - Sprint: Sprint 012
        - Date: 2026-06-28
        - Scope: Preparation only
        - Statut propose: READY_FOR_DG_OPENING

        ## 1. Resume du Sprint 011 herite

        Sprint 011 est cloture officiellement. Les trois tickets planifies sont couverts, le risque bloquant reste false et le PCC est coherent avec la trace de cloture. Le lot precedent est consolide et la suite peut se concentrer sur notifications.

        ## 2. Objectif du Sprint 012

        diffuser les messages au bon moment et par le bon canal. Ce sprint correspond au bloc S012 du plan directeur d implementation et reste aligne avec les references `06-DATABASE-REFERENCE.md`, `10-NOTIFICATION-REFERENCE.md`, `29-CAMPAY-PAYMENT-REFERENCE.md`, `30-I18N-L10N-REFERENCE.md`.

        ## 3. Liste des tickets

        - T12.01 | Notification model | entree: S011-T03 | sortie: structurer les notifications et leur trace | dependances: 10-NOTIFICATION-REFERENCE.md, 06-DATABASE-REFERENCE.md
- T12.02 | Channel adapters | entree: S012-T01 | sortie: brancher les canaux officiels | dependances: 10-NOTIFICATION-REFERENCE.md, 29-CAMPAY-PAYMENT-REFERENCE.md
- T12.03 | Templates and preferences | entree: S012-T02 | sortie: centraliser les gabarits et préférences | dependances: 10-NOTIFICATION-REFERENCE.md, 30-I18N-L10N-REFERENCE.md

        ## 4. Ordre recommande

        1. T12.01 - Notification model.
2. T12.02 - Channel adapters.
3. T12.03 - Templates and preferences.

        T12.01 est le gate dur du sprint. Les autres tickets ne peuvent pas demarrer avant la consolidation du contrat precedent.

        ## 5. Dependances

        - Decision DG d'ouverture du Sprint 012.
        - Confirmation de cloture du sprint precedent et validation PCC.
        - S012-T01 comme gate technique.
        - `S011`.
- `S004.`.

        ## 6. Chemin critique

        Confirmation de cloture du sprint precedent -> Decision DG d'ouverture -> T12.01 -> T12.02 -> T12.03 -> cloture Sprint 012.

        T12.01 est le gate dur. Les autres tickets ne peuvent pas demarrer avant lui et doivent tous etre disponibles avant qu'un lancement du sprint soit considere coherent.

        ## 7. Risques

        - bruit, doublons, mauvaise priorité.

        ## 8. Recommandations

        - Reutiliser les references officielles avant toute creation de logique.
        - Garder le perimetre documentaire explicite et trace.
        - Conserver les secrets et les politiques hors depot.
        - Maintenir le gate dur comme condition de passage.

        ## 9. Etat du PCC

        - Sprint 011: TERMINE.
        - Tickets Sprint 011: 3/3 couverts.
        - Blocking risk: false.
        - PCC: coherent avec la cloture et les fondations heritees.
        - Sprint 012: prepare, non ouvert.
        - Aucun ticket Sprint 012 n existe encore.
        - Les registres dependances et risques restent alignes avec l'ouverture preparee.

        ## 10. Decision proposee au Directeur General

        GO AVEC RESERVES. Le Sprint 012 peut etre ouvert une fois la decision DG tracee, sous reserve de garder le perimetre strictement aligne avec les references officielles.

        ```yaml
        sprint: 012
        status: READY_FOR_DG_OPENING
        planning: PASS
        dependencies: VERIFIED
        risks: ACCEPTABLE
        blocking_risk: false
        next_ticket: T12.01
        decision_required: true
        ```
