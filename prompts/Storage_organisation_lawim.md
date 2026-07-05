
# RELEASE PROGRAM AAC-B

# LAWIM STORAGE ORCHESTRATOR

## MASTER IMPLEMENTATION PROMPT

### VERSION 1.0

---

# CONTEXTE

Tu poursuis l'implémentation officielle de LAWIM_V2.

Cette release constitue l'une des fondations techniques les plus importantes de toute la plateforme.

Elle met en place l'architecture définitive de gestion :

* du stockage,
* des médias,
* des sauvegardes,
* de l'archivage,
* de la restauration,
* de la synchronisation,
* du cycle de vie des données,
* et de l'optimisation des ressources.

Cette architecture devra pouvoir accompagner LAWIM pendant de nombreuses années sans remise en cause majeure.

---

# PRINCIPES GÉNÉRAUX

Cette release est :

* additive uniquement ;
* rétrocompatible avec LAWIM 1.0 ;
* compatible avec LAWIM 2.0 ;
* compatible avec LAWIM 3.0 ;
* indépendante du fournisseur de stockage ;
* extensible.

Aucune régression n'est autorisée.

Aucun contrat backend existant ne doit être modifié.

Aucune API existante ne doit être cassée.

---

# PHILOSOPHIE DE L'ARCHITECTURE

LAWIM ne doit jamais dépendre d'un fournisseur de stockage.

Google Drive n'est qu'un fournisseur.

Demain ce pourra être :

* OneDrive
* Amazon S3
* Cloudflare R2
* Backblaze
* Wasabi
* MinIO
* NAS
* FTP
* SFTP
* tout autre fournisseur.

Le changement de fournisseur ne doit jamais provoquer une modification des données métier.

---

# OBJECTIFS

Construire la plateforme définitive de gestion des données.

Elle comprend :

* Storage Orchestrator
* Backup Center
* Media Registry
* Lifecycle Engine
* Backup Manager
* Restore Manager
* Storage Optimizer
* Distributed Storage Manager
* External Backup Manager
* Storage Setup Wizard

---

# ARCHITECTURE VALIDÉE

```
                   LAWIM VPS OVH

        données actives
        PostgreSQL
        Redis
        miniatures
        cache
        médias chauds

                    │
                    │
                    ▼

        Synchronisation quotidienne

                    │
                    ▼

          BACKUP CENTER

        (Laptop / PC / NAS)

                    │

     Vérification
     Compression
     Déduplication
     Chiffrement
     Validation

                    │
                    ▼

       Distribution automatique

                    │
                    ▼

        10 Google Drive

                    │
                    ▼

    Sauvegarde hebdomadaire

                    │
                    ▼

          Disque dur externe
```

---

# RÔLE DU VPS

Le VPS n'est PAS une sauvegarde.

Le VPS contient uniquement :

* les services LAWIM ;
* PostgreSQL actif ;
* Redis ;
* les fichiers actifs ;
* les miniatures ;
* les fichiers récemment créés ;
* les fichiers fréquemment utilisés.

Les médias archivés pourront quitter le VPS selon leur cycle de vie.

---

# RÔLE DU BACKUP CENTER

Le Backup Center devient le cœur du système de sauvegarde.

Il ne représente PAS obligatoirement un ordinateur portable.

Il constitue une abstraction.

Il pourra être :

* un Laptop ;
* un PC fixe ;
* un NAS ;
* un serveur dédié de sauvegarde.

Le reste de LAWIM ne devra jamais connaître le matériel utilisé.

Le Backup Center est responsable de :

* récupérer les nouveautés ;
* vérifier les checksums ;
* compresser ;
* dédupliquer ;
* chiffrer ;
* distribuer ;
* restaurer ;
* conserver l'historique ;
* copier vers le disque externe.

---

# RÈGLE ABSOLUE

Aucune synchronisation Google Drive ne doit partir directement du VPS.

Le flux officiel est toujours :

```
OVH

↓

Backup Center

↓

Google Drive

↓

Disque externe
```

Cette règle garantit :

* la réduction de la bande passante ;
* la possibilité de contrôler les sauvegardes ;
* la validation avant diffusion ;
* la restauration centralisée.

---

# RÔLE DES GOOGLE DRIVE

Les dix comptes Google Drive ne sont PAS des sauvegardes temporaires.

Ils constituent ensemble :

**la mémoire distribuée permanente de LAWIM.**

Ils conservent les données archivées après leur sortie du VPS.

Ils permettent :

* la conservation long terme ;
* la redondance ;
* la haute disponibilité ;
* la réduction du stockage OVH.

---

# RÉPARTITION VALIDÉE DES 10 GOOGLE DRIVE

### Drive 1

Vidéos et audio (lot A)

### Drive 2

Vidéos et audio (lot B)

### Drive 3

Vidéos et audio (lot C)

### Drive 4

Photos originales

### Drive 5

Documents

PDF

Word

Excel

Plans

Contrats

### Drive 6

Base PostgreSQL

Media Registry

Configurations

Secrets chiffrés

Exports critiques

### Drive 7

Archives froides

Anciennes données

Historique

### Drive 8

Débordement intelligent

Overflow automatique

### Drive 9

Quarantaine

Restauration

Validation

### Drive 10

Réplication critique

Index global

Métadonnées de secours

---

# OBJECTIF DE CETTE RÉPARTITION

Équilibrer :

* la charge ;
* les performances ;
* la bande passante ;
* la croissance future ;
* les restaurations.

Aucun Drive ne devra atteindre 100 %.

Le Storage Orchestrator devra maintenir automatiquement l'équilibre.

## RELEASE PROGRAM AAC-B

# PARTIE 2 — STORAGE ORCHESTRATOR, MEDIA REGISTRY ET LIFECYCLE ENGINE

---

# STORAGE ORCHESTRATOR

Le Storage Orchestrator constitue le cerveau de toute la plateforme de stockage.

Aucun module de LAWIM ne décide directement où enregistrer un fichier.

Tous les modules passent obligatoirement par le Storage Orchestrator.

Il reçoit une demande.

Il prend une décision.

Puis il délègue cette décision au fournisseur de stockage approprié.

---

# RESPONSABILITÉS

Le Storage Orchestrator doit décider automatiquement :

* où enregistrer un nouveau média ;
* quand déplacer un média ;
* quand archiver un média ;
* quand restaurer un média ;
* quand supprimer un original du VPS ;
* quand répliquer un média ;
* quand équilibrer les Google Drive ;
* quand lancer une synchronisation.

Aucun utilisateur ne choisit directement le Drive.

---

# CRITÈRES DE DÉCISION

Chaque décision doit être basée sur :

* type du fichier ;
* taille ;
* catégorie ;
* priorité métier ;
* fréquence d'utilisation ;
* nombre de consultations ;
* espace libre ;
* niveau de saturation ;
* historique ;
* politique de conservation.

---

# ÉQUILIBRAGE INTELLIGENT

Le système surveille en permanence l'occupation des dix Google Drive.

Règles :

```text
0–70 %      fonctionnement normal

70–85 %     surveillance

85–92 %     ralentissement

>92 %       arrêt des nouvelles écritures importantes
             migration automatique
```

Le rééquilibrage doit être totalement transparent.

---

# FOURNISSEURS DE STOCKAGE

Le Storage Orchestrator ne connaît jamais Google Drive directement.

Il dialogue uniquement avec des Providers.

Exemple :

```text
Storage Orchestrator

↓

Storage Provider

↓

Google Drive Provider

↓

Google API
```

Demain le Provider pourra être :

* OneDrive
* Dropbox
* Amazon S3
* Cloudflare R2
* Backblaze
* Wasabi
* MinIO
* NAS
* FTP
* SFTP

sans modifier LAWIM.

---

# STORAGE PROVIDER

Créer une abstraction complète.

Chaque Provider devra exposer les mêmes opérations :

```text
save()

read()

restore()

archive()

delete()

move()

copy()

checksum()

exists()

generateSecureAccess()

health()

quota()

usage()
```

Aucun Provider ne doit casser les autres.

---

# MEDIA REGISTRY

Le Media Registry devient la source unique de vérité.

Tous les médias y sont enregistrés.

Aucun média ne peut exister sans Media Registry.

---

# RÈGLE ABSOLUE

Les objets métier ne connaissent jamais le stockage.

Un bien immobilier ne connaît jamais :

* Google Drive
* Dropbox
* OneDrive
* Amazon S3

Il connaît uniquement :

```text
Property

↓

MediaID
```

---

# STRUCTURE

Chaque média possède :

```text
MediaID

Nom

Extension

Type

Taille

Checksum

MimeType

Créateur

Date création

Dernière modification

Dernière consultation

Nombre de consultations

Statut

Provider

Provider FileID

Drive logique

Emplacement VPS

Emplacement Backup Center

Emplacement Cloud

Date synchronisation

Date archivage

Date restauration

Date suppression OVH

Miniature

Version

Historique

Priorité

Classification

Niveau de sécurité
```

---

# URL

Aucune URL Google Drive ne doit être enregistrée.

Interdiction absolue.

Le système conserve uniquement :

```text
Provider

FileID

MediaID
```

---

# ACCÈS AUX MÉDIAS

Lorsqu'un utilisateur ouvre un bien :

```text
Bien

↓

MediaID

↓

Media Registry

↓

Storage Orchestrator

↓

Provider

↓

FileID

↓

Lien temporaire sécurisé

↓

Utilisateur
```

Le lien est généré à la demande.

---

# AVANTAGES

Un fichier peut :

* changer de Drive ;
* changer de compte Google ;
* changer de fournisseur ;
* être déplacé ;
* être restauré ;

sans casser les liens.

---

# MINIATURES

Les miniatures restent toujours sur OVH.

Même lorsque l'original est archivé.

Ainsi :

* les listes restent rapides ;
* les recherches restent instantanées ;
* les fiches immobilières restent fluides.

---

# LIFECYCLE ENGINE

Créer un moteur de cycle de vie intelligent.

Il décide automatiquement :

* conservation ;
* archivage ;
* restauration ;
* suppression ;
* réplication.

---

# ÉTATS

Chaque média peut être :

```text
NEW

HOT

WARM

COLD

ARCHIVED

RESTORE_PENDING

RESTORED

DELETED
```

---

# CRITÈRES

Le moteur ne décide jamais uniquement avec l'âge.

Il prend également en compte :

* fréquence d'utilisation ;
* taille ;
* priorité métier ;
* importance ;
* nombre de consultations ;
* dépendances.

---

# EXEMPLES

### Vidéo récente

```text
HOT
```

---

### Photo rarement consultée

```text
COLD
```

---

### Ancien contrat

```text
ARCHIVED
```

---

### Média demandé

```text
RESTORE_PENDING

↓

RESTORED
```

---

# STORAGE OPTIMIZER

Créer un moteur d'optimisation permanent.

Objectifs :

* réduire les doublons ;
* compresser ;
* optimiser les transferts ;
* réduire les écritures ;
* équilibrer les Drives ;
* réduire les coûts ;
* limiter la bande passante.

---

# SYNCHRONISATION DELTA

Ne jamais recopier un fichier inchangé.

Comparer :

* checksum ;
* taille ;
* version ;
* date.

Synchroniser uniquement les différences.

---

# DÉDUPLICATION

Deux fichiers identiques ne doivent jamais être stockés deux fois.

Utiliser le checksum.

---

# COMPRESSION

Les documents et archives doivent être compressés avant distribution lorsque cela est pertinent, sans perte de données.

Les médias déjà compressés (JPEG, MP4, MP3, etc.) ne doivent pas être recompressés inutilement.

---

# OPTIMISATION BANDE PASSANTE

Les transferts doivent privilégier :

* les synchronisations nocturnes programmées ;
* les transferts différentiels (delta) ;
* la reprise automatique après interruption ;
* la limitation du débit si nécessaire pour ne pas perturber les utilisateurs.

---

# SURVEILLANCE

Le Storage Optimizer doit produire des indicateurs sur :

* taux de compression ;
* espace économisé ;
* doublons éliminés ;
* bande passante économisée ;
* répartition des données ;
* évolution de l'occupation des supports.

---

La **Partie 3** couvrira le **Backup Center**, le **Storage Setup Wizard**, les tableaux de bord Administrateur/Gestionnaire, les politiques de sauvegarde, les restaurations, les validations, la documentation, les rapports et la clôture Git de la release **AAC-B**.


# RELEASE PROGRAM AAC-B

# PARTIE 3 — BACKUP CENTER, STORAGE SETUP WIZARD, DASHBOARDS, RESTAURATION, VALIDATION ET CLÔTURE

---

# BACKUP CENTER

Le **Backup Center** devient le centre officiel de sauvegarde de LAWIM.

Il ne s'agit pas d'un simple dossier de sauvegarde.

Il constitue une plateforme de gestion capable de :

* recevoir les synchronisations du VPS ;
* vérifier les fichiers ;
* préparer les distributions ;
* conserver les historiques ;
* restaurer les données ;
* piloter les Google Drive ;
* piloter les sauvegardes externes.

Le Backup Center est le seul point d'entrée des sauvegardes.

---

# FLUX OFFICIEL

Aucun flux alternatif n'est autorisé.

```text
OVH VPS
      │
      ▼
Backup Center
      │
      ├────────► Google Drive
      │
      └────────► Disque externe
```

---

# SAUVEGARDE QUOTIDIENNE

Chaque jour :

```text
OVH

↓

Détection des nouveautés

↓

Checksum

↓

Compression

↓

Déduplication

↓

Synchronisation vers Backup Center

↓

Validation

↓

Distribution Google Drive
```

---

# SAUVEGARDE HEBDOMADAIRE

Une fois par semaine :

```text
Backup Center

↓

Disque externe

↓

Checksum

↓

Validation

↓

Journal
```

Cette sauvegarde est totalement indépendante des Google Drive.

---

# RESTAURATION

Le système doit permettre :

## restauration d'un média

## restauration d'un dossier

## restauration d'un client

## restauration d'un projet

## restauration PostgreSQL

## restauration complète

---

# RESTAURATION D'UN MÉDIA

Le processus est :

```text
MediaID

↓

Media Registry

↓

Storage Orchestrator

↓

Provider

↓

Google Drive

↓

Backup Center

↓

OVH

↓

Utilisateur
```

Le processus est entièrement automatique.

---

# STORAGE SETUP WIZARD

Créer un assistant graphique complet.

ATTENTION

Il ne sera jamais exécuté pendant cette release.

Il sera utilisé uniquement lors de la première mise en production.

---

# LE WIZARD DOIT CONFIGURER

## serveur LAWIM

## Backup Center

Le Backup Center pourra être :

* Laptop
* PC fixe
* NAS
* Serveur dédié

LAWIM ne devra jamais dépendre du matériel.

---

## Google Drive

Ajouter graphiquement :

les 10 comptes.

Pour chacun :

* nom logique
* priorité
* quota
* catégorie
* stratégie

Les identifiants réels seront renseignés uniquement lors de la mise en production.

---

## disque externe

Détection automatique.

Validation.

Historique.

---

## politiques

Configurer :

* synchronisation
* archivage
* restauration
* optimisation
* seuils

---

# IMPORTANT

Pendant AAC-B

Ne jamais demander :

* Client ID Google
* Client Secret
* Refresh Token
* Clé SSH
* Mot de passe
* Secret de production

Utiliser uniquement :

* interfaces
* modèles
* placeholders

---

# DASHBOARD ADMINISTRATEUR

Créer un tableau de bord complet.

Afficher :

Occupation VPS

Occupation Backup Center

Occupation des dix Google Drive

Occupation disque externe

Historique

Alertes

Synchronisations

Archivages

Restaurations

Optimisations

Rééquilibrages

Checksum

Compression

Déduplication

Bande passante

Coût estimé

Santé générale

---

# DASHBOARD GESTIONNAIRE

Créer une version simplifiée.

Afficher :

Dernière sauvegarde

Dernière synchronisation

Nombre de médias archivés

Nombre de restaurations

Alertes

État global

---

# ALERTES

Créer un moteur d'alertes.

Exemples :

Drive presque plein

Erreur checksum

Erreur synchronisation

Erreur restauration

Google Drive indisponible

Disque externe absent

Backup Center inaccessible

---

# HISTORIQUE

Toutes les opérations doivent être historisées.

Conserver :

date

heure

utilisateur

action

résultat

durée

fichier

taille

checksum

provider

---

# LOGS

Créer des journaux spécialisés :

Storage Log

Backup Log

Restore Log

Optimization Log

Synchronization Log

Lifecycle Log

Audit Log

---

# TABLEAUX DE BORD D'OPTIMISATION

Afficher :

CPU économisé

RAM économisée

Bande passante économisée

Stockage économisé

Compression

Déduplication

Coût mensuel estimé

Évolution

---

# DOCUMENTATION À PRODUIRE

Créer :

BACKUP_CENTER.md

BACKUP_MANAGER.md

RESTORATION_ENGINE.md

STORAGE_ORCHESTRATOR.md

MEDIA_REGISTRY.md

MEDIA_PROVIDER_ABSTRACTION.md

GOOGLE_DRIVE_DISTRIBUTED_STORAGE.md

STORAGE_SETUP_WIZARD.md

DATA_RETENTION_POLICY.md

LINK_RESOLUTION_ARCHITECTURE.md

MEDIA_ARCHIVING.md

LIFECYCLE_ENGINE.md

STORAGE_OPTIMIZER.md

BACKUP_SECURITY.md

RESTORE_POLICY.md

---

# RAPPORTS

Créer :

RELEASE-PROGRAM-AAC-B-BACKUP-CENTER.md

RELEASE-PROGRAM-AAC-B-STORAGE-ORCHESTRATOR.md

RELEASE-PROGRAM-AAC-B-LIFECYCLE.md

RELEASE-PROGRAM-AAC-B-STORAGE-OPTIMIZER.md

RELEASE-PROGRAM-AAC-B-MEDIA-REGISTRY.md

RELEASE-PROGRAM-AAC-B-LINK-ABSTRACTION.md

RELEASE-PROGRAM-AAC-B-BANDWIDTH-OPTIMIZATION.md

RELEASE-PROGRAM-AAC-B-DISTRIBUTED-STORAGE.md

---

# TESTS À AJOUTER

Créer des tests couvrant notamment :

* Storage Orchestrator
* Media Registry
* Lifecycle Engine
* Storage Provider
* Google Drive Manager
* Backup Center
* Restore Engine
* Storage Optimizer
* Storage Setup Wizard
* tableaux de bord

Objectif :

100 % des nouveaux modules testés.

---

# VALIDATIONS OBLIGATOIRES

Exécuter :

```bash
npm install

npm run typecheck

npm run test

npm run build

git diff --check
```

Aucune erreur.

Aucun warning critique.

Aucune régression.

---

# GIT

Créer un seul commit.

Message :

```text
feat(storage): implement distributed storage orchestrator and backup platform
```

Créer le tag :

```text
release-program-aac-b
```

Pousser vers :

```text
develop/2.0-intelligent-platform
```

---

# LIVRABLE FINAL

À la fin de l'exécution, retourner uniquement :

* résumé des fonctionnalités implémentées ;
* résultats des validations ;
* nombre de nouveaux modules créés ;
* nombre de tests ajoutés et réussis ;
* documentation générée ;
* rapports générés ;
* hash du commit ;
* tag Git ;
* état Git final ;
* confirmation que tous les biens immobiliers utilisent exclusivement le **Media Registry** comme point d'accès aux médias ;
* confirmation qu'aucune URL Google Drive n'est stockée dans les données métier ;
* confirmation que le système est rétrocompatible avec LAWIM 1.0 ;
* confirmation qu'il prépare nativement LAWIM 2.0 et LAWIM 3.0 ;
* confirmation que l'architecture permet de remplacer Google Drive par n'importe quel autre fournisseur de stockage sans modifier les données métier ni casser les liens existants.

---

Avec ces trois parties, tu disposes d'une **spécification de niveau architecture** pour AAC-B. Elle formalise non seulement l'implémentation, mais aussi les règles de gouvernance, d'évolutivité et de pérennité du stockage de LAWIM. C'est une base suffisamment robuste pour accompagner les futures évolutions de la plateforme sans remettre en cause les choix fondamentaux que nous avons validés.


