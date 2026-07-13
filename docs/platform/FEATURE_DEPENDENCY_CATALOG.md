# Feature Dependency Catalog

This catalog records the main dependency chains used by LAWIM.

## Examples

- Conversation Core -> shared memory + qualification matrices + AI orchestrator + response validator + channel adapters
- Brain conversation -> shared memory + qualification matrices + orchestrator
- Minimum search threshold -> qualification matrix + search engine + matching engine
- WhatsApp outbound -> WhatsApp connector + valid chat id + delivery adapter
- Telegram outbound -> Telegram connector + bot token + webhook secret + IPv4-capable transport
- Relationship request -> matching + consent + relation engine
- Visit scheduling -> relationship + workflow + notifications
- Offer / negotiation -> commercial engine + workflow + document review
- Financial action -> financial core + payment provider
- Follow-up -> relation engine + workflow + notifications

## Rule

- A dependency missing at runtime must fail closed and log the reason.
- A dependency must never be recreated independently inside a channel connector.
