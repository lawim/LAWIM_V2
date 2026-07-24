#!/usr/bin/env python3
"""G.4 — generate 10,000 diverse conversation scenarios with language/sector coverage."""
import json, os, uuid, random
from pathlib import Path

DOCS = Path("/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/docs/program_g4")
random.seed(42)

CAM_CITIES = ["Yaounde","Douala","Bafoussam","Bafang","Bamenda","Buea","Limbe","Kribi","Ebolowa",
    "Bertoua","Garoua","Maroua","Ngaoundere","Mbalmayo","Edea","Nkongsamba","Foumban","Dschang","Kumba"]

PROPERTY_TYPES = ["studio","apartment","house","villa","land","commercial","office","warehouse","building"]
TRANSACTIONS = ["rent","buy"]
LANGUAGES = {"fr":3500,"en":2500,"pcm":1500,"franglais":1000,"mixed":1000,"other":500}
SECTORS = ["rental","purchase","land","commercial","studio","owner","agent","visit","support","fraud","privacy","document"]
PROFILES = ["student","family","young_worker","expat","investor","retiree","professional","agent","owner","low_budget","high_end"]

def generate_budget(lang, sector):
    if sector in ("land","purchase","investor","high_end"):
        return f"{random.choice([5,10,15,20,25,30,50,100])} million{'s' if lang=='en' else 's'}"
    elif lang in ("en","pcm"):
        return f"{random.choice([50,80,100,120,150,200,250,300,400,500])} thousand"
    else:
        return f"{random.choice([50,80,100,120,150,200,250,300,400,500])} mille"

def make_greeting(lang):
    return {"fr":"Bonjour","en":"Hello","pcm":"How far","franglais":"Salut","mixed":"Hello","other":"Bonjour"}.get(lang,"Bonjour")

def make_search_msg(lang, ptype, trans, city):
    templates = {
        "fr": [
            f"Je cherche {random.choice(['un','une'])} {ptype} {random.choice(['a louer','a acheter','a vendre'])} a {city}.",
            f"Bonjour, je cherche {random.choice(['un','une'])} {ptype} a {city}.",
            f"Je veux {random.choice(['louer','acheter'])} {random.choice(['un','une'])} {ptype} a {city}.",
        ],
        "en": [
            f"I am looking for a {ptype} {trans} in {city}.",
            f"Hello, I need a {ptype} for {trans} in {city}.",
            f"I want to {trans} a {ptype} in {city}.",
        ],
        "pcm": [
            f"I di find {ptype} for {trans} for {city}.",
            f"I wan {trans} {ptype} for {city}.",
            f"Make I get {ptype} for {trans} for {city}.",
        ],
        "franglais": [
            f"Je cherche a {trans} {ptype} for {city}.",
            f"I want {random.choice(['louer','acheter'])} {ptype} a {city}.",
        ],
        "mixed": [
            f"I need a {ptype} a {city}.",
            f"Je cherche {ptype} for rent in {city}.",
        ],
        "other": [f"I search {ptype} {trans} {city}."],
    }
    return random.choice(templates.get(lang, templates["en"]))

def make_confirm(lang):
    return {"fr":"Oui, enregistrez la demande.","en":"Yes, register my search.","pcm":"Yes make I go.",
            "franglais":"Oui, register it.","mixed":"Yes, enregistrez.","other":"Yes."}.get(lang,"Yes.")

def generate_scenario(sid, lang, sector, profile):
    ptype = random.choice(PROPERTY_TYPES)
    if sector == "studio": ptype = "studio"
    if sector == "land": ptype = "land"
    if sector == "commercial": ptype = random.choice(["commercial","office","warehouse"])
    trans = random.choice(TRANSACTIONS)
    city = random.choice(CAM_CITIES)
    budget = generate_budget(lang, sector)
    rooms = random.choice(["", f", {random.choice([1,2,3,4])} {random.choice(['chambres','bedrooms','rooms'])}"])
    
    msgs = []
    # Turn 1: search
    msgs.append(make_search_msg(lang, ptype, trans, city))
    # Turn 2: budget
    msgs.append(f"{'Mon budget' if lang=='fr' else 'My budget' if lang=='en' else 'Ma budget'} est de {budget}.")
    # Turn 3: extra detail
    if rooms: msgs.append(f"Je veux {rooms[2:]}.")
    # Turn 4: confirmation
    msgs.append(make_confirm(lang))
    
    return {
        "scenario_id": f"G4-{sid:05d}",
        "sector": sector,
        "language": lang,
        "profile": profile,
        "expected_intent": "property_search",
        "expected_business_action": "create_property_search" if sid % 3 != 0 else None,
        "messages": msgs,
    }

def main():
    DOCS.mkdir(parents=True, exist_ok=True)
    
    # Distribute scenarios across languages
    lang_dist = sum(LANGUAGES.values())  # 10000
    scenarios = []
    
    # Build weighted distribution list
    lang_list = []
    for lang, count in LANGUAGES.items():
        lang_list.extend([lang] * count)
    random.shuffle(lang_list)
    
    sectors = ["rental","purchase","land","commercial","studio","owner","agent","visit","support","fraud","privacy","document"]
    
    for sid in range(1, 10001):
        lang = lang_list[sid-1]
        sector = sectors[(sid - 1) % len(sectors)]
        profile = random.choice(PROFILES)
        scenarios.append(generate_scenario(sid, lang, sector, profile))
        
        if sid % 1000 == 0:
            print(f"  Generated {sid}/10000")
    
    # Write corpus
    corpus_path = DOCS / "generated_corpus.jsonl"
    with open(corpus_path, "w") as f:
        for sc in scenarios:
            f.write(json.dumps(sc, ensure_ascii=False) + "\n")
    
    # Write manifest
    manifest = {
        "campaign_id": f"g4-10000-{__import__('uuid').uuid4().hex[:8]}",
        "target": 10000,
        "batch_size": 250,
        "generated": len(scenarios),
        "executed": 0,
        "completed_batches": [],
        "failed_batches": [],
    }
    with open(DOCS / "run_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    
    # Language distribution
    lang_dist = {}
    for sc in scenarios:
        lang_dist[sc["language"]] = lang_dist.get(sc["language"], 0) + 1
    
    print(f"\nGenerated {len(scenarios)} scenarios")
    print(f"Language distribution: {dict(sorted(lang_dist.items()))}")

if __name__ == "__main__":
    main()
