from __future__ import annotations

import json
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tests.mission_3b.corpus import CONVERSATIONS

from lawim_v2.conversation import Conversation, ConversationDecision, ConversationState, NormalizedMessage
from lawim_v2.conversation.domain.facts import Fact, FactCollection, FactStatus
from lawim_v2.conversation.domain.states import STATE_TRANSITIONS
from lawim_v2.conversation.planning import Planner, detect_loop
from lawim_v2.conversation.understanding.extractor import extract_all
from lawim_v2.conversation.understanding.short_replies import classify_short_reply
from lawim_v2.conversation.generation.composer import GenerativeComposer
from lawim_v2.conversation.generation.validator import ContentValidator
from lawim_v2.conversation.memory.service import MemoryService
from lawim_v2.conversation.qualification.evaluator import QualificationEvaluator
from lawim_v2.conversation.qualification.matrices import get_matrix


class RepositoryStub:
    def __init__(self):
        self.conversations = {}
        self.decisions = []
        self._next_id = 1

    def get_conversation(self, conversation_id):
        return self.conversations.get(conversation_id)

    def save_conversation(self, conv):
        if conv.conversation_id is None:
            conv.conversation_id = self._next_id
            self._next_id += 1
        self.conversations[conv.conversation_id] = conv
        return conv

    def save_decision(self, decision):
        decision.decision_id = str(uuid.uuid4())[:12]
        self.decisions.append(decision)
        return decision

    def list_projects(self, user_id):
        return []

    def get_user_active_projects(self, user_id):
        return []

    def create_maintenance_message(self, **kwargs):
        return {"id": 1}

    def record_event(self, event_kind, payload):
        pass

    def create_message(self, **kwargs):
        return {"id": 1}

    def close(self):
        pass

    def execute(self, sql, params=None):
        return type("R", (), {"fetchone": lambda: None, "fetchall": lambda: []})()

    def fetch_one(self, sql, params=None):
        return None

    def fetch_all(self, sql, params=None):
        return []

    def scalar(self, sql, params=None):
        return 0


class MemoryRepoStub:
    def __init__(self):
        self.facts = []
        self._next_id = 1

    def save_fact(self, fact):
        fact.fact_id = str(self._next_id)
        self._next_id += 1
        fact.created_at = datetime.now(timezone.utc).isoformat()
        fact.updated_at = fact.created_at
        fact.valid_from = fact.created_at
        self.facts.append(fact)
        return fact

    def supersede_fact(self, fact_id, timestamp):
        for f in self.facts:
            if f.fact_id == fact_id:
                f.confirmation_status = FactStatus.SUPERSEDED
                f.valid_to = timestamp

    def update_fact_status(self, fact_id, status):
        for f in self.facts:
            if f.fact_id == fact_id:
                f.confirmation_status = status

    def get_active_facts(self, project_id=None, dossier_id=None, conversation_id=None):
        return [f for f in self.facts if f.valid_to is None]

    def get_latest_confirmed_fact(self, field, project_id=None):
        confirmed = [f for f in self.facts if f.field == field and f.valid_to is None and f.is_confirmed()]
        if confirmed:
            return max(confirmed, key=lambda f: f.created_at or "")
        return None

    def get_facts_by_status(self, status, project_id=None):
        return [f for f in self.facts if f.confirmation_status == status and f.valid_to is None]


class ConfigStub:
    lawim_core_rebuild_maintenance_mode = False
    conversation_service_enabled = True


def run_conversation(scenario: dict) -> dict:
    repo = RepositoryStub()
    memory_repo = MemoryRepoStub()
    memory_service = MemoryService(memory_repo)
    planner = Planner()
    composer = GenerativeComposer()
    evaluator = QualificationEvaluator()

    conv = Conversation(
        user_id=1,
        channel="web",
        state=ConversationState.NEW,
    )
    conv.facts = FactCollection()
    repo.save_conversation(conv)

    steps = []
    errors = []
    loop_count = 0
    confirmed_fields = set()

    for msg_idx, msg_data in enumerate(scenario["messages"]):
        user_text = msg_data["user"]
        try:
            message = NormalizedMessage(
                raw_text=user_text,
                normalized_text=user_text.strip(),
                channel="web",
                user_id=1,
                conversation_id=conv.conversation_id,
            )

            if conv.state == ConversationState.CLOSED:
                conv.state = ConversationState.NEW
                conv.apply_transition("message_received")

            extracted = extract_all(user_text)
            for fact_data in extracted.get("facts", []):
                field = fact_data["field"]
                raw_val = str(fact_data.get("raw_value", ""))
                norm_val = fact_data.get("normalized_value")
                source = fact_data.get("source_type", "explicit")
                conf = fact_data.get("confidence", 1.0)

                existing = memory_repo.get_latest_confirmed_fact(field, project_id=conv.project_id)
                if existing:
                    memory_service.handle_correction(
                        field=field,
                        old_fact_id=existing.fact_id,
                        new_raw_value=raw_val,
                        new_normalized=norm_val,
                        source_type=source,
                        confidence=conf,
                        project_id=conv.project_id,
                        conversation_id=conv.conversation_id,
                    )
                else:
                    memory_service.add_fact(
                        field=field,
                        raw_value=raw_val,
                        normalized_value=norm_val,
                        source_type=source,
                        confidence=conf,
                        project_id=conv.project_id,
                        conversation_id=conv.conversation_id,
                    )
                confirmed_fields.add(field)

            known = memory_service.all_confirmed_as_dict(project_id=conv.project_id)
            conv.facts = memory_service.get_confirmed_facts(
                project_id=conv.project_id,
                conversation_id=conv.conversation_id,
            )

            active_projects = repo.get_user_active_projects(1)
            intent_candidates = []

            handover_request = message.is_handover_request()
            greeting = message.is_greeting()

            loop_result = detect_loop(conv, user_text, current_field=conv.last_question_field)
            if loop_result.loop_detected:
                loop_count += 1
                if loop_result.action == "handover":
                    conv.apply_transition("handover_requested")
                    steps.append({
                        "msg_idx": msg_idx,
                        "user": user_text,
                        "state_after": "HUMAN_HANDOVER",
                        "action": "HANDOVER_TO_HUMAN",
                        "response": "handover",
                        "loop_detected": True,
                    })
                    continue

            if handover_request or conv.state == ConversationState.HUMAN_HANDOVER:
                conv.apply_transition("handover_requested")
                steps.append({
                    "msg_idx": msg_idx,
                    "user": user_text,
                    "state_after": "HUMAN_HANDOVER",
                    "action": "HANDOVER_TO_HUMAN",
                    "response": "handover",
                })
                continue

            if conv.state == ConversationState.NEW:
                conv.apply_transition("message_received")
                decision = ConversationDecision(
                    conversation_id=conv.conversation_id,
                    user_id=1,
                    channel="web",
                    raw_message=user_text,
                    state_before=ConversationState.NEW,
                    state_after=ConversationState.AWAITING_INTENT,
                    action="GREETING",
                    known_facts=known,
                )
                response = composer.compose(decision)
                steps.append({
                    "msg_idx": msg_idx,
                    "user": user_text,
                    "state_after": "AWAITING_INTENT",
                    "action": "GREETING",
                    "response": response[:80],
                })
                continue

            if conv.state == ConversationState.AWAITING_INTENT:
                has_type = "property_type" in known
                has_transaction = "transaction_type" in known
                if has_type or has_transaction:
                    conv.apply_transition("intent_identified")
                    intent_name = known.get("property_type", known.get("transaction_type", "property"))
                    decision = ConversationDecision(
                        state_before=ConversationState.AWAITING_INTENT,
                        state_after=ConversationState.QUALIFYING,
                        action="UPDATE_FACT",
                        known_facts=known,
                        selected_intent=intent_name,
                        intent_confidence=0.8,
                    )
                    response = composer.compose(decision)
                    steps.append({
                        "msg_idx": msg_idx,
                        "user": user_text,
                        "state_after": "QUALIFYING",
                        "action": "UPDATE_FACT",
                        "response": response[:80],
                    })
                    continue
                else:
                    decision = ConversationDecision(
                        state_before=ConversationState.AWAITING_INTENT,
                        state_after=ConversationState.AWAITING_INTENT,
                        action="REQUEST_CLARIFICATION",
                        known_facts=known,
                        response_type="ask_intent",
                    )
                    response = composer.compose(decision)
                    steps.append({
                        "msg_idx": msg_idx,
                        "user": user_text,
                        "state_after": "AWAITING_INTENT",
                        "action": "REQUEST_CLARIFICATION",
                        "response": response[:80],
                    })
                    continue

            if conv.state == ConversationState.QUALIFYING:
                has_city = "city" in known
                has_budget = any("budget" in k for k in known)
                has_property = "property_type" in known
                has_transaction = "transaction_type" in known
                has_bedroom = "bedroom_count" in known

                ready = has_city and has_budget and has_property
                if ready:
                    conv.apply_transition("minimum_readiness")
                    decision = ConversationDecision(
                        state_before=ConversationState.QUALIFYING,
                        state_after=ConversationState.READY_FOR_SEARCH,
                        action="START_SEARCH",
                        known_facts=known,
                    )
                    response = composer.compose(decision)
                    steps.append({
                        "msg_idx": msg_idx,
                        "user": user_text,
                        "state_after": "READY_FOR_SEARCH",
                        "action": "START_SEARCH",
                        "response": response[:80],
                    })
                    continue

                if not has_city:
                    decision = ConversationDecision(
                        state_before=ConversationState.QUALIFYING,
                        state_after=ConversationState.QUALIFYING,
                        action="UPDATE_FACT",
                        known_facts=known,
                        requires_clarification=True,
                        response_type="ask_city",
                    )
                    response = "Dans quelle ville recherchez-vous ?"
                    steps.append({
                        "msg_idx": msg_idx,
                        "user": user_text,
                        "state_after": "QUALIFYING",
                        "action": "REQUEST_CLARIFICATION",
                        "response": response[:80],
                    })
                    continue

                if not has_budget and has_city:
                    decision = ConversationDecision(
                        state_before=ConversationState.QUALIFYING,
                        state_after=ConversationState.QUALIFYING,
                        action="UPDATE_FACT",
                        known_facts=known,
                        requires_clarification=True,
                        response_type="ask_budget",
                    )
                    response = "Quel est votre budget ?"
                    steps.append({
                        "msg_idx": msg_idx,
                        "user": user_text,
                        "state_after": "QUALIFYING",
                        "action": "REQUEST_CLARIFICATION",
                        "response": response[:80],
                    })
                    continue

                if not has_transaction and has_property:
                    decision = ConversationDecision(
                        state_before=ConversationState.QUALIFYING,
                        state_after=ConversationState.QUALIFYING,
                        action="UPDATE_FACT",
                        known_facts=known,
                        requires_clarification=True,
                        response_type="ask_transaction_type",
                    )
                    response = "Souhaitez-vous acheter ou louer ?"
                    steps.append({
                        "msg_idx": msg_idx,
                        "user": user_text,
                        "state_after": "QUALIFYING",
                        "action": "REQUEST_CLARIFICATION",
                        "response": response[:80],
                    })
                    continue

                decision = ConversationDecision(
                    state_before=ConversationState.QUALIFYING,
                    state_after=ConversationState.QUALIFYING,
                    action="UPDATE_FACT",
                    known_facts=known,
                )
                response = composer.compose(decision)
                steps.append({
                    "msg_idx": msg_idx,
                    "user": user_text,
                    "state_after": "QUALIFYING",
                    "action": "UPDATE_FACT",
                    "response": response[:80],
                })
                continue

            if conv.state == ConversationState.AWAITING_CLARIFICATION:
                conv.apply_transition("clarification_provided")
                decision = ConversationDecision(
                    state_before=ConversationState.AWAITING_CLARIFICATION,
                    state_after=ConversationState.QUALIFYING,
                    action="UPDATE_FACT",
                    known_facts=known,
                )
                response = composer.compose(decision)
                steps.append({
                    "msg_idx": msg_idx,
                    "user": user_text,
                    "state_after": "QUALIFYING",
                    "action": "UPDATE_FACT",
                    "response": response[:80],
                })
                continue

            if conv.state == ConversationState.READY_FOR_SEARCH:
                conv.apply_transition("search_requested")
                conv.apply_transition("results_available")
                decision = ConversationDecision(
                    state_before=ConversationState.READY_FOR_SEARCH,
                    state_after=ConversationState.RESULTS_AVAILABLE,
                    action="PRESENT_RESULTS",
                    known_facts=known,
                )
                response = composer.compose(decision)
                steps.append({
                    "msg_idx": msg_idx,
                    "user": user_text,
                    "state_after": "RESULTS_AVAILABLE",
                    "action": "PRESENT_RESULTS",
                    "response": response[:80],
                })
                continue

            decision = ConversationDecision(
                state_before=conv.state,
                state_after=conv.state,
                action="PROVIDE_INFORMATION",
                known_facts=known,
            )
            response = composer.compose(decision)
            steps.append({
                "msg_idx": msg_idx,
                "user": user_text,
                "state_after": conv.state.value,
                "action": "PROVIDE_INFORMATION",
                "response": response[:80],
            })

        except Exception as e:
            import traceback
            steps.append({
                "msg_idx": msg_idx,
                "user": user_text,
                "error": f"{type(e).__name__}: {e}",
                "traceback": traceback.format_exc(),
            })
            errors.append({"msg_idx": msg_idx, "error": str(e), "traceback": traceback.format_exc()})

    return {
        "scenario_id": scenario["id"],
        "title": scenario["title"],
        "category": scenario.get("category", "unknown"),
        "steps": steps,
        "errors": errors,
        "passed": len(errors) == 0,
    }


def main():
    print("=" * 60)
    print("LAWIM V2 - MISSION 3B - BEHAVIORAL HOMOLOGATION")
    print("=" * 60)
    print(f"\nCorpus: {len(CONVERSATIONS)} conversations, {sum(len(c['messages']) for c in CONVERSATIONS)} messages")
    print()

    start = time.time()
    results = [run_conversation(s) for s in CONVERSATIONS]
    elapsed = time.time() - start

    total_steps = sum(len(r["steps"]) for r in results)
    total_errors = sum(len(r["errors"]) for r in results)
    passed = sum(1 for r in results if r["passed"])

    state_dist = {}
    action_dist = {}
    loops = 0
    handovers = 0
    clarifications = 0
    max_steps = 0
    min_steps = float("inf")

    for r in results:
        steps = len(r["steps"])
        max_steps = max(max_steps, steps)
        min_steps = min(min_steps, steps)
        for s in r["steps"]:
            sa = s.get("state_after", "?")
            state_dist[sa] = state_dist.get(sa, 0) + 1
            ac = s.get("action", "?")
            action_dist[ac] = action_dist.get(ac, 0) + 1
            if s.get("loop_detected"):
                loops += 1
            if s.get("action") == "HANDOVER_TO_HUMAN":
                handovers += 1

    print(f"Completed in {elapsed:.1f}s")
    print(f"\n{'='*60}")
    print(f"RESULTS")
    print(f"{'='*60}")
    print(f"  Conversations:  {len(results)}")
    print(f"  Messages processed: {total_steps}")
    print(f"  Passed:         {passed}/{len(results)} ({(passed/len(results)*100) if results else 0:.1f}%)")
    print(f"  Errors:         {total_errors}")
    print(f"  Loops detected: {loops}")
    print(f"  Handovers:      {handovers}")
    print(f"  Avg steps/conversation: {total_steps/len(results):.1f}")
    print(f"  Steps range:    {min_steps}-{max_steps}")

    print(f"\n{'='*60}")
    print(f"STATE DISTRIBUTION")
    print(f"{'='*60}")
    for s, c in sorted(state_dist.items(), key=lambda x: -x[1]):
        print(f"  {s:40s} {c:5d}")

    print(f"\n{'='*60}")
    print(f"ACTION DISTRIBUTION")
    print(f"{'='*60}")
    for a, c in sorted(action_dist.items(), key=lambda x: -x[1]):
        print(f"  {a:40s} {c:5d}")

    errors_by_file = {}
    for r in results:
        for e in r["errors"]:
            cat = e.get("error", "unknown").split(":")[0]
            errors_by_file[cat] = errors_by_file.get(cat, 0) + 1

    if errors_by_file:
        print(f"\n{'='*60}")
        print(f"ERRORS BY TYPE")
        print(f"{'='*60}")
        for err_type, count in sorted(errors_by_file.items(), key=lambda x: -x[1]):
            print(f"  {err_type}: {count}")

    output = Path("/tmp/lawim-mission-3b-results.json")
    with open(output, "w") as f:
        json.dump({
            "summary": {
                "total_conversations": len(results),
                "total_messages": total_steps,
                "passed": passed,
                "failed": len(results) - passed,
                "errors": total_errors,
                "loops": loops,
                "handovers": handovers,
                "state_distribution": dict(sorted(state_dist.items(), key=lambda x: -x[1])),
                "action_distribution": dict(sorted(action_dist.items(), key=lambda x: -x[1])),
            },
            "results": [{
                "id": r["scenario_id"],
                "title": r["title"],
                "category": r["category"],
                "passed": r["passed"],
                "steps": len(r["steps"]),
                "errors": [{"msg_idx": e.get("msg_idx"), "error": e.get("error", "")[:200]} for e in r["errors"]],
            } for r in results],
        }, f, indent=2)
    print(f"\nResults saved to {output}")
    return passed == len(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
