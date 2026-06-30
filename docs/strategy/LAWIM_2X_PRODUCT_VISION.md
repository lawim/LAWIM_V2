# LAWIM 2.x — Product Vision

**Programme :** LAWIM_2X  
**Statut :** Draft for Direction Générale review  
**Base publiée :** v1.0.0 (gelée)  
**Branche programme :** `develop/2.0-intelligent-platform`

---

## 1. Pourquoi LAWIM 2.x existe

LAWIM 1.0 a livré une **plateforme exécutable** : listings, matching par règles, conversations, notifications, RBAC, persistance SQLite/PostgreSQL, packaging et CI. C’est la fondation technique.

LAWIM 2.x transforme cette fondation en **plateforme d’accompagnement immobilier intelligent**, alignée sur le [Plan Stratégique 2026–2027](PLAN_STRATEGIQUE_DEPLOIEMENT_LAWIM_2026_2027_V2.md) :

> « LAWIM n’est pas un portail d’annonces — c’est un facilitateur de projets immobiliers. »

Le produit ne part pas d’une annonce, mais d’un **projet de vie** (loger, investir, construire, sécuriser un patrimoine, accompagner la diaspora).

---

## 2. Promesse 2.x

**Chaque personne avec un projet immobilier au Cameroun avance avec méthode, confiance et transparence — guidée par LAWIM, ses partenaires qualifiés et une intelligence utile, jamais substitutive.**

Mesure de succès prioritaire (héritée du plan stratégique) :

> « LAWIM m’a aidé à prendre une meilleure décision. »

---

## 3. Les dix piliers produit 2.x

### 3.1 Accompagnement de projet immobilier

- Objet central : le **Projet** (besoin, budget, horizon, contraintes, étape).
- Les annonces et services sont des **moyens**, pas le point d’entrée.
- Parcours explicites : acheteur, vendeur, locataire, investisseur, diaspora, promoteur.

### 3.2 Assistant intelligent

- Copilote conversationnel **contextualisé au projet** (pas un chatbot générique).
- Réponses **ancrées** dans la base de connaissance et les données utilisateur autorisées.
- Règle absolue : **décision humaine** — l’IA propose, l’utilisateur et les professionnels décident.

### 3.3 Moteur de connaissance

- Référentiel structuré : marché, quartiers, prix, procédures, droit pratique, checklists.
- Alimenté par données internes, partenaires et retours d’expérience (continuous learning).
- Versionné, auditable, distinct du code applicatif.

### 3.4 Parcours utilisateur guidés

- Wizards et états de parcours (qualification → recherche → visite → négociation → clôture service).
- Reprise de session, reprise multi-canal (web, mobile, WhatsApp/Telegram futurs).
- Héritage 1.0 : conversations et négociations deviennent des **étapes** de parcours.

### 3.5 Partenaires qualifiés

- Annuaire de partenaires **vérifiés** (agences, notaires, géomètres, artisans, banques…).
- Profils, zones, spécialités, disponibilité, historique de missions.
- Mise en relation **contextuelle** au projet, pas listing générique.

### 3.6 Scoring de confiance

- Score composite : qualité des données, historique partenaire, vérifications, retours utilisateurs.
- Visible de façon **explicable** (pas boîte noire).
- Renforce le pilier « confiance » du plan stratégique — premier produit LAWIM.

### 3.7 Marketplace de services

- Catalogue de **services à valeur ajoutée** (accompagnement, recherche sur mesure, vérification documentaire, visites, diaspora…).
- Monétisation **sans commission** sur transactions immobilières (règle 1.0 conservée).
- Intégration paiement (Campay) et suivi d’exécution.

### 3.8 Recherche intelligente

- Au-delà des filtres 1.0 : recherche sémantique, similarité de projets, recommandations expliquées.
- Matching enrichi par profil projet + connaissance marché + confiance.
- Priorité qualité des résultats sur volume d’annonces.

### 3.9 Mobile-first

- Expérience conçue **mobile d’abord** (PWA puis apps natives si justifié).
- Parcours courts, offline partiel, notifications push.
- API stable pour clients mobiles — le monolithe 1.0 sert de backend initial.

### 3.10 Analytics produit

- Événements produit structurés, entonnoirs, rétention, satisfaction.
- Tableaux de bord Produit / Business / Marketing / Direction (plan stratégique Partie 7).
- Décisions basées sur les données — pas sur l’intuition seule.

---

## 4. Ce que LAWIM 2.x n’est pas

- Un nouveau portail d’annonces généraliste.
- Une agence immobilière digitale.
- Un remplacement des professionnels.
- Une refonte Big Bang de LAWIM 1.0 (branches 1.0 gelées).
- Une plateforme IA autonome sans gouvernance humaine.

---

## 5. Personas prioritaires (ordre 2.x)

| Persona | Besoin 2.x |
|---------|------------|
| Acheteur / locataire | Comprendre, comparer, avancer sans arnaque |
| Propriétailre | Diffuser avec crédibilité, être accompagné |
| Diaspora | Confiance, suivi à distance, transparence |
| Agent / agence | Prospects qualifiés, outils, visibilité |
| Admin LAWIM | Qualité données, partenaires, pilotage |
| Partenaire métier | Missions qualifiées, réputation |

---

## 6. Principes de décision produit (hérités + 2.x)

Avant toute fonctionnalité 2.x, répondre oui à au moins une question :

1. Renforce-t-elle la **confiance** ?
2. Améliore-t-elle l’**accompagnement du projet** ?
3. Crée-t-elle de la **valeur durable** (données, partenaires, connaissance) ?
4. Est-elle cohérente avec la **Constitution et les référentiels** LAWIM ?

---

## 7. Horizon

| Phase | Focus |
|-------|--------|
| **2.0** | Fondations : projet, parcours, connaissance MVP, assistant limité, analytics base |
| **2.1** | Partenaires qualifiés, confiance, marketplace services pilote |
| **2.2** | Recherche intelligente avancée, mobile mature, diaspora premium |
| **2.x+** | Échelle nationale, continuous learning opérationnel, extension régionale (après succès CM) |

---

## 8. Relation avec LAWIM 1.0

LAWIM 1.0 reste la **runtime stable** publiée (`v1.0.0`). LAWIM 2.x **étend** :

- Domaine `Project` au-dessus de `Property`
- Couches `knowledge`, `assistant`, `trust`, `marketplace`, `analytics`
- UI mobile-first consommant les API existantes et nouvelles

Aucune modification des branches `release/1.0.0-beta`, `maintenance/1.0.x` ou `main` pour le développement 2.x.

---

*Document de référence programme — ne remplace pas la Constitution, la Gouvernance ni le Plan Stratégique global.*
