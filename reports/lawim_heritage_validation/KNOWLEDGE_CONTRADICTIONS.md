# KNOWLEDGE CONTRADICTIONS — Contradictions Identifiées

**Statut :** Contradictions entre les documents patrimoniaux et les sources disponibles

---

## 1. Contradictions de Comptage

### _archive/ — 61 vs ~27 fichiers

| Source | Comptage |
|--------|----------|
| DATASETS.md §2.2 | 61 fichiers d'archives |
| SOURCE_INVENTORY.md (knowledge_unified/sources/) | 27 fichiers listés dans _archive/ |
| **Écart** | **+34 fichiers** |

**Impact :** Surestimation probable. Les 61 fichiers incluent peut-être _archive/ + _archive_minimal/ (16 fichiers : 27+16 = 43, toujours pas 61).

### _repair_backup/ — 84 vs ~60 fichiers

| Source | Comptage |
|--------|----------|
| DATASETS.md §2.2 | 84 fichiers de backup de réparation |
| SOURCE_INVENTORY.md | ~60 fichiers |
| **Écart** | **+24 fichiers** |

**Impact :** Surestimation probable.

### Volume LAWIMA — ~400 vs ~220

| Source | Comptage |
|--------|----------|
| HERITAGE_INDEX.md §2 | ~400 fichiers |
| SOURCE_INVENTORY.md (total inventoried) | ~220 fichiers toutes branches |
| **Écart** | **+180 fichiers** |

**Impact :** Le volume LAWIMA inclut peut-être les fichiers runtime et config (03_ENGINE/, 01_DATABASE/) qui ne sont pas dans l'inventaire knowledge.

---

## 2. Contradictions sur les Connaissances Uniques

### Lead scoring LAWIM vs LAWIMA

| HERITAGE_INDEX.md §7 | KNOWLEDGE_COVERAGE_MATRIX.md §5 |
|---------------------|----------------------------------|
| Scoring leads présent dans LAWIM (lead_scoring/) | Scoring leads listé comme dupliqué entre LAWIM + LAWIMA |
| **Contradiction :** §7 le marque comme dupliqué, §8 ne le liste pas comme unique (correct) |

### Règles moteur

| HERITAGE_INDEX.md §7 | KNOWLEDGE_COVERAGE_MATRIX.md §6 |
|---------------------|----------------------------------|
| Règles moteur : LAWIMA + ancienne (5 versions) | LAWIMA : Rule engine V5 comme unique |
| **Analyse :** §7 considère comme dupliqué LAWIMA/ancienne, §6 le liste comme unique LAWIMA. Pas de contradiction réelle car ancienne_structure est un sous-ensemble de LAWIMA. |

---

## 3. Contradictions Potentielles avec Constitution LAWIM

### Feature flags payments désactivé vs Constitution

**Constitution** (Article 1) : "LAWIM finance son activité par les services LAWIM et la mise en relation payante"
**FEATURE_FLAGS** (DOMAIN_MODEL.md §4.4) : payments désactivé

**Analyse :** La Constitution prévoit une monétisation, mais les feature flags indiquent que cette fonctionnalité est désactivée dans le backup. Cohérent: le modèle économique est défini mais pas encore implémenté.

### Zéro commission vs services payants

**Constitution :** Zéro commission sur transactions
**DOMAIN_MODEL :** Accompagnement payant 50k FCFA

**Analyse :** Cohérent — zéro commission (pas de % sur vente), mais service d'accompagnement payant (forfait). Pas de contradiction.

---

## 4. Contradictions sur les Sources

| Document | Source déclarée | Chemin réel |
|----------|----------------|-------------|
| HERITAGE_INDEX.md | LAWIM_BACKUP/LAWIM/ | N'existe pas — fichiers dans backup branch: docs/Directive/ |
| TRACEABILITY_MATRIX.md | LAWIM/KNOWLEDGE/ (chemin absolu) | N'existe plus |
| DATASETS.md | LAWIMA/02_KNOWLEDGE/ | N'existe pas |
| DATASETS.md | LAWIMA/01_DATABASE/ | N'existe pas |
| DOMAIN_MODEL.md | LAWIMA `persons` table (SQL) | implement_all.sql absent |

---

## 5. Contradictions sur les Règles Métier

### Anti-spam

| DOMAIN_MODEL.md §4.5 | Glossary |
|---------------------|----------|
| Maximum 10 messages/minute | 10 msg/min |
| Blocage 60 minutes | Blocage automatique pour 60 minutes |
| Table blocked_users | Non mentionné dans Glossary |

**Analyse :** Cohérent.

### Hot/Warm/Cold thresholds

| HERITAGE_GLOSSARY.md (V1) | KNOWLEDGE_COVERAGE_MATRIX.md (V5) |
|---------------------------|------------------------------------|
| Cold: score < 40 | Cold: score < 0.3 |
| Warm: score ≥ 60 | Warm: score ≥ 0.5 |
| Hot: score ≥ 80 | Hot: score ≥ 0.8 |

**Analyse :** Cohérent — V1 utilise 0-100, V5 utilise 0-1. Pas de contradiction, changement d'échelle.
