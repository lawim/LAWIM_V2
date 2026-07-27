#!/usr/bin/env python3
"""LCIP B.4 — Reconstruct Gold specifications from source dialogues + business rules.

Sources:
  - ZIP archives (blocks 1-2): original dialogue content
  - Derivation rules: expected_derivation_rules.json
  - LAWIM state machine, language policy, qualification rules

Output: tests/gold_corpus/specifications/b4/<ID>/
"""

import hashlib
import json
import os
import re
import sys
import zipfile
from collections import Counter
from datetime import datetime, timezone

_base = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..", "..", ".."))
ZIP_DIR = "/media/abel/1A4696CE4696AA51/Telechargement/LAWIM_GOLD_CORPUS_BLOCK"
SKIP_ZIPS = {"LAWIM_GOLD_CORPUS_BLOCK_02_DETAILED (1).zip"}
OUT_DIR = os.path.join(_base, "tests", "gold_corpus", "specifications", "b4")
RULES_PATH = os.path.join(_base, "tests", "gold_corpus", "specification", "rules", "expected_derivation_rules.json")

INTENT_PATTERNS = {
    "property_search": ["cherche", "recherche", "rechercher", "find", "looking for", "want", "search"],
    "visit_scheduling": ["visite", "visit", "voir", "see"],
    "correction": ["non", "finalement", "change", "corrige", "actually", "instead", "plutôt"],
    "confirmation": ["oui", "yes", "confirme", "ok", "d'accord", "confirm"],
    "refusal": ["non merci", "pas maintenant", "no thanks", "not now", "arrête", "stop"],
    "create_case": ["crée", "créer", "create", "nouveau", "new", "dossier"],
}

PHASE_SEQUENCE = ["initial", "qualifying", "qualified", "completed"]
PENDING_BY_INTENT = {
    "property_search": ["ASK_BUDGET", "ASK_BEDROOMS", "ASK_AREAS", "ASK_CITY", "ASK_PROPERTY_TYPE", "ASK_TRANSACTION", "CONFIRM_QUALIFICATION"],
    "visit_scheduling": ["ASK_DATE", "ASK_TIME", "ASK_PROPERTY", "CONFIRM_CREATION"],
    "create_case": ["CONFIRM_CREATION"],
}

QUESTION_TYPE_MAP = {
    "ASK_BUDGET": ["budget", "prix", "price", "combien", "how much"],
    "ASK_BEDROOMS": ["chambre", "bedroom", "pièce", "pièces"],
    "ASK_AREAS": ["quartier", "area", "zone", "préfère", "prefer", "endroit", "place"],
    "ASK_CITY": ["ville", "city", "où", "where"],
    "ASK_PROPERTY_TYPE": ["type de bien", "quel bien", "property type", "maison", "appartement"],
    "ASK_TRANSACTION": ["achat", "location", "rent", "buy", "louer", "acheter"],
    "CONFIRM_QUALIFICATION": ["confirmer", "correct", "confirmez", "bien récapitulé", "récapitul"],
    "CONFIRM_CREATION": ["créer", "lancer", "confirmer la création", "create", "confirm"],
}


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def detect_intent(text: str) -> str:
    """Detect intent from user message text."""
    tl = text.lower()
    for intent, patterns in INTENT_PATTERNS.items():
        for p in patterns:
            if p in tl:
                return intent
    return "property_search"


def determine_pending(assistant_text: str) -> str:
    """Determine pending_user_action from assistant question."""
    for pending, patterns in QUESTION_TYPE_MAP.items():
        for p in patterns:
            if p in assistant_text.lower():
                return pending
    if assistant_text.endswith("?"):
        return "ASK_BUDGET"
    return "NONE"


def determine_phase(turn_idx: int, all_facts: dict, pending: str,
                    business_action: str, confirmed: bool) -> str:
    """Determine conversation phase based on state."""
    if business_action and business_action != "none":
        return "completed"
    if confirmed:
        return "completed"
    if len(all_facts) >= 4:
        return "qualified"
    if len(all_facts) > 0:
        return "qualifying"
    return "initial"


def extract_numeric(text: str) -> int:
    """Extract numbers from text, handling common formats."""
    text = text.replace(" ", "").replace(",", "").replace(".", "")
    nums = re.findall(r'(\d+)', text)
    return int(nums[0]) if nums else 0


def extract_facts(user_text: str, existing_facts: dict) -> dict:
    """Extract facts from user message, merging with existing facts."""
    facts = dict(existing_facts)
    tl = user_text.lower()

    # Transaction type
    if any(w in tl for w in ["louer", "location", "rent"]):
        facts["transaction_type"] = "rent"
    elif any(w in tl for w in ["acheter", "achat", "buy", "purchase", "acquerir"]):
        facts["transaction_type"] = "buy"

    # Property type
    if any(w in tl for w in ["appartement", "appt", "apartment"]):
        facts["property_type"] = "apartment"
    elif any(w in tl for w in ["maison", "house", "villa"]):
        facts["property_type"] = "house"
    elif any(w in tl for w in ["studio"]):
        facts["property_type"] = "studio"
    elif any(w in tl for w in ["terrain", "land"]):
        facts["property_type"] = "land"

    # City
    cities = ["douala", "yaoundé", "yaounde", "bafoussam", "garoua", "bamenda"]
    for c in cities:
        if c in tl:
            facts["city"] = c.capitalize()
            break

    # Budget
    nums = extract_numeric(user_text)
    if nums and any(w in tl for w in ["budget", "f cfa", "fcfa", "f CFA", "franc", "million", "prix", "price"]):
        facts["budget"] = nums

    # Bedrooms
    if "chambre" in tl or "bedroom" in tl or "pièce" in tl or "pieces" in tl:
        nums = extract_numeric(user_text)
        if nums:
            facts["bedrooms"] = nums
        elif "deux" in tl or "2" in tl:
            facts["bedrooms"] = 2
        elif "trois" in tl or "3" in tl:
            facts["bedrooms"] = 3

    # Preferred areas
    areas_keywords = ["à ", "quartier", "area", "zone", "préfère", "prefer"]
    if any(k in tl for k in areas_keywords) and not any(m in tl for m in ["combien", "budget", "prix"]):
        # Extract area name
        for prefix in ["à ", "au quartier ", "le quartier ", "préfère ", "prefer ", "zone "]:
            if prefix in tl:
                area = tl.split(prefix)[-1].split()[0].strip("?.!,").capitalize()
                if area and len(area) > 2:
                    existing = facts.get("preferred_areas", [])
                    if isinstance(existing, list) and area not in existing:
                        existing.append(area)
                        facts["preferred_areas"] = existing
                    break

    # Correction handling (non replaces old data)
    if "non" in tl or "finalement" in tl or "actually" in tl:
        # Check what's being corrected
        nums = extract_numeric(user_text)
        if nums and "budget" not in facts:
            pass
        if "budget" in tl or "f cfa" in tl or "fcfa" in tl or "prix" in tl:
            facts["budget"] = nums
        areas_keywords = ["à ", "quartier", "area"]
        if any(a in tl for a in areas_keywords) and nums == 0:
            for prefix in ["à ", "au quartier ", "le quartier "]:
                if prefix in tl:
                    area = tl.split(prefix)[-1].split()[0].strip("?.!,").capitalize()
                    if area and len(area) > 2:
                        facts["preferred_areas"] = [area]
                        break

    return facts


def reconstruct_conversation(source_conv: dict, source_zip: str) -> dict:
    """Rebuild a complete Gold specification from source data."""
    conv_id = f"B{source_conv.get('_index', 0):06d}"
    category_raw = source_conv.get("category", "rental_search")
    language = source_conv.get("language", "fr")
    channel = source_conv.get("channel", "web")
    difficulty = source_conv.get("difficulty", "standard")
    turns = source_conv.get("turns", [])

    # Build messages from source
    messages = []
    for t in turns:
        messages.append({"role": t.get("role", "user"), "text": t.get("text", "")})

    # Determine facts progressively
    facts = {}
    last_pending = "NONE"
    last_intent = "property_search"
    business_action = "none"
    confirmed = False
    last_assistant_question = ""

    # Track expected state per turn (use last assistant turn as reference)
    for i, t in enumerate(turns):
        role = t.get("role", "user")
        text = t.get("text", "")

        if role == "user":
            intent = detect_intent(text)
            if intent == "refusal":
                business_action = "none"
                confirmed = False
            elif intent == "confirmation":
                confirmed = True
                if last_pending in ["CONFIRM_QUALIFICATION", "CONFIRM_CREATION"]:
                    business_action = "create_search_request"
            last_intent = intent
            # Extract facts, handling corrections
            if "non" in text.lower() or "finalement" in text.lower():
                # Correction mode — targeted fact replacement
                facts = extract_facts(text, {})
                # Preserve non-targeted facts from previous state
                # (simplified — we rebuild from scratch per turn)
            else:
                facts = extract_facts(text, facts)

        elif role == "assistant":
            if text.endswith("?"):
                last_pending = determine_pending(text)
                last_assistant_question = text
            else:
                last_pending = "NONE"

    # Build final expected state
    phase = determine_phase(len(turns) // 2, facts, last_pending, business_action, confirmed)
    intent = last_intent

    conversation = {
        "id": conv_id,
        "category": "rental",
        "level": "basic" if difficulty in ("standard", "simple") else difficulty,
        "channel": channel,
        "language": language,
        "description": source_conv.get("title", f"Conversation {conv_id}"),
        "tags": source_conv.get("tags", []),
        "business_object": facts.get("property_type", "unknown"),
        "source_zip": source_zip,
        "source_id": source_conv.get("id", ""),
        "messages": messages,
    }

    expected_state = {
        "intent": intent,
        "qualification_status": "qualified" if phase in ("qualified", "completed") else "in_progress",
        "slots_filled": {k: v for k, v in facts.items() if v is not None},
        "next_action": last_pending if last_pending != "NONE" else (business_action if business_action != "none" else "NONE"),
        "memory_retained": list(facts.keys()),
    }

    expected_business = {
        "business_action": business_action,
        "target_service": "PropertySearchService" if business_action != "none" else "None",
        "parameters": facts,
        "expected_result": "Recherche de biens" if business_action != "none" else "Aucune action",
        "handover_required": False,
    }

    expected_questions = {"maximum_questions_per_turn": 1, "required_questions": [], "forbidden_questions": []}
    for i, t in enumerate(turns):
        if t.get("role") == "assistant" and t.get("text", "").endswith("?"):
            expected_questions["required_questions"].append({
                "turn": i // 2, "expected_question": t["text"],
                "context": f"Turn {i // 2}",
            })

    expected_language = {
        "primary_language": language,
        "responses_language": language,
        "allow_code_switch": False,
        "forbidden_phrases": ["assistant neutre", "I cannot make business decisions"],
        "footer_required": True,
        "identity": "LAWIM AI",
    }

    expected_runtime = {
        "engine": "ConversationJourneyOrchestrator",
        "expected_services": ["ConversationStateService", "QualificationService"],
        "expected_repositories": ["ConversationStateRepository"],
        "timeout_seconds": 30, "retry_allowed": True,
        "fallback_chain": ["deepseek", "openai", "gemini"],
    }

    assertions = []
    if facts:
        assertions.append({
            "id": "ASSERT-B4-001", "type": "memory",
            "description": "Faits extraits conservés en mémoire",
            "expected": list(facts.keys()),
            "path": "memory_retained", "operator": "contains",
        })
    if business_action != "none":
        assertions.append({
            "id": "ASSERT-B4-002", "type": "business",
            "description": "Action métier correcte",
            "expected": business_action,
            "path": "business_action", "operator": "eq",
        })
    assertions.append({
        "id": "ASSERT-B4-003", "type": "language",
        "description": "Langue correcte",
        "expected": language, "path": "responses_language", "operator": "eq",
    })

    return {
        "conversation.json": conversation,
        "expected_state.json": expected_state,
        "expected_business.json": expected_business,
        "expected_questions.json": expected_questions,
        "expected_language.json": expected_language,
        "expected_runtime.json": expected_runtime,
        "expected_assertions.json": {"assertions": assertions},
    }


def load_source_conversations():
    """Load all conversations from blocks 1 & 2 ZIPs."""
    seen_hashes = {}
    all_convos = []
    for fname in sorted(os.listdir(ZIP_DIR)):
        if not fname.endswith(".zip") or fname in SKIP_ZIPS:
            continue
        fpath = os.path.join(ZIP_DIR, fname)
        zh = sha256_file(fpath)
        if zh in seen_hashes:
            continue
        seen_hashes[zh] = fname
        block_num = 1 if "BLOCK_01" in fname else 2
        with zipfile.ZipFile(fpath) as zf:
            for name in zf.namelist():
                if name.endswith(".json") and "manifest" not in name and not name.startswith("README"):
                    data = json.loads(zf.read(name))
                    convs = data if isinstance(data, list) else [data]
                    for idx, c in enumerate(convs):
                        c["_index"] = len(all_convos) + 1
                        c["_block"] = block_num
                        c["_archive"] = fname
                        all_convos.append(c)
    return all_convos


def main():
    print("B.4 Gold Specification Reconstruction")
    print("=" * 50)

    # Load source conversations (blocks 1-2)
    print("\nLoading source conversations from ZIPs...")
    source_convos = load_source_conversations()
    print(f"  Loaded: {len(source_convos)} conversations")

    os.makedirs(OUT_DIR, exist_ok=True)

    stats = {"total": 0, "errors": 0, "outputs": []}

    for conv in source_convos:
        try:
            files = reconstruct_conversation(conv, conv.get("_archive", ""))
            cid = files["conversation.json"]["id"]
            conv_dir = os.path.join(OUT_DIR, cid)
            os.makedirs(conv_dir, exist_ok=True)
            for fname, data in files.items():
                with open(os.path.join(conv_dir, fname), "w") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            stats["total"] += 1
            stats["outputs"].append(cid)
        except Exception as e:
            stats["errors"] += 1
            print(f"  ERROR: {e}")

    print(f"\nReconstruction complete:")
    print(f"  Created: {stats['total']} specifications")
    print(f"  Errors: {stats['errors']}")
    print(f"  Output: {OUT_DIR}/")

    return stats


if __name__ == "__main__":
    result = main()
