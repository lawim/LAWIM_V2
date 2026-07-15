# Agent: whatsapp-internal-validator

## Description
Validates the WhatsApp channel internally, checking message formatting, interactive components, and template compliance.

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
Markdown report with WhatsApp-specific validation results, including button/list rendering, media handling, and rate-limit compliance.

## Success criteria
- All WhatsApp message types (text, image, list, button) render correctly
- Interactive components navigate to the correct flows
- Template messages meet WhatsApp Business API specification
- No media upload or download failures

## Stop conditions
- All WhatsApp channel test cases pass or are documented as failures
- WhatsApp Business API endpoint unreachable
- Template rejection from API
