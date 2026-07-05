# Server Architecture

## Storage tree

```text
/opt/lawim
├── app
├── compose
├── config
├── data
│   ├── postgres
│   ├── redis
│   ├── media
│   ├── thumbnails
│   ├── registry
│   └── runtime
├── backups
│   └── pre-start
├── logs
├── secrets
│   └── tls
├── scripts
├── releases
│   └── bc46a686
├── shared
│   ├── media
│   ├── exports
│   ├── imports
│   ├── tmp
│   └── cache
└── current -> /opt/lawim/releases/bc46a686
```

## Docker networks

- `lawim-public` carries the application ingress path.
- `lawim-private` isolates app-to-service traffic.
- `lawim-data` isolates database and cache traffic.

## Runtime flow

```text
Client
  -> Nginx on Ubuntu
    -> lawim-app container on 127.0.0.1:3000
      -> lawim-postgres container
      -> lawim-redis container
      -> /opt/lawim/shared and /opt/lawim/data for runtime files
```

## Storage responsibilities

- `/opt/lawim/data/postgres`: PostgreSQL volume.
- `/opt/lawim/data/redis`: Redis volume.
- `/opt/lawim/shared/media`: public and shared media exchange.
- `/opt/lawim/shared/exports`: generated exports.
- `/opt/lawim/backups`: backup archives and dumps.
- `/opt/lawim/logs`: host-level logs and exported runtime logs.
- `/opt/lawim/secrets`: server-only secret material.

## Operational stance

- application code is containerized;
- database and cache are containerized;
- reverse proxy is native on the host;
- secrets never leave the server;
- documentation never enters the OVH payload.
