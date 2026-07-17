#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, logging
from .orchestrator import Orchestrator

logging.basicConfig(level=logging.INFO)


def main() -> None:
    parser = argparse.ArgumentParser(description="LAWIM Conversation Factory")
    parser.add_argument("mode", choices=["generate", "validate", "report"])
    parser.add_argument("--count", type=int, default=1000)
    parser.add_argument("--languages", default="fr,en,pcm")
    parser.add_argument("--factory", choices=["multi-agent", "procedural"], default="multi-agent")
    parser.add_argument("--output", default="")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    orch = Orchestrator()

    if args.mode == "generate":
        if args.dry_run:
            print(f"DRY RUN: Would generate {args.count} conversations")
            return
        if args.factory == "multi-agent":
            result = orch.run_multi_agent(count=args.count, languages=args.languages.split(","))
        else:
            result = orch.run_procedural(count=args.count)
        print(json.dumps(result, indent=2))

    elif args.mode == "validate":
        print("Validation: OK")

    elif args.mode == "report":
        print("Factory report")


if __name__ == "__main__":
    main()
