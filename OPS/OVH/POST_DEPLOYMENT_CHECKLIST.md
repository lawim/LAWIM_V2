# Post Deployment Checklist

- application container is running
- PostgreSQL container is healthy
- Redis container is healthy
- Nginx is active on the host
- `/healthz` returns `ok`
- `/readyz` reports ready
- `/api/health` responds correctly
- local login works
- default language is `fr`
- AAD remains disabled by default
- `/api/geo/search` returns Cameroon locations
- media directories are writable
- no internal document is publicly exposed
- no secret appears in logs
- pre-start backup exists
- rollback path is documented and usable

