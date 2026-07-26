# PCM Template Review — LAWIM V1.1

**Date:** 2026-07-26

## Canonical Greetings

| Template | FR | EN | PCM | PCM Quality | 
|----------|----|----|-----|-------------|
| Welcome | `Bonjour et bienvenue sur LAWIM. Veuillez décrire votre projet immobilier…` | `Hello and welcome to LAWIM. Please describe your real estate project…` | `Welcome to LAWIM. Tell us your property project: buy, sell, rent, land, management or any other property need.` | PRESENT, LANGUAGE_VALID, PROFESSIONAL |

## Internal Engine Templates

| Template | FR | EN | PCM | PCM Quality |
|----------|----|----|-----|-------------|
| Handover | `Je vais vous mettre en relation avec un conseiller LAWIM…` | `I will connect you with a LAWIM advisor…` | `I understand. I go connect you with LAWIM advisor wey fit help you.` | PRESENT, LANGUAGE_VALID, PROFESSIONAL |
| Rephrase | `Je reformule ma question : {q}` | `Let me rephrase: {q}` | `Make I talk am well: {q}` | PRESENT, LANGUAGE_VALID, PROFESSIONAL |
| Acknowledge | `Très bien. Vous recherchez {facts}.` | `Very well. You are looking for {facts}.` | `Okay. You dey find {facts}.` | PRESENT, LANGUAGE_VALID, PROFESSIONAL |
| Correction | `J'ai bien noté votre correction` | `I have noted your correction` | `I don note your correction` | PRESENT, LANGUAGE_VALID, PROFESSIONAL |
| Readiness | `Merci ! Vos informations sont complètes.` | `Thank you! Your information is complete.` | `Thank you! Your information complete. I go start search.` | PRESENT, LANGUAGE_VALID, PROFESSIONAL |
| Summary | `Récapitulons vos informations` | `Let me summarize your information` | `Make I recap your information` | PRESENT, LANGUAGE_VALID, PROFESSIONAL |
| Error | `Désolé, je n'ai pas pu traiter votre demande.` | `Sorry, I could not process your request.` | `Sorry, I no fit handle your request. You fit talk am again?` | PRESENT, LANGUAGE_VALID, PROFESSIONAL |
| Confirm summary | `Ces informations sont-elles correctes ?` | `Is this information correct?` | `Dis information correct?` | PRESENT, LANGUAGE_VALID, PROFESSIONAL |

## Legacy Runtime Templates (`_LANG_MSGS`)

| Key | FR | EN | PCM (improved) | PCM Quality |
|-----|----|----|----------------|-------------|
| registered | `Votre demande a bien été enregistrée.` | `Your request has been registered.` | `Your request don register. I fit help you with anything else?` | PRESENT, LANGUAGE_VALID, PROFESSIONAL |
| updating | `Je mets à jour votre demande` | `I am updating your request` | `I dey update your request` | PRESENT, LANGUAGE_VALID, PROFESSIONAL |
| failed | `Je n'ai pas pu enregistrer…` | `I could not save your request…` | `I no fit save your request now. Try again later.` | PRESENT, LANGUAGE_VALID, PROFESSIONAL |
| complete_ask | `Les informations de votre recherche sont complètes. Souhaitez-vous que je l'enregistre ?` | `Your search information is complete. Should I register it?` | `Your search information complete. You want make I register am?` | PRESENT, LANGUAGE_VALID, PROFESSIONAL |
| recap | `Je récapitule votre recherche` | `Here is your search summary` | `Here be your search summary` | PRESENT, LANGUAGE_VALID, PROFESSIONAL |
| proceeding | `Je procède à la recherche…` | `I will proceed with the search.` | `I go look for property.` | PRESENT, LANGUAGE_VALID, PROFESSIONAL |
| correction | `Je prends note de votre correction` | `I note your correction` | `I don hear say you change am` | PRESENT, LANGUAGE_VALID, PROFESSIONAL |
| note | `Je prends note de vos informations…` | `I have noted your information…` | `I don note your information. Continue when you ready.` | PRESENT, LANGUAGE_VALID, PROFESSIONAL |
| empty_input | `Je n'ai pas compris votre message. Pouvez-vous reformuler ?` | `I did not understand your message. Could you rephrase?` | `I no understand your message. You fit explain again?` | PRESENT, LANGUAGE_VALID, PROFESSIONAL |

## Footer Texts

| Language | Text | Verdict |
|----------|------|---------|
| FR | `ℹ️ Réponse assistée par LAWIM AI.` | PRESENT, valid |
| EN | `ℹ️ Response assisted by LAWIM AI.` | PRESENT, valid |
| PCM | `ℹ️ LAWIM AI fit help for this answer.` | PRESENT, LANGUAGE_VALID, PROFESSIONAL |

## Question Catalog (PCM samples)

All questions in `question_catalog.py` have FR/EN/PCM variants.
PCM variants use natural Pidgin English adapted for Cameroonian real estate context.
