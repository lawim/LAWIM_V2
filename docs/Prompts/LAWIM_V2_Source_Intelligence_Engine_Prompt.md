# LAWIM V2 --- Implémentation du Source Intelligence Engine (SIE)

> **Mission générale**
>
> Remplacer l'ancien système de Tracking Code par un **Source
> Intelligence Engine (SIE)** qui devient le référentiel unique des
> sources d'acquisition de LAWIM.

------------------------------------------------------------------------

# 1. Objectifs

Le système doit permettre de :

-   identifier automatiquement la source d'acquisition de chaque lead ;
-   suivre les performances des sources marketing ;
-   produire des statistiques marketing avancées ;
-   enrichir automatiquement les sources grâce à l'IA ;
-   fonctionner indépendamment des réseaux sociaux.

------------------------------------------------------------------------

# 2. Principes d'architecture

## Principe n°1 --- Le système est centré sur les Sources

Une Source représente tout point d'entrée vers LAWIM :

-   publication Facebook
-   publication Instagram
-   TikTok
-   LinkedIn
-   Telegram
-   partenaire
-   client
-   ambassadeur
-   groupe Facebook
-   QR Code
-   flyer
-   carte de visite
-   email
-   campagne
-   statut WhatsApp
-   etc.

------------------------------------------------------------------------

## Principe n°2 --- Chaque Source possède un Reference Code

Exemple :

    #7K4P9M

Le Reference Code est :

-   court ;
-   unique ;
-   immuable ;
-   sans intelligence métier.

Il sert uniquement d'identifiant.

------------------------------------------------------------------------

## Principe n°3 --- Toute l'intelligence est stockée dans le contexte

Le contexte contient notamment :

-   réseau
-   URL
-   auteur
-   campagne
-   ville
-   quartier
-   type de bien
-   cible
-   format
-   langue
-   tags
-   analyse IA
-   score de confiance

Le contexte peut évoluer.

Le Reference Code ne change jamais.

------------------------------------------------------------------------

## Principe n°4 --- Chaque Lead référence une Source

Le Lead référence uniquement :

-   SourceId

Toutes les autres informations sont retrouvées via la Source.

------------------------------------------------------------------------

# 3. Workflow

1.  Publier normalement sur un réseau social.
2.  Copier l'URL de la publication.
3.  Dans LAWIM → **Nouvelle Source**.
4.  Coller l'URL.
5.  LAWIM crée automatiquement la Source.
6.  Génération automatique du Reference Code.
7.  Analyse IA.
8.  Création du SourceContext.
9.  Génération automatique du lien WhatsApp contenant le Reference Code.
10. L'utilisateur remplace simplement le lien présent dans sa
    publication.

L'IA est facultative. Le système doit fonctionner même si elle est
indisponible.

------------------------------------------------------------------------

# 4. Modèle de données

## Source

-   id
-   referenceCode
-   status
-   createdAt
-   createdBy
-   target

## SourceContext

-   sourceId
-   network
-   publicationUrl
-   publicationTitle
-   publicationText
-   publicationAuthor
-   campaign
-   city
-   district
-   propertyType
-   targetAudience
-   format
-   language
-   tags
-   aiClassification
-   aiConfidence
-   notes

## Lead

Ajouter :

-   sourceId

------------------------------------------------------------------------

# 5. IA

Créer un service chargé d'extraire automatiquement :

-   ville
-   quartier
-   type de bien
-   cible
-   sujet
-   langue
-   hashtags
-   ton
-   sentiment
-   format
-   call-to-action

Les résultats sont enregistrés dans SourceContext et restent
modifiables.

------------------------------------------------------------------------

# 6. Tableau de bord

Chaque Source affiche :

-   Reference Code
-   Canal
-   URL
-   Statut
-   Date
-   Conversations WhatsApp
-   Leads
-   Clients
-   Taux de conversion
-   Analyse IA

Le tableau de bord doit permettre d'analyser :

-   réseaux sociaux
-   campagnes
-   villes
-   quartiers
-   types de biens
-   formats
-   publics cibles
-   performances

------------------------------------------------------------------------

# 7. Analyse d'impact (obligatoire)

Avant toute implémentation :

-   identifier tous les modules impactés ;
-   identifier toutes les dépendances ;
-   produire un inventaire complet des impacts.

------------------------------------------------------------------------

# 8. Migration de l'existant

Modifier toutes les fonctionnalités utilisant directement ou
indirectement l'ancien Tracking Code.

Inclut notamment :

-   WhatsApp
-   Green API
-   CRM
-   IA
-   Leads
-   campagnes
-   QR Codes
-   ambassadeurs
-   partenaires
-   tableaux de bord
-   statistiques
-   analytics
-   reporting
-   API
-   services
-   jobs
-   scripts
-   tests
-   modèles de données
-   interfaces utilisateur

Supprimer le code obsolète.

------------------------------------------------------------------------

# 9. Analyse des évolutions futures

Identifier toutes les fonctionnalités prévues mais non développées
devant utiliser le SIE.

Adapter leur conception.

Le SIE devient le référentiel unique.

------------------------------------------------------------------------

# 10. Refactoring

Lorsque nécessaire :

-   renommer classes ;
-   services ;
-   DTO ;
-   API ;
-   composants ;
-   événements ;
-   modèles ;
-   supprimer les duplications ;
-   simplifier les workflows.

------------------------------------------------------------------------

# 11. Documentation (obligatoire)

Aucune implémentation n'est terminée sans documentation.

Mettre à jour :

-   documentation fonctionnelle ;
-   documentation technique ;
-   architecture ;
-   workflows ;
-   modèle de données ;
-   règles métier ;
-   API ;
-   guides utilisateurs ;
-   tableaux de bord ;
-   documentation IA.

------------------------------------------------------------------------

# 12. Migration documentaire

Retrouver toutes les références à l'ancien Tracking Code.

Mettre à jour les documents concernés.

Supprimer les parties obsolètes.

Garantir la cohérence documentaire.

------------------------------------------------------------------------

# 13. Knowledge Packs

Mettre à jour :

-   LAWIM_V2_FULL_KNOWLEDGE_PACK.md
-   LAWIM_V2_DEVELOPER_KNOWLEDGE_PACK.md
-   tous les Knowledge Packs concernés.

Aucune divergence entre code, documentation et Knowledge Packs.

------------------------------------------------------------------------

# 14. Tests

Créer ou adapter les tests pour :

-   création d'une Source ;
-   génération du Reference Code ;
-   import d'une publication ;
-   création du SourceContext ;
-   association Lead → Source ;
-   génération du lien WhatsApp ;
-   statistiques.

------------------------------------------------------------------------

# 15. Vérification de cohérence

Contrôler :

-   code
-   base de données
-   API
-   documentation
-   Knowledge Packs
-   tests
-   workflows
-   événements
-   automatisations

Corriger toute incohérence.

------------------------------------------------------------------------

# 16. Rapport final

Produire un rapport contenant :

-   fonctionnalités impactées ;
-   fonctionnalités modifiées ;
-   fonctionnalités futures concernées ;
-   migrations ;
-   documentation mise à jour ;
-   fichiers créés ;
-   fichiers modifiés ;
-   tests créés ;
-   risques de régression ;
-   recommandations ;
-   validation finale.

------------------------------------------------------------------------

# 17. Architecture cible

``` text
Campaign
    │
    ▼
Source
    │
    ├── Reference Code
    ├── Canal
    ├── URL
    ├── Statut
    │
    ▼
SourceContext
    │
    ├── Analyse IA
    ├── Ville
    ├── Quartier
    ├── Type
    ├── Campagne
    ├── Tags
    │
    ▼
Lead
    │
    ▼
CRM
    │
    ▼
Marketing Intelligence Dashboard
```

# Objectif final

Le Source Intelligence Engine devient le référentiel unique des sources
d'acquisition de LAWIM.

Le parcours utilisateur reste extrêmement simple :

1.  publier ;
2.  coller l'URL dans LAWIM ;
3.  laisser LAWIM générer le Reference Code, analyser la Source,
    produire le lien WhatsApp et assurer le suivi marketing.
