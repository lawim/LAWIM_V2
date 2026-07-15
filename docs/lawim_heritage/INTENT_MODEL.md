# INTENT MODEL — Modèle d'intentions LAWIM

**Sources :** LAWIM `KNOWLEDGE/intents/*.json`, LAWIMA `02_KNOWLEDGE/intents/*.json`, `03_ENGINE/intent_detector/intent_detector.py`, `03_ENGINE/lawim_engine_v1.py`, `06_AI_MODELS/lead_classifier/lead_classifier_v1.json`
**Principe :** Documentation exhaustive des intentions sans fusion ni renommage

---

## 1. Intentions principales

Cinq intentions principales identifiées dans les fichiers d'intention.

Chaque fichier contient : `intent_id`, `keywords[]`, `expressions_fr[]`, `expressions_en[]`, `expressions_pidgin[]`

### 1.1 ACHAT / BUY

**Fichiers :** `KNOWLEDGE/intents/buy_property.json` (LAWIM), `02_KNOWLEDGE/intents/buy_property.json` (LAWIMA/ancienne)

**Flux de qualification :** ask_city → ask_budget → ask_property_type → show_properties

**Mots-clés identifiés dans le code (expressions FR/EN/Pidgin) :**
- acheter, buy, je veux acheter, j'achète, I want to buy, I need to buy
- recherche appartement, looking for apartment, need house

### 1.2 LOCATION / RENT

**Fichiers :** `KNOWLEDGE/intents/rent_property.json` (LAWIM), `02_KNOWLEDGE/intents/rent_property.json` (LAWIMA/ancienne)

**Flux de qualification :** ask_city → ask_neighborhood → ask_budget → show_properties

**Mots-clés identifiés (code) :**
- location, louer, rent, à louer, for rent, I want to rent
- cherche maison à louer, looking for apartment to rent

### 1.3 VENTE / SELL

**Fichiers :** `KNOWLEDGE/intents/sell_property.json` (LAWIM), `02_KNOWLEDGE/intents/sell_property.json` (LAWIMA/ancienne)

**Flux de qualification :** ask_property_details → collect_contact → create_listing

**Mots-clés identifiés (code) :**
- vente, vendre, sell, à vendre, for sale, I want to sell
- j'ai une maison à vendre, I have a property

### 1.4 RECHERCHE / SEARCH

**Fichiers :** `KNOWLEDGE/intents/search_property.json` (LAWIM), `02_KNOWLEDGE/intents/search_property.json` (LAWIMA/ancienne)

**Mots-clés identifiés (code) :**
- je cherche, i need, looking for, besoin, recherche
- je veux, I want, I'm looking

### 1.5 INVESTISSEUR / INVESTOR

**Fichiers :** `KNOWLEDGE/intents/investor_intent.json` (LAWIM), `02_KNOWLEDGE/intents/investor_intent.json` (LAWIMA/ancienne)

**Flux de qualification :** ask_city → ask_budget → ask_investment_goal → show_opportunities

## 2. Intentions supplémentaires (détectées dans le code)

**Source :** LAWIMA `03_ENGINE/lawim_engine_v1.py`

### 2.1 VISITE / VISIT_REQUEST
- Mots-clés : visite, voir, visit, on passe, check
- Sous-intention de BUY ou RENT

### 2.2 URGENCE / URGENT_SIGNAL
- Mots-clés : urgent, asap, vite, rapidement, immediately, now
- Modificateur de scoring (+20)

### 2.3 PRIX / PRICE_SIGNAL
- Mots-clés : prix, budget, max, k, mille
- Sous-intention, utilisée pour l'extraction d'information

### 2.4 BROKER / COURTTER
- Mots-clés : je peux trouver, j'ai un contact
- Détecte les intermédiaires non-agréés

### 2.5 DIASPORA
- Détection par localisation (france, paris, london, etc.) ou indicatif téléphonique (+33, +1, etc.)
- Modificateur de scoring (+25)

## 3. Détection multi-intention

**Source :** LAWIMA `08_CONFIG/rule_engine/RULE_ENGINE_V5.json`

- `multi_intent_allowed: true`
- Un message peut contenir plusieurs intentions simultanées
- Exemple : "Je cherche une maison à vendre à Douala" → SELL + SEARCH

## 4. Hiérarchie de détection des intentions

**Source :** LAWIMA `03_ENGINE/intent_detector/intent_detector.py`

1. **Keyword matching** contre les fichiers JSON d'intention
2. Chargement dynamique des fichiers depuis `02_KNOWLEDGE/intents/`
3. Correspondance par mots-clés prioritaires

## 5. Score de priorité des intentions (lead_classifier)

**Source :** LAWIMA `06_AI_MODELS/lead_classifier/lead_classifier_v1.json`

| Intention | Score de base | Priorité implicite |
|-----------|--------------|-------------------|
| INVESTOR (investisseur) | 80 | Très haute |
| DIASPORA_INVESTOR | 95 | Maximale |
| BUY (acheteur) | 60 | Haute |
| SELL (vendeur) | 50 | Moyenne |
| RENT (locataire) | 40 | Standard |

## 6. Flows de qualification par intention

**Source :** LAWIMA `06_AI_MODELS/conversation_flows/conversation_flows_v1.json`

| Intention | Flow |
|-----------|------|
| SEARCH_PROPERTY | ask_city → ask_neighborhood → ask_budget → show_properties |
| RENT_PROPERTY | ask_city → ask_neighborhood → ask_budget → show_properties |
| BUY_PROPERTY | ask_city → ask_budget → ask_property_type → show_properties |
| SELL_PROPERTY | ask_property_details → collect_contact → create_listing |
| INVESTOR_INTENT | ask_city → ask_budget → ask_investment_goal → show_opportunities |

---

*Document patrimonial — Aucune décision de reconstruction n'est prise ici.*
