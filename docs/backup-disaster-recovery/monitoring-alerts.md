# Monitoring and Alerts

STATUT : CIBLE DOCUMENTAIRE ACTIVE

## Goal

Operators must see backup health, destination health, errors, and restore evidence without opening raw logs first.

## Metrics

- backup count
- average duration
- max duration
- failure count
- backup size
- available disk space
- upload time
- age of last validated copy

## Alerts

- Google Drive unavailable
- local disk missing
- external disk missing
- checksum invalid
- encryption failure
- restore test failed
- retention skipped
- concurrency detected

## Status model

- INFO
- WARNING
- CRITICAL

## Safety rules

- No token appears in the alert body.
- No secret appears in the alert body.
- Technical details stay in logs or detail panels.

