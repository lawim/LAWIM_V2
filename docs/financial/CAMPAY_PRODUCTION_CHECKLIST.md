# Campay Production Checklist

This checklist is the operational gate between DEV validation and production activation.

## 1. Environment Gate
- [ ] Confirm the current mission evidence is limited to DEV or sandbox validation.
- [ ] Confirm the production flag is still disabled in LAWIM.
- [ ] Confirm the backend still treats LAWIM as the source of truth.

## 2. Secret Replacement
- [ ] Replace the local development app credentials with fresh production credentials.
- [ ] Regenerate the webhook secret before production cutover.
- [ ] Rotate any token, username/password, or related provider credential used during DEV validation.
- [ ] Confirm no secret was copied into documentation, logs, or commits.

## 3. URL and HTTPS Gate
- [ ] Confirm the public base URL uses HTTPS.
- [ ] Confirm the webhook endpoint is reachable from Campay.
- [ ] Confirm the reverse proxy and certificate chain are valid.
- [ ] Confirm the redirect URL matches the production domain.

## 4. Feature Flags
- [ ] Enable only the flags that are required for the target environment.
- [ ] Keep `campay_widget_enabled`, `campay_payment_links_enabled`, and `campay_disbursement_enabled` off until each capability is revalidated.
- [ ] Set `campay_dev_mode` and `campay_prod_mode` so that only one mode is active.

## 5. Backups and DRF
- [ ] Verify the latest PostgreSQL backup completed successfully.
- [ ] Verify the latest Recovery Bundle includes the financial tables and documents.
- [ ] Verify the secret inventory records the Campay secrets as metadata only.
- [ ] Verify rollback instructions were updated after the last change.

## 6. Functional Recette
- [ ] Create a small production test invoice.
- [ ] Initiate the payment from LAWIM backend only.
- [ ] Confirm the payment via webhook or provider status.
- [ ] Verify the invoice transitions to paid.
- [ ] Verify the receipt is generated only after confirmation.
- [ ] Verify reconciliation and audit entries are present.

## 7. Rollback
- [ ] Confirm the previous release is still available.
- [ ] Confirm migration rollback is documented or safely skipped.
- [ ] Confirm active payments will survive a rollback.
- [ ] Confirm Campay can be disabled without losing payment evidence.

## 8. Final Decision
- [ ] Only promote to production if the payment path, webhook validation, reconciliation, audit, and backup checks all pass.
- [ ] If any step fails, keep Campay production disabled and document the reserve.
