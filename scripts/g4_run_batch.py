#!/usr/bin/env python3
"""G.4 — Batch executor for 10,000 conversations. Resumable, idempotent."""
import json, os, sys, time, hashlib
from pathlib import Path
from collections import Counter

sys.path.insert(0, "/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2")
sys.path.insert(0, "/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/code")
os.environ.setdefault("LAWIM_VAULT_KEY", "x")
import warnings; warnings.filterwarnings("ignore")

from lawim_runtime.conversation.journey import ConversationJourneyOrchestrator, JourneyState, BusinessActionResult

DOCS = Path("/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/docs/program_g4")
BATCH_SIZE = 250

class _Biz:
    def __init__(self): self.calls = []
    def create_search_request(self, **kw):
        oid = f"g4-{kw.get('conversation_id','?')[:16]}"
        self.calls.append(kw)
        return BusinessActionResult(True, "create_property_search", "marketplace_service_request", oid, "ok")

def main():
    # Load manifest
    manifest_path = DOCS / "run_manifest.json"
    if not manifest_path.exists():
        print("ERROR: manifest not found. Run g4_generate_corpus.py first.")
        return
    
    with open(manifest_path) as f:
        manifest = json.load(f)
    
    # Load corpus
    corpus_path = DOCS / "generated_corpus.jsonl"
    if not corpus_path.exists():
        print(f"ERROR: corpus not found at {corpus_path}")
        return
    
    with open(corpus_path) as f:
        scenarios = [json.loads(line) for line in f if line.strip()]
    
    # Determine which batches to run
    completed = set(manifest.get("completed_batches", []))
    batch_size = manifest.get("batch_size", BATCH_SIZE)
    total = len(scenarios)
    
    orch = ConversationJourneyOrchestrator(property_search_service=_Biz())
    all_results = []
    
    for batch_num in range(0, total, batch_size):
        batch_id = batch_num // batch_size + 1
        if batch_id in completed:
            print(f"  Batch {batch_id}: already completed, skipping")
            continue
        
        batch_scenarios = scenarios[batch_num:batch_num + batch_size]
        batch_results = []
        
        print(f"  Batch {batch_id}: scenarios {batch_num+1}-{min(batch_num+batch_size, total)}")
        
        for sc in batch_scenarios:
            conv_id = f"g4-{sc['scenario_id']}"
            state = JourneyState()
            state.conversation_id = conv_id
            turns = []
            for msg in sc["messages"]:
                r = orch.process(msg, state)
                rp = r.response_plan
                resp = (rp.message or rp.question_text or "") if rp else ""
                intent = r.intent.intent if r.intent else ""
                turns.append(dict(
                    message=msg, response=resp, intent=intent,
                    status=state.journey_status.value,
                    facts=dict(state.confirmed_facts),
                    missing=list(state.missing_fields),
                    biz_ids=dict(state.business_object_ids) if state.business_object_ids else {},
                ))
            batch_results.append(dict(
                scenario_id=sc["scenario_id"], sector=sc["sector"],
                language=sc["language"], turns=turns,
                final_status=state.journey_status.value,
                business_object=bool(state.business_object_ids),
            ))
        
        # Save batch results
        batch_file = DOCS / f"batch_{batch_id:04d}.json"
        with open(batch_file, "w") as f:
            json.dump(batch_results, f, ensure_ascii=False, indent=2)
        
        completed.add(batch_id)
        manifest["completed_batches"] = sorted(completed)
        manifest["executed"] = len(completed) * batch_size
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)
        
        print(f"    Done: {len(batch_results)} conversations, updated manifest")
    
    # Aggregate results
    verdicts = Counter()
    total_biz = 0
    total_turns = 0
    lang_dist = Counter()
    sector_dist = Counter()
    
    for batch_id in sorted(completed):
        batch_file = DOCS / f"batch_{batch_id:04d}.json"
        if not batch_file.exists(): continue
        with open(batch_file) as f:
            batch_results = json.load(f)
        for r in batch_results:
            status = r.get("final_status", "?")
            verdicts[status] += 1
            total_biz += 1 if r.get("business_object") else 0
            total_turns += len(r.get("turns", []))
            lang_dist[r.get("language", "?")] += 1
            sector_dist[r.get("sector", "?")] += 1
    
    print(f"\n=== G.4 CAMPAIGN SUMMARY ===")
    print(f"Total batches: {len(completed)}/{total//batch_size + 1}")
    print(f"Total conversations: {manifest['executed']}")
    print(f"Total turns: {total_turns}")
    print(f"Business objects: {total_biz}")
    print(f"Status distribution: {dict(verdicts.most_common())}")
    print(f"Language distribution: {dict(lang_dist.most_common())}")
    
    if manifest['executed'] >= 10000:
        print("\n✅ 10,000 conversations reached!")

if __name__ == "__main__":
    main()
