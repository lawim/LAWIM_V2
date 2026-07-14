from __future__ import annotations

import json
import subprocess
import sys
import time
from http import HTTPStatus
from pathlib import Path

from tests.lawim_harness import LawimTestHarness
from lawim_v2.observability import METRICS, RuntimeMetrics
from lawim_v2.schema_ddl import POSTGRESQL_INIT_STATEMENTS, SQLITE_INIT_SCRIPT


class Week002ProductionTest(LawimTestHarness):
    def test_production_indexes_present_in_ddl(self) -> None:
        ddl_blob = "\n".join(POSTGRESQL_INIT_STATEMENTS) + SQLITE_INIT_SCRIPT
        for index_name in (
            "idx_events_kind_created",
            "idx_sessions_user_expires",
            "idx_sessions_expires_at",
            "idx_properties_owner_status",
        ):
            self.assertIn(index_name, ddl_blob)

    def test_readyz_includes_storage_probe(self) -> None:
        response = self.invoke("/readyz")
        self.assertEqual(response.status, HTTPStatus.OK)
        payload = response.body_json()
        self.assertEqual(payload.get("status"), "ready")
        storage = payload.get("storage") or {}
        self.assertTrue(storage.get("ready"))

    def test_metrics_snapshot_includes_latency(self) -> None:
        response = self.invoke("/api/health")
        self.assertEqual(response.status, HTTPStatus.OK)
        snapshot = METRICS.snapshot()
        self.assertIn("latency_ms", snapshot)
        self.assertIn("routes_top", snapshot)

    def test_events_support_kind_filter(self) -> None:
        token = self.login(email="admin@lawim.local")
        self.repository.record_event("audit_probe", {"scope": "week002"})
        response = self.invoke("/api/events?kind=audit_probe&limit=5", token=token)
        self.assertEqual(response.status, HTTPStatus.OK)
        events = response.body_json().get("events") or []
        self.assertTrue(events)
        self.assertEqual(events[0].get("kind"), "audit_probe")

    def test_get_conversation_uses_indexed_message_lookup(self) -> None:
        token = self.login(email="admin@lawim.local")
        conversations = self.invoke("/api/conversations", token=token)
        items = conversations.body_json().get("conversations") or []
        if not items:
            self.skipTest("No seeded conversations")
        conversation_id = items[0]["id"]
        detail = self.invoke(f"/api/conversations/{conversation_id}", token=token)
        self.assertEqual(detail.status, HTTPStatus.OK)
        payload = detail.body_json().get("conversation") or {}
        self.assertIn("message_count", payload)

    def test_benchmark_runtime_script_runs(self) -> None:
        root = Path(__file__).resolve().parent.parent
        result = subprocess.run(
            [sys.executable, str(root / "scripts" / "benchmark_runtime.py")],
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        report = json.loads(result.stdout)
        self.assertIn("routes", report)
        self.assertGreaterEqual(len(report["routes"]), 3)

    def test_production_validation_script_passes(self) -> None:
        root = Path(__file__).resolve().parent.parent
        result = subprocess.run(
            ["bash", str(root / "platform/validate-production.sh")],
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr or result.stdout)
        self.assertIn("PRODUCTION VALIDATION OK", result.stdout)


class RuntimeMetricsUnitTest(LawimTestHarness):
    def test_record_request_tracks_percentiles(self) -> None:
        metrics = RuntimeMetrics()
        for value in (1.0, 2.0, 3.0, 4.0, 100.0):
            metrics.record_request(route="/api/health", duration_ms=value)
        snapshot = metrics.snapshot()
        latency = snapshot["latency_ms"]
        self.assertEqual(latency["samples"], 5)
        self.assertGreaterEqual(latency["p95"], latency["p50"])
