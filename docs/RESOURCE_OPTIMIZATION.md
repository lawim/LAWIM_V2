# Resource Optimization Plan

## Scope
This phase targets resource efficiency only. No business behavior, no security posture, and no release-critical functionality are altered.

## Baseline
- Frontend production build: 2 entry points, 200 modules transformed.
- Current asset profile:
  - web CSS: 18.76 kB
  - admin CSS: 18.63 kB
  - web JS: 119.68 kB
  - admin JS: 120.42 kB
  - shared shell chunk: 199.53 kB
- Service worker precache footprint: 467.39 KiB.

## Implemented low-risk actions
1. Enabled Vite target `es2020` to avoid unnecessary modern syntax overhead.
2. Disabled source maps in production to reduce artifact size and CI storage cost.
3. Split vendor chunks by dependency family to improve cache reuse and reduce re-download pressure.
4. Kept the existing UI structure and API contracts intact.

## Expected impact
- Lower initial JS payload per route.
- Better cache reuse for shared dependencies.
- Reduced artifact size and storage overhead.
- No change to user-visible business workflows.
