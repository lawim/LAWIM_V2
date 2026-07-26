#!/usr/bin/env python3
"""Build statistics from the Gold Corpus."""

import json
import os
import sys
from collections import Counter, defaultdict


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_conversation(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def build_statistics(conversations_dir: str = None) -> dict:
    if conversations_dir is None:
        conversations_dir = os.path.join(BASE_DIR, "conversations")

    stats = {
        "total_conversations": 0,
        "categories": Counter(),
        "languages": Counter(),
        "levels": Counter(),
        "channels": Counter(),
        "business_objects": Counter(),
        "total_messages": 0,
        "total_user_messages": 0,
        "total_assistant_messages": 0,
        "avg_messages_per_conversation": 0.0,
        "avg_turns_per_conversation": 0.0,
        "coverage": {},
    }

    if not os.path.isdir(conversations_dir):
        print("WARNING: No conversations directory found")
        return stats

    entries = sorted(os.listdir(conversations_dir))
    turns_list = []

    for entry in entries:
        conv_dir = os.path.join(conversations_dir, entry)
        conv_file = os.path.join(conv_dir, "conversation.json")
        if not os.path.isdir(conv_dir) or not os.path.isfile(conv_file):
            continue

        conv = load_conversation(conv_file)
        stats["total_conversations"] += 1
        stats["categories"][conv.get("category", "unknown")] += 1
        stats["languages"][conv.get("language", "unknown")] += 1
        stats["levels"][conv.get("level", "unknown")] += 1
        stats["channels"][conv.get("channel", "unknown")] += 1
        stats["business_objects"][conv.get("business_object", "unknown")] += 1

        messages = conv.get("messages", [])
        stats["total_messages"] += len(messages)
        for m in messages:
            if m.get("role") == "user":
                stats["total_user_messages"] += 1
            elif m.get("role") == "assistant":
                stats["total_assistant_messages"] += 1

        turns = sum(1 for m in messages if m.get("role") == "user")
        turns_list.append(turns)

    if stats["total_conversations"] > 0:
        stats["avg_messages_per_conversation"] = round(
            stats["total_messages"] / stats["total_conversations"], 2
        )
        stats["avg_turns_per_conversation"] = round(
            sum(turns_list) / stats["total_conversations"], 2
        )
        stats["coverage"] = {
            "categories": len(stats["categories"]),
            "languages": len(stats["languages"]),
            "levels": len(stats["levels"]),
            "channels": len(stats["channels"]),
            "business_objects": len(stats["business_objects"]),
        }

    return stats


def format_stats(stats: dict) -> str:
    lines = []
    lines.append("# Gold Corpus Statistics")
    lines.append("")
    lines.append(f"**Total conversations:** {stats['total_conversations']}")
    lines.append(f"**Total messages:** {stats['total_messages']}")
    lines.append(f"**User messages:** {stats['total_user_messages']}")
    lines.append(f"**Assistant messages:** {stats['total_assistant_messages']}")
    lines.append(f"**Avg messages/conversation:** {stats['avg_messages_per_conversation']}")
    lines.append(f"**Avg turns/conversation:** {stats['avg_turns_per_conversation']}")
    lines.append("")
    lines.append("## By Category")
    lines.append("")
    lines.append("| Category | Count |")
    lines.append("| -------- | ----- |")
    for cat, count in sorted(stats["categories"].items()):
        lines.append(f"| {cat} | {count} |")
    lines.append("")
    lines.append("## By Language")
    lines.append("")
    lines.append("| Language | Count |")
    lines.append("| -------- | ----- |")
    for lang, count in sorted(stats["languages"].items()):
        lines.append(f"| {lang} | {count} |")
    lines.append("")
    lines.append("## By Level")
    lines.append("")
    lines.append("| Level | Count |")
    lines.append("| ----- | ----- |")
    for level, count in sorted(stats["levels"].items()):
        lines.append(f"| {level} | {count} |")
    lines.append("")
    lines.append("## By Channel")
    lines.append("")
    lines.append("| Channel | Count |")
    lines.append("| ------- | ----- |")
    for ch, count in sorted(stats["channels"].items()):
        lines.append(f"| {ch} | {count} |")
    lines.append("")
    lines.append("## By Business Object")
    lines.append("")
    lines.append("| Object | Count |")
    lines.append("| ------ | ----- |")
    for obj, count in sorted(stats["business_objects"].items()):
        lines.append(f"| {obj} | {count} |")
    lines.append("")
    lines.append("## Coverage")
    lines.append("")
    lines.append("| Dimension | Unique Values |")
    lines.append("| --------- | ------------- |")
    for dim, count in sorted(stats["coverage"].items()):
        lines.append(f"| {dim} | {count} |")

    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Build statistics from Gold Corpus")
    parser.add_argument("--conversations-dir", default=None,
                        help="Path to conversations directory")
    parser.add_argument("-o", "--output", default=None,
                        help="Output file path for statistics (JSON)")
    args = parser.parse_args()

    stats = build_statistics(args.conversations_dir)

    print(format_stats(stats))

    if args.output:
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, "w") as f:
            json.dump(stats, f, indent=2)
        print(f"\nStatistics written to: {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
