# PCM Language Pipeline — LAWIM V1.1

**Date:** 2026-07-26
**Canonical SHA:** 28a9a6da
**Branch:** feature/lawim-v1.1-pcm-stabilization-20260726

---

## Pipeline Overview

```
User message
  → _detect_language(text)                    [journey.py:344]  — legacy runtime
  → LawimLanguagePolicy.detect_language(text)  [language_policy.py:28] — V2 policy
  → _response_lang(state, text)                [journey.py:389] — persistence + stability
  → _msg(state, key) / template selection       [journey.py:427]
  → Response generation                         [internal_engine.py]
  → _format_ai_footer(language, channel)        [service.py:717]
```

## Components

### 1. Legacy Detection: `_detect_language` in `lawim_runtime/conversation/journey.py:344`

| Aspect | Detail |
|--------|--------|
| File | `lawim_runtime/conversation/journey.py` |
| Signature | `def _detect_language(text: str) -> str` |
| Returns | `"fr"`, `"en"`, `"pcm"`, `"unknown"` |
| Phase 1 | Explicit switch patterns (full phrase match) |
| Phase 2 | PCM strong bigram markers (≥2 hits → pcm) |
| Phase 3 | Keyword scoring (fr_kw, en_kw, pcm_single) |

### 2. V2 Detection: `LawimLanguagePolicy` in `code/lawim_v2/conversation/policy/language_policy.py:28`

| Aspect | Detail |
|--------|--------|
| File | `code/lawim_v2/conversation/policy/language_policy.py` |
| Signature | `def detect_language(self, text: str) -> str \| None` |
| Returns | `"fr"`, `"en"`, `"pcm"`, `None` |
| Markers | Three sets: `_FRENCH_MARKERS`, `_ENGLISH_MARKERS`, `_PCM_MARKERS` |
| Switch guard | `should_switch()` — stability rules |

### 3. Language Persistence: `_response_lang` in `journey.py:389`

- Stores `state._conversation_lang`
- Default: `"fr"`
- First message: accepts detected language immediately
- Subsequent: requires ≥2 non-domain words + ≥10 chars
- Explicit switch patterns override immediately

### 4. Template Selection

| Source | File | Lines |
|--------|------|-------|
| Legacy MSG templates | `lawim_runtime/conversation/journey.py` | 994-1029 |
| Canonical greetings | `code/lawim_v2/conversation/policy/greetings.py` | 3-28 |
| Internal engine | `code/lawim_v2/conversation/policy/internal_engine.py` | 16-173 |
| Questions | `code/lawim_v2/conversation/qualification/question_catalog.py` | 1-529 |
| Footer | `code/lawim_v2/communication/service.py` | 714-718 |

## Language Policy (V1.1)

### Three values:
- `detected_language`: from message content only
- `conversation_language`: persistent across turns (stored in state)
- `effective_response_language`: used for templates + footer

### Stability Rules:
1. Messages ≤3 words never change conversation language
2. Real-estate domain terms alone never trigger switch
3. Explicit switch (e.g., "Speak English") takes effect immediately
4. PCM bigram markers ≥2 → strong PCM detection
5. English/French keyword scoring with PCM penalty

### PCM Strong Markers (bigrams):
`no be`, `wey dey`, `make i`, `i wan`, `i di`, `i dey`, `i don`, `i go`, `e dey`, `e don`, `na so`, `na which`, `how much`, `make we`, `i no`, `no vex`, `na rent`, `na buy`, `don register`

### PCM Single Markers:
`abeg`, `wetin`, `sabi`, `komot`, `broda`, `sista`, `pikin`, `una`, `wuna`, `dey`, `abi`, `kom`
