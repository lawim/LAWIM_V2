#!/usr/bin/env python3
"""C.0 Industrial Dialogue Generator."""
import json, random, os
from typing import Optional

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

def load_data():
    with open(os.path.join(DATA_DIR, "cities.json")) as f:
        return json.load(f)["cities"] if "cities" in open(os.path.join(DATA_DIR, "cities.json")).read()[:20] else json.load(open(os.path.join(DATA_DIR, "cities.json")))

def generate_dialogue(archetype_id: str, seed: int, variation_plan: dict = None) -> dict:
    random.seed(seed)
    arch_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             "archetypes", archetype_id, "archetype.json")
    with open(arch_path) as f:
        arch = json.load(f)
    
    conv_id = f"C0-{seed:04d}"
    messages = [
        {"role": "user", "text": f"Je cherche un {arch['property_type']} à louer à Douala.", "intent": "SEARCH_PROPERTY"},
        {"role": "assistant", "text": "Quel budget mensuel souhaitez-vous consacrer ?", "intent": "ASK_BUDGET"},
        {"role": "user", "text": f"{random.randint(5,30)*10000} FCFA.", "intent": "unknown"},
        {"role": "assistant", "text": "Combien de chambres souhaitez-vous ?", "intent": "ASK_BEDROOMS"},
        {"role": "user", "text": f"{random.randint(1,4)} chambres.", "intent": "unknown"},
        {"role": "assistant", "text": "Quel quartier préférez-vous ?", "intent": "ASK_AREAS"},
        {"role": "user", "text": "Bonamoussadi.", "intent": "unknown"},
        {"role": "assistant", "text": "Quand souhaitez-vous emménager ?", "intent": "ASK_MOVE_IN_DATE"},
        {"role": "user", "text": "Le mois prochain.", "intent": "unknown"},
        {"role": "assistant", "text": "Souhaitez-vous enregistrer cette recherche ?", "intent": "CONFIRM_BUSINESS_CREATION"},
        {"role": "user", "text": "Oui.", "intent": "unknown"},
        {"role": "assistant", "text": "Votre recherche a été enregistrée.", "intent": "NONE"},
    ]
    
    return {
        "conversation_id": conv_id,
        "archetype_id": archetype_id,
        "seed": seed,
        "messages": messages,
        "channel": "web",
        "language": "fr",
        "category": arch["category"],
        "tags": ["generated"],
    }

def generate_specification(dialogue: dict, archetype_id: str) -> dict:
    return {"conversation_id": dialogue["conversation_id"], "expected_business_action": "CREATE_SEARCH",
            "expected_business_object_count": 1, "language": dialogue["language"]}
