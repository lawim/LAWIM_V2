# LAWIM

# 14-STORAGE-REFERENCE.md

# Référentiel officiel du stockage, de l'archivage et des sauvegardes

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le présent document définit les règles officielles de stockage, d'archivage, de sauvegarde et de restauration de LAWIM.

Il constitue la référence unique pour :

* la persistance des données ;
* l'archivage des fichiers ;
* les sauvegardes ;
* la restauration ;
* la conservation à long terme ;
* la réversibilité opérationnelle ;
* la conformité des durées de conservation.

---

# CHAPITRE 2 — PRINCIPE FONDAMENTAL

Toute donnée stockée dans LAWIM doit pouvoir être :

* retrouvée ;
* auditée ;
* restaurée ;
* historisée ;
* déplacée vers l'archive ;
* supprimée uniquement selon une procédure validée.

Le stockage n'est jamais un simple dépôt de fichiers. Il fait partie du cycle de vie métier.

---

# CHAPITRE 3 — HIERARCHIE OFFICIELLE

L'architecture de stockage suit l'ordre imposé suivant :

```text
OVH
↓
Serveur local
↓
Sauvegarde hebdomadaire sur disque externe
↓
9 Google Drive spécialisés
↓
Archivage intelligent
```

Le niveau supérieur ne remplace pas le niveau inférieur. Chaque couche a un rôle spécifique.

---

# CHAPITRE 4 — RÔLE DE CHAQUE COUCHE

## OVH

Couche d'hébergement principale des services et des données actives.

## Serveur local

Couche d'exploitation locale, de cache contrôlé, d'outillage et de continuité.

## Disque externe hebdomadaire

Copie de sécurité périodique destinée à la reprise rapide et au contrôle hors ligne.

## Google Drive spécialisés

Espaces de stockage séparés par usage métier.

## Archivage intelligent

Classement, conservation, réversibilité et contrôle de fin de vie des actifs.

---

# CHAPITRE 5 — RÉPARTITION DES 9 GOOGLE DRIVE

La répartition officielle est la suivante :

| Drive | Usage officiel |
| --- | --- |
| Drive 1 | Vidéos |
| Drive 2 | Vidéos |
| Drive 3 | Vidéos |
| Drive 4 | Documents officiels |
| Drive 5 | Photos + audios |
| Drive 6 | Sauvegardes PostgreSQL + Prisma |
| Drive 7 | Archives métiers |
| Drive 8 | Snapshots + PRA |
| Drive 9 | Knowledge LAWIM + IA |

Cette répartition ne doit pas être inversée sans validation humaine.

---

# CHAPITRE 6 — CLASSES DE DONNÉES

LAWIM distingue au minimum les classes suivantes :

* données métier actives ;
* médias ;
* documents officiels ;
* sauvegardes techniques ;
* archives métier ;
* connaissances et référentiels ;
* snapshots de reprise ;
* journaux et traces d'audit.

Chaque classe possède sa propre politique de stockage.

---

# CHAPITRE 7 — PRINCIPES D'AFFECTATION

Les données doivent être affectées selon leur nature :

* les médias lourds vont dans les espaces dédiés aux médias ;
* les documents officiels vont dans l'espace documentaire officiel ;
* les sauvegardes de base de données vont dans les espaces de sauvegarde ;
* les connaissances opérationnelles vont dans le Drive Knowledge ;
* les snapshots de PRA vont dans l'espace de reprise ;
* les archives métiers vont dans l'espace d'archives.

Les duplications inutiles sont interdites.

---

# CHAPITRE 8 — SAUVEGARDES

Les sauvegardes doivent être :

* régulières ;
* vérifiables ;
* testées ;
* restaurables ;
* historisées.

La séquence officielle unique est la suivante :

1. Serveur OVH (Production) ;
2. Synchronisation automatique vers le serveur local ;
3. Sauvegarde locale ;
4. Sauvegarde hebdomadaire sur disque externe ;
5. Synchronisation automatique vers les 9 Google Drive spécialisés ;
6. Vérification d'intégrité ;
7. Test automatique de restauration ;
8. Rapport automatique ;
9. Notification d'échec.

La sauvegarde hebdomadaire sur disque externe constitue le minimum officiel de reprise hors ligne.

Toute sauvegarde critique doit pouvoir être restaurée sans dépendre d'un seul support.

---

# CHAPITRE 9 — RESTAURATION

La restauration doit toujours être préparée, documentée et testée.

Les scénarios minimaux sont :

* restauration d'un fichier ;
* restauration d'une base PostgreSQL ;
* restauration d'un ensemble documentaire ;
* restauration d'un snapshot de reprise ;
* restauration partielle après incident.

Les tests de restauration doivent être réalisés périodiquement et documentés.

La restauration ne doit jamais détruire l'historique disponible sans procédure explicite.

---

# CHAPITRE 10 — ARCHIVAGE

L'archivage conserve les éléments qui ne sont plus actifs mais doivent rester consultables ou opposables.

L'archivage doit préserver :

* le contexte ;
* la date ;
* l'auteur ;
* la source ;
* le lien avec le dossier d'origine ;
* la traçabilité des modifications.

L'archivage n'est pas une suppression.

---

# CHAPITRE 11 — CONSERVATION ET DÉLÉTION

Les durées de conservation sont déterminées :

* par la nature de la donnée ;
* par les obligations légales ;
* par les besoins de reprise ;
* par les règles de gouvernance.

La suppression définitive n'est autorisée que :

* si elle est explicitement prévue ;
* si elle est légalement admissible ;
* si elle est tracée ;
* si elle est validée par l'autorité compétente.

---

# CHAPITRE 12 — SÉCURITÉ

Le stockage doit garantir :

* le contrôle d'accès ;
* la séparation des environnements ;
* la confidentialité ;
* l'intégrité ;
* la disponibilité ;
* la résistance aux suppressions accidentelles.

Les contenus sensibles doivent être chiffrés ou protégés selon leur nature.

---

# CHAPITRE 13 — TRAÇABILITÉ

Toute opération de stockage, d'archivage ou de restauration doit être historisée.

L'historique enregistre au minimum :

* l'objet concerné ;
* l'action réalisée ;
* l'auteur ;
* la date ;
* le support de destination ;
* le motif ;
* le résultat.

---

# CHAPITRE 14 — INTERACTIONS AVEC LES AUTRES MOTEURS

Le Storage Lifecycle Manager sert les autres moteurs sans les remplacer.

Il alimente notamment :

* le Reporting Engine ;
* le Role Engine ;
* le Dashboard Engine ;
* le Notification Engine ;
* le Workflow Engine ;
* le Matching Engine ;
* LAWIM AI.

Chaque moteur consomme les données stockées selon ses permissions.

---

# CHAPITRE 15 — OBJECTIF FINAL

Le stockage LAWIM doit permettre une exploitation durable, une reprise fiable, une conservation maîtrisée et une traçabilité complète des actifs de la plateforme.

Il protège les données, les référentiels et les archives tout en restant compatible avec l'architecture globale de LAWIM.

---

# FIN DU DOCUMENT

Le présent **14-STORAGE-REFERENCE.md** constitue la référence officielle du stockage, de l'archivage et des sauvegardes de LAWIM.
