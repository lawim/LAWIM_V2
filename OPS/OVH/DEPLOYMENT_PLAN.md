# Deployment Plan

## Goal

Deploy LAWIM_V2 to OVH without copying local documentation, prompts, tests or analysis material.

## Validated sequence

1. verify server access;
2. create the `lawim` system user and the `/opt/lawim` tree;
3. verify Docker, Nginx, Certbot and firewall tooling;
4. create Docker networks for public, private and data traffic;
5. transfer only the approved runtime bundle;
6. extract the bundle into `/opt/lawim/releases/bc46a686`;
7. repoint `/opt/lawim/current`;
8. create server-only environment files and secrets;
9. create a pre-start backup;
10. start PostgreSQL, Redis and the application;
11. configure host Nginx;
12. validate `/healthz`, `/readyz`, `/api/health`, login and geolocation;
13. keep DNS/TLS finalization documented separately.

## Rollback

- stop the stack;
- repoint `/opt/lawim/current` to the previous release;
- restore the latest backup only if data rollback is required;
- rerun healthchecks before reopening traffic.
