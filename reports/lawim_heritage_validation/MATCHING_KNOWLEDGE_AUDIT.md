# AUDIT COMPLET DES CONNAISSANCES MATCHING — LAWIM HERITAGE GOLD

**Date :** 2026-07-15
**Auditeur :** Matching Expert — Re-audit exhaustif
**Sources vérifiées :** 11 fichiers sur 3 branches legacy (LAWIMA, LAWIM, backup)

---

## LÉGENDE

| Champ | Description |
|-------|-------------|
| KNOWLEDGE_ID | Identifiant unique MR-xxx |
| CONCEPT | Domaine fonctionnel |
| DESCRIPTION | Résumé de la règle ou connaissance |
| SOURCE_FILE | Fichier source exact |
| EXCERPT | Citation textuelle de la source |
| CONFIDENCE | VALIDATED / PARTIAL / NON_VALIDE |

---

## 1. DIMENSIONS ET POIDS DE SCORING (V1 — matching_weights)

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-001 | Scoring Weights | City match = 30% du score | `LAWIMA/06_AI_MODELS/matching_engine/property_matching_v1.json` | `"matching_weights": { "city": 30, "neighborhood": 25, "budget": 25, "property_type": 15, "title_status": 5 }` | VALIDATED |
| MR-002 | Scoring Weights | Neighborhood match = 25% du score | idem | idem | VALIDATED |
| MR-003 | Scoring Weights | Budget match = 25% du score | idem | idem | VALIDATED |
| MR-004 | Scoring Weights | Property type match = 15% du score | idem | idem | VALIDATED |
| MR-005 | Scoring Weights | Title foncier status = 5% du score | idem | idem | VALIDATED |

---

## 2. DIMENSIONS DE SCORING (version Decision Engine — Ch26)

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-006 | Scoring Weights (DE) | Type de bien = 25% du score immobilier | `LAWIM/Directive/04-DECISION-ENGINE-REFERENCE.md` (Ch26) | `Type de bien: 25%, Opération: 20%, Budget: 15%, Localisation: 15%, Caractéristiques critiques: 15%, Caractéristiques recommandées: 10%` | VALIDATED |
| MR-007 | Scoring Weights (DE) | Opération = 20% du score immobilier | idem | idem | VALIDATED |
| MR-008 | Scoring Weights (DE) | Budget = 15% du score immobilier | idem | idem | VALIDATED |
| MR-009 | Scoring Weights (DE) | Localisation = 15% du score immobilier | idem | idem | VALIDATED |
| MR-010 | Scoring Weights (DE) | Caractéristiques critiques = 15% | idem | idem | VALIDATED |
| MR-011 | Scoring Weights (DE) | Caractéristiques recommandées = 10% | idem | idem | VALIDATED |

---

## 3. TRANSACTION SUCCESS SCORE (Decision Engine — Ch90)

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-012 | Transaction Success Score | Compatibilité immobilière = 30% | idem (Ch90) | `Compatibilité immobilière: 30%, Géographique: 15%, Disponibilité: 10%, Documentaire: 10%, Réactivité détenteur: 10%, Historique demandeur: 10%, Faisabilité financière: 10%, Probabilité négociation: 5%` | VALIDATED |
| MR-013 | Transaction Success Score | Compatibilité géographique = 15% | idem | idem | VALIDATED |
| MR-014 | Transaction Success Score | Disponibilité réelle = 10% | idem | idem | VALIDATED |
| MR-015 | Transaction Success Score | Situation documentaire = 10% | idem | idem | VALIDATED |
| MR-016 | Transaction Success Score | Réactivité du détenteur = 10% | idem | idem | VALIDATED |
| MR-017 | Transaction Success Score | Historique du demandeur = 10% | idem | idem | VALIDATED |
| MR-018 | Transaction Success Score | Faisabilité financière = 10% | idem | idem | VALIDATED |
| MR-019 | Transaction Success Score | Probabilité de négociation = 5% | idem | idem | VALIDATED |

---

## 4. TOLÉRANCES BUDGÉTAIRES

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-020 | Budget Tolerance | Location (rent) = 20% d'écart | `LAWIMA/06_AI_MODELS/matching_engine/property_matching_v1.json` | `"budget_tolerance": { "rent": 0.20, "buy": 0.15, "invest": 0.25 }` | VALIDATED |
| MR-021 | Budget Tolerance | Achat (buy) = 15% d'écart | idem | idem | VALIDATED |
| MR-022 | Budget Tolerance | Investissement (invest) = 25% d'écart | idem | idem | VALIDATED |

---

## 5. BOOSTS (priority_rules)

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-023 | Boost Rule | Exact neighborhood match = +25 | idem | `{ "condition": "exact_neighborhood_match", "boost": 25 }` | VALIDATED |
| MR-024 | Boost Rule | Exact city match = +20 | idem | `{ "condition": "exact_city_match", "boost": 20 }` | VALIDATED |
| MR-025 | Boost Rule | Budget within range = +15 | idem | `{ "condition": "budget_within_range", "boost": 15 }` | VALIDATED |
| MR-026 | Boost Rule | Title foncier present = +10 | idem | `{ "condition": "title_foncier", "boost": 10 }` | VALIDATED |
| MR-027 | Boost Rule | Diaspora investor = +20 | idem | `{ "condition": "diaspora_investor", "boost": 20 }` | VALIDATED |

---

## 6. ALGORITHME V5 (scoring par points)

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-028 | V5 Scoring | Location match = +40 pts | `LAWIMA/03_ENGINE/property_matcher/property_matcher_v5.py` (l.51-52) | `if city and city.lower() in prop.get("location","").lower(): score += 40` | VALIDATED |
| MR-029 | V5 Scoring | Budget exact = +50 pts | idem (l.56-57) | `if diff == 0: score += 50` | VALIDATED |
| MR-030 | V5 Scoring | Budget ±10% = +35 pts | idem (l.58-59) | `elif diff < budget * 0.1: score += 35` | VALIDATED |
| MR-031 | V5 Scoring | Budget ±30% = +20 pts | idem (l.60-61) | `elif diff < budget * 0.3: score += 20` | VALIDATED |
| MR-032 | V5 Scoring | Budget ±50% = +10 pts | idem (l.62-63) | `elif diff < budget * 0.5: score += 10` | VALIDATED |
| MR-033 | V5 Scoring | Property type match = +10 (V5) ou +25 (V4) | idem (l.65-66) et `property_matcher_supabase.py` (l.69) | `score += 10` (V5) ; +25 dans V4 | VALIDATED |

---

## 7. SYSTÈME DE NOTATION PAR ÉTOILES

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-034 | Star Rating | Score ≥80 = 5/5 | `LAWIMA/03_ENGINE/property_matcher/property_matcher_v5.py` (l.30-40) | `if score >= 80: return "⭐⭐⭐⭐⭐ (5/5)"` | VALIDATED |
| MR-035 | Star Rating | Score ≥60 = 4/5 | idem | `elif score >= 60: return "⭐⭐⭐⭐ (4/5)"` | VALIDATED |
| MR-036 | Star Rating | Score ≥40 = 3/5 | idem | `elif score >= 40: return "⭐⭐⭐ (3/5)"` | VALIDATED |
| MR-037 | Star Rating | Score ≥20 = 2/5 | idem | `elif score >= 20: return "⭐⭐ (2/5)"` | VALIDATED |
| MR-038 | Star Rating | Score <20 = 1/5 | idem | `else: return "⭐ (1/5)"` | VALIDATED |

---

## 8. SEUILS MINIMUM ET LIMITES

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-039 | Minimum Score | Score minimum = 60/100 | `LAWIMA/06_AI_MODELS/matching_engine/property_matching_v1.json` | `"minimum_match_score": 60` | VALIDATED |
| MR-040 | Results Limit | Maximum résultats = 10 (V1) | idem | `"top_results_limit": 10` | VALIDATED |
| MR-041 | First Proposal Limit | Maximum 5 biens au premier matching | `LAWIM/Directive/04-DECISION-ENGINE-REFERENCE.md` (Ch34) | `Le moteur ne propose jamais plus de 5 biens lors d'un premier matching.` | VALIDATED |
| MR-042 | Score Threshold (DE) | Score <60% = jamais proposé | idem (Ch26) | `Si le score est inférieur à 60 %, le bien n'est jamais proposé.` | VALIDATED |
| MR-043 | Score Threshold (DE) | Score <25% = ne jamais proposer | idem (Ch92) | `Score 25% → Ne jamais proposer.` | PARTIAL — cohérent mais redondant avec 60% du Ch26, source du seuil exact à clarifier |

---

## 9. CLASSIFICATION DES LEADS (lead_classifier_v1.json)

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-044 | Lead Classification | Tenant → base_score=40 | `LAWIMA/06_AI_MODELS/lead_classifier/lead_classifier_v1.json` | `"tenant": { "intents": ["RENT_PROPERTY"], "base_score": 40 }` | VALIDATED |
| MR-045 | Lead Classification | Buyer → base_score=60 | idem | `"buyer": { "intents": ["BUY_PROPERTY"], "base_score": 60 }` | VALIDATED |
| MR-046 | Lead Classification | Seller → base_score=50 | idem | `"seller": { "intents": ["SELL_PROPERTY"], "base_score": 50 }` | VALIDATED |
| MR-047 | Lead Classification | Investor → base_score=80 | idem | `"investor": { "intents": ["INVESTOR_INTENT"], "base_score": 80 }` | VALIDATED |
| MR-048 | Lead Classification | Diaspora investor → base_score=95 | idem | `"diaspora_investor": { "intents": ["INVESTOR_INTENT"], "base_score": 95 }` | VALIDATED |

---

## 10. BOOSTERS ET PÉNALITÉS DE SCORE LEAD

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-049 | Lead Score Booster | Budget detected = +15 | idem | `"budget_detected": 15` | VALIDATED |
| MR-050 | Lead Score Booster | City detected = +10 | idem | `"city_detected": 10` | VALIDATED |
| MR-051 | Lead Score Booster | Neighborhood detected = +10 | idem | `"neighborhood_detected": 10` | VALIDATED |
| MR-052 | Lead Score Booster | Urgent request = +20 | idem | `"urgent_request": 20` | VALIDATED |
| MR-053 | Lead Score Booster | Diaspora detected = +25 | idem | `"diaspora_detected": 25` | VALIDATED |
| MR-054 | Lead Score Booster | Cash purchase = +15 | idem | `"cash_purchase": 15` | VALIDATED |
| MR-055 | Lead Score Penalty | Missing budget = -10 | idem | `"missing_budget": -10` | VALIDATED |
| MR-056 | Lead Score Penalty | Unclear location = -10 | idem | `"unclear_location": -10` | VALIDATED |
| MR-057 | Lead Score Penalty | Spam-like message = -50 | idem | `"spam_like_message": -50` | VALIDATED |

---

## 11. SEUILS DE TEMPÉRATURE DES LEADS

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-058 | Lead Temperature | Hot lead threshold = ≥80 | idem | `"hot_lead_threshold": 80` | VALIDATED |
| MR-059 | Lead Temperature | Warm lead threshold = ≥60 | idem | `"warm_lead_threshold": 60` | VALIDATED |
| MR-060 | Lead Temperature | Cold lead threshold = ≥40 | idem | `"cold_lead_threshold": 40` | VALIDATED |

---

## 12. PRIORITÉ DU RAISONNEMENT

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-061 | Reasoning Priority | Ordre: intent → location → budget → property_type | `LAWIMA/06_AI_MODELS/reasoning/reasoning_rules_v1.json` | `"priority_order": ["intent", "location", "budget", "property_type"]` | VALIDATED |
| MR-062 | Reasoning Steps | Séquences: detect_intent → detect_city → detect_neighborhood → detect_budget → classify_lead → match_properties → rank_results | idem | `"reasoning_steps": ["detect_intent", "detect_city", "detect_neighborhood", "detect_budget", "classify_lead", "match_properties", "rank_results"]` | VALIDATED |
| MR-063 | Confidence Threshold | Seuil de confiance global = 0.70 | idem | `"confidence_threshold": 0.70` | VALIDATED |

---

## 13. SCORING LEAD PAR TYPE D'UTILISATEUR (lead_scoring.json)

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-064 | Lead Scoring | Diaspora investor (high urgency) = 100, P0 | `LAWIM/KNOWLEDGE/lead_scoring/lead_scoring.json` | `{ "user_type": "diaspora_investor", "score": 100, "priority": "P0" }` | VALIDATED |
| MR-065 | Lead Scoring | Buyer (budget ≥50M) = 95, P0 | idem | `{ "user_type": "buyer", "budget_min": 50000000, "score": 95, "priority": "P0" }` | VALIDATED |
| MR-066 | Lead Scoring | Seller = 90, P1 | idem | `{ "user_type": "seller", "score": 90, "priority": "P1" }` | VALIDATED |
| MR-067 | Lead Scoring | Land buyer = 85, P1 | idem | `{ "user_type": "land_buyer", "score": 85, "priority": "P1" }` | VALIDATED |
| MR-068 | Lead Scoring | Tenant = 40, P3 | idem | `{ "user_type": "tenant", "score": 40, "priority": "P3" }` | VALIDATED |

---

## 14. RÈGLES DE SCORING LEAD (lead_scoring_rules.json)

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-069 | Lead Scoring Rules | Budget = 20 (poids) | `LAWIM/KNOWLEDGE/scoring/lead_scoring_rules.json` | `"budget": 20` | VALIDATED |
| MR-070 | Lead Scoring Rules | Location = 15 | idem | `"location": 15` | VALIDATED |
| MR-071 | Lead Scoring Rules | Urgency = 20 | idem | `"urgency": 20` | VALIDATED |
| MR-072 | Lead Scoring Rules | Diaspora = 10 | idem | `"diaspora": 10` | VALIDATED |
| MR-073 | Lead Scoring Rules | Phone = 5 | idem | `"phone": 5` | VALIDATED |
| MR-074 | Lead Scoring Rules | Property type = 15 | idem | `"property_type": 15` | VALIDATED |
| MR-075 | Lead Scoring Rules | Investment profile = 10 | idem | `"investment_profile": 10` | VALIDATED |

---

## 15. RÈGLES D'EXCLUSION

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-076 | Exclusion | Propriétés archivées exclues (statut != 'available') | `LAWIMA/03_ENGINE/property_matcher/property_matcher_v5.py` (l.16) et `MATCHING_ENGINE_V1_SUMMARY.md` | `self.supabase.table("properties").select("*").eq("status", status).execute()` + cas test #7-8 | VALIDATED |
| MR-077 | Exclusion | Budget hors tolérance → score 0 | `MATCHING_ENGINE_V1_SUMMARY.md` (cas test #8) | `Budget overflow → Score 0` | VALIDATED |
| MR-078 | Exclusion | Ville différente → score 0 (sauf multi-ville) | idem (cas test #7) | `Different city → Score 0` | VALIDATED |
| MR-079 | Exclusion | Propriétés déjà envoyées → blacklist | `MATCHING_ENGINE_V1_IMPLEMENTATION_SCOPE.md` | Blacklist check referenced | VALIDATED |
| MR-080 | Exclusion | Opération incompatible (location ≠ vente) | `LAWIM/Directive/04-DECISION-ENGINE-REFERENCE.md` (Ch25) | `Location → Vente → Éliminé` | VALIDATED |
| MR-081 | Exclusion | Type de bien incompatible (appartement ≠ terrain) | idem | `Appartement → Terrain → Éliminé` | VALIDATED |
| MR-082 | Exclusion | Budget dépassé de manière manifeste | idem | `Budget 50M → Bien 120M → Éliminé (sauf si dépassement autorisé)` | VALIDATED |
| MR-083 | Exclusion | Bien indisponible (vendu/loué/archivé/suspendu) | idem (Ch16, Ch28) | `Un bien indisponible ne participe pas au matching. Vendu/Loué/Archivé → 0%` | VALIDATED |

---

## 16. RÈGLES DE COMPATIBILITÉ (4 niveaux)

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-084 | Compatibility | Niveau 1 — Critique: champs obligatoires, sans lesquels aucun matching possible | `LAWIM/Directive/04-DECISION-ENGINE-REFERENCE.md` (Ch9) | `Niveau 1 — Compatibilité critique: Sans compatibilité critique, aucun matching n'est possible.` | VALIDATED |
| MR-085 | Compatibility | Niveau 2 — Fonctionnelle: chambres, superficie, budget, type de bien | idem | `Le bien répond correctement aux besoins principaux. Exemple: nombre de chambres, superficie, budget, type de bien.` | VALIDATED |
| MR-086 | Compatibility | Niveau 3 — Confort: garage, forage, jardin, piscine, balcon, terrasse | idem | `Le bien possède des éléments appréciés mais non indispensables.` | VALIDATED |
| MR-087 | Compatibility | Niveau 4 — Préférentielle: quartier préféré, orientation, vue, proximité école/travail | idem | `Le moteur tient compte des préférences observées.` | VALIDATED |

---

## 17. GESTION DES PRÉFÉRENCES ET APPRENTISSAGE

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-088 | Preference Learning | Le moteur apprend des refus/acceptations: 3 refus pour absence garage → garage devient prioritaire | idem (Ch19) | `Trois refus pour absence de garage → le garage devient prioritaire.` | VALIDATED |
| MR-089 | Preference Learning | Quartier régulièrement accepté → favorisé | idem | `Acceptation répétée d'un quartier → Ce quartier est favorisé.` | VALIDATED |
| MR-090 | Preference Learning | Ajustement propre au dossier, ne modifie pas le référentiel global | idem (Ch59) | `Ces ajustements sont propres au dossier. Ils ne modifient pas le référentiel global.` | VALIDATED |
| MR-091 | Preference Learning | Apprentissage global des tendances du marché | idem (Ch73) | `Les appartements meublés à Bonapriso sont très demandés → Le moteur adapte leur priorité.` | VALIDATED |
| MR-092 | Preference Learning | Budget flexible: bien légèrement supérieur possible si autres critères excellents | idem (Ch13) | `Le moteur peut proposer un bien légèrement supérieur au budget uniquement lorsque les autres critères sont excellents.` | VALIDATED |

---

## 18. PROXIMITÉ GÉOGRAPHIQUE ET QUARTIERS

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-093 | Geographic Proximity | Si quartier demandé vide → proposer quartiers voisins similaires | idem (Ch14) | `Lorsque le quartier demandé ne contient aucun bien compatible, le moteur peut proposer des quartiers voisins présentant des caractéristiques similaires.` | VALIDATED |
| MR-094 | Geographic Proximity | Si GPS disponible → distance réelle, pas à vol d'oiseau | idem (Ch15) | `Lorsque les coordonnées GPS sont disponibles, le moteur utilise la distance réelle.` | VALIDATED |
| MR-095 | Geographic Score | Ville + quartier + GPS + distance réelle + temps de trajet | idem (Ch27) | `Le score géographique tient compte: ville, quartier, GPS, distance réelle, temps de trajet.` | VALIDATED |
| MR-096 | City Affinity | Règle: Ville exacte → Quartier exact → Affinité forte → Validation utilisateur → WAITLISTED | `LAWIM/KNOWLEDGE/city-affinity-matrix.md` | `Ville exacte → Quartier exact → Affinité forte → Validation utilisateur → WAITLISTED` | VALIDATED |
| MR-097 | City Affinity | Interdictions: Soa→Obala, Soa→Bafia, Yaoundé→Soa, Douala→Dibombari | idem | Tableau des interdictions avec raisons | VALIDATED |
| MR-098 | City Affinity | 10 villes principales: Yaoundé, Douala, Bafoussam, Kribi, Limbe, Garoua, Bamenda, Maroua, Ngaoundéré, Bertoua | idem | Liste des 10 villes principales | VALIDATED |

---

## 19. SCORE DE DISPONIBILITÉ

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-099 | Availability Score | Disponible = 100% | `LAWIM/Directive/04-DECISION-ENGINE-REFERENCE.md` (Ch28) | `100% → Disponible.` | VALIDATED |
| MR-100 | Availability Score | Réservation en cours = 70% | idem | `70% → Réservation en cours.` | VALIDATED |
| MR-101 | Availability Score | Réponse propriétaire en attente = 30% | idem | `30% → Réponse propriétaire en attente.` | VALIDATED |
| MR-102 | Availability Score | Vendu/Loué/Archivé = 0%, jamais proposé | idem | `0% → Vendu/Loué/Archivé. Les biens à 0% ne sont jamais proposés.` | VALIDATED |

---

## 20. SCORE DOCUMENTAIRE

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-103 | Document Score | Titre foncier = 100% | idem (Ch29) | `Titre foncier → 100%` | VALIDATED |
| MR-104 | Document Score | En cours d'immatriculation = 80% | idem | `En cours d'immatriculation → 80%` | VALIDATED |
| MR-105 | Document Score | Droit coutumier = 60% | idem | `Droit coutumier → 60%` | VALIDATED |
| MR-106 | Document Score | Documents inconnus = 40% | idem | `Documents inconnus → 40%` | VALIDATED |

---

## 21. SCORE QUALITÉ ET CONFIANCE

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-107 | Quality Score | Points pour: photos, GPS, description, qualification complète, disponibilité confirmée | idem (Ch30) | `Points attribués pour: photos, GPS, description, qualification complète, disponibilité confirmée.` | VALIDATED |
| MR-108 | Trust Index | Indice: Très élevé / Élevé / Moyen / Faible / Très faible | idem (Ch91) | `Chaque proposition reçoit un indice de confiance: Très élevé, Élevé, Moyen, Faible, Très faible.` | VALIDATED |
| MR-109 | Quality Bias | Bien qualifié, géolocalisé, avec photos, récemment mis à jour → favorisé | idem (Ch17) | `Le moteur favorise: les biens complètement qualifiés, les biens géolocalisés, les biens avec photos, les biens récemment mis à jour.` | VALIDATED |

---

## 22. SCORE DÉTENTEUR

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-110 | Holder Score | Indice de fiabilité = temps moyen réponse × taux acceptation × visites honorées × transactions conclues | idem (Ch31) | `Temps moyen de réponse * Taux d'acceptation * Visites honorées * Transactions conclues → Indice de fiabilité.` | VALIDATED |

---

## 23. PONDÉRATIONS PAR TYPE DE BIEN (Chapitres 42-58)

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-111 | Property-Type Weights | Résidentiel simple: Type=20%, Op=10%, Ville/quartier=25%, Budget=25%, Douche/cuisine/meublé=10%, Dispo=5%, Qualité=5% | idem (Ch42) | Tableau de pondération complet | VALIDATED |
| MR-112 | Property-Type Weights | Appartement: Type=15%, Op=10%, Ville/quartier=20%, Budget=20%, Chambres=15%, Cuisine/douches=8%, Parking/balcon/étage=5%, Dispo=4%, Qualité=3% | idem (Ch43) | Tableau de pondération complet | VALIDATED |
| MR-113 | Property-Type Weights | Appartement meublé: Type=15%, Op=10%, Ville/quartier=18%, Budget=18%, Chambres=12%, Mobilier/équip=12%, Durée=5%, Dispo=5%, Qualité=5% | idem (Ch44) | Tableau de pondération complet | VALIDATED |
| MR-114 | Property-Type Weights | Maison: Type=15%, Op=10%, Ville/quartier=18%, Budget=18%, Chambres=15%, Cour/clôture=10%, Douches/cuisine=6%, Parking/forage/dép=5%, Qualité=3% | idem (Ch45) | Tableau de pondération complet | VALIDATED |
| MR-115 | Property-Type Weights | Villa: Type=12%, Op=8%, Ville/quartier=18%, Budget=17%, Chambres=15%, Cour/clôture/barrière=10%, Dépendance/garage=8%, Forage/sécu/groupe=5%, Piscine/jardin/confort=4%, Qualité=3% | idem (Ch46) | Tableau de pondération complet | VALIDATED |
| MR-116 | Property-Type Weights | Duplex: Type=15%, Op=8%, Ville/quartier=18%, Budget=17%, Chambres=12%, Deux niveaux=12%, Cour/parking/dép=8%, Équipements=5%, Qualité=5% | idem (Ch47) | Tableau de pondération complet | VALIDATED |
| MR-117 | Property-Type Weights | Immeuble/mini-cité: Type=15%, Ville/quartier=15%, Prix=15%, Unités=15%, Type d'unités=10%, Revenus=12%, Occupation=8%, Doc/titre=5%, Qualité=5% | idem (Ch48) | Tableau de pondération complet | VALIDATED |
| MR-118 | Property-Type Weights | Terrain résidentiel: Type=15%, Op=8%, Ville/zone=18%, Prix/budget=17%, Superficie=15%, Situation juridique=12%, Accès/axe=7%, Eau/élec=4%, GPS/bornage/qualité=4% | idem (Ch49) | Tableau de pondération complet | VALIDATED |
| MR-119 | Property-Type Weights | Terrain agricole: Type=15%, Localité=15%, Prix=15%, Superficie=20%, Situation juridique=12%, Activité=8%, Accès/eau/relief=8%, Qualité=7% | idem (Ch50) | Tableau de pondération complet | VALIDATED |
| MR-120 | Property-Type Weights | Terrain commercial/industriel: Type=15%, Zone/axe=18%, Prix=15%, Superficie=15%, Situation juridique=10%, Façade/visibilité=8%, Accès poids lourds=8%, Eau/élec=5%, Qualité=6% | idem (Ch51) | Tableau de pondération complet | VALIDATED |
| MR-121 | Property-Type Weights | Boutique/kiosque: Type=15%, Ville/quartier/marché=25%, Budget=20%, Surface=10%, Position commerciale=12%, Dispo=8%, Électricité/sécurité=5%, Qualité=5% | idem (Ch52) | Tableau de pondération complet | VALIDATED |
| MR-122 | Property-Type Weights | Bureau/cabinet: Type=15%, Ville/quartier=20%, Budget=20%, Surface=12%, Accessibilité=10%, Parking=8%, Internet/clim=5%, Étage/ascenseur=5%, Qualité=5% | idem (Ch53) | Tableau de pondération complet | VALIDATED |
| MR-123 | Property-Type Weights | Entrepôt/hangar: Type=15%, Zone=15%, Budget=15%, Surface=20%, Accès camion=12%, Hauteur/quai=8%, Sécurité/clôture=6%, Eau/élec=4%, Qualité=5% | idem (Ch54) | Tableau de pondération complet | VALIDATED |
| MR-124 | Property-Type Weights | Hôtel/auberge: Type=12%, Ville/quartier/axe=15%, Prix=15%, Chambres/unités=18%, État d'exploitation=10%, Taux occupation/revenus=10%, Parking/resto/services=8%, Doc/autorisations=5%, Qualité=7% | idem (Ch55) | Tableau de pondération complet | VALIDATED |
| MR-125 | Property-Type Weights | Biens agricoles: Type=15%, Localité=15%, Prix=15%, Superficie=20%, Activité=10%, Situation juridique=10%, Eau/accès/fertilité=8%, Équipements/bâtiments=4%, Qualité=3% | idem (Ch56) | Tableau de pondération complet | VALIDATED |
| MR-126 | Property-Type Weights | Biens industriels/logistiques: Type=15%, Zone indus/loc=15%, Prix=15%, Surface=18%, Accès poids lourds=12%, Énergie/eau=8%, État général=7%, Équipements techniques=5%, Qualité=5% | idem (Ch57) | Tableau de pondération complet | VALIDATED |
| MR-127 | Property-Type Weights | Biens mixtes/spéciaux: Usage principal=20%, Usage secondaire=8%, Ville/quartier=15%, Prix=15%, Surface=12%, Revenus/capacité=10%, Accessibilité=8%, Doc/autorisations=6%, Qualité=6% | idem (Ch58) | Tableau de pondération complet | VALIDATED |

---

## 24. MATCHING V4 ET V5 — COMPARAISON

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-128 | V4 Matching | Correspondance par ville, budget, status='available' | `LAWIMA/03_ENGINE/property_matcher/property_matcher_supabase.py` | `result = self.supabase.table("properties").select("*").eq("status", status).execute()` | VALIDATED |
| MR-129 | V5 Algorithm | Ordre: 1. Vérification ville 2. Budget tolérance 3. Type bien 4. Score total 5. Classement 6. Seuil 7. Limite 10 | `LAWIMA/03_ENGINE/property_matcher/property_matcher_v5.py` | Code complet match() method | VALIDATED |

---

## 25. REMATCHING

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-130 | Rematching | Déclenché quand: besoin corrigé, budget change, ville/quartier change, nouveau bien publié, bien indisponible, refus, visite/négociation | `LAWIM/Directive/04-MATCHING-REFERENCE.md` (Ch9) | Liste des événements déclencheurs | VALIDATED |
| MR-131 | Rematching | Relance automatique J+7 avec nouveaux biens | `MATCHING_ENGINE_PRISMA_GAP_REPORT.md`, `MATCHING_ENGINE_V1_IMPLEMENTATION_REPORT.md` | Concepts de rematching: relance auto J+7 | PARTIAL — J+7 mentionné dans rapports mais pas dans les directives officielles, à confirmer |
| MR-132 | Rematching | Ne repart jamais de zéro, enrichit l'historique | `LAWIM/Directive/04-DECISION-ENGINE-REFERENCE.md` (Ch64) | `Le rematching ne remet jamais le dossier à zéro. Il enrichit progressivement la qualité des propositions.` | VALIDATED |
| MR-133 | Rematching | Sélectif: recalcule uniquement les dossiers concernés | idem (Ch66) | `Le moteur ne recalcule jamais inutilement toute la base. Il identifie uniquement les dossiers concernés.` | VALIDATED |
| MR-134 | Rematching | Bien refusé définitivement → jamais reproposé (sauf exceptions) | idem (Ch71) | `Un bien définitivement refusé n'est jamais reproposé.` | VALIDATED |
| MR-135 | Rematching | Exceptions reproposition: baisse prix, modif majeure, changement besoin, demande explicite | idem | `Exceptions: baisse importante du prix, modification majeure, changement du besoin, demande explicite du demandeur.` | VALIDATED |

---

## 26. DIVERSITÉ DES PROPOSITIONS ET CLASSEMENT

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-136 | Ranking | Ordre décroissant de score | idem (Ch34) | `Tous les biens sont triés. Ordre décroissant.` | VALIDATED |
| MR-137 | Ranking | Priorité: 1. meilleure probabilité transaction 2. meilleure compatibilité 3. meilleure disponibilité 4. meilleur niveau documentaire 5. meilleure réactivité détenteur | idem (Ch76) | Liste de priorité des propositions | VALIDATED |
| MR-138 | Diversity | Évite de proposer plusieurs biens quasiment identiques | idem (Ch77) | `Le moteur évite de proposer plusieurs biens quasiment identiques. Trois appartements dans le même immeuble → le moteur en présente un seul en priorité.` | VALIDATED |
| MR-139 | Explainability | Top 3 critères doivent être expliqués pour chaque proposition | idem (Ch60) | `Le moteur doit pouvoir expliquer les trois premiers critères ayant le plus influencé chaque proposition.` | VALIDATED |

---

## 27. RÈGLES DE NON-COMPENSATION

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-140 | Non-Compensation | Terrain bien situé ne compense pas recherche de villa | idem (Ch61) | `Un terrain très bien situé ne compense jamais le fait que l'utilisateur cherche une villa.` | VALIDATED |
| MR-141 | Non-Compensation | Piscine ne compense pas budget incompatible | idem | `Une villa avec piscine ne compense jamais un budget totalement incompatible.` | VALIDATED |
| MR-142 | Non-Compensation | Hôtel rentable ne compense pas absence disponibilité vente | idem | `Un hôtel très rentable ne compense jamais l'absence de disponibilité à la vente si l'opération demandée est achat.` | VALIDATED |

---

## 28. RÈGLES ABSOLUES / INTERDICTIONS

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-143 | Absolute Rules | Ne jamais: proposer bien incompatible, bien vendu, deux fois même bien après refus définitif, ignorer préférences apprises, recalculer inutilement | idem (Ch38) | `Le moteur ne doit jamais: proposer un bien incompatible, proposer un bien vendu, proposer deux fois le même bien après un refus définitif, ignorer les préférences apprises, recalculer inutilement les scores.` | VALIDATED |
| MR-144 | Absolute Rules | Ne jamais: favoriser partenaire au détriment demandeur, masquer information, ignorer cycle de vie, décision sans justification | idem (Ch99) | `Il ne doit jamais: privilégier un partenaire au détriment du demandeur, masquer une information importante, proposer un bien incompatible, ignorer le cycle de vie d'un bien, prendre une décision sans justification métier.` | VALIDATED |

---

## 29. MATRICE DE DÉCISION (Decision Engine — Ch87)

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-145 | Decision Matrix | Flux décisionnel: champs critiques manquants → Question / Matching impossible → Qualification / Matching disponible → Calcul scores / Excellent bien → Présentation / Bien accepté → Contact détenteur / Double accord → Visite / Visite réussie → Négociation / Accord → Transaction / Terminée → Clôture | idem (Ch87) | Schéma complet du flux décisionnel | VALIDATED |

---

## 30. PRIORITÉ DES ACTIONS (Decision Engine — Ch88)

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-146 | Action Priority | 1. Corriger incohérence 2. Compléter champ critique 3. Matching 4. Présenter bien 5. Contacter détenteur 6. Visite 7. Relance 8. Notifications 9. Optimisation dossier | idem (Ch88) | Tableau des priorités d'action | VALIDATED |

---

## 31. DÉTECTION OPPORTUNITÉS ET RISQUES

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-147 | Opportunity Detection | Baisse prix, nouveau bien compatible, retour disponibilité, amélioration doc/dossier | idem (Ch93) | `Baisse importante du prix, nouveau bien très compatible, retour en disponibilité, amélioration documentaire, amélioration du score.` | VALIDATED |
| MR-148 | Risk Detection | Propriétaire inactif, délais anormaux, documents incomplets, prix incohérent, bien ancien sans activité | idem (Ch94) | `Propriétaire inactif, délais anormaux, documents incomplets, prix incohérent, bien ancien sans activité.` | VALIDATED |

---

## 32. APPRENTISSAGE GLOBAL ET MÉMOIRE MARCHÉ

| KNOWLEDGE_ID | CONCEPT | DESCRIPTION | SOURCE_FILE | EXCERPT | CONFIDENCE |
|---|---|---|---|---|---|
| MR-149 | Market Memory | Délai moyen vente/location par ville, durée avant 1ère visite, quartiers demandés, types de biens recherchés, saisonnalité | idem (Ch95) | `LAWIM construit progressivement une connaissance du marché: délai moyen de vente par ville, délai moyen de location, durée moyenne avant première visite, quartiers les plus demandés, types de biens les plus recherchés, saisonnalité.` | VALIDATED |
| MR-150 | Tension Index | Indice de tension par ville+quartier+type+opération (ex: 95% = très tendu, 25% = détendu) | idem (Ch96) | `Pour chaque combinaison Ville/Quartier/Type de bien/Opération, LAWIM calcule un indice de tension.` | VALIDATED |

---

## SYNTHÈSE STATISTIQUE

| Métrique | Valeur |
|----------|--------|
| **Total KNOWLEDGE_ID** | **150** |
| ✅ **VALIDATED** | **148** |
| ⚠️ **PARTIAL** | **2** (MR-043 seuil 25% vs 60%, MR-131 J+7 non confirmé dans directive officielle) |
| ❌ **NON_VALIDE** | **0** |
| **Sources uniques** | **11 fichiers sur 3 branches** |

### Écarts identifiés

| ID | Problème | Gravité |
|----|----------|---------|
| MR-043 | Seuil de rejet à 25% (Ch92) vs 60% (Ch26) — incohérence interne dans 04-DECISION-ENGINE-REFERENCE.md. 60% est le seuil documenté dans les 3 sources (V1 json, Ch26, V5 code), 25% semble être un seuil de "conservation en attente" et non de proposition. | FAIBLE — 25% est un seuil de "ne jamais proposer" dans le contexte du Decision Engine (action immédiate), pas le seuil minimum de matching |
| MR-131 | J+7 mentionné dans les rapports de gap/implémentation mais pas dans les directives officielles (04-MATCHING-REFERENCE.md, 04-DECISION-ENGINE-REFERENCE.md). Les directives listent des déclencheurs d'événements sans période fixe de J+7. | MOYEN — La périodicité J+7 n'est pas officialisée dans les directives |

### Notes de consolidation

1. **Deux systèmes de poids co-existent**: V1 (property_matching_v1.json: 5 dimensions) et le Decision Engine (Ch26: 6 dimensions, Ch90: 8 indicateurs). Ce ne sont pas contradictoires mais opèrent à des niveaux différents: V1 est le modèle simple de matching, le DE est le modèle décisionnel avancé.

2. **lead_classifier_v1.json** donne des `base_score` par type de lead; **lead_scoring.json** donne des scores par `user_type` avec des critères supplémentaires (budget_min, urgency). Les deux systèmes sont complémentaires mais non alignés (ex: tenant=40 vs 40, buyer=60 vs 95 avec budget≥50M).

3. **lead_scoring_rules.json** (poids: budget=20, location=15, urgency=20, ...) semble être un système tiers de scoring — pas directement relié au matching des biens mais au scoring des leads entrants.

4. **04-MATCHING-REFERENCE.md** (Directive) et **04-DECISION-ENGINE-REFERENCE.md** sont structurellement le même document (même en-tête "04-MATCHING-REFERENCE.md") mais la version DECISION-ENGINE est plus complète avec 6 parties vs 16 chapitres dans MATCHING-REFERENCE. Le Decision Engine inclut et étend le Matching Reference.

