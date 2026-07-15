# CONVERSATION TURN CONTRACT

**Statut :** Gold Standard
**Source :** `docs/lawim_heritage_gold/CONVERSATION_MODEL.md`
**Rôle :** Conversation Execution Architect — Définit le contrat entrée/sortie de chaque tour de conversation.

---

## 1. Contrat d'entrée (Input Contract)

### 1.1 Structure `TurnInput`

```typescript
interface TurnInput {
  message_raw: string;           // Texte brut du message entrant
  media_url?: string;            // URL du média si présent (image, audio, vidéo)
  channel: ChannelType;          // whatsapp | telegram | facebook | dashboard | sms
  actor_id: string;              // Identifiant unique de l'expéditeur
  session_id: string;            // Identifiant de session en cours
  timestamp: string;             // ISO 8601 — horodatage du message
  metadata?: Record<string, any>; // Métadonnées propres au canal
}
```

### 1.2 Contraintes d'entrée

| Champ | Requis | Validation | Défaut |
|-------|:------:|------------|--------|
| `message_raw` | Oui | String non vide, max 4096 car. | — |
| `channel` | Oui | Un des canaux supportés | — |
| `actor_id` | Oui | Format UUID ou hash canal+expéditeur | — |
| `session_id` | Oui | Généré par Identity Resolver si nouveau | — |
| `timestamp` | Oui | ISO 8601, doit être ≤ maintenant + 5 min | — |
| `media_url` | Non | URL valide ou null | null |
| `metadata` | Non | JSON valide | {} |

### 1.3 Exemple d'entrée

```json
{
  "message_raw": "Bonjour, je cherche un appartement à Douala",
  "channel": "whatsapp",
  "actor_id": "550e8400-e29b-41d4-a716-446655440000",
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "timestamp": "2026-07-15T14:30:00Z",
  "metadata": {
    "greenapi_id": "whatsapp:237691234567",
    "message_type": "text"
  }
}
```

---

## 2. Pipeline de traitement

```
┌─────────────┐
│ TurnInput   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│ 1. LANGUAGE DETECTION               │
│    DeepSeek → FR / EN / PID         │
│    Fallback → Règles locales        │
│    Sortie : detected_language       │
│    Réf. : CONV-008, CONV-016        │
└──────────────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ 2. NORMALIZATION                    │
│    Nettoyage : minuscule, trim,     │
│    removal des caractères spéciaux  │
│    Adaptation canal (WhatsApp 1 Q,  │
│    Telegram 2-3 champs)             │
│    Sortie : normalized_text         │
│    Réf. : CONV-005                  │
└──────────────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ 3. ENTITY EXTRACTION                │
│    DeepSeek → ville, budget, type,  │
│    quartier, urgence, rôle          │
│    Regex → mots-clés, commandes     │
│    Sortie : entities[]              │
│    Réf. : CONV-004, CONV-008        │
└──────────────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ 4. INTENT DETECTION                 │
│    Classification :                 │
│    RENT / BUY / SELL / INVESTOR /  │
│    VISIT / SIGNAL / COMMAND /       │
│    CONSENT / FEEDBACK / GREETING /  │
│    HELP / THANKS / STOP / OTHER     │
│    Sortie : intent + confidence     │
│    Réf. : CONV-008, CONV-018        │
└──────────────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ 5. CONTEXT LOADING                  │
│    Court terme (session cache)      │
│    Long terme (DB, 365 jours)       │
│    Familiarité J1-J4                │
│    Résumé dernière session          │
│    Sortie : conversation_context    │
│    Réf. : CONV-009, CONV-010,       │
│            CONV-017                 │
└──────────────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ 6. DECISION REQUEST                 │
│    Hiérarchie :                     │
│    1. DeepSeek AI (prompt context)  │
│    2. Règles locales                │
│    3. Templates                     │
│    Sortie : decision                │
│    Réf. : CONV-018                  │
└──────────────┬──────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ 7. RESPONSE COMPOSITION             │
│    Template matching                │
│    Ton, langue, canal adaptation    │
│    Vouvoiement systématique         │
│    Sortie : response_text           │
│    Réf. : CONV-003, CONV-013,       │
│            CONV-014, CONV-015        │
└──────────────┬──────────────────────┘
       │
       ▼
┌─────────────┐
│ TurnOutput  │
└─────────────┘
```

---

## 3. Contrat de sortie (Output Contract)

### 3.1 Structure `TurnOutput`

```typescript
interface TurnOutput {
  response_text: string | null;     // Réponse à envoyer à l'utilisateur (null si action silencieuse)
  action_to_execute: Action | null; // Action à exécuter
  state_update: StateUpdate;        // Mise à jour de l'état conversationnel
  events: TraceEvent[];             // Événements de traçabilité générés
  metadata: {                       // Métadonnées de traitement
    processing_time_ms: number;
    pipeline_steps: string[];
    decision_source: 'deepseek' | 'local_rules' | 'template';
    language: 'FR' | 'EN' | 'PID';
    intent: string;
    confidence: number;
  };
}
```

### 3.2 Types associés

```typescript
interface Action {
  type: ActionType;
  // SEND_MESSAGE | CREATE_LEAD | ROUTE_CRM | SCHEDULE_FOLLOWUP |
  // ESCALATE | ANONYMIZE | CREATE_DISPUTE | ACTIVATE_SERVICE | NONE
  payload: Record<string, any>;
  priority: 'high' | 'normal' | 'low';
}

interface StateUpdate {
  session: Partial<SessionState>;  // Mise à jour court terme
  long_term?: Partial<LongTermState>; // Mise à jour long terme
  clear_session?: boolean;
}

interface TraceEvent {
  type: TraceEventType;
  // message_received | intent_detected | lead_scored | lead_classified |
  // crm_routed | response_sent | follow_up_scheduled | escalation_triggered
  timestamp: string;
  data: Record<string, any>;
}
```

### 3.3 Exemple de sortie

```json
{
  "response_text": "Bonjour, je suis LAWIM. Dans quelle ville cherchez-vous un logement ?",
  "action_to_execute": {
    "type": "SEND_MESSAGE",
    "payload": {
      "channel": "whatsapp",
      "recipient_id": "550e8400-e29b-41d4-a716-446655440000",
      "template": "ask_city",
      "language": "FR"
    },
    "priority": "high"
  },
  "state_update": {
    "session": {
      "user_role": "tenant",
      "preferred_language": "FR"
    },
    "long_term": {
      "search_history": ["Douala"]
    }
  },
  "events": [
    {
      "type": "message_received",
      "timestamp": "2026-07-15T14:30:00Z",
      "data": { "channel": "whatsapp", "content_truncated": true }
    },
    {
      "type": "intent_detected",
      "timestamp": "2026-07-15T14:30:00.120Z",
      "data": { "intent": "RENT", "confidence": 0.95 }
    },
    {
      "type": "response_sent",
      "timestamp": "2026-07-15T14:30:00.350Z",
      "data": { "channel": "whatsapp", "template": "ask_city", "latency_ms": 350 }
    }
  ],
  "metadata": {
    "processing_time_ms": 350,
    "pipeline_steps": ["language_detection", "normalization", "entity_extraction", "intent_detection", "context_loading", "decision_request", "response_composition"],
    "decision_source": "deepseek",
    "language": "FR",
    "intent": "RENT",
    "confidence": 0.95
  }
}
```

---

## 4. États d'erreur

### 4.1 Erreurs de pipeline

| Erreur | Condition | Comportement |
|--------|-----------|--------------|
| `unrecognized_message` | Message vide, contenu illisible, bruit seul | Réponse template `help`, demander reformulation |
| `ambiguous_intent` | Confidence < 0.5, intentions multiples sans dominance | Question de clarification "Souhaitez-vous acheter, louer ou vendre ?" |
| `extraction_failure` | DeepSeek ne peut extraire aucune entité | Template `no_match` + question simplifiée |
| `language_unknown` | Langue non supportée détectée | Réponse en français par défaut + proposition changement |
| `channel_unsupported` | Canal non reconnu | Rejeter avec log, pas de réponse |
| `identity_resolution_failed` | Impossible de créer/résoudre actor_id | Session anonyme, pas de persistance long terme |
| `decision_timeout` | DeepSeek timeout (> 5s) | Fallback règles locales → templates |
| `decision_all_failed` | DeepSeek + règles + templates échouent | Réponse générique d'excuse + escalade technique |

### 4.2 Réponses par état d'erreur

| Erreur | Réponse FR | Réponse EN |
|--------|------------|------------|
| `unrecognized_message` | "Je n'ai pas bien compris. Pouvez-vous reformuler ?" | "I didn't understand. Could you rephrase?" |
| `ambiguous_intent` | "Souhaitez-vous acheter, louer ou vendre un bien ?" | "Are you looking to buy, rent, or sell?" |
| `extraction_failure` | "Pouvez-vous préciser votre recherche ?" | "Could you provide more details?" |
| `decision_timeout` | "Veuillez patienter, je prépare ma réponse..." | "Please wait, I'm preparing my response..." |

### 4.3 Classification des intentions ambiguës

| Scénario | Mots-clés | Réponse clarification |
|----------|-----------|-----------------------|
| Achat vs Location | "prix", "combien", "cher" | "Souhaitez-vous acheter ou louer ce bien ?" |
| Vente vs Location | "j'ai un bien", "propriétaire" | "Souhaitez-vous vendre ou mettre en location votre bien ?" |
| Visite vs Achat | "voir", "visite" | "Souhaitez-vous visiter le bien ou avoir plus d'informations ?" |

---

## 5. Règles de validation du contrat

| # | Règle | Réf. | Application |
|:-:|-------|:----:|-------------|
| 1 | Tout message reçu doit produire un TurnOutput valide | CONV-001 | Garantie de réponse |
| 2 | response_text ou action_to_execute doit être non null | CONV-001 | Au moins une action |
| 3 | La langue de sortie doit correspondre à detected_language | CONV-016 | Cohérence multilingue |
| 4 | Le vouvoiement est maintenu dans response_text | CONV-003 | Ton professionnel |
| 5 | state_update ne contredit pas les données persistées | CONV-009 | Correction prioritaire |
| 6 | Les événements de traçabilité sont générés pour chaque étape | CONV-006 §6 | Traçabilité complète |
| 7 | Le temps de traitement total est < 5000ms sinon fallback | CONV-004 | Réactivité |
| 8 | Aucune donnée sensible n'est loguée dans les événements | CONV-012 | RGPD |

---

*Document patrimonial Gold — Toute reconstruction doit respecter ce modèle validé.*
