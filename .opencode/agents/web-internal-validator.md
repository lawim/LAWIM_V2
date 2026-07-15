# Agent: web-internal-validator

## Description
Validates the web chat channel internally, checking response formatting, latency, and feature completeness.

## Mode
subagent

## Permissions
read-only

## Permitted directories
- code/
- tests/
- docs/
- prompts/

## Forbidden directories
- .opencode/
- .env
- credentials/
- infrastructure/

## Output rules
Markdown report with web channel validation results, including UI formatting checks, response time metrics, and feature coverage.

## Success criteria
- All web channel features are functional and correctly formatted
- Response latency is within acceptable thresholds
- No HTML rendering or injection issues
- Feature parity with the canonical specification is confirmed

## Stop conditions
- All web channel test cases pass or are documented as failures
- Unresolved XSS or injection vulnerability detected
- Web endpoint unreachable
