# LAWIM V2 Unified Knowledge Repository

## Purpose

The `knowledge_unified/` directory is the single source of truth for all LAWIM domain knowledge. It consolidates, canonicalizes, and maintains the business logic that was previously scattered across ~220 files in the legacy `LAWIM/KNOWLEDGE/` directory.

## Structure

```
knowledge_unified/
├── commercial/              # Sales, negotiation, objection handling, tone
├── geography/               # Cities, neighborhoods, aliases, proximity rules
├── language/                # Multilingual expressions, variants, abbreviations
├── legal_and_documents/     # Document categories, legal info, disclaimers
├── matching/                # Matching engine dimensions, scoring, ranking
├── professionals/           # Agent/partner categories, qualifications, profiles
├── qualification/           # User typologies, intents, qualification matrices
├── real_estate/             # Property types, transaction types, amenities
├── schemas/                 # JSON Schema definitions (future)
├── sources/                 # Legacy source inventory and traceability matrix
├── validation/              # Validation reports, conflicts, quality assessments
└── README.md                # This file
```

## Domain Overview

| Domain | Description | Format |
|--------|-------------|--------|
| **commercial/** | Conversation techniques for negotiation, objection handling, closing, follow-up, and tone guidelines | Markdown |
| **geography/** | Canonical cities (priority + secondary), neighborhoods, district aliases, proximity scoring rules, and mobility modes | JSON + Markdown |
| **language/** | Multilingual expressions (FR/EN/Pidgin/Camfranglais), spelling variants, abbreviations, amount expressions, and intent phrases | JSON |
| **legal_and_documents/** | Document categories with fraud signals, legal information index, and disclaimer rules | JSON + Markdown |
| **matching/** | Matching engine dimensions with weights, scoring rules, exclusion criteria, ranking methodology, and geographic weights | JSON + Markdown |
| **professionals/** | Professional categories (agent, owner, promoter, notary, etc.), qualification requirements, partner profile fields, and relationship rules | JSON + Markdown |
| **qualification/** | User typologies, intentions, search matrices (rent, buy, land, commercial), professional matrices, and qualification lifecycle rules | JSON + Markdown |
| **real_estate/** | Canonical property types, aliases, transaction types, amenities, constraints, and search criteria | JSON + Markdown |
| **schemas/** | Reserved for JSON Schema definitions of the knowledge files | (future) |
| **sources/** | Legacy source inventory and traceability matrix linking legacy → canonical | Markdown |
| **validation/** | Validation reports, conflict documentation, unresolved items, and quality assessments | JSON + Markdown |

## File Format Conventions

### JSON Files
- Every JSON file includes a `metadata` block with `version`, `source` (legacy reference), and optionally `generated_at`
- Strings use French as primary language, English as secondary
- IDs use UPPER_SNAKE_CASE convention
- Enums are explicitly documented in-line

### Markdown Files
- First line is always an H1 heading matching the file name
- Source attribution in the second block
- Use tables for structured comparisons
- Use code blocks for examples and templates

## Usage

### How to Use This Knowledge

1. **Runtime** (`code/`): The runtime loads JSON files directly for matching, qualification, and language processing
2. **LLM Context**: Markdown files serve as grounding context for LAWIM's LLM-based conversational agent
3. **Reference**: All business logic decisions trace back to files in this directory
4. **Development**: Add or modify knowledge here, not in legacy `LAWIM/KNOWLEDGE/`

### Adding New Knowledge

1. Identify the correct domain directory
2. Use the established JSON or Markdown format (see existing files)
3. Include a `metadata.source` field referencing the origin
4. Update `validation/quality_report.md` if coverage changes
5. Run `scripts/validate_unified_knowledge.py` to validate
6. Update `sources/TRACEABILITY_MATRIX.md` if adding new legacy traceability

## Validation

Run the validation script from the project root:

```bash
PYTHONPATH=code python3 scripts/validate_unified_knowledge.py
```

The validator checks:
- All required directories and files exist
- JSON files parse correctly
- No duplicate IDs in datasets
- No sensitive content (credentials, keys, etc.)
- No code patterns in knowledge files

## Related Documentation

- `sources/SOURCE_INVENTORY.md` - Full inventory of legacy LAWIM knowledge files
- `sources/TRACEABILITY_MATRIX.md` - Traceability from legacy to canonical files
- `validation/validation_report.json` - Latest automated validation result
- `validation/conflicts.md` - Documented conflicts between legacy and canonical
- `validation/quality_report.md` - Quality assessment of the unified knowledge

## Migration Status

| Phase | Status | Date |
|-------|--------|------|
| Legacy source inventory | COMPLETE | 2026-07-15 |
| Geography consolidation | COMPLETE | 2026-07-15 |
| Qualification consolidation | COMPLETE | 2026-07-15 |
| Matching consolidation | COMPLETE | 2026-07-15 |
| Language consolidation | COMPLETE | 2026-07-15 |
| Commercial consolidation | COMPLETE | 2026-07-15 |
| Real estate knowledge | COMPLETE | 2026-07-15 |
| Professionals knowledge | COMPLETE | 2026-07-15 |
| Legal & documents knowledge | COMPLETE | 2026-07-15 |
| Validation & quality docs | COMPLETE | 2026-07-15 |
| **Overall** | **~80%** | 2026-07-15 |
