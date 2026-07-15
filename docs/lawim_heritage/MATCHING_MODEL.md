# MATCHING MODEL — Modèle de matching LAWIM

**Sources :** LAWIM documents `MATCHING_ENGINE_*.md` (7 documents), LAWIMA `03_ENGINE/property_matcher/` (3 versions), `06_AI_MODELS/matching_engine/property_matching_v1.json`, `08_CONFIG/rule_engine/RULE_ENGINE_V*.json`, LAWIM `Directive/04-MATCHING-REFERENCE.md`
**Principe :** Documentation exhaustive des règles de matching

---

## 1. Dimensions de matching

### 1.1 Dimensions principales (V1)

**Source :** LAWIMA `06_AI_MODELS/matching_engine/property_matching_v1.json`

| Dimension | Poids | Description |
|-----------|-------|-------------|
| city | 30% | Correspondance de ville |
| neighborhood | 25% | Correspondance de quartier |
| budget | 25% | Compatibilité budgétaire |
| property_type | 15% | Type de bien |
| title_status | 5% | Statut du titre foncier |

### 1.2 Dimensions additionnelles (V4/V5)

**Source :** LAWIMA `03_ENGINE/property_matcher/property_matcher_v5.py`

- **Location match** : +40 pts
- **Budget exact** : +50 pts
- **Budget ±10%** : +35 pts
- **Budget ±30%** : +20 pts
- **Budget ±50%** : +10 pts
- **Type match** : +10 à +25 pts

## 2. Tolérances budgétaires

**Source :** LAWIMA `06_AI_MODELS/matching_engine/property_matching_v1.json`

| Type de transaction | Tolérance |
|--------------------|-----------|
| Location (rent) | 20% d'écart |
| Achat (buy) | 15% d'écart |
| Investissement (invest) | 25% d'écart |

## 3. Règles de priorité et boosts

**Source :** LAWIMA `06_AI_MODELS/matching_engine/property_matching_v1.json`

| Condition | Bonus |
|-----------|-------|
| Correspondance exacte du quartier | +25 |
| Correspondance exacte de la ville | +20 |
| Budget dans la fourchette | +15 |
| Titre foncier présent | +10 |
| Investisseur diaspora | +20 |

## 4. Seuils et limites

**Source :** LAWIMA `06_AI_MODELS/matching_engine/property_matching_v1.json`

| Paramètre | Valeur |
|-----------|--------|
| Score minimum | 60/100 |
| Nombre maximum de résultats | 10 |

## 5. Système de notation par étoiles

**Source :** LAWIMA `03_ENGINE/property_matcher/property_matcher_v5.py`

| Score | Étoiles |
|-------|---------|
| ≥ 80 | 5/5 ⭐⭐⭐⭐⭐ |
| ≥ 60 | 4/5 ⭐⭐⭐⭐ |
| ≥ 40 | 3/5 ⭐⭐⭐ |
| ≥ 20 | 2/5 ⭐⭐ |
| < 20 | 1/5 ⭐ |

Affichage dans les résultats : `⭐ notes`

## 6. Algorithmes de matching (par version)

### 6.1 Matching V4 (Supabase)

**Source :** LAWIMA `03_ENGINE/property_matcher/property_matcher_supabase.py`

Correspondance par :
- Ville (requête Supabase)
- Budget (filtre par plage)
- Propriétés disponibles (status = 'available')

### 6.2 Matching V5 (Scoring)

**Source :** LAWIMA `03_ENGINE/property_matcher/property_matcher_v5.py`

Algorithme de scoring :
1. Vérification de la ville
2. Correspondance du budget avec tolérance
3. Correspondance du type de bien
4. Calcul du score total
5. Classement par score
6. Filtre (score ≥ seuil)
7. Limite (max 10 résultats)

## 7. Exclusions et incompatibilités

**Source :** LAWIM documents matching, LAWIMA données (non exhaustif)

Règles d'exclusion identifiées dans les sources :
- Propriétés archivées exclues (sauf statut 'available')
- Budget hors tolérance
- Ville différente (sauf si demande multi-ville)
- Propriétés déjà envoyées au même lead

## 8. Rematching

**Source :** LAWIM documents `MATCHING_ENGINE_PRISMA_GAP_REPORT.md`, `MATCHING_ENGINE_V1_IMPLEMENTATION_REPORT.md`

Concepts de rematching :
- Relance automatique J+7 avec nouveaux biens
- Mise à jour des préférences après feedback
- Historique des matchs déjà présentés

## 9. Documents matching engine (LAWIM)

Sept documents dédiés au matching engine dans LAWIM :

| Document | Contenu |
|----------|---------|
| `MATCHING_ENGINE_IMPLEMENTATION_ROADMAP.md` | Roadmap d'implémentation du matching engine |
| `MATCHING_ENGINE_PHASE0_ARCHITECTURE.md` | Architecture Phase 0 du matching engine |
| `MATCHING_ENGINE_PRISMA_GAP_REPORT.md` | Analyse des écarts entre design et schema Prisma |
| `MATCHING_ENGINE_V1_IMPLEMENTATION_REPORT.md` | Rapport d'implémentation V1 |
| `MATCHING_ENGINE_V1_IMPLEMENTATION_SCOPE.md` | Périmètre de l'implémentation V1 |
| `MATCHING_ENGINE_V1_SUMMARY.md` | Résumé du matching engine V1 |
| `MATCHING_PRISMA_SPRINT1.diff` | Patch des changements Prisma Sprint 1 |

## 10. Request engine (documents associés)

Trois documents sur le request engine :

| Document | Contenu |
|----------|---------|
| `REQUEST_ENGINE_FINAL_IMPLEMENTATION_PLAN.md` | Plan final d'implémentation |
| `REQUEST_ENGINE_IMPLEMENTATION_DECISIONS.md` | Décisions architecturales |
| `REQUEST_ENGINE_VALIDATION_REPORT.md` | Rapport de validation |

## 11. Scoring géographique dans le matching

**Source :** LAWIMA `02_KNOWLEDGE` (données de scoring), `property_matching_v1.json`

- **City match** : 30% du score
- **Neighborhood match** : 25% du score
- La matrice d'affinité des villes (LAWIM KNOWLEDGE/city-affinity-matrix.md) influence potentiellement le scoring

---

*Document patrimonial — Aucune décision de reconstruction n'est prise ici.*
