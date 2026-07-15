# Réaudit GOLD — Domaines Conversation & Négociation

**Date :** 2026-07-15  
**Périmètre :** 22 fichiers analysés (13 Conversation, 4 Négociation, 5 transverses)  
**Auteur :** Agent réauditeur LAWIM

---

## Table des matières

1. [Vérification des points faibles H0.1](#1-vérification-des-points-faibles-h01)
2. [Règles Conversation — Extraites et vérifiées](#2-règles-conversation)
3. [Règles Négociation — Extraites et vérifiées](#3-règles-négociation)
4. [Règles Transverses](#4-règles-transverses)
5. [Glossaire des seuils et constantes](#5-glossaire-des-seuils-et-constantes)
6. [Anomalies et corrections obligatoires](#6-anomalies-et-corrections-obligatoires)

---

## 1. Vérification des points faibles H0.1

### 1.1 Camfranglais : est-ce vraiment une 4e langue supportée ?

| Statut | Détail |
|--------|--------|
| **FAUX** | Le Camfranglais N'EST PAS une 4e langue supportée dans les moteurs de détection et de réponse. |

**Preuves :**
- `language_detector.py` : ne supporte que `fr`, `en`, `pidgin`
- `language_detector_ia.py` : ne supporte que `fr`, `en`, `pidgin`
- `multilingual_responses.py` : ne contient que `fr`, `en`, `pidgin`
- `language_handler.py` : ne contient que `fr`, `en`
- `deepseek_prompt.txt` : mentionne « français, anglais, pidgin »
- `RESPONSE_POLICY.md` : mentionne « français, anglais, pidgin »

**Seule trace :** `whatsapp_language.json` contient des entrées `"language": "camfranglais"` dans son dictionnaire lexical, mais aucun module de routage ou de réponse ne l'exploite.

**Décision GOLD :** Ne pas promouvoir le camfranglais en 4e langue supportée. Rester sur 3 langues (FR/EN/PIDGIN). Les expressions camfranglaises sont absorbées par le pidgin.

---

### 1.2 Rétention mémoire : 90 jours ou 365 jours ?

| Statut | Détail |
|--------|--------|
| **LES DEUX** | Deux valeurs coexistent selon le contexte. Ce n'est pas une contradiction mais une spécialisation non documentée. |

**Preuves :**
- `long_term_memory.py:92` : `if days_ago < 365` → rétention mémoire longue = **365 jours (1 an)**
- `follow_up_system.py:27` : relance maximale à `2160h = 90 jours` → cycle de relance = **90 jours**
- `follow_up_system.py:22` : planning des relances = `24h, 7j, 30j, 90j`

**Décision GOLD :** Maintenir les deux :
- **365 jours** pour la mémoire longue (contexte de recherche)
- **90 jours** pour le cycle de relance actif

---

### 1.3 Signaux d'intention : 7 ou moins ?

| Statut | Détail |
|--------|--------|
| **5 (cinq)** | Il existe exactement 5 fichiers d'intention, pas 7. |

**Preuves :**
- `intent_detector.py:13-18` : fichiers = `buy_property.json`, `rent_property.json`, `sell_property.json`, `investor_intent.json`, `search_property.json` → **5 intentions**
- `conversation-patterns.md` : 10 patterns de conversation (dont Search, Rent, Sell, Investor, Negotiation, Urgency, Chatty, Language switch, Title transparency, Human transfer)

**Décision GOLD :** Le nombre de signaux d'intention dans le détecteur est **5**. Les « 7 signaux » n'existent pas dans le code. Corriger toute documentation qui en mentionnerait 7.

---

### 1.4 12 peurs acheteurs : 12 ou 10 ?

| Statut | Détail |
|--------|--------|
| **10 (dix)** | Exactement 10 peurs sont listées dans le tableau, pas 12. |

**Preuves :**
- `trust-and-objection-patterns.md` section « Ce que les acheteurs craignent » :
  1. Fraude / arnaque
  2. Paiement anticipé sans visite
  3. Faux propriétaire
  4. Dossier juridique flou
  5. Conflits familiaux / successoraux
  6. Zone enclavée / accès
  7. Vendeur peu crédible
  8. Mauvaise affaire / revente
  9. Frais cachés
  10. Curiosité sans sérieux

**Décision GOLD :** Corriger toute mention de « 12 peurs » en « 10 peurs acheteurs ».

---

### 1.5 4 moments clés annuels : existent-ils vraiment ?

| Statut | Détail |
|--------|--------|
| **N'EXISTENT PAS** | Aucune trace de « 4 moments clés annuels » dans les fichiers audités. |

**Preuves :**
- Les « moments clés » dans `negotiation-patterns.md` décrivent les **étapes du cycle de négociation** (annonce → comparaison → visite → preuves → validation → conclusion), pas des moments annuels.
- Aucun fichier ne mentionne de saisonnalité ou de moments calendaires annuels.

**Décision GOLD :** Supprimer toute référence à « 4 moments clés annuels ». Remplacer par le cycle de négociation documenté dans `negotiation-patterns.md`.

---

### 1.6 conversation_tone.md existe-t-il ?

| Statut | Détail |
|--------|--------|
| **N'EXISTE PAS** | Aucun fichier nommé `conversation_tone.md` n'a été trouvé. |

**Preuves :**
- Glob `**/*conversation_tone*` → 0 résultat
- Glob `**/*conversation-tone*` → 0 résultat
- Le fichier le plus proche est `channel-tone-guidelines.md`

**Décision GOLD :** Créer `conversation_tone.md` dans la version GOLD (à faire dans le cadre du projet GOLD). Pour l'instant, les règles de ton sont dans `conversation-style-guide.md`, `channel-tone-guidelines.md` et `multilingual-conversation-guidelines.md`.

---

### 1.7 5 arguments propriétés : sont-ils dans le playbook ?

| Statut | Détail |
|--------|--------|
| **N'EXISTENT PAS** | Aucune trace de « 5 arguments » ou « 5 raisons » pour les propriétés dans le playbook. |

**Preuves :**
- `48-LAWIM-SALES-PLAYBOOK.md` : Section 13 liste les services (mise en relation, accompagnement, vérification documentaire, photographie, vidéo, visite assistée, visibilité premium, boost, assistance personnalisée, accompagnement diaspora) — mais pas sous forme de « 5 arguments propriétés ».
- Aucune occurrence de « 5 argument », « 5 raison », « 5 bénéfice », « 5 avantage » dans le playbook.

**Décision GOLD :** Les arguments pour convaincre les propriétaires sont dans le playbook section 9 (meilleure présentation, visibilité, accompagnement, mise en relation, réduction désordre informel, suivi — 6 points, pas 5). Supprimer toute mention de « 5 arguments propriétés ».

---

### 1.8 Messages de relance : correspondent-ils au code ?

| Statut | Détail |
|--------|--------|
| **OUI** | Les messages dans `follow_up_system.py` sont exactement ceux envoyés. |

**Preuves :**
- `follow_up_system.py:23-28` : 4 messages correspondant aux 4 seuils :
  - 24h → message J+1
  - 168h (7j) → message S+1
  - 720h (30j) → message M+1
  - 2160h (90j) → message M+3

**Décision GOLD :** Aucune correction nécessaire. Les messages de relance sont cohérents avec le code.

---

### Synthèse H0.1

| Point | Ancienne valeur | Valeur réelle | Confiance |
|-------|----------------|---------------|-----------|
| Camfranglais 4e langue | OUI | NON (seulement dans lexique) | ÉLEVÉE |
| Rétention mémoire | 90 ou 365 ? | Les deux : 365j mémoire, 90j relance | ÉLEVÉE |
| Signaux d'intention | 7 | 5 | ÉLEVÉE |
| 12 peurs acheteurs | 12 | 10 | ÉLEVÉE |
| 4 moments clés annuels | OUI | FAUX (inexistants) | ÉLEVÉE |
| conversation_tone.md | Existe | N'EXISTE PAS | ÉLEVÉE |
| 5 arguments propriétés | Dans playbook | FAUX (absents) | ÉLEVÉE |
| Messages de relance | Correspondent | CORRESPONDENT | ÉLEVÉE |

---

## 2. Règles Conversation

### CONV-001 : Politique de positionnement
- **Description :** LAWIM est un intermédiaire (mise en relation), zéro commission, pas de garantie sur les biens (score indicatif).
- **Source :** `LAWIMA/00_GLOBAL/rules/RESPONSE_POLICY.md:3-6`
- **Confiance :** ÉLEVÉE

### CONV-002 : Ton obligatoire
- **Description :** Professionnel, courtois, vendeur. Vouvoiement systématique.
- **Source :** `LAWIMA/00_GLOBAL/rules/RESPONSE_POLICY.md:8-10` ; `deepseek_prompt.txt:2`
- **Confiance :** ÉLEVÉE

### CONV-003 : Langues supportées (3)
- **Description :** Français, Anglais, Pidgin Cameroon. Détection automatique. Pas de camfranglais.
- **Source :** `LAWIMA/00_GLOBAL/rules/RESPONSE_POLICY.md:11` ; `multilingual_responses.py` ; `language_detector.py` ; `multilingual-conversation-guidelines.md:5-7`
- **Confiance :** ÉLEVÉE

### CONV-004 : Réponse dans la langue du message courant
- **Description :** Ne jamais mélanger les langues dans une même réponse. Si l'utilisateur change de langue, le système switch sans redémarrer la conversation.
- **Source :** `multilingual-conversation-guidelines.md:21-22` ; `conversation-patterns.md:34`
- **Confiance :** ÉLEVÉE

### CONV-005 : Sécurité juridique
- **Description :** Si question juridique, orienter vers un notaire.
- **Source :** `RESPONSE_POLICY.md:14` ; `deepseek_prompt.txt:9`
- **Confiance :** ÉLEVÉE

### CONV-006 : Complétude (champs obligatoires)
- **Description :** DeepSeek demande les champs manquants : type, localisation, budget.
- **Source :** `RESPONSE_POLICY.md:15` ; `deepseek_prompt.txt:5`
- **Confiance :** ÉLEVÉE

### CONV-007 : Budget obligatoire avant matching
- **Description :** Ne jamais lancer le matching sans budget exploitable. Demander le budget dès que le contexte le requiert.
- **Source :** `conversation-style-guide.md:51-52` ; `response-policy.md:25-27`
- **Confiance :** ÉLEVÉE

### CONV-008 : Qualification order strict
- **Description :** Ordre de qualification : intention → type de bien → localisation → budget → délai → critères spécifiques → préférences → confirmation.
- **Source :** `conversation-style-guide.md:37-47`
- **Confiance :** ÉLEVÉE

### CONV-009 : Une seule question à la fois
- **Description :** Maximum une question principale par message. Ne pas empiler plusieurs questions complexes.
- **Source :** `conversation-style-guide.md:30-33` ; `omnichannel-playbook.md:19`
- **Confiance :** ÉLEVÉE

### CONV-010 : Maximum 1-3 phrases par réponse
- **Description :** 1 à 3 phrases maximum. Simple vocabulary. Short paragraphs only.
- **Source :** `conversation-style-guide.md:30-33`
- **Confiance :** ÉLEVÉE

### CONV-011 : Maximum 1-2 emojis utiles par message
- **Description :** Limiter les emojis à 👋 accueil, 📍 localisation, 💰 budget.
- **Source :** `multilingual-conversation-guidelines.md:25`
- **Confiance :** ÉLEVÉE

### CONV-012 : Réponse structurée obligatoire (DeepSeek)
- **Description :** Format JSON obligatoire avec extracted, missing, response_text, confidence, routing.
- **Source :** `deepseek_prompt.txt:13-20`
- **Confiance :** ÉLEVÉE

### CONV-013 : Routage vers agent/propriétaire si match
- **Description :** Notifier l'agent ou le propriétaire quand un match est trouvé.
- **Source :** `RESPONSE_POLICY.md:16`
- **Confiance :** ÉLEVÉE

### CONV-014 : Accompagnement payant (50k FCFA)
- **Description :** Service d'accompagnement payant à 50 000 FCFA sur demande (commande ACCOMPAGNEMENT).
- **Source :** `RESPONSE_POLICY.md:17,24`
- **Confiance :** ÉLEVÉE

### CONV-015 : Commande SIGNALER
- **Description :** `SIGNALER [raison]` crée un litige dans la table disputes.
- **Source :** `RESPONSE_POLICY.md:18,22`
- **Confiance :** ÉLEVÉE

### CONV-016 : Commande SUPPRIMER MES DONNÉES (RGPD)
- **Description :** Anonymise la personne. Délai d'exécution : 7 jours.
- **Source :** `RESPONSE_POLICY.md:19,23`
- **Confiance :** ÉLEVÉE

### CONV-017 : Mémoire conversation courte (50 échanges max)
- **Description :** L'historique de conversation est limité à 50 échanges maximum.
- **Source :** `conversation_memory.py:187-188` : `if len(history) > 50: history = history[-50:]`
- **Confiance :** ÉLEVÉE

### CONV-018 : Mémoire longue (365 jours)
- **Description :** Le contexte des recherches précédentes est conservé jusqu'à 365 jours (1 an).
- **Source :** `long_term_memory.py:92` : `if days_ago < 365`
- **Confiance :** ÉLEVÉE

### CONV-019 : Relance leads (24h, 7j, 30j, 90j)
- **Description :** 4 seuils de relance automatique : 24h, 168h (7j), 720h (30j), 2160h (90j). Une seule relance par seuil.
- **Source :** `follow_up_system.py:22-28, 54`
- **Confiance :** ÉLEVÉE

### CONV-020 : Messages d'accueil personnalisés (4 niveaux)
- **Description :** 4 niveaux de familiarité selon le délai de retour : J+1 (niveau 1), J+2-7 (niveau 2), J+8-30 (niveau 3), J+31+ (niveau 4).
- **Source :** `conversation_memory.py:136-143`
- **Confiance :** ÉLEVÉE

### CONV-021 : Détection de langue par hiérarchie IA
- **Description :** DeepSeek → (Gemini futur) → Règles locales (mots-clés). Fallback = français si aucun mot-clé détecté.
- **Source :** `language_detector_ia.py:76-94`
- **Confiance :** ÉLEVÉE

### CONV-022 : Détection de feedback (👍/👎/notes 1-5)
- **Description :** Détection automatique des feedbacks : thumbs up (👍, ok, oui, merci…), thumbs down (👎, non, pas bien…), notes 1-5, "note X".
- **Source :** `feedback_handler.py:17-38`
- **Confiance :** ÉLEVÉE

### CONV-023 : Anti-spam (10 msg/min, blocage 60 min)
- **Description :** Limite de 10 messages par minute. Au-delà, blocage de 60 minutes.
- **Source :** `anti_spam.py:3,17-18`
- **Confiance :** ÉLEVÉE

### CONV-024 : Hiérarchie de réponse (3 niveaux)
- **Description :** DeepSeek IA (priorité) → Google API (2e niveau) → Règles locales → Templates (fallback).
- **Source :** `response_router.py:2` ; `response_router.py:58-65`
- **Confiance :** MOYENNE (le niveau Google API n'est pas implémenté, seulement DeepSeek et règles locales)

### CONV-025 : Ne jamais garantir un bien
- **Description :** Le score est indicatif. Ne jamais promettre une vente ou location garantie.
- **Source :** `deepseek_prompt.txt:8` ; `48-LAWIM-SALES-PLAYBOOK.md:272-273`
- **Confiance :** ÉLEVÉE

### CONV-026 : Interdiction de mentionner l'IA
- **Description :** Ne jamais mentionner AI, bot, assistant, ou statut technique. Ne pas utiliser d'intros robotiques.
- **Source :** `conversation-style-guide.md:89-91`
- **Confiance :** ÉLEVÉE

### CONV-027 : Structure de réponse
- **Description :** Chaque réponse doit : 1) accuser réception, 2) poser la prochaine question critique, 3) confirmer implicitement, 4) indiquer la prochaine étape.
- **Source :** `conversation-style-guide.md:19-26`
- **Confiance :** ÉLEVÉE

### CONV-028 : Préfixe obligatoire 🤖 LAWIM IA: (hors dashboard)
- **Description :** Les messages sortants doivent être préfixés par `🤖 LAWIM IA:` sauf pour les métadonnées dashboard.
- **Source :** `multilingual-conversation-guidelines.md:23`
- **Confiance :** ÉLEVÉE

### CONV-029 : Budget par type de transaction
- **Description :** Location = mensuel + caution + avance, Vente = prix global, Terrain = prix global ou prix/m², Commercial = mensuel + éventuel pas-de-porte.
- **Source :** `conversation-style-guide.md:54-58`
- **Confiance :** ÉLEVÉE

### CONV-030 : Vocabulaire Cameroun
- **Description :** Utiliser « chambres », « douches », « salons ». Ne pas utiliser « pièces », « standing ».
- **Source :** `conversation-style-guide.md:63-74`
- **Confiance :** ÉLEVÉE

### CONV-031 : Arrêt précoce de qualification
- **Description :** Arrêter la qualification si : ville non couverte, inventaire vide, handoff humain requis, conversation répétitive/hors-sujet/confuse.
- **Source :** `conversation-style-guide.md:77-85` ; `response-policy.md:31-34`
- **Confiance :** ÉLEVÉE

### CONV-032 : Watchlist si ville non couverte ou inventaire vide
- **Description :** Proposer une watchlist (mise en veille) au lieu de continuer la qualification si la ville n'est pas couverte ou l'inventaire vide.
- **Source :** `response-policy.md:31-34`
- **Confiance :** ÉLEVÉE

### CONV-033 : Handoff vers humain
- **Description :** Déclencheurs : demande explicite, confiance faible, cas sensible, litige, signaux de fraude récurrents, peur documentaire diaspora non résolue après preuves.
- **Source :** `omnichannel-playbook.md:117-123` ; `response-policy.md:38-41`
- **Confiance :** ÉLEVÉE

### CONV-034 : Qualité de handoff
- **Description :** Transmettre l'historique complet, préserver la demande/lead courant, assigner un propriétaire explicitement, marquer la prochaine action due, ne pas révéler les contacts privés.
- **Source :** `omnichannel-playbook.md:127-131`
- **Confiance :** ÉLEVÉE

### CONV-035 : États de statut visibles
- **Description :** 7 états : open, waiting_user, waiting_agent, waiting_owner, waiting_agency, resolved, closed, archived.
- **Source :** `omnichannel-playbook.md:139-147`
- **Confiance :** MOYENNE (basée sur recommandation, pas encore implémentée dans tous les canaux)

### CONV-036 : Qualification WhatsApp (1 question à la fois)
- **Description :** WhatsApp : très court, naturel, mobile first, une question à la fois.
- **Source :** `whatsapp-telegram-dashboard-qualification.md:9-13`
- **Confiance :** ÉLEVÉE

### CONV-037 : Qualification Telegram (2-3 champs par message)
- **Description :** Telegram : structuré, listes à puces, 2-3 champs par message.
- **Source :** `whatsapp-telegram-dashboard-qualification.md:9-13`
- **Confiance :** ÉLEVÉE

### CONV-038 : Qualification Dashboard (formulaire complet)
- **Description :** Dashboard : formulaire guidé, opérateur, champ obligatoire visible, état du dossier, bouton d'escalade.
- **Source :** `whatsapp-telegram-dashboard-qualification.md:9-13, 33-40`
- **Confiance :** ÉLEVÉE

### CONV-039 : Escalade WhatsApp (2 questions sans réponse)
- **Description :** Escalader si 2 questions consécutives restent sans réponse, si titre/usage/budget flous, si client veut un humain.
- **Source :** `whatsapp-telegram-dashboard-qualification.md:161-163`
- **Confiance :** ÉLEVÉE

### CONV-040 : 7 comportements fréquents WhatsApp Cameroun
- **Description :** Messages courts, vocaux, demandes directes, besoin de réactivité. LAWIM doit répondre simplement, rester humain, éviter les blocs longs.
- **Source :** `omnichannel-playbook.md:168-179`
- **Confiance :** ÉLEVÉE

### CONV-041 : Gestion du silence (ne pas classer comme perdu)
- **Description :** Un lead silencieux n'est pas automatiquement perdu. Ne pas classer comme inintéressé sur la base du silence seul.
- **Source :** `conversation-patterns.md:245-248` ; `omnichannel-playbook.md:92-93`
- **Confiance :** ÉLEVÉE

### CONV-042 : Cycle de décision long
- **Description :** Un acheteur peut disparaître et revenir après plusieurs jours/semaines. LAWIM conserve un ton accueillant.
- **Source :** `conversation-patterns.md:234-242` ; `omnichannel-playbook.md:88-89`
- **Confiance :** ÉLEVÉE

### CONV-043 : Validation sociale = pas une objection
- **Description :** « Mon grand frère doit voir », « mon cousin va vérifier », etc. sont des étapes normales du cycle de décision. Ne pas traiter comme objections.
- **Source :** `conversation-patterns.md:221-231` ; `omnichannel-playbook.md:79-85`
- **Confiance :** ÉLEVÉE

### CONV-044 : Confiance progressive (séquence)
- **Description :** Intérêt → Vérification → Réassurance → Visite → Validation documentaire → Décision. Jamais Intérêt → Achat direct.
- **Source :** `conversation-patterns.md:252-262` ; `omnichannel-playbook.md:96-101`
- **Confiance :** ÉLEVÉE

### CONV-045 : Ton 70/20/10
- **Description :** 70% conseiller immobilier expérimenté, 20% proche qui connaît le marché local, 10% concierge premium.
- **Source :** `multilingual-conversation-guidelines.md:44-46`
- **Confiance :** ÉLEVÉE

### CONV-046 : Interdictions tonales
- **Description :** Interdit : jargon CRM, formulaire, assistant administratif, ton commercial agressif, urgence artificielle, pression, demande d'acompte avant visite.
- **Source :** `multilingual-conversation-guidelines.md:48` ; `conversation-patterns.md:299-300`
- **Confiance :** ÉLEVÉE

### CONV-047 : Suivi explicite uniquement sur signal de continuité
- **Description :** Réutiliser l'historique seulement si message contient signal de continuité : « Je reviens concernant ma demande », « Dossier LAW-xxxx », « Any update », « Na the same request ».
- **Source :** `multilingual-conversation-guidelines.md:33-40`
- **Confiance :** ÉLEVÉE

### CONV-048 : Accueil social (GREETING_ONLY)
- **Description :** Pour les salutations pures : salutation + question ouverte, sans reformulation ni injection d'historique. Extraction et reformulation désactivés.
- **Source :** `multilingual-conversation-guidelines.md:27-31`
- **Confiance :** ÉLEVÉE

### CONV-049 : Pas de re-qualification après confiance établie
- **Description :** Une fois la confiance établie après visite, ne pas re-qualifier inutilement. Transaction peut accélérer.
- **Source :** `trust-and-objection-patterns.md:75-76`
- **Confiance :** MOYENNE

### CONV-050 : Urgence réelle vs artificielle
- **Description :** Distinguer urgence réelle du vendeur (liquidité) de l'urgence artificielle marketing. Ne pas créer de fausse urgence.
- **Source :** `negotiation-patterns.md:119` ; `omnichannel-playbook.md:220`
- **Confiance :** ÉLEVÉE

---

## 3. Règles Négociation

### NEG-001 : Négociation normale sur le marché camerounais
- **Description :** Le marché camerounais fonctionne beaucoup par négociation. La négociation se joue sur les détails, souvent après la visite.
- **Source :** `negotiation-patterns.md:11`
- **Confiance :** ÉLEVÉE

### NEG-002 : LAWIM accompagne la négociation (ne simule pas)
- **Description :** LAWIM accompagne la négociation, ne simule pas un agent commercial agressif.
- **Source :** `negotiation-patterns.md:24`
- **Confiance :** ÉLEVÉE

### NEG-003 : Expressions de négociation (lexique)
- **Description :** Expressions détectées : « dernier prix », « prix ferme », « prix négociable », « à débattre », « on peut s'entendre », « best price », « nego possible », « combien dernier ? ».
- **Source :** `negotiation.json:2-11`
- **Confiance :** ÉLEVÉE

### NEG-004 : Réponse à « dernier prix »
- **Description :** Ne jamais réduire la conversation au seul prix. Toujours : comprendre le besoin, confirmer le contexte, rappeler les caractéristiques du bien, proposer la suite logique (visite, documents, clarification).
- **Source :** `conversation-patterns.md:148-157`
- **Confiance :** ÉLEVÉE

### NEG-005 : Gestion du budget irréaliste
- **Description :** Rester respectueux, expliquer, proposer des alternatives réalistes. Ne jamais humilier l'utilisateur.
- **Source :** `conversation-patterns.md:160-167`
- **Confiance :** ÉLEVÉE

### NEG-006 : Signaux de fraude/vigilance
- **Description :** Prix anormalement bas, documents incohérents, refus de visite, informations contradictoires, urgence artificielle, interlocuteur non identifiable.
- **Source :** `conversation-patterns.md:197-202` ; `omnichannel-playbook.md:55-59`
- **Confiance :** ÉLEVÉE

### NEG-007 : Réponse aux signaux de fraude
- **Description :** Ne jamais accuser. Recommander vérifications, encourager prudence, proposer validation documentaire, proposer visite.
- **Source :** `conversation-patterns.md:205-213` ; `omnichannel-playbook.md:64-71`
- **Confiance :** ÉLEVÉE

### NEG-008 : Vendeur — prix ambitieux initial + marge intégrée
- **Description :** Le vendeur fixe un prix ambitieux avec marge intégrée. Attend que l'acheteur propose le premier prix.
- **Source :** `negotiation-patterns.md:14-17`
- **Confiance :** ÉLEVÉE

### NEG-009 : Acheteur — négociation tôt après première offre
- **Description :** L'acheteur négocie tôt après la première offre. Compare comme levier. Interprète la contre-offre comme test.
- **Source :** `negotiation-patterns.md:19-21`
- **Confiance :** ÉLEVÉE

### NEG-010 : Diaspora — suivi à distance, confiance, traçabilité
- **Description :** La diaspora accorde importance à : confiance, traçabilité, documents, vidéos, preuves. Peur dominante : arnaque documentaire.
- **Source :** `conversation-patterns.md:170-183` ; `negotiation-patterns.md:67-74`
- **Confiance :** ÉLEVÉE

### NEG-011 : Urgence_signals (8 expressions)
- **Description :** Expressions d'urgence : urgent, très urgent, asap, immédiatement, aujourd'hui, avant fin semaine, je déménage demain, need now.
- **Source :** `urgency_signals.json:2-12`
- **Confiance :** ÉLEVÉE

### NEG-012 : Services vendables (10)
- **Description :** 10 services : mise en relation, accompagnement, vérification documentaire, photographie, vidéo, visite assistée, visibilité premium, boost, assistance personnalisée, accompagnement diaspora.
- **Source :** `48-LAWIM-SALES-PLAYBOOK.md:170-181`
- **Confiance :** ÉLEVÉE

### NEG-013 : Objections commerciales (8)
- **Description :** 8 objections traitées dans le playbook : Facebook gratuit, travail avec agents, refus de payer, méconnaissance LAWIM, fiabilité, agence vs plateforme, commission, utilité.
- **Source :** `48-LAWIM-SALES-PLAYBOOK.md:186-218`
- **Confiance :** ÉLEVÉE

### NEG-014 : Processus commercial (8 étapes)
- **Description :** Prospection → Qualification → Présentation → Proposition → Suivi → Conclusion → Activation → Fidélisation.
- **Source :** `48-LAWIM-SALES-PLAYBOOK.md:222-230`
- **Confiance :** ÉLEVÉE

### NEG-015 : Règles commerciales (7 règles)
- **Description :** Ne pas promettre vente garantie, location garantie, ne pas inventer un bien, ne pas masquer conditions, présenter services payants avant engagement, respecter confidentialité, rappeler zéro commission.
- **Source :** `48-LAWIM-SALES-PLAYBOOK.md:271-278`
- **Confiance :** ÉLEVÉE

### NEG-016 : KPI commerciaux (8)
- **Description :** Prospects contactés, partenaires signés, biens ajoutés, agences intégrées, taux de conversion, revenus services, rétention partenaires, satisfaction client.
- **Source :** `48-LAWIM-SALES-PLAYBOOK.md:284-293`
- **Confiance :** ÉLEVÉE

### NEG-017 : Cibles commerciales (8)
- **Description :** Agences, propriétaires, promoteurs, partenaires, investisseurs, diaspora, entreprises, particuliers.
- **Source :** `48-LAWIM-SALES-PLAYBOOK.md:54-63`
- **Confiance :** ÉLEVÉE

### NEG-018 : 10 peurs acheteurs (pas 12)
- **Description :** Voir section 1.4 ci-dessus pour la liste exhaustive des 10 peurs.
- **Source :** `trust-and-objection-patterns.md:13-26`
- **Confiance :** ÉLEVÉE

### NEG-019 : 7 peurs vendeurs
- **Description :** Acheteurs non sérieux, négociation aggressive, perte de temps, divulgation excessive, vente à perte, arnaque, visibilité insuffisante, mauvaise image du bien.
- **Source :** `trust-and-objection-patterns.md:32-41`
- **Confiance :** ÉLEVÉE

### NEG-020 : 12 objections fréquentes
- **Description :** Dernier prix, titre, visite, écart de prix, agence vs proprio, vidéo, validation sociale, délai salaire, trop questions, pas de baisse, urgence, réponses vagues.
- **Source :** `trust-and-objection-patterns.md:47-61`
- **Confiance :** ÉLEVÉE

### NEG-021 : 10 déclencheurs émotionnels
- **Description :** Visite physique, preuve concrète, cohérence discours, réactivité, recommandation, rareté perçue, projection quartier, transaction rapide après rassurance, patrimoine, réduction effort mental.
- **Source :** `trust-and-objection-patterns.md:66-78`
- **Confiance :** ÉLEVÉE

### NEG-022 : 5 profils prospects (ton uniquement)
- **Description :** Sérieux (accompagner), curieux (question ouverte), méfiant (rassurance), pressé (clarté), fantaisiste (recentrer ou clôturer).
- **Source :** `trust-and-objection-patterns.md:87-94`
- **Confiance :** ÉLEVÉE

---

## 4. Règles Transverses

### TRA-001 : Moteur LAWIM Engine v1 (4 rôles)
- **Description :** 4 rôles utilisateur : buyer, tenant, seller, investor. Détection via intent_detector → scoring → réponse.
- **Source :** `lawim_engine_v1.py:29-34`
- **Confiance :** ÉLEVÉE

### TRA-002 : 5 fichiers d'intention
- **Description :** buy_property.json, rent_property.json, sell_property.json, investor_intent.json, search_property.json.
- **Source :** `intent_detector.py:13-18`
- **Confiance :** ÉLEVÉE

### TRA-003 : 6 types de biens supportés
- **Description :** Appartement, maison, villa, terrain, studio, bureau.
- **Source :** `conversation_memory.py:95-101`
- **Confiance :** ÉLEVÉE

### TRA-004 : Parité des canaux
- **Description :** Les mêmes règles sémantiques s'appliquent à WhatsApp et Telegram. Le dashboard est le canal opérateur.
- **Source :** `omnichannel-playbook.md:9-14`
- **Confiance :** ÉLEVÉE

### TRA-005 : Un seul besoin métier par thread actif
- **Description :** Garder un seul besoin métier par thread actif. Une question de clarification à la fois.
- **Source :** `omnichannel-playbook.md:18-19`
- **Confiance :** ÉLEVÉE

### TRA-006 : Qualification matricielle par type de bien
- **Description :** Matrice de qualification spécifique par type de bien (studio/appartement, maison/villa, terrain, local commercial, meublé, investissement) avec niveaux de détail différents par canal.
- **Source :** `whatsapp-telegram-dashboard-qualification.md:44-51`
- **Confiance :** ÉLEVÉE

### TRA-007 : Lifetime du lead
- **Description :** Inbound → détection langue et intention → qualification du besoin → normalisation entités → score urgence et fit → match ou création suivi → handoff humain si nécessaire → suivi jusqu'à clôture.
- **Source :** `omnichannel-playbook.md:29-38`
- **Confiance :** ÉLEVÉE

---

## 5. Glossaire des seuils et constantes

| Constante | Valeur | Source | Usage |
|-----------|--------|--------|-------|
| Rétention mémoire longue | 365 jours | `long_term_memory.py:92` | Contexte recherche |
| Cycle de relance max | 90 jours (2160h) | `follow_up_system.py:27` | Relance commerciale |
| Seuils de relance | 24h, 168h, 720h, 2160h | `follow_up_system.py:22-28` | Planning relances |
| Taille historique conversation | 50 échanges max | `conversation_memory.py:187-188` | Mémoire courte |
| Niveaux d'accueil retour | 4 (J+1, J+2-7, J+8-30, J+31+) | `conversation_memory.py:136-143` | Personnalisation |
| Anti-spam | 10 msg/min, blocage 60 min | `anti_spam.py:17-18` | Sécurité |
| Budget accompagnement | 50 000 FCFA | `RESPONSE_POLICY.md:17` | Service payant |
| Délai RGPD | 7 jours | `RESPONSE_POLICY.md:19` | Suppression données |
| DeepSeek température | 0.7 | `response_router.py:38` | Génération réponse |
| DeepSeek max_tokens | 500 | `response_router.py:39` | Génération réponse |
| DeepSeek température détection langue | 0.1 | `language_detector_ia.py:48` | Détection langue |
| Langues supportées | 3 (fr, en, pidgin) | Multiples fichiers | Conversation |
| Types de biens | 6 | `conversation_memory.py:95-101` | Recherche |
| Rôles utilisateur | 4 (buyer, tenant, seller, investor) | `lawim_engine_v1.py:29-34` | Scoring |
| Fichiers d'intention | 5 | `intent_detector.py:13-18` | Détection |
| Peurs acheteurs | 10 | `trust-and-objection-patterns.md` | Psychologie |
| Peurs vendeurs | 7 | `trust-and-objection-patterns.md` | Psychologie |
| Objections fréquentes | 12 | `trust-and-objection-patterns.md` | Gestion objections |
| Déclencheurs émotionnels | 10 | `trust-and-objection-patterns.md` | Conversion |
| Profils prospects | 5 | `trust-and-objection-patterns.md` | Ton uniquement |
| Services vendables | 10 | `playbook.md:170-181` | Commercial |
| Objections commerciales | 8 | `playbook.md:186-218` | Commercial |
| KPI commerciaux | 8 | `playbook.md:284-293` | Suivi |
| Étapes processus commercial | 8 | `playbook.md:222-230` | Vente |
| Règles commerciales | 7 | `playbook.md:271-278` | Conformité |
| Cibles commerciales | 8 | `playbook.md:54-63` | Marketing |
| Expressions de négociation | 8 | `negotiation.json:2-11` | Détection |
| Signaux d'urgence | 8 | `urgency_signals.json:2-12` | Détection |
| Ton (ratio) | 70/20/10 | `multilingual-conversation-guidelines.md:44-46` | Voix |
| Emojis max par message | 1-2 | `multilingual-conversation-guidelines.md:25` | Formatage |
| Phrases max par réponse | 1-3 | `conversation-style-guide.md:30` | Formatage |
| États de statut (recommandés) | 7 | `omnichannel-playbook.md:139-147` | Suivi |
| Quartiers premium | 5 (Bastos, Golf, Santa Barbara, Omnisports résidentiel, Mbankomo) | `conversation-patterns.md:268-272` | Qualification |

---

## 6. Anomalies et corrections obligatoires

### A-001 : Camfranglais dans whatsapp_language.json non routé
- **Problème :** Le fichier `whatsapp_language.json` contient des entrées `"language": "camfranglais"` mais aucun module ne les utilise pour le routage ou la réponse.
- **Correction :** Harmoniser : soit ajouter le support complet (détection + templates), soit migrer les expressions camfranglaises vers le pidgin.
- **Priorité :** MOYENNE

### A-002 : Hiérarchie de réponse incomplète
- **Problème :** `response_router.py` mentionne « DeepSeek → Google API → Règles locales → Templates », mais le niveau Google API n'est pas implémenté.
- **Correction :** Soit implémenter, soit corriger la documentation.
- **Priorité :** FAIBLE

### A-003 : Documentation du nombre de peurs à corriger
- **Problème :** Certaines présentations mentionnent « 12 peurs acheteurs » alors que le fichier source en contient 10.
- **Correction :** Remplacer par 10.
- **Priorité :** ÉLEVÉE

### A-004 : Nombre de signaux d'intention à corriger
- **Problème :** Si une source mentionne « 7 signaux d'intention », c'est faux. Il y en a 5.
- **Correction :** Remplacer par 5.
- **Priorité :** ÉLEVÉE

### A-005 : conversation_tone.md manquant
- **Problème :** Le fichier `conversation_tone.md` n'existe pas mais est peut-être référencé.
- **Correction :** Créer le fichier dans le cadre GOLD, ou supprimer les références.
- **Priorité :** MOYENNE

### A-006 : 4 moments clés annuels à supprimer
- **Problème :** Aucun fichier ne documente de moments clés annuels. Cette notion est inventée.
- **Correction :** Supprimer toute référence.
- **Priorité :** ÉLEVÉE

### A-007 : 5 arguments propriétés à supprimer
- **Problème :** Aucun fichier ne liste 5 arguments propriétés. Le playbook liste 6 points dans la section propriétaire.
- **Correction :** Supprimer ou remplacer par les 6 points réels du playbook.
- **Priorité :** ÉLEVÉE

---

## Fichiers audités

| # | Fichier | Domaine | Lignes | Règles extraites |
|---|---------|---------|--------|------------------|
| 1 | `LAWIMA/00_GLOBAL/rules/RESPONSE_POLICY.md` | Conversation | 24 | 1-8, 14-17 |
| 2 | `LAWIMA/03_ENGINE/conversation_memory.py` | Conversation | 211 | 17, 20 |
| 3 | `LAWIMA/03_ENGINE/long_term_memory.py` | Conversation | 101 | 18 |
| 4 | `LAWIMA/03_ENGINE/follow_up_system.py` | Conversation | 113 | 19 |
| 5 | `LAWIMA/03_ENGINE/response_router.py` | Conversation | 69 | 24 |
| 6 | `LAWIMA/03_ENGINE/multilingual_responses.py` | Conversation | 69 | 3 |
| 7 | `LAWIMA/03_ENGINE/feedback_handler.py` | Conversation | 80 | 22 |
| 8 | `LAWIMA/03_ENGINE/deepseek_prompt.txt` | Conversation | 22 | 2, 6, 12, 25 |
| 9 | `LAWIMA/03_ENGINE/lawim_engine_v1.py` | Conversation | 65 | TRA-001 |
| 10 | `LAWIMA/03_ENGINE/language_handler.py` | Conversation | 85 | 3 |
| 11 | `LAWIMA/03_ENGINE/language_detector.py` | Conversation | 67 | 3 |
| 12 | `LAWIMA/03_ENGINE/language_detector_ia.py` | Conversation | 113 | 21 |
| 13 | `LAWIM/KNOWLEDGE/conversation-patterns.md` | Conversation | 306 | 30, 41-44 |
| 14 | `LAWIM/KNOWLEDGE/conversation-style-guide.md` | Conversation | 105 | 8-9, 10, 26-30 |
| 15 | `LAWIM/KNOWLEDGE/multilingual-conversation-guidelines.md` | Conversation | 48 | 4, 11, 28, 45-47 |
| 16 | `LAWIM/KNOWLEDGE/omnichannel-playbook.md` | Conversation | 221 | 33-34, 35, 40, 50 |
| 17 | `LAWIM/KNOWLEDGE/response-policy.md` | Conversation | 60 | 5, 7, 31-33 |
| 18 | `LAWIM/KNOWLEDGE/trust-and-objection-patterns.md` | Négociation | 107 | NEG-018-022 |
| 19 | `LAWIM/KNOWLEDGE/channel-tone-guidelines.md` | Conversation | 46 | 36-38 |
| 20 | `LAWIM/KNOWLEDGE/channels/whatsapp-telegram-dashboard-qualification.md` | Conversation | 183 | 36-39 |
| 21 | `LAWIM/Directive/48-LAWIM-SALES-PLAYBOOK.md` | Négociation | 311 | NEG-012-017 |
| 22 | `LAWIM/KNOWLEDGE/negotiation-patterns.md` | Négociation | 121 | NEG-001-011 |
| 23 | `LAWIMA/02_KNOWLEDGE/whatsapp_language/negotiation.json` | Négociation | 12 | NEG-003 |
| 24 | `LAWIMA/03_ENGINE/anti_spam.py` | Conversation | 76 | 23 |
| 25 | `LAWIMA/03_ENGINE/intent_detector/intent_detector.py` | Conversation | 68 | TRA-002 |
| 26 | `LAWIM/KNOWLEDGE/whatsapp_language/urgency_signals.json` | Négociation | 12 | NEG-011 |
| 27 | `LAWIM/KNOWLEDGE/whatsapp_language/whatsapp_language.json` | Conversation | ~500 | Lexique camfranglais non routé |

---

**Fin du rapport.**

*Ce document est la base de référence GOLD pour les domaines Conversation et Négociation. Toute divergence entre ce rapport et les implémentations doit être résolue en faveur du rapport.*
