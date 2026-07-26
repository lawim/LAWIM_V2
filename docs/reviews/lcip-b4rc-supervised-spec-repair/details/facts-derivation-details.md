# Facts Derivation Details — LCIP B.4R-C

## Method

Chaque fait attendu est dérivé du dialogue source avec :
- Valeur extraite du texte
- Tour source identifié
- Règle EXP applicable
- Confiance documentée

## Example: B000001

| Field | Value | Source Turn | Source Text | Rule ID | Confidence |
|-------|-------|-------------|-------------|---------|------------|
| transaction_type | rent | 1 | "Bonjour, je cherche un maison à louer à Yaoundé." | EXP-0001 | 1.0 |
| property_type | house | 1 | "...un maison à louer..." | EXP-0002 | 1.0 |
| city | Yaoundé | 1 | "...à louer à Yaoundé." | EXP-0003 | 1.0 |
| budget | 75000 | 3 | "Mon budget maximum est de 75 000 FCFA." | EXP-0004 | 1.0 |
| bedrooms | 2 | 5 | "2 chambres." | EXP-0005 | 1.0 |
| preferred_areas | [Melen, Ngoa-Ekellé] | 7 | "Melen ou Ngoa-Ekellé." | EXP-0006 | 1.0 |
| move_in_date | Septembre | 9 | "En septembre." | EXP-qualification | 1.0 |

## Correction Pattern: B000056

| Field | Before | After | Source Turn | Rule |
|-------|--------|-------|-------------|------|
| budget | 150000 | 200000 | 5 | EXP-0007 |
| preferred_areas | [Bastos] | [Melen] | 5 | EXP-0007 |
| bedrooms | 2 | 2 (unchanged) | - | EXP-0008 |
| move_in_date | Octobre | Octobre (unchanged) | - | EXP-0008 |

## All 20 Conversations

Les dérivations complètes sont dans chaque fiche de revue :
`review/<CONVERSATION_ID>.md`
