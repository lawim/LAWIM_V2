# LAWIM Runtime Foundation

Date: 2026-06-28
Status: FOUNDATION_CREATED

## Purpose

This directory contains the internal runtime skeleton for LAWIM_V2.
It prepares the command, service, policy, and reporting boundaries without adding business logic.

## Source of truth

- Contracts: `.lawim/architecture-backlog/contracts/`
- Policies: `.lawim/architecture-backlog/policies/`
- Runtime docs: `.lawim/runtime/docs/`
- Runtime skeletons: `.lawim/runtime/src/`
- Runtime validation: `.lawim/runtime/tests/`
- Runtime report: `reports/runtime/`

## What exists now

- Command skeletons for `status`, `doctor`, `run`, `batch-run`, `review`, `close-sprint`, and `git-sync`.
- Service skeletons for Workflow, Policy, Execution, Review, Git, PCC, Planning, and Report.
- A small `bin/lawim` entrypoint stub that only advertises the contract surface.
- A smoke test script that checks the foundation files exist.

## Non goals

- No business feature implementation.
- No workflow redesign.
- No policy rewrite.
- No duplicate contract copies.
- No opening of LOT-003 or Sprint 007.
