# B000096 — Runtime Certification Summary

**Classification:** RUNTIME_BEHAVIOR_ERROR
**Runtime called:** True
**Adapter:** lawim_v2.conversation.program_f_adapter.ProgramFEngineAdapter
**Orchestrator:** lawim_runtime.conversation.journey.ConversationJourneyOrchestrator
**Duration:** 40.8ms
**User turns:** 6
**Assertions:** 0P / 5F

## Violations
- B000096-MEM-001: expected=['transaction_type', 'property_type', 'city', 'budget', 'bedrooms', 'preferred_areas', 'move_in_date'], actual=['property_type', 'transaction_type', 'city', 'budget_max', 'bedrooms', 'district']
- B000096-BIZ-001: expected=create_search_request, actual=NONE
- B000096-LANG-001: expected=pcm, actual=fr
- B000096-Q-001: expected=1, actual=None
- B000096-OBJ-001: expected=1, actual=None