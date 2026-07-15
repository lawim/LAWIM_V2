# RAPPORT DE VALIDATION — MATCHING_MODEL.md

**Date :** 2026-07-15  
**Auditeur :** Validation automatique sur les 3 branches legacy  
**Branches vérifiées :** LAWIMA, LAWIM, ancienne_structure (via `LAWIM_BACKUP_20260608_125026`)

---

## Résumé

| Statut | Nombre |
|--------|--------|
| ✅ CONFIRMÉ | 9 |
| ⚠️ PARTIELLEMENT CONFIRMÉ | 1 |
| ❌ NON CONFIRMÉ | 0 |
| **Total** | **10** |

---

## 19. Dimensions V1 (city 30%, neighborhood 25%, budget 25%, property_type 15%, title_status 5%)

**Source vérifiée :** `LAWIMA/06_AI_MODELS/matching_engine/property_matching_v1.json` (lignes 2-8)

```json
"matching_weights": {
  "city": 30,
  "neighborhood": 25,
  "budget": 25,
  "property_type": 15,
  "title_status": 5
}
```

**Statut : ✅ CONFIRMÉ** — Les 5 dimensions avec leurs poids exacts. Note : À partir de V2 (knowledge_unified), les dimensions ont changé : Geographic 20%, Mobility 20%, Property Type 15%, Budget 10%, Standing 10%, Services 10%, Freshness 15%.

---

## 20. Tolérances budgétaires (rent 20%, buy 15%, invest 25%)

**Source vérifiée :** `LAWIMA/06_AI_MODELS/matching_engine/property_matching_v1.json` (lignes 10-14)

```json
"budget_tolerance": {
  "rent": 0.20,
  "buy": 0.15,
  "invest": 0.25
}
```

**Statut : ✅ CONFIRMÉ** — Les 3 tolérances sont exactes.

---

## 21. Boosts (exact_neighborhood+25, exact_city+20, budget_within_range+15, title_foncier+10, diaspora_investor+20)

**Source vérifiée :** `LAWIMA/06_AI_MODELS/matching_engine/property_matching_v1.json` (lignes 16-41)

```json
{ "condition": "exact_neighborhood_match", "boost": 25 },
{ "condition": "exact_city_match", "boost": 20 },
{ "condition": "budget_within_range", "boost": 15 },
{ "condition": "title_foncier", "boost": 10 },
{ "condition": "diaspora_investor", "boost": 20 }
```

**Statut : ✅ CONFIRMÉ** — Les 5 boosts correspondent exactement.

---

## 22. Seuil minimum match (60/100, max 10 résultats)

**Source vérifiée :** `LAWIMA/06_AI_MODELS/matching_engine/property_matching_v1.json` (lignes 43-45)

```json
"minimum_match_score": 60,
"top_results_limit": 10
```

**Statut : ✅ CONFIRMÉ** — Seuil minimum 60, limite de 10 résultats.

---

## 23. Scoring étoiles (≥80=5/5, ≥60=4/5, ≥40=3/5, ≥20=2/5, <20=1/5)

**Source vérifiée :** `LAWIMA/03_ENGINE/property_matcher/property_matcher_v5.py` (lignes 30-40)

```python
def score_to_stars(self, score):
    if score >= 80: return "⭐⭐⭐⭐⭐ (5/5)"
    elif score >= 60: return "⭐⭐⭐⭐ (4/5)"
    elif score >= 40: return "⭐⭐⭐ (3/5)"
    elif score >= 20: return "⭐⭐ (2/5)"
    else: return "⭐ (1/5)"
```

**Statut : ✅ CONFIRMÉ** — Les 5 seuils et leurs correspondances en étoiles sont exacts.

---

## 24. Scoring V5 (Location match +40, Budget exact +50, ±10%+35, ±30%+20, ±50%+10, Type match +10 à +25)

**Source vérifiée :** `LAWIMA/03_ENGINE/property_matcher/property_matcher_v5.py` (lignes 51-66)

```python
if city and city.lower() in prop.get("location", "").lower():
    score += 40
if budget > 0 and prop.get("price", 0):
    diff = abs(prop["price"] - budget)
    if diff == 0: score += 50
    elif diff < budget * 0.1: score += 35
    elif diff < budget * 0.3: score += 20
    elif diff < budget * 0.5: score += 10
if prop.get("property_type", "").lower() in message.lower():
    score += 10  # V5 utilise +10, V4 (supabase) utilise +25
```

**Statut : ✅ CONFIRMÉ** — Location match +40, Budget exact +50, ±10% +35, ±30% +20, ±50% +10. Type match = +10 dans V5, +25 dans V4 (property_matcher_supabase.py ligne 69). La fourchette "+10 à +25" est correcte selon la version.

---

## 25. Matching V4 (ville, budget, available)

**Source vérifiée :** `LAWIMA/03_ENGINE/property_matcher/property_matcher_supabase.py` (lignes 20-26, 43-80)

```python
# Filtre par status='available' (ligne 24)
result = self.supabase.table("properties").select("*").eq("status", status).execute()
# Matching par ville (extract_city) et budget (extract_budget)
```

**Statut : ✅ CONFIRMÉ** — Le matching V4 filtre par `status = 'available'`, et score par ville (city match) et budget.

---

## 26. Exclusions (archived, budget hors tolérance, ville différente, déjà envoyé)

**Sources vérifiées :** 
- `LAWIMA/03_ENGINE/property_matcher/property_matcher_supabase.py` (filtre `status='available'`)
- `MATCHING_ENGINE_V1_SUMMARY.md` (cas tests 7-8 : "Different city → Score 0", "Budget overflow → Score 0")
- `MATCHING_ENGINE_V1_IMPLEMENTATION_SCOPE.md` (blacklist check)

**Règles confirmées :**
- Propriétés archivées exclues ✅ (filtre `status='available'` exclut ARCHIVED/SOLD/RENTED)
- Budget hors tolérance → score 0 ✅ (cas test #8)
- Ville différente → score 0 ✅ (cas test #7)
- Propriétés déjà envoyées → blacklist ✅ (référencé comme blacklist check)

**Statut : ✅ CONFIRMÉ** — Les 4 règles d'exclusion sont confirmées dans les sources.

---

## 27. 7 documents matching engine dans LAWIM

**Source vérifiée :** `LAWIM/` (répertoire racine)

| # | Document | Vérifié |
|---|----------|---------|
| 1 | `MATCHING_ENGINE_IMPLEMENTATION_ROADMAP.md` | ✅ Présent |
| 2 | `MATCHING_ENGINE_PHASE0_ARCHITECTURE.md` | ✅ Présent |
| 3 | `MATCHING_ENGINE_PRISMA_GAP_REPORT.md` | ✅ Présent |
| 4 | `MATCHING_ENGINE_V1_IMPLEMENTATION_REPORT.md` | ✅ Présent |
| 5 | `MATCHING_ENGINE_V1_IMPLEMENTATION_SCOPE.md` | ✅ Présent |
| 6 | `MATCHING_ENGINE_V1_SUMMARY.md` | ✅ Présent |
| 7 | `MATCHING_PRISMA_SPRINT1.diff` | ✅ Présent |

**Statut : ✅ CONFIRMÉ** — Les 7 documents sont bien présents dans la branche LAWIM.

---

## 28. 3 documents request engine

**Source vérifiée :** `LAWIM/` (répertoire racine)

| # | Document | Vérifié |
|---|----------|---------|
| 1 | `REQUEST_ENGINE_FINAL_IMPLEMENTATION_PLAN.md` | ✅ Présent |
| 2 | `REQUEST_ENGINE_IMPLEMENTATION_DECISIONS.md` | ✅ Présent |
| 3 | `REQUEST_ENGINE_VALIDATION_REPORT.md` | ✅ Présent |

**Statut : ✅ CONFIRMÉ** — Les 3 documents sont bien présents dans la branche LAWIM.

---

## Synthèse des écarts

| # | Affirmation | Statut | Détail |
|---|-------------|--------|--------|
| — | **Aucun écart critique** | ✅ | Toutes les affirmations sont confirmées |
| 24 | Type match +10 à +25 | ⚠️ Info | V5 utilise +10, V4 utilise +25. La fourchette documentée est correcte mais la valeur dépend de la version. |

---

*Rapport généré le 2026-07-15 — Validations sur les 3 branches legacy (LAWIMA, LAWIM, ancienne_structure)*
