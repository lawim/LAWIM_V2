# LAWIM

# 29-CAMPAY-PAYMENT-REFERENCE.md

# Référentiel officiel du paiement Campay

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le présent document définit les règles officielles du Campay Payment Engine.

Il constitue la référence unique pour :

* l'initiation de paiement ;
* la confirmation ;
* les statuts de paiement ;
* les webhooks ;
* le reçu ;
* le rapprochement ;
* le reporting ;
* l'administration.

Les interfaces Campay, y compris les reçus, confirmations, SMS, emails, notifications et messages d'erreur, doivent être disponibles en Français, English et Pidgin English via 30B-TRANSLATION-REFERENCE.md.

---

# CHAPITRE 2 — PAIEMENTS CONCERNÉS

Les paiements concernés sont exclusivement ceux des services LAWIM :

* mise en relation ;
* services LAWIM ;
* accompagnement de visite ;
* accompagnement de transaction ;
* contrôle documentaire ;
* photographie ;
* vidéo ;
* vérification ;
* boost ;
* visibilité premium ;
* services partenaires ;
* assistance.

---

# CHAPITRE 3 — PAIEMENTS EXCLUS

Le module ne traite jamais :

* une commission sur vente ;
* une commission sur location ;
* un prélèvement automatique sur un prix de transaction immobilière.

Le modèle économique de LAWIM reste inchangé.

---

# CHAPITRE 4 — ARCHITECTURE DU FLUX

Le flux de paiement suit l'ordre suivant :

1. création d'une opération de paiement LAWIM ;
2. génération d'une référence unique ;
3. appel API Campay ;
4. attente de confirmation ;
5. réception du webhook ;
6. vérification serveur à serveur ;
7. activation du service ;
8. émission du reçu ;
9. reporting et rapprochement.

Le paiement n'est jamais confirmé par le frontend seul.

---

# CHAPITRE 5 — STATUTS DE PAIEMENT

Les statuts officiels sont notamment :

* `PAYMENT_CREATED` ;
* `PAYMENT_INITIATED` ;
* `PAYMENT_PENDING` ;
* `PAYMENT_CONFIRMED` ;
* `PAYMENT_FAILED` ;
* `PAYMENT_EXPIRED` ;
* `PAYMENT_CANCELLED` ;
* `PAYMENT_REFUNDED` ;
* `PAYMENT_DISPUTED` ;
* `PAYMENT_RECONCILED`.

Chaque changement de statut doit être historisé.

Les services gratuits ne créent pas d'opération de paiement et ne doivent pas réutiliser ces statuts.

---

# CHAPITRE 6 — WEBHOOKS

Les webhooks doivent respecter :

* une signature vérifiée ;
* l'idempotence ;
* la journalisation ;
* le rejet des doublons ;
* le rejet des webhooks frauduleux ;
* la reprise après incident.

Aucun webhook non vérifié ne vaut preuve de paiement.

---

# CHAPITRE 7 — SÉCURITÉ

Les interdictions absolues sont :

* ne jamais valider un paiement depuis le frontend seul ;
* ne jamais activer un service sans confirmation backend fiable ;
* ne jamais stocker les clés Campay en clair ;
* ne jamais ignorer une divergence entre Campay et LAWIM ;
* ne jamais considérer un webhook non vérifié comme preuve de paiement.

---

# CHAPITRE 8 — ADMINISTRATION

L'administration doit permettre :

* la consultation des transactions ;
* la recherche ;
* le filtrage ;
* le rapprochement ;
* l'export ;
* la gestion des échecs ;
* la relance ;
* le remboursement si applicable ;
* l'audit ;
* le support utilisateur.

---

# CHAPITRE 9 — REPORTING

Les indicateurs officiels incluent notamment :

* nombre de paiements ;
* volume payé ;
* paiements confirmés ;
* paiements échoués ;
* paiements en attente ;
* revenus par service ;
* revenus par période ;
* revenus par canal ;
* taux de rapprochement ;
* délais de confirmation.

---

# CHAPITRE 10 — INTERACTIONS

Le Campay Payment Engine coopère notamment avec :

* Security Engine ;
* API Gateway ;
* Workflow Engine ;
* Notification Engine ;
* Reporting Engine ;
* Dashboard Engine ;
* Administration Engine ;
* 12-TESTS-REFERENCE.md.

---

# CHAPITRE 11 — TESTS

Les tests obligatoires couvrent :

* paiement réussi ;
* paiement échoué ;
* paiement en attente ;
* webhook reçu deux fois ;
* webhook frauduleux ;
* coupure réseau ;
* API Campay indisponible ;
* service non activé sans paiement ;
* activation après paiement confirmé ;
* rapprochement reporting ;
* audit administrateur ;
* rendu multilingue des reçus, confirmations, SMS, emails et notifications.

---

# CHAPITRE 13 — ATTRIBUTION ANALYTIQUE

Lorsqu'un paiement Campay est confirmé, les données peuvent être reliées à :

* un Reference Code ;
* une campagne ;
* une publication ;
* un canal ;
* un actorId ;
* un service LAWIM ;
* un lead ;
* une conversion.

Cette attribution est analytique et documentaire.

Elle ne crée aucune commission immobilière et ne modifie pas le modèle économique de LAWIM.

---

# CHAPITRE 14 — OBJECTIF FINAL

Le référentiel Campay permet à LAWIM d'encadrer un paiement sûr, traçable et compatible avec son modèle économique sans commission immobilière.

# FIN DU DOCUMENT
