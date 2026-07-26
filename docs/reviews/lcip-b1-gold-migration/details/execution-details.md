# Execution Details — LCIP B.1

## Migration

```bash
$ python tests/gold_corpus/import/migrate_gold_corpus.py

Migration complete in 6.18s
  Total: 990
  Certified: 990
  Repairable: 0
  Rejected: 0
  Import Errors: 0
```

## Certification batch

```bash
$ python tests/gold_corpus/import/batch_certify.py

Batch certification complete in 1.4s
  Total: 990
  Certified: 990
  Mean global score: 1.0000
```

## Reporting check

```bash
$ python tools/reporting/check_reporting_policy.py docs/reviews/lcip-b1-gold-migration/

REPORTING_POLICY_PASS
```

## Contrôle

EXEC-0001 : PASS
