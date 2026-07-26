# B000056 — Runtime Certification Summary

**Classification:** RUNTIME_BEHAVIOR_ERROR
**Runtime called:** True
**Adapter:** lawim_v2.conversation.program_f_adapter.ProgramFEngineAdapter
**Orchestrator:** lawim_runtime.conversation.journey.ConversationJourneyOrchestrator
**Duration:** 20.3ms
**User turns:** 4
**Assertions:** 1P / 4F

## Violations
- B000056-MEM-001: expected=['transaction_type', 'property_type', 'city', 'budget', 'bedrooms', 'preferred_areas', 'move_in_date'], actual=['property_type', 'transaction_type', 'city', 'district', 'budget_max', 'bedrooms', 'move_in_date', 'preferred_areas']
- B000056-BIZ-001: expected=create_search_request, actual=CONFIRM_BUSINESS_CREATION
- B000056-Q-001: expected=1, actual=None
- B000056-OBJ-001: expected=1, actual=None