# Reviewed Spec Adapter Details — LCIP B.4R-E

Adapter: tests/gold_corpus/certification/runtime/reviewed_spec_adapter.py
Checker: tests/gold_corpus/certification/runtime/executability.py

Pipeline:
b4rc-reviewed/<ID>/ -> ReviewedSpecAdapter -> RuntimeExecutor -> ProgramFEngineAdapter -> ConversationJourneyOrchestrator
