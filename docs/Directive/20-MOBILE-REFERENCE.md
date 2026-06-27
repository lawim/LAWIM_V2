# LAWIM

# 20-MOBILE-REFERENCE.md

# Référentiel officiel mobile

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le présent document définit les règles officielles de l'expérience mobile de LAWIM.

Il constitue la référence unique pour :

* Android ;
* iOS futur ;
* l'offline ;
* la synchronisation ;
* la caméra ;
* la vidéo ;
* l'audio ;
* les notifications push ;
* le paiement mobile via Campay.

---

# CHAPITRE 2 — PRINCIPES FONDAMENTAUX

L'expérience mobile doit être :

* rapide ;
* lisible ;
* cohérente avec le Web ;
* sécurisée ;
* capable de fonctionner partiellement hors ligne ;
* synchronisable sans perte de contexte.

---

# CHAPITRE 3 — FONCTIONS MOBILES

Le mobile doit permettre notamment :

* la recherche ;
* la conversation ;
* la consultation des matchings ;
* la publication ou la mise à jour autorisée ;
* la capture de photos ;
* la capture de vidéos ;
* l'enregistrement audio ;
* le suivi des notifications ;
* le paiement Campay.

---

# CHAPITRE 4 — OFFLINE ET SYNCHRONISATION

Le mobile doit gérer :

* le cache local ;
* les files de synchronisation ;
* la reprise après coupure réseau ;
* la résolution des conflits selon les règles métier ;
* la synchronisation vers les moteurs officiels.

Les données critiques ne doivent jamais être écrasées sans historisation.

---

# CHAPITRE 5 — CAPTEURS ET MÉDIAS

Le mobile peut utiliser :

* le GPS ;
* la caméra ;
* le microphone ;
* la galerie ;
* le partage natif ;
* les permissions système.

Les permissions doivent rester minimales et explicites.

---

# CHAPITRE 6 — NOTIFICATIONS PUSH

Les notifications push doivent être :

* utiles ;
* prioritaires ;
* cohérentes avec le workflow ;
* compatibles avec les préférences de l'utilisateur.

Les notifications de paiement doivent refléter l'état réel du service.

---

# CHAPITRE 7 — SÉCURITÉ MOBILE

Le mobile doit respecter :

* la sécurité des jetons ;
* le chiffrement local si nécessaire ;
* la protection contre le device sharing non autorisé ;
* la révocation de session ;
* la protection des documents sensibles.

Un paiement ne peut jamais être validé côté mobile seul.

---

# CHAPITRE 8 — PAIEMENT MOBILE VIA CAMPAY

Le mobile peut :

* initier un paiement ;
* afficher un statut ;
* guider l'utilisateur ;
* afficher un reçu ;
* attendre la confirmation backend.

Le mobile ne doit jamais confirmer lui-même un paiement.

---

# CHAPITRE 9 — PERFORMANCE ET UX

L'expérience mobile doit rester :

* fluide ;
* stable ;
* compatible avec des appareils modestes ;
* claire sur les états de chargement ;
* cohérente avec le système de design.

---

# CHAPITRE 10 — TESTS

Les tests mobiles doivent couvrir :

* navigation ;
* connexion ;
* capture média ;
* synchronisation ;
* notifications ;
* paiement Campay ;
* reprise après coupure réseau ;
* permissions système.

---

# CHAPITRE 11 — SUPPORT MULTILINGUE

Le mobile doit permettre :

* le changement instantané de langue ;
* la mémorisation de la préférence utilisateur ;
* le cache local des traductions ;
* le fonctionnement hors ligne ;
* la mise à jour automatique des ressources linguistiques ;
* la synchronisation des packs de traduction.

L'interface mobile doit s'appuyer sur 30-I18N-L10N-REFERENCE.md, 30B-TRANSLATION-REFERENCE.md et 30C-LANGUAGE-DETECTION-REFERENCE.md.

---

# CHAPITRE 12 — OBJECTIF FINAL

Le référentiel mobile garantit que LAWIM offre une expérience utile, sûre et cohérente sur les appareils mobiles.

# FIN DU DOCUMENT
