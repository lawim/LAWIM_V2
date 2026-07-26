# LAWIM — Canonical Conversation Specification

Ce dossier definit la spécification officielle d'une conversation LAWIM.

Il constitue le cadre de certification pour tout le moteur conversationnel.

## Architecture

```
specification/

    README.md                            ← ce fichier

    schema/
        canonical_state.schema.json      ← modèle d'état canonique
        turn_spec.schema.json            ← spécification par tour
        conversation_lifecycle.schema.json  ← cycle de vie et transitions
        certification_level.schema.json  ← niveaux de certification

    assertions/
        assertion_library.json           ← bibliothèque d'assertions standardisées
        __init__.py

    variants/
        variants_policy.json             ← mécanisme de variantes acceptées

    engine/
        certification_engine.py          ← moteur de certification
        __init__.py

    tests/
        turns_B000001.json               ← test : spécification par tour B000001

    levels.json                          ← niveaux de certification
```

## Modèle conversationnel

Le modèle canonique d'une conversation LAWIM est défini par quatre composants :

1. **État canonique** (`canonical_state.schema.json`) — l'état complet de la
   conversation à tout moment : phase, intention, qualification, mémoire,
   objet métier, langue, canal.

2. **Spécification par tour** (`turn_spec.schema.json`) — chaque tour décrit
   l'entrée utilisateur, les entités attendues, les faits extraits, les
   modifications de mémoire, les questions autorisées/interdites, la
   transition attendue et les assertions à vérifier.

3. **Cycle de vie** (`conversation_lifecycle.schema.json`) — les 7 phases
   possibles (initial → in_progress → qualified|unqualified →
   completed|handover|error) et les transitions autorisées entre elles.

4. **Niveaux de certification** (`certification_level.schema.json`) —
   BRONZE, SILVER, GOLD, PLATINUM avec scores minimums et assertions
   requises.

## Cycle de vie d'une conversation

```
initial
  ↓ (user message received)
in_progress
  ↓ (all criteria collected)    ↓ (criteria impossible)
qualified                      unqualified
  ↓                              ↓
  ├→ completed                   ├→ completed
  ├→ handover (if needed)         └→ handover
  └→ error                       └→ error
```

Transitions autorisées :

| From | To | Trigger |
|------|----|---------|
| initial | in_progress | user_message |
| in_progress | in_progress | criteria_collected_partial |
| in_progress | qualified | all_criteria_collected |
| in_progress | unqualified | criteria_conflict |
| qualified | completed | business_action_done |
| qualified | handover | requires_human |
| unqualified | completed | user_accepts |
| unqualified | handover | requires_human |
| any | error | system_error |

## Assertions

La bibliothèque d'assertions standardisées se trouve dans
`assertions/assertion_library.json`.

Catégories :

| Catégorie | Description | Nombre |
|-----------|-------------|--------|
| memory | Rétention et mise à jour de la mémoire | 7 |
| qualification | Statut et progression de la qualification | 3 |
| business | Actions et objets métier | 4 |
| intent | Détection de l'intention | 2 |
| language | Langue, identité, footer | 4 |
| questions | Questions posées par tour | 3 |
| runtime | Moteur, fallback | 2 |
| channel | Comportement canal | 1 |
| idempotence | Non-régression et idempotence | 2 |
| state | Transitions et état final | 3 |

Chaque assertion a un identifiant unique (ex: MEM-0001), une catégorie,
un opérateur de comparaison et une sévérité (error/warning).

## Variantes acceptées

Le mécanisme de variantes (`variants/variants_policy.json`) permet de
déclarer plusieurs formulations équivalentes pour une même entrée
utilisateur.

Types de variantes :
- **lexical** : synonymes (appartement/appt)
- **syntaxic** : reformulations (Je cherche / Je voudrais)
- **semantic** : sens équivalent (Je suis intéressé / Je veux visiter)
- **language_switch** : même intention dans une autre langue
- **partial_input** : entrée partielle avec mêmes entités

Règle de certification : une conversation est certifiée si elle satisfait
les assertions pour AU MOINS UNE formulation de chaque tour.

## Niveaux de certification

| Niveau | Score Global Min | Assertions Requises | Tolérance |
|--------|-----------------|---------------------|-----------|
| BRONZE | 0.50 | 7 | 2 échecs |
| SILVER | 0.70 | 15 | 1 échec |
| GOLD | 0.85 | 23 | 0 échec |
| PLATINUM | 0.95 | 31 | 0 échec |

Détails complets dans `levels.json`.

## Utilisation du moteur de certification

```bash
# Certifier une conversation par rapport à sa spécification
python tests/gold_corpus/specification/engine/certification_engine.py \
    tests/gold_corpus/specification/tests/ \
    tests/gold_corpus/examples/B000001/
```

Le moteur produit :
- verdict (PASS / FAIL / PARTIAL)
- scores par dimension
- assertions satisfaites et violées
- résultats par tour
- rapport JSON dans `reports/`
