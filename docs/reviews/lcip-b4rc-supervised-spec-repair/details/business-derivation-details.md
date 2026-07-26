# Business Derivation Details — LCIP B.4R-C

## Method

Une création métier est attendue uniquement lorsque :
1. Question finale explicite (CONFIRM_BUSINESS_CREATION)
2. Réponse utilisateur positive (oui/yes/enregistrez)
3. Faits obligatoires complets
4. Aucune correction ou négation simultanée

## Results per Conversation

| ID | Final Ask Turn | Consent Turn | Facts Complete | Correction in Confirm | Expected Action | Object Count |
|----|---------------|-------------|----------------|---------------------|----------------|-------------|
| B000001 | 10 | 11 | OUI | NON | CREATE_SEARCH | 1 |
| B000002 | 10 | 11 | OUI | NON | CREATE_SEARCH | 1 |
| B000004 | 10 | 11 | OUI | NON | CREATE_SEARCH | 1 |
| B000005 | 10 | 11 | OUI | NON | CREATE_SEARCH | 1 |
| B000021 | 8 | 9 | OUI | NON | CREATE_SEARCH | 1 |
| B000056 | 6 | 7 | OUI | OUI | CREATE_SEARCH | 1 |
| B000057 | 6 | 7 | OUI | OUI | CREATE_SEARCH | 1 |
| B000101 | 10 | 11 | OUI | OUI | CREATE_SEARCH | 1 |
| B000111 | 12 | 13 | OUI | OUI | CREATE_SEARCH | 1 |
| B000121 | 6 | 7 | OUI | OUI | CREATE_SEARCH | 1 |
| B000089 | 10 | 11 | OUI | NON | CREATE_SEARCH | 1 |
| B000090 | 10 | 11 | OUI | NON | CREATE_SEARCH | 1 |
| B000095 | 10 | 11 | OUI | NON | CREATE_SEARCH | 1 |
| B000096 | 10 | 11 | OUI | NON | CREATE_SEARCH | 1 |
| B000076 | 2 | - | OUI | - | NONE | 0 |
| B000077 | 2 | - | OUI | - | NONE | 0 |
| B000066 | 16 | 17 | OUI | NON | CREATE_SEARCH | 1 |
| B000083 | 10 | 11 | OUI | NON | CREATE_SEARCH | 1 |
| B000131 | 10 | 11 | OUI | OUI | CREATE_SEARCH | 1 |
| B000036 | 8 | 9 | OUI | NON | CREATE_SEARCH | 1 |

## Rules

EXP-0009: Confirmation finale requise avant action métier
EXP-0010: Refus bloque création métier
EXP-0011: Confirmation explicite autorise création
EXP-0012: Création unique par conversation
