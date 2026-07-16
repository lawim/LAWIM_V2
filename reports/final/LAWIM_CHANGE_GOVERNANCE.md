# LAWIM — CHANGE GOVERNANCE POLICY

**Version:** 2.0.0  
**Status:** FROZEN — MAINTENANCE MODE

---

## Change Categories

| Category | Description | Approval | Tests Required | Tag Required |
|----------|-------------|----------|---------------|-------------|
| BUGFIX | Functional defect fix | Technical lead | Yes | Yes |
| SECURITY_FIX | Vulnerability patch | Security lead | Yes | Yes |
| OPERATIONS_FIX | Deployment/config fix | Ops lead | Recommended | Yes |
| PERFORMANCE_FIX | Optimization | Tech lead | Yes | Yes |
| DOCUMENTATION | Non-functional doc update | Any maintainer | No | No |
| MINOR_RELEASE | Backward-compatible addition | Architecture board | Yes | Yes |
| MAJOR_RELEASE | Breaking change | Full governance | Yes | Yes |
| MARKETPLACE_EXTENSION | New extension | Ecosystem lead | Yes | Yes |
| CONNECTOR_UPDATE | Connector update | Integration lead | Yes | Yes |

## Rules

1. No new alphabetic programs (T, U, etc.) without full governance review
2. No new features on the certified baseline — branch first, merge after certification
3. All fixes require tests
4. All releases require a signed tag
5. Rollback plan required for any behavioral change
6. Progressive activation via feature flags
7. Human validation required for security, financial, and legal changes
8. All changes must maintain backward compatibility with existing data

## Baseline

The certified head `9a9f84a7` and all 13 program tags are the immutable reference points. No destructive changes to this history.
