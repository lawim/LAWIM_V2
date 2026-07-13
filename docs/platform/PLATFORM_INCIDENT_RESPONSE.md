# Platform Incident Response

## Common incidents

- Webhook rejected by authentication
- Double response prevented by idempotence
- Channel delivery failure
- Provider timeout or quota issue
- Persona mismatch

## Response steps

1. Capture the failing event.
2. Identify the exact stage of the break.
3. Validate configuration and runtime variables.
4. Fix only the root cause.
5. Add a regression test if code changed.
6. Re-run the affected tests.
7. Redeploy and re-check the channel.

