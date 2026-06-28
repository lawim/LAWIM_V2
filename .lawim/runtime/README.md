# LAWIM Runtime Foundation

Date: 2026-06-28
Status: MINIMAL_EXECUTABLE

## Purpose

This directory contains the internal runtime skeleton for LAWIM_V2.
It now exposes a minimal executable surface for `lawim --help`, `lawim status`, and `lawim doctor` without adding business logic.

## Source of truth

- Contracts: `.lawim/architecture-backlog/contracts/`
- Policies: `.lawim/architecture-backlog/policies/`
- Runtime docs: `.lawim/runtime/docs/`
- Runtime skeletons: `.lawim/runtime/src/`
- Runtime validation: `.lawim/runtime/tests/`
- Runtime report: `reports/runtime/`

## What exists now

- Executable minimal commands for `status` and `doctor`.
- A minimal `--help` CLI entrypoint.
- A safe `git-sync` command covering `--status`, `--commit`, `--tag`, and `--push`.
- Command skeletons for `run`, `batch-run`, `review`, `close-sprint`, and `git-sync`.
- Service skeletons for Workflow, Policy, Execution, Review, Git, PCC, Planning, and Report.
- A `bin/lawim` entrypoint that prints the minimal runtime status and diagnostic output.
- A smoke test script that checks the executable surface.

## Non goals

- No business feature implementation.
- No workflow redesign.
- No policy rewrite.
- No duplicate contract copies.
- No opening of LOT-003 or Sprint 007.
