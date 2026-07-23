# Backup/Restore Evidence Report

**Programme:** G.6
**Status:** NOT VALIDATED
**Date:** 2026-07-23

---

## Prérequis non satisfaits

Ce test nécessite :

- PostgreSQL accessible avec données réelles
- Répertoire de backup accessible en écriture

## Procédure

```bash
# Backup
bash deployment/scripts/backup.sh
# Backup créé dans deployment/backup/lawim-backup-YYYYMMDD-HHMMSS/

# Restore (simulation de perte)
docker stop lawim-db
docker rm lawim-db
docker compose up -d db
# Base est vide — restaurer
bash deployment/scripts/restore.sh deployment/backup/lawim-backup-YYYYMMDD-HHMMSS/

# Vérification
docker exec lawim-db psql -U lawim lawim_v3 -c "SELECT COUNT(*) FROM sessions;"
docker exec lawim-db psql -U lawim lawim_v3 -c "SELECT COUNT(*) FROM profiles;"
```

## Vérifications

| Vérification | Statut | Preuve |
|-------------|--------|--------|
| Backup base | NON VALIDÉ | Requiert PostgreSQL |
| Backup config | NON VALIDÉ | Requiert déploiement |
| Checksums SHA256 | NON VALIDÉ | Requiert exécution |
| Restauration | NON VALIDÉ | Requiert test réel |
| Comparaison avant/après | NON VALIDÉ | Requiert données réelles |

## Conclusion

**Backup/Restore : NON VALIDÉ L6.** Les scripts sont implémentés et testés L4. La validation réelle nécessite une base PostgreSQL contenant des données et un test de restauration complet.
