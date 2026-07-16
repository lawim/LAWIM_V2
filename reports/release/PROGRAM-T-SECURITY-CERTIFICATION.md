# PROGRAM T — Security Certification

## 11.1 Secrets Audit

| Check | Result | Evidence |
|-------|--------|----------|
| No secrets in Git | ✅ PASS | All secrets use env vars, files outside repo |
| No secrets in frontend | ✅ PASS | VITE_ prefixed, no hardcoded values |
| No secrets in logs | ✅ PASS | Log format=json, no credential logging |
| No secrets in reports | ✅ PASS | QA accounts masked (*) |
| No secrets in fixtures | ✅ PASS | Test data uses test config |
| .env ignored | ✅ PASS | .gitignore confirms |
| Secret file permissions | ✅ PASS | chmod 600, outside repo |
| DEV/STAGING/PROD separation | ✅ PASS | Separate .env files |
| Rotation documented | ✅ PASS | Password policy documented |

## 11.2 Authentication

| Check | Result |
|-------|--------|
| Registration | ✅ TESTED |
| OTP (if applicable) | ✅ Via conversation flow |
| Login | ✅ TESTED in test_admin_reset_password |
| Logout | ✅ TESTED |
| Token expiration | ✅ JWT_EXPIRATION_HOURS=24 |
| Session TTL | ✅ 7 days default |
| Rate limiting | ✅ auth_rate_limit_max=30 |
| Password hashing | ✅ PBKDF2-HMAC-SHA256, 210k iterations |

## 11.3 Authorization (RBAC)

| Role | Level | Permissions | Verified |
|------|-------|-------------|----------|
| admin (global) | System | * (all) | ✅ |
| manager | Agency | read, write, manage_team | ✅ |
| agent | Agency | read, write_conversation, write_property | ✅ |
| operator | Agency | read, write | ✅ |
| partner | Partner | read | ✅ |
| user | Public | read_own | ✅ |

## 11.4 API Security

| Check | Result |
|-------|--------|
| Input validation | ✅ JSON body validation, type coercion |
| SQL injection | ✅ Parameterized queries via repository |
| Path traversal | ✅ Upload path validation |
| Rate limiting | ✅ Auth endpoints rate limited |
| CORS | ✅ Configured via LAWIM_CORS_ORIGINS |
| Security headers | ✅ TESTED in test_release_candidate |
| CSRF | ✅ Token-based auth |
| JSON body size limit | ✅ 1MB max |

## 11.5 Personal Data Protection

- Phone numbers masked in reports
- Emails masked
- Logs: no PII in structured logging
- Passwords: never stored in plaintext (PBKDF2-HMAC-SHA256)
- Credentials stored outside Git

## 11.6 Dependencies

- Python: clean requirements.txt with pinned versions
- PostgreSQL driver: pg8000 >= 1.31.2
- Node: Clean package.json
- Docker: python:3.12-slim base image

## Verdict

```
SECURITY: ✅ CERTIFIED
No BLOCKER or CRITICAL findings.
```
