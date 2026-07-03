# LAWIM

# 22A-PRODUCT-EXPERIENCE-GUIDE.md

# Product Experience Guide officiel

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le présent document définit la fondation de l'expérience produit LAWIM V2 pour le frontend.

Il vise à fournir une base concrète pour :

* la cohérence produit Web/Mobile ;
* les parcours utilisateur prioritaires ;
* les composants frontend essentiels ;
* les règles d'affichage des informations métiers ;
* la conception d'une expérience progressive sans modifier le backend.

---

# CHAPITRE 2 — PÉRIMÈTRE

Ce guide couvre uniquement la fondation produit/UX/UI et la documentation front-end.

Il exclut explicitement :

* toute modification backend/API ;
* toute modification de schéma ou de migration ;
* toute refonte de logique métier serveur ;
* toute fonctionnalité nécessitant une nouvelle API.

Le périmètre retenu est :

* audit de l'expérience existante ;
* définition des principes UX/UI ;
* cadrage des composants réutilisables ;
* orientation mobile et responsive ;
* validation documentaire pour Program N.

---

# CHAPITRE 3 — PRINCIPES PRODUIT

L'expérience produit LAWIM doit être :

* claire et transparente ;
* actionnable en un minimum de clics ;
* fiable sur les parcours métiers clés ;
* cohérente entre Web et Mobile ;
* accessible et performante sur appareils modestes ;
* compatible avec l'internationalisation et les formats locaux.

Les principes de conception sont :

* priorité aux tâches métier réelles ;
* affichage progressif de la complexité ;
* feedbacks visuels immédiats ;
* cohérence des statuts et des actions ;
* anticipation des erreurs métier ;
* harmonisation des composants avec le design system existant.

---

# CHAPITRE 4 — PARCOURS UTILISATEUR FONDAMENTAUX

Les parcours prioritaires pour la fondation sont :

1. Découverte et navigation générale.
2. Création et consultation de projet immobilier.
3. Consultation et interaction avec les recommandations et les décisions.
4. Recherche et sélection de partenaires/services.
5. Suivi de l'état d'un workflow ou d'une intervention.
6. Notifications et rappels de statut.
7. Mobile / offline léger et synchronisation de l'expérience.

Chaque parcours doit être présenté comme une suite d'étapes lisibles, avec :

* point d'entrée clair ;
* état actuel visible ;
* action suivante identifiée ;
* informations métier contextualisées ;
* navigation cohérente entre les vues.

---

# CHAPITRE 5 — COMPOSANTS DE BASE

Les composants de la fondation sont :

* cartes d'information métier ;
* listes et tableaux simplifiés ;
* badges de statut ;
* barres d'action persistantes ;
* formulaires guidés ;
* champs de recherche ;
* modales de confirmation ;
* alertes et notifications in-app ;
* skeletons de chargement ;
* fiches de détails projet / partenaire / service.

Chaque composant doit être :

* réutilisable ;
* descriptif ;
* lisible sur petit écran ;
* facilement localisé ;
* compatible avec les couleurs et la typographie du design system.

---

# CHAPITRE 6 — DESIGN SYSTEM ET COHÉRENCE

Ce guide complète le système de design existant (`docs/Directive/21-UX-UI-DESIGN-SYSTEM.md`).

La fondation doit garantir :

* une hiérarchie visuelle stable ;
* une palette de couleurs sobre et métier ;
* une typographie claire et accessible ;
* des états de composants cohérents ;
* des retours d'erreur explicites ;
* des transitions simples et non intrusives.

Les règles doivent couvrir les écrans suivants :

* pages de liste et de tableau ;
* pages de détail projet ;
* écrans d'action / workflow ;
* écrans de notification et d'alerte ;
* vues mobiles et responsive.

---

# CHAPITRE 7 — MOBILE ET RESPONSIVE

L'expérience mobile doit être :

* priorisée pour les écrans clés ;
* adaptée à la navigation tactile ;
* lisible sans surcharge ;
* limitée aux interactions les plus utiles ;
* synchronisée avec l'expérience Web sans créer de divergence sémantique.

Elle doit s'appuyer sur :

* `docs/Directive/20-MOBILE-REFERENCE.md` ;
* `docs/Directive/30-I18N-L10N-REFERENCE.md` ;
* `docs/Directive/30B-TRANSLATION-REFERENCE.md`.

---

# CHAPITRE 8 — VALIDATION DOCUMENTAIRE

La validation doit couvrir :

* conformité aux principes UX/UI ;
* cohérence avec les parcours métier existants ;
* absence de dépendance à des modifications backend ;
* alignement avec la documentation développeur ;
* relecture produit et design.

Checklist minimale :

- [ ] Principes UX validés.
- [ ] Parcours fondamentaux identifiés.
- [ ] Composants de base cadrés.
- [ ] Contraintes backend explicitement documentées.
- [ ] Références de design et mobile listées.
- [ ] Plan de mise en œuvre front-end préparé.

---

# CHAPITRE 9 — RÉFÉRENCES

* `docs/Directive/21-UX-UI-DESIGN-SYSTEM.md`
* `docs/Directive/20-MOBILE-REFERENCE.md`
* `docs/Directive/24-DEVELOPER-GUIDE.md`
* `docs/Directive/16-API-REFERENCE.md`
* `docs/Directive/30-I18N-L10N-REFERENCE.md`
* `docs/Directive/30B-TRANSLATION-REFERENCE.md`
* `docs/strategy/LAWIM_2X_PROGRAM_ROADMAP.md`

# FIN DU DOCUMENT
