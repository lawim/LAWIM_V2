# Qualification Rules

## Core Principles

1. **Qualification order**: Intention → Type de bien → Ville → Quartier → Budget → Délai → Critères spécifiques → Préférences → Confirmation
2. **One question at a time on WhatsApp**, 2-3 fields on Telegram
3. **Budget is mandatory before matching**
4. **Never re-ask for already-provided fields**
5. **Stop early** when: city not covered, inventory empty, human handoff needed, conversation off-topic

## Cameroon-Specific Attributes

Use (not "nombre de pièces" or "standing"):
- chambres (bedrooms)
- douches (bathrooms)  
- salons (living rooms)
- meublé / non meublé
- bordure de route (road frontage)
- accessibilité
- titre foncier (land title)
- loti / non loti (serviced land)

Standing is **deduced** from: `prix + quartier + photos + finitions`

## Qualification Statuses

| Status | Meaning |
|--------|---------|
| MISSING_CORE_FIELDS | Core fields not yet collected |
| DRAFT_CREATED | Draft created, qualification in progress |
| QUALIFIED | All required fields collected |
| MATCH_READY | Ready for matching engine |
| WAITLISTED | City not covered or no inventory |
| NO_ACTIVE_MATCH | No active matches found |

## Human Escalation Triggers

Escalate when user says:
- "Je veux parler à quelqu'un"
- "Je veux négocier"
- "Le titre n'est pas clair"
- "Le terrain n'est pas loti"
- "Il y a plusieurs propriétaires"
- "Il faut une décision rapide"
- Repeated fraud signals

## Request Lifespan

| Property Type | Default Lifespan |
|--------------|-----------------|
| Chambre | 30 days |
| Studio | 30 days |
| Appartement | 90 days |
| Maison/Villa | 90 days |
| Bureau/Commerce | 90 days |
| Terrain | 365 days |

## Forbidden

- Never mention "standing" explicitly
- Never use "nombre de pièces"
- Never propose a different city when requested city is uncovered
- Never pressure for budget on greetings only (History Gate)
