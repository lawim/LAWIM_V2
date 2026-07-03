# ADR-001 --- Adoption du Source Intelligence Engine (SIE)

**Statut :** Acceptée\
**Projet :** LAWIM V2\
**Date :** 2026-07-02

------------------------------------------------------------------------

# Contexte

LAWIM utilisait jusqu'à présent un concept de **Tracking Code** destiné
à identifier l'origine d'un lead.

Au cours de la conception, plusieurs limites ont été identifiées :

-   le Tracking Code transportait potentiellement des informations
    métier ;
-   il était difficile de gérer les publications externes, les groupes
    Facebook, les partenaires, les ambassadeurs ou les partages
    spontanés ;
-   les statistiques marketing risquaient d'être limitées ou dépendantes
    de la structure du code.

Une nouvelle approche a donc été étudiée.

------------------------------------------------------------------------

# Décision

Le projet adopte officiellement une nouvelle architecture :

**Source Intelligence Engine (SIE).**

Le SIE devient le référentiel unique des sources d'acquisition de LAWIM.

Le Tracking Code est remplacé par un **Reference Code**.

Ce code :

-   est court ;
-   est unique ;
-   est immuable ;
-   ne contient aucune information métier.

------------------------------------------------------------------------

# Principes retenus

## 1. Le cœur du système est la Source

Une Source représente n'importe quel point d'entrée vers LAWIM :

-   publication officielle ;
-   partenaire ;
-   client ;
-   ambassadeur ;
-   groupe Facebook ;
-   publication spontanée ;
-   QR Code ;
-   flyer ;
-   email ;
-   campagne ;
-   etc.

------------------------------------------------------------------------

## 2. Le Reference Code identifie uniquement une Source

Le code ne décrit jamais :

-   la ville ;
-   le quartier ;
-   le type de bien ;
-   la campagne ;
-   le réseau social.

Toutes ces informations sont stockées ailleurs.

------------------------------------------------------------------------

## 3. Les métadonnées sont stockées dans SourceContext

Le contexte est enrichi automatiquement par l'IA ou par l'utilisateur.

Il peut évoluer sans modifier le Reference Code.

------------------------------------------------------------------------

## 4. Les Leads référencent une Source

Le Lead référence uniquement la Source.

Toutes les statistiques sont calculées à partir de cette relation.

------------------------------------------------------------------------

# Conséquences

## Avantages

-   architecture plus simple ;
-   code stable ;
-   meilleure évolutivité ;
-   compatible avec tous les réseaux sociaux ;
-   compatible avec les QR Codes ;
-   compatible avec les ambassadeurs ;
-   compatible avec les partenaires ;
-   compatible avec les publications inconnues ;
-   statistiques beaucoup plus riches.

## Inconvénients

-   nécessité de migrer l'ancien système ;
-   mise à jour de la documentation ;
-   adaptation des modules existants.

------------------------------------------------------------------------

# Workflow officiel

1.  Publication sur un réseau social.
2.  Copie de l'URL.
3.  Import dans LAWIM.
4.  Création automatique de la Source.
5.  Génération du Reference Code.
6.  Analyse IA.
7.  Génération du lien WhatsApp.
8.  Ajout du lien dans la publication.
9.  Attribution automatique des futurs leads.

------------------------------------------------------------------------

# Décisions d'architecture

Le SIE devient la seule source de vérité concernant l'origine des leads.

Aucune nouvelle fonctionnalité ne devra créer un système parallèle de
suivi des sources.

Toute évolution future devra s'intégrer au SIE.

------------------------------------------------------------------------

# Évolutions prévues

-   API Meta
-   LinkedIn
-   TikTok
-   Telegram
-   QR Codes intelligents
-   Liens courts LAWIM
-   Attribution multi-touch
-   Marketing Automation

Toutes ces évolutions devront utiliser le SIE comme référentiel unique.

------------------------------------------------------------------------

# Validation

Cette ADR constitue la décision officielle d'architecture concernant la
gestion des sources d'acquisition dans LAWIM V2.
