# Traceabilité

| Assertion | Preuve | Fichier | Ligne |
|-----------|--------|---------|-------|
| ENTRYPOINT | Docker inspect | evidence/raw/container/inspect.txt | — |
| CMD=null | Docker inspect | evidence/raw/container/inspect.txt | — |
| HealthHandler utilisé | entrypoint.sh | scripts/entrypoint.sh | 51-71 |
| LawimRequestHandler non démarré | entrypoint.sh | scripts/entrypoint.sh | 11-72 |
| Routes web définies | server.py | code/lawim_v2/server.py | 210-214, 401-439, 744-773 |
| Routes web inactives | entrypoint.sh ne démarre pas server | scripts/entrypoint.sh | 51-71 |
| Telegram webhook défini | server.py | code/lawim_v2/server.py | 213-214, 2566-2590 |
| WhatsApp webhook défini | server.py | code/lawim_v2/server.py | 210-211, 2542-2564 |
| PF adapter importé | services.py | code/lawim_v2/services.py | 198-226 |
| PF adapter = None | services.py (exception catchee) | code/lawim_v2/services.py | 224-226 |
| lawim_runtime absent | container inspect | evidence/raw/container/inspect.txt | — |
| JourneyOrchestrator jamais cree | program_f_adapter.py | code/lawim_v2/conversation/program_f_adapter.py | 84-87 |
| V3 feature disabled | var env LAWIM_FEATURE_CONVERSATION_V2 | evidence/raw/container/inspect.txt | — |
| LROS jamais lus | grep LROS code/ | evidence/normalized/audit-results.json | — |
| asgi_app.py non fonctionnel | import manquant | code/lawim_v2/asgi_app.py | 1-3 |
