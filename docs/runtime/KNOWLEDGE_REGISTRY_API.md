# Knowledge Registry API (v4, Internal)

Base path: `/api/v4/knowledge/`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v4/knowledge/health` | Runtime health + registry counts |
| GET | `/api/v4/knowledge/version` | Deterministic version hash |
| GET | `/api/v4/knowledge/registries` | All registry summaries |
| GET | `/api/v4/knowledge/property-types` | List all property types (query: `?q=`) |
| GET | `/api/v4/knowledge/property-types/{id}` | Single property type |
| GET | `/api/v4/knowledge/services` | List all services (query: `?q=`) |
| GET | `/api/v4/knowledge/services/{id}` | Single service |
| GET | `/api/v4/knowledge/roles` | All roles |
| GET | `/api/v4/knowledge/intents` | All intents |
| GET | `/api/v4/knowledge/transactions` | All transactions |
| GET | `/api/v4/knowledge/matrices` | All matrices |
| GET | `/api/v4/knowledge/matrices/{id}` | Single matrix |
| GET | `/api/v4/knowledge/fields/{id}` | Single field definition |
| GET | `/api/v4/knowledge/source-trace/{id}` | Source provenance |

All endpoints require `LAWIM_FEATURE_KNOWLEDGE_INTERNAL_API=true`. Returns JSON.
