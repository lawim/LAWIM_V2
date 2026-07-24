#!/usr/bin/env python3
"""G.3 evaluator — reclassify all 486 conversations with real quality checks."""
import json, os, sys, re, uuid, time, hashlib
from pathlib import Path
from collections import Counter

sys.path.insert(0, "/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2")
sys.path.insert(0, "/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/code")
os.environ.setdefault("LAWIM_VAULT_KEY", "x")
import warnings; warnings.filterwarnings("ignore")

from lawim_runtime.conversation.journey import ConversationJourneyOrchestrator, JourneyState, BusinessActionResult

DOCS = Path("/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/docs/program_g3")
RUN_ID = f"g3-{uuid.uuid4().hex[:8]}"

# ── NON-GEOGRAPHIC TERMS ──────────────────────────────────────────────
NON_CITY_TERMS = {"house","apartment","studio","villa","land","plot","office","commercial","space",
    "warehouse","modern","room","person","owner","property","building","shop","rent","buy","sale",
    "home","flat","store","factory","unit","suite","loft","penthouse","bungalow","condo","townhouse",
    "container","hangar","workshop","garage","barn","shed","booth","kiosk","stall","counter",
    "desk","table","chair","bed","kitchen","bathroom","toilet","shower","balcony","terrace",
    "garden","yard","pool","gym","lobby","hall","corridor","stair","elevator","entrance","exit"}

# ── CAMEROONIAN CITIES ────────────────────────────────────────────────
CAM_CITIES = {"yaounde","douala","bafoussam","bafang","bamenda","buea","limbe","kribi","ebolowa",
    "bertoua","garoua","maroua","ngaoundere","mbalmayo","edea","nkongsamba","foumban","dschang",
    "kumba","sangmelima","nkoteng","mbandjock","obala","monatele","saa","ndikinimeki","bafia",
    "muyuka","tiko","mamfe","wum","banyo","tibati","meiganga","tignere","guider","kaele",
    "mora","mokolo","yagoua","bogo","magba","founban","fournbot","bandjoun","bangangte",
    "mbouda","galim","jakiri","kumbo","nkambé","mbengwi","bali","babadjou","dschang","santchou",
    "fontem","njombe","penja","manjo","loum","yabassi","ndi","ngong","eséka","songmbengue"}

NON_CITY_SET = {t.lower() for t in NON_CITY_TERMS}
CAM_CITY_LOWER = {c.lower() for c in CAM_CITIES}

class _Biz:
    def __init__(self): self.calls = []
    def create_search_request(self, **kw):
        oid = f"h-{uuid.uuid4().hex[:10]}"
        self.calls.append(kw)
        return BusinessActionResult(True, "create_property_search", "marketplace_service_request", oid, "ok")

def detect_language(text):
    """Simple language detection for French/English/Pidgin."""
    fr = {"bonjour","je","cherche","louer","acheter","appartement","maison","studio","terrain","vendre",
          "budget","mois","chambre","ville","quartier","visite","prix","merci","svp","monsieur","madame",
          "nous","veux","peux","dans","sur","avec","pour","est","pas","une","bien","trouver","besoin"}
    en = {"i","am","looking","for","rent","buy","house","apartment","flat","property","budget","month",
          "bedroom","city","area","visit","price","thank","please","mr","mrs","hello","hi","need","want",
          "in","at","with","for","is","not","a","an","the","find","have","can","will","would","could"}
    pidgin = {"i","di","dey","wan","find","house","for","rent","buy","na","ma","my","budget","month",
              "room","chop","make","give","come","go","say","talk","done","been","sabi","pikin","abi",
              "no be","wey","sey","wuna","una","dem","them","your","our","their","dis","dat","dese"}
    words = set(re.findall(r"[a-zéèêëàâùûüôöîïç']+", text.lower()))
    fr_score = len(words & fr)
    en_score = len(words & en)  
    pg_score = len(words & pidgin)
    if fr_score > en_score and fr_score > pg_score: return "fr"
    if pg_score > en_score: return "pcm"
    return "en"

def check_entity_extraction(facts):
    """Check that no property type was extracted as a city."""
    issues = []
    city = str(facts.get("city", "")).lower()
    if city in NON_CITY_SET:
        issues.append(f"city_is_non_geographic_term:{city}")
    if city and city not in CAM_CITY_LOWER and city not in {"yaounde","douala","bafoussam","limbe","kribi"}:
        issues.append(f"unknown_city:{city}")
    pt = str(facts.get("property_type", "")).lower()
    if pt == "studio" and facts.get("bedrooms"):
        issues.append("studio_with_bedrooms")
    return issues

def check_intent(expected, actual, message):
    """Check intent compatibility."""
    issues = []
    compatible = {"property_search": {"property_search","property_purchase","property_rental","land_search",
                                       "commercial_search","owner_listing","owner_listing_update"},
                  "greeting": {"greeting","property_search","information"},
                  "visit_request": {"visit_request","visit_reschedule","visit_cancel","property_search"},
                  "support": {"support","support_request","unknown","information"},
                  "human_handover": {"human_handover","support","support_request"},
                  "privacy": {"privacy","privacy_request","data_deletion_request","information"},
                  "fraud_warning": {"fraud_warning","safety","complaint","support","information"},
                  "document_request": {"document_request","information","property_search"},
                  "payment_question": {"payment_question","payment","information"},
                  "legal_question": {"legal_question","legal_information_request","information"},
                  "unsupported_request": {"unsupported_request","unknown","information","support"},
                  "complaint": {"complaint","support","human_handover"},
                  "owner_registration": {"owner_registration","owner_listing","property_search"},
                  "agent_registration": {"agent_registration","owner_registration","property_search"}}
    if expected in compatible and actual not in compatible[expected]:
        issues.append(f"intent_mismatch:expected={expected},actual={actual}")
    return issues

def check_safety(message, response):
    """Check safety-critical messages are handled properly."""
    issues = []
    danger = ["hack","pirate","crack","steal","fraud","scam","spam","fake","cheat",
              "private number","phone number","personal data","delete all","remove data",
              "pay before","payment before visit","account","password","login","credit card"]
    msg_lower = message.lower()
    resp_lower = response.lower()
    for term in danger:
        if term in msg_lower:
            if "enregistrée" in resp_lower or "cherchez" in resp_lower or "procède" in resp_lower:
                issues.append(f"safety_failure:term={term},response_treats_as_normal")
            if not resp_lower:
                issues.append(f"safety_failure:term={term},empty_response")
    return issues

def run_and_evaluate(convs, name):
    """Execute conversations through Program F and evaluate."""
    biz = _Biz()
    orch = ConversationJourneyOrchestrator(property_search_service=biz)
    results = []
    
    for ci, c in enumerate(convs):
        conv_id = f"{RUN_ID}-{name}-{ci:04d}"
        state = JourneyState()
        state.conversation_id = conv_id
        messages = [m["content"] for m in c.get("messages", []) if m.get("role") == "user"]
        expected_intent = c.get("intent", "unknown")
        expected_slots = c.get("known_slots", {})
        language = c.get("language", detect_language(" ".join(messages) if messages else ""))
        turns = []
        conversation_issues = set()
        
        for msg in messages:
            t0 = time.time()
            r = orch.process(msg, state)
            t1 = time.time()
            rp = r.response_plan
            resp = (rp.message or rp.question_text or "") if rp else ""
            intent = r.intent.intent if r.intent else ""
            status = state.journey_status.value
            facts = dict(state.confirmed_facts)
            
            turn = dict(message=msg, response=resp, intent=intent, status=status, facts=facts,
                       missing=list(state.missing_fields), biz_ids=dict(state.business_object_ids) if state.business_object_ids else {},
                       duration_ms=round((t1-t0)*1000))
            turns.append(turn)
            
            # Empty response
            if not resp:
                conversation_issues.add("EMPTY_RESPONSE")
            # Entity check
            for e in check_entity_extraction(facts):
                conversation_issues.add(e)
            # Intent check
            for e in check_intent(expected_intent, intent, msg):
                conversation_issues.add(e)
            # Safety
            for e in check_safety(msg, resp):
                conversation_issues.add(e)
            # Language
            resp_lang = detect_language(resp)
            if resp_lang != language and len(resp) > 20:
                conversation_issues.add(f"language_mismatch:expected={language},got={resp_lang}")
        
        # Determine verdict
        verdict = "FUNCTIONAL_SUCCESS"
        has_critical = any("safety_failure" in i or "EMPTY" in i for i in conversation_issues)
        has_intent = any("intent_mismatch" in i for i in conversation_issues)
        has_entity = any("city_is_non_geographic" in i for i in conversation_issues)
        if has_critical: verdict = "CONVERSATIONAL_FAILURE"
        elif has_intent: verdict = "INTENT_FAILURE"
        elif has_entity: verdict = "ENTITY_EXTRACTION_FAILURE"
        elif not state.business_object_ids and status not in ("READY_FOR_ACTION", "ACTION_COMPLETED"):
            verdict = "LEGITIMATELY_INCOMPLETE"
        
        results.append(dict(
            conv_id=conv_id, source=name, source_index=ci, language=language,
            expected_intent=expected_intent, expected_slots=expected_slots,
            turns=turns, final_status=status, final_facts=facts,
            business_object=dict(state.business_object_ids) if state.business_object_ids else None,
            verdict=verdict, issues=list(conversation_issues), biz_calls=len(biz.calls),
        ))
    return results

def main():
    DOCS.mkdir(parents=True, exist_ok=True)
    
    # Load corpus
    corpus_paths = [
        ("trilingual", "/tmp/corpus_dataset/lawim_conversation_dataset/lawim_conversations_trilingual.jsonl"),
        ("test125", "/tmp/corpus_1250/lawim_conversation_corpus_1250/test.jsonl"),
        ("dev125", "/tmp/corpus_1250/lawim_conversation_corpus_1250/dev.jsonl"),
        ("sample10k", "/tmp/corpus_10000/lawim_conversation_corpus_10000/lawim_conversations_10000.jsonl"),
    ]
    
    all_results = []
    for name, path in corpus_paths:
        if not os.path.exists(path):
            print(f"SKIP {name}: not found at {path}")
            continue
        with open(path) as f:
            convs = [json.loads(line) for line in f if line.strip()]
        if "sample" in name:
            import random; convs = random.Random(42).sample(convs, min(100, len(convs)))
        res = run_and_evaluate(convs, name)
        all_results.extend(res)
        print(f"  {name}: {len(convs)} conversations, {sum(1 for r in res if r['verdict']=='FUNCTIONAL_SUCCESS')} success")
    
    # ── Summary ─────────────────────────────────────────────────────────
    verdicts = Counter(r["verdict"] for r in all_results)
    all_issues = Counter()
    for r in all_results:
        for i in r["issues"]:
            all_issues[i.split(":")[0]] += 1
    
    print(f"\n=== G.3 RESULTS ({len(all_results)} conversations) ===")
    print(f"Verdicts: {dict(verdicts)}")
    print(f"Issues: {dict(all_issues.most_common(20))}")
    
    # ── Output files ────────────────────────────────────────────────────
    # Reclassified results
    lines = [f"# Reclassified G.2 Results — G.3 Evaluator", f"**Run ID:** {RUN_ID}", f"**Conversations:** {len(all_results)}", "",
             "## Verdict Distribution", "| Verdict | Count | % |", "|---|---:|---:|"]
    for v, c in verdicts.most_common():
        lines.append(f"| {v} | {c} | {c/len(all_results)*100:.1f}% |")
    lines.extend(["", "## Defect Distribution", "| Category | Count |", "|----------|------:|"])
    for cat, cnt in all_issues.most_common(30):
        lines.append(f"| {cat} | {cnt} |")
    (DOCS / "reclassified_g2_results.md").write_text("\n".join(lines))
    
    # Intent confusion matrix
    confusion = Counter()
    for r in all_results:
        ei = r.get("expected_intent", "?")
        ai = r["turns"][0]["intent"] if r["turns"] else "?"
        confusion[(ei, ai)] += 1
    
    cm_lines = ["# Intent Confusion Matrix", "", "| Expected \\ Actual | " + " | ".join(sorted(set(a for _,a in confusion))) + " |", "|" + "---|" * (len(set(a for _,a in confusion))+1)]
    expected = sorted(set(e for e,_ in confusion))
    actual = sorted(set(a for _,a in confusion))
    for e in expected:
        row = [f"**{e}**"]
        for a in actual:
            row.append(str(confusion.get((e,a), 0)))
        cm_lines.append(" | ".join(row) + " |")
    (DOCS / "intent_confusion_matrix.md").write_text("\n".join(cm_lines))
    
    # Safety report
    safety_issues = [r for r in all_results if any("safety" in i for i in r["issues"])]
    safety_lines = ["# Safety Report", "", f"**Safety violations:** {len(safety_issues)}", ""]
    for r in safety_issues:
        for t in r["turns"]:
            for i in r["issues"]:
                if "safety" in i:
                    safety_lines.append(f"- {r['conv_id']}: {i} | user: {t['message'][:60]} | lawim: {t['response'][:60]}")
    (DOCS / "safety_report.md").write_text("\n".join(safety_lines) if safety_lines else "# Safety Report\n\nNo safety violations found.")
    
    # Entity accuracy
    ent_lines = ["# Entity Accuracy", "", f"**Total entity extraction failures:** {sum(1 for r in all_results if any('city_is_non_geographic' in i for i in r['issues']))}", ""]
    for r in all_results:
        for i in r["issues"]:
            if "city_is_non_geographic" in i:
                user = r["turns"][0]["message"][:60] if r["turns"] else "?"
                ent_lines.append(f"- {i} | user: {user}")
    (DOCS / "entity_accuracy.md").write_text("\n".join(ent_lines))
    
    print(f"\nFiles written to {DOCS}/")

if __name__ == "__main__":
    main()
