# KNOWLEDGE GAPS — Heritage Gold Readiness

**Audité par :** Knowledge Gap Hunter (H0.3)
**Date :** 2026-07-15

## Gaps HAUT impact (12)

| ID | Domaine | Concept manquant | Source | Impact |
|----|---------|-----------------|--------|--------|
| KG-001 | Workflow | **Machine à états Dossier** (12 états) | 05-WORKFLOW-REFERENCE.md Ch.54 | Bloque la gestion complète du cycle de vie des dossiers |
| KG-002 | Workflow | **Machine à états Bien** (11 états) | 05-WORKFLOW-REFERENCE.md Ch.35 | Bloque le lifecycle des propriétés |
| KG-003 | Workflow | **SLA par type de bien** | 05-WORKFLOW-REFERENCE.md Ch.22 | Bloque l'automatisation temporelle |
| KG-004 | Workflow | **Next Best Action (NBA) Engine** | 05-WORKFLOW-REFERENCE.md Ch.11,69,160 | Bloque l'architecture proactive du système |
| KG-005 | Workflow | **Progressive Search Expansion** (6 niveaux) | 05-WORKFLOW-REFERENCE.md Ch.23-27 | Bloque la gestion des échecs de matching |
| KG-006 | Workflow | **Continuous Market Surveillance** | 05-WORKFLOW-REFERENCE.md Ch.27 | Bloque le monitoring passif des dossiers |
| KG-007 | Workflow | **Diagnostic Automatique pour Matching Échoué** | 05-WORKFLOW-REFERENCE.md Ch.25 | Bloque l'analyse des causes d'échec |
| KG-008 | Workflow | **Machine à états Visite** (9 états) | 05-WORKFLOW-REFERENCE.md Ch.95 | Bloque la gestion des visites |
| KG-009 | Workflow | **Machine à états Négociation** (7 états) | 05-WORKFLOW-REFERENCE.md Ch.111 | Bloque la gestion des négociations |
| KG-010 | Workflow | **Machine à états Transaction** (8 états) | 05-WORKFLOW-REFERENCE.md Ch.131 | Bloque la gestion des transactions |
| KG-011 | Workflow | **Machine à états Paiement** (10 états) | 05-WORKFLOW-REFERENCE.md Ch.153 | Bloque la gestion des paiements |
| KG-012 | Workflow | **Dossier Health Score** (4 niveaux) | 05-WORKFLOW-REFERENCE.md Ch.30 | Bloque la priorisation des dossiers |

## Gaps MOYEN impact (10)

| ID | Domaine | Concept manquant | Source | Impact |
|----|---------|-----------------|--------|--------|
| KG-013 | Workflow | **Property Health Score** | 05-WORKFLOW-REFERENCE.md Ch.31 | Qualité matching |
| KG-014 | Workflow | **Learning from Events** | 05-WORKFLOW-REFERENCE.md Ch.106,125,143 | Apprentissage comportemental |
| KG-015 | Workflow | **Non-Responsive Owner Escalation** (3 étapes) | 05-WORKFLOW-REFERENCE.md Ch.29,80 | Gestion propriétaires inactifs |
| KG-016 | Workflow | **Intelligent Search Suggestions** | 05-WORKFLOW-REFERENCE.md Ch.26 | Suggestions automatiques |
| KG-017 | Workflow | **Incident/Litigation State Machine** | 05-WORKFLOW-REFERENCE.md Ch.168 | Gestion des litiges |
| KG-018 | Workflow | **Service Payment Lifecycle** (7 états) | 05-WORKFLOW-REFERENCE.md Ch.149 | Cycle de vie des services |
| KG-019 | Profile | **Channel-Specific Data Collection** | knowledge_builder.py:152-168 | Collecte par canal |
| KG-020 | Profile | **Extended User Profile Fields** (26) | knowledge_builder.py:24-31 | Profil utilisateur complet |
| KG-021 | Profile | **Profile Completeness Scoring** | knowledge_builder.py:194-196 | Complétude profil |
| KG-022 | Workflow | **Mise en Relation lifecycle** | 05-WORKFLOW-REFERENCE.md Ch.74-89 | Mise en relation complète |

## Gaps FAIBLE impact (9)

| ID | Domaine | Concept manquant | Source | Impact |
|----|---------|-----------------|--------|--------|
| KG-023 | Knowledge | **Auto Knowledge Base Enrichment** | knowledge_enricher.py:30-68 | Enrichissement automatique |
| KG-024 | Knowledge | **Dynamic knowledge_entries Table** | knowledge_enricher.py:58-64 | Table de connaissances |
| KG-025 | Property | **Category-Specific Fields** (3 catégories) | property_types.py:35-38 | Champs par catégorie |
| KG-026 | Property | **Multilingual Property Synonyms** | property_types.py:5-31 | Synonymes multilingues |
| KG-027 | Storage | **Supabase File Storage** | file_upload.py:15-51 | Upload fichiers |
| KG-028 | Storage | **Identity Document Upload** (CNI) | file_upload.py:46-47 | Upload CNI |
| KG-029 | Service | **Service Configuration System** | service_manager.py:12-16 | Configuration services |
| KG-030 | Comm | **WhatsApp Deep Link Generation** | phone_formatter.py:183-189 | Lien WhatsApp direct |
| KG-031 | Comm | **Health Endpoint** | whatsapp_gateway_v2.py:62-64 | Monitoring |

## Résumé

| Niveau | Nombre |
|--------|:------:|
| HAUT | 12 |
| MOYEN | 10 |
| FAIBLE | 9 |
| **Total** | **31** |

Les 12 gaps HAUT sont tous dans le domaine Workflow — les machines à états complètes qui pilotent le comportement du système. Sans elles, LAWIM_V2 serait un système passif sans orchestration.
