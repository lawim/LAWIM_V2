# B000002 — Runtime Certification Summary

**Classification:** RUNTIME_BEHAVIOR_ERROR
**Runtime called:** True
**Adapter:** lawim_v2.conversation.program_f_adapter.ProgramFEngineAdapter
**Orchestrator:** lawim_runtime.conversation.journey.ConversationJourneyOrchestrator
**Duration:** 29.9ms
**User turns:** 6
**Assertions:** 1P / 4F

## Violations
- B000002-MEM-001: expected=['transaction_type', 'property_type', 'city', 'budget', 'bedrooms', 'preferred_areas', 'move_in_date'], actual=['property_type', 'transaction_type', 'city', 'budget_max', 'bedrooms', 'district', 'preferred_areas', 'move_in_date']
- B000002-BIZ-001: expected=create_search_request, actual=CONFIRM_BUSINESS_CREATION
- B000002-Q-001: expected=1, actual=None
- B000002-OBJ-001: expected=1, actual=None