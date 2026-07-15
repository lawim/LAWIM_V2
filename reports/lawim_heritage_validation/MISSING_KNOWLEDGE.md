# MISSING KNOWLEDGE — Connaissances Manquantes dans le Patrimoine

**Statut :** Connaissances documentées par HERITAGE_INDEX.md mais dont les sources sont absentes ou non vérifiables

---

## 1. Connaissances LAWIMA Non Vérifiables (Sources Supprimées)

### Fichiers Engine (03_ENGINE/)

| Fichier | Domaine | Impact |
|---------|---------|--------|
| `lawim_engine_v1.py` | Orchestrateur | Perte de la logique d'orchestration |
| `conversation_memory.py` | Mémoire conversation | Perte de l'implémentation mémoire |
| `long_term_memory.py` | Mémoire long-terme | Perte des règles de rétention (90 jours) |
| `follow_up_system.py` | Relance | Perte de la logique J1/J7/J30/J90 |
| `anti_spam.py` | Anti-spam | Perte des règles 10 msg/min, 60 min |
| `identity_resolution.py` | Résolution d'identité | Perte de l'algorithme de dédoublonnage |
| `data_quality_engine.py` | Qualité données | Perte des scores A+ à D |
| `property_lifecycle_engine.py` | Cycle de vie | Perte des transitions d'états |
| `location_normalizer.py` | Normalisation | Perte de la logique Levenshtein |
| `phone_formatter.py` | Formatage téléphone | Perte de la normalisation internationale |
| `knowledge_builder.py` | Profils (32 champs) | Perte de l'extraction automatique |
| `knowledge_enricher.py` | Enrichissement | Perte de l'apprentissage continu |
| `multilingual_responses.py` | Multilingue | Perte de la logique FR/EN/PID |
| `diaspora_filter.py` | Diaspora | Perte de la détection diaspora |
| `response_router.py` | Routage | Perte de la logique de routage |

### Fichiers Configuration (08_CONFIG/)

| Fichier | Domaine | Impact |
|---------|---------|--------|
| `RULE_ENGINE_V2.json` à V5.json | Règles moteur | Perte de 5 versions de règles évolutives |
| `FEATURE_FLAGS.json` | Feature flags | Perte de la liste des 19 flags |
| `USER_STATES.json` | États utilisateur | Perte des 7 états |
| `EVENT_TYPES.json` | Événements | Perte des 11 types d'événements |
| `CAMPAY_CONFIG.json` | Paiement | Perte de la config CamPay |
| `GREEN_API_CONFIG.json` | WhatsApp | Perte de la config GreenAPI |

### Fichiers IA (06_AI_MODELS/)

| Fichier | Domaine | Impact |
|---------|---------|--------|
| `lead_classifier_v1.json` | Classification leads | Perte des règles de scoring |
| `property_matching_v1.json` | Matching engine | Perte des dimensions/poids |
| `conversation_flows_v1.json` | Flows conversation | Perte des séquences de dialogue |
| `memory_rules_v1.json` | Règles mémoire | Perte des niveaux de familiarité (J1-J4) |
| `reasoning_rules_v1.json` | Raisonnement | Perte de la logique de raisonnement |
| `system_prompt_v1.md` | Prompt système (73 lignes) | Perte du prompt IA |

### Fichiers Base de Données (01_DATABASE/)

| Fichier | Domaine | Impact |
|---------|---------|--------|
| `runtime/agents.csv` | Agents runtime | Perte des données runtime |
| `runtime/users.csv` | Utilisateurs runtime | Perte des données runtime |
| `runtime/properties.csv` | Propriétés runtime | Perte des données runtime |
| `runtime/leads.csv` | Leads runtime | Perte des données runtime |
| `ready_for_supabase/*.csv` | Données Supabase | Perte des données préparées |
| `supabase_ready/*.csv` | Données Supabase | Perte des données finales |

### Scripts SQL (05_AUTOMATIONS/)

| Fichier | Domaine | Impact |
|---------|---------|--------|
| `implement_all.sql` | Implémentation SQL | Perte de 15 définitions de tables |
| `setup_database.sql` | Setup base | Perte du schéma initial |

---

## 2. Connaissances Partiellement Documentées

| Connaissance | Source actuelle | Manque |
|-------------|----------------|--------|
| Feature flags | HERITAGE_INDEX.md §6, DOMAIN_MODEL.md §4.4 | Détail des flags, documentation des décisions |
| Anti-spam | DOMAIN_MODEL.md §4.5 | Code source, détails d'implémentation |
| Tables SQL | DOMAIN_MODEL.md §7 | Scripts SQL, types de colonnes, contraintes |
| Règles moteur V2-V5 | Mentionnées mais non vérifiables | Contenu des versions, évolution |
| Qualité données | HERITAGE_INDEX.md §8 | Scores A+ à D, algorithmes |
| Monétisation | Connaissance unique mentionnée | Logique détaillée, intégration CamPay |

---

## 3. Contradictions de Comptage

| Élément | HERITAGE_INDEX.md / DATASETS.md | SOURCE_INVENTORY.md | Écart |
|---------|-------------------------------|---------------------|-------|
| _archive/ fichiers | 61 | ~27 | +34 |
| _repair_backup/ fichiers | 84 | ~60 | +24 |
| ancienne_structure volume | ~300 fichiers | Sous-ensemble LAWIMA | Non quantifiable |
| LAWIMA volume | ~400 fichiers | ~220 fichiers toutes branches | Surestimation probable |

---

## 4. Connaissances Identifiées Comme Perdues (KNOWLEDGE_COVERAGE_MATRIX.md §4)

1. **Logique détaillée de l'ADR-009** — Documenté dans LAWIM_V2 mais pas dans les branches legacy
2. **Processus d'escalade complets** — Partiellement dans conversation-patterns.md (source absente)
3. **Règles de pricing avancées** — pricing.json présent mais contenu non vérifiable
4. **Détail des documents financiers (.docx)** — Format non lisible
5. **Contenu des documents marketing (.odt)** — Format non lisible
