#!/usr/bin/env python3
"""Generate complete LAWIM Demo World V1 reference YAML — expanded coverage."""

from __future__ import annotations

import yaml

_NEIGHBORHOODS_YDE = ["Mvan", "Bastos", "Odza", "Nlongkak", "Tsinga", "Ngousso", "Essos", "Mendong", "Biyem-Assi", "Nkoabang", "Emana", "Etoug-Ebe", "Ekounou", "Messassi", "Nkolbisson", "Nkolfoulou"]
_NEIGHBORHOODS_DLA = ["Akwa", "Bonanjo", "Bonapriso", "Deido", "Makepe", "Bonamoussadi", "Logbaba", "Bassa", "Nylon"]
_NEIGHBORHOODS_BFS = ["Djeleng", "Kouogouo", "Tamdja", "Banengo"]
_NEIGHBORHOODS_KRI = ["Mpangou", "Bebamboue", "Lobe"]
_NEIGHBORHOODS_LIM = ["Bota", "Mile 2", "Mile 4", "Mokunda"]

_NAMES = ["des Acacias", "du Lac", "des Cocotiers", "Soleil", "Bleu", "Vert", "du Centre", "Bellevue", "des Fleurs", "du Paradis", "Royal", "Princier", "du Stade", "de la Gare", "du Marché", "des Eaux", "Diana", "Beau Séjour", "les Manguiers", "Saint Michel"]

def _uid(role, n):
    return f"DEMO-USER-{role.upper()}-{n:03d}"

def _pid(prof, n):
    return f"DEMO-PRO-{prof.upper()}-{n:03d}"

def _bid(c, n):
    return f"DEMO-PROPERTY-{c.upper()}-{n:03d}"

def _sid(n):
    return f"DEMO-SERVICE-{n:03d}"

def _oid(cat, n):
    return f"DEMO-ORG-{cat.upper()}-{n:03d}"

def _scid(n):
    return f"SCENARIO-{n:04d}"

def build():
    # --- Users (25 total) ---
    users = []
    for i in range(1, 9):  # 8 clients
        status = "active" if i <= 6 else "inactive"
        verif = "verified" if i <= 5 else "unverified"
        consent = "granted" if i <= 6 else ("pending" if i == 7 else "denied")
        city = "Yaoundé" if i <= 4 else "Douala" if i <= 6 else "Bafoussam"
        users.append({"id": _uid("CLIENT", i), "full_name": ["Jean Dupont","Alice Mbarga","Pierre Kamga","Marie Ngo Bissa","Paul Etoundi","Sarah Nkwi","Robert Tchinda","Esther Mvogo"][i-1], "role": "client", "city": city, "profile_status": status, "verification_status": verif, "consent_status": consent, "preferred_language": "fr"})

    for i in range(1, 6):  # 5 owners
        city = "Yaoundé" if i <= 3 else "Douala" if i == 4 else "Bafoussam"
        multi = i == 1
        consent = "granted" if i <= 3 else ("pending" if i == 4 else "denied")
        users.append({"id": _uid("OWNER", i), "full_name": ["Thomas Mvogo","Christine Eyanga","Suzanne Mbah","Joseph Obama","Beatrice Simo"][i-1], "role": "owner", "city": city, "profile_status": "active" if i <= 4 else "inactive", "verification_status": "verified" if i <= 3 else "unverified", "consent_status": consent, "has_multiple_properties": multi})

    for i in range(1, 4):  # 3 agents
        users.append({"id": _uid("AGENT", i), "full_name": ["Luc Tchinda","Rosalie Nkwi","Emmanuel Simo"][i-1], "role": "agent", "city": "Yaoundé" if i <= 2 else "Douala", "organization_id": _oid("AGENCY", 1) if i <= 2 else _oid("AGENCY", 2), "profile_status": "active" if i <= 2 else "suspended", "verification_status": "verified" if i <= 2 else "unverified"})

    for i in range(1, 5):  # 4 pros (SERVICE_PROVIDER role)
        users.append({"id": _uid("PRO", i), "full_name": ["Pierre Atangana","Marie Ekwé","Jean Meka","Chantal Ngo"][i-1], "role": "service_provider", "city": "Yaoundé", "profile_status": "active", "verification_status": "verified"})

    # 2 support/admin
    users.append({"id": _uid("SUPPORT", 1), "full_name": "Fabrice Noah", "role": "commercial", "city": "Yaoundé", "profile_status": "active", "verification_status": "verified"})
    users.append({"id": _uid("ADMIN", 1), "full_name": "Admin LAWIM", "role": "admin", "city": "Yaoundé", "profile_status": "active", "verification_status": "verified"})

    # --- Professional Profiles (16) ---
    pro_data = [
        ("ARCH", 1, "architect", _uid("PRO", 1), _oid("ARCHI", 1), 12, True, True),
        ("ARCH", 2, "architect", _uid("PRO", 2), _oid("ARCHI", 1), 6, True, True),
        ("NOTARY", 1, "notary", _uid("PRO", 3), _oid("NOTARY", 1), 20, True, True),
        ("SURVEYOR", 1, "surveyor", _uid("PRO", 4), _oid("SURVEY", 1), 15, True, True),
        ("LAWYER", 1, "lawyer", None, _oid("LEGAL", 1), 18, True, True),
        ("BUILDER", 1, "builder", None, _oid("CONSTRUCT", 1), 22, True, True),
        ("ELECTRICIAN", 1, "electrician", None, _oid("CONSTRUCT", 1), 8, True, True),
        ("PLUMBER", 1, "plumber", None, _oid("MAINT", 1), 10, True, True),
        ("AGENT", 1, "real_estate_agent", _uid("AGENT", 1), _oid("AGENCY", 1), 7, True, True),
        ("AGENT", 2, "real_estate_agent", _uid("AGENT", 2), _oid("AGENCY", 1), 5, True, True),
        ("MOVER", 1, "mover", None, _oid("MOVER", 1), 9, True, True),
        ("FINANCE", 1, "financial_advisor", None, _oid("FINANCE", 1), 11, True, True),
        ("INSURANCE", 1, "insurance_agent", None, _oid("FINANCE", 1), 14, True, True),
        ("MAINT", 1, "maintenance_tech", None, _oid("MAINT", 1), 6, True, True),
        ("CLEANER", 1, "cleaner", None, _oid("MAINT", 1), 4, True, False),
        ("PHOTO", 1, "photographer", None, _oid("AGENCY", 1), 5, True, True),
    ]
    profs = []
    for prefix, n, prof, uid, oid, exp, verified, available in pro_data:
        profs.append({"id": _pid(prefix, n), "profession": prof, "user_id": uid, "organization_id": oid, "years_experience": exp, "verified": verified, "available": available})

    # --- Organizations (12) ---
    orgs = [
        {"id": _oid("AGENCY", 1), "name": "DEMO Agence Centrale", "category": "real_estate_agency", "city": "Yaoundé"},
        {"id": _oid("AGENCY", 2), "name": "DEMO Immo Services", "category": "real_estate_agency", "city": "Douala"},
        {"id": _oid("NOTARY", 1), "name": "DEMO Étude Notariale", "category": "notary", "city": "Yaoundé"},
        {"id": _oid("ARCHI", 1), "name": "DEMO Architecture Studio", "category": "architecture", "city": "Yaoundé"},
        {"id": _oid("LEGAL", 1), "name": "DEMO Cabinet Juridique", "category": "legal", "city": "Yaoundé"},
        {"id": _oid("CONSTRUCT", 1), "name": "DEMO Bâtir Plus", "category": "construction", "city": "Yaoundé"},
        {"id": _oid("SURVEY", 1), "name": "DEMO Géomètre Expert", "category": "surveying", "city": "Yaoundé"},
        {"id": _oid("MAINT", 1), "name": "DEMO Maintenance Pro", "category": "maintenance", "city": "Yaoundé"},
        {"id": _oid("MOVER", 1), "name": "DEMO Déménagement Express", "category": "moving", "city": "Yaoundé"},
        {"id": _oid("FINANCE", 1), "name": "DEMO Conseil Finance", "category": "financial", "city": "Yaoundé"},
        {"id": _oid("PROPERTYMGMT", 1), "name": "DEMO Gestion Immobilière", "category": "property_management", "city": "Yaoundé"},
        {"id": _oid("ASSURANCE", 1), "name": "DEMO Assurances", "category": "insurance", "city": "Douala"},
    ]

    # --- Properties (117, keeping existing algorithm) ---
    props = []
    for i, district in enumerate(_NEIGHBORHOODS_YDE):
        max_props = 6 if i < 5 else 3
        for j in range(max_props):
            idx = i * max_props + j + 1
            if idx > 50: break
            ptype = "APARTMENT" if j % 3 == 0 else "HOUSE" if j % 3 == 1 else "STUDIO"
            price = 100_000 + (hash(f"yde-{district}-{j}") % 400_000)
            if district == "Mvan" and j < 2: price = 180_000 + j * 40000
            elif district == "Mvan" and j == 2: price = 300_000; ptype = "APARTMENT"
            elif district == "Mvan" and j == 3: price = 220_000
            elif district == "Mvan" and j == 4: price = 350_000; ptype = "APARTMENT"
            elif district == "Mvan" and j == 5: price = 200_000
            name = _NAMES[(idx * 7) % len(_NAMES)]
            status = "active" if idx % 10 != 0 else "suspended"
            if district == "Mvan" and j == 4: status = "suspended"
            available = True if idx % 5 != 0 else False
            if district == "Mvan" and j == 5: available = False
            props.append({
                "id": _bid("YDE", idx), "city": "Yaoundé", "district": district,
                "property_type": ptype, "price": price, "currency": "XAF",
                "bedrooms": 2 if district == "Mvan" and j in (0, 3, 5) else (idx % 4) + 1,
                "title": _PROPERTY_TEMPLATES[ptype][0].format(name=name),
                "status": status, "owner_id": _uid("OWNER", (idx % 5) + 1),
                "features": ["parking"] if idx % 2 == 0 else [], "available": available,
            })

    for i, district in enumerate(_NEIGHBORHOODS_DLA):
        for j in range(3):
            idx = i * 3 + j + 1
            if idx > 25: break
            ptype = "APARTMENT" if j < 2 else "HOUSE"
            price = 200_000 + (hash(f"dla-{district}-{j}") % 400_000)
            name = _NAMES[(idx * 13) % len(_NAMES)]
            props.append({"id": _bid("DLA", idx), "city": "Douala", "district": district, "property_type": ptype, "price": price, "currency": "XAF", "bedrooms": (idx % 4) + 1, "title": _PROPERTY_TEMPLATES[ptype][0].format(name=name), "status": "active", "owner_id": _uid("OWNER", (idx % 5) + 1), "features": [], "available": True})

    land_locations = [("Yaoundé","Nkoabang",15_000_000),("Yaoundé","Odza",12_000_000),("Yaoundé","Mvan",8_000_000),("Douala","Logbaba",10_000_000),("Bafoussam","Djeleng",5_000_000),("Kribi","Lobe",7_000_000),("Yaoundé","Nkolbisson",6_000_000)]
    for li, (lc, ld, lp) in enumerate(land_locations):
        props.append({"id": _bid("LND", li+1), "city": lc, "district": ld, "property_type": "LAND", "price": lp, "currency": "XAF", "bedrooms": 0, "title": f"Terrain à {ld}, {lc}", "status": "active" if li%3!=0 else "suspended", "owner_id": _uid("OWNER", (li%5)+1), "features": ["borné"] if li%2==0 else [], "available": li%4!=0, "surface_m2": 500+li*200})

    for ci, (city, hoods) in enumerate([("Bafoussam",_NEIGHBORHOODS_BFS),("Kribi",_NEIGHBORHOODS_KRI),("Limbé",_NEIGHBORHOODS_LIM)]):
        for di, district in enumerate(hoods):
            for j in range(2):
                idx = di*2+j+1
                if idx > 8: break
                ptype = "HOUSE" if j==0 else "APARTMENT"
                price = 100_000 + (hash(f"{city}-{district}") % 250_000)
                name = _NAMES[(idx*17)%len(_NAMES)]
                props.append({"id": _bid(city[:3].upper(), idx), "city": city, "district": district, "property_type": ptype, "price": price, "currency": "XAF", "bedrooms": (idx%3)+1, "title": _PROPERTY_TEMPLATES[ptype][0].format(name=name), "status": "active" if idx%5!=0 else "suspended", "owner_id": _uid("OWNER", (idx%5)+1), "features": [], "available": idx%4!=0})

    # --- Services (18) ---
    services = [
        {"id": _sid(1), "name": "Consultation architecturale initiale", "provider_id": _pid("ARCH",1), "category": "architecture", "price": 150000},
        {"id": _sid(2), "name": "Plan de construction", "provider_id": _pid("ARCH",1), "category": "architecture", "price": 500000},
        {"id": _sid(3), "name": "Suivi de chantier", "provider_id": _pid("ARCH",1), "category": "architecture", "price": 800000},
        {"id": _sid(4), "name": "Vérification de titre foncier", "provider_id": _pid("NOTARY",1), "category": "notary", "price": 200000},
        {"id": _sid(5), "name": "Acte de vente", "provider_id": _pid("NOTARY",1), "category": "notary", "price": 350000},
        {"id": _sid(6), "name": "Bornage de terrain", "provider_id": _pid("SURVEYOR",1), "category": "surveying", "price": 250000},
        {"id": _sid(7), "name": "Levé topographique", "provider_id": _pid("SURVEYOR",1), "category": "surveying", "price": 400000},
        {"id": _sid(8), "name": "Conseil juridique immobilier", "provider_id": _pid("LAWYER",1), "category": "legal", "price": 100000},
        {"id": _sid(9), "name": "Gros œuvre construction", "provider_id": _pid("BUILDER",1), "category": "construction", "price": 2500000},
        {"id": _sid(10), "name": "Installation électrique complète", "provider_id": _pid("ELECTRICIAN",1), "category": "electrical", "price": 150000},
        {"id": _sid(11), "name": "Plomberie complète", "provider_id": _pid("PLUMBER",1), "category": "plumbing", "price": 100000},
        {"id": _sid(12), "name": "Déménagement local", "provider_id": _pid("MOVER",1), "category": "moving", "price": 200000},
        {"id": _sid(13), "name": "Consultation crédit immobilier", "provider_id": _pid("FINANCE",1), "category": "financial", "price": 50000},
        {"id": _sid(14), "name": "Assurance habitation", "provider_id": _pid("INSURANCE",1), "category": "insurance", "price": 75000},
        {"id": _sid(15), "name": "Maintenance urgente", "provider_id": _pid("MAINT",1), "category": "maintenance", "price": 50000},
        {"id": _sid(16), "name": "Nettoyage professionnel", "provider_id": _pid("CLEANER",1), "category": "cleaning", "price": 35000},
        {"id": _sid(17), "name": "Photographie immobilière", "provider_id": _pid("PHOTO",1), "category": "photography", "price": 80000},
        {"id": _sid(18), "name": "Recherche et mise en relation", "provider_id": _uid("AGENT",1), "category": "real_estate", "price": 0},
    ]

    # --- Scenarios (12) ---
    scenarios = [
        {"scenario_id": _scid(1), "title": "Location appartement 2 chambres à Mvan", "category": "property_rental", "status": "READY", "personas": [_uid("CLIENT",1),_uid("OWNER",1),_uid("AGENT",1)], "properties": [_bid("YDE",1),_bid("YDE",2),_bid("YDE",3)], "services": [_sid(18)]},
        {"scenario_id": _scid(2), "title": "Location studio à Mvan", "category": "property_rental", "status": "READY", "personas": [_uid("CLIENT",2),_uid("OWNER",2)], "properties": [_bid("YDE",5)], "services": []},
        {"scenario_id": _scid(3), "title": "Achat maison à Bastos", "category": "property_purchase", "status": "READY", "personas": [_uid("CLIENT",3),_uid("OWNER",3),_pid("NOTARY",1)], "properties": [_bid("YDE",4)], "services": [_sid(4),_sid(5)]},
        {"scenario_id": _scid(4), "title": "Achat terrain Nkoabang avec géomètre", "category": "land_purchase", "status": "READY", "personas": [_uid("CLIENT",1),_uid("OWNER",4),_pid("SURVEYOR",1)], "properties": [p["id"] for p in props if p["property_type"]=="LAND"][:2], "services": [_sid(6),_sid(7),_sid(8)]},
        {"scenario_id": _scid(5), "title": "Recherche architecte pour construction", "category": "professional_search", "status": "READY", "personas": [_uid("CLIENT",2),_pid("ARCH",1)], "properties": [], "services": [_sid(1),_sid(2),_sid(3)]},
        {"scenario_id": _scid(6), "title": "Consultation notariale", "category": "professional_search", "status": "READY", "personas": [_uid("CLIENT",4),_pid("NOTARY",1)], "properties": [], "services": [_sid(4),_sid(5)]},
        {"scenario_id": _scid(7), "title": "Travaux rénovation maison", "category": "renovation", "status": "READY", "personas": [_uid("CLIENT",5),_pid("BUILDER",1),_pid("ELECTRICIAN",1)], "properties": [_bid("YDE",10)], "services": [_sid(9),_sid(10)]},
        {"scenario_id": _scid(8), "title": "Maintenance urgence plomberie", "category": "maintenance", "status": "READY", "personas": [_uid("CLIENT",6),_pid("PLUMBER",1)], "properties": [], "services": [_sid(11),_sid(15)]},
        {"scenario_id": _scid(9), "title": "Recherche géomètre bornage terrain", "category": "professional_search", "status": "READY", "personas": [_uid("CLIENT",3),_pid("SURVEYOR",1)], "properties": [], "services": [_sid(6)]},
        {"scenario_id": _scid(10), "title": "Déménagement vers nouveau logement", "category": "moving", "status": "READY", "personas": [_uid("CLIENT",7),_pid("MOVER",1)], "properties": [], "services": [_sid(12)]},
        {"scenario_id": _scid(11), "title": "Financement acquisition immobilière", "category": "financial", "status": "READY", "personas": [_uid("CLIENT",1),_pid("FINANCE",1)], "properties": [], "services": [_sid(13)]},
        {"scenario_id": _scid(12), "title": "Location gestion locative", "category": "property_management", "status": "READY", "personas": [_uid("OWNER",1),_uid("AGENT",1)], "properties": [_bid("YDE",7)], "services": [_sid(18)]},
    ]

    # --- Negative cases (8) ---
    neg_cases = [
        {"id": "NEG-NO-MATCH-001", "description": "Aucun bien ne correspond aux critères (budget trop bas)", "scenario": _scid(1)},
        {"id": "NEG-NO-CONSENT-001", "description": "Propriétaire sans consentement pour mise en relation", "user": _uid("OWNER", 5)},
        {"id": "NEG-SUSPENDED-001", "description": "Bien suspendu sélectionné", "property": [p["id"] for p in props if p.get("status")=="suspended"][:1]},
        {"id": "NEG-DUPLICATE-CONNECTION-001", "description": "Double tentative de connexion sur le même match"},
        {"id": "NEG-BLOCKED-USER-001", "description": "Utilisateur suspendu tente une recherche", "user": _uid("AGENT", 3)},
        {"id": "NEG-UNAVAILABLE-PRO-001", "description": "Professionnel indisponible pour une mission", "professional": _pid("CLEANER", 1)},
        {"id": "NEG-NO-DOCUMENT-001", "description": "Document manquant pour finaliser une transaction"},
        {"id": "NEG-EXPIRED-PROPERTY-001", "description": "Bien expiré ou retiré pendant la conversation"},
    ]

    return {
        "dataset": {"id": "LAWIM_DEMO_WORLD_V1", "version": "1.0.0", "status": "IN_PROGRESS", "description": "Univers de démonstration complet LAWIM — 25 users, 16 pros, 12 orgs, 117 biens, 18 services, 12 scénarios, 8 cas négatifs.", "created_at": "2026-07-23", "updated_at": "2026-07-23"},
        "coverage": {
            "roles": ["client", "owner", "agent", "service_provider", "commercial", "admin"],
            "professions": ["architect", "notary", "surveyor", "lawyer", "builder", "electrician", "plumber", "real_estate_agent", "mover", "financial_advisor", "insurance_agent", "maintenance_tech", "cleaner", "photographer"],
            "property_types": ["APARTMENT", "HOUSE", "STUDIO", "LAND"],
            "cities": ["Yaoundé", "Douala", "Bafoussam", "Kribi", "Limbé"],
        },
        "cities": [
            {"id": "CITY-YDE-001", "name": "Yaoundé", "districts": _NEIGHBORHOODS_YDE},
            {"id": "CITY-DLA-001", "name": "Douala", "districts": _NEIGHBORHOODS_DLA},
            {"id": "CITY-BFS-001", "name": "Bafoussam", "districts": _NEIGHBORHOODS_BFS},
            {"id": "CITY-KRI-001", "name": "Kribi", "districts": _NEIGHBORHOODS_KRI},
            {"id": "CITY-LIM-001", "name": "Limbé", "districts": _NEIGHBORHOODS_LIM},
        ],
        "users": users,
        "professional_profiles": profs,
        "organizations": orgs,
        "services": services,
        "properties": props,
        "negative_cases": neg_cases,
        "scenarios": scenarios,
    }


_PROPERTY_TEMPLATES = {
    "APARTMENT": ["Résidence {name}", "Appartement {name}"],
    "HOUSE": ["Maison {name}", "Villa {name}"],
    "STUDIO": ["Studio {name}"],
    "LAND": ["Terrain {name}"],
}

if __name__ == "__main__":
    data = build()
    path = "demo/reference/LAWIM-DEMO-WORLD-REFERENCE.yaml"
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    secs = {k: len(v) for k, v in data.items() if isinstance(v, list)}
    props = data.get("properties", [])
    cities = set(p.get("city","") for p in props)
    ptypes = set(p.get("property_type","") for p in props)
    print(f"Generated {path}")
    for s, c in secs.items():
        print(f"  {s}: {c}")
    print(f"  cities: {len(cities)} | types: {len(ptypes)}")
