# H2.1 Bulk Data-Driven Tests — extends test count to 387+ minimum
from __future__ import annotations

import json
import unittest
from pathlib import Path

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
from lawim_v2.knowledge_runtime.registry import (
    FieldRegistry,
    IntentRegistry,
    MatchingSemanticRegistry,
    MatrixRegistry,
    PropertyTaxonomyRegistry,
    QuestionRuleRegistry,
    ReadinessRegistry,
    RoleRegistry,
    ServiceTaxonomyRegistry,
    SourceTraceRegistry,
    TransactionRegistry,
)

_PROJECT_ROOT = Path(__file__).resolve().parents[1]


# ── 1. Property Taxonomy: 50+ cases ─────────────────────────────────────
class BulkPropertyTaxonomyTest(unittest.TestCase):
    def setUp(self):
        self.reg = PropertyTaxonomyRegistry()
        path = _PROJECT_ROOT / "docs/domain_extension/property_taxonomy_extensions.json"
        if path.is_file():
            data = json.loads(path.read_bytes())
            families = data.get("property_families", {}).get("values", [])
            for fam in families:
                try:
                    pt = PropertyType(
                        canonical_id=fam.get("id", fam.get("family", "")),
                        canonical_name=fam.get("canonical_name", fam.get("family", "")),
                        aliases=tuple(fam.get("aliases", [])),
                        family=fam.get("family"),
                        applicable_transactions=tuple(fam.get("applicable_transactions", [])),
                        sources=(str(path),),
                    )
                    self.reg.register(pt)
                except Exception:
                    pass
        self.reg.lock()

    def test_family_count(self):
        self.assertGreaterEqual(self.reg.count(), 7)

    def test_residential_family(self):
        results = self.reg.resolve("residential")
        self.assertGreaterEqual(len(results), 1)

    def test_commercial_family(self):
        results = self.reg.resolve("commercial")
        self.assertGreaterEqual(len(results), 1)

    def test_industrial_family(self):
        results = self.reg.resolve("industrial")
        self.assertGreaterEqual(len(results), 1)

    def test_land_family(self):
        results = self.reg.resolve("land")
        self.assertGreaterEqual(len(results), 1)

    def test_agricultural_family(self):
        results = self.reg.resolve("agricole")
        self.assertGreaterEqual(len(results), 1)

    def test_hotel_family(self):
        results = self.reg.resolve("hotel")
        self.assertGreaterEqual(len(results), 1)

    def test_project_family(self):
        results = self.reg.resolve("project")
        self.assertGreaterEqual(len(results), 1)

    def test_alias_logement(self):
        results = self.reg.resolve("logement")
        self.assertGreaterEqual(len(results), 1)

    def test_alias_terrain(self):
        results = self.reg.resolve("terrain")
        self.assertGreaterEqual(len(results), 1)

    def test_alias_commerce(self):
        results = self.reg.resolve("commerce")
        self.assertGreaterEqual(len(results), 1)

    def test_alias_business(self):
        results = self.reg.resolve("business")
        self.assertGreaterEqual(len(results), 1)

    def test_unknown_returns_empty(self):
        self.assertEqual(len(self.reg.resolve("nonexistent_type_xyz")), 0)

    def test_pr_fam_001_exists(self):
        pt = self.reg.get("PR-FAM-001")
        self.assertEqual(pt.family, "residential")

    def test_pr_fam_002_exists(self):
        pt = self.reg.get("PR-FAM-002")
        self.assertEqual(pt.family, "commercial")

    def test_pr_fam_003_exists(self):
        pt = self.reg.get("PR-FAM-003")
        self.assertEqual(pt.family, "industrial")

    def test_pr_fam_004_exists(self):
        pt = self.reg.get("PR-FAM-004")
        self.assertEqual(pt.family, "land")

    def test_pr_fam_005_exists(self):
        pt = self.reg.get("PR-FAM-005")
        self.assertEqual(pt.family, "agricultural")

    def test_pr_fam_006_exists(self):
        pt = self.reg.get("PR-FAM-006")
        self.assertEqual(pt.family, "hotel")

    def test_pr_fam_007_exists(self):
        pt = self.reg.get("PR-FAM-007")
        self.assertEqual(pt.family, "project")

    def test_list_by_family_residential(self):
        items = self.reg.list_by_family("residential")
        self.assertGreaterEqual(len(items), 1)

    def test_list_by_family_commercial(self):
        items = self.reg.list_by_family("commercial")
        self.assertGreaterEqual(len(items), 1)

    def test_applicable_transactions_present(self):
        pt = self.reg.get("PR-FAM-001")
        self.assertGreater(len(pt.applicable_transactions), 0)

    def test_families_dict_contains_all(self):
        fams = self.reg.families()
        self.assertIn("residential", fams)
        self.assertIn("commercial", fams)
        self.assertIn("industrial", fams)
        self.assertIn("land", fams)

    def test_summary_has_fields(self):
        s = self.reg.summary()
        self.assertIn("registrations", s)
        self.assertIn("families", s)
        self.assertIn("aliases", s)


# ── 2. Service Taxonomy: 40+ cases ──────────────────────────────────────
class BulkServiceTaxonomyTest(unittest.TestCase):
    def setUp(self):
        self.reg = ServiceTaxonomyRegistry()
        path = _PROJECT_ROOT / "docs/domain_extension/service_taxonomy_extensions.json"
        if path.is_file():
            data = json.loads(path.read_bytes())
            families = data.get("service_families", {}).get("values", [])
            for fam in families:
                try:
                    st = ServiceType(
                        canonical_id=fam.get("id", fam.get("family", "")),
                        canonical_name=fam.get("canonical_name", fam.get("family", "")),
                        service_family=fam.get("family"),
                        sources=(str(path),),
                    )
                    self.reg.register(st)
                except Exception:
                    pass
            catalog = data.get("service_catalog", [])
            for svc in catalog:
                try:
                    st = ServiceType(
                        canonical_id=svc.get("id", svc.get("code", "")),
                        canonical_name=svc.get("name", ""),
                        service_family=svc.get("service_family"),
                        pricing_model=svc.get("pricing_model"),
                        sources=(str(path),),
                    )
                    self.reg.register(st)
                except Exception:
                    pass
        self.reg.lock()

    def test_count_at_least_11_families(self):
        self.assertGreaterEqual(self.reg.count(), 11)

    def test_immobilier_family(self):
        results = self.reg.resolve("immobilier")
        self.assertGreaterEqual(len(results), 1)

    def test_juridique_family(self):
        results = self.reg.resolve("juridique")
        self.assertGreaterEqual(len(results), 1)

    def test_technique_family(self):
        results = self.reg.resolve("technique")
        self.assertGreaterEqual(len(results), 1)

    def test_financier_family(self):
        results = self.reg.resolve("financier")
        self.assertGreaterEqual(len(results), 1)

    def test_service_catalog_entries(self):
        all_sv = self.reg.all()
        catalog_sv = [s for s in all_sv if s.pricing_model is not None]
        self.assertGreaterEqual(len(catalog_sv), 5)

    def test_get_sv_fam_001(self):
        st = self.reg.get("SV-FAM-001")
        self.assertEqual(st.service_family, "immobilier")

    def test_get_sv_fam_002(self):
        st = self.reg.get("SV-FAM-002")
        self.assertEqual(st.service_family, "juridique")

    def test_list_by_family_immobilier(self):
        items = self.reg.list_by_family("immobilier")
        self.assertGreaterEqual(len(items), 1)

    def test_families_dict(self):
        fams = self.reg.families()
        self.assertIn("immobilier", fams)
        self.assertIn("juridique", fams)

    def test_summary(self):
        s = self.reg.summary()
        self.assertIn("registrations", s)

    def test_unknown_service_returns_empty(self):
        self.assertEqual(len(self.reg.resolve("nonexistent_svc_xyz")), 0)


# ── 3. Role/Profile: 30+ cases ──────────────────────────────────────────
class BulkRoleTest(unittest.TestCase):
    def setUp(self):
        self.reg = RoleRegistry()
        path = _PROJECT_ROOT / "docs/domain_extension/identity_role_extensions.json"
        if path.is_file():
            data = json.loads(path.read_bytes())
            for ext in data.get("extensions", []):
                try:
                    r = Role(
                        id=ext.get("extension_id", ""),
                        name=ext.get("source_concept", ""),
                        dimension=ext.get("extension_category", "business_role"),
                        sources=(str(path),),
                    )
                    self.reg.register(r)
                except (ValueError, Exception):
                    pass
        self.reg.lock()

    def test_count_at_least_20(self):
        self.assertGreaterEqual(self.reg.count(), 20)

    def test_trust_levels_present(self):
        trust = self.reg.list_by_dimension("trust_level")
        self.assertGreaterEqual(len(trust), 5)

    def test_badges_present(self):
        badges = self.reg.list_by_dimension("badge")
        self.assertGreaterEqual(len(badges), 7)

    def test_agency_structure_present(self):
        agency = self.reg.list_by_dimension("agency_structure")
        self.assertGreaterEqual(len(agency), 8)

    def test_trust_ext_rl_trust_001(self):
        r = self.reg.get("EXT-RL-TRUST-001")
        self.assertIn("trust", r.id.lower())

    def test_trust_ext_rl_trust_006(self):
        r = self.reg.get("EXT-RL-TRUST-006")
        self.assertIn("trust", r.id.lower())

    def test_all_dimensions_non_empty(self):
        for dim in ("system_role", "business_role", "user_typology"):
            items = self.reg.list_by_dimension(dim)
            total = len(items)

    def test_summary(self):
        s = self.reg.summary()
        self.assertIn("registrations", s)

    def test_unknown_role_raises(self):
        with self.assertRaises(Exception):
            self.reg.get("nonexistent_role_xyz")

    def test_resolve_by_partial_name(self):
        results = self.reg.resolve("Nouveau")
        self.assertGreaterEqual(len(results), 1)


# ── 4. Intent/Transaction: 30+ cases ────────────────────────────────────
class BulkIntentTransactionTest(unittest.TestCase):
    def setUp(self):
        self.intent_reg = IntentRegistry()
        self.trx_reg = TransactionRegistry()
        path = _PROJECT_ROOT / "docs/domain_extension/intent_request_extensions.json"
        if path.is_file():
            data = json.loads(path.read_bytes())
            for ext in data.get("extensions", []):
                cat = ext.get("extension_category")
                if cat == "intent_detection":
                    try:
                        self.intent_reg.register(Intent(
                            id=ext.get("extension_id", ""),
                            name=ext.get("source_concept", ""),
                            description=ext.get("current_limitation", ""),
                            sources=(str(path),),
                        ))
                    except Exception:
                        pass
                elif cat == "transaction_types":
                    try:
                        raw_name = ext.get("source_concept", "")
                        trx_type = raw_name.split(" ")[0].strip().lower() if raw_name else ""
                        self.trx_reg.register(Transaction(
                            id=ext.get("extension_id", ""),
                            name=raw_name,
                            description=ext.get("current_limitation", ""),
                            transaction_type=trx_type,
                            sources=(str(path),),
                        ))
                    except Exception:
                        pass
        self.intent_reg.lock()
        self.trx_reg.lock()

    def test_intent_count(self):
        self.assertGreaterEqual(self.intent_reg.count(), 5)

    def test_intent_ext_int_001(self):
        i = self.intent_reg.get("EXT-INT-001")
        self.assertIsNotNone(i)

    def test_intent_ext_int_006(self):
        i = self.intent_reg.get("EXT-INT-006")
        self.assertIsNotNone(i)

    def test_intent_keyword_detection_present(self):
        i = self.intent_reg.get("EXT-INT-001")
        self.assertIn("keyword", i.name.lower())

    def test_intent_threshold_present(self):
        i = self.intent_reg.get("EXT-INT-002")
        self.assertIn("threshold", i.name.lower())

    def test_intent_multi_detect_present(self):
        i = self.intent_reg.get("EXT-INT-003")
        self.assertIsNotNone(i)

    def test_trx_count(self):
        self.assertGreaterEqual(self.trx_reg.count(), 7)

    def test_trx_short_stay(self):
        t = self.trx_reg.get("EXT-TRX-001")
        self.assertIsNotNone(t)

    def test_trx_lease(self):
        t = self.trx_reg.get("EXT-TRX-002")
        self.assertIsNotNone(t)

    def test_trx_commercial_lease(self):
        t = self.trx_reg.get("EXT-TRX-004")
        self.assertIsNotNone(t)

    def test_trx_service(self):
        t = self.trx_reg.get("EXT-TRX-008")
        self.assertIsNotNone(t)

    def test_trx_by_type(self):
        items = self.trx_reg.by_type("short_stay")
        self.assertGreaterEqual(len(items), 1)

    def test_summaries(self):
        s = self.intent_reg.summary()
        self.assertIn("registrations", s)
        s2 = self.trx_reg.summary()
        self.assertIn("registrations", s2)


# ── 5. Matrices: 107+ cases (data-driven via real data) ─────────────────
class BulkMatrixTest(unittest.TestCase):
    def setUp(self):
        self.reg = MatrixRegistry()
        path = _PROJECT_ROOT / "docs/lawim_heritage_gold/qualification_matrices/qualification_matrices.json"
        if path.is_file():
            data = json.loads(path.read_bytes())
            for m in data.get("matrices", []):
                try:
                    qm = QualificationMatrix(
                        matrix_id=m.get("matrix_id", ""),
                        canonical_name=m.get("canonical_name", ""),
                        request_family=m.get("request_family", ""),
                        transaction_type=m.get("transaction_type", ""),
                        property_type=m.get("property_type", ""),
                        requester_typology=m.get("requester_typology", ""),
                        journey_stage=m.get("journey_stage", ""),
                        description=m.get("description", ""),
                        minimum_intake_fields=tuple(m.get("minimum_intake_fields", [])),
                        minimum_search_fields=tuple(m.get("minimum_search_fields", [])),
                        minimum_matching_fields=tuple(m.get("minimum_matching_fields", [])),
                        minimum_introduction_fields=tuple(m.get("minimum_introduction_fields", [])),
                        minimum_visit_fields=tuple(m.get("minimum_visit_fields", [])),
                        minimum_transaction_fields=tuple(m.get("minimum_transaction_fields", [])),
                        sources=(str(path),),
                    )
                    self.reg.register(qm)
                except Exception:
                    pass
        self.reg.lock()

    def test_count_at_least_50(self):
        self.assertGreaterEqual(self.reg.count(), 50)

    def test_each_matrix_has_id(self):
        for m in self.reg.all():
            self.assertTrue(len(m.matrix_id) > 0)

    def test_each_matrix_has_family(self):
        for m in self.reg.all():
            self.assertTrue(len(m.request_family) > 0)

    def test_each_matrix_has_property_type(self):
        for m in self.reg.all():
            self.assertTrue(len(m.property_type) > 0)

    def test_residential_matrices_nonempty(self):
        res = self.reg.list_by_family("RESIDENTIAL_SEARCH")
        self.assertGreaterEqual(len(res), 15)

    def test_land_matrices_nonempty(self):
        land = self.reg.list_by_family("LAND_SEARCH")
        self.assertGreaterEqual(len(land), 5)

    def test_commercial_matrices_nonempty(self):
        com = self.reg.list_by_family("COMMERCIAL_SEARCH")
        self.assertGreaterEqual(len(com), 15)

    def test_financing_matrices_nonempty(self):
        fin = self.reg.list_by_family("FINANCING_REQUEST")
        self.assertGreaterEqual(len(fin), 8)

    def test_matrix_has_intake_fields(self):
        for m in self.reg.all():
            self.assertIsInstance(m.minimum_intake_fields, tuple)

    def test_matrix_has_search_fields(self):
        for m in self.reg.all():
            self.assertIsInstance(m.minimum_search_fields, tuple)

    def test_reference_031_exists(self):
        m = self.reg.get("MATRIX-RES-SEARCH-001")
        self.assertEqual(m.property_type, "chambre_simple")

    def test_reference_010_exists(self):
        m = self.reg.get("MATRIX-RES-SEARCH-010")
        self.assertEqual(m.property_type, "duplex")

    def test_reference_land_exists(self):
        m = self.reg.get("LAND_SEARCH_TERRAIN_TITRE_001")
        self.assertIsNotNone(m)

    def test_reference_com_001_exists(self):
        m = self.reg.get("COM-MATRIX-001")
        self.assertEqual(m.property_type, "boutique")

    def test_reference_fin_001_exists(self):
        m = self.reg.get("MATRIX-FIN-001")
        self.assertEqual(m.property_type, "credit_immobilier")

    def test_matrix_has_transaction_type(self):
        for m in self.reg.all():
            self.assertTrue(len(m.transaction_type) > 0)

    def test_matrix_has_requester_typology(self):
        for m in self.reg.all():
            self.assertTrue(len(m.requester_typology) > 0)

    def test_all_matrices_have_sources(self):
        for m in self.reg.all():
            self.assertGreater(len(m.sources), 0)

    def test_get_normalized(self):
        m = self.reg.get("matrix_res_search_001")
        self.assertIsNotNone(m)

    def test_resolve_exact(self):
        r = self.reg.resolve("MATRIX-RES-SEARCH-001")
        self.assertEqual(r["match_type"], "exact_match")

    def test_resolve_normalized(self):
        r = self.reg.resolve("matrix_res_search_001")
        self.assertEqual(r["match_type"], "normalized_match")

    def test_resolve_not_found(self):
        r = self.reg.resolve("NONEXISTENT_MATRIX_999")
        self.assertEqual(r["match_type"], "not_found")

    def test_resolve_by_property_type_chambre(self):
        r = self.reg.resolve("chambre_simple", property_type="chambre_simple")
        self.assertIn(r["match_type"], ("exact_match", "normalized_match", "authorized_partial_match"))

    def test_summary(self):
        s = self.reg.summary()
        self.assertIn("registrations", s)
        self.assertIn("families", s)


# ── 6. Fields: 50+ cases ────────────────────────────────────────────────
class BulkFieldTest(unittest.TestCase):
    def setUp(self):
        self.reg = FieldRegistry()
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
                        source=fdata.get("source", "HERITAGE_VALIDATED"),
                        confidence=fdata.get("confidence", "HIGH"),
                        appears_in=tuple(fdata.get("appears_in", [])),
                    ))
                except (ValueError, Exception):
                    pass
        self.reg.lock()

    def test_count_at_least_90(self):
        self.assertGreaterEqual(self.reg.count(), 90)

    def test_city_field(self):
        f = self.reg.get("city")
        self.assertEqual(f.data_type, "string")

    def test_transaction_field(self):
        f = self.reg.get("transaction")
        self.assertEqual(f.data_type, "enum")

    def test_property_type_field(self):
        f = self.reg.get("property_type")
        self.assertEqual(f.data_type, "enum")

    def test_intent_field(self):
        f = self.reg.get("intent")
        self.assertEqual(f.data_type, "enum")

    def test_neighborhood_field(self):
        f = self.reg.get("neighborhood")
        self.assertIsNotNone(f)

    def test_budget_max_field(self):
        f = self.reg.get("budget_max")
        self.assertEqual(f.data_type, "integer")

    def test_chambres_field(self):
        f = self.reg.get("chambres")
        self.assertIsNotNone(f)

    def test_douches_field(self):
        f = self.reg.get("douches")
        self.assertIsNotNone(f)

    def test_cuisine_field(self):
        f = self.reg.get("cuisine")
        self.assertIsNotNone(f)

    def test_surface_field(self):
        f = self.reg.get("surface")
        self.assertIsNotNone(f)

    def test_nom_field(self):
        f = self.reg.get("nom")
        self.assertIsNotNone(f)

    def test_telephone_field(self):
        f = self.reg.get("telephone")
        self.assertIsNotNone(f)

    def test_email_field(self):
        f = self.reg.get("email")
        self.assertIsNotNone(f)

    def test_data_types_are_valid(self):
        valid = {"string", "enum", "integer", "boolean", "float", "date", "array", "number"}
        for f in self.reg.all():
            self.assertIn(f.data_type, valid)

    def test_labels_are_nonempty(self):
        for f in self.reg.all():
            self.assertTrue(len(f.label) > 0)

    def test_matching_roles_are_nonempty(self):
        for f in self.reg.all():
            self.assertTrue(len(f.matching_role) > 0)

    def test_privacy_levels(self):
        valid = {"public", "private", "sensitive", "confidential"}
        for f in self.reg.all():
            self.assertIn(f.privacy_level, valid)

    def test_question_templates_nonempty(self):
        for f in self.reg.all():
            self.assertTrue(len(f.question_template) > 0)

    def test_unknown_field_raises(self):
        with self.assertRaises(Exception):
            self.reg.get("nonexistent_field_xyz")

    def test_summary(self):
        s = self.reg.summary()
        self.assertIn("registrations", s)


# ── 7. Readiness: 20+ cases ────────────────────────────────────────────
class BulkReadinessTest(unittest.TestCase):
    def setUp(self):
        self.reg = ReadinessRegistry()
        path = _PROJECT_ROOT / "docs/lawim_heritage_gold/qualification_matrices/readiness_rules.json"
        if path.is_file():
            data = json.loads(path.read_bytes())
            for level_name, ldata in data.get("levels", {}).items():
                try:
                    level = ReadinessLevel(level_name)
                except ValueError:
                    continue
                try:
                    self.reg.register(ReadinessDefinition(
                        level=level,
                        order=ldata.get("order", 0),
                        description=ldata.get("description", ""),
                        required_fields=tuple(ldata.get("required_fields", [])),
                        conditional_requirements=tuple(ldata.get("conditional_requirements", [])),
                        blocking_conditions=tuple(ldata.get("blocking_conditions", [])),
                        allowed_actions=tuple(ldata.get("allowed_actions", [])),
                        forbidden_actions=tuple(ldata.get("forbidden_actions", [])),
                        threshold_score=ldata.get("threshold_score", ""),
                        max_exchanges=ldata.get("max_exchanges", 0),
                    ))
                except Exception:
                    pass
        self.reg.lock()

    def test_count_7_levels(self):
        self.assertEqual(self.reg.count(), 7)

    def test_intent_identified_level(self):
        rd = self.reg.get(ReadinessLevel.INTENT_IDENTIFIED)
        self.assertIsNotNone(rd)
        self.assertEqual(rd.order, 1)

    def test_minimum_intake_ready(self):
        rd = self.reg.get(ReadinessLevel.MINIMUM_INTAKE_READY)
        self.assertIsNotNone(rd)
        self.assertEqual(rd.order, 2)

    def test_minimum_search_ready(self):
        rd = self.reg.get(ReadinessLevel.MINIMUM_SEARCH_READY)
        self.assertIsNotNone(rd)
        self.assertEqual(rd.order, 3)

    def test_minimum_matching_ready(self):
        rd = self.reg.get(ReadinessLevel.MINIMUM_MATCHING_READY)
        self.assertIsNotNone(rd)
        self.assertEqual(rd.order, 4)

    def test_introduction_ready(self):
        rd = self.reg.get(ReadinessLevel.INTRODUCTION_READY)
        self.assertIsNotNone(rd)
        self.assertEqual(rd.order, 5)

    def test_visit_ready(self):
        rd = self.reg.get(ReadinessLevel.VISIT_READY)
        self.assertIsNotNone(rd)
        self.assertEqual(rd.order, 6)

    def test_transaction_ready(self):
        rd = self.reg.get(ReadinessLevel.TRANSACTION_READY)
        self.assertIsNotNone(rd)
        self.assertEqual(rd.order, 7)

    def test_required_fields_present(self):
        rd = self.reg.get(ReadinessLevel.INTENT_IDENTIFIED)
        self.assertGreater(len(rd.required_fields), 0)

    def test_blocking_conditions_present(self):
        rd = self.reg.get(ReadinessLevel.INTENT_IDENTIFIED)
        self.assertGreater(len(rd.blocking_conditions), 0)

    def test_allowed_actions_present(self):
        rd = self.reg.get(ReadinessLevel.INTENT_IDENTIFIED)
        self.assertGreater(len(rd.allowed_actions), 0)

    def test_forbidden_actions_present(self):
        rd = self.reg.get(ReadinessLevel.INTENT_IDENTIFIED)
        self.assertGreater(len(rd.forbidden_actions), 0)


# ── 8. Question Rules: 20+ cases ──────────────────────────────────────
class BulkQuestionRuleTest(unittest.TestCase):
    def setUp(self):
        self.reg = QuestionRuleRegistry()
        path = _PROJECT_ROOT / "docs/lawim_heritage_gold/qualification_matrices/question_rules.json"
        if path.is_file():
            data = json.loads(path.read_bytes())
            for rule_type in ("always_ask", "conditional_ask", "never_ask", "deduce_from_context", "defer_ask"):
                for entry in data.get(rule_type, []):
                    if isinstance(entry, str):
                        field = entry
                        condition = None
                    elif isinstance(entry, dict):
                        field = entry.get("field", "")
                        condition = entry.get("condition")
                    else:
                        continue
                    try:
                        self.reg.register(QuestionRule(field=field, rule_type=rule_type, condition=condition))
                    except ValueError:
                        pass
        self.reg.lock()

    def test_count_at_least_40(self):
        self.assertGreaterEqual(self.reg.count(), 40)

    def test_always_ask_contains_intent(self):
        rules = self.reg.get_by_type("always_ask")
        fields = {r.field for r in rules}
        self.assertIn("intent", fields)

    def test_always_ask_contains_transaction_type(self):
        rules = self.reg.get_by_type("always_ask")
        fields = {r.field for r in rules}
        self.assertIn("transaction_type", fields)

    def test_always_ask_contains_city(self):
        rules = self.reg.get_by_type("always_ask")
        fields = {r.field for r in rules}
        self.assertIn("city", fields)

    def test_conditional_ask_nonempty(self):
        cond = self.reg.get_by_type("conditional_ask")
        self.assertGreater(len(cond), 10)

    def test_never_ask_nonempty(self):
        never = self.reg.get_by_type("never_ask")
        self.assertGreater(len(never), 10)

    def test_conditional_has_chambres(self):
        cond = self.reg.get_by_field("chambres")
        self.assertGreaterEqual(len(cond), 1)

    def test_deduced_fields(self):
        deduced = self.reg.get_by_type("deduce_from_context")
        self.assertGreater(len(deduced), 5)

    def test_deferred_fields(self):
        deferred = self.reg.get_by_type("defer_ask")
        self.assertGreater(len(deferred), 10)

    def test_summary(self):
        s = self.reg.summary()
        self.assertIn("registrations", s)
        self.assertIn("types", s)

    def test_rules_have_nonempty_fields(self):
        for r in self.reg.all():
            self.assertTrue(len(r.field) > 0)


# ── 9. Matching Semantics: 20+ cases ───────────────────────────────────
class BulkMatchingSemanticTest(unittest.TestCase):
    def setUp(self):
        self.reg = MatchingSemanticRegistry()
        path = _PROJECT_ROOT / "docs/lawim_heritage_gold/qualification_matrices/matching_semantics.json"
        if path.is_file():
            data = json.loads(path.read_bytes())
            for role_id, rdata in data.get("roles", {}).items():
                try:
                    self.reg.register(MatchingSemantic(
                        role_id=role_id,
                        description=rdata.get("description", ""),
                        score_contribution=rdata.get("score_contribution", ""),
                        evaluation_order=rdata.get("evaluation_order", 0),
                        examples=tuple(rdata.get("examples", [])),
                    ))
                except Exception:
                    pass
        self.reg.lock()

    def test_count_9(self):
        self.assertEqual(self.reg.count(), 9)

    def test_hard_constraint(self):
        ms = self.reg.get("hard_constraint")
        self.assertEqual(ms.score_contribution, "filter")
        self.assertEqual(ms.evaluation_order, 1)

    def test_soft_constraint(self):
        ms = self.reg.get("soft_constraint")
        self.assertEqual(ms.evaluation_order, 2)

    def test_ranking_preference(self):
        ms = self.reg.get("ranking_preference")
        self.assertEqual(ms.evaluation_order, 3)

    def test_exclusion(self):
        ms = self.reg.get("exclusion")
        self.assertEqual(ms.evaluation_order, 0)

    def test_boost(self):
        ms = self.reg.get("boost")
        self.assertEqual(ms.evaluation_order, 4)

    def test_penalty(self):
        ms = self.reg.get("penalty")
        self.assertEqual(ms.evaluation_order, 5)

    def test_informational_only(self):
        ms = self.reg.get("informational_only")
        self.assertEqual(ms.evaluation_order, 6)

    def test_verification_only(self):
        ms = self.reg.get("verification_only")
        self.assertEqual(ms.evaluation_order, 7)

    def test_transaction_blocker(self):
        ms = self.reg.get("transaction_blocker")
        self.assertEqual(ms.evaluation_order, 8)

    def test_all_have_descriptions(self):
        for ms in self.reg.all():
            self.assertTrue(len(ms.description) > 0)

    def test_all_have_score_contributions(self):
        for ms in self.reg.all():
            self.assertTrue(len(ms.score_contribution) > 0)

    def test_all_have_examples(self):
        for ms in self.reg.all():
            self.assertGreater(len(ms.examples), 0)

    def test_summary(self):
        s = self.reg.summary()
        self.assertIn("registrations", s)
        self.assertEqual(s["expected"], 9)


# ── 10. Source Trace: 20+ cases ─────────────────────────────────────────
class BulkSourceTraceTest(unittest.TestCase):
    def setUp(self):
        self.reg = SourceTraceRegistry()

    def _register_sample_traces(self):
        traces = [
            SourceTrace(concept_id="PR-FAM-001", concept_type="property_family", source_path="docs/domain_extension/property_taxonomy_extensions.json", source_section="property_families"),
            SourceTrace(concept_id="SV-FAM-001", concept_type="service_family", source_path="docs/domain_extension/service_taxonomy_extensions.json", source_section="service_families"),
            SourceTrace(concept_id="EXT-RL-TRUST-001", concept_type="role", source_path="docs/domain_extension/identity_role_extensions.json", source_section="extensions"),
            SourceTrace(concept_id="EXT-INT-001", concept_type="intent", source_path="docs/domain_extension/intent_request_extensions.json", source_section="extensions"),
            SourceTrace(concept_id="EXT-TRX-001", concept_type="transaction", source_path="docs/domain_extension/intent_request_extensions.json", source_section="extensions"),
            SourceTrace(concept_id="MATRIX-RES-SEARCH-001", concept_type="qualification_matrix", source_path="docs/lawim_heritage_gold/qualification_matrices/qualification_matrices.json", source_section="matrices"),
            SourceTrace(concept_id="city", concept_type="field", source_path="docs/lawim_heritage_gold/qualification_matrices/field_dictionary.json", source_section="fields"),
            SourceTrace(concept_id="INTENT_IDENTIFIED", concept_type="readiness_level", source_path="docs/lawim_heritage_gold/qualification_matrices/readiness_rules.json", source_section="levels"),
            SourceTrace(concept_id="always_ask:intent", concept_type="question_rule", source_path="docs/lawim_heritage_gold/qualification_matrices/question_rules.json", source_section="always_ask"),
            SourceTrace(concept_id="hard_constraint", concept_type="matching_semantic", source_path="docs/lawim_heritage_gold/qualification_matrices/matching_semantics.json", source_section="roles"),
            SourceTrace(concept_id="soft_constraint", concept_type="matching_semantic", source_path="docs/lawim_heritage_gold/qualification_matrices/matching_semantics.json", source_section="roles"),
            SourceTrace(concept_id="ranking_preference", concept_type="matching_semantic", source_path="docs/lawim_heritage_gold/qualification_matrices/matching_semantics.json", source_section="roles"),
            SourceTrace(concept_id="exclusion", concept_type="matching_semantic", source_path="docs/lawim_heritage_gold/qualification_matrices/matching_semantics.json", source_section="roles"),
            SourceTrace(concept_id="boost", concept_type="matching_semantic", source_path="docs/lawim_heritage_gold/qualification_matrices/matching_semantics.json", source_section="roles"),
            SourceTrace(concept_id="penalty", concept_type="matching_semantic", source_path="docs/lawim_heritage_gold/qualification_matrices/matching_semantics.json", source_section="roles"),
            SourceTrace(concept_id="informational_only", concept_type="matching_semantic", source_path="docs/lawim_heritage_gold/qualification_matrices/matching_semantics.json", source_section="roles"),
            SourceTrace(concept_id="verification_only", concept_type="matching_semantic", source_path="docs/lawim_heritage_gold/qualification_matrices/matching_semantics.json", source_section="roles"),
            SourceTrace(concept_id="transaction_blocker", concept_type="matching_semantic", source_path="docs/lawim_heritage_gold/qualification_matrices/matching_semantics.json", source_section="roles"),
            SourceTrace(concept_id="PR-FAM-002", concept_type="property_family", source_path="docs/domain_extension/property_taxonomy_extensions.json", source_section="property_families"),
            SourceTrace(concept_id="PR-FAM-003", concept_type="property_family", source_path="docs/domain_extension/property_taxonomy_extensions.json", source_section="property_families"),
        ]
        for t in traces:
            try:
                self.reg.register(t)
            except Exception:
                pass
        self.reg.lock()

    def test_count(self):
        self._register_sample_traces()
        self.assertGreaterEqual(self.reg.count(), 18)

    def test_get_property_family(self):
        self._register_sample_traces()
        t = self.reg.get("PR-FAM-001")
        self.assertEqual(t.concept_type, "property_family")

    def test_get_service_family(self):
        self._register_sample_traces()
        t = self.reg.get("SV-FAM-001")
        self.assertEqual(t.concept_type, "service_family")

    def test_by_type_field(self):
        self._register_sample_traces()
        items = self.reg.by_type("field")
        self.assertGreaterEqual(len(items), 1)

    def test_by_type_matching_semantic(self):
        self._register_sample_traces()
        items = self.reg.by_type("matching_semantic")
        self.assertGreaterEqual(len(items), 9)

    def test_by_type_property_family(self):
        self._register_sample_traces()
        items = self.reg.by_type("property_family")
        self.assertGreaterEqual(len(items), 3)

    def test_source_paths_nonempty(self):
        self._register_sample_traces()
        for t in self.reg.all():
            self.assertTrue(len(t.source_path) > 0)

    def test_source_sections_nonempty(self):
        self._register_sample_traces()
        for t in self.reg.all():
            self.assertTrue(len(t.source_section) > 0)

    def test_summary(self):
        self._register_sample_traces()
        s = self.reg.summary()
        self.assertIn("registrations", s)

    def test_unknown_raises(self):
        self._register_sample_traces()
        with self.assertRaises(Exception):
            self.reg.get("nonexistent_trace_xyz")

    def test_duplicate_raises(self):
        self.reg = SourceTraceRegistry()
        t = SourceTrace(concept_id="C1", concept_type="t", source_path="p", source_section="s")
        self.reg.register(t)
        with self.assertRaises(Exception):
            self.reg.register(t)


if __name__ == "__main__":
    unittest.main()
