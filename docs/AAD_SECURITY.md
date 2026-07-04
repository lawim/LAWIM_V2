# AAD integration scaffold

This document captures an additive Microsoft Entra ID integration scaffold for LAWIM_V2.

Principles:
- Keep secret handling external and never commit real tenant credentials.
- Let AAD remain opt-in through `LAWIM_AAD_ENABLED`.
- Reuse the existing `SECRET_PROVIDER` contract so the platform can switch to `entra` without changing the app logic.

Expected environment variables:
- `LAWIM_AAD_ENABLED`
- `LAWIM_AAD_TENANT_ID`
- `LAWIM_AAD_CLIENT_ID`
- `LAWIM_AAD_SCOPES`
- `LAWIM_AAD_REDIRECT_URI`
- `SECRET_PROVIDER`

Palier 2 behavior:
- AAD remains disabled by default.
- The authentication layer exposes an optional entry point for future Entra integration.
- No Microsoft network call is performed by the scaffold.
- Local authentication remains the primary path unless an explicit AAD integration is enabled later.
