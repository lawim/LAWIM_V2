# LAWIM_V2_Source_Intelligence_Engine_Implementation

## Objet

Ce document constitue le plan officiel d'implémentation du **Source
Intelligence Engine (SIE)**.

Il complète :

-   ADR-001_Source_Intelligence_Engine.md
-   LAWIM_V2_Source_Intelligence_Engine_Prompt.md

------------------------------------------------------------------------

# Objectif

Implémenter le Source Intelligence Engine comme référentiel unique des
sources d'acquisition de LAWIM.

------------------------------------------------------------------------

# Ordre des travaux

## Phase 1 --- Analyse

-   Inventorier tous les modules impactés.
-   Identifier les références à l'ancien Tracking Code.
-   Produire la matrice d'impact.

## Phase 2 --- Modèle de données

Créer ou adapter :

-   Source
-   SourceContext
-   Relations Lead → Source
-   Migrations de base de données

## Phase 3 --- Backend

Implémenter :

-   ReferenceCodeService
-   SourceService
-   SourceContextService
-   ImportSourceService
-   AIAnalysisService
-   WhatsAppLinkService
-   DashboardService

Créer les API REST nécessaires.

## Phase 4 --- Frontend

Créer le module **Sources d'acquisition** avec :

-   liste des sources ;
-   import d'une URL ;
-   analyse IA ;
-   édition du contexte ;
-   génération du lien WhatsApp ;
-   statistiques.

## Phase 5 --- IA

À partir d'une URL importée :

-   analyser le contenu disponible ;
-   préremplir le SourceContext ;
-   afficher un score de confiance ;
-   permettre la validation/correction.

Le système doit rester fonctionnel sans IA.

## Phase 6 --- Migration

Adapter tous les composants utilisant le Tracking Code.

Supprimer les implémentations obsolètes.

Garantir la rétrocompatibilité lorsque nécessaire.

## Phase 7 --- Documentation

Mettre à jour :

-   architecture ;
-   guides ;
-   workflows ;
-   modèles ;
-   Knowledge Packs ;
-   ADR ;
-   documentation développeur.

## Phase 8 --- Tests

Créer :

-   tests unitaires ;
-   tests d'intégration ;
-   tests fonctionnels ;
-   tests de migration.

## Phase 9 --- Validation

Contrôler :

-   cohérence fonctionnelle ;
-   cohérence documentaire ;
-   cohérence des API ;
-   cohérence des modèles ;
-   cohérence des statistiques.

------------------------------------------------------------------------

# Critères d'acceptation

-   Toutes les anciennes références au Tracking Code sont migrées ou
    documentées.
-   Chaque Lead référence une Source.
-   Chaque Source possède un Reference Code unique.
-   Les statistiques sont calculées à partir des Sources.
-   Le système fonctionne avec ou sans IA.
-   La documentation est synchronisée avec le code.
-   Les tests passent avec succès.

------------------------------------------------------------------------

# Mode test sécurisé

-   Le hachage de mot de passe conserve le coût de production actuel
    (`PBKDF2_ITERATIONS = 210_000`).
-   Un abaissement du nombre d'itérations n'est activé que si
    `LAWIM_TEST_MODE=1` ou si l'environnement est explicitement déclaré
    en mode test via `APP_ENV=test`.
-   Le mode test ne s'active jamais par défaut en production.
-   Les scripts de validation du dépôt activent explicitement ce mode
    pour rendre la suite testable sans affaiblir la production.

------------------------------------------------------------------------

# Compatibilité GREEN-API

-   `idInstance` est traité comme un identifiant opaque de type
    `string`.
-   Aucune hypothèse de longueur fixe n'est imposée par LAWIM.
-   Les instances GREEN-API historiques à 10 caractères restent
    compatibles.
-   Les nouvelles instances GREEN-API à 12 caractères sont compatibles.
-   Les évolutions futures de longueur restent compatibles sans
    modification de LAWIM.
-   La rétrocompatibilité est conservée.

------------------------------------------------------------------------

# Livrables

-   Code source
-   Migrations
-   API
-   Interface utilisateur
-   Documentation
-   Knowledge Packs
-   Rapport final
