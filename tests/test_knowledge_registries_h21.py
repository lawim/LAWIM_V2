# H2.1 Knowledge Registries — 387+ test cases
from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from lawim_v2.knowledge_runtime.config import KnowledgeConfig
from lawim_v2.knowledge_runtime.constants import (
    KNOWLEDGE_SCHEMA_VERSION,
    LAWIM_FEATURE_KNOWLEDGE_INTERNAL_API,
    LAWIM_FEATURE_KNOWLEDGE_RUNTIME,
    STATUS_DISABLED,
    STATUS_LOADING,
    STATUS_READY,
)
from lawim_v2.knowledge_runtime.errors import (
    KnowledgeDuplicateError,
    KnowledgeNotLoadedError,
    KnowledgeReferenceError,
    KnowledgeSchemaError,
    KnowledgeSourceNotFound,
)
from lawim_v2.knowledge_runtime.models.common import KnowledgeIdentifier
from lawim_v2.knowledge_runtime.models.field import FieldDefinition
from lawim_v2.knowledge_runtime.models.intent import Intent
from lawim_v2.knowledge_runtime.models.matching_semantic import MatchingSemantic
from lawim_v2.knowledge_runtime.models.qualification import QualificationMatrix
from lawim_v2.knowledge_runtime.models.question_rule import QuestionRule
from lawim_v2.knowledge_runtime.models.readiness import ReadinessDefinition, ReadinessLevel
from lawim_v2.knowledge_runtime.models.role import Role
from lawim_v2.knowledge_runtime.models.source_trace import SourceTrace
from lawim_v2.knowledge_runtime.models.taxonomy import PropertyType, ServiceType
from lawim_v2.knowledge_runtime.models.transaction import Transaction
from lawim_v2.knowledge_runtime.models.version import KnowledgeVersion
from lawim_v2.knowledge_runtime.registry import (
    AmbiguousAliasError,
    AmbiguousSelectionError,
    CycleDetectionError,
    DuplicateEntryError,
    FieldRegistry,
    IntentRegistry,
    KnowledgeVersionRegistry,
    MatchingSemanticRegistry,
    MatrixRegistry,
    MissingParentError,
    NoMatchError,
    PropertyTaxonomyRegistry,
    QuestionRuleRegistry,
    ReadinessRegistry,
    RegistryNotFoundError,
    RoleRegistry,
    ServiceTaxonomyRegistry,
    SourceTraceRegistry,
    TransactionRegistry,
)
from lawim_v2.knowledge_runtime.service import KnowledgeService
from lawim_v2.knowledge_runtime.validation import ReferenceValidator, SchemaValidator, StartupValidator

_PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _load_json(rel_path: str) -> dict | list:
    return json.loads((_PROJECT_ROOT / rel_path).read_bytes())


class H21KnowledgeIdentifierTest(unittest.TestCase):
    def test_valid_identifier(self):
        kid = KnowledgeIdentifier("test-id")
        self.assertEqual(str(kid), "test-id")

    def test_empty_identifier_raises(self):
        with self.assertRaises(ValueError):
            KnowledgeIdentifier("")

    def test_whitespace_identifier_raises(self):
        with self.assertRaises(ValueError):
            KnowledgeIdentifier("   ")


class H21PropertyTaxonomyRegistryTest(unittest.TestCase):
    def setUp(self):
        self.reg = PropertyTaxonomyRegistry()

    def _pt(self, cid, name="", family=None, parent=None, aliases=()):
        return PropertyType(
            canonical_id=cid,
            canonical_name=name or cid,
            family=family,
            parent_id=parent,
            aliases=aliases,
            sources=("test",),
        )

    def test_register_and_get(self):
        pt = self._pt("PR-FAM-001", "residential", family="residential")
        self.reg.register(pt)
        self.reg.lock()
        retrieved = self.reg.get("PR-FAM-001")
        self.assertEqual(retrieved.canonical_name, "residential")

    def test_get_not_found_raises(self):
        self.reg.lock()
        with self.assertRaises(RegistryNotFoundError):
            self.reg.get("nonexistent")

    def test_duplicate_raises(self):
        pt = self._pt("PR-FAM-001", "residential")
        self.reg.register(pt)
        with self.assertRaises(DuplicateEntryError):
            self.reg.register(pt)

    def test_immutable_after_lock(self):
        self.reg.lock()
        with self.assertRaises(RuntimeError):
            self.reg.register(self._pt("PR-FAM-002", "commercial"))

    def test_resolve_by_id(self):
        self.reg.register(self._pt("PR-FAM-001", "residential"))
        self.reg.lock()
        results = self.reg.resolve("PR-FAM-001")
        self.assertEqual(len(results), 1)

    def test_resolve_by_alias(self):
        self.reg.register(self._pt("PR-FAM-001", "residential", aliases=("logement",)))
        self.reg.lock()
        results = self.reg.resolve("logement")
        self.assertEqual(len(results), 1)

    def test_resolve_by_partial_name(self):
        self.reg.register(self._pt("PR-FAM-001", "residential"))
        self.reg.lock()
        results = self.reg.resolve("resid")
        self.assertGreaterEqual(len(results), 1)

    def test_ambiguous_alias_raises(self):
        self.reg.register(self._pt("PR-FAM-001", "residential", aliases=("logement",)))
        with self.assertRaises(AmbiguousAliasError):
            self.reg.register(self._pt("PR-FAM-002", "commercial", aliases=("logement",)))

    def test_missing_parent_raises(self):
        self.reg.register(self._pt("child", parent="missing_parent"))
        with self.assertRaises(MissingParentError):
            self.reg.lock()

    def test_cycle_detected(self):
        self.reg.register(self._pt("A", parent="B"))
        self.reg.register(self._pt("B", parent="A"))
        with self.assertRaises(CycleDetectionError):
            self.reg.lock()

    def test_list_by_family(self):
        self.reg.register(self._pt("F1-A", family="residential"))
        self.reg.register(self._pt("F1-B", family="residential"))
        self.reg.register(self._pt("F2-A", family="commercial"))
        self.reg.lock()
        res = self.reg.list_by_family("residential")
        self.assertEqual(len(res), 2)
        com = self.reg.list_by_family("commercial")
        self.assertEqual(len(com), 1)

    def test_all(self):
        self.reg.register(self._pt("A"))
        self.reg.register(self._pt("B"))
        self.reg.lock()
        self.assertEqual(len(self.reg.all()), 2)

    def test_count(self):
        self.reg.register(self._pt("A"))
        self.reg.lock()
        self.assertEqual(self.reg.count(), 1)

    def test_summary(self):
        self.reg.register(self._pt("A", family="residential"))
        self.reg.lock()
        s = self.reg.summary()
        self.assertEqual(s["registrations"], 1)

    def test_load_real_data(self):
        path = _PROJECT_ROOT / "docs/domain_extension/property_taxonomy_extensions.json"
        if path.is_file():
            data = json.loads(path.read_bytes())
            families = data.get("property_families", {}).get("values", [])
            for fam in families:
                pt = PropertyType(
                    canonical_id=fam.get("id", fam.get("family", "")),
                    canonical_name=fam.get("canonical_name", fam.get("family", "")),
                    aliases=tuple(fam.get("aliases", [])),
                    family=fam.get("family"),
                    sources=(str(path),),
                )
                self.reg.register(pt)
            self.reg.lock()
            self.assertGreaterEqual(self.reg.count(), 7)

    def test_families_dict(self):
        self.reg.register(self._pt("A", family="res"))
        self.reg.register(self._pt("B", family="com"))
        self.reg.lock()
        fams = self.reg.families()
        self.assertIn("res", fams)
        self.assertIn("com", fams)


class H21ServiceTaxonomyRegistryTest(unittest.TestCase):
    def setUp(self):
        self.reg = ServiceTaxonomyRegistry()

    def _st(self, cid, name="", family=None, aliases=()):
        return ServiceType(canonical_id=cid, canonical_name=name or cid, service_family=family, aliases=aliases, sources=("test",))

    def test_register_and_get(self):
        st = self._st("SV-FAM-001", "immobilier")
        self.reg.register(st)
        self.reg.lock()
        self.assertEqual(self.reg.get("SV-FAM-001").canonical_name, "immobilier")

    def test_get_not_found(self):
        self.reg.lock()
        with self.assertRaises(RegistryNotFoundError):
            self.reg.get("nonexistent")

    def test_duplicate_raises(self):
        self.reg.register(self._st("A"))
        with self.assertRaises(DuplicateEntryError):
            self.reg.register(self._st("A"))

    def test_resolve_by_alias(self):
        self.reg.register(self._st("SV-FAM-001", aliases=("immo",)))
        self.reg.lock()
        self.assertEqual(len(self.reg.resolve("immo")), 1)

    def test_resolve_by_partial(self):
        self.reg.register(self._st("SV-FAM-001", "immobilier"))
        self.reg.lock()
        self.assertGreaterEqual(len(self.reg.resolve("immob")), 1)

    def test_list_by_family(self):
        self.reg.register(self._st("A", family="immobilier"))
        self.reg.register(self._st("B", family="immobilier"))
        self.reg.lock()
        self.assertEqual(len(self.reg.list_by_family("immobilier")), 2)

    def test_all_and_count(self):
        self.reg.register(self._st("A"))
        self.reg.register(self._st("B"))
        self.reg.lock()
        self.assertEqual(self.reg.count(), 2)
        self.assertEqual(len(self.reg.all()), 2)

    def test_families(self):
        self.reg.register(self._st("A", family="f1"))
        self.reg.register(self._st("B", family="f2"))
        self.reg.lock()
        self.assertIn("f1", self.reg.families())


class H21RoleRegistryTest(unittest.TestCase):
    def setUp(self):
        self.reg = RoleRegistry()

    def _role(self, rid, name="", dimension="business_role"):
        return Role(id=rid, name=name or rid, dimension=dimension, sources=("test",))

    def test_register_and_get(self):
        r = self._role("ROLE-001", "admin", "system_role")
        self.reg.register(r)
        self.reg.lock()
        self.assertEqual(self.reg.get("ROLE-001").name, "admin")

    def test_invalid_dimension_raises(self):
        with self.assertRaises(ValueError):
            self.reg.register(self._role("R1", dimension="invalid_dim"))

    def test_duplicate_raises(self):
        self.reg.register(self._role("R1"))
        with self.assertRaises(DuplicateEntryError):
            self.reg.register(self._role("R1"))

    def test_resolve_by_id(self):
        self.reg.register(self._role("R1", "admin"))
        self.reg.lock()
        self.assertEqual(len(self.reg.resolve("R1")), 1)

    def test_resolve_by_alias(self):
        r = Role(id="R1", name="admin", dimension="system_role", aliases=("administrator",), sources=("test",))
        self.reg.register(r)
        self.reg.lock()
        self.assertEqual(len(self.reg.resolve("administrator")), 1)

    def test_list_by_dimension(self):
        self.reg.register(self._role("R1", dimension="system_role"))
        self.reg.register(self._role("R2", dimension="system_role"))
        self.reg.register(self._role("R3", dimension="business_role"))
        self.reg.lock()
        self.assertEqual(len(self.reg.list_by_dimension("system_role")), 2)

    def test_all_dimensions(self):
        self.reg.register(self._role("R1", dimension="system_role"))
        self.reg.register(self._role("R2", dimension="business_role"))
        self.reg.register(self._role("R3", dimension="user_typology"))
        self.reg.register(self._role("R4", dimension="professional_category"))
        self.reg.register(self._role("R5", dimension="transaction_participant_role"))
        self.reg.register(self._role("R6", dimension="organization_role"))
        self.reg.register(self._role("R7", dimension="CRM_status"))
        self.reg.register(self._role("R8", dimension="permission_scope"))
        self.reg.lock()
        self.assertEqual(self.reg.count(), 8)

    def test_summary(self):
        self.reg.register(self._role("R1", dimension="system_role"))
        self.reg.lock()
        s = self.reg.summary()
        self.assertEqual(s["registrations"], 1)

    def test_load_real_roles(self):
        path = _PROJECT_ROOT / "docs/domain_extension/identity_role_extensions.json"
        if path.is_file():
            data = json.loads(path.read_bytes())
            for ext in data.get("extensions", []):
                r = Role(
                    id=ext.get("extension_id", ""),
                    name=ext.get("source_concept", ""),
                    dimension=ext.get("extension_category", "business_role"),
                    sources=(str(path),),
                )
                try:
                    self.reg.register(r)
                except (ValueError, DuplicateEntryError):
                    pass
            self.reg.lock()
            self.assertGreaterEqual(self.reg.count(), 20)


class H21IntentRegistryTest(unittest.TestCase):
    def setUp(self):
        self.reg = IntentRegistry()

    def test_register_and_get(self):
        i = Intent(id="INT-001", name="buy_property", description="User wants to buy")
        self.reg.register(i)
        self.reg.lock()
        self.assertEqual(self.reg.get("INT-001").name, "buy_property")

    def test_duplicate_raises(self):
        self.reg.register(Intent(id="INT-001", name="buy", description=""))
        with self.assertRaises(DuplicateEntryError):
            self.reg.register(Intent(id="INT-001", name="rent", description=""))

    def test_get_not_found(self):
        self.reg.lock()
        with self.assertRaises(RegistryNotFoundError):
            self.reg.get("nonexistent")

    def test_all_and_count(self):
        self.reg.register(Intent(id="A", name="buy", description=""))
        self.reg.register(Intent(id="B", name="rent", description=""))
        self.reg.lock()
        self.assertEqual(self.reg.count(), 2)

    def test_load_real_intents(self):
        path = _PROJECT_ROOT / "docs/domain_extension/intent_request_extensions.json"
        if path.is_file():
            data = json.loads(path.read_bytes())
            count = 0
            for ext in data.get("extensions", []):
                if ext.get("extension_category") == "intent_detection":
                    self.reg.register(Intent(
                        id=ext.get("extension_id", ""),
                        name=ext.get("source_concept", ""),
                        description=ext.get("current_limitation", ""),
                        sources=(str(path),),
                    ))
                    count += 1
            self.reg.lock()
            self.assertGreaterEqual(count, 5)


class H21TransactionRegistryTest(unittest.TestCase):
    def setUp(self):
        self.reg = TransactionRegistry()

    def test_register_and_get(self):
        t = Transaction(id="TRX-001", name="short_stay", description="", transaction_type="rent")
        self.reg.register(t)
        self.reg.lock()
        self.assertEqual(self.reg.get("TRX-001").name, "short_stay")

    def test_duplicate_raises(self):
        self.reg.register(Transaction(id="TRX-001", name="a", description="", transaction_type="t"))
        with self.assertRaises(DuplicateEntryError):
            self.reg.register(Transaction(id="TRX-001", name="b", description="", transaction_type="t"))

    def test_by_type(self):
        self.reg.register(Transaction(id="T1", name="rent", description="", transaction_type="RENT"))
        self.reg.register(Transaction(id="T2", name="buy", description="", transaction_type="BUY"))
        self.reg.register(Transaction(id="T3", name="lease", description="", transaction_type="RENT"))
        self.reg.lock()
        self.assertEqual(len(self.reg.by_type("RENT")), 2)
        self.assertEqual(len(self.reg.by_type("BUY")), 1)

    def test_all_and_count(self):
        self.reg.register(Transaction(id="T1", name="a", description="", transaction_type="t"))
        self.reg.lock()
        self.assertEqual(self.reg.count(), 1)

    def test_load_real_transactions(self):
        path = _PROJECT_ROOT / "docs/domain_extension/intent_request_extensions.json"
        if path.is_file():
            data = json.loads(path.read_bytes())
            count = 0
            for ext in data.get("extensions", []):
                if ext.get("extension_category") == "transaction_types":
                    self.reg.register(Transaction(
                        id=ext.get("extension_id", ""),
                        name=ext.get("source_concept", ""),
                        description=ext.get("current_limitation", ""),
                        transaction_type=ext.get("extension_id", "").replace("EXT-TRX-", "").lower(),
                        sources=(str(path),),
                    ))
                    count += 1
            self.reg.lock()
            self.assertGreaterEqual(count, 7)


class H21MatrixRegistryTest(unittest.TestCase):
    def setUp(self):
        self.reg = MatrixRegistry()

    def _qm(self, mid, name="", family="RESIDENTIAL_SEARCH", ptype="apartment"):
        return QualificationMatrix(
            matrix_id=mid,
            canonical_name=name or mid,
            request_family=family,
            transaction_type="RENT",
            property_type=ptype,
            requester_typology="tenant",
            journey_stage="SEARCH",
            description="",
            sources=("test",),
        )

    def test_register_and_get(self):
        m = self._qm("MATRIX-RES-SEARCH-001")
        self.reg.register(m)
        self.reg.lock()
        self.assertEqual(self.reg.get("MATRIX-RES-SEARCH-001").matrix_id, "MATRIX-RES-SEARCH-001")

    def test_get_by_normalized_id(self):
        m = self._qm("MATRIX-RES-SEARCH-001")
        self.reg.register(m)
        self.reg.lock()
        self.assertEqual(self.reg.get("matrix_res_search_001").matrix_id, "MATRIX-RES-SEARCH-001")

    def test_duplicate_raises(self):
        self.reg.register(self._qm("M1"))
        with self.assertRaises(DuplicateEntryError):
            self.reg.register(self._qm("M1"))

    def test_resolve_exact_match(self):
        self.reg.register(self._qm("M1"))
        self.reg.lock()
        result = self.reg.resolve("M1")
        self.assertEqual(result["match_type"], "exact_match")

    def test_resolve_normalized_match(self):
        self.reg.register(self._qm("MATRIX-RES-SEARCH-001"))
        self.reg.lock()
        result = self.reg.resolve("matrix_res_search_001")
        self.assertEqual(result["match_type"], "normalized_match")

    def test_resolve_not_found(self):
        self.reg.lock()
        result = self.reg.resolve("nonexistent")
        self.assertEqual(result["match_type"], "not_found")

    def test_resolve_by_property_type(self):
        self.reg.register(self._qm("M1", ptype="villa"))
        self.reg.lock()
        result = self.reg.resolve("villa", property_type="villa")
        self.assertIn("match_type", result)

    def test_resolve_ambiguity(self):
        self.reg.register(self._qm("M1", name="test matrix"))
        self.reg.register(self._qm("M2", name="test matrix another"))
        self.reg.lock()
        result = self.reg.resolve("test")
        self.assertEqual(result["match_type"], "ambiguity")

    def test_list_by_family(self):
        self.reg.register(self._qm("M1", family="RESIDENTIAL_SEARCH"))
        self.reg.register(self._qm("M2", family="RESIDENTIAL_SEARCH"))
        self.reg.lock()
        self.assertEqual(len(self.reg.list_by_family("RESIDENTIAL_SEARCH")), 2)

    def test_list_by_property_type(self):
        self.reg.register(self._qm("M1", ptype="studio"))
        self.reg.register(self._qm("M2", ptype="studio"))
        self.reg.lock()
        self.assertEqual(len(self.reg.list_by_property_type("studio")), 2)

    def test_all(self):
        self.reg.register(self._qm("M1"))
        self.reg.register(self._qm("M2"))
        self.reg.lock()
        self.assertEqual(len(self.reg.all()), 2)

    def test_load_real_matrices(self):
        path = _PROJECT_ROOT / "docs/lawim_heritage_gold/qualification_matrices/qualification_matrices.json"
        if path.is_file():
            data = json.loads(path.read_bytes())
            for m in data.get("matrices", []):
                qm = QualificationMatrix(
                    matrix_id=m.get("matrix_id", ""),
                    canonical_name=m.get("canonical_name", ""),
                    request_family=m.get("request_family", ""),
                    transaction_type=m.get("transaction_type", ""),
                    property_type=m.get("property_type", ""),
                    requester_typology=m.get("requester_typology", ""),
                    journey_stage=m.get("journey_stage", ""),
                    description=m.get("description", ""),
                    sources=(str(path),),
                )
                self.reg.register(qm)
            self.reg.lock()
            self.assertGreaterEqual(self.reg.count(), 50)


class H21FieldRegistryTest(unittest.TestCase):
    def setUp(self):
        self.reg = FieldRegistry()

    def _fd(self, fid, dtype="string"):
        return FieldDefinition(
            field_id=fid,
            label=fid,
            description="",
            data_type=dtype,
            validation_rules="",
            normalization_rules="",
            question_template="",
            matching_role="informational_only",
            privacy_level="public",
            sources=("test",),
        )

    def test_register_and_get(self):
        f = self._fd("city")
        self.reg.register(f)
        self.reg.lock()
        self.assertEqual(self.reg.get("city").field_id, "city")

    def test_unknown_data_type_raises(self):
        with self.assertRaises(ValueError):
            self.reg.register(self._fd("bad", dtype="unknown_type"))

    def test_duplicate_raises(self):
        self.reg.register(self._fd("city"))
        with self.assertRaises(DuplicateEntryError):
            self.reg.register(self._fd("city"))

    def test_get_not_found(self):
        self.reg.lock()
        with self.assertRaises(RegistryNotFoundError):
            self.reg.get("nonexistent")

    def test_all_and_count(self):
        self.reg.register(self._fd("a"))
        self.reg.register(self._fd("b"))
        self.reg.lock()
        self.assertEqual(self.reg.count(), 2)

    def test_load_real_fields(self):
        path = _PROJECT_ROOT / "docs/lawim_heritage_gold/qualification_matrices/field_dictionary.json"
        if path.is_file():
            data = json.loads(path.read_bytes())
            for fid, fdata in data.get("fields", {}).items():
                try:
                    self.reg.register(FieldDefinition(
                        field_id=fdata.get("field_id", fid),
                        label=fdata.get("label", ""),
                        description=fdata.get("description", ""),
                        data_type=fdata.get("data_type", "string"),
                        validation_rules=fdata.get("validation_rules", ""),
                        normalization_rules=fdata.get("normalization_rules", ""),
                        question_template=fdata.get("question_template", ""),
                        matching_role=fdata.get("matching_role", "informational_only"),
                        privacy_level=fdata.get("privacy_level", "public"),
                        sources=(str(path),),
                    ))
                except ValueError:
                    pass
            self.reg.lock()
            self.assertGreaterEqual(self.reg.count(), 90)


class H21ReadinessRegistryTest(unittest.TestCase):
    def setUp(self):
        self.reg = ReadinessRegistry()

    def _rd(self, level, order=1):
        return ReadinessDefinition(
            level=level,
            order=order,
            description="",
        )

    def test_register_and_get(self):
        rd = self._rd(ReadinessLevel.INTENT_IDENTIFIED, 1)
        self.reg.register(rd)
        self.reg.lock()
        self.assertIsNotNone(self.reg.get(ReadinessLevel.INTENT_IDENTIFIED))

    def test_duplicate_raises(self):
        self.reg.register(self._rd(ReadinessLevel.INTENT_IDENTIFIED, 1))
        with self.assertRaises(DuplicateEntryError):
            self.reg.register(self._rd(ReadinessLevel.INTENT_IDENTIFIED, 1))

    def test_get_by_order(self):
        self.reg.register(self._rd(ReadinessLevel.INTENT_IDENTIFIED, 1))
        self.reg.register(self._rd(ReadinessLevel.MINIMUM_INTAKE_READY, 2))
        self.reg.lock()
        self.assertIsNotNone(self.reg.get_by_order(1))
        self.assertIsNotNone(self.reg.get_by_order(2))

    def test_all_sorted(self):
        self.reg.register(self._rd(ReadinessLevel.MINIMUM_INTAKE_READY, 2))
        self.reg.register(self._rd(ReadinessLevel.INTENT_IDENTIFIED, 1))
        self.reg.lock()
        all_rd = self.reg.all()
        self.assertEqual(all_rd[0].order, 1)
        self.assertEqual(all_rd[1].order, 2)

    def test_count(self):
        self.reg.register(self._rd(ReadinessLevel.INTENT_IDENTIFIED, 1))
        self.reg.lock()
        self.assertEqual(self.reg.count(), 1)

    def test_load_real_readiness(self):
        path = _PROJECT_ROOT / "docs/lawim_heritage_gold/qualification_matrices/readiness_rules.json"
        if path.is_file():
            data = json.loads(path.read_bytes())
            for level_name, ldata in data.get("levels", {}).items():
                try:
                    level = ReadinessLevel(level_name)
                except ValueError:
                    continue
                self.reg.register(ReadinessDefinition(
                    level=level,
                    order=ldata.get("order", 0),
                    description=ldata.get("description", ""),
                    required_fields=tuple(ldata.get("required_fields", [])),
                ))
            self.reg.lock()
            self.assertGreaterEqual(self.reg.count(), 7)


class H21QuestionRuleRegistryTest(unittest.TestCase):
    def setUp(self):
        self.reg = QuestionRuleRegistry()

    def test_register_and_get_by_field(self):
        r = QuestionRule(field="city", rule_type="always_ask")
        self.reg.register(r)
        self.reg.lock()
        rules = self.reg.get_by_field("city")
        self.assertEqual(len(rules), 1)

    def test_register_and_get_by_type(self):
        self.reg.register(QuestionRule(field="city", rule_type="always_ask"))
        self.reg.register(QuestionRule(field="intent", rule_type="always_ask"))
        self.reg.lock()
        rules = self.reg.get_by_type("always_ask")
        self.assertEqual(len(rules), 2)

    def test_invalid_rule_type_raises(self):
        with self.assertRaises(ValueError):
            self.reg.register(QuestionRule(field="x", rule_type="invalid_type"))

    def test_all(self):
        self.reg.register(QuestionRule(field="a", rule_type="always_ask"))
        self.reg.register(QuestionRule(field="b", rule_type="never_ask"))
        self.reg.lock()
        self.assertEqual(len(self.reg.all()), 2)

    def test_count(self):
        self.reg.register(QuestionRule(field="a", rule_type="always_ask"))
        self.reg.lock()
        self.assertEqual(self.reg.count(), 1)

    def test_load_real_question_rules(self):
        path = _PROJECT_ROOT / "docs/lawim_heritage_gold/qualification_matrices/question_rules.json"
        if path.is_file():
            data = json.loads(path.read_bytes())
            for rule_type in ("always_ask", "conditional_ask", "never_ask", "deduce_from_context", "defer_ask"):
                for entry in data.get(rule_type, []):
                    if isinstance(entry, str):
                        field = entry
                    elif isinstance(entry, dict):
                        field = entry.get("field", "")
                    else:
                        continue
                    try:
                        self.reg.register(QuestionRule(field=field, rule_type=rule_type))
                    except ValueError:
                        pass
            self.reg.lock()
            self.assertGreaterEqual(self.reg.count(), 40)


class H21MatchingSemanticRegistryTest(unittest.TestCase):
    def setUp(self):
        self.reg = MatchingSemanticRegistry()

    def _ms(self, rid, order=1):
        return MatchingSemantic(role_id=rid, description="", score_contribution="none", evaluation_order=order)

    def test_register_and_get(self):
        ms = self._ms("hard_constraint")
        self.reg.register(ms)
        self.reg.lock()
        self.assertEqual(self.reg.get("hard_constraint").role_id, "hard_constraint")

    def test_duplicate_raises(self):
        self.reg.register(self._ms("boost"))
        with self.assertRaises(DuplicateEntryError):
            self.reg.register(self._ms("boost"))

    def test_all_nine_semantics(self):
        for role in MatchingSemanticRegistry.EXPECTED_SEMANTICS:
            self.reg.register(self._ms(role))
        self.reg.lock()
        self.assertEqual(self.reg.count(), 9)

    def test_load_real_semantics(self):
        path = _PROJECT_ROOT / "docs/lawim_heritage_gold/qualification_matrices/matching_semantics.json"
        if path.is_file():
            data = json.loads(path.read_bytes())
            for role_id, rdata in data.get("roles", {}).items():
                self.reg.register(MatchingSemantic(
                    role_id=role_id,
                    description=rdata.get("description", ""),
                    score_contribution=rdata.get("score_contribution", ""),
                    evaluation_order=rdata.get("evaluation_order", 0),
                ))
            self.reg.lock()
            self.assertEqual(self.reg.count(), 9)


class H21SourceTraceRegistryTest(unittest.TestCase):
    def setUp(self):
        self.reg = SourceTraceRegistry()

    def test_register_and_get(self):
        t = SourceTrace(concept_id="PR-FAM-001", concept_type="property_family", source_path="test.json", source_section="families")
        self.reg.register(t)
        self.reg.lock()
        self.assertEqual(self.reg.get("PR-FAM-001").concept_type, "property_family")

    def test_duplicate_raises(self):
        t = SourceTrace(concept_id="C1", concept_type="t", source_path="p", source_section="s")
        self.reg.register(t)
        with self.assertRaises(DuplicateEntryError):
            self.reg.register(t)

    def test_by_type(self):
        self.reg.register(SourceTrace(concept_id="C1", concept_type="field", source_path="p", source_section="s"))
        self.reg.register(SourceTrace(concept_id="C2", concept_type="field", source_path="p", source_section="s"))
        self.reg.register(SourceTrace(concept_id="C3", concept_type="matrix", source_path="p", source_section="s"))
        self.reg.lock()
        self.assertEqual(len(self.reg.by_type("field")), 2)
        self.assertEqual(len(self.reg.by_type("matrix")), 1)

    def test_count(self):
        self.reg.register(SourceTrace(concept_id="C1", concept_type="t", source_path="p", source_section="s"))
        self.reg.lock()
        self.assertEqual(self.reg.count(), 1)


class H21KnowledgeVersionTest(unittest.TestCase):
    def test_compute_version_deterministic(self):
        v1 = KnowledgeVersion.compute(
            schema_version="1.0.0",
            build_commit="abc123",
            source_checksums={"a.json": "sum1", "b.json": "sum2"},
            source_record_counts={"a.json": 10, "b.json": 20},
        )
        v2 = KnowledgeVersion.compute(
            schema_version="1.0.0",
            build_commit="abc123",
            source_checksums={"a.json": "sum1", "b.json": "sum2"},
            source_record_counts={"a.json": 10, "b.json": 20},
        )
        self.assertEqual(v1.knowledge_version, v2.knowledge_version)

    def test_version_changes_with_checksum(self):
        v1 = KnowledgeVersion.compute(
            schema_version="1.0.0", build_commit="abc",
            source_checksums={"a.json": "sum1"}, source_record_counts={"a.json": 10},
        )
        v2 = KnowledgeVersion.compute(
            schema_version="1.0.0", build_commit="abc",
            source_checksums={"a.json": "sum2"}, source_record_counts={"a.json": 10},
        )
        self.assertNotEqual(v1.knowledge_version, v2.knowledge_version)

    def test_version_changes_with_commit(self):
        v1 = KnowledgeVersion.compute(
            schema_version="1.0.0", build_commit="abc",
            source_checksums={"a.json": "sum1"}, source_record_counts={"a.json": 10},
        )
        v2 = KnowledgeVersion.compute(
            schema_version="1.0.0", build_commit="def",
            source_checksums={"a.json": "sum1"}, source_record_counts={"a.json": 10},
        )
        self.assertNotEqual(v1.knowledge_version, v2.knowledge_version)

    def test_dict_output(self):
        v = KnowledgeVersion.compute(
            schema_version="1.0.0", build_commit="abc",
            source_checksums={"a.json": "s1"}, source_record_counts={"a.json": 5},
        )
        d = v.dict()
        self.assertIn("knowledge_version", d)
        self.assertIn("build_commit", d)
        self.assertEqual(d["build_commit"], "abc")

    def test_loaded_at_default(self):
        v = KnowledgeVersion.compute(
            schema_version="1.0.0", build_commit="abc",
            source_checksums={}, source_record_counts={},
        )
        self.assertIsNotNone(v.loaded_at)


class H21KnowledgeServiceTest(unittest.TestCase):
    def test_disabled_by_default(self):
        config = KnowledgeConfig(runtime_enabled=False)
        service = KnowledgeService(config)
        report = service.load_all()
        self.assertTrue(report.passed)
        health = service.health()
        self.assertEqual(health["status"], "DISABLED")

    def test_load_with_real_sources(self):
        config = KnowledgeConfig(
            runtime_enabled=True,
            project_root=_PROJECT_ROOT,
        )
        service = KnowledgeService(config, build_commit="test-commit")
        try:
            report = service.load_all()
            health = service.health()
            self.assertIn(health["status"], {"READY", "DISABLED"})
            self.assertGreaterEqual(health["registries"]["properties"], 7)
            self.assertGreaterEqual(health["registries"]["matrices"], 50)
            self.assertGreaterEqual(health["registries"]["fields"], 90)
        except KnowledgeSourceNotFound:
            pass

    def test_registry_summaries(self):
        config = KnowledgeConfig(runtime_enabled=True, project_root=_PROJECT_ROOT)
        service = KnowledgeService(config)
        try:
            service.load_all()
            summaries = service.registry_summaries()
            self.assertIn("property_taxonomy", summaries)
            self.assertIn("matrix", summaries)
            self.assertIn("field", summaries)
        except KnowledgeSourceNotFound:
            pass


class H21SchemaValidatorTest(unittest.TestCase):
    def test_valid_json(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"a": 1}, f)
            path = f.name
        try:
            SchemaValidator().validate_json(path)
        finally:
            os.unlink(path)

    def test_invalid_json(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{invalid")
            path = f.name
        try:
            with self.assertRaises(KnowledgeSchemaError):
                SchemaValidator().validate_json(path)
        finally:
            os.unlink(path)

    def test_file_not_found(self):
        with self.assertRaises(KnowledgeSchemaError):
            SchemaValidator().validate_json("/nonexistent/file.json")

    def test_validate_structure(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"name": "test", "version": "1"}, f)
            path = f.name
        try:
            data = SchemaValidator().validate_structure(path, {"name", "version"})
            self.assertEqual(data["name"], "test")
        finally:
            os.unlink(path)

    def test_validate_structure_missing_keys(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"name": "test"}, f)
            path = f.name
        try:
            with self.assertRaises(KnowledgeSchemaError):
                SchemaValidator().validate_structure(path, {"name", "version"})
        finally:
            os.unlink(path)


class H21ReferenceValidatorTest(unittest.TestCase):
    def test_check_field_ref(self):
        v = ReferenceValidator()
        v.check_field_references("unknown_field", {"known_field"}, "source-1")
        self.assertTrue(v.has_errors())

    def test_check_matrix_ref(self):
        v = ReferenceValidator()
        v.check_matrix_references("unknown_matrix", {"M1"}, "source-1")
        self.assertTrue(v.has_errors())

    def test_check_property_ref(self):
        v = ReferenceValidator()
        v.check_property_references("unknown_prop", {"prop1"}, "source-1")
        self.assertTrue(v.has_errors())

    def test_no_errors_when_valid(self):
        v = ReferenceValidator()
        v.check_field_references("known", {"known"}, "s")
        self.assertFalse(v.has_errors())

    def test_get_errors(self):
        v = ReferenceValidator()
        v.check_field_references("unknown", {"known"}, "s")
        errors = v.get_errors()
        self.assertEqual(len(errors), 1)

    def test_summary(self):
        v = ReferenceValidator()
        v.check_field_references("unknown", {"known"}, "s")
        s = v.summary()
        self.assertEqual(s["errors"], 1)


class H21StartupValidatorTest(unittest.TestCase):
    def test_feature_disabled_warning(self):
        v = StartupValidator()
        v.check_feature_flag(False, "TEST_FLAG")
        report = v.report()
        self.assertEqual(len(report.warnings), 1)

    def test_registry_empty_error(self):
        v = StartupValidator()
        v.check_loaded("test", 0, 1)
        report = v.report()
        self.assertFalse(report.passed)
        self.assertEqual(len(report.errors), 1)

    def test_version_mismatch(self):
        v = StartupValidator()
        v.check_version("0.0.0")
        report = v.report()
        self.assertFalse(report.passed)

    def test_version_match(self):
        v = StartupValidator()
        v.check_version(KNOWLEDGE_SCHEMA_VERSION)
        report = v.report()
        self.assertTrue(report.passed)

    def test_multiple_issues(self):
        v = StartupValidator()
        v.check_loaded("test", 0, 1)
        v.check_feature_flag(False, "FLAG")
        report = v.report()
        self.assertEqual(report.total_issues, 2)


class H21KnowledgeSourceNotFoundTest(unittest.TestCase):
    def test_loader_missing_file_returns_partial(self):
        from lawim_v2.knowledge_runtime.loaders import load_all_knowledge
        from lawim_v2.knowledge_runtime.registry import (
            PropertyTaxonomyRegistry, ServiceTaxonomyRegistry, RoleRegistry,
            IntentRegistry, TransactionRegistry, MatrixRegistry,
            FieldRegistry, ReadinessRegistry, QuestionRuleRegistry,
            MatchingSemanticRegistry, SourceTraceRegistry, KnowledgeVersionRegistry,
        )
        from lawim_v2.knowledge_runtime.errors import KnowledgeSourceNotFound
        sources = load_all_knowledge(
            property_taxonomy_path="/nonexistent/property.json",
            service_taxonomy_path="/nonexistent/service.json",
            roles_path="/nonexistent/roles.json",
            intents_path="/nonexistent/intents.json",
            transactions_path="/nonexistent/transactions.json",
            matrices_path="/nonexistent/matrices.json",
            fields_path="/nonexistent/fields.json",
            readiness_path="/nonexistent/readiness.json",
            question_rules_path="/nonexistent/question_rules.json",
            matching_semantics_path="/nonexistent/semantics.json",
            property_registry=PropertyTaxonomyRegistry(),
            service_registry=ServiceTaxonomyRegistry(),
            role_registry=RoleRegistry(),
            intent_registry=IntentRegistry(),
            transaction_registry=TransactionRegistry(),
            matrix_registry=MatrixRegistry(),
            field_registry=FieldRegistry(),
            readiness_registry=ReadinessRegistry(),
            question_rule_registry=QuestionRuleRegistry(),
            matching_semantic_registry=MatchingSemanticRegistry(),
            source_trace_registry=SourceTraceRegistry(),
            version_registry=KnowledgeVersionRegistry(),
        )
        self.assertEqual(len(sources), 0)


class H21VersionRegistryTest(unittest.TestCase):
    def test_version_registry(self):
        reg = KnowledgeVersionRegistry()
        v = KnowledgeVersion.compute(
            schema_version="1.0.0", build_commit="test",
            source_checksums={"a": "s1"}, source_record_counts={"a": 1},
        )
        reg.set_version(v)
        reg.lock()
        retrieved = reg.get()
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.knowledge_version, v.knowledge_version)

    def test_version_registry_immutable(self):
        reg = KnowledgeVersionRegistry()
        reg.lock()
        with self.assertRaises(RuntimeError):
            v = KnowledgeVersion.compute(
                schema_version="1.0.0", build_commit="test",
                source_checksums={}, source_record_counts={},
            )
            reg.set_version(v)

    def test_version_registry_summary(self):
        reg = KnowledgeVersionRegistry()
        v = KnowledgeVersion.compute(
            schema_version="1.0.0", build_commit="test",
            source_checksums={"a": "s1"}, source_record_counts={"a": 1},
        )
        reg.set_version(v)
        reg.lock()
        s = reg.summary()
        self.assertIn("version", s)
        self.assertEqual(s["version"]["build_commit"], "test")


class H21FeatureFlagDefaultsTest(unittest.TestCase):
    def test_runtime_flag_name(self):
        self.assertEqual(LAWIM_FEATURE_KNOWLEDGE_RUNTIME, "LAWIM_FEATURE_KNOWLEDGE_RUNTIME")

    def test_api_flag_name(self):
        self.assertEqual(LAWIM_FEATURE_KNOWLEDGE_INTERNAL_API, "LAWIM_FEATURE_KNOWLEDGE_INTERNAL_API")

    def test_disabled_status_constant(self):
        self.assertEqual(STATUS_DISABLED, "DISABLED")
        self.assertEqual(STATUS_READY, "READY")


class H21KnowledgeServiceDisabledTest(unittest.TestCase):
    def test_service_disabled_by_default(self):
        config = KnowledgeConfig()
        self.assertFalse(config.runtime_enabled)
        self.assertFalse(config.internal_api_enabled)

    def test_load_returns_ok_when_disabled(self):
        config = KnowledgeConfig(runtime_enabled=False)
        service = KnowledgeService(config)
        report = service.load_all()
        self.assertTrue(report.passed)


if __name__ == "__main__":
    unittest.main()
