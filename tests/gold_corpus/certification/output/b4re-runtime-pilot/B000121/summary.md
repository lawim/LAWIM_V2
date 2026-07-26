# B000121 — Runtime Certification Summary

**Classification:** RUNTIME_BEHAVIOR_ERROR
**Runtime called:** True
**Adapter:** lawim_v2.conversation.program_f_adapter.ProgramFEngineAdapter
**Orchestrator:** lawim_runtime.conversation.journey.ConversationJourneyOrchestrator
**Duration:** 19.5ms
**User turns:** 4
**Assertions:** 1P / 4F

## Violations
- B000121-MEM-001: expected=['transaction_type', 'property_type', 'city', 'budget', 'preferred_areas', 'move_in_date', 'bedrooms'], actual=['property_type', 'transaction_type', 'city', 'district', 'budget_max', 'move_in_date', 'bedrooms']
- B000121-BIZ-001: expected=create_search_request, actual=CONFIRM_BUSINESS_CREATION
- B000121-Q-001: expected=1, actual=None
- B000121-OBJ-001: expected=1, actual=None