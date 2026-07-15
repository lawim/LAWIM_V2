# CONVERSATION EXECUTION ARCHITECTURE

**Statut :** Gold Standard
**Source :** `docs/lawim_heritage_gold/CONVERSATION_MODEL.md`
**Rôle :** Conversation Execution Architect — Définit le pipeline, les composants et la consommation des règles Heritage Gold.

---

## 0. H0.5 Integration Points — Qualification Pipeline

The H0.5 qualification matrices integrate into the conversation pipeline between Fact Extraction (step 4) and Decision Engine (step 7). The following 7-step integration adds matrix-driven qualification logic:

```
Extract Facts (step 4)
    │
    ▼
┌──────────────────────────────────────────────────────────────────┐
│ 1. DETECT REQUEST FAMILY    │ Resolve intent + property_type to  │
│                              │ request_family (RESIDENTIAL_SEARCH,│
│                              │ LAND_SEARCH, COMMERCIAL_SEARCH,    │
│                              │ FINANCING_REQUEST, etc.)           │
├──────────────────────────────────────────────────────────────────┤
│ 2. SELECT H0.5 MATRIX       │ Load matrix from                   │
│                              │ qualification_matrices.json by     │
│                              │ (family, transaction_type,         │
│                              │ property_type) triple              │
├──────────────────────────────────────────────────────────────────┤
│ 3. EXTRACT FIELDS           │ Extract all field values from      │
│                              │ message per field_dictionary.json  │
│                              │ validation & normalization rules    │
├──────────────────────────────────────────────────────────────────┤
│ 4. CALCULATE MISSING FIELDS │ Compare extracted fields against   │
│                              │ matrix field requirements per      │
│                              │ current readiness level            │
├──────────────────────────────────────────────────────────────────┤
│ 5. COMPUTE READINESS LEVEL  │ Using readiness_rules.json +       │
│                              │ matrix field lists → determine    │
│                              │ INTENT_IDENTIFIED → TRANSACTION_READY│
├──────────────────────────────────────────────────────────────────┤
│ 6. SELECT NEXT QUESTION     │ Using question_rules.json priority │
│                              │ rules + matching_semantics.json   │
│                              │ → build priority queue            │
├──────────────────────────────────────────────────────────────────┤
│ 7. CHECK STOP CONDITION     │ Stop questioning when target       │
│                              │ action is allowed per readiness   │
│                              │ level (e.g., LAUNCH_FIRST_SEARCH  │
│                              │ at MINIMUM_SEARCH_READY)          │
└──────────────────────────────────────────────────────────────────┘
    │
    ▼
Query Decision Engine (step 7)
```

### 0.1 Integration Data Flow

```typescript
interface H0_5IntegrationInput {
  raw_message: string;
  extracted_entities: Map<string, any>;   // From Fact Extractor
  detected_intent: IntentResult;          // From Intent Detector
  session_context: SessionContext;        // From Context Loader
}

interface H0_5IntegrationOutput {
  matrix: SelectedMatrix;                 // From step 2
  fields: ExtractedFields;                // From step 3
  missing: MissingFieldsByLevel;          // From step 4
  readiness: ReadinessLevel;              // From step 5
  next_question: Question | null;         // From step 6
  stop_reason: "SEARCH_LAUNCH" | "INTRODUCTION" | "TRANSACTION" | null;  // From step 7
}
```

### 0.2 Source H0.5 Files

| Integration Step | H0.5 Source Files |
|-----------------|-------------------|
| 1. Detect request family | `field_dictionary.json` (appears_in per field) |
| 2. Select matrix | `qualification_matrices.json` (75 matrices) |
| 3. Extract fields | `field_dictionary.json` (validation, normalization, templates) |
| 4. Calculate missing | `qualification_matrices.json` (minimum_* field lists) |
| 5. Compute readiness | `readiness_rules.json`, `READINESS_LEVELS.md` |
| 6. Select next question | `question_rules.json`, `matching_semantics.json` |
| 7. Check stop condition | `readiness_rules.json` (allowed_actions per level) |

The H0.5 integration is non-invasive — it operates between existing pipeline components without modifying them. The 7-step sub-pipeline runs synchronously after Fact Extraction and before the Decision Engine query.

---

## 1. H1 Heritage Layer — Pipeline de conversation (11 étapes)

```
Message entrant
    │
    ▼
┌──────────────────────────────────────────────────────────────────┐
│ 1. RECEIVE MESSAGE          │ Entrée brute : texte, média, canal │
├──────────────────────────────────────────────────────────────────┤
│ 2. NORMALIZE CHANNEL        │ Adapter au format du canal cible  │
├──────────────────────────────────────────────────────────────────┤
│ 3. RESOLVE IDENTITY         │ Actor_id, session_id, profil      │
├──────────────────────────────────────────────────────────────────┤
│ 4. EXTRACT FACTS            │ Entités, langues, mots-clés       │
├──────────────────────────────────────────────────────────────────┤
│ 5. DETECT INTENT            │ RENT / BUY / SELL / INVESTOR /    │
│                              │ VISIT / SIGNAL / COMMAND / ...   │
├──────────────────────────────────────────────────────────────────┤
│ 6. LOAD CONTEXT             │ Court terme + long terme          │
├──────────────────────────────────────────────────────────────────┤
│ 7. QUERY DECISION ENGINE    │ DeepSeek + Règles + Templates     │
├──────────────────────────────────────────────────────────────────┤
│ 8. RECEIVE NEXT ACTION      │ Response, action, state_update    │
├──────────────────────────────────────────────────────────────────┤
│ 9. COMPOSE RESPONSE         │ Template, ton, langue, canal      │
├──────────────────────────────────────────────────────────────────┤
│10. EXECUTE / DELEGATE       │ Envoyer message, créer lead,      │
│                              │ planifier follow-up, escalader   │
├──────────────────────────────────────────────────────────────────┤
│11. PERSIST TURN             │ Journaliser, tracer événements    │
└──────────────────────────────────────────────────────────────────┘
```

---

## 2. Composants du système

| # | Composant | Responsabilité | Technologie |
|:-:|-----------|----------------|-------------|
| 1 | **Message Receiver** | Écouter les webhooks entrants (GreenAPI, Telegram Bot API, etc.) | Webhook / Polling |
| 2 | **Channel Normalizer** | Normaliser le payload selon le canal d'origine en structure interne | Adapter pattern |
| 3 | **Identity Resolver** | Associer l'expéditeur à un actor_id existant ou créer un profil anonyme | Base de données |
| 4 | **Fact Extractor** | Extraire entités (ville, budget, type de bien), langue, mots-clés | DeepSeek AI + Regex |
| 5 | **Intent Detector** | Classifier l'intention principale et secondaire | DeepSeek AI + Règles |
| 6 | **Context Loader** | Charger mémoire court terme (session) et long terme (365 jours) | Cache + DB |
| 7 | **Decision Engine Client** | Interroger DeepSeek AI, moteur de règles, templates par hiérarchie | API + Local |
| 8 | **Response Composer** | Formater la réponse selon canal, langue, ton | Template engine |
| 9 | **Action Executor** | Exécuter actions (créer lead, routage CRM, planifier follow-up) | Service layer |
| 10 | **Turn Persister** | Journaliser le tour, tracer événements de traçabilité | Logger + Events |

### 2.1 Interactions entre composants

```
Message Receiver
    │
    ▼
Channel Normalizer ──→ Turn Persister (event: message_received)
    │
    ▼
Identity Resolver ──→ Turn Persister (event: lead_scored)
    │
    ▼
Fact Extractor ──→ Turn Persister
    │
    ▼
Intent Detector ──→ Turn Persister (event: intent_detected)
    │
    ▼
Context Loader
    │
    ▼
Decision Engine Client ──→ Turn Persister (event: response_sent)
    │
    ▼
Response Composer
    │
    ▼
Action Executor ──→ Turn Persister (events: lead_classified, crm_routed,
    │                                         follow_up_scheduled, escalation_triggered)
    │
    ▼
Turn Persister ──→ Journal + Traçabilité
```

---

## 3. Consommation des règles Heritage Gold (CONV-001 à CONV-023)

Chaque règle Heritage Gold est encapsulée dans un composant du pipeline. Les règles sont chargées au démarrage et évaluées à chaque étape.

### 3.1 Catalogue des règles

| Réf. | Règle | Section source | Composant applicateur |
|:----:|-------|----------------|------------------------|
| CONV-001 | Positionnement intermédiaire | §1.1 | Response Composer, Decision Engine |
| CONV-002 | Zéro commission | §1.2 | Response Composer, Template Engine |
| CONV-003 | Ton professionnel, vouvoiement | §1.3 | Response Composer, Tone Enforcer |
| CONV-004 | Langage naturel, non robotique | §1.4 | Decision Engine (DeepSeek prompt) |
| CONV-005 | Progressive disclosure (1 msg WhatsApp) | §1.5 | Channel Normalizer, Response Composer |
| CONV-006 | Double consentement | §1.6, §4 | Identity Resolver, Action Executor |
| CONV-007 | Anonymisation RGPD (7 jours) | §1.7, §5 | Identity Resolver, Turn Persister |
| CONV-008 | Détection automatique langue et intention | §1.8 | Fact Extractor, Intent Detector |
| CONV-009 | Correction utilisateur écrase contexte | §1.9, §20 | Context Loader (update priority) |
| CONV-010 | Non-redémarrage de conversation | §1.10 | Context Loader (resume policy) |
| CONV-011 | Double consentement — partage coordonnées | §4 | Action Executor (permission gate) |
| CONV-012 | Anonymat — pseudonyme, données sensibles | §5 | Identity Resolver, Data Sanitizer |
| CONV-013 | Politique de réponse (intermédiaire, commission, ton) | §8 | Response Composer, Decision Engine |
| CONV-014 | Humanisation (empathie, expressions locales, variété) | §9 | Decision Engine (DeepSeek prompt) |
| CONV-015 | Guide de style (phrases courtes, positif, CTA) | §10 | Response Composer |
| CONV-016 | Multilingue (FR/EN/PID, hiérarchie détection) | §11 | Fact Extractor, Response Composer |
| CONV-017 | Mémoire conversationnelle (court terme session, long terme 365j) | §12 | Context Loader, Memory Store |
| CONV-018 | Routage des réponses (DeepSeek → Règles → Templates) | §13 | Decision Engine Client |
| CONV-019 | Planning de relance (J1/J7/J30/J90) | §14 | Action Executor (Follow-up Scheduler) |
| CONV-020 | Commandes spéciales (SIGNALER, SUPPRIMER, etc.) | §15 | Intent Detector, Action Executor |
| CONV-021 | Gestion des objections (12 acheteurs, 8 vendeurs) | §16 | Decision Engine (Objection Handler) |
| CONV-022 | Règles d'escalade humaine (juridique, litige, 3 échecs) | §17 | Decision Engine, Action Executor |
| CONV-023 | Feedback utilisateur (👍=5, 👎=1) | §19 | Fact Extractor, Turn Persister |

### 3.2 Mécanisme d'application

Les règles CONV-* sont chargées dans un `RuleEngine` central au démarrage. Chaque règle expose :

```typescript
interface ConversationRule {
  id: string;             // "CONV-001"
  condition: (ctx: TurnContext) => boolean;
  action: (ctx: TurnContext) => void;
  priority: number;       // 1 (critique) → 5 (informatif)
  component: string;      // composant cible
}
```

À chaque étape du pipeline, le `RuleEngine` évalue les règles dont le composant correspond.

---

## 4. Système de mémoire

### 4.1 Hiérarchie

| Niveau | Type | Durée | Stockage | Contenu |
|--------|------|-------|----------|---------|
| **Court terme** | Session | Session utilisateur | Cache Redis (TTL session) | city, neighborhood, budget, property_type, user_role, preferred_language |
| **Long terme** | Persistant | 365 jours | Base de données | favorite_locations, investment_preferences, diaspora_country, search_history, satisfaction_score |
| **Archive** | Froid | > 365 jours | Data Lake | Agrégats anonymisés, statistiques |

### 4.2 Niveaux de familiarité (J1-J4)

| Niveau | Code | Critère | Comportement |
|:------:|:----:|---------|--------------|
| **J1** | Découverte | Premier message, aucune historique | Présentation complète, question ouverte |
| **J2** | Retour | Historique > 1 session | Reprise contextuelle, résumé de la dernière interaction |
| **J3** | Investi | 3+ sessions, données collectées | Qualification avancée, suggestions personnalisées |
| **J4** | Prioritaire | Lead HOT, engagement fort | Priorité de réponse, offre spéciale, accompagnement prioritaire |

### 4.3 Règles de rétention

| Règle | Valeur | Réf. Heritage |
|-------|--------|:-------------:|
| Durée de rétention long terme | 365 jours | CONV-017 |
| Oubli complet après inactivité | 90 jours | CONV-017 |
| Lead relançable après | 12 mois | CONV-017 |
| Anonymisation sur demande | 7 jours max | CONV-007, CONV-012 |

---

## 5. Planification des relances (Follow-up)

### 5.1 Échéances

| Code | Délai | Message | Canal |
|:----:|:-----:|---------|:-----:|
| **J1** | 24h | Nouveaux biens correspondant à la recherche | WhatsApp |
| **J7** | 7 jours | 5 nouvelles annonces disponibles | WhatsApp |
| **J30** | 30 jours | Mois prioritaire gratuit | WhatsApp + Email |
| **J90** | 90 jours | 500+ requêtes traitées, relance ? | WhatsApp |

### 5.2 Déclencheurs

- Fin de qualification réussie → J1 planifié
- Interaction utilisateur → réinitialisation compteur d'inactivité
- Nouveaux biens en base → J7/J30 accéléré si correspondance forte

---

## 6. Hiérarchie des réponses

| Ordre | Mécanisme | Déclencheur | Réf. |
|:-----:|-----------|-------------|:----:|
| 1 | **DeepSeek AI** | Message complexe, extraction, intention non triviale | CONV-018 |
| 2 | **Règles locales** | Salutations, remerciements, commandes, mots-clés simples | CONV-018 |
| 3 | **Templates** | Messages standards (welcome, help, no_match, thanks, etc.) | CONV-018 |

Si DeepSeek AI échoue (timeout, erreur API), fallback automatique vers règles locales, puis templates.

---

## 7. Support multi-canal

| Canal | Normalisation | Limites | Particularité |
|-------|--------------|---------|---------------|
| **WhatsApp** | GreenAPI → texte + média | 1 question/message | Canal principal, logs `whatsapp_logs` |
| **Telegram** | Bot API → texte + boutons | 2-3 champs/message | Boutons inline, messages plus longs |
| **Facebook** | Messenger API → texte | Qualification simplifiée | Intégration page business |
| **Dashboard** | API REST → formulaire structuré | Complet | Qualification manuelle, suivi CRM |
| **SMS** | API SMS → texte court | 160 caratères max | Qualification minimale |

### 7.1 Ton par canal

| Canal | Ton | Longueur | Directives |
|-------|-----|----------|------------|
| WhatsApp | Professionnel, concis | 1-2 phrases | CONV-005, CONV-003 |
| Telegram | Décontracté, direct | 2-3 champs | CONV-005 |
| Dashboard | Formel, structuré | Complet | CONV-003 |

---

## 8. Gestion des commandes spéciales

| Commande | Intention | Action | Réf. |
|----------|-----------|--------|:----:|
| `SIGNALER [raison]` | SIGNAL | Créer un litige dans `disputes` table, escalade support | CONV-020 |
| `SUPPRIMER MES DONNÉES` | ERASE | Anonymiser l'utilisateur sous 7 jours, flag RGPD | CONV-007, CONV-020 |
| `ACCOMPAGNEMENT` | ACCOMPAGNEMENT | Activer service payant (50 000 FCFA), routage conseiller | CONV-020 |
| `STATS` | STATS | Afficher les performances (agents seulement) | CONV-020 |
| `LANGUE [FR/EN/PID]` | LANGUE | Basculer la langue de conversation | CONV-016, CONV-020 |
| `RECHERCHE` | SEARCH | Nouveaux biens depuis la relance J7 | CONV-019, CONV-020 |
| `PRIORITAIRE` | PRIORITY | Activer recherche prioritaire (J30) | CONV-019, CONV-020 |
| `RELANCER` | RESTART | Reprendre la recherche (J90) | CONV-019, CONV-020 |
| `OUI` / `NON` | CONSENT | Réponse à une demande de permission | CONV-006, CONV-011 |

---

## 9. Événements de traçabilité

| # | Événement | Déclencheur | Étape pipeline |
|:-:|-----------|-------------|:--------------:|
| 1 | `message_received` | Nouveau message entrant | 1 |
| 2 | `intent_detected` | Intention identifiée | 5 |
| 3 | `lead_scored` | Score calculé | 3 |
| 4 | `lead_classified` | Classification (HOT/WARM/COLD/SPAM) | 7 |
| 5 | `crm_routed` | Lead routé vers un agent | 10 |
| 6 | `response_sent` | Réponse envoyée | 10 |
| 7 | `follow_up_scheduled` | Relance programmée | 10 |
| 8 | `escalation_triggered` | Escalade humaine activée | 10 |

---

---

## 10. NBA Integration

Every conversation turn produces an NBA (Next Best Action) determined by the Decision Engine based on conversation state:

| Conversation State | NBA | Trigger |
|-------------------|-----|---------|
| Incoming message | `qualify.initial` | New user message |
| Qualifying | `qualify.continue` | Missing qualification fields |
| Qualified | `match.search` | Qualification complete |
| Awaiting response | `follow_up` | Inactivity timeout |
| Objection raised | `objection.handle` | Objection pattern detected |
| Escalation requested | `escalation.trigger` | User requests agent |

The NBA is recalculated after each pipeline step via the NBA Trigger (see WORKFLOW_EXECUTION_ARCHITECTURE.md §1.7). Every pipeline step emits an `audit_event` recorded in the turn history.

---

*Document patrimonial Gold — Toute reconstruction doit respecter ce modèle validé.*
