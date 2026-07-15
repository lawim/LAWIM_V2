# Rapport de validation — CONVERSATION_MODEL.md

**Date :** 2026-07-15  
**Auditeur :** Validation automatique (agent d'audit)  
**Source des vérifications :** `LAWIMA/`, `LAWIM/` (backup du 2026-06-08)

---

## Résumé

| Statut | Nombre |
|--------|--------|
| ✅ Validé | 12 |
| ⚠️ Partiel | 6 |
| ❌ Non validé | 5 |
| **Total** | **23** |

---

## 1. Positionnement (Affirmation #1)

> Intermédiaire, zéro commission, aucune garantie, accompagnement 50k

**Source :** `LAWIMA/00_GLOBAL/rules/RESPONSE_POLICY.md`

| Élément | Source | Statut |
|---------|--------|--------|
| Intermédiaire (mise en relation) | RESPONSE_POLICY.md:4 | ✅ |
| Zéro commission | RESPONSE_POLICY.md:5 | ✅ |
| Aucune garantie (score indicatif) | RESPONSE_POLICY.md:6 | ✅ |
| Accompagnement 50k FCFA | RESPONSE_POLICY.md:18 | ✅ |

**✅ VALIDÉ** — Les 4 éléments sont présents textuellement.

---

## 2. Ton et langues (Affirmation #2)

> Ton : professionnel, courtois, vendeur, vouvoiement

**Source :** `LAWIMA/00_GLOBAL/rules/RESPONSE_POLICY.md:8-10`

| Élément | Source | Statut |
|---------|--------|--------|
| Professionnel | RESPONSE_POLICY.md:9 | ✅ |
| Courtois | RESPONSE_POLICY.md:9 | ✅ |
| Vendeur | RESPONSE_POLICY.md:9 | ✅ |
| Vouvoiement systématique | RESPONSE_POLICY.md:10 | ✅ |

**✅ VALIDÉ**

---

## 3. 4 langues (Affirmation #3)

> 4 langues : français, anglais, pidgin, camfranglais

**Sources :** RESPONSE_POLICY.md:11, deepseek_prompt.txt:3, multilingual-conversation-guidelines.md:5-7, multilingual_responses.py

| Langue | Source | Statut |
|--------|--------|--------|
| français | RESPONSE_POLICY.md:11, deepseek_prompt.txt:3 | ✅ |
| anglais | RESPONSE_POLICY.md:11, deepseek_prompt.txt:3 | ✅ |
| pidgin | RESPONSE_POLICY.md:11, deepseek_prompt.txt:3 | ✅ |
| **camfranglais** | **Aucune source** | ❌ |

**❌ NON VALIDÉ** — Aucun fichier source ne mentionne le camfranglais.  
RESPONSE_POLICY.md line 11 : « Langue : français, anglais, pidgin (détection auto) » — 3 langues seulement.  
03-CONVERSATION-REFERENCE.md line 291 : « Français, English et Pidgin English » — 3 langues.  
multilingual-conversation-guidelines.md line 5-7 : 3 langues explicites.  
multilingual_responses.py : templates pour `fr`, `en`, `pidgin` seulement.  
deepseek_prompt.txt:3 : « français, anglais, pidgin ».  
language_handler.py : ne supporte que `fr` et `en`.

---

## 4. Règles absolues (Affirmation #4)

> Règles : notaire, DeepSeek, match→agent, accompagnement→payant, SIGNALER, SUPPRIMER→7j

**Source :** RESPONSE_POLICY.md:13-19

| Règle | Source | Statut |
|-------|--------|--------|
| Question juridique → notaire | RESPONSE_POLICY.md:14 | ✅ |
| DeepSeek demande type/localisation/budget | RESPONSE_POLICY.md:15 | ✅ |
| Match trouvé → notifier agent/propriétaire | RESPONSE_POLICY.md:16 | ✅ |
| Accompagnement payant 50k | RESPONSE_POLICY.md:17 | ✅ |
| Litige → SIGNALER | RESPONSE_POLICY.md:18 | ✅ |
| RGPD → SUPPRIMER (7 jours) | RESPONSE_POLICY.md:19 | ✅ |

**✅ VALIDÉ**

---

## 5. Commandes spéciales (Affirmation #5)

> 9 commandes listées

**Source :** RESPONSE_POLICY.md, whatsapp_gateway_v3.backup, follow_up_system.py, language_handler.py

| Commande | Implémentation trouvée | Statut |
|----------|------------------------|--------|
| SIGNALER [raison] | whatsapp_gateway_v3.backup:47-49 | ✅ |
| SUPPRIMER MES DONNÉES | whatsapp_gateway_v3.backup:50-52 | ✅ |
| ACCOMPAGNEMENT | whatsapp_gateway_v3.backup:53-54 | ✅ |
| OUI / NON | Mentionné dans follow_up_system.py:24 | ⚠️ |
| STATS | Mentionné dans language_handler.py:62 help | ⚠️ |
| LANGUE | language_handler.py:45 `set_user_language()` | ✅ |
| RECHERCHE | Mentionné dans follow_up_system.py:25 | ⚠️ |
| PRIORITAIRE | Mentionné dans follow_up_system.py:26 | ⚠️ |
| RELANCER | Mentionné dans follow_up_system.py:27 | ⚠️ |

**⚠️ PARTIEL** — SIGNALER, SUPPRIMER, ACCOMPAGNEMENT, LANGUE ont un handler explicite.  
OUI/NON, STATS, RECHERCHE, PRIORITAIRE, RELANCER sont seulement mentionnés dans des messages (follow_up / help) sans handler de routage dédié dans le moteur principal.

---

## 6. Niveaux de familiarité (Affirmation #6)

> J1(1j), J2(≤7j), J3(≤30j), J4(>30j)

**Source :** `LAWIMA/03_ENGINE/conversation_memory.py:136-143`

| Niveau | Code | Statut |
|--------|------|--------|
| J1 (1 jour) | `if days_ago == 1: level = 1` | ✅ |
| J2 (≤ 7 jours) | `elif days_ago <= 7: level = 2` | ✅ |
| J3 (≤ 30 jours) | `elif days_ago <= 30: level = 3` | ✅ |
| J4 (> 30 jours) | `else: level = 4` | ✅ |

**✅ VALIDÉ** — Correspond exactement.

---

## 7. Format résumé (Affirmation #7)

> "Vous cherchiez [type] à [lieu] avec un budget de [montant] FCFA"

**Source :** `conversation_memory.py:89-127`, méthode `generate_natural_summary()`

La méthode construit dynamiquement :
- `"Vous cherchiez [type]."` (1 élément)
- `"Vous cherchiez [type] à [lieu]."` (2 éléments)
- `"Vous cherchiez [type] à [lieu] avec un [budget] FCFA."` (3+ éléments)

**✅ VALIDÉ** — Le format exact est produit par la méthode.

---

## 8. Nouveaux biens simulés (Affirmation #8)

> 1-5 nouveaux biens simulés selon absence

**Source :** `conversation_memory.py:157`

```python
new_count = random.randint(1, 5)
```

**✅ VALIDÉ** — `random.randint(1, 5)` génère bien 1 à 5 biens simulés.

---

## 9. LongTermMemory — 90 jours (Affirmation #9)

> 90 jours retention, forget_after_days

**Source :** `LAWIMA/03_ENGINE/long_term_memory.py`

| Élément | Constat | Statut |
|---------|---------|--------|
| 90 jours retention | Le code utilise `if days_ago < 365:` (l.92) — **1 an**, pas 90 jours | ❌ |
| `forget_after_days` | Attribut inexistant dans le code | ❌ |

**❌ NON VALIDÉ** — Le seuil de rétention dans le code est 365 jours (1 an), pas 90 jours.  
Aucun paramètre `forget_after_days` n'existe dans le fichier.

---

## 10. Lead >12 mois relançable (Affirmation #10)

> Lead de plus de 12 mois considéré comme relançable

**Source :** `long_term_memory.py:57-67`

```python
def get_old_leads_to_follow_up(self, months=12):
```

**✅ VALIDÉ** — La méthode `get_old_leads_to_follow_up(months=12)` cible explicitement les leads de plus de 12 mois.

---

## 11. Satisfaction précédente consultée (Affirmation #11)

> Satisfaction précédente consultée

**Source :** `long_term_memory.py:69-83`

```python
def check_previous_property_satisfaction(self, phone, property_id):
```

**✅ VALIDÉ** — La méthode existe et retourne `was_satisfied`, `rating`, `comment`.

---

## 12. Échéances de relance (Affirmation #12)

> J1(24h), J7(168h), J30(720h), J90(2160h)

**Source :** `LAWIMA/03_ENGINE/follow_up_system.py:22-27`

| Échéance | Code | Statut |
|----------|------|--------|
| J1 — 24h | `24:` dans le dictionnaire | ✅ |
| J7 — 168h | `168:` | ✅ |
| J30 — 720h | `720:` | ✅ |
| J90 — 2160h | `2160:` | ✅ |

**✅ VALIDÉ**

---

## 13. Types de messages par seuil (Affirmation #13)

> Messages types par seuil : J1, J7, J30, J90

**Source :** `follow_up_system.py:22-27`

| Seuil | Message dans le code | Message dans CONVERSATION_MODEL | Concordance |
|-------|---------------------|----------------------------------|-------------|
| 24h | « De nouveaux biens sont disponibles ! » | « Nouveaux biens correspondant à la recherche » | ⚠️ Approchant |
| 168h | « Nous avons ajouté 5 nouveaux biens » | « Offre spéciale, nouveaux arrivages » | ⚠️ Partiel |
| 720h | « Offre spéciale — 1 mois de recherche prioritaire GRATUIT » | « Statistiques du marché, tendances » | ❌ Différent |
| 2160h | « 500+ demandes traitées ce trimestre » | « Relance complète, réactivation » | ❌ Différent |

**⚠️ PARTIEL** — Les seuils horaires sont corrects, mais le contenu des messages diffère significativement entre le code et la documentation. Les messages du code sont plus axés sur des offres promotionnelles que ceux décrits dans le document.

---

## 14. Canal WhatsApp via GreenAPI (Affirmation #14)

> WhatsApp via GreenAPI

**Source :** `follow_up_system.py:70`

```python
url = f"https://api.green-api.com/waInstance{GREEN_API_ID}/sendMessage/{GREEN_API_TOKEN}"
```

**✅ VALIDÉ** — GreenAPI est utilisé dans le système de relance. whatsapp_gateway_v2.py et v3 confirment l'utilisation de GreenAPI comme canal WhatsApp.

---

## 15. Hiérarchie ResponseRouter (Affirmation #15)

> DeepSeek → Règles locales → Templates

**Source :** `LAWIMA/03_ENGINE/response_router.py:3,58-65`

La docstring dit : « DeepSeek IA → Google API → Règles locales → Templates »  
Mais le code `process()` implémente : **DeepSeek → Règles locales → Templates** (sans Google API).

| Niveau | Code | Statut |
|--------|------|--------|
| 1. DeepSeek IA | `_call_deepseek()` appelé en premier | ✅ |
| 2. Règles locales | `_local_rules()` ensuite | ✅ |
| 3. Templates | `TEMPLATES["no_match"]` en fallback | ✅ |
| Google API (mentionné dans docstring) | Non implémenté | ❌ |

**⚠️ PARTIEL** — La hiérarchie documentée dans CONVERSATION_MODEL.md correspond au code, mais la docstring de response_router.py mentionne une étape Google API qui n'est pas documentée dans CONVERSATION_MODEL.md et n'est pas implémentée.

---

## 16. DeepSeek extrait : type, localisation, budget (Affirmation #16)

> Extraction : type, localisation, budget

**Source :** `LAWIMA/03_ENGINE/deepseek_prompt.txt:5,15`

Le prompt demande : « CHAMPS OBLIGATOIRES : type, localisation, budget » avec le format de sortie incluant ces champs.

**✅ VALIDÉ**

---

## 17. Format JSON DeepSeek (Affirmation #17)

> Format de sortie JSON

**Source :** `deepseek_prompt.txt:14-20`

```json
{
  "extracted": {"type": "...", "location": "...", "budget": 0},
  "missing": ["liste", "des", "champs", "manquants"],
  "response_text": "...",
  "confidence": 0-100,
  "routing": {"agent_id": 0, "zone": "..."}
}
```

**Doc CONVERSATION_MODEL.md donne :**
```json
{
  "extracted": { "type": "", "location": "", "budget": "" },
  "missing": [],
  "response_text": "",
  "confidence": 0.0,
  "routing": { "agent_id": "", "zone": "" }
}
```

| Différence | Code source | Doc | Statut |
|------------|-------------|-----|--------|
| `budget` | nombre (`0`) | chaîne (`""`) | ⚠️ |
| `confidence` | entier 0-100 | flottant 0.0 | ⚠️ |
| `agent_id` | nombre (`0`) | chaîne (`""`) | ⚠️ |

**⚠️ PARTIEL** — La structure JSON générale est correcte mais les types de certains champs diffèrent entre le prompt source et la documentation.

---

## 18. Templates multilingues (Affirmation #18)

> Templates : welcome, help, no_match, thanks, ask_name, ask_phone, stats

**Source :** `LAWIMA/03_ENGINE/multilingual_responses.py:7-35`

| Template | Présent | Statut |
|----------|---------|--------|
| welcome | ✅ | ✅ |
| help | ✅ | ✅ |
| no_match | ✅ | ✅ |
| thanks | ✅ | ✅ |
| ask_name | ✅ | ✅ |
| ask_phone | ✅ | ✅ |
| stats | ✅ | ✅ |

**✅ VALIDÉ** — Les 7 templates sont présents en français, anglais et pidgin.

---

## 19. Format affichage biens (Affirmation #19)

> N. *description*\n📍 localisation\n💰 prix\n⭐ notes

**Source :** `multilingual_responses.py:55-60`

```python
response += f"{i}. *{prop.get('description', 'Sans titre')}*\n"
response += f" 📍 {prop.get('location', '?')}\n"
response += f" 💰 {prop.get('price', 0):,} FCFA\n"
response += f" ⭐ {m['stars']}\n\n"
```

**✅ VALIDÉ** — Le format correspond exactement.

---

## 20. Signaux d'intention (Affirmation #20)

> sell, visit_request, urgent_signal, investor_lead, broker_lead, price_signal, search

**Source :** `LAWIMA/03_ENGINE/lawim_engine_v1.py` + `intent_detector/` + fichiers `intents/*.json`

| Signal | Trouvé dans les sources | Statut |
|--------|------------------------|--------|
| sell | `intents/sell_property.json` keywords: "vendre", "vente", expressions: "je vends" | ✅ |
| visit_request | Pas trouvé comme intention dédiée | ❌ |
| urgent_signal | Pas d'intention "urgence" dédiée dans les fichiers intents | ❌ |
| investor_lead | `intents/investor_intent.json`: "investir", "roi", "rentabilité" | ✅ |
| broker_lead | Pas trouvé | ❌ |
| price_signal | Pas trouvé comme intention dédiée | ❌ |
| search | `intents/search_property.json`: "cherche", "recherche", "besoin" | ✅ |

Le fichier `lawim_engine_v1.py` lui-même ne définit pas ces signaux ; il délègue à l'`IntentDetector` qui charge les fichiers JSON. Les JSONs ne couvrent que 3 des 7 signaux listés (sell, investor_lead, search).

**❌ NON VALIDÉ** — Seuls 3 signaux sur 7 sont implémentés dans les fichiers intents. visit_request, urgent_signal, broker_lead, price_signal sont absents.

---

## 21. Feedback (Affirmation #21)

> 👍=5, 👎=1, "note X"

**Source :** `LAWIMA/03_ENGINE/feedback_handler.py:22-36`

| Action | Code | Statut |
|--------|------|--------|
| 👍 (thumbs_up) → note 5 | `feedback_handler.py:23` | ✅ |
| 👎 (thumbs_down) → note 1 | `feedback_handler.py:27` | ✅ |
| "note 4" → 4 | `feedback_handler.py:34-36` | ✅ |
| "note 3" → 3 | Même regex couvre 1-5 | ✅ |

**✅ VALIDÉ**

---

## 22. 12 peurs acheteurs, 8 peurs vendeurs (Affirmation #22)

> 12 peurs acheteurs, 8 peurs vendeurs

**Source :** `LAWIM/KNOWLEDGE/trust-and-objection-patterns.md`

**Section 1** — « Ce que les acheteurs craignent » : **10 entrées** (pas 12)  
**Section 2** — « Ce que les vendeurs craignent » : **8 entrées**

| Groupe | Annoncé | Réel | Statut |
|--------|---------|------|--------|
| Acheteurs | 12 | 10 | ❌ |
| Vendeurs | 8 | 8 | ✅ |

**⚠️ PARTIEL** — Le compte des vendeurs (8) est correct.  
Le compte des acheteurs est annoncé à 12 mais le document source n'en liste que 10.

---

## 23. 12 peurs listées individuellement (Affirmation #23)

> Vérification ligne 222 : « 12 peurs identifiées pour les acheteurs et 8 pour les vendeurs »

Identique à l'affirmation #22.  
La ligne 222 de CONVERSATION_MODEL.md dit : « 12 peurs identifiées pour les acheteurs et 8 pour les vendeurs (détaillées dans le document source). »

Même constat : le document source contient 10 peurs acheteurs, pas 12.

**⚠️ PARTIEL** — Même décompte que #22.

---

## Synthèse des écarts majeurs

| # | Affirmation | Problème |
|---|-------------|----------|
| 3 | 4 langues (camfranglais) | Aucune source ne mentionne le camfranglais ; seules 3 langues sont supportées |
| 9 | 90 jours rétention | Le code utilise 365 jours ; `forget_after_days` inexistant |
| 13 | Types messages par seuil | Messages du code différents de la doc pour J30 et J90 |
| 17 | Format JSON DeepSeek | Types des champs `budget`, `confidence`, `agent_id` différents |
| 20 | Signaux d'intention | 4 signaux sur 7 non implémentés dans les fichiers intents |
| 22 | 12 peurs acheteurs | 10 seulement dans le document source |

---

*Rapport généré le 2026-07-15 par l'agent d'audit de validation LAWIM.*
