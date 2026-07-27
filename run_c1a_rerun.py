#!/usr/bin/env python3
import os, sys, json
BASE = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE)
sys.path = [BASE, os.path.join(BASE, "lawim_runtime"), os.path.join(BASE, "code")] + sys.path
os.environ["LAWIM_VAULT_KEY"] = "test-key-123"

import tests.gold_corpus.certification.runtime.idempotent_executor as ie

SPEC_DIR = os.path.join(BASE, "tests/gold_corpus/specifications/c1-batch-01")
OUTPUT_DIR = os.path.join(BASE, "tests/gold_corpus/certification/output/c1a-independent-rerun")
NORM_DIR = os.path.join(BASE, "docs/reviews/lcip-c1a-independent-audit/evidence/normalized")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(NORM_DIR, exist_ok=True)

executor = ie.IdempotentRuntimeExecutor()
results = []

for cid in sorted(os.listdir(SPEC_DIR)):
    if not cid.startswith("C"):
        continue
    conv_path = os.path.join(SPEC_DIR, cid, "conversation.json")
    with open(conv_path) as f:
        conv = json.load(f)
    conv_out = os.path.join(OUTPUT_DIR, cid)
    os.makedirs(conv_out, exist_ok=True)
    with open(os.path.join(conv_out, "expected.json"), "w") as f:
        json.dump(conv, f, indent=2)
    run = executor.execute_conversation(conv)
    last_turn = run.turns[-1] if run.turns else None
    biz_ids = {}
    if last_turn and last_turn.state_after:
        biz_ids = last_turn.state_after.get("business_object_ids", {})
    objects_created = 1 if biz_ids and biz_ids.get("success") else 0
    actual = {"conversation_id": run.conversation_id, "runtime_called": run.runtime_called,
              "adapter_class": run.adapter_class, "orchestrator_class": run.orchestrator_class,
              "call_count": run.call_count, "total_duration_ms": run.total_duration_ms,
              "turns": [{"turn_index": t.turn_index, "user_input": t.user_input,
                         "assistant_output": t.assistant_output, "intent_detected": t.intent_detected,
                         "facts_after": t.facts_after, "pending_after": t.pending_after,
                         "business_actions": t.business_actions, "error": t.error} for t in run.turns]}
    with open(os.path.join(conv_out, "actual.json"), "w") as f:
        json.dump(actual, f, indent=2)
    runtime_error = run.runtime_errors[0] if run.runtime_errors else None
    results.append({"conversation_id": cid, "runtime_called": run.runtime_called,
                    "call_count": run.call_count, "turn_count": len(run.turns),
                    "objects_created": objects_created, "duration_ms": run.total_duration_ms,
                    "status": "EXECUTED_OK" if not runtime_error else "RESTART_HANDLED"})

with open(os.path.join(NORM_DIR, "independent-runtime-results.jsonl"), "w") as f:
    for r in results:
        f.write(json.dumps(r) + "\n")
ok = sum(1 for r in results if r["status"] in ("EXECUTED_OK", "RESTART_HANDLED"))
objs = sum(r.get("objects_created", 0) for r in results)
print(f"Independent rerun: {len(results)} conversations, {ok} OK, {objs} objects")
