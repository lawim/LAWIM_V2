# Feature Dependency Catalog

This catalog records the main dependency chains used by LAWIM.

## Examples

- Brain conversation -> shared memory + qualification matrices + orchestrator
- WhatsApp outbound -> WhatsApp connector + valid chat id + delivery adapter
- Telegram outbound -> Telegram connector + bot token + webhook secret + IPv4-capable transport
- Relationship request -> Matching + consent + relation engine
- Financial action -> Financial core + payment provider
- Follow-up -> relation engine + workflow + notifications

## Rule

- A dependency missing at runtime must fail closed and log the reason.

