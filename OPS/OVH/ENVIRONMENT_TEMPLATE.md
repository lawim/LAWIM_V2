# Environment Template

This template is for the server only. It must not be committed as a real secret file.

```env
LAWIM_ENV=production
APP_ENV=production
STACK_PROFILE=production
LOG_LEVEL=info
PUBLIC_BASE_URL=http://164.132.44.192
SECRET_PROVIDER=external
LAWIM_HOST=0.0.0.0
LAWIM_PORT=3000
LAWIM_DB_DRIVER=postgresql
LAWIM_DATABASE_URL=postgresql://lawim:__POSTGRES_PASSWORD__@postgres:5432/lawim_v2
LAWIM_DB_FALLBACK=false
LAWIM_AAD_ENABLED=false
LAWIM_DEFAULT_LANGUAGE=fr
LAWIM_MEDIA_PROVIDER=local
LAWIM_MEDIA_STORAGE_PATH=/opt/lawim/shared/media
LAWIM_PUBLIC_MEDIA=false
LAWIM_SEED_DEMO_DATA=false
LAWIM_GEOCODING_PROVIDER=local
LAWIM_CORS_ORIGINS=http://164.132.44.192
REDIS_URL=redis://:__REDIS_PASSWORD__@redis:6379/0
DATABASE_URL=postgresql://lawim:__POSTGRES_PASSWORD__@postgres:5432/lawim_v2
SECRET_KEY=__REPLACE_ON_SERVER__
```

Notes:

- the application reads `LAWIM_DATABASE_URL`;
- `DATABASE_URL` is kept for operational tooling compatibility;
- all secret values are placeholders and must be replaced on the server only;
- temporary access by IPv4 is acceptable until DNS and TLS are finalized.

