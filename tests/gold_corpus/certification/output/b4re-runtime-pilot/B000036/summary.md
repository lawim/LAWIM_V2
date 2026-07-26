# B000036 — Runtime Certification Summary

**Classification:** RUNTIME_BEHAVIOR_ERROR
**Runtime called:** True
**Adapter:** lawim_v2.conversation.program_f_adapter.ProgramFEngineAdapter
**Orchestrator:** lawim_runtime.conversation.journey.ConversationJourneyOrchestrator
**Duration:** 28.8ms
**User turns:** 5
**Assertions:** 1P / 4F

## Violations
- B000036-MEM-001: expected=['transaction_type', 'property_type', 'city', 'preferred_areas', 'move_in_date', 'budget', 'price', 'is_owner'], actual=['property_type', 'transaction_type', 'city', 'district', 'budget_max']
- B000036-BIZ-001: expected=create_search_request, actual=CONFIRM_BUSINESS_CREATION
- B000036-Q-001: expected=1, actual=None
- B000036-OBJ-001: expected=1, actual=None