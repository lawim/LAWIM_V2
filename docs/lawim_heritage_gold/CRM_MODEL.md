# CRM MODEL — Gold — Modèle CRM LAWIM

**Mission :** H0 — LAWIM Heritage Gold
**Date :** 15 juillet 2026
**Principe :** Documentation exhaustive et validée du système CRM LAWIM

---

## 1. Pipeline CRM (8 stages)

**Source :** LAWIMA `08_CONFIG/rule_engine/RULE_ENGINE_V5.json`, `03_ENGINE/lawim_engine_v1.py`

| Stage | Entrée | Traitement | Sortie |
|-------|--------|------------|--------|
| 1. **incoming_message** | Message brut WhatsApp/TG | Réception et formatage | Message normalisé |
| 2. **normalize_text** | Message normalisé | Normalisation orthographique, typo, argot | Texte nettoyé |
| 3. **extract_entities** | Texte nettoyé | Extraction entités (budget, ville, type bien, téléphone) | Entités structurées |
| 4. **detect_intent** | Entités + texte | Classification d'intention (buy/rent/sell/invest) | Intention + confiance |
| 5. **context_enrichment** | Intention + entités | Enrichissement contexte (historique, profil, comportement) | Contexte complet |
| 6. **lead_scoring** | Contexte complet | Calcul du score (base + boosters - pénalités) | Score numérique |
| 7. **lead_classification** | Score numérique | Classification HOT/WARM/COLD/LOW/SPAM | Classe + priorité |
| 8. **crm_routing** | Classe + priorité | Routage vers agent, dashboard, ou réponse auto | Action CRM |

---

## 2. Lead Types with Base Scores

**Source :** LAWIMA `06_AI_MODELS/lead_classifier/lead_classifier_v1.json`

| Type de lead | Base Score | Description |
|-------------|-----------|-------------|
| **tenant** | 40 | Locataire potentiel — recherche location |
| **buyer** | 60 | Acheteur potentiel — recherche achat |
| **seller** | 50 | Vendeur — met en vente un bien |
| **investor** | 80 | Investisseur — recherche rendement |
| **diaspora_investor** | 95 | Investisseur diaspora — pouvoir d'achat élevé + besoin sécurité |

---

## 3. Score Boosters and Penalties

**Source :** LAWIMA `06_AI_MODELS/lead_classifier/lead_classifier_v1.json`, `03_ENGINE/lead_scorer/lead_scorer.py`

### 3.1 Boosters

| Signal | Bonus | Condition |
|--------|-------|-----------|
| Budget détecté | +15 | Montant explicite ou fourchette |
| Ville détectée | +10 | Ville nommée dans le message |
| Quartier détecté | +10 | Quartier spécifique mentionné |
| Urgence exprimée | +20 | Mots-clés : urgent, vite, asap, immédiatement |
| Diaspora détectée | +25 | Indicatif étranger, localisation hors Cameroun |
| Achat comptant | +15 | Paiement cash, pas de crédit nécessaire |
| Message > 20 caractères | +30 | Message détaillé = engagement sérieux |
| Budget présent | +25 | Budget explicite ou implicite |
| Localisation présente | +25 | Ville ou quartier mentionné |
| Type de bien présent | +20 | Maison, terrain, appartement, villa, etc. |
| Visite demandée | +20 | "Je peux visiter", "visite possible?" |
| Document demandé | +15 | "Y'a le papier?", "titre foncier?" |
| Référence externe | +10 | Recommandation, bouche-à-oreille |

### 3.2 Penalties

| Signal | Malus | Condition |
|--------|-------|-----------|
| Budget manquant | -10 | Aucune mention de budget |
| Localisation floue | -10 | "Quelque part", "au Cameroun", "en ville" |
| Message suspect (spam) | -50 | Pattern de spam détecté |
| Message trop court | -20 | Moins de 10 caractères |
| Liens externes | -30 | URL suspectes, promotion externe |
| Comportement répétitif | -25 | Même message envoyé plusieurs fois |
| Coordonnées incomplètes | -15 | Pas de téléphone valide |
| Intention non détectée | -20 | Impossible de classifier l'intention |

---

## 4. Classification Thresholds

**Source :** LAWIMA `06_AI_MODELS/lead_classifier/lead_classifier_v1.json`, `08_CONFIG/rule_engine/RULE_ENGINE_V5.json`

### 4.1 Thresholds V1 (Numeric)

| Classe | Seuil | Label |
|--------|-------|-------|
| **HOT** | ≥ 80 | Prêt à acheter/visiter — action immédiate |
| **WARM** | ≥ 60 | Intérêt confirmé — envoyer des annonces |
| **COLD** | ≥ 40 | Intérêt faible — demander plus d'infos |
| **LOW** | < 40 | Faible priorité — relance longue |
| **SPAM** | < 40 + patterns | Message indésirable — ignorer/bloquer |

### 4.2 Thresholds V5 (Normalized 0–1)

| Classe | Seuil | Label |
|--------|-------|-------|
| **HOT** | ≥ 0.8 | Action immédiate requise |
| **WARM** | ≥ 0.5 | Envoyer propositions |
| **COLD** | ≥ 0.3 | Qualification complémentaire |
| **LOW** | < 0.3 | Relance passive |
| **SPAM** | ≥ 0.2 (spam rules) | Blocage temporaire |

### 4.3 Recommended Actions per Class

| Classe | Action prioritaire | Délai | Canal |
|--------|-------------------|-------|-------|
| **HOT** | call_immediately (appel immédiat) | < 1h | Téléphone + WhatsApp |
| **WARM** | send_listings (envoyer annonces) | < 24h | WhatsApp |
| **COLD** | request_budget (demander budget/compléments) | < 48h | WhatsApp |
| **LOW** | follow_up (relance périodique) | J+7 / J+30 / J+90 | WhatsApp |
| **SPAM** | ignore (ignorer + bloquer si récidive) | Immédiat | Aucun |

---

## 5. Lead Priority (P0 / P1 / P3)

**Source :** LAWIMA `03_ENGINE/lead_scorer/lead_scorer.py`, `08_CONFIG/rule_engine/RULE_ENGINE_V5.json`

| Priorité | Types | Action | SLA |
|----------|-------|--------|-----|
| **P0** | diaspora_investor, buyer > 50M FCFA | Réponse immédiate, appel prioritaire | < 30 min |
| **P1** | seller, land_buyer (acheteur terrain) | Réponse rapide, qualification approfondie | < 2h |
| **P2** | buyer standard, investor standard | Suivi normal, envoi annonces | < 24h |
| **P3** | tenant, prospect non qualifié | Relance automatisée, qualification lente | J+1 à J+7 |

---

## 6. Behavior Tracking

**Source :** LAWIMA `08_CONFIG/rule_engine/RULE_ENGINE_V5.json`

| Comportement traqué | Données collectées | Usage |
|---------------------|-------------------|-------|
| **message_history** | Messages précédents, intentions, entités | Enrichissement contexte, scoring historique |
| **response_time** | Temps de réponse moyen du prospect | Engagement, suivi adapté |
| **budget_changes** | Évolution du budget dans le temps | Négociation, scoring dynamique |
| **visit_requests** | Demandes de visite, réalisées ou non | Engagement, closing |
| **property_views** | Annonces consultées, temps de consultation | Affinité, matching |
| **document_requests** | Demandes de documents spécifiques | Sérieux de l'intention |
| **call_attempts** | Tentatives d'appel, résultats | Suivi commercial |
| **referral_source** | Source d'acquisition (ami, pub, recherche) | ROI acquisition |

---

## 7. Anti-Fraud Layers

**Source :** LAWIM `KNOWLEDGE/fraud-signals-and-verification.md`, LAWIMA `08_CONFIG/rule_engine/RULE_ENGINE_V5.json`

### 7.1 Detection Layers

| Couche | Détection | Action |
|--------|-----------|--------|
| **broker_spam** | Messages promotionnels répétés, sollicitation multiple | Blocage 60 min, flag broker |
| **duplicate_listing** | Même bien publié par plusieurs comptes | Fusion, avertissement |
| **fake_price** | Prix anormalement bas ou haut vs marché | Flag, vérification manuelle |
| **suspicious_urgency** | Pression artificielle pour paiement rapide | Alerte, vérification renforcée |

### 7.2 Fraud Signal Weights

| Signal | Poids | Seuil d'alerte |
|--------|-------|----------------|
| Prix < 50% du marché | 0.9 | Alerte immédiate |
| Pas de téléphone valide | 0.8 | Blocage création |
| Même bien > 3 annonces | 0.7 | Flag duplication |
| Paiement demandé avant visite | 0.9 | Blocage transaction |
| IP suspecte (hors Cameroun + nouveau compte) | 0.6 | Vérification manuelle |

---

## 8. Identity Resolution

**Source :** LAWIMA `03_ENGINE/identity_resolution.py`

### 8.1 Duplicate Detection Criteria

| Critère | Score de correspondance | Algorithme |
|---------|----------------------|------------|
| Téléphone identique | 100 | Correspondance exacte après normalisation (+237) |
| Email identique | 95 | Correspondance exacte insensible à la casse |
| Prénom + nom similaire + téléphone similaire | ≥ 40 | Fuzzy matching (Levenshtein) |
| WhatsApp ID identique | 100 | Correspondance exacte |
| Nom similaire + ville identique | ≥ 60 | Fuzzy matching + exact location |

### 8.2 Phone Normalization

| Format entrée | Format normalisé | Exemple |
|--------------|-----------------|---------|
| 6XXXXXXXX | +237 6XXXXXXXX | +237 691234567 |
| 00237 6XXXXXXXX | +237 6XXXXXXXX | +237 691234567 |
| +237 6XXXXXXXX | +237 6XXXXXXXX | +237 691234567 |
| 691234567 | +237 691234567 | +237 691234567 |

### 8.3 Merge Algorithm

| Step | Description |
|------|-------------|
| 1. **Détection** | Parcourir les candidats au merge |
| 2. **Calcul score** | Appliquer critères avec poids |
| 3. **Seuil** | Confirmation si score ≥ 40 |
| 4. **Statut** | `pending` en attente de validation humaine |
| 5. **Table** | `duplicate_candidates` stockage des candidatures |

---

## 9. Data Quality Engine

**Source :** LAWIMA `03_ENGINE/data_quality_engine.py`

### 9.1 Source Reliability Scores

| Source | Fiabilité | Justification |
|--------|-----------|---------------|
| **agent** | 90 | Données saisies par agent formé |
| **google_form** | 85 | Formulaire structuré |
| **import** | 70 | Import batch de données existantes |
| **whatsapp** | 50 | Message non structuré, extractible |
| **unknown** | 30 | Source non identifiée |

### 9.2 Quality Score Formula

```
Quality Score = (Completeness × 0.6) + (Reliability × 0.4)
```

| Composante | Poids | Calcul |
|-----------|-------|--------|
| **Completeness** | 60% | Champs remplis / Total champs requis × 100 |
| **Reliability** | 40% | Score de fiabilité de la source (0–100) |

### 9.3 Quality Grading

| Grade | Score | Label | Action |
|-------|-------|-------|--------|
| **A+** | ≥ 80 | Excellent | Utilisable directement, confiance élevée |
| **A** | ≥ 60 | Bon | Utilisable après vérification mineure |
| **B** | ≥ 40 | Moyen | Nécessite complétion |
| **C** | ≥ 20 | Faible | Enrichissement nécessaire |
| **D** | < 20 | À vérifier | Source douteuse, re-qualification requise |

---

## 10. Anti-Spam System

**Source :** LAWIMA `03_ENGINE/anti_spam.py`

| Règle | Valeur | Action |
|-------|--------|--------|
| Rate limit | 10 messages/minute | Dépassement → alerte |
| Auto-block duration | 60 minutes | Blocage temporaire après dépassement |
| Scoring penalty | -50 | Pénalité appliquée au score du lead |
| Table de stockage | `blocked_users` | Historique des blocages |
| Récidive | > 3 blocages | Blocage permanent, flag spammer |

---

## 11. Agent Opt-In System

**Source :** LAWIMA `03_ENGINE/agent_optin.py`

| Step | Action | Description |
|------|--------|-------------|
| 1 | **Détection du besoin** | Le système identifie qu'un agent est nécessaire (zone, type de bien) |
| 2 | **Demande de permission** | "Voulez-vous recevoir le contact d'un agent spécialisé dans votre zone ?" |
| 3 | **Log de consentement** | Enregistrement dans `agent_optins` (statut : accepted/declined) |
| 4 | **Partage conditionnel** | Contact partagé UNIQUEMENT si accepté |
| 5 | **Refus** | Si refusé, pas de partage, pas de relance agent |

**Règle d'or :** Aucun contact agent partagé sans consentement explicite de l'utilisateur.

---

## 12. Agent Rating System

**Source :** LAWIMA `03_ENGINE/agent_rating.py`

| Critère | Valeur |
|---------|--------|
| Échelle | 1 à 5 étoiles |
| Calcul | Moyenne de toutes les notes reçues |
| Stockage | `whatsapp_agents` table |
| Affichage | `⭐ X/5` ou `🆕` pour nouvel agent sans note |
| Mise à jour | Après chaque feedback client |

---

## 13. Feedback Handling

**Source :** LAWIM `KNOWLEDGE/commercial/conversation_tone.md`

| Type de feedback | Format | Usage |
|-----------------|--------|-------|
| **Thumbs up/down** | Binaire (👍/👎) | Feedback rapide après interaction |
| **Note numérique** | 1 à 5 | Évaluation de l'agent ou du service |
| **Commentaire libre** | Texte libre | Analyse qualitative |

---

## 14. Monetized Services (13 services with prices)

**Source :** LAWIMA `core/monetisation.py`, `08_CONFIG/features/FEATURE_FLAGS.json`

| # | Service | Code | Prix (FCFA) | Type |
|---|---------|------|-------------|------|
| 1 | Boost annonce 7 jours | boost_7j | 2 000 | Annonce |
| 2 | Boost annonce 30 jours | boost_30j | 5 000 | Annonce |
| 3 | Premium listing (visibilité max) | premium_listing | 10 000 | Annonce |
| 4 | Abonnement Agent Pro (mensuel) | agent_pro | 10 000/mois | Abonnement |
| 5 | Abonnement Agent Business (mensuel) | agent_business | 25 000/mois | Abonnement |
| 6 | Lead Bronze (1 contact) | lead_bronze | 500 | Lead |
| 7 | Lead Silver (5 contacts) | lead_silver | 1 500 | Lead |
| 8 | Lead Gold (15 contacts) | lead_gold | 3 000 | Lead |
| 9 | Déblocage coordonnées propriétaire | deblocage_coordonnees | 500 | Transaction |
| 10 | Demandeur Premium (visibilité prioritaire) | demandeur_premium | 1 000 | Profil |
| 11 | Diaspora Simple (accès biens vérifiés) | diaspora_simple | 25 000 | Diaspora |
| 12 | Diaspora Rapport (accompagnement + rapports) | diaspora_rapport | 50 000 | Diaspora |
| 13 | Diaspora Complet (accompagnement total) | diaspora_complet | 75 000 | Diaspora |

---

## 15. Feature Flags

**Source :** LAWIMA `08_CONFIG/features/FEATURE_FLAGS.json`

### 15.1 Core Features (ON)

| Flag | Statut | Description |
|------|--------|-------------|
| `whatsapp_core` | ON | Fonctionnalités WhatsApp de base |
| `property_ingestion` | ON | Ingestion des propriétés |
| `matching_simple` | ON | Matching de base |
| `lead_generation` | ON | Génération de leads |

### 15.2 Advanced Features (OFF)

| Flag | Statut | Description | Activation prévue |
|------|--------|-------------|-------------------|
| `payments` | OFF | Paiements en ligne | Phase 2 |
| `boost` | OFF | Boost d'annonces payant | Phase 2 |
| `subscriptions` | OFF | Abonnements agents | Phase 2 |
| `diaspora` | OFF | Services diaspora premium | Phase 2 |
| `ai_scoring` | OFF | Scoring IA avancé | Phase 3 |
| `escrow` | OFF | Paiement sécurisé séquestre | Phase 3 |
| `multi_canal` | OFF | Telegram, Facebook, Email | Phase 3 |

---

## 16. CamPay Payment Integration (Disabled)

**Source :** LAWIMA `08_CONFIG/features/FEATURE_FLAGS.json`

| Élément | Valeur |
|---------|--------|
| Statut | Désactivé (feature flag `payments: OFF`) |
| Opérateurs | MTN Mobile Money, Orange Money |
| Type | Mobile Money (USSD) |
| Activation | Prévue Phase 2 |
| Utilisation | Boost, abonnements, services diaspora |

---

## 17. System Event Types

**Source :** LAWIMA `08_CONFIG/state_machine/EVENT_TYPES.json`

| Événement | Déclencheur | Action système |
|-----------|-------------|----------------|
| `message.received` | Message entrant WhatsApp/Telegram | Normalisation, routage pipeline |
| `intent.detected` | Intention identifiée (buy/rent/sell/invest) | Scoring, classification |
| `user.created` | Nouvel utilisateur enregistré | Profil par défaut, onboarding |
| `property.created` | Nouveau bien ajouté | Indexation, matching |
| `lead.created` | Lead qualifié généré | Routage agent, notification |
| `match.generated` | Correspondance lead × bien | Notification au lead |
| `payment.success` | Paiement réussi | Activation du service |
| `subscription.renewed` | Abonnement renouvelé | Mise à jour accès |
| `boost.applied` | Boost d'annonce activé | Visibilité augmentée |
| `access.granted` | Permis d'accès accordé | Déblocage fonctionnalité |
| `user.state_changed` | Changement d'état utilisateur | Mise à jour machine d'état |
| `feedback.submitted` | Feedback reçu | Mise à jour rating |
| `fraud.detected` | Fraude suspectée | Blocage, alerte admin |

---

## 18. User States

**Source :** LAWIMA `08_CONFIG/state_machine/USER_STATES.json`

| État | Code | Description | Transition possible vers |
|------|------|-------------|------------------------|
| **NEW_USER** | `new_user` | Nouvel utilisateur, aucune interaction | SEARCHING_PROPERTY, PROPERTY_OWNER, INACTIVE |
| **SEARCHING_PROPERTY** | `searching_property` | En recherche active de bien | LEAD_CREATED, INACTIVE |
| **PROPERTY_OWNER** | `property_owner` | Propriétaire d'un bien (vendeur/bailleur) | LEAD_CREATED, INACTIVE |
| **AGENT** | `agent` | Agent immobilier enregistré | PREMIUM_AGENT, INACTIVE |
| **LEAD_CREATED** | `lead_created` | Lead qualifié (acheteur/locataire/investisseur) | SEARCHING_PROPERTY, INACTIVE |
| **PREMIUM_AGENT** | `premium_agent` | Agent avec abonnement actif | AGENT (si abonnement expire) |
| **INACTIVE** | `inactive` | Utilisateur inactif (> 90 jours sans interaction) | NEW_USER (si reactivé) |

---

## 19. CRM Database Tables (Schema Overview)

**Source :** LAWIMA `05_AUTOMATIONS/scripts/implement_all.sql`, `setup_database.sql`

### 19.1 Core Tables

| Table | Clé primaire | Description |
|-------|-------------|-------------|
| `persons` | person_id | Utilisateurs, prospects, clients |
| `contact_channels` | channel_id | Canaux de contact (WhatsApp, Tel, Email) |
| `agents` | agent_id | Agents immobiliers |
| `properties` | property_id | Biens immobiliers |
| `leads` | lead_id | Opportunités commerciales |
| `data_sources` | source_id | Sources d'import |
| `events` | event_id | Journal d'événements |

### 19.2 Management Tables

| Table | Description |
|-------|-------------|
| `agent_routing_history` | Historique de routage des leads vers agents |
| `agent_zones` | Zones d'activité des agents |
| `agent_credits` | Crédits et soldes des agents |
| `agent_optins` | Consentements de partage de contact |
| `boost_purchases` | Achats de boost d'annonce |
| `diaspora_services` | Abonnements services diaspora |
| `subscriptions` | Abonnements agents (pro/business) |
| `role_permissions` | Permissions par rôle |
| `user_permissions` | Permissions spécifiques par utilisateur |
| `pending_permission_changes` | Changements de permissions en attente |

### 19.3 Fraud & Compliance Tables

| Table | Description |
|-------|-------------|
| `blocked_users` | Utilisateurs bloqués (anti-spam) |
| `duplicate_candidates` | Candidats fusion (identity resolution) |
| `disputes` | Litiges et réclamations |
| `anonymization_requests` | Demandes RGPD d'effacement |

### 19.4 Learning & Logs Tables

| Table | Description |
|-------|-------------|
| `training_conversations` | Conversations d'entraînement IA |
| `system_logs` | Logs système |
| `whatsapp_logs` | Logs WhatsApp |

---

*Document patrimonial Gold — Validé pour LAWIM Heritage Gold Mission*
