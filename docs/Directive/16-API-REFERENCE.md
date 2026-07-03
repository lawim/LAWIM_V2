# LAWIM

# 16-API-REFERENCE.md

# Référentiel officiel des API

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le présent document définit les règles officielles des API de LAWIM.

Il constitue la référence unique pour :

* les API Web ;
* les API Mobile ;
* les API Admin ;
* les API partenaires ;
* les API Reporting ;
* les API IA ;
* les API Campay ;
* les webhooks.

---

# CHAPITRE 2 — PRINCIPES FONDAMENTAUX

Les API de LAWIM doivent être :

* explicites ;
* versionnées ;
* sécurisées ;
* traçables ;
* compatibles ascendantes autant que possible ;
* dépourvues de logique métier cachée.

Une API n'est qu'une interface. Elle ne remplace jamais le moteur propriétaire.

---

# CHAPITRE 3 — SURFACES OFFICIELLES

Les surfaces exposées sont notamment :

* Web ;
* Mobile ;
* Administration ;
* Partenaires ;
* Reporting ;
* IA ;
* Source Intelligence ;
* Campay Payment Engine ;
* API Gateway.

Chaque surface peut avoir ses propres permissions et contrats.

---

# CHAPITRE 4 — AUTHENTIFICATION ET VERSIONING

Les API doivent appliquer :

* l'authentification officielle ;
* les jetons valides ;
* la vérification des permissions ;
* le versioning explicite ;
* la compatibilité ascendante autant que possible.

Les ruptures de contrat doivent être rares, documentées et annoncées.

---

# CHAPITRE 5 — CONVENTIONS D'API

Les API doivent respecter des conventions stables :

* ressources nommées clairement ;
* verbes HTTP cohérents ;
* pagination ;
* filtrage ;
* tri ;
* recherche ;
* identifiants stables ;
* réponses structurées.

Les valeurs métier doivent être normalisées avant exposition.

---

# CHAPITRE 6 — ERREURS ET RETOURS

Les erreurs doivent être :

* lisibles ;
* codifiées ;
* traçables ;
* compatibles avec le frontend et les clients externes.

Chaque erreur utile doit indiquer :

* la cause ;
* le contexte ;
* la correction possible ;
* le niveau de criticité.

---

# CHAPITRE 7 — WEBHOOKS ET CALLBACKS

Les webhooks doivent être :

* signés ;
* idempotents ;
* journalisés ;
* protégés contre le rejeu ;
* validés côté serveur.

Les webhooks Campay font l'objet de contrôles renforcés.

---

# CHAPITRE 8 — DOCUMENTATION OPENAPI / SWAGGER

Chaque API officielle doit disposer d'une documentation exploitable.

La documentation doit préciser :

* les routes ;
* les paramètres ;
* les schémas ;
* les erreurs ;
* les règles de sécurité ;
* les exemples utiles.

---

# CHAPITRE 9 — SÉCURITÉ ET PERFORMANCE

Les API doivent intégrer :

* rate limiting ;
* validation des entrées ;
* protection des secrets ;
* contrôle des accès ;
* surveillance de la latence ;
* prévention des abus.

Les routes critiques doivent être surveillées et testées.

---

# CHAPITRE 10 — COMPATIBILITÉ ASCENDANTE

Lorsqu'une API évolue, LAWIM doit préserver au maximum :

* les clients existants ;
* les intégrations partenaires ;
* les appels du frontend ;
* les webhooks métiers.

Une dépréciation doit toujours être documentée.

---

# CHAPITRE 11 — TESTS ET AUDIT

Les API doivent être testées pour :

* succès ;
* échec ;
* droits insuffisants ;
* version invalide ;
* webhook invalide ;
* webhook dupliqué ;
* réponse lente ;
* données incohérentes.

---

# CHAPITRE 12 — SUPPORT MULTILINGUE

Les API doivent gérer explicitement :

* `Accept-Language` ;
* `Content-Language` ;
* la détection automatique de la langue ;
* la préférence utilisateur ;
* la langue par session ;
* la langue par appareil ;
* le fallback ;
* le versioning des traductions.

Les messages d'API doivent être restitués dans la langue active lorsque cela est disponible.

Les formats de dates, de nombres et de devises doivent rester cohérents avec la locale résolue.

---

# CHAPITRE 13 — SOURCE INTELLIGENCE ET ANALYTICS

Les API existantes doivent exposer le Source Intelligence Engine comme référentiel unique des sources d'acquisition.

Les endpoints officiels incluent notamment :

* `GET /api/v2/source-intelligence` ;
* `GET /api/v2/source-intelligence/dashboard` ;
* `GET /api/v2/source-intelligence/stats` ;
* `GET /api/v2/source-intelligence/sources` ;
* `GET /api/v2/source-intelligence/sources/{id}` ;
* `GET /api/v2/source-intelligence/sources/{id}/context` ;
* `GET /api/v2/source-intelligence/sources/{id}/whatsapp-link` ;
* `GET /api/v2/source-intelligence/imports` ;
* `POST /api/v2/source-intelligence/reference-code` ;
* `POST /api/v2/source-intelligence/sources` ;
* `POST /api/v2/source-intelligence/imports` ;
* `POST /api/v2/source-intelligence/analyze` ;
* `PATCH /api/v2/source-intelligence/sources/{id}` ;
* `PATCH /api/v2/source-intelligence/sources/{id}/context`.

L'alias `/api/v2/sie` reste pris en charge pour compatibilité.

Ces routes utilisent la couche API existante, les permissions existantes et la journalisation officielle.

Le Reference Code doit rester lisible, stable, unique et exploitable par jointure.

---

# CHAPITRE 14 — OBJECTIF FINAL

Le référentiel API permet à LAWIM d'offrir des interfaces stables, sûres et cohérentes à tous ses clients techniques et fonctionnels.

# FIN DU DOCUMENT
