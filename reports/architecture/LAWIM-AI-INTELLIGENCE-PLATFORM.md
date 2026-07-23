# LAWIM AI Intelligence Platform

**Date:** 2026-07-23
**Program:** F
**Status:** COMPLETE_WITH_RESERVATIONS

## Architecture

```
InteractionEnvelope
  -> AIIntelligenceGateway (mode: DISABLED|DETERMINISTIC|SHADOW|CANARY|PRIMARY)
    -> StructuredExtractionEngine
      -> ExtractionCandidate[]
      -> CandidateUpdate[]
      -> Field Registry Validation
      -> ProfilePatch -> ProjectProfile
    -> LLMGateway
      -> ProviderRegistry
      -> ProviderRouter
      -> AIProvider.generate()
      -> Response validation
    -> KnowledgeGateway
      -> KnowledgeQuery
      -> RAG retrieval
      -> Citation building
    -> AIResponseWriter
      -> ResponseValidator
      -> DeterministicResponseWriter fallback
    -> AIEvaluator
      -> Extraction accuracy
      -> Hallucination tracking
      -> Safety metrics
```

## Core Contracts

| Contract | File | Purpose |
|----------|------|---------|
| AIIntelligenceGateway | gateway.py | Central AI orchestrator with mode routing |
| AIRequest | request.py | Standardized AI task request |
| AIResult | result.py | Standardized AI task result |
| AIContext | context.py | AI execution context |
| StructuredExtractionEngine | extraction/engine.py | Field extraction with deterministic + LLM |
| ExtractionCandidate | extraction/candidate.py | Single field extraction with provenance |
| AIProvider | providers/base.py | Abstract LLM provider |
| ProviderRegistry | providers/registry.py | Provider registration and routing |
| PromptRegistry | prompts/registry.py | Versioned prompt management |
| PromptRenderer | prompts/renderer.py | Deterministic prompt rendering |
| PromptInjectionDetector | prompts/injection.py | Injection pattern detection |
| KnowledgeGateway | knowledge/engine.py | Source-aware knowledge retrieval |
| AIResponseWriter | writing/writer.py | LLM + deterministic response generation |
| ResponseValidator | safety/validation.py | Post-generation claim validation |
| RedactionPolicy | safety/redaction.py | Sensitive data masking |
| DataClassification | safety/classification.py | Data sensitivity levels |
| AIEvaluator | evaluation/evaluator.py | Extraction and generation quality |
| AIMetrics | observability/metrics.py | AI observability counters |

## Modes

| Mode | Behavior | Default |
|------|----------|---------|
| AI_DISABLED | Returns UNAVAILABLE | No |
| AI_DETERMINISTIC | Uses deterministic extractor only | Yes |
| AI_SHADOW | Deterministic + LLM in parallel, no LLM effects | No |
| AI_CANARY | LLM for authorized users only | No |
| AI_PRIMARY_WITH_DETERMINISTIC_FALLBACK | LLM with deterministic fallback | No |
| AI_PRIMARY | LLM only | No |

## Feature Flags

All default to false:
- lros_ai_intelligence_enabled
- lros_ai_extraction_enabled
- lros_ai_response_writer_enabled
- lros_ai_knowledge_enabled
- lros_ai_rag_enabled
- lros_ai_shadow_mode
- lros_ai_provider_calls_enabled
