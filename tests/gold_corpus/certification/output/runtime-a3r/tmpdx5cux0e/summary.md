# A.3R Runtime Certification Summary

**Verdict:** RUNTIME_FAIL
**Runtime called:** True
**Adapter:** lawim_v2.conversation.program_f_adapter.ProgramFEngineAdapter
**Orchestrator:** lawim_runtime.conversation.journey.ConversationJourneyOrchestrator
**Call count:** 1
**Tautology check:** True
**Expected type:** CORPUS_FILE
**Actual type:** RUNTIME_EXECUTION

## Assertions
- Total: 3
- PASS: 0
- FAIL: 3

## Violations
- ASSERT-INTENT: op=eq, expected=visit_scheduling, actual=visit_request
- ASSERT-QUAL: op=eq, expected=qualified, actual=QUALIFYING
- ASSERT-ACTION: op=eq, expected=search, actual=CONFIRM_FIELD_VALUE