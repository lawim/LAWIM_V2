# Unresolved Items

## Date: 2026-07-15

## Items That Could Not Be Resolved or Verified

### Item 1: Gemini-Recovered GPS Data
- **File**: KNOWLEDGE/geography/gemini_recovered_gps.json
- **Issue**: GPS coordinates recovered via Gemini API for neighborhoods. Accuracy cannot be verified against ground truth.
- **Status**: NOT incorporated into geography/cities.json
- **Recommended Action**: Manual verification against known landmarks or deferral to v3.1.

### Item 2: Neighborhood GPS Coordinates
- **File**: KNOWLEDGE/geography/neighborhood_gps.json
- **Issue**: Contains GPS for individual neighborhoods but quality/coverage incomplete. Some coordinates are clearly approximate.
- **Status**: NOT incorporated into geography/neighborhoods.json
- **Recommended Action**: Batch verification + inclusion in geography v3.1 with confidence flags.

### Item 3: Pricing Data
- **File**: KNOWLEDGE/pricing/pricing.json + KNOWLEDGE/pricing/pricing_expressions.json
- **Issue**: Pricing data exists in legacy but is not yet represented in knowledge_unified/. No pricing/ directory exists.
- **Status**: DEFERRED - No canonical pricing knowledge file created yet.
- **Recommended Action**: Create knowledge_unified/pricing/ with market pricing data and price expression patterns.

### Item 4: Historical GPS Backup
- **File**: KNOWLEDGE/geography/cameroon_geography_before_mass_gps_20260610_084253.json
- **Issue**: Pre-mass-GPS snapshot kept as backup. Contains coordinates that differ from the main geography file.
- **Status**: Not evaluated for correctness. Kept as historical reference only.
- **Recommended Action**: No action unless mass-GPS data is found to be degraded.

### Item 5: V1 Archive Data Accuracy
- **Source**: KNOWLEDGE/_archive/ (27 JSON files)
- **Issue**: Older v1 snapshots of cities, typo mappings, pricing, etc. Superseded by v2/v3 data but no diff analysis performed.
- **Status**: NOT analyzed for regression.
- **Recommended Action**: Include in automated regression tests if knowledge_unified/ gains CI.

### Item 6: WhatsApp-Specific Language Rules
- **Source**: KNOWLEDGE/whatsapp_language/ (7 files with WhatsApp-specific expressions)
- **Issue**: Some WhatsApp idioms may be channel-specific and should not apply globally. The unified language files currently treat all expressions as cross-channel.
- **Status**: NOT channel-tagged in knowledge_unified/.
- **Recommended Action**: Add optional `channels` metadata field to language expression entries.

### Item 7: Onboarding Email Templates
- **Source**: KNOWLEDGE/bootstrap-access.md
- **Issue**: Access rules and onboarding flows referenced in legacy but not abstracted into knowledge_unified/.
- **Status**: DEFERRED.
- **Recommended Action**: Create knowledge_unified/operations/ or add to legal_and_documents/ as access rules.

### Item 8: Channel-Specific Qualification
- **Source**: KNOWLEDGE/channels/whatsapp-telegram-dashboard-qualification.md
- **Issue**: Channel-specific qualification rules exist in legacy but are not reflected in qualification/ files.
- **Status**: NOT incorporated.
- **Recommended Action**: Add channel-specific qualification variants or notes to qualification/ files.

### Item 9: Diaspora Behavior Model
- **Source**: KNOWLEDGE/diaspora-behavior-model.md
- **Issue**: Detailed diaspora behavior patterns not yet abstracted into canonical knowledge.
- **Status**: DEFERRED - partially referenced in language/ and qualification/ but not fully represented.
- **Recommended Action**: Create knowledge_unified/diaspora/ or integrate into qualification/ as diaspora persona attributes.

### Item 10: Legacy Repair Backup Files
- **Source**: KNOWLEDGE/_repair_backup/ (~60 files)
- **Issue**: Intermediate repair state files. Unknown which, if any, contain corrections not reflected elsewhere.
- **Status**: NOT analyzed.
- **Recommended Action**: No action unless data corruption is suspected in the canonical geography files.
