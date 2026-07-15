# CONVERSATION MODEL — Modèle de conversation (Gold Standard)

**Mission :** LAWIM Heritage Gold
**Statut :** Validé — Toute reconstruction doit respecter ce modèle.
**Principe :** Modèle exhaustif et validé de dialogue LAWIM.

**Sources :** `Directive/03-CONVERSATION-REFERENCE.md`, `RESPONSE_POLICY.md`, `conversation_memory.py`, `long_term_memory.py`, `follow_up_system.py`, `response_router.py`, `multilingual_responses.py`, `omnichannel-playbook.md`, `conversation-patterns.md`, `conversation-style-guide.md`, `multilingual-conversation-guidelines.md`

---

## 1. Principes directeurs (10)

Issus de `Directive/03-CONVERSATION-REFERENCE.md` :

| # | Principe | Description |
|:-:|----------|-------------|
| 1 | **Positionnement intermédiaire** | LAWIM est un intermédiaire de mise en relation, pas un agent immobilier |
| 2 | **Zéro commission** | Aucune commission sur les transactions |
| 3 | **Ton professionnel** | Courtois, vendeur, vouvoiement systématique |
| 4 | **Langage naturel** | Éviter les réponses robotiques, adapter le ton au profil |
| 5 | **Progressive disclosure** | Une question par message (WhatsApp), 2-3 champs max (Telegram) |
| 6 | **Double consentement** | Ne jamais partager les coordonnées sans accord explicite des deux parties |
| 7 | **Anonymisation** | Anonymiser les utilisateurs qui le demandent (RGPD, délai 7 jours) |
| 8 | **Détection automatique** | Détecter automatiquement la langue et l'intention |
| 9 | **Correction prioritaire** | Toute correction utilisateur écrase le contexte précédent |
| 10 | **Non-redémarrage** | Ne jamais recommencer une conversation depuis le début |

---

## 2. Canaux supportés (6)

| Canal | Statut | Particularités |
|-------|--------|----------------|
| **WhatsApp** | Principal | 1 question/message, GreenAPI, logs `whatsapp_logs` |
| **Telegram** | Secondaire | 2-3 champs/message, plus flexibles |
| **Dashboard** | Back-office | Qualification manuelle, suivi CRM |
| **Facebook Messenger** | Secondaire | Qualification simplifiée |
| **SMS** | Secondaire | Messages courts, qualification minimale |
| **Appel vocal** | Manuel | Escalade humaine uniquement |

### 2.1 Ton par canal

| Canal | Ton | Longueur |
|-------|-----|----------|
| WhatsApp | Professionnel, concis | 1-2 phrases |
| Telegram | Décontracté, direct | 2-3 champs |
| Dashboard | Formel, structuré | Complet |

---

## 3. Interactions moteur (4)

| Moteur | Rôle | Interaction |
|--------|------|-------------|
| **DeepSeek AI** | Analyse intelligente, extraction, génération | Prompt contextuel, sortie JSON structurée |
| **Moteur de règles** | Règles locales (bonjour, merci, aide) | Réponses pré-définies, templates |
| **Moteur de qualification** | Scoring, classification, routage | Pipeline 8 étapes V5 |
| **Moteur CRM** | Suivi leads, relances, routage agents | Tables leads, agents, files d'attente |

---

## 4. Double consentement

| Principe | Règle |
|----------|-------|
| **Partage de coordonnées** | Ne jamais partager téléphone, email ou adresse sans consentement explicite des deux parties |
| **Mise en relation** | Demander au demandeur : "Puis-je partager vos coordonnées avec le propriétaire/agent ?" |
| **RGPD** | Commande `SUPPRIMER MES DONNÉES` → anonymisation sous 7 jours |

---

## 5. Anonymat

| Règle | Description |
|-------|-------------|
| Anonymat par défaut | L'identité de l'utilisateur n'est jamais divulguée sans consentement |
| Pseudonyme | Utilisation d'un prénom ou pseudonyme dans les échanges |
| Données sensibles | Ne jamais stocker de pièces d'identité, relevés bancaires, etc. |
| Délai d'anonymisation | 7 jours maximum après demande `SUPPRIMER MES DONNÉES` |

---

## 6. Événements de traçabilité (8)

| # | Événement | Déclencheur | Trace |
|:-:|-----------|-------------|-------|
| 1 | `message_received` | Nouveau message entrant | Horodatage, canal, contenu tronqué |
| 2 | `intent_detected` | Intention identifiée | Intent, confiance |
| 3 | `lead_scored` | Score calculé | Score, boosters, pénalités |
| 4 | `lead_classified` | Classification attribuée | Classe (HOT/WARM/COLD/SPAM) |
| 5 | `crm_routed` | Lead routé vers un agent | Agent, file d'attente, priorité |
| 6 | `response_sent` | Réponse envoyée | Canal, template, délai |
| 7 | `follow_up_scheduled` | Relance programmée | Échéance, type (J1/J7/J30/J90) |
| 8 | `escalation_triggered` | Escalade humaine activée | Raison, destinataire |

---

## 7. Flux conversationnels par intent

### 7.1 RENT (Location)

```
ask_city → ask_neighborhood → ask_budget → show_properties
```

| Étape | Champ collecté | Question type |
|-------|----------------|---------------|
| 1 | Ville | "Dans quelle ville cherchez-vous un logement ?" |
| 2 | Quartier | "Avez-vous un quartier préféré à [ville] ?" |
| 3 | Budget | "Quel est votre budget mensuel maximum ?" |
| 4 | — | "Voici les biens disponibles à [ville] dans votre budget..." |

### 7.2 BUY (Achat)

```
ask_city → ask_budget → ask_property_type → show_properties
```

| Étape | Champ collecté | Question type |
|-------|----------------|---------------|
| 1 | Ville | "Dans quelle ville souhaitez-vous acheter ?" |
| 2 | Budget | "Quel est votre budget maximum ?" |
| 3 | Type de bien | "Quel type de bien recherchez-vous ?" |
| 4 | — | "Voici les annonces correspondant à votre recherche..." |

### 7.3 SELL (Vente)

```
ask_property_details → collect_contact → create_listing
```

| Étape | Champ collecté | Question type |
|-------|----------------|---------------|
| 1 | Détails du bien | "Parlez-moi du bien que vous souhaitez vendre..." |
| 2 | Contact | "Quel est votre numéro pour qu'on vous contacte ?" |
| 3 | — | "Votre annonce a été créée. Nous vous contacterons sous 24h." |

### 7.4 INVESTOR (Investissement)

```
ask_city → ask_budget → ask_investment_goal → show_opportunities
```

| Étape | Champ collecté | Question type |
|-------|----------------|---------------|
| 1 | Ville | "Dans quelle ville souhaitez-vous investir ?" |
| 2 | Budget | "Quel budget souhaitez-vous investir ?" |
| 3 | Objectif | "Quel type d'investissement : locatif, revente, terrain ?" |
| 4 | — | "Voici les opportunités d'investissement à [ville]..." |

---

## 8. Politique de réponse

| Règle | Description |
|-------|-------------|
| **Positionnement** | LAWIM est un intermédiaire de mise en relation |
| **Zéro commission** | Aucune commission sur les transactions, accompagnement payant : 50 000 FCFA |
| **Ton** | Professionnel, courtois, vouvoiement systématique |
| **Langue** | Auto-détection : français, anglais, pidgin |
| **Aucune garantie** | Score indicatif seulement, pas de garantie sur les biens |
| **Pas de conseil juridique** | Rediriger vers un notaire |

---

## 9. Humanisation

| Règle | Application |
|-------|-------------|
| Langage naturel | Éviter les réponses robotiques, les listes numérotées systématiques |
| Empathie | Reconnaître les frustrations, les urgences |
| Expressions locales | Utiliser des expressions adaptées au contexte culturel |
| Variété | Alterner les formulations, ne pas répéter les mêmes phrases |
| Signes de vie | Accuser réception, montrer qu'on a compris avant de répondre |

---

## 10. Guide de style

| Règle | Application |
|-------|-------------|
| Phrases courtes | Maximum 2 lignes par message |
| Structure claire | Un sujet par message |
| Pas de jargon | Éviter les termes techniques non expliqués |
| Positif | Reformuler les contraintes en opportunités |
| Appel à l'action | Terminer par une question ou une proposition |
| Pas de promesse | Ne jamais garantir un résultat |

---

## 11. Multilingue

### 11.1 Hiérarchie de détection

| Ordre | Méthode | Statut |
|:-----:|---------|--------|
| 1 | DeepSeek AI | Actif |
| 2 | Gemini | Non implémenté |
| 3 | Règles locales (mots-clés, indicatifs) | Actif |

### 11.2 Langues supportées

| Langue | Niveau | Notes |
|--------|--------|-------|
| **Français (FR)** | Complet | Langue par défaut |
| **Anglais (EN)** | Complet | Détection automatique |
| **Pidgin (PID)** | Partiel | ~14 mots, phrases de base |

### 11.3 Commande LANGUE

| Commande | Action |
|----------|--------|
| `LANGUE FR` | Basculer en français |
| `LANGUE EN` | Basculer en anglais |
| `LANGUE PID` | Basculer en pidgin (partiel) |

---

## 12. Mémoire conversationnelle

### 12.1 Champs mémoire court terme

| Champ | Description | Persistance |
|-------|-------------|-------------|
| `city` | Ville recherchée | Session |
| `neighborhood` | Quartier préféré | Session |
| `budget` | Budget déclaré | Session |
| `property_type` | Type de bien recherché | Session |
| `user_role` | Rôle détecté (buyer/tenant/seller/investor) | Session |
| `preferred_language` | Langue de conversation | Session + base |

### 12.2 Mémoire long terme

| Champ | Description |
|-------|-------------|
| `favorite_locations` | Localisations fréquemment recherchées |
| `investment_preferences` | Préférences d'investissement (locatif, revente, terrain) |
| `diaspora_country` | Pays de résidence pour la diaspora |
| `search_history` | Historique des recherches précédentes |
| `satisfaction_score` | Score de satisfaction historique |

### 12.3 Rétention

| Règle | Valeur |
|-------|--------|
| Durée de rétention | 90 jours |
| Après 90 jours d'inactivité | Oubli complet du contexte |
| Lead > 12 mois | Considéré comme relançable |

---

## 13. Routage des réponses

### 13.1 Hiérarchie

| Ordre | Mécanisme | Description |
|:-----:|-----------|-------------|
| 1 | **DeepSeek AI** | Analyse intelligente, extraction, génération de réponse |
| 2 | **Règles locales** | Réponses pré-définies (bonjour, merci, aide, commandes) |
| 3 | **Templates** | Messages standards multilingues |

### 13.2 Templates disponibles

| Template | Usage | Langues |
|----------|-------|---------|
| `welcome` | Message de bienvenue | FR, EN, PID |
| `help` | Message d'aide | FR, EN |
| `no_match` | Aucun résultat trouvé | FR, EN, PID |
| `thanks` | Remerciement | FR, EN |
| `ask_name` | Demande du nom | FR, EN |
| `ask_phone` | Demande du téléphone | FR, EN |
| `stats` | Statistiques | FR, EN |

---

## 14. Planning de relance (Follow-up)

| Échéance | Délai | Message type |
|----------|:-----:|--------------|
| **J1** | 24h | Nouveaux biens correspondant à la recherche |
| **J7** | 7 jours | 5 nouvelles annonces disponibles |
| **J30** | 30 jours | Offre : mois prioritaire gratuit |
| **J90** | 90 jours | 500+ requêtes traitées, souhaitez-vous relancer ? |

### 14.1 Messages types

| Étape | Message |
|-------|---------|
| J1 | "J'ai trouvé [N] nouveaux biens qui pourraient vous intéresser à [ville]..." |
| J7 | "Il y a [N] nouvelles annonces de [type] à [ville] qui correspondent à votre recherche..." |
| J30 | "Bonne nouvelle ! Vous bénéficiez d'un mois prioritaire gratuit pour votre recherche à [ville]..." |
| J90 | "Nous avons traité plus de 500 requêtes depuis votre dernière visite. Souhaitez-vous relancer votre recherche ?" |

### 14.2 Canal de relance

| Canal | Usage |
|-------|-------|
| WhatsApp (GreenAPI) | Canal principal de relance |
| Email | Canal secondaire (si email collecté) |

---

## 15. Commandes spéciales

| Commande | Action |
|----------|--------|
| `SIGNALER [raison]` | Crée un litige dans la table disputes |
| `SUPPRIMER MES DONNÉES` | Anonymise la personne (RGPD, délai 7 jours) |
| `ACCOMPAGNEMENT` | Active le service payant (50 000 FCFA) |
| `OUI` / `NON` | Réponse à une demande de permission |
| `STATS` | Affiche les performances (agents) |
| `LANGUE [FR/EN/PID]` | Change la langue de la conversation |
| `RECHERCHE` | Voir les nouveaux biens (relance J7) |
| `PRIORITAIRE` | Active la recherche prioritaire (relance J30) |
| `RELANCER` | Reprendre la recherche (relance J90) |

---

## 16. Gestion des objections

| Catégorie | Peurs / Objections |
|-----------|-------------------|
| **Acheteurs (12)** | Arnaque, qualité du bien, prix trop élevé, quartier dangereux, absence de titre foncier, vices cachés, litige, voisinage, accessibilité, financement, délai, revente |
| **Vendeurs (8)** | Prix trop bas, délai trop long, confidentialité, arnaque, visites sans filtre, commission cachée, pas d'acquéreur sérieux, paperasse |

---

## 17. Règles d'escalade humaine

| Condition | Action |
|-----------|--------|
| Question juridique | Rediriger vers un notaire |
| Litige / dispute | Activer commande `SIGNALER`, escalade support |
| Demande explicite de parler à un humain | Transférer au conseiller disponible |
| 3 échecs de qualification consécutifs | Escalade manuelle |
| Signalement d'urgence suspect | Vérification manuelle |

---

## 18. Détection d'intention dans la conversation

| Signal | Mots-clés |
|--------|-----------|
| `sell` | j'ai, je vends, proprio, available, for sale |
| `visit_request` | visite, voir, visit, on passe, check |
| `urgent_signal` | urgent, asap, vite, rapidement, now |
| `investor_lead` | investir, rentable, ROI, cash flow |
| `broker_lead` | je peux trouver, j'ai un contact |
| `price_signal` | prix, budget, max, k, mille |
| `search` | je cherche, i need, looking for, besoin, recherche |

---

## 19. Feedback utilisateur

| Entrée | Interprétation | Action |
|--------|----------------|--------|
| 👍 (thumbs_up emoji) | Note 5/5 | Enregistrer satisfaction |
| 👎 (thumbs_down emoji) | Note 1/5 | Escalade support |
| "note 4", "note 3" | Note sur 5 | Enregistrer satisfaction |
| Message négatif | Insatisfaction | Proposer d'améliorer, escalade si persistant |

---

## 20. Règles avancées

| Règle | Description |
|-------|-------------|
| **Gestion des corrections** | "Non, je parlais de..." → Mettre à jour le champ, ne pas contredire |
| **Changement de sujet** | Si l'utilisateur change de sujet, suivre son lead sans insister |
| **Reformulations** | Accepter les reformulations comme des mises à jour |
| **Stop explicite** | "Merci, ça suffit" → Arrêter la qualification |
| **Stop implicite** | 3 messages sans information nouvelle → Arrêter la qualification |
| **Reprise après interruption** | Résumer la conversation précédente avant de continuer |

---

*Document patrimonial Gold — Toute reconstruction doit respecter ce modèle validé.*
