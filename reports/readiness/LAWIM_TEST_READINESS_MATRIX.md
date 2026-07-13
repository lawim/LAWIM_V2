# LAWIM Test Readiness Matrix

## Coverage axes

| Axis | Examples | Proof |
| --- | --- | --- |
| Profiles | Admin, agent, client, partner | Authenticated sessions |
| Languages | FR, EN, PCM | UI and chat responses |
| Modules | Brain, matching, notifications, finance | API and UI checks |
| Channels | Web, WhatsApp, Telegram, Email | Real or simulated delivery |
| Intent families | Rent, buy, land, build, pay, follow-up | Conversation transcripts |
| Cycle states | Discovery, qualification, search, consent, relation, follow-up, close | State transitions |
| Actors | User, LAWIM AI, staff, professional | Structured sender metadata |
| Permissions | Read, create, approve, publish | Role-gated actions |
| Consent | Relationship, sharing, transactional messages | Explicit audit events |
| Positive cases | Happy path qualification and delivery | Tests and logs |
| Negative cases | Invalid secret, duplicate, timeout, no result | Error handling checks |
| Environments | Dev, staging, production | Deployment checks |

## Minimum evidence

- Test command and result
- Log excerpt without secrets
- Database persistence proof
- Delivery proof when applicable
- Commit hash if code changed

