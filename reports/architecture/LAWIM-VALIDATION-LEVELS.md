# LAWIM — Validation Levels L0-L8

**Version:** 3.0.0-alpha
**Last Updated:** 2026-07-22
**Status:** CANONICAL

---

## 1. Validation Level Definitions

| Level | Name | Definition | How to Achieve |
|-------|------|------------|----------------|
| L0 | Code Present | Source files exist in the repository | `git ls-files <path>` returns the file |
| L1 | Static Validation | Code compiles, imports resolve, no circular imports, no syntax errors | `compileall` passes; `pytest --import-mode` succeeds; `ruff`/`mypy` pass |
| L2 | Unit Test | Individual components tested in isolation with controlled inputs/outputs | `pytest` per module passes; all edge cases covered; no external dependencies |
| L3 | Component Integration | Multiple components wired together; no real external services | Integration tests pass with in-memory dependencies; cross-component contract verified |
| L4 | Runtime Integration | Full pipeline executes in a controlled environment (dev/staging) | End-to-end test in dev environment; all pipeline stages exercised |
| L5 | External Sandbox | Connected to real external service in sandbox/dry-run mode | Sandbox provider tests pass (e.g., Green API sandbox, Telegram test bot); no real user traffic |
| L6 | Real Channel Test | Real user message received via real webhook, processed end-to-end, real response delivered | Full E2E channel test protocol executed; correlation_id tracked through entire pipeline |
| L7 | Production Verification | Verified on production with real traffic from real users | Feature is live for real users; monitoring confirms correct behavior; no regressions |
| L8 | Business Certification | Accepted by business stakeholders as meeting requirements | Business stakeholder signs off; acceptance criteria met; user acceptance test passed |

---

## 2. Validation Progression Rules

- A component MUST pass all lower levels before being tested at a higher level.
- Each level requires documented evidence specific to that level.
- Evidence from a lower level does NOT substitute for a higher level.
- L4 (Runtime Integration) requires the full pipeline in a controlled environment — passing L2 does not satisfy L4.
- L6 (Real Channel Test) requires a real user message and real webhook — passing L4 does not satisfy L6.

---

## 3. Forbidden Equivalence Statements

The following equivalences are strictly forbidden. No report, tag, commit message, or status update may claim or imply them.

| Statement | Reason |
|-----------|--------|
| L2 = L4 | Unit tests (isolated components) are not equivalent to integration tests (wired pipeline). |
| L4 = L6 | Controlled environment integration is not equivalent to real channel end-to-end. |
| L6 = L7 | A single real channel test is not equivalent to sustained production verification. |
| L7 = L8 | Production technical verification is not equivalent to business stakeholder acceptance. |
| SIMULATED_SUCCESS = DOMAIN_INTEGRATION_PASS | A test with mocked externals is not equivalent to real external integration. |
| AUTOMATED_TEST_PASS = REAL_CHANNEL_PASS | Any automated test (unit, integration) is not equivalent to a real message on a real channel. |
| CODE_PRESENT = RUNTIME_ACTIVE | Code in the repository is not equivalent to code running and serving users. |
| COMMIT_CREATED = COMMIT_DEPLOYED | A commit on any branch is not equivalent to deployment to any environment. |
| DEPLOYED = VERIFIED | Software deployed is not equivalent to software behaving correctly in production. |
| HEALTHZ_PASS = BUSINESS_FLOW_PASS | A health endpoint returning 200 is not equivalent to a complete business journey functioning. |

---

## 4. Evidence Requirements by Level

| Level | Acceptable Evidence | Not Acceptable |
|-------|---------------------|----------------|
| L0 | `git ls-files` output | README mention, verbal claim |
| L1 | `compileall` log, `ruff`/`mypy` pass, no circular import check | "Compiles on my machine", "No visible errors" |
| L2 | `pytest` output showing all tests PASS | "All existing tests pass" without specifying which |
| L3 | Integration test output with multi-component scenarios | Single-component unit tests |
| L4 | Full pipeline test log in dev environment with correlation_id trace | "Everything works together" without trace |
| L5 | Sandbox provider response logs (e.g., Green API sandbox) | "Provider authorized" without test message |
| L6 | Real user message, webhook receipt timestamp, correlation_id, pipeline log, delivery confirmation, response content verification | "Channel is configured" |
| L7 | Production monitoring dashboards, alert logs, user feedback, no regression evidence | "Deployed to production" |
| L8 | Signed business acceptance document, user acceptance test protocol results | Engineering lead sign-off alone |

---

## 5. Current Status by Program

| Program | Highest Validated Level | Evidence |
|---------|------------------------|----------|
| A (LROS Foundation) | L3 | 38 integration tests pass across all LROS components |
| B (ProjectProfile) | L3 | Integration tests with LROS pass |
| C (Qualification + Decision) | L3 | Integration tests with Program B pass |
| C.5 (Action Execution) | L3 | 276 tests pass; 3 pre-existing V2 baseline failures confirmed |
| D (Domain Engines) | L0 | Code not yet written |
| V2 Conversation Runtime | L7 | Production-verified on WhatsApp and Telegram |
