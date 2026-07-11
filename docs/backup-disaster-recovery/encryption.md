# Encryption

STATUT : CIBLE DOCUMENTAIRE ACTIVE

## Goal

Backups are encrypted before they leave the server.
Key material is never stored in Git and is never displayed by the Cockpit.

## Required properties

- centralized encryption service
- future key rotation support
- decryption only in controlled restore flows
- secret source limited to environment or approved secret manager

## Current state

| Aspect | Target | Implemented | Deployed | Tested | Validated |
|---|---|---|---|---|---|
| Encryption service | Yes | Partial legacy script support | No confirmed canonical service | No | No |
| Key handling | Yes | Environment-only expectation | No confirmed runtime binding | No | No |
| Rotation support | Yes | Not yet | No | No | No |

## Safety rules

- Do not commit keys.
- Do not print keys.
- Do not derive keys in the frontend.
- Do not use an unverified path or command from the browser.

