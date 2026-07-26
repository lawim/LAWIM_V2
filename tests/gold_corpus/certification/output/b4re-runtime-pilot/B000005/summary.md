# B000005 — Runtime Certification Summary

**Classification:** RUNTIME_BEHAVIOR_ERROR
**Runtime called:** True
**Adapter:** lawim_v2.conversation.program_f_adapter.ProgramFEngineAdapter
**Orchestrator:** lawim_runtime.conversation.journey.ConversationJourneyOrchestrator
**Duration:** 34.0ms
**User turns:** 6
**Assertions:** 1P / 4F

## Violations
- B000005-MEM-001: expected=['transaction_type', 'property_type', 'city', 'move_in_date', 'budget', 'bedrooms', 'preferred_areas'], actual=['property_type', 'transaction_type', 'city', 'budget_max', 'bedrooms', 'district', 'preferred_areas', 'move_in_date']
- B000005-BIZ-001: expected=create_search_request, actual=CONFIRM_BUSINESS_CREATION
- B000005-Q-001: expected=1, actual=None
- B000005-OBJ-001: expected=1, actual=None