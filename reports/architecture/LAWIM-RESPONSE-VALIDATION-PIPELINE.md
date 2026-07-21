# LAWIM — Response Validation Pipeline

- Author: LAWIM AI
- Date: 2026-07-21
- Status: IMPLEMENTED
- Chantier: 4 — Controlled Generation

## 1. Pipeline Overview

```
Provider Response (raw text)
  → StructuralValidator
    → BusinessValidator
      → ConversationValidator
        → RepairHandler (if any validation fails)
          → ResponseQualityEvaluator
            → Validated Response
```

## 2. Component Details

### StructuralValidator

**File:** `validation/structural.py:18-102`

Validates structural integrity of the provider response.

| Check | Method | Description |
|-------|--------|-------------|
| Valid JSON | `_check_valid_json()` | Parse as JSON, must be a dict |
| Required fields | `_check_required_fields()` | Must have: content, dialogue_act, language |
| Field types | `_check_types()` | content: str, dialogue_act: str, language: str, question_count: int |
| Non-empty content | `_check_non_empty()` | content must have non-whitespace characters |
| Language support | `_check_language()` | Must be fr, en, or pcm |
| Dialogue act validity | `_check_dialogue_act()` | Must be one of 12 canonical acts |
| Question count | `_check_question_count()` | question_count ≤ maximum_questions |
| Max size | `_check_max_size()` | content length ≤ maximum_length |

**Supported languages:** fr, en, pcm

**Valid dialogue acts:**
- WELCOME, HANDOVER, REPHRASE_LAST_QUESTION, ACKNOWLEDGE_AND_ASK
- CONFIRM_CORRECTION_AND_ASK, CLARIFY_CURRENT_SLOT
- SEARCH_READY, PUBLICATION_READY, VISIT_READY, TRANSACTION_READY
- SUMMARIZE_AND_CONFIRM, CONTROLLED_ERROR

### BusinessValidator

**File:** `validation/business.py:6-103`

Validates that the response respects business decisions.

| Check | Method | Description |
|-------|--------|-------------|
| Question conformity | `_check_question_conforms()` | Response must address the planned next question |
| Single question | `_check_single_question()` | At most 1 question mark in content |
| No re-asked known | `_check_no_reasked_known()` | Must not ask for already-known facts |
| No invented values | `_check_no_invented_values()` | Must not invent property criteria |
| No intent change | `_check_no_intent_change()` | Must not deviate from current business intent |

### ConversationValidator

**File:** `validation/conversation.py:6-52`

Validates against conversation policies and forbidden content.

| Category | Patterns | Reason |
|----------|----------|--------|
| neutral_assistant | "assistant neutre", "neutral assistant", "i cannot make business decisions", "je ne peux pas prendre de décisions commerciales", "provide more context for your request" | LAWIM is an operational platform, not a neutral assistant |
| external_referral | "jumia", "seloger", "leboncoin", "facebook", "lamudi" | LAWIM handles requests internally |
| translation | "french for", "in english", "français signifie", "in french" | Language changes only on user request |
| grammar | "correct spelling is", "the correct phrasing", "you wrote", "vous avez écrit", "l'orthographe correcte", "la bonne orthographe" | No unsolicited grammar correction |

### RepairHandler

**File:** `validation/repair.py:12-127`

Attempts a **single** repair of an invalid response.

| Repair | Condition | Action |
|--------|-----------|--------|
| Structural repair | Non-JSON response | Extract text content, wrap in valid JSON with ACKNOWLEDGE_AND_ASK act |
| Conversation repair | Forbidden content found | Strip sentences containing forbidden patterns |
| Business repair | Business validation fails | Returns None (cannot repair) |
| Repair success | Content passes all validators after repair | Returns repaired JSON string |
| Repair failure | Content still invalid after repair | Returns None (→ internal fallback) |

**Repair flow:**

```
Invalid response
  → StructuralValidator fails
    → RepairHandler._repair_structural()
      → Extract content from non-JSON text
        → Build valid JSON: {content, dialogue_act, language, question_count}
          → ConversationValidator
            → Forbidden content found
              → RepairHandler._strip_forbidden_content()
                → Remove sentences with forbidden patterns
                  → BusinessValidator
                    → Fails → return None (cannot repair)
                    → Passes → return repaired JSON
```

**Important:** Only one repair attempt is made. If it fails, the response is discarded and the next provider in the chain is tried (or internal fallback is used).

### ResponseQualityEvaluator

**File:** `validation/quality.py:7-126`

Evaluates response quality on a continuous scale (0.0 - 1.0).

| Criterion | Weight | Scoring Method |
|-----------|--------|----------------|
| accuracy | 0.25 | Base score (1.0 if non-empty) |
| relevance | 0.15 | Base score (1.0 if non-empty) |
| conciseness | 0.15 | Word count: ≤30=1.0, ≤60=0.7, ≤100=0.4, >100=0.2 |
| clarity | 0.10 | Average sentence length: ≤15=1.0, ≤25=0.7, ≤40=0.4, >40=0.2 |
| naturalness | 0.10 | Fixed at 0.8 |
| professional_tone | 0.10 | Penalizes unprofessional words (lol, omg, wtf, etc.) |
| language_consistency | 0.10 | Fixed at 1.0 |
| no_jargon | 0.05 | Fixed at 0.9 |

**Acceptability threshold:** 0.6

Responses below 0.6 are flagged but not rejected (quality is informational — the pipeline already ensures structural, business, and conversation validity before quality evaluation).

## 3. Validation → Repair → Internal Fallback Flow

```
Provider returns response
  → StructuralValidator.validate()
    → FAIL: RepairHandler.repair()
      → SUCCESS: continue to quality
      → FAIL: discard → next provider in chain
    → PASS: continue
  → BusinessValidator.validate()
    → FAIL: RepairHandler.repair()
      → SUCCESS: continue to quality
      → FAIL: discard → next provider in chain
    → PASS: continue
  → ConversationValidator.validate()
    → FAIL: RepairHandler.repair()
      → SUCCESS: continue to quality
      → FAIL: discard → next provider in chain
    → PASS: continue
  → ResponseQualityEvaluator.evaluate()
    → Score ≥ 0.6: accept
    → Score < 0.6: accept (informational)
  → Return validated response
```

## 4. Observability Events

| Event | Trigger |
|-------|---------|
| generation_response_schema_invalid | StructuralValidator fails |
| generation_response_policy_invalid | BusinessValidator or ConversationValidator fails |
| generation_response_repair_started | RepairHandler begins repair |
| generation_response_repair_succeeded | Repair succeeds |
| generation_response_validated | All validation passes |
| generation_internal_fallback_used | All providers + repair fail |
| generation_response_delivered | Response sent to channel |

## 5. Metrics

| Metric | Type | Description |
|--------|------|-------------|
| generation_total | Counter | Total generation requests |
| generation_provider_success_total | Counter | Successful provider calls |
| generation_provider_failure_total | Counter | Failed provider calls |
| generation_provider_timeout_total | Counter | Provider timeouts |
| generation_schema_failure_total | Counter | Structural validation failures |
| generation_policy_failure_total | Counter | Business/conversation validation failures |
| generation_repair_total | Counter | Repair attempts |
| generation_repair_failure_total | Counter | Failed repair attempts |
| generation_internal_fallback_total | Counter | Internal fallback activations |
| generation_duplicate_delivery_total | Counter | Duplicate delivery attempts |
| generation_latency_seconds | Histogram | Response latency |
| generation_quality_score | Gauge | Response quality score |
