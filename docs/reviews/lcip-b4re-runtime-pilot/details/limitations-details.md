# Limitations — LCIP B.4R-E

1. No business object creation (no ActionExecutionEngine)
2. No idempotence test (needs business creation)
3. No restart test (RuntimeExecutor skips system events)
4. Non-French conversations processed in French
5. Field name mismatch (budget vs budget_max)
6. AGENT_STRUCTURED_REVIEW only

Recommend: activate ActionExecutionEngine, align field names, test restart for B000083.
