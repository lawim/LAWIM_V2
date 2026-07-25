# LAWIM — Project Master Context

## Metadata
- **HEAD :** 1056ec68
- **Branche active :** feature/lawim-v1-definitive-cleanup-20260725
- **Branche de production :** main
- **Tags de release :** lawim-v3-program-f-conversation-engine-complete, lawim-v1-runtime-clean, lawim-v1-pre-cleanup-20260725-160240
- **Tags de preuve :** lawim-pre-runtime-consolidation-20260725-143856, lawim-pre-consolidation-20260725-143856, lawim-v1-pre-cleanup-20260725-160240
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

### Scripts canoniques
| Fonction | Script | Statut |
|---|---|---|
| Deploiement OVH | deployment/scripts/deploy_program_f_acceptance.sh | **CANONIQUE** |
| Acceptance Web | deployment/scripts/acceptance_program_f_web.py | **CANONIQUE** |
| Validation gold corpus | scripts/g5_validate_corpus.py | **CANONIQUE** |
| Validation G.5 | scripts/g5_validate_corpus.py | **CANONIQUE** |
| Admin reset password | scripts/admin_reset_password.py | **CANONIQUE** |

### Docker Compose
| Environnement | Fichier | Statut |
|---|---|---|
| Production OVH | deployment/compose/docker-compose.ovh.yml (ou .prod.yml adapte) | **CANONIQUE** |
| Developpement | deployment/compose/docker-compose.dev.yml | Support |
| Staging | deployment/compose/docker-compose.staging.yml | Support |

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
    -> Fallback: ConversationStateEngine (V2) [si PF indisponible]
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

| Suite | Commande | Resultat |
|---|---|---|
| Conversation | python3 -m pytest lawim_runtime/conversation/tests/ | 118 PASS |
| Globale | python3 -m pytest --ignore=tests --ignore=code --ignore=docs --ignore=demo --ignore=deployment | 856 PASS |
| Gold corpus | python3 scripts/g5_validate_corpus.py | 30 sc. 20 PASS / 10 FAIL |

## Limites connues

1. **Derives PCM (10 scenarios)** : Les templates PCM utilisent un anglais simplifie, _detect_language classe comme EN
2. **PostgreSQL** : Adaptateur code present mais validation reelle bloquee (abel n'a pas CREATEDB)
3. **Gold corpus** : Clarification, restart, annulation non couverts dans les 30 scenarios
4. **Barriere metier** : Active, biz_unexpected != 0 → RC non-zero

## Branches

### Actives
- main (production)
- feature/program-g5d-regression-recovery-20260724 (travail en cours)
- feature/program-f-conversation-engine (archive, fusionne dans main)

### Historiques (non fusionnees, a archiver)
- feature/action-execution-engine-20260722
- feature/ai-intelligence-platform-20260723
- feature/controlled-response-generation-20260721
- feature/conversation-memory-continuity-20260721
- feature/demo-world-*
- feature/external-operational-certification-20260723
- feature/interaction-platform-multichannel-20260723
- feature/production-*
- feature/program-e-completion-20260723
- feature/program-g2-*
- feature/program-g5-multilingual-semantic-postgres-20260724
- feature/project-profile-field-registry-20260722
- feature/qualification-decision-engine-20260722
- governance/vscode-lawim-context-20260720

## Prochaine etape recommandee
- Fusionner feature/program-g5d-regression-recovery-20260724 dans main
- Tagguer lawim-v3-program-g5-stability-complete
- Nettoyer les branches historiques
- Programme G.6 : 10 000 conversations industrielles (si PostgreSQL valide)
