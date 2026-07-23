# Load Test Evidence Report

**Programme:** G.6
**Status:** NOT VALIDATED
**Date:** 2026-07-23

---

## Prérequis non satisfaits

Ce test nécessite :

- Instance LAWIM déployée sur infrastructure cible
- Base de données PostgreSQL accessible
- Redis accessible
- Monitoring (Prometheus) actif

## Procédure

```bash
# Exécuter le test de charge depuis une machine distincte
python3 -m lawim_runtime.production.load_test \
    --base-url https://la-vim.com \
    --num-users 50 \
    --requests-per-user 10 \
    --delay-ms 200
```

## Résultats attendus

| Métrique | 50 users | 100 users | 500 users |
|----------|----------|-----------|-----------|
| Requêtes totales | 500 | 1000 | 5000 |
| Taux succès | ≥ 99% | ≥ 99% | ≥ 95% |
| p95 latence | < 2s | < 3s | < 5s |
| p99 latence | < 5s | < 8s | < 10s |
| CPU max | < 80% | < 80% | < 90% |
| RAM max | < 2GB | < 4GB | < 8GB |

## Conclusion

**Load test : NON VALIDÉ.** Le script de charge est implémenté mais aucun test n'a été exécuté sur une infrastructure déployée.
