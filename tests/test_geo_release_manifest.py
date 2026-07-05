from __future__ import annotations

from pathlib import Path
from unittest import TestCase


ROOT = Path(__file__).resolve().parents[1]


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class GeoReleaseManifestTest(TestCase):
    def test_deployment_manifest_includes_geo_runtime_and_exclusions(self) -> None:
        text = read_text("release/manifests/DEPLOYMENT_MANIFEST.md")

        for snippet in (
            "code/lawim_v2/geo_domain.py",
            "code/lawim_v2/geo_reference.py",
            "code/lawim_v2/geocoding_provider.py",
            "code/lawim_v2/services.py",
            "code/lawim_v2/dto.py",
            "code/lawim_v2/data/cameroon_locations.json",
        ):
            self.assertIn(snippet, text)

        for snippet in (
            "- `docs/`",
            "- `reports/`",
            "- `prompts/`",
            "- `tests/`",
            "- `release/`",
            "- `code/lawim_v2/migration.py`",
            "no raw LAWIM or LAWIMA source tree is copied into OVH",
        ):
            self.assertIn(snippet, text)

    def test_release_manifest_records_geo_closure(self) -> None:
        text = read_text("release/manifests/RELEASE_MANIFEST.md")

        for snippet in (
            "Geo Intelligence closure",
            "code/lawim_v2/geo_reference.py",
            "code/lawim_v2/data/cameroon_locations.json",
            "offline geocoding",
            "alias normalization",
            "local search merge",
            "deterministic fallback",
        ):
            self.assertIn(snippet, text)

    def test_security_classification_mentions_geo_runtime(self) -> None:
        text = read_text("release/manifests/SECURITY_CLASSIFICATION.md")

        self.assertIn("raw LAWIM and LAWIMA source snapshots used for analysis", text)
        self.assertIn("code/lawim_v2/data/", text)
        self.assertIn("curated geo reference bundle", text)
