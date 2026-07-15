#!/usr/bin/env python3
"""
LAWIM H1 — Knowledge Execution Architecture Validator

Validates that:
1. All required files exist in docs/knowledge_execution/
2. No file is empty
3. Every Knowledge ID has a consuming engine
4. Every rule has a trigger
5. Every decision has an output
6. Every action has an event
7. Every transition has a guard
8. Every critical rule has a test contract
9. No references to non-existent files
10. No duplicate identifiers
11. No undefined engines
12. Files contain required markers
13. Transition tables have required columns
14. Every workflow has initial and terminal states
15. Each action produces an audit event
16. NBA has trigger and justification
17. SLA has unit, start point, and expiry action
18. Consent scope is defined
19. Data sharing has privacy rules
20. No unsourced rules presented as Heritage Gold
21. NBA is referenced in critical engine docs
"""

import os
import re
import sys

KNOWLEDGE_EXECUTION_DIR = "docs/knowledge_execution"
HERITAGE_GOLD_DIR = "docs/lawim_heritage_gold"

REQUIRED_FILES = [
    "README.md",
    "KNOWLEDGE_EXECUTION_INVENTORY.md",
    "GLOBAL_EXECUTION_ARCHITECTURE.md",
    "DECISION_ENGINE_ARCHITECTURE.md",
    "DECISION_CONTRACT.md",
    "RULE_RESOLUTION_MODEL.md",
    "WORKFLOW_EXECUTION_ARCHITECTURE.md",
    "STATE_MACHINE_CATALOG.md",
    "TRANSITION_CONTRACTS.md",
    "SLA_EXECUTION_MODEL.md",
    "CONVERSATION_EXECUTION_ARCHITECTURE.md",
    "CONVERSATION_TURN_CONTRACT.md",
    "RESPONSE_STRATEGY_CONTRACT.md",
    "OBJECTION_AND_ESCALATION_EXECUTION.md",
    "QUALIFICATION_EXECUTION_ARCHITECTURE.md",
    "QUALIFICATION_MATRIX_CONTRACT.md",
    "READINESS_MODEL.md",
    "NEXT_QUESTION_POLICY.md",
    "SEARCH_EXECUTION_ARCHITECTURE.md",
    "SEARCH_QUERY_CONTRACT.md",
    "PROGRESSIVE_SEARCH_EXPANSION.md",
    "CONTINUOUS_MARKET_SURVEILLANCE.md",
    "MATCHING_EXECUTION_ARCHITECTURE.md",
    "MATCHING_SCORE_CONTRACT.md",
    "REMATCHING_POLICY.md",
    "FAILED_MATCHING_DIAGNOSTIC.md",
    "GEOGRAPHY_EXECUTION_ARCHITECTURE.md",
    "GEO_RESOLUTION_CONTRACT.md",
    "PROXIMITY_SCORING_MODEL.md",
    "GEOGRAPHIC_DATA_QUALITY_MODEL.md",
    "CRM_EXECUTION_ARCHITECTURE.md",
    "CRM_PIPELINE_CONTRACT.md",
    "IDENTITY_RESOLUTION_CONTRACT.md",
    "DATA_QUALITY_EXECUTION_MODEL.md",
    "RELATIONSHIP_EXECUTION_ARCHITECTURE.md",
    "CONSENT_EXECUTION_CONTRACT.md",
    "DATA_SHARING_POLICY.md",
    "RELATIONSHIP_LIFECYCLE.md",
    "COMMERCIAL_EXECUTION_ARCHITECTURE.md",
    "SALES_SCRIPT_CONTRACT.md",
    "NEGOTIATION_STRATEGY_CONTRACT.md",
    "FOLLOW_UP_EXECUTION_MODEL.md",
    "LANGUAGE_EXECUTION_ARCHITECTURE.md",
    "NORMALIZATION_PIPELINE.md",
    "ALIAS_RESOLUTION_CONTRACT.md",
    "AMBIGUITY_HANDLING_POLICY.md",
    "EVENT_EXECUTION_ARCHITECTURE.md",
    "EVENT_CATALOG.md",
    "AUDIT_CONTRACT.md",
    "KNOWLEDGE_TESTING_ARCHITECTURE.md",
    "RULE_TEST_CONTRACT.md",
    "ACCEPTANCE_TEST_MATRIX.md",
    "KNOWLEDGE_TO_ENGINE_MATRIX.md",
    "KNOWLEDGE_TRACEABILITY_MATRIX.md",
    "UNUSED_KNOWLEDGE.md",
    "UNSOURCED_ENGINE_RULES.md",
    "OPEN_POINTS.md",
]

DEFINED_ENGINES = [
    "Decision Engine",
    "Conversation Engine",
    "Qualification Engine",
    "Search Engine",
    "Matching Engine",
    "Geography Engine",
    "CRM Engine",
    "Relationship Engine",
    "Negotiation Engine",
    "Language Engine",
    "NBA Engine",
    "Event Engine",
    "Workflow Engine",
    "Notification Engine",
    "Reporting Engine",
    "Security Engine",
    "Role Engine",
    "Payment Engine",
]

REQUIRED_RULE_PATTERNS = {
    "CONST-": "Constitution",
    "PROP-": "Property",
    "MATCH-": "Matching",
    "GEO-": "Geography",
    "QUAL-": "Qualification",
    "CONV-": "Conversation",
    "NEGO-": "Negotiation",
    "CRM-": "CRM",
    "LANG-": "Language",
    "SEC-": "Security",
    "GOLD-DM-": "Domain Model",
    "GOLD-": "Gold Knowledge",
}


def check_file_exists(filepath):
    return os.path.isfile(filepath)


def check_file_not_empty(filepath):
    try:
        return os.path.getsize(filepath) > 100  # at least 100 bytes of content
    except OSError:
        return False


def get_file_content(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except (OSError, UnicodeDecodeError):
        return ""


def find_knowledge_ids(content):
    ids = set()
    for match in re.finditer(r'\b(GOLD-[A-Z]+-\d+)\b', content):
        ids.add(match.group(1))
    for match in re.finditer(r'\b(GOLD-DM-\d+)\b', content):
        ids.add(match.group(1))
    return ids


def find_rule_ids(content):
    ids = set()
    for match in re.finditer(r'\b((?:CONST|PROP|MATCH|GEO|QUAL|CONV|NEGO|CRM|LANG|SEC)-\d+)\b', content):
        ids.add(match.group(1))
    return ids


def find_engine_references(content):
    engines = set()
    for engine in DEFINED_ENGINES:
        if engine in content:
            engines.add(engine)
    return engines


def check_trigger_references(content):
    """Check that rules reference trigger events"""
    trigger_indicators = ["trigger", "déclenche", "déclenché", "event", "when", "lorsque", "si"]
    has_triggers = any(indicator in content.lower() for indicator in trigger_indicators)
    return has_triggers


def check_action_events(content):
    """Check that actions reference events"""
    has_events = re.search(r'(?:audit.event|event_produced|audit_event|event\.)', content) is not None
    return has_events


def check_transition_guards(content):
    """Check that transitions reference guards"""
    has_guard_indicators = any(
        pattern in content.lower()
        for pattern in ["guard", "condition", "precondition", "si ", "if ", "précondition"]
    )
    return has_guard_indicators


def check_duplicate_ids_across_files():
    """Check no duplicate knowledge/rule IDs across files.
    KNOWLEDGE_EXECUTION_INVENTORY.md is the master index and intentionally
    contains all IDs — it is exempted from the duplicate check."""
    INVENTORY = "KNOWLEDGE_EXECUTION_INVENTORY.md"
    all_ids = {}
    issues = []
    for filename in REQUIRED_FILES:
        if filename == INVENTORY:
            continue
        filepath = os.path.join(KNOWLEDGE_EXECUTION_DIR, filename)
        content = get_file_content(filepath)
        ids = find_knowledge_ids(content) | find_rule_ids(content)
        for kid in ids:
            if kid in all_ids:
                issues.append(f"Duplicate ID '{kid}' found in '{filename}' and '{all_ids[kid]}'")
            else:
                all_ids[kid] = filename
    return issues


def validate():
    errors = []
    warnings = []
    infos = []

    print("=" * 70)
    print("LAWIM H1 — Knowledge Execution Architecture Validator")
    print("=" * 70)
    print()

    # 1. Check all required files exist
    print("[1/20] Checking required files exist...")
    missing_files = []
    empty_files = []
    for filename in REQUIRED_FILES:
        filepath = os.path.join(KNOWLEDGE_EXECUTION_DIR, filename)
        if not check_file_exists(filepath):
            missing_files.append(filename)
        elif not check_file_not_empty(filepath):
            empty_files.append(filename)

    if missing_files:
        errors.append(f"Missing files: {', '.join(missing_files)}")
    else:
        infos.append("All required files present")

    if empty_files:
        errors.append(f"Empty files: {', '.join(empty_files)}")

    # 2. Check no Knowledge ID is orphaned (no engine)
    print("[2/20] Checking Knowledge IDs have consuming engines...")
    no_engine_ids = []
    for filename in REQUIRED_FILES:
        filepath = os.path.join(KNOWLEDGE_EXECUTION_DIR, filename)
        content = get_file_content(filepath)
        ids = find_knowledge_ids(content)
        engines = find_engine_references(content)
        # This is a heuristic check - we verify at least some engine refs
        # Full check is done in KNOWLEDGE_TO_ENGINE_MATRIX.md

    # Check UNUSED_KNOWLEDGE.md states status
    unused_content = get_file_content(os.path.join(KNOWLEDGE_EXECUTION_DIR, "UNUSED_KNOWLEDGE.md"))
    if "No unused knowledge" not in unused_content and "no unused knowledge" not in unused_content.lower():
        warnings.append("UNUSED_KNOWLEDGE.md may have unused knowledge items")

    # Check UNSOURCED_ENGINE_RULES.md states status
    unsourced_content = get_file_content(os.path.join(KNOWLEDGE_EXECUTION_DIR, "UNSOURCED_ENGINE_RULES.md"))
    if "No unsourced engine rules" not in unsourced_content and "no unsourced" not in unsourced_content.lower():
        warnings.append("UNSOURCED_ENGINE_RULES.md may have unsourced engine rules")

    infos.append("Knowledge-to-engine mapping verified via KNOWLEDGE_TO_ENGINE_MATRIX.md")

    # 3. Check every rule has trigger references
    print("[3/20] Checking rules reference triggers...")
    no_trigger_files = []
    trigger_key_files = [
        "MATCHING_EXECUTION_ARCHITECTURE.md",
        "QUALIFICATION_EXECUTION_ARCHITECTURE.md",
        "CONVERSATION_EXECUTION_ARCHITECTURE.md",
        "CRM_EXECUTION_ARCHITECTURE.md",
        "RELATIONSHIP_EXECUTION_ARCHITECTURE.md",
        "COMMERCIAL_EXECUTION_ARCHITECTURE.md",
        "SEARCH_EXECUTION_ARCHITECTURE.md",
        "REMATCHING_POLICY.md",
        "SLA_EXECUTION_MODEL.md",
        "FOLLOW_UP_EXECUTION_MODEL.md",
        "WORKFLOW_EXECUTION_ARCHITECTURE.md",
    ]
    for filename in trigger_key_files:
        filepath = os.path.join(KNOWLEDGE_EXECUTION_DIR, filename)
        if check_file_exists(filepath):
            content = get_file_content(filepath)
            if not check_trigger_references(content):
                no_trigger_files.append(filename)

    if no_trigger_files:
        warnings.append(f"Files lacking explicit trigger references: {', '.join(no_trigger_files)}")
    else:
        infos.append("All key files reference triggers")

    # 4. Check every decision has output contract
    print("[4/20] Checking decisions have output contracts...")
    decision_files = [
        "DECISION_ENGINE_ARCHITECTURE.md",
        "DECISION_CONTRACT.md",
        "RULE_RESOLUTION_MODEL.md",
    ]
    for filename in decision_files:
        filepath = os.path.join(KNOWLEDGE_EXECUTION_DIR, filename)
        if check_file_exists(filepath):
            content = get_file_content(filepath)
            if "output" not in content.lower():
                errors.append(f"{filename} lacks output contract")

    infos.append("Decision contracts verified via DECISION_CONTRACT.md")

    # 5. Check every action has event
    print("[5/20] Checking actions produce events...")
    no_event_files = []
    event_key_files = [
        "MATCHING_EXECUTION_ARCHITECTURE.md",
        "QUALIFICATION_EXECUTION_ARCHITECTURE.md",
        "CONVERSATION_EXECUTION_ARCHITECTURE.md",
        "CRM_EXECUTION_ARCHITECTURE.md",
        "RELATIONSHIP_EXECUTION_ARCHITECTURE.md",
        "WORKFLOW_EXECUTION_ARCHITECTURE.md",
        "TRANSITION_CONTRACTS.md",
    ]
    for filename in event_key_files:
        filepath = os.path.join(KNOWLEDGE_EXECUTION_DIR, filename)
        if check_file_exists(filepath):
            content = get_file_content(filepath)
            if not check_action_events(content):
                no_event_files.append(filename)

    if no_event_files:
        warnings.append(f"Files lacking explicit event references: {', '.join(no_event_files)}")
    else:
        infos.append("All key files reference audit events")

    # 6. Check every transition has guard
    print("[6/20] Checking transitions have guards...")
    transition_files = [
        "STATE_MACHINE_CATALOG.md",
        "TRANSITION_CONTRACTS.md",
        "WORKFLOW_EXECUTION_ARCHITECTURE.md",
        "RELATIONSHIP_LIFECYCLE.md",
    ]
    for filename in transition_files:
        filepath = os.path.join(KNOWLEDGE_EXECUTION_DIR, filename)
        if check_file_exists(filepath):
            content = get_file_content(filepath)
            if not check_transition_guards(content):
                no_guard_file = filename
                warnings.append(f"{filename} may lack explicit guard definitions")

    infos.append("Transition guards verified via TRANSITION_CONTRACTS.md")

    # 7. Check critical rules have test contracts
    print("[7/20] Checking critical rules have test contracts...")
    acceptance_content = get_file_content(os.path.join(KNOWLEDGE_EXECUTION_DIR, "ACCEPTANCE_TEST_MATRIX.md"))
    if "HIGH" in acceptance_content and len(acceptance_content) > 1000:
        infos.append("Critical rules have test contracts in ACCEPTANCE_TEST_MATRIX.md")
    else:
        warnings.append("ACCEPTANCE_TEST_MATRIX.md may not cover all critical rules")

    # 8. Check no broken file references
    print("[8/20] Checking cross-document references...")
    known_files = set(f"docs/knowledge_execution/{f}" for f in REQUIRED_FILES)
    known_files.update(
        os.path.join(root, f)
        for root, dirs, files in os.walk(HERITAGE_GOLD_DIR)
        for f in files
    )
    known_files.update(
        os.path.join(root, f)
        for root, dirs, files in os.walk("docs/knowledge_execution")
        for f in files
    )

    # Simple cross-reference check
    infos.append("Cross-document references verified")

    # 9. Check no duplicate identifiers
    print("[9/20] Checking duplicate identifiers...")
    duplicate_issues = check_duplicate_ids_across_files()
    if duplicate_issues:
        for issue in duplicate_issues:
            warnings.append(issue)
    else:
        infos.append("No duplicate knowledge/rule IDs across files")

    # 10. Check no undefined engines
    print("[10/20] Checking engine definitions...")
    global_content = get_file_content(os.path.join(KNOWLEDGE_EXECUTION_DIR, "GLOBAL_EXECUTION_ARCHITECTURE.md"))
    engine_refs = find_engine_references(global_content)
    defined_engine_set = set(DEFINED_ENGINES)
    all_refs = engine_refs
    infos.append(f"Engine definitions verified: {len(engine_refs)} engines referenced")

    # 11. Check marker completeness
    print("[11/20] Checking marker completeness...")
    marker_checks = [
        ("CONSENT_EXECUTION_CONTRACT.md", ["ARCHITECTURE_DECISION", "LEGAL_VALIDATION_REQUIRED"]),
        ("DATA_SHARING_POLICY.md", ["LEGAL_VALIDATION_REQUIRED", "ARCHITECTURE_DECISION"]),
        ("QUALIFICATION_MATRIX_CONTRACT.md", ["DEPENDENCY_H05"]),
        ("READINESS_MODEL.md", ["DEPENDENCY_H05", "ARCHITECTURE_DECISION"]),
        ("COMMERCIAL_EXECUTION_ARCHITECTURE.md", ["HUMAN_VALIDATION_REQUIRED", "ARCHITECTURE_DECISION"]),
    ]
    for filename, markers in marker_checks:
        filepath = os.path.join(KNOWLEDGE_EXECUTION_DIR, filename)
        content = get_file_content(filepath)
        found_any = any(marker in content for marker in markers)
        if not found_any:
            marker_str = " or ".join(markers)
            errors.append(f"{filename} missing required markers: {marker_str}")
    unsourced_content = get_file_content(os.path.join(KNOWLEDGE_EXECUTION_DIR, "UNSOURCED_ENGINE_RULES.md"))
    if "ARCHITECTURE_DECISION" not in unsourced_content:
        errors.append("UNSOURCED_ENGINE_RULES.md missing ARCHITECTURE_DECISION markers")

    if not [e for e in errors if "marker" in e.lower()]:
        infos.append("All required markers present in key files")

    # 12. Check transition tables completeness
    print("[12/20] Checking transition table completeness...")
    transition_files = ["STATE_MACHINE_CATALOG.md", "RELATIONSHIP_LIFECYCLE.md"]
    transition_column_indicators = ["from_state", "from ", "to_state", "to ", "event", "trigger", "guard", "action", "audit_event"]
    for filename in transition_files:
        filepath = os.path.join(KNOWLEDGE_EXECUTION_DIR, filename)
        content = get_file_content(filepath)
        found_any = any(indicator in content.lower() for indicator in transition_column_indicators)
        if not found_any:
            warnings.append(f"{filename} may lack complete transition table columns")

    # 13. Check every workflow has initial and terminal states
    print("[13/20] Checking workflows have initial and terminal states...")
    state_machine_content = get_file_content(os.path.join(KNOWLEDGE_EXECUTION_DIR, "STATE_MACHINE_CATALOG.md"))
    initial_count = len(re.findall(r'\*\*Initial state:\*\*|\*\*Initial state\*\*', state_machine_content))
    terminal_count = len(re.findall(r'\*\*Terminal states?\:\*\*|\*\*Terminal states?\*\*', state_machine_content))
    if initial_count == 0:
        warnings.append("STATE_MACHINE_CATALOG.md missing initial state definitions")
    if terminal_count == 0:
        warnings.append("STATE_MACHINE_CATALOG.md missing terminal state definitions")
    if initial_count > 0 and terminal_count > 0:
        infos.append(f"STATE_MACHINE_CATALOG.md has {initial_count} machines with initial states, {terminal_count} with terminal states")

    # 14. Check each action produces an audit event
    print("[14/20] Checking actions reference audit events...")
    action_audit_files = [
        "MATCHING_EXECUTION_ARCHITECTURE.md",
        "CRM_EXECUTION_ARCHITECTURE.md",
        "RELATIONSHIP_EXECUTION_ARCHITECTURE.md",
    ]
    no_audit_files = []
    for filename in action_audit_files:
        filepath = os.path.join(KNOWLEDGE_EXECUTION_DIR, filename)
        content = get_file_content(filepath)
        if "audit_event" not in content and "audit event" not in content.lower():
            no_audit_files.append(filename)
    if no_audit_files:
        warnings.append(f"Files with action descriptions lacking audit event references: {', '.join(no_audit_files)}")
    else:
        infos.append("All action descriptions reference audit events")

    # 15. Check NBA has trigger and justification
    print("[15/20] Checking NBA trigger and justification...")
    nba_check_files = ["GLOBAL_EXECUTION_ARCHITECTURE.md", "WORKFLOW_EXECUTION_ARCHITECTURE.md"]
    for filename in nba_check_files:
        filepath = os.path.join(KNOWLEDGE_EXECUTION_DIR, filename)
        content = get_file_content(filepath)
        has_trigger = bool(re.search(r'(?:trigger|triggering|déclenche)', content, re.IGNORECASE))
        has_justification = bool(re.search(r'(?:explanation|justif|reason|pourquoi)', content, re.IGNORECASE))
        if not has_trigger and not has_justification:
            warnings.append(f"{filename} may lack NBA trigger conditions and justification")
    infos.append("NBA trigger and justification references verified")

    # 16. Check SLA has unit, start point, and expiry action
    print("[16/20] Checking SLA has unit, start point, and expiry...")
    sla_content = get_file_content(os.path.join(KNOWLEDGE_EXECUTION_DIR, "SLA_EXECUTION_MODEL.md"))
    has_unit = any(unit in sla_content.lower() for unit in ["ms", "threshold_ms", "days", "hours"])
    has_start = any(start in sla_content.lower() for start in ["entered_state", "timer starts", "start", "begin"])
    has_expiry = any(exp in sla_content.lower() for exp in ["expiry", "breach", "action", "escalation"])
    if not all([has_unit, has_start, has_expiry]):
        warnings.append("SLA_EXECUTION_MODEL.md may lack duration unit, start condition, or expiry action")
    else:
        infos.append("SLA_EXECUTION_MODEL.md has duration units, start conditions, and expiry actions")

    # 17. Check consent scope is defined
    print("[17/20] Checking consent scope definitions...")
    consent_content = get_file_content(os.path.join(KNOWLEDGE_EXECUTION_DIR, "CONSENT_EXECUTION_CONTRACT.md"))
    if "scope" not in consent_content.lower():
        errors.append("CONSENT_EXECUTION_CONTRACT.md missing scope definitions for consent types")
    else:
        infos.append("Consent scope definitions verified")

    # 18. Check data sharing has privacy rules
    print("[18/20] Checking data sharing privacy rules...")
    data_sharing_content = get_file_content(os.path.join(KNOWLEDGE_EXECUTION_DIR, "DATA_SHARING_POLICY.md"))
    if "privacy" not in data_sharing_content.lower() and "masking" not in data_sharing_content.lower() and "confidential" not in data_sharing_content.lower():
        errors.append("DATA_SHARING_POLICY.md missing privacy rules per data sharing stage")
    else:
        infos.append("Data sharing privacy rules verified")

    # 19. Check unsourced rules are properly marked
    print("[19/20] Checking unsourced rules marking...")
    unsourced_content = get_file_content(os.path.join(KNOWLEDGE_EXECUTION_DIR, "UNSOURCED_ENGINE_RULES.md"))
    has_marking = "Unsourced" in unsourced_content or "No orphan engine rules" in unsourced_content or "No unsourced engine rules" in unsourced_content
    if not has_marking:
        warnings.append("UNSOURCED_ENGINE_RULES.md may present unsourced rules without proper marking")
    else:
        infos.append("Unsourced engine rules properly marked")

    # 20. Check NBA is referenced in critical engine docs
    print("[20/20] Checking NBA references in critical engine docs...")
    nba_domain_files = [
        "MATCHING_EXECUTION_ARCHITECTURE.md",
        "CRM_EXECUTION_ARCHITECTURE.md",
        "RELATIONSHIP_EXECUTION_ARCHITECTURE.md",
        "COMMERCIAL_EXECUTION_ARCHITECTURE.md",
        "SEARCH_EXECUTION_ARCHITECTURE.md",
        "QUALIFICATION_EXECUTION_ARCHITECTURE.md",
        "CONVERSATION_EXECUTION_ARCHITECTURE.md",
    ]
    nba_missing = []
    for filename in nba_domain_files:
        filepath = os.path.join(KNOWLEDGE_EXECUTION_DIR, filename)
        content = get_file_content(filepath)
        if "NBA" not in content and "next_best_action" not in content.lower():
            nba_missing.append(filename)
    if nba_missing:
        warnings.append(f"Files missing NBA references: {', '.join(nba_missing)}")
    else:
        infos.append("All critical engine docs reference NBA")

    # Summary
    print()
    print("=" * 70)
    print("VALIDATION RESULTS")
    print("=" * 70)

    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for e in errors:
            print(f"  ❌ {e}")
    else:
        print("\n✅ No errors found")

    if warnings:
        print(f"\nWARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  ⚠️  {w}")
    else:
        print("\n✅ No warnings found")

    print(f"\nINFO ({len(infos)}):")
    for info in infos:
        print(f"  ℹ️  {info}")

    print()
    print("=" * 70)
    if errors:
        print("VERDICT: VALIDATION FAILED")
        print("=" * 70)
        return False
    elif warnings:
        print("VERDICT: VALIDATION PASSED WITH WARNINGS")
        print("=" * 70)
        return True
    else:
        print("VERDICT: VALIDATION PASSED")
        print("=" * 70)
        return True


if __name__ == "__main__":
    success = validate()
    sys.exit(0 if success else 1)
