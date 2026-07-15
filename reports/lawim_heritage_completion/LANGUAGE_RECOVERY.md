# LANGUAGE RECOVERY REPORT — LAWIM H0.4

**Date:** 15 July 2026
**Source:** 30-I18N-L10N-REFERENCE.md, 30A-BUSINESS-DICTIONARY-REFERENCE.md, 30C-LANGUAGE-DETECTION-REFERENCE.md, 30D-MULTILINGUAL-SEARCH-REFERENCE.md, knowledge_unified/language/

---

## What Was Recovered

| Concept | Details | Source |
|---------|---------|--------|
| 3 supported languages | FR(full), EN(full), PID(partial) | 03-CONVERSATION Ch18 |
| Camfranglais status | NOT a 4th language, only in expression corpus | OPEN_POINTS C-007 |
| Language detection | DeepSeek → Gemini(disabled) → Local rules | 30C-LANGUAGE-DETECTION |
| 18 FR keywords | Max in language_detector_ia.py | LANGUAGE_VALIDATION |
| 18 EN keywords | Max in language_detector_ia.py | LANGUAGE_VALIDATION |
| 14 PID keywords | In IA detector (12 in basic detector) | LANGUAGE_VALIDATION |
| 8 templates (FR/EN/PID) | welcome, help, no_match, thanks, ask_name, ask_phone, stats, language_changed | multilingual_responses.py |
| 20+ entity linking entries | equivalent_to, synonym, related_to, typo_of, abbreviation_of | entity_linking.json |
| 5 typo databases | cities(10 cities), neighborhoods(6), property_types(9), general(49), whatsapp | typo_database/ |
| 7 WhatsApp corpus files | whatsapp, diaspora, investor, negotiation, listing, search, urgency | whatsapp_language/ |
| 38 country codes | Phone formatting | phone_formatter.py |
| Cameroon phone format | 237 + 9 digits | phone_formatter.py |
| WhatsApp link | https://wa.me/{normalized} | phone_formatter.py |
| FR/EN/PID/Camfranglais matrices | 24+ expression groups | knowledge_unified/language/ |
| 30 real estate terms | Business dictionary | 30A-BUSINESS-DICTIONARY |
| 26 marketing vocabulary entries | FR/EN/PID | 30A-BUSINESS-DICTIONARY |
| 8 translation policy rules | Key management, versioning, human validation | 30B-TRANSLATION |
| 6 intent detection categories | BUY, RENT, SELL, INVESTOR, SEARCH, NEGOTIATE + urgency | knowledge_unified/language/ |

**Source:** docs/lawim_heritage_gold/LANGUAGE_MODEL.md + docs/lawim_heritage_gold/LANGUAGE_BUSINESS_KNOWLEDGE.md
