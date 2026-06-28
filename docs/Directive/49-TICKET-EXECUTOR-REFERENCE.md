# LAWIM

# 49-TICKET-EXECUTOR-REFERENCE.md

# Reference Ticket Executor

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le Ticket Executor est le point d'entree unique de traitement des tickets LAWIM_V2.

Il transforme un ticket en execution controlee, en rapport standard, en traces PCC et History, et en preparation Git, sans executer Git.

---

# CHAPITRE 2 — ROLE

Le Ticket Executor doit toujours :

* lire le ticket source ;
* lire les regles applicables ;
* lire le PCC ;
* lire le workflow officiel ;
* identifier les dependances ;
* identifier les livrables ;
* verifier si des elements existent deja ;
* reutiliser l'existant ;
* implementer uniquement le perimetre du ticket ;
* respecter les conventions du projet ;
* verifier les criteres d'acceptation ;
* produire un rapport d'execution standard ;
* preparer la mise a jour du PCC ;
* preparer la mise a jour des historiques ;
* preparer la mise a jour du statut du ticket ;
* preparer les informations pour le commit Git sans executer Git ;
* preparer le contexte du ticket suivant ;
* s'arreter.

---

# CHAPITRE 3 — SOURCES OBLIGATOIRES

Le Ticket Executor s'appuie au minimum sur :

* le ticket source ;
* `.lawim/pcc/PCC.md` ;
* `.lawim/workflows/ticket-workflow.md` ;
* `.lawim/status/ticket-status.md` ;
* `.lawim/status/sprint-status.md` ;
* `.lawim/history/*.md` ;
* `templates/ticket-template.md` ;
* `templates/ticket-execution-report-template.md` ;
* `docs/Directive/05-WORKFLOW-REFERENCE.md` ;
* `docs/Directive/27-TRACEABILITY-MATRIX.md` ;
* `docs/Directive/33-CODEX-IMPLEMENTATION-RULES.md` ;
* `docs/Directive/38-GIT-STRATEGY.md` ;
* `docs/Directive/41-OPERATIONAL-PROCEDURES.md` ;
* les documents metier directement concernes par le ticket.

---

# CHAPITRE 4 — LIVRABLES

Chaque execution doit preparer :

* un rapport d'execution standard ;
* la liste des fichiers crees ;
* la liste des fichiers modifies ;
* la liste des fichiers reutilises ;
* une note de mise a jour PCC ;
* une note de mise a jour History ;
* une validation des criteres d'acceptation ;
* une proposition de message Git ;
* une proposition de tag recommande si applicable ;
* le contexte du ticket suivant ;
* un statut propose du ticket.

---

# CHAPITRE 5 — INTEGRATION PCC

Le Ticket Executor ne remplace pas le PCC.

Il doit en preparer les mises a jour et y laisser une trace exploitable, notamment pour :

* les decisions ;
* les validations ;
* les dependances ;
* les risques ;
* les references de ticket.

Le Ticket Executor ne modifie jamais le workflow officiel, la gouvernance ou les regles metier.

---

# CHAPITRE 6 — INTEGRATION WORKFLOW

Le Ticket Executor suit le workflow officiel des tickets :

BROUILLON -> VALIDE DG -> PLANIFIE -> ASSIGNE -> EN COURS -> REVUE ARCHITECTE -> REVUE QA -> REVUE SECURITY -> INTEGRATION -> VALIDATION DG -> FERME

Il ne saute aucune etape.

Si une decision de gouvernance est necessaire, le Ticket Executor s'arrete et remonte au Directeur General.

---

# CHAPITRE 7 — INTEGRATION HISTORY

Les historiques sont append-only.

Le Ticket Executor doit preparer les mises a jour factuelles, datees et traceables des journaux concernes, notamment :

* release-history ;
* decision-log ;
* architecture-log ;
* risk-history.

Il ne re-ecrit pas l'historique et ne supprime aucune trace.

---

# CHAPITRE 8 — PREPARATION GIT

Le Ticket Executor ne lance jamais Git.

Il prepare uniquement :

* les chemins de `git add` ;
* le message de commit ;
* le tag recommande, si applicable.

---

# CHAPITRE 9 — LIMITES

Le Ticket Executor ne peut jamais :

* ouvrir un ticket ;
* fermer un ticket ;
* modifier la gouvernance ;
* modifier le Bootstrap Pack ;
* modifier la Constitution ;
* modifier les regles metier ;
* modifier le perimetre d'un ticket ;
* inventer une nouvelle regle ;
* executer Git.

---

# CHAPITRE 10 — OBJECTIF FINAL

Le Ticket Executor garantit une execution unique, tracee, reutilisable et compatible avec le PCC, le workflow et les historiques de LAWIM_V2.

# FIN DU DOCUMENT
