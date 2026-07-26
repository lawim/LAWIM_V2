# B000089 — Runtime Certification Summary

**Classification:** RUNTIME_BEHAVIOR_ERROR
**Runtime called:** True
**Adapter:** lawim_v2.conversation.program_f_adapter.ProgramFEngineAdapter
**Orchestrator:** lawim_runtime.conversation.journey.ConversationJourneyOrchestrator
**Duration:** 53.0ms
**User turns:** 6
**Assertions:** 0P / 5F

## Violations
- B000089-MEM-001: expected=['transaction_type', 'property_type', 'city', 'budget', 'preferred_areas', 'move_in_date'], actual=['property_type', 'transaction_type', 'city', 'bedrooms', 'district']
- B000089-BIZ-001: expected=create_search_request, actual=NONE
- B000089-LANG-001: expected=en, actual=fr
- B000089-Q-001: expected=1, actual=None
- B000089-OBJ-001: expected=1, actual=None