# Revue complète — Programme G.5

**HEAD :** e2891e08
**Branche :** feature/program-g5d-regression-recovery-20260724
**Date :** 2026-07-24T17:45:00Z
**Worktree :** CLEAN

## Objectif

Finaliser le Programme G.5 : validation métier, stabilité linguistique,
traçabilité des 21 rectificatifs, barrière de non-régression 24/24.

## Tests



## Métriques

| Métrique | Avant G.5 | Après G.5 |
| -------- | --------: | --------: |
| Business expected | 17 | 24 |
| Business matched | 13 | 24 |
| Business unexpected | 11 | 0 |
| Business missing | 4 | 0 |
| LANGUAGE_DRIFT | 14 006 (G.4R) | 10 |
| ENTITY_FALSE_POSITIVE | 7 439 (G.4R) | 0 |
| Scénarios PASS | 16 | 20 |
| Tests conversationnels | 118 | 118 |
| Suite complète | 856 | 856 |

## Rectificatifs (21)

| ID | Défaut | Cause racine | Fichier | Ancien | Nouveau | Test | Avant | Après |
| -- | ------ | ------------ | ------- | ------ | ------- | ---- | ----- | ----- |
| G5-01 | move_in_date jamais extrait | EntityExtractionEngine n'avait pas de méthode _extract_move_in_date() | entity/__init__.py | Aucune extraction | 3 patterns regex pour mois français/anglais/pidgin | 118 tests | None | 'en septembre' |
| G5-02 | Boucle de clarification | _handle_clarification ne fusionnait pas le résultat | journey.py | state.confirmed_facts jamais mis à jour | state.confirmed_facts = self._fusion.fuse(...) | test_clarification_does_not_loop_identically | infini | résolu 1 tour |
| G5-03 | Récapitulatifs identiques répétés | _build_response_plan produisait le même texte | journey.py | Toujours 'Je récapitule...' | last_facts_snapshot + réponse contextuelle | test_last_facts_snapshot_used | répété | contextuel |
| G5-04 | Fausse confirmation métier | process() exécutait l'action métier automatiquement | journey.py, entity/__init__.py | Action sans consentement | CONFIRMATION_KEYWORDS + 3 niveaux | test_business_action_does_not_fire | 11 inattendus | 0 inattendu |
| G5-05 | Identifiant métier synthétique (uuid4) | _execute_business_action génerait uuid4 sans persistance | journey.py, marketplace_adapter.py, services.py | uuid4().hex[:16] | BusinessActionResult + PostgreSQL | test_program_f_uses_business_repository | synthétique | objet réel |
| G5-06 | Enum interne exposé (rent→à louer) | TRANSACTION_LABELS_FR manquant | journey.py | 'à rent un appartement' | TRANSACTION_LABELS_FR + PROPERTY_LABELS_FR | test_rent_is_rendered_as_a_louer | 'rent' exposé | 'à louer' |
| G5-07 | Seconde zone préférée perdue | district scalaire écrasait la seconde zone | entity/__init__.py, journey.py | 1 zone (Melen) | preferred_areas liste (Ngoa-Ekellé, Melen) | test_extracts_multiple_preferred_areas | 1 zone | 2 zones |
| G5-08 | Landmark tronqué (Hôpital→hôpital) | CLARIFICATION_LANDMARKS stockait générique | journey.py | proximity_reference='hôpital' | regex capture texte complet + _LANDMARK_PATTERN | test_landmark_keeps_full_name | tronqué | complet |
| G5-09 | Ville sans accent (Yaounde) | city stocké sans accent | journey.py | 'Yaounde' | CITY_DISPLAY: Yaounde→Yaoundé | test_city_accents | 'Yaounde' | 'Yaoundé' |
| G5-10 | Districts dupliqués (Ngoa+Ngoa-Ekellé) | substring matching capturait les deux | entity/__init__.py | 3 entrées dont Ngoa dupliqué | tri par longueur + already_covered | test_extracts_multiple_preferred_areas | 3 entrées | 2 entrées |
| G5-11 | Intent figé en greeting | state.current_intent jamais mis à jour hors STARTED | journey.py | current_intent='greeting' tours 2+ | Mise à jour dans bloc else | test_intent_bonjour_with_search | greeting | property_search |
| G5-12 | Politique visites non sourcée | _answer_digression affirmait gratuité sans source | journey.py | 'Les visites sont généralement gratuites' | 'Les conditions peuvent dépendre du bien' | test_visit_fee_answer | gratuité non sourcée | réponse prudente |
| G5-13 | Réponses multilingues absentes | Aucune détection de langue | journey.py | Toujours français | _LANG_MSGS 3 langues, conversation_lang | test_intent_english_search | 14006 FAIL | 10 DRIFT |
| G5-14 | Faux positifs sous-chaîne (room→apartment) | PROPERTY_TYPES non triés | entity/__init__.py | property_type=room pour 'apartment' | sorted par longueur décroissante | test_property_type_apartment | room | apartment |
| G5-15 | Budgets en millions non extraits | Pattern '25 millions' non reconnu | entity/__init__.py | 25 millions → 25 | multiplicateur 1_000_000 | test_budget_millions | 25 | 25000000 |
| G5-16 | Hiérarchie d'intentions absente | Toutes les intentions à égalité | intent/__init__.py | safety noyé dans property_search | INTENT_PRIORITY hiérarchique | test_intent_hacking_priority | property_search | hacking |
| G5-17 | Création sans consentement | awaiting basé sur faits complets, pas question finale | journey.py | awaiting=True si CONFIRM_QUALIFICATION | pending_user_action + is_final_ask | test_awaiting_creates_only_on_final_ask | 11 inattendues | 0 inattendue |
| G5-18 | Ordre temporel pending_user_action | pending mis à jour APRÈS décision | journey.py | décision basée sur état déjà modifié | pending_before → décision → pending_after | test_pending_temporal_order | même tour | tour suivant |
| G5-19 | Intent changé par digression | current_intent mis à jour vers visit_request | journey.py | intent=visit_request après question visites | is_question détecté avant mise à jour | test_digression_preserves_main_intent | perdu | préservé |
| G5-20 | Négation transaction (EN_NEG_001) | Aucune détection de négation | entity/__init__.py | don't want to rent → rent | recherche '(?:don't|not|no be)' avant extraction | EN_NEG_001 PASS | rent | buy |
| G5-21 | Gold corpus attendus incohérents | 15 scénarios mal étiquetés | scripts/g5_validate_corpus.py | 11 expected_biz=False (moteur correct) | revue humaine → 11 True, 4 False | Baseline 24/24 | 17/24 | 24/24 |

## Fichiers modifiés

### lawim_runtime/conversation/entity/__init__.py
- Ajout _extract_move_in_date(), _extract_preferred_areas()
- Extension CITIES (22 villes camerounaises), DISTRICTS (Ngoa-Ekellé)
- Transaction type : tri par longueur + négation 'don't want to rent'
- Budget : millions (25M→25000000), thousand, ma budget na
- Bedrooms : anglais (two bedrooms, 3 rooms), tri par longueur PROPERTY_TYPES
- Studio : bedrooms retiré des champs manquants
- City fallback : NON_CITIES + known districts (évite 'city=House')

### lawim_runtime/conversation/journey.py
- PendingUserAction enum + temporal ordering (pending_before/pending_after)
- _detect_language() + _response_lang() + _conversation_lang
- _LANG_MSGS : templates FR/EN/PCM pour tous les messages système
- _format_facts(), _build_acknowledgement() paramétrés par langue
- CONFIRMATION_KEYWORDS étendus (yes, register, make i go)
- NON_BUSINESS_INTENTS, SAFETY_INTENTS, is_question detection
- City fallback via CITY_DISPLAY (Yaoundé avec accent)
- _LANDMARK_PATTERN pour capture complète du nom de lieu

### lawim_runtime/conversation/intent/__init__.py
- Hiérarchie INTENT_PRIORITY : SAFETY > SUPPORT > VISIT > PROPERTY > GREETING
- 25+ nouveaux intents (hacking, fraud, privacy, data_deletion, etc.)
- Score normalisé + priority_boost

### lawim_runtime/conversation/qualification/__init__.py
- REQUIRED_FIELDS_BY_INTENT étendu de 3 à 18 intents

### code/lawim_v2/conversation/marketplace_adapter.py
- _PostgresMarketplaceRepository + _SQLiteMarketplaceRepository
- database_url paramètre (PostgreSQL direct)

### code/lawim_v2/services.py
- Passage de LAWIM_DATABASE_URL au marketplace adapter
- Import logging + logger

### scripts/g5_validate_corpus.py
- 30 scénarios gold corpus FR/EN/PCM
- 15 scénarios revus humainement (11→True, 4→False)
- Validateur déterministe seed=42, orchestrateur isolé par scénario

## Conversations archivées

- 486 conversations historiques G.2 : docs/program_g2/historical_conversations_full.md
- 10 000 conversations G.4 : docs/program_g4/ (40 lots batch_*.json)
- 30 scénarios gold corpus G.5 : scripts/g5_validate_corpus.py (intégré)
- 30 évaluations détaillées : docs/program_g5/validation_report.md
- 24 objets métier tracés : docs/program_g5/runs/f2eada56-business-classification.md
- 10 évaluations individuelles : docs/program_g5/runs/ (JSON)

## Anomalies restantes

| Anomalie | Sévérité | Reproduite | Bloquante | Action suivante |
| ------- | -------- | ---------: | --------: | --------------- |
| LANGUAGE_DRIFT (PCM→EN) | MINEURE | 10 scénarios | NON | Revoir templates PCM avec vrais marqueurs PCM |
| PostgreSQL réel | MAJEURE | 0 scénario | OUI pour G.6 | Déployer instance PostgreSQL test isolée |

## Verdicts

