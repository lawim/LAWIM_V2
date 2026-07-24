# Programme F — Conversation Engine Architecture

**Date:** 2026-07-24
**HEAD:** fb53e3d1 (commit conversation engine)
**Tests:** 784 PASS

## Architecture

```
User Input
  → ConversationEngine.process()
    → LLMAdapter.analyze() (optional, provider-independent)
    → IntentEngine.detect() (LLM-independent)
    → EntityExtractionEngine.extract() (LLM-independent)
    → ConversationMemory.add_entry()
    → QualificationEngine.evaluate() (LLM-independent)
    → Response type determination (business logic)
  → ConversationTurnResult
```

## Components

| Component | File | Responsibility |
|-----------|------|----------------|
| ConversationEngine | `engine/__init__.py` | Orchestrates the turn processing |
| IntentEngine | `intent/__init__.py` | Keyword-based intent detection (no LLM) |
| EntityExtractionEngine | `entity/__init__.py` | Regex + keyword entity extraction (no LLM) |
| ConversationMemory | `memory/__init__.py` | Short/long term memory, preferences, summary |
| QualificationEngine | `qualification/__init__.py` | Missing field detection, qualification level |
| LLMAdapter | `llm/__init__.py` | Abstract contract for LLM analysis |
| OpenAIAdapter | `adapters/__init__.py` | OpenAI provider adapter |
| DeepSeekAdapter | `adapters/__init__.py` | DeepSeek provider adapter |
| ClaudeAdapter | `adapters/__init__.py` | Anthropic/Claude provider adapter |
| GeminiAdapter | `adapters/__init__.py` | Google Gemini provider adapter |
| MistralAdapter | `adapters/__init__.py` | Mistral provider adapter |
| DeterministicLLMAdapter | `llm/__init__.py` | No-LLM fallback adapter |

## LLM Contract

```python
@dataclass
class LLMContract:
    intent: str = ""
    confidence: float = 0.0
    entities: dict[str, Any] = field(default_factory=dict)
    missing_information: list[str] = field(default_factory=list)
    summary: str = ""
    needs_clarification: bool = False
```

The LLM contract contains NO business decision fields (no action, payment, approve, reject, etc.).

## Tests

- 47 new conversation engine tests
- 0 regression (784 total)
- All adapters tested without API keys (graceful fallback)
- Contract enforcement tests verify LLM cannot influence business decisions
