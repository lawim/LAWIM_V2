#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "docs" / "canonical"
REQUIRED = [
    "README.md",
    "00_LAWIM_VISION_AND_SCOPE.md",
    "01_PRINCIPLES_AND_GOVERNANCE.md",
    "02_USERS_ROLES_AND_ACTORS.md",
    "03_DOMAIN_BOUNDARIES.md",
    "04_CANONICAL_DATA_MODEL.md",
    "05_PROJECTS_AND_DOSSIERS.md",
    "06_PROPERTIES_AND_LISTINGS.md",
    "07_CONVERSATION_TARGET_SPECIFICATION.md",
    "08_QUALIFICATION_TARGET_SPECIFICATION.md",
    "09_SEARCH_AND_MATCHING_TARGET_SPECIFICATION.md",
    "10_RELATIONSHIP_TARGET_SPECIFICATION.md",
    "11_VISITS_COMMERCIAL_AND_TRANSACTION_FLOW.md",
    "12_DOCUMENTS_AND_LEGAL_INFORMATION.md",
    "13_FINANCIAL_CORE_AND_CAMPAY.md",
    "14_CHANNELS_AND_OMNICHANNEL.md",
    "15_AI_GOVERNANCE.md",
    "16_FEATURE_MANAGEMENT.md",
    "17_ADMINISTRATION_AND_COCKPITS.md",
    "18_SECURITY_PRIVACY_AND_CONSENT.md",
    "19_EVENTS_OBSERVABILITY_AND_AUDIT.md",
    "20_TESTING_AND_ACCEPTANCE_STANDARD.md",
    "21_DEPLOYMENT_OPERATIONS_AND_RECOVERY.md",
    "22_REBUILD_SCOPE_AND_DECOMMISSION_PLAN.md",
    "23_TRACEABILITY_MATRIX.md",
    "24_GLOSSARY.md",
]
DOMAINS = {
    "Identity and Access", "Users and Profiles", "Channels and Communication", "CRM",
    "Properties and Listings", "Projects and Dossiers", "Documents and GED", "Conversation",
    "Qualification", "Search", "Matching", "Relationship", "Visits", "Commercial Follow-up",
    "Transactions", "Financial Core", "Campay", "Notifications", "Feature Management",
    "Administration and Cockpits", "Audit and Observability", "Backup and Disaster Recovery",
    "AI Governance", "Testing",
}
STATUS = {
    "NOT_IMPLEMENTED", "PARTIAL", "IMPLEMENTED_UNVERIFIED", "VERIFIED", "TO_DELETE", "TO_REBUILD",
    "KEEP_AS_IS", "KEEP_AND_CLEAN", "REVIEW", "DELETE", "REBUILD_FROM_ZERO", "MERGE", "SPLIT",
    "KEEP", "CLEAN", "REBUILD", "REMOVE_ROUTE", "REMOVE_TEST", "REMOVE_DOCUMENT", "UNVALIDATED",
}
REMOVED_REFS = [
    "docs/" + "Directive/", "docs/" + "platform/", "docs/" + "PRODUCT_BIBLE/", "docs/" + "strategy/",
    "docs/" + "Specifications/", "docs/" + "ADR/" + "ADR-001_Source_Intelligence_Engine.md",
    "Mission_" + "10_Report.md", "Mission_" + "11_Report.md", "Mission_" + "15_Platform_Readiness.md",
    "LAWIM_V2_" + "Conversation_Core_Runtime_Validation.md",
]

def fail(msg: str, errors: list[str]) -> None:
    errors.append(msg)

def main() -> int:
    errors: list[str] = []
    for name in REQUIRED:
        path = CANON / name
        if not path.exists():
            fail(f"missing canonical document: {name}", errors)
        elif path.stat().st_size < 200:
            fail(f"canonical document too small: {name}", errors)

    names = [p.name for p in CANON.glob("*.md")]
    if len(names) != len(set(names)):
        fail("duplicate canonical document filename", errors)

    req_ids: set[str] = set()
    trace = CANON / "23_TRACEABILITY_MATRIX.md"
    if trace.exists():
        text = trace.read_text(encoding="utf-8")
        for req in re.findall(r"\bREQ-[A-Z]+-\d{3}\b", text):
            if req in req_ids:
                fail(f"duplicate requirement id: {req}", errors)
            req_ids.add(req)
        for domain in ["Conversation", "Qualification", "Search", "Matching", "Relationship", "Financial Core", "Feature Management", "Backup and Disaster Recovery"]:
            if domain not in text:
                fail(f"traceability missing domain: {domain}", errors)
        for line in text.splitlines():
            if line.startswith("| REQ-"):
                parts = [part.strip() for part in line.strip("|").split("|")]
                if len(parts) >= 12:
                    domain = parts[1]
                    status = parts[10]
                    if domain not in DOMAINS:
                        fail(f"unauthorized domain in traceability: {domain}", errors)
                    if status not in STATUS:
                        fail(f"unauthorized status in traceability: {status}", errors)

    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for path in CANON.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        for target in link_pattern.findall(text):
            if target.startswith(("http://", "https://", "mailto:")) or target.startswith("#"):
                continue
            target_path = (path.parent / target.split("#", 1)[0]).resolve()
            if not target_path.exists():
                fail(f"broken link in {path.relative_to(ROOT)}: {target}", errors)
        for ref in REMOVED_REFS:
            if ref in text:
                fail(f"canonical doc references removed document {ref} in {path.name}", errors)

    for required_adr in range(1, 10):
        matches = list((ROOT / "docs" / "adr").glob(f"ADR-{required_adr:03d}-*.md"))
        if not matches:
            fail(f"missing ADR-{required_adr:03d}", errors)

    forbidden_dirs = [ROOT / "docs" / name for name in ("archive", "legacy", "old", "deprecated")]
    for directory in forbidden_dirs:
        if directory.exists():
            fail(f"forbidden archive-like directory exists: {directory.relative_to(ROOT)}", errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"canonical docs validation OK: {len(REQUIRED)} documents, {len(req_ids)} requirements")
    return 0

if __name__ == "__main__":
    sys.exit(main())
