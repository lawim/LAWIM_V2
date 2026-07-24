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
    if role in ("OWNER", "AGENT", "CLIENT"):
        return f"DEMO-USER-{role}-AUTH-{n:03d}"
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

def _mid(n):
    return f"DEMO-MEDIA-{n:03d}"

def _pnid(prefix, n):
    return f"DEMO-PRO-{prefix.upper()}-{n:03d}"

def build():
    users = []
    auth_users = []  # auth credentials metadata
    team_members = []

    # --- Auth/Noauth pairs for each category ---
    auth_categories = [
        # (prefix, role, name_auth, name_noauth, city, org)
        # Clients
        ("CLIENT", "client", "Jean Dupont", "Client sans accès", "Yaoundé", None),
        ("CLIENT", "client", "Alice Mbarga", "Alice (noauth)", "Douala", None),
        ("CLIENT", "client", "Pierre Kamga", "Pierre (noauth)", "Yaoundé", None),
        ("CLIENT", "client", "Marie Ngo Bissa", "Marie (noauth)", "Bafoussam", None),
        ("CLIENT", "client", "Paul Etoundi", "Paul (noauth)", "Douala", None),
        ("CLIENT", "client", "Sarah Nkwi", "Sarah (noauth)", "Yaoundé", None),
        ("CLIENT", "client", "Robert Tchinda", "Robert (noauth)", "Yaoundé", None),
        ("CLIENT", "client", "Esther Mvogo", "Esther (noauth)", "Bafoussam", None),
        # Owners
        ("OWNER", "owner", "Thomas Mvogo", "Thomas (noauth)", "Yaoundé", None),
        ("OWNER", "owner", "Christine Eyanga", "Christine (noauth)", "Yaoundé", None),
        ("OWNER", "owner", "Joseph Obama", "Joseph (noauth)", "Douala", None),
        ("OWNER", "owner", "Suzanne Mbah", "Suzanne (noauth)", "Yaoundé", None),
        # Agents
        ("AGENT", "agent", "Luc Tchinda", "Luc (noauth)", "Yaoundé", "DEMO-ORG-AGENCY-001"),
        ("AGENT", "agent", "Rosalie Nkwi", "Rosalie (noauth)", "Yaoundé", "DEMO-ORG-AGENCY-001"),
        ("AGENT", "agent", "Emmanuel Simo", "Emmanuel (noauth)", "Douala", "DEMO-ORG-AGENCY-002"),
    ]

    auth_idx = {"CLIENT": 0, "OWNER": 0, "AGENT": 0}
    for prefix, role, name_auth, name_noauth, city, org in auth_categories:
        auth_idx[prefix] += 1
        ref = auth_idx[prefix]
        uid_auth = f"DEMO-USER-{prefix}-AUTH-{ref:03d}"
        uid_noauth = f"DEMO-USER-{prefix}-NOAUTH-{ref:03d}"
        # Auth user
        users.append({"id": uid_auth, "full_name": name_auth, "role": role, "city": city, "organization_id": org, "profile_status": "active", "verification_status": "verified", "consent_status": "granted", "can_login": True, "preferred_language": "fr", "is_demo_data": True, "demo_dataset_id": "LAWIM_DEMO_WORLD_V1"})
        auth_users.append({"demo_reference_id": uid_auth, "full_name": name_auth, "role": role, "can_login": True, "username": f"{prefix.lower()}.auth.{ref:03d}", "email": f"{prefix.lower()}.auth.{ref:03d}@demo.lawim.local", "phone_alias": f"+2376000{ref:04d}", "password_source": "generated", "organization_id": org})
        # Noauth user
        users.append({"id": uid_noauth, "full_name": name_noauth, "role": role, "city": city, "organization_id": org, "profile_status": "inactive", "verification_status": "unverified", "consent_status": "pending", "can_login": False, "is_demo_data": True, "demo_dataset_id": "LAWIM_DEMO_WORLD_V1"})

    # Professional users (service_provider role)
    pro_auth_names = [("ARCH", "Pierre Atangana"), ("ARCH", "Marie Ekwé"), ("NOTARY", "Jean Meka"), ("SURVEYOR", "Chantal Ngo")]
    for idx, (prefix, name) in enumerate(pro_auth_names, 1):
        uid = f"DEMO-USER-PRO-{prefix}-AUTH-{idx:03d}"
        users.append({"id": uid, "full_name": name, "role": "service_provider", "city": "Yaoundé", "profile_status": "active", "verification_status": "verified", "can_login": True, "is_demo_data": True, "demo_dataset_id": "LAWIM_DEMO_WORLD_V1"})
        auth_users.append({"demo_reference_id": uid, "full_name": name, "role": "service_provider", "can_login": True, "username": f"pro.{prefix.lower()}.auth.{idx:03d}", "email": f"pro.{prefix.lower()}.auth.{idx:03d}@demo.lawim.local", "phone_alias": f"+237600030{idx:02d}", "password_source": "generated"})
        uid_no = f"DEMO-USER-PRO-{prefix}-NOAUTH-{idx:03d}"
        users.append({"id": uid_no, "full_name": f"{name} (noauth)", "role": "service_provider", "city": "Yaoundé", "profile_status": "inactive", "verification_status": "unverified", "can_login": False, "is_demo_data": True, "demo_dataset_id": "LAWIM_DEMO_WORLD_V1"})

    # Team members
    team_defs = [
        ("SUPERADMIN", "Super Admin LAWIM", "super_admin", ["all"]),
        ("ADMIN", "Admin LAWIM", "admin", ["users:read", "users:write", "properties:read", "properties:write", "settings:read", "settings:write"]),
        ("SUPPORT", "Fabrice Noah", "commercial", ["users:read", "properties:read", "tickets:read", "tickets:write"]),
        ("COMMERCIAL", "Commercial LAWIM", "commercial", ["properties:read", "properties:write", "leads:read", "leads:write"]),
        ("MODERATOR", "Moderateur LAWIM", "moderator", ["properties:read", "properties:moderate", "users:read"]),
        ("AUDITOR", "Auditeur LAWIM", "auditor", ["audit:read", "users:read", "properties:read"]),
        ("FINANCE", "Gestionnaire financier", "finance_manager", ["payments:read", "payments:write", "invoices:read"]),
        ("DOCS", "Gestionnaire documentaire", "doc_manager", ["documents:read", "documents:write", "users:read"]),
        ("PROPERTY", "Gestionnaire des biens", "property_manager", ["properties:read", "properties:write", "media:read", "media:write"]),
        ("VISITS", "Gestionnaire des visites", "visit_manager", ["visits:read", "visits:write", "users:read"]),
    ]
    for prefix, name, role, perms in team_defs:
        uid = f"DEMO-TEAM-{prefix}-AUTH-001"
        users.append({"id": uid, "full_name": name, "role": role, "city": "Yaoundé", "profile_status": "active", "verification_status": "verified", "can_login": True, "is_demo_data": True, "demo_dataset_id": "LAWIM_DEMO_WORLD_V1"})
        auth_users.append({"demo_reference_id": uid, "full_name": name, "role": role, "can_login": True, "username": f"team.{prefix.lower()}.auth.001", "email": f"team.{prefix.lower()}.auth.001@demo.lawim.local", "phone_alias": f"+23760005{team_defs.index((prefix,name,role,perms))+1:02d}", "password_source": "generated", "permissions": perms})
        team_members.append({"id": uid, "full_name": name, "role": role, "permissions": perms, "team": "LAWIM Operations"})
        uid_no = f"DEMO-TEAM-{prefix}-NOAUTH-001"

    # --- Professional Profiles (all with user_id) ---
    pro_data = [
        ("ARCH", 1, "architect", "DEMO-USER-PRO-ARCH-AUTH-001", _oid("ARCHI", 1), 12, True, True),
        ("ARCH", 2, "architect", "DEMO-USER-PRO-ARCH-AUTH-002", _oid("ARCHI", 1), 6, True, True),
        ("NOTARY", 1, "notary", "DEMO-USER-PRO-NOTARY-AUTH-001", _oid("NOTARY", 1), 20, True, True),
        ("SURVEYOR", 1, "surveyor", "DEMO-USER-PRO-SURVEYOR-AUTH-001", _oid("SURVEY", 1), 15, True, True),
        ("LAWYER", 1, "lawyer", "DEMO-USER-PRO-LAWYER-NOAUTH-001", _oid("LEGAL", 1), 18, True, True),
        ("BUILDER", 1, "builder", None, _oid("CONSTRUCT", 1), 22, True, True),
        ("ELECTRICIAN", 1, "electrician", None, _oid("CONSTRUCT", 1), 8, True, True),
        ("PLUMBER", 1, "plumber", None, _oid("MAINT", 1), 10, True, True),
        ("AGENT", 1, "real_estate_agent", "DEMO-USER-AGENT-AUTH-001", _oid("AGENCY", 1), 7, True, True),
        ("AGENT", 2, "real_estate_agent", "DEMO-USER-AGENT-AUTH-002", _oid("AGENCY", 1), 5, True, True),
        ("MOVER", 1, "mover", None, _oid("MOVER", 1), 9, True, True),
        ("FINANCE", 1, "financial_advisor", None, _oid("FINANCE", 1), 11, True, True),
        ("INSURANCE", 1, "insurance_agent", None, _oid("FINANCE", 1), 14, True, True),
        ("MAINT", 1, "maintenance_tech", None, _oid("MAINT", 1), 6, True, True),
        ("CLEANER", 1, "cleaner", None, _oid("MAINT", 1), 4, True, False),
        ("PHOTO", 1, "photographer", None, _oid("AGENCY", 1), 5, True, True),
    ]
    profs = []
    for prefix, n, prof, uid, oid, exp, verified, available in pro_data:
        p_entry = {"id": _pnid(prefix, n), "profession": prof, "user_id": uid, "organization_id": oid, "years_experience": exp, "verified": verified, "available": available, "can_receive_connection": True, "can_receive_appointment": True, "can_receive_message": True}
        if not uid:
            p_entry["can_receive_connection"] = False
        profs.append(p_entry)

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
    idx = 0
    for i, district in enumerate(_NEIGHBORHOODS_YDE):
        max_props = 6 if i < 5 else 3
        for j in range(max_props):
            idx += 1
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
                "status": status, "owner_id": _uid("OWNER", (idx % 4) + 1),
                "features": ["parking"] if idx % 2 == 0 else [], "available": available,
            })

    dla_idx = 0
    for i, district in enumerate(_NEIGHBORHOODS_DLA):
        for j in range(3):
            dla_idx += 1
            if dla_idx > 25: break
            ptype = "APARTMENT" if j < 2 else "HOUSE"
            price = 200_000 + (hash(f"dla-{district}-{j}") % 400_000)
            name = _NAMES[(dla_idx * 13) % len(_NAMES)]
            props.append({"id": _bid("DLA", dla_idx), "city": "Douala", "district": district, "property_type": ptype, "price": price, "currency": "XAF", "bedrooms": (dla_idx % 4) + 1, "title": _PROPERTY_TEMPLATES[ptype][0].format(name=name), "status": "active", "owner_id": _uid("OWNER", (dla_idx % 4) + 1), "features": [], "available": True})

    land_locations = [("Yaoundé","Nkoabang",15_000_000),("Yaoundé","Odza",12_000_000),("Yaoundé","Mvan",8_000_000),("Douala","Logbaba",10_000_000),("Bafoussam","Djeleng",5_000_000),("Kribi","Lobe",7_000_000),("Yaoundé","Nkolbisson",6_000_000)]
    for li, (lc, ld, lp) in enumerate(land_locations):
        props.append({"id": _bid("LND", li+1), "city": lc, "district": ld, "property_type": "LAND", "price": lp, "currency": "XAF", "bedrooms": 0, "title": f"Terrain à {ld}, {lc}", "status": "active" if li%3!=0 else "suspended", "owner_id": _uid("OWNER", (li%4)+1), "features": ["borné"] if li%2==0 else [], "available": li%4!=0, "surface_m2": 500+li*200})

    for ci, (city, hoods) in enumerate([("Bafoussam",_NEIGHBORHOODS_BFS),("Kribi",_NEIGHBORHOODS_KRI),("Limbé",_NEIGHBORHOODS_LIM)]):
        for di, district in enumerate(hoods):
            for j in range(2):
                idx = di*2+j+1
                if idx > 8: break
                ptype = "HOUSE" if j==0 else "APARTMENT"
                price = 100_000 + (hash(f"{city}-{district}") % 250_000)
                name = _NAMES[(idx*17)%len(_NAMES)]
                props.append({"id": _bid(city[:3].upper(), idx), "city": city, "district": district, "property_type": ptype, "price": price, "currency": "XAF", "bedrooms": (idx%3)+1, "title": _PROPERTY_TEMPLATES[ptype][0].format(name=name), "status": "active" if idx%5!=0 else "suspended", "owner_id": _uid("OWNER", (idx%4)+1), "features": [], "available": idx%4!=0})

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
        {"id": "NEG-NO-CONSENT-001", "description": "Propriétaire sans consentement pour mise en relation", "user": _uid("OWNER", 3)},
        {"id": "NEG-SUSPENDED-001", "description": "Bien suspendu sélectionné", "property": [p["id"] for p in props if p.get("status")=="suspended"][:1]},
        {"id": "NEG-DUPLICATE-CONNECTION-001", "description": "Double tentative de connexion sur le même match"},
        {"id": "NEG-BLOCKED-USER-001", "description": "Utilisateur suspendu tente une recherche", "user": _uid("AGENT", 3)},
        {"id": "NEG-UNAVAILABLE-PRO-001", "description": "Professionnel indisponible pour une mission", "professional": _pid("CLEANER", 1)},
        {"id": "NEG-NO-DOCUMENT-001", "description": "Document manquant pour finaliser une transaction"},
        {"id": "NEG-EXPIRED-PROPERTY-001", "description": "Bien expiré ou retiré pendant la conversation"},
    ]

    return {
        "dataset": {"id": "LAWIM_DEMO_WORLD_V1", "version": "1.0.0", "status": "IN_PROGRESS", "description": "Univers de démonstration complet LAWIM — auth/noauth pairs, 14 professions, team members.", "created_at": "2026-07-23", "updated_at": "2026-07-23"},
        "coverage": {
            "roles": ["client", "owner", "agent", "service_provider", "commercial", "admin", "super_admin", "moderator", "auditor", "finance_manager", "doc_manager", "property_manager", "visit_manager"],
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
        "auth_credentials_metadata": auth_users,
        "team_members": team_members,
        "professional_profiles": profs,
        "organizations": orgs,
        "services": services,
        "properties": props,
        "property_media": _build_media(props),
        "documents": _build_documents(),
        "appointments": _build_appointments(),
        "negative_cases": neg_cases,
        "scenarios": scenarios,
    }


def _build_media(props):
    media = []
    mime_types = {"APARTMENT": "image/jpeg", "HOUSE": "image/jpeg", "STUDIO": "image/jpeg", "LAND": "image/png"}
    for i, p in enumerate(props[:45]):
        mid = f"DEMO-MEDIA-{i+1:03d}"
        is_primary = i % 5 == 0
        status = "VALID" if i % 7 != 0 else "UNAVAILABLE"
        media.append({
            "id": mid, "owner_type": "property", "owner_id": p["id"],
            "media_type": "photo", "path": f"demo/media/property-{p['id'].lower()}.jpg",
            "mime_type": mime_types.get(p.get("property_type",""), "image/jpeg"),
            "status": status, "is_primary": is_primary, "position": i % 5 + 1,
            "checksum": f"demo-{mid}-sha256",
        })
    for i, pp_id in enumerate(["DEMO-PRO-ARCH-001","DEMO-PRO-NOTARY-001","DEMO-PRO-BUILDER-001"]):
        media.append({
            "id": f"DEMO-MEDIA-PRO-{i+1:03d}", "owner_type": "professional", "owner_id": pp_id,
            "media_type": "photo", "path": f"demo/media/professional-{pp_id.lower()}.jpg",
            "mime_type": "image/jpeg", "status": "VALID", "is_primary": True, "position": 1,
        })
    for i, oid in enumerate(["DEMO-ORG-AGENCY-001","DEMO-ORG-ARCHI-001","DEMO-ORG-NOTARY-001"]):
        media.append({
            "id": f"DEMO-MEDIA-ORG-LOGO-{i+1:03d}", "owner_type": "organization", "owner_id": oid,
            "media_type": "logo", "path": f"demo/media/logo-{oid.lower()}.png",
            "mime_type": "image/png", "status": "VALID", "is_primary": True, "position": 1,
        })
    return media


def _build_documents():
    docs = []
    doc_templates = [
        ("Titre foncier simulé", "titre_foncier", "valid", "DEMO-PROPERTY-YDE-001"),
        ("Attestation de propriété", "attestation", "valid", "DEMO-PROPERTY-YDE-002"),
        ("Mandat de gestion", "mandat_gestion", "valid", "DEMO-ORG-PROPERTYMGMT-001"),
        ("Mandat de vente", "mandat_vente", "pending", "DEMO-PROPERTY-YDE-004"),
        ("Bail location", "bail", "valid", "DEMO-PROPERTY-YDE-005"),
        ("Pièce d'identité (Jean Dupont)", "id_card", "valid", "DEMO-USER-CLIENT-AUTH-001"),
        ("Plan architectural", "plan", "valid", "DEMO-PRO-ARCH-001"),
        ("Devis construction", "devis", "pending", "DEMO-PRO-BUILDER-001"),
        ("Facture honoraires notaire", "facture", "valid", "DEMO-PRO-NOTARY-001"),
        ("Reçu de loyer", "recu", "valid", "DEMO-PROPERTY-YDE-001"),
        ("Rapport d'expertise", "expertise", "valid", "DEMO-PROPERTY-LND-001"),
        ("Procès-verbal de visite", "pv_visite", "pending", "DEMO-PROPERTY-YDE-007"),
        ("État des lieux", "etat_lieux", "valid", "DEMO-PROPERTY-YDE-008"),
        ("Promesse de vente", "promesse_vente", "valid", "DEMO-PROPERTY-YDE-003"),
        ("Contrat de prestation architecte", "contrat_prestation", "valid", "DEMO-PRO-ARCH-001"),
        ("Attestation de vérification", "attestation", "expired", "DEMO-PROPERTY-YDE-010"),
    ]
    for i, (title, doc_type, status, owner) in enumerate(doc_templates):
        docs.append({
            "id": f"DEMO-DOCUMENT-{i+1:03d}", "title": title, "document_type": doc_type,
            "owner_id": owner, "status": status,
            "path": f"demo/documents/{doc_type}-{i+1:03d}.pdf",
            "mime_type": "application/pdf",
            "marker": "DOCUMENT DE DÉMONSTRATION — SANS VALEUR JURIDIQUE",
        })
    return docs


def _build_appointments():
    appts = []
    now = "2026-07-25T10:00:00+01:00"
    for i in range(12):
        statuses = ["confirmed","pending","cancelled","confirmed","confirmed","pending","rescheduled","confirmed","confirmed","confirmed","confirmed","no_show"]
        participants = [
            ("DEMO-USER-CLIENT-AUTH-001","DEMO-PRO-ARCH-001","DEMO-SERVICE-001"),
            ("DEMO-USER-CLIENT-AUTH-002","DEMO-PRO-NOTARY-001","DEMO-SERVICE-005"),
            ("DEMO-USER-CLIENT-AUTH-003","DEMO-PRO-ARCH-001",None),
            ("DEMO-USER-CLIENT-AUTH-004","DEMO-PRO-BUILDER-001","DEMO-SERVICE-009"),
            ("DEMO-USER-CLIENT-AUTH-001","DEMO-PRO-SURVEYOR-001","DEMO-SERVICE-006"),
            ("DEMO-USER-CLIENT-AUTH-005","DEMO-PRO-NOTARY-001","DEMO-SERVICE-004"),
            ("DEMO-USER-CLIENT-AUTH-006","DEMO-PRO-PLUMBER-001","DEMO-SERVICE-011"),
            ("DEMO-USER-CLIENT-AUTH-001","DEMO-PRO-ELECTRICIAN-001","DEMO-SERVICE-010"),
            ("DEMO-USER-CLIENT-AUTH-002","DEMO-PRO-MOVER-001","DEMO-SERVICE-012"),
            ("DEMO-USER-CLIENT-AUTH-003","DEMO-PRO-FINANCE-001","DEMO-SERVICE-013"),
            ("DEMO-USER-CLIENT-AUTH-004","DEMO-PRO-INSURANCE-001","DEMO-SERVICE-014"),
            ("DEMO-USER-CLIENT-AUTH-001","DEMO-PRO-NOTARY-001","DEMO-SERVICE-004"),
        ]
        p = participants[i]
        appts.append({
            "id": f"DEMO-APPOINTMENT-{i+1:03d}", "status": statuses[i],
            "requester_id": p[0], "provider_id": p[1], "service_id": p[2],
            "scheduled_at": f"2026-07-{(25+i%5):02d}T{(9+i%8):02d}:00:00+01:00",
            "duration_minutes": 60,
        })
    return appts


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
