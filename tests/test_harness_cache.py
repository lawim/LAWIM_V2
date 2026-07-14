from __future__ import annotations

from unittest import TestCase

from tests.lawim_harness import build_test_fixture
from lawim_v2.db import NotFoundError


class TestHarnessTemplateCacheIsolation(TestCase):
    def test_cached_template_clones_are_isolated(self) -> None:
        first = build_test_fixture()
        try:
            baseline_organizations = int(first.repository.summary()["organizations"])
            first.repository.create_organization(
                name="Cache Probe Organization",
                slug="cache-probe-organization",
                kind="owner",
            )
            self.assertEqual(int(first.repository.summary()["organizations"]), baseline_organizations + 1)
        finally:
            first.repository.close()
            first.tempdir.cleanup()

        second = build_test_fixture()
        try:
            self.assertEqual(int(second.repository.summary()["organizations"]), baseline_organizations)
            with self.assertRaises(NotFoundError):
                second.repository.get_organization_by_slug("cache-probe-organization")
        finally:
            second.repository.close()
            second.tempdir.cleanup()
