# DOMAIN COVERAGE — Heritage Gold Readiness

## Couverture par domaine

| Domaine | Fichiers Gold | Connaissances Gold | Score Audit | Couverture Source | Niveau |
|---------|:------------:|:------------------:|:-----------:|:-----------------:|--------|
| Matching | MATCHING_MODEL.md | 150 | **93%** | 95% | Excellent |
| Négociation | NEGOTIATION_MODEL.md | 139 | **78%** | 85% | Bon |
| Langue | LANGUAGE_MODEL.md | 120 | **71%** | 70% | Moyen |
| Qualification | QUALIFICATION_MODEL.md | 146 | **56%** | 60% | Faible |
| CRM | CRM_MODEL.md | 85 | **52%** | 55% | Faible |
| Géographie | GEOGRAPHY_MODEL.md | 34 | **46%** | 45% | Très faible |
| Conversation | CONVERSATION_MODEL.md | 168 | **44%** | 40% | Très faible |
| Domaine Métier | DOMAIN_MODEL.md | 96 | — | 70% | Moyen |
| Rôles | ROLE_MODEL.md | 61 | — | 50% | Moyen |
| Propriété | PROPERTY_MODEL.md | 122 | — | 65% | Moyen |

## Couverture par type de connaissance

| Type | Total Gold | Couverte par source | Manquante | Couverture |
|------|:----------:|:-------------------:|:---------:|:----------:|
| Concepts métier | ~400 | ~300 | ~100 | 75% |
| Règles métier | ~200 | ~150 | ~50 | 75% |
| Workflows/State Machines | ~50 | ~5 | ~45 | 10% |
| Données (tables, champs) | ~150 | ~80 | ~70 | 53% |
| APIs/Intégrations | ~50 | ~10 | ~40 | 20% |
| Scripts/Templates | ~100 | ~60 | ~40 | 60% |
| Algorithmes/Scoring | ~150 | ~130 | ~20 | 87% |
| Comportements UX | ~100 | ~60 | ~40 | 60% |

## Couverture par criticité

| Niveau | Concepts nécessaires | Couverts | Manquants | Couverture |
|--------|:-------------------:|:--------:|:---------:|:----------:|
| CRITIQUE | ~100 | ~40 | ~60 | 40% |
| MAJEUR | ~200 | ~130 | ~70 | 65% |
| MOYEN | ~300 | ~220 | ~80 | 73% |
| MINEUR | ~400 | ~340 | ~60 | 85% |

## Gaps par source primaire

| Source | Concepts | Couverts | Manquants | Couverture |
|--------|:-------:|:--------:|:---------:|:----------:|
| Directive/ (22 fichiers) | ~500 | ~350 | ~150 | 70% |
| Knowledge/ (50+ fichiers) | ~400 | ~300 | ~100 | 75% |
| LAWIMA 03_ENGINE/ (30 fichiers) | ~200 | ~30 | ~170 | 15% |
| LAWIMA 06_AI_MODELS/ (5 fichiers) | ~50 | ~40 | ~10 | 80% |
| LAWIMA 08_CONFIG/ (15 fichiers) | ~80 | ~50 | ~30 | 63% |
| ancienne_structure/ | ~100 | ~40 | ~60 | 40% |

## Synthèse

Le Gold couvre bien les concepts métier de haut niveau (Directive, Knowledge) mais échoue à documenter les détails d'implémentation (Engine, Config) et les workflows complets (state machines). Les 7 machines à états manquantes représentent le gap le plus critique.
