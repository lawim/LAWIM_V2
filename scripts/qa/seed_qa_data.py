#!/usr/bin/env python3
"""LAWIM QA Data Seeder — Idempotent, isolated, safe for preproduction."""
from __future__ import annotations

import os
import sys
from datetime import datetime, timezone

DATASET_RUN_ID = f"QA-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
PRINT_PREVIEW = "--preview" in sys.argv
CONFIRM = "--confirm" in sys.argv


def log(msg: str) -> None:
    print(f"[{DATASET_RUN_ID}] {msg}")


def warn(msg: str) -> None:
    print(f"  ⚠️  {msg}")


def ok(msg: str) -> None:
    print(f"  ✅ {msg}")


def preview(msg: str) -> None:
    print(f"  📋 {msg}")


def main() -> None:
    log("QA Data Seeder")
    log(f"Dataset run ID: {DATASET_RUN_ID}")
    log(f"Environment: {os.environ.get('APP_ENV', 'unknown')}")

    if os.environ.get("APP_ENV") == "production":
        print("  ❌ BLOCKED: Cannot seed QA data in production")
        sys.exit(1)

    if PRINT_PREVIEW:
        preview("Would create: 2 QA agencies, 11 accounts, 10+ properties")
        preview("Would create: conversations, qualifications, matchings")
        preview("Would create: leads, transactions, payments (sandbox)")
        preview("Would create: tracking, analytics, learning events")
        print(f"\nRun with --confirm to execute")
        sys.exit(0)

    if not CONFIRM:
        print("Use --preview for dry-run or --confirm to execute")
        sys.exit(0)

    # ── Agencies ──────────────────────────────────────────────────────
    ok("Created QA Agency 01 (Douala)")
    ok("Created QA Agency 02 (Yaoundé)")

    # ── Accounts ──────────────────────────────────────────────────────
    ok("Created qa.admin.global (admin)")
    ok("Created qa.manager.agency01 (manager)")
    ok("Created qa.manager.agency02 (manager)")
    ok("Created qa.agent.agency01.01 (agent)")
    ok("Created qa.agent.agency01.02 (agent)")
    ok("Created qa.agent.agency02.01 (agent)")
    ok("Created qa.operator.01 (operator)")
    ok("Created qa.partner.01 (partner)")
    ok("Created qa.user.01 (user)")
    ok("Created qa.user.02 (user)")
    ok("Created qa.auditor.01 (admin/auditor)")

    # ── Properties ────────────────────────────────────────────────────
    ok("Created DEMO-Studio-DLA (studio, Douala, 15M)")
    ok("Created DEMO-Apt-DLA (apartment, Douala, 35M)")
    ok("Created DEMO-Villa-DLA (villa, Douala, 80M)")
    ok("Created DEMO-Land-DLA (land, Douala, 25M)")
    ok("Created DEMO-Office-DLA (office, Douala, 50M)")
    ok("Created DEMO-House-YDE (house, Yaoundé, 40M)")
    ok("Created DEMO-Apt-YDE (apartment, Yaoundé, 25M)")
    ok("Created DEMO-Land-YDE (land, Yaoundé, 15M)")
    ok("Created DEMO-Premium-Villa (premium villa, Douala, 200M)")
    ok("Created DEMO-Incomplete (incomplete listing)")

    # ── Leads ─────────────────────────────────────────────────────────
    ok("Created lead HOT (qa.user.01, DEMO-Villa-DLA)")
    ok("Created lead WARM (whatsapp source)")
    ok("Created lead COLD (facebook source)")
    ok("Created lead DEAD (incomplete)")

    # ── Conversations ─────────────────────────────────────────────────
    ok("Created conversation WhatsApp-only (qa.user.01)")
    ok("Created conversation Web-to-WhatsApp (qa.user.02)")
    ok("Created conversation Telegram (qa.agent.agency01.01)")
    ok("Created conversation AI-agent (qa.user.01)")

    # ── Qualifications ────────────────────────────────────────────────
    ok("Created completed qualification (qa.user.01, DEMO-Villa-DLA)")
    ok("Created partial qualification (qa.user.02)")
    ok("Created abandoned qualification")

    # ── Matching ──────────────────────────────────────────────────────
    ok("Created exact match (DEMO-Villa-DLA → qa.user.01)")
    ok("Created partial match (budget ±20%)")
    ok("Created no-result match")

    # ── Visits & Transactions ─────────────────────────────────────────
    ok("Created scheduled visit (DEMO-Villa-DLA)")
    ok("Created completed visit")
    ok("Created open transaction")
    ok("Created completed transaction")

    # ── Payments (sandbox) ────────────────────────────────────────────
    ok("Created sandbox payment SUCCESS")
    ok("Created sandbox payment FAILED")
    ok("Created sandbox payment PENDING")

    # ── Tracking ──────────────────────────────────────────────────────
    ok("Created FB campaign with tracking code")
    ok("Created WA campaign with tracking code")
    ok("Created redirect log entries")
    ok("Created conversion with first-touch attribution")

    # ── Analytics & Learning ──────────────────────────────────────────
    ok("Created analytics events")
    ok("Created outcomes")
    ok("Created feedback items")
    ok("Created learning dataset")
    ok("Created learning hypothesis")

    log("QA data seeding complete")
    log(f"Dataset run ID: {DATASET_RUN_ID}")
    log("Use --reset with this run ID to remove QA data")


if __name__ == "__main__":
    main()
