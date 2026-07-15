#!/usr/bin/env python3
"""
Comprehensive validation script for LAWIM qualification matrices.

Validates Markdown matrix files and associated JSON files in the
qualification_matrices directory for structural correctness,
content completeness, business rules, and cross-references.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX_DIR = ROOT / "docs" / "lawim_heritage_gold" / "qualification_matrices"

ALLOWED_TRANSACTION_TYPES = {
    "RENT", "BUY", "SELL", "RENT_OUT", "CONSTRUCT", "RENOVATE",
    "INVEST", "FIND", "FINANCE", "LEASE", "CESSION_BAIL",
    "BAIL_COMMERCIAL", "CESSION",
}
ALLOWED_DATA_TYPES = {"string", "integer", "float", "boolean", "enum", "date", "number", "text", "range", "object", "array"}
ALLOWED_MATCHING_ROLES = {
    "hard_constraint", "soft_constraint", "ranking_preference", "exclusion",
    "boost", "penalty", "informational_only", "verification_only",
    "transaction_blocker", "MATCHING_FINANCEUR", "COMMERCIAL",
}
ALLOWED_PRIVACY_LEVELS = {"public", "private", "sensitive", "confidential", "semi_private"}
ALLOWED_SOURCES = {
    "HERITAGE_VALIDATED", "HERITAGE_NORMALIZED", "HERITAGE_CONFLICTING",
    "EXTERNAL_CONFIRMED", "EXTERNAL_COMPLEMENT", "EXPERT_PROPOSAL",
    "HUMAN_VALIDATION_REQUIRED", "REJECTED",
}
ALLOWED_CONFIDENCE = {"HIGH", "MEDIUM", "LOW"}

MATRIX_ID_PATTERN = re.compile(
    r"^(?:COM-MATRIX-\d{3}|MATRIX-RES-SEARCH-\d{3}|"
    r"MATRIX-FIN-\d{3}|LAND_SEARCH_[A-Z_]+_\d{3}|"
    r"PRO-[A-Z]+-\d{3}|SVC-[A-Z]+-\d{3}|"
    r"RESIDENTIAL_SEARCH_[A-Z_]+_\d{3}|"
    r"RESIDENTIAL_LISTING_[A-Z_]+_\d{3}|"
    r"LAND_LISTING_[A-Z_]+_\d{3}|"
    r"COMMERCIAL_MATRIX_\d{3}|INV_MATRIX_\d{3}|"
    r"CONSTRUCTION_[A-Z_]+_\d{3}|DOC_[A-Z_]+_\d{3}|"
    r"VISIT_[A-Z_]+_\d{3}|MGMT_[A-Z_]+_\d{3}|"
    r"[A-Z_]+_MATRIX_\d{3}|MATRIX-\d{3})$"
)

REQUIRED_FILES = [
    "README.md", "MATRIX_CATALOG.md", "COMMON_FIELD_DICTIONARY.md",
    "READINESS_LEVELS.md", "QUESTION_PRIORITY_POLICY.md",
    "CONDITIONAL_QUESTION_RULES.md", "MATCHING_FIELD_SEMANTICS.md",
    "PRIVACY_AND_SENSITIVE_FIELDS.md",
    "residential_search_matrices.md", "residential_listing_matrices.md",
    "land_search_matrices.md", "land_listing_matrices.md",
    "commercial_property_matrices.md",
    "financing_request_matrices.md", "professional_service_matrices.md",
    "real_estate_service_matrices.md",
    "construction_and_renovation_matrices.md",
    "document_and_legal_service_matrices.md",
    "visit_and_inspection_matrices.md", "property_management_matrices.md",
    "SOURCE_TRACEABILITY.md", "EXTERNAL_COMPLEMENTS.md",
    "HUMAN_VALIDATION_REQUIRED.md",
    "qualification_matrices.json", "field_dictionary.json",
    "readiness_rules.json", "question_rules.json", "matching_semantics.json",
]

READINESS_LEVELS = {
    "INTENT_IDENTIFIED", "MINIMUM_INTAKE_READY", "MINIMUM_SEARCH_READY",
    "MINIMUM_MATCHING_READY", "INTRODUCTION_READY", "VISIT_READY",
    "TRANSACTION_READY",
}

FORBIDDEN_LAND_FIELDS = {"chambres", "douches", "salon", "standing", "pieces"}

MATRIX_METADATA_KEYS = {
    "matrix_id", "canonical_name", "request_family", "transaction_type",
    "property_or_service_type", "authoritative_name", "description",
}

COMPOSITE_REQUIRED_KEYS = {
    "minimum_intake_fields", "minimum_search_fields", "minimum_matching_fields",
    "minimum_introduction_fields", "minimum_visit_fields",
    "minimum_transaction_fields", "recommended_fields", "optional_fields",
    "conditional_fields", "sensitive_fields", "forbidden_questions",
    "derived_fields",
}

SECTION_TITLE_PATTERN = re.compile(r"^#{2,4}\s+(.+)$")
TABLE_ROW_RE = re.compile(r"^\|(.+)\|$")
YAML_FENCE_RE = re.compile(r"^```(yaml|yml)")
TABLE_SEPARATOR_RE = re.compile(r"^\|[\s\-:]+\|")

DIRECTIONAL_RE = re.compile(
    r"(?:standing|nombre\s+de\s+pieces|pieces\s+principales)",
    re.IGNORECASE,
)
BEDROOM_FIELD_RE = re.compile(r"chambres?\s*(?:à\s*coucher)?", re.IGNORECASE)


class ValidationResult:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.matrices: list[dict] = []
        self.fields_found: set[str] = set()
        self.matrix_ids: set[str] = set()

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def read_all_files(result: ValidationResult) -> dict[str, str]:
    files_found: dict[str, str] = {}
    for fname in REQUIRED_FILES:
        path = MATRIX_DIR / fname
        if path.exists():
            files_found[fname] = path.read_text(encoding="utf-8")
        else:
            result.warn(f"[file_existence] missing expected file: {fname}")
    for path in MATRIX_DIR.glob("*.md"):
        if path.name not in files_found:
            files_found[path.name] = path.read_text(encoding="utf-8")
    for path in MATRIX_DIR.glob("*.json"):
        if path.name not in files_found:
            files_found[path.name] = path.read_text(encoding="utf-8")
    return files_found


def parse_kv_table(table_text: str) -> dict[str, str]:
    pairs: dict[str, str] = {}
    for line in table_text.strip().split("\n"):
        line = line.strip()
        if not line or not line.startswith("|") or not line.endswith("|"):
            continue
        if re.match(r"^\|[\s\-:]+\|$", line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 2 and cells[0] and cells[1]:
            key = cells[0].strip().lower().replace(" ", "_").replace("-", "_")
            pairs[key] = cells[1].strip()
    return pairs


def parse_field_table(table_text: str) -> list[dict[str, str]]:
    lines = table_text.strip().split("\n")
    if len(lines) < 2:
        return []
    header_cells = [c.strip().lower().replace(" ", "_").replace("-", "_").replace("/", "_")
                    for c in lines[0].strip("|").split("|")]
    header_cells = [h for h in header_cells if h]
    if not header_cells:
        return []
    fields: list[dict[str, str]] = []
    for line in lines[2:]:
        line = line.strip()
        if not line or not line.startswith("|") or not line.endswith("|"):
            continue
        if TABLE_SEPARATOR_RE.match(line):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        cells = cells[:len(header_cells)]
        row: dict[str, str] = {}
        for i, h in enumerate(header_cells):
            if i < len(cells) and cells[i] and cells[i] != "—" and cells[i] != "--":
                row[h] = cells[i]
            else:
                row[h] = ""
        if row.get("field_id") or row.get("field_name") or row.get("forbidden_field"):
            fields.append(row)
    return fields


def parse_yaml_fields(yaml_block: str) -> list[dict[str, str]]:
    fields: list[dict[str, str]] = []
    field_name = ""
    current: dict[str, str] = {}
    for line in yaml_block.split("\n"):
        m = re.match(r"^\s*-\s*field_name\s*:\s*(.+)$", line)
        if m:
            if current and field_name:
                current["field_id"] = field_name
                fields.append(current)
            field_name = m.group(1).strip()
            current = {"field_name": field_name}
            continue
        m = re.match(r"^\s+field_name\s*:\s*(.+)$", line)
        if m and not field_name:
            field_name = m.group(1).strip()
            if current.get("field_name"):
                current["field_id"] = current["field_name"]
                fields.append(current)
            current = {"field_name": field_name}
            continue
        m = re.match(r"^\s{2,}(\w+)\s*:\s*(.*)$", line)
        if m and current is not None:
            key = m.group(1).strip().lower().replace("-", "_")
            val = m.group(2).strip().strip('"').strip("'")
            if val and key not in ("items", "sub_fields"):
                current[key] = val
    if current and field_name:
        current["field_id"] = field_name
        fields.append(current)
    return fields


def extract_matrix_id_from_value_table(pairs: dict[str, str]) -> str | None:
    for key in pairs:
        if key in ("matrix_id", "id"):
            return pairs[key]
        if key == "service_id":
            return pairs[key]
    return None


def parse_residential_matrix(text: str, start: int) -> tuple[dict | None, int]:
    matrix: dict[str, any] = {"_fields": {}, "_type": "residential"}
    lines = text.split("\n")
    i = start
    while i < len(lines) and not re.match(r"^###\s+matrix_id\s*$", lines[i].strip()):
        i += 1
    if i >= len(lines):
        return None, start
    matrix["matrix_id"] = lines[i + 1].strip() if i + 1 < len(lines) else ""
    i += 2
    sections = {
        "canonical_name", "request_family", "transaction_type",
        "property_or_service_type", "requester_typology", "journey_stage",
        "description",
    }
    while i < len(lines):
        line = lines[i].strip()
        m = re.match(r"^###\s+(\S[\w\s]*)$", line)
        if m:
            sec = m.group(1).strip().lower().replace(" ", "_").replace("-", "_").replace("/", "_")
            if sec in sections:
                val_lines: list[str] = []
                i += 1
                while i < len(lines) and not lines[i].strip().startswith("###"):
                    val_lines.append(lines[i])
                    i += 1
                matrix[sec] = " ".join(v.strip() for v in val_lines if v.strip()).strip()
                continue
            table_start = i + 1
            while i + 1 < len(lines) and not re.match(r"^#{2,4}\s", lines[i + 1].strip()):
                i += 1
            table_text = "\n".join(lines[table_start:i + 1]) if i >= table_start else ""
            if "field_id" in table_text or "FIELD-ID" in table_text or "field_name" in table_text:
                fields = parse_field_table(table_text)
                matrix["_fields"][sec] = fields
            i += 1
            continue
        i += 1
    return matrix, i


def parse_commercial_matrix(text: str, start: int) -> tuple[dict | None, int]:
    matrix: dict[str, any] = {"_fields": {}, "_type": "commercial"}
    lines = text.split("\n")
    i = start
    kv_lines: list[str] = []
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("|") and "field" in line.lower() and "value" in line.lower():
            i += 1
            while i < len(lines) and lines[i].strip().startswith("|") and not TABLE_SEPARATOR_RE.match(lines[i]):
                kv_lines.append(lines[i])
                i += 1
            break
        i += 1
    if kv_lines:
        pairs = parse_kv_table("\n".join(kv_lines))
        for k, v in pairs.items():
            matrix[k] = v
    section_map: dict[str, str] = {
        r"minimum\s*intake": "minimum_intake_fields",
        r"minimum\s*search": "minimum_search_fields",
        r"minimum\s*matching": "minimum_matching_fields",
        r"minimum\s*introduction": "minimum_introduction_fields",
        r"minimum\s*visit": "minimum_visit_fields",
        r"minimum\s*transaction": "minimum_transaction_fields",
        r"recommended": "recommended_fields",
        r"optional": "optional_fields",
        r"conditional": "conditional_fields",
        r"sensitive": "sensitive_fields",
        r"forbidden": "forbidden_questions",
        r"derived": "derived_fields",
        r"matrix\s*identification": None,
    }
    while i < len(lines):
        line = lines[i].strip()
        m = re.match(r"^###\s+Matrix\s+\d+\.\d+\s+[-–—]+\s+(.+)$", line)
        if not m:
            m = re.match(r"^###\s+(.+)$", line)
        if m:
            sec = m.group(1).strip().lower()
            target = None
            for pat, name in section_map.items():
                if re.search(pat, sec):
                    target = name
                    break
            if target is None:
                i += 1
                continue
            table_start = i + 1
            i += 1
            while i < len(lines) and not re.match(r"^#{2,4}\s", lines[i].strip()):
                i += 1
            table_text = "\n".join(lines[table_start:i]) if i > table_start else ""
            if "field_id" in table_text.lower():
                fields = parse_field_table(table_text)
                matrix["_fields"][target] = fields
            continue
        i += 1
    return matrix, i


def parse_land_matrix(text: str, start: int) -> tuple[dict | None, int]:
    matrix: dict[str, any] = {"_fields": {}, "_type": "land"}
    lines = text.split("\n")
    i = start
    while i < len(lines):
        line = lines[i].strip()
        if line == "### Matrix Header":
            i += 1
            kv_lines: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                if not TABLE_SEPARATOR_RE.match(lines[i]):
                    kv_lines.append(lines[i])
                i += 1
            if kv_lines:
                pairs = parse_kv_table("\n".join(kv_lines))
                for k, v in pairs.items():
                    if k == "authoritative_name":
                        matrix["canonical_name"] = v
                    else:
                        matrix[k] = v
            continue
        m = re.match(r"^###\s+(.+)$", line)
        if m:
            sec = m.group(1).strip().lower().replace(" ", "_").replace("-", "_")
            sec = sec.replace("/", "_").replace("é", "e").replace("è", "e")
            if sec in ("description",):
                desc_lines: list[str] = []
                i += 1
                while i < len(lines) and not re.match(r"^#{2,4}\s", lines[i].strip()):
                    desc_lines.append(lines[i])
                    i += 1
                matrix["description"] = " ".join(d.strip() for d in desc_lines if d.strip()).strip()
                continue
            section_name = None
            for pat in ["minimum_intake_fields", "minimum_search_fields",
                        "minimum_matching_fields", "minimum_introduction_fields",
                        "minimum_visit_fields", "minimum_transaction_fields",
                        "recommended_fields", "optional_fields",
                        "conditional_fields", "sensitive_fields",
                        "derived_fields", "forbidden_questions"]:
                if pat in sec or sec in pat:
                    section_name = pat
                    break
            if section_name:
                i += 1
                while i < len(lines) and not re.match(r"^#{2,4}\s", lines[i].strip()):
                    i += 1
                # table is between the header and next header
                # scan backwards from i to find table start
                ti = i - 1
                while ti > 0 and not lines[ti].strip().startswith("|"):
                    ti -= 1
                table_text = "\n".join(lines[table_start:ti + 1]) if 'table_start' in dir() else ""
                if "field_id" in table_text.lower() or "forbidden_field" in table_text.lower():
                    fields = parse_field_table(table_text)
                    matrix["_fields"][section_name] = fields
            i += 1
            continue
        # check for table headers starting a section (some land matrices skip ###)
        m2 = re.match(r"^###\s+(minimum_\w+|recommended_\w+|optional_\w+|conditional_\w+|sensitive_\w+|derived_\w+|forbidden_\w+)", line)
        if m2:
            sec = m2.group(1)
            i += 1
            while i < len(lines) and not re.match(r"^#{2,4}\s", lines[i].strip()):
                i += 1
        i += 1
    return matrix, i


def parse_financing_matrix(text: str, start: int) -> tuple[dict | None, int]:
    matrix: dict[str, any] = {"_fields": {}, "_type": "financing"}
    lines = text.split("\n")
    i = start
    heads = ["### Matrix Metadata", "#### Matrix Metadata", "### Metadata"]
    head_found = False
    for h in heads:
        pos = text.find(h, start)
        if pos >= 0:
            i = text[:pos].count("\n")
            head_found = True
            break
    if not head_found:
        return None, start
    i += 1
    kv_lines: list[str] = []
    while i < len(lines) and lines[i].strip().startswith("|"):
        if not TABLE_SEPARATOR_RE.match(lines[i]):
            kv_lines.append(lines[i])
        i += 1
    if kv_lines:
        pairs = parse_kv_table("\n".join(kv_lines))
        for k, v in pairs.items():
            matrix[k] = v
    section_map: dict[str, str] = {
        "minimum intake": "minimum_intake_fields",
        "minimum search": "minimum_search_fields",
        "minimum matching": "minimum_matching_fields",
        "minimum introduction": "minimum_introduction_fields",
        "minimum transaction": "minimum_transaction_fields",
        "recommended": "recommended_fields",
        "optional": "optional_fields",
        "conditional": "conditional_fields",
        "sensitive": "sensitive_fields",
        "forbidden": "forbidden_questions",
    }
    while i < len(lines):
        line = lines[i].strip()
        m = re.match(r"^#{2,4}\s+(.+)$", line)
        if m:
            sec = m.group(1).strip().lower()
            target = None
            for pat, name in section_map.items():
                if pat in sec:
                    target = name
                    break
            if target:
                table_start = i + 1
                i += 1
                while i < len(lines) and not re.match(r"^#{2,4}\s", lines[i].strip()):
                    i += 1
                table_text = "\n".join(lines[table_start:i]) if i > table_start else ""
                if "field_id" in table_text.lower() or "forbidden_question" in table_text.lower():
                    fields = parse_field_table(table_text)
                    matrix["_fields"][target] = fields
                continue
        i += 1
    return matrix, i


def parse_yaml_matrix(text: str, start: int) -> tuple[dict | None, int]:
    matrix: dict[str, any] = {"_fields": {}, "_type": "yaml"}
    lines = text.split("\n")
    i = start
    while i < len(lines) and not YAML_FENCE_RE.match(lines[i].strip()):
        i += 1
    if i >= len(lines):
        return None, start
    fence_start = i
    i += 1
    yaml_lines: list[str] = []
    while i < len(lines) and not lines[i].strip().startswith("```"):
        yaml_lines.append(lines[i])
        i += 1
    yaml_block = "\n".join(yaml_lines)
    if YAML_FENCE_RE.match(lines[fence_start].strip()):
        pass
    # Parse simple YAML-like structure
    current_key: str | None = None
    current_list: list[dict[str, str]] = []
    in_list = False
    for line in yaml_lines:
        m = re.match(r"^(\w[\w_]*)\s*:", line)
        if m:
            current_key = m.group(1)
            if current_key in ("matrix_id", "service_id", "canonical_name",
                                "request_family", "transaction_type",
                                "property_or_service_type", "description"):
                val = line.split(":", 1)[1].strip().strip("'").strip('"').strip(">")
                matrix[current_key] = val
            in_list = False
            continue
        if re.match(r"^\s+-\s+field_name", line) or re.match(r"^\s+-\s+\w", line):
            if current_key:
                section_name = None
                for pat in ["minimum_intake", "minimum_search",
                            "minimum_matching", "minimum_introduction",
                            "minimum_visit", "minimum_transaction",
                            "recommended", "optional", "conditional",
                            "sensitive", "forbidden", "derived",
                            "minimum_service_ready", "minimum_provider_matching_ready",
                            "minimum_quote_ready", "minimum_execution_ready"]:
                    if pat in current_key:
                        section_name = current_key
                        break
                if section_name:
                    if current_list:
                        matrix["_fields"].setdefault(section_name, []).extend(current_list)
                    current_list = []
            in_list = True
    if current_list and current_key:
        matrix["_fields"][current_key] = current_list
    for key in list(matrix["_fields"].keys()):
        if key not in matrix["_fields"] or not matrix["_fields"][key]:
            del matrix["_fields"][key]
    return matrix, i + 1


def validate_matrix_content(matrix: dict, fname: str, result: ValidationResult) -> None:
    mid = matrix.get("matrix_id", matrix.get("service_id", ""))
    if not mid:
        result.error(f"[{fname}] matrix missing matrix_id")
        return
    if mid in result.matrix_ids:
        result.error(f"[{fname}] duplicate matrix_id: {mid}")
    result.matrix_ids.add(mid)
    if not MATRIX_ID_PATTERN.match(mid):
        result.warn(f"[{fname}:{mid}] matrix_id format unexpected: {mid}")
    for key in ("canonical_name", "request_family"):
        if key not in matrix and "authoritative_name" not in matrix:
            # YAML service matrices define request_family at file level, not per service
            if matrix.get("_type") == "yaml":
                result.warn(f"[{fname}:{mid}] missing {key} (may be defined at file level)")
            else:
                result.error(f"[{fname}:{mid}] missing {key}")
    tx_type = matrix.get("transaction_type", "")
    if tx_type:
        parts = [t.strip() for t in tx_type.replace(",", " ").split() if t.strip()]
        for pt in parts:
            if pt not in ALLOWED_TRANSACTION_TYPES:
                result.warn(f"[{fname}:{mid}] unexpected transaction_type: {pt}")
    if not matrix.get("description") and not matrix.get("display_name"):
        result.warn(f"[{fname}:{mid}] missing or empty description")
    required_sections = [
        "minimum_intake_fields", "minimum_search_fields",
        "minimum_matching_fields", "minimum_introduction_fields",
        "minimum_visit_fields", "minimum_transaction_fields",
        "recommended_fields", "optional_fields", "conditional_fields",
        "sensitive_fields",
    ]
    for sec in required_sections:
        fields = matrix.get("_fields", {}).get(sec, [])
        if not fields:
            result.warn(f"[{fname}:{mid}] missing or empty section: {sec}")

    # Collect all field_ids from this matrix
    for sec, fields in matrix.get("_fields", {}).items():
        for field in fields:
            fid = (field.get("field_id") or field.get("field_name")
                   or field.get("forbidden_field") or "")
            if fid:
                result.fields_found.add(fid)


def validate_business_rules(matrix: dict, fname: str, result: ValidationResult) -> None:
    mid = matrix.get("matrix_id", "")
    ptype = matrix.get("property_or_service_type", "").lower()
    canonical = matrix.get("canonical_name", "").lower()
    is_residential = "residential" in fname or "studio" in canonical or "chambre" in canonical
    is_land = "land" in fname or "LAND_SEARCH" in fname or "_TERRAIN_" in mid
    is_studio_chambre = any(kw in canonical or kw in ptype
                            for kw in ["studio", "chambre", "chambre_simple",
                                       "chambre_moderne", "studio_moderne", "studio_meuble"])

    for sec, fields in matrix.get("_fields", {}).items():
        for field in fields:
            fid = (field.get("field_id") or field.get("field_name") or "").lower()

            if is_studio_chambre and "chambres" in fid:
                result.error(
                    f"[{fname}:{mid}] studio/chambre matrix contains 'chambres' field: {fid}"
                )
            if is_studio_chambre and "bedroom" in fid:
                result.error(
                    f"[{fname}:{mid}] studio/chambre matrix contains 'bedroom' field: {fid}"
                )
            if is_land:
                for forbidden in FORBIDDEN_LAND_FIELDS:
                    if forbidden in fid:
                        result.error(
                            f"[{fname}:{mid}] land matrix contains forbidden field '{forbidden}': {fid}"
                        )

    # Budget in minimum_search_fields
    search_fields = matrix.get("_fields", {}).get("minimum_search_fields", [])
    budget_in_search = any(
        "budget" in (f.get("field_id") or f.get("field_name") or "").lower()
        for f in search_fields
    )
    if not budget_in_search and "FINANCING_REQUEST" not in matrix.get("request_family", ""):
        result.warn(f"[{fname}:{mid}] no budget-type field in minimum_search_fields")

    # City/location in minimum_intake_fields
    intake_fields = matrix.get("_fields", {}).get("minimum_intake_fields", [])
    city_in_intake = any(
        any(kw in (f.get("field_id") or f.get("field_name") or "").lower()
            for kw in ["ville", "city", "localisation", "location"])
        for f in intake_fields
    )
    if not city_in_intake:
        result.warn(f"[{fname}:{mid}] no city/location field in minimum_intake_fields")

    # Transaction type in intake
    if matrix.get("transaction_type", "").strip() and "FINANCING_REQUEST" not in matrix.get("request_family", ""):
        tx_in_intake = any(
            "transaction" in (f.get("field_id") or f.get("field_name") or "").lower()
            for f in intake_fields
        )
        if not tx_in_intake:
            result.warn(f"[{fname}:{mid}] no transaction type field in minimum_intake_fields")


def validate_forbidden_patterns(text: str, fname: str, result: ValidationResult) -> None:
    questions = re.findall(r'question_template\s*["\']?([^"\'\n]+)', text)
    for q in questions:
        if re.search(r"\bstanding\b", q, re.IGNORECASE):
            result.error(
                f"[{fname}] direct 'standing' question detected: {q[:60]}"
            )
    if "nombre de pieces" in text.lower() or "nombre_pieces" in text.lower():
        for line in text.split("\n"):
            if re.search(r"nombre\s+de\s+pieces", line, re.IGNORECASE):
                result.warn(
                    f"[{fname}] 'nombre de pieces' as main criterion: {line.strip()[:80]}"
                )


def validate_readiness_rules(result: ValidationResult) -> None:
    rr_path = MATRIX_DIR / "readiness_rules.json"
    if not rr_path.exists():
        result.warn("[readiness_rules.json] file not found, skipping readiness rules validation")
        return
    try:
        data = json.loads(rr_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        result.error(f"[readiness_rules.json] invalid JSON: {e}")
        return
    if isinstance(data, dict):
        # Handle nested structure: {"levels": {"INTENT_IDENTIFIED": {...}}}
        # or flat: {"INTENT_IDENTIFIED": {...}}
        if "levels" in data:
            levels_data = data["levels"]
        else:
            levels_data = data
        if isinstance(levels_data, dict):
            levels = set(levels_data.keys())
        else:
            levels = set()
    elif isinstance(data, list):
        levels = set()
        for item in data:
            if isinstance(item, dict):
                levels.update(item.keys())
        levels_data = data
    else:
        result.error("[readiness_rules.json] unexpected JSON structure")
        return
    for rl in READINESS_LEVELS:
        if rl not in levels:
            result.warn(f"[readiness_rules.json] missing readiness level: {rl}")
    if isinstance(levels_data, dict):
        for level_name, level_data in levels_data.items():
            if isinstance(level_data, dict):
                if "required_fields" not in level_data and "required" not in level_data:
                    result.warn(
                        f"[readiness_rules.json:{level_name}] missing required_fields"
                    )
                if "allowed_actions" not in level_data and "actions" not in level_data:
                    result.warn(
                        f"[readiness_rules.json:{level_name}] missing allowed_actions"
                    )


def validate_json_file(fname: str, result: ValidationResult) -> None:
    path = MATRIX_DIR / fname
    if not path.exists():
        result.warn(f"[{fname}] file not found, skipping validation")
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        result.error(f"[{fname}] invalid JSON: {e}")
        return
    if fname == "field_dictionary.json":
        validate_field_dictionary(data, result)
    elif fname == "qualification_matrices.json":
        validate_matrices_json(data, result)


def validate_field_dictionary(data: any, result: ValidationResult) -> None:
    entries = data if isinstance(data, list) else [data]
    for entry in entries:
        if isinstance(entry, dict):
            fid = entry.get("field_id", entry.get("id", ""))
            if not fid:
                continue
            if entry.get("data_type", "") not in ALLOWED_DATA_TYPES:
                dt = entry.get("data_type", "")
                if dt:
                    result.warn(
                        f"[field_dictionary.json:{fid}] unexpected data_type: {dt}"
                    )
            if entry.get("question_priority") is not None:
                try:
                    qp = int(entry["question_priority"])
                    if qp < 1 or qp > 100:
                        result.warn(
                            f"[field_dictionary.json:{fid}] question_priority out of range: {qp}"
                        )
                except (ValueError, TypeError):
                    pass
            mr = entry.get("matching_role", "")
            if mr and mr not in ALLOWED_MATCHING_ROLES:
                result.warn(f"[field_dictionary.json:{fid}] unexpected matching_role: {mr}")
            pl = entry.get("privacy_level", "")
            if pl and pl not in ALLOWED_PRIVACY_LEVELS:
                result.warn(f"[field_dictionary.json:{fid}] unexpected privacy_level: {pl}")
            src = entry.get("source", "")
            if src and src not in ALLOWED_SOURCES:
                result.warn(f"[field_dictionary.json:{fid}] unexpected source: {src}")
            cf = entry.get("confidence", "")
            if cf and cf not in ALLOWED_CONFIDENCE:
                result.warn(f"[field_dictionary.json:{fid}] unexpected confidence: {cf}")
            qt = entry.get("question_template", "")
            if qt and not qt.strip().endswith("?"):
                if qt.strip() not in ("—", "-"):
                    result.warn(f"[field_dictionary.json:{fid}] question_template may not end with '?': {qt}")


def validate_matrices_json(data: any, result: ValidationResult) -> None:
    entries = data if isinstance(data, list) else [data]
    for entry in entries:
        if isinstance(entry, dict):
            mid = entry.get("matrix_id", "")
            if mid and mid in result.matrix_ids:
                pass
            elif mid:
                result.matrix_ids.add(mid)


def validate_field_completeness(result: ValidationResult) -> None:
    fd_path = MATRIX_DIR / "field_dictionary.json"
    if not fd_path.exists():
        result.warn("[field_completeness] field_dictionary.json not found, using inline fields only")
        return
    try:
        fd_data = json.loads(fd_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return
    if isinstance(fd_data, dict):
        fd_list = [fd_data]
    elif isinstance(fd_data, list):
        fd_list = fd_data
    else:
        return
    for entry in fd_list:
        fid = entry.get("field_id", entry.get("id", ""))
        if not fid:
            continue
        for req_key in ["field_id", "label", "data_type", "validation_rules",
                        "question_template"]:
            if req_key not in entry:
                result.error(f"[field_dictionary.json:{fid}] missing required key: {req_key}")


def parse_all_matrices(files: dict[str, str], result: ValidationResult) -> None:
    parsers = {
        "residential_search_matrices.md": parse_residential_matrix,
        "commercial_property_matrices.md": parse_commercial_matrix,
        "land_search_matrices.md": parse_land_matrix,
        "financing_request_matrices.md": parse_financing_matrix,
        "professional_service_matrices.md": parse_yaml_matrix,
        "real_estate_service_matrices.md": parse_yaml_matrix,
    }
    for fname, text in files.items():
        if not fname.endswith(".md") or fname.startswith("_"):
            continue
        if fname in parsers:
            parser = parsers[fname]
        else:
            ext = text.find("```")
            if ext >= 0 and "yaml" in text[ext:ext+10]:
                parser = parse_yaml_matrix
            elif "matrix_id" in text.lower()[:500]:
                parser = parse_commercial_matrix
            else:
                continue
        i = 0
        lines = text.split("\n")
        while i < len(lines):
            matrix, next_i = parser(text, i if parser != parse_yaml_matrix else i)
            if matrix and matrix.get("matrix_id", matrix.get("service_id", "")):
                result.matrices.append(matrix)
                validate_matrix_content(matrix, fname, result)
                validate_business_rules(matrix, fname, result)
            if next_i > i:
                i = next_i
            else:
                i += 1
        validate_forbidden_patterns(text, fname, result)


def main() -> int:
    result = ValidationResult()
    files = read_all_files(result)
    parse_all_matrices(files, result)
    validate_field_completeness(result)
    validate_readiness_rules(result)
    for json_file in ["qualification_matrices.json", "field_dictionary.json",
                       "readiness_rules.json", "question_rules.json",
                       "matching_semantics.json"]:
        if json_file in files:
            validate_json_file(json_file, result)

    missing_required = [f for f in REQUIRED_FILES if f not in files]
    files_checked = len(set(files.keys()) | set(REQUIRED_FILES))
    files_present_count = len(files)

    print("=" * 52)
    print("  QUALIFICATION MATRICES VALIDATION REPORT")
    print("=" * 52)
    print(f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Directory: {MATRIX_DIR}")
    print()
    print(f"  FILES CHECKED: {files_present_count}/{files_checked}")
    print(f"  MATRICES FOUND: {len(result.matrices)}")
    print(f"  FIELDS FOUND: {len(result.fields_found)}")
    print()

    unique_ids_pass = len(result.matrices) == len(result.matrix_ids)
    id_errors = [e for e in result.errors if "duplicate" in e or "missing matrix_id" in e]
    readiness_errors = [e for e in result.errors if "readiness" in e]
    completeness_errors = [e for e in result.errors if "completeness" in e or "required key" in e]
    business_errors = [e for e in result.errors if "business" in e or "forbidden" in e
                       or "chambres" in e or "land" in e]
    source_errors = [e for e in result.errors if "source" in e.lower() or "confidence" in e.lower()]
    forbidden_errors = [e for e in result.errors if "standing" in e or "question" in e.lower()]

    print("  RESULTS:")
    print(f"  - Unique matrix IDs:        {'PASS' if unique_ids_pass else 'FAIL'}"
          f"{'  (' + str(len(result.matrices) - len(result.matrix_ids)) + ' duplicates)' if not unique_ids_pass else ''}")
    print(f"  - Required readiness levels: {'PASS' if not readiness_errors else 'FAIL'}")
    print(f"  - Field completeness:       {'PASS' if not completeness_errors else 'FAIL'}")
    print(f"  - Business rules:           {'PASS' if not business_errors else 'FAIL'}")
    print(f"  - Source validation:        {'PASS' if not source_errors else 'FAIL'}")
    print(f"  - Forbidden patterns:       {'PASS' if not forbidden_errors else 'FAIL'}")
    print()

    all_errors = result.errors
    if id_errors:
        all_errors = id_errors + [e for e in all_errors if e not in id_errors]

    if all_errors:
        print("  ERRORS:")
        for idx, err in enumerate(all_errors, 1):
            print(f"  {idx}. {err}")
        print()
    else:
        print("  ERRORS: None")
        print()

    if result.warnings:
        print("  WARNINGS:")
        for idx, warn in enumerate(result.warnings, 1):
            print(f"  {idx}. {warn}")
        print()

    verdict = "FAIL" if all_errors else "PASS"
    print(f"  VERDICT: {verdict}")
    print()

    if missing_required:
        print(f"  Note: {len(missing_required)} expected files not found on disk.")
    return 1 if all_errors else 0


if __name__ == "__main__":
    sys.exit(main())
