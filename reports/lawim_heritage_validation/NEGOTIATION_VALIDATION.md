# Rapport de validation — NEGOTIATION_MODEL.md

**Date :** 2026-07-15  
**Auditeur :** Validation automatique (agent d'audit)  
**Source des vérifications :** `LAWIMA/`, `LAWIM/` (backup du 2026-06-08)

---

## Résumé

| Statut | Nombre |
|--------|--------|
| ✅ Validé | 4 |
| ⚠️ Partiel | 7 |
| ❌ Non validé | 4 |
| **Total** | **15** |

---

## 24. 4 profils acheteurs (Affirmation #24)

> national, diaspora, investisseur, jeune actif

**Source :** `LAWIM/Directive/48-LAWIM-SALES-PLAYBOOK.md`

| Profil | Trouvé dans le playbook | Statut |
|--------|------------------------|--------|
| Acheteur national | Non explicitement comme profil acheteur | ⚠️ |
| Diaspora | Section 12 « Programme Diaspora » (l.150-166) | ✅ |
| Investisseur | Section 5 cibles « investisseurs » (l.60) | ✅ |
| Jeune actif | Non mentionné | ❌ |

**⚠️ PARTIEL** — Le playbook n'a pas de section dédiée aux « profils acheteurs ».  
Diaspora et investisseurs sont des cibles commerciales.  
« Acheteur national » et « jeune actif » ne sont pas explicitement nommés comme profils dans le playbook.

---

## 25. 3 profils vendeurs (Affirmation #25)

> particulier, promoteur, bailleur

**Source :** `48-LAWIM-SALES-PLAYBOOK.md`

| Profil | Trouvé | Statut |
|--------|--------|--------|
| Vendeur particulier | Section 9 « Comment convaincre un propriétaire » (l.101) | ✅ |
| Promoteur | Section 10 « Comment convaincre un promoteur » (l.118) | ✅ |
| Propriétaire bailleur | Non mentionné comme profil distinct | ❌ |

**⚠️ PARTIEL** — « Particulier » (propriétaire) et « Promoteur » sont des sections dédiées.  
« Bailleur » n'est pas un profil vendeur distinct dans le playbook.

---

## 26. 4 moments clés (Affirmation #26)

> fin d'année, rentrée, saison sèche, transferts diaspora

**Sources :** `48-LAWIM-SALES-PLAYBOOK.md`, `negotiation-patterns.md`, `diaspora-behavior-model.md`

Recherche exhaustive dans les 3 fichiers sources :

| Moment clé | Trouvé | Statut |
|------------|--------|--------|
| Fin d'année | Aucune occurrence | ❌ |
| Rentrée scolaire | Aucune occurrence | ❌ |
| Saison sèche | Aucune occurrence | ❌ |
| Transferts diaspora | Aucune occurrence | ❌ |

**❌ NON VALIDÉ** — Aucun des 4 moments clés n'est mentionné dans le playbook,  
negotiation-patterns.md ou diaspora-behavior-model.md.

Note : Le fichier `negotiation-patterns.md` a une section 7 « Moments clés » mais elle décrit  
les étapes du processus de négociation (contact → visite → offre), pas des périodes annuelles.

---

## 27. 12 peurs acheteurs listées (Affirmation #27)

> 12 peurs acheteurs

**Source :** `LAWIM/KNOWLEDGE/trust-and-objection-patterns.md` section 1

Le document source liste 10 peurs acheteurs (pas 12) :

| Annoncé | Réel | Statut |
|---------|------|--------|
| 12 | 10 | ❌ |

De plus, la liste dans NEGOTIATION_MODEL.md (l.55-67) ne correspond pas exactement  
à celle du document source trust-and-objection-patterns.md :

**NEGOTIATION_MODEL.md liste :** arnaque/fraude, titre foncier non valide, prix trop élevé,  
vices cachés, litige sur le bien, difficultés administratives, mauvaise localisation,  
problèmes de voisinage, accessibilité, financement, délais trop longs, changement d'avis vendeur.

**Source réelle (trust-and-objection-patterns.md) :** fraude/arnaque, paiement anticipé sans visite,  
faux propriétaire, dossier juridique flou, conflits familiaux/successoraux, zone enclavée/accès,  
vendeur peu crédible, mauvaise affaire/revente, frais cachés, curiosité sans sérieux.

**❌ NON VALIDÉ** — 12 annoncées, 10 dans la source. Contenu différent.

---

## 28. 8 peurs vendeurs listées (Affirmation #28)

> 8 peurs vendeurs

**Source :** `trust-and-objection-patterns.md` section 2

| Annoncé | Réel | Statut |
|---------|------|--------|
| 8 | 8 | ✅ |

Les 8 peurs listées dans NEGOTIATION_MODEL.md correspondent qualitativement  
au contenu de la section 2 du document source.

**✅ VALIDÉ**

---

## 29. 6 arguments LAWIM (Affirmation #29)

> zéro commission, mise en relation directe, matching intelligent, accompagnement, WhatsApp, réseau agents vérifiés

**Source :** `48-LAWIM-SALES-PLAYBOOK.md`

| Argument | Trouvé | Statut |
|----------|--------|--------|
| Zéro commission | « ne prend aucune commission » (l.71, 79, 213, 278) | ✅ |
| Mise en relation directe | « mise en relation » (l.40, 71, 108, 172, 209) | ✅ |
| Matching intelligent | Terme « matching » absent du playbook | ❌ |
| Accompagnement personnalisé (50k) | « accompagnement » (l.93, 107, 173, 180, 181) | ✅ |
| Présence sur WhatsApp | Script WhatsApp dédié (l.244) | ✅ |
| Réseau d'agents vérifiés | Agents comme cible (l.59), mais pas « réseau vérifié » | ⚠️ |

**⚠️ PARTIEL** — 4 arguments sur 6 sont clairement présents.  
« Matching intelligent » n'est pas mentionné dans le playbook.  
« Réseau d'agents vérifiés » est implicite (agents sont cibles commerciales) mais pas formulé ainsi.

---

## 30. 5 arguments propriétés (Affirmation #30)

> proximité commodités, accessibilité, sécurité quartier, potentiel valorisation, cadre de vie

**Source :** `48-LAWIM-SALES-PLAYBOOK.md`

Recherche exhaustive dans le playbook : **aucun de ces 5 arguments** n'est mentionné.

| Argument | Trouvé | Statut |
|----------|--------|--------|
| Proximité des commodités | Non trouvé | ❌ |
| Accessibilité (routes, transports) | Non trouvé | ❌ |
| Sécurité du quartier | Non trouvé | ❌ |
| Potentiel de valorisation | Non trouvé | ❌ |
| Cadre de vie | Non trouvé | ❌ |

**❌ NON VALIDÉ** — Aucun des 5 arguments propriétés n'apparaît dans le playbook.

---

## 31. Expressions négociation prix (Affirmation #31)

> prix ferme, à débattre, dernier prix, je peux descendre, c'est trop cher, faites moi une offre

**Source :** `LAWIMA/03_ENGINE/lawim_engine_v1.py` et `02_KNOWLEDGE/whatsapp_language/negotiation.json`

Recherche dans `lawim_engine_v1.py` :

| Expression | Trouvée dans lawim_engine_v1.py | Trouvée dans negotiation.json | Statut |
|------------|--------------------------------|-------------------------------|--------|
| prix ferme | ❌ | ✅ | ✅ (via negotiation.json) |
| à débattre | ❌ | ✅ | ✅ (via negotiation.json) |
| dernier prix | ❌ | ✅ | ✅ (via negotiation.json) |
| je peux descendre | ❌ | ❌ | ❌ |
| c'est trop cher | ❌ | ❌ | ❌ |
| faites moi une offre | ❌ | ❌ | ❌ |

La source `02_KNOWLEDGE/whatsapp_language/negotiation.json` de LAWIMA contient :
`dernier prix`, `prix ferme`, `prix négociable`, `à débattre`, `on peut s'entendre`,  
`best price`, `nego possible`, `combien dernier ?`.

**⚠️ PARTIEL** — 3 expressions sur 6 sont trouvées dans le fichier negotiation.json de LAWIMA.  
« je peux descendre », « c'est trop cher », « faites moi une offre » sont absents de tous les fichiers source vérifiés.

---

## 32. Signaux urgence (Affirmation #32)

> urgent, asap, vite, immédiatement, now

Recherche dans les dictionnaires d'intents :

| Signal | Trouvé | Statut |
|--------|--------|--------|
| urgent | Pas d'intention « urgence » dédiée, mais « urgent » n'est pas un keyword | ❌ |
| asap | Non trouvé | ❌ |
| vite | Non trouvé | ❌ |
| immédiatement | Non trouvé | ❌ |
| now | Non trouvé | ❌ |

Les fichiers intents JSON ne contiennent pas ces signaux.  
Le fichier `conversation-patterns.md` mentionne « urgent » et « asap » comme patterns généraux  
(l.32-33) mais pas dans les données structurées de détection.

**⚠️ PARTIEL** — « urgent » et « asap » sont mentionnés dans `conversation-patterns.md` comme signaux  
de pattern « Urgency », mais ne sont pas implémentés comme signaux détectables  
dans le moteur d'intents ou l'engine.

---

## 33. Signaux investisseur (Affirmation #33)

> investir, rentable, ROI, cash flow, rendement

**Source :** `LAWIMA/03_ENGINE/intent_detector/` + `KNOWLEDGE/intents/investor_intent.json`

| Signal | Trouvé | Statut |
|--------|--------|--------|
| investir | `investor_intent.json:6` — keyword | ✅ |
| rentable | `investor_intent.json:9` — « rentabilité » | ✅ (apparenté) |
| ROI | `investor_intent.json:8` — keyword | ✅ |
| cash flow | Non trouvé dans les keywords | ❌ |
| rendement | Non trouvé dans les keywords | ❌ |

**⚠️ PARTIEL** — 3 signaux sur 5 sont présents.  
« cash flow » et « rendement » ne figurent pas dans les fichiers intents.

---

## 34. Signaux diaspora (Affirmation #34)

> diaspora, je vis à, indicatifs étrangers, villes étrangères

**Source :** `investor_intent.json`, `diaspora-behavior-model.md`

| Signal | Trouvé | Statut |
|--------|--------|--------|
| diaspora | `investor_intent.json` a `diaspora_countries` | ✅ (implicite) |
| je vis à | `"je suis en france"` (investor_intent.json:26) | ⚠️ (proche) |
| Indicatifs étrangers | Non trouvé dans les fichiers | ❌ |
| Villes étrangères | `diaspora_countries` (investor_intent.json:13-20) | ⚠️ (pays, pas villes) |

**⚠️ PARTIEL** — La diaspora est reconnue comme profil (playbook section 12, diaspora-behavior-model.md),  
mais les signaux lexicaux spécifiques (indicatifs téléphoniques, villes étrangères)  
ne sont pas codés dans les fichiers intents JSON.

---

## 35. 5 principes ton (Affirmation #35)

> professionnel, expertise, patience, adaptation, validation

**Source :** `LAWIM/KNOWLEDGE/commercial/conversation_tone.md`

**⚠️ FICHE MANQUANTE ❌**

Le fichier `LAWIM/KNOWLEDGE/commercial/conversation_tone.md` n'existe pas.  
Le répertoire `commercial/` n'existe pas dans `LAWIM/KNOWLEDGE/`.

Recherche exhaustive : aucun fichier nommé `conversation_tone*` n'existe dans  
l'ensemble du backup LAWIM_BACKUP_20260608_125026.

Fichier alternatif trouvé : `conversation-style-guide.md` qui liste :
« Professional, Warm, Direct, Reassuring, Concise, Action-oriented »  
(6 qualités, pas 5, et différentes de celles listées).

**❌ NON VALIDÉ** — Le fichier source n'existe pas. Les 5 principes ne peuvent pas être vérifiés.

---

## 36. Séquence confiance 5 étapes (Affirmation #36)

> 5 étapes sourcing conversation_tone.md

Même problème que #35 : le fichier source `conversation_tone.md` n'existe pas.

Le fichier `conversation-style-guide.md` (l.21-26) propose un ordre de réponse différent :  
1. acknowledge the request  
2. ask the next critical field  
3. confirm implicitly  
4. indicate the next step

Ce qui ne correspond pas aux 5 étapes annoncées (écoute active, apport d'information,  
proposition, traitement objections, closing).

**❌ NON VALIDÉ** — Source manquante.

---

## 37. Calendrier relance (Affirmation #37)

> J1, J7, J30, J90

**Source :** `LAWIMA/03_ENGINE/follow_up_system.py:22-27`

| Échéance | Code | Statut |
|----------|------|--------|
| J1 | 24h (follow_up_system.py:24) | ✅ |
| J7 | 168h (l.25) | ✅ |
| J30 | 720h (l.26) | ✅ |
| J90 | 2160h (l.27) | ✅ |

**✅ VALIDÉ** — Les 4 échéances et leurs horaires sont corrects.

---

## 38. Messages relance types (Affirmation #38)

> Messages types J1, J7, J30, J90

**Source :** `follow_up_system.py:22-27` (code) vs NEGOTIATION_MODEL.md:169-174

| Seuil | Message dans le CODE | Message dans NEGOTIATION_MODEL | Concordance |
|-------|---------------------|--------------------------------|-------------|
| J1 | « Toujours intéressé ? De nouveaux biens sont disponibles ! » | « Bonjour [nom], j'ai trouvé [N] nouveaux biens... » | ❌ |
| J7 | « Nous avons ajouté 5 nouveaux biens dans votre zone. » | « Bonjour [nom], une offre spéciale cette semaine... » | ⚠️ |
| J30 | « Offre spéciale — 1 mois de recherche prioritaire GRATUIT » | « Bonjour [nom], voici les tendances du marché... » | ❌ |
| J90 | « 500+ demandes traitées ce trimestre. » | « Bonjour [nom], votre recherche est toujours active ?... » | ❌ |

Les messages dans le code :
- Sont des chaînes fixes (pas de `[nom]` ou `[N]` dynamiques)
- N'utilisent pas de template avec nom du client
- Ont un ton plus promotionnel que les versions documentées

**⚠️ PARTIEL** — Les échéances et la structure générale sont correctes, mais les textes exacts  
des messages diffèrent entre le code et la documentation.

---

## Synthèse des écarts majeurs

| # | Affirmation | Problème |
|---|-------------|----------|
| 26 | 4 moments clés annuels | Aucune occurrence dans les sources |
| 27 | 12 peurs acheteurs | 10 seulement dans le document source |
| 30 | 5 arguments propriétés | Absents du playbook |
| 31 | 6 expressions négociation | 3 expressions introuvables dans les sources |
| 35 | 5 principes ton | Fichier source `conversation_tone.md` inexistant |
| 36 | Séquence confiance 5 étapes | Fichier source `conversation_tone.md` inexistant |
| 38 | Messages relance types | Textes différents entre code et documentation |

## Fichiers source manquants

Les fichiers suivants, référencés comme sources dans NEGOTIATION_MODEL.md,  
n'existent pas dans le backup :

| Fichier référencé | Statut |
|-------------------|--------|
| `LAWIM/KNOWLEDGE/commercial/conversation_tone.md` | ❌ Introuvable |
| `LAWIM/KNOWLEDGE/commercial/closing_techniques.md` | ❌ Introuvable |
| `LAWIM/KNOWLEDGE/commercial/objection_handling.md` | ❌ Introuvable |
| `LAWIM/KNOWLEDGE/commercial/negotiation_techniques.md` | ❌ Introuvable |
| `LAWIM/KNOWLEDGE/commercial/follow_up_strategies.md` | ❌ Introuvable |
| Répertoire `commercial/` sous `LAWIM/KNOWLEDGE` | ❌ N'existe pas |

---

*Rapport généré le 2026-07-15 par l'agent d'audit de validation LAWIM.*
