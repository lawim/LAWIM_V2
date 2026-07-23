# LAWIM Pre-Deployment Checklist

**Date:** 2026-07-23
**Status:** CHECKLIST — éléments requis non satisfaits

---

## 1. Git

- [x] Branche propre : `feature/external-operational-certification-20260723`
- [x] Aucun changement non commité
- [x] HEAD : `d2cc96ad`
- [ ] Tag de release créé

## 2. Infrastructure

- [ ] Serveur cible accessible (IP / hostname : \_\_\_\_\_\_\_\_\_\_)
- [ ] Docker et Docker Compose installés
- [ ] PostgreSQL 16 accessible
- [ ] Redis 7 accessible
- [ ] Nom de domaine configuré (\_\_\_\_\_\_\_\_\_\_)
- [ ] Certificat TLS émis (Let's Encrypt / autre : \_\_\_\_\_\_\_\_\_\_)
- [ ] Ports 80, 443, 3000 ouverts

## 3. Secrets requis

| Secret | Configuré | Source |
|--------|-----------|--------|
| `OPENAI_API_KEY` | NON | OpenAI dashboard |
| `ANTHROPIC_API_KEY` | NON | Anthropic console |
| `DEEPSEEK_API_KEY` | NON | DeepSeek platform |
| `GEMINI_API_KEY` | NON | Google AI Studio |
| `GREEN_API_INSTANCE` | NON | Green API settings |
| `GREEN_API_TOKEN` | NON | Green API settings |
| `TELEGRAM_BOT_TOKEN` | NON | BotFather |
| `CAMPAY_API_USERNAME` | NON | Campay dashboard |
| `CAMPAY_API_PASSWORD` | NON | Campay dashboard |
| `CAMPAY_WEBHOOK_SECRET` | NON | Campay dashboard |
| `LAWIM_API_TOKEN` | NON | Généré localement |
| `LAWIM_VAULT_KEY` | NON | Généré localement |
| `POSTGRES_PASSWORD` | NON | Généré localement |
| `GRAFANA_PASSWORD` | NON | Généré localement |

**Aucun secret requis n'est actuellement configuré.**

## 4. Feature flags (production)

| Flag | Valeur | Requis pour |
|------|--------|-------------|
| `interaction_gateway_enabled` | `true` | Activer le pipeline V3 |
| `whatsapp_adapter_enabled` | `true` | WhatsApp L6 |
| `telegram_adapter_enabled` | `true` | Telegram L6 |
| `ai_intelligence_enabled` | `true` | IA |
| `ai_extraction_enabled` | `true` | Extraction IA |
| `ai_response_writer_enabled` | `true` | Writer IA |
| `ai_provider_calls_enabled` | `true` | Appels LLM réels |
| `ai_shadow_mode` | `false` | Mode primaire |

**Tous les flags sont actuellement à `false` par défaut.**

## 5. Migrations

- [ ] Moteur de migration validé : `lawim_runtime/production/migrate.py`
- [ ] 4 migrations à appliquer (sessions, profiles, deliveries, events)
- [x] Rollback validé par test automatisé

## 6. Observabilité

- [ ] Prometheus endpoint accessible
- [ ] Grafana dashboards provisionnés
- [ ] Alertes configurées (5 règles)
- [ ] Logs structurés activés

## 7. Backups

- [ ] Script backup : `deployment/scripts/backup.sh`
- [ ] Script restore : `deployment/scripts/restore.sh`
- [ ] Rotation configurée

## 8. Tests

- [x] 721 tests LROS PASS
- [x] 24 V2 baseline PASS (3 preexisting)
- [ ] Tests WhatsApp L6 : NON EXÉCUTÉS
- [ ] Tests Telegram L6 : NON EXÉCUTÉS
- [ ] Tests Campay L6 : NON EXÉCUTÉS
- [ ] Tests LLM réels : NON EXÉCUTÉS
- [ ] Tests charge : NON EXÉCUTÉS
- [ ] Tests reprise incident : NON EXÉCUTÉS
- [ ] Tests backup/restore : NON EXÉCUTÉS

## Conclusion

**Blocage : 13 secrets requis non configurés. Aucun test L6 exécuté.**
