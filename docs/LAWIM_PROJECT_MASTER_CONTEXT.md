# LAWIM — Project Master Context

## Metadata
- **HEAD :** e39c2c51
- **Origin/main :** d7cdd410 (push pending)
- **Branche active :** main
- **Branche active secondaire :** maintenance/1.0.x
- **Tags de release :** lawim-v1.0.0, lawim-v1.0.0-multichannel-accepted
- **Tags supprimés :** 320 tags historiques supprimés (restent uniquement les 2 tags V1)
- **Remote :** git@github-lawim:lawim/LAWIM_V2.git

## Architecture canonique

### Moteur conversationnel
| Composant | Emplacement | Statut |
|---|---|---|
| **ConversationJourneyOrchestrator** | lawim_runtime/conversation/journey.py:432 | **CANONIQUE** |
| ProgramFEngineAdapter (adapter) | code/lawim_v2/conversation/program_f_adapter.py | **CANONIQUE** |
| ConversationStateEngine (V2 legacy) | ~~code/lawim_v2/conversation/state/engine.py~~ | **SUPPRIME** (cleanup 1056ec68) |
| IntentEngine | lawim_runtime/conversation/intent/__init__.py | **CANONIQUE** |
| EntityExtractionEngine | lawim_runtime/conversation/entity/__init__.py | **CANONIQUE** |
| QualificationEngine | lawim_runtime/conversation/qualification/__init__.py | **CANONIQUE** |
| ConversationMemory | lawim_runtime/conversation/memory/__init__.py | **CANONIQUE** |

### Repositories
| Repository | Technologie | Emplacement | Statut |
|---|---|---|---|
| JourneyState (conversationnel) | SQLite | _SQLiteJourneyRepository dans program_f_adapter.py | **CANONIQUE** |
| Metier (marketplace) | PostgreSQL (prod), SQLite (dev) | _PostgresMarketplaceRepository / _SQLiteMarketplaceRepository dans marketplace_adapter.py | **CANONIQUE** |
| V2 ConversationStateRepository | SQLite | ConversationStateRepository (fallback V2) | Fallback |

### Scripts canoniques (conservés)
| Fonction | Script | Statut |
|---|---|---|
| Deploiement OVH | deployment/scripts/deploy_program_f_acceptance.sh | **CANONIQUE** |
| Acceptance Web | deployment/scripts/acceptance_program_f_web.py | **CANONIQUE** |
| Deploiement general | deployment/scripts/deploy.sh | **CANONIQUE** |
| Rollback | deployment/scripts/rollback.sh | **CANONIQUE** |
| Backup | deployment/scripts/backup.sh | **CANONIQUE** |
| Restore | deployment/scripts/restore.sh | **CANONIQUE** |
| Healthcheck | deployment/health/health_checker.py | **CANONIQUE** |
| Migration plan | deployment/migration/ (6 fichiers) | **CANONIQUE** |
| Migrations Prisma | prisma/migrations/ (3 migrations) | **CANONIQUE** |

### Scripts supprimés (récupérables via Git)
- `scripts/` entier (56 fichiers) : dev, validation, QA — non nécessaires au runtime
- `scripts/g5_validate_corpus.py` → `git show d7cdd410:scripts/g5_validate_corpus.py`
- `scripts/admin_reset_password.py` → `git show d7cdd410:scripts/admin_reset_password.py`

### Docker Compose
| Environnement | Fichier | Statut |
|---|---|---|
| Production OVH | /opt/lawim/compose/docker-compose.ovh.yml | **CANONIQUE** |
| Production (deployment) | deployment/compose/docker-compose.prod.yml | **CANONIQUE** |
| Developpement | deployment/compose/docker-compose.dev.yml (supprimé — récup. git) | HISTORICAL |
| Staging | deployment/compose/docker-compose.staging.yml (supprimé — récup. git) | HISTORICAL |

## Pipeline de traitement d'un message

```
Web/WhatsApp/Telegram
  -> CommunicationService._generate_ai_reply()
    -> ProgramFEngineAdapter.process_turn() [PRIMARY]
      -> _SQLiteJourneyRepository.load() (chargement etat)
      -> ConversationJourneyOrchestrator.process()
        -> IntentEngine.detect() [INTENT_PRIORITY hierarchy]
        -> EntityExtractionEngine.extract()
        -> FactFusionEngine.fuse()
        -> QualificationEngine.evaluate()
        -> _build_response_plan() [with _msg() templates FR/EN/PCM]
        -> _execute_business_action()
          -> PropertySearchService.create_search_request()
            -> MarketplacePropertySearchAdapter
              -> _PostgresMarketplaceRepository [PostgreSQL, si database_url]
              -> _SQLiteMarketplaceRepository [SQLite, fallback]
        -> _SQLiteJourneyRepository.save() (persistance etat)
    -> Fallback: safety response (ProgramFEngineAdapter gère son propre fallback interne)
```

## OVH

- **Host :** vps-6da158cc.vps.ovh.net (164.132.44.192)
- **Utilisateur SSH :** ubuntu (mot de passe fourni en-dehors de Git)
- **Chemin canonique :** /opt/lawim/releases/f1c4734b/ (current -> f1c4734b)
- **Compose :** /opt/lawim/compose/docker-compose.ovh.yml
- **Donnees runtime :** /opt/lawim/data/runtime/
- **SQLite Journey :** /opt/lawim/data/runtime/conversation/program_f_state.sqlite3
- **PostgreSQL :** interne au compose, base lawim_v2
- **Services :** 3 conteneurs (app, postgres, redis)

## Tests

| Suite | Commande | Resultat | Date |
|---|---|---|---|
| Conversation + Runtime | `pytest tests/test_conversation_*.py lawim_runtime/ -q` | **988 PASS, 0 FAIL** | 2026-07-26 |
| Full suite | `pytest tests/ lawim_runtime/ -q` | **5,087 PASS, 0 FAIL** | 2026-07-26 |
| Compilation | `compileall lawim_runtime code` | **0 erreurs** | 2026-07-26 |

Tests supprimés : 107 (27 LEGACY, 80 HISTORICAL, 0 UNKNOWN).
Détail dans `docs/reviews/release/e39c2c51-disappeared-tests.json`.

## 23 Capacités V1 validées

| # | Capacité | Tsts | Canal | Preuve runtime |
|---|---|---|---|---|
| 1 | Qualification location | 14 | Web/TG/WA | SQLite state |
| 2 | Qualification achat | 2 | Web | PostgreSQL |
| 3 | Correction budget | 7 | Web | SQLite history |
| 4 | Correction zone | 7 | Web | SQLite history |
| 5 | Plusieurs zones | 17 | Web | SQLite history |
| 6 | Date d'entrée | 72 | Web | SQLite history |
| 7 | Négation | 2 | TG/WA | Pipeline |
| 8 | Confirmation | 19 | TG/WA | Pipeline |
| 9 | Refus | 2 | TG/WA | Pipeline |
| 10 | Consentement métier | 13 | TG/WA | Pipeline |
| 11 | Création métier | 5 | Web | PostgreSQL objects |
| 12 | Idempotence | 21 | TG/WA | Duplicate detection |
| 13 | Restart | 2 | TG/WA | State persists |
| 14 | SQLite | 31 | All | program_f_state.sqlite3 |
| 15 | PostgreSQL | 13 | All | lawim-postgres |
| 16 | Web | 4 | Web | https://lawim.app |
| 17 | Telegram | 3 | TG | event 524 |
| 18 | WhatsApp | 30 | WA | event 525 |
| 19 | Authentification | 32 | Web | API |
| 20 | Administration | 33 | Web | API |
| 21 | Sécurité | 11 | All | API |
| 22 | Healthz | 23 | API | HTTP 200 |
| 23 | Readyz | 24 | API | HTTP 200 |

## Limites connues

1. **Derives PCM** : Identifiées, à corriger dans LAWIM V1.1
2. **PostgreSQL** : Operationnel sur OVH (`lawim-postgres` sain)
3. **e39c2c51** : Non encore poussé sur origin/main
4. **Tags OVH** : 322 tags historiques encore présents sur OVH (sync git push)
5. **Anciens scripts/répertoires** : Récupérables via Git (`git show d7cdd410:<path>`)

## Branches

| Branche | Statut |
|---|---|
| main | **ACTIVE** — production |
| maintenance/1.0.x | **ACTIVE** — support V1 |
| Toutes les autres (23) | **SUPPRIMEES** — fusionnées dans main |

## Traçabilité des suppressions

Index de récupération : `docs/consolidation/deleted-evidence-recovery-index.md`
Tests disparus : `docs/reviews/release/e39c2c51-disappeared-tests.json`
Rapport de vérification : `docs/reviews/release/e39c2c51-baseline-independent-verification.md`
Certification finale : `docs/reviews/release/e39c2c51-baseline-final-certification.md`

## Prochaine etape recommandee
- **LAWIM V1.1 — PCM STABILIZATION** (après push de e39c2c51 sur origin/main)
- Pousser e39c2c51 sur origin/main
- Déployer e39c2c51 sur OVH (docker build + compose up -d)
- Synchroniser tags OVH
