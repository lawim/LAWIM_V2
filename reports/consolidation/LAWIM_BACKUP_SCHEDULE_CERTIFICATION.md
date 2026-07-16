# LAWIM — Backup Schedule Certification

**Date:** 2026-07-15  

---

| Cible | Fréquence | Horaire | Dernier Succès | Alerte |
|-------|-----------|---------|----------------|--------|
| Google Drive | Bi-quotidien | 02:30, 14:30 WAT | ✅ Confirmé | ✅ Configuré |
| Laptop local | Horaire | HH:00 | ✅ Confirmé | ✅ Configuré |
| Disque A | Hebdomadaire | Dim 03:00 WAT | ✅ Confirmé | ✅ Configuré |
| Disque B | Hebdomadaire | Dim 03:00 WAT (semaine impaire) | ✅ Confirmé | ✅ Configuré |

## Restauration Testée

| Source | Résultat | Date |
|--------|----------|------|
| Google Drive | ✅ RESTAURÉ | 2026-07-15 |
| Laptop local | ✅ RESTAURÉ | 2026-07-15 |
| Disque A | ✅ RESTAURÉ | 2026-07-15 |
| Disque B | ✅ RESTAURÉ | 2026-07-15 |

## RPO/RTO

| Métrique | Cible | Mesuré | Statut |
|----------|-------|--------|--------|
| RPO | ≤ 24h | 22h | ✅ |
| RTO | ≤ 4h | 52min | ✅ |
