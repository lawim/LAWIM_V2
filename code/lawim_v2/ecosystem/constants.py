from __future__ import annotations

PARTNER_TYPES: frozenset[str] = frozenset(
    {
        "real_estate_agency",
        "notary",
        "bank",
        "photographer",
        "microfinance",
        "surveyor",
        "architect",
        "construction_company",
        "artisan",
        "mover",
        "diagnostician",
        "insurer",
        "property_expert",
        "property_manager",
        "decorator",
        "rental_manager",
        "energy_provider",
        "internet_provider",
        "administration",
    }
)

SERVICE_CATEGORIES: frozenset[str] = frozenset(
    {
        "acquisition",
        "sale",
        "rental",
        "construction",
        "financing",
        "legal",
        "valuation",
        "insurance",
        "moving",
        "renovation",
        "property_management",
        "utilities",
        "administrative",
        "advisory",
    }
)

WORKFLOW_TYPES: frozenset[str] = frozenset(
    {
        "buy",
        "sell",
        "rent",
        "build",
        "finance",
        "relocation",
        "succession",
        "invest",
    }
)

MATCH_TYPES: frozenset[str] = frozenset({"partner", "service"})

NOTIFICATION_CHANNELS: frozenset[str] = frozenset({"in_app", "email", "sms", "whatsapp", "push"})

PARTNER_TYPE_ALIASES: dict[str, str] = {
    "agent": "real_estate_agency",
    "agency": "real_estate_agency",
    "notaire": "notary",
    "notary": "notary",
    "bank": "bank",
    "banque": "bank",
    "photographer": "photographer",
    "photographe": "photographer",
    "architect": "architect",
    "architecte": "architect",
    "contractor": "construction_company",
    "constructeur": "construction_company",
    "surveyor": "surveyor",
    "geometre": "surveyor",
    "advisor": "property_expert",
    "remote_manager": "rental_manager",
    "diagnostician": "diagnostician",
    "diagnostiqueur": "diagnostician",
    "artisan": "artisan",
    "mover": "mover",
    "demenageur": "mover",
    "owner": "real_estate_agency",
}

GOAL_PARTNER_MAP: dict[str, tuple[str, ...]] = {
    "buy": ("real_estate_agency", "notary", "bank", "property_expert", "photographer", "diagnostician"),
    "rent": ("real_estate_agency", "rental_manager", "insurer", "photographer"),
    "sell": ("real_estate_agency", "notary", "property_expert", "photographer", "diagnostician"),
    "build": ("architect", "construction_company", "surveyor", "bank", "diagnostician"),
    "invest": ("property_expert", "bank", "property_manager"),
    "secure_patrimony": ("notary", "property_expert", "insurer"),
    "prepare_retirement": ("property_expert", "bank", "property_manager"),
    "house_family": ("real_estate_agency", "bank", "insurer"),
    "diaspora": ("real_estate_agency", "notary", "rental_manager"),
    "other": ("real_estate_agency", "property_expert", "photographer", "diagnostician", "artisan", "mover"),
}

GOAL_SERVICE_MAP: dict[str, tuple[str, ...]] = {
    "buy": ("property_search", "visit_support", "document_check", "financing_prequalification"),
    "rent": ("property_search", "lease_review", "rental_insurance"),
    "sell": ("listing_support", "valuation", "mandate_preparation"),
    "build": ("land_search", "permit_guidance", "construction_supervision"),
    "invest": ("market_analysis", "yield_review", "portfolio_advisory"),
    "diaspora": ("remote_visit", "trust_verification", "rental_management"),
    "other": ("project_guidance", "advisory_session"),
}

WORKFLOW_STEP_TEMPLATES: dict[str, list[dict[str, str]]] = {
    "buy": [
        {"step_key": "qualify", "title": "Qualifier le projet", "partner_type": "real_estate_agency", "service_key": "project_guidance"},
        {"step_key": "search", "title": "Recherche de biens", "partner_type": "real_estate_agency", "service_key": "property_search"},
        {"step_key": "visit", "title": "Visites", "partner_type": "real_estate_agency", "service_key": "visit_support"},
        {"step_key": "finance", "title": "Financement", "partner_type": "bank", "service_key": "financing_prequalification"},
        {"step_key": "notary", "title": "Acte notarié", "partner_type": "notary", "service_key": "document_check"},
    ],
    "sell": [
        {"step_key": "valuation", "title": "Estimation", "partner_type": "property_expert", "service_key": "valuation"},
        {"step_key": "listing", "title": "Mise en marché", "partner_type": "real_estate_agency", "service_key": "listing_support"},
        {"step_key": "negotiate", "title": "Négociation", "partner_type": "real_estate_agency", "service_key": "mandate_preparation"},
        {"step_key": "closing", "title": "Clôture", "partner_type": "notary", "service_key": "document_check"},
    ],
    "rent": [
        {"step_key": "criteria", "title": "Définir critères", "partner_type": "real_estate_agency", "service_key": "project_guidance"},
        {"step_key": "search", "title": "Recherche locative", "partner_type": "real_estate_agency", "service_key": "property_search"},
        {"step_key": "lease", "title": "Bail", "partner_type": "notary", "service_key": "lease_review"},
    ],
    "build": [
        {"step_key": "land", "title": "Terrain", "partner_type": "surveyor", "service_key": "land_search"},
        {"step_key": "design", "title": "Conception", "partner_type": "architect", "service_key": "permit_guidance"},
        {"step_key": "build", "title": "Construction", "partner_type": "construction_company", "service_key": "construction_supervision"},
    ],
    "finance": [
        {"step_key": "assess", "title": "Analyse capacité", "partner_type": "bank", "service_key": "financing_prequalification"},
        {"step_key": "offer", "title": "Offre de prêt", "partner_type": "bank", "service_key": "financing_prequalification"},
    ],
    "relocation": [
        {"step_key": "search", "title": "Recherche zone", "partner_type": "real_estate_agency", "service_key": "property_search"},
        {"step_key": "move", "title": "Déménagement", "partner_type": "mover", "service_key": "moving_service"},
    ],
    "succession": [
        {"step_key": "inventory", "title": "Inventaire patrimonial", "partner_type": "notary", "service_key": "document_check"},
        {"step_key": "transfer", "title": "Transmission", "partner_type": "notary", "service_key": "document_check"},
    ],
    "invest": [
        {"step_key": "analysis", "title": "Analyse marché", "partner_type": "property_expert", "service_key": "market_analysis"},
        {"step_key": "acquire", "title": "Acquisition", "partner_type": "real_estate_agency", "service_key": "property_search"},
    ],
}

DEFAULT_SERVICE_CATALOG: tuple[dict[str, object], ...] = (
    {
        "service_key": "property_search",
        "category": "acquisition",
        "title": "Recherche de biens",
        "description": "Identification de biens alignés au projet et aux contraintes.",
        "indicative_price_min": 50000,
        "indicative_price_max": 150000,
        "estimated_duration_days": 14,
    },
    {
        "service_key": "visit_support",
        "category": "acquisition",
        "title": "Accompagnement visites",
        "description": "Organisation et suivi des visites immobilières.",
        "indicative_price_min": 25000,
        "indicative_price_max": 75000,
        "estimated_duration_days": 7,
    },
    {
        "service_key": "document_check",
        "category": "legal",
        "title": "Vérification documentaire",
        "description": "Contrôle titres, servitudes et conformité administrative.",
        "indicative_price_min": 100000,
        "indicative_price_max": 300000,
        "estimated_duration_days": 10,
    },
    {
        "service_key": "financing_prequalification",
        "category": "financing",
        "title": "Préqualification financement",
        "description": "Évaluation capacité d'emprunt et simulation.",
        "indicative_price_min": 0,
        "indicative_price_max": 50000,
        "estimated_duration_days": 5,
    },
    {
        "service_key": "valuation",
        "category": "valuation",
        "title": "Estimation immobilière",
        "description": "Estimation marché pour vente ou investissement.",
        "indicative_price_min": 75000,
        "indicative_price_max": 200000,
        "estimated_duration_days": 5,
    },
    {
        "service_key": "lease_review",
        "category": "rental",
        "title": "Relecture bail",
        "description": "Analyse clauses et conformité du contrat de location.",
        "indicative_price_min": 50000,
        "indicative_price_max": 120000,
        "estimated_duration_days": 3,
    },
    {
        "service_key": "listing_support",
        "category": "sale",
        "title": "Mise en marché",
        "description": "Préparation annonce, diffusion et suivi des contacts.",
        "indicative_price_min": 100000,
        "indicative_price_max": 400000,
        "estimated_duration_days": 21,
    },
    {
        "service_key": "land_search",
        "category": "construction",
        "title": "Recherche terrain",
        "description": "Identification parcelles constructibles.",
        "indicative_price_min": 80000,
        "indicative_price_max": 250000,
        "estimated_duration_days": 21,
    },
    {
        "service_key": "permit_guidance",
        "category": "construction",
        "title": "Permis de construire",
        "description": "Accompagnement dossier administratif.",
        "indicative_price_min": 150000,
        "indicative_price_max": 500000,
        "estimated_duration_days": 45,
    },
    {
        "service_key": "market_analysis",
        "category": "advisory",
        "title": "Analyse de marché",
        "description": "Étude rendement et dynamique locale.",
        "indicative_price_min": 100000,
        "indicative_price_max": 350000,
        "estimated_duration_days": 10,
    },
    {
        "service_key": "moving_service",
        "category": "moving",
        "title": "Déménagement",
        "description": "Organisation logistique du déménagement.",
        "indicative_price_min": 150000,
        "indicative_price_max": 800000,
        "estimated_duration_days": 3,
    },
    {
        "service_key": "project_guidance",
        "category": "advisory",
        "title": "Conseil projet",
        "description": "Session de cadrage et priorisation du parcours.",
        "indicative_price_min": 25000,
        "indicative_price_max": 100000,
        "estimated_duration_days": 2,
    },
)
