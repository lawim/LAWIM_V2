# Storage Orchestrator

The storage orchestrator resolves access to storage providers in a provider-agnostic way while keeping the media registry as the source of truth.

## Principles

- Resolve temporary access through the provider layer
- Keep provider decisions separated from business entities
- Support mock providers for local, Google Drive, backup center, and external disk scenarios
- Choose the first available resource on the official storage route
- Keep the routed drive traceable in the admin dashboard
