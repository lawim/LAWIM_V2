# LAWIM — LPEP A.1 Audit et réparation de la chaîne d'exécution conversationnelle réelle

**Date :** 2026-07-27  
**HEAD local :** 8f3ebf9d  
**HEAD OVH :** 229d8cd3  
**Conteneur :** lawim-app (lawim/v3:latest)

## Résumé

L'audit révèle que le conteneur de production exécute un **serveur HTTP minimal
(`HealthHandler`)** défini en ligne dans `entrypoint.sh:51-71` qui ne sert que
`/health`, `/ready` et une page statique fourre-tout.

Le **serveur HTTP complet (`LawimRequestHandler`)** de 4104 lignes, qui
implémente toutes les routes API (webhooks Telegram/WhatsApp, conversations
web, API V3, etc.), est présent dans l'image mais **n'est jamais démarré**.

Aucune chaîne conversationnelle réelle ne peut fonctionner en production.

## Données brutes

### CONTAINER_ENTRYPOINT

- **Fichier :** `scripts/entrypoint.sh:38` → `ENTRYPOINT ["/app/entrypoint.sh"]`
- **Fichier image :** `/app/entrypoint.sh`
- **Lignes :** 72
- **Action :** Exécute un heredoc Python qui démarre `HealthHandler`

### CONTAINER_COMMAND

- **Fichier :** `deployment/compose/docker-compose.prod.yml:10-14`
- **Image :** `lawim/v3:${LAWIM_VERSION:-latest}`
- **Commande :** Aucune (`CMD` non définie, utilise `ENTRYPOINT`)
- **Docker inspect :** `"CMD": null, "ENTRYPOINT": ["/app/entrypoint.sh"]`
- **docker-compose.prod.yml ligne 14 :** `image: lawim/v3:${LAWIM_VERSION:-latest}` (pas de `command:`)

### PYTHON_MODULE_STARTED

- **Fichier :** `scripts/entrypoint.sh:11-72`
- **Lance :** `python3` avec un heredoc inline
- **N'utilise PAS :** `python -m lawim_v2` (qui irait dans `code/lawim_v2/__main__.py:1-7` puis `server.main()`)
- **N'utilise PAS :** `code/lawim_v2/asgi_app.py` (qui tenterait `from lawim_v2.communication import app` et crasherait car `app` n'existe pas dans `lawim_v2/communication/__init__.py`)
- **Modules importés par entrypoint.sh :** `lawim_v2.credential_vault.CredentialVault`, `lawim_v2.config.AppConfig`, `lawim_v2.bootstrap.build_runtime`, `http.server.BaseHTTPRequestHandler`
- **Modules NON importés par entrypoint.sh :** `lawim_v2.server.LawimRequestHandler`, `lawim_v2.server.create_server`, `lawim_v2.server.main`

### HTTP_APPLICATION_STARTED

- **Classe :** `HealthHandler` (définie dans `entrypoint.sh:51-67`)
- **Héritage :** `http.server.BaseHTTPRequestHandler`
- **Routes :**
  - `GET /health` → `{"status":"healthy"}` (200)
  - `GET /ready` → `{"status":"ready"}` (200)
  - `GET *` → `<h1>LAWIM Runtime</h1><p>Health: OK</p>` (200)
- **NOT started :** `LawimRequestHandler` dans `code/lawim_v2/server.py:68-4034` (ThreadingHTTPServer, 4104 lignes)
- **NOT started :** `create_server()` dans `server.py:4037-4056`

### WEB_CONVERSATION_ROUTES

**Routes définies dans `server.py` mais JAMAIS démarrées :**

- `GET /api/conversations` — `server.py:401-413`
- `GET /api/conversations/{id}/messages` — `server.py:428-433`
- `GET /api/conversations/{id}` — `server.py:435-439`
- `POST /api/conversations` — `server.py:744-757`
- `POST /api/conversations/{id}/messages` — `server.py:764-773`
- `PUT/PATCH/DELETE /api/conversations/{id}` — `server.py:1021-1035`
- `GET /api/v3/conversations` — `server.py:3664-3671`
- `GET /api/v3/conversations/{id}` — `server.py:3673-3677`
- `POST /api/v3/conversations/messages` — `server.py:3705-3708`

**Routes réellement actives (HealthHandler) :** Aucune route conversation.

### TELEGRAM_WEBHOOK_ROUTES

**Route définie dans `server.py:213-214` mais JAMAIS démarrée :**

- `POST /api/notifications/telegram/webhook` → `_handle_telegram_webhook()` (lignes 2566-2590)
  - Validation : `X-Telegram-Bot-Api-Secret-Token` via `validate_telegram_webhook_authorization` (fichier `code/lawim_v2/communication/telegram_webhook.py:102`)

**Route réellement active (HealthHandler) :** Retourne page statique HTML pour TOUTES les requêtes.

### WHATSAPP_WEBHOOK_ROUTES

**Route définie dans `server.py:210-211` mais JAMAIS démarrée :**

- `POST /api/notifications/whatsapp/webhook` → `_handle_green_api_webhook()` (lignes 2542-2564)
  - Validation : `Authorization` header via `validate_webhook_authorization` (fichier `code/lawim_v2/communication/green_api.py:84`)

**Route réellement active (HealthHandler) :** Retourne page statique HTML pour TOUTES les requêtes.

### PROGRAM_F_ADAPTER_PRODUCTION_INSTANTIATIONS

**Fichier :** `code/lawim_v2/services.py:219-223`

```python
_conv_engine_pf = ProgramFEngineAdapter(
    db_path=_conv_pf_db_path,
    property_search_service=_conv_biz_service,
)
```

- **Condition :** Exécuté pendant `build_runtime()` → `LawimServices.__init__()`
- **Appelé depuis :** `entrypoint.sh:43` → `build_runtime(config)` → `LawimServices.__init__()`
- **Statut :** L'instanciation EST exécutée, mais `ProgramFEngineAdapter.__init__` (ligne 84-86 de `program_f_adapter.py`) lève `ImportError` car `lawim_runtime` n'existe PAS dans le conteneur
- **Réel :** `_conv_engine_pf = None` (exception catchée ligne 224-226)
- **Log attendu :** `"Program F engine unavailable — fallback disabled"`
- **Fichier dans conteneur :** `/app/code/lawim_v2/conversation/program_f_adapter.py`
- **lawim_runtime dans conteneur :** **ABSENT** (`/app/lawim_runtime/` n'existe pas)

### JOURNEY_ORCHESTRATOR_PRODUCTION_INSTANTIATIONS

**Fichier :** `code/lawim_v2/conversation/program_f_adapter.py:87-89`

```python
self._orchestrator = ConversationJourneyOrchestrator(
    property_search_service=property_search_service,
)
```

- **Condition :** Exécuté dans `ProgramFEngineAdapter.__init__()`
- **Statut :** JAMAIS instancié car `ProgramFEngineAdapter.__init__()` lève `ImportError` avant (ligne 86)
- **Cause :** `try: from lawim_runtime.conversation.journey import ConversationJourneyOrchestrator` (lignes 14-23) échoue car `lawim_runtime` n'existe pas
- **Fichier dans conteneur :** Vérifié — `lawim_runtime/` ABSENT

### PRODUCTION_ROUTING_MODE

- **Aucun mode de routage implémenté dans le code.**
- **Recherche effectuée :** `V2_ONLY`, `V3_SHADOW`, `V3_CANARY`, `V3_PRIMARY`, `V3_ONLY`, `routing_mode`, `ROUTING_MODE` — 0 résultats
- **LROS_* flags dans compose :** Définis dans `docker-compose.prod.yml:24-32` mais JAMAIS lus par le code Python (recherche `LROS_` dans `code/` = 0 résultats)
- **LAWIM_FEATURE_CONVERSATION_V2 :** Non défini dans l'environnement → `_v3_feature_enabled()` (`server.py:3659-3661`) retourne `False`
- **Mode effectif :** Aucun — le serveur ne peut pas router ce qui n'est pas démarré

### WEB_STATIC_PATH

- **Défini dans `server.py:44-52` :** `_resolve_dist_root()` cherche `frontend/dist/` dans les parents du répertoire de `server.py`
- **jamais utilisée :** HealthHandler ne sert pas la SPA frontend
- **nginx.conf :** ProxyPass vers `http://app:3000` — reçoit la page statique du HealthHandler

### TELEGRAM_STATIC_PATH

- **Dans `server.py:2566-2590` :** Handler complet avec signature et validation
- **jamais appelé :** `_handle_telegram_webhook()` défini mais jamais invoqué
- **Fournisseur :** Bot Telegram `@lawim_bot` — webhook non configuré

### WHATSAPP_STATIC_PATH

- **Dans `server.py:2542-2564` :** Handler complet avec validation Authorization
- **jamais appelé :** `_handle_green_api_webhook()` défini mais jamais invoqué
- **Fournisseur :** Green API — webhook non configuré

### ROOT_CAUSE

**Le conteneur de production (`lawim-app`) démarre le mauvais serveur HTTP.**

`scripts/entrypoint.sh:51-71` définit et démarre une classe `HealthHandler`
minimale qui ne répond qu'aux endpoints `/health` et `/ready`.

Le fichier `code/lawim_v2/server.py` (4104 lignes) contient le vrai serveur
HTTP (`LawimRequestHandler`) avec toutes les routes API, webhooks Telegram,
webhooks WhatsApp, conversations web, API V3, routes CRUD, etc., mais il
n'est **jamais importé ni démarré**.

La solution existe dans le code. Le problème est uniquement dans le point
d'entrée (`entrypoint.sh`).

Par ailleurs, `lawim_runtime` (le package contenant
`ConversationJourneyOrchestrator`) est absent de l'image, ce qui désactive
silencieusement `ProgramFEngineAdapter` (exception catchée dans
`services.py:224-226`). Le moteur conversationnel Program F n'est donc pas
disponible même si le serveur HTTP complet était démarré.

Enfin, `asgi_app.py` tente d'importer `lawim_v2.communication.app` qui
n'existe pas (`communication/__init__.py` exporte uniquement
`CommunicationService`), ce qui planterait s'il était utilisé.

### ROOT_CAUSE_CONFIDENCE

**TRÈS ÉLEVÉE** (toutes les preuves sont directes — code lu, conteneur inspecté,
routes vérifiées, instanciations tracées)

### REPAIR_SCOPE

| Priorité | Réparation | Fichier | Ligne |
|----------|-----------|---------|-------|
| P0 | Remplacer `HealthHandler` par `LawimRequestHandler` dans `entrypoint.sh` | `scripts/entrypoint.sh` | 51-71 |
| P0 | Démarrer via `server.main()` ou `create_server()` | `scripts/entrypoint.sh` | remplacer heredoc |
| P1 | Installer `lawim_runtime` dans l'image Docker | `Dockerfile` | Ajouter COPY |
| P1 | Définir `LAWIM_FEATURE_CONVERSATION_V2=true` | `docker-compose.prod.yml` ou `.env.production` | Ajouter env |
| P2 | Nettoyer `LROS_*` inutilisés ou les connecter au code | `docker-compose.prod.yml:24-32` | Supprimer ou implémenter |
| P2 | Implémenter ou supprimer `asgi_app.py` | `code/lawim_v2/asgi_app.py` | Implémenter ou supprimer |

### REPAIR_REQUIRED

**OUI** — Bloquant pour toute conversation réelle (Web, Telegram, WhatsApp).

Aucun message utilisateur ne peut être traité. Aucun webhook ne peut être reçu.
Aucune réponse ne peut être générée. L'infrastructure est en place (nginx,
PostgreSQL, Redis, Green API authorized, Telegram getMe ok) mais le serveur
HTTP applicatif n'est pas démarré.
