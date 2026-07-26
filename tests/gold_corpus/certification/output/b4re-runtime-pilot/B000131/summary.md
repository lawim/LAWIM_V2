# B000131 — Runtime Certification Summary

**Classification:** RUNTIME_BEHAVIOR_ERROR
**Runtime called:** True
**Adapter:** lawim_v2.conversation.program_f_adapter.ProgramFEngineAdapter
**Orchestrator:** lawim_runtime.conversation.journey.ConversationJourneyOrchestrator
**Duration:** 39.3ms
**User turns:** 6
**Assertions:** 1P / 4F

## Violations
- B000131-MEM-001: expected=['transaction_type', 'property_type', 'city', 'budget', 'preferred_areas'], actual=['property_type', 'transaction_type', 'city', 'budget_max']
- B000131-BIZ-001: expected=create_search_request, actual=CONFIRM_BUSINESS_CREATION
- B000131-Q-001: expected=1, actual=None
- B000131-OBJ-001: expected=1, actual=None