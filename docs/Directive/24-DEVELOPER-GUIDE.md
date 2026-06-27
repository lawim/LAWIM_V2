# LAWIM

# 24-DEVELOPER-GUIDE.md

# Guide développeur officiel

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le présent document définit les règles de développement de LAWIM.

Il constitue la référence unique pour :

* la structure du code ;
* les conventions ;
* les branches Git ;
* les commits ;
* les tests ;
* les revues de code ;
* la documentation ;
* l'intégration Campay.

---

# CHAPITRE 2 — PRINCIPES

Le développement doit suivre :

* refactor avant rewrite ;
* extension avant invention ;
* maintien de la compatibilité ;
* documentation avant implémentation ;
* respect strict des moteurs.

---

# CHAPITRE 3 — STRUCTURE DU CODE

Le code doit rester organisé par moteurs et responsabilités.

Aucun module ne doit contourner son moteur propriétaire.

Les dépendances circulaires doivent être évitées.

---

# CHAPITRE 4 — CONVENTIONS GIT

Les branches doivent être nommées de manière explicite.

Les commits doivent être :

* petits ;
* traçables ;
* descriptifs ;
* centrés sur une seule intention.

---

# CHAPITRE 5 — TESTS ET PR

Chaque modification doit être accompagnée :

* des tests nécessaires ;
* d'une revue de code ;
* d'une validation documentaire si le périmètre métier évolue.

Les PR doivent rester lisibles et réversibles.

---

# CHAPITRE 6 — DOCUMENTATION

Toute évolution significative doit mettre à jour :

* les référentiels ;
* les tests ;
* les matrices de traçabilité ;
* les guides d'exploitation si nécessaire.

---

# CHAPITRE 7 — RÈGLES CODEX

Les règles de travail suivantes s'imposent :

* ne pas inventer de décision métier ;
* ne pas supprimer de règle validée ;
* ne pas créer de logique cachée ;
* vérifier les impacts croisés ;
* préserver le modèle économique.

---

# CHAPITRE 8 — INTÉGRATION CAMPAY

L'intégration Campay doit respecter :

* la validation backend ;
* la signature des webhooks ;
* l'idempotence ;
* le rapprochement ;
* l'absence de commission sur transaction immobilière.

---

# CHAPITRE 9 — SÉCURITÉ DES SECRETS

Les secrets ne doivent jamais être :

* committés en clair ;
* exposés dans les logs ;
* partagés sans contrôle ;
* réutilisés sans rotation si la politique exige un renouvellement.

---

# CHAPITRE 10 — DETTE TECHNIQUE

La dette technique doit être explicitée, limitée et suivie.

Elle ne doit jamais masquer une règle métier ou une décision d'architecture.

---

# CHAPITRE 11 — SUPPORT MULTILINGUE

Le code doit respecter les référentiels linguistiques officiels.

En particulier :

* aucune chaîne d'interface ne doit être codée en dur lorsqu'une clé de traduction existe ;
* les formats de date, de nombre et de devise doivent respecter la locale résolue ;
* les messages API et UI doivent s'appuyer sur les clés centralisées ;
* les contributions doivent mettre à jour les ressources de traduction concernées ;
* les tests doivent couvrir les langues officielles lorsque le périmètre l'exige.

Le développement doit s'aligner sur 30-I18N-L10N-REFERENCE.md, 30B-TRANSLATION-REFERENCE.md et 30C-LANGUAGE-DETECTION-REFERENCE.md.

---

# CHAPITRE 12 — TRACKING MARKETING ET CONVENTIONS CODE

Le développement doit respecter les conventions suivantes pour le tracking marketing :

* le Tracking Code est immuable ;
* l'actorId est immuable ;
* le rôle de l'acteur est historisé séparément ;
* aucune logique locale ne doit recalculer le Tracking Code ;
* les événements de tracking doivent être partagés entre les moteurs ;
* les statistiques doivent rester recalculables par jointure ;
* aucune commission immobilière ne doit être introduite par les données marketing.

Le code doit exploiter les référentiels 06-DATABASE-REFERENCE.md, 16-API-REFERENCE.md, 27-TRACEABILITY-MATRIX.md et 30A-BUSINESS-DICTIONARY-REFERENCE.md.

---

# CHAPITRE 13 — OBJECTIF FINAL

Le guide développeur garantit une contribution cohérente, sûre et durable à la plateforme LAWIM.

# FIN DU DOCUMENT
