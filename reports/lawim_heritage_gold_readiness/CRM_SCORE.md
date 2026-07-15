# CRM SCORE — Heritage Gold Readiness

**Audité par :** CRM Expert (H0.3)
**Date :** 2026-07-15

## Score global : 52/100

## Sous-dimensions

| # | Dimension | Score | Justification |
|---|-----------|:-----:|---------------|
| 1 | **Roles & permissions** | 30 | Gold cite 6 familles. Source 08-ROLE-REFERENCE.md (2760 lignes) en définit 4 vraisemblablement. Massivement sous-documenté. |
| 2 | **Partners/actors management** | 35 | Gold mentionne agents/diaspora. Source définit 5 types de partenaires (notaire, géomètre, banquier, expert, prestataire). Aucune section gestion partenaires. |
| 3 | **Workflows & state machines** | 60 | 7 états utilisateur + 13 événements. Source USER_STATES.json : 7 états sans transitions. EVENT_TYPES.json : 11 événements. 05-WORKFLOW-REFERENCE.md (4749 lignes) capturé superficiellement. |
| 4 | **Permissions & access control** | 40 | Gold référence des tables. Source détaille 5 catégories de permissions (auto, validée, temporaire, suspendue, révoquée manuellement). |
| 5 | **Transaction management** | 55 | 13 services avec prix exacts. Tous les paiements sont désactivés (payments:OFF, boost:OFF). Bon catalogue, pas d'implémentation. |
| 6 | **Identity resolution** | 70 | Normalisation téléphone OK. Gold utilise +237, source utilise 237. 3 méthodes source vs 5 Gold (manque WhatsApp ID et name+city). Seuil merge ≥40 OK. |
| 7 | **Anti-spam & security** | 45 | Rate-limit 10/min OK, block 60min OK. Gold ajoute pénalité -50 + récidive (>3 blocks = permanent) — PAS dans la source. Anti-fraude (broker_spam, duplicate_listing, fake_price, suspicious_urgency) — PAS implémenté. |
| 8 | **Data quality management** | 95 | Scores de fiabilité source (agent=90, google_form=85, etc.), formule complétude×0.6 + fiabilité×0.4, notes A+≥80 à D<20 — quasi-parfait. |
| 9 | **Lead tracking & routing** | 30 | Gold : pipeline 8 étapes, 5 types leads, boosters, priorités P0-P3. Source lawim_engine_v1.py : pipeline 3 étapes basique (détecter→scorer→répondre). Pas de routage, pas de classification, pas de boosters. Gold est purement aspirationnel. |
| 10 | **Agent network management** | 60 | Opt-in (5 étapes) OK. Rating 1-5 OK. Tables agent_zones, agent_credits référencées mais non vérifiées. |

## Forces

- Data quality : quasi-parfait (95/100)
- Identity resolution : bon (70/100)
- Agent network : correct (60/100)
- 13 services avec prix exacts

## Faiblesses critiques

- Roles/permissions (30/100) : massivement sous-documenté
- Lead routing (30/100) : pipeline 8 étapes aspirationnel vs 3 étapes réel
- Partners (35/100) : 5 types de partenaires non documentés
- Permissions (40/100) : 5 catégories non détaillées
- Anti-fraude (45/100) : 4 couches annoncées, 0 implémentées

## Conclusion

Le CRM est un domaine inégal : excellent sur la qualité des données et l'identité, mais très faible sur les rôles, le routage et les permissions. Le pipeline 8 étapes est le problème le plus critique — il décrit un système qui n'existe pas dans le code. LAWIM_V2 ne peut pas reconstruire le CRM sans retour aux sources.
