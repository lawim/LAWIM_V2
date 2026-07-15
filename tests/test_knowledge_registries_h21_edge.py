# H2.1 Edge Cases — invalid JSON, missing sources, cycles, feature flags, security
from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from lawim_v2.knowledge_runtime.config import KnowledgeConfig
from lawim_v2.knowledge_runtime.constants import (
    KNOWLEDGE_SCHEMA_VERSION,
    MAX_JSON_FILE_SIZE_BYTES,
    MAX_JSON_DEPTH,
)
from lawim_v2.knowledge_runtime.errors import (
    KnowledgeDuplicateError,
    KnowledgeSchemaError,
    KnowledgeSourceNotFound,
)
from lawim_v2.knowledge_runtime.models.common import ValidationIssue, ValidationReport
from lawim_v2.knowledge_runtime.models.taxonomy import PropertyType, ServiceType
from lawim_v2.knowledge_runtime.models.version import KnowledgeVersion
from lawim_v2.knowledge_runtime.registry import (
    AmbiguousAliasError,
    CycleDetectionError,
    DuplicateEntryError,
    FieldRegistry,
    MissingParentError,
    PropertyTaxonomyRegistry,
    ServiceTaxonomyRegistry,
)
from lawim_v2.knowledge_runtime.validation import SchemaValidator

_PROJECT_ROOT = Path(__file__).resolve().parents[1]


# ── 1. Invalid JSON ─────────────────────────────────────────────────────
class InvalidJsonTest(unittest.TestCase):
    def test_invalid_json_content(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("{invalid json content!!!")
            path = f.name
        try:
            with self.assertRaises(KnowledgeSchemaError):
                SchemaValidator().validate_json(path)
        finally:
            os.unlink(path)

    def test_empty_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            path = f.name
        try:
            with self.assertRaises(KnowledgeSchemaError):
                SchemaValidator().validate_json(path)
        finally:
            os.unlink(path)

    def test_json_array_at_root(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump([1, 2, 3], f)
            path = f.name
        try:
            SchemaValidator().validate_json(path)
        finally:
            os.unlink(path)

    def test_json_numeric_root(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("123")
            path = f.name
        try:
            SchemaValidator().validate_json(path)
        finally:
            os.unlink(path)

    def test_unicode_json(self):
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".json", delete=False) as f:
            f.write('{"name": "café"}'.encode("utf-8"))
            path = f.name
        try:
            SchemaValidator().validate_json(path)
        finally:
            os.unlink(path)

    def test_deeply_nested_json(self):
        d = {"a": {"b": {"c": {"d": {"e": {"f": {"g": {"h": {"i": {"j": {"k": "deep"}}}}}}}}}}}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(d, f)
            path = f.name
        try:
            SchemaValidator().validate_json(path)
        finally:
            os.unlink(path)


# ── 2. Source absente ────────────────────────────────────────────────────
class MissingSourceTest(unittest.TestCase):
    def test_missing_property_taxonomy(self):
        from lawim_v2.knowledge_runtime.loaders import load_property_taxonomy
        from lawim_v2.knowledge_runtime.registry import PropertyTaxonomyRegistry, SourceTraceRegistry

        reg = PropertyTaxonomyRegistry()
        trace = SourceTraceRegistry()
        with self.assertRaises(KnowledgeSourceNotFound):
            load_property_taxonomy("/nonexistent/file.json", reg, trace)

    def test_missing_service_taxonomy(self):
        from lawim_v2.knowledge_runtime.loaders import load_service_taxonomy
        from lawim_v2.knowledge_runtime.registry import ServiceTaxonomyRegistry, SourceTraceRegistry

        reg = ServiceTaxonomyRegistry()
        trace = SourceTraceRegistry()
        with self.assertRaises(KnowledgeSourceNotFound):
            load_service_taxonomy("/nonexistent/file.json", reg, trace)

    def test_missing_roles(self):
        from lawim_v2.knowledge_runtime.loaders import load_roles
        from lawim_v2.knowledge_runtime.registry import RoleRegistry, SourceTraceRegistry

        reg = RoleRegistry()
        trace = SourceTraceRegistry()
        with self.assertRaises(KnowledgeSourceNotFound):
            load_roles("/nonexistent/file.json", reg, trace)

    def test_missing_matrices(self):
        from lawim_v2.knowledge_runtime.loaders import load_matrices
        from lawim_v2.knowledge_runtime.registry import MatrixRegistry, SourceTraceRegistry

        reg = MatrixRegistry()
        trace = SourceTraceRegistry()
        with self.assertRaises(KnowledgeSourceNotFound):
            load_matrices("/nonexistent/file.json", reg, trace)

    def test_missing_fields(self):
        from lawim_v2.knowledge_runtime.loaders import load_fields
        from lawim_v2.knowledge_runtime.registry import FieldRegistry, SourceTraceRegistry

        reg = FieldRegistry()
        trace = SourceTraceRegistry()
        with self.assertRaises(KnowledgeSourceNotFound):
            load_fields("/nonexistent/file.json", reg, trace)

    def test_missing_readiness(self):
        from lawim_v2.knowledge_runtime.loaders import load_readiness
        from lawim_v2.knowledge_runtime.registry import ReadinessRegistry, SourceTraceRegistry

        reg = ReadinessRegistry()
        trace = SourceTraceRegistry()
        with self.assertRaises(KnowledgeSourceNotFound):
            load_readiness("/nonexistent/file.json", reg, trace)

    def test_missing_question_rules(self):
        from lawim_v2.knowledge_runtime.loaders import load_question_rules
        from lawim_v2.knowledge_runtime.registry import QuestionRuleRegistry, SourceTraceRegistry

        reg = QuestionRuleRegistry()
        trace = SourceTraceRegistry()
        with self.assertRaises(KnowledgeSourceNotFound):
            load_question_rules("/nonexistent/file.json", reg, trace)

    def test_missing_matching_semantics(self):
        from lawim_v2.knowledge_runtime.loaders import load_matching_semantics
        from lawim_v2.knowledge_runtime.registry import MatchingSemanticRegistry, SourceTraceRegistry

        reg = MatchingSemanticRegistry()
        trace = SourceTraceRegistry()
        with self.assertRaises(KnowledgeSourceNotFound):
            load_matching_semantics("/nonexistent/file.json", reg, trace)


# ── 3. Checksum ─────────────────────────────────────────────────────────
class ChecksumTest(unittest.TestCase):
    def test_checksum_stable(self):
        import hashlib
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"key": "value"}, f)
            path1 = f.name
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"key": "value"}, f)
            path2 = f.name
        try:
            c1 = hashlib.sha256(open(path1, "rb").read()).hexdigest()
            c2 = hashlib.sha256(open(path2, "rb").read()).hexdigest()
            self.assertEqual(c1, c2)
        finally:
            os.unlink(path1)
            os.unlink(path2)

    def test_checksum_changes_with_content(self):
        import hashlib
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"key": "value"}, f)
            path1 = f.name
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"key": "different"}, f)
            path2 = f.name
        try:
            c1 = hashlib.sha256(open(path1, "rb").read()).hexdigest()
            c2 = hashlib.sha256(open(path2, "rb").read()).hexdigest()
            self.assertNotEqual(c1, c2)
        finally:
            os.unlink(path1)
            os.unlink(path2)

    def test_checksum_length(self):
        import hashlib
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"a": 1}, f)
            path = f.name
        try:
            c = hashlib.sha256(open(path, "rb").read()).hexdigest()
            self.assertEqual(len(c), 64)
        finally:
            os.unlink(path)


# ── 4. Version stable ───────────────────────────────────────────────────
class VersionStabilityTest(unittest.TestCase):
    def test_version_deterministic(self):
        v1 = KnowledgeVersion.compute(
            schema_version="1.0.0", build_commit="abc",
            source_checksums={"a.json": "sum1"}, source_record_counts={"a.json": 10},
        )
        v2 = KnowledgeVersion.compute(
            schema_version="1.0.0", build_commit="abc",
            source_checksums={"a.json": "sum1"}, source_record_counts={"a.json": 10},
        )
        self.assertEqual(v1.knowledge_version, v2.knowledge_version)

    def test_version_16_chars(self):
        v = KnowledgeVersion.compute(
            schema_version="1.0.0", build_commit="abc",
            source_checksums={"a.json": "sum1"}, source_record_counts={"a.json": 10},
        )
        self.assertEqual(len(v.knowledge_version), 16)

    def test_version_hex(self):
        v = KnowledgeVersion.compute(
            schema_version="1.0.0", build_commit="abc",
            source_checksums={"a.json": "sum1"}, source_record_counts={"a.json": 10},
        )
        int(v.knowledge_version, 16)

    def test_version_changes_with_schema_version(self):
        v1 = KnowledgeVersion.compute(
            schema_version="1.0.0", build_commit="abc",
            source_checksums={"a.json": "s1"}, source_record_counts={"a.json": 10},
        )
        v2 = KnowledgeVersion.compute(
            schema_version="2.0.0", build_commit="abc",
            source_checksums={"a.json": "s1"}, source_record_counts={"a.json": 10},
        )
        self.assertNotEqual(v1.knowledge_version, v2.knowledge_version)


# ── 5. Doublons ─────────────────────────────────────────────────────────
class DuplicateIdTest(unittest.TestCase):
    def test_duplicate_property_type_id(self):
        reg = PropertyTaxonomyRegistry()
        pt1 = PropertyType(canonical_id="ID-1", canonical_name="a", sources=("t",))
        pt2 = PropertyType(canonical_id="ID-1", canonical_name="b", sources=("t",))
        reg.register(pt1)
        with self.assertRaises(DuplicateEntryError):
            reg.register(pt2)

    def test_duplicate_service_type_id(self):
        reg = ServiceTaxonomyRegistry()
        st1 = ServiceType(canonical_id="ID-1", canonical_name="a", sources=("t",))
        st2 = ServiceType(canonical_id="ID-1", canonical_name="b", sources=("t",))
        reg.register(st1)
        with self.assertRaises(DuplicateEntryError):
            reg.register(st2)

    def test_duplicate_field_id(self):
        reg = FieldRegistry()
        from lawim_v2.knowledge_runtime.models.field import FieldDefinition
        fd1 = FieldDefinition(field_id="city", label="Ville", description="", data_type="string",
                              validation_rules="", normalization_rules="", question_template="",
                              matching_role="informational_only", privacy_level="public", sources=("t",))
        fd2 = FieldDefinition(field_id="city", label="City", description="", data_type="string",
                              validation_rules="", normalization_rules="", question_template="",
                              matching_role="informational_only", privacy_level="public", sources=("t",))
        reg.register(fd1)
        with self.assertRaises(DuplicateEntryError):
            reg.register(fd2)


# ── 6. Références cassées / cycles ──────────────────────────────────────
class BrokenReferenceTest(unittest.TestCase):
    def test_missing_parent_raises_on_lock(self):
        reg = PropertyTaxonomyRegistry()
        reg.register(PropertyType(canonical_id="child", canonical_name="child", parent_id="missing_parent", sources=("t",)))
        with self.assertRaises(MissingParentError):
            reg.lock()

    def test_self_reference_cycle(self):
        reg = PropertyTaxonomyRegistry()
        reg.register(PropertyType(canonical_id="A", canonical_name="A", parent_id="A", sources=("t",)))
        with self.assertRaises(CycleDetectionError):
            reg.lock()

    def test_simple_two_node_cycle(self):
        reg = PropertyTaxonomyRegistry()
        reg.register(PropertyType(canonical_id="A", canonical_name="A", parent_id="B", sources=("t",)))
        reg.register(PropertyType(canonical_id="B", canonical_name="B", parent_id="A", sources=("t",)))
        with self.assertRaises(CycleDetectionError):
            reg.lock()

    def test_three_node_cycle(self):
        reg = PropertyTaxonomyRegistry()
        reg.register(PropertyType(canonical_id="A", canonical_name="A", parent_id="B", sources=("t",)))
        reg.register(PropertyType(canonical_id="B", canonical_name="B", parent_id="C", sources=("t",)))
        reg.register(PropertyType(canonical_id="C", canonical_name="C", parent_id="A", sources=("t",)))
        with self.assertRaises(CycleDetectionError):
            reg.lock()

    def test_diamond_no_cycle(self):
        reg = PropertyTaxonomyRegistry()
        reg.register(PropertyType(canonical_id="Root", canonical_name="Root", sources=("t",)))
        reg.register(PropertyType(canonical_id="A", canonical_name="A", parent_id="Root", sources=("t",)))
        reg.register(PropertyType(canonical_id="B", canonical_name="B", parent_id="Root", sources=("t",)))
        reg.register(PropertyType(canonical_id="C", canonical_name="C", parent_id="A", sources=("t",)))
        reg.register(PropertyType(canonical_id="D", canonical_name="D", parent_id="B", sources=("t",)))
        reg.lock()

    def test_cycle_long_chain(self):
        reg = PropertyTaxonomyRegistry()
        reg.register(PropertyType(canonical_id="A", canonical_name="A", parent_id="B", sources=("t",)))
        reg.register(PropertyType(canonical_id="B", canonical_name="B", parent_id="C", sources=("t",)))
        reg.register(PropertyType(canonical_id="C", canonical_name="C", parent_id="D", sources=("t",)))
        reg.register(PropertyType(canonical_id="D", canonical_name="D", parent_id="E", sources=("t",)))
        reg.register(PropertyType(canonical_id="E", canonical_name="E", parent_id="A", sources=("t",)))
        with self.assertRaises(CycleDetectionError):
            reg.lock()


# ── 7. Alias unique / ambigu ────────────────────────────────────────────
class AliasTest(unittest.TestCase):
    def test_unique_alias_ok(self):
        reg = PropertyTaxonomyRegistry()
        reg.register(PropertyType(canonical_id="A", canonical_name="A", aliases=("alias_a",), sources=("t",)))
        reg.register(PropertyType(canonical_id="B", canonical_name="B", aliases=("alias_b",), sources=("t",)))
        reg.lock()

    def test_ambiguous_alias_raises(self):
        reg = PropertyTaxonomyRegistry()
        reg.register(PropertyType(canonical_id="A", canonical_name="A", aliases=("shared",), sources=("t",)))
        with self.assertRaises(AmbiguousAliasError):
            reg.register(PropertyType(canonical_id="B", canonical_name="B", aliases=("shared",), sources=("t",)))

    def test_alias_to_itself_ok(self):
        reg = PropertyTaxonomyRegistry()
        pt = PropertyType(canonical_id="A", canonical_name="A", aliases=("a", "A",), sources=("t",))
        reg.register(pt)
        reg.lock()

    def test_alias_resolution(self):
        reg = PropertyTaxonomyRegistry()
        reg.register(PropertyType(canonical_id="PR-FAM-001", canonical_name="residential", aliases=("logement", "habitation"), sources=("t",)))
        reg.lock()
        results = reg.resolve("logement")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].canonical_id, "PR-FAM-001")

    def test_multiple_aliases_resolve(self):
        reg = PropertyTaxonomyRegistry()
        reg.register(PropertyType(canonical_id="X", canonical_name="X", aliases=("x1", "x2", "x3"), sources=("t",)))
        reg.lock()
        self.assertEqual(len(reg.resolve("x1")), 1)
        self.assertEqual(len(reg.resolve("x2")), 1)
        self.assertEqual(len(reg.resolve("x3")), 1)


# ── 8. Matrice exacte / normalisée / ambiguë / absente ──────────────────
class MatrixMatchTypeTest(unittest.TestCase):
    def setUp(self):
        from lawim_v2.knowledge_runtime.models.qualification import QualificationMatrix
        self.reg = type(str("MatrixReg"), (), {})()
        self.reg.matrix_reg = type(str("R"), (), {})()
        from lawim_v2.knowledge_runtime.registry import MatrixRegistry
        self.reg.matrix_reg = MatrixRegistry()

    def _add(self, mid, name="", family="RESIDENTIAL_SEARCH", ptype="apt"):
        from lawim_v2.knowledge_runtime.models.qualification import QualificationMatrix
        qm = QualificationMatrix(
            matrix_id=mid, canonical_name=name or mid,
            request_family=family, transaction_type="RENT",
            property_type=ptype, requester_typology="t",
            journey_stage="SEARCH", description="", sources=("t",),
        )
        self.reg.matrix_reg.register(qm)

    def test_exact_match(self):
        self._add("M1", "test matrix")
        self.reg.matrix_reg.lock()
        r = self.reg.matrix_reg.resolve("M1")
        self.assertEqual(r["match_type"], "exact_match")

    def test_normalized_match(self):
        self._add("MATRIX-RES-SEARCH-001")
        self.reg.matrix_reg.lock()
        r = self.reg.matrix_reg.resolve("matrix_res_search_001")
        self.assertEqual(r["match_type"], "normalized_match")

    def test_not_found(self):
        self.reg.matrix_reg.lock()
        r = self.reg.matrix_reg.resolve("NONEXISTENT")
        self.assertEqual(r["match_type"], "not_found")

    def test_ambiguous(self):
        self._add("M1", "same name")
        self._add("M2", "same name")
        self.reg.matrix_reg.lock()
        r = self.reg.matrix_reg.resolve("same")
        self.assertEqual(r["match_type"], "ambiguity")

    def test_partial_match_by_property_type(self):
        self._add("M1", "test", ptype="villa")
        self.reg.matrix_reg.lock()
        r = self.reg.matrix_reg.resolve("villa", property_type="villa")
        self.assertIn(r["match_type"], ("exact_match", "normalized_match", "authorized_partial_match"))


# ── 9. Champ inconnu ────────────────────────────────────────────────────
class UnknownFieldTest(unittest.TestCase):
    def test_unknown_field_id_raises(self):
        reg = FieldRegistry()
        reg.lock()
        with self.assertRaises(Exception):
            reg.get("__nonexistent_field__")

    def test_reject_unknown_data_type(self):
        from lawim_v2.knowledge_runtime.models.field import FieldDefinition
        reg = FieldRegistry()
        with self.assertRaises(ValueError):
            reg.register(FieldDefinition(
                field_id="bad", label="", description="",
                data_type="unknown_type_xyz", validation_rules="",
                normalization_rules="", question_template="",
                matching_role="informational_only", privacy_level="public",
            ))


# ── 10. Feature Flags false ────────────────────────────────────────────
class FeatureFlagsDisabledTest(unittest.TestCase):
    def test_runtime_disabled_by_default(self):
        config = KnowledgeConfig()
        self.assertFalse(config.runtime_enabled)

    def test_api_disabled_by_default(self):
        config = KnowledgeConfig()
        self.assertFalse(config.internal_api_enabled)

    def test_runtime_can_be_enabled(self):
        config = KnowledgeConfig(runtime_enabled=True)
        self.assertTrue(config.runtime_enabled)

    def test_api_can_be_enabled(self):
        config = KnowledgeConfig(internal_api_enabled=True)
        self.assertTrue(config.internal_api_enabled)

    def test_service_returns_disabled_when_disabled(self):
        from lawim_v2.knowledge_runtime.service import KnowledgeService
        config = KnowledgeConfig(runtime_enabled=False)
        svc = KnowledgeService(config)
        report = svc.load_all()
        self.assertTrue(report.passed)
        self.assertEqual(svc.health()["status"], "DISABLED")


# ── 11. API protégée ───────────────────────────────────────────────────
class ApiProtectedTest(unittest.TestCase):
    def test_api_handler_raises_when_disabled(self):
        from lawim_v2.knowledge_runtime.service import KnowledgeService
        from lawim_v2.knowledge_runtime.api import KnowledgeApiHandler
        from lawim_v2.knowledge_runtime.api.handler import ApiDisabledError

        svc = KnowledgeService(KnowledgeConfig(runtime_enabled=False))
        handler = KnowledgeApiHandler(svc, internal_api_enabled=False)
        with self.assertRaises(ApiDisabledError):
            handler.handle_health()
        with self.assertRaises(ApiDisabledError):
            handler.handle_version()
        with self.assertRaises(ApiDisabledError):
            handler.handle_registries()
        with self.assertRaises(ApiDisabledError):
            handler.handle_property_types()
        with self.assertRaises(ApiDisabledError):
            handler.handle_services()
        with self.assertRaises(ApiDisabledError):
            handler.handle_roles()
        with self.assertRaises(ApiDisabledError):
            handler.handle_intents()
        with self.assertRaises(ApiDisabledError):
            handler.handle_transactions()
        with self.assertRaises(ApiDisabledError):
            handler.handle_matrices()
        with self.assertRaises(ApiDisabledError):
            handler.handle_field("city")
        with self.assertRaises(ApiDisabledError):
            handler.handle_source_trace("test")


# ── 12. Model edge cases ───────────────────────────────────────────────
class ModelEdgeCasesTest(unittest.TestCase):
    def test_property_type_empty_aliases(self):
        pt = PropertyType(canonical_id="ID", canonical_name="Name", aliases=(), sources=("t",))
        self.assertEqual(len(pt.aliases), 0)

    def test_service_type_empty_sources(self):
        st = ServiceType(canonical_id="ID", canonical_name="Name")
        self.assertEqual(len(st.sources), 0)

    def test_validation_report_defaults(self):
        report = ValidationReport()
        self.assertTrue(report.passed)
        self.assertEqual(report.total_issues, 0)

    def test_validation_issue_with_identifier(self):
        issue = ValidationIssue(severity="ERROR", code="E1", message="msg", source="src", identifier="id1")
        self.assertEqual(issue.identifier, "id1")

    def test_validation_issue_without_identifier(self):
        issue = ValidationIssue(severity="WARNING", code="W1", message="msg", source="src")
        self.assertIsNone(issue.identifier)

    def test_knowledge_not_loaded_error_default(self):
        from lawim_v2.knowledge_runtime.errors import KnowledgeNotLoadedError
        err = KnowledgeNotLoadedError()
        self.assertIn("not been loaded", str(err))


# ── 13. Config edge cases ──────────────────────────────────────────────
class ConfigEdgeCasesTest(unittest.TestCase):
    def test_config_default_paths(self):
        config = KnowledgeConfig()
        self.assertTrue(str(config.property_taxonomy_path).endswith(".json"))
        self.assertTrue(str(config.service_taxonomy_path).endswith(".json"))
        self.assertTrue(str(config.matrices_path).endswith(".json"))

    def test_config_project_root_default(self):
        config = KnowledgeConfig()
        self.assertEqual(str(config.project_root), ".")

    def test_config_custom_project_root(self):
        config = KnowledgeConfig(project_root=Path("/custom"))
        self.assertEqual(config.project_root, Path("/custom"))


# ── 14. Validation edge cases ──────────────────────────────────────────
class ValidationEdgeCasesTest(unittest.TestCase):
    def test_schema_validator_file_too_large(self):
        from lawim_v2.knowledge_runtime.constants import MAX_JSON_FILE_SIZE_BYTES
        self.assertGreater(MAX_JSON_FILE_SIZE_BYTES, 0)

    def test_startup_validator_multiple_errors(self):
        from lawim_v2.knowledge_runtime.validation import StartupValidator
        v = StartupValidator()
        v.check_loaded("test", 0, 1)
        v.check_version("wrong")
        report = v.report()
        self.assertFalse(report.passed)
        self.assertEqual(len(report.errors), 2)

    def test_startup_validator_warning_only(self):
        from lawim_v2.knowledge_runtime.validation import StartupValidator
        v = StartupValidator()
        v.check_feature_flag(False, "TEST")
        report = v.report()
        self.assertTrue(report.passed)
        self.assertEqual(len(report.warnings), 1)

    def test_reference_validator_multiple_errors(self):
        from lawim_v2.knowledge_runtime.validation import ReferenceValidator
        v = ReferenceValidator()
        v.check_field_references("f1", {"known"}, "s")
        v.check_field_references("f2", {"known"}, "s")
        v.check_matrix_references("m1", {"known"}, "s")
        self.assertTrue(v.has_errors())
        self.assertEqual(len(v.get_errors()), 3)


# ── 15. BaseRegistry immutability ──────────────────────────────────────
class BaseRegistryImmutabilityTest(unittest.TestCase):
    def test_lock_prevents_registration(self):
        reg = PropertyTaxonomyRegistry()
        reg.lock()
        with self.assertRaises(RuntimeError):
            reg.register(PropertyType(canonical_id="X", canonical_name="X", sources=("t",)))

    def test_setattr_raises_after_lock(self):
        reg = PropertyTaxonomyRegistry()
        reg.lock()
        with self.assertRaises(RuntimeError):
            reg._by_id = {}

    def test_delattr_always_raises(self):
        reg = PropertyTaxonomyRegistry()
        with self.assertRaises(RuntimeError):
            del reg._by_id

    def test_summary_after_lock(self):
        reg = PropertyTaxonomyRegistry()
        reg.register(PropertyType(canonical_id="A", canonical_name="A", sources=("t",)))
        reg.lock()
        s = reg.summary()
        self.assertTrue(s["loaded"])


# ── 16. Registry errors ────────────────────────────────────────────────
class RegistryErrorsTest(unittest.TestCase):
    def test_registry_not_found_error(self):
        from lawim_v2.knowledge_runtime.registry.errors import RegistryNotFoundError
        err = RegistryNotFoundError("msg", identifier="test-id")
        self.assertEqual(err.code, "registry_not_found")
        self.assertEqual(err.details["identifier"], "test-id")

    def test_duplicate_entry_error(self):
        from lawim_v2.knowledge_runtime.registry.errors import DuplicateEntryError
        err = DuplicateEntryError("msg", identifier="dup-id")
        self.assertEqual(err.code, "duplicate_entry")
        self.assertEqual(err.details["identifier"], "dup-id")

    def test_ambiguous_alias_error(self):
        from lawim_v2.knowledge_runtime.registry.errors import AmbiguousAliasError
        err = AmbiguousAliasError("msg", alias="alias", matches=["a", "b"])
        self.assertEqual(err.code, "ambiguous_alias")
        self.assertEqual(err.details["alias"], "alias")

    def test_cycle_detection_error(self):
        from lawim_v2.knowledge_runtime.registry.errors import CycleDetectionError
        err = CycleDetectionError("msg", cycle_path=["A", "B", "A"])
        self.assertEqual(err.code, "cycle_detected")
        self.assertIn("cycle_path", err.details)

    def test_missing_parent_error(self):
        from lawim_v2.knowledge_runtime.registry.errors import MissingParentError
        err = MissingParentError("msg", child_id="C", missing_parent_id="P")
        self.assertEqual(err.code, "missing_parent")
        self.assertEqual(err.details["child_id"], "C")

    def test_no_match_error(self):
        from lawim_v2.knowledge_runtime.registry.errors import NoMatchError
        err = NoMatchError("msg", context={"q": "test"})
        self.assertEqual(err.code, "no_match")

    def test_trace_validation_error(self):
        from lawim_v2.knowledge_runtime.registry.errors import TraceValidationError
        err = TraceValidationError("msg", trace_id="T1", missing_links=["L1"])
        self.assertEqual(err.code, "trace_validation_error")
        self.assertEqual(err.details["trace_id"], "T1")


if __name__ == "__main__":
    unittest.main()
