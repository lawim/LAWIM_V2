# Matrice De Tracabilite

Version: 1.0
Date: 2026-07-14
Commit de reference: d30d61e1d89427ece9c180cec4639cce77fdcba3
Statut: CANONICAL

## Principe
Exigence cible != code actuel != preuve actuelle. Un element de code sans exigence canonique est candidat a suppression. Une exigence sans code est a construire.

| Requirement ID | Domaine | Description | Document canonique | Objet metier | API cible | Module cible | Evenement | Feature Flag | Test attendu | Statut actuel | Decision future |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-LAWIM-001 | Projects and Dossiers | LAWIM comprend, structure, qualifie, recherche, met en relation, accompagne et suit. | 00_LAWIM_VISION_AND_SCOPE.md | Project | /api/v2/projects | project_service | project.created | none | acceptance corpus | PARTIAL | KEEP_AND_CLEAN |
| REQ-CONV-001 | Conversation | Conversation cible reconstruite sans dependance a l ancien runtime. | 07_CONVERSATION_TARGET_SPECIFICATION.md | Conversation | /api/v2/conversation-v2 | conversation_v2 | message.received | LAWIM_FEATURE_CONVERSATION_V2 | behavioral multichannel | TO_REBUILD | REBUILD |
| REQ-QUAL-001 | Qualification | Matrices executables par parcours. | 08_QUALIFICATION_TARGET_SPECIFICATION.md | Fact | /api/v2/qualification | qualification_v2 | fact.confirmed | LAWIM_FEATURE_QUALIFICATION_V2 | domain/property tests | TO_REBUILD | REBUILD |
| REQ-SEARCH-001 | Search | Criteres qualifies transformes en requetes autorisees. | 09_SEARCH_AND_MATCHING_TARGET_SPECIFICATION.md | SearchRequest | /api/v2/search | search_v2 | search.requested | LAWIM_FEATURE_SEARCH_V2 | integration tests | TO_REBUILD | REBUILD |
| REQ-MATCH-001 | Matching | Matching explicable sans criteres insuffisants. | 09_SEARCH_AND_MATCHING_TARGET_SPECIFICATION.md | Match | /api/v2/matching-v2 | matching_v2 | match.proposed | LAWIM_FEATURE_MATCHING_V2 | property tests | TO_REBUILD | REBUILD |
| REQ-REL-001 | Relationship | Relation creee seulement apres consentements requis. | 10_RELATIONSHIP_TARGET_SPECIFICATION.md | Relationship | /api/v2/relationships | relationship_v2 | relationship.created | LAWIM_FEATURE_RELATIONSHIP_V2 | security/live tests | TO_REBUILD | REBUILD |
| REQ-CHAN-001 | Channels and Communication | Canaux comme adaptateurs sans logique metier autonome. | 14_CHANNELS_AND_OMNICHANNEL.md | ChannelIdentity | /api/notifications/* | communication | channel.verified | channel flags | webhook/integration | PARTIAL | CLEAN |
| REQ-AI-001 | AI Governance | IA comme capacite linguistique interchangeable. | 15_AI_GOVERNANCE.md | AuditEvent | /api/admin/ai/* | ai | ai.call.completed | AI_ORCHESTRATOR_ENABLED | security/runtime | IMPLEMENTED_UNVERIFIED | CLEAN |
| REQ-FIN-001 | Financial Core | Financial Core conserve sous controle. | 13_FINANCIAL_CORE_AND_CAMPAY.md | Payment | /api/v2/financial/* | financial | payment.created | LAWIM_FEATURE_FINANCIAL_CORE | domain/integration/live | IMPLEMENTED_UNVERIFIED | KEEP_AND_CLEAN |
| REQ-FEAT-001 | Feature Management | Tout module majeur est desactivable. | 16_FEATURE_MANAGEMENT.md | FeatureFlag | /api/v2/features-target | feature_management | feature_flag.changed | all major flags | unit/integration/audit | PARTIAL | CLEAN |
| REQ-TEST-001 | Testing | Validation metier exige corpus, integration, live et preuve de version. | 20_TESTING_AND_ACCEPTANCE_STANDARD.md | AuditEvent | n/a | tests | acceptance.proven | none | full acceptance suite | PARTIAL | BUILD |
| REQ-OPS-001 | Backup and Disaster Recovery | Fondations operations et recovery conservees. | 21_DEPLOYMENT_OPERATIONS_AND_RECOVERY.md | AuditEvent | /api/v2/backup/* | backup | backup.completed | backup flags | restore tests | IMPLEMENTED_UNVERIFIED | KEEP_AND_CLEAN |

## Mise A Jour Mission 2

| Domaine canonique | Statut actuel apres Mission 2 | Decision future | Preuve |
| --- | --- | --- | --- |
| Conversation | TO_REBUILD / DECOMMISSIONED | REBUILD | Modules Conversation Core, Assistant, Brain conversationnel et routes associees supprimes; maintenance deterministe active. |
| Qualification | TO_REBUILD / DECOMMISSIONED | REBUILD | Progression, known_fields, missing_fields et next_question legacy supprimes avec les tests historiques. |
| Search | TO_REBUILD / DECOMMISSIONED | REBUILD | Routes Search legacy et SDK matching supprimes. |
| Matching | TO_REBUILD / DECOMMISSIONED | REBUILD | Moteurs `matching.py`, `MatchingEngine2`, `MatchingEngine` et `RequestMatchingEngine` supprimes. |
| Relationship | TO_REBUILD / DECOMMISSIONED | REBUILD | Proposals, consentements automatiques et RelationEngine supprimes. |
| Channels and Communication | PARTIAL / MAINTENANCE_MODE | CLEAN | Web, WhatsApp et Telegram conservent la reception et reponse maintenance sans LLM. |
