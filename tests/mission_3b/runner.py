from __future__ import annotations

import json
import sqlite3
import sys
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from lawim_v2.conversation import (
    Conversation,
    ConversationDecision,
    ConversationState,
    NormalizedMessage,
    ActionType,
)
from lawim_v2.conversation.planning import Planner
from lawim_v2.conversation.domain.facts import FactStatus
from lawim_v2.conversation.understanding.extractor import extract_all
from lawim_v2.conversation.understanding.short_replies import classify_short_reply
from lawim_v2.conversation.generation.composer import GenerativeComposer
from lawim_v2.conversation.generation.validator import ContentValidator

from tests.mission_3b.corpus import CONVERSATIONS


class SimpleDb:
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self):
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS test_users (
                id INTEGER PRIMARY KEY, username TEXT, email TEXT, role TEXT DEFAULT 'user',
                password_salt TEXT DEFAULT '', password_hash TEXT DEFAULT '',
                created_at TEXT
            );
            CREATE TABLE IF NOT EXISTS test_projects (
                id INTEGER PRIMARY KEY, user_id INTEGER, title TEXT, status TEXT DEFAULT 'ACTIVE',
                project_type TEXT DEFAULT '', objective TEXT DEFAULT '',
                created_at TEXT, updated_at TEXT
            );
            CREATE TABLE IF NOT EXISTS test_properties (
                id INTEGER PRIMARY KEY, title TEXT, city TEXT, property_type TEXT,
                price_max INTEGER, status TEXT DEFAULT 'available', created_at TEXT
            );
        """)
        self.conn.commit()

    def execute(self, sql: str, params: list | None = None):
        return self.conn.execute(sql, params or [])

    def fetch_one(self, sql: str, params: list | None = None):
        return self.conn.execute(sql, params or []).fetchone()

    def fetch_all(self, sql: str, params: list | None = None):
        return self.conn.execute(sql, params or []).fetchall()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()


class MemoryRepoStub:
    def __init__(self, db):
        self.db = db
        self.facts = []

    def save_fact(self, fact):
        fact.fact_id = str(uuid.uuid4())[:8]
        fact.created_at = datetime.now(timezone.utc).isoformat()
        fact.updated_at = fact.created_at
        self.facts.append(fact)
        return fact

    def supersede_fact(self, fact_id, timestamp):
        for f in self.facts:
            if f.fact_id == fact_id:
                f.confirmation_status = FactStatus.SUPERSEDED
                f.valid_to = timestamp
                break

    def update_fact_status(self, fact_id, status):
        for f in self.facts:
            if f.fact_id == fact_id:
                f.confirmation_status = status
                break

    def get_active_facts(self, project_id=None, dossier_id=None, conversation_id=None):
        return [f for f in self.facts if f.valid_to is None]

    def get_latest_confirmed_fact(self, field, project_id=None):
        active = [f for f in self.facts if f.field == field and f.valid_to is None and f.is_confirmed()]
        if active:
            return max(active, key=lambda f: f.created_at or "")
        return None

    def get_facts_by_status(self, status, project_id=None):
        return [f for f in self.facts if f.confirmation_status == status and f.valid_to is None]


class ConversationEngine:
    def __init__(self, db: SimpleDb):
        self.db = db
        self.memory_repo = MemoryRepoStub(db)
        self.composer = GenerativeComposer()

    def process_message(
        self,
        text: str,
        conversation: Conversation,
        channel: str = "web",
        user_id: int = 1,
    ) -> tuple[ConversationDecision, str]:
        message = NormalizedMessage(
            raw_text=text,
            normalized_text=text.strip(),
            channel=channel,
            user_id=user_id,
        )
        extracted = extract_all(text)
        facts = extracted.get("facts", [])
        ambiguous = extracted.get("ambiguous", [])

        for fact_data in facts:
            f = self.memory_repo.save_fact(
                type("Fact", (), {
                    "field": fact_data["field"],
                    "raw_value": str(fact_data.get("raw_value", "")),
                    "normalized_value": fact_data.get("normalized_value"),
                    "source_type": fact_data.get("source_type", "explicit"),
                    "confidence": fact_data.get("confidence", 1.0),
                    "is_confirmed": lambda self=self: True,
                    "is_active": lambda self=self: True,
                    "confirmation_status": FactStatus.CONFIRMED,
                    "fact_id": "",
                    "valid_to": None,
                    "created_at": "",
                    "project_id": conversation.project_id,
                    "supersedes_fact_id": None,
                    "to_dict": lambda self=self: {},
                })()
            )
            conversation.facts.add_fact(f)
            conversation.mark_field_known(fact_data["field"])
            if fact_data.get("source_type") == "inferred":
                conversation.facts.get_latest_confirmed(fact_data["field"])
            if fact_data["field"] == "city":
                pass

        short_reply = classify_short_reply(text)
        handover_request = message.is_handover_request()
        greeting = message.is_greeting()

        if handover_request:
            conversation.apply_transition("handover_requested")
            decision = ConversationDecision(
                conversation_id=conversation.conversation_id,
                user_id=user_id,
                channel=channel,
                raw_message=text,
                normalized_message=text.strip(),
                state_before=conversation.state,
                state_after=conversation.state,
                action=ActionType.HANDOVER_TO_HUMAN.value,
                requires_human=True,
            )
            response_text = "Je transfère votre demande à un conseiller LAWIM."
            return decision, response_text

        planner = Planner()
        plan = planner.plan(
            message=message,
            conversation=conversation,
            active_projects=[],
            intent_candidates=[],
        )
        decision = plan

        if decision.action in (ActionType.GREETING.value, None, ""):
            if conversation.state == ConversationState.NEW:
                conversation.apply_transition("message_received")
            decision.state_after = conversation.state
            decision.action = ActionType.GREETING.value
            response_text = f"Bonjour ! Je suis LAWIM, votre assistant immobilier. Comment puis-je vous aider ?"
            return decision, response_text

        if decision.requires_human:
            response_text = "Je transfère votre demande à un conseiller LAWIM."
            return decision, response_text

        if decision.requires_clarification:
            response_text = "Pourriez-vous reformuler votre réponse ?"
            return decision, response_text

        if decision.action == ActionType.UPDATE_FACT.value or not decision.action:
            if conversation.state == ConversationState.AWAITING_INTENT:
                conversation.apply_transition("intent_identified")
                decision.state_after = conversation.state
                response_text = "Merci ! Dans quelle ville recherchez-vous ?"
                return decision, response_text

        if facts or ambiguous:
            confirmed_fields = conversation.facts.all_confirmed_fields()
            has_city = "city" in confirmed_fields
            has_budget = any("budget" in f for f in confirmed_fields)
            has_property = "property_type" in confirmed_fields
            has_transaction = "transaction_type" in confirmed_fields

            if has_city and has_budget and has_property:
                conversation.apply_transition("minimum_readiness")
                decision.state_after = conversation.state
                response_text = "Parfait ! Je lance la recherche dans les bases LAWIM."
                return decision, response_text

            if has_city and has_property:
                if not has_budget:
                    response_text = "Quel est votre budget ?"
                    return decision, response_text
                if not has_transaction:
                    response_text = "Souhaitez-vous acheter ou louer ?"
                    return decision, response_text

            if not has_city:
                response_text = "Dans quelle ville recherchez-vous ?"
                return decision, response_text

        response_text = self.composer.compose(decision)
        return decision, response_text


def run_all_conversations() -> dict:
    db = SimpleDb(":memory:")
    engine = ConversationEngine(db)
    results = []

    for scenario in CONVERSATIONS:
        conv = Conversation(
            conversation_id=hash(scenario["id"]) & 0xFFFFFF,
            user_id=1,
            channel="web",
        )
        scenario_result = {
            "id": scenario["id"],
            "title": scenario["title"],
            "category": scenario.get("category", "unknown"),
            "steps": [],
            "passed": True,
            "errors": [],
            "duration_ms": 0,
        }
        start = time.time()

        for msg in scenario["messages"]:
            user_text = msg["user"]
            try:
                decision, response = engine.process_message(user_text, conv)
                conv.state = decision.state_after or conv.state
                step = {
                    "user": user_text,
                    "state_after": decision.state_after.value if decision.state_after else None,
                    "action": decision.action,
                    "response": response[:100],
                    "requires_clarification": decision.requires_clarification,
                    "requires_human": decision.requires_human,
                    "loop_detected": decision.loop_detected,
                    "error": None,
                }
                scenario_result["steps"].append(step)
            except Exception as e:
                scenario_result["steps"].append({
                    "user": user_text,
                    "error": str(e),
                })
                scenario_result["errors"].append(str(e))
                scenario_result["passed"] = False

        scenario_result["duration_ms"] = int((time.time() - start) * 1000)
        results.append(scenario_result)

    db.close()
    return results


def analyze_results(results: list[dict]) -> dict:
    total = len(results)
    passed = sum(1 for r in results if r["passed"])
    total_errors = sum(len(r["errors"]) for r in results)
    total_steps = sum(len(r["steps"]) for r in results)

    loops = 0
    handovers = 0
    clarifications = 0
    state_counts = {}
    action_counts = {}

    for r in results:
        for s in r["steps"]:
            state = s.get("state_after")
            if state:
                state_counts[state] = state_counts.get(state, 0) + 1
            action = s.get("action")
            if action:
                action_counts[action] = action_counts.get(action, 0) + 1
            if s.get("loop_detected"):
                loops += 1
            if s.get("requires_human"):
                handovers += 1
            if s.get("requires_clarification"):
                clarifications += 1

    return {
        "total_conversations": total,
        "total_messages": total_steps,
        "passed_conversations": passed,
        "failed_conversations": total - passed,
        "total_errors": total_errors,
        "loops_detected": loops,
        "handovers": handovers,
        "clarifications": clarifications,
        "state_distribution": dict(sorted(state_counts.items(), key=lambda x: -x[1])),
        "action_distribution": dict(sorted(action_counts.items(), key=lambda x: -x[1])),
        "pass_rate": f"{passed/total*100:.1f}%" if total else "0%",
    }


if __name__ == "__main__":
    print("Running all 500 conversations...")
    start = time.time()
    results = run_all_conversations()
    elapsed = time.time() - start
    analysis = analyze_results(results)

    print(f"\nCompleted in {elapsed:.1f}s")
    print(f"Conversations: {analysis['total_conversations']}")
    print(f"Messages: {analysis['total_messages']}")
    print(f"Passed: {analysis['passed_conversations']}/{analysis['total_conversations']} ({analysis['pass_rate']})")
    print(f"Errors: {analysis['total_errors']}")
    print(f"Loops: {analysis['loops_detected']}")
    print(f"Handovers: {analysis['handovers']}")
    print(f"Clarifications: {analysis['clarifications']}")

    print(f"\nState distribution (top 10):")
    for state, count in sorted(analysis['state_distribution'].items(), key=lambda x: -x[1])[:10]:
        print(f"  {state}: {count}")

    print(f"\nAction distribution (top 10):")
    for action, count in sorted(analysis['action_distribution'].items(), key=lambda x: -x[1])[:10]:
        print(f"  {action}: {count}")

    # Show failed conversations
    failures = [r for r in results if not r["passed"]]
    if failures:
        print(f"\nFailed conversations ({len(failures)}):")
        for f in failures[:10]:
            print(f"  {f['id']}: {f['errors'][:3]}")

    # Save results
    output = Path("/tmp/lawim-mission-3b-results.json")
    with open(output, "w") as f:
        json.dump({
            "analysis": analysis,
            "results": [{
                "id": r["id"],
                "passed": r["passed"],
                "steps": len(r["steps"]),
                "errors": r["errors"],
            } for r in results],
        }, f, indent=2)
    print(f"\nResults saved to {output}")
