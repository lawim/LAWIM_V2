# LAWIM Brain

The LAWIM Brain is the orchestration layer for the new intelligent foundation. It does not call the backend directly; instead it coordinates the conversation engine, memory, digital twin, and learning services using the frontend SDK.

## Responsibilities

- Understand an intent
- Build a context
- Select modules
- Produce an execution plan
- Aggregate outputs
- Return a final response

## Architecture

- BrainIntent: captures the user intent
- BrainContext: provides the session context
- BrainRegistry: lists modules and their capabilities
- BrainRouter: selects modules for an intent
- BrainOrchestrator: executes the plan
