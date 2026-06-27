LAWIM
11-REPORTING-REFERENCE.md
PARTIE 1
Principes fondamentaux

Version 1.0

CHAPITRE 1 — OBJECTIF

Le présent document définit les règles officielles de production, de diffusion, d'exploitation et de gouvernance des rapports et indicateurs de LAWIM.

Il constitue la référence unique pour :

les tableaux de bord ;
les statistiques ;
les indicateurs de performance ;
les rapports d'activité ;
les analyses décisionnelles ;
les analyses prédictives ;
les exports.

Toutes les données de reporting sont produites exclusivement par le Reporting Engine.

CHAPITRE 2 — PRINCIPE FONDAMENTAL

Le Reporting Engine ne crée aucune donnée.

Il exploite uniquement les données validées provenant des autres moteurs de LAWIM.

Il transforme ces données en :

indicateurs ;
graphiques ;
tableaux ;
synthèses ;
rapports.

Le Reporting Engine constitue la source officielle de toutes les statistiques de LAWIM.

CHAPITRE 3 — SOURCES DE DONNÉES

Le Reporting Engine exploite notamment les données provenant :

Workflow Engine ;
Matching Engine ;
Conversation Engine ;
Role Engine ;
Geo Engine ;
Notification Engine ;
Dashboard Engine ;
Storage Lifecycle Manager ;
LAWIM AI ;
Campay Payment Engine ;
29-CAMPAY-PAYMENT-REFERENCE.md pour les paiements Campay ;
02I-PRICING-REFERENCE.md pour les analyses de prix ;
30-I18N-L10N-REFERENCE.md ;
30B-TRANSLATION-REFERENCE.md ;
30D-MULTILINGUAL-SEARCH-REFERENCE.md.

Aucune donnée externe n'est utilisée sans validation.

CHAPITRE 4 — TYPES DE REPORTING

LAWIM distingue plusieurs familles.

Reporting opérationnel.
Reporting métier.
Reporting décisionnel.
Reporting financier.
Reporting géographique.
Reporting qualité.
Reporting sécurité.
Reporting technique.

Chaque famille possède ses propres indicateurs.

CHAPITRE 5 — PÉRIODES D'ANALYSE

Les indicateurs peuvent être calculés :

en temps réel ;
par heure ;
par jour ;
par semaine ;
par mois ;
par trimestre ;
par semestre ;
par année ;
sur une période personnalisée.

Les comparaisons entre périodes sont possibles.

CHAPITRE 6 — UTILISATEURS

Les rapports sont adaptés selon le rôle.

Exemples :

demandeur ;
propriétaire ;
agence ;
partenaire ;
conseiller LAWIM ;
administrateur.

Chaque utilisateur ne voit que les informations auxquelles il est autorisé.

CHAPITRE 7 — TRAÇABILITÉ

Chaque indicateur doit être explicable.

Le Reporting Engine doit permettre d'identifier :

sa source ;
sa période ;
son mode de calcul ;
sa date de génération.
CHAPITRE 8 — OBJECTIF FINAL

Le Reporting Engine permet de mesurer objectivement l'activité de LAWIM et de fournir des informations fiables pour le pilotage opérationnel, stratégique et décisionnel.

FIN DE LA PARTIE 1
PARTIE 2
Référentiel officiel des indicateurs

Version 1.0

CHAPITRE 9 — PRINCIPE FONDAMENTAL

Tous les indicateurs utilisés dans LAWIM doivent appartenir au catalogue officiel.

Chaque indicateur possède :

un identifiant ;
un nom ;
une définition ;
une formule de calcul ;
une fréquence de mise à jour ;
une source.
CHAPITRE 10 — INDICATEURS UTILISATEURS

Exemples.

utilisateurs inscrits ;
nouveaux utilisateurs ;
utilisateurs actifs ;
utilisateurs inactifs ;
utilisateurs connectés ;
évolution des inscriptions ;
évolution des rôles.
CHAPITRE 11 — INDICATEURS DES BIENS

Exemples.

biens publiés ;
biens actifs ;
biens archivés ;
biens loués ;
biens vendus ;
durée moyenne de publication ;
délai moyen de mise en relation.

Ces indicateurs peuvent être ventilés par type de bien.

Ils peuvent aussi être ventilés par langue d'utilisation afin de suivre la répartition des utilisateurs, recherches, conversations, paiements et notifications en Français, English et Pidgin English.

Le Reporting Engine s'appuie pour cela sur 30-I18N-L10N-REFERENCE.md, 30B-TRANSLATION-REFERENCE.md et 30D-MULTILINGUAL-SEARCH-REFERENCE.md.

CHAPITRE 12 — INDICATEURS DES DEMANDES

Exemples.

demandes créées ;
demandes satisfaites ;
demandes expirées ;
demandes archivées ;
temps moyen avant premier matching.
CHAPITRE 13 — INDICATEURS DE MATCHING

Exemples.

nombre de matchings ;
taux de matching ;
délai moyen ;
score moyen ;
matchings refusés ;
matchings expirés.
CHAPITRE 14 — INDICATEURS DE CONVERSATION

Exemples.

conversations créées ;
conversations actives ;
messages échangés ;
documents partagés ;
temps moyen de réponse.
CHAPITRE 15 — INDICATEURS DE SERVICES

Exemples.

missions créées ;
missions terminées ;
missions annulées ;
durée moyenne ;
satisfaction.

Pour les services payants, le Reporting Engine suit également :

* paiements initiés ;
* paiements confirmés ;
* paiements échoués ;
* paiements en attente ;
* taux de rapprochement ;
* délais de confirmation.
CHAPITRE 16 — INDICATEURS GÉOGRAPHIQUES

Exemples.

biens par ville ;
biens par quartier ;
demandes par secteur ;
couverture des agences ;
couverture des partenaires ;
Zones LAWIM les plus actives.
CHAPITRE 17 — INDICATEURS DES NOTIFICATIONS

Exemples.

notifications envoyées ;
notifications lues ;
taux d'ouverture ;
taux d'échec ;
temps moyen de lecture.
CHAPITRE 18 — ÉVOLUTIVITÉ

Tout nouvel indicateur doit être ajouté au présent référentiel avant son implémentation.

FIN DE LA PARTIE 2
PARTIE 3
Reporting opérationnel

Version 1.0

CHAPITRE 19 — PRINCIPE FONDAMENTAL

Le reporting opérationnel permet de suivre l'activité quotidienne de LAWIM.

Il fournit une vision en temps réel des opérations en cours.

CHAPITRE 20 — ACTIVITÉ GLOBALE

Le Reporting Engine produit notamment :

activité de la journée ;
activité de la semaine ;
activité du mois ;
activité annuelle.
CHAPITRE 21 — SUIVI DES BIENS

Visualisation notamment de :

nouveaux biens ;
biens modifiés ;
biens archivés ;
biens en attente de validation.
CHAPITRE 22 — SUIVI DES DEMANDES

Visualisation notamment de :

nouvelles demandes ;
demandes satisfaites ;
demandes sans matching ;
demandes en attente de relance.
CHAPITRE 23 — SUIVI DES SERVICES

Visualisation notamment de :

missions programmées ;
missions en cours ;
missions terminées ;
missions en retard.
CHAPITRE 24 — SUIVI DES ÉQUIPES

Pour l'équipe LAWIM et les agences.

Exemples :

dossiers en attente ;
validations à effectuer ;
charge par conseiller ;
charge par agence ;
interventions urgentes.
CHAPITRE 25 — ALERTES OPÉRATIONNELLES

Le Reporting Engine met en évidence les situations nécessitant une attention particulière.

Exemples :

accumulation de dossiers ;
absence de matching ;
retards de traitement ;
notifications en échec ;
missions bloquées.

Ces alertes sont transmises au Dashboard Engine afin d'être affichées de manière visible aux utilisateurs concernés.

CHAPITRE 26 — OBJECTIF FINAL

Le reporting opérationnel permet à LAWIM de piloter en temps réel l'activité de la plateforme, d'identifier rapidement les anomalies et de faciliter les prises de décision quotidiennes grâce à des indicateurs fiables et actualisés.

FIN DE LA PARTIE 3


LAWIM
11-REPORTING-REFERENCE.md
PARTIE 4
Reporting métier

Version 1.0

CHAPITRE 27 — PRINCIPE FONDAMENTAL

Le reporting métier permet à chaque acteur de LAWIM de suivre son activité.

Les rapports sont adaptés au rôle de l'utilisateur.

Chaque acteur visualise uniquement les informations correspondant à ses responsabilités.

CHAPITRE 28 — REPORTING DEMANDEUR

Le demandeur peut consulter notamment :

nombre de recherches actives ;
recherches archivées ;
biens proposés ;
taux de matching ;
temps moyen avant premier matching ;
conversations ouvertes ;
visites programmées ;
services demandés.
CHAPITRE 29 — REPORTING DÉTENTEUR DE BIENS

Le détenteur consulte notamment :

biens actifs ;
biens archivés ;
nombre de consultations ;
nombre de matchings ;
nombre de conversations ;
nombre de visites ;
durée moyenne avant mise en relation ;
taux de transformation (mise en relation aboutissant à une location ou à une vente).
CHAPITRE 30 — REPORTING AGENCES

Les agences disposent notamment :

portefeuille de biens ;
portefeuille de demandeurs ;
biens publiés ;
biens retirés ;
performances par agent ;
performances par secteur ;
missions en cours ;
activité quotidienne ;
évolution mensuelle.
CHAPITRE 31 — REPORTING PARTENAIRES

Les partenaires visualisent notamment :

missions reçues ;
missions acceptées ;
missions terminées ;
délais moyens ;
satisfaction des utilisateurs ;
répartition géographique des interventions.
CHAPITRE 32 — REPORTING ÉQUIPE LAWIM

Les responsables LAWIM disposent notamment :

dossiers en attente ;
validations documentaires ;
interventions urgentes ;
litiges ;
médiations ;
contrôles qualité ;
charge de travail.
CHAPITRE 33 — REPORTING GÉOGRAPHIQUE

Le Reporting Engine fournit notamment :

activité par région ;
activité par ville ;
activité par quartier ;
activité par Zone LAWIM ;
couverture des agences ;
couverture des partenaires ;
densité des biens ;
densité des demandes.
CHAPITRE 34 — OBJECTIF FINAL

Le reporting métier fournit à chaque acteur une vision claire de son activité afin de faciliter le suivi quotidien et l'amélioration continue.

FIN DE LA PARTIE 4
PARTIE 5
Reporting décisionnel

Version 1.0

CHAPITRE 35 — PRINCIPE FONDAMENTAL

Le reporting décisionnel fournit aux responsables de LAWIM les indicateurs nécessaires au pilotage stratégique de la plateforme.

Les données sont consolidées et comparables dans le temps.

CHAPITRE 36 — PILOTAGE GÉNÉRAL

Le Reporting Engine permet notamment de suivre :

croissance de la plateforme ;
évolution des utilisateurs ;
évolution des biens ;
évolution des demandes ;
évolution des organisations ;
évolution des partenaires.
CHAPITRE 37 — PILOTAGE DU MATCHING

Indicateurs notamment :

taux de matching global ;
taux par type de bien ;
délai moyen ;
taux d'échec ;
taux de relance ;
évolution mensuelle.
CHAPITRE 38 — PILOTAGE DES SERVICES

Visualisation notamment :

nombre de missions ;
taux de réalisation ;
délais moyens ;
satisfaction ;
répartition des interventions.
CHAPITRE 39 — PILOTAGE GÉOGRAPHIQUE

Le Reporting Engine permet notamment :

comparaison des villes ;
comparaison des quartiers ;
évolution des Zones LAWIM ;
secteurs insuffisamment couverts ;
zones de forte demande.
CHAPITRE 40 — PILOTAGE DES ÉQUIPES

Indicateurs notamment :

charge par conseiller ;
charge par agence ;
productivité ;
validations réalisées ;
dossiers traités ;
délais de traitement.
CHAPITRE 41 — TENDANCES

Le Reporting Engine met en évidence :

les progressions ;
les diminutions ;
les anomalies ;
les ruptures de tendance.

Les comparaisons peuvent être réalisées entre différentes périodes.

CHAPITRE 42 — OBJECTIF FINAL

Le reporting décisionnel fournit aux dirigeants de LAWIM une vision consolidée permettant d'orienter les décisions stratégiques de la plateforme.

FIN DE LA PARTIE 5
PARTIE 6
Reporting des performances

Version 1.0

CHAPITRE 43 — PRINCIPE FONDAMENTAL

Le reporting des performances mesure l'efficacité des processus, des utilisateurs, des organisations et des moteurs de LAWIM.

Il identifie les points forts, les difficultés et les opportunités d'amélioration.

CHAPITRE 44 — PERFORMANCES DES BIENS

Indicateurs notamment :

délai moyen avant premier matching ;
délai moyen avant location ;
délai moyen avant vente ;
taux de consultation ;
taux de conversion.

Les indicateurs tiennent compte du cycle de vie spécifique de chaque type de bien.

CHAPITRE 45 — PERFORMANCES DES DEMANDES

Le Reporting Engine mesure notamment :

délai moyen de satisfaction ;
taux de satisfaction ;
relances nécessaires ;
recherches élargies ;
demandes archivées sans résultat.
CHAPITRE 46 — PERFORMANCES DES AGENCES

Les agences peuvent suivre notamment :

activité des agents ;
délais de traitement ;
taux de transformation ;
qualité des dossiers ;
satisfaction des clients.
CHAPITRE 47 — PERFORMANCES DES PARTENAIRES

Le Reporting Engine mesure notamment :

ponctualité ;
qualité des prestations ;
délais d'intervention ;
disponibilité ;
taux de satisfaction.

Ces indicateurs peuvent être utilisés pour améliorer l'affectation des missions, sans constituer le seul critère de sélection.

CHAPITRE 48 — PERFORMANCES DES MOTEURS

Le Reporting Engine suit également les performances techniques de LAWIM.

Exemples :

temps moyen de matching ;
temps moyen de génération des notifications ;
temps moyen de réponse des recherches ;
disponibilité des services ;
volume des traitements.

Ces indicateurs servent au pilotage technique de la plateforme.

CHAPITRE 49 — INDICATEURS DE QUALITÉ

Le Reporting Engine mesure notamment :

qualité des annonces ;
qualité des dossiers ;
qualité des localisations ;
qualité des documents ;
taux d'erreurs détectées ;
taux de corrections.
CHAPITRE 50 — COMPARAISONS

Toutes les performances peuvent être comparées :

par heure ;
par jour ;
par semaine ;
par mois ;
par trimestre ;
par année ;

et selon :

le type de bien ;
la région ;
la ville ;
la Zone LAWIM ;
l'agence ;
le partenaire.
CHAPITRE 51 — OBJECTIF FINAL

Le reporting des performances permet à LAWIM d'améliorer en permanence la qualité de ses services, l'efficacité de ses équipes et le fonctionnement de ses moteurs, grâce à des indicateurs objectifs, comparables et exploitables.

FIN DE LA PARTIE 6

# LAWIM

# 11-REPORTING-REFERENCE.md

# PARTIE 7

# Reporting prédictif, analytique et Intelligence Artificielle

Version 1.0

---

# CHAPITRE 52 — PRINCIPE FONDAMENTAL

Le Reporting Engine ne se limite pas à produire des statistiques.

Il constitue également le moteur d'analyse de LAWIM.

À partir des données validées produites par les différents moteurs de la plateforme, il fournit :

* des analyses ;
* des tendances ;
* des prévisions ;
* des recommandations ;
* des indicateurs d'aide à la décision.

Les analyses restent des outils d'assistance. Elles ne remplacent jamais les décisions des utilisateurs ou des administrateurs.

---

# CHAPITRE 53 — ANALYTICS ENGINE

Le Reporting Engine intègre un **Analytics Engine** chargé d'exploiter les données historiques et courantes.

Il permet notamment :

* d'identifier les tendances ;
* de détecter les anomalies ;
* de produire des projections ;
* d'assister LAWIM AI ;
* d'alimenter les Dashboards stratégiques.

L'Analytics Engine travaille exclusivement sur des données validées.

---

# CHAPITRE 54 — ANALYSE DES TENDANCES

Le système analyse en continu les évolutions observées.

Exemples :

* évolution des recherches ;
* évolution des publications ;
* évolution des locations ;
* évolution des ventes ;
* évolution des délais de mise en relation ;
* évolution des services demandés.

Les analyses peuvent être réalisées :

* par quartier ;
* par ville ;
* par région ;
* par Zone LAWIM ;
* par type de bien ;
* par période.

---

# CHAPITRE 55 — ANALYSE DU MARCHÉ IMMOBILIER

Le Reporting Engine fournit des indicateurs permettant de suivre l'évolution du marché.

Exemples :

* quartiers les plus recherchés ;
* secteurs où l'offre est insuffisante ;
* secteurs où la demande diminue ;
* types de biens les plus demandés ;
* durée moyenne de commercialisation ;
* évolution des prix lorsque des données suffisamment fiables sont disponibles.

Ces analyses servent uniquement d'indicateurs et ne constituent pas une estimation officielle du marché.

---

# CHAPITRE 56 — ANALYSE DES COMPORTEMENTS

Le système peut analyser les comportements d'utilisation de manière agrégée.

Exemples :

* fréquence des recherches ;
* horaires de connexion ;
* utilisation des filtres ;
* délais de réponse ;
* taux d'abandon des recherches ;
* fréquence des mises à jour des annonces.

Ces analyses visent exclusivement à améliorer les services proposés par LAWIM.

---

# CHAPITRE 57 — DÉTECTION D'ANOMALIES

L'Analytics Engine identifie automatiquement certaines situations inhabituelles.

Exemples :

* augmentation anormale des publications ;
* baisse brutale du taux de matching ;
* hausse inhabituelle des annulations de visites ;
* accumulation de dossiers en attente ;
* pics de notifications en échec ;
* comportements susceptibles de révéler une fraude ou un usage abusif.

Toute anomalie détectée doit être validée avant de donner lieu à une action.

---

# CHAPITRE 58 — ANALYSE PRÉDICTIVE

Lorsque les données disponibles sont suffisantes.

Le Reporting Engine peut produire des prévisions.

Exemples :

* volume prévisionnel de demandes ;
* charge prévisionnelle des conseillers ;
* besoins futurs en partenaires ;
* évolution des services ;
* saturation de certaines Zones LAWIM.

Les prévisions sont accompagnées d'un niveau de confiance.

---

# CHAPITRE 59 — RECOMMANDATIONS

À partir des analyses réalisées.

Le système peut formuler des recommandations.

Exemples :

Pour un demandeur :

* élargir la zone de recherche ;
* modifier certains critères.

Pour un détenteur de bien :

* compléter son annonce ;
* améliorer les photographies ;
* mettre à jour les informations.

Pour une agence :

* renforcer sa présence dans une zone ;
* recruter de nouveaux agents.

Pour LAWIM :

* développer une nouvelle ville ;
* renforcer une équipe ;
* ouvrir une nouvelle zone de services.

Les recommandations restent consultatives.

---

# CHAPITRE 60 — ASSISTANCE À LAWIM AI

Le Reporting Engine met à disposition de LAWIM AI des indicateurs consolidés.

LAWIM AI peut notamment :

* générer des synthèses ;
* expliquer des tendances ;
* comparer des périodes ;
* suggérer des axes d'amélioration ;
* répondre aux questions analytiques des utilisateurs autorisés.

LAWIM AI ne modifie jamais les indicateurs produits par le Reporting Engine.

---

# CHAPITRE 61 — AIDE À LA DÉCISION

Le Reporting Engine fournit aux responsables LAWIM des informations facilitant les décisions.

Exemples :

* ouverture d'une nouvelle agence ;
* affectation de nouveaux conseillers ;
* lancement d'un nouveau service ;
* renforcement d'une zone géographique ;
* adaptation des campagnes de communication.

Les décisions restent de la responsabilité des personnes habilitées.

---

# CHAPITRE 62 — ÉTHIQUE ET TRANSPARENCE

Toutes les analyses doivent être :

* explicables ;
* reproductibles ;
* fondées sur des données vérifiables.

Aucune recommandation ne doit reposer sur des critères discriminatoires.

Les utilisateurs doivent pouvoir comprendre l'origine des indicateurs et des recommandations qui les concernent.

---

# CHAPITRE 63 — APPRENTISSAGE ET ÉVOLUTION

Les modèles analytiques peuvent évoluer.

Toute évolution doit :

* être validée ;
* être documentée ;
* conserver la compatibilité avec les historiques ;
* permettre la comparaison des indicateurs dans le temps.

Les changements majeurs sont historisés.

---

# CHAPITRE 64 — RÈGLES ABSOLUES

Le Reporting Engine doit toujours :

✓ produire des analyses fondées sur des données validées ;

✓ distinguer les faits, les tendances et les prévisions ;

✓ présenter un niveau de confiance pour les projections ;

✓ respecter la confidentialité des données ;

✓ fournir des recommandations explicables ;

✓ rester compatible avec les autres moteurs de LAWIM.

Il est interdit :

❌ de modifier automatiquement une donnée métier à partir d'une prédiction ;

❌ de prendre une décision exclusivement sur une analyse prédictive ;

❌ de présenter une estimation comme une certitude ;

❌ d'utiliser des données non validées pour produire des rapports stratégiques.

---

# CHAPITRE 65 — OBJECTIF FINAL

Le Reporting Engine doit permettre à LAWIM de passer d'une logique de simple observation à une logique d'anticipation.

Grâce à l'Analytics Engine et à l'assistance de LAWIM AI, la plateforme est capable d'identifier les tendances, de détecter les anomalies, d'estimer les évolutions futures et de formuler des recommandations utiles aux utilisateurs, aux organisations et à l'équipe LAWIM, tout en garantissant la transparence, la confidentialité et la maîtrise humaine des décisions.

---

# FIN DE LA PARTIE 7

# LAWIM

# 11-REPORTING-REFERENCE.md

# PARTIE 8

# Diffusion, visualisation et exploitation des rapports

Version 1.0

---

# CHAPITRE 66 — PRINCIPE FONDAMENTAL

Le Reporting Engine ne se limite pas à produire des indicateurs.

Il est également responsable de leur diffusion, de leur présentation et de leur exploitation.

Chaque utilisateur autorisé doit pouvoir accéder aux informations pertinentes, sous la forme la plus adaptée à son rôle, à son contexte et à son besoin.

Le Reporting Engine fournit les données.

Le Dashboard Engine décide de leur présentation visuelle.

---

# CHAPITRE 67 — MODES DE CONSULTATION

Les rapports peuvent être consultés sous plusieurs formes :

* tableau interactif ;
* graphique ;
* indicateur synthétique (KPI) ;
* carte géographique ;
* chronologie ;
* tableau comparatif ;
* rapport détaillé.

L'utilisateur peut passer librement d'un mode d'affichage à un autre lorsque cela est pertinent.

---

# CHAPITRE 68 — TABLEAUX DE BORD

Le Reporting Engine alimente les différents tableaux de bord de LAWIM.

Exemples :

* Dashboard personnel ;
* Dashboard propriétaire ;
* Dashboard demandeur ;
* Dashboard agence ;
* Dashboard partenaire ;
* Dashboard équipe LAWIM ;
* Dashboard administrateur.

Chaque tableau de bord affiche uniquement les indicateurs autorisés.

---

# CHAPITRE 69 — FILTRES ET EXPLORATION

Les rapports doivent permettre une exploration dynamique.

Les utilisateurs autorisés peuvent filtrer notamment selon :

* période ;
* type de bien ;
* type de demande ;
* catégorie de service ;
* ville ;
* quartier ;
* Zone LAWIM ;
* agence ;
* partenaire ;
* conseiller LAWIM ;
* statut ;
* rôle.

Les filtres peuvent être combinés.

---

# CHAPITRE 70 — NAVIGATION DANS LES DONNÉES

Le Reporting Engine permet une navigation hiérarchique.

Exemple :

```text
Cameroun

↓

Région de l'Ouest

↓

Bafoussam

↓

Quartier

↓

Type de bien

↓

Annonce concernée (si autorisée)
```

Le niveau de détail accessible dépend des permissions de l'utilisateur.

---

# CHAPITRE 71 — EXPORTS

Les utilisateurs autorisés peuvent exporter les rapports dans différents formats.

Formats supportés :

* PDF ;
* Excel (XLSX) ;
* CSV ;
* JSON (pour les intégrations autorisées).

Les exports respectent toujours les permissions du demandeur.

---

# CHAPITRE 72 — RAPPORTS PLANIFIÉS

Le Reporting Engine permet la génération automatique de rapports.

Exemples :

* rapport quotidien ;
* rapport hebdomadaire ;
* rapport mensuel ;
* rapport trimestriel ;
* rapport annuel.

Les rapports peuvent être générés automatiquement selon une planification configurable.

---

# CHAPITRE 73 — ABONNEMENTS AUX RAPPORTS

Les utilisateurs autorisés peuvent s'abonner à certains rapports.

Exemples :

* activité d'une agence ;
* évolution d'une ville ;
* nouveaux biens par catégorie ;
* performances des équipes ;
* évolution des services.

Le Reporting Engine diffuse automatiquement ces rapports selon la fréquence définie.

---

# CHAPITRE 74 — DIFFUSION

Les rapports peuvent être transmis :

* dans le Dashboard ;
* par notification interne ;
* par courrier électronique ;
* via une API sécurisée ;
* par téléchargement manuel.

Le Notification Engine informe l'utilisateur lorsqu'un rapport planifié est disponible.

---

# CHAPITRE 75 — VISUALISATIONS

Le Dashboard Engine peut présenter les données sous différentes formes.

Exemples :

* courbes ;
* histogrammes ;
* diagrammes circulaires ;
* cartes thermiques ;
* cartes géographiques ;
* jauges ;
* tableaux croisés ;
* indicateurs synthétiques.

Les visualisations doivent rester cohérentes avec les données produites par le Reporting Engine.

---

# CHAPITRE 76 — COMPARAISONS

Le Reporting Engine permet de comparer :

* deux périodes ;
* plusieurs villes ;
* plusieurs quartiers ;
* plusieurs agences ;
* plusieurs partenaires ;
* plusieurs catégories de biens ;
* plusieurs types de services.

Les comparaisons utilisent toujours les mêmes règles de calcul.

---

# CHAPITRE 77 — PARTAGE

Les rapports peuvent être partagés avec d'autres utilisateurs autorisés.

Le partage respecte :

* les rôles ;
* les permissions ;
* la confidentialité ;
* les restrictions de diffusion.

Un rapport partagé ne donne jamais accès à des données auxquelles le destinataire n'est pas autorisé.

---

# CHAPITRE 78 — RAPPORTS STRATÉGIQUES

Le Reporting Engine produit des rapports consolidés pour la direction de LAWIM.

Ils peuvent notamment porter sur :

* la croissance de la plateforme ;
* l'évolution des utilisateurs ;
* la couverture géographique ;
* la qualité des services ;
* les performances des agences ;
* les performances des partenaires ;
* les revenus issus de la mise en relation ;
* les revenus issus des services d'accompagnement (visites, contrôles documentaires, vidéos, photographies, accompagnement administratif, etc.).
* les revenus issus des paiements Campay ;
* le volume des paiements Campay ;

Conformément au modèle économique de LAWIM, ces rapports **n'intègrent aucune commission sur les transactions immobilières**, puisque la plateforme n'en prélève pas.

---

# CHAPITRE 79 — INDICATEURS TEMPS RÉEL

Lorsque cela est pertinent.

Le Reporting Engine peut mettre à disposition des indicateurs actualisés en temps réel.

Exemples :

* utilisateurs connectés ;
* nouvelles annonces ;
* nouveaux matchings ;
* visites du jour ;
* missions en cours ;
* notifications en attente.

Les indicateurs temps réel sont clairement identifiés comme tels.

---

# CHAPITRE 80 — RÈGLES ABSOLUES

Le Reporting Engine doit toujours :

✓ diffuser des rapports conformes aux permissions ;

✓ garantir la cohérence entre les rapports et les tableaux de bord ;

✓ permettre l'export des données autorisées ;

✓ assurer une présentation claire et exploitable ;

✓ respecter le modèle économique officiel de LAWIM.

Il est interdit :

❌ d'exporter des données non autorisées ;

❌ de partager un rapport contenant des informations confidentielles avec un utilisateur non habilité ;

❌ de produire un rapport financier reposant sur des commissions de transaction inexistantes.

---

# CHAPITRE 81 — OBJECTIF FINAL

Le Reporting Engine permet à chaque acteur de LAWIM d'accéder, au moment opportun et sous la forme la plus adaptée, aux informations nécessaires à son activité.

Grâce à ses capacités de diffusion, d'exploration, d'exportation et de visualisation, il transforme les données de la plateforme en outils d'aide à la décision, tout en respectant les rôles, les permissions et le modèle économique de LAWIM.

---

# FIN DE LA PARTIE 8

# LAWIM

# 11-REPORTING-REFERENCE.md

# PARTIE 9

# Administration, supervision, qualité des données et sécurité

Version 1.0

---

# CHAPITRE 82 — PRINCIPE FONDAMENTAL

Le Reporting Engine est administré de manière centralisée.

Son administration garantit :

* la qualité des données ;
* la cohérence des indicateurs ;
* la disponibilité des rapports ;
* la sécurité des informations ;
* la traçabilité des traitements.

Toutes les opérations d'administration sont réservées aux utilisateurs autorisés.

---

# CHAPITRE 83 — ADMINISTRATION

Les administrateurs habilités peuvent notamment :

* créer un nouvel indicateur officiel ;
* modifier une formule de calcul ;
* activer ou désactiver un rapport ;
* créer un tableau de bord standard ;
* gérer les rapports planifiés ;
* gérer les abonnements ;
* gérer les exports ;
* consulter les journaux d'audit.

Toute modification est historisée.

---

# CHAPITRE 84 — QUALITÉ DES DONNÉES

Le Reporting Engine ne produit des indicateurs qu'à partir de données validées.

Avant tout calcul, il vérifie notamment :

* la cohérence des données ;
* l'intégrité des enregistrements ;
* l'absence de doublons ;
* la présence des informations obligatoires ;
* la validité des références entre les différents moteurs.

Les données incomplètes ou incohérentes sont signalées sans être intégrées aux indicateurs officiels.

---

# CHAPITRE 85 — CONTRÔLE DES INDICATEURS

Chaque indicateur officiel possède une définition documentée.

Cette définition comprend notamment :

* son identifiant ;
* son objectif ;
* sa formule de calcul ;
* ses sources ;
* sa fréquence de mise à jour ;
* son propriétaire fonctionnel.

Deux indicateurs portant le même nom ne peuvent jamais avoir des formules de calcul différentes.

---

# CHAPITRE 86 — SUPERVISION

Le Reporting Engine surveille en permanence :

* les traitements programmés ;
* les calculs en cours ;
* les rapports planifiés ;
* les exports ;
* les files d'attente ;
* les temps de génération ;
* les erreurs de traitement.

Les anomalies sont signalées aux administrateurs concernés.

---

# CHAPITRE 87 — AUDIT

Toutes les opérations importantes sont historisées.

Le journal d'audit comprend notamment :

* utilisateur concerné ;
* rôle ;
* opération réalisée ;
* rapport concerné ;
* indicateur concerné ;
* ancienne valeur ;
* nouvelle valeur ;
* date et heure ;
* justification lorsqu'elle est requise.

Les journaux sont conservés conformément au référentiel de stockage.

---

# CHAPITRE 88 — SÉCURITÉ

Le Reporting Engine applique les règles de sécurité définies par LAWIM.

Les accès aux rapports sont contrôlés selon :

* le rôle ;
* les permissions ;
* l'organisation ;
* le niveau de confidentialité ;
* le contexte du dossier.

Un utilisateur ne peut consulter que les données auxquelles il est autorisé.

---

# CHAPITRE 89 — CONFIDENTIALITÉ

Les rapports peuvent contenir des données sensibles.

Le Reporting Engine doit notamment :

* masquer les informations personnelles lorsqu'elles ne sont pas nécessaires ;
* limiter les exports aux données autorisées ;
* anonymiser les analyses globales lorsque cela est approprié ;
* empêcher la reconstitution d'informations confidentielles à partir de croisements de données.

Les statistiques publiques sont toujours agrégées.

---

# CHAPITRE 90 — DISPONIBILITÉ

Le Reporting Engine doit garantir une disponibilité élevée.

En cas d'incident.

Le système doit permettre :

* la reprise automatique des traitements ;
* la relance des calculs interrompus ;
* la conservation des rapports validés ;
* la reprogrammation des traitements non exécutés.

Aucun incident ne doit entraîner une perte silencieuse de données.

---

# CHAPITRE 91 — PERFORMANCE

Le Reporting Engine doit rester performant même lorsque le volume de données augmente.

Il met en œuvre notamment :

* des calculs différés lorsque cela est approprié ;
* des agrégations intermédiaires ;
* des mécanismes de cache ;
* des traitements asynchrones ;
* une optimisation des requêtes.

Ces optimisations ne doivent jamais modifier les résultats fonctionnels.

---

# CHAPITRE 92 — CONTINUITÉ DE SERVICE

Le Reporting Engine s'appuie sur l'architecture de stockage et de sauvegarde de LAWIM.

Les rapports, indicateurs et historiques sont protégés conformément au référentiel de stockage.

En particulier :

* les données de production sont hébergées sur OVH ;
* les sauvegardes locales sont synchronisées avec l'infrastructure définie dans **14-STORAGE-REFERENCE.md** ;
* les historiques restent disponibles même après l'archivage des données opérationnelles.

Le Reporting Engine doit pouvoir reconstruire les indicateurs historiques à partir des archives lorsque cela est nécessaire.

---

# CHAPITRE 93 — SURVEILLANCE DU MODÈLE ÉCONOMIQUE

Le Reporting Engine produit des indicateurs permettant de suivre le modèle économique de LAWIM.

Il mesure notamment :

* les revenus issus des mises en relation ;
* les revenus issus des services d'accompagnement ;
* l'utilisation des services complémentaires ;
* la répartition des revenus par catégorie de service ;
* les tendances d'évolution.

Conformément à la Constitution de LAWIM, aucun indicateur ne doit calculer ou présenter des commissions sur les transactions immobilières, car LAWIM ne prélève aucune commission sur les ventes ou locations.

---

# CHAPITRE 94 — RÈGLES ABSOLUES

Le Reporting Engine doit toujours :

✓ produire des indicateurs reproductibles ;

✓ utiliser uniquement des données validées ;

✓ garantir une traçabilité complète des calculs ;

✓ protéger les informations confidentielles ;

✓ respecter les rôles et les permissions ;

✓ assurer la continuité de service ;

✓ rester cohérent avec le référentiel de stockage et le modèle économique de LAWIM.

Il est interdit :

❌ de modifier directement un indicateur officiel sans procédure de validation ;

❌ de publier un rapport fondé sur des données non validées ;

❌ de contourner les règles de sécurité pour accéder à un rapport ;

❌ de supprimer un historique avant la fin de sa durée de conservation ;

❌ de créer des indicateurs incompatibles avec les référentiels officiels de LAWIM.

---

# CHAPITRE 95 — OBJECTIF FINAL

L'administration et la supervision du Reporting Engine garantissent la fiabilité, la sécurité et la pérennité des informations stratégiques de LAWIM.

Grâce à une gouvernance rigoureuse, un contrôle permanent de la qualité des données et une parfaite intégration avec les autres moteurs de la plateforme, le Reporting Engine fournit des indicateurs de confiance permettant de piloter durablement l'activité, d'accompagner les décisions et de soutenir le développement de LAWIM.

---

# FIN DE LA PARTIE 9


# LAWIM

# 11-REPORTING-REFERENCE.md

# PARTIE 10

# Gouvernance, évolution et vision stratégique du Reporting Engine

Version 1.0

---

# CHAPITRE 96 — PRINCIPE FONDAMENTAL

Le Reporting Engine constitue le moteur officiel de production, d'analyse et de diffusion des informations décisionnelles de LAWIM.

Il fournit une vision fiable, cohérente et durable de l'activité de la plateforme.

Toutes les statistiques, tous les indicateurs et tous les rapports officiels proviennent exclusivement du Reporting Engine.

---

# CHAPITRE 97 — GOUVERNANCE

La gouvernance du Reporting Engine est assurée par l'équipe LAWIM.

Elle comprend notamment :

* la validation des nouveaux indicateurs ;
* la validation des méthodes de calcul ;
* la validation des rapports officiels ;
* la validation des tableaux de bord de référence ;
* la validation des évolutions fonctionnelles.

Toute évolution importante doit être documentée avant sa mise en production.

---

# CHAPITRE 98 — RÉFÉRENTIEL UNIQUE

Le Reporting Engine constitue l'unique référence officielle concernant :

* les indicateurs de performance ;
* les statistiques ;
* les analyses ;
* les tableaux de bord ;
* les rapports décisionnels ;
* les rapports stratégiques.

Aucun autre moteur ne peut produire un indicateur officiel différent.

Les autres moteurs publient uniquement les données nécessaires au Reporting Engine.

---

# CHAPITRE 99 — ÉVOLUTIVITÉ

Le Reporting Engine est conçu pour évoluer.

Les évolutions peuvent notamment concerner :

* de nouveaux indicateurs ;
* de nouvelles familles de rapports ;
* de nouveaux tableaux de bord ;
* de nouvelles analyses ;
* de nouvelles visualisations ;
* de nouveaux moteurs d'analyse ;
* de nouveaux services d'aide à la décision.

Toutes les évolutions doivent rester compatibles avec les historiques existants.

---

# CHAPITRE 100 — INTEROPÉRABILITÉ

Le Reporting Engine peut communiquer avec :

* les applications Web ;
* les applications mobiles ;
* les API de LAWIM ;
* les outils d'administration ;
* les outils de Business Intelligence autorisés.

Les échanges utilisent exclusivement les interfaces officielles de LAWIM.

---

# CHAPITRE 101 — INDÉPENDANCE TECHNOLOGIQUE

Le Reporting Engine doit rester indépendant des technologies de visualisation ou d'analyse utilisées.

LAWIM doit pouvoir remplacer un composant technique sans modifier :

* les indicateurs ;
* les formules de calcul ;
* les référentiels métier ;
* les historiques.

Cette indépendance garantit la pérennité du système.

---

# CHAPITRE 102 — AMÉLIORATION CONTINUE

Le Reporting Engine fait l'objet d'une amélioration continue.

Les évolutions peuvent être proposées notamment à partir :

* des retours des utilisateurs ;
* des analyses de LAWIM AI ;
* des besoins des agences ;
* des besoins des partenaires ;
* des besoins de l'équipe LAWIM ;
* des évolutions du marché immobilier.

Chaque amélioration est évaluée avant son intégration.

---

# CHAPITRE 103 — COMPATIBILITÉ AVEC LES AUTRES MOTEURS

Le Reporting Engine fonctionne en interaction permanente avec :

* Workflow Engine ;
* Matching Engine ;
* Conversation Engine ;
* Dashboard Engine ;
* Geo Engine ;
* Notification Engine ;
* Role Engine ;
* Storage Lifecycle Manager ;
* LAWIM AI.

Il exploite leurs données validées sans modifier leur fonctionnement.

---

# CHAPITRE 104 — CONFORMITÉ AU MODÈLE ÉCONOMIQUE

Le Reporting Engine doit toujours refléter fidèlement le modèle économique officiel de LAWIM.

Les rapports financiers et stratégiques portent notamment sur :

* les revenus issus des mises en relation ;
* les revenus issus des services d'accompagnement ;
* les revenus des services payés via Campay ;
* le volume des paiements Campay ;
* les coûts d'exploitation ;
* les investissements techniques ;
* les indicateurs de croissance.

Le Reporting Engine ne doit jamais intégrer de commissions sur les transactions immobilières, car LAWIM ne prélève aucune commission sur les ventes ou locations.

Toute évolution future du modèle économique devra d'abord être validée dans la Constitution de LAWIM avant d'être prise en compte dans les rapports.

---

# CHAPITRE 105 — PÉRENNITÉ DES DONNÉES

Le Reporting Engine doit garantir la continuité historique des indicateurs.

Même après l'archivage des données opérationnelles :

* les indicateurs historiques restent consultables selon les permissions ;
* les comparaisons entre périodes demeurent possibles ;
* les rapports déjà publiés restent reproductibles ;
* les historiques conservent leur cohérence.

Le Reporting Engine s'appuie sur la stratégie de stockage et d'archivage de LAWIM afin de préserver cette continuité.

---

# CHAPITRE 106 — TRANSPARENCE

Les rapports produits par LAWIM doivent être compréhensibles.

Chaque indicateur officiel doit pouvoir être documenté.

La documentation comprend notamment :

* sa définition ;
* sa méthode de calcul ;
* sa fréquence de mise à jour ;
* sa source ;
* ses limites éventuelles.

Les utilisateurs autorisés doivent pouvoir interpréter correctement les informations qui leur sont présentées.

---

# CHAPITRE 107 — RÈGLES ABSOLUES

Le Reporting Engine doit toujours :

✓ constituer la source officielle des rapports et indicateurs ;

✓ produire des résultats reproductibles ;

✓ garantir la cohérence des historiques ;

✓ respecter les rôles et les permissions ;

✓ protéger les données sensibles ;

✓ rester indépendant des technologies utilisées ;

✓ demeurer compatible avec tous les moteurs de LAWIM ;

✓ respecter en permanence le modèle économique officiel de LAWIM.

Il est interdit :

❌ de produire des statistiques officielles en dehors du Reporting Engine ;

❌ de modifier une formule de calcul sans validation ;

❌ de publier des rapports utilisant des données non validées ;

❌ de supprimer un historique sans respecter la politique de conservation ;

❌ de créer des rapports financiers fondés sur des commissions inexistantes.

---

# CHAPITRE 108 — VISION STRATÉGIQUE

À long terme, le Reporting Engine doit devenir l'outil central de pilotage de LAWIM.

Il doit permettre :

* d'accompagner la croissance de la plateforme ;
* d'améliorer les décisions opérationnelles ;
* d'orienter les investissements ;
* d'optimiser les services proposés aux utilisateurs ;
* d'identifier les opportunités de développement ;
* de soutenir l'expansion de LAWIM dans de nouveaux territoires.

Grâce à son intégration avec LAWIM AI, le Reporting Engine évoluera progressivement d'un système de reporting vers un véritable système d'aide à la décision, tout en conservant la maîtrise humaine des choix stratégiques.

---

# CHAPITRE 110 — REPORTING MARKETING ET ATTRIBUTION

Le Reporting Engine doit produire automatiquement les rapports suivants :

* rapport quotidien ;
* rapport hebdomadaire ;
* rapport mensuel ;
* rapport trimestriel ;
* rapport annuel ;
* rapport campagne ;
* rapport acteur ;
* rapport agence ;
* rapport partenaire ;
* rapport canal ;
* rapport publication ;
* rapport ville ;
* rapport quartier ;
* rapport langue ;
* rapport type de bien ;
* rapport revenus ;
* rapport Campay ;
* rapport IA.

Le Reporting Engine doit également fournir les vues d'attribution et de performance suivantes :

* canal ;
* campagne ;
* publication ;
* acteur ;
* lead ;
* redirection ;
* conversion ;
* funnel ;
* revenue attribution ;
* performance géographique ;
* performance temporelle.

Les KPI marketing à documenter incluent notamment :

* nombre de clics ;
* clics uniques ;
* CTR ;
* comptes créés ;
* leads ;
* conversations ;
* matchings ;
* visites ;
* paiements Campay ;
* conversions ;
* revenus ;
* taux clic -> lead ;
* taux lead -> conversation ;
* taux conversation -> matching ;
* taux matching -> visite ;
* taux visite -> paiement ;
* taux paiement -> fidélisation ;
* revenus par campagne ;
* revenus par publication ;
* revenus par acteur ;
* revenus par canal ;
* performances géographiques ;
* performances linguistiques ;
* performances temporelles.

Les données restent recalculables à partir des événements historisés.

---

# CHAPITRE 111 — OBJECTIF FINAL

Le Reporting Engine constitue la mémoire analytique et décisionnelle de LAWIM.

Il transforme les données issues des différents moteurs en informations fiables, exploitables et pérennes.

En garantissant la qualité des indicateurs, la cohérence des rapports et le respect du modèle économique de LAWIM, il fournit à tous les acteurs de la plateforme les éléments nécessaires pour comprendre le présent, analyser le passé et préparer l'avenir.

---

# FIN DU DOCUMENT

Le présent **11-REPORTING-REFERENCE.md** constitue le référentiel officiel du Reporting Engine de LAWIM.

Toute implémentation Web, Mobile, API ou évolution future devra respecter les principes, les modèles, les règles et les contraintes définis dans ce document.

Aucun rapport, indicateur ou tableau de bord officiel ne pourra être développé en dehors du Reporting Engine.
