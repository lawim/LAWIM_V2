# KNOWLEDGE DUPLICATES — Connaissances Dupliquées entre Branches

**Statut :** Vérification basée sur TRACEABILITY_MATRIX.md et SOURCE_INVENTORY.md

---

## 1. Duplications Identifiées par HERITAGE_INDEX.md (§7)

| Connaissance | Branches | Degré déclaré | Vérification |
|-------------|----------|---------------|-------------|
| Intentions (buy/rent/sell/search/investor) | LAWIM + LAWIMA + ancienne | Similaire | TRACEABILITY_MATRIX.md confirme : QUAL-003 à QUAL-007 mergés comme identiques. Les 5 fichiers étaient présents dans les 3 branches. |
| Quartiers | LAWIM + LAWIMA | Légères différences | TRACEABILITY_MATRIX.md : neighborhoods/ présents dans les 3 branches. Différences non vérifiables (fichiers sources absents). |
| Géographie | LAWIM + LAWIMA | LAWIM plus riche | TRACEABILITY_MATRIX.md : LAWIM avait 11 fichiers geography/ + cities/, LAWIMA avait moins de fichiers. |
| Scoring leads | LAWIM + LAWIMA | 2 dossiers de scoring | TRACEABILITY_MATRIX.md : lead_scoring.json et scoring/ présents. Fichiers sources absents. |
| WhatsApp language | LAWIM + LAWIMA + ancienne | Similaires | TRACEABILITY_MATRIX.md LANG-001 à LANG-007 : 7 fichiers identiques dans les 3 branches. |
| Entity linking | LAWIM + LAWIMA + ancienne | Identique | TRACEABILITY_MATRIX.md : Entité non listée explicitement mais mentionnée dans KNOWLEDGE_COVERAGE_MATRIX.md. |
| Moteur de matching | LAWIM + LAWIMA | Différents niveaux de détail | TRACEABILITY_MATRIX.md MATCH-001 à MATCH-006 : LAWIM docs matching, LAWIMA property_matcher. |
| Règles moteur | LAWIMA + ancienne | 5 versions évolutives | Non vérifiable. RULE_ENGINE V2-V5 absents. |
| Flows conversation | LAWIM + LAWIMA | Format différent (MD vs JSON) | COMM-001 à COMM-008 : conversation-patterns.md (LAWIM) vs conversation_flows_v1.json (LAWIMA). |

---

## 2. Duplications Confirmées par TRACEABILITY_MATRIX.md

| Domaine | Entrées mergées | Branches sources | Degré |
|---------|----------------|-----------------|-------|
| Géographie | GEO-002 (v2_backup) → cities.json | LAWIM (v1+v2) | Identique après merge |
| Géographie | GEO-008 (district_aliases_v2) → aliases.json | LAWIM (v2+v3) | Identique après merge |
| Qualification | QUAL-003 à QUAL-007 → intentions.json | LAWIM (5 intents) | Identique |
| Langage | LANG-002 à LANG-007 → common_expressions.json | LAWIM (diaspora, investor, negotiation, listing, search, urgency) | Identique après merge |
| Langage | LANG-009 à LANG-012 → spelling_variants.json | LAWIM (4 fichiers typo) | Identique après merge |
| Immobilier | RE-003 (property_taxonomy_v1) → property_types.json | LAWIM (v1+v2) | V2 a superseded V1 |

---

## 3. Duplications Potentielles Non Documentées

| Connaissance | Raison de suspicion |
|-------------|-------------------|
| CRM schema | Présent dans 3 dossiers (crm/, crm_schema/) dans LAWIM + LAWIMA |
| Pricing expressions | Présent dans pricing/ et pricing_expressions/ (duplicata noté dans DATASETS.md §1.8) |
| Search aliases | Présent dans search/ et search_aliases/ (duplicata noté dans DATASETS.md §1.8) |
| Investors | Présent dans investor/ et investors/ (dossiers séparés) |

---

## 4. Recommandations

1. Les duplications entre LAWIM LAWIMA ancienne_structure sont principalement dues à la séparation historique des branches
2. TRACEABILITY_MATRIX.md a déjà résolu la plupart des duplications via des merges vers knowledge_unified/
3. Les duplicatas internes à LAWIM (crm/crm_schema, pricing/pricing_expressions, search/search_aliases, investor/investors) devraient être nettoyés
4. Vérifier si les contenus sont identiques ou s'il s'agit de versions différentes
