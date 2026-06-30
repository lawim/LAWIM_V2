# LAWIM 2.x — Architecture Principles

**Programme :** LAWIM_2X  
**Base runtime :** LAWIM v1.0.0 monolith (`code/lawim_v2/`)  
**Branche :** `develop/2.0-intelligent-platform`

---

## 1. Philosophie

LAWIM 2.x **étend** le monolithe 1.0 par **modules à frontières claires**, pas par réécriture. L’objectif est une plateforme intelligente maintenable par une petite équipe, avec un chemin de migration progressif vers des services séparés **uniquement** lorsque la charge ou l’équipe le justifient.

---

## 2. Principes fondamentaux

### P1 — Projet avant annonce

Le modèle de domaine 2.x place **Project** au centre. Property, Conversation, Match, ServiceOrder sont des **agrégats liés** au projet, pas des silos indépendants.

```
User ──► Project ──► Journey (state machine)
              ├── Properties (0..n)
              ├── Conversations / Negotiations
              ├── Knowledge queries
              ├── Partner assignments
              └── Service orders
```

### P2 — API-first, mobile-ready

- Toute capacité 2.x expose d’abord une **API HTTP JSON** stable.
- Le bootstrap UI 1.0 reste un client ; la PWA 2.x en est un autre.
- Versionnement API : `/api/v2/...` pour les nouveaux domaines ; `/api/...` 1.0 inchangé jusqu’à dépréciation explicite.

### P3 — Connaissance séparée du code

Le **Knowledge Engine** est un module avec :

- Schéma de contenu versionné (pas hardcodé dans `server.py`)
- Ingestion, indexation, recherche dédiées
- Pas de logique métier immobilière dans les templates de contenu

Permet alimentation par équipe éditoriale / partenaires sans redéploiement applicatif complet.

### P4 — IA avec garde-fous

- **RAG obligatoire** : réponses assistant ancrées dans knowledge + contexte projet autorisé.
- **Human-in-the-loop** : escalade vers agent/partenaire sur décisions sensibles.
- **Audit** : journalisation requêtes/réponses (sans données sensibles en clair dans logs publics).
- **Pas de LLM en chemin critique transactionnel** (paiement, signature, validation juridique).

### P5 — Confiance explicable

Le **Trust Scoring** produit des scores **décomposables** (facteurs + poids + date). Pas de modèle opaque unique bloquant l’accès utilisateur sans recours admin.

### P6 — Événements pour l’analytics

- Actions utilisateur significatives émises comme **Product Events** (schema versionné).
- Stockage initial : table PostgreSQL / SQLite `product_events` ; export futur vers BI.
- Corrélation possible avec `audit_events` 1.0 sans les fusionner.

### P7 — Persistance additive

- Migrations **additives** uniquement (schema v6+ sur branche 2.x).
- SQLite dev / PostgreSQL prod conservés (héritage WEEK-002).
- Prisma schema aligné pour documentation et tooling.

### P8 — Sécurité héritée et renforcée

Conserver et étendre les acquis 1.0 :

- Sessions, RBAC, rate limiting auth, CORS allowlist, validation config prod
- RBAC 2.x : rôles `partner`, `knowledge_editor` en extension
- Isolation stricte des données par `user_id` / `project_id`

### P9 — Testabilité

- Chaque module 2.x : tests unitaires + intégration HTTP.
- Régression suite 1.0 obligatoire avant merge programme.
- Pas de feature sans critère de sortie testable.

### P10 — Observabilité

- Métriques latence héritées (WEEK-002) étendues aux nouveaux endpoints.
- Traces corrélées par `request_id` et `project_id` quand applicable.
- `/readyz` inclut dépendances 2.x (knowledge index, assistant provider health).

---

## 3. Architecture logique cible (2.0)

```
┌─────────────────────────────────────────────────────────────────┐
│                     Clients (Web PWA, Mobile)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS JSON
┌────────────────────────────▼────────────────────────────────────┐
│              LAWIM HTTP Server (Python 3.12 monolith)            │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │
│  │ Core 1.0     │ │ Project &    │ │ Knowledge Engine         │ │
│  │ properties   │ │ Journey      │ │ ingest / search / version│ │
│  │ auth conv    │ │ module       │ └──────────────────────────┘ │
│  │ matching     │ └──────────────┘ ┌──────────────────────────┐ │
│  └──────────────┘ ┌──────────────┐ │ Assistant (RAG gateway)  │ │
│                   │ Trust Score  │ └──────────────────────────┘ │
│                   │ Marketplace  │ ┌──────────────────────────┐ │
│                   │ module       │ │ Analytics Events         │ │
│                   └──────────────┘ └──────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
         SQLite/PG      Media store    External LLM API
         (schema v6+)   (optional)     (configurable provider)
```

**Décision 2.0 :** monolithe modulaire. Extraction en microservices **différée** jusqu’à preuve de charge (matching sémantique, index vectoriel lourd).

---

## 4. Modules 2.x — responsabilités

| Module | Responsabilité | Dépendances |
|--------|----------------|-------------|
| **project** | CRUD projet, types, budget, stade | auth, db |
| **journey** | State machine parcours, reprise session | project |
| **knowledge** | Fiches, index, recherche, versioning | db |
| **assistant** | Orchestration RAG, prompts, garde-fous | knowledge, project |
| **partners** | Annuaire, qualification, zones | trust (lecture) |
| **trust** | Calcul score, facteurs, historique | partners, properties, audit |
| **marketplace** | Catalogue services, commandes, statuts | project, partners |
| **search_v2** | Index sémantique, matching enrichi | knowledge, project, properties |
| **analytics** | Ingestion events, agrégats, export | db |

Emplacement code proposé : `code/lawim_v2/modules/<name>/` avec enregistrement routes dans `server.py`.

---

## 5. Modèle de données (extensions preview)

Nouvelles tables indicatives (PROGRAM 002+) :

- `projects` — entité centrale
- `project_journey_states` — historique états parcours
- `knowledge_documents` — contenu structuré
- `knowledge_document_versions`
- `partner_profiles` — extension utilisateurs partenaires
- `trust_scores` — scores matérialisés + facteurs JSON
- `service_catalog`, `service_orders`
- `product_events` — analytics
- `assistant_sessions`, `assistant_messages` — audit IA

Relations existantes 1.0 (`properties`, `conversations`, `matches`) reçoivent `project_id` nullable puis requis par migration progressive.

---

## 6. Recherche intelligente (2.x)

**Phase 1 (PROGRAM 008) :**

- Index full-text PostgreSQL + embeddings optionnels (table `property_embeddings`)
- Requête hybride : filtres 1.0 + similarité vectorielle + signaux confiance
- Explication utilisateur : « pourquoi ce bien » (top 3 facteurs)

**Phase 2 (ultérieur) :** moteur dédié (OpenSearch, pgvector) si volume > seuil défini par DG.

---

## 7. Mobile-first

- **PWA** : service worker, manifest, responsive breakpoints mobile-first CSS
- API pagination et payloads optimisés (champs réduits `?fields=`)
- Notifications : Web Push puis FCM/APNs si apps natives
- Offline : cache lecture projets / fiches knowledge (pas écriture critique offline v1)

---

## 8. Intégrations externes (roadmap)

| Système | Usage | Programme |
|---------|-------|-----------|
| LLM provider (OpenAI-compatible) | Assistant RAG | 004 |
| Campay | Paiement services | 007 |
| Telegram / WhatsApp | Notifications, bot | 005+ |
| Géocodage (existant) | Enrichissement | 002 |
| BI / Metabase (futur) | Dashboards | 009 |

Toutes intégrations : **adapter pattern**, config via env, stubs en test.

---

## 9. CI/CD et branches

| Branche | Usage |
|---------|--------|
| `main` | Production 1.0 GA (gel) |
| `maintenance/1.0.x` | Correctifs 1.0 |
| `release/1.0.0-beta` | Beta 1.0 (gel) |
| `develop/2.0-intelligent-platform` | Développement 2.x |

Pipeline CI 2.x : tests 1.0 + tests modules 2.x + `git diff --check` + packaging.

Tags programme : `lawim-2x-program-NNN`.

---

## 10. Anti-patterns à éviter

1. Big bang rewrite du monolithe.
2. Logique métier dans les prompts LLM sans validation code.
3. Scores de confiance non auditables.
4. Marketplace sans qualification partenaires préalable.
5. Mobile comme afterthought (desktop-only d’abord).
6. Analytics sans schema d’events versionné.
7. Modifications rétroactives sur branches 1.0 gelées.

---

## 11. Décisions différées (ADR à produire en PROGRAM 002)

- Choix provider LLM et hébergement données (souveraineté)
- pgvector vs service vectoriel externe
- PWA seule vs React Native / Flutter
- Modèle pricing marketplace (forfait vs abonnement partenaire)

---

*Principes d’architecture programme — complètent le Plan Stratégique et la Vision Produit 2.x.*
