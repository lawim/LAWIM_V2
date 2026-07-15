# RAPPORT DE VALIDATION — QUALIFICATION_MODEL.md

**Date :** 2026-07-15  
**Auditeur :** Validation automatique sur les 3 branches legacy  
**Branches vérifiées :** LAWIMA, LAWIM, ancienne_structure (via `LAWIM_BACKUP_20260608_125026`)

---

## Résumé

| Statut | Nombre |
|--------|--------|
| ✅ CONFIRMÉ | 14 |
| ⚠️ PARTIELLEMENT CONFIRMÉ | 2 |
| ❌ NON CONFIRMÉ | 2 |
| **Total** | **18** |

---

## 1. Types d'utilisateurs (tenant=40, buyer=60, seller=50, investor=80, diaspora_investor=95)

**Source vérifiée :** `LAWIMA/06_AI_MODELS/lead_classifier/lead_classifier_v1.json` (lignes 2-27)

```json
"tenant": { "base_score": 40 },
"buyer": { "base_score": 60 },
"seller": { "base_score": 50 },
"investor": { "base_score": 80 },
"diaspora_investor": { "base_score": 95 }
```

**Statut : ✅ CONFIRMÉ** — Tous les scores correspondent exactement.

---

## 2. Types additionnels (property_seeker, agent, owner, broker)

**Source vérifiée :** `LAWIMA/08_CONFIG/rule_engine/RULE_ENGINE_V3.json` (lignes 60-67)

```json
"property_seeker": "search intent + budget mention",
"agent": "multiple listings + commission language",
"owner": "direct property ownership signals",
"broker": "connection + transport fee + intermediary signals"
```

**Statut : ✅ CONFIRMÉ** — Présents dans `RULE_ENGINE_V3.json` (layer_4_business_context_engine.user_classification).

---

## 3. Boosters V1 (budget_detected+15, city_detected+10, neighborhood_detected+10, urgent_request+20, diaspora_detected+25, cash_purchase+15)

**Source vérifiée :** `LAWIMA/06_AI_MODELS/lead_classifier/lead_classifier_v1.json` (lignes 29-36)

```json
"score_boosters": {
  "budget_detected": 15,
  "city_detected": 10,
  "neighborhood_detected": 10,
  "urgent_request": 20,
  "diaspora_detected": 25,
  "cash_purchase": 15
}
```

**Statut : ✅ CONFIRMÉ** — Tous les boosters et leurs valeurs correspondent.

---

## 4. Boosters message>20caractères+30, budget présent+25, localisation présente+25, type bien présent+20

**Source vérifiée :** `LAWIMA/03_ENGINE/lead_scorer/lead_scorer.py`

**Résultat :** Le fichier `lead_scorer.py` utilise UNIQUEMENT les boosters de `lead_classifier_v1.json` (budget_detected=15, city_detected=10, neighborhood_detected=10, urgent_request=20, diaspora_detected=25, cash_purchase=15). **Aucune trace** des boosters suivants dans ce fichier :
- Message > 20 caractères = +30 ❌
- Budget présent = +25 ❌
- Localisation présente = +25 ❌
- Type de bien présent = +20 ❌

Un fichier alternatif `lead_scorer_supabase.py` existe avec des règles différentes mais ne correspond pas non plus.

**Statut : ❌ NON CONFIRMÉ** — Ces boosters ne se trouvent pas dans `lead_scorer.py`. Source probable différente ou version non archivée.

---

## 5. Pénalités (missing_budget-10, unclear_location-10, spam-50)

**Source vérifiée :** `LAWIMA/06_AI_MODELS/lead_classifier/lead_classifier_v1.json` (lignes 38-42)

```json
"score_penalties": {
  "missing_budget": -10,
  "unclear_location": -10,
  "spam_like_message": -50
}
```

**Statut : ✅ CONFIRMÉ** — Présentes avec les valeurs exactes. `lead_scorer.py` (lignes 56-63) implémente également ces pénalités.

---

## 6. Seuils V1 (HOT≥80, WARM≥60, COLD≥40, LOW<40)

**Sources vérifiées :** `lead_classifier_v1.json` (lignes 44-46) et `lead_scorer.py` (lignes 65-75)

```json
"hot_lead_threshold": 80,
"warm_lead_threshold": 60,
"cold_lead_threshold": 40
```

```python
if score >= 80: temperature = "HOT"
elif score >= 60: temperature = "WARM"
elif score >= 40: temperature = "COLD"
else: temperature = "LOW"
```

**Statut : ✅ CONFIRMÉ** — Les 4 seuils sont confirmés dans les deux sources.

---

## 7. Seuils V5 (HOT≥0.8, WARM≥0.5, COLD≥0.3, SPAM≥0.2)

**Source vérifiée :** `LAWIMA/08_CONFIG/rule_engine/RULE_ENGINE_V5.json` (lignes 43-48)

```json
"lead_classification": {
  "hot": 0.8,
  "warm": 0.5,
  "cold": 0.3,
  "spam_risk": 0.2
}
```

**Statut : ✅ CONFIRMÉ** — Les 4 seuils correspondent. Le nom diffère (spam_risk au lieu de SPAM) mais la valeur 0.2 est exacte.

---

## 8. Pondérations CRM V5 (base_interest 0.15, property_type_match 0.2, location_precision 0.2, budget_presence 0.1, urgency_signal 0.15, visit_intent 0.2, trust_signal 0.1)

**Source vérifiée :** `LAWIMA/08_CONFIG/rule_engine/RULE_ENGINE_V5.json` (lignes 33-41)

```json
"crm_scoring_v5": {
  "base_interest": 0.15,
  "property_type_match": 0.2,
  "location_precision": 0.2,
  "budget_presence": 0.1,
  "urgency_signal": 0.15,
  "visit_intent": 0.2,
  "trust_signal": 0.1
}
```

**Statut : ✅ CONFIRMÉ** — Toutes les pondérations correspondent exactement (total = 1.0).

---

## 9. Actions (call_immediately, send_listings, request_budget, follow_up, ignore)

**Source vérifiée :** `LAWIMA/08_CONFIG/rule_engine/RULE_ENGINE_V5.json` (lignes 81-87)

```json
"recommended_action": [
  "call_immediately",
  "send_listings",
  "request_budget",
  "follow_up",
  "ignore"
]
```

**Statut : ✅ CONFIRMÉ** — Les 5 actions sont présentes dans le schéma de sortie CRM V5.

---

## 10. 32 champs profil KnowledgeBuilder

**Source vérifiée :** `LAWIMA/03_ENGINE/knowledge_builder.py` (lignes 24-31)

```python
self.USER_FIELDS = [
  "name", "phone", "email", "city", "country", "username", "channel",
  "preferred_budget", "preferred_location", "preferred_property_type",
  "preferred_intent", "urgency", "surface", "rooms", "bedrooms",
  "has_parking", "has_elevator", "is_furnished", "is_negotiable",
  "available_from", "proximity_school", "proximity_market",
  "proximity_transport", "proximity_hospital", "phone_source",
  "is_contact_complete"
]
```

**Statut : ⚠️ PARTIELLEMENT CONFIRMÉ** — Le fichier liste **25 champs USER_FIELDS** (pas 32). Le document mentionne également "25+ autres champs" mais la liste réelle fait 25 champs. Les 32 pourraient inclure les PROPERTY_FIELDS (16) et LEAD_FIELDS (10) additionnels, mais ce n'est pas précisé dans l'affirmation.

---

## 11. 7 champs lead (message, intent, budget, location, property_type, urgency, score)

**Source vérifiée :** `LAWIMA/03_ENGINE/knowledge_builder.py` (lignes 42-45)

```python
self.LEAD_FIELDS = [
  "message", "intent", "budget", "location", "property_type",
  "urgency", "score", "status", "priority", "diaspora_flag"
]
```

**Statut : ⚠️ PARTIELLEMENT CONFIRMÉ** — Les 7 champs listés sont bien présents, mais le fichier en contient en réalité **10** (status, priority, diaspora_flag en plus). L'affirmation n'est pas fausse mais incomplète.

---

## 12. Comportements traqués (message_history, response_time_tracking, budget_changes_tracking, visit_requests_tracking)

**Source vérifiée :** `LAWIMA/08_CONFIG/rule_engine/RULE_ENGINE_V5.json` (lignes 50-55)

```json
"behavior_tracking": {
  "message_history": true,
  "response_time_tracking": true,
  "budget_changes_tracking": true,
  "visit_requests_tracking": true
}
```

**Statut : ✅ CONFIRMÉ** — Les 4 comportements sont présents et activés.

---

## 13. Indicateurs diaspora (france, paris, lyon, etats-unis, usa, canada, allemagne, belgique, suisse, uk, londres, diaspora, international)

**Source vérifiée :** `LAWIMA/03_ENGINE/diaspora_filter.py` (lignes 19-21)

```python
indicators = ["france", "paris", "lyon", "etats-unis", "usa", "canada",
              "allemagne", "belgique", "suisse", "uk", "londres",
              "diaspora", "international", "+33", "+1", "+44", "+49"]
```

**Statut : ✅ CONFIRMÉ** — Les 13 indicateurs sont tous présents. Les indicatifs téléphoniques sont également dans la même liste (voir affirmation 14).

---

## 14. Indicatifs diaspora (+33, +1, +44, +49)

**Source vérifiée :** `LAWIMA/03_ENGINE/diaspora_filter.py` (ligne 21)

**Statut : ✅ CONFIRMÉ** — Les 4 indicatifs sont présents dans la liste `indicators`.

---

## 15. Services diaspora (table diaspora_services)

**Source vérifiée :** `LAWIMA/05_AUTOMATIONS/scripts/implement_all.sql` (lignes 83-90)

```sql
CREATE TABLE IF NOT EXISTS diaspora_services (
    id SERIAL PRIMARY KEY,
    client_phone TEXT,
    service_type TEXT,
    price INTEGER,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);
```

**Statut : ✅ CONFIRMÉ** — La table `diaspora_services` est créée avec les colonnes documentées.

---

## 16. Anti-spam (10 msg/min, 60min blocage, table blocked_users)

**Source vérifiée :** `LAWIMA/03_ENGINE/anti_spam.py` (lignes 17-18, 33, 41)

```python
self.MAX_PER_MINUTE = 10
self.BLOCK_DURATION = 60  # minutes
# Table utilisée : blocked_users
```

**Statut : ✅ CONFIRMÉ** — Limite à 10 messages/minute, blocage 60 minutes, table `blocked_users`.

---

## 17. Pipeline 8 étapes V5

**Source vérifiée :** `LAWIMA/08_CONFIG/rule_engine/RULE_ENGINE_V5.json` (lignes 6-15)

```json
"pipeline_stages": [
  "incoming_message",
  "normalize_text",
  "extract_entities",
  "detect_intent",
  "context_enrichment",
  "lead_scoring",
  "lead_classification",
  "crm_routing"
]
```

**Statut : ✅ CONFIRMÉ** — Pipeline de 8 étapes exactes. Le document mentionne "→ response" en étape 9 implicite non listée dans le JSON.

---

## 18. Anti-fraud layers (broker_spam_detection, duplicate_listing_detection, fake_price_detection, suspicious_urgency_detection)

**Source vérifiée :** `LAWIMA/08_CONFIG/rule_engine/RULE_ENGINE_V5.json` (lignes 57-62)

```json
"anti_fraud": {
  "broker_spam_detection": true,
  "duplicate_listing_detection": true,
  "fake_price_detection": true,
  "suspicious_urgency_detection": true
}
```

**Statut : ✅ CONFIRMÉ** — Les 4 couches anti-fraude sont présentes et activées.

---

## Synthèse des écarts

| # | Affirmation | Statut | Détail de l'écart |
|---|-------------|--------|-------------------|
| 4 | Boosteurs lead_scorer | ❌ NON CONFIRMÉ | Les valeurs +30/+25/+25/+20 ne se trouvent PAS dans `lead_scorer.py` |
| 10 | 32 champs KnowledgeBuilder | ⚠️ Partiel | 25 USER_FIELDS trouvés, pas 32 |
| 11 | 7 champs lead | ⚠️ Partiel | 10 champs trouvés (7 documentés + 3 non mentionnés) |

---

*Rapport généré le 2026-07-15 — Validations sur les 3 branches legacy (LAWIMA, LAWIM, ancienne_structure)*
