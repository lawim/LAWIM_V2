# Cockpit

STATUT : CIBLE DOCUMENTAIRE ACTIVE

## Goal

The Cockpit is the operator surface for backup status, history, schedules, alerts, and restore actions.
It must show the backend state, not a simulated state.

## Main views

- Overview
- History
- Supports
- Schedules
- Restorations
- Alerts
- Configuration
- Logs

## Permission model

- Super admin: configuration and critical actions
- Technical admin: support tests and operational actions
- Auditor: read-only views and reports
- Standard user: no access

## Safety rules

- Never show secrets.
- Never accept shell commands from the browser.
- Never let the frontend invent the state.
- Never allow destructive restore to production by default.

## Current state

| Aspect | Target | Implemented | Deployed | Tested | Validated |
|---|---|---|---|---|---|
| BDR cockpit page | Yes | Not yet | No | No | No |
| Real-time updates | Yes | Not yet | No | No | No |
| History pagination | Yes | Not yet | No | No | No |
| Alert center | Yes | Not yet | No | No | No |

