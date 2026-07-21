# LAWIM — Provider Failure Matrix

- Author: LAWIM AI
- Date: 2026-07-21
- Status: IMPLEMENTED
- Chantier: 4 — Controlled Generation

## Provider Chain

Default: **DeepSeek → OpenAI → Gemini Primary → Gemini Secondary → Internal**

## Failure Matrix

| # | Scenario | DeepSeek | OpenAI | Gemini Primary | Gemini Secondary | Internal | Expected Outcome |
|---|----------|----------|--------|----------------|------------------|----------|-----------------|
| 1 | All succeed | tried ✓ | skipped | skipped | skipped | skipped | Return DeepSeek response |
| 2 | 1st fails | fails ✗ | tried ✓ | skipped | skipped | skipped | Return OpenAI response |
| 3 | 1st times out | timeout ⏱ | tried ✓ | skipped | skipped | skipped | Return OpenAI response |
| 4 | 1st circuit open | skip ⚠ | tried ✓ | skipped | skipped | skipped | Return OpenAI response |
| 5 | 1st+2nd fail | fails ✗ | fails ✗ | tried ✓ | skipped | skipped | Return Gemini Primary response |
| 6 | 1st+2nd+3rd fail | fails ✗ | fails ✗ | fails ✗ | tried ✓ | skipped | Return Gemini Secondary response |
| 7 | All external fail | fails ✗ | fails ✗ | fails ✗ | fails ✗ | used ✓ | Return internal fallback |
| 8 | 1st circuit, 2nd circuit | skip ⚠ | skip ⚠ | tried ✓ | skipped | skipped | Return Gemini Primary response |
| 9 | All circuits open | skip ⚠ | skip ⚠ | skip ⚠ | skip ⚠ | used ✓ | Return internal fallback |
| 10 | 1st invalid response | invalid ✗ | tried ✓ | skipped | skipped | skipped | Return OpenAI response |
| 11 | All timeout | timeout ⏱ | timeout ⏱ | timeout ⏱ | timeout ⏱ | used ✓ | Return internal fallback |
| 12 | 1st retry succeeds | retry1→✓ | skipped | skipped | skipped | skipped | Return DeepSeek (after retry) |
| 13 | 1st retry fails → 2nd | retry1→✗ | tried ✓ | skipped | skipped | skipped | Return OpenAI |
| 14 | 1st timeout → retry → fails → 2nd | timeout→✗ | tried ✓ | skipped | skipped | skipped | Retry counted, 2nd tried |
| 15 | 3 failures → circuit opens | fails(x3) | tried ✓ | skipped | skipped | skipped | 3rd failure opens circuit for DeepSeek; OpenAI used |
| 16 | Circuit recovery after 60s | open→closed | skipped | skipped | skipped | skipped | After 60s, circuit transitions back to CLOSED |
| 17 | Internal fallback fails | fails ✗ | fails ✗ | fails ✗ | fails ✗ | fails ✗ | AllProvidersFailedError raised |
| 18 | Language FR all succeed | tried ✓ | skipped | skipped | skipped | skipped | French response returned |
| 19 | Language EN all succeed | tried ✓ | skipped | skipped | skipped | skipped | English response returned |
| 20 | Language PCM all succeed | tried ✓ | skipped | skipped | skipped | skipped | PCM response returned |

## Legend

| Symbol | Meaning |
|--------|---------|
| ✓ | Succeeded |
| ✗ | Failed |
| ⏱ | Timed out |
| ⚠ | Skipped (circuit open) |
| → | Transition |

## Key Behaviors

### Timeout
- Total deadline: 30s (configurable via DEFAULT_TOTAL_TIMEOUT)
- Per-provider timeout: connect 10s + read 20s
- If total deadline is reached mid-chain, remaining providers are skipped
- Timeout counts as failure for circuit breaker
- Recorded via `ProviderRegistry.record_timeout()`

### Retry
- Max 1 retry per provider
- Retryable errors: timeout, rate_limit, server_error, 429, 500, 503, connection, temporary, too many requests, service unavailable
- Non-retryable: authentication_error (401, 403), empty response
- Backoff: 1.0s fixed

### Circuit Breaker
- Threshold: 3 consecutive failures → OPEN
- Recovery time: 60s
- While OPEN: provider is skipped in chain
- On success: immediately CLOSED, failure count reset
- State tracked via `CircuitBreakerState` (provider, state, failure_count, open_until)

### Internal Fallback
- Invoked when all external providers fail
- Uses `InternalReasoningEngine.reason()` for intent-based responses
- If internal fallback also fails: `AllProvidersFailedError` raised
- Error propagates to `CommunicationService` which returns CONTROLLED_ERROR dialogue act

### Invalid Response
- Non-JSON, missing fields, wrong types → RepairHandler attempts single repair
- Repair fails → response discarded → next provider tried
- If response is repaired and validates → counted as success from original provider

### Order Guarantee
| # | Provider | Reason |
|---|----------|--------|
| 1 | DeepSeek | Lowest cost, primary model |
| 2 | OpenAI | Highest quality, secondary |
| 3 | Gemini Primary | Gemini redundancy |
| 4 | Gemini Secondary | Gemini redundancy |
| 5 | Internal | Last resort (no API cost) |
