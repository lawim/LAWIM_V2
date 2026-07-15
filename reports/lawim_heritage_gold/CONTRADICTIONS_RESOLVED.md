# RAPPORT DE RÉSOLUTION DES CONTRADICTIONS H0.1

**Mission :** H0.1 — Résolution des contradictions et interprétations non marquées
**Date :** 15 juillet 2026
**Statut :** FINAL

---

## CONTRADICTIONS DOCUMENTÉES (H0)

### C1. _archive/ : 61 vs 27 fichiers

| Champ | Valeur |
|-------|--------|
| **Description** | Écart de comptage des fichiers dans `_archive/` entre DATASETS.md et SOURCE_INVENTORY.md |
| **Source A** | `docs/lawim_heritage/DATASETS.md §2.2` — 61 fichiers d'archives |
| **Source B** | `knowledge_unified/sources/SOURCE_INVENTORY.md` — 27 fichiers listés dans _archive/ |
| **Vérification backup** | `LAWIM_BACKUP_20260608_125026/LAWIMA/02_KNOWLEDGE/_archive/` = **61 fichiers** |
| **Analyse** | Le backup réel contient 61 fichiers. SOURCE_INVENTORY.md inventorait un sous-ensemble ou provenait d'un snapshot incomplet. DATASETS.md est correct. |
| **Résolution** | **RÉSOLUE** |
| **Valeur GOLD** | 61 fichiers |

### C2. _repair_backup/ : 84 vs ~60 fichiers

| Champ | Valeur |
|-------|--------|
| **Description** | Écart de comptage des fichiers dans `_repair_backup/` |
| **Source A** | `docs/lawim_heritage/DATASETS.md §2.2` — 84 fichiers de backup de réparation |
| **Source B** | `knowledge_unified/sources/SOURCE_INVENTORY.md` — ~60 fichiers |
| **Vérification backup** | `LAWIM_BACKUP_20260608_125026/LAWIMA/02_KNOWLEDGE/_repair_backup/` = **84 fichiers** |
| **Analyse** | Le backup réel contient 84 fichiers. SOURCE_INVENTORY.md donnait une approximation (~60) basée sur un état partiel. DATASETS.md est correct. |
| **Résolution** | **RÉSOLUE** |
| **Valeur GOLD** | 84 fichiers |

### C3. Volume LAWIMA : ~400 vs ~220 fichiers

| Champ | Valeur |
|-------|--------|
| **Description** | Écart de volume total LAWIMA entre HERITAGE_INDEX.md et SOURCE_INVENTORY.md |
| **Source A** | `docs/lawim_heritage/HERITAGE_INDEX.md §2` — ~400 fichiers pour LAWIMA |
| **Source B** | `knowledge_unified/sources/SOURCE_INVENTORY.md` — ~220 fichiers total toutes branches |
| **Vérification backup** | `LAWIMA/02_KNOWLEDGE/` = 221 fichiers. `LAWIMA/` complet (hors restore copies) = ~2979 fichiers |
| **Analyse** | Les deux sources comptent des périmètres différents : **HERITAGE_INDEX.md** (~400) compte les fichiers de LAWIMA/02_KNOWLEDGE/ + 03_ENGINE/ + 06_AI_MODELS/ + 08_CONFIG/ + 01_DATABASE/ (knowledge + engine + config + IA). **SOURCE_INVENTORY.md** (~220) ne compte que LAWIMA/02_KNOWLEDGE/ (la sous-branche knowledge). Le backup réel de LAWIMA/02_KNOWLEDGE/ contient 221 fichiers, confirmant SOURCE_INVENTORY. Mais le périmètre HERITAGE_INDEX est plus large et inclut les fichiers engine, config, IA et DB (~400), ce qui est plausible mais non vérifiable précisément sans recenser manuellement ces dossiers. |
| **Résolution** | **PARTIELLEMENT RÉSOLUE** — Les périmètres sont différents, les deux chiffres peuvent être corrects dans leur contexte. La valeur ~400 de HERITAGE_INDEX est une estimation haute incluant le knowledge (221) plus les autres branches (engine, config, IA, DB). |
| **Valeur GOLD** | LAWIMA/02_KNOWLEDGE = 221 fichiers. LAWIMA total estimé ~400-500 fichiers (knowledge + engine + config + IA + DB, hors restore copies et venv). |

---

## INTERPRÉTATIONS NON MARQUÉES (H0)

### I1. Camfranglais comme 4e langue supportée

| Champ | Valeur |
|-------|--------|
| **Description** | CONVERSATION_MODEL.md déclare "4 langues supportées : français, anglais, pidgin, camfranglais" |
| **Source A** | `docs/lawim_heritage/CONVERSATION_MODEL.md §1.2` — "4 langues supportées" |
| **Source B** | `LAWIMA/03_ENGINE/language_detector.py`, `language_detector_ia.py`, `multilingual_responses.py`, `language_handler.py` |
| **Vérification code** | **3 langues seulement** dans TOUS les fichiers sources : `fr`, `en`, `pidgin`. `language_detector.py` lignes 8-11 : `KEYWORDS = {"fr": [...], "en": [...], "pidgin": [...]}`. `multilingual_responses.py` ligne 7 : templates `"fr"`, `"en"`, `"pidgin"` uniquement. `language_detector_ia.py` : prompt système "Réponds UNIQUEMENT par le code de langue: fr, en, ou pidgin." |
| **Analyse** | Aucune occurrence de "camfranglais" dans les sources Python du backup LAWIMA. Le fichier `knowledge_unified/language/cameroon_expressions.json` (créé après H0) liste "camfranglais" comme langue mais ne fournit aucune implémentation. La mention "camfranglais" dans `LANGUAGE_MODEL.md` est plus prudente : "Détection limitée dans les expressions". **H0 a interprété la présence de mots camfranglais dans les corpus WhatsApp comme une 4e langue supportée, ce qui est incorrect.** |
| **Résolution** | **RÉSOLUE** — Interprétation non marquée confirmée |
| **Valeur GOLD** | 3 langues supportées : français, anglais, pidgin camerounais. Camfranglais n'est PAS une langue supportée. Il peut y avoir des expressions camfranglaises dans les corpus, mais pas de détection/réponse dédiée. |

### I2. 10 statuts de paiement

| Champ | Valeur |
|-------|--------|
| **Description** | PROPERTY_MODEL.md §10 déclare "Dix statuts de paiement identifiés dans le code de monétisation" |
| **Source A** | `docs/lawim_heritage/PROPERTY_MODEL.md §10` — "Dix statuts de paiement" |
| **Source B** | `LAWIMA/core/monetisation.py` |
| **Vérification code** | Statuts trouvés dans monetisation.py : **purchase** (completed, pending, expired — 3), **invoice** (paid, pending — 2), **subscription** (active, expired — 2). Total : **7 statuts uniques** répartis sur 3 tables différentes, pas une liste de 10 statuts de paiement. |
| **Analyse** | Aucune liste de "10 statuts de paiement" n'existe dans le code. H0 a probablement additionné tous les statuts possibles de toutes les entités (purchases, invoices, subscriptions, agents, services) pour arriver à 10. Cette interprétation est une reconstruction, pas une donnée source. |
| **Résolution** | **RÉSOLUE** — Interprétation non marquée confirmée |
| **Valeur GOLD** | Il n'existe PAS "10 statuts de paiement". Les statuts réels dans monetisation.py sont : purchase→completed/pending/expired ; invoice→paid/pending ; subscription→active/expired. Soit 7 valeurs d'énumération réparties sur 3 tables. |

---

## AUTRES POINTS VÉRIFIÉS

### P1. Rétention mémoire : 90 jours (H0) vs 365 jours (H0.1)

| Champ | Valeur |
|-------|--------|
| **Description** | CONVERSATION_MODEL.md §3.2 : "Durée de rétention : 90 jours (configurable dans `forget_after_days`)" |
| **Source A** | `docs/lawim_heritage/CONVERSATION_MODEL.md §3.2` — 90 jours, paramètre `forget_after_days` |
| **Source B** | `LAWIMA/03_ENGINE/long_term_memory.py` + `LAWIMA/06_AI_MODELS/memory/memory_rules_v1.json` |
| **Vérification code** | **Deux sources distinctes :** — (a) `long_term_memory.py` ligne 92 : `if days_ago < 365:` → 365 jours codé en dur. PAS de paramètre `forget_after_days`. — (b) `memory_rules_v1.json` ligne 19 : `"forget_after_days": 90` → Le paramètre existe DANS LA CONFIG IA, mais n'est PAS LU par le code Python. |
| **Analyse** | Le code (`long_term_memory.py`) utilise 365 jours en dur. Le paramètre `forget_after_days: 90` existe dans la config IA (`memory_rules_v1.json`) mais n'est pas implémenté dans le moteur d'exécution. H0 a correctement rapporté la valeur de la config IA (90) mais a mentionné à tort un paramètre `forget_after_days` dans `long_term_memory.py` alors qu'il n'y est pas. |
| **Résolution** | **RÉSOLUE** |
| **Valeur GOLD** | Rétention code : **365 jours** (hardcodé dans `long_term_memory.py`). Config IA : `forget_after_days: 90` (dans `memory_rules_v1.json`, non utilisé par le code). La valeur réelle exécutée est 365 jours. La valeur intentionnelle (config) est 90 jours. |

### P2. 12 peurs acheteurs (H0) vs 10 (H0.1)

| Champ | Valeur |
|-------|--------|
| **Description** | CONVERSATION_MODEL.md §11 et NEGOTIATION_MODEL.md §3.1 déclarent "12 peurs acheteurs" |
| **Source A** | `docs/lawim_heritage/CONVERSATION_MODEL.md §11` + `NEGOTIATION_MODEL.md §3.1` — 12 peurs |
| **Source B** | `LAWIM/KNOWLEDGE/trust-and-objection-patterns.md §1` — 10 peurs explicitement listées dans le tableau |
| **Vérification source** | Le document source liste **10 peurs** dans la section 1 (Fraude, Paiement anticipé, Faux propriétaire, Dossier juridique, Conflits familiaux, Zone enclavée, Vendeur peu crédible, Mauvaise affaire, Frais cachés, Curiosité). NEGOTIATION_MODEL.md en a ajouté 2 : "Délais trop longs" et "Changement d'avis du vendeur". |
| **Analyse** | Les 2 peurs supplémentaires (délais, changement d'avis) sont dérivées des objections (section 3 du source) mais ne sont PAS listées comme "peurs des acheteurs" dans le document source. H0 a fusionné les objections et les peurs pour arriver à 12. |
| **Résolution** | **RÉSOLUE** — Interprétation non marquée |
| **Valeur GOLD** | 10 peurs acheteurs documentées dans `trust-and-objection-patterns.md`. Les 2 supplémentaires sont des objections, pas des peurs. |

### P3. conversation_tone.md : existe ou pas ?

| Champ | Valeur |
|-------|--------|
| **Description** | NEGOTIATION_MODEL.md §6 référence `LAWIM/KNOWLEDGE/commercial/conversation_tone.md` |
| **Source A** | `docs/lawim_heritage/NEGOTIATION_MODEL.md §6` — référence à `commercial/conversation_tone.md` |
| **Source B** | Backup LAWIM : `LAWIM/KNOWLEDGE/commercial/` n'existe PAS. Fichier `conversation_tone.md` introuvable dans tout le backup. |
| **Vérification** | Le fichier existe dans `LAWIM_V2/knowledge_unified/commercial/conversation_tone.md` (créé post-H0) mais PAS dans le backup original. Les sources déclarées dans ce fichier (`conversation-style-guide.md`, `channel-tone-guidelines.md`, `conversation-humanization-rules.md`) existent bien dans le backup LAWIM/KNOWLEDGE/. |
| **Analyse** | `conversation_tone.md` est une reconstruction synthétique créée dans `knowledge_unified/` à partir de sources originales. Il n'existait PAS dans le backup LAWIM. H0 a référencé ce fichier comme s'il était une source originale, ce qui est incorrect. |
| **Résolution** | **RÉSOLUE** |
| **Valeur GOLD** | `conversation_tone.md` n'existe PAS dans le backup original. Le fichier `knowledge_unified/commercial/conversation_tone.md` est un artefact de reconstruction. Les sources originales équivalentes sont : `conversation-style-guide.md`, `channel-tone-guidelines.md`, `conversation-humanization-rules.md`. |

### P4. Messages de relance J30/J90 : correspondent-ils au code ?

| Champ | Valeur |
|-------|--------|
| **Description** | CONVERSATION_MODEL.md §4.2 et NEGOTIATION_MODEL.md §7.2 décrivent des messages de relance |
| **Source A** | `docs/lawim_heritage/CONVERSATION_MODEL.md §4.2` + `NEGOTIATION_MODEL.md §7.2` — messages en langage naturel |
| **Source B** | `LAWIMA/03_ENGINE/follow_up_system.py` lignes 23-28 — messages réels du code |
| **Vérification code** | **Messages code (follow_up_system.py) :** — 24h (J1) : "🏠 *Toujours intéressé ?* De nouveaux biens sont disponibles !\n\nRépondez 'OUI' pour que je relance votre recherche." — 168h (J7) : "📊 *Votre recherche LAWIM* - 7 jours\n\nNous avons ajouté 5 nouveaux biens dans votre zone.\n\n👉 Envoyez 'RECHERCHE' pour les voir." — 720h (J30) : "🎁 *Offre spéciale* - 30 jours\n\n1 mois de recherche prioritaire GRATUIT pour vous.\n\n👉 Envoyez 'PRIORITAIRE' pour activer." — 2160h (J90) : "🏆 *LAWIM* - 90 jours\n\n500+ demandes traitées ce trimestre.\n\n👉 Envoyez 'RELANCER' pour reprendre votre recherche." **Messages CONVERSATION_MODEL.md :** messages génériques sans commandes. **Messages NEGOTIATION_MODEL.md :** messages conversationnels "Bonjour [nom]..." avec variantes. |
| **Analyse** | Aucun des deux documents H0 ne correspond aux messages réels du code. Les vrais messages sont des templates WhatsApp avec emojis et commandes actionnables (OUI, RECHERCHE, PRIORITAIRE, RELANCER). Les seuils (24h→J1, 168h→J7, 720h→J30, 2160h→J90) sont corrects dans les deux docs. |
| **Résolution** | **NON RÉSOLUE** — Les messages documentés ne correspondent pas au code. Le mapping temporel (J1/J7/J30/J90 ↔ 24h/168h/720h/2160h) est correct, mais le contenu textuel est différent. |
| **Valeur GOLD** | Seuils corrects : 24h(J1), 168h(J7), 720h(J30), 2160h(J90). Messages réels = ceux de `follow_up_system.py` avec commandes OUI/RECHERCHE/PRIORITAIRE/RELANCER. Les messages des docs H0 sont des reformulations. |

### P5. Moments clés annuels : existent-ils dans le playbook ?

| Champ | Valeur |
|-------|--------|
| **Description** | NEGOTIATION_MODEL.md §2.3 : "Périodes de forte activité identifiées dans le playbook" |
| **Source A** | `docs/lawim_heritage/NEGOTIATION_MODEL.md §2.3` — 4 moments clés annuels présentés comme issus du playbook |
| **Source B** | `LAWIM/Directive/48-LAWIM-SALES-PLAYBOOK.md` |
| **Vérification** | Le playbook (311 lignes) ne contient AUCUNE mention de moments clés annuels, de saisonnalité, de calendrier commercial, de périodes de transferts diaspora, de rentrée scolaire, de saison sèche, ou de fin d'année. La grep de "Fin d'année|Rentrée scolaire|Saison sèche|moments clés" dans tout le backup LAWIM retourne zéro résultat. |
| **Analyse** | Les 4 moments clés annuels sont une **invention complète** de H0. Ils n'existent dans aucun document source du backup. Bien que plausibles d'un point de vue métier, ils ne sont pas documentés dans les sources patrimoniales. |
| **Résolution** | **RÉSOLUE** — Interprétation non marquée (fabrication) |
| **Valeur GOLD** | Les moments clés annuels ne sont PAS documentés dans les sources backup. Ils peuvent être considérés comme une recommandation métier mais PAS comme un fait patrimonial. Aucune valeur GOLD à retenir. |

---

## RÉCAPITULATIF

| ID | Type | Statut | Valeur GOLD |
|----|------|--------|-------------|
| C1 | Contradiction _archive | **RÉSOLUE** | 61 fichiers |
| C2 | Contradiction _repair_backup | **RÉSOLUE** | 84 fichiers |
| C3 | Contradiction volume LAWIMA | **PARTIELLEMENT RÉSOLUE** | 02_KNOWLEDGE=221, total ~400-500 |
| I1 | Interprétation camfranglais | **RÉSOLUE** | 3 langues (fr, en, pidgin) |
| I2 | Interprétation 10 statuts | **RÉSOLUE** | 7 statuts sur 3 tables |
| P1 | Rétention mémoire 90 vs 365 | **RÉSOLUE** | Code=365j, Config IA=90j |
| P2 | 12 vs 10 peurs acheteurs | **RÉSOLUE** | 10 peurs documentées |
| P3 | conversation_tone.md | **RÉSOLUE** | N'existe pas dans backup |
| P4 | Messages J30/J90 | **NON RÉSOLUE** | Messages docs ≠ code |
| P5 | Moments clés annuels | **RÉSOLUE** | Aucune source, fabrication H0 |

**Total :** 10 points analysés — 7 RÉSOLUES, 1 PARTIELLEMENT RÉSOLUE, 1 NON RÉSOLUE, 1 fabrication identifiée.

---

*Rapport généré le 15 juillet 2026 — Résolveur de contradictions H0.1*
