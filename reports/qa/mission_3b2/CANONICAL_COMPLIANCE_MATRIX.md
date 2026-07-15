# CANONICAL COMPLIANCE MATRIX — Mission 3B.2 Vague 1

**Date:** 2026-07-15
**Canonical Baseline:** d30d61e1d89427ece9c180cec4639cce77fdcba3
**Exigence:** REBUILD_FROM_ZERO (Conversation, Qualification, Search, Matching, Relationship)

---

## 1. SEARCH — Criteria-based, zero-result handled, no external platforms

| Req ID | Exigence | Domaine | Scénario | Test | Preuve | Statut | Écart |
|--------|----------|---------|----------|------|--------|--------|-------|
| SRC-01 | Search transforme critères qualifiés en requêtes sur sources autorisées | Search | Qualification → recherche structurée | `test_qualification_matrices.py` | Matrices de qualification, readiness score | Partiel | Pas de test d'appel au moteur de recherche |
| SRC-02 | Zéro résultat ne produit pas de fausse proposition | Search | Recherche sans résultat | `test_states.py:transition_searching_zero_results` | Transition `zero_results` → back to QUALIFYING | Partiel | Pas de test vérifiant l'explication des critères bloquants |
| SRC-03 | Zéro résultat explique critères bloquants | Search | Recherche sans résultat | Aucun | — | Non couvert | Absence totale de tests d'explication de zéro résultat |
| SRC-04 | Zéro résultat propose élargir, alerte ou agent LAWIM | Search | Recherche sans résultat | Aucun | — | Non couvert | Aucun test de propositions alternatives |
| SRC-05 | Aucune plateforme externe non autorisée | Search | Sources autorisées uniquement | Aucun | — | Non couvert | Aucun test de vérification des sources |
| SRC-06 | Recherche basée sur critères uniquement | Search | Qualification complète → READY_FOR_SEARCH | `test_behavioral.py:TestSearchNotLaunchedWithoutMinimumQualification` | Readiness score, required fields | Conforme | Tests valident les critères minimaux |
| SRC-07 | Disponibilité, filtres, recherche active et alertes | Search | Gestion des résultats | Aucun | — | Non couvert | Pas de test de filtres, alertes ou recherche active |

---

## 2. MATCHING — Explainable scoring, deterministic, no insufficient criteria

| Req ID | Exigence | Domaine | Scénario | Test | Preuve | Statut | Écart |
|--------|----------|---------|----------|------|--------|--------|-------|
| MTC-01 | Matching classe par critères obligatoires et préférentiels | Matching | Classement des candidats | Aucun | — | Non couvert | Pas de test de scoring |
| MTC-02 | Score explicable avec raisons principales | Matching | Explicabilité du score | Aucun | — | Non couvert | Aucun test de transparence du score |
| MTC-03 | Pas de matching avec critères insuffisants | Matching | Critères insuffisants → pas de matching | `test_behavioral.py:TestMatchingNotCreatedWithoutRealResults` | Vérification état avant matching | Conforme | Test unitaire présent |
| MTC-04 | Pas de relation créée par Matching | Matching | Séparation Matching → Relationship | `test_behavioral.py:TestRelationshipNotCreatedWithoutConsent` | Consentement requis avant relation | Conforme | Domaines bien séparés |
| MTC-05 | Pas de données privées dans un résultat | Matching | Résultat sans données privées | `test_behavioral.py:TestPrivateCoordinatesNeverSharedBeforeAuthorization` | Coordonnées absentes de l'extraction | Conforme | Test présent |
| MTC-06 | Score déterministe | Matching | Mêmes entrées → même score | `test_behavioral.py:TestIdenticalDecisionInIdenticalContextRemainsDeterministic` | Déterminisme prouvé | Conforme | Tests de normalisation déterministe |
| MTC-07 | Pas de score opaque comme unique justification | Matching | Explicabilité obligatoire | Aucun | — | Non couvert | Pas de test de justification du score |

---

## 3. RELATIONSHIP — Consent-first, no relationship without consent

| Req ID | Exigence | Domaine | Scénario | Test | Preuve | Statut | Écart |
|--------|----------|---------|----------|------|--------|--------|-------|
| REL-01 | Aucune relation sans consentement explicite | Relationship | Consentement requis | `test_behavioral.py:TestRelationshipNotCreatedWithoutConsent` | Consentement requis avant transition | Conforme | Tests unitaires valides |
| REL-02 | Consentement de chaque partie requise | Relationship | Double consentement | Aucun | — | Non couvert | Pas de test de consentement multipartite |
| REL-03 | Aucune donnée privée avant consentement | Relationship | Partage conditionnel | `test_behavioral.py:TestPrivateCoordinatesNeverSharedBeforeAuthorization` | Absence de coordonnées dans extraction | Conforme | Test présent |
| REL-04 | Fiche partageable = vue limitée, pas l'objet complet | Relationship | Partage de fiche | Aucun | — | Non couvert | Pas de test de fiche partageable |
| REL-05 | Interlocuteur actif toujours visible et audité | Relationship | Traçabilité | Aucun | — | Non couvert | Pas de test d'audit d'interlocuteur |
| REL-06 | LAWIM coordonne sans se substituer | Relationship | Limitation du rôle LAWIM | Aucun | — | Non couvert | Pas de test de non-substitution |
| REL-07 | Proposition + identité + consentement → relation | Relationship | Cycle de vie complet | `test_states.py` | Transitions consent_granted → RELATIONSHIP_PROPOSED → RELATIONSHIP_ACTIVE | Partiel | Transitions testées mais pas le cycle complet avec parties |

---

## 4. PRIVACY — No private data shared before consent

| Req ID | Exigence | Domaine | Scénario | Test | Preuve | Statut | Écart |
|--------|----------|---------|----------|------|--------|--------|-------|
| PRV-01 | Minimisation, finalité, consentement explicite | Privacy | Principes généraux | Aucun | — | Non couvert | Pas de test de minimisation |
| PRV-02 | Consentement lié: acteur, finalité, données, durée, preuve | Privacy | Structure du consentement | Aucun | — | Non couvert | Pas de test de structure Consent |
| PRV-03 | Refus possible sans échec technique | Privacy | Refus de consentement | `test_states.py:transition_consent_denied` | Transition consent_denied → QUALIFYING | Conforme | Test présent |
| PRV-04 | Retrait possible | Privacy | Révocation de consentement | Aucun | — | Non couvert | Pas de test de révocation |
| PRV-05 | Données sensibles protégées | Privacy | Protection des données | `test_behavioral.py:TestPrivateCoordinatesNeverSharedBeforeAuthorization` | Pas de coordonnées dans l'extraction standard | Conforme | Test présent |
| PRV-06 | Aucun partage avant consentement et finalité claire | Privacy | Partage conditionnel | Aucun | — | Non couvert | Pas de test de vérification finalité |
| PRV-07 | Séparation des rôles | Privacy | RBAC | Aucun | — | Non couvert | Pas de test de séparation des rôles |

---

## 5. OMNICHANNEL — Channels are adapters only, no business logic

| Req ID | Exigence | Domaine | Scénario | Test | Preuve | Statut | Écart |
|--------|----------|---------|----------|------|--------|--------|-------|
| CHN-01 | Canaux = adaptateurs techniques uniquement | Omnichannel | Canal sans logique métier | Aucun | — | Non couvert | Aucun test d'isolation des canaux |
| CHN-02 | Aucune logique de décision dans canal | Omnichannel | Décision centralisée | Aucun | — | Non couvert | Pas de test de non-décision par canal |
| CHN-03 | Aucune mémoire métier dans canal | Omnichannel | Mémoire centralisée | Aucun | — | Non couvert | Pas de test de centralisation mémoire |
| CHN-04 | Identité de canal liée à User | Omnichannel | Lien canal-utilisateur | Aucun | — | Non couvert | Pas de test de liaison d'identité |
| CHN-05 | Vérification du canal avant action sensible | Omnichannel | Sécurité canal | Aucun | — | Non couvert | Pas de test de vérification |
| CHN-06 | Idempotence des webhooks | Omnichannel | Webhooks | Aucun | — | Non couvert | Pas de test d'idempotence |
| CHN-07 | Normalisation des messages entrants | Omnichannel | Normalisation | `test_message.py` | NormalizedMessage structuré | Conforme | Normalisation testée |
| CHN-08 | Continuité cross-channel sans perte d'état | Omnichannel | Changement de canal | `test_behavioral.py:TestChannelChangeDoesNotLoseProjectDossierFacts` | Project, dossier, facts, state préservés | Conforme | Tests valides |
| CHN-09 | Handover humain cohérent entre canaux | Omnichannel | Handover | Aucun | — | Non couvert | Pas de test handover cross-canal |

---

## 6. AI GOVERNANCE — LLM is linguistic capability only, doesn't decide

| Req ID | Exigence | Domaine | Scénario | Test | Preuve | Statut | Écart |
|--------|----------|---------|----------|------|--------|--------|-------|
| AI-01 | LLM = capacité linguistique interchangeable | AI Governance | Interchangeabilité | Aucun | — | Non couvert | Pas de test de substituabilité |
| AI-02 | Sorties non souveraines sans validation LAWIM | AI Governance | Validation des sorties | Aucun | — | Non couvert | Pas de test de validation |
| AI-03 | Extraction linguistique autorisée | AI Governance | Extraction | `test_extractor.py` | Extraction fonctionnelle | Conforme | Tests présents |
| AI-04 | Reformulation, résumé, classification autorisés | AI Governance | Traitement linguistique | Aucun | — | Non couvert | Pas de test spécifique LLM |
| AI-05 | Pas de possession de règles métier par LLM | AI Governance | Règles déléguées au runtime | Aucun | — | Non couvert | Pas de test de séparation règles/LLM |
| AI-06 | Pas d'écriture directe de la mémoire canonique | AI Governance | Mémoire protégée | Aucun | — | Non couvert | Pas de test de protection mémoire |
| AI-07 | Pas de prise de décision par LLM | AI Governance | Décision runtime | `test_behavioral.py:TestLLMFailureDoesNotBlockDeterministicPath` | Extraction sans LLM, transitions sans LLM | Conforme | Fonctionnalités déterministes sans LLM |
| AI-08 | Pas de création de relation par LLM | AI Governance | Relation protégée | REL-01 | Consentement requis | Conforme | Redondant avec REL-01 |
| AI-09 | Pas d'autorisation de paiement par LLM | AI Governance | Paiement protégé | Aucun | — | Non couvert | Pas de test financier |
| AI-10 | Pas de contournement de Feature Flag | AI Governance | Feature flags | Aucun | — | Non couvert | Pas de test de kill switch |
| AI-11 | Rédaction des données sensibles | AI Governance | Protection données | Aucun | — | Non couvert | Pas de test de rédaction |
| AI-12 | Circuit breaker, fallback interne | AI Governance | Résilience | Aucun | — | Non couvert | Pas de test de circuit breaker |
| AI-13 | Journalisation des appels | AI Governance | Audit | Aucun | — | Non couvert | Pas de test de journalisation AI |
| AI-14 | Kill switch fournisseur | AI Governance | Interrupteur | Aucun | — | Non couvert | Pas de test de kill switch |
| AI-15 | Audit des prompts | AI Governance | Traçabilité prompts | Aucun | — | Non couvert | Pas de test d'audit prompts |

---

## 7. CROSS-CUTTING PROPERTIES (from 20_TESTING_AND_ACCEPTANCE_STANDARD)

| Req ID | Exigence | Test | Preuve | Statut | Écart |
|--------|----------|------|--------|--------|-------|
| CCP-01 | Fait confirmé jamais redemandé | `test_behavioral.py:TestConfirmedFactNeverReAsked` | Confirmed facts skipped in qualification | Conforme | — |
| CCP-02 | Ambiguïté jamais validée arbitrairement | `test_behavioral.py:TestAmbiguityNeverAutoResolved` | AMBIGUOUS → AWAITING_CLARIFICATION | Conforme | — |
| CCP-03 | Dossier jamais repris sans choix | `test_behavioral.py:TestSimpleOkDoesNotSelectProject`, `test_project_selector.py` | Project selection explicite | Conforme | — |
| CCP-04 | Opération jamais supposée sans preuve | `test_behavioral.py:TestAnnouncedActionIsActuallyExecuted` | Action vérifiée après exécution | Conforme | — |
| CCP-05 | Matching jamais produit avec critères insuffisants | MTC-03 | Readiness check | Conforme | — |
| CCP-06 | Relation jamais créée sans consentement | REL-01 | Consent flow | Conforme | — |
| CCP-07 | Donnée privée jamais partagée prématurément | PRV-05 | Coordinates not in extraction | Conforme | — |
| CCP-08 | Action annoncée réellement exécutée | `test_behavioral.py:TestAnnouncedActionIsActuallyExecuted` | Search readiness verification | Conforme | — |
| CCP-09 | Changement de canal ne perd aucun état | CHN-08 | Cross-channel preservation | Conforme | — |
| CCP-10 | Panne IA ne détruit pas le parcours | AI-07 | Deterministic fallback works | Conforme | — |

---

## Résumé

| Domaine | Conforme | Partiel | Non couvert | Total |
|---------|----------|---------|-------------|-------|
| Search | 1 | 2 | 4 | 7 |
| Matching | 4 | 0 | 3 | 7 |
| Relationship | 3 | 1 | 3 | 7 |
| Privacy | 2 | 0 | 5 | 7 |
| Omnichannel | 2 | 0 | 7 | 9 |
| AI Governance | 2 | 0 | 13 | 15 |
| Cross-Cutting | 10 | 0 | 0 | 10 |
| **Total** | **24** | **3** | **35** | **62** |

**Taux de couverture canonique:** 24/62 (39%) conformes, 3/62 (5%) partiels, 35/62 (56%) non couverts.

**Recommandations immédiates:**
1. Créer des tests dédiés Search (zéro résultat, explication, élargissement, alertes)
2. Créer des tests Matching (score explicable, classement, raisons principales)
3. Créer des tests d'isolation des canaux (aucune logique métier dans adaptateurs)
4. Créer des tests AI Governance (interchangeabilité, validation, circuit breaker)
5. Créer des tests Privacy (révocation, minimisation, structure consentement)
6. Créer des tests Relationship (double consentement, fiche partageable, audit)
