# Program J — Analytics, Dashboards and Recalculation

**Document ID:** LAWIM-PROGRAM-J-ANALYTICS-V1
**Status:** CANONICAL
**Date:** 2026-07-15

---

## 1. Metric Catalog

Central registry of 25+ metrics across 11 domains:

| Domain | Example Metrics |
|--------|----------------|
| CHANNEL | CLICKS_TOTAL, CLICKS_UNIQUE, REDIRECTS_TOTAL, BOT_EVENTS_TOTAL |
| CAMPAIGN | CAMPAIGNS_TOTAL |
| PUBLICATION | PUBLICATIONS_TOTAL |
| CONVERSATION | CONVERSATIONS_STARTED, AVERAGE_RESPONSE_TIME, HUMAN_HANDOVER_RATE |
| QUALIFICATION | QUALIFICATIONS_STARTED, QUALIFICATIONS_COMPLETED |
| MATCHING | MATCHINGS_CREATED |
| VISIT | VISITS_REQUESTED, VISITS_COMPLETED |
| TRANSACTION | TRANSACTIONS_STARTED, TRANSACTIONS_COMPLETED |
| PAYMENT | PAYMENTS_INITIATED, PAYMENTS_CONFIRMED, REVENUE_TOTAL |
| CONVERSION | CONVERSIONS_TOTAL, CONVERSION_RATE, AVERAGE_CONVERSION_TIME, ATTRIBUTION_COVERAGE_RATE |
| GENERAL | DUPLICATE_RATE |

Each metric has: code, name, description, domain, unit, aggregation_type, formula, formula_version, status.

## 2. Dimensions

34 dimensions available: channel, provider, campaign, publication, tracking_code, publication_actor, actor_role_at_publication, current_actor_role, organization, agency, team, conversation_actor, exchange_type, business_intent, content_type, exchange_result, qualification_type, property_type, service, matching, visit, transaction, payment, conversion_type, language, country, city, lawim_zone, year, quarter, month, week, day, hour.

## 3. Analytics Engine

Provides deterministic, versioned calculations:
- `calculate_metric(code, events, filters)` — single metric
- `calculate_metrics(codes, events, filters)` — batch
- `group_by(code, events, dimension, filters)` — breakdown
- `compare_periods(code, events, p1, p2)` — time comparison
- `rebuild_aggregates(events, mode)` — recalculation
- `validate_aggregates(aggregates)` — consistency checks
- `explain_metric(code)` — metric definition

## 4. Data Quality

Checks: orphan events (no actor/channel), duplicate conversions, missing campaign references. Statuses: VALID, WARNING, INCOMPLETE, INCONSISTENT, STALE, REBUILD_REQUIRED.

## 5. Recalculation

Modes: FULL_REBUILD, INCREMENTAL, TARGETED, VALIDATION_ONLY. Each run preserves: run_id, mode, scope, period, metric_codes, formula_versions, timestamps, event/aggregate counts, warnings, errors.

## 6. Dashboards

### Administration
Total campaigns, publications, clicks, unique clicks, bots, redirects, conversations, leads, conversions, payments, revenue, top channels, top actors, data quality, last recalculation.

### Reporting
Daily/weekly/monthly/yearly comparisons, campaign/publication/channel/actor/conversion/revenue evolution. Filters: territory, language, property type.

### Matching
Origin by channel, campaign, publication, actor, city, zone, property type, language. Pass-through rates: matching→visit, matching→conversion.

### Campay
Payments by channel, campaign, publication, actor, agency, service, period, status. Revenue, reconciliation rate, unattributed payments, conversions without payment.

### Continuous Learning (descriptive only)
Best campaigns, hours, days, cities, neighborhoods, property types, channels, actors, publications, languages. Abandon points, handovers, conversion rates. No automatic recommendations.

## 7. Feature Flags

| Flag | Default | Purpose |
|------|---------|---------|
| marketing_analytics_enabled | false | Metric catalog and calculation APIs |
| analytics_dashboards_enabled | false | Dashboard view APIs |
| analytics_recalculation_enabled | false | Recalculation trigger APIs |

## 8. Privacy

- Phone numbers masked in all views
- No full conversation content in statistics
- Aggregated views respect minimum thresholds
- Filters scoped by agency/organization permissions
- No raw provider identifiers exposed
- Individual data access restricted

## 9. Known Limitations

- Analytics engine calculates in-memory (no dedicated aggregate table yet)
- Data quality checks are rule-based, not ML-based
- Continuous Learning dashboard is descriptive only (no ML recommendations)
- Dashboard integration requires existing frontend to consume new API contracts
- ACTOR domain has no metrics currently defined
- No MIN/MAX/DURATION aggregation types currently used
