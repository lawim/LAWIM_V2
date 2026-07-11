# Restore Media

STATUT : CIBLE DOCUMENTAIRE ACTIVE

## Goal

Restore media and documents selectively or completely into an isolated directory before any production replacement.

## Canonical steps

1. select the archive
2. verify checksum and manifest
3. decrypt if needed
4. extract into a temporary directory
5. compare file counts and ownership
6. validate the content
7. perform the approved copy

## Safety rules

- Do not extract directly into production without validation.
- Do not delete the source archive immediately after a failed attempt.

