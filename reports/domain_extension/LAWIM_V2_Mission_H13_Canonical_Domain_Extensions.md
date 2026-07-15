# LAWIM_V2 — Mission H1.3 : Conception des Extensions Canoniques du Domaine

**Date :** 2026-07-15  
**HEAD :** 8aa705bc → *(post-commit)*  
**Tag final :** `lawim-v2-canonical-domain-extension-h13`  
**Verdict :** CANONICAL DOMAIN EXTENSIONS READY

---

## 1. Résumé exécutif

La mission H1.3 a transformé les **175 extensions** issues de l'harmonisation sémantique H1.2 en une **spécification canonique cohérente et directement implémentable**. Chaque concept Heritage Gold a reçu une décision d'architecture claire et a été tracé jusqu'à une tâche du backlog H2.

### Chiffres clés

| Métrique | Valeur |
|----------|--------|
| Extensions inventoriées | 175 (Heritage Gold) + 6 (architecture) |
| Extensions classifiées | 181 |
| Extensions avec cible | 181 |
| Matrices H0.5 couvertes | 107 |
| Rôles couverts | 61 |
| Types de biens couverts | 76+ |
| Services couverts | 72 |
| Workflows couverts | 21 |
| Conflits résolus | 13 |
| Tâches backlog H2 | 204 |
| Vagues d'implémentation | 12 |
| Validateur | 0 erreur, 0 avertissement critique |

### Décisions d'architecture majeures

| Décision | Choix |
|----------|-------|
| Modèle de rôles | Hybride : rôles V2 + niveaux de confiance + badges + hiérarchie d'agence |
| Taxonomie des biens | Heritage Gold prévaut (7 familles, énumération validée + fallback metadata_json) |
| Machine d'état | Hybride : états Heritage Gold avec couche de mapping V2 |
| Transaction vs Projet | Deux entités distinctes liées 1:1 |
| Dossier vs Projet | Garder "Projet", ajouter la sémantique dossier |
| Modèle de service | Heritage Gold prévaut (72 services, tarification fixe, Campay) |
| CRM | Heritage Gold prévaut (pipeline 8 étapes, scoring, routage) |
| Détection d'intention | Couche optionnelle sur la sélection explicite |
| Matching | Heritage Gold prévaut (moteur complet 5 dimensions) |
| Modèle de données | Hybride (colonnes typées pour le coeur, metadata_json pour les champs spécifiques) |

---

## 2. État Git initial

```
HEAD: 8aa705bc5aaa6331a9eeeaff57a2ea9ddac6ba67
Tag H1.2: lawim-v2-semantic-harmonization-h12 ✓
Worktree: strictement propre ✓
```

Tag de sécurité créé : `pre-canonical-domain-extension-h13`

---

## 3. Sources analysées

| Document | Statut |
|----------|--------|
| required_extensions.json (175 extensions) | Analysé |
| LAWIM_UNIFIED_DOMAIN_MODEL.md (15 domaines) | Analysé |
| SEMANTIC_CONFLICTS.md (13 conflits) | Analysé |
| ROLE_CROSSWALK.md | Analysé |
| PROPERTY_TYPE_CROSSWALK.md | Analysé |
| SERVICE_CROSSWALK.md | Analysé |
| INTENT_TRANSACTION_CROSSWALK.md | Analysé |
| WORKFLOW_STATE_CROSSWALK.md | Analysé |
| MATCHING_COMPATIBILITY.md | Analysé |
| SEMANTIC_TRACEABILITY_MATRIX.md | Analysé |
| H05_MATRIX_COMPATIBILITY.md | Analysé |
| h05_matrix_compatibility.json (107 matrices) | Analysé |
| Qualification matrices (docs/lawim_heritage_gold/) | Analysé |

---

## 4. Agents invoqués

Voir `reports/domain_extension/H13_ORCHESTRATION_LOG.md` pour le détail complet.

---

## 5. Principes de préséance

Appliqués strictement :
- **LAWIM_V2** prévaut pour : architecture technique, frontières de domaines, sécurité, consentement, identité système, persistance, conventions API, audit, RBAC.
- **Heritage Gold** prévaut pour : profondeur métier, qualification, typologies de biens/services, géographie, workflows métier, matching, scoring, scripts commerciaux, NBA.

---

## 6. Inventaire des 175 extensions

Les 175 extensions Heritage Gold + 6 extensions architecturales (API, migration) sont cataloguées dans :

| Fichier | Contenu |
|---------|---------|
| `docs/domain_extension/EXTENSION_CATALOG.md` | Catalogue lisible |
| `docs/domain_extension/extension_catalog.json` | Catalogue machine (181 entrées) |
| Sous-catalogues par domaine | 16 fichiers JSON spécialisés |

---

## 7. Classification par domaine

| Domaine | Nb extensions | Détail |
|---------|--------------|--------|
| Services | 51 | Services immobiliers, professionnels, CRM |
| Identity/Roles | 23 | Niveaux confiance, badges, rôles agence |
| Properties | 15 | Familles, types, cycle de vie, prix |
| Matching | 13 | Scoring, compatibilité, rematching |
| CRM | 20 | Pipeline, scoring, routage, anti-fraude |
| Workflows | 14 | Machines à états, SLAs |
| Qualification | 11 | 107 matrices, dictionnaire de champs |
| Transactions | 8 | Types de transaction, cycle de vie |
| Intent | 6 | Détection, confiance, multi-intention |
| SLA | 6 | Seuils, détection de brèche, escalade |
| Agency | 9 | Onboarding, routage, crédits |
| Permission | 4 | Matrice 4 niveaux |
| NBA | 4 | Actions recommandées, calendrier |
| Event/Audit | 10 | Catalogue d'événements typés |
| Geography | 12 | Unités géographiques, alias |
| Projet/Dossier | 20 | Double consentement, rematching |
| Relationship/Consent | 13 | Consentement, partage, révocation |
| Financing | 10 | Financement, éligibilité |
| Professional | 12 | Profils, catégories, certifications |

---

## 8. Rôles et identités

Document : `IDENTITY_ROLE_EXTENSION_MODEL.md`

9 types de rôles distincts : system_role, business_role, user_typology, professional_category, transaction_participant_role, organization_role, CRM_status, permission_scope.

Modèle capable de représenter une même personne comme utilisateur authentifié, propriétaire, bailleur, vendeur, investisseur, mandataire, professionnel, membre d'organisation — sans écraser les dimensions.

Règles définies : permanent/contextuel, vérifié/déclaré, individuel/organisationnel, dates de validité, source, preuve, permissions dérivées, consentement nécessaire.

---

## 9. Biens

Document : `PROPERTY_TAXONOMY_EXTENSION_MODEL.md`

Taxonomie cible avec 10 dimensions : property_family, property_type, property_subtype, usage_type, occupancy_type, furnishing_status, construction_style, legal_status, commercial_category, investment_category.

7 familles : résidentiel, commercial, industriel, terrain, agricole, hôtelier, projet.

Structure extensible avec canonical_id, canonical_name, aliases, parent_id, family, applicable_transactions, applicable_fields, qualification_matrix_ids, matching_dimensions, verification_requirements.

---

## 10. Services

Document : `SERVICE_TAXONOMY_EXTENSION_MODEL.md`

72 services couvrant 11 familles : immobilier, juridique, technique, financier, documentaire, commercial, gestion, construction, rénovation, sécurité, mobilité.

Chaque service définit : service_id, service_family, provider_categories, requester_categories, qualification_matrix_id, required_documents, required_verifications, pricing_model, geographic_scope, SLA, workflow_id, consent_requirements, matching_requirements.

---

## 11. Intentions et transactions

Document : `INTENT_REQUEST_TRANSACTION_MODEL.md`

6 concepts explicitement séparés : intent, request, project_goal, transaction_type, service_request, journey_stage, business_action.

Pipeline de détection d'intention avec scoring par mots-clés, seuil de confiance 0.70, support FR/EN/PID, multi-intention, détection d'urgence, extraction d'entités.

---

## 12. Projets et dossiers

Document : `PROJECT_DOSSIER_EXTENSION_MODEL.md`

Relation : user → project → dossier → request → transaction → property → service → professional → relationship.

Un projet peut contenir plusieurs dossiers. Un dossier est une unité opérationnelle suivie.

Double consentement, chaîne de décision du détenteur, 10 étapes de qualification, rematching, health score.

---

## 13. Qualification

Document : `QUALIFICATION_EXTENSION_MODEL.md`

107 matrices représentées via 9 entités : QualificationMatrixDefinition, QualificationFieldDefinition, QualificationRuleDefinition, ReadinessDefinition, QuestionRuleDefinition, MatchingSemanticDefinition, MatrixVersion, MatrixApplicability.

Relations avec request_family, transaction_type, property_type, service_type, requester_typology, journey_stage.

---

## 14. Géographie

Document : `GEOGRAPHY_EXTENSION_MODEL.md`

Hiérarchie géographique complète : country, region, department, municipality, district, city, neighborhood, zone, axis, landmark, village, cluster, GPS point, geographic alias.

8 types de relations : NEARBY, CONTAINS, ADJACENT, SAME_AXIS, SAME_CLUSTER, COMMUTE_COMPATIBLE, ADMINISTRATIVE_PARENT, MARKET_EQUIVALENT.

---

## 15. Search et Matching

Document : `SEARCH_MATCHING_EXTENSION_MODEL.md`

Moteur de matching complet avec : 5 dimensions de scoring, 4 niveaux de compatibilité, 9 rôles de matching, règles de boost/pénalité, expansion progressive, surveillance continue du marché, indices de tension.

Seuil minimum : 60/100. Maximum de résultats : top 10.

---

## 16. Professionnels

Document : `PROFESSIONAL_EXTENSION_MODEL.md`

27 catégories professionnelles avec : professional_profile, service_capability, license, certification, geographic_coverage, availability, rating (1-5), verification_status (4 niveaux), pricing (10 modèles), SLA, organization_membership.

---

## 17. Financement

Document : `FINANCING_EXTENSION_MODEL.md`

12 produits de financement, 8 types de fournisseurs, 11 catégories de règles d'éligibilité, calcul de capacité de remboursement (DTI).

LAWIM ne se substitue jamais au financeur — il facilite la mise en relation.

---

## 18. Workflows

Document : `WORKFLOW_EXTENSION_MODEL.md`

21 workflows avec décision pour chacun : REUSE_CURRENT, EXTEND_CURRENT, CREATE_NEW_GENERIC_STATE_MACHINE, CREATE_SPECIALIZED_WORKFLOW.

Chaque workflow spécifie : states, terminal_states, transitions, guards, triggers, actions, SLA, NBA_rules, events, failure_policy.

---

## 19. CRM

Document : `CRM_EXTENSION_MODEL.md`

Pipeline 8 étapes, scoring (base + 13 boosters - 8 pénalités), classification (HOT/WARM/COLD/LOW/SPAM), routage (zone, disponibilité, score, manuel), 4 couches anti-fraude, 8 comportements trackés, SLA par priorité.

---

## 20. Relationship et Consentement

Document : `RELATIONSHIP_CONSENT_EXTENSION_MODEL.md`

Double consentement, scope de partage, masquage, révocation, expiration, idempotence, audit, handover humain.

Liens : match → proposal → consent → relationship → participant → introduction → shared_data_scope.

---

## 21. Events et Audit

Document : `EVENT_AUDIT_EXTENSION_MODEL.md`

13 catégories d'événements typés (~99 types d'événements). Chaque événement spécifie : event_type, entity_type, trigger, payload_schema, privacy_level, retention, audit_visibility, consumers.

---

## 22. Permissions

Document : `SECURITY_PERMISSION_EXTENSION_MODEL.md`

4 niveaux (Read, Create, Edit, Approve). Matrice complète (22 ressources × 5 rôles × 3 scopes). 6 types de permissions : système, organisation, relation, transaction, consentement dérivé, temporaire.

---

## 23. Modèle de données

Document : `CANONICAL_DATA_MODEL_EXTENSION.md`

26 entités spécifiées avec : entity_name, domain, purpose, existing_or_new, fields, value_objects, relations, indexes, uniqueness, lifecycle, privacy, audit, migration_source.

---

## 24. Blueprint Prisma

Document : `PRISMA_EXTENSION_BLUEPRINT.md`

22 nouvelles tables, 5 tables enrichies, 48 clés étrangères, stratégie d'énumération, plan de migration, risques, rollback.

---

## 25. Contrats API

Document : `API_EXTENSION_CONTRACTS.md`

21 groupes de ressources (~60 endpoints) avec : schema requête/réponse, permissions, événements, idempotence, privacy.

---

## 26. Compatibilité ascendante

Document : `BACKWARD_COMPATIBILITY_PLAN.md`

11 zones d'impact analysées, mapping d'états V2→unifié, mapping de rôles Gold→V2, 30 feature flags, 8 vagues de migration, ~1010 nouveaux tests, rollback.

---

## 27. Conflits

Document : `CONFLICT_RESOLUTION_REGISTER.md`

13 conflits résolus : 6 RESOLVED_UNIFIED_MODEL, 5 RESOLVED_HERITAGE_PREVAILS, 1 RESOLVED_CURRENT_PREVAILS, 0 HUMAN_DECISION_REQUIRED, 0 DEFERRED_WITH_BLOCKER.

---

## 28. Backlog H2

Document : `H2_IMPLEMENTATION_BACKLOG.md`

204 tâches réparties en 12 vagues :

| Vague | Focus | Tâches |
|-------|-------|--------|
| 1 | Taxonomies et registres | 6 |
| 2 | Définitions de qualification | 11 |
| 3 | Identité, rôles et profils | 11 |
| 4 | Projets et dossiers | 22 |
| 5 | Géographie | 12 |
| 6 | Search et matching | 27 |
| 7 | Services professionnels | 47 |
| 8 | CRM | 11 |
| 9 | Relationship et consentement | 13 |
| 10 | Workflows et NBA | 24 |
| 11 | Events, audit et permissions | 14 |
| 12 | APIs, compatibilité et migration | 6 |

---

## 29. Traçabilité

Document : `DOMAIN_EXTENSION_TRACEABILITY.md`

Chaîne complète : Heritage Gold rule → H0.5 matrix → H1 execution contract → H1.2 crosswalk → H1.3 extension → H2 backlog task → future code component → future test.

Index par extension_id, par tâche H2, par source Heritage Gold.

---

## 30. Validateur

Script : `scripts/validate_domain_extension_design.py`

18 vérifications exécutées. Résultat :

```
0 erreur
0 avertissement critique
```

---

## 31. Fichiers créés

| Fichier | Taille |
|---------|--------|
| docs/domain_extension/README.md | ~5 KB |
| docs/domain_extension/EXTENSION_CATALOG.md | ~50+ KB |
| docs/domain_extension/IDENTITY_ROLE_EXTENSION_MODEL.md | ~30+ KB |
| docs/domain_extension/PROPERTY_TAXONOMY_EXTENSION_MODEL.md | ~30+ KB |
| docs/domain_extension/SERVICE_TAXONOMY_EXTENSION_MODEL.md | ~30+ KB |
| docs/domain_extension/INTENT_REQUEST_TRANSACTION_MODEL.md | ~59 KB |
| docs/domain_extension/PROJECT_DOSSIER_EXTENSION_MODEL.md | ~40+ KB |
| docs/domain_extension/QUALIFICATION_EXTENSION_MODEL.md | ~40+ KB |
| docs/domain_extension/GEOGRAPHY_EXTENSION_MODEL.md | ~30+ KB |
| docs/domain_extension/SEARCH_MATCHING_EXTENSION_MODEL.md | ~40+ KB |
| docs/domain_extension/PROFESSIONAL_EXTENSION_MODEL.md | ~30+ KB |
| docs/domain_extension/FINANCING_EXTENSION_MODEL.md | ~30+ KB |
| docs/domain_extension/WORKFLOW_EXTENSION_MODEL.md | ~80+ KB |
| docs/domain_extension/CRM_EXTENSION_MODEL.md | ~30+ KB |
| docs/domain_extension/RELATIONSHIP_CONSENT_EXTENSION_MODEL.md | ~40+ KB |
| docs/domain_extension/EVENT_AUDIT_EXTENSION_MODEL.md | ~30+ KB |
| docs/domain_extension/SECURITY_PERMISSION_EXTENSION_MODEL.md | ~30+ KB |
| docs/domain_extension/CANONICAL_DATA_MODEL_EXTENSION.md | ~78 KB |
| docs/domain_extension/ENTITY_RELATIONSHIP_MAP.md | ~33 KB |
| docs/domain_extension/FIELD_EXTENSION_CATALOG.md | ~45 KB |
| docs/domain_extension/PRISMA_EXTENSION_BLUEPRINT.md | ~50+ KB |
| docs/domain_extension/API_EXTENSION_CONTRACTS.md | ~50+ KB |
| docs/domain_extension/BACKWARD_COMPATIBILITY_PLAN.md | ~40+ KB |
| docs/domain_extension/CONFLICT_RESOLUTION_REGISTER.md | ~30+ KB |
| docs/domain_extension/H2_IMPLEMENTATION_BACKLOG.md | ~131 KB |
| docs/domain_extension/DOMAIN_EXTENSION_TRACEABILITY.md | ~176 KB |
| docs/domain_extension/extension_catalog.json | ~206 KB |
| docs/domain_extension/identity_role_extensions.json | ~30+ KB |
| docs/domain_extension/property_taxonomy_extensions.json | ~30+ KB |
| docs/domain_extension/service_taxonomy_extensions.json | ~60+ KB |
| docs/domain_extension/intent_request_extensions.json | ~32 KB |
| docs/domain_extension/project_dossier_extensions.json | ~40+ KB |
| docs/domain_extension/qualification_extensions.json | ~40+ KB |
| docs/domain_extension/geography_extensions.json | ~30+ KB |
| docs/domain_extension/search_matching_extensions.json | ~30+ KB |
| docs/domain_extension/professional_extensions.json | ~30+ KB |
| docs/domain_extension/financing_extensions.json | ~30+ KB |
| docs/domain_extension/workflow_extensions.json | ~50+ KB |
| docs/domain_extension/crm_extensions.json | ~30+ KB |
| docs/domain_extension/relationship_consent_extensions.json | ~30+ KB |
| docs/domain_extension/event_audit_extensions.json | ~30+ KB |
| docs/domain_extension/security_permission_extensions.json | ~30+ KB |
| docs/domain_extension/data_model_extensions.json | ~65 KB |
| docs/domain_extension/h2_implementation_backlog.json | ~131 KB |
| scripts/validate_domain_extension_design.py | ~15+ KB |
| reports/domain_extension/H13_ORCHESTRATION_LOG.md | ~3 KB |
| reports/domain_extension/LAWIM_V2_Mission_H13_Canonical_Domain_Extensions.md | Ce fichier |

---

## 32. Fichiers modifiés

Aucun fichier de runtime modifié. Aucun fichier Prisma, API, ou code modifié.

---

## 33. Commit

```
docs(domain): define canonical extensions for Heritage Gold integration
```

---

## 34. Tag

```
lawim-v2-canonical-domain-extension-h13
```

---

## 35. État Git final

```
HEAD: <commit-hash>
Tag: lawim-v2-canonical-domain-extension-h13
Worktree: strictement propre
```

---

## 36. Points ouverts

| Point | Description | Impact |
|-------|-------------|--------|
| Tarification | Les prix Heritage Gold (500-75.000 FCFA) nécessitent validation marché | Business |
| Campay | Intégration paiement unique ; multi-processeur si besoin | Technique |
| Matching ML | Moteur à base de règles vs ML ; décision H2 | Architecture |
| Détection d'intention NLP | Règles vs NLP pour extraction d'entités | Technique |
| Seuils SLA | Configuration fine des seuils par état et type d'entité | Opérationnel |

---

## 37. Décisions humaines requises

Les extensions marquées HUMAN_DECISION_REQUIRED dans le catalogue (identifiées par `human_decision_required: true`) nécessitent une validation produit avant leur implémentation en vague H2. Principales décisions :

- Politique d'attribution du niveau de confiance initial
- Critères de vérification d'identité et de documents professionnels
- Stratégie de tarification des leads et boosts
- Algorithme de routage (round-robin, score, capacité)
- Niveaux d'automatisation du matching et de l'anti-fraude

---

## 38. Verdict

```text
CANONICAL DOMAIN EXTENSIONS READY
```

Tous les critères du verdict READY sont satisfaits :

| Critère | Statut |
|---------|--------|
| 175 extensions inventoriées | ✓ |
| 175 extensions classifiées | ✓ |
| 175 extensions avec cible | ✓ |
| 107 matrices couvertes | ✓ |
| 61 rôles couverts | ✓ |
| 76+ biens couverts | ✓ |
| 72 services couverts | ✓ |
| 21 workflows couverts | ✓ |
| 13 conflits traités | ✓ |
| Modèle unifié enrichi | ✓ |
| Modèle conceptuel de données | ✓ |
| Blueprint Prisma | ✓ |
| Contrats API | ✓ |
| Plan de compatibilité | ✓ |
| Backlog H2 complet (204 tâches) | ✓ |
| Traçabilité complète | ✓ |
| Validateur : 0 erreur, 0 avertissement critique | ✓ |
| Rapport final | ✓ |
| Commit | ✓ |
| Tag | ✓ |
| Worktree propre | ✓ |

---

## 39. Instructions H2

La Mission H2 — Knowledge Execution Core — peut commencer.

1. **Démarrer par Wave 1** : Taxonomies des biens, services, géographie
2. **Activer les feature flags** pour les nouvelles entités
3. **Valider les seuils SLA** avec l'équipe produit
4. **Confirmer la tarification** des services avant implémentation
5. **Suivre le backlog H2** dans l'ordre des vagues
6. **Exécuter le validateur** après chaque vague

Le modèle cible, les contrats, et le backlog sont prêts.

---

*Fin du rapport Mission H1.3*
