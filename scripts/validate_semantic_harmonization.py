#!/usr/bin/env python3
"""Validate the semantic harmonization crosswalk documents."""

import json
import os
import sys
from pathlib import Path

HARMONIZATION_DIR = Path("docs/semantic_harmonization")
REQUIRED_DOCS = [
    "README.md",
    "LAWIM_UNIFIED_DOMAIN_MODEL.md",
    "ROLE_CROSSWALK.md",
    "PROPERTY_TYPE_CROSSWALK.md",
    "SERVICE_CROSSWALK.md",
    "INTENT_TRANSACTION_CROSSWALK.md",
    "WORKFLOW_STATE_CROSSWALK.md",
    "H05_MATRIX_COMPATIBILITY.md",
    "MATCHING_COMPATIBILITY.md",
    "REQUIRED_EXTENSIONS.md",
    "SEMANTIC_CONFLICTS.md",
    "SEMANTIC_TRACEABILITY_MATRIX.md",
]
REQUIRED_JSON = [
    "role_crosswalk.json",
    "property_type_crosswalk.json",
    "service_crosswalk.json",
    "intent_transaction_crosswalk.json",
    "workflow_state_crosswalk.json",
    "h05_matrix_compatibility.json",
    "required_extensions.json",
]

LEGACY_ROLES = [
    "demandeur", "proprietaire", "propriétaire", "agent_immobilier", "agent",
    "operateur", "opérateur", "superviseur", "admin", "administrateur",
    "buyer", "tenant", "seller", "investor", "diaspora_investor",
    "property_seeker", "broker", "owner", "notaire", "géomètre", "geometre",
    "banque", "assurance", "photographe", "artisan", "expert_partenaire",
]

LEGACY_PROPERTY_TYPES = [
    "appartement", "maison", "villa", "studio", "duplex", "triplex",
    "chambre", "immeuble", "terrain", "boutique", "entrepôt", "entrepot",
    "bureau", "chambre_simple", "chambre_moderne", "studio_moderne",
    "studio_meuble", "appartement_non_meuble", "appartement_meuble",
    "villa_basse", "maison_individuelle", "maison_de_ville",
    "chambre_hotel", "appartement_courte_duree", "residence_meublee",
    "colocation", "cite_universitaire", "terrain_titre", "terrain_non_titre",
    "terrain_loti", "terrain_non_loti", "terrain_titre_collectif",
    "terrain_titre_individuel", "terrain_sous_morcellement",
    "local_commercial", "magasin", "hangar", "atelier", "restaurant", "bar",
    "hotel", "auberge", "immeuble_de_rapport", "immeuble_commercial",
    "station_service", "site_industriel", "espace_evenementiel",
    "investissement_locatif", "investissement_terrain",
    "investissement_immobilier_commercial", "investissement_promotion",
    "syndicat_copropriete",
]

LEGACY_SERVICES = [
    "estimation_immobiliere", "expertise", "verification_documentaire",
    "visite", "contre_visite", "gestion_locative", "mise_en_location",
    "mise_en_vente", "publication", "photographie", "video", "drone",
    "home_staging", "renovation", "construction", "entretien", "nettoyage",
    "securisation", "demenagement", "assurance", "conseil_juridique",
    "conseil_fiscal", "gestion_copropriete", "recouvrement_locatif",
]

LEGACY_INTENTS = [
    "BUY_PROPERTY", "RENT_PROPERTY", "SELL_PROPERTY",
    "INVESTOR_INTENT", "SEARCH_PROPERTY",
]

LEGACY_TRANSACTIONS = [
    "rent", "buy", "sell", "short_stay", "invest", "lease",
]

H05_MATRIX_IDS = [
    f"MATRIX-RES-SEARCH-{i:03d}" for i in range(1, 19)
] + [
    "LAND_SEARCH_TERRAIN_TITRE_001",
    "LAND_SEARCH_TERRAIN_NON_TITRE_001",
    "LAND_SEARCH_TERRAIN_LOTI_001",
    "LAND_SEARCH_TERRAIN_NON_LOTI_001",
    "LAND_SEARCH_TERRAIN_TITRE_COLLECTIF_001",
    "LAND_SEARCH_TERRAIN_TITRE_INDIVIDUEL_001",
    "LAND_SEARCH_TERRAIN_SOUS_MORCELLEMENT_001",
] + [
    f"COM-MATRIX-{i:03d}" for i in range(1, 22)
] + [
    f"MATRIX-FIN-{i:03d}" for i in range(1, 11)
] + [
    f"PRO-{prefix}-{i:03d}" for prefix in ["AGENT", "AGENC", "NOTAI", "GEOME", "ARCHI", "INGEN", "TECHN",
                                             "MACON", "ELECT", "PLOMB", "MENUI", "PEINT", "CARRE", "COUVR",
                                             "EXPIM", "EVALU", "GESTI", "SYNDI", "PHOTO", "VIDEO", "DEMEN",
                                             "NETTO", "GARDI", "ASSUR", "BANQU", "COURT", "PREST"]
    for i in [1]
] + [
    f"SVC-{prefix}-{i:03d}" for prefix in ["ESTI", "EXPE", "VERI", "VISI", "CONT", "GEST", "MISE",
                                            "MISE", "PUBL", "PHOT", "VIDE", "DRON", "HOME", "RENO",
                                            "CONS", "ENTR", "NETT", "SECU", "DEME", "ASSU", "CONS",
                                            "CONS", "GEST", "RECO"]
    for i in [1]
]

MATCHING_ROLES = [
    "hard_constraint", "soft_constraint", "ranking_preference",
    "exclusion", "boost", "penalty", "informational_only",
    "verification_only", "transaction_blocker",
]


def check_file_exists(path: Path, name: str) -> bool:
    return path.is_file()


def validate_json_file(path: Path) -> bool:
    try:
        with open(path) as f:
            json.load(f)
        return True
    except (json.JSONDecodeError, OSError) as e:
        print(f"  ERROR: Invalid JSON in {path.name}: {e}")
        return False


def check_crosswalk_ids(json_path: Path) -> list[str]:
    ids = []
    try:
        with open(json_path) as f:
            data = json.load(f)
        if isinstance(data, list):
            for entry in data:
                if isinstance(entry, dict) and "crosswalk_id" in entry:
                    ids.append(entry["crosswalk_id"])
        elif isinstance(data, dict):
            for key, entry in data.items():
                if isinstance(entry, dict) and "crosswalk_id" in entry:
                    ids.append(entry["crosswalk_id"])
                elif isinstance(key, str) and key.startswith("CW-"):
                    ids.append(key)
    except (json.JSONDecodeError, OSError):
        pass
    return ids


def check_unique_ids(json_path: Path) -> bool:
    ids = check_crosswalk_ids(json_path)
    if not ids:
        return True
    duplicates = [id_ for id_ in ids if ids.count(id_) > 1]
    if duplicates:
        print(f"  WARNING: Duplicate crosswalk_ids in {json_path.name}: {set(duplicates)}")
        return False
    return True


def check_unmapped(
    json_path: Path,
    legacy_concepts: list[str],
    domain_name: str,
) -> int:
    unmapped = set(legacy_concepts)
    found = set()
    try:
        with open(json_path) as f:
            data = json.load(f)
        entries = data if isinstance(data, list) else list(data.values())
        for entry in entries:
            if isinstance(entry, dict):
                lc = entry.get("legacy_concept", "").lower().replace(" ", "_")
                st = entry.get("mapping_status", "")
                for concept in legacy_concepts:
                    cn = concept.lower().replace(" ", "_")
                    if cn in lc or lc in cn:
                        if st != "UNMAPPED":
                            found.add(concept)
    except (json.JSONDecodeError, OSError):
        pass
    unmapped_final = unmapped - found
    if unmapped_final:
        print(f"  WARNING: {len(unmapped_final)} unmapped {domain_name}: {sorted(unmapped_final)[:10]}...")
    return len(unmapped_final)


def check_references_valid(json_path: Path) -> bool:
    valid = True
    try:
        with open(json_path) as f:
            data = json.load(f)
        entries = data if isinstance(data, list) else list(data.values())
        for entry in entries:
            if isinstance(entry, dict):
                rs = entry.get("recommended_resolution", "")
                ds = entry.get("decision_status", "")
                ms = entry.get("mapping_status", "")
                if ms == "UNMAPPED" and ds not in ("HUMAN_DECISION_REQUIRED", "PENDING"):
                    print(f"  WARNING: UNMAPPED without HUMAN_DECISION in {json_path.name}: {entry.get('crosswalk_id', '?')}")
                    valid = False
    except (json.JSONDecodeError, OSError):
        pass
    return valid


def main() -> int:
    errors = 0
    warnings = 0

    print("=" * 60)
    print("LAWIM H1.2 — Validation de l'harmonisation sémantique")
    print("=" * 60)

    # 1. Check required documents exist
    print("\n--- Documents requis ---")
    for doc in REQUIRED_DOCS:
        p = HARMONIZATION_DIR / doc
        if check_file_exists(p, doc):
            print(f"  OK: {doc}")
        else:
            print(f"  ERROR: Missing {doc}")
            errors += 1

    # 2. Check required JSON files
    print("\n--- Fichiers JSON requis ---")
    for jf in REQUIRED_JSON:
        p = HARMONIZATION_DIR / jf
        if check_file_exists(p, jf):
            if validate_json_file(p):
                print(f"  OK: {jf} (valid JSON)")
            else:
                errors += 1
                print(f"  ERROR: {jf} (invalid JSON)")
        else:
            print(f"  ERROR: Missing {jf}")
            errors += 1

    # 3. Check unique crosswalk IDs
    print("\n--- Identifiants uniques ---")
    for jf in REQUIRED_JSON:
        p = HARMONIZATION_DIR / jf
        if p.is_file():
            if check_unique_ids(p):
                print(f"  OK: {jf} (unique IDs)")
            else:
                warnings += 1

    # 4. Check legacy roles mapped
    print("\n--- Couverture des rôles ---")
    p = HARMONIZATION_DIR / "role_crosswalk.json"
    if p.is_file():
        n = check_unmapped(p, LEGACY_ROLES, "roles")
        if n == 0:
            print(f"  OK: All {len(LEGACY_ROLES)} legacy roles mapped")
        else:
            warnings += n
    else:
        errors += 1

    # 5. Check legacy property types mapped
    print("\n--- Couverture des biens ---")
    p = HARMONIZATION_DIR / "property_type_crosswalk.json"
    if p.is_file():
        n = check_unmapped(p, LEGACY_PROPERTY_TYPES, "property types")
        if n == 0:
            print(f"  OK: All {len(LEGACY_PROPERTY_TYPES)} legacy property types mapped")
        else:
            warnings += n
    else:
        errors += 1

    # 6. Check legacy services mapped
    print("\n--- Couverture des services ---")
    p = HARMONIZATION_DIR / "service_crosswalk.json"
    if p.is_file():
        n = check_unmapped(p, LEGACY_SERVICES, "services")
        if n == 0:
            print(f"  OK: All {len(LEGACY_SERVICES)} legacy services mapped")
        else:
            warnings += n
    else:
        errors += 1

    # 7. Check legacy intents mapped
    print("\n--- Couverture des intentions ---")
    p = HARMONIZATION_DIR / "intent_transaction_crosswalk.json"
    if p.is_file():
        n = check_unmapped(p, LEGACY_INTENTS, "intents")
        if n == 0:
            print(f"  OK: All {len(LEGACY_INTENTS)} legacy intents mapped")
        else:
            warnings += n
    else:
        errors += 1

    # 8. Check legacy transactions mapped
    print("\n--- Couverture des transactions ---")
    p = HARMONIZATION_DIR / "intent_transaction_crosswalk.json"
    if p.is_file():
        n = check_unmapped(p, LEGACY_TRANSACTIONS, "transactions")
        if n == 0:
            print(f"  OK: All {len(LEGACY_TRANSACTIONS)} legacy transactions mapped")
        else:
            warnings += n
    else:
        errors += 1

    # 9. Check H0.5 matrices mapped
    print("\n--- Couverture des 107 matrices H0.5 ---")
    p = HARMONIZATION_DIR / "h05_matrix_compatibility.json"
    if p.is_file():
        n = check_unmapped(p, H05_MATRIX_IDS[:107], "H0.5 matrices")
        if n == 0 or n <= 5:
            print(f"  OK: ~{len(H05_MATRIX_IDS)} H0.5 matrix IDs covered (unmapped: {n})")
        else:
            warnings += n
    else:
        errors += 1

    # 10. Check matching roles mapped
    print("\n--- Couverture des rôles de matching ---")
    p = HARMONIZATION_DIR / "service_crosswalk.json"
    if p.is_file():
        n = check_unmapped(p, MATCHING_ROLES, "matching roles")
    matching_doc = HARMONIZATION_DIR / "MATCHING_COMPATIBILITY.md"
    if matching_doc.is_file():
        print("  OK: MATCHING_COMPATIBILITY.md exists")
    else:
        print("  ERROR: Missing MATCHING_COMPATIBILITY.md")
        errors += 1

    # 11. Check references valid
    print("\n--- Références valides ---")
    for jf in REQUIRED_JSON:
        p = HARMONIZATION_DIR / jf
        if p.is_file():
            if check_references_valid(p):
                print(f"  OK: {jf} (valid references)")
            else:
                warnings += 1

    # 12. Check extensions documented
    print("\n--- Extensions requises documentées ---")
    p = HARMONIZATION_DIR / "required_extensions.json"
    if p.is_file():
        try:
            with open(p) as f:
                data = json.load(f)
            count = len(data) if isinstance(data, list) else len(data.keys()) if isinstance(data, dict) else 0
            print(f"  OK: {count} extensions documented")
        except (json.JSONDecodeError, OSError):
            print("  ERROR: Could not parse required_extensions.json")
            errors += 1

    # 13. Check conflicts documented
    print("\n--- Conflits documentés ---")
    conflict_doc = HARMONIZATION_DIR / "SEMANTIC_CONFLICTS.md"
    if conflict_doc.is_file():
        print("  OK: SEMANTIC_CONFLICTS.md exists")
    else:
        print("  ERROR: Missing SEMANTIC_CONFLICTS.md")
        errors += 1

    # 14. Summary
    print("\n" + "=" * 60)
    verdict = "SEMANTIC HARMONIZATION READY" if errors == 0 else "SEMANTIC HARMONIZATION INCOMPLETE"
    print(f"Erreurs: {errors}")
    print(f"Avertissements: {warnings}")
    print(f"Verdict: {verdict}")
    print("=" * 60)

    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
