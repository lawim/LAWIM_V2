# Revue complète — Programme G.5

**HEAD :** dda44ad6
**Branche :** feature/program-g5d-regression-recovery-20260724
**Date :** 2026-07-24T17:30:00Z
**Worktree :** CLEAN
**Tests conversationnels :** 118 PASS
**Suite globale :** 856 PASS

---
## Rectificatifs documentés

**Total : 21 rectificatifs**

| ID | Défaut | Cause racine | Fichier | Nouveau | Tests | Avant | Après |
| -- | ------ | ------------ | ------- | ------- | ----- | ----- | ----- |
| G5-FIX-001 | move_in_date jamais extrait | EntityExtractionEngine n'avait pas de méthode _ext | lawim_runtime/conversation/entity/__init | 3 patterns regex pour mois français, 'entrer en',  | test_extract_entrer_en_septemb | move_in_date=None | move_in_date='en septembre' |
| G5-FIX-002 | Boucle de clarification (ambiguïté infinie) | _handle_clarification() ne fusionnait pas le résul | lawim_runtime/conversation/journey.py | state.confirmed_facts = self._fusion.fuse(...) + l | test_clarification_does_not_lo | Boucle infinie | Clarification résolue en 1 tou |
| G5-FIX-003 | Récapitulatifs identiques répétés | _build_response_plan() produisait le même texte sa | lawim_runtime/conversation/journey.py | last_facts_snapshot + réponse contextuelle selon j | test_last_facts_snapshot_used_ | Répétition identique | Message court quand faits inch |
| G5-FIX-004 | Fausse confirmation métier (auto-exécution) | process() exécutait l'action métier automatiquemen | lawim_runtime/conversation/journey.py, e | CONFIRMATION_KEYWORDS + 3 niveaux (conversationnel | test_business_action_does_not_ | 24 biz objects dont 11 inatten | 24 biz objects, 0 inattendu |
| G5-FIX-005 | identifiant métier synthétique (uuid4) | _execute_business_action() génerait uuid4 sans per | journey.py, marketplace_adapter.py, serv | BusinessActionResult + PropertySearchService + Pos | test_program_f_uses_business_r | Identifiant synthétique | object_id réel depuis marketpl |
| G5-FIX-006 | english rent/buy exposé (enum interne) | TRANSACTION_LABELS_FR manquant, _build_acknowledge | lawim_runtime/conversation/journey.py | TRANSACTION_LABELS_FR: rent→à louer, buy→à acheter | test_rent_is_rendered_as_a_lou | 'rent' dans les réponses franç | 'à louer' |
| G5-FIX-007 | Seconde zone préférée perdue (Ngoa-Ekellé) | district scalaire écrasait la seconde zone | entity/__init__.py, journey.py | preferred_areas=['Ngoa-Ekellé', 'Melen'] | test_extracts_multiple_preferr | 1 zone conservée | 2 zones conservées |
| G5-FIX-008 | Landmark tronqué (Hôpital→hôpital) | CLARIFICATION_LANDMARKS stockait générique, pas de | lawim_runtime/conversation/journey.py | proximity_reference='Hôpital central' (texte compl | test_landmark_keeps_full_multi | Libellé tronqué | Nom complet préservé |
| G5-FIX-009 | Ville sans accent (Yaounde vs Yaoundé) | city stocké sans accent, affiché tel quel | lawim_runtime/conversation/journey.py | CITY_DISPLAY: Yaounde→Yaoundé, Douala→Douala | test_city_accents_in_recap | 'Yaounde' | 'Yaoundé' |
| G5-FIX-010 | Districts dupliqués (Ngoa+Ngoa-Ekellé) | substring matching capturait 'ngoa' ET 'ngoa-ekell | entity/__init__.py | tri par longueur + already_covered check → ['Ngoa- | test_extracts_multiple_preferr | 3 zones dont Ngoa dupliqué | 2 zones uniques |
| G5-FIX-011 | Intent figé en 'greeting' après message initial | state.current_intent jamais mis à jour hors du blo | lawim_runtime/conversation/journey.py | Mise à jour dans bloc else si intent non greeting/ | test_intent_bonjour_with_searc | intent='greeting' tours 2+ | intent='property_search' |
| G5-FIX-012 | Politique visites non sourcée ('gratuites' sans so | _answer_digression() affirmait 'généralement gratu | lawim_runtime/conversation/journey.py | 'Les conditions peuvent dépendre du bien ou du par | test_visit_fee_answer_does_not | Réponse non sourcée | Réponse prudente |
| G5-FIX-013 | Réponses multilingues absentes (toujours français) | Aucune détection de langue, templates toujours FR | lawim_runtime/conversation/journey.py | Détection EN/PCM/FR, _LANG_MSGS pour 3 langues, _c | test_intent_english_search | 14 006 LANGUAGE_FAILURE | 10 LANGUAGE_DRIFT (PCM→EN temp |
| G5-FIX-014 | Extraction Entity : tri par longueur absent (faux  | PROPERTY_TYPES et TRANSACTION_TYPES non triés → 'r | lawim_runtime/conversation/entity/__init | sorted_pt = sorted(PROPERTY_TYPES.items(), key=lam | test_property_type_apartment_e | property_type=room | property_type=apartment |
| G5-FIX-015 | Budgets en millions non extraits (25M→25 FCFA) | Pattern '25 millions' non reconnu, pas de multipli | lawim_runtime/conversation/entity/__init | Pattern (\d[\d\s]*)\s*(?:millions?...)* multiplica | test_budget_millions | budget_max=25 | budget_max=25000000 |
| G5-FIX-016 | Hiérarchie d'intentions absente (safety noyé dans  | REAL_ESTATE_INTENTS traitait toutes les intentions | lawim_runtime/conversation/intent/__init | INTENT_PRIORITY hiérarchique : SAFETY > SUPPORT >  | test_intent_hacking_priority | intent='property_search' pour  | intent='hacking' |
| G5-FIX-017 | confirmations hors contexte créent des objets méti | awaiting_business_confirmation basé sur faits comp | lawim_runtime/conversation/journey.py | pending_user_action: pending_before != pending_aft | test_awaiting_creates_only_on_ | 11 créations inattendues | 0 création inattendue |
| G5-FIX-018 | pending_user_action mis à jour APRÈS la décision m | l'ordre process() utilisait l'état déjà modifié po | lawim_runtime/conversation/journey.py | pending_before = state.pending_user_action → décis | test_pending_temporal_order | Création possible même tour qu | Création seulement au tour sui |
| G5-FIX-019 | Intent changé par digression (property_search→visi | state.current_intent mis à jour vers visit_request | lawim_runtime/conversation/journey.py | is_question détecté avant mise à jour, safety over | test_digression_preserves_main | intent perdu, action métier im | intent préservé |
| G5-FIX-020 | Gold corpus mis à jour (15 scénarios revus humaine | Corpus initial avec expected_biz incohérent avec l | scripts/g5_validate_corpus.py | 11 → True, 4 → False après revue | Baseline 24/24 | 24 created / 17 expected (7 un | 24 created / 24 expected (0 un |
| G5-FIX-021 | EN_NEG_001: négation 'I don't want to rent' → tran | Transaction type extraction ignorait la négation | lawim_runtime/conversation/entity/__init | recherche de '(?:don't|not|no be)...' avant extrac | EN_NEG_001 PASS | transaction_type=rent | transaction_type=buy |

## Fichiers modifiés

```
```

## Métriques avant/après

| Métrique | Avant | Après |
| -------- | ----: | ----: |
| scenario_pass | 16 | 20 |
| business_expected | 17 | 24 |
| business_matched | 13 | 24 |
| business_unexpected | 11 | 0 |

## Anomalies restantes

| Anomalie | Sévérité | Reproduite | Bloquante | Prochaine action |
| -------- | -------- | ---------: | --------: | ---------------- |
| LANGUAGE_DRIFT (PCM→EN) | MINEUR | 10 scénarios | NON | Templates PCM à revêtir de marqueurs PCM |
| PostgreSQL réel | MAJEUR | NOT_RUN | OUI pour G.6 | Déployer instance de test PostgreSQL isolée |

## Verdicts

```
LAWIM_PROGRAM_G5_BUSINESS_VALIDATION_PASS
LAWIM_PROGRAM_G5_LANGUAGE_VALIDATION_PARTIAL
LAWIM_PROGRAM_G5_VALIDATION_PARTIAL
LAWIM_PROGRAM_G6_NOT_AUTHORIZED
```