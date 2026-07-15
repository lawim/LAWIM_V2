#!/usr/bin/env python3
"""Mission 3B.1 — Corpus Audit Script

Audits the conversation test corpus for completeness, coverage, and quality.
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter, defaultdict
from typing import Any

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from corpus import CONVERSATIONS


def message_length(msg: str) -> int:
    return len(msg)


def classify_intent(text: str) -> str | None:
    t = text.lower()
    if re.search(r'\b(acheter|achat|buy|vendre|vente)\b', t):
        return "buy"
    if re.search(r'\b(louer|location|rent|locataire)\b', t):
        return "rent"
    if re.search(r'\b(construire|construction|construct|building)\b', t):
        return "construct"
    if re.search(r'\b(vendre|vente|sell)\b', t):
        return "sell"
    if re.search(r'\b(architecte|architect|professionnel|professional)\b', t):
        return "professional"
    return None


def detect_handover(text: str) -> bool:
    t = text.lower()
    return bool(re.search(r'\b(parler à un humain|agent humain|assistance|svp|aide moi|je bloque)\b', t))


def detect_greeting(text: str) -> bool:
    t = text.strip().lower()
    return t in ("bonjour", "salut", "bonsoir", "hello", "salut ça va", "bonjour ça va")


def is_short_reply(text: str) -> bool:
    t = text.strip().lower()
    short_words = {"ok", "oui", "non", "d'accord", "daccord", "merci", "go", "yes", "no", "si", "super", "parfait"}
    return t in short_words or t in ("ok", "oui", "non", "d'accord", "merci", "yes", "no")


def has_ambiguity(text: str) -> bool:
    t = text.lower().strip()
    if re.search(r'\bmil\b', t):
        return True
    if re.search(r'\b\d{3}\s*mil(le?s?)?\b', t):
        return True
    if re.match(r'^\d{3}$', t):
        return True
    if re.match(r'^\d+\s*(mille|mil)\s*(f|cf(a)?)?\s*$', t) and not re.search(r'millions?\b', t):
        return True
    return False


def detect_budget_mention(text: str) -> bool:
    t = text.lower()
    if re.search(r'\b\d+[\s,]?\d*\s*(millions?|mille|mil|f|cfa|fcfa|usd|eur|euros|dollars)\b', t):
        return True
    if re.search(r'\bbudget\b', t):
        return True
    if re.match(r'^\d[\d\s,]*$', t) and len(t) >= 3:
        return True
    return False


def detect_property_type(text: str) -> list[str]:
    types = []
    t = text.lower()
    mapping = {
        "maison": "HOUSE", "appartement": "APARTMENT", "appart": "APARTMENT",
        "studio": "STUDIO", "villa": "VILLA", "terrain": "LAND", "immeuble": "BUILDING",
        "bureau": "OFFICE", "local": "COMMERCIAL", "magasin": "COMMERCIAL",
    }
    for keyword, ptype in mapping.items():
        if re.search(r'\b' + re.escape(keyword) + r'\b', t):
            types.append(ptype)
    return types


def detect_channel(text: str) -> list[str]:
    channels = []
    t = text.lower()
    if "whatsapp" in t:
        channels.append("whatsapp")
    if "telegram" in t:
        channels.append("telegram")
    if "web" in t or "site" in t or "internet" in t:
        channels.append("web")
    return channels


def extract_cities(text: str) -> list[str]:
    cities = []
    t = text.lower()
    known_cities = [
        "douala", "yaoundé", "yaounde", "garoua", "bafoussam", "buea", "kribi",
        "limbe", "ebolowa", "dschang", "kumbo", "kousseri", "mbouda", "foumban",
        "muyuka", "nkongsamba", "maroua", "ngaoundéré", "ngaoundere", "bertoua",
        "mbandjoun", "mbanga", "sangmelima", "bali", "bamenda", "nkongsamba",
    ]
    for city in known_cities:
        if re.search(r'\b' + re.escape(city) + r'\b', t):
            cities.append(city.title() if city != "yaoundé" else "Yaoundé")
    return cities


def extract_neighborhoods(text: str) -> list[str]:
    hoods = []
    t = text.lower()
    known = [
        "mvog-mbi", "mfoundi", "bonapriso", "akwa", "bassa", "makepe",
        "bonanjo", "deido", "bonamoussadi", "odza", "bastos", "biyem-assi",
        "biyemassi", "roumde-adje", "roumde", "mvog ada", "mvog-ada",
        "quartier", "cite-verte", "cite verte", "mokolo", "essos",
        "nsam", "efoulan", "mendong", "titi garage",
    ]
    for hood in known:
        if re.search(r'\b' + re.escape(hood) + r'\b', t):
            hoods.append(hood.title())
    return list(set(hoods))


def user_message_sequence(conv: dict) -> tuple[str, ...]:
    return tuple(m["user"] for m in conv["messages"])


def get_expected_diagnostics(expected: dict) -> dict:
    diag = {"has_state_after": "state_after" in expected,
            "has_action": "action" in expected,
            "has_checks": "checks" in expected and len(expected.get("checks", [])) > 0,
            "check_count": len(expected.get("checks", [])),
            "check_types": [c[0] for c in expected.get("checks", [])]}
    return diag


def audit_corpus() -> dict[str, Any]:
    report: dict[str, Any] = {}

    # 1. Conversation count
    total_convs = len(CONVERSATIONS)
    report["conversation_count"] = total_convs
    report["claimed_conversation_count"] = 1910
    report["conversation_count_match"] = total_convs == 1910

    # 2. Message count
    total_msgs = sum(len(c["messages"]) for c in CONVERSATIONS)
    report["message_count"] = total_msgs
    report["claimed_message_count"] = 10037
    report["message_count_match"] = total_msgs == 10037

    # 3. Message length stats per conversation
    msg_lengths = [message_length(m["user"]) for c in CONVERSATIONS for m in c["messages"]]
    conv_msg_lengths = [
        [message_length(m["user"]) for m in c["messages"]]
        for c in CONVERSATIONS
    ]
    conv_avg_lengths = [sum(lens) / len(lens) if lens else 0 for lens in conv_msg_lengths]

    report["message_length"] = {
        "min": min(msg_lengths),
        "max": max(msg_lengths),
        "avg": round(sum(msg_lengths) / len(msg_lengths), 2),
        "per_conversation": {
            "min_avg": round(min(conv_avg_lengths), 2),
            "max_avg": round(max(conv_avg_lengths), 2),
            "overall_avg": round(sum(conv_avg_lengths) / len(conv_avg_lengths), 2),
        },
    }

    # 4. Distribution of conversation lengths
    conv_lengths = [len(c["messages"]) for c in CONVERSATIONS]
    length_counter = Counter(conv_lengths)
    buckets = {
        "1-2 msgs": sum(1 for l in conv_lengths if l <= 2),
        "3-4 msgs": sum(1 for l in conv_lengths if 3 <= l <= 4),
        "5-6 msgs": sum(1 for l in conv_lengths if 5 <= l <= 6),
        "7-8 msgs": sum(1 for l in conv_lengths if 7 <= l <= 8),
        "9+ msgs": sum(1 for l in conv_lengths if l >= 9),
    }
    report["conversation_length_distribution"] = {
        "histogram": dict(sorted(length_counter.items())),
        "buckets": buckets,
        "min_messages": min(conv_lengths),
        "max_messages": max(conv_lengths),
        "avg_messages": round(sum(conv_lengths) / len(conv_lengths), 2),
    }

    # 5. Category breakdown
    categories = Counter(c["category"] for c in CONVERSATIONS)
    report["category_breakdown"] = dict(categories.most_common())

    # 6. Intent detection
    intent_counter: Counter = Counter()
    for c in CONVERSATIONS:
        for m in c["messages"]:
            intent = classify_intent(m["user"])
            if intent:
                intent_counter[intent] += 1
    report["intent_keywords_detected"] = dict(intent_counter.most_common())

    # 7. City/neighborhood references
    city_counter: Counter = Counter()
    hood_counter: Counter = Counter()
    for c in CONVERSATIONS:
        cities_in_conv = set()
        hoods_in_conv = set()
        for m in c["messages"]:
            for city in extract_cities(m["user"]):
                cities_in_conv.add(city)
            for hood in extract_neighborhoods(m["user"]):
                hoods_in_conv.add(hood)
        for city in cities_in_conv:
            city_counter[city] += 1
        for hood in hoods_in_conv:
            hood_counter[hood] += 1
    report["city_references"] = dict(city_counter.most_common())
    report["neighborhood_references"] = dict(hood_counter.most_common())
    report["cities_covered"] = len(city_counter)

    # 8. Property type mentions
    pt_counter: Counter = Counter()
    for c in CONVERSATIONS:
        pts_in_conv = set()
        for m in c["messages"]:
            for pt in detect_property_type(m["user"]):
                pts_in_conv.add(pt)
        for pt in pts_in_conv:
            pt_counter[pt] += 1
    report["property_type_mentions"] = dict(pt_counter.most_common())

    # 9. Channel references
    ch_counter: Counter = Counter()
    for c in CONVERSATIONS:
        for m in c["messages"]:
            for ch in detect_channel(m["user"]):
                ch_counter[ch] += 1
    report["channel_references"] = dict(ch_counter.most_common())

    # 10. Duplicate detection
    seen_sequences: dict[tuple, list[str]] = defaultdict(list)
    for c in CONVERSATIONS:
        seq = user_message_sequence(c)
        seen_sequences[seq].append(c["id"])
    duplicates = {k: v for k, v in seen_sequences.items() if len(v) > 1}
    report["duplicate_conversations"] = {
        "count": len(duplicates),
        "total_duplicate_instances": sum(len(v) for v in duplicates.values()),
        "examples": [
            {"ids": v, "seq": list(k)}
            for k, v in list(duplicates.items())[:10]
        ],
    }

    # 11. Short reply detection
    short_reply_counter: Counter = Counter()
    total_short = 0
    for c in CONVERSATIONS:
        for m in c["messages"]:
            if is_short_reply(m["user"]):
                total_short += 1
                short_reply_counter[m["user"].strip().lower()] += 1
    report["short_replies"] = {
        "total": total_short,
        "percentage": round(total_short / total_msgs * 100, 2) if total_msgs else 0,
        "breakdown": dict(short_reply_counter.most_common()),
    }

    # 12. Ambiguity detection
    ambig_counter = 0
    ambig_examples = []
    for c in CONVERSATIONS:
        for m in c["messages"]:
            try:
                if has_ambiguity(str(m["user"])):
                    ambig_counter += 1
                    if len(ambig_examples) < 10:
                        ambig_examples.append({"scenario": c["id"], "message": str(m["user"])})
            except Exception:
                pass
    report["ambiguity_detection"] = {
        "total": ambig_counter,
        "percentage": round(ambig_counter / total_msgs * 100, 2) if total_msgs else 0,
        "examples": ambig_examples,
    }

    # 13. Budget mentions
    budget_counter = 0
    for c in CONVERSATIONS:
        for m in c["messages"]:
            if detect_budget_mention(m["user"]):
                budget_counter += 1
    report["budget_mentions"] = {
        "total": budget_counter,
        "percentage": round(budget_counter / total_msgs * 100, 2) if total_msgs else 0,
    }

    # 14. Handover request detection
    handover_counter = 0
    handover_examples = []
    for c in CONVERSATIONS:
        for m in c["messages"]:
            if detect_handover(m["user"]):
                handover_counter += 1
                if len(handover_examples) < 10:
                    handover_examples.append({"scenario": c["id"], "message": m["user"]})
    report["handover_requests"] = {
        "total": handover_counter,
        "examples": handover_examples,
    }

    # 15. Greeting detection
    greeting_counter = 0
    greeting_examples = []
    for c in CONVERSATIONS:
        for m in c["messages"]:
            if detect_greeting(m["user"]):
                greeting_counter += 1
                if len(greeting_examples) < 10:
                    greeting_examples.append({"scenario": c["id"], "message": m["user"]})
    report["greetings"] = {
        "total": greeting_counter,
        "percentage": round(greeting_counter / total_msgs * 100, 2) if total_msgs else 0,
        "examples": greeting_examples,
    }

    # --- Bonus: Assertion quality in expected dict ---
    total_expected_checks = 0
    state_checks = 0
    action_checks = 0
    fact_checks = 0
    behavioral_checks = 0
    missing_expected = 0
    for c in CONVERSATIONS:
        for m in c["messages"]:
            exp = m.get("expected", {})
            if not exp:
                missing_expected += 1
                continue
            if "state_after" in exp:
                state_checks += 1
            if "action" in exp:
                action_checks += 1
            for check in exp.get("checks", []):
                total_expected_checks += 1
                if check[0] in ("no_loop", "not_ask_city", "no_external_recommendation"):
                    behavioral_checks += 1
                else:
                    fact_checks += 1

    report["expected_assertions"] = {
        "messages_with_state_after": state_checks,
        "messages_with_action": action_checks,
        "total_fact_checks": fact_checks,
        "total_behavioral_checks": behavioral_checks,
        "total_checks_all": total_expected_checks,
        "messages_missing_expected": missing_expected,
    }

    # --- State coverage ---
    states_used: Counter = Counter()
    for c in CONVERSATIONS:
        for m in c["messages"]:
            s = m.get("expected", {}).get("state_after")
            if s:
                states_used[s] += 1
    report["state_coverage"] = dict(states_used.most_common())

    # --- Action coverage ---
    actions_used: Counter = Counter()
    for c in CONVERSATIONS:
        for m in c["messages"]:
            a = m.get("expected", {}).get("action")
            if a:
                actions_used[a] += 1
    report["action_coverage"] = dict(actions_used.most_common())

    return report


def main():
    report = audit_corpus()

    # Print to stdout
    print("=" * 70)
    print("  MISSION 3B.1 — CORPUS AUDIT REPORT")
    print("=" * 70)

    print(f"\n1. CONVERSATION COUNT: {report['conversation_count']} (claimed: {report['claimed_conversation_count']})")
    print(f"   Match: {report['conversation_count_match']}")

    print(f"\n2. MESSAGE COUNT: {report['message_count']} (claimed: {report['claimed_message_count']})")
    print(f"   Match: {report['message_count_match']}")

    print(f"\n3. MESSAGE LENGTHS:")
    ml = report["message_length"]
    print(f"   Min: {ml['min']}, Max: {ml['max']}, Avg: {ml['avg']}")
    print(f"   Per-conversation avg: min={ml['per_conversation']['min_avg']}, "
          f"max={ml['per_conversation']['max_avg']}, "
          f"overall={ml['per_conversation']['overall_avg']}")

    print(f"\n4. CONVERSATION LENGTH DISTRIBUTION:")
    cd = report["conversation_length_distribution"]
    print(f"   Min: {cd['min_messages']}, Max: {cd['max_messages']}, Avg: {cd['avg_messages']}")
    print(f"   Buckets: {cd['buckets']}")

    print(f"\n5. CATEGORY BREAKDOWN:")
    for cat, cnt in report["category_breakdown"].items():
        print(f"   {cat}: {cnt}")

    print(f"\n6. INTENT KEYWORDS DETECTED:")
    for intent, cnt in report["intent_keywords_detected"].items():
        print(f"   {intent}: {cnt}")

    print(f"\n7. CITY & NEIGHBORHOOD REFERENCES:")
    print(f"   Cities covered: {report['cities_covered']}")
    for city, cnt in list(report["city_references"].items())[:15]:
        print(f"   City {city}: {cnt}")
    print(f"   Total neighborhoods found: {sum(report['neighborhood_references'].values())}")

    print(f"\n8. PROPERTY TYPE MENTIONS:")
    for pt, cnt in report["property_type_mentions"].items():
        print(f"   {pt}: {cnt}")

    print(f"\n9. CHANNEL REFERENCES:")
    for ch, cnt in report["channel_references"].items():
        print(f"   {ch}: {cnt}")

    print(f"\n10. DUPLICATE DETECTION:")
    print(f"    Duplicate groups: {report['duplicate_conversations']['count']}")
    print(f"    Total duplicate instances: {report['duplicate_conversations']['total_duplicate_instances']}")

    print(f"\n11. SHORT REPLIES:")
    print(f"    Total: {report['short_replies']['total']} ({report['short_replies']['percentage']}%)")
    print(f"    Top: {dict(list(report['short_replies']['breakdown'].items())[:10])}")

    print(f"\n12. AMBIGUITY DETECTION:")
    print(f"    Total ambiguous messages: {report['ambiguity_detection']['total']} ({report['ambiguity_detection']['percentage']}%)")

    print(f"\n13. BUDGET MENTIONS:")
    print(f"    Total: {report['budget_mentions']['total']} ({report['budget_mentions']['percentage']}%)")

    print(f"\n14. HANDOVER REQUESTS:")
    print(f"    Total: {report['handover_requests']['total']}")

    print(f"\n15. GREETINGS:")
    print(f"    Total: {report['greetings']['total']} ({report['greetings']['percentage']}%)")

    print(f"\n--- EXPECTED ASSERTIONS QUALITY ---")
    for k, v in report["expected_assertions"].items():
        print(f"   {k}: {v}")

    print(f"\n--- STATE COVERAGE ---")
    for s, cnt in report["state_coverage"].items():
        print(f"   {s}: {cnt}")

    print(f"\n--- ACTION COVERAGE ---")
    for a, cnt in report["action_coverage"].items():
        print(f"   {a}: {cnt}")

    # Save JSON
    out_path = "/tmp/mission-3b1-corpus-audit.json"
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\nJSON report saved to {out_path}")


if __name__ == "__main__":
    main()
