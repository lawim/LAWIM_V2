# B000021 — Runtime Certification Summary

**Classification:** RUNTIME_BEHAVIOR_ERROR
**Runtime called:** True
**Adapter:** lawim_v2.conversation.program_f_adapter.ProgramFEngineAdapter
**Orchestrator:** lawim_runtime.conversation.journey.ConversationJourneyOrchestrator
**Duration:** 33.7ms
**User turns:** 5
**Assertions:** 1P / 4F

## Violations
- B000021-MEM-001: expected=['transaction_type', 'property_type', 'city', 'move_in_date', 'budget', 'preferred_areas', 'bedrooms'], actual=['property_type', 'transaction_type', 'city', 'budget_max', 'district', 'preferred_areas', 'bedrooms']
- B000021-BIZ-001: expected=create_search_request, actual=CONFIRM_BUSINESS_CREATION
- B000021-Q-001: expected=1, actual=None
- B000021-OBJ-001: expected=1, actual=None