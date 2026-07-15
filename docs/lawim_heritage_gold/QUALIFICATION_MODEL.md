# QUALIFICATION MODEL — Modèle de qualification (Gold Standard)

**Mission :** LAWIM Heritage Gold
**Statut :** Validé — Toute reconstruction doit respecter ce modèle.
**Principe :** Modèle exhaustif et validé de qualification des leads LAWIM.

---

## 1. Rôles utilisateur et scores de base

### 1.1 Classification des rôles

**Source :** `lead_classifier_v1.json`

| Rôle | Score de base | Description |
|------|:------------:|-------------|
| tenant | 40 | Locataire potentiel |
| buyer | 60 | Acheteur potentiel |
| seller | 50 | Vendeur |
| investor | 80 | Investisseur |
| diaspora_investor | 95 | Investisseur diaspora |

### 1.2 Mapping intents → rôles

| Intent | Rôle(s) cible(s) |
|--------|-------------------|
| `RENT_PROPERTY` | tenant |
| `BUY_PROPERTY` | buyer |
| `SELL_PROPERTY` | seller |
| `INVESTOR_INTENT` | investor, diaspora_investor |

---

## 2. Scoring des leads

### 2.1 Boosters de score

| Signal | Bonus |
|--------|:-----:|
| `budget_detected` | +15 |
| `city_detected` | +10 |
| `neighborhood_detected` | +10 |
| `urgent_request` | +20 |
| `diaspora_detected` | +25 |
| `cash_purchase` | +15 |

### 2.2 Pénalités de score

| Signal | Malus |
|--------|:-----:|
| `missing_budget` | -10 |
| `unclear_location` | -10 |
| `spam_like_message` | -50 |

### 2.3 Seuils de classification

#### V1 (seuils entiers)

| Classe | Seuil V1 | Action recommandée |
|--------|:--------:|--------------------|
| HOT | ≥ 80 | call_immediately |
| WARM | ≥ 60 | send_listings |
| COLD | ≥ 40 | request_budget |
| LOW | < 40 | follow_up |

#### V5 (seuils normalisés)

| Classe | Seuil V5 | Action recommandée |
|--------|:--------:|--------------------|
| HOT | ≥ 0.8 | call_immediately |
| WARM | ≥ 0.5 | send_listings |
| COLD | ≥ 0.3 | request_budget |
| SPAM | ≤ 0.2 | ignore |

---

## 3. Pipeline de qualification V5

Pipeline en 8 étapes séquentielles :

| Étape | Entrée | Sortie | Description |
|-------|--------|--------|-------------|
| 1 | `incoming_message` | `normalize_text` | Nettoyage, normalisation, préparation du message brut |
| 2 | `normalize_text` | `extract_entities` | Extraction des entités (ville, quartier, budget, type de bien) |
| 3 | `extract_entities` | `detect_intent` | Détection de l'intention (RENT/BUY/SELL/INVESTOR) |
| 4 | `detect_intent` | `context_enrichment` | Enrichissement contextuel (historique, préférences, mémoire long terme) |
| 5 | `context_enrichment` | `lead_scoring` | Calcul du score composite du lead |
| 6 | `lead_scoring` | `lead_classification` | Classification (HOT/WARM/COLD/SPAM) |
| 7 | `lead_classification` | `crm_routing` | Routage CRM (agent, file d'attente, priorité) |
| 8 | `crm_routing` | `response` | Génération de la réponse finale |

---

## 4. Scoring CRM V5 (7 facteurs)

### 4.1 Pondérations

| Facteur | Poids | Description |
|---------|:-----:|-------------|
| `base_interest` | 0.15 | Intérêt de base exprimé par l'utilisateur |
| `property_type_match` | 0.20 | Correspondance entre le type de bien recherché et l'offre disponible |
| `location_precision` | 0.20 | Précision de la localisation (ville + quartier) |
| `budget_presence` | 0.10 | Présence et clarté du budget |
| `urgency_signal` | 0.15 | Signal d'urgence (temporalité explicite) |
| `visit_intent` | 0.20 | Intention de visite exprimée |
| `trust_signal` | 0.10 | Signal de confiance (référence, recommandation, historique) |

### 4.2 Comportements traqués

| Comportement | Description | Usage |
|-------------|-------------|-------|
| `message_history` | Historique des messages échangés | Analyse de cohérence, détection de changements d'intention |
| `response_time` | Temps de réponse moyen | Mesure d'engagement, priorisation |
| `budget_changes` | Évolution du budget déclaré | Détection d'indécision ou de mise à jour |
| `visit_requests` | Demandes de visite | Signal fort d'intention d'achat |

---

## 5. Ordre de qualification (10 étapes)

L'ordre strict de qualification, à respecter dans toutes les conversations :

| Ordre | Étape | Canal | Description |
|:-----:|-------|-------|-------------|
| 1 | **Intention** | Tous | Déterminer le besoin : louer, acheter, vendre, investir |
| 2 | **Type bien** | Tous | Studio, appartement, maison, villa, duplex, terrain, commercial |
| 3 | **Ville** | Tous | Localisation principale |
| 4 | **Quartier** | WhatsApp/Telegram | Quartier ou zone préférée |
| 5 | **Budget** | Tous | Budget maximum (achat) ou mensuel (location) |
| 6 | **Délai** | Tous | Horizon temporel : urgent, 1 mois, 3 mois, pas de délai |
| 7 | **Critères** | Tous | Surface, nombre de pièces, étage, parking, meublé, etc. |
| 8 | **Préférences** | WhatsApp/Telegram | Préférences supplémentaires (étage, exposition, standing) |
| 9 | **Confirmation** | Tous | Récapitulatif et validation des informations collectées |
| 10 | **Escalade** | Tous | Décision : résultats, rendez-vous, transfert humain |

---

## 6. Champs minimum par profil

### 6.1 Acheteur (buyer)

| Niveau | Champs |
|--------|--------|
| **Obligatoire** | type_de_bien, ville, budget_maximum |
| **Recommandé** | quartier, delai, nombre_de_pieces, usage (résidence principale / investissement) |
| **Optionnel** | source_financement, situation_actuelle (locataire / propriétaire) |

### 6.2 Locataire (tenant)

| Niveau | Champs |
|--------|--------|
| **Obligatoire** | type_de_bien, ville, budget_mensuel |
| **Recommandé** | quartier, duree_souhaitee, nombre_de_pieces |
| **Optionnel** | meuble, animaux_acceptes, parking |

### 6.3 Vendeur (seller)

| Niveau | Champs |
|--------|--------|
| **Obligatoire** | type_de_bien, ville, prix_souhaite |
| **Recommandé** | titre_propriete, surface, description, photos |
| **Optionnel** | motif_vente, disponibilite, historique_bien |

### 6.4 Investisseur (investor)

| Niveau | Champs |
|--------|--------|
| **Obligatoire** | budget, type_investissement (locatif / revente / terrain), ville |
| **Recommandé** | rendement_attendu, horizon, zone_preferee |
| **Optionnel** | experience_immobiliere, autres_investissements |

---

## 7. Champs minimum par type de bien

| Type de bien | Champs obligatoires |
|-------------|---------------------|
| studio | ville, budget, surface_min |
| apartment | ville, budget, nombre_de_pieces |
| house | ville, budget, surface, nombre_de_chambres |
| villa | ville, budget, surface_terrain, nombre_de_chambres |
| duplex | ville, budget, surface, etage |
| land | ville, budget, surface, type_terrain (constructible/agricole) |
| commercial | ville, budget, surface, type_commerce |

---

## 8. Règles de qualification progressive

### 8.1 Règles générales

| Règle | Description |
|-------|-------------|
| **Un message par question** | Sur WhatsApp : une seule question par message |
| **Limite de champs** | Sur Telegram : 2-3 champs maximum par message |
| **Pas de redemande** | Ne jamais redemander un champ déjà collecté |
| **Pas de redémarrage** | Ne jamais recommencer la qualification depuis le début |
| **Correction prioritaire** | La correction de l'utilisateur écrase toujours le contexte obsolète |

### 8.2 Critères d'arrêt

| Condition | Action |
|-----------|--------|
| Ville non couverte | Arrêter la qualification, informer l'utilisateur |
| Inventaire vide pour les critères | Arrêter la qualification, proposer alternatives |
| L'utilisateur demande un humain | Escalade immédiate vers un conseiller |
| Thread répétitif | Arrêter après 3 échanges sans progression |
| L'utilisateur change d'intention | Réinitialiser le contexte partiellement, reprendre à l'étape 1 |

---

## 9. Couches anti-fraude

| Couche | Détection | Action |
|--------|-----------|--------|
| `broker_spam` | Messages de courtiers non sollicités | Pénalité -50, flag manuel |
| `duplicate_listing` | Même bien posté plusieurs fois | Dédoublonnage, avertissement |
| `fake_price` | Prix anormalement bas ou haut | Flag pour vérification manuelle |
| `suspicious_urgency` | Urgence artificielle pour pression | Réduction du poids urgency_signal |

---

## 10. Règles d'escalade

| Type | Condition | Cible |
|------|-----------|-------|
| **Vente** | Lead HOT avec budget confirmé + intention de visite | Agent commercial |
| **Demande** | Question juridique, litige, réclamation | Support / Notaire |
| **Humain** | Sur demande explicite ou après 3 échecs de qualification | Conseiller disponible |

---

## 11. Champs de qualification complets

### 11.1 Champs extraits (KnowledgeBuilder)

| Catégorie | Champs |
|-----------|--------|
| Identité | nom, telephone, email |
| Localisation | ville, pays, quartier |
| Bien | type_bien, surface, pieces, etage |
| Budget | budget_min, budget_max, cash |
| Temporalité | urgence, delai, disponibilite |
| Intention | intent, source, satisfaction_precedente |
| Session | historique_recherche, message_count, session_id |

### 11.2 Champs de lead (7)

| Champ | Description |
|-------|-------------|
| `message` | Message brut de l'utilisateur |
| `intent` | Intention détectée |
| `budget` | Budget extrait |
| `location` | Localisation extraite |
| `property_type` | Type de bien extrait |
| `urgency` | Niveau d'urgence |
| `score` | Score composite calculé |

---

## 12. Détection diaspora

### 12.1 Indicateurs

| Type | Indicateurs |
|------|-------------|
| Localisation | france, paris, lyon, etats-unis, usa, canada, allemagne, belgique, suisse, uk, londres, diaspora, international |
| Indicatif téléphonique | +33, +1, +44, +49 |

### 12.2 Impact

| Élément | Valeur |
|---------|--------|
| Score de base diaspora_investor | 95 (le plus élevé) |
| Bonus matching | +20 |

---

*Document patrimonial Gold — Toute reconstruction doit respecter ce modèle validé.*
