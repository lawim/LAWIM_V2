# RELEASE PROGRAM F — Workflow Automation Platform

**Programme :** RELEASE PROGRAM F  
**Date :** 2026-07-01  
**Branche :** `develop/2.0-intelligent-platform`  
**Tag :** `release-program-f`  
**Schema :** v12  
**Prérequis :** Programs A–E

---

## 1. Résumé exécutif

RELEASE PROGRAM F ajoute le **moteur d'automatisation des processus métier** à LAWIM_V2 : définition de workflows, exécution, machine à états, règles, tâches, files d'attente, planification, relances, escalades, SLA, validations multi-niveaux, notifications, audit et monitoring — intégré aux programmes A–E (IA, connaissances, écosystème).

**625+ tests** passent (objectif 600+).

---

## 2. Architecture

Package : `code/lawim_v2/workflow_automation/`

```
Process Engine (orchestration)
├── State Machine + Transition Engine
├── Rules Engine (expressions déterministes)
├── Task Engine + Queue Manager
├── Scheduler + Timer + Retry + Timeout
├── Escalation + Approval + Notification
├── Audit + Metrics Engine
└── AI Integration Bridge → Programs C/D/E
```

Préfixe tables : `automation_*` (sans collision avec ecosystem `workflows` / `workflow_*`).

---

## 3. Schema v12

22 tables (`schema_v12_ddl.py`) :

- Définitions : `automation_workflow_definitions`, `automation_templates`, `automation_states`, `automation_transitions`
- Exécution : `automation_process_instances`, `automation_executions`, `automation_tasks`
- Orchestration : `automation_queues`, `automation_queue_items`, `automation_events`, `automation_schedules`, `automation_timers`
- Fiabilité : `automation_retries`, `automation_escalations`, `automation_sla_policies`
- Gouvernance : `automation_approvals`, `automation_rules`, `automation_rule_bindings`
- Traçabilité : `automation_notifications`, `automation_audit_log`, `automation_history`, `automation_metrics_snapshots`

---

## 4. Domaines métier

| Domaine | Processus |
|---------|-----------|
| Immobilier | achat, vente, location, visite, vérification, publication, signature |
| Juridique | contrats, conformité, validation documentaire, contentieux, archivage |
| Financement | demande, étude, scoring, validation, décaissement |
| Administration | comptes, modération, support, incidents, réclamations |
| IA | analyse, recommandations, décisions assistées, enrichissement, assistant |

6 workflows seedés + files d'attente par domaine.

---

## 5. API v2 workflows (automation)

| Endpoint | Description |
|----------|-------------|
| `GET /api/v2/workflows` | **Program B** — templates écosystème (inchangé) |
| `GET/POST /api/v2/workflows/definitions` | Définitions automation |
| `POST /api/v2/workflows/definitions/{key}/activate\|deactivate\|duplicate` | Cycle de vie |
| `GET/POST /api/v2/workflows/templates` | Modèles |
| `GET /api/v2/workflows/executions` | Exécutions |
| `GET/POST /api/v2/workflows/instances` | Instances + démarrage |
| `POST /api/v2/workflows/instances/{id}/advance` | Avancement state machine |
| `GET /api/v2/workflows/tasks` + `POST .../complete` | Tâches |
| `GET /api/v2/workflows/queues` + enqueue/dequeue | Files |
| `GET/POST /api/v2/workflows/events` | Événements |
| `GET/POST /api/v2/workflows/approvals` + decide | Validations |
| `GET/POST /api/v2/workflows/rules` + evaluate | Règles |
| `GET /api/v2/workflows/schedules`, `/timers`, `/notifications` | Planification |
| `GET /api/v2/workflows/history`, `/audit`, `/metrics`, `/monitoring` | Observabilité |
| `POST /api/v2/workflows/ai-hook` | Intégration IA A–E |

---

## 6. Admin UI

Panel **Workflow automation** dans `static/index.html` / `static/app.js` :

- Statistiques workflows/instances/tâches
- Liste des définitions actives
- Monitoring SLA / approbations / escalades

---

## 7. Observabilité

Compteurs : `workflow_*`, `process_*`, `task_*`, `queue_*`, `event_*`, `automation_*`, `approval_*`, `notification_*` + latence `process_execution_latency_ms`.

---

## 8. Compatibilité Programs A–E

- `GET /api/v2/workflows` → ecosystem (Program B)
- `GET /api/v2/projects/{id}/workflows` → inchangé
- Routes knowledge, assistant, cognition intactes
- Tables v7–v11 préservées

---

## 9. Validations

```bash
./scripts/validate-install.sh
./scripts/validate-packaging.sh
./scripts/run-tests.sh
python3 scripts/validate_prisma_manifest.py
python3 scripts/smoke_runtime.py
./platform/validate-platform.sh
./platform/run-postgres-tests.sh
git diff --check
```
