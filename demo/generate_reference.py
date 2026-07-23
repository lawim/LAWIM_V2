#!/usr/bin/env python3
"""Generate complete LAWIM Demo World V1 reference YAML."""

from __future__ import annotations

import yaml


def _bid(c: str, n: int) -> str:
    return f"DEMO-PROPERTY-{c.upper()}-{n:03d}"

def _uid(role: str, n: int) -> str:
    return f"DEMO-USER-{role.upper()}-{n:03d}"

def _sid(n: int) -> str:
    return f"DEMO-SERVICE-{n:03d}"

def _docid(n: int) -> str:
    return f"DEMO-DOCUMENT-{n:03d}"

_NEIGHBORHOODS_YDE = ["Mvan", "Bastos", "Odza", "Nlongkak", "Tsinga", "Ngousso", "Essos", "Mendong", "Biyem-Assi", "Nkoabang", "Emana", "Etoug-Ebe", "Ekounou", "Messassi", "Nkolbisson", "Nkolfoulou"]
_NEIGHBORHOODS_DLA = ["Akwa", "Bonanjo", "Bonapriso", "Deido", "Makepe", "Bonamoussadi", "Logbaba", "Bassa", "Nylon"]
_NEIGHBORHOODS_BFS = ["Djeleng", "Kouogouo", "Tamdja", "Banengo"]
_NEIGHBORHOODS_KRI = ["Mpangou", "Bebamboue", "Lobe"]
_NEIGHBORHOODS_LIM = ["Bota", "Mile 2", "Mile 4", "Mokunda"]

_PROPERTY_TYPES = ["APARTMENT", "HOUSE", "STUDIO", "VILLA", "LAND", "COMMERCIAL", "ROOM"]
_PROPERTY_TEMPLATES = {
    "APARTMENT": ["Résidence {name}", "Appartement {name}", "Immeuble {name}"],
    "HOUSE": ["Villa {name}", "Maison {name}", "Pavillon {name}"],
    "STUDIO": ["Studio {name}", "Meublé {name}"],
    "VILLA": ["Villa {name}", "Propriété {name}"],
    "LAND": ["Terrain {name}", "Parcelle {name}"],
    "COMMERCIAL": ["Local commercial {name}", "Boutique {name}"],
    "ROOM": ["Chambre {name}", "Chambre meublée {name}"],
}
_NAMES = ["des Acacias", "du Lac", "des Cocotiers", "Soleil", "Bleu", "Vert", "du Centre", "Bellevue", "des Fleurs", "du Paradis", "Royal", "Princier", "du Stade", "de la Gare", "du Marché", "des Eaux", "Diana", "Beau Séjour", "les Manguiers", "Saint Michel"]

def build():
    props = []
    # Yaoundé ~50 properties
    for i, district in enumerate(_NEIGHBORHOODS_YDE):
        for j in range(3):
            idx = i * 3 + j + 1
            if idx > 50: break
            ptype = "APARTMENT" if j % 3 == 0 else "HOUSE" if j % 3 == 1 else "STUDIO"
            price = 150_000 + (hash(district) % 350_000)
            name = _NAMES[(idx * 7) % len(_NAMES)]
            props.append({
                "id": _bid("YDE", idx), "city": "Yaoundé", "district": district,
                "property_type": ptype, "price": price, "currency": "XAF",
                "bedrooms": (idx % 4) + 1, "title": _PROPERTY_TEMPLATES[ptype][0].format(name=name),
                "status": "active", "owner_id": _uid("OWNER", (idx % 4) + 1),
                "features": ["parking"] if idx % 2 == 0 else [], "available": True,
            })
    # Douala ~25 properties
    for i, district in enumerate(_NEIGHBORHOODS_DLA):
        for j in range(3):
            idx = i * 3 + j + 1
            if idx > 25: break
            ptype = "APARTMENT" if j < 2 else "HOUSE"
            price = 200_000 + (hash(f"dla-{district}-{j}") % 400_000)
            name = _NAMES[(idx * 13) % len(_NAMES)]
            props.append({
                "id": _bid("DLA", idx), "city": "Douala", "district": district,
                "property_type": ptype, "price": price, "currency": "XAF",
                "bedrooms": (idx % 4) + 1, "title": _PROPERTY_TEMPLATES[ptype][0].format(name=name),
                "status": "active", "owner_id": _uid("OWNER", (idx % 3) + 1),
                "features": [], "available": True,
            })
    # Other cities ~25 properties
    other_cities = [("Bafoussam", _NEIGHBORHOODS_BFS), ("Kribi", _NEIGHBORHOODS_KRI), ("Limbé", _NEIGHBORHOODS_LIM)]
    for city, hoods in other_cities:
        for i, district in enumerate(hoods):
            for j in range(2):
                idx = i * 2 + j + 1
                if idx > 8: break
                ptype = "HOUSE" if j == 0 else "APARTMENT"
                price = 100_000 + (hash(f"{city}-{district}") % 250_000)
                name = _NAMES[(idx * 17) % len(_NAMES)]
                props.append({
                    "id": _bid(city[:3].upper(), idx), "city": city, "district": district,
                    "property_type": ptype, "price": price, "currency": "XAF",
                    "bedrooms": (idx % 3) + 1, "title": _PROPERTY_TEMPLATES[ptype][0].format(name=name),
                    "status": "active" if idx % 5 != 0 else "suspended",
                    "owner_id": _uid("OWNER", (idx % 3) + 1), "features": [], "available": idx % 4 != 0,
                })

    services = [
        {"id": _sid(1), "name": "Consultation architecturale initiale", "provider_id": "DEMO-PRO-ARCH-001", "price": 150000},
        {"id": _sid(2), "name": "Plan de construction", "provider_id": "DEMO-PRO-ARCH-001", "price": 500000},
        {"id": _sid(3), "name": "Suivi de chantier", "provider_id": "DEMO-PRO-ARCH-001", "price": 800000},
        {"id": _sid(4), "name": "Vérification de titre foncier", "provider_id": "DEMO-PRO-NOTARY-001", "price": 200000},
        {"id": _sid(5), "name": "Acte de vente", "provider_id": "DEMO-PRO-NOTARY-001", "price": 350000},
        {"id": _sid(6), "name": "Bornage de terrain", "provider_id": "DEMO-PRO-SURVEYOR-001", "price": 250000},
        {"id": _sid(7), "name": "Levé topographique", "provider_id": "DEMO-PRO-SURVEYOR-001", "price": 400000},
        {"id": _sid(8), "name": "Conseil juridique", "provider_id": "DEMO-PRO-LAWYER-001", "price": 100000},
        {"id": _sid(9), "name": "Gros œuvre", "provider_id": "DEMO-PRO-BUILDER-001", "price": 2500000},
        {"id": _sid(10), "name": "Installation électrique", "provider_id": "DEMO-PRO-ELECTRICIAN-001", "price": 150000},
        {"id": _sid(11), "name": "Plomberie", "provider_id": "DEMO-PRO-PLUMBER-001", "price": 100000},
    ]

    scenarios = [
        {"scenario_id": "SCENARIO-RENT-MVAN-001", "title": "Location appartement 2 chambres à Mvan", "category": "property_rental", "status": "READY",
         "personas": ["DEMO-USER-CLIENT-001", "DEMO-USER-OWNER-001", "DEMO-USER-AGENT-001"],
         "properties": [_bid("YDE", 1), _bid("YDE", 2), _bid("YDE", 3)], "services": [], "start_messages": ["Bonjour, je cherche un appartement à louer à Yaoundé.", "À Mvan.", "Mon budget maximal est de 200 000 F par mois.", "Je veux deux chambres.", "Finalement, mon budget maximal est de 250 000 F."]},
        {"scenario_id": "SCENARIO-RENT-MVAN-002", "title": "Location studio à Mvan", "category": "property_rental", "status": "READY",
         "personas": ["DEMO-USER-CLIENT-002", "DEMO-USER-OWNER-002"], "properties": [_bid("YDE", 5)], "services": []},
        {"scenario_id": "SCENARIO-BUY-BASTOS-001", "title": "Achat maison à Bastos", "category": "property_purchase", "status": "READY",
         "personas": ["DEMO-USER-CLIENT-003", "DEMO-USER-OWNER-003", "DEMO-PRO-NOTARY-001"], "properties": [_bid("YDE", 4)], "services": [_sid(4), _sid(5)]},
        {"scenario_id": "SCENARIO-LAND-NKOABANG-001", "title": "Achat terrain à Nkoabang", "category": "land_purchase", "status": "READY",
         "personas": ["DEMO-USER-CLIENT-001", "DEMO-USER-OWNER-004", "DEMO-PRO-SURVEYOR-001"], "properties": [p["id"] for p in props if p["property_type"] == "LAND"][:2], "services": [_sid(6), _sid(7)]},
        {"scenario_id": "SCENARIO-ARCHITECT-YAOUNDE-001", "title": "Recherche d'architecte à Yaoundé", "category": "professional_search", "status": "READY",
         "personas": ["DEMO-USER-CLIENT-002", "DEMO-PRO-ARCH-001"], "properties": [], "services": [_sid(1), _sid(2), _sid(3)]},
        {"scenario_id": "SCENARIO-NOTARY-YAOUNDE-001", "title": "Consultation notariale", "category": "professional_search", "status": "READY",
         "personas": ["DEMO-USER-CLIENT-004", "DEMO-PRO-NOTARY-001"], "properties": [], "services": [_sid(4), _sid(5)]},
    ]

    return {
        "dataset": {"id": "LAWIM_DEMO_WORLD_V1", "version": "1.0.0", "status": "IN_PROGRESS", "description": "Univers de démonstration complet de LAWIM.", "created_at": "2026-07-23", "updated_at": "2026-07-23"},
        "coverage": {
            "roles": ["client", "owner", "agent", "admin", "support", "commercial", "property_manager"],
            "professions": ["architect", "notary", "surveyor", "lawyer", "builder", "electrician", "plumber"],
            "property_types": _PROPERTY_TYPES,
            "transaction_types": ["RENT", "BUY", "SELL", "CONSTRUCT"],
            "cities": ["Yaoundé", "Douala", "Bafoussam", "Kribi", "Limbé"],
            "scenarios": [s["scenario_id"] for s in scenarios],
        },
        "cities": [
            {"id": "CITY-YDE-001", "name": "Yaoundé", "region": "Centre", "districts": _NEIGHBORHOODS_YDE},
            {"id": "CITY-DLA-001", "name": "Douala", "region": "Littoral", "districts": _NEIGHBORHOODS_DLA},
            {"id": "CITY-BFS-001", "name": "Bafoussam", "region": "Ouest", "districts": _NEIGHBORHOODS_BFS},
            {"id": "CITY-KRI-001", "name": "Kribi", "region": "Sud", "districts": _NEIGHBORHOODS_KRI},
            {"id": "CITY-LIM-001", "name": "Limbé", "region": "Sud-Ouest", "districts": _NEIGHBORHOODS_LIM},
        ],
        "users": [
            {"id": _uid("CLIENT", 1), "full_name": "Jean Dupont", "role": "client", "city": "Yaoundé", "preferred_language": "fr", "profile_status": "active", "verification_status": "verified", "consent_status": "granted"},
            {"id": _uid("CLIENT", 2), "full_name": "Alice Mbarga", "role": "client", "city": "Douala", "preferred_language": "fr", "profile_status": "active", "verification_status": "verified", "consent_status": "granted"},
            {"id": _uid("CLIENT", 3), "full_name": "Pierre Kamga", "role": "client", "city": "Yaoundé", "preferred_language": "fr", "profile_status": "active", "verification_status": "unverified", "consent_status": "pending"},
            {"id": _uid("CLIENT", 4), "full_name": "Marie Ngo Bissa", "role": "client", "city": "Bafoussam", "preferred_language": "fr", "profile_status": "active", "verification_status": "verified", "consent_status": "granted"},
            {"id": _uid("CLIENT", 5), "full_name": "Paul Etoundi", "role": "client", "city": "Douala", "preferred_language": "fr", "profile_status": "active", "verification_status": "unverified", "consent_status": "denied"},
            {"id": _uid("OWNER", 1), "full_name": "Thomas Mvogo", "role": "owner", "city": "Yaoundé", "preferred_language": "fr", "profile_status": "active", "verification_status": "verified", "consent_status": "granted", "has_multiple_properties": True},
            {"id": _uid("OWNER", 2), "full_name": "Christine Eyanga", "role": "owner", "city": "Yaoundé", "preferred_language": "fr", "profile_status": "active", "verification_status": "verified", "consent_status": "granted"},
            {"id": _uid("OWNER", 3), "full_name": "Joseph Obama", "role": "owner", "city": "Douala", "preferred_language": "fr", "profile_status": "inactive", "verification_status": "unverified", "consent_status": "pending"},
            {"id": _uid("OWNER", 4), "full_name": "Suzanne Mbah", "role": "owner", "city": "Yaoundé", "preferred_language": "fr", "profile_status": "active", "verification_status": "verified", "consent_status": "granted"},
            {"id": _uid("AGENT", 1), "full_name": "Luc Tchinda", "role": "agent", "city": "Yaoundé", "preferred_language": "fr", "profile_status": "active", "verification_status": "verified", "organization_id": "DEMO-ORG-AGENCY-001"},
            {"id": _uid("AGENT", 2), "full_name": "Rosalie Nkwi", "role": "agent", "city": "Yaoundé", "preferred_language": "fr", "profile_status": "active", "verification_status": "verified", "organization_id": "DEMO-ORG-AGENCY-001"},
            {"id": _uid("AGENT", 3), "full_name": "Emmanuel Simo", "role": "agent", "city": "Douala", "preferred_language": "fr", "profile_status": "suspended", "verification_status": "unverified", "organization_id": "DEMO-ORG-AGENCY-002"},
            {"id": _uid("COMMERCIAL", 1), "full_name": "Fabrice Noah", "role": "commercial", "city": "Yaoundé", "preferred_language": "fr", "profile_status": "active", "verification_status": "verified"},
        ],
        "organizations": [
            {"id": "DEMO-ORG-AGENCY-001", "name": "DEMO Agence Centrale", "category": "real_estate_agency", "city": "Yaoundé", "district": "Mvan", "status": "active"},
            {"id": "DEMO-ORG-AGENCY-002", "name": "DEMO Immo Services", "category": "real_estate_agency", "city": "Douala", "district": "Bonanjo", "status": "active"},
            {"id": "DEMO-ORG-NOTARY-001", "name": "DEMO Étude Notariale", "category": "notary", "city": "Yaoundé", "district": "Bastos", "status": "active"},
            {"id": "DEMO-ORG-ARCHI-001", "name": "DEMO Architecture Studio", "category": "architecture", "city": "Yaoundé", "district": "Nlongkak", "status": "active"},
            {"id": "DEMO-ORG-LEGAL-001", "name": "DEMO Cabinet Juridique", "category": "legal", "city": "Yaoundé", "district": "Bastos", "status": "active"},
            {"id": "DEMO-ORG-CONSTRUCT-001", "name": "DEMO Bâtir Plus", "category": "construction", "city": "Yaoundé", "district": "Mendong", "status": "active"},
            {"id": "DEMO-ORG-SURVEY-001", "name": "DEMO Géomètre Expert", "category": "surveying", "city": "Yaoundé", "district": "Odza", "status": "active"},
            {"id": "DEMO-ORG-MAINT-001", "name": "DEMO Maintenance Pro", "category": "maintenance", "city": "Yaoundé", "district": "Essos", "status": "active"},
            {"id": "DEMO-ORG-MOVER-001", "name": "DEMO Déménagement Express", "category": "moving", "city": "Yaoundé", "district": "Nkoabang", "status": "active"},
            {"id": "DEMO-ORG-FINANCE-001", "name": "DEMO Conseil Finance", "category": "financial", "city": "Yaoundé", "district": "Bastos", "status": "active"},
        ],
        "professional_profiles": [
            {"id": "DEMO-PRO-ARCH-001", "organization_id": "DEMO-ORG-ARCHI-001", "profession": "architect", "title": "Architecte principal", "years_experience": 12, "verified": True, "available": True},
            {"id": "DEMO-PRO-NOTARY-001", "organization_id": "DEMO-ORG-NOTARY-001", "profession": "notary", "title": "Notaire", "years_experience": 20, "verified": True, "available": True},
            {"id": "DEMO-PRO-SURVEYOR-001", "organization_id": "DEMO-ORG-SURVEY-001", "profession": "surveyor", "title": "Géomètre expert", "years_experience": 15, "verified": True, "available": True},
            {"id": "DEMO-PRO-LAWYER-001", "organization_id": "DEMO-ORG-LEGAL-001", "profession": "lawyer", "title": "Avocat en immobilier", "years_experience": 18, "verified": True, "available": True},
            {"id": "DEMO-PRO-BUILDER-001", "organization_id": "DEMO-ORG-CONSTRUCT-001", "profession": "builder", "title": "Chef de chantier", "years_experience": 22, "verified": True, "available": True},
            {"id": "DEMO-PRO-ELECTRICIAN-001", "organization_id": "DEMO-ORG-CONSTRUCT-001", "profession": "electrician", "title": "Électricien", "years_experience": 8, "verified": True, "available": True},
            {"id": "DEMO-PRO-PLUMBER-001", "organization_id": "DEMO-ORG-MAINT-001", "profession": "plumber", "title": "Plombier", "years_experience": 10, "verified": True, "available": True},
        ],
        "services": services,
        "properties": props,
        "negative_cases": [
            {"id": "NEG-NO-MATCH-001", "description": "Aucun bien ne correspond aux critères (budget trop bas)", "scenario": "SCENARIO-RENT-MVAN-001"},
            {"id": "NEG-NO-CONSENT-001", "description": "Propriétaire sans consentement pour mise en relation", "user": _uid("OWNER", 3)},
            {"id": "NEG-SUSPENDED-001", "description": "Bien suspendu sélectionné par erreur", "property": [p["id"] for p in props if p.get("status") == "suspended"][:1]},
            {"id": "NEG-DUPLICATE-CONNECTION-001", "description": "Double tentative de connexion sur le même match"},
            {"id": "NEG-BLOCKED-USER-001", "description": "Utilisateur bloqué tente une recherche", "user": _uid("AGENT", 3)},
        ],
        "scenarios": scenarios,
    }


if __name__ == "__main__":
    data = build()
    path = "demo/reference/LAWIM-DEMO-WORLD-REFERENCE.yaml"
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    cnt = sum(len(v) for v in data.values() if isinstance(v, list))
    print(f"Generated {path} — {cnt} entities across all sections")
    print(f"  Properties: {len(data.get('properties', []))}")
    print(f"  Users: {len(data.get('users', []))}")
    print(f"  Organizations: {len(data.get('organizations', []))}")
    print(f"  Professionals: {len(data.get('professional_profiles', []))}")
    print(f"  Services: {len(data.get('services', []))}")
    print(f"  Scenarios: {len(data.get('scenarios', []))}")
    print(f"  Negative cases: {len(data.get('negative_cases', []))}")
