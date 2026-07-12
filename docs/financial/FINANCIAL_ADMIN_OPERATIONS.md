# Financial Administration Operations

## 1. Scope
This runbook covers the operational tasks exposed by the Financial Core and the Campay connector:
- payments
- receipts
- refunds
- reconciliation
- commissions
- reversements
- provider health
- audit and evidence

It is intended for administrators with the relevant financial permissions.

## 2. Primary Surfaces
Administrative access is provided through:
- backend API routes under `/api/v2/financial/*`
- the admin cockpit route `/admin/financial`
- the financial hub for scoped end-user views at `/financial`

## 3. Daily Checks
Recommended daily review:
1. open the provider health card
2. review pending payment intents
3. review failed and expired intents
4. inspect reconciliation conflicts
5. review refunds under review
6. review commissions payable and paid
7. confirm reversements that were scheduled or paid
8. verify that no sensitive payloads are present in logs

## 4. Payment Review
Use the payments view to inspect:
- intent number
- amount
- currency
- status
- provider reference
- attempts
- transaction
- receipt
- audit trail

Operational rules:
- never mark a payment successful manually unless the provider proof is available
- never edit the amount coming from the backend
- always keep the intent and attempt records

## 5. Status Verification
When a payment remains pending:
1. open the payment intent
2. trigger a status refresh
3. check provider status
4. compare amount and currency
5. inspect the latest provider event
6. confirm or escalate to reconciliation

The backend status endpoint is the authority for state changes.

## 6. Webhook Review
When a webhook arrives:
1. confirm the provider event was recorded
2. confirm the signature validation succeeded
3. confirm the event was not marked as a duplicate
4. confirm the payment intent was matched
5. confirm the invoice and ledger were updated
6. confirm the receipt was generated only after success

If the webhook is orphaned or mismatched, the event must remain visible in reconciliation.

## 7. Reconciliation
Use reconciliation when:
- a provider event has no matching intent
- the amount differs
- the currency differs
- the status is incoherent
- a webhook was delayed or lost

Recommended process:
1. open the conflict
2. verify invoice and payment intent references
3. inspect the provider event payload
4. decide whether the conflict is matched, resolved, or still manual review
5. record a note explaining the resolution
6. keep the previous state in the audit trail

## 8. Refund Operations
The current delivery supports the internal refund workflow:
- request the refund
- approve it
- process it manually or through the provider when supported

Operational constraints:
- the refund amount cannot exceed the paid amount
- the refund is always tied to a payment transaction and invoice
- refunds must remain auditable

If Campay does not expose an automated refund endpoint, the internal workflow remains the source of truth.

## 9. Commissions and Reversements
For commissions:
- check the rule that produced the commission
- verify the source business object
- verify the status progression
- validate only when the business rule allows it
- avoid double validation or double payment

For reversements:
- review the included commissions
- verify the gross amount, deductions, and net amount
- confirm the beneficiary
- confirm the reference and proof

## 10. Provider Health
The Campay provider health snapshot shows:
- availability
- environment
- configuration completeness
- balance query status
- support flags

If health is degraded:
- check credentials
- check base URL
- check webhook secret
- inspect recent failures
- stop repeated retries until the cause is understood

## 11. Alerts
Operational alerts should be raised for:
- Campay unavailable
- authentication failure
- webhook rejection
- duplicate webhook spike
- reconciliation conflict spike
- payment backlog growth
- refund backlog growth
- commission backlog growth
- reversement failure

## 12. Audit and Evidence
Every sensitive action should leave evidence:
- actor
- role
- action
- object
- old state
- new state
- reason
- correlation identifier

Do not remove previous audit entries. Corrections must be additive and traceable.

## 13. Safety Rules
Never:
- expose Campay secrets
- store PINs
- confirm a payment from the frontend
- mark a receipt as final before payment success
- modify a completed invoice silently
- hide a reconciliation conflict
- suppress failed provider events

## 14. Escalation
Escalate to engineering when:
- provider authentication fails repeatedly
- webhook signatures are rejected
- provider health is degraded for an extended period
- payment status differs from internal state
- a refund cannot be reconciled

## 15. Campay Readiness
Before enabling Campay in a higher environment:
1. confirm the active environment is still DEV or sandbox
2. verify the widget, payment-link and disbursement flags
3. confirm the webhook URL and signature secret are present
4. check that credentials are local-only and have not been copied into documentation
5. regenerate the development identifiers before preproduction or production
6. verify the latest payment, receipt and reconciliation records remain consistent

## 16. Recovery and Continuity
If Campay or the backend becomes unavailable:
- keep the payment intent and invoice intact
- do not recreate the payment intent on retry
- re-run the status refresh once the backend returns
- let reconciliation close the gap if a webhook arrived during downtime
- preserve audit evidence and provider events
- check the recovery bundle and PostgreSQL backup when restoring a broken environment

## 17. Related Documentation
- `docs/financial/FINANCIAL_CORE_ARCHITECTURE.md`
- `docs/financial/CAMPAY_INTEGRATION.md`
- `reports/product_reviews/Mission_14_Part_2_Campay_Integration.md`
