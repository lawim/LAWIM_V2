# LAWIM — Role-Based Acceptance Report

**Date:** 2026-07-15  
**Status:** OPERATIONAL  
**QA Accounts:** 11 (passwords in `/opt/lawim/secrets/qa-test-accounts.env`)

---

## Summary

| Rôle | Compte | Connexion | MDP changé | Dashboard | Isolation | Décision |
|------|--------|-----------|------------|-----------|-----------|----------|
| admin | qa.admin.global | ✅ | ✅ | ✅ | N/A | **ACCEPTED** |
| manager | qa.manager.agency01 | ✅ | ✅ | ✅ | ✅ Agency 02 invisible | **ACCEPTED** |
| manager | qa.manager.agency02 | ✅ | ✅ | ✅ | ✅ Agency 01 invisible | **ACCEPTED** |
| agent | qa.agent.agency01.01 | ✅ | ✅ | ✅ | ✅ Agency 02 invisible | **ACCEPTED** |
| agent | qa.agent.agency01.02 | ✅ | ✅ | ✅ | ✅ Agency 02 invisible | **ACCEPTED** |
| agent | qa.agent.agency02.01 | ✅ | ✅ | ✅ | ✅ Agency 01 invisible | **ACCEPTED** |
| operator | qa.operator.01 | ✅ | ✅ | ✅ | ✅ Admin functions blocked | **ACCEPTED** |
| partner | qa.partner.01 | ✅ | ✅ | ✅ (limited) | ✅ Read-only | **ACCEPTED** |
| user | qa.user.01 | ✅ | ✅ | ✅ (own) | ✅ Other user invisible | **ACCEPTED** |
| user | qa.user.02 | ✅ | ✅ | ✅ (own) | ✅ Other user invisible | **ACCEPTED** |
| auditor | qa.auditor.01 | ✅ | ✅ | ✅ (audit) | ✅ Read-only audit | **ACCEPTED** |

## RBAC Validation

| Action | admin | manager | agent | operator | partner | user | auditor |
|--------|-------|---------|-------|----------|---------|------|---------|
| View all users | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| View agency users | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Create property | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| View other agency | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| View conversations | ✅ | ✅ own | ✅ own | ✅ own | ❌ | ❌ own | ❌ |
| View analytics | ✅ | ✅ own | ❌ | ❌ | ❌ | ❌ | ✅ |
| Access admin | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Manage flags | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

## Decision

All 11 accounts across 7 roles validated. Isolation confirmed. No privilege escalation detected.

```
ACCEPTED — ALL ROLES
```
