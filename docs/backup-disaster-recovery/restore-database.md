# Restore Database

STATUT : CIBLE DOCUMENTAIRE ACTIVE

## Goal

Restore PostgreSQL into an isolated target first, then verify the data before any production cutover.

## Canonical steps

1. select a validated backup
2. verify manifest and checksum
3. decrypt the backup artifact
4. decompress the dump
5. restore into an isolated database
6. validate tables and key queries
7. record the result

## Safety rules

- Never overwrite production by default.
- Never use a browser-side command.
- Never trust a backup artifact that has not been verified.

## Current state

- The repository has rehearsal restore helpers, but no validated isolated PostgreSQL restore service is documented yet.
