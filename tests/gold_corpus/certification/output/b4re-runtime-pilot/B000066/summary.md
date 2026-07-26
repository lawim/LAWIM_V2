# B000066 — Runtime Certification Summary

**Classification:** RUNTIME_BEHAVIOR_ERROR
**Runtime called:** True
**Adapter:** lawim_v2.conversation.program_f_adapter.ProgramFEngineAdapter
**Orchestrator:** lawim_runtime.conversation.journey.ConversationJourneyOrchestrator
**Duration:** 72.4ms
**User turns:** 9
**Assertions:** 1P / 4F

## Violations
- B000066-MEM-001: expected=['transaction_type', 'property_type', 'city', 'budget', 'preferred_areas', 'move_in_date'], actual=['transaction_type', 'property_type', 'city', 'budget_max', 'district']
- B000066-BIZ-001: expected=create_search_request, actual=CONFIRM_BUSINESS_CREATION
- B000066-Q-001: expected=1, actual=None
- B000066-OBJ-001: expected=1, actual=None