# Mission 04 Frontend UX Release Report

## Scope

Rebuild the LAWIM login experience, remove role selection from the access page, and route users to the correct dashboard from the API role payload.

## Production frontend source decision

The production frontend source is `code/lawim_v2/static`.

Why:
- `code/lawim_v2/server.py` serves `/`, `/app.js`, and `/styles.css` directly from that static tree.
- The active OVH runtime documented in `OPS/OVH/SERVER_ARCHITECTURE.md` is the `lawim-app` container on port `3000`.
- The current release flow is therefore the Python runtime plus its embedded static frontend, not the Vite build under `frontend/`.

## Changes delivered

- Reworked the public login shell with the LAWIM logo and explicit slogan line.
- Kept the login form to email + password only.
- Removed any visible demo access affordances from the login page.
- Added role resolution from the API response:
  - `admin`
  - `agent`
  - `owner`
- Added controlled auth traces:
  - `LOGIN_OK`
  - `ROLE_RESOLVED`
  - `DASHBOARD_SELECTED`
  - `DASHBOARD_RENDERED`
  - plus the existing `REFRESH_START`, `REFRESH_DONE`, `APPLY_JOURNEY`, and `RENDER_DONE` lifecycle traces
- Tightened login and session error messages:
  - incorrect credentials
  - server unavailable
  - session expired
  - access not authorized
- Removed stale demo-button hooks from the static runtime.
- Updated tests to reflect the production branding and role-based routing.

## Validation

Frontend:
- `npm run test -- --run`
- `npm run build`

Python:
- `PYTHONPATH=../code:. python3 -m unittest test_lawim_v2`
- `PYTHONPATH=code:. python3 -m unittest tests.test_runtime_smoke`

All of the above passed at the end of the run.

## Deployment procedure

1. Build the release from the repository state that contains `code/lawim_v2/static`.
2. Package the release artifact and upload it to `/opt/lawim/releases/<release-id>`.
3. Update `/opt/lawim/current` to point to the new release.
4. Restart `lawim-app`.
5. Verify:
   - `/` loads the new login page.
   - `/api/health` is healthy.
   - `admin@lawim.app` logs in and opens the admin dashboard.

## Rollback procedure

1. Stop or drain the current `lawim-app` instance if needed.
2. Point `/opt/lawim/current` back to the previous release directory.
3. Restart `lawim-app`.
4. Recheck `/` and `/api/health`.

## Notes

- No changes were made to PostgreSQL, Redis, or Nginx.
- No backend auth change was required for this mission.
- Unrelated pre-existing worktree changes were left untouched.
