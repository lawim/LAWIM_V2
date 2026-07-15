from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
from typing import Any

from ..constants import MAX_JSON_FILE_SIZE_BYTES, MAX_JSON_DEPTH
from ..errors import KnowledgeSourceNotFound, KnowledgeSchemaError
from ..models.common import KnowledgeSource
from ..models.field import FieldDefinition
from ..models.intent import Intent
from ..models.matching_semantic import MatchingSemantic
from ..models.qualification import QualificationMatrix
from ..models.question_rule import QuestionRule
from ..models.readiness import ReadinessDefinition, ReadinessLevel
from ..models.role import Role
from ..models.source_trace import SourceTrace
from ..models.taxonomy import PropertyType, ServiceType
from ..models.transaction import Transaction
from ..models.version import KnowledgeVersion
from ..registry import (
    AmbiguousAliasError,
    DuplicateEntryError,
    FieldRegistry,
    IntentRegistry,
    KnowledgeVersionRegistry,
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

logger = logging.getLogger(__name__)


def _read_json_file(path: str) -> Any:
    p = Path(path)
    if not p.is_file():
        raise KnowledgeSourceNotFound(path, f"Source file not found: {path}")
    size = p.stat().st_size
    if size > MAX_JSON_FILE_SIZE_BYTES:
        raise KnowledgeSchemaError(
            path,
            f"File size {size} exceeds maximum {MAX_JSON_FILE_SIZE_BYTES} bytes",
        )
    raw = p.read_bytes()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise KnowledgeSchemaError(path, f"Invalid JSON: {exc}") from exc
    return data


def _compute_checksum(path: str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _build_source(path: str, section: str, domain: str, record_count: int, checksum: str) -> KnowledgeSource:
    return KnowledgeSource(
        path=path,
        section=section,
        domain=domain,
        version="1.0.0",
        checksum=checksum,
        record_count=record_count,
        status="LOADED",
    )


def load_property_taxonomy(
    path: str,
    registry: PropertyTaxonomyRegistry,
    trace_registry: SourceTraceRegistry,
) -> KnowledgeSource:
    data = _read_json_file(path)
    checksum = _compute_checksum(path)
    count = 0

    families = data.get("property_families", {}).get("values", [])
    for fam in families:
        pt = PropertyType(
            canonical_id=fam.get("id", fam.get("family", "")),
            canonical_name=fam.get("canonical_name", fam.get("family", "")),
            aliases=tuple(fam.get("aliases", [])),
            family=fam.get("family"),
            applicable_transactions=tuple(fam.get("applicable_transactions", [])),
            sources=(path,),
            status=fam.get("status", "ACTIVE"),
        )
        try:
            registry.register(pt)
        except AmbiguousAliasError:
            logger.warning("Alias collision for family %s, skipping aliases", pt.canonical_id)
            pt = PropertyType(
                canonical_id=pt.canonical_id,
                canonical_name=pt.canonical_name,
                aliases=(),
                family=pt.family,
                applicable_transactions=pt.applicable_transactions,
                sources=pt.sources,
                status=pt.status,
            )
            registry.register(pt)
        trace_registry.register(SourceTrace(
            concept_id=pt.canonical_id,
            concept_type="property_family",
            source_path=path,
            source_section="property_families",
            source_rule_ids=tuple(fam.get("gold_source", "")) if isinstance(fam.get("gold_source"), str) else (),
        ))
        count += 1

    types = data.get("property_types", {})
    if isinstance(types, dict):
        values = types.get("values", [])
        for pt_data in values:
            if isinstance(pt_data, dict) and "canonical_id" in pt_data:
                pt = PropertyType(
                    canonical_id=pt_data["canonical_id"],
                    canonical_name=pt_data.get("canonical_name", pt_data["canonical_id"]),
                    aliases=tuple(pt_data.get("aliases", [])),
                    parent_id=pt_data.get("parent_id"),
                    family=pt_data.get("family"),
                    subtype=pt_data.get("subtype"),
                    usage_types=tuple(pt_data.get("usage_types", [])),
                    applicable_transactions=tuple(pt_data.get("applicable_transactions", [])),
                    qualification_matrix_ids=tuple(pt_data.get("qualification_matrix_ids", [])),
                    status=pt_data.get("status", "ACTIVE"),
                    sources=(path,),
                )
                try:
                    registry.register(pt)
                except AmbiguousAliasError:
                    pt = PropertyType(
                        canonical_id=pt_data["canonical_id"],
                        canonical_name=pt_data.get("canonical_name", pt_data["canonical_id"]),
                        aliases=(),
                        parent_id=pt_data.get("parent_id"),
                        family=pt_data.get("family"),
                        subtype=pt_data.get("subtype"),
                        usage_types=tuple(pt_data.get("usage_types", [])),
                        applicable_transactions=tuple(pt_data.get("applicable_transactions", [])),
                        qualification_matrix_ids=tuple(pt_data.get("qualification_matrix_ids", [])),
                        status=pt_data.get("status", "ACTIVE"),
                        sources=(path,),
                    )
                    registry.register(pt)
                trace_registry.register(SourceTrace(
                    concept_id=pt.canonical_id,
                    concept_type="property_type",
                    source_path=path,
                    source_section="property_types",
                ))
                count += 1

    return _build_source(path, "property_taxonomy", "domain_extension", count, checksum)


def load_service_taxonomy(
    path: str,
    registry: ServiceTaxonomyRegistry,
    trace_registry: SourceTraceRegistry,
) -> KnowledgeSource:
    data = _read_json_file(path)
    checksum = _compute_checksum(path)
    count = 0

    families = data.get("service_families", {}).get("values", [])
    for fam in families:
        st = ServiceType(
            canonical_id=fam.get("id", fam.get("family", "")),
            canonical_name=fam.get("canonical_name", fam.get("family", "")),
            aliases=tuple(fam.get("aliases", [])),
            service_family=fam.get("family"),
            sources=(path,),
            status="ACTIVE",
        )
        registry.register(st)
        trace_registry.register(SourceTrace(
            concept_id=st.canonical_id,
            concept_type="service_family",
            source_path=path,
            source_section="service_families",
        ))
        count += 1

    catalog = data.get("service_catalog", [])
    if isinstance(catalog, list):
        for svc in catalog:
            st = ServiceType(
                canonical_id=svc.get("id", svc.get("code", "")),
                canonical_name=svc.get("name", ""),
                service_family=svc.get("service_family"),
                provider_categories=tuple(svc.get("provider_categories", [])),
                requester_categories=tuple(svc.get("requester_categories", [])),
                pricing_model=svc.get("pricing_model"),
                geographic_scope=svc.get("geographic_scope"),
                SLA_reference=str(svc.get("sla_hours", "")) if svc.get("sla_hours") else None,
                workflow_id=svc.get("workflow_id"),
                sources=(path,),
                status="ACTIVE",
            )
            registry.register(st)
            trace_registry.register(SourceTrace(
                concept_id=st.canonical_id,
                concept_type="service",
                source_path=path,
                source_section="service_catalog",
            ))
            count += 1

    return _build_source(path, "service_taxonomy", "domain_extension", count, checksum)


def load_roles(
    path: str,
    registry: RoleRegistry,
    trace_registry: SourceTraceRegistry,
) -> KnowledgeSource:
    data = _read_json_file(path)
    checksum = _compute_checksum(path)
    count = 0

    extensions = data.get("extensions", [])
    if isinstance(extensions, list):
        for ext in extensions:
            role = Role(
                id=ext.get("extension_id", ext.get("id", "")),
                name=ext.get("source_concept", ext.get("name", "")),
                dimension=ext.get("extension_category", "business_role"),
                aliases=(),
                sources=(path,),
                status="ACTIVE",
            )
            registry.register(role)
            trace_registry.register(SourceTrace(
                concept_id=role.id,
                concept_type="role",
                source_path=path,
                source_section="extensions",
                source_rule_ids=tuple(ext.get("source_rule_ids", [])),
            ))
            count += 1

    return _build_source(path, "roles", "domain_extension", count, checksum)


def load_intents(
    path: str,
    registry: IntentRegistry,
    trace_registry: SourceTraceRegistry,
) -> KnowledgeSource:
    data = _read_json_file(path)
    checksum = _compute_checksum(path)
    count = 0

    extensions = data.get("extensions", [])
    if isinstance(extensions, list):
        for ext in extensions:
            if ext.get("extension_category") == "intent_detection":
                intent = Intent(
                    id=ext.get("extension_id", ""),
                    name=ext.get("source_concept", ""),
                    description=ext.get("current_limitation", ""),
                    transaction_types=tuple(ext.get("H0.5_matrices_impacted", [])),
                    detection_keywords=(),
                    confidence_threshold=0.7,
                    sources=(path,),
                )
                registry.register(intent)
                trace_registry.register(SourceTrace(
                    concept_id=intent.id,
                    concept_type="intent",
                    source_path=path,
                    source_section="extensions",
                    source_rule_ids=tuple(ext.get("source_rule_ids", [])),
                ))
                count += 1

    return _build_source(path, "intents", "domain_extension", count, checksum)


def load_transactions(
    path: str,
    registry: TransactionRegistry,
    trace_registry: SourceTraceRegistry,
) -> KnowledgeSource:
    data = _read_json_file(path)
    checksum = _compute_checksum(path)
    count = 0

    extensions = data.get("extensions", [])
    if isinstance(extensions, list):
        for ext in extensions:
            if ext.get("extension_category") == "transaction_types":
                raw_name = ext.get("source_concept", "")
                trx_type = raw_name.split(" ")[0].strip().lower() if raw_name else ""
                transaction = Transaction(
                    id=ext.get("extension_id", ""),
                    name=raw_name,
                    description=ext.get("current_limitation", ""),
                    transaction_type=trx_type,
                    status="ACTIVE",
                    sources=(path,),
                )
                registry.register(transaction)
                trace_registry.register(SourceTrace(
                    concept_id=transaction.id,
                    concept_type="transaction",
                    source_path=path,
                    source_section="extensions",
                    source_rule_ids=tuple(ext.get("source_rule_ids", [])),
                ))
                count += 1

    return _build_source(path, "transactions", "domain_extension", count, checksum)


def load_matrices(
    path: str,
    registry: MatrixRegistry,
    trace_registry: SourceTraceRegistry,
) -> KnowledgeSource:
    data = _read_json_file(path)
    checksum = _compute_checksum(path)
    count = 0

    matrices = data.get("matrices", [])
    if isinstance(matrices, list):
        for m in matrices:
            matrix = QualificationMatrix(
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
                recommended_fields=tuple(m.get("recommended_fields", [])),
                optional_fields=tuple(m.get("optional_fields", [])),
                conditional_fields=tuple(m.get("conditional_fields", [])),
                sensitive_fields=tuple(m.get("sensitive_fields", [])),
                forbidden_questions=tuple(m.get("forbidden_questions", [])),
                source=m.get("source", "HERITAGE_VALIDATED"),
                confidence=m.get("confidence", "HIGH"),
                sources=(path,),
            )
            registry.register(matrix)
            trace_registry.register(SourceTrace(
                concept_id=matrix.matrix_id,
                concept_type="qualification_matrix",
                source_path=path,
                source_section="matrices",
            ))
            count += 1

    return _build_source(path, "matrices", "qualification_matrices", count, checksum)


def load_fields(
    path: str,
    registry: FieldRegistry,
    trace_registry: SourceTraceRegistry,
) -> KnowledgeSource:
    data = _read_json_file(path)
    checksum = _compute_checksum(path)
    count = 0

    fields = data.get("fields", {})
    if isinstance(fields, dict):
        for fid, fdata in fields.items():
            field = FieldDefinition(
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
            )
            registry.register(field)
            trace_registry.register(SourceTrace(
                concept_id=field.field_id,
                concept_type="field",
                source_path=path,
                source_section="fields",
            ))
            count += 1

    return _build_source(path, "fields", "qualification_matrices", count, checksum)


def load_readiness(
    path: str,
    registry: ReadinessRegistry,
    trace_registry: SourceTraceRegistry,
) -> KnowledgeSource:
    data = _read_json_file(path)
    checksum = _compute_checksum(path)
    count = 0

    levels = data.get("levels", {})
    if isinstance(levels, dict):
        for level_name, ldata in levels.items():
            try:
                level = ReadinessLevel(level_name)
            except ValueError:
                logger.warning("Unknown readiness level: %s", level_name)
                continue
            rd = ReadinessDefinition(
                level=level,
                order=ldata.get("order", 0),
                description=ldata.get("description", ""),
                required_fields=tuple(ldata.get("required_fields", [])),
                conditional_requirements=tuple(ldata.get("conditional_requirements", [])),
                blocking_conditions=tuple(ldata.get("blocking_conditions", [])),
                non_blocking_missing_fields=tuple(ldata.get("non_blocking_missing_fields", [])),
                allowed_actions=tuple(ldata.get("allowed_actions", [])),
                forbidden_actions=tuple(ldata.get("forbidden_actions", [])),
                threshold_score=ldata.get("threshold_score", ""),
                max_exchanges=ldata.get("max_exchanges", 0),
            )
            registry.register(rd)
            trace_registry.register(SourceTrace(
                concept_id=level_name,
                concept_type="readiness_level",
                source_path=path,
                source_section="levels",
            ))
            count += 1

    return _build_source(path, "readiness", "qualification_matrices", count, checksum)


def load_question_rules(
    path: str,
    registry: QuestionRuleRegistry,
    trace_registry: SourceTraceRegistry,
) -> KnowledgeSource:
    data = _read_json_file(path)
    checksum = _compute_checksum(path)
    count = 0

    for rule_type in ("always_ask", "conditional_ask", "never_ask", "deduce_from_context", "defer_ask"):
        entries = data.get(rule_type, [])
        if isinstance(entries, list):
            for entry in entries:
                if isinstance(entry, str):
                    field = entry
                    condition = None
                    priority = 0
                elif isinstance(entry, dict):
                    field = entry.get("field", "")
                    condition = entry.get("condition")
                    priority = entry.get("priority", 0)
                else:
                    continue
                rule = QuestionRule(
                    field=field,
                    rule_type=rule_type,
                    condition=condition,
                    priority=priority,
                )
                registry.register(rule)
                trace_id = f"{rule_type}:{field}" if field else f"{rule_type}:rule"
                try:
                    trace_registry.register(SourceTrace(
                        concept_id=trace_id,
                        concept_type="question_rule",
                        source_path=path,
                        source_section=rule_type,
                    ))
                except DuplicateEntryError:
                    pass
                count += 1

    rules = data.get("rules", [])
    if isinstance(rules, list):
        for entry in rules:
            if isinstance(entry, dict):
                field = entry.get("id", entry.get("rule_id", entry.get("field", "")))
                rule = QuestionRule(
                    field=field,
                    rule_type="rule",
                    condition=entry.get("condition"),
                    priority=entry.get("priority", 0),
                )
                registry.register(rule)
                try:
                    trace_registry.register(SourceTrace(
                        concept_id=rule.field,
                        concept_type="question_rule",
                        source_path=path,
                        source_section="rules",
                    ))
                except DuplicateEntryError:
                    pass
                count += 1

    return _build_source(path, "question_rules", "qualification_matrices", count, checksum)


def load_matching_semantics(
    path: str,
    registry: MatchingSemanticRegistry,
    trace_registry: SourceTraceRegistry,
) -> KnowledgeSource:
    data = _read_json_file(path)
    checksum = _compute_checksum(path)
    count = 0

    roles = data.get("roles", {})
    if isinstance(roles, dict):
        for role_id, rdata in roles.items():
            semantic = MatchingSemantic(
                role_id=role_id,
                description=rdata.get("description", ""),
                score_contribution=rdata.get("score_contribution", ""),
                evaluation_order=rdata.get("evaluation_order", 0),
                examples=tuple(rdata.get("examples", [])),
            )
            registry.register(semantic)
            trace_registry.register(SourceTrace(
                concept_id=role_id,
                concept_type="matching_semantic",
                source_path=path,
                source_section="roles",
            ))
            count += 1

    return _build_source(path, "matching_semantics", "qualification_matrices", count, checksum)


def load_all_knowledge(
    property_taxonomy_path: str,
    service_taxonomy_path: str,
    roles_path: str,
    intents_path: str,
    transactions_path: str,
    matrices_path: str,
    fields_path: str,
    readiness_path: str,
    question_rules_path: str,
    matching_semantics_path: str,
    *,
    property_registry: PropertyTaxonomyRegistry,
    service_registry: ServiceTaxonomyRegistry,
    role_registry: RoleRegistry,
    intent_registry: IntentRegistry,
    transaction_registry: TransactionRegistry,
    matrix_registry: MatrixRegistry,
    field_registry: FieldRegistry,
    readiness_registry: ReadinessRegistry,
    question_rule_registry: QuestionRuleRegistry,
    matching_semantic_registry: MatchingSemanticRegistry,
    source_trace_registry: SourceTraceRegistry,
    version_registry: KnowledgeVersionRegistry,
    build_commit: str = "unknown",
) -> list[KnowledgeSource]:
    sources: list[KnowledgeSource] = []
    source_checksums: dict[str, str] = {}
    source_record_counts: dict[str, int] = {}

    loaders = [
        ("property_taxonomy", property_taxonomy_path, property_registry, load_property_taxonomy),
        ("service_taxonomy", service_taxonomy_path, service_registry, load_service_taxonomy),
        ("roles", roles_path, role_registry, load_roles),
        ("intents", intents_path, intent_registry, load_intents),
        ("transactions", transactions_path, transaction_registry, load_transactions),
        ("matrices", matrices_path, matrix_registry, load_matrices),
        ("fields", fields_path, field_registry, load_fields),
        ("readiness", readiness_path, readiness_registry, load_readiness),
        ("question_rules", question_rules_path, question_rule_registry, load_question_rules),
        ("matching_semantics", matching_semantics_path, matching_semantic_registry, load_matching_semantics),
    ]

    for name, filepath, reg, loader_fn in loaders:
        try:
            ks = loader_fn(filepath, reg, source_trace_registry)
            sources.append(ks)
            source_checksums[filepath] = ks.checksum
            source_record_counts[filepath] = ks.record_count
            logger.info("Loaded %s: %d records from %s", name, ks.record_count, filepath)
        except KnowledgeSourceNotFound:
            logger.warning("Source not found, skipping %s: %s", name, filepath)
        except Exception:
            logger.exception("Failed to load %s from %s", name, filepath)
            raise

    version = KnowledgeVersion.compute(
        schema_version="1.0.0",
        build_commit=build_commit,
        source_checksums=source_checksums,
        source_record_counts=source_record_counts,
    )
    version_registry.set_version(version)

    for reg in [
        property_registry, service_registry, role_registry,
        intent_registry, transaction_registry, matrix_registry,
        field_registry, readiness_registry, question_rule_registry,
        matching_semantic_registry, source_trace_registry, version_registry,
    ]:
        reg.lock()

    return sources
