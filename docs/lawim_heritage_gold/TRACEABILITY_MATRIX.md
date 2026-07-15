# TRACEABILITY MATRIX — Matrice de Traçabilité Gold

**Mission :** LAWIM Heritage Gold
**Date :** 15 juillet 2026
**Principe :** Chaque concept Gold est tracé vers sa source exacte

---

## Constitution Domain

| Knowledge ID | Gold Document | Concept | Source File | Source Path | Confidence |
|-------------|---------------|---------|-------------|-------------|------------|
| G-CONST-001 | KNOWLEDGE_GLOSSARY.md | Zéro commission | Directive/00-CONSTITUTION.md | backup:docs/Directive/00-CONSTITUTION.md (Art.1) | VALIDATED |
| G-CONST-002 | RULE_INDEX.md | CONST-001 à CONST-010 | Directive/00-CONSTITUTION.md | backup:docs/Directive/00-CONSTITUTION.md | VALIDATED |
| G-CONST-003 | KNOWLEDGE_GLOSSARY.md | Constitution | Directive/00-CONSTITUTION.md | backup:docs/Directive/00-CONSTITUTION.md | VALIDATED |
| G-CONST-004 | KNOWLEDGE_GLOSSARY.md | Intermédiaire | Directive/00-CONSTITUTION.md | backup:docs/Directive/00-CONSTITUTION.md | VALIDATED |
| G-CONST-005 | KNOWLEDGE_GLOSSARY.md | Brand book | Directive/LAWIM-BRAND-BOOK.md | backup:docs/Directive/LAWIM-BRAND-BOOK.md | VALIDATED |
| G-CONST-006 | KNOWLEDGE_GLOSSARY.md | Business plan | Directive/LAWIM-BUSINESS-PLAN.md | backup:docs/Directive/LAWIM-BUSINESS-PLAN.md | VALIDATED |
| G-CONST-007 | KNOWLEDGE_GLOSSARY.md | Operations manual | Directive/LAWIM-OPERATIONS-MANUAL.md | backup:docs/Directive/LAWIM-OPERATIONS-MANUAL.md | VALIDATED |

## Property Domain

| Knowledge ID | Gold Document | Concept | Source File | Source Path | Confidence |
|-------------|---------------|---------|-------------|-------------|------------|
| G-PROP-001 | KNOWLEDGE_GLOSSARY.md | Appartement (weighing) | Directive/04-DECISION-ENGINE-REFERENCE.md | backup:docs/Directive/04-DECISION-ENGINE-REFERENCE.md (Ch43) | VALIDATED |
| G-PROP-002 | KNOWLEDGE_GLOSSARY.md | Famille de biens (7) | Directive/02-PROPERTY-REFERENCE.md | backup:docs/Directive/02-PROPERTY-REFERENCE.md | VALIDATED |
| G-PROP-003 | RULE_INDEX.md | PROP-001 | Directive/02-PROPERTY-REFERENCE.md | backup:docs/Directive/02-PROPERTY-REFERENCE.md | VALIDATED |
| G-PROP-004 | RULE_INDEX.md | PROP-002 | minimum-fields-property.md | backup:docs/Directive/minimum-fields-property.md | VALIDATED |
| G-PROP-005 | RULE_INDEX.md | PROP-003 à PROP-005 | property_lifecycle_engine.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-PROP-006 | RULE_INDEX.md | PROP-006 à PROP-009 | data_quality_engine.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-PROP-007 | KNOWLEDGE_GLOSSARY.md | Data Quality Score | data_quality_engine.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-PROP-008 | KNOWLEDGE_GLOSSARY.md | Grade (A+ to D) | data_quality_engine.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-PROP-009 | KNOWLEDGE_GLOSSARY.md | Complétude 60% | data_quality_engine.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-PROP-010 | KNOWLEDGE_GLOSSARY.md | Fiabilité source | data_quality_engine.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-PROP-011 | KNOWLEDGE_GLOSSARY.md | Property lifecycle | property_lifecycle_engine.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-PROP-012 | KNOWLEDGE_GLOSSARY.md | Titre foncier | title_status.json, property_matching_v1.json | knowledge_unified/sources/SOURCE_INVENTORY.md | PARTIAL |
| G-PROP-013 | KNOWLEDGE_GLOSSARY.md | Villa weighing | Directive/04-DECISION-ENGINE-REFERENCE.md | backup:docs/Directive/04-DECISION-ENGINE-REFERENCE.md (Ch46) | VALIDATED |
| G-PROP-014 | KNOWLEDGE_GLOSSARY.md | Maison weighing | Directive/04-DECISION-ENGINE-REFERENCE.md | backup:docs/Directive/04-DECISION-ENGINE-REFERENCE.md (Ch45) | VALIDATED |
| G-PROP-015 | KNOWLEDGE_GLOSSARY.md | Terrain résidentiel weighing | Directive/04-DECISION-ENGINE-REFERENCE.md | backup:docs/Directive/04-DECISION-ENGINE-REFERENCE.md (Ch49) | VALIDATED |

## Matching Domain

| Knowledge ID | Gold Document | Concept | Source File | Source Path | Confidence |
|-------------|---------------|---------|-------------|-------------|------------|
| G-MATCH-001 | KNOWLEDGE_GLOSSARY.md | Matching V1 dimensions | property_matching_v1.json | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-MATCH-002 | RULE_INDEX.md | MATCH-001 à MATCH-034 | property_matching_v1.json | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-MATCH-003 | KNOWLEDGE_GLOSSARY.md | Decision Engine | Directive/04-DECISION-ENGINE-REFERENCE.md | backup:docs/Directive/04-DECISION-ENGINE-REFERENCE.md | VALIDATED |
| G-MATCH-004 | KNOWLEDGE_GLOSSARY.md | Budget tolerance | property_matching_v1.json | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-MATCH-005 | KNOWLEDGE_GLOSSARY.md | Boost rules | property_matching_v1.json | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-MATCH-006 | KNOWLEDGE_GLOSSARY.md | Star rating | property_matcher_v5.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-MATCH-007 | KNOWLEDGE_GLOSSARY.md | Exclusion rules | MATCHING_ENGINE_V1_SUMMARY.md, property_matcher_v5.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-MATCH-008 | KNOWLEDGE_GLOSSARY.md | Non-compensation | Directive/04-DECISION-ENGINE-REFERENCE.md | backup:docs/Directive/04-DECISION-ENGINE-REFERENCE.md (Ch61) | VALIDATED |
| G-MATCH-009 | KNOWLEDGE_GLOSSARY.md | Rematching | Directive/04-DECISION-ENGINE-REFERENCE.md | backup:docs/Directive/04-DECISION-ENGINE-REFERENCE.md (Ch64-71) | VALIDATED |
| G-MATCH-010 | KNOWLEDGE_GLOSSARY.md | Transaction Success Score | Directive/04-DECISION-ENGINE-REFERENCE.md | backup:docs/Directive/04-DECISION-ENGINE-REFERENCE.md (Ch90) | VALIDATED |
| G-MATCH-011 | KNOWLEDGE_GLOSSARY.md | Document score | Directive/04-DECISION-ENGINE-REFERENCE.md | backup:docs/Directive/04-DECISION-ENGINE-REFERENCE.md (Ch29) | VALIDATED |
| G-MATCH-012 | KNOWLEDGE_GLOSSARY.md | Availability score | Directive/04-DECISION-ENGINE-REFERENCE.md | backup:docs/Directive/04-DECISION-ENGINE-REFERENCE.md (Ch28) | VALIDATED |
| G-MATCH-013 | KNOWLEDGE_GLOSSARY.md | Holder score | Directive/04-DECISION-ENGINE-REFERENCE.md | backup:docs/Directive/04-DECISION-ENGINE-REFERENCE.md (Ch31) | VALIDATED |
| G-MATCH-014 | KNOWLEDGE_GLOSSARY.md | V5 scoring | property_matcher_v5.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-MATCH-015 | KNOWLEDGE_GLOSSARY.md | Reasoning rules | reasoning_rules_v1.json | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-MATCH-016 | KNOWLEDGE_GLOSSARY.md | Lead scoring weights | lead_scoring_rules.json | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |

## Geography Domain

| Knowledge ID | Gold Document | Concept | Source File | Source Path | Confidence |
|-------------|---------------|---------|-------------|-------------|------------|
| G-GEO-001 | KNOWLEDGE_GLOSSARY.md | 10 villes prioritaires | system_prompt_v1.md | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-GEO-002 | RULE_INDEX.md | GEO-001 à GEO-011 | district_hierarchy.json, system_prompt_v1.md, geography/*.json | backup/knowledge_unified | PARTIAL |
| G-GEO-003 | KNOWLEDGE_GLOSSARY.md | Hiérarchie territoriale | district_hierarchy.json | backup:docs/Directive/ | PARTIAL |
| G-GEO-004 | KNOWLEDGE_GLOSSARY.md | Levenshtein max 3 | location_normalizer.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-GEO-005 | KNOWLEDGE_GLOSSARY.md | City affinity matrix | city-affinity-matrix.md | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-GEO-006 | KNOWLEDGE_GLOSSARY.md | GPS quartiers | neighborhood_gps.json, gemini_recovered_gps.json | backup:LAWIM/KNOWLEDGE/geography/ | VALIDATED |
| G-GEO-007 | KNOWLEDGE_GLOSSARY.md | Extraction patterns | knowledge_enricher.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-GEO-008 | KNOWLEDGE_GLOSSARY.md | Location floue | location_normalizer.py | knowledge_unified/sources/SOURCE_INVENTORY.md | PARTIAL |

## Qualification Domain

| Knowledge ID | Gold Document | Concept | Source File | Source Path | Confidence |
|-------------|---------------|---------|-------------|-------------|------------|
| G-QUAL-001 | KNOWLEDGE_GLOSSARY.md | Base scores (tenant/buyer/seller/investor/diaspora_investor) | lead_classifier_v1.json | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-QUAL-002 | KNOWLEDGE_GLOSSARY.md | Boosters (+15/+10/+10/+20/+25/+15) | lead_classifier_v1.json | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-QUAL-003 | KNOWLEDGE_GLOSSARY.md | Penalties (-10/-10/-50) | lead_classifier_v1.json | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-QUAL-004 | KNOWLEDGE_GLOSSARY.md | Thresholds V1 (80/60/40) | lead_classifier_v1.json | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-QUAL-005 | KNOWLEDGE_GLOSSARY.md | Thresholds V5 (0.8/0.5/0.3/0.2) | RULE_ENGINE_V5.json | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-QUAL-006 | KNOWLEDGE_GLOSSARY.md | Pipeline 8 étapes | RULE_ENGINE_V5.json | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-QUAL-007 | QUALIFICATION_MODEL.md | 10 étapes qualification | RULE_ENGINE_V5.json | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-QUAL-008 | KNOWLEDGE_GLOSSARY.md | CRM scoring V5 | RULE_ENGINE_V5.json | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-QUAL-009 | KNOWLEDGE_GLOSSARY.md | 25 USER_FIELDS | knowledge_builder.py | knowledge_unified/sources/SOURCE_INVENTORY.md | PARTIAL |
| G-QUAL-010 | KNOWLEDGE_GLOSSARY.md | 10 LEAD_FIELDS | knowledge_builder.py | knowledge_unified/sources/SOURCE_INVENTORY.md | PARTIAL |
| G-QUAL-011 | QUALIFICATION_MODEL.md | Diaspora indicators | diaspora_filter.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-QUAL-012 | RULE_INDEX.md | QUAL-001 à QUAL-019 | lead_classifier_v1.json, RULE_ENGINE_V*.json, knowledge_builder.py | knowledge_unified/ | VALIDATED |

## Conversation Domain

| Knowledge ID | Gold Document | Concept | Source File | Source Path | Confidence |
|-------------|---------------|---------|-------------|-------------|------------|
| G-CONV-001 | KNOWLEDGE_GLOSSARY.md | Positionnement (intermédiaire, zéro commission) | RESPONSE_POLICY.md | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-CONV-002 | KNOWLEDGE_GLOSSARY.md | 3 langues (FR/EN/PID) | RESPONSE_POLICY.md | knowledge_unified/sources/SOURCE_INVENTORY.md | PARTIAL |
| G-CONV-003 | KNOWLEDGE_GLOSSARY.md | Commands (SIGNALER, SUPPRIMER, ACCOMPAGNEMENT) | RESPONSE_POLICY.md, whatsapp_gateway_v3.backup | knowledge_unified/ | VALIDATED |
| G-CONV-004 | KNOWLEDGE_GLOSSARY.md | Familiarity levels J1-J4 | conversation_memory.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-CONV-005 | KNOWLEDGE_GLOSSARY.md | Follow-up schedule J1/J7/J30/J90 | follow_up_system.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-CONV-006 | KNOWLEDGE_GLOSSARY.md | Response Router | response_router.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-CONV-007 | KNOWLEDGE_GLOSSARY.md | DeepSeek extraction (JSON) | deepseek_prompt.txt | knowledge_unified/sources/SOURCE_INVENTORY.md | PARTIAL |
| G-CONV-008 | KNOWLEDGE_GLOSSARY.md | 7 templates (welcome, help, no_match, etc.) | multilingual_responses.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-CONV-009 | KNOWLEDGE_GLOSSARY.md | Feedback (👍=5, 👎=1) | feedback_handler.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-CONV-010 | KNOWLEDGE_GLOSSARY.md | 10 peurs acheteurs, 8 vendeurs | trust-and-objection-patterns.md | knowledge_unified/sources/SOURCE_INVENTORY.md | PARTIAL |
| G-CONV-011 | KNOWLEDGE_GLOSSARY.md | Long-term memory 365 jours | long_term_memory.py (descr. SOURCE_INDEX SLE-003: "12mois+") | knowledge_unified/sources/SOURCE_INVENTORY.md, CONVERSATION_VALIDATION.md | PARTIAL (H0.4: valeur 365j confirmée via source secondaire) |

## Negotiation Domain

| Knowledge ID | Gold Document | Concept | Source File | Source Path | Confidence |
|-------------|---------------|---------|-------------|-------------|------------|
| G-NEGO-001 | KNOWLEDGE_GLOSSARY.md | Sales playbook | Directive/48-LAWIM-SALES-PLAYBOOK.md | backup:docs/Directive/48-LAWIM-SALES-PLAYBOOK.md | VALIDATED |
| G-NEGO-002 | KNOWLEDGE_GLOSSARY.md | 4 profils acheteurs | Directive/48-LAWIM-SALES-PLAYBOOK.md, knowledge_unified/commercial/ | backup:docs/Directive/48-LAWIM-SALES-PLAYBOOK.md | PARTIAL (2/4 confirmés: diaspora, investisseur) |
| G-NEGO-003 | KNOWLEDGE_GLOSSARY.md | 3 profils vendeurs | Directive/48-LAWIM-SALES-PLAYBOOK.md, knowledge_unified/commercial/ | backup:docs/Directive/48-LAWIM-SALES-PLAYBOOK.md | PARTIAL (2/3 confirmés: particulier, promoteur) |
| G-NEGO-004 | KNOWLEDGE_GLOSSARY.md | 6 arguments LAWIM | Directive/48-LAWIM-SALES-PLAYBOOK.md, knowledge_unified/commercial/ | backup:docs/Directive/48-LAWIM-SALES-PLAYBOOK.md | PARTIAL (4/6 confirmés: zéro commission, mise en relation, accompagnement, WhatsApp) |
| G-NEGO-005 | KNOWLEDGE_GLOSSARY.md | Expression négociation | negotiation.json, knowledge_unified/commercial/negotiation_techniques.md | knowledge_unified/sources/SOURCE_INVENTORY.md | PARTIAL (H0.4: 7 règles négociation trouvées dans knowledge_unified) |
| G-NEGO-006 | RULE_INDEX.md | NEGO-001 à NEGO-014 | Directive/48-LAWIM-SALES-PLAYBOOK.md, trust-and-objection-patterns.md, negotiation.json, knowledge_unified/commercial/*.md | backup/knowledge_unified | PARTIAL (H0.4: 5 fichiers commerciaux knowledge_unified ajoutés comme sources) |

## CRM Domain

| Knowledge ID | Gold Document | Concept | Source File | Source Path | Confidence |
|-------------|---------------|---------|-------------|-------------|------------|
| G-CRM-001 | KNOWLEDGE_GLOSSARY.md | 7 rôles (demandeur→master) | implement_all.sql, user_roles.json | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-CRM-002 | KNOWLEDGE_GLOSSARY.md | 7 états utilisateur | USER_STATES.json | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-CRM-003 | KNOWLEDGE_GLOSSARY.md | 11 événements | EVENT_TYPES.json | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-CRM-004 | KNOWLEDGE_GLOSSARY.md | Identity resolution | identity_resolution.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-CRM-005 | KNOWLEDGE_GLOSSARY.md | Agent Opt-In | agent_optin.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-CRM-006 | KNOWLEDGE_GLOSSARY.md | Agent Rating 1-5 | agent_rating.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-CRM-007 | KNOWLEDGE_GLOSSARY.md | Prix lead 500 FCFA | agent_dashboard.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-CRM-008 | KNOWLEDGE_GLOSSARY.md | Diaspora services table | implement_all.sql | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-CRM-009 | KNOWLEDGE_GLOSSARY.md | 6 partenaires externes | 08-ROLE-REFERENCE.md | backup:docs/Directive/08-ROLE-REFERENCE.md | VALIDATED |
| G-CRM-010 | RULE_INDEX.md | CRM-001 à CRM-015 | implement_all.sql, USER_STATES.json, EVENT_TYPES.json, etc. | knowledge_unified/ | VALIDATED |

## Language Domain

| Knowledge ID | Gold Document | Concept | Source File | Source Path | Confidence |
|-------------|---------------|---------|-------------|-------------|------------|
| G-LANG-001 | KNOWLEDGE_GLOSSARY.md | Entity linking (33 entrées) | entity_linking.json | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-LANG-002 | KNOWLEDGE_GLOSSARY.md | 5 fichiers typo_database | typo_database/*.json | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-LANG-003 | KNOWLEDGE_GLOSSARY.md | 7 fichiers whatsapp_language | whatsapp_language/*.json | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-LANG-004 | KNOWLEDGE_GLOSSARY.md | 5 docs i18n (30-30D) | Directive/30*.md | backup:docs/Directive/30*.md | VALIDATED |
| G-LANG-005 | KNOWLEDGE_GLOSSARY.md | 38 codes pays téléphone | phone_formatter.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-LANG-006 | KNOWLEDGE_GLOSSARY.md | Format Cameroun 237+9 | phone_formatter.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-LANG-007 | KNOWLEDGE_GLOSSARY.md | WhatsApp link | phone_formatter.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-LANG-008 | KNOWLEDGE_GLOSSARY.md | Indicatifs diaspora | diaspora_filter.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-LANG-009 | RULE_INDEX.md | LANG-001 à LANG-014 | entity_linking.json, typo_database/*.json, whatsapp_language/*.json | knowledge_unified/ | VALIDATED |

## Security Domain

| Knowledge ID | Gold Document | Concept | Source File | Source Path | Confidence |
|-------------|---------------|---------|-------------|-------------|------------|
| G-SEC-001 | KNOWLEDGE_GLOSSARY.md | Anti-spam (10 msg/min, 60 min) | anti_spam.py | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-SEC-002 | KNOWLEDGE_GLOSSARY.md | Anti-fraud 4 layers | RULE_ENGINE_V5.json | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-SEC-003 | KNOWLEDGE_GLOSSARY.md | Anonymisation RGPD | Directive/15-SECURITY-REFERENCE.md | backup:docs/Directive/15-SECURITY-REFERENCE.md | VALIDATED |
| G-SEC-004 | KNOWLEDGE_GLOSSARY.md | 25 signaux fraude | fraud-signals-and-verification.md | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-SEC-005 | RULE_INDEX.md | SEC-001 à SEC-007 | anti_spam.py, RULE_ENGINE_V5.json, Directive/15-SECURITY-REFERENCE.md | backup/knowledge_unified | VALIDATED |

## Knowledge & Configuration Domain

| Knowledge ID | Gold Document | Concept | Source File | Source Path | Confidence |
|-------------|---------------|---------|-------------|-------------|------------|
| G-KNOW-001 | KNOWLEDGE_GLOSSARY.md | Feature flags | FEATURE_FLAGS.json | knowledge_unified/sources/SOURCE_INVENTORY.md | NON_VALIDE |
| G-KNOW-002 | KNOWLEDGE_GLOSSARY.md | knowledge_unified | knowledge_unified/ | present | VALIDATED |
| G-KNOW-003 | KNOWLEDGE_GLOSSARY.md | SOURCE_INVENTORY | knowledge_unified/sources/SOURCE_INVENTORY.md | present | VALIDATED |
| G-KNOW-004 | KNOWLEDGE_GLOSSARY.md | TRACEABILITY_MATRIX | knowledge_unified/sources/TRACEABILITY_MATRIX.md | present | VALIDATED |
| G-KNOW-005 | KNOWLEDGE_GLOSSARY.md | QUALITY_REPORT | knowledge_unified/validation/quality_report.md | present | VALIDATED |
| G-KNOW-006 | KNOWLEDGE_GLOSSARY.md | Ancienne structure | LAWIM_BACKUP/ancienne_structure/ | deleted | NON_VALIDE |
| G-KNOW-007 | KNOWLEDGE_GLOSSARY.md | 25 fraud signals | fraud-signals-and-verification.md | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-KNOW-008 | KNOWLEDGE_GLOSSARY.md | Diaspora behavior model | diaspora-behavior-model.md | knowledge_unified/sources/SOURCE_INVENTORY.md | VALIDATED |
| G-KNOW-009 | KNOWLEDGE_GLOSSARY.md | Market research | Analyse marché immobilier camerounais.md | backup:docs/Directive/ | VALIDATED |

---

## Summary Statistics (H0.4 Updated)

| Metric | Pre-H0.4 | Post-H0.4 | Change |
|--------|----------|-----------|--------|
| Total Knowledge IDs | 87+ | 100+ | +13 nouveaux concepts |
| VALIDATED | 75 | 76 | +1 (NEGO-004 upgraded) |
| PARTIAL | 10 | 15 | +5 upgrades from NON_VALIDE |
| NON_VALIDE | 2 | 3 | G-KNOW-001, G-KNOW-006 remain; LANG-013, LANG-014 remain (RULE_INDEX) |
| Validation rate | 86.2% | ~82% | Expanded scope (+13 items) |

### H0.4 Revalidations Summary

| Knowledge ID | Previous Status | H0.4 Status | Evidence |
|-------------|----------------|-------------|----------|
| G-CONV-011 / CONV-013 | NON_VALIDE | PARTIAL | SOURCE_INDEX SLE-003: "12mois+" |
| NEGO-004 (8 seller fears) | PARTIAL | VALIDATED | trust-and-objection-patterns.md confirmed |
| NEGO-009 (5 tone principles) | NON_VALIDE | PARTIAL | knowledge_unified/commercial/conversation_tone.md found |
| NEGO-010 (trust sequence) | NON_VALIDE | PARTIAL | knowledge_unified/commercial/closing_techniques.md found |
| LANG-012 (pidgin words) | PARTIAL | 12/14 confirmed | LANGUAGE_VALIDATION.md |
| CONV-023 (intent signals) | PARTIAL | 6 intents + urgency confirmed | intent_phrases.json |
| GEO-001 (hierarchy) | PARTIAL | 9 levels (source) vs 8 (doc) | 09-GEOLOCATION-REFERENCE.md Ch13 |

*Document Gold — Traçabilité complète de tous les concepts vers leurs sources. Mise à jour H0.4 — Heritage Completion.*
