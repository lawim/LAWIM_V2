# LAWIM

# 33-CODEX-IMPLEMENTATION-RULES.md

# Règles d'implémentation pour Codex

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le présent document encadre le travail de Codex sur LAWIM.

---

# CHAPITRE 2 — RÈGLES ABSOLUES

Codex ne doit jamais :

* développer plusieurs moteurs simultanément ;
* modifier plusieurs couches techniques dans un même ticket ;
* réécrire des fichiers sans rapport ;
* supprimer une fonctionnalité existante ;
* contourner la validation humaine ;
* modifier un référentiel sans justification.

---

# CHAPITRE 3 — RESPONSABILITÉ

Un ticket doit correspondre à :

* une responsabilité ;
* une fonctionnalité ;
* un objectif mesurable ;
* des tests ;
* un résultat vérifiable.

---

# CHAPITRE 4 — DISCIPLINE DE CODE

Codex doit :

* préserver la cohérence documentaire ;
* limiter le périmètre des changements ;
* documenter les hypothèses ;
* proposer des sauvegardes ou rollbacks lorsque nécessaire ;
* garder la terminologie officielle.
* conserver le périmètre transverse du tracking marketing sans créer de moteur supplémentaire.

---

# CHAPITRE 5 — OBJECTIF FINAL

Ces règles garantissent que Codex implémente LAWIM sans créer d'ambiguïté ni dette documentaire inutile.

Elles s'appliquent aussi aux lots d'implémentation liés au tracking marketing, à l'attribution et aux statistiques, sans remise en cause des décisions déjà validées.

---

# CHAPITRE 6 — TICKET EXECUTOR

Le Ticket Executor est le point d'entree unique de traitement des tickets LAWIM_V2.

Il lit le ticket, les regles applicables, le PCC, le workflow, les dependances, les livrables et les historiques avant toute action.

Il reutilise l'existant, implemente uniquement le perimetre du ticket, prepare le rapport standard et produit les traces necessaires pour le PCC, les historiques et la preparation Git.

Il ne lance jamais Git, ne modifie jamais la gouvernance, le Bootstrap Pack, la Constitution ou les regles metier, et ne saute jamais une etape du workflow.

Le detail operationnel est defini dans `49-TICKET-EXECUTOR-REFERENCE.md`.
