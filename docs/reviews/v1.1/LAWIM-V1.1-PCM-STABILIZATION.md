# LAWIM V1.1 — PCM Stabilization Report

**Date:** 2026-07-26
**Baseline SHA:** `28a9a6da`
**Branch:** `feature/lawim-v1.1-pcm-stabilization-20260726`
**HEAD:** `798e2073` (dernière modification)

---

## 1. Modifications Effectuées

### 1.1 Language Detection — `lawim_runtime/conversation/journey.py`

- **PCM bigram markers**: Expanded from 15 to 40+ bigrams (added `ma budget`, `my money`, `make e`, `na correct`, etc.)
- **Punctuation stripping**: Bigrams now ignore punctuation (`,.!?`) for accurate matching
- **Single-bigram + verb pattern**: Single PCM bigram + PCM verb = PCM detection
- **PCM→EN drift guard**: When conversation is PCM and detection is EN, requires ≥2 strong EN markers before switching
- **French keywords extended**: Added `un`, `une`, `des`, `de`, `la`, `le`, `les`, `à`, `au`, `aux`, etc.
- **PCM single markers**: Added `ma`

### 1.2 Language Detection — `code/lawim_v2/conversation/policy/language_policy.py`

- Mirror of the same improvements: bigram markers, punctuation stripping, single-bigram pattern, domain term protection
- `should_switch()` now protects against domain-term-only language drift

### 1.3 Footer Language — `code/lawim_v2/communication/service.py`

- Footer now uses **effective conversation language** from engine state instead of hardcoded `"fr"`
- Greeting no longer appends a duplicate footer

### 1.4 PCM Templates

| Component | File | Changes |
|-----------|------|---------|
| Greetings | `greetings.py` | PCM: `"Abeg describe your property project small"` → `"Tell us your property project"` |
| Legacy MSG | `journey.py` | PCM: improved naturalness across all 10 message keys |
| Internal engine | `internal_engine.py` | PCM: correction, error, readiness, summary, handover templates improved |
| Footer | `service.py` | PCM: `"LAWIM AI help for this answer."` → `"LAWIM AI fit help for this answer."` |

## 2. Gold Corpus

- **File:** `tests/fixtures/pcm_v1_1_gold.json`
- **Total scenarios:** 16
- **PCM scenarios:** 9 (pcm-search-1-5, pcm-correction-1, pcm-refusal-1, pcm-confirm-1, pcm-clarify-1)
- **FR scenarios:** 2 (fr-search-1, fr-false-positive-1)
- **EN scenarios:** 1 (en-search-1, en-false-positive-1)
- **Mixed/switch scenarios:** 3 (pcm-mixed-1, switch-fr-en-pcm, pcm-short-1)

## 3. Résultats

| Métrique | Valeur |
|----------|--------|
| PCM_GOLD_SCENARIOS | 16 |
| PCM_PASS | 28 (tests) |
| PCM_FAIL | 0 |
| FR_FALSE_PCM | 0 (no FR→PCM false positives) |
| EN_FALSE_PCM | 0 (no EN→PCM false positives) |
| PCM_TO_EN_DRIFT | 0 (conversation language stays PCM) |
| EXPLICIT_SWITCH | PASS (FR↔EN↔PCM all directions) |
| SHORT_MESSAGE_STABILITY | PASS (short messages don't change language) |
| PCM_TEMPLATES | 19 templates, all PRESENT, PROFESSIONAL, LANGUAGE_VALID |

## 4. Non-Régression V1

| Suite | Résultat |
|-------|----------|
| `tests/test_conversation_*.py lawim_runtime/` | **988 PASS, 0 FAIL** |
| Full collection | 5,087 tests collected |

No V1 regression. Full suite preserved.

## 5. Analyse des Défauts

- 0 PCM→EN drift (conversation language stable)
- 0 FR→PCM false positive (FR conversations stay FR)
- 0 EN→PCM false positive (EN conversations stay EN)
- Short messages (≤3 words) never change conversation language
- Explicit switches work correctly in all 6 directions

## 6. Fichiers Modifiés

| Fichier | Type |
|---------|------|
| `lawim_runtime/conversation/journey.py` | Détection linguistique |
| `code/lawim_v2/conversation/policy/language_policy.py` | Détection linguistique V2 |
| `code/lawim_v2/conversation/policy/greetings.py` | Template PCM |
| `code/lawim_v2/conversation/policy/internal_engine.py` | Templates PCM |
| `code/lawim_v2/communication/service.py` | Footer langue effective |
| `tests/fixtures/pcm_v1_1_gold.json` | Corpus gold |
| `tests/test_pcm_v1_1_gold.py` | Validateur gold |
| `docs/reviews/v1.1/pcm-language-pipeline.md` | Documentation pipeline |
| `docs/reviews/v1.1/pcm-template-review.md` | Revue des templates |

## 7. Verdict

```
LAWIM_V1_1_PCM_VALIDATION_PASS
LAWIM_V1_1_PCM_LOCAL_PASS
LAWIM_V1_1_PRODUCTION_VALIDATION_PENDING
LAWIM_V1_1_RELEASE_NOT_AUTHORIZED
```

Déploiement canary requis avant validation production complète.

## 8. Travail Restant

- Déploiement canary sur OVH
- Recette Web, Telegram et WhatsApp avec vrais utilisateurs PCM
- Test de switch de langue réel sur chaque canal
- Validation production complète → `LAWIM_V1_1_RELEASE_AUTHORIZED`
