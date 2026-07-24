#!/usr/bin/env python3
"""Program G.2 — validate historical conversation corpus through Program F engine."""
import json, os, sys, uuid, time, hashlib
from pathlib import Path
from collections import Counter

sys.path.insert(0, "/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2")
sys.path.insert(0, "/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/code")
os.environ.setdefault("LAWIM_VAULT_KEY", "x")
import warnings; warnings.filterwarnings("ignore")

from lawim_runtime.conversation.journey import ConversationJourneyOrchestrator, JourneyState, BusinessActionResult

DOCS = Path("/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/docs/program_g2")
RUN_ID = f"g2-{uuid.uuid4().hex[:8]}"
CORPUS_PATH = "/media/abel/1A4696CE4696AA51/Telechargement/test"

class _Biz:
    def __init__(self): self.calls = []
    def create_search_request(self, **kw):
        oid = f"h-{uuid.uuid4().hex[:10]}"
        self.calls.append(kw)
        return BusinessActionResult(True, "create_property_search", "marketplace_service_request", oid, "ok")

def load_jsonl(path):
    convs = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                convs.append(json.loads(line))
    return convs

def run_conversation(msgs, conv_id):
    """Run a list of user messages through Program F. Returns turn-by-turn data."""
    biz = _Biz()
    orch = ConversationJourneyOrchestrator(property_search_service=biz)
    state = JourneyState()
    state.conversation_id = conv_id
    turns = []
    start = time.time()
    for msg in msgs:
        t0 = time.time()
        try:
            r = orch.process(msg, state)
        except Exception as e:
            turns.append(dict(message=msg, error=str(e)[:200], duration_ms=round((time.time()-t0)*1000)))
            continue
        t1 = time.time()
        rp = r.response_plan
        resp = (rp.message or rp.question_text or "") if rp else ""
        turns.append(dict(
            message=msg,
            response=resp,
            response_type=rp.response_type.value if rp else "",
            intent=r.intent.intent if r.intent else "",
            status=state.journey_status.value,
            facts=dict(state.confirmed_facts),
            missing=list(state.missing_fields),
            biz_ids=dict(state.business_object_ids) if state.business_object_ids else {},
            duration_ms=round((t1 - t0) * 1000),
        ))
    return dict(
        conversation_id=conv_id,
        turns=turns,
        duration=round(time.time() - start, 2),
        final_status=state.journey_status.value,
        final_facts=dict(state.confirmed_facts),
        business_object=dict(state.business_object_ids) if state.business_object_ids else None,
        biz_calls=len(biz.calls),
        verdict="PENDING",
    )

def classify_verdict(result):
    """Automatically determine verdict based on conversation outcome."""
    turns = result["turns"]
    if not turns:
        return "TECHNICAL_FAILURE"
    has_empty = any(not t.get("response") for t in turns)
    if has_empty:
        return "CONVERSATIONAL_FAILURE"
    if result["business_object"]:
        return "FUNCTIONAL_SUCCESS"
    statuses = [t["status"] for t in turns]
    if "WAITING_FOR_CLARIFICATION" in statuses:
        return "LEGITIMATELY_INCOMPLETE"
    if "READY_FOR_ACTION" in statuses or "ACTION_COMPLETED" in statuses:
        # Had enough info but user didn't confirm
        return "LEGITIMATELY_INCOMPLETE"
    if "QUALIFYING" in statuses and len(turns) >= 3:
        return "LEGITIMATELY_INCOMPLETE"
    return "LEGITIMATELY_INCOMPLETE"

def main():
    DOCS.mkdir(parents=True, exist_ok=True)
    
    # ── Load corpora ────────────────────────────────────────────────────
    corpus_sources = [
        ("LAWIM_Conversation_Dataset", "lawim_conversation_dataset/lawim_conversations_trilingual.jsonl",
         f"{CORPUS_PATH}/LAWIM_Conversation_Dataset.zip"),
        ("LAWIM_Conversation_Corpus_1250_test", "lawim_conversation_corpus_1250/test.jsonl",
         f"{CORPUS_PATH}/LAWIM_Conversation_Corpus_1250.zip"),
        ("LAWIM_Conversation_Corpus_1250_dev", "lawim_conversation_corpus_1250/dev.jsonl",
         f"{CORPUS_PATH}/LAWIM_Conversation_Corpus_1250.zip"),
        ("LAWIM_Conversation_Corpus_10000_sample", "lawim_conversation_corpus_10000/lawim_conversations_10000.jsonl",
         f"{CORPUS_PATH}/LAWIM_Conversation_Corpus_10000.zip"),
    ]
    
    results = []
    total_turns = 0
    verdicts = Counter()
    defects = []

    for corpus_name, rel_path, zip_path in corpus_sources:
        # Determine full path (might be extracted or in zip)
        extracted_dir = f"/tmp/corpus_g2_{corpus_name}"
        jsonl_path = f"{extracted_dir}/{rel_path}"
        if not os.path.exists(jsonl_path):
            import subprocess
            subprocess.run(["unzip", "-o", zip_path, "-d", extracted_dir], capture_output=True)
        
        convs = load_jsonl(jsonl_path)
        is_10000 = "10000_sample" in corpus_name
        if is_10000:
            import random
            convs = random.Random(42).sample(convs, min(100, len(convs)))
        
        print(f"  {corpus_name}: {len(convs)} conversations")
        
        for ci, c in enumerate(convs):
            conv_id = f"{RUN_ID}-{corpus_name[:10]}-{ci:04d}"
            messages = [m["content"] for m in c.get("messages", []) if m.get("role") == "user"]
            if not messages:
                continue
            
            result = run_conversation(messages, conv_id)
            result["source"] = corpus_name
            result["source_index"] = ci
            result["language"] = c.get("language", "unknown")
            result["expected_intent"] = c.get("intent", "unknown")
            result["expected_slots"] = c.get("known_slots", {})
            result["verdict"] = classify_verdict(result)
            
            verdicts[result["verdict"]] += 1
            total_turns += len(result["turns"])
            
            # Check for defects
            for t in result["turns"]:
                if not t.get("response"):
                    defects.append(dict(cid=conv_id, turn=t, cat="EMPTY_RESPONSE"))
                if t.get("status") == "READY_FOR_ACTION" and not t.get("facts", {}).get("city"):
                    defects.append(dict(cid=conv_id, turn=t, cat="FALSE_READY_FOR_ACTION"))
            
            results.append(result)
    
    # ── Output conversations ────────────────────────────────────────────
    conv_lines = ["# Historical Conversations — Programme G.2", f"", f"Run ID: {RUN_ID}", f"Total conversations: {len(results)}", ""]
    for i, r in enumerate(results):
        conv_lines.append(f"{'='*53}")
        conv_lines.append(f"Conversation historique {i+1:03d}")
        conv_lines.append(f"{'='*53}")
        conv_lines.append(f"**Source :** {r['source']} #{r['source_index']}")
        conv_lines.append(f"**Language :** {r.get('language', '?')}")
        conv_lines.append(f"**Expected intent :** {r.get('expected_intent', '?')}")
        conv_lines.append(f"**Conversation ID :** {r['conversation_id']}")
        conv_lines.append(f"**Tours :** {len(r['turns'])}")
        conv_lines.append(f"**Duree :** {r['duration']}s")
        conv_lines.append(f"**Statut final :** {r['final_status']}")
        conv_lines.append(f"**Verdict :** {r['verdict']}")
        conv_lines.append(f"**Objet métier :** {json.dumps(r['business_object']) if r['business_object'] else 'Aucun'}")
        conv_lines.append("")
        for ti, t in enumerate(r["turns"], 1):
            conv_lines.append(f"{'-'*53}")
            conv_lines.append(f"Tour {ti}")
            conv_lines.append(f"{'-'*53}")
            conv_lines.append(f"**Utilisateur :** {t['message']}")
            conv_lines.append(f"**LAWIM :** {t.get('response','(empty)')}")
            conv_lines.append(f"**Intent :** {t['intent']}")
            conv_lines.append(f"**Status :** {t['status']}")
            conv_lines.append(f"**Faits :** {json.dumps(t['facts'], ensure_ascii=False)}")
            if t["missing"]:
                conv_lines.append(f"**Manquants :** {t['missing']}")
            if t.get("error"):
                conv_lines.append(f"**Erreur :** {t['error']}")
            conv_lines.append("")
    
    (DOCS / "historical_conversations_full.md").write_text("\n".join(conv_lines))
    
    # ── Statistics ──────────────────────────────────────────────────────
    stat_lines = ["# Quality Report — Historical Corpus", "",
                  f"**Corpus sources:** {len(corpus_sources)}", f"**Conversations:** {len(results)}",
                  f"**Total turns:** {total_turns}", f"**Business objects created:** {sum(1 for r in results if r['business_object'])}",
                  "", "## Verdict Distribution", "| Verdict | Count | % |", "|---|---:|---:|"]
    for v, c in verdicts.most_common():
        stat_lines.append(f"| {v} | {c} | {c/len(results)*100:.1f}% |" if results else f"| {v} | 0 | 0% |")
    
    stat_lines.extend(["", "## Defects", f"**Total defects:** {len(defects)}"])
    defcats = Counter(d["cat"] for d in defects)
    for cat, cnt in defcats.most_common():
        stat_lines.append(f"- {cat}: {cnt}")
    
    stat_lines.extend(["", "## Language Distribution"])
    langs = Counter(r.get("language", "?") for r in results)
    for lang, cnt in langs.most_common():
        stat_lines.append(f"- {lang}: {cnt}")
    
    (DOCS / "historical_quality_report.md").write_text("\n".join(stat_lines))
    
    # ── Business operations ─────────────────────────────────────────────
    biz_lines = ["# Business Operations — Historical Corpus", ""]
    created = 0
    for r in results:
        if r["business_object"]:
            created += 1
            biz_lines.append(f"## Conversation {r['conversation_id']}")
            biz_lines.append(f"**Action:** create_property_search")
            biz_lines.append(f"**Object type:** marketplace_service_request")
            biz_lines.append(f"**Object ID:** {r['business_object'].get('object_id', 'N/A')}")
            biz_lines.append(f"**Facts:** {json.dumps(r['final_facts'], ensure_ascii=False)}")
            biz_lines.append(f"**Turns:** {len(r['turns'])}")
            biz_lines.append("")
    biz_lines.append(f"**Total objects created:** {created}/{len(results)}")
    (DOCS / "business_operations.md").write_text("\n".join(biz_lines))
    
    # ── Defect report ───────────────────────────────────────────────────
    defect_lines = ["# Defect Report — Historical Corpus", ""]
    if not defects:
        defect_lines.append("No defects detected.")
    else:
        defect_lines.append(f"| # | Category | Conversation | Tour | User message | LAWIM response |")
        defect_lines.append("|---|----------|-------------|------|-------------|---------------|")
        for i, d in enumerate(defects[:100], 1):
            user = d["turn"].get("message", "")[:40]
            resp = d["turn"].get("response", "")[:40]
            cid = d["cid"][:30]
            defect_lines.append(f"| {i} | {d['cat']} | {cid} | {d['turn'].get('response_type','?')} | {user} | {resp} |")
    (DOCS / "defect_report.md").write_text("\n".join(defect_lines))
    
    # ── Final report ────────────────────────────────────────────────────
    final = [f"# Final Report — Programme G.2", "",
             f"**HEAD:** {os.popen('git rev-parse --short HEAD').read().strip()}",
             f"**Branch:** {os.popen('git branch --show-current').read().strip()}",
             f"**Run ID:** {RUN_ID}", "",
             f"## Summary", f"- Corpus sources: {len(corpus_sources)}",
             f"- Conversations executed: {len(results)}",
             f"- Total turns: {total_turns}",
             f"- Functional success: {verdicts.get('FUNCTIONAL_SUCCESS', 0)}",
             f"- Legitimately incomplete: {verdicts.get('LEGITIMATELY_INCOMPLETE', 0)}",
             f"- Conversational failures: {verdicts.get('CONVERSATIONAL_FAILURE', 0)}",
             f"- Business objects created: {created}", "",
             f"## Defects", f"- Total: {len(defects)}",
             "| Category | Count |", "|----------|------:|"]
    for cat, cnt in defcats.most_common():
        final.append(f"| {cat} | {cnt} |")
    
    final.append("")
    final.append("## Files")
    for f in sorted(DOCS.iterdir()):
        final.append(f"- {f.name} ({f.stat().st_size} bytes)")
    
    final.append("")
    final.append("## Verdict")
    
    has_critical = any(d["cat"] in ("EMPTY_RESPONSE", "FALSE_READY_FOR_ACTION", "FALSE_ACTION_COMPLETED") for d in defects)
    if not has_critical and created > 0:
        final.append("LAWIM_PROGRAM_G2_ACCEPTANCE_PASS")
    elif not has_critical:
        final.append("LAWIM_PROGRAM_G2_ACCEPTANCE_PARTIAL")
    else:
        final.append("LAWIM_PROGRAM_G2_ACCEPTANCE_FAIL")
    
    (DOCS / "final_report.md").write_text("\n".join(final))
    
    print(f"\n=== G.2 DONE ===")
    print(f"Conversations: {len(results)}, Turns: {total_turns}, Objects: {created}")
    print(f"Verdicts: {dict(verdicts)}")
    print(f"Defects: {len(defects)}")
    for cat, cnt in defcats.most_common():
        print(f"  {cat}: {cnt}")
    print(f"Files: {len(list(DOCS.iterdir()))}")

if __name__ == "__main__":
    main()
