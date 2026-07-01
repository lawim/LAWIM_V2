from __future__ import annotations

KNOWLEDGE_DOMAINS: dict[str, tuple[str, ...]] = {
    "immobilier": (
        "achat",
        "vente",
        "location",
        "gestion_locative",
        "copropriete",
        "investissement",
        "promotion_immobiliere",
        "construction",
        "renovation",
        "urbanisme",
    ),
    "juridique": (
        "contrats",
        "compromis",
        "actes",
        "obligations",
        "responsabilites",
        "procedures",
        "fiscalite_immobiliere",
        "successions",
        "donations",
        "baux",
    ),
    "financement": (
        "prets",
        "banques",
        "apport",
        "taux",
        "assurance",
        "garanties",
        "simulations",
        "capacite_emprunt",
    ),
    "technique": (
        "construction",
        "materiaux",
        "diagnostics",
        "energie",
        "maintenance",
        "securite",
        "normes",
    ),
    "administration": (
        "permis",
        "cadastre",
        "impots",
        "formalites",
        "procedures_administratives",
    ),
}

IMPORT_FORMATS: frozenset[str] = frozenset({"markdown", "html", "pdf", "docx", "txt"})
EXPORT_FORMATS: frozenset[str] = frozenset({"markdown", "html", "json", "txt"})
DOCUMENT_STATUSES: frozenset[str] = frozenset({"draft", "review", "approved", "published", "archived"})
PUBLICATION_STATUSES: frozenset[str] = frozenset({"draft", "published", "unpublished"})

INDEX_TYPES: frozenset[str] = frozenset({"lexical", "semantic", "hybrid"})
RELATION_TYPES: frozenset[str] = frozenset({"references", "cites", "extends", "contradicts", "supports"})

DEFAULT_EMBEDDING_MODEL = "lawim-deterministic-v1"
DEFAULT_CHUNK_SIZE = 320
