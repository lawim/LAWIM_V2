# LAWIM

# 23-INSTALLATION-GUIDE.md

# Guide d'installation officiel

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le présent document définit les règles officielles d'installation de LAWIM.

Il constitue la référence unique pour :

* l'installation serveur ;
* les prérequis ;
* Docker ;
* PostgreSQL ;
* Prisma ;
* Redis ;
* Nginx ;
* la configuration Campay ;
* le premier lancement.

---

# CHAPITRE 2 — PRÉREQUIS

L'installation suppose notamment :

* un serveur compatible ;
* les dépendances système ;
* l'accès aux secrets ;
* les accès aux référentiels ;
* les accès de test aux services externes autorisés.

---

# CHAPITRE 3 — INSTALLATION DU STACK

L'installation doit suivre l'ordre suivant :

* Docker ;
* PostgreSQL ;
* Prisma ;
* Redis ;
* Nginx ;
* dépendances applicatives ;
* migrations ;
* seed si nécessaire.

---

# CHAPITRE 4 — VARIABLES D'ENVIRONNEMENT

Les variables d'environnement doivent être :

* documentées ;
* distinctes selon l'environnement ;
* chargées de manière contrôlée ;
* protégées contre l'exposition dans les logs.

Les secrets Campay doivent être séparés entre sandbox et production.

---

# CHAPITRE 5 — CONFIGURATION CAMPAY

La configuration Campay doit distinguer :

* le mode sandbox ;
* le mode production ;
* les webhooks ;
* les URLs de redirection ;
* les clés de signature ;
* les paramètres de rapprochement.

---

# CHAPITRE 6 — MIGRATION ET SEED

Les migrations doivent être exécutées de manière contrôlée.

Le seed ne doit être appliqué que si le contexte l'autorise.

Tout changement de schéma doit être compatible avec les référentiels.

---

# CHAPITRE 7 — PREMIER LANCEMENT

Le premier lancement doit vérifier :

* l'accès API ;
* l'accès base de données ;
* l'état des services ;
* les webhooks critiques ;
* l'état du paiement Campay si activé.

---

# CHAPITRE 8 — TESTS DE VÉRIFICATION

Après installation, exécuter au minimum :

* tests unitaires ;
* tests d'intégration ;
* tests de démarrage ;
* tests de base de données ;
* tests de webhook ;
* tests Campay.

---

# CHAPITRE 9 — RÉVERSIBILITÉ

Toute installation doit rester réversible.

Les sauvegardes et la procédure de restauration doivent être prêtes avant la mise en production.

---

# CHAPITRE 10 — OBJECTIF FINAL

Le guide d'installation garantit que LAWIM peut être installé de manière fiable, reproductible et documentée.

# FIN DU DOCUMENT
