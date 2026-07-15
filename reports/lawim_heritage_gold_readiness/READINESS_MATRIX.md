# READINESS MATRIX — Heritage Gold Readiness

## Matrice de préparation par domaine

| Domaine | Score | Couverture Gold | Couverture Source | Gaps | Conclusion |
|---------|:-----:|:--------------:|:-----------------:|:----:|------------|
| **Matching** | 93% | 95% | 95% | Mineurs (algorithme décisionnel, rematching) | PRÊT |
| **Négociation** | 78% | 85% | 82% | Sales scripts, diaspora comportements | PRESQUE PRÊT |
| **Langue** | 71% | 80% | 70% | Entity linking 50% fabriqué, templates simplifiés | MOYEN |
| **Qualification** | 56% | 60% | 55% | Pipeline 8 étapes non vérifiable, anti-fraude, agent network | INSUFFISANT |
| **CRM** | 52% | 55% | 40% | Rôles, permissions, lead routing aspirationnel | INSUFFISANT |
| **Géographie** | 46% | 45% | 35% | Voisinage, hiérarchie, GPS metadata, alias | INSUFFISANT |
| **Conversation** | 44% | 40% | 35% | Objections, escalade, behavioral tracking, channel rules | INSUFFISANT |

## Matrice de criticité

| Domaine | Score /100 | Priorité | Effort estimation |
|---------|:--------:|:--------:|:-----------------:|
| Conversation | 44 | 🔴 URGENT | 3-4 semaines |
| Géographie | 46 | 🔴 URGENT | 4-6 semaines |
| CRM | 52 | 🟡 MOYEN | 2-3 semaines |
| Qualification | 56 | 🟡 MOYEN | 2-3 semaines |
| Langue | 71 | 🟢 FAIBLE | 1 semaine |
| Négociation | 78 | 🟢 FAIBLE | 1 semaine |
| Matching | 93 | ✅ OK | 0 (prêt) |

## Matrice d'interdépendance

| Dépend de ↓ | Matching | Négociation | Langue | Qualification | CRM | Géographie | Conversation |
|-------------|:--------:|:-----------:|:------:|:-------------:|:---:|:----------:|:------------:|
| **Matching** | — | 🟢 | 🟢 | 🟢 | 🟡 | 🔴 | 🟢 |
| **Négociation** | 🟢 | — | 🟢 | 🟡 | 🟢 | 🟢 | 🔴 |
| **Langue** | 🟢 | 🟢 | — | 🟢 | 🟢 | 🟢 | 🔴 |
| **Qualification** | 🔴 | 🟢 | 🟢 | — | 🔴 | 🟡 | 🔴 |
| **CRM** | 🟡 | 🟢 | 🟢 | 🔴 | — | 🟢 | 🔴 |
| **Géographie** | 🔴 | 🟢 | 🟢 | 🟡 | 🟢 | — | 🟢 |
| **Conversation** | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | — |

Légende : 🔴 Dépendance forte / 🟡 Dépendance modérée / 🟢 Pas de dépendance

## Bloqueurs identifiés

1. Géographie → Matching : le matching dépend des données de proximité qui n'existent pas
2. Qualification → Matching : le scoring dépend des champs collectés par qualification
3. Conversation → Tous : la conversation est le point d'entrée de tout le système
4. Qualification → CRM : le pipeline CRM dépend de la qualification

## Recommandations

1. **Priorité 1** : Compléter les machines à états (Workflow Reference, 4749 lignes disponibles)
2. **Priorité 2** : Ajouter les données de proximité géographique (50+ heures)
3. **Priorité 3** : Documenter le NBA Engine concept central
4. **Priorité 4** : Ajouter les scripts commerciaux (8 scripts)
5. **Priorité 5** : Corriger l'entity linking (10 paires fabriquées à corriger)
