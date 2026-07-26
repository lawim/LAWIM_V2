# Execution Details — LCIP A.3

## Certification Orchestrator

```bash
$ python tests/gold_corpus/certification/engine/orchestrator.py \
    tests/gold_corpus/specification/tests/B000001/ \
    tests/gold_corpus/examples/B000001/ \
    --output-dir tests/gold_corpus/certification/output/

certification.json -> tests/gold_corpus/certification/output/certification.json
violations.json     -> tests/gold_corpus/certification/output/violations.json
diagnostics.json    -> tests/gold_corpus/certification/output/diagnostics.json
summary.md          -> tests/gold_corpus/certification/output/summary.md

Verdict: FAIL
Violations: 1
Components affected: 1
Scores: 0.8125
```

## Reporting Policy Check

```bash
$ python tools/reporting/check_reporting_policy.py docs/reviews/lcip-a3-certification-engine/

REPORTING_POLICY_PASS
```

## Contrôle

EXEC-0001 : PASS
