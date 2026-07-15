# Traceability Matrix: Legacy LAWIM → knowledge_unified/

## Matrix Date: 2026-07-15

| Knowledge ID | Domain | Source in Legacy LAWIM | Status in LAWIM_V2 | Decision | File in knowledge_unified/ | Confidence | Conflicts |
|---|---|---|---|---|---|---|---|
| GEO-001 | geography | KNOWLEDGE/geography/cameroon_geography.json | Migrated | KEEP | geography/cities.json | HIGH | None |
| GEO-002 | geography | KNOWLEDGE/geography/cameroon_geography_v2_backup.json | Merged | MERGE | geography/cities.json | HIGH | Merged v1+v2 coordinates |
| GEO-003 | geography | KNOWLEDGE/cities/cameroon_cities.json | Migrated | MERGE | geography/cities.json | HIGH | Aliases merged from both sources |
| GEO-004 | geography | KNOWLEDGE/cities/cameroon_geography_before_mass_gps_20260610_084253.json | Archived | REJECT | N/A (historical reference) | MEDIUM | Superseded by v2 |
| GEO-005 | geography | KNOWLEDGE/geography/neighborhood_inventory_final.json | Migrated | KEEP | geography/neighborhoods.json | HIGH | None |
| GEO-006 | geography | KNOWLEDGE/geography/neighborhood_inventory.json | Merged | MERGE | geography/neighborhoods.json | MEDIUM | Raw → clean → final pipeline |
| GEO-007 | geography | KNOWLEDGE/geography/district_aliases_v3.json | Migrated | KEEP | geography/aliases.json | HIGH | None |
| GEO-008 | geography | KNOWLEDGE/geography/district_aliases_v2.json | Merged | MERGE | geography/aliases.json | HIGH | Merged v2+v3 aliases |
| GEO-009 | geography | KNOWLEDGE/geography/district_aliases.json | Merged | MERGE | geography/aliases.json | MEDIUM | Superseded by v2/v3 |
| GEO-010 | geography | KNOWLEDGE/geography/district_hierarchy.json | Migrated | KEEP | geography/aliases.json (district_hierarchy) | HIGH | None |
| GEO-011 | geography | KNOWLEDGE/location-segmentation-canonical.md | Migrated | KEEP | geography/proximity_rules.json | HIGH | None |
| GEO-012 | geography | KNOWLEDGE/location-segmentation-discovery.md | Archived | REJECT | N/A (superseded by canonical) | MEDIUM | Discovery doc, not canonical |
| GEO-013 | geography | KNOWLEDGE/geography/gemini_recovered_gps.json | Update pending | UPDATE | geography/cities.json | LOW | GPS values need verification |
| GEO-014 | geography | KNOWLEDGE/geography/neighborhood_gps.json | Update pending | UPDATE | geography/cities.json | LOW | GPS data not yet incorporated |
| QUAL-001 | qualification | KNOWLEDGE/roles-matrix.md | Migrated | KEEP | qualification/user_typologies.json | HIGH | None |
| QUAL-002 | qualification | KNOWLEDGE/conversation-patterns.md | Migrated | KEEP | qualification/user_typologies.json | HIGH | None |
| QUAL-003 | qualification | KNOWLEDGE/intents/buy_property.json | Merged | MERGE | qualification/intentions.json | HIGH | Merged across all intents |
| QUAL-004 | qualification | KNOWLEDGE/intents/rent_property.json | Merged | MERGE | qualification/intentions.json | HIGH | Merged across all intents |
| QUAL-005 | qualification | KNOWLEDGE/intents/sell_property.json | Merged | MERGE | qualification/intentions.json | HIGH | Merged across all intents |
| QUAL-006 | qualification | KNOWLEDGE/intents/investor_intent.json | Migrated | KEEP | qualification/intentions.json | HIGH | None |
| QUAL-007 | qualification | KNOWLEDGE/intents/search_property.json | Migrated | KEEP | qualification/intentions.json | HIGH | None |
| QUAL-008 | qualification | KNOWLEDGE/property-qualification-reference.md | Migrated | KEEP | qualification/property_search_matrices.json | HIGH | None |
| QUAL-009 | qualification | KNOWLEDGE/conversation-qualification-questions.md | Migrated | KEEP | qualification/property_search_matrices.json | HIGH | None |
| QUAL-010 | qualification | KNOWLEDGE/18_QUALIFICATION_MATRIX_IMPLEMENTATION.md | Migrated | KEEP | qualification/*_matrices.json | HIGH | None |
| QUAL-011 | qualification | KNOWLEDGE/qualification-implementation-backlog.md | Partial | UPDATE | qualification/qualification_rules.md | MEDIUM | Backlog items not yet implemented |
| QUAL-012 | qualification | KNOWLEDGE/minimum-fields-property.md | Migrated | KEEP | qualification/property_search_matrices.json | HIGH | None |
| QUAL-013 | qualification | KNOWLEDGE/minimum-fields-request.md | Migrated | KEEP | qualification/property_search_matrices.json | HIGH | None |
| MATCH-001 | matching | KNOWLEDGE/4-Matching Engine LAWIM.docx | Migrated | KEEP | matching/matching_dimensions.json | HIGH | None |
| MATCH-002 | matching | KNOWLEDGE/MATCHING_ENGINE_V1_SUMMARY.md | Migrated | KEEP | matching/matching_dimensions.json | HIGH | None |
| MATCH-003 | matching | KNOWLEDGE/MATCHING_ENGINE_V1_IMPLEMENTATION_SCOPE.md | Archived | REJECT | N/A (scope doc, superseded) | MEDIUM | Implementation plan, not spec |
| MATCH-004 | matching | KNOWLEDGE/MATCHING_ENGINE_PHASE0_ARCHITECTURE.md | Partial | UPDATE | matching/*.json | MEDIUM | Phase 0 arch outdated vs current design |
| MATCH-005 | matching | KNOWLEDGE/scoring/lead_scoring_rules.json | Migrated | KEEP | matching/scoring_rules.json | HIGH | None |
| MATCH-006 | matching | KNOWLEDGE/master/05_SCORING_V1.md | Reference | KEEP | matching/scoring_rules.json | HIGH | None |
| LANG-001 | language | KNOWLEDGE/whatsapp_language/whatsapp_language.json | Migrated | KEEP | language/common_expressions.json | HIGH | None |
| LANG-002 | language | KNOWLEDGE/whatsapp_language/diaspora_language.json | Merged | MERGE | language/common_expressions.json | HIGH | Merged into common expressions |
| LANG-003 | language | KNOWLEDGE/whatsapp_language/investor_language.json | Merged | MERGE | language/common_expressions.json | HIGH | Merged into common expressions |
| LANG-004 | language | KNOWLEDGE/whatsapp_language/negotiation.json | Migrated | KEEP | language/common_expressions.json | HIGH | None |
| LANG-005 | language | KNOWLEDGE/whatsapp_language/property_listing.json | Migrated | KEEP | language/common_expressions.json | HIGH | None |
| LANG-006 | language | KNOWLEDGE/whatsapp_language/property_search.json | Migrated | KEEP | language/common_expressions.json | HIGH | None |
| LANG-007 | language | KNOWLEDGE/whatsapp_language/urgency_signals.json | Migrated | KEEP | language/common_expressions.json (urgency_signals) | HIGH | None |
| LANG-008 | language | KNOWLEDGE/conversation-humanization-rules.md | Migrated | KEEP | language/cameroon_expressions.json | HIGH | None |
| LANG-009 | language | KNOWLEDGE/typo_database/typo_database.json | Migrated | KEEP | language/spelling_variants.json | HIGH | None |
| LANG-010 | language | KNOWLEDGE/typo_database/cities_typo.json | Merged | MERGE | language/spelling_variants.json | HIGH | Merged into variants |
| LANG-011 | language | KNOWLEDGE/typo_database/neighborhoods_typo.json | Merged | MERGE | language/spelling_variants.json | HIGH | Merged into variants |
| LANG-012 | language | KNOWLEDGE/typo_database/property_types_typo.json | Merged | MERGE | language/spelling_variants.json | HIGH | Merged into variants |
| LANG-013 | language | KNOWLEDGE/typo_database/whatsapp_typo.json | Merged | MERGE | language/abbreviations.json | HIGH | WhatsApp-specific typos |
| LANG-014 | language | KNOWLEDGE/multilingual-conversation-guidelines.md | Migrated | KEEP | language/common_expressions.json | HIGH | None |
| COMM-001 | commercial | KNOWLEDGE/negotiation-patterns.md | Migrated | KEEP | commercial/negotiation_techniques.md | HIGH | None |
| COMM-002 | commercial | KNOWLEDGE/trust-and-objection-patterns.md | Migrated | KEEP | commercial/objection_handling.md | HIGH | None |
| COMM-003 | commercial | KNOWLEDGE/conversation-style-guide.md | Migrated | KEEP | commercial/conversation_tone.md | HIGH | None |
| COMM-004 | commercial | KNOWLEDGE/channel-tone-guidelines.md | Migrated | KEEP | commercial/conversation_tone.md | HIGH | None |
| COMM-005 | commercial | KNOWLEDGE/response-policy.md | Migrated | KEEP | commercial/follow_up_strategies.md | HIGH | None |
| COMM-006 | commercial | KNOWLEDGE/omnichannel-playbook.md | Partial | UPDATE | commercial/follow_up_strategies.md | MEDIUM | Omnichannel rules partially applied |
| COMM-007 | commercial | KNOWLEDGE/telegram-runtime.md | Migrated | UPDATE | commercial/conversation_tone.md | MEDIUM | Telegram-specific rules need verification |
| COMM-008 | commercial | KNOWLEDGE/facebook-page-profile.md | External ref | UPDATE | commercial/conversation_tone.md | MEDIUM | Facebook channel rules not fully canonical |
| PROF-001 | professionals | KNOWLEDGE/roles-matrix.md (Agent/Operator roles) | Migrated | KEEP | professionals/professional_categories.json | HIGH | None |
| PROF-002 | professionals | KNOWLEDGE/conversation-patterns.md (Agent intro patterns) | Migrated | KEEP | professionals/professional_categories.json | HIGH | None |
| PROF-003 | professionals | KNOWLEDGE/runtime-gap-remediation-plan.md | Partial | UPDATE | professionals/relationship_requirements.md | MEDIUM | Gap plan not fully implemented |
| LEGAL-001 | legal_and_documents | KNOWLEDGE/minimum-fields-property.md (Title status) | Migrated | KEEP | legal_and_documents/document_categories.json | HIGH | None |
| LEGAL-002 | legal_and_documents | KNOWLEDGE/fraud-signals-and-verification.md | Migrated | KEEP | legal_and_documents/legal_information_index.json | HIGH | None |
| RE-001 | real_estate | KNOWLEDGE/property_types/property_types.json | Migrated | KEEP | real_estate/property_types.json | HIGH | None |
| RE-002 | real_estate | KNOWLEDGE/real_estate/property_taxonomy_v2.json | Migrated | KEEP | real_estate/property_types.json | HIGH | None |
| RE-003 | real_estate | KNOWLEDGE/real_estate/property_taxonomy.json | Merged | MERGE | real_estate/property_types.json | HIGH | Superseded by v2 |
| RE-004 | real_estate | KNOWLEDGE/immobilier_cameroun.json | Migrated | KEEP | real_estate/property_types.json | HIGH | Cameroon-specific types |
| RE-005 | real_estate | KNOWLEDGE/vocabulary/real_estate_vocabulary.json | Migrated | KEEP | real_estate/property_type_aliases.json | HIGH | None |
| RE-006 | real_estate | KNOWLEDGE/market-research-real-estate-cameroon.md | Reference | KEEP | commercial/conversation_tone.md | MEDIUM | Market research context |
| RE-007 | real_estate | KNOWLEDGE/search_aliases/search_aliases.json | Migrated | KEEP | real_estate/search_criteria.md | HIGH | None |
