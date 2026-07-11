# STATUT : ARCHIVE HISTORIQUE
# NON APPLICABLE A LA VERSION ACTUELLE
#
# Documentation active :
# `backup-disaster-recovery/google-drive.md`

# Google Drive OAuth

This document defines the OAuth contract for the Google Drive connector used by LAWIM_V2.

## Fields

- Client ID
- Client Secret
- Refresh Token
- Access Token
- Token type
- Expiry state
- Scope list
- Refresh strategy

## Policy

- All OAuth values remain placeholders until the secure assistant phase
- No real secret value is requested during this release
- Automatic refresh is represented as a contract, not as an external login flow
- The test connection only validates the placeholder wiring and the internal routing path

## Status values

- `placeholder-configured`
- `activation-ready`
- `healthy`
- `watch`
- `blocked`

## Guardrails

- No Google Drive URL is embedded in OAuth payloads
- No real credential material is stored in business data
- OAuth status is surfaced in the admin center and monitoring view
