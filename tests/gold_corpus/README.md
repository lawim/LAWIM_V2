# LAWIM Gold Corpus

Le Gold Corpus est la spécification officielle du moteur conversationnel LAWIM.

Aucune évolution du `ConversationJourneyOrchestrator` ne pourra être validée
sans passer le Gold Benchmark.

## Architecture

```
tests/gold_corpus/

    README.md                            ← ce fichier

    schema/                              ← schémas JSON de validation
        conversation.schema.json
        expected_state.schema.json
        expected_business.schema.json
        expected_questions.schema.json
        expected_language.schema.json
        expected_runtime.schema.json
        assertions.schema.json

    categories/                          ← dossiers par catégorie (pour organisation)
        purchase/
        rental/
        seller/
        ...

    conversations/                       ← conversations certifiées
        <id>/
            conversation.json
            expected_state.json
            expected_business.json
            expected_questions.json
            expected_language.json
            expected_runtime.json
            expected_assertions.json
            rationale.md

    validators/                          ← scripts de validation
        validate_schema.py
        validate_conversation.py
        validate_assertions.py
        validate_business.py

    benchmark/                           ← moteur de benchmark
        run_gold_benchmark.py
        score.py
        report.py

    statistics/                          ← générateur de statistiques
        build_statistics.py

    manifests/                           ← manifests du corpus
    reports/                             ← rapports de benchmark

    examples/                            ← exemples de conversations
        B000001/
```

## Conventions

### Identifiants

Chaque conversation reçoit un identifiant unique au format `A######` :

| Préfixe | Catégorie |
|---------|-----------|
| B | Basic (scénarios de base) |
| I | Intermediate |
| A | Advanced |
| E | Expert / Edge cases |
| M | Multilingual |
| R | Restart / Recovery |
| C | Correction |
| N | Negotiation |
| Q | Qualification |
| P | Purchase |
| L | Rental (location) |
| S | Seller (vente) |
| V | Visit |
| K | Marketplace |
| F | Followup |
| X | Idempotence |
| H | Investment |

### Catégories

| Catégorie | Description |
|-----------|-------------|
| purchase | Parcours d'achat |
| rental | Parcours de location |
| seller | Mise en vente |
| visit | Planification de visite |
| investment | Investissement immobilier |
| multilingual | Conversations multilingues |
| correction | Correction d'erreur utilisateur |
| restart | Redémarrage de conversation |
| idempotence | Test d'idempotence |
| negotiation | Négociation de prix |
| qualification | Qualification poussée |
| marketplace | Place de marché |
| followup | Suivi de dossier |
| edge_cases | Cas limites |

### Niveaux de difficulté

| Niveau | Description |
|--------|-------------|
| basic | Parcours simple, critères explicites |
| intermediate | Parcours avec quelques ambiguïtés |
| advanced | Parcours complexe, critères implicites |
| expert | Cas très complexes ou ambigus |

### Langues

| Code | Langue |
|------|--------|
| fr | Français |
| en | Anglais |
| pcm | Pidgin camerounais |

## Ajouter une conversation

1. Choisir un identifiant libre dans la séquence appropriée
2. Créer un dossier `conversations/<id>/`
3. Créer les 8 fichiers requis :
   - `conversation.json`
   - `expected_state.json`
   - `expected_business.json`
   - `expected_questions.json`
   - `expected_language.json`
   - `expected_runtime.json`
   - `expected_assertions.json`
   - `rationale.md`
4. Valider avec les validateurs
5. Vérifier que le benchmark passe avec les scores attendus

Niveaux de difficulté conseillés pour l'ajout :

- **basic** → 1-3 tours, critères explicites
- **intermediate** → 3-5 tours, une ambiguïté
- **advanced** → 5-8 tours, sous-entendus
- **expert** → 8+ tours, multiples corrections ou changements d'avis

## Validation

```bash
# Valider une conversation contre les schémas
python tests/gold_corpus/validators/validate_schema.py tests/gold_corpus/conversations/B000001/

# Valider l'intégrité structurelle
python tests/gold_corpus/validators/validate_conversation.py tests/gold_corpus/conversations/B000001/

# Valider les assertions
python tests/gold_corpus/validators/validate_assertions.py tests/gold_corpus/conversations/B000001/expected_assertions.json

# Valider le comportement métier
python tests/gold_corpus/validators/validate_business.py tests/gold_corpus/conversations/B000001/expected_business.json
```

## Benchmark

```bash
# Exécuter le benchmark complet
python tests/gold_corpus/benchmark/run_gold_benchmark.py

# Avec options avancées
python tests/gold_corpus/benchmark/run_gold_benchmark.py \
    --conversations-dir tests/gold_corpus/conversations/ \
    --output-dir tests/gold_corpus/reports/
```

Le benchmark produit :

- `reports/benchmark_results.json` — résultats bruts
- `reports/benchmark_report.md` — rapport formaté

## Scoring

Le scoring LAWIM attribue un score entre 0.0 et 1.0 pour chaque catégorie,
puis un score global pondéré.

### Catégories et poids

| Catégorie | Poids | Description |
|-----------|-------|-------------|
| Conversation | 0.15 | Conformité structurelle et schémas |
| Memory | 0.15 | Rétention des informations entre les tours |
| Qualification | 0.15 | Détection correcte du statut |
| Business | 0.15 | Action métier correcte |
| Runtime | 0.15 | Moteur et services corrects |
| Language | 0.10 | Langue et identité correctes |
| Channel | 0.05 | Comportement canal correct |
| Intent | 0.10 | Intention détectée correcte |

### Score global = moyenne pondérée

Un score global ≥ 0.50 est requis pour qu'une conversation soit considérée
comme réussie dans le benchmark.

## Statistiques

```bash
# Générer les statistiques du corpus
python tests/gold_corpus/statistics/build_statistics.py

# Avec export JSON
python tests/gold_corpus/statistics/build_statistics.py \
    --output tests/gold_corpus/manifests/statistics.json
```

## Règle absolue

Le Gold Corpus est la spécification officielle du moteur conversationnel.

Aucune évolution de `ConversationJourneyOrchestrator` ne sera validée sans
passer le Gold Benchmark.

Toute conversation ajoutée au corpus doit être validée par au moins un
réviseur indépendant.
