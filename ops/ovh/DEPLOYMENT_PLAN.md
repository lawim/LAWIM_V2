# Deployment Plan

## Goal

Prepare the OVH VPS for LAWIM_V2 and deploy the approved runtime bundle without copying local documentation or analysis material.

## Sequence

1. Verify SSH access to the VPS.
2. Create the `lawim` system user if it does not exist.
3. Create the production tree under `/opt/lawim`.
4. Install host packages required by the target:
   - Docker
   - Docker Compose v2
   - Nginx
   - Certbot
   - firewall tooling
5. Create Docker networks for public, private and data traffic if needed.
6. Transfer the approved runtime tarball to `/opt/lawim/releases/`.
7. Extract the tarball into `/opt/lawim/releases/bc46a686/`.
8. Point `/opt/lawim/current` to the extracted release.
9. Create server-side environment files in `/opt/lawim/secrets/`.
10. Prepare the application, PostgreSQL and Redis containers.
11. Configure host Nginx to proxy the application on the temporary IPv4 endpoint.
12. Run the pre-start backup.
13. Start PostgreSQL, Redis and the application.
14. Validate health endpoints, login flow, language default and geolocation search.
15. Keep DNS/TLS as a follow-up if a production domain is not yet available.

## Rollback

- stop the stack;
- repoint `/opt/lawim/current` to the previous release;
- restore the last backup only if data rollback is required;
- re-run healthchecks before reopening access.

