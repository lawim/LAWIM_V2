# Maintenance Guide

## Routine operations

- restart the application after code or config updates;
- verify the stack health after each restart;
- keep the current release symlink stable unless a deliberate rollback is planned;
- clean old archives only after a verified retention review.

## Updates

- update the release bundle locally;
- transfer only the approved runtime payload;
- keep secrets on the server;
- do not modify the database schema during routine maintenance unless a validated migration is explicitly scheduled.

## Rollback

- use the previous release directory under `/opt/lawim/releases/`;
- restore the last backup only when data rollback is required;
- document the rollback outcome.
