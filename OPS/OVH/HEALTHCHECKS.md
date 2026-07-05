# Healthchecks

## HTTP endpoints

- `/healthz` should return `ok`;
- `/readyz` should report ready state;
- `/api/health` should report the application, database and storage status;
- `/api/geo/search` should resolve Cameroon locations during runtime validation.

## Host checks

- `systemctl is-active nginx`
- `docker ps`
- `docker inspect lawim-app`
- `curl -k https://164.132.44.192/healthz`
- `curl -k https://164.132.44.192/readyz`
- `curl -k https://164.132.44.192/api/health`
- `df -h /opt/lawim`
- `free -m`

## Expectations

- no critical log spam;
- no 5xx on the public path;
- no exposed internal documentation;
- backup path present and writable.
