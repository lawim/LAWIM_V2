# LAWIM Gold Corpus — Audit Report

**Date:** 2026-07-26
**Audit HEAD:** `4d65582ad956c88f6c132b348616da2e85105e5d`
**Source:** `/media/abel/1A4696CE4696AA51/Telechargement/LAWIM_GOLD_CORPUS_BLOCK/`

---

## 1. Archive Inventory

| Bloc | Archive | Taille | SHA-256 | Fichiers | Statut |
|------|---------|------:|---------|---------:|--------|
| 1 | `LAWIM_GOLD_CORPUS_BLOCK_01.zip` | 22,591 | `534fe46102550ded2df913c6da7b5deac9fcd72e61829e8c3a76166125eac762` | 4 | PRIMARY |
| 2 | `LAWIM_GOLD_CORPUS_BLOCK_02_DETAILED.zip` | 25,539 | `8dc4e70cd0bd7a940464b578f1bcb401088b35ad4841825d0d05e1a94c5ff76b` | 4 | PRIMARY |
| 2 | `LAWIM_GOLD_CORPUS_BLOCK_02_DETAILED (1).zip` | 25,539 | `8dc4e70cd0bd7a940464b578f1bcb401088b35ad4841825d0d05e1a94c5ff76b` | 4 | DUPLICATE |
| 3 | `LAWIM_GOLD_CORPUS_BLOCK_03_DETAILED.zip` | 12,490 | `08950ee51ca4b8763e4e0be42b4affe23e0a4ee4322c8f35f124c1bb2003a1b6` | 3 | PRIMARY |
| 4 | `LAWIM_GOLD_CORPUS_BLOCK_04_DETAILED.zip` | 12,830 | `b3d29295eae7b85f02a89752b6986e93225e63b09a05099f8c5414772707cad6` | 3 | PRIMARY |
| 5 | `LAWIM_GOLD_CORPUS_BLOCK_05_DETAILED.zip` | 8,610 | `6ffd246693b35a2eebc84a0749e92228445c1e9eed781927c7ee4c2166cc4fee` | 3 | PRIMARY |
| 6 | `LAWIM_GOLD_CORPUS_BLOCK_06_DETAILED.zip` | 8,492 | `686f850d52f9a9566209bea5b90ab2500ac070b3a2f7487f2324c636f073ffb8` | 3 | PRIMARY |
| 7 | `LAWIM_GOLD_CORPUS_BLOCK_07_DETAILED.zip` | 8,869 | `c58eeba064f5a4a8e073ee5c48847f82d75b7cee3d600c7d6f6573ef3db6486b` | 3 | PRIMARY |
| 8 | `LAWIM_GOLD_CORPUS_BLOCK_08_DETAILED.zip` | 9,044 | `235a1e0818a38e49e1140acb4300e177f2b78edebce710183918ea76e3fb3951` | 3 | PRIMARY |
| 9 | `LAWIM_GOLD_CORPUS_BLOCK_09_DETAILED.zip` | 10,138 | `6934bad3ffc6499392f53248c53faba1a84aa72abb1c2048b5bfdb0b32150123` | 3 | PRIMARY |
| 10 | `LAWIM_GOLD_CORPUS_BLOCK_10_DETAILED.zip` | 12,025 | `ffc689d6585ca4d0ef46e9757a76167b157a51a920bd1f32c6235a5f6a3baf66` | 3 | PRIMARY |

**Total archives: 11** (10 uniques + 1 duplicate)
**Security check:** PASS — no path traversal, no secrets, no personal data, no executables

---

## 2. Conversation Classification

| Statut | Nombre | Détail |
|--------|------:|--------|
| GOLD_CERTIFIED | 100 | Block 02: real dialogues, assertions, expected states |
| GOLD_REPAIRABLE | 100 | Block 01: real dialogues, missing assertions |
| SCENARIO_TEMPLATE | 790 | Blocks 03-10: User turn / Assistant turn placeholders |
| OUT_OF_SCOPE | 10 | Block 03: declared 100 conversations, only 90 delivered |
| INVALID_SCHEMA | 0 | — |
| DUPLICATE | 0 | — |
| **TOTAL** | **1,000** | |

### Arithmetic verification

```
100 (GOLD_CERTIFIED)
+ 100 (GOLD_REPAIRABLE)
+ 790 (SCENARIO_TEMPLATE)
+ 10 (OUT_OF_SCOPE: block_03 missing 10 conversations)
= 1,000 TOTAL_CLASSIFIED ✓
```

---

## 3. Per-Block Breakdown

| Bloc | Conversations | Tours | GOLD | REPAIRABLE | TEMPLATE | OUT_OF_SCOPE |
|------|-------------:|-----:|----:|-----------:|---------:|------------:|
| 01 | 100 | 1,078 | 0 | 100 | 0 | 0 |
| 02 | 100 | 964 | 100 | 0 | 0 | 0 |
| 03 | 90+10 | 2,070 | 0 | 0 | 90 | 10 |
| 04 | 100 | 2,000 | 0 | 0 | 100 | 0 |
| 05 | 100 | 2,100 | 0 | 0 | 100 | 0 |
| 06 | 100 | 2,100 | 0 | 0 | 100 | 0 |
| 07 | 100 | 2,100 | 0 | 0 | 100 | 0 |
| 08 | 100 | 1,900 | 0 | 0 | 100 | 0 |
| 09 | 100 | 2,200 | 0 | 0 | 100 | 0 |
| 10 | 100 | 2,700 | 0 | 0 | 100 | 0 |
| **Total** | **1,000** | **19,212** | **100** | **100** | **790** | **10** |

---

## 4. Validator Results

| Check | Result |
|-------|--------|
| Validator path | `tests/gold_corpus/validators/validate_gold_corpus.py` |
| Conversations parsed | 200 (blocks 01-02, only real dialogues in repo) |
| Executable (Gold) | 100 |
| Errors | 0 |
| Exit code | 0 |

---

## 5. Diversity Analysis

| Dimension | Measure |
|-----------|---------|
| Languages | FR (primary), EN, PCM |
| Channels | web, telegram, whatsapp, cross_channel |
| Categories | rental_search, purchase_search, property_visit, document_request, long_memory |
| Real dialogues | 200 (blocks 01-02, manually authored) |
| Templates | 790 (blocks 03-10, machine-generated with placeholders) |

---

## 6. Certified Gold Summary

**100 GOLD_CERTIFIED conversations** in block 02:
- All have complete JSON schema
- All have assertions (business_object_count, memory_preserved, idempotent, etc.)
- All have expected_final_state
- All have realistic real estate dialogues
- All are executable through the validator

**100 GOLD_REPAIRABLE conversations** in block 01:
- All have realistic real estate dialogues
- All have expected_final_state
- All MISSING assertions array (needs to be added to certify)
- All have complete JSON schema otherwise

---

## 7. Classification Files

| File | Lines | Path |
|------|-----:|------|
| corpus-classification.jsonl | 1,000 | `docs/reviews/evidence/lawim-v1.1-production/normalized/` |
| corpus-certified.jsonl | 100 | `docs/reviews/evidence/lawim-v1.1-production/normalized/` |
| corpus-repairable.jsonl | 100 | `docs/reviews/evidence/lawim-v1.1-production/normalized/` |
| corpus-rejected.jsonl | 800 | `docs/reviews/evidence/lawim-v1.1-production/normalized/` |

---

## 8. Verdict

```
LAWIM_GOLD_CORPUS_VALIDATION_PARTIAL
```

Reason: 100 certified + 100 repairable = 200 real dialogues out of 1,000 declared.  
Full certification requires adding assertions to block 01 (100 conversations) and replacing 790 templates with real dialogues.
