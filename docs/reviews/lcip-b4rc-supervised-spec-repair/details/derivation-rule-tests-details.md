# Derivation Rule Tests Details — LCIP B.4R-C

## Rules Tested (EXP-0001 to EXP-0020)

20 rules × 2 tests (1 positive + 1 negative) = 40 tests.

## Results

```
40 passed in 0.17s
```

## Per-Rule Results

| Rule | Positive | Negative | Status |
|------|----------|----------|--------|
| EXP-0001: transaction_type from first user turn | PASS | PASS | ACTIVE |
| EXP-0002: property_type from user dialogue | PASS | PASS | ACTIVE |
| EXP-0003: city is explicitly stated | PASS | PASS | ACTIVE |
| EXP-0004: budget extracted as integer | PASS | PASS | ACTIVE |
| EXP-0005: bedrooms explicitly stated | PASS | PASS | ACTIVE |
| EXP-0006: multiple preferred areas preserved as list | PASS | PASS | ACTIVE |
| EXP-0007: correction replaces only the targeted fact | PASS | PASS | ACTIVE |
| EXP-0008: uncorrected facts are preserved | PASS | PASS | ACTIVE |
| EXP-0009: final confirmation required before business action | PASS | PASS | ACTIVE |
| EXP-0010: refusal blocks business creation | PASS | PASS | ACTIVE |
| EXP-0011: explicit confirmation allows business creation | PASS | PASS | ACTIVE |
| EXP-0012: unique business object creation | PASS | PASS | ACTIVE |
| EXP-0013: pending_action set after assistant question | PASS | PASS | ACTIVE |
| EXP-0014: pending_action reset after business action | PASS | PASS | ACTIVE |
| EXP-0015: conversational language persists | PASS | PASS | ACTIVE |
| EXP-0016: short message does not change language | PASS | PASS | ACTIVE |
| EXP-0017: explicit language switch recognized | PASS | PASS | ACTIVE |
| EXP-0018: restart preserves confirmed facts | PASS | PASS | ACTIVE |
| EXP-0019: final replay is idempotent | PASS | PASS | ACTIVE |
| EXP-0020: recap based on current state | PASS | PASS | ACTIVE |

## Command

```bash
python3 -m pytest tests/gold_corpus/specification/tests/test_expected_derivation_rules.py -q -ra
```

## Test File

`tests/gold_corpus/specification/tests/test_expected_derivation_rules.py`

## Evidence

- JUnit XML: `evidence/raw/tests/b4rc-tests.xml`
- Normalized: `evidence/normalized/derivation-rule-tests.jsonl`
