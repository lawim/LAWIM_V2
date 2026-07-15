# Program O — Ecosystem, Integrations & Marketplace Tests
from __future__ import annotations

import json
import unittest

from lawim_v2.ecosystem import (
    ConnectorDefinition, ConnectorRegistry, ConnectorStatus, ConnectorType,
    EcosystemConfig,
    ExtensionDefinition, ExtensionManifest, ExtensionRegistry, ExtensionStatus,
    LicenseType,
    MarketplaceListing, MarketplaceRegistry, MarketplaceStatus,
    PartnerDefinition, PartnerRegistry, PartnerStatus, PartnerTier,
    PluginDefinition, PluginRegistry, PluginStatus,
    SdkDefinition, SdkLanguage, SdkRegistry, SdkStatus,
)

# ── Plugin Registry Tests ──────────────────────────────────────────────


class PluginRegistryTest(unittest.TestCase):
    def setUp(self):
        self.reg = PluginRegistry()

    def test_register(self):
        p = self.reg.register(PluginDefinition(plugin_code="test", name="Test"))
        self.assertIsNotNone(self.reg.get("test"))

    def test_list(self):
        self.reg.register(PluginDefinition(plugin_code="a"))
        self.reg.register(PluginDefinition(plugin_code="b"))
        self.assertEqual(self.reg.count(), 2)

    def test_list_by_status(self):
        self.reg.register(PluginDefinition(plugin_code="a", status=PluginStatus.ACTIVE))
        self.reg.register(PluginDefinition(plugin_code="b", status=PluginStatus.DRAFT))
        active = self.reg.list(PluginStatus.ACTIVE)
        self.assertEqual(len(active), 1)

    def test_to_dict(self):
        p = PluginDefinition(plugin_code="test", name="Test Plugin", version="1.0.0")
        d = p.to_dict()
        self.assertEqual(d["name"], "Test Plugin")


# ── Extension Registry Tests ───────────────────────────────────────────


class ExtensionRegistryTest(unittest.TestCase):
    def setUp(self):
        self.reg = ExtensionRegistry()

    def test_register(self):
        e = self.reg.register(ExtensionDefinition(extension_code="ext1", name="Ext1"))
        self.assertIsNotNone(self.reg.get("ext1"))

    def test_manifest(self):
        e = ExtensionDefinition(extension_code="e1", manifest=ExtensionManifest(
            min_core_version="2.0.0", checksum="abc123"))
        self.assertEqual(e.manifest.checksum, "abc123")


# ── Connector Registry Tests ───────────────────────────────────────────


class ConnectorRegistryTest(unittest.TestCase):
    def setUp(self):
        self.reg = ConnectorRegistry()

    def test_register(self):
        c = self.reg.register(ConnectorDefinition(
            connector_code="campay", name="Campay",
            connector_type=ConnectorType.PAYMENT, provider="campay"))
        self.assertIsNotNone(self.reg.get("campay"))
        self.assertEqual(c.connector_type, ConnectorType.PAYMENT)

    def test_list_by_type(self):
        self.reg.register(ConnectorDefinition(connector_code="c1", connector_type=ConnectorType.SMS))
        self.reg.register(ConnectorDefinition(connector_code="c2", connector_type=ConnectorType.SMS))
        sms = self.reg.list(ConnectorType.SMS)
        self.assertEqual(len(sms), 2)

    def test_all_connector_types(self):
        count = len(list(ConnectorType))
        self.assertEqual(count, 15)  # All 15 connector types


# ── Marketplace Tests ──────────────────────────────────────────────────


class MarketplaceRegistryTest(unittest.TestCase):
    def setUp(self):
        self.reg = MarketplaceRegistry()

    def test_register(self):
        m = self.reg.register(MarketplaceListing(listing_id="m1", name="Test Extension"))
        self.assertEqual(self.reg.count(), 1)

    def test_list_by_status(self):
        self.reg.register(MarketplaceListing(listing_id="m1", status=MarketplaceStatus.PUBLISHED))
        self.reg.register(MarketplaceListing(listing_id="m2", status=MarketplaceStatus.DRAFT))
        pub = self.reg.list(MarketplaceStatus.PUBLISHED)
        self.assertEqual(len(pub), 1)

    def test_to_dict(self):
        m = MarketplaceListing(listing_id="m1", name="Ext", downloads=150, rating=4.5)
        d = m.to_dict()
        self.assertEqual(d["downloads"], 150)


# ── SDK Registry Tests ─────────────────────────────────────────────────


class SdkRegistryTest(unittest.TestCase):
    def setUp(self):
        self.reg = SdkRegistry()

    def test_register(self):
        s = self.reg.register(SdkDefinition(language=SdkLanguage.PYTHON, version="1.0.0"))
        self.assertGreaterEqual(self.reg.count(), 1)

    def test_list(self):
        self.reg.register(SdkDefinition(language=SdkLanguage.PYTHON, version="1.0"))
        self.reg.register(SdkDefinition(language=SdkLanguage.JAVASCRIPT, version="1.0"))
        self.assertEqual(self.reg.count(), 2)


# ── Partner Registry Tests ─────────────────────────────────────────────


class PartnerRegistryTest(unittest.TestCase):
    def setUp(self):
        self.reg = PartnerRegistry()

    def test_register(self):
        p = self.reg.register(PartnerDefinition(partner_code="agency1", name="Agency 1"))
        self.assertIsNotNone(self.reg.get("agency1"))

    def test_tier(self):
        p = PartnerDefinition(partner_code="p1", tier=PartnerTier.GOLD)
        self.assertEqual(p.tier, PartnerTier.GOLD)

    def test_white_label(self):
        p = PartnerDefinition(partner_code="p1", white_label_enabled=True, domain="agency.lawim.app")
        self.assertTrue(p.white_label_enabled)
        self.assertEqual(p.domain, "agency.lawim.app")

    def test_to_dict(self):
        p = PartnerDefinition(partner_code="p1", name="Partner", tier=PartnerTier.PLATINUM)
        d = p.to_dict()
        self.assertEqual(d["tier"], "PLATINUM")


# ── Config Tests ───────────────────────────────────────────────────────


class EcosystemConfigTest(unittest.TestCase):
    def test_default_disabled(self):
        cfg = EcosystemConfig()
        self.assertFalse(cfg.extension_platform_enabled)
        self.assertFalse(cfg.connector_framework_enabled)
        self.assertFalse(cfg.marketplace_enabled)
        self.assertFalse(cfg.public_api_enabled)
        self.assertFalse(cfg.partner_ecosystem_enabled)


# ── Enum Tests ─────────────────────────────────────────────────────────


class ConnectorTypeEnumTest(unittest.TestCase):
    def test_values(self):
        self.assertEqual(ConnectorType.PAYMENT.value, "PAYMENT")
        self.assertEqual(ConnectorType.OCR.value, "OCR")
        self.assertEqual(ConnectorType.ERP.value, "ERP")


class PluginStatusEnumTest(unittest.TestCase):
    def test_values(self):
        self.assertEqual(PluginStatus.ACTIVE.value, "ACTIVE")
        self.assertEqual(PluginStatus.UNINSTALLED.value, "UNINSTALLED")


class PartnerTierEnumTest(unittest.TestCase):
    def test_values(self):
        self.assertEqual(PartnerTier.BRONZE.value, "BRONZE")
        self.assertEqual(PartnerTier.PLATINUM.value, "PLATINUM")


class LicenseTypeEnumTest(unittest.TestCase):
    def test_values(self):
        self.assertEqual(LicenseType.MIT.value, "MIT")
        self.assertEqual(LicenseType.PROPRIETARY.value, "PROPRIETARY")


class SdkLanguageEnumTest(unittest.TestCase):
    def test_values(self):
        self.assertEqual(SdkLanguage.PYTHON.value, "PYTHON")
        self.assertEqual(SdkLanguage.PHP.value, "PHP")


# ── Serialization Tests ────────────────────────────────────────────────


class EcosystemSerializationTest(unittest.TestCase):
    def test_plugin_json(self):
        p = PluginDefinition(plugin_code="test", name="Test", version="1.0.0")
        s = json.dumps(p.to_dict(), ensure_ascii=False, sort_keys=True)
        self.assertIn("1.0.0", s)

    def test_connector_json(self):
        c = ConnectorDefinition(connector_code="campay", name="Campay",
                                 connector_type=ConnectorType.PAYMENT)
        s = json.dumps(c.to_dict(), ensure_ascii=False, sort_keys=True)
        self.assertIn("PAYMENT", s)

    def test_marketplace_json(self):
        m = MarketplaceListing(listing_id="m1", name="Ext", downloads=100)
        s = json.dumps(m.to_dict(), ensure_ascii=False, sort_keys=True)
        self.assertIn("100", s)

    def test_partner_json(self):
        p = PartnerDefinition(partner_code="p1", name="Partner", tier=PartnerTier.GOLD)
        s = json.dumps(p.to_dict(), ensure_ascii=False, sort_keys=True)
        self.assertIn("GOLD", s)


if __name__ == "__main__":
    unittest.main()
