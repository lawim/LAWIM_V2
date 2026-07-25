# Audit independant — Programme G.5

**HEAD audite :** 875c47bc  
**HEAD courant :** e2891e08  
**Branche :** feature/program-g5d-regression-recovery-20260724  
**Date :** 2026-07-25T12:30:00Z  
**Worktree :** CLEAN  

## 1. Resume executif

| Domaine | Verdict | Preuve |
|---|---|---|
| Architecture | PARTIAL | Adapter pattern OK, barriere metier incomplete |
| Conversation | PARTIAL | pending_user_action OK, 10 LANGUAGE_DRIFT |
| Parcours utilisateur | PARTIAL | 20/30 PASS, 10 echecs linguistiques |
| Machine d'etat | PASS | 6 etats, 8 transitions, ordre temporel |
| Metier | PARTIAL | 24/24 business, pas de barriere auto dans validate() |
| Langues | PARTIAL | FR/EN OK, PCM vers EN 10 derives |
| Extraction | PASS | Negation OK, millions OK, tri longueur OK, studio OK |
| Runtime | PARTIAL | ProgramFEngineAdapter OK, fallback V2 possible |
| Persistance | PARTIAL | SQLite OK, PostgreSQL code present mais non teste |
| PostgreSQL | FAIL | Code present, AUCUN test reel |
| SQLite | PASS | SQLiteJourneyRepository operationnel |
| Tests | PASS | 118+856=0, pas de test PostgreSQL reel |
| Gold corpus | PARTIAL | 30 scenarios, manque clarification, restart, switch langue |
| Securite | PASS | SAFETY_INTENTS hierarchie OK, hacking/fraud detectes |
| Robustesse | PARTIAL | Restart non teste, messages simultanes non testes |

## 2. Verification critique : barriere metier

**Probleme :** Le validateur `g5_validate_corpus.py` calcule `biz_unexpected` mais ne retourne PAS d'erreur si la valeur est > 0.

```python
# Lignes 287-295 du validateur
print(f"Business: {biz_created_total} created / {biz_expected} expected")
if passes['PASS'] < 16:
    print("REGRESSION: PASS count below baseline 16")
    return 1
# MANQUANT: if biz_created_total != biz_expected: return 1
```

**Impact :** Une regression metier pourrait passer inapercue si le nombre de PASS reste >= 16.

## 3. Verification du consentement

**Mecanisme actuel (journey.py lignes 551-607) :**

1. `pending_before = state.pending_user_action` (ligne 551)
2. ResponsePlan construit (ligne 557-558)
3. `pending_after` determine par ResponsePlan (lignes 563-585)
4. Creation si `pending_before == CONFIRM_BUSINESS_CREATION` (ligne 588-590)

**Risque identifie :** La condition `is_confirmation = any(kw in lower for kw in CONFIRMATION_KEYWORDS)` (ligne 589) verifie des mots-cles sans contexte. Un message comme "Oui, Melen" pourrait declencher une creation si `pending_before == CONFIRM_BUSINESS_CREATION`. Risque FAIBLE car les gardes supplementaires sont presentes.

## 4. Verification de la negation

**Statut : PASS**  

```python
# entity/__init__.py lignes 82-90
sorted_tt = sorted(TRANSACTION_TYPES.items(), key=lambda x: -len(x[0]))
for fr, en in sorted_tt:
    if fr in lower:
        neg = re.search(r"(?:don't|dont|not|no be|i no)...", text, re.I)
        if neg:
            continue
        result.entities["transaction_type"] = en
        break
```

Tests :
- "I don't want to rent, I want to buy." → buy OK
- "Not for rent, I want to purchase." → buy OK
- "I want to buy a house." → buy OK
- "Je veux louer une maison." → rent OK

**Limite :** La negation n'est implementee que pour `transaction_type`. `property_type`, `bedrooms`, `budget` n'ont pas de gestion de negation.

## 5. Verification du gold corpus

| Type | FR | EN | PCM | Total |
|---|---|---|---|---|
| Location | 4 | 3 | 3 | 10 |
| Achat | 2 | 3 | 2 | 7 |
| Terrain | 1 | 1 | 1 | 3 |
| Studio | 1 | 1 | 0 | 2 |
| Visite | 1 | 0 | 0 | 1 |
| Correction | 2 | 1 | 1 | 4 |
| Negation | 1 | 1 | 1 | 3 |
| Court | 1 | 1 | 1 | 3 |
| Mixte | 1 | 1 | 0 | 2 |
| Switch langue | 0 | 1 | 0 | 1 |

**Scenarios manquants :**
1. Clarification (WAITING_FOR_CLARIFICATION)
2. Redemarrage au milieu du parcours
3. Annulation ("Je ne suis plus interesse")
4. Support ("Je n'arrive pas a me connecter")
5. Paiement / frais de visite
6. Changement de ville en cours de conversation
7. Messages dupliques (idempotence)

## 6. Verification linguistique

| Langue | Scenarios | Drift | Taux |
|---|---|---|---|
| FR | 10 | 1 | 10% |
| EN | 10 | 0 | 0% |
| PCM | 8 | 7 | 88% |
| Mixed | 2 | 2 | 100% |

**Cause :** Les templates PCM dans `_LANG_MSGS` (journey.py) utilisent un anglais simplifie que `_detect_language()` classifie comme EN. Par exemple : "I don get this information before" contient "get", "this", "information", "before" qui sont des mots anglais.

**Solution proposee :** Ne pas detecter la langue sur les reponses generees par le systeme. La decision linguistique devrait uniquement se baser sur les messages utilisateur.

## 7. Tests manquants critiques

| Test | Present | Priorite |
|---|---|---|
| PostgreSQL read-after-write | NON | CRITIQUE |
| Barriere metier automatisee | NON (incomplete) | CRITIQUE |
| Restart avec langue persistee | NON | IMPORTANT |
| Idempotence message_id | NON | IMPORTANT |
| Concurrence (2 users simultanes) | NON | MOYEN |
| Changement ville en conversation | NON | MOYEN |
| Annulation parcours | NON | MOYEN |

## 8. Dette technique

| ID | Description | Priorite |
|---|---|---|
| TECH-001 | Barriere metier incomplete dans validate() | CRITIQUE |
| TECH-002 | Aucun test PostgreSQL reel | CRITIQUE |
| TECH-003 | 10 derives PCM dans templates | IMPORTANT |
| TECH-004 | Gold corpus lacunaire | IMPORTANT |
| TECH-005 | Pas de test d'idempotence message_id | MOYEN |
| TECH-006 | Detections de negation partielle (tx only) | MOYEN |
| TECH-007 | Fallback V2 sans alerte explicite | MOYEN |

## 9. Verdicts finaux

| Verdict | Statut | Justification |
|---|---|---|
| Architecture | PARTIAL | Barriere metier incomplete, mais bonne separation |
| Machine d'etat | PASS | 6 etats, 8 transitions, ordre temporel OK |
| pending_user_action | PASS | pending_before/pending_after OK |
| Extraction entites | PASS | Negation, millions, tri, studio OK |
| Validation metier | PARTIAL | 24/24 business OK, barriere non automatisee |
| Langues | PARTIAL | FR/EN OK, PCM 88% derives |
| Gold corpus | PARTIAL | 30 sc. OK mais lacunes |
| Tests | PASS | 118+856=0, mais pas de test PG |
| PostgreSQL | FAIL | Code present, aucun test reel |
| Robustesse | PARTIAL | Restart non teste |
| G.5 | PARTIAL | BUSINESS VALIDATION PASS, LANGUE PARTIAL |
| G.6 | NOT AUTHORIZED | PostgreSQL non valide, derives PCM, barriere incomplete |

## 10. Priorites de correction

1. **CRITIQUE :** Ajouter `if biz_created_total != biz_expected: return 1` dans validate()
2. **CRITIQUE :** Creer test PostgreSQL isole avec read-after-write
3. **IMPORTANT :** Corriger templates PCM (ajouter marqueurs PCM dans les reponses)
4. **IMPORTANT :** Completer gold corpus (clarification, restart, annulation)
5. **MOYEN :** Ajouter tests d'idempotence message_id
6. **MOYEN :** Etendre negation a property_type et budget
