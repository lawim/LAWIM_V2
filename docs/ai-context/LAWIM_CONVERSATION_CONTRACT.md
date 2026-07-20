# LAWIM — Contrat Conversationnel Canonique

## Architecture canonique

```
message entrant
→ normalisation
→ résolution de l'acteur
→ résolution de la conversation
→ chargement de la mémoire
→ détection de la langue
→ détection de l'intention
→ extraction des critères
→ fusion avec l'état existant
→ moteur de qualification
→ choix de la prochaine action
→ agent métier
→ formulation
→ validation
→ rendu du canal
→ persistance
→ livraison
```

## Rôle du LLM

Le LLM peut :

- reformuler
- résumer
- expliquer
- rédiger une réponse
- rendre une question naturelle

Le LLM ne peut pas décider seul :

- de l'intention métier
- de l'état de la conversation
- de la prochaine étape métier
- de la disponibilité d'un bien
- du statut d'une visite
- du statut d'un paiement
- de la création d'un handover

## Mémoire obligatoire

Le système doit conserver les informations déjà fournies.

Exemple canonique :

```
Utilisateur :
Je cherche un appartement de deux chambres à Douala.

Utilisateur :
Mon budget est de 180 000 FCFA par mois.

Utilisateur :
Je préfère Bonamoussadi.
```

État attendu :

```yaml
intent: rental_search
property_type: apartment
bedrooms: 2
city: Douala
budget_xaf: 180000
district: Bonamoussadi
qualification_status: in_progress
```

Le système ne doit plus demander :

- le type de bien
- le nombre de chambres
- la ville
- le budget
- le quartier

une fois qu'ils ont été fournis.

## Prochaine question

Chaque réponse doit poser au maximum une seule prochaine question utile.

## Handover

Un handover humain nécessite obligatoirement :

- `handover_required=true`
- `handover_id`
- raison
- équipe cible
- statut persistant
- audit

Aucune salutation ou demande ordinaire ne doit provoquer automatiquement un handover.

## Footer IA

Le footer français canonique doit comporter au maximum dix mots :

`ℹ️ LAWIM AI peut se tromper. Vérifiez les informations importantes.`

Il doit être :

- discret
- non bloquant
- séparé du contenu
- adapté au canal

## Règles d'identité

- Messages utilisateur : `👤 <nom/identifiant>`
- Messages LAWIM : `🤖 LAWIM AI`
- Jamais de noms de fournisseurs IA visibles

---

## Architecture contract (Chantier 1)

### Canonical runtime chain

```
message entrant
  → normalisation
  → CommunicationService._generate_ai_reply()
    → ConversationStateEngine.process_turn()
      → ConversationResolver.resolve()
      → ConversationStateRepository.load()
      → greeting / handover / rephrase detection
      → slot extraction + merge
      → ProgressiveWizard (if configured)
      → _build_response_plan() → ResponsePlan
      → _generate_response() → LLM (AIOrchestrator)
      → ConversationStateRepository.save()
    → ConversationResponseValidator.validate()
    → footer append (WhatsApp / Telegram only)
  → provider delivery (send_whatsapp / send_telegram)
```

### ResponsePlan mandatory

No provider call may occur without a `ResponsePlan`. The state engine produces one via `_build_response_plan()` for every turn. The fallback path (when `ConversationStateEngine` is unavailable) creates a synthetic `ResponsePlan(maximum_questions=1)`. Both paths validate the response against the plan before delivery.

### ResponseValidator active

`ConversationResponseValidator.validate()` is called on every response. It performs:

1. **Forbidden content detection** — blocks neutral assistant phrases, external real-estate platform referrals, unrequested translation, and grammar correction.
2. **Question count enforcement** — if `response.count("?") > plan.maximum_questions`, the response is replaced with `plan.next_question_text` (status `REPAIR`).

### Forbidden content list

| Category | Patterns | Action |
|----------|----------|--------|
| Neutral assistant | "assistant neutre", "neutral assistant", "I cannot make business decisions", "je ne peux pas prendre de décisions commerciales", "provide more context for your request" | REPAIR |
| External referrals | "Jumia", "SeLoger", "Leboncoin", "Facebook", "Lamudi" | REPAIR / BLOCK |
| Unrequested translation | "french for", "in english", "français signifie", "in french" | REPAIR |
| Grammar correction | "correct spelling is", "the correct phrasing", "you wrote", "vous avez écrit", "l'orthographe correcte", "la bonne orthographe" | REPAIR |

### One question per response

`ResponsePlan.maximum_questions` defaults to 1. If the generated response contains more questions than the plan allows, the validator replaces the response with `plan.next_question_text`.

### Language continuity rules

1. `ConversationState.language` tracks the active language (default: `"fr"`).
2. Language is detected on each turn via `_detect_language()`.
3. If the detected language differs from `state.language`, the state is updated.
4. A single foreign word does not change the conversation language.
5. English conversations stay in English; French conversations stay in French.
