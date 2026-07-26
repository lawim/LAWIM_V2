# B000090 — Runtime Certification Summary

**Classification:** RUNTIME_BEHAVIOR_ERROR
**Runtime called:** True
**Adapter:** lawim_v2.conversation.program_f_adapter.ProgramFEngineAdapter
**Orchestrator:** lawim_runtime.conversation.journey.ConversationJourneyOrchestrator
**Duration:** 39.2ms
**User turns:** 6
**Assertions:** 0P / 5F

## Violations
- B000090-MEM-001: expected=['transaction_type', 'property_type', 'city', 'budget', 'preferred_areas', 'move_in_date'], actual=['property_type', 'transaction_type', 'city', 'bedrooms', 'district']
- B000090-BIZ-001: expected=create_search_request, actual=NONE
- B000090-LANG-001: expected=en, actual=fr
- B000090-Q-001: expected=1, actual=None
- B000090-OBJ-001: expected=1, actual=None