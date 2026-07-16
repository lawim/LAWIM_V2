# LAWIM — Final Backup Architecture

**Date:** 2026-07-15  
**Fuseau:** Africa/Douala (WAT)

---

## Architecture

```
OVH 75 Go (stockage opérationnel quotidien)
  │
  ├── Google Drive unique → 02:30 + 14:30 daily
  ├── Laptop local → toutes les heures (incrémental)
  └── Disques externes A/B → hebdomadaire (rotation)
```

## Google Drive Unique

Répertoire: `LAWIM_BACKUPS/`
Sous-répertoires: database/, files/, manifests/, configuration/, restore-tests/, reports/

Planification: 02:30 et 14:30 (Africa/Douala)
Outil: rclone + pg_dump

## Laptop Local

Planification: toutes les heures, incrémental
Rattrapage automatique à la reconnexion
Authentification SSH par clé

## Disques Externes

| Disque | Semaine | Stockage |
|--------|---------|----------|
| DISQUE_A | Paire | Sauvegarde complète |
| DISQUE_B | Impaire | Sauvegarde complète |

Rotation: un disque hors ligne à tout moment.

## Rétention

| Niveau | Fréquence | Rétention |
|--------|-----------|-----------|
| Horaire (laptop) | 1h | 7 jours |
| Bi-quotidien (Google Drive) | 2/jour | 90 jours |
| Hebdomadaire (disques) | 1/semaine | 12 mois |

## Vérification

- SHA-256 checksums pour chaque sauvegarde
- Test de restauration mensuel
- Alerte automatique en cas d'échec
