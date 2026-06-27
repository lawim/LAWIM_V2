# LAWIM

# 22-OPERATIONS-RUNBOOK.md

# Guide d'exploitation officiel

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le présent document définit les procédures d'exploitation de LAWIM.

Il constitue la référence unique pour :

* le démarrage ;
* l'arrêt ;
* le redémarrage ;
* les sauvegardes ;
* les restaurations ;
* les incidents ;
* l'escalade ;
* la supervision Campay.

---

# CHAPITRE 2 — PRINCIPES FONDAMENTAUX

L'exploitation doit être :

* documentée ;
* reproductible ;
* tracée ;
* réversible ;
* compatible avec le PRA.

Chaque opération critique doit être consignée.

---

# CHAPITRE 3 — DÉMARRAGE

Avant tout démarrage, vérifier :

* l'état d'OVH ;
* le serveur local ;
* PostgreSQL ;
* Redis ;
* Nginx ;
* les secrets ;
* les sauvegardes ;
* l'accessibilité Campay si le paiement est exposé.

---

# CHAPITRE 4 — ARRÊT ET REDÉMARRAGE

L'arrêt doit respecter l'ordre de dépendance.

Le redémarrage doit respecter :

* les services critiques d'abord ;
* les dépendances ensuite ;
* les interfaces enfin ;
* les vérifications post-redémarrage en dernier.

---

# CHAPITRE 5 — SAUVEGARDE ET RESTAURATION

Les opérations de sauvegarde et restauration doivent suivre le référentiel de stockage.

La séquence officielle unique est la suivante :

* Serveur OVH (Production) ;
* synchronisation automatique vers le serveur local ;
* sauvegarde locale ;
* sauvegarde hebdomadaire sur disque externe ;
* synchronisation automatique vers les 9 Google Drive spécialisés ;
* vérification d'intégrité ;
* test automatique de restauration ;
* rapport automatique ;
* notification d'échec.

Cette séquence est la seule référence opérationnelle. Elle doit rester alignée sur 14-STORAGE-REFERENCE.md.

Les restaurations doivent être testées sur :

* un fichier ;
* une base PostgreSQL ;
* un ensemble documentaire ;
* un snapshot ;
* un incident partiel.

---

# CHAPITRE 6 — INCIDENTS INFRASTRUCTURE

Les incidents à traiter comprennent notamment :

* OVH indisponible ;
* base de données indisponible ;
* Google Drive indisponible ;
* disque local défaillant ;
* stockage saturé ;
* déploiement cassé.

Chaque incident doit déclencher une traçabilité et une escalade adaptées.

---

# CHAPITRE 7 — INCIDENTS PAIEMENT CAMPAY

Les incidents Campay comprennent notamment :

* API indisponible ;
* webhook indisponible ;
* webhook frauduleux ;
* paiement confirmé mais non rapproché ;
* divergence entre Campay et LAWIM.

Aucun service ne doit être activé sur la base d'une simple hypothèse.

---

# CHAPITRE 8 — CHECKLIST QUOTIDIENNE

La checklist quotidienne doit vérifier :

* les sauvegardes ;
* les alertes ;
* les erreurs applicatives ;
* les files d'attente ;
* les incidents actifs ;
* l'état des paiements et webhooks.

---

# CHAPITRE 9 — CHECKLIST HEBDOMADAIRE

La checklist hebdomadaire doit vérifier :

* la sauvegarde externe ;
* les tests de restauration ;
* la cohérence documentaire ;
* les incidents récurrents ;
* l'état de santé des intégrations critiques.

---

# CHAPITRE 10 — CHECKLIST APRÈS DÉPLOIEMENT

Après chaque déploiement, vérifier :

* l'accessibilité de l'application ;
* la santé des API ;
* les métriques de base ;
* les webhooks ;
* les paiements ;
* les logs critiques.

---

# CHAPITRE 11 — ESCALADE

L'escalade doit être déclenchée selon la criticité :

* incident mineur ;
* incident majeur ;
* incident bloquant ;
* incident de sécurité ;
* incident de paiement.

Les actions d'escalade doivent être tracées.

---

# CHAPITRE 12 — OBJECTIF FINAL

Le runbook d'exploitation garantit la continuité de service et la gestion structurée des incidents de LAWIM.

# FIN DU DOCUMENT
