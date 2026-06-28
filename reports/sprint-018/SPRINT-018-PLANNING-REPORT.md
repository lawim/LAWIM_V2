        # Sprint 018 Planning Report

        - Sprint: Sprint 018
        - Date: 2026-06-28
        - Scope: Preparation only
        - Statut propose: READY_FOR_DG_OPENING

        ## 1. Resume du Sprint 017 herite

        Sprint 017 est cloture officiellement. Les trois tickets planifies sont couverts, le risque bloquant reste false et le PCC est coherent avec la trace de cloture. Le lot precedent est consolide et la suite peut se concentrer sur lawim ai.

        ## 2. Objectif du Sprint 018

        brancher l'assistance IA sur les données, la langue et la connaissance. Ce sprint correspond au bloc S018 du plan directeur d implementation et reste aligne avec les references `18-LAWIM-AI-REFERENCE.md`, `27-TRACEABILITY-MATRIX.md`, `30C-LANGUAGE-DETECTION-REFERENCE.md`, `30D-MULTILINGUAL-SEARCH-REFERENCE.md`, `LAWIM-KNOWLEDGE-BASE-MASTER.md`.

        ## 3. Liste des tickets

        - T18.01 | AI service scaffold | entree: S017-T02 | sortie: poser la structure d'assistance IA | dependances: 18-LAWIM-AI-REFERENCE.md, LAWIM-KNOWLEDGE-BASE-MASTER.md
- T18.02 | Language and search intelligence | entree: S018-T01 | sortie: comprendre la langue et la requête | dependances: 30C-LANGUAGE-DETECTION-REFERENCE.md, 30D-MULTILINGUAL-SEARCH-REFERENCE.md
- T18.03 | Source-grounded responses | entree: S018-T02 | sortie: produire des réponses fondées sur les référentiels | dependances: 18-LAWIM-AI-REFERENCE.md, 27-TRACEABILITY-MATRIX.md

        ## 4. Ordre recommande

        1. T18.01 - AI service scaffold.
2. T18.02 - Language and search intelligence.
3. T18.03 - Source-grounded responses.

        T18.01 est le gate dur du sprint. Les autres tickets ne peuvent pas demarrer avant la consolidation du contrat precedent.

        ## 5. Dependances

        - Decision DG d'ouverture du Sprint 018.
        - Confirmation de cloture du sprint precedent et validation PCC.
        - S018-T01 comme gate technique.
        - `S017`.
- `S013`.
- `S016.`.

        ## 6. Chemin critique

        Confirmation de cloture du sprint precedent -> Decision DG d'ouverture -> T18.01 -> T18.02 -> T18.03 -> cloture Sprint 018.

        T18.01 est le gate dur. Les autres tickets ne peuvent pas demarrer avant lui et doivent tous etre disponibles avant qu'un lancement du sprint soit considere coherent.

        ## 7. Risques

        - hallucinations, mauvaise langue, sur-automatisation.

        ## 8. Recommandations

        - Reutiliser les references officielles avant toute creation de logique.
        - Garder le perimetre documentaire explicite et trace.
        - Conserver les secrets et les politiques hors depot.
        - Maintenir le gate dur comme condition de passage.

        ## 9. Etat du PCC

        - Sprint 017: TERMINE.
        - Tickets Sprint 017: 3/3 couverts.
        - Blocking risk: false.
        - PCC: coherent avec la cloture et les fondations heritees.
        - Sprint 018: prepare, non ouvert.
        - Aucun ticket Sprint 018 n existe encore.
        - Les registres dependances et risques restent alignes avec l'ouverture preparee.

        ## 10. Decision proposee au Directeur General

        GO AVEC RESERVES. Le Sprint 018 peut etre ouvert une fois la decision DG tracee, sous reserve de garder le perimetre strictement aligne avec les references officielles.

        ```yaml
        sprint: 018
        status: READY_FOR_DG_OPENING
        planning: PASS
        dependencies: VERIFIED
        risks: ACCEPTABLE
        blocking_risk: false
        next_ticket: T18.01
        decision_required: true
        ```
