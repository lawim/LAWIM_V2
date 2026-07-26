# Execution Details — LCIP A.2

## Certification Engine — B000001

```bash
$ python tests/gold_corpus/specification/engine/certification_engine.py \
    tests/gold_corpus/specification/tests/B000001/ \
    tests/gold_corpus/examples/B000001/

Certification Verdict: FAIL
Assertions: 12 PASS, 1 FAIL
  FAIL: BIZ-0001 (business_object_created) — exists=False
  PASS: QST-0001 (one_question_per_turn)
  PASS: MEM-0001 (memory_retained)
  PASS: QLF-0001 (qualification_complete) — expected=qualified, actual=qualified
  PASS: BIZ-0002 (business_action_correct) — expected=search, actual=search
  PASS: STATE-0002 (final_state_correct) — expected=qualified, actual=qualified
  PASS: MEM-0003 (budget_modified) — expected=180000, actual=180000
  PASS: MEM-0002 (memory_updated)
  PASS: CHANNEL-0001 (channel_behavior_correct)
  PASS: STATE-0001 (phase_transition_correct) — expected=qualified, actual=qualified
  PASS: MEM-0004 (zone_preserved)
  PASS: STATE-0003 (slots_filled_correctly)
  PASS: INT-0001 (intent_correct) — expected=rental_search, actual=rental_search

Scores:
  business: 0.5000
  questions: 1.0000
  memory: 1.0000
  qualification: 1.0000
  state: 1.0000
  channel: 1.0000
  intent: 1.0000
  global: 0.8125
```

Note : BIZ-0001 échoue car l'exemple B000001 ne va pas jusqu'à la recherche
(qualification seulement). C'est un comportement correct du moteur.

## Gold Corpus Reporting Check

```bash
$ python tools/reporting/check_reporting_policy.py docs/reviews/lcip-a2-specification/

REPORTING_POLICY_PASS
```

## Contrôle

EXEC-0001 : PASS
