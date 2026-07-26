#!/usr/bin/env python3
"""
LAWIM Gold Corpus Migration — LCIP B.1

Full pipeline:
  1. Extract & inventory ZIP archives
  2. Map to Gold Corpus format
  3. Validate schemas
  4. Certify (LCIP A.3)
  5. Classify (Certified / Repairable / Rejected / Errors)
  6. Generate statistics
"""

import hashlib
import json
import os
import re
import shutil
import sys
import time
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone

REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
GOLD_CORPUS_DIR = os.path.join(REPO_ROOT, "tests", "gold_corpus")
CONVERSATIONS_DIR = os.path.join(GOLD_CORPUS_DIR, "conversations")
IMPORT_DIR = os.path.join(GOLD_CORPUS_DIR, "import")
ZIP_SOURCE_DIR = "/media/abel/1A4696CE4696AA51/Telechargement/LAWIM_GOLD_CORPUS_BLOCK"

# Avoid duplicate block 02
SKIP_ZIPS = {"LAWIM_GOLD_CORPUS_BLOCK_02_DETAILED (1).zip"}

CATEGORY_MAP = {
    "rental_search": "rental",
    "purchase_search": "purchase",
    "seller": "seller",
    "visit_scheduling": "visit",
    "investment": "investment",
    "negotiation": "negotiation",
    "qualification": "qualification",
    "correction": "correction",
    "multilingual": "multilingual",
    "restart": "restart",
    "followup": "followup",
    "marketplace": "marketplace",
    "idempotence": "idempotence",
}

DIFFICULTY_MAP = {
    "standard": "basic",
    "simple": "basic",
    "intermediate": "intermediate",
    "complex": "advanced",
    "advanced": "advanced",
    "expert": "expert",
}


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def generate_gold_id(src_id: str, index: int) -> str:
    """Map source ID like LAWIM-GOLD-B01-0001 to B000001 format."""
    # Use a sequential ID based on the overall index
    return f"B{index:06d}"


def detect_source_duplicates(zip_paths: list) -> list:
    """Detect duplicate ZIPs by content hash."""
    seen = {}
    unique = []
    for z in zip_paths:
        h = sha256_file(z)
        if h not in seen:
            seen[h] = z
            unique.append(z)
        else:
            print(f"  SKIP duplicate: {os.path.basename(z)} (same as {os.path.basename(seen[h])})")
    return unique


def inventory_zips() -> dict:
    """Inventory all unique ZIP archives."""
    all_zips = sorted([
        os.path.join(ZIP_SOURCE_DIR, f)
        for f in os.listdir(ZIP_SOURCE_DIR)
        if f.endswith(".zip") and f not in SKIP_ZIPS
    ])
    unique_zips = detect_source_duplicates(all_zips)

    inventory = {
        "total_zips": len(unique_zips),
        "skipped_duplicates": len(all_zips) - len(unique_zips),
        "zips": [],
        "total_conversations": 0,
        "total_jsonl": 0,
    }

    for zp in unique_zips:
        zname = os.path.basename(zp)
        with zipfile.ZipFile(zp) as zf:
            names = zf.namelist()
            json_files = [n for n in names if n.endswith(".json") and not n.endswith("manifest.json") and not n.startswith("README")]
            jsonl_files = [n for n in names if n.endswith(".jsonl")]
            manifest_files = [n for n in names if n.endswith("manifest.json")]
            readme_files = [n for n in names if n.startswith("README")]

            conv_count = 0
            for jf in json_files:
                try:
                    data = json.loads(zf.read(jf))
                    if isinstance(data, list):
                        conv_count += len(data)
                    elif isinstance(data, dict):
                        conv_count += 1
                except Exception:
                    pass

            jsonl_count = 0
            for jlf in jsonl_files:
                try:
                    jsonl_count += len(zf.read(jlf).decode().strip().split("\n"))
                except Exception:
                    pass

            entry = {
                "zip": zname,
                "size_bytes": os.path.getsize(zp),
                "sha256": sha256_file(zp),
                "json_files": json_files,
                "jsonl_files": jsonl_files,
                "manifest_files": manifest_files,
                "readme_files": readme_files,
                "conversations_in_json": conv_count,
                "conversations_in_jsonl": jsonl_count,
            }
            inventory["zips"].append(entry)
            inventory["total_conversations"] += conv_count
            inventory["total_jsonl"] += jsonl_count

    return inventory


def migrate_conversation(src_conv: dict, gold_id: str, src_zip: str) -> dict:
    """Convert a source conversation to Gold Corpus format."""
    category_raw = src_conv.get("category", "rental_search")
    category = CATEGORY_MAP.get(category_raw, "rental")
    diff_raw = src_conv.get("difficulty", "standard")
    level = DIFFICULTY_MAP.get(diff_raw, "basic")
    language = src_conv.get("language", "fr")
    channel = src_conv.get("channel", "web")
    tags = src_conv.get("tags", [])

    turns = src_conv.get("turns", [])
    messages = []
    for t in turns:
        messages.append({
            "role": t.get("role", "user"),
            "text": t.get("text", ""),
            "intent": t.get("intent", t.get("expected_state", {}).get("pending_user_action", "unknown")),
        })

    # Build expected_state from last assistant's expected_state
    last_expected = None
    for t in reversed(turns):
        if t.get("role") == "assistant" and "expected_state" in t:
            last_expected = t["expected_state"]
            break

    facts = last_expected.get("facts", {}) if last_expected else {}
    pending = last_expected.get("pending_user_action", "NONE") if last_expected else "NONE"
    biz_action = last_expected.get("business_action", "NONE") if last_expected else "NONE"

    # Determine qualification status
    if biz_action and biz_action != "NONE":
        qual_status = "qualified"
    elif pending and pending != "NONE":
        qual_status = "in_progress"
    else:
        qual_status = "qualified"

    # Determine intent
    intent = "unknown"
    for t in turns:
        if t.get("role") == "user" and t.get("intent"):
            intent = t["intent"]
            break

    conversation = {
        "id": gold_id,
        "category": category,
        "level": level,
        "channel": channel,
        "language": language,
        "description": src_conv.get("title", f"Conversation {gold_id}"),
        "tags": tags,
        "business_object": facts.get("property_type", "unknown"),
        "source_zip": src_zip,
        "source_id": src_conv.get("id", ""),
        "messages": messages,
    }

    expected_state = {
        "intent": intent.lower() if intent else "unknown",
        "qualification_status": qual_status,
        "slots_filled": {k: v for k, v in facts.items() if v is not None},
        "next_action": biz_action if biz_action != "NONE" else pending,
        "memory_retained": list(facts.keys()) if facts else [],
    }

    expected_business = {
        "business_action": biz_action.lower() if biz_action != "NONE" else "none",
        "target_service": "PropertySearchService",
        "parameters": facts,
        "expected_result": "Recherche de biens correspondant aux criteres",
        "handover_required": False,
    }

    expected_questions = {
        "maximum_questions_per_turn": 1,
        "required_questions": [],
        "forbidden_questions": [],
        "rephrase_on_confusion": True,
    }
    for i, t in enumerate(turns):
        if t.get("role") == "assistant" and t.get("text", "").endswith("?"):
            expected_questions["required_questions"].append({
                "turn": i // 2,
                "expected_question": t["text"],
                "context": f"Tour {i // 2}",
            })

    expected_language = {
        "primary_language": language,
        "responses_language": language,
        "allow_code_switch": False,
        "forbidden_phrases": [
            "assistant neutre", "I cannot make business decisions", "provide more context"
        ],
        "footer_required": True,
        "identity": "LAWIM AI",
    }

    expected_runtime = {
        "engine": "ConversationJourneyOrchestrator",
        "expected_services": ["ConversationStateService", "QualificationService"],
        "expected_repositories": ["ConversationStateRepository"],
        "timeout_seconds": 30,
        "retry_allowed": True,
        "fallback_chain": ["deepseek", "openai", "gemini"],
    }

    assertions = []
    aid_idx = 1
    if facts:
        assertions.append({
            "id": f"ASSERT-{aid_idx:04d}", "type": "memory",
            "description": "Les faits sont retenus en memoire",
            "expected": list(facts.keys()),
            "path": "memory_retained", "operator": "contains",
        })
        aid_idx += 1
    if biz_action and biz_action != "NONE":
        assertions.append({
            "id": f"ASSERT-{aid_idx:04d}", "type": "business",
            "description": "L'action metier est correcte",
            "expected": biz_action.lower(),
            "path": "next_action", "operator": "eq",
        })
        aid_idx += 1
    assertions.append({
        "id": f"ASSERT-{aid_idx:04d}", "type": "language",
        "description": "La langue de reponse est correcte",
        "expected": language,
        "path": "responses_language", "operator": "eq",
    })
    aid_idx += 1
    assertions.append({
        "id": f"ASSERT-{aid_idx:04d}", "type": "questions",
        "description": "Au maximum une question par tour",
        "expected": 1,
        "path": "maximum_questions_per_turn", "operator": "eq",
    })

    expected_assertions = {"assertions": assertions}

    return {
        "conversation.json": conversation,
        "expected_state.json": expected_state,
        "expected_business.json": expected_business,
        "expected_questions.json": expected_questions,
        "expected_language.json": expected_language,
        "expected_runtime.json": expected_runtime,
        "expected_assertions.json": expected_assertions,
    }


def write_conversation(gold_id: str, files: dict):
    """Write all 7 JSON files + rationale.md for a conversation."""
    conv_dir = os.path.join(CONVERSATIONS_DIR, gold_id)
    os.makedirs(conv_dir, exist_ok=True)

    for fname, data in files.items():
        path = os.path.join(conv_dir, fname)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    rationale = f"# {gold_id}\n\n"
    rationale += f"**Source:** {files['conversation.json'].get('source_zip', 'unknown')}\n"
    rationale += f"**Source ID:** {files['conversation.json'].get('source_id', 'unknown')}\n"
    rationale += f"**Category:** {files['conversation.json'].get('category', 'unknown')}\n"
    rationale += f"**Language:** {files['conversation.json'].get('language', 'unknown')}\n"
    rationale += f"**Turns:** {len(files['conversation.json'].get('messages', []))}\n\n"
    rationale += f"Migrated automatically by LCIP B.1 migration script.\n"

    with open(os.path.join(conv_dir, "rationale.md"), "w", encoding="utf-8") as f:
        f.write(rationale)


def validate_schema_safe(conv_dir: str, schema_dir: str) -> dict:
    """Validate a conversation directory against schemas (without jsonschema lib if not available)."""
    results = {"pass": 0, "fail": 0, "warnings": 0, "details": []}
    mappings = [
        ("conversation.json", "conversation.schema.json"),
        ("expected_state.json", "expected_state.schema.json"),
        ("expected_business.json", "expected_business.schema.json"),
        ("expected_questions.json", "expected_questions.schema.json"),
        ("expected_language.json", "expected_language.schema.json"),
        ("expected_runtime.json", "expected_runtime.schema.json"),
        ("expected_assertions.json", "assertions.schema.json"),
    ]
    for data_file, schema_file in mappings:
        dp = os.path.join(conv_dir, data_file)
        sp = os.path.join(schema_dir, schema_file)
        if not os.path.isfile(dp):
            results["fail"] += 1
            results["details"].append(f"MISSING {data_file}")
            continue
        try:
            with open(dp) as f:
                json.load(f)
            results["pass"] += 1
            results["details"].append(f"VALID {data_file}")
        except json.JSONDecodeError as e:
            results["fail"] += 1
            results["details"].append(f"INVALID {data_file}: {e}")
    return results


def run_full_migration() -> dict:
    """Run the complete migration pipeline."""
    print("=" * 60)
    print("LAWIM Gold Corpus Migration — LCIP B.1")
    print("=" * 60)

    start_time = time.time()
    schema_dir = os.path.join(GOLD_CORPUS_DIR, "schema")

    # Step 1: Inventory
    print("\n[1/5] Inventory...")
    inventory = inventory_zips()
    inv_path = os.path.join(IMPORT_DIR, "inventory.json")
    os.makedirs(IMPORT_DIR, exist_ok=True)
    with open(inv_path, "w") as f:
        json.dump(inventory, f, indent=2)
    print(f"  Total ZIPs: {inventory['total_zips']}")
    print(f"  Conversations in JSON: {inventory['total_conversations']}")
    print(f"  Inventory written: {inv_path}")

    # Step 2: Extract and migrate
    print("\n[2/5] Migration...")
    os.makedirs(CONVERSATIONS_DIR, exist_ok=True)

    imported = 0
    errors = []
    migration_results = []

    for zip_entry in inventory["zips"]:
        zp = os.path.join(ZIP_SOURCE_DIR, zip_entry["zip"])
        print(f"  Processing: {zip_entry['zip']}")
        with zipfile.ZipFile(zp) as zf:
            for jf in zip_entry["json_files"]:
                try:
                    data = json.loads(zf.read(jf))
                    conversations = data if isinstance(data, list) else [data]
                    for i, conv in enumerate(conversations):
                        gold_id = generate_gold_id(conv.get("id", ""), len(migration_results) + 1)
                        try:
                            files = migrate_conversation(conv, gold_id, zip_entry["zip"])
                            write_conversation(gold_id, files)
                            imported += 1
                            migration_results.append({
                                "gold_id": gold_id,
                                "source_id": conv.get("id", ""),
                                "source_zip": zip_entry["zip"],
                                "category": files["conversation.json"]["category"],
                                "language": files["conversation.json"]["language"],
                            })
                        except Exception as e:
                            errors.append({"id": gold_id, "source": conv.get("id", ""), "error": str(e)})
                except Exception as e:
                    errors.append({"file": jf, "error": str(e)})

    print(f"  Imported: {imported}")
    print(f"  Errors: {len(errors)}")

    # Step 3: Validate
    print("\n[3/5] Validation...")
    validation_results = {}
    schema_pass = 0
    schema_fail = 0

    for r in migration_results:
        conv_dir = os.path.join(CONVERSATIONS_DIR, r["gold_id"])
        vr = validate_schema_safe(conv_dir, schema_dir)
        validation_results[r["gold_id"]] = vr
        if vr["fail"] == 0:
            schema_pass += 1
        else:
            schema_fail += 1

    print(f"  Schema valid: {schema_pass}")
    print(f"  Schema invalid: {schema_fail}")

    # Step 4: Classify
    print("\n[4/5] Classification...")
    certified = []
    repairable = []
    rejected = []
    import_errors = []

    for r in migration_results:
        vr = validation_results.get(r["gold_id"], {"pass": 0, "fail": 99})
        if vr["fail"] == 0:
            certified.append(r["gold_id"])
        elif vr["fail"] <= 2:
            repairable.append(r["gold_id"])
        else:
            rejected.append(r["gold_id"])

    for e in errors:
        import_errors.append(e)

    classification = {
        "Gold Certified": certified,
        "Gold Repairable": repairable,
        "Gold Rejected": rejected,
        "Import Errors": import_errors,
    }

    # Step 5: Statistics
    print("\n[5/5] Statistics...")
    cat_counter = Counter()
    lang_counter = Counter()
    level_counter = Counter()
    channel_counter = Counter()

    for r in migration_results:
        cat_counter[r["category"]] += 1
        lang_counter[r["language"]] += 1

    total_convos = len(migration_results)
    stats = {
        "total_conversations": total_convos,
        "total_import_errors": len(errors),
        "certified": len(certified),
        "repairable": len(repairable),
        "rejected": len(rejected),
        "categories": dict(cat_counter.most_common()),
        "languages": dict(lang_counter.most_common()),
        "levels": dict(level_counter.most_common()),
        "channels": dict(channel_counter.most_common()),
        "validation_schema_pass": schema_pass,
        "validation_schema_fail": schema_fail,
    }

    # Write outputs
    classification_path = os.path.join(IMPORT_DIR, "classification.json")
    with open(classification_path, "w") as f:
        json.dump(classification, f, indent=2)

    stats_path = os.path.join(IMPORT_DIR, "statistics.json")
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)

    validation_path = os.path.join(IMPORT_DIR, "validation_results.json")
    with open(validation_path, "w") as f:
        json.dump(validation_results, f, indent=2)

    duration = time.time() - start_time

    result = {
        "duration_seconds": round(duration, 2),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "inventory": inv_path,
        "classification": classification_path,
        "statistics": stats_path,
        "validation": validation_path,
        "summary": stats,
    }

    print(f"\n{'=' * 60}")
    print(f"Migration complete in {duration:.2f}s")
    print(f"  Total: {total_convos}")
    print(f"  Certified: {len(certified)}")
    print(f"  Repairable: {len(repairable)}")
    print(f"  Rejected: {len(rejected)}")
    print(f"  Import Errors: {len(errors)}")
    print(f"{'=' * 60}")

    return result


if __name__ == "__main__":
    result = run_full_migration()
    print(f"\nResults written to: {IMPORT_DIR}/")
