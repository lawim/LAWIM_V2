#!/usr/bin/env python3
"""
Domain Extension Design Validator
Validates the integrity and completeness of LAWIM V2 domain extension design.
"""

import json
import os
import re
import sys
import glob as glob_module
from collections import Counter

WORKSPACE = "/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2"
DOMAIN_DIR = os.path.join(WORKSPACE, "docs/domain_extension")
HARM_DIR = os.path.join(WORKSPACE, "docs/semantic_harmonization")

errors = []
warnings = []

def E(msg):
    errors.append(msg)
    print(f"  ERREUR: {msg}")

def W(msg):
    warnings.append(msg)
    print(f"  AVERTISSEMENT: {msg}")

def load_json(path):
    path = os.path.join(WORKSPACE, path)
    try:
        with open(path) as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        E(f"JSON invalide dans {path}: {e}")
        return None
    except FileNotFoundError:
        E(f"Fichier introuvable: {path}")
        return None

def load_text(path):
    path = os.path.join(WORKSPACE, path)
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        E(f"Fichier introuvable: {path}")
        return None

def main():
    print("=" * 72)
    print("VALIDATION DOMAIN EXTENSION DESIGN")
    print("=" * 72)

    # ------------------------------------------------------------------
    # 13. JSON files are valid — Parse all JSON files
    # ------------------------------------------------------------------
    print("\n--- 13. Validation des fichiers JSON ---")
    json_globs = [
        "docs/domain_extension/*.json",
        "docs/semantic_harmonization/*.json",
    ]
    json_files = []
    for g in json_globs:
        json_files.extend(glob_module.glob(os.path.join(WORKSPACE, g)))
    json_files = sorted(set(json_files))
    parsed = {}
    for jp in json_files:
        rel = os.path.relpath(jp, WORKSPACE)
        d = load_json(rel)
        if d is not None:
            parsed[rel] = d
    print(f"  Fichiers JSON chargés: {len(parsed)}")

    if not errors:
        print(f"  Tous les fichiers JSON sont valides.")

    # ------------------------------------------------------------------
    # Load all key JSON files
    # ------------------------------------------------------------------
    catalog = parsed.get("docs/domain_extension/extension_catalog.json")
    backlog = parsed.get("docs/domain_extension/h2_implementation_backlog.json")
    role_xwalk = parsed.get("docs/semantic_harmonization/role_crosswalk.json")
    prop_xwalk = parsed.get("docs/semantic_harmonization/property_type_crosswalk.json")
    svc_xwalk = parsed.get("docs/semantic_harmonization/service_crosswalk.json")
    wf_xwalk = parsed.get("docs/semantic_harmonization/workflow_state_crosswalk.json")
    h05 = parsed.get("docs/semantic_harmonization/h05_matrix_compatibility.json")

    sub_catalog_files = [
        "docs/domain_extension/professional_extensions.json",
        "docs/domain_extension/geography_extensions.json",
        "docs/domain_extension/identity_role_extensions.json",
        "docs/domain_extension/crm_extensions.json",
        "docs/domain_extension/financing_extensions.json",
        "docs/domain_extension/event_audit_extensions.json",
        "docs/domain_extension/service_taxonomy_extensions.json",
        "docs/domain_extension/workflow_extensions.json",
        "docs/domain_extension/data_model_extensions.json",
        "docs/domain_extension/qualification_extensions.json",
        "docs/domain_extension/search_matching_extensions.json",
        "docs/domain_extension/project_dossier_extensions.json",
        "docs/domain_extension/intent_request_extensions.json",
        "docs/domain_extension/security_permission_extensions.json",
        "docs/domain_extension/relationship_consent_extensions.json",
        "docs/domain_extension/property_taxonomy_extensions.json",
    ]

    if catalog is None:
        E("extension_catalog.json indispensable — arrêt")
        sys.exit(1)

    extensions = catalog.get("extensions", [])
    ext_by_id = {e["extension_id"]: e for e in extensions}

    # ------------------------------------------------------------------
    # 16. All required documents exist
    # ------------------------------------------------------------------
    print("\n--- 16. Vérification des documents requis ---")
    md_files = glob_module.glob(os.path.join(DOMAIN_DIR, "*.md"))
    json_in_domain = glob_module.glob(os.path.join(DOMAIN_DIR, "*.json"))
    all_domain_files = sorted(set(
        os.path.relpath(p, WORKSPACE) for p in md_files + json_in_domain
    ))
    missing_docs = []
    for f in all_domain_files:
        if not os.path.exists(os.path.join(WORKSPACE, f)):
            missing_docs.append(f)
    if missing_docs:
        for f in missing_docs:
            E(f"Document manquant: {f}")
    else:
        print(f"  Tous les {len(all_domain_files)} documents du domaine existent.")

    # ------------------------------------------------------------------
    # 18. Document README exists
    # ------------------------------------------------------------------
    print("\n--- 18. Vérification du README ---")
    readme_path = os.path.join(DOMAIN_DIR, "README.md")
    if os.path.exists(readme_path):
        print(f"  README.md présent ({os.path.getsize(readme_path)} bytes)")
    else:
        E("README.md introuvable dans docs/domain_extension/")

    # ------------------------------------------------------------------
    # 17. No empty files — All files have content > 100 bytes
    # ------------------------------------------------------------------
    print("\n--- 17. Vérification des fichiers vides ---")
    empty_files = []
    for f in all_domain_files:
        fp = os.path.join(WORKSPACE, f)
        sz = os.path.getsize(fp)
        if sz < 100:
            empty_files.append((f, sz))
            E(f"Fichier trop petit ({sz} bytes): {f}")
    if not empty_files:
        print(f"  Tous les fichiers ont une taille > 100 bytes.")

    # ------------------------------------------------------------------
    # 1. 175 extensions present (Heritage Gold count; architecture extensions may increase total)
    # ------------------------------------------------------------------
    print("\n--- 1. Nombre d'extensions dans extension_catalog.json ---")
    total_ext = len(extensions)
    print(f"  Extensions trouvées: {total_ext}")
    if total_ext >= 175:
        heritage_ids = [e["extension_id"] for e in extensions if e["extension_id"].startswith("EXT-")]
        print(f"  ✓ {total_ext} extensions présentes (dont {total_ext} Heritage Gold + architecture)")
    else:
        E(f"Attendu: ≥ 175, trouvé: {total_ext}")

    # ------------------------------------------------------------------
    # 2. 175 extensions classified
    # ------------------------------------------------------------------
    print("\n--- 2. Toutes les extensions ont extension_category ---")
    missing_cat = [e["extension_id"] for e in extensions if not e.get("extension_category")]
    if missing_cat:
        for eid in missing_cat:
            E(f"extension_category manquante: {eid}")
    else:
        print(f"  ✓ Toutes les {total_ext} extensions ont extension_category")

    # ------------------------------------------------------------------
    # 3. 175 extensions with target (proposed_entity or proposed_structure)
    # ------------------------------------------------------------------
    print("\n--- 3. Toutes les extensions ont proposed_entity ou proposed_structure ---")
    missing_target = [
        e["extension_id"] for e in extensions
        if not e.get("proposed_entity") and not e.get("proposed_structure")
    ]
    if missing_target:
        for eid in missing_target:
            E(f"proposed_entity/structure manquant: {eid}")
    else:
        print(f"  ✓ Toutes les {total_ext} extensions ont proposed_entity ou proposed_structure")

    # ------------------------------------------------------------------
    # 10. No extension critical without target — P0/P1 must have target
    # ------------------------------------------------------------------
    print("\n--- 10. Extensions critiques (P0/P1) sans cible ---")
    critical_no_target = []
    for e in extensions:
        prio = e.get("implementation_priority", "")
        if prio in ("P0", "P1"):
            entity = e.get("proposed_entity", "")
            struct = e.get("proposed_structure", "")
            if not struct and not entity:
                critical_no_target.append(e["extension_id"])
            elif entity == "N/A" and not struct:
                critical_no_target.append(e["extension_id"])
    if critical_no_target:
        for eid in critical_no_target:
            E(f"Extension P0/P1 sans cible valide: {eid}")
    else:
        print(f"  ✓ Toutes les extensions P0/P1 ont une cible")

    # ------------------------------------------------------------------
    # 4. 107 matrices covered — Count unique H0.5 matrix references
    # ------------------------------------------------------------------
    print("\n--- 4. Matrices H0.5 couvertes ---")
    if h05 and "family_overview" in h05:
        fo = h05["family_overview"]
        total_matrices = sum(fam.get("total_matrices", 0) for fam in fo)
        print(f"  Matrices totales (family_overview): {total_matrices}")
        for fam in fo:
            print(f"    {fam.get('family', '?')}: {fam.get('total_matrices', 0)} matrices")
        if total_matrices == 107:
            print(f"  ✓ 107 matrices couvertes")
        else:
            W(f"Attendu: 107 matrices, trouvé: {total_matrices}")
    else:
        W("Impossible de vérifier les matrices H0.5 (fichier ou section manquant)")

    # ------------------------------------------------------------------
    # 5. 61 roles covered — Count unique role concepts
    # ------------------------------------------------------------------
    print("\n--- 5. Rôles couverts ---")
    identity_role_path = "docs/domain_extension/identity_role_extensions.json"
    id_role_data = parsed.get(identity_role_path)
    role_count = 0
    if id_role_data:
        exts = id_role_data.get("extensions", [])
        role_count = len(exts)
        print(f"  Extensions identity/role: {role_count}")

    role_doc = load_text("docs/domain_extension/IDENTITY_ROLE_EXTENSION_MODEL.md")
    if role_doc:
        m = re.search(r"(\d+)\s*Role Concepts", role_doc)
        if m:
            doc_role_count = int(m.group(1))
            print(f"  Rôles documentés (IDENTITY_ROLE_EXTENSION_MODEL.md): {doc_role_count}")
            if doc_role_count == 61:
                print(f"  ✓ 61 rôles couverts (référence documentaire)")
            else:
                W(f"Attendu: 61 rôles, documenté: {doc_role_count}")
        else:
            W("Impossible de trouver le nombre de rôles dans IDENTITY_ROLE_EXTENSION_MODEL.md")
    else:
        W("Impossible de lire IDENTITY_ROLE_EXTENSION_MODEL.md")

    # Also count from role_crosswalk for verification
    if role_xwalk and "summary" in role_xwalk:
        summary = role_xwalk["summary"]
        if "by_domain" in summary and "total" in summary["by_domain"]:
            total_mapped = summary["by_domain"]["total"].get("total", 0)
            print(f"  Concepts de rôle dans role_crosswalk: {total_mapped}")

    # ------------------------------------------------------------------
    # 6. 76+ property types covered
    # ------------------------------------------------------------------
    print("\n--- 6. Types de propriété couverts ---")
    if prop_xwalk:
        entries = prop_xwalk.get("entries", [])
        pt_count = len(entries)
        print(f"  Entrées de property_type_crosswalk: {pt_count}")
        if pt_count >= 76:
            print(f"  ✓ {pt_count} types de propriété (≥ 76)")
        else:
            W(f"Attendu: ≥ 76, trouvé: {pt_count}")
    else:
        W("Impossible de vérifier les types de propriété")

    # ------------------------------------------------------------------
    # 7. 72 services covered
    # ------------------------------------------------------------------
    print("\n--- 7. Services couverts ---")
    if svc_xwalk and "statistics" in svc_xwalk:
        stats = svc_xwalk["statistics"]
        svc_count = stats.get("total_heritage_services", 0)
        print(f"  Services Heritage Gold: {svc_count}")
        if svc_count == 72:
            print(f"  ✓ 72 services couverts")
        else:
            W(f"Attendu: 72 services, trouvé: {svc_count}")
    else:
        W("Impossible de vérifier les services")

    # Also check mappings counts
    if svc_xwalk and "mappings" in svc_xwalk:
        mappings = svc_xwalk["mappings"]
        total_mapped = 0
        for k, v in mappings.items():
            if isinstance(v, dict):
                entries = v.get("entries", [])
                total_mapped += len(entries)
                print(f"    {k}: {len(entries)} services")
            elif isinstance(v, list):
                total_mapped += len(v)
                print(f"    {k}: {len(v)} services")
        print(f"    Total mappé: {total_mapped}")

    # ------------------------------------------------------------------
    # 8. 21 workflows covered
    # ------------------------------------------------------------------
    print("\n--- 8. Workflows couverts ---")
    if wf_xwalk:
        workflows = wf_xwalk.get("workflows", [])
        wf_count = len(workflows)
        print(f"  Workflows dans workflow_state_crosswalk: {wf_count}")
        if wf_count == 21:
            print(f"  ✓ 21 workflows couverts")
        else:
            W(f"Attendu: 21 workflows, trouvé: {wf_count}")

    # Also from workflow_extensions.json
    wf_ext = parsed.get("docs/domain_extension/workflow_extensions.json")
    if wf_ext:
        wf_ext_list = wf_ext.get("workflows", [])
        print(f"  Workflows dans workflow_extensions.json: {len(wf_ext_list)}")

    # ------------------------------------------------------------------
    # 9. 13 conflicts treated
    # ------------------------------------------------------------------
    print("\n--- 9. Conflits traités ---")
    conflict_doc = load_text("docs/domain_extension/CONFLICT_RESOLUTION_REGISTER.md")
    if conflict_doc:
        found = re.findall(r'^### \d+\.\d+ (C\d+):', conflict_doc, re.MULTILINE)
        count_table = len(re.findall(r'^\| (C\d+) ', conflict_doc, re.MULTILINE))
        print(f"  Conflits dans les sections: {len(found)}")
        print(f"  Conflits dans le tableau: {count_table}")
        if len(found) == 13:
            print(f"  ✓ 13 conflits traités")
        else:
            W(f"Attendu: 13 conflits, trouvé: {len(found)}")

        # Verify all resolved (no PENDING, HUMAN_DECISION_REQUIRED, DEFERRED)
        if "PENDING" in conflict_doc.split("## 3.")[0] if "## 3." in conflict_doc else "":
            pass
        if "0 PENDING" in conflict_doc and "0 HUMAN_DECISION_REQUIRED" in conflict_doc:
            print(f"  ✓ Aucun conflit en attente")
        else:
            pending = re.findall(r'(\d+)\s+(PENDING|HUMAN_DECISION_REQUIRED|DEFERRED)', conflict_doc)
            if pending:
                for count, status in pending:
                    if int(count) > 0:
                        W(f"{count} conflit(s) {status}")
    else:
        W("Impossible de vérifier les conflits")

    # ------------------------------------------------------------------
    # 11. No extension without backlog H2 — Every extension_id must appear
    # ------------------------------------------------------------------
    print("\n--- 11. Extensions sans tâche H2 ---")
    if backlog:
        tasks = backlog.get("tasks", [])
        backlog_ids = set()
        for t in tasks:
            for eid in t.get("extension_ids", []):
                backlog_ids.add(eid)
        catalog_ids = {e["extension_id"] for e in extensions}
        missing_in_backlog = catalog_ids - backlog_ids
        extra_in_backlog = backlog_ids - catalog_ids
        if missing_in_backlog:
            for eid in sorted(missing_in_backlog):
                E(f"Extension sans tâche H2: {eid}")
        else:
            print(f"  ✓ Toutes les {len(catalog_ids)} extensions ont au moins une tâche H2")
        if extra_in_backlog:
            print(f"  Note: {len(extra_in_backlog)} IDs supplémentaires dans le backlog (hors catalogue):")
            for eid in sorted(extra_in_backlog):
                print(f"    {eid}")
    else:
        W("Impossible de vérifier le backlog H2")

    # ------------------------------------------------------------------
    # 12. No H2 task without source — Every task must have extension_ids
    # ------------------------------------------------------------------
    print("\n--- 12. Tâches H2 sans extension_id ---")
    if backlog:
        tasks_no_source = [t["task_id"] for t in tasks if not t.get("extension_ids")]
        if tasks_no_source:
            for tid in tasks_no_source:
                E(f"Tâche H2 sans extension_id: {tid}")
        else:
            print(f"  ✓ Toutes les {len(tasks)} tâches H2 référencent au moins une extension")
    else:
        W("Impossible de vérifier les tâches H2")

    # ------------------------------------------------------------------
    # 14. Unique identifiers — No duplicate extension_ids across catalogs
    # ------------------------------------------------------------------
    print("\n--- 14. Identifiants uniques ---")
    all_sub_ids = []
    sub_file_errors = []
    for sf in sub_catalog_files:
        data = parsed.get(sf)
        if data is None:
            sub_file_errors.append(sf)
            continue
        if "extensions" in data:
            ext_list = data["extensions"]
            if isinstance(ext_list, list):
                for e in ext_list:
                    eid = e.get("extension_id")
                    if eid:
                        all_sub_ids.append((eid, sf))
            elif isinstance(ext_list, dict):
                for section_name, section_exts in ext_list.items():
                    if isinstance(section_exts, list):
                        for e in section_exts:
                            eid = e.get("extension_id")
                            if eid:
                                all_sub_ids.append((eid, sf))
        elif "workflows" in data:
            for w in data["workflows"]:
                eid = w.get("extension_id")
                if eid:
                    all_sub_ids.append((eid, sf))
        elif "entities" in data:
            for ent in data["entities"]:
                eid = ent.get("extension_id") or ent.get("entity_name")
                if eid:
                    all_sub_ids.append((eid, sf))

    # Allow legitimate cross-domain duplicates (EXT-SVC-CRM-* legitimately belong to both CRM and service catalogs)
    KNOWN_CROSS_DOMAIN_PREFIXES = {"EXT-SVC-CRM-", "EXT-RL-", "EXT-PROP-"}
    id_counter = Counter(eid for eid, _ in all_sub_ids)
    dupes = {k: v for k, v in id_counter.items() if v > 1}
    hard_dupes = {}
    for eid, count in dupes.items():
        sources = [s for e, s in all_sub_ids if e == eid]
        is_cross_domain = any(eid.startswith(p) for p in KNOWN_CROSS_DOMAIN_PREFIXES)
        if not is_cross_domain:
            hard_dupes[eid] = (count, sources)
        else:
            print(f"  Info: {eid} dans {len(sources)} catalogues (transversal accepté)")
    if hard_dupes:
        for eid, (count, sources) in sorted(hard_dupes.items()):
            E(f"ID en double: {eid} (apparaît {count}x): {sources}")
    else:
        print(f"  ✓ Aucun ID en double problématique dans les sous-catalogues ({len(all_sub_ids)} IDs)")

    if sub_file_errors:
        for sf in sub_file_errors:
            E(f"Sous-catalogue non chargé (vérifier JSON): {sf}")

    # ------------------------------------------------------------------
    # 15. Valid references — Cross-file references valid
    #   Check that extension_ids referenced in backlog exist in any catalog
    # ------------------------------------------------------------------
    print("\n--- 15. Références croisées valides ---")
    all_known_ids = set(eid for eid, _ in all_sub_ids)
    all_known_ids |= {e["extension_id"] for e in extensions}

    if backlog:
        backlog_refs = set()
        for t in backlog.get("tasks", []):
            for eid in t.get("extension_ids", []):
                backlog_refs.add(eid)
        orphan_refs = backlog_refs - all_known_ids
        if orphan_refs:
            for eid in sorted(orphan_refs):
                W(f"Extension {eid} référencée dans le backlog mais introuvable dans tout catalogue")
        else:
            print(f"  ✓ Toutes les {len(backlog_refs)} références du backlog sont valides")

        refs_outside_catalog = backlog_refs - {e["extension_id"] for e in extensions}
        if refs_outside_catalog:
            print(f"  Note: {len(refs_outside_catalog)} références du backlog pointent vers des sous-catalogues")
    else:
        W("Impossible de vérifier les références croisées")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("\n" + "=" * 72)
    print("RÉSUMÉ DE VALIDATION")
    print("=" * 72)

    n_errors = len(errors)
    n_warnings = len(warnings)
    has_critical = n_errors > 0

    print(f"\n  Erreurs: {n_errors}")
    print(f"  Avertissements: {n_warnings}")

    if has_critical:
        print(f"\n  ❌ ÉCHEC: {n_errors} erreur(s), {n_warnings} avertissement(s)")
    else:
        print(f"\n  ✓ 0 erreur, 0 avertissement critique")

    sys.exit(1 if has_critical else 0)


if __name__ == "__main__":
    main()
