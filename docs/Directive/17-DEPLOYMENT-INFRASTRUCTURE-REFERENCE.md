# LAWIM

# 17-DEPLOYMENT-INFRASTRUCTURE-REFERENCE.md

# Référentiel officiel de déploiement et d'infrastructure

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le présent document définit les règles officielles d'infrastructure et de déploiement de LAWIM.

Il constitue la référence unique pour :

* OVH ;
* les environnements Dev, Test, Staging et Production ;
* Docker ;
* Nginx ;
* PostgreSQL ;
* PostGIS ;
* Redis ;
* les sauvegardes ;
* la supervision des paiements.

---

# CHAPITRE 2 — ARCHITECTURE CIBLE

L'architecture officielle suit l'ordre suivant :

* OVH en production ;
* serveur local pour la continuité et les synchronisations ;
* disque externe pour la sauvegarde hebdomadaire ;
* 9 Google Drive spécialisés ;
* archivage intelligent piloté par le Storage Lifecycle Manager.

Cette architecture doit être documentée et testée.

---

# CHAPITRE 3 — ENVIRONNEMENTS

Les environnements officiels sont :

* Development ;
* Test ;
* Staging ;
* Production.

Chaque environnement doit être isolé, configuré explicitement et protégé par des secrets distincts.

---

# CHAPITRE 4 — STACK TECHNIQUE

Le déploiement doit s'appuyer sur :

* Docker ;
* Nginx ;
* PostgreSQL ;
* PostGIS ;
* Redis ;
* Node.js ;
* outils de migration ;
* outils de supervision.

Les versions doivent être maîtrisées et documentées.

---

# CHAPITRE 5 — CONFIGURATION ET SECRETS

Les variables d'environnement doivent être :

* clairement nommées ;
* séparées par environnement ;
* documentées ;
* non commitées en clair ;
* vérifiées avant déploiement.

Les certificats, secrets Campay et clés d'infrastructure doivent être protégés.

---

# CHAPITRE 6 — CI/CD ET DÉPLOIEMENTS

Chaque déploiement doit suivre une chaîne contrôlée :

* build ;
* tests ;
* validation ;
* déploiement ;
* contrôle post-déploiement ;
* journalisation.

Les déploiements critiques doivent permettre un rollback rapide.

---

# CHAPITRE 7 — SAUVEGARDES ET SYNCHRONISATION

Les sauvegardes doivent respecter la séquence de référence :

* Serveur OVH (Production) ;
* synchronisation automatique vers le serveur local ;
* sauvegarde locale ;
* sauvegarde hebdomadaire sur disque externe ;
* synchronisation automatique vers les 9 Google Drive spécialisés ;
* vérification d'intégrité ;
* test automatique de restauration ;
* rapport automatique ;
* notification d'échec.

Cette séquence est la seule référence de déploiement, de supervision et de reprise. Elle doit correspondre à 14-STORAGE-REFERENCE.md.

---

# CHAPITRE 8 — SUPERVISION ET MONITORING

La supervision doit couvrir :

* disponibilité ;
* latence ;
* erreurs ;
* consommation des ressources ;
* santé des webhooks ;
* état des paiements Campay ;
* état des sauvegardes.

Les alertes doivent être historisées et visibles pour l'administration.

---

# CHAPITRE 9 — PRA ET ROLLBACK

LAWIM doit disposer d'un plan de reprise d'activité.

Ce plan couvre notamment :

* incident OVH ;
* incident base de données ;
* incident disque local ;
* incident Google Drive ;
* incident réseau ;
* incident paiement Campay.

Toute restauration doit être testée périodiquement.

---

# CHAPITRE 10 — TESTS ET AUDIT

Les tests de déploiement doivent couvrir :

* installation propre ;
* migration ;
* restauration ;
* redémarrage ;
* rollback ;
* indisponibilité de Campay ;
* indisponibilité de Nginx ;
* indisponibilité de PostgreSQL.

---

# CHAPITRE 11 — OBJECTIF FINAL

Le référentiel de déploiement garantit que LAWIM peut être installé, exploité, restauré et maintenu de manière industrialisable.

# FIN DU DOCUMENT
