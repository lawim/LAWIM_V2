# LAWIM — Audit des Mémoires Existantes

**Date :** 2026-07-21
**Chantier :** 3 — Conversation Memory and Cross-Channel Continuity
**HEAD :** 21e2483e
**Branche :** feature/conversation-memory-continuity-20260721

## Résumé

5 sous-systèmes mémoire distincts identifiés. Aucun parallélisme critique, mais des
chevauchements entre `program_r.MemoryEntry`, `program_l.AgentMemory` et
`ai.memory.MemoryEntry`. Le chantier 3 doit consolider ces 3 représentations sous
une hiérarchie canonique unique sans créer de nouveau modèle parallèle.

---

## 1. ConversationState (state/state.py)

| Attribut | Valeur |
|----------|--------|
| **Module** | `code/lawim_v2/conversation/state/state.py` |
| **Responsabilité** | État actif du tour conversationnel : langue, intention, slots connus, dernière question, statut qualification, version |
| **Durée de vie** | Session active + persistée en base |
| **Source de vérité** | `conversation_states` table (SQLite/PostgreSQL) |
| **Clé** | `(channel, channel_session_id)` |
| **Persistance** | UPSERT dans `ConversationStateRepository` |
| **Consentement** | Aucun |
| **Appelants** | `ConversationStateEngine`, `ConversationService` |
| **Doublons** | Aucun (unique key) |
| **Conflits** | Pas d'optimistic locking — `version` existe mais n'est pas vérifiée |
| **Statut cible** | **CONSERVER** — ajouter `case_id`, `journey_code`, optimistic locking |

## 2. Fact-based Memory (memory/service.py + repository.py)

| Attribut | Valeur |
|----------|--------|
| **Module** | `code/lawim_v2/conversation/memory/service.py` |
| **Responsabilité** | Persistance des faits extraits (slots) avec versionnement via `supersedes_fact_id` |
| **Durée de vie** | Durée du projet/dossier |
| **Source de vérité** | `conversation_facts` table |
| **Clé** | `fact_id` |
| **Persistance** | INSERT + UPDATE (supersede) |
| **Consentement** | Aucun (données métier uniquement) |
| **Appelants** | `ConversationService`, `MemoryContextBuilder` (futur) |
| **Doublons** | Possible si plusieurs conversations pour un même projet |
| **Conflits** | Gérés via `supersedes_fact_id` (chaînage) |
| **Statut cible** | **CONSERVER** — consolider comme `SlotValueHistory` |

## 3. AI Memory (ai/memory.py)

| Attribut | Valeur |
|----------|--------|
| **Module** | `code/lawim_v2/ai/memory.py` |
| **Responsabilité** | Mémoire structurée pour contexte LLM : short_term, long_term, persistent |
| **Durée de vie** | TTL configurable (24h, 30j, ∞) |
| **Source de vérité** | In-memory + base via `MemoryOptimizer` |
| **Clé** | `(memory_type, key)` |
| **Persistance** | Via `MemoryOptimizer` |
| **Consentement** | Aucun |
| **Appelants** | `AIOrchestrator` |
| **Doublons** | Possible |
| **Conflits** | Non gérés |
| **Statut cible** | **RÉÉCRIRE** — remplacer par `MemoryContextBuilder` + `ProviderMemoryContext` |

## 4. Agent Memory (program_l/agent_models.py + runtime.py)

| Attribut | Valeur |
|----------|--------|
| **Module** | `code/lawim_v2/program_l/agent_models.py` |
| **Responsabilité** | Mémoire de travail des agents : `AgentMemory` avec `MemoryType` (WORKING, CONVERSATION, CASE, USER_PREFERENCE, etc.) |
| **Durée de vie** | Session agent (in-memory) |
| **Source de vérité** | `AgentMemoryService` (dict in-memory) |
| **Clé** | `(conversation_id, actor_id, case_id, key)` |
| **Persistance** | Aucune (in-memory) |
| **Consentement** | Aucun |
| **Appelants** | `AgentInvocationService` |
| **Doublons** | Possible |
| **Conflits** | Non gérés |
| **Statut cible** | **CONSERVER** — ajouter persistance optionnelle |

## 5. Memory Governance (program_r/r10_memory.py)

| Attribut | Valeur |
|----------|--------|
| **Module** | `code/lawim_v2/program_r/r10_memory.py` |
| **Responsabilité** | Politiques de rétention, gouvernance, `MemorySummary` |
| **Durée de vie** | Documentée |
| **Source de vérité** | Modèles de données uniquement |
| **Clé** | `entry_id` |
| **Persistance** | Non connectée au runtime |
| **Consentement** | `IntelligenceReview` |
| **Appelants** | Aucun (modèles non connectés) |
| **Doublons** | Aucun |
| **Conflits** | Non gérés |
| **Statut cible** | **CONNECTER** au runtime, pas de nouveau modèle |

## 6. Domain DossierInfo / ProjectInfo

| Attribut | Valeur |
|----------|--------|
| **Module** | `code/lawim_v2/conversation/domain/dossier.py`, `project.py` |
| **Responsabilité** | Modèles légers de dossier de recherche et de projet |
| **Durée de vie** | Cycle de vie projet/dossier |
| **Source de vérité** | Non persisté directement |
| **Persistance** | Non (utilisé comme DTO) |
| **Statut cible** | **RÉÉCRIRE** dans `LawimCase` unifié |

## 7. CRM Customer360 + Timeline

| Attribut | Valeur |
|----------|--------|
| **Module** | `code/lawim_v2/crm/engines.py`, `intelligent/engines.py` |
| **Responsabilité** | Vue 360° client, timeline CRM |
| **Persistance** | Via `intelligent/repository.py` |
| **Statut cible** | **CONSERVER** — déjà connecté au CRM |

## 8. UnifiedConversation (program_j/conversation.py)

| Attribut | Valeur |
|----------|--------|
| **Module** | `code/lawim_v2/program_j/conversation.py` |
| **Responsabilité** | Modèle de conversation intercanale unifiée |
| **Statut cible** | **CONSERVER** — sert de base pour CrossChannelIdentity |

---

## Décisions de Consolidation

| Modèle | Action |
|--------|--------|
| `ConversationState` | +case_id, +journey_code, +optimistic locking |
| `LawimCase` (nouveau) | Unifie DossierInfo + ProjectInfo + qualification state |
| `Fact` / `MemoryService` | Devient `SlotValueHistory` — déjà compatible |
| `AgentMemory` (program_l) | +persistance optionnelle |
| `MemoryEntry` (program_r) | Connecter au runtime comme couche de gouvernance |
| `AI Memory` (ai/memory) | Remplacer par `MemoryContextBuilder` |
| `ConversationSummary` | Nouveau service |
| `MemoryContextBuilder` | Nouveau — remplace AI Memory comme source LLM |
| `CrossChannelIdentityResolver` | Nouveau — utilise UnifiedConversation |
| `ActiveCaseResolver` | Nouveau |
| `MemoryRetentionPolicy` | Programme_r existant à connecter |

## Mémoires Parallèles Identifiées

1. `ai.memory.MemoryEntry` ↔ `program_l.AgentMemory` ↔ `program_r.MemoryEntry` — à unifier
2. `DossierInfo` + `ProjectInfo` — à fusionner dans `LawimCase`
3. `ConversationState.known_slots` + `conversation_facts` — faits dupliqués entre état de session et mémoire persistante

## Conflits Identifiés

- `ConversationStateRepository` n'a pas d'optimistic locking sur `version`
- `known_slots` dans `ConversationState` peut diverger des `conversation_facts`
- Aucun lien explicite conversation ↔ dossier (« case »)
- Aucune identité intercanale résolue
- Aucun `MemoryContextBuilder` pour limiter le contexte LLM
