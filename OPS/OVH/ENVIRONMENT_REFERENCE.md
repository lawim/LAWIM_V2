# Environment Reference

| Variable | Role | Required |
| --- | --- | --- |
| `LAWIM_ENV` | runtime environment selector | yes |
| `APP_ENV` | application environment selector | yes |
| `STACK_PROFILE` | deployment profile name | yes |
| `LOG_LEVEL` | runtime logging verbosity | yes |
| `PUBLIC_BASE_URL` | external base URL | yes |
| `SECRET_PROVIDER` | secret sourcing mode | yes |
| `LAWIM_HOST` | bind host for the app | yes |
| `LAWIM_PORT` | bind port for the app | yes |
| `LAWIM_DB_DRIVER` | database driver selector | yes |
| `LAWIM_DATABASE_URL` | primary database URL | yes |
| `LAWIM_DB_FALLBACK` | allow sqlite fallback | yes |
| `LAWIM_AAD_ENABLED` | AAD switch | yes |
| `LAWIM_DEFAULT_LANGUAGE` | default UI language | yes |
| `LAWIM_MEDIA_PROVIDER` | media backend | yes |
| `LAWIM_MEDIA_STORAGE_PATH` | media storage root | yes |
| `LAWIM_PUBLIC_MEDIA` | public media flag | yes |
| `LAWIM_SEED_DEMO_DATA` | seed demo data switch | yes |
| `LAWIM_GEOCODING_PROVIDER` | geocoding provider | yes |
| `LAWIM_CORS_ORIGINS` | allowed origins | yes |
| `REDIS_URL` | Redis connection string | yes |
| `DATABASE_URL` | tooling compatibility URL | yes |
| `SECRET_KEY` | application secret key | yes |
| mail/SMS/WhatsApp credentials | future integrations only | optional |

No values are stored here. The values live on the server only.
