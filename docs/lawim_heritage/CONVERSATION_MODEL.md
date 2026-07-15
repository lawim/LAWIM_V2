# CONVERSATION MODEL — Modèle de conversation LAWIM

**Sources :** LAWIM `Directive/03-CONVERSATION-REFERENCE.md`, LAWIMA `00_GLOBAL/rules/RESPONSE_POLICY.md`, `03_ENGINE/conversation_memory.py`, `03_ENGINE/long_term_memory.py`, `03_ENGINE/follow_up_system.py`, `03_ENGINE/response_router.py`, `03_ENGINE/multilingual_responses.py`, `03_ENGINE/feedback_handler.py`, `03_ENGINE/deepseek_prompt.txt`, LAWIM `KNOWLEDGE/conversation-patterns.md`, `conversation-style-guide.md`, `multilingual-conversation-guidelines.md`, `omnichannel-playbook.md`
**Principe :** Documentation exhaustive des règles de dialogue

---

## 1. Politique de réponse

**Source :** LAWIMA `00_GLOBAL/rules/RESPONSE_POLICY.md`, LAWIM `KNOWLEDGE/response-policy.md`

### 1.1 Positionnement
- LAWIM est un **intermédiaire** de mise en relation
- **Zéro commission** sur les transactions
- **Aucune garantie** sur les biens (score indicatif seulement)
- Accompagnement payant disponible : 50 000 FCFA

### 1.2 Ton et langues
- Ton : professionnel, courtois, vendeur
- Vouvoiement systématique
- 4 langues supportées : français, anglais, pidgin, camfranglais
- Détection automatique de la langue

### 1.3 Règles absolues (non-négociables)

| Règle | Action |
|-------|--------|
| Question juridique | Orienter vers un notaire |
| Champ manquant | DeepSeek demande type/localisation/budget |
| Match trouvé | Notifier agent/propriétaire |
| Demande accompagnement | Activer service payant (50k FCFA) |
| Litige | Activer commande `SIGNALER` |
| Demande RGPD | Activer commande `SUPPRIMER MES DONNÉES` (délai 7 jours) |

## 2. Commandes spéciales utilisateur

**Source :** LAWIMA `03_ENGINE/lawim_engine_v1.py`, `RESPONSE_POLICY.md`

| Commande | Action |
|----------|--------|
| `SIGNALER [raison]` | Crée un litige dans la table disputes |
| `SUPPRIMER MES DONNÉES` | Anonymise la personne (RGPD, 7 jours) |
| `ACCOMPAGNEMENT` | Active le service payant |
| `OUI` / `NON` | Réponse à la demande de permission |
| `STATS` | Affiche les performances (agents) |
| `LANGUE` | Change la langue de conversation |
| `RECHERCHE` | Voir les nouveaux biens (relance J7) |
| `PRIORITAIRE` | Active la recherche prioritaire (relance J30) |
| `RELANCER` | Reprendre la recherche (relance J90) |

## 3. Gestion de la mémoire

### 3.1 ConversationMemory

**Source :** LAWIMA `03_ENGINE/conversation_memory.py`

#### Niveaux de familiarité
| Délai de retour | Niveau | Comportement |
|-----------------|--------|--------------|
| 1 jour | J1 | Message de suivi léger |
| ≤ 7 jours | J2 | Message de rappel |
| ≤ 30 jours | J3 | Message de relance |
| > 30 jours | J4 | Message de reprise complet |

#### Banque de phrases
- Phrases d'accueil (plusieurs variantes, choix aléatoire)
- Résumé de la recherche précédente
- Phrase de transition
- Question finale

#### Format de résumé
"Vous cherchiez [type] à [lieu] avec un budget de [montant] FCFA"

#### Nouveaux biens simulés
- 1 à 5 nouveaux biens selon la durée d'absence
- Intègre une vérification de disponibilité

### 3.2 LongTermMemory

**Source :** LAWIMA `03_ENGINE/long_term_memory.py`

- Durée de rétention : 90 jours (configurable dans `forget_after_days`)
- Rappel de la recherche précédente avec contexte temporel
- Lead de plus de 12 mois considéré comme relançable
- Satisfaction précédente consultée pour les recommandations
- Stockage des historiques de recherche par utilisateur
- Reconnaissance multi-session

## 4. Système de relance

**Source :** LAWIMA `03_ENGINE/follow_up_system.py`

### 4.1 Échéances de relance

| Échéance | Délai | Message |
|----------|-------|---------|
| J1 | 24h | Nouveaux biens correspondant à la recherche |
| J7 | 168h | Offre spéciale, nouveaux arrivages |
| J30 | 720h | Statistiques du marché, tendances |
| J90 | 2160h | Relance complète, réactivation |

### 4.2 Types de messages par seuil
- J1 : "J'ai trouvé [N] nouveaux biens qui pourraient vous intéresser..."
- J7 : "Offre spéciale cette semaine sur [type] à [ville]..."
- J30 : "Voici les tendances du marché immobilier à [ville]..."
- J90 : "Souhaitez-vous relancer votre recherche ?"

### 4.3 Canal de relance
- WhatsApp via GreenAPI

## 5. Gestion des réponses

### 5.1 Hiérarchie ResponseRouter

**Source :** LAWIMA `03_ENGINE/response_router.py`

1. **DeepSeek IA** (analyse + génération de réponse intelligente)
2. **Règles locales** (bonjour, merci, aide — réponses pré-définies)
3. **Templates** (messages standards)

### 5.2 DeepSeek Prompt

**Source :** LAWIMA `03_ENGINE/deepseek_prompt.txt`

Le prompt DeepSeek extrait :
- Type de bien
- Localisation
- Budget

Format de sortie JSON :
```json
{
  "extracted": { "type": "", "location": "", "budget": "" },
  "missing": [],
  "response_text": "",
  "confidence": 0.0,
  "routing": { "agent_id": "", "zone": "" }
}
```

### 5.3 Templates de réponse multilingues

**Source :** LAWIMA `03_ENGINE/multilingual_responses.py`

Templates disponibles en français, anglais et pidgin :
- **welcome** : Message de bienvenue
- **help** : Message d'aide
- **no_match** : Aucun résultat trouvé (inclut la requête)
- **thanks** : Remerciement
- **ask_name** : Demande du nom
- **ask_phone** : Demande du téléphone
- **stats** : Statistiques (leads, acceptés, conversion, note/5)

Format d'affichage des biens :
```
N. *description*
📍 localisation
💰 prix FCFA
⭐ notes
```

## 6. Détection des intentions dans la conversation

**Source :** LAWIMA `03_ENGINE/lawim_engine_v1.py`

### 6.1 Signaux d'intention supplémentaires

| Signal | Mots-clés |
|--------|-----------|
| sell | j'ai, je vends, proprio, available, for sale |
| visit_request | visite, voir, visit, on passe, check |
| urgent_signal | urgent, asap, vite, rapidement, now |
| investor_lead | investir, rentable, ROI, cash flow |
| broker_lead | je peux trouver, j'ai un contact |
| price_signal | prix, budget, max, k, mille |
| search | je cherche, i need, looking for, besoin, recherche |

## 7. Feedback utilisateur

**Source :** LAWIMA `03_ENGINE/feedback_handler.py`

| Action | Interprétation |
|--------|----------------|
| 👍 (emoji) | thumbs_up → note 5 |
| 👎 (emoji) | thumbs_down → note 1 |
| "note 4" | Note sur 5 |
| "note 3" | Note sur 5 |

Détection dans `whatsapp_logs` (messages WhatsApp).

## 8. Qualification par canal

**Source :** LAWIM `KNOWLEDGE/channels/whatsapp-telegram-dashboard-qualification.md`

Règles de qualification spécifiques selon le canal d'entrée. Document source pour les détails.

## 9. Règles de dialogue avancées

**Source :** LAWIM `KNOWLEDGE/conversation-patterns.md`

Patterns de conversation documentés :
- Gestion des corrections ("non, je parlais de...")
- Changement de sujet
- Reformulations
- Règles d'arrêt (quand arrêter de qualifier)
- Règles d'escalade (quand passer à un humain)

## 10. Style guide

**Source :** LAWIM `KNOWLEDGE/conversation-style-guide.md`

Directives de style pour les conversations IA :
- Langage naturel et humain
- Éviter les réponses robotiques
- Adapter le ton au profil de l'utilisateur
- Utiliser des expressions locales appropriées

## 11. Gestion des objections

**Source :** LAWIM `KNOWLEDGE/trust-and-objection-patterns.md`

12 peurs identifiées pour les acheteurs et 8 pour les vendeurs (détaillées dans le document source).

## 12. Omnicanal

**Source :** LAWIM `KNOWLEDGE/omnichannel-playbook.md`

Stratégie de communication omnicanale : WhatsApp comme canal principal, Telegram, Facebook, Dashboard comme canaux secondaires.

---

*Document patrimonial — Aucune décision de reconstruction n'est prise ici.*
