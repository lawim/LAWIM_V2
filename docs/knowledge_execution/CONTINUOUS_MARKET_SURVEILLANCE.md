# CONTINUOUS MARKET SURVEILLANCE — Surveillance Continue du Marché LAWIM V5

**Component of:** Knowledge Execution Architecture (H1)
**Date:** 2026-07-15
**Status:** CANONICAL
**References:** WORKFLOW_EXTRACTION_COMPLETE.md §22 (Continuous Market Surveillance Rules), MATCHING_MODEL.md, PROGRESSIVE_SEARCH_EXPANSION.md, DECISION_ENGINE_ARCHITECTURE.md

---

## 1. Overview

Continuous Market Surveillance is the always-on monitoring subsystem of LAWIM. Even without active user interaction, the engine continuously monitors the property inventory for events that match active dossier criteria. When a relevant event is detected, the engine re-executes the search, scores new/updated properties, and triggers notification if the match threshold is met.

> **Core Principle (WORKFLOW §22):** Even without user interaction, LAWIM continuously monitors new publications, price decreases, returns to availability, new neighborhoods, new compatible listings.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CONTINUOUS MARKET SURVEILLANCE                        │
│                                                                         │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────────────────┐    │
│  │ Active        │   │ Event        │   │ Event Classifier         │    │
│  │ Dossier Pool  │──→│ Monitor      │──→│ (NEW_LISTING | PRICE_DROP│    │
│  │ (surveillance)│   │ (poll/pubsub)│   │  | STATUS_CHANGE | ...)  │    │
│  └──────────────┘   └──────────────┘   └──────────┬───────────────┘    │
│                                                    │                     │
│                                                    ▼                     │
│  ┌──────────────────────────────────────────────────────────────┐       │
│  │              Match Evaluator                                  │       │
│  │  Load dossier search query → Score property against it        │       │
│  └──────────────────────────┬───────────────────────────────────┘       │
│                             │                                           │
│                             ▼                                           │
│  ┌──────────────────────────────────────────────────────────────┐       │
│  │              Threshold Gate                                    │       │
│  │  score ≥ notification_threshold?                              │       │
│  │  type matches? location matches? budget matches?              │       │
│  └──────────────────────────┬───────────────────────────────────┘       │
│                             │                                           │
│                    ┌────────┴────────┐                                  │
│                    ▼                 ▼                                  │
│  ┌──────────────────────┐  ┌──────────────────────┐                     │
│  │  Notification Queue   │  │  Ignore (below       │                     │
│  │  (anti-noise applied) │  │  threshold)          │                     │
│  └──────────┬───────────┘  └──────────────────────┘                     │
│             │                                                           │
│             ▼                                                           │
│  ┌──────────────────────────────────────────────────────────────┐       │
│  │              NBA Engine                                         │     │
│  │  Decide: notify now? wait? aggregate? escalate?              │       │
│  └──────────────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Monitored Events

### 2.1 Event Catalog

From WORKFLOW §22 (What Is Monitored):

| Event Type | Trigger | Priority | Immediate Re-Score? |
|-----------|---------|----------|:-------------------:|
| **NEW_LISTING** | New property published | HIGH | Yes |
| **PRICE_DROP** | Property price decreased | HIGH | Yes |
| **PRICE_INCREASE** | Property price increased | LOW | No (unless dossier criteria change) |
| **STATUS_CHANGE_AVAILABLE** | Property returns to `Disponible` | HIGH | Yes |
| **STATUS_CHANGE_UNAVAILABLE** | Property becomes SOLD/RENTED/ARCHIVED | MEDIUM | No (remove from results) |
| **STATUS_CHANGE_RESERVED** | Property becomes `Réservé` | MEDIUM | Yes (update availability score) |
| **PROPERTY_MODIFIED** | Property details updated (surface, rooms, photos) | MEDIUM | Yes |
| **NEIGHBORHOOD_NEW_LISTING** | New property in requested neighborhood | HIGH | Yes |
| **HOLDER_RESPONSE** | Holder responds after silence | MEDIUM | Yes (update holder reliability) |
| **DOCUMENT_ADDED** | Title/document added to property | LOW | Yes (update document score) |

### 2.2 Event Sources

| Source | Mechanism | Frequency |
|--------|-----------|-----------|
| Property CRUD (create/update) | Database trigger → event bus | Real-time |
| Price update | Agent or system price change | Real-time |
| Status transition | Workflow state machine | Real-time |
| Periodic inventory scan | Scheduled job | Every 6 hours (low-priority) |
| Holder activity | Holder response or action | Real-time |
| Data quality improvement | System or agent enrichment | As triggered |

---

## 3. Dossier Surveillance Lifecycle

### 3.1 States

```
INACTIVE (not monitored)
    │
    ├──→ ACTIVE (monitoring enabled)
    │       │
    │       ├──→ NEW_MATCH (property found, pending notification)
    │       ├──→ NOTIFIED (user has been notified)
    │       ├──→ FOLLOW_UP (user hasn't responded to notification)
    │       └──→ DISMISSED (user rejected or dossier closed)
    │
    └──→ ARCHIVED (dossier closed, monitoring stopped)
```

### 3.2 State Transitions

| From | To | Trigger |
|------|----|---------|
| INACTIVE | ACTIVE | User opts in, dossier created with surveillance consent |
| ACTIVE | NEW_MATCH | Property event triggers score ≥ notification threshold |
| NEW_MATCH | NOTIFIED | Notification sent to user |
| NOTIFIED | FOLLOW_UP | User hasn't responded within notification SLA |
| FOLLOW_UP | ACTIVE | User responds (acknowledges, requests details, or rejects) |
| ACTIVE | DISMISSED | User explicitly dismisses dossier or rejects all |
| ACTIVE | ARCHIVED | Dossier closed, 90 days inactivity (PROP-005) |
| DISMISSED | ARCHIVED | Dossier closed |
| ARCHIVED | ACTIVE | Dossier reopened (WORKFLOW §3: reopening conditions) |

### 3.3 Surveillance Activation Criteria

| Condition | Action |
|-----------|--------|
| Initial search returns 0 results | Offer surveillance activation (Level 6 expansion) |
| User expresses frustration with inventory | Proactive surveillance suggestion |
| User explicitly asks to be notified | Immediate activation |
| All expansion levels exhausted | Automatic surveillance activation |
| Rematching finds no new results for 2 cycles | Surveillance remains active, reduce notification frequency |
| Dossier inactive for > 7 days | Automatic follow-up: "Still looking?" |

---

## 4. Notification Criteria

### 4.1 Match Threshold for Notification

| Event Type | Minimum Score to Notify | Notes |
|-----------|:----------------------:|-------|
| New listing | ≥ 60 | Standard notification threshold |
| Price drop (≥ 10%) | ≥ 55 | Reduce threshold for significant price drops |
| Return to availability | ≥ 60 | Previously unavailable, now available |
| New in neighborhood | ≥ 65 | Higher bar — user specified exact neighborhood |
| Property modification | ≥ 60 | Only if modification affects scoring positively |

### 4.2 Notification Frequency Rules

| User Preference | Max Notifications/Day | Cooldown Between Same Property |
|----------------|:--------------------:|:------------------------------:|
| REAL_TIME | 5 | 24h (no repeat for same property) |
| DAILY_DIGEST | 1 (daily summary) | N/A (batched) |
| WEEKLY_DIGEST | 1 (weekly summary) | N/A (batched) |
| ONLY_IMPORTANT | 2 | 48h |
| NONE | 0 | N/A |

Default: `DAILY_DIGEST` for new users, `REAL_TIME` for HOT/WARM leads.

### 4.3 Notification Content

```typescript
interface SurveillanceNotification {
  id: string;
  dossierId: string;
  userId: string;
  type: "NEW_MATCH" | "PRICE_DROP" | "BACK_AVAILABLE" | "DIGEST";

  // Core content
  title: string;         // "New apartment matching your search"
  body: string;          // "3-bedroom apartment in Bonanjo, Douala — XAF 45M"
  properties: ScoredProperty[];
  matchCount: number;    // total new matches since last notification
  bestScore: number;

  // Action buttons
  actions: {
    view: string;        // "View properties"
    dismiss: string;     // "Not interested"
    adjust: string;      // "Adjust my criteria"
    contact: string;     // "Contact holder"
    pause: string;       // "Pause alerts (7 days)"
  };

  // Anti-noise metadata
  isUrgent: boolean;     // true if user is HOT or property is exceptional
  priority: "LOW" | "NORMAL" | "HIGH";
  channel: "WHATSAPP" | "TELEGRAM" | "IN_APP" | "DIGEST";
}
```

### 4.4 Notification Channel Selection

| User Segment | Primary Channel | Digest Channel |
|-------------|----------------|----------------|
| HOT lead | WhatsApp (immediate) | N/A |
| WARM lead | WhatsApp | Daily digest via WhatsApp |
| COLD lead | WhatsApp | Weekly digest via Telegram |
| LOW lead | Telegram | Weekly digest |
| Premium user | WhatsApp + In-App | Real-time |
| Agent | WhatsApp + Dashboard | Daily digest |

---

## 5. Price Change Monitoring

### 5.1 Price Decrease Detection

| Threshold | Action |
|-----------|--------|
| ≥ 10% decrease | Re-score property against all matching dossiers. Notify if score ≥ 55. |
| ≥ 20% decrease | High priority. Immediate notification. Remove from blacklist (MATCH-018). |
| ≥ 30% decrease | Critical. Immediate notification + agent alert. |
| < 10% decrease | Log only. Notify only if user preference = REAL_TIME. |

### 5.2 Price Increase Detection

| Scenario | Action |
|----------|--------|
| Price increase on non-matched property | Ignore (no impact on existing matches) |
| Price increase on matched (scored 60-79) property | Re-score. If drops below 60, remove from results |
| Price increase on matched (scored ≥ 80) property | Re-score. If still ≥ 60, keep with updated score |
| Price increase on blacklisted property | No action (already excluded) |

### 5.3 Price Drop Blacklist Exception (MATCH-018)

```
Blacklisted Property
    │
    ├── Price drop ≥ 10%
    │       ↓
    │   Re-evaluate against dossier criteria
    │       ↓
    │   Score ≥ notification threshold?
    │       ↓
    │   YES → Remove from blacklist, notify user with explanation:
    │          "Property X has dropped in price from XAF {old} to XAF {new}. You may want to reconsider."
    │
    └── Price drop < 10%
            ↓
        No action (remains blacklisted)
```

---

## 6. Availability Change Monitoring

### 6.1 Status Transitions

| From | To | Impact on Surveillance |
|------|----|----------------------|
| SOLD/RENTED/ARCHIVED | Disponible | **Notify** — property is back on market |
| Réservé | Disponible | **Notify** — deal fell through, availability restored |
| Sous négociation | Disponible | **Notify** — negotiation failed |
| Indisponible | Disponible | **Notify** — owner returned to market |
| Disponible | Réservé | Update score (availability penalty), no notification |
| Disponible | SOLD/RENTED | Remove from results, no notification (expected outcome) |
| Disponible | Suspendu | Remove from results, no notification |
| Any | Archivé | Remove from results, no notification |

### 6.2 Holder Silence Monitoring (WORKFLOW §22)

```
Holder unresponsive → Property marked "à confirmer"
    │
    ├── First reminder (J+1)
    ├── Second reminder (J+3)
    ├── Last reminder (J+7)
    │
    └── Property marked inactive → Rematching for demandeur
```

---

## 7. Search Re-Execution Triggers

### 7.1 Trigger Matrix

| Trigger | Action | Dossier Scope | Priority |
|---------|--------|---------------|----------|
| New listing published | Score against all active dossiers | All dossiers in property's city | HIGH |
| Price drop ≥ 10% | Re-score property against matching dossiers | Dossiers with budget tolerance overlap | HIGH |
| Status → Disponible | Re-score property against matching dossiers | All dossiers that previously excluded it | HIGH |
| Property modified | Re-score property | Dossiers that had it in results | MEDIUM |
| Dossier criteria changed | Re-execute full search | Single dossier | HIGH |
| J+7 rematch timer | Re-execute full search | Single dossier | MEDIUM |
| J+30 follow-up | Re-execute full search | Single dossier | LOW |
| New neighborhood added to inventory | Score new neighborhood properties | Dossiers with location expansion | LOW |

### 7.2 Re-Execution SLA

| Trigger | Processing SLA |
|---------|:--------------:|
| New listing | ≤ 1 minute |
| Price drop ≥ 10% | ≤ 5 minutes |
| Price drop ≥ 20% | ≤ 1 minute |
| Status → Disponible | ≤ 5 minutes |
| Dossier criteria change | ≤ 30 seconds |
| J+7 rematch | ≤ 1 hour (batch window) |

---

## 8. Anti-Noise Rules

### 8.1 Notification Fatigue Prevention

| Rule | Implementation |
|------|---------------|
| **Same property cooldown** | Never notify same property twice within 24h unless price drop ≥ 15% |
| **Daily cap** | Max notifications per user per day based on preference (Real-time: 5, Digest: 1) |
| **Score floor** | Never notify for score < 55 (exceptions: price drop ≥ 20%) |
| **Batch similar properties** | If 3+ properties match in same batch, send as digest, not individual |
| **Progressive cooldown** | If user ignores 3+ consecutive notifications, auto-downgrade to DAILY_DIGEST |
| **Silent hours** | No notifications 22:00-07:00 (user timezone) unless score ≥ 85 |
| **Aggregation rule** | Same property type + same neighborhood = single notification max |
| **Diversity rule** | Max 3 properties per notification (top 3 by score) |
| **User dismissal signal** | If user dismisses 5+ consecutive notifications → pause surveillance, ask user |

### 8.2 Cooldown State Machine

```
For each (dossier_id, property_id) pair:

NOT_NOTIFIED
    │
    ├── Property matches → NOTIFIED
    │
    NOTIFIED
    │
    ├── 24h passed → READY_FOR_RENOTIFICATION
    ├── Price drop ≥ 15% → READY_FOR_RENOTIFICATION (immediate)
    ├── User dismissed → DISMISSED (skip cooldown)
    └── Property became unavailable → REMOVE_FROM_TRACKING
    │
    READY_FOR_RENOTIFICATION
    │
    ├── Re-score → if still ≥ threshold → NOTIFIED
    └── If below threshold → NOTIFIED_WITH_WARNING
```

### 8.3 User Feedback Signals

| User Action | System Interpretation | Notification Adjustment |
|-------------|----------------------|------------------------|
| Clicks notification | Interested | Maintain or increase frequency |
| Requests property details | Very interested | Upgrade to REAL_TIME |
| Dismisses notification | Not interested | Reduce frequency for similar properties |
| Ignores 3+ notifications | Low engagement | Downgrade to DAILY_DIGEST |
| Unsubscribes from alerts | No interest | Stop all surveillance, archive |
| Reopens dossier | Renewed interest | Reset to default frequency |

---

## 9. Integration with NBA Engine

### 9.1 NBA Actions from Surveillance Events

| Surveillance Event | NBA | Description |
|-------------------|-----|-------------|
| New property match (score ≥ 60) | `present_property` | Send property to user with details |
| New property match (score ≥ 80) | `present_property_urgent` | High-priority presentation |
| Price drop ≥ 10% on matched property | `notify_price_drop` | "Property X has decreased in price" |
| Price drop ≥ 20% on previously rejected | `reconsider_property` | "You may want to reconsider X" |
| Status → Disponible | `notify_availability` | "Property X is available again" |
| No new matches for J+7 | `follow_up_surveillance` | "Still searching? I'm monitoring for you" |
| J+30 with no user activity | `re_engagement` | "Any updates on your search?" |
| Holder responds | `contact_holder_outcome` | Update on holder response |
| Multiple new matches (batch) | `digest_notification` | Weekly/daily summary |

### 9.2 Decision Engine Priority for Surveillance

From WORKFLOW §4, Ch88:

| Priority | Surveillance NBA |
|----------|-----------------|
| 1-2 | (reserved for incoherence/critical field — not surveillance) |
| 3 | **Matching** (surveillance re-execution) |
| 4 | **Present property** (new match found) |
| 5 | (contact holder — not surveillance-initiated) |
| 6 | (organize visit — follow-up from notification) |
| 7 | **Follow up** (no results, re-engagement) |
| 8 | **Notifications** (price drop, availability) |
| 9 | (dossier optimization — not surveillance) |

### 9.3 NBA Resolver Integration

```
SurveillanceEvent
    │
    ├──→ MatchEvaluator.score(dossier, property)
    │
    ├── score ≥ threshold?
    │       │
    │       ├── yes → NBA Resolver
    │       │           │
    │       │           ├── User preference = REAL_TIME
    │       │           │       ↓
    │       │           │   NBA = PRESENT_PROPERTY (immediate)
    │       │           │
    │       │           ├── User preference = DAILY_DIGEST
    │       │           │       ↓
    │       │           │   NBA = AGGREGATE_FOR_DIGEST
    │       │           │
    │       │           └── User preference = WEEKLY_DIGEST
    │       │                   ↓
    │       │               NBA = AGGREGATE_FOR_WEEKLY
    │       │
    │       └── no → NBA = NO_ACTION (continue surveillance)
    │
    └──→ Audit trail written
```

---

## 10. User Preference Management

### 10.1 Surveillance Preferences

```typescript
interface SurveillancePreferences {
  dossierId: string;

  // Notification frequency
  notificationFrequency: "REAL_TIME" | "DAILY_DIGEST" | "WEEKLY_DIGEST" | "ONLY_IMPORTANT" | "NONE";
  digestDay: "MONDAY" | "TUESDAY" | ... | "SUNDAY";         // for weekly digest
  digestTime: string;                                         // HH:mm in user timezone

  // Price alert thresholds
  priceDropThreshold: number;     // default: 10% (0-100)
  notifyOnPriceIncrease: boolean; // default: false

  // Availability alerts
  notifyOnBackAvailable: boolean; // default: true
  notifyOnNewListing: boolean;    // default: true

  // Quiet hours
  quietHoursStart: string | null; // HH:mm
  quietHoursEnd: string | null;   // HH:mm
  timezone: string;               // IANA timezone

  // Property type specificity
  strictTypeOnly: boolean;        // true = only exact property type
  allowTypeFamilyExpansion: boolean; // true = allow family matches

  // Pause
  pausedUntil: string | null;     // ISO date, null = active
  pauseReason: string | null;
}
```

### 10.2 Default Preferences by Lead Class

| Lead Class | Default Frequency | Price Drop | Back Available | New Listing |
|------------|:-----------------:|:----------:|:--------------:|:-----------:|
| HOT | REAL_TIME | 10% | Yes | Yes |
| WARM | REAL_TIME | 10% | Yes | Yes |
| COLD | DAILY_DIGEST | 15% | Yes | Yes |
| LOW | WEEKLY_DIGEST | 20% | No | No |
| SPAM | NONE | N/A | N/A | N/A |

### 10.3 Preference Modification Commands

| User Says | System Interprets | Action |
|-----------|-------------------|--------|
| "Notify me immediately" | Set REAL_TIME | Update preferences |
| "Send me daily updates" | Set DAILY_DIGEST | Update preferences |
| "Only tell me about price drops" | Set notifyOnNewListing=false | Update preferences |
| "Pause alerts for 2 weeks" | Set pausedUntil = now+14d | Pause surveillance |
| "Stop notifying me" | Set NONE | Disable notifications |
| "I'm no longer looking" | Close dossier | Archive dossier, stop surveillance |

---

## 11. Market Intelligence Integration

From WORKFLOW §22 (Market Intelligence Indicators):

### 11.1 Market Tension Index

| Value | Meaning | Engine Adaptation |
|:-----:|---------|-----------------|
| ≥ 80% | Very tense market (rare properties) | Lower notification threshold to 55, notify faster |
| 50-79% | Moderate tension | Standard thresholds |
| < 50% | Relaxed market (many available) | Raise notification threshold to 65, reduce frequency |

The Market Tension Index is computed per `City × Neighborhood × PropertyType × Operation` combination.

### 11.2 Surveillance Adaptation Based on Market

| Market Condition | Notification Behavior |
|-----------------|---------------------|
| High tension, scarce inventory | Notify every qualifying new listing immediately. Lower threshold. |
| Low tension, abundant inventory | Batch notifications, only top 20% by score. Raise threshold. |
| Seasonal peak (high demand) | Prioritize freshness, notify within minutes |
| Seasonal low (low demand) | Daily digest, focus on price drops and incentives |

---

## 12. Audit Trail

### 12.1 Surveillance Audit Record

```typescript
interface SurveillanceAuditRecord {
  id: string;
  dossierId: string;
  userId: string;
  propertyId: string | null;
  eventType: SurveillanceEventType;
  timestamp: string;

  // Match evaluation
  score: number | null;
  thresholdReached: boolean;
  thresholdValue: number;

  // Notification
  notificationSent: boolean;
  notificationChannel: string | null;
  notificationId: string | null;

  // User response
  userResponse: "VIEWED" | "REQUESTED" | "DISMISSED" | "IGNORED" | null;
  responseTimestamp: string | null;

  // Anti-noise
  cooldownActive: boolean;
  dailyQuotaRemaining: number;
}

type SurveillanceEventType =
  | "NEW_LISTING_EVALUATED"
  | "PRICE_DROP_EVALUATED"
  | "STATUS_CHANGE_EVALUATED"
  | "PROPERTY_MODIFIED_EVALUATED"
  | "SURVEILLANCE_ACTIVATED"
  | "SURVEILLANCE_DEACTIVATED"
  | "SCHEDULED_REMATCH"
  | "FOLLOW_UP_SENT"
  | "DIGEST_SENT";
```

### 12.2 Audit Retention

| Audit Type | Retention |
|-----------|-----------|
| Per-event evaluation | 90 days |
| Notification sent | Dossier lifetime + 3 years |
| User response | Dossier lifetime + 3 years |
| Preference changes | Dossier lifetime |

---

## 13. Edge Cases & Error Handling

| Scenario | Detection | Handling |
|----------|-----------|----------|
| Property database unavailable | Connection error | Retry in 15 min, log error, no notification |
| Event flood (bulk import of 1000 listings) | Burst detection | Batch process, rate-limit to 100/min, digest only |
| User changes criteria while surveillance active | Dossier update event | Re-score all tracked properties with new criteria |
| Same property matches multiple dossiers for same user | Deduplication check | Single notification per user, not per dossier |
| Property removed from inventory | Delete/Cascade event | Remove from all surveillance queues, no notification |
| User deletes account | Account deletion | Immediate stop all surveillance, anonymize audit |
| Price decreases below blacklist threshold | Cross-reference check | Remove from blacklist, re-evaluate (MATCH-018) |
| Multiple price changes in 24h | Volatility detection | Only notify on final price if total change ≥ 10% |

---

## 14. Gold Knowledge Register — Continuous Market Surveillance

| ID (CMS-) | Concept | Description | Source | Confidence |
|-----------|---------|-------------|--------|------------|
| CMS-001 | What Is Monitored | New publications, price decreases, returns to availability, new neighborhoods, new compatible listings, statuses, dossiers, documents, prices, holder responses | WORKFLOW §22 | HIGH |
| CMS-002 | Market Intelligence Indicators | Average sale time, rental time, time to first visit, most requested neighborhoods, most searched types, seasonality, Market Tension Index | WORKFLOW §22 | HIGH |
| CMS-003 | Market Tension Index | Per City×Neighborhood×Type×Operation. 95%=very tense, 25%=relaxed | WORKFLOW §22 | HIGH |
| CMS-004 | Surveillance Continuity | Continuous as long as dossier is active. Significant change = new matching | WORKFLOW §22 | HIGH |
| CMS-005 | Zero-Result Follow-up | "I am actively pursuing your search. Since our last exchange, no property exactly matches your criteria. Would you like to maintain your search as-is or explore some alternatives?" | WORKFLOW §22 | VERY HIGH |
| CMS-006 | Holder Silence Workflow | First→Second→Last reminder → Marked inactive → Rematching | WORKFLOW §22 | HIGH |
| CMS-007 | Refused Property Exceptions | Price decrease ≥10%, major modification, changed need, explicit request | MATCH-018 | VERY HIGH |
| CMS-008 | Rematching Triggers | New listing, price drop, availability change, criteria change, J+7 timer | MATCHING_MODEL §13 | VERY HIGH |

---

*Canonical document — Continuous Market Surveillance for LAWIM V5. Defines the always-on monitoring subsystem, event handling, notification rules, anti-noise policies, and NBA integration. Fully aligned with Heritage Gold WORKFLOW_EXTRACTION_COMPLETE §22 and MATCHING_MODEL.*
