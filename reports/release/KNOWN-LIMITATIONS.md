# LAWIM V3 — Known Limitations (Release 1.0)

**Date:** 2026-07-23

---

## Limitations bloquantes

| # | Limitation | Impact | Programme | Résolution |
|---|-----------|--------|-----------|------------|
| L1 | WhatsApp L6 non validé | Aucun utilisateur WhatsApp réel | G.6 | Credentials Green API + test réel |
| L2 | Telegram L6 non validé | Aucun utilisateur Telegram réel | G.6 | Token Bot + test réel |
| L3 | Campay L6 non validé | Aucun paiement réel | G.6 | Credentials sandbox + test réel |
| L4 | Aucun provider LLM configuré | Mode déterministe uniquement | G.6 | Clés API + budget |
| L5 | Aucun déploiement réel | Utilisation locale uniquement | G.6 | Infrastructure cible |
| L6 | CI/CD non configuré | Déploiement manuel | G | Pipeline à construire |

## Limitations fonctionnelles

| # | Limitation | Impact | Contournement |
|---|-----------|--------|---------------|
| F1 | RAG avec embeddings hash-based | Recherche sémantique limitée | Mode déterministe |
| F2 | Persistance InMemory (sessions, profils) | Données volatiles en l'absence de PostgreSQL | Configurer PostgreSQL |
| F3 | Pas d'analyse d'images | Les photos ne sont pas interprétées | Programme F (future) |
| F4 | Pas de streaming LLM | Réponse générée en bloc | Mode déterministe |
| F5 | ConversationStateEngine (V2) non testé | 873 lignes sans couverture de test | Migration vers V3 |
| F6 | Pas d'anthropic provider dans la chaîne V2 | Provider manquant dans le fallback V2 | Ajout futur |

## Limitations de performance

| # | Limitation | Seuil |
|---|-----------|-------|
| P1 | Tests de charge non exécutés | Aucune donnée de performance |
| P2 | Pas de caching Redis configuré pour les sessions | Dépend de PostgreSQL |
| P3 | Pas de CDN pour les médias | Tous les médias servis par l'application |

## Limitations de sécurité

| # | Limitation | Risque |
|---|-----------|--------|
| S1 | TLS non configuré | Communications en clair |
| S2 | Rate limiting implémenté mais non testé en charge | DDoS potentiel |
| S3 | Pas d'audit de sécurité externe | Vulnérabilités non identifiées |

## Limitations documentaires

| # | Limitation |
|---|-----------|
| D1 | Aucun tests WhatsApp/Telegram/Campay/LLM réels exécutés |
| D2 | Aucune preuve de déploiement sur infrastructure cible |
| D3 | Aucune procédure de mise à jour versionnée testée |
