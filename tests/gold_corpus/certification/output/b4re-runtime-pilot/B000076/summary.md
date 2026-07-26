# B000076 — Runtime Certification Summary

**Classification:** RUNTIME_BEHAVIOR_ERROR
**Runtime called:** True
**Adapter:** lawim_v2.conversation.program_f_adapter.ProgramFEngineAdapter
**Orchestrator:** lawim_runtime.conversation.journey.ConversationJourneyOrchestrator
**Duration:** 19.6ms
**User turns:** 3
**Assertions:** 1P / 4F

## Violations
- B000076-MEM-001: expected=['transaction_type', 'property_type', 'city', 'budget', 'bedrooms', 'preferred_areas', 'move_in_date'], actual=['property_type', 'transaction_type', 'city', 'district', 'budget_max', 'bedrooms']
- B000076-BIZ-001: expected=none, actual=CONFIRM_BUSINESS_CREATION
- B000076-Q-001: expected=1, actual=None
- B000076-OBJ-001: expected=0, actual=None