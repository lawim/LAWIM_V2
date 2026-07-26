# B000111 — Runtime Certification Summary

**Classification:** RUNTIME_BEHAVIOR_ERROR
**Runtime called:** True
**Adapter:** lawim_v2.conversation.program_f_adapter.ProgramFEngineAdapter
**Orchestrator:** lawim_runtime.conversation.journey.ConversationJourneyOrchestrator
**Duration:** 45.3ms
**User turns:** 7
**Assertions:** 1P / 4F

## Violations
- B000111-MEM-001: expected=['transaction_type', 'property_type', 'city', 'budget', 'bedrooms', 'preferred_areas', 'move_in_date'], actual=['property_type', 'transaction_type', 'city', 'budget_max', 'move_in_date']
- B000111-BIZ-001: expected=create_search_request, actual=CONFIRM_BUSINESS_CREATION
- B000111-Q-001: expected=1, actual=None
- B000111-OBJ-001: expected=1, actual=None