# Disclaimer Rules for Legal Information

## Source: LAWIM KNOWLEDGE/fraud-signals-and-verification.md + compliance requirements

## Core Principle

LAWIM is a **real estate matching platform**, not a law firm, notary, or legal advisory service. All legal information provided by LAWIM is for **informational purposes only** and does not constitute legal advice.

## When to Display Disclaimers

| Situation | Disclaimer Required | Severity |
|-----------|-------------------|----------|
| General information about land title process | Yes | Standard |
| Information about transfer fees/taxes | Yes | Standard |
| Fraud indicators | No (educational) | None |
| Rental regulation information | Yes | Standard |
| Property valuation guidance | Yes | Standard |
| Specific legal advice ("Is this title valid?") | Yes + Refer to notary | HIGH |
| Contract review or drafting | Yes + Refer to notary | HIGH |
| Litigation or dispute advice | Yes + Refer to lawyer | CRITICAL |

## Standard Disclaimer Template (French)

```
⚠️ Information à titre indicatif
Ces informations sont fournies à titre indicatif seulement et ne constituent pas
un conseil juridique. Pour une consultation adaptée à votre situation,
nous vous recommandons de contacter un notaire ou un avocat spécialisé.
```

## Standard Disclaimer Template (English)

```
⚠️ Informational Notice
This information is provided for guidance only and does not constitute legal advice.
For advice tailored to your situation, please consult a notary or qualified lawyer.
```

## Standard Disclaimer Template (Pidgin)

```
⚠️ Info for guide
Dis info na for guide only, no be legal advice. For advice wey fit you,
contact notary or lawyer.
```

## HIGH Severity Response Template

```
⚠️ Consultation juridique
Cette question nécessite l'avis d'un professionnel du droit.
Nous vous recommandons de consulter un notaire ou un avocat.
Je ne peux pas fournir de conseil juridique spécifique.

Would you like me to connect you with a partner notary?
```

## CRITICAL Severity Response Template

```
⚠️ Assistance juridique requise
Cette situation nécessite une assistance juridique professionnelle.
Veuillez consulter un avocat dès que possible.
Je ne peux pas vous assister sur cette question.
```

## Situations Requiring Mandatory Disclaimer

1. **Title foncier questions** - When user asks about title validity or process
2. **Tax/fee questions** - When user asks about specific tax amounts
3. **Contract questions** - When user asks to review or draft a contract
4. **Dispute resolution** - When user describes a legal dispute
5. **Inheritance/succession** - When property is involved in inheritance
6. **Co-ownership conflicts** - When user describes co-owner disagreements
7. **Construction permits** - When user asks about permit requirements

## Situations Where Disclaimer Is NOT Required

1. **Fraud awareness** - Educational fraud indicators (factual)
2. **General process descriptions** - Standard procedures (factual)
3. **Property condition** - Physical condition of property
4. **Market information** - Prices, trends, neighborhoods
5. **Document checklists** - What documents are typically needed

## Enforcement Rules

| Rule | Description |
|------|-------------|
| Mandatory | Legal disclaimers must be displayed BEFORE any legal information |
| Placement | First response in the legal topic conversation turn |
| Replacement | Never replace disclaimer with a referral without a disclaimer |
| Language | Disclaimer must match user's conversation language if possible |
| Tracking | All disclaimer displays should be logged for compliance audit |

## Referral Partner Network

When a disclaimer is shown, offer referral to verified partners:

| Legal Topic | Refer To | Partner Category |
|-------------|----------|-----------------|
| Title foncier | Notaire partenaire | NOTAIRE |
| Taxe/frais | Notaire ou expert comptable | NOTAIRE |
| Contrat | Notaire | NOTAIRE |
| Litige | Avocat partenaire | AVOCAT |
| Succession | Notaire | NOTAIRE |
| Permis construire | Architecte | ARCHITECTE |
| Expertise foncière | Expert foncier | EXPERT_FONCIER |
