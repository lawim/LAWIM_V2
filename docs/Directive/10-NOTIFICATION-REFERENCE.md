# LAWIM

# 10-NOTIFICATION-REFERENCE.md

# Référentiel officiel du moteur de notification

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le présent document définit les règles officielles du moteur de notification de LAWIM.

Il constitue la référence unique pour :

* les notifications in-app ;
* les notifications mobiles ;
* les notifications e-mail ;
* les notifications SMS ;
* les notifications WhatsApp ;
* les notifications Telegram ;
* les règles de priorité et de regroupement.

---

# CHAPITRE 2 — PRINCIPE FONDAMENTAL

Une notification est toujours déclenchée par un événement identifiable.

Elle n'est jamais une décision métier autonome.

Le moteur de notification relaie, alerte et trace. Il ne remplace ni le workflow, ni le matching, ni le reporting.

---

# CHAPITRE 3 — RÉFÉRENCES OBLIGATOIRES

Le moteur de notification applique obligatoirement :

* 00-CONSTITUTION.md ;
* 03-CONVERSATION-REFERENCE.md ;
* 05-WORKFLOW-REFERENCE.md ;
* 06-DATABASE-REFERENCE.md ;
* 07-DASHBOARD-REFERENCE.md ;
* 08-ROLE-REFERENCE.md ;
* 11-REPORTING-REFERENCE.md ;
* 29-CAMPAY-PAYMENT-REFERENCE.md ;
* 13-ARCHITECTURE-GOVERNANCE-REFERENCE.md ;
* 14-STORAGE-REFERENCE.md.

---

# CHAPITRE 4 — SOURCES DE NOTIFICATION

Les notifications peuvent être générées par :

* le Workflow Engine ;
* le Matching Engine ;
* le Conversation Engine ;
* le Dashboard Engine ;
* le Reporting Engine ;
* le Geo Engine ;
* le Role Engine ;
* LAWIM AI ;
* le Storage Lifecycle Manager ;
* les événements de tracking marketing transverse ;
* les services payants ;
* le Campay Payment Engine ;
* les événements d'administration.

Chaque notification doit conserver sa source d'origine.

---

# CHAPITRE 5 — CANAUX OFFICIELS

Les canaux de communication sont ceux du modèle de données et des intégrations officielles :

* IN_APP ;
* EMAIL ;
* SMS ;
* WHATSAPP ;
* TELEGRAM.

Le choix du canal dépend du contexte, des permissions et des préférences utilisateur.

---

# CHAPITRE 6 — TYPES DE NOTIFICATION

LAWIM distingue notamment :

* information ;
* alerte ;
* rappel ;
* validation ;
* refus ;
* sécurité ;
* workflow ;
* marketing ;
* attribution ;
* analytics ;
* service payant ;
* paiement ;
* reporting ;
* maintenance ;
* audit.

Chaque type possède une priorité et une logique d'affichage propres.

---

# CHAPITRE 7 — PRIORITÉ ET REGROUPEMENT

Les notifications doivent être classées selon leur criticité.

Le moteur doit :

* prioriser les urgences ;
* regrouper les notifications répétitives ;
* éviter les doublons ;
* limiter le bruit ;
* faire remonter les éléments réellement actionnables.

Une même cause ne doit pas générer une avalanche de messages identiques.

---

# CHAPITRE 8 — RÈGLES DE DIFFUSION

Une notification ne peut être envoyée que si :

* elle est autorisée par le rôle ;
* elle respecte les préférences ;
* elle respecte la confidentialité ;
* elle dispose d'un destinataire identifiable ;
* elle provient d'un événement validé.

Les notifications sensibles doivent rester masquées ou résumées lorsqu'elles apparaissent sur un support partagé.

---

# CHAPITRE 9 — INTERACTIONS AVEC LES AUTRES MOTEURS

Le moteur de notification sert notamment :

* le Dashboard Engine pour les alertes visibles ;
* le Workflow Engine pour les rappels ;
* le Matching Engine pour les propositions ;
* le Reporting Engine pour les alertes d'exploitation ;
* le Conversation Engine pour les réponses et suivis ;
* le Role Engine pour les notifications d'administration ;
* le Campay Payment Engine pour les confirmations, échecs et expirations de paiement ;
* le Storage Lifecycle Manager pour les rappels de conservation.

---

# CHAPITRE 10 — TRAÇABILITÉ

Chaque notification doit être historisée avec :

* son identifiant ;
* son origine ;
* son destinataire ;
* son canal ;
* son niveau de priorité ;
* son horodatage ;
* son état de livraison ;
* son état de lecture si applicable.

Cette traçabilité permet de produire les indicateurs de livraison et de lecture.

---

# CHAPITRE 11 — ÉCHECS ET RETRAITEMENTS

Si une notification échoue, le moteur doit :

* conserver le motif d'échec ;
* tenter le canal de secours si autorisé ;
* tracer la tentative ;
* signaler l'anomalie lorsque cela est nécessaire.

Les notifications liées à Campay doivent être alignées sur le statut réel du paiement et ne jamais annoncer une confirmation non vérifiée.

L'échec de notification ne doit jamais supprimer l'événement source.

---

# CHAPITRE 12 — CONFIDENTIALITÉ

Le moteur de notification doit respecter les règles de confidentialité de LAWIM.

Il est interdit :

* d'exposer un document sensible sans autorisation ;
* de divulguer une adresse exacte à un destinataire non habilité ;
* de transmettre un message de mise en relation sans double consentement ;
* de contourner un paramètre de confidentialité.

---

# CHAPITRE 13 — RÈGLES ABSOLUES

Le moteur de notification doit toujours :

* rester rattaché à un événement source ;
* conserver l'origine du message ;
* respecter les permissions ;
* respecter le contexte de l'utilisateur ;
* rester compatible avec le Dashboard et les Workflows ;
* être historisé.

Il est interdit :

* de générer une notification sans origine ;
* de fabriquer une notification métier hors des référentiels ;
* de faire croire qu'une transaction a produit une commission inexistante.

---

# CHAPITRE 14 — OBJECTIF FINAL

Le moteur de notification doit informer la bonne personne, au bon moment, par le bon canal, avec le bon niveau de détail, tout en conservant une traçabilité complète.

---

# CHAPITRE 15 — SUPPORT MULTILINGUE

Toutes les notifications système doivent pouvoir être rendues en Français, English et Pidgin English.

Les modèles de notification doivent être centralisés et versionnés via 30B-TRANSLATION-REFERENCE.md.

Le moteur de notification doit respecter la langue active du contexte utilisateur.

---

# FIN DU DOCUMENT

Le présent **10-NOTIFICATION-REFERENCE.md** constitue le référentiel officiel du moteur de notification de LAWIM.
