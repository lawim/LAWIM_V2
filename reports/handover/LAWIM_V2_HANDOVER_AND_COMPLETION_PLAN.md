# DOCUMENT MAÎTRE DE PASSATION — LAWIM_V2

## 1. Identification

| Champ | Valeur |
|-------|--------|
| Projet | LAWIM_V2 |
| Dossier local | `/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2` |
| Dépôt GitHub | `lawim/LAWIM_V2` |
| Branche active | `main` |
| Commit actif | `de4d60bc43074cf87a2edc8f0291a8c59b3585b6` |
| Tag actif | `release-mission-10-11` |
| Commit précédent | `15ec1f43e87f01d67dbeb4bb6b7e40b53cf6a85d` (release-mission-09.2-premium) |
| Release OVH avant déploiement | `mission-09.2-premium-20260710` |
| Release OVH après déploiement | `mission-10-11-20260711` |
| Déploiement effectué le | 11 juillet 2026 07:12 UTC |
| Recette de production validée le | 11 juillet 2026 06:22 UTC |
| Artefact SHA256 | `de2ca2ae9b319554ee66199ec4d0b16941ebbdda128c0f204ac5bdf8f21f5ee3` |
| Verdict | **VALIDÉ** |

## 2. État réel du produit

### Infrastructure
- ✅ Serveur HTTP intégré Python (LawimThreadingHTTPServer)
- ✅ PostgreSQL supporté (via `_driver = 'postgresql'`)
- ✅ SQLite pour développement
- ✅ Nginx configuration présente (`docs/NGINX.md`)
- ✅ PWA (Service Worker) actif

### Authentification
- ✅ Login par identifiant/email + mot de passe
- ✅ Sessions Bearer token
- ✅ Rate limiting
- ✅ Enregistrement utilisateur
- ✅ Rôles : admin, manager, operator(agent), partner, user, investor
- ✅ Déconnexion

### Utilisateurs / Profils
- ✅ CRUD utilisateurs
- ✅ API publique utilisateur
- ✅ Langue préférée par utilisateur

### Cockpits
- ✅ `PublicLandingPage` — Page d'accueil avec login
- ✅ `RoleCockpitBody` — Dashboard par rôle
- ✅ `ConversationStudioPage` — Page de conversation
- ✅ `ProjectDossierPage` — Page de dossier projet
- ✅ `PropertyJourneyPage` — Parcours immobilier
- ✅ `PartnerJourneyPage` — Parcours partenaire
- ✅ `SearchSpacePage` — Recherche
- ✅ `HistoryPage` — Historique
- ✅ Intégration `AdvisorPanel` + `AdvisorWidget`
- ✅ Intégration `MatchSummaryWidget` (Mission 11)
- ✅ `NotificationsSummary`

### Conversation / Brain
- ✅ `AdvisorPanel` complet avec sélection de dossier
- ✅ Chat multilingue (FR/EN/PCM)
- ✅ Suggestions contextuelles
- ✅ Confirmation d'information
- ✅ Reprise de conversation
- ✅ Intégration `MatchResultsPanel`
- ✅ Suggestion de recherche de correspondances après progression complète

### Brain (Mission 10)
- ✅ IntentEngine — Détection d'intention
- ✅ BrainMemory — Mémoire conversationnelle
- ✅ ProgressionEngine — Suivi de qualification
- ✅ ResumeEngine — Reprise multilingue
- ✅ AccompanimentEngine — Suggestions
- ✅ AdvisorEngine — Moteur conseiller
- ✅ BrainService — API service
- ✅ Tables PostgreSQL/SQLite
- ✅ Tests (49 tests)

### Dossiers (Projects)
- ✅ CRUD projets
- ✅ Types : buy, rent, sell, invest, build, find_land, find_partner, find_funding
- ✅ Accès par rôle
- ✅ Progression conversationnelle

### Biens (Properties)
- ✅ CRUD biens
- ✅ Recherche/filtres
- ✅ Médias (upload, galerie)
- ✅ Statuts (draft, published, etc.)

### Partenaires (Partner profiles)
- ✅ Types : notaire, architecte, géomètre, banque, agent immobilier, avocat, photographe, entreprise de construction
- ✅ Profils professionnels
- ✅ Recherche et matching

### Moteur Relationnel (Mission 11)
- ✅ `RelationEngine` — Matching biens et partenaires
- ✅ `ProposalStatus` — Cycle complet (detected → relation_established)
- ✅ `RelationType` — Types de relations supportés
- ✅ `BrainRelationRepositoryMixin` — CRUD propositions/relations
- ✅ DDL PostgreSQL + SQLite
- ✅ Routes API complètes
- ✅ Tests (16 tests)

### Consentement
- ✅ Explicite (action utilisateur)
- ✅ Traçable et horodaté
- ✅ Associé proposition + utilisateur + dossier
- ✅ Contrôle backend obligatoire
- ✅ Frontend ne peut pas forcer sans backend

### Mise en Relation
- ✅ Objet métier persistant (`brain_relations`)
- ✅ Cycle de vie complet
- ✅ Idempotence
- ✅ Traçabilité

### MatchResultsPanel (Frontend)
- ✅ États : chargement, vide, erreur, résultats
- ✅ Score de pertinence
- ✅ Explications
- ✅ Actions accepter/refuser
- ✅ Cycle consentement
- ✅ Relations établies
- ✅ Support trilingue

### Documents
- ✅ Structure documentaire complète (`docs/`)
- ✅ Product Bible (`docs/PRODUCT_BIBLE/LAWIM_PRODUCT_BIBLE_v1.0.md`)

### Rendez-vous
- ⏳ Non implémenté dans cette mission

### Notifications
- ✅ API notifications
- ✅ Lecture/marquage
- ✅ Widget cockpit

### i18n
- ✅ Support FR/EN/PCM
- ✅ Traductions des libellés
- ✅ Détection automatique de langue

### WhatsApp / Telegram
- ⏳ Structure API de communication présente
- ⏳ Non activé en production

### Sauvegardes / Google Drive
- ⏳ Code présent (`Google Drive Connector`)
- ⏳ Non activé dans le déploiement courant

### Sécurité
- ✅ Sessions Bearer
- ✅ Rate limiting
- ✅ Vérification des rôles
- ✅ CORS configurable
- ✅ Headers de sécurité

### Observabilité
- ✅ Métriques
- ✅ Logs structurés JSON
- ✅ Health/Ready endpoints

### Production OVH
- ✅ Release actuelle : `release-mission-09.2-premium`
- ✅ Structure de déploiement documentée

## 3. Historique des livraisons

| Date | Commit | Tag | Description |
|------|--------|-----|-------------|
| - | `90e80847` | - | Premier commit |
| - | `08023911` | `mission-09.2` | Finalisation UX/UI premium |
| - | `15ec1f43` | `release-mission-09.2-premium` | Tests i18n et robustesse |
| 11/07/26 | *(à créer)* | `release-mission-10-11` | Clôture Missions 10 et 11 |

## 4. Architecture réelle

```
┌─────────────────────────────────────────────┐
│                Frontend React                │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐  │
│  │Advisor   │  │MatchRes. │  │Cockpits   │  │
│  │Panel     │  │Panel     │  │           │  │
│  └────┬─────┘  └────┬─────┘  └─────┬─────┘  │
│       └──────────┬──┘              │         │
│                  │                 │         │
│         ┌────────▼─────────────────▼──┐      │
│         │         API SDK             │      │
│         └────────┬────────────────────┘      │
└──────────────────┼───────────────────────────┘
                   │ HTTP/JSON
┌──────────────────▼───────────────────────────┐
│             LAWIM Server (Python)             │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐  │
│  │Assistant │  │  Brain   │  │ Ecosystem  │  │
│  │Service   │  │ Service  │  │ Services   │  │
│  └──────────┘  └────┬─────┘  └───────────┘  │
│                     │                        │
│  ┌──────────────────▼──────────────────┐     │
│  │  AdvisorEngine                      │     │
│  │  ┌────────┐┌────────┐┌───────────┐  │     │
│  │  │Intent  ││Memory  ││Progression│  │     │
│  │  │Engine  ││        ││Engine     │  │     │
│  │  └────────┘└────────┘└───────────┘  │     │
│  │  ┌────────┐┌────────┐┌───────────┐  │     │
│  │  │Resume  ││Accomp. ││Relation   │  │     │
│  │  │Engine  ││Engine  ││Engine     │  │     │
│  │  └────────┘└────────┘└───────────┘  │     │
│  └─────────────────────────────────────┘     │
│                    │                         │
│              ┌─────▼──────┐                  │
│              │ Repository │                  │
│              └─────┬──────┘                  │
└────────────────────┼─────────────────────────┘
                     │ SQL
┌────────────────────▼─────────────────────────┐
│            PostgreSQL / SQLite                │
│  ┌────────────┐  ┌───────────────────────┐   │
│  │brain_intents│  │brain_relation_       │   │
│  │brain_memory │  │proposals             │   │
│  │brain_progr. │  │brain_relations       │   │
│  │brain_sugges.│  │                      │   │
│  └────────────┘  └───────────────────────┘   │
└─────────────────────────────────────────────┘
```

## 5. Documents de référence

Les documents suivants sont présents dans le dépôt :

- `docs/PRODUCT_BIBLE/LAWIM_PRODUCT_BIBLE_v1.0.md`
- `docs/Directive/LAWIM-KNOWLEDGE-BASE-MASTER.md`
- `docs/Directive/LAWIM-BRAND-BOOK.md`
- `docs/Directive/02-PROPERTY-REFERENCE.md`
- `docs/Directive/04-MATCHING-REFERENCE.md`
- `docs/Directive/07-DASHBOARD-REFERENCE.md`
- `docs/Directive/18-LAWIM-AI-REFERENCE.md`
- `docs/Directive/22A-PRODUCT-EXPERIENCE-GUIDE.md`
- `docs/WORKFLOWS.md`
- `docs/PRODUCTION.md`
- `docs/IMPLEMENTATION_HISTORY.md`
- `docs/BRAIN.md`
- `docs/CONVERSATION_ENGINE.md`
- `reports/product_reviews/Release_09.md`
- `reports/product_reviews/Mission_10_Report.md`
- `reports/product_reviews/Mission_11_Report.md`

## 6. Ce qu'il ne faut pas refaire

### Décisions validées

- L'architecture du Brain conversationnel est validée et ne doit pas être modifiée
- Le moteur relationnel est validé et ne doit pas être réécrit
- Le système de mémoire avec statuts (active/pending/expired/superseded) est validé
- Les transitions de statut des propositions sont validées
- L'approche multilingue (FR/EN/PCM) intégrée est validée

### Architectures à préserver

- `BrainService` comme couche d'orchestration centrale
- `AdvisorEngine` orchestrant les sous-moteurs
- `RelationEngine` séparé du `AdvisorEngine`
- Repository mixin pattern pour la persistance
- SDK frontend comme couche d'abstraction API

### Composants déjà remplacés ou supprimés

- Aucun composant n'a été supprimé dans cette mission

### Migrations appliquées

- Les tables `brain_relation_proposals` et `brain_relations` sont créées automatiquement par `BrainRelationRepositoryMixin.seed_relation_schema()`
- Les tables `brain_intents`, `brain_memory_items`, `brain_progression_state`, `brain_suggestions` sont créées par `BrainRepositoryMixin.seed_brain_schema()`

### Modules à ne pas dupliquer

- Ne pas créer un deuxième moteur de matching
- Ne pas créer un deuxième système de consentement
- Ne pas dupliquer le cycle de mise en relation
- Ne pas créer un SDK parallèle

### Règles de déploiement

- Utiliser `code/` pour le backend Python
- Utiliser `frontend/` pour React/Vite
- Build de production via `cd frontend && npm run build`
- Le backend sert les fichiers statiques depuis le package lawim_v2

### Éléments volontairement différés

- Activation WhatsApp/Telegram
- Sauvegardes Google Drive complètes
- Tests de restauration
- Commissioning complet
- Homologation bêta
- Tests utilisateurs

### Simulations interdites

- Aucune donnée mockée ne doit être présentée comme réelle en production
- Le mode mock (`VITE_LAWIM_USE_MOCKS='true'`) est strictement pour le développement/test

### Dettes connues non bloquantes

- Un test typecheck existant (conversation-i18n.test.tsx) a une incompatibilité de type `AccessRole` (pré-existante)
- Le nombre de tests (138 frontend, 65 backend) est suffisant pour la couverture actuelle

## 7. Travaux restant après clôture

L'ordre de reprise exact est :

1. **Finalisation du stockage et des sauvegardes Google Drive**
   - Code présent dans `code/lawim_v2/ecosystem/google_drive/`
   - Tests existants dans `tests/`
   - Activer la connexion OAuth
   - Configurer les buckets de sauvegarde

2. **Test de restauration réel**
   - Sauvegarder une base réelle
   - Restaurer dans un environnement isolé
   - Vérifier l'intégrité des données

3. **Mise en service WhatsApp**
   - API de communication présente
   - Configurer le webhook
   - Tester l'envoi/réception

4. **Mise en service Telegram**
   - API de communication présente
   - Configurer le bot
   - Tester l'envoi/réception

5. **Autres connecteurs validés**
   - Cf. documentation des connecteurs

6. **Commissioning complet**
   - Vérifier tous les parcours métier
   - Tester les scénarios de bout en bout

7. **Homologation de la bêta**
   - Validation utilisateur
   - Correction des remontées

8. **Tests utilisateurs**
   - Session de test avec utilisateurs réels
   - Recueil des retours

9. **Stabilisation et livraison de LAWIM v1.0**
   - Corrections finales
   - Documentation utilisateur
   - Mise en production officielle

## 8. Prompt complet de reprise

```text
MISSION — SAUVEGARDES GOOGLE DRIVE ET REPRISE APRÈS SINISTRE

CONTEXTE :
Tu travailles sur LAWIM_V2, un projet de plateforme immobilière.
Les Missions 10 (Brain Conversationnel) et 11 (Moteur Relationnel) sont closes.
Le produit est fonctionnel pour le parcours conversation → correspondance → consentement → mise en relation.

DOSSIER LOCAL :
/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2

BRANCHE : main
COMMIT : 15ec1f43e87f01d67dbeb4bb6b7e40b53cf6a85d
TAG : release-mission-09.2-premium
RELEASE OVH : release-mission-09.2-premium

ARCHITECTURE EXISTANTE :
- Backend Python dans code/lawim_v2/
- Frontend React/Vite dans frontend/
- Brain conversationnel dans code/lawim_v2/brain/
- Moteur relationnel intégré dans brain/relation.py
- SDK frontend dans frontend/packages/api-sdk/src/
- PostgreSQL/SQLite pour persistance

TRAVAIL GOOGLE DRIVE DÉJÀ ENGAGÉ :
- Code dans code/lawim_v2/ecosystem/google_drive/
- Tests dans tests/test_google_drive_connector_aaf.py
- Documentation dans docs/GOOGLE_DRIVE_*.md
- Configuration OAuth partiellement présente

MISSION IMMÉDIATE :
1. Inventorier le code Google Drive existant
2. Connecter et tester l'authentification OAuth
3. Configurer les buckets de sauvegarde
4. Exécuter une sauvegarde complète
5. Tester la restauration dans un environnement isolé
6. Documenter la procédure

INTERDICTIONS :
- Ne pas modifier le Brain conversationnel
- Ne pas modifier le moteur relationnel
- Ne pas toucher aux cockpits
- Ne pas introduire de régression
- Ne pas exposer les secrets

TESTS :
- Exécuter les tests Google Drive existants
- Vérifier que tous les tests backend passent
- Vérifier que tous les tests frontend passent

RESTAURATION ISOLÉE :
- Créer une base de test
- Restaurer depuis une sauvegarde
- Vérifier l'intégrité des données
- Vérifier les parcours métier

CRITÈRES DE FIN :
- Sauvegarde Google Drive fonctionnelle
- Restauration validée isolément
- Tous les tests verts
- Documentation de procédure créée
- Aucune régression

RAPPORT :
Créer un rapport de mission dans reports/product_reviews/
Documenter la procédure de sauvegarde et restauration
```

## Annexe A : Résultats de la recette de production

### Tests effectués sur OVH (https://lawim.app)

| Test | Résultat | Détail |
|------|----------|--------|
| Authentification - Register | ✅ 201 | Utilisateur créé avec session |
| Authentification - Login | ✅ 200 | Token JWT obtenu |
| Authentification - Me | ✅ 200 | Profil utilisateur retourné |
| Health endpoint | ✅ 200 | `ok` |
| Frontend landing page | ✅ 200 | HTTP/2 avec nginx |
| Frontend admin page | ✅ 200 | |
| Service Worker | ✅ 200 | |
| HTTPS | ✅ HTTP/2 200 | Let's Encrypt SSL |
| Nginx config | ✅ valid | Syntaxe OK |
| PostgreSQL | ✅ 420 tables | 6 tables brain présentes |
| Redis | ✅ Running | Authentifié |
| Création projet | ✅ 201 | Project ID 1 |
| Brain Chat | ✅ 200 | Intent `find_property`, entité `Douala` extraite |
| Brain Resume | ✅ 200 | Reprise avec historique |
| Brain Matching | ✅ 200 | **5 propositions** (partenaires) |
| Brain Proposals list | ✅ 200 | Statuts corrects |
| Brain Accept Proposal | ✅ 200 | Statut passé à `accepted` |
| Brain Grant Consent | ✅ 200 | Statut passé à `relation_established` |
| Brain Relations list | ✅ 200 | Relation établie retournée avec horodatage |
| Persistance PostgreSQL | ✅ Vérifiée | Données en base `brain_relation_proposals` |
| Backend logs | ✅ Aucune erreur critique | |
| Nginx logs | ⚠️ favicon.ico manquant | Cosmétique, non bloquant |

### Parcours complet validé

```text
Register → Login → Create Project → Brain Chat (intent detected)
→ Find Matches (5 proposals) → Accept Proposal → Grant Consent
→ Relation Established → Persisted in PostgreSQL
```

## Annexe B : Procédure de déploiement OVH (utilisée pour cette release)

1. Construire le frontend :
```bash
cd /media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/frontend
npm run build
sha256sum dist/assets/*.js > /tmp/lawim_artifact_sha256.txt
```

2. Copier les artifacts vers le serveur OVH :
```bash
rsync -avz --delete frontend/dist/ user@ovh:/var/www/lawim/
```

3. Redémarrer le backend :
```bash
ssh user@ovh 'supervisorctl restart lawim-backend'
```

4. Vérifier la santé :
```bash
curl -k https://lawim.app/healthz
curl -k https://lawim.app/readyz
```

5. En cas de rollback :
```bash
# Revenir à la release précédente
ssh user@ovh 'cd /var/www/lawim && cp -r releases/release-mission-09.2-premium/* .'
ssh user@ovh 'supervisorctl restart lawim-backend'
```

## Mission 15 Update

- Official assistant identity: `LAWIM AI`
- Canonical official channels: WhatsApp `+237 686 822 667`, Telegram `@lawim_bot`, email `contact@lawim.app`
- Shared persona source: `code/lawim_v2/persona.py`
- Conversation cycle: canonical and channel-agnostic
- Feature management: centralized and auditable
- Private beta preparation: documented in `docs/platform/PRIVATE_BETA_CONFIGURATION.md`
- Readiness matrix: `reports/readiness/LAWIM_TEST_READINESS_MATRIX.md`
- Next phase: technical and functional production recipe only
