# LAWIM

# 05-WORKFLOW-REFERENCE.md

# Référentiel Officiel des Workflows

Version 1.0

---

# PARTIE 1

# Architecture générale des workflows

---

# CHAPITRE 1 — OBJECTIF

Le présent document définit l'ensemble des workflows métier de LAWIM.

Un workflow décrit la succession des états, des événements, des décisions et des actions permettant de conduire un objet métier jusqu'à son terme.

Les workflows constituent la colonne vertébrale de LAWIM.

Toute implémentation devra respecter ce document.

---

# CHAPITRE 2 — PRINCIPE FONDAMENTAL

Dans LAWIM, tout possède un cycle de vie.

Notamment :

* un bien ;
* un dossier ;
* un lead ;
* une conversation ;
* une visite ;
* une négociation ;
* une transaction ;
* un utilisateur ;
* un service payant ;
* une notification.

Chaque objet évolue selon son propre workflow.

---

# CHAPITRE 3 — UN WORKFLOW N'EST PAS UNE SUITE D'ÉCRANS

Le workflow est indépendant :

* du Web ;
* du Mobile ;
* de WhatsApp ;
* de Telegram ;
* des API.

Les interfaces ne font qu'afficher l'état courant du workflow.

Le comportement métier est exclusivement défini ici.

---

# CHAPITRE 4 — LES COMPOSANTS D'UN WORKFLOW

Tout workflow est composé des éléments suivants.

## État

Situation actuelle de l'objet.

Exemple :

Publié

Visite planifiée

Négociation

---

## Événement

Fait déclenchant une évolution.

Exemple :

Publication.

Réponse du propriétaire.

Visite.

Paiement.

---

## Transition

Passage d'un état à un autre.

Une transition est toujours contrôlée.

---

## Action

Traitement automatique ou manuel.

Exemple :

Notifier.

Créer un rendez-vous.

Relancer.

Rematching.

---

## Condition

Règle autorisant ou interdisant une transition.

---

# CHAPITRE 5 — TYPES DE WORKFLOWS

LAWIM distingue plusieurs familles.

## Workflow Bien

Suit la vie d'un bien.

---

## Workflow Dossier

Suit le besoin du demandeur.

---

## Workflow Matching

Suit les propositions.

---

## Workflow Mise en relation

Suit les échanges entre les parties.

---

## Workflow Visite

Suit l'organisation et la réalisation des visites.

---

## Workflow Transaction

Suit les ventes et locations.

---

## Workflow Services payants

Suit les services optionnels et leurs paiements.

---

## Workflow Support

Suit les incidents.

---

# CHAPITRE 6 — ÉVÉNEMENTS

Tous les workflows sont pilotés par des événements.

Exemples.

Création.

Publication.

Modification.

Matching.

Rematching.

Acceptation.

Refus.

Relance.

Visite.

Négociation.

Signature.

Paiement.

Clôture.

Archivage.

Chaque événement est horodaté.

---

# CHAPITRE 7 — RÈGLES DE TRANSITION

Une transition doit toujours respecter :

* les règles métier ;
* les droits des utilisateurs ;
* les référentiels officiels.

Une transition invalide est interdite.

Exemple.

Transaction

↓

Création

Interdit.

---

Visite

↓

Matching

Interdit.

---

Matching

↓

Visite

Autorisé.

---

# CHAPITRE 8 — TRAÇABILITÉ

Chaque transition est enregistrée.

Les informations conservées sont notamment :

* ancien état ;
* nouvel état ;
* auteur ;
* date ;
* motif ;
* commentaires éventuels.

L'historique n'est jamais supprimé.

---

# CHAPITRE 9 — AUTOMATISATION

LAWIM privilégie l'automatisation.

Toute action pouvant être exécutée automatiquement doit l'être.

Exemples.

* matching ;
* rematching ;
* notifications ;
* relances ;
* rappels ;
* changements d'état.

Les interventions humaines sont réservées aux situations nécessitant une décision ou une validation.

---

# CHAPITRE 10 — WORKFLOWS ACTIFS

Les workflows LAWIM sont des workflows actifs.

Ils ne se contentent pas d'attendre des événements.

Ils surveillent en permanence :

* les délais ;
* les opportunités ;
* les risques ;
* les changements du marché.

Ils déclenchent automatiquement les actions prévues.

---

# CHAPITRE 11 — NEXT BEST ACTION

Chaque objet métier possède en permanence une prochaine action optimale.

Exemples.

Relancer le propriétaire.

↓

Programmer une visite.

↓

Lancer un rematching.

↓

Demander un document.

↓

Archiver.

Cette action est calculée automatiquement.

Elle est réévaluée après chaque événement.

---

# CHAPITRE 12 — SLA MÉTIER

Chaque workflow possède des délais maximums.

Ces délais dépendent notamment :

* du type de bien ;
* du type d'opération ;
* de l'état courant.

Lorsqu'un délai est dépassé.

Le workflow déclenche automatiquement une action.

---

# CHAPITRE 13 — OBJECTIF FINAL

Le workflow n'a pas pour objectif de faire évoluer des états.

Il a pour objectif de conduire chaque dossier jusqu'à une transaction réussie.

Toutes les décisions prises dans LAWIM doivent contribuer à cet objectif.

---

# FIN DE LA PARTIE 1

# PARTIE 2

# Workflows actifs, SLA métier et gestion proactive des dossiers

Version 1.0

---

# CHAPITRE 20 — PRINCIPE FONDAMENTAL

Dans LAWIM.

Un workflow ne se contente jamais d'attendre.

Il agit.

Chaque dossier.

Chaque bien.

Chaque transaction.

Chaque visite.

Chaque mise en relation.

Possède une prochaine action.

Un workflow sans prochaine action est considéré comme défaillant.

---

# CHAPITRE 21 — SLA MÉTIER

LAWIM applique des délais maximums appelés SLA (Service Level Agreement).

Un SLA définit le délai maximal acceptable avant qu'une nouvelle action ne soit entreprise.

Les SLA dépendent :

* du type de bien ;
* de l'opération (vente, location, etc.) ;
* de l'étape du workflow.

---

# CHAPITRE 22 — SLA PAR TYPE DE BIEN

Les valeurs ci-dessous constituent les paramètres par défaut.

| Type de bien        | Premier matching | Premier rematching | Première relance |
| ------------------- | ---------------: | -----------------: | ---------------: |
| Chambre             |         immédiat |               24 h |             48 h |
| Chambre moderne     |         immédiat |               24 h |             48 h |
| Studio              |         immédiat |               48 h |             72 h |
| Appartement         |         immédiat |               72 h |          5 jours |
| Maison              |         immédiat |            5 jours |          7 jours |
| Villa               |         immédiat |            7 jours |         10 jours |
| Duplex              |         immédiat |            7 jours |         10 jours |
| Terrain résidentiel |         immédiat |           10 jours |         15 jours |
| Terrain agricole    |         immédiat |           15 jours |         20 jours |
| Terrain industriel  |         immédiat |           20 jours |         30 jours |
| Commerce            |         immédiat |            7 jours |         10 jours |
| Bureau              |         immédiat |           10 jours |         15 jours |
| Entrepôt            |         immédiat |           15 jours |         20 jours |
| Hôtel               |         immédiat |           30 jours |         45 jours |
| Immeuble            |         immédiat |           30 jours |         45 jours |

Ces valeurs sont configurables.

---

# CHAPITRE 23 — DOSSIER SANS MATCH

Lorsqu'aucun bien compatible n'est trouvé.

LAWIM ne clôture jamais le dossier.

Le moteur applique automatiquement les étapes suivantes.

1.

Recherche normale.

↓

2.

Recherche élargie.

↓

3.

Recherche intelligente.

↓

4.

Recherche continue.

↓

5.

Notification du demandeur.

↓

6.

Relance automatique.

---

# CHAPITRE 24 — RECHERCHE ÉLARGIE

Le moteur peut progressivement :

* élargir le quartier ;
* élargir la distance ;
* rechercher dans les quartiers limitrophes ;
* proposer des variantes compatibles.

Les champs critiques ne sont jamais modifiés sans accord du demandeur.

---

# CHAPITRE 25 — DIAGNOSTIC AUTOMATIQUE

Lorsque plusieurs rematchings restent infructueux.

LAWIM recherche automatiquement la cause.

Exemples.

Budget insuffisant.

↓

Zone trop restrictive.

↓

Critères trop exigeants.

↓

Absence de biens disponibles.

↓

Propriétaires inactifs.

Chaque cause entraîne une stratégie spécifique.

---

# CHAPITRE 26 — SUGGESTIONS INTELLIGENTES

LAWIM ne modifie jamais un dossier sans autorisation.

Il formule des propositions.

Exemple.

🤖 LAWIM AI

Je n'ai trouvé aucun appartement correspondant exactement à votre recherche.

Je peux :

• élargir la recherche aux quartiers voisins ;

• rechercher des appartements de trois chambres au lieu de quatre ;

• poursuivre la surveillance du marché.

La décision appartient toujours au demandeur.

---

# CHAPITRE 27 — SURVEILLANCE PERMANENTE

Même sans interaction de l'utilisateur.

LAWIM continue à surveiller :

* les nouvelles publications ;
* les baisses de prix ;
* les retours en disponibilité ;
* les nouveaux quartiers ;
* les nouvelles annonces compatibles.

Tout changement significatif déclenche un nouveau matching.

---

# CHAPITRE 28 — RELANCE DU DEMANDEUR

Si aucun résultat pertinent n'est trouvé dans le délai prévu.

LAWIM reprend contact.

Exemple.

🤖 LAWIM AI

Je poursuis activement votre recherche.

Depuis notre dernier échange, aucun bien ne correspond exactement à vos critères.

Souhaitez-vous maintenir votre recherche telle quelle ou explorer quelques alternatives ?

---

# CHAPITRE 29 — RELANCE DU DÉTENTEUR

Lorsqu'un propriétaire ne répond pas.

LAWIM applique automatiquement.

Premier rappel.

↓

Deuxième rappel.

↓

Dernier rappel.

↓

Bien marqué comme inactif.

↓

Rematching.

---

# CHAPITRE 30 — SANTÉ DU DOSSIER

Chaque dossier possède un indice de santé.

Critères pris en compte.

* activité récente ;
* réponses ;
* nombre de propositions ;
* progression ;
* interactions.

Valeurs.

🟢 Excellent

🟡 Normal

🟠 À surveiller

🔴 Critique

Les dossiers critiques deviennent prioritaires.

---

# CHAPITRE 31 — SANTÉ D'UN BIEN

Chaque bien possède également un indice de santé.

Le moteur prend notamment en compte.

* disponibilité confirmée ;
* âge de l'annonce ;
* nombre de vues ;
* nombre de matchs ;
* nombre de visites ;
* refus ;
* qualité documentaire.

Un bien dont la santé devient faible doit automatiquement faire l'objet d'une action.

Exemples.

* confirmation de disponibilité ;
* amélioration de l'annonce ;
* ajout de photos ;
* vérification du prix ;
* archivage si nécessaire.

---

# CHAPITRE 32 — RÈGLE ABSOLUE

Aucun dossier actif.

Aucun bien publié.

Aucune transaction.

Ne doit rester sans action au-delà du délai SLA correspondant.

Si ce délai est dépassé.

LAWIM déclenche obligatoirement une action adaptée.

L'inaction est considérée comme une anomalie de fonctionnement.

---

# CHAPITRE 33 — OBJECTIF FINAL

Le workflow de LAWIM est un workflow actif.

Le système ne se contente jamais d'enregistrer des événements.

Il pilote en permanence les dossiers afin de maximiser les chances de réussite des transactions, tout en respectant les préférences des utilisateurs et les réalités du marché immobilier.

# FIN DE LA PARTIE 2

# LAWIM

# 05-WORKFLOW-REFERENCE.md

# PARTIE 3

# Workflow du cycle de vie des biens

Version 1.0

---

# CHAPITRE 34 — PRINCIPE FONDAMENTAL

Tout bien enregistré dans LAWIM possède un cycle de vie.

Ce cycle commence lors de sa création.

Il se termine uniquement lorsque le bien est définitivement archivé.

Le cycle de vie est indépendant :

* des conversations ;
* des dossiers ;
* des utilisateurs.

Un même bien peut participer à plusieurs dossiers successifs au cours de sa vie.

---

# CHAPITRE 35 — ÉTATS OFFICIELS D'UN BIEN

Tous les biens utilisent les états suivants.

```text
Création

↓

Qualification

↓

Validation

↓

Publié

↓

Disponible

↓

Matching

↓

Visites

↓

Négociation

↓

Réservé

↓

Transaction

↓

Indisponible

↓

Réactivation éventuelle

↓

Archivé
```

Aucun autre état n'est autorisé sans évolution officielle du référentiel.

---

# CHAPITRE 36 — CRÉATION

Le bien est créé.

À ce stade :

* il n'est pas visible ;
* il ne participe pas au matching ;
* il peut être incomplet.

Le moteur vérifie immédiatement les champs obligatoires définis dans :

02-PROPERTY-REFERENCE.md.

---

# CHAPITRE 37 — QUALIFICATION

Le bien est enrichi.

Le système complète notamment :

* type ;
* opération ;
* localisation ;
* attributs ;
* documents ;
* coordonnées GPS (OpenStreetMap lorsque disponibles) ;
* médias.

Le bien reçoit un premier **Property Health Score**.

---

# CHAPITRE 38 — VALIDATION

Avant publication.

LAWIM vérifie :

✓ cohérence des informations ;

✓ conformité du type de bien ;

✓ présence des champs obligatoires ;

✓ unicité ;

✓ disponibilité déclarée.

Un bien non conforme reste en validation.

---

# CHAPITRE 39 — PUBLICATION

Une fois validé.

Le bien devient visible.

Il peut désormais :

* apparaître dans les recherches ;
* participer au matching ;
* recevoir des visites.

La date de publication est enregistrée.

---

# CHAPITRE 40 — DISPONIBILITÉ

Un bien publié possède obligatoirement un statut de disponibilité.

Valeurs autorisées :

* Disponible ;
* Réservé ;
* Sous négociation ;
* Sous compromis ;
* Loué ;
* Vendu ;
* Suspendu ;
* Archivé.

Les statuts **Loué** et **Vendu** empêchent tout nouveau matching.

---

# CHAPITRE 41 — PARTICIPATION AU MATCHING

Dès qu'un bien est disponible.

LAWIM calcule automatiquement tous les dossiers compatibles.

Le bien reçoit :

* un Match Count ;
* un Score moyen de compatibilité ;
* un Score d'attractivité.

Ces indicateurs sont recalculés en permanence.

---

# CHAPITRE 42 — VISITES

Lorsqu'un demandeur accepte une proposition.

Le bien passe dans un cycle de visites.

Chaque visite est enregistrée avec :

* date ;
* demandeur ;
* résultat ;
* observations.

Le nombre de visites influence le Health Score.

---

# CHAPITRE 43 — NÉGOCIATION

Après une visite positive.

Le bien peut entrer en négociation.

Le système conserve :

* les offres ;
* les contre-offres ;
* les décisions ;
* les délais.

Un bien peut connaître plusieurs négociations successives.

---

# CHAPITRE 44 — RÉSERVATION

Lorsqu'un accord de principe est obtenu.

Le bien peut être marqué **Réservé**.

Pendant cette période :

* il n'est plus proposé aux nouveaux demandeurs ;
* les dossiers existants restent informés de son évolution.

Une réservation possède une date d'expiration.

À son expiration, le bien redevient automatiquement disponible si aucune transaction n'a été conclue.

---

# CHAPITRE 45 — TRANSACTION

Lorsque la vente ou la location est finalisée.

Le bien passe à l'état :

* Vendu ; ou
* Loué.

La date de transaction est enregistrée.

Le bien cesse immédiatement de participer au matching.

---

# CHAPITRE 46 — RÉACTIVATION

Un bien peut redevenir disponible.

Exemples :

* fin de bail ;
* annulation de réservation ;
* annulation de vente ;
* retrait d'un compromis.

Le moteur relance automatiquement le matching.

---

# CHAPITRE 47 — ARCHIVAGE

Le bien est archivé lorsque :

* le propriétaire le demande ;
* il est définitivement retiré ;
* il est obsolète ;
* les règles d'archivage sont atteintes.

Un bien archivé :

* n'est plus visible ;
* ne participe plus au matching ;
* reste consultable pour l'historique.

---

# CHAPITRE 48 — CINÉTIQUE PAR TYPE DE BIEN

Chaque type de bien possède un profil de marché.

Exemples de valeurs de référence :

| Type                | Rotation normale |
| ------------------- | ---------------: |
| Chambre             |   1 à 4 semaines |
| Studio              |   2 à 8 semaines |
| Appartement         |       1 à 4 mois |
| Villa               |      3 à 12 mois |
| Terrain résidentiel |      3 à 18 mois |
| Terrain agricole    |      6 à 36 mois |
| Commerce            |       1 à 6 mois |
| Bureau              |       2 à 8 mois |
| Hôtel               |      6 à 36 mois |

Ces valeurs servent de référence pour les alertes et les automatisations.

---

# CHAPITRE 49 — BIEN EN RETARD

Lorsque la durée de commercialisation dépasse la durée normale.

LAWIM déclenche automatiquement un diagnostic.

Le système analyse notamment :

* prix ;
* qualité des photos ;
* description ;
* disponibilité réelle ;
* activité du propriétaire ;
* nombre de matchs ;
* nombre de visites ;
* nombre de refus.

Le moteur choisit ensuite la meilleure action.

---

# CHAPITRE 50 — ACTIONS CORRECTIVES

Selon le diagnostic.

LAWIM peut notamment :

* demander une confirmation de disponibilité ;
* suggérer une baisse de prix ;
* recommander de nouvelles photos ;
* demander des informations complémentaires ;
* élargir le matching ;
* proposer une mise en avant du bien ;
* suspendre temporairement la diffusion ;
* archiver le bien.

Aucune modification n'est effectuée sans l'accord du détenteur, sauf lorsqu'il s'agit de règles automatiques prévues par la Constitution (par exemple l'archivage après une transaction).

---

# CHAPITRE 51 — OBJECTIF FINAL

Le cycle de vie d'un bien ne consiste pas uniquement à publier une annonce.

Il consiste à maintenir en permanence un bien :

* disponible lorsque c'est pertinent ;
* correctement qualifié ;
* attractif ;
* activement proposé ;
* et retiré du marché au moment opportun.

Le moteur doit accompagner chaque bien jusqu'à sa sortie naturelle du marché.

---

# FIN DE LA PARTIE 3

# LAWIM

# 05-WORKFLOW-REFERENCE.md

# PARTIE 4

# Workflow du cycle de vie des dossiers (Case Management)

Version 1.0

---

# CHAPITRE 52 — PRINCIPE FONDAMENTAL

Dans LAWIM, le **dossier** est l'objet métier principal.

Le bien est un objet partagé.

La conversation est un moyen de communication.

Le matching est un mécanisme de décision.

Le dossier est le fil conducteur qui relie l'ensemble.

Tout utilisateur possède un dossier pour chacun de ses projets immobiliers.

Un même utilisateur peut posséder plusieurs dossiers simultanément.

---

# CHAPITRE 53 — DÉFINITION D'UN DOSSIER

Un dossier représente un besoin immobilier unique.

Exemples :

* louer une chambre ;
* acheter une villa ;
* vendre un terrain ;
* louer un bureau ;
* acheter un hôtel.

Chaque dossier possède :

* un identifiant unique ;
* un demandeur ;
* un type de bien ;
* une opération ;
* un workflow ;
* un historique complet.

---

# CHAPITRE 54 — ÉTATS OFFICIELS DU DOSSIER

Tous les dossiers utilisent les états suivants.

```text
Création

↓

Qualification

↓

Matching

↓

Présentation

↓

Attente décision demandeur

↓

Contact détenteur

↓

Attente décision détenteur

↓

Mise en relation

↓

Visite

↓

Négociation

↓

Accord

↓

Transaction

↓

Clôture

↓

Archivage
```

Aucun état ne peut être supprimé.

Toute évolution devra passer par une nouvelle version officielle de ce document.

---

# CHAPITRE 55 — CRÉATION

Le dossier est créé dès qu'un utilisateur exprime un besoin immobilier.

La création peut provenir :

* du Web ;
* de WhatsApp ;
* de Telegram ;
* de l'application mobile ;
* d'un collaborateur LAWIM.

Le dossier reçoit immédiatement :

* une date de création ;
* un responsable (LAWIM AI) ;
* un niveau de priorité ;
* une Next Best Action.

---

# CHAPITRE 56 — QUALIFICATION

LAWIM collecte progressivement les informations nécessaires.

Le moteur ne cherche jamais à remplir un formulaire.

Il recherche uniquement les champs critiques définis dans :

02-PROPERTY-REFERENCE.md.

Dès que les champs critiques sont connus.

Le matching peut commencer.

---

# CHAPITRE 57 — MATCHING

Le moteur applique :

04-MATCHING-REFERENCE.md.

Les meilleurs biens sont calculés.

Ils sont classés.

Ils sont enregistrés dans le dossier.

Le dossier conserve l'historique de toutes les propositions.

---

# CHAPITRE 58 — PRÉSENTATION DES BIENS

Les propositions sont présentées progressivement.

Le moteur évite :

* les doublons ;
* les propositions massives ;
* les biens incompatibles.

Chaque proposition possède :

* un score ;
* une justification ;
* une date.

---

# CHAPITRE 59 — DÉCISION DU DEMANDEUR

Pour chaque proposition.

Le demandeur peut :

* accepter ;
* refuser ;
* demander plus d'informations ;
* demander une visite ;
* mettre en attente.

Chaque décision enrichit automatiquement le dossier.

---

# CHAPITRE 60 — CONTACT DU DÉTENTEUR

Lorsqu'un bien est retenu.

LAWIM contacte automatiquement le détenteur.

Le moteur enregistre :

* date ;
* mode de contact ;
* réponse ;
* délai de réponse.

Le dossier passe en attente de décision du détenteur.

---

# CHAPITRE 61 — DÉCISION DU DÉTENTEUR

Le détenteur peut :

* accepter ;
* refuser ;
* demander des précisions ;
* proposer une autre date ;
* déclarer le bien indisponible.

Chaque réponse déclenche automatiquement une nouvelle Next Best Action.

---

# CHAPITRE 62 — MISE EN RELATION

La mise en relation n'intervient qu'après un double accord.

Conditions obligatoires :

✓ demandeur intéressé ;

✓ détenteur favorable.

À partir de ce moment.

Le changement d'interlocuteur est clairement visible.

Exemple :

🤖 LAWIM AI

↓

👤 Propriétaire

ou

👤 Agence

ou

👤 Introduceur

ou

👨‍💼 Collaborateur LAWIM

Le nom affiché est limité à huit caractères conformément à la Constitution.

---

# CHAPITRE 63 — VISITE

Une visite constitue un événement du dossier.

Elle possède :

* une date ;
* un lieu ;
* un statut ;
* un résultat.

Statuts autorisés :

* Planifiée ;
* Confirmée ;
* Reportée ;
* Réalisée ;
* Annulée ;
* Absence demandeur ;
* Absence détenteur.

Chaque visite influence les indicateurs du dossier.

---

# CHAPITRE 64 — NÉGOCIATION

Après une visite positive.

Le dossier peut entrer en négociation.

Le moteur conserve :

* toutes les offres ;
* toutes les contre-offres ;
* les délais ;
* les décisions.

Aucune information n'est supprimée.

---

# CHAPITRE 65 — TRANSACTION

Le dossier passe en transaction lorsque les parties sont parvenues à un accord.

Le moteur suit notamment :

* les documents ;
* les paiements ;
* les signatures ;
* la remise des clés ou la prise de possession.

Le détail de ces étapes est défini dans les workflows spécialisés.

---

# CHAPITRE 66 — CLÔTURE

Le dossier est clôturé lorsque :

* la transaction est terminée ;

ou

* le projet est abandonné définitivement.

La clôture ne supprime jamais les données.

---

# CHAPITRE 67 — ARCHIVAGE

Après clôture.

Le dossier est archivé.

Il reste :

* consultable ;
* exploitable pour les statistiques ;
* disponible pour l'audit.

Il ne participe plus aux workflows actifs.

---

# CHAPITRE 68 — RÉOUVERTURE

Un dossier clôturé peut être rouvert.

Exemples :

* nouvelle recherche ;
* transaction annulée ;
* retour d'un besoin.

La réouverture conserve tout l'historique.

---

# CHAPITRE 69 — NEXT BEST ACTION

À tout instant.

Chaque dossier possède une action prioritaire.

Exemples.

* Poser une question.

* Lancer un matching.

* Organiser une visite.

* Relancer le détenteur.

* Attendre une réponse.

* Ouvrir une négociation.

* Clôturer.

Cette action est recalculée après chaque événement.

---

# CHAPITRE 70 — SLA DU DOSSIER

Chaque état possède un délai maximal.

Exemple.

Matching :

≤ immédiat.

---

Attente du détenteur :

selon le type de bien.

---

Attente du demandeur :

selon le niveau d'urgence.

---

Visite programmée :

suivi automatique jusqu'à sa réalisation.

En cas de dépassement.

LAWIM déclenche automatiquement une action adaptée.

---

# CHAPITRE 71 — DOSSIER SANS ÉVOLUTION

Un dossier actif ne doit jamais rester sans événement significatif au-delà du SLA applicable.

Lorsque ce délai est atteint.

Le moteur doit obligatoirement :

* lancer un rematching ;
* relancer une partie ;
* proposer un ajustement ;
* ou escalader le dossier vers un collaborateur LAWIM.

L'inaction est interdite.

---

# CHAPITRE 72 — TRAÇABILITÉ

Le dossier conserve obligatoirement :

* tous les changements d'état ;
* tous les matchs ;
* tous les rematchings ;
* toutes les notifications ;
* toutes les visites ;
* toutes les négociations ;
* toutes les mises en relation ;
* tous les changements d'interlocuteur.

Aucune suppression n'est autorisée.

---

# CHAPITRE 73 — OBJECTIF FINAL

Le dossier constitue la mémoire officielle du projet immobilier.

Toutes les décisions de LAWIM doivent contribuer à faire progresser le dossier jusqu'à l'une des issues suivantes :

* location réalisée ;
* vente réalisée ;
* achat réalisé ;
* projet abandonné.

Le dossier ne doit jamais être laissé sans suivi tant qu'il reste actif.

---

# FIN DE LA PARTIE 4

# LAWIM

# 05-WORKFLOW-REFERENCE.md

# PARTIE 5

# Workflow de la mise en relation

Version 1.0

---

# CHAPITRE 74 — PRINCIPE FONDAMENTAL

La mise en relation constitue l'étape où LAWIM fait passer un dossier d'une simple proposition de bien à une interaction réelle entre les parties.

Elle est entièrement pilotée.

LAWIM ne transmet jamais les coordonnées d'un détenteur sans respecter les règles définies dans ce document.

---

# CHAPITRE 75 — OBJECTIFS

La mise en relation poursuit quatre objectifs.

* protéger le demandeur ;
* protéger le détenteur ;
* maximiser les chances de transaction ;
* conserver la traçabilité complète.

---

# CHAPITRE 76 — CONDITIONS OBLIGATOIRES

Une mise en relation est autorisée uniquement si :

✓ le dossier est actif ;

✓ le bien est disponible ;

✓ le demandeur confirme son intérêt ;

✓ le détenteur accepte d'être mis en relation.

En l'absence d'une seule de ces conditions.

La mise en relation est interdite.

---

# CHAPITRE 77 — DOUBLE CONSENTEMENT

LAWIM applique obligatoirement le principe du double consentement.

```text
Matching

↓

Demandeur intéressé

↓

Détenteur intéressé

↓

Mise en relation
```

Aucune exception n'est autorisée.

---

# CHAPITRE 78 — DEMANDEUR INTÉRESSÉ

Le demandeur peut :

* accepter la proposition ;
* demander des informations complémentaires ;
* demander une visite ;
* refuser.

Un refus déclenche automatiquement le rematching.

---

# CHAPITRE 79 — DÉTENTEUR SOLLICITÉ

Le détenteur reçoit une demande de mise en relation.

Il peut :

* accepter ;
* refuser ;
* demander un délai ;
* proposer une autre disponibilité ;
* déclarer le bien indisponible.

Chaque réponse est enregistrée.

---

# CHAPITRE 80 — SILENCE DU DÉTENTEUR

En l'absence de réponse.

LAWIM applique automatiquement le workflow suivant.

```text
Premier rappel

↓

Deuxième rappel

↓

Dernier rappel

↓

Bien marqué "à confirmer"

↓

Rematching
```

Le délai entre les rappels dépend du type de bien conformément aux SLA.

---

# CHAPITRE 81 — REFUS DU DÉTENTEUR

Lorsque le détenteur refuse.

Le dossier ne s'arrête jamais.

LAWIM :

* enregistre le refus ;
* conserve le motif si disponible ;
* déclenche immédiatement un rematching.

Le bien n'est plus proposé à ce demandeur tant que sa situation n'évolue pas.

---

# CHAPITRE 82 — CHANGEMENT D'INTERLOCUTEUR

À partir du moment où la mise en relation commence.

L'utilisateur doit immédiatement voir le changement d'interlocuteur.

Exemple.

```text
🤖 LAWIM AI

↓

👤 Propriétaire

↓

👨🏽‍💼 Conseiller LAWIM

↓

🤖 LAWIM AI
```

Le changement est matérialisé par :

* l'icône ;
* le nom (8 caractères maximum) ;
* le rôle.

Aucun utilisateur ne doit avoir le moindre doute sur l'identité de son interlocuteur.

---

# CHAPITRE 83 — IDENTITÉ DES INTERVENANTS

Les rôles affichés sont notamment :

🤖 LAWIM AI

👤 Propriétaire

🏢 Agence

🤝 Introduceur

👨🏽‍💼 Conseiller LAWIM

🛠 Support LAWIM

Chaque rôle possède son icône officielle.

---

# CHAPITRE 84 — ÉCHANGE DES COORDONNÉES

Les coordonnées personnelles sont échangées uniquement selon les règles définies par LAWIM.

Le système doit pouvoir appliquer différents niveaux de confidentialité selon les politiques commerciales.

Toutes les divulgations sont tracées.

---

# CHAPITRE 85 — HISTORIQUE

Chaque mise en relation enregistre obligatoirement :

* date ;
* heure ;
* demandeur ;
* détenteur ;
* bien concerné ;
* canal utilisé ;
* résultat.

Aucune suppression n'est autorisée.

---

# CHAPITRE 86 — ISSUE DE LA MISE EN RELATION

Une mise en relation peut aboutir à :

* visite programmée ;
* demande d'informations complémentaires ;
* négociation ;
* refus ;
* abandon ;
* rematching.

Le dossier poursuit ensuite son workflow.

---

# CHAPITRE 87 — RELANCES

Si aucune évolution n'est constatée après la mise en relation.

LAWIM déclenche automatiquement les actions prévues par les SLA.

Exemples :

* rappel au demandeur ;
* rappel au détenteur ;
* proposition de nouvelle date ;
* rematching.

Le dossier ne reste jamais sans suivi.

---

# CHAPITRE 88 — INDICATEURS

Chaque mise en relation produit des indicateurs.

Exemples :

* délai moyen avant réponse ;
* taux d'acceptation ;
* taux de refus ;
* taux de transformation en visite ;
* taux de transformation en transaction.

Ces indicateurs alimentent le Reporting et les scores de fiabilité.

---

# CHAPITRE 89 — OBJECTIF FINAL

La mise en relation ne consiste pas simplement à transmettre des coordonnées.

Elle constitue une étape contrôlée destinée à :

* sécuriser les échanges ;
* préparer la visite ;
* améliorer la qualité des interactions ;
* maximiser les chances de réussite de la transaction.

LAWIM demeure le coordinateur du dossier jusqu'à sa clôture, même lorsque les parties sont mises en relation.

---

# FIN DE LA PARTIE 5


# LAWIM

# 05-WORKFLOW-REFERENCE.md

# PARTIE 6

# Workflow des visites

Version 1.0

---

# CHAPITRE 90 — PRINCIPE FONDAMENTAL

La visite constitue le premier contact physique entre un demandeur et un bien.

Son objectif est de permettre au demandeur d'évaluer le bien avant toute négociation ou transaction.

LAWIM organise, suit et trace intégralement le processus de visite.

---

# CHAPITRE 91 — CONDITIONS PRÉALABLES

Une visite ne peut être programmée que si les conditions suivantes sont réunies :

✓ le bien est disponible ;

✓ le demandeur a manifesté un intérêt ;

✓ le détenteur accepte une visite ;

✓ le dossier est actif.

Dans tous les autres cas, la visite est interdite.

---

# CHAPITRE 92 — DEMANDE DE VISITE

La demande de visite peut être initiée :

* par le demandeur ;
* par LAWIM AI (suggestion) ;
* par un collaborateur LAWIM.

Chaque demande reçoit :

* un identifiant unique ;
* une date ;
* un statut.

---

# CHAPITRE 93 — VALIDATION DE LA VISITE

Avant toute confirmation.

LAWIM vérifie :

* la disponibilité du bien ;
* la disponibilité du détenteur ;
* la disponibilité du demandeur ;
* l'état du dossier.

Une visite ne peut jamais être confirmée si le bien est déjà :

* réservé ;
* vendu ;
* loué ;
* archivé.

---

# CHAPITRE 94 — PLANIFICATION

Une visite confirmée comporte obligatoirement :

* la date ;
* l'heure ;
* le lieu ;
* les coordonnées GPS si disponibles ;
* le nom du détenteur ou de son représentant ;
* les coordonnées du demandeur.

Le moteur génère automatiquement les rappels nécessaires.

---

# CHAPITRE 95 — STATUTS DE LA VISITE

Les statuts autorisés sont :

* Demandée ;
* En attente de confirmation ;
* Confirmée ;
* Reportée ;
* Annulée ;
* Réalisée ;
* Refusée ;
* Absence du demandeur ;
* Absence du détenteur.

Aucun autre statut n'est autorisé.

---

# CHAPITRE 96 — RAPPELS AUTOMATIQUES

LAWIM envoie automatiquement des rappels.

Par défaut :

* 24 heures avant la visite ;
* 2 heures avant la visite.

Des rappels supplémentaires peuvent être configurés.

Les rappels sont envoyés au :

* demandeur ;
* détenteur ;
* collaborateur LAWIM concerné.

---

# CHAPITRE 97 — CHANGEMENT D'INTERLOCUTEUR

Lorsque la visite est confirmée.

L'utilisateur est informé du changement d'interlocuteur.

Exemple :

🤖 LAWIM AI

↓

👤 Propriétaire

ou

👤 Agence

ou

👨🏽‍💼 Collaborateur LAWIM

Le changement doit être immédiatement visible grâce :

* au nom ;
* à l'icône ;
* au rôle affiché.

---

# CHAPITRE 98 — DÉROULEMENT DE LA VISITE

À l'heure prévue.

LAWIM considère la visite comme :

En cours.

À la fin.

Le système demande séparément :

Au demandeur :

* la visite a-t-elle eu lieu ?

Au détenteur :

* la visite a-t-elle eu lieu ?

En cas de divergence.

Le dossier est signalé pour vérification.

---

# CHAPITRE 99 — RÉSULTAT DE LA VISITE

Après la visite.

Le demandeur peut indiquer :

* Très satisfait ;
* Satisfait ;
* Mitigé ;
* Insatisfait.

Le détenteur peut également fournir un retour.

Ces informations enrichissent le dossier.

---

# CHAPITRE 100 — DÉCISION APRÈS VISITE

Après une visite.

Le moteur choisit automatiquement la Next Best Action.

Possibilités :

* ouvrir une négociation ;

* programmer une seconde visite ;

* proposer un autre bien ;

* lancer un rematching ;

* clôturer cette proposition.

---

# CHAPITRE 101 — VISITE ANNULÉE

Une visite peut être annulée :

* par le demandeur ;
* par le détenteur ;
* par LAWIM (bien indisponible).

Le motif est enregistré.

Le moteur décide ensuite :

* nouvelle programmation ;

ou

* rematching.

---

# CHAPITRE 102 — ABSENCE

Deux cas sont distingués.

## Absence du demandeur

Le moteur :

* enregistre l'absence ;
* informe le détenteur ;
* propose une nouvelle date.

---

## Absence du détenteur

Le moteur :

* informe le demandeur ;
* diminue l'indice de fiabilité du détenteur ;
* propose une nouvelle date ou un autre bien.

---

# CHAPITRE 103 — VISITES MULTIPLES

Un dossier peut comporter plusieurs visites.

Chaque visite possède son propre historique.

Les visites précédentes restent consultables.

---

# CHAPITRE 104 — VISITES SUR PLUSIEURS BIENS

Le demandeur peut visiter plusieurs biens.

Le moteur évite cependant de programmer inutilement plusieurs visites similaires le même jour.

Il privilégie un parcours cohérent et optimisé.

---

# CHAPITRE 105 — INDICATEURS

Chaque visite produit des indicateurs.

Exemples :

* délai avant première visite ;
* taux de confirmation ;
* taux d'annulation ;
* taux d'absence ;
* taux de satisfaction ;
* taux de transformation en négociation.

Ces indicateurs alimentent le Reporting.

---

# CHAPITRE 106 — APPRENTISSAGE

Le moteur apprend de chaque visite.

Exemples.

Le demandeur refuse plusieurs villas sans dépendance.

↓

La dépendance devient un critère fortement recommandé.

---

Le détenteur annule fréquemment.

↓

Son indice de fiabilité diminue.

---

# CHAPITRE 107 — OBJECTIF FINAL

Une visite n'est jamais une simple prise de rendez-vous.

Elle constitue une étape stratégique destinée à :

* confirmer la compatibilité entre le demandeur et le bien ;
* préparer la négociation ;
* augmenter la probabilité de réussite de la transaction.

Toutes les automatisations de LAWIM doivent contribuer à rendre les visites plus simples, plus fiables et plus efficaces.

---

# CHAPITRE 108 — RÈGLES ABSOLUES

Le workflow des visites doit toujours :

✓ vérifier la disponibilité réelle du bien ;

✓ informer clairement toutes les parties ;

✓ assurer le suivi jusqu'au résultat ;

✓ enregistrer chaque événement ;

✓ recalculer automatiquement la Next Best Action après chaque visite.

Il ne doit jamais :

❌ programmer une visite pour un bien indisponible ;

❌ perdre l'historique d'une visite ;

❌ laisser une visite sans suivi ;

❌ maintenir un dossier sans action après une visite.

---

# FIN DE LA PARTIE 6


# LAWIM

# 05-WORKFLOW-REFERENCE.md

# PARTIE 7

# Workflow des négociations

Version 1.0

---

# CHAPITRE 109 — PRINCIPE FONDAMENTAL

La négociation constitue l'étape durant laquelle les parties recherchent un accord mutuellement acceptable.

LAWIM ne négocie jamais à la place des parties.

LAWIM facilite.

LAWIM accompagne.

LAWIM sécurise.

LAWIM conserve la traçabilité complète.

---

# CHAPITRE 110 — CONDITIONS D'OUVERTURE

Une négociation peut être ouverte uniquement si :

✓ une visite satisfaisante a eu lieu ;

ou

✓ les deux parties souhaitent négocier sans visite.

Le dossier doit être actif.

Le bien doit rester disponible.

---

# CHAPITRE 111 — ÉTATS DE LA NÉGOCIATION

Toutes les négociations utilisent les états suivants.

```text
Ouverte

↓

En discussion

↓

Offre

↓

Contre-offre

↓

Accord de principe

↓

Accord final

↓

Transaction

ou

Échec

↓

Rematching
```

---

# CHAPITRE 112 — ÉLÉMENTS NÉGOCIABLES

Selon le type de bien.

Les éléments suivants peuvent être négociés.

## Vente

* prix ;
* modalités de paiement ;
* délais ;
* mobilier inclus ;
* équipements ;
* date de libération.

---

## Location

* loyer ;
* caution ;
* avance ;
* durée du bail ;
* date d'entrée ;
* travaux éventuels.

---

## Terrain

* prix ;
* bornage ;
* documents ;
* délais.

---

## Commerce

* loyer ;
* pas-de-porte ;
* équipements ;
* durée.

---

# CHAPITRE 113 — OFFRES

Chaque offre possède :

* un identifiant ;
* un auteur ;
* une date ;
* un montant ;
* un commentaire éventuel ;
* un statut.

Toutes les offres sont historisées.

Aucune suppression n'est autorisée.

---

# CHAPITRE 114 — CONTRE-OFFRES

Chaque partie peut répondre par :

✓ acceptation ;

✓ refus ;

✓ contre-offre.

Le moteur enregistre chaque étape.

Le fil des négociations reste consultable.

---

# CHAPITRE 115 — IA D'ASSISTANCE À LA NÉGOCIATION

LAWIM peut assister les parties.

Exemple.

Prix demandé :

85 M

Budget :

82 M

↓

Écart :

3 M

LAWIM peut indiquer :

> 🤖 **LAWIM AI**
>
> Les positions des deux parties sont proches.
>
> Les chances d'aboutir à un accord sont élevées.

LAWIM ne propose jamais un prix sans autorisation.

LAWIM ne décide jamais à la place des parties.

---

# CHAPITRE 116 — DÉLAIS

Une négociation possède un délai maximal.

Le délai dépend :

* du type de bien ;
* du type d'opération ;
* des règles commerciales.

À expiration.

LAWIM déclenche une relance.

---

# CHAPITRE 117 — RELANCES

En cas d'absence de réponse.

LAWIM applique automatiquement.

Premier rappel.

↓

Deuxième rappel.

↓

Dernier rappel.

↓

Clôture automatique de la négociation.

↓

Rematching éventuel.

Les délais sont définis par les SLA.

---

# CHAPITRE 118 — MODIFICATION DU BIEN PENDANT LA NÉGOCIATION

Si le bien devient :

* vendu ;
* loué ;
* suspendu ;
* indisponible.

La négociation est automatiquement interrompue.

Les parties sont immédiatement informées.

Le dossier poursuit son workflow.

---

# CHAPITRE 119 — REFUS

Le refus d'une offre ne clôture pas automatiquement la négociation.

LAWIM peut :

* attendre une nouvelle offre ;
* proposer une contre-offre ;
* suspendre temporairement ;
* lancer un rematching.

---

# CHAPITRE 120 — ACCORD DE PRINCIPE

Lorsqu'un accord verbal est obtenu.

Le dossier passe :

Accord de principe.

À ce stade.

Le moteur prépare automatiquement :

* les documents nécessaires ;
* la transaction ;
* les prochaines étapes.

Le bien peut être marqué **Réservé**.

---

# CHAPITRE 121 — ÉCHEC

Une négociation est déclarée en échec lorsque :

* les parties mettent fin aux échanges ;
* le délai maximal est dépassé ;
* le bien devient indisponible ;
* une partie se retire.

L'échec est enregistré.

Le dossier n'est jamais supprimé.

---

# CHAPITRE 122 — REMATCHING APRÈS ÉCHEC

En cas d'échec.

LAWIM déclenche automatiquement.

* un diagnostic ;

* un rematching ;

* une nouvelle proposition.

Le dossier continue tant que le projet immobilier reste actif.

---

# CHAPITRE 123 — HISTORIQUE

Chaque négociation conserve obligatoirement :

* toutes les offres ;
* toutes les contre-offres ;
* les messages importants ;
* les décisions ;
* les changements d'état ;
* les dates.

Aucune information n'est supprimée.

---

# CHAPITRE 124 — INDICATEURS

Chaque négociation produit des indicateurs.

Exemples :

* durée moyenne ;

* nombre d'offres ;

* nombre de contre-offres ;

* taux d'accord ;

* taux d'échec ;

* écart moyen entre prix initial et prix final.

Ces indicateurs alimentent :

* le Reporting ;

* les scores de fiabilité ;

* le Decision Engine.

---

# CHAPITRE 125 — APPRENTISSAGE

LAWIM apprend des négociations.

Exemples.

Un propriétaire accepte systématiquement une réduction de 5 %.

↓

Le moteur améliore ses prévisions.

---

Un demandeur refuse toujours au-delà d'un certain budget.

↓

Le moteur affine les futurs matchings.

Ces apprentissages servent uniquement à améliorer les recommandations.

Ils ne remplacent jamais la décision humaine.

---

# CHAPITRE 126 — OBJECTIF FINAL

La négociation a pour objectif de parvenir à un accord équilibré.

LAWIM doit :

✓ faciliter les échanges ;

✓ réduire les délais ;

✓ conserver la traçabilité ;

✓ préparer automatiquement la transaction ;

✓ protéger les intérêts des deux parties.

La décision finale appartient toujours aux utilisateurs.

---

# CHAPITRE 127 — RÈGLES ABSOLUES

Le workflow des négociations doit toujours :

✓ conserver toutes les offres ;

✓ respecter les délais ;

✓ assurer les relances automatiques ;

✓ préparer la transaction dès qu'un accord est trouvé ;

✓ déclencher un rematching après un échec.

Il ne doit jamais :

❌ modifier une offre ;

❌ supprimer une contre-offre ;

❌ négocier à la place d'une partie ;

❌ poursuivre une négociation sur un bien indisponible ;

❌ perdre l'historique.

---

# FIN DE LA PARTIE 7


# LAWIM

# 05-WORKFLOW-REFERENCE.md

# PARTIE 8

# Workflow des transactions

Version 1.0

---

# CHAPITRE 128 — PRINCIPE FONDAMENTAL

La transaction constitue l'aboutissement normal d'un dossier immobilier.

Elle commence dès qu'un accord définitif est obtenu entre les parties.

Elle se termine uniquement lorsque toutes les obligations prévues sont exécutées.

LAWIM pilote la transaction jusqu'à sa clôture.

LAWIM suit les étapes, trace les événements et accompagne les parties jusqu'à la clôture.

LAWIM peut suivre les paiements de services LAWIM associés à l'opération.

> LAWIM ne prélève aucune commission sur les transactions immobilières. Les revenus LAWIM proviennent des frais de mise en relation, des services optionnels, de la visibilité premium, du boost, de la vérification et de l'assistance.

---

# CHAPITRE 129 — TYPES DE TRANSACTIONS

LAWIM distingue notamment :

* location ;
* vente ;
* achat ;
* bail professionnel ;
* bail commercial ;
* location saisonnière.

Chaque type applique ensuite des règles spécifiques.

---

# CHAPITRE 130 — CONDITIONS D'OUVERTURE

Une transaction ne peut être ouverte que si :

✓ le dossier est actif ;

✓ un accord existe ;

✓ le bien est toujours disponible ;

✓ les parties confirment leur intention.

---

# CHAPITRE 131 — ÉTATS DE LA TRANSACTION

Toutes les transactions utilisent les états suivants.

```text
Accord

↓

Préparation

↓

Documents

↓

Paiement

↓

Signature

↓

Remise des clés

↓

Confirmation

↓

Transaction terminée

↓

Archivage
```

---

# CHAPITRE 132 — PRÉPARATION

Avant la transaction.

LAWIM vérifie notamment :

* identité des parties ;
* disponibilité du bien ;
* documents requis ;
* calendrier.

Toute anomalie bloque la suite du workflow.

---

# CHAPITRE 133 — GESTION DOCUMENTAIRE

Selon le type de transaction.

Le moteur contrôle les documents nécessaires.

Exemples.

Vente :

* titre foncier ;
* pièce d'identité ;
* procuration éventuelle.

Location :

* contrat ;
* caution ;
* état des lieux.

Les documents manquants déclenchent automatiquement une relance.

---

# CHAPITRE 134 — PAIEMENT

LAWIM enregistre les étapes du paiement.

Exemples.

* acompte ;

* caution ;

* premier loyer ;

* paiement intégral ;

* échéances.

Le système peut enregistrer plusieurs paiements successifs.

---

# CHAPITRE 135 — SIGNATURE

La signature constitue une étape officielle.

LAWIM enregistre notamment :

* date ;
* heure ;
* lieu ;
* signataires.

Une transaction ne peut être finalisée sans cette étape lorsqu'elle est juridiquement requise.

---

# CHAPITRE 136 — REMISE DES CLÉS OU PRISE DE POSSESSION

Selon le type de bien.

LAWIM suit :

* remise des clés ;
* prise de possession ;
* remise des documents ;
* remise des accès.

La date est enregistrée.

---

# CHAPITRE 137 — CONFIRMATION

Après la remise.

Les deux parties peuvent confirmer :

✓ transaction réalisée ;

✓ bien reçu ;

✓ paiement effectué.

Le dossier passe ensuite en clôture.

---

# CHAPITRE 138 — ÉCHEC

Une transaction peut échouer.

Exemples.

* paiement abandonné ;

* documents impossibles à produire ;

* retrait d'une partie.

Le moteur conserve tout l'historique.

Le dossier peut retourner :

* en négociation ;

ou

* en rematching.

---

# CHAPITRE 139 — ANNULATION

Une transaction annulée reste historisée.

Le système indique notamment :

* auteur ;

* date ;

* motif.

Le bien peut redevenir disponible automatiquement.

---

# CHAPITRE 140 — SUIVI POST-TRANSACTION

Après la transaction.

LAWIM peut assurer :

* confirmation de satisfaction ;

* suivi des engagements restants ;

* mise à jour des statistiques ;

* amélioration des scores de fiabilité.

---

# CHAPITRE 141 — SUIVI DES SERVICES PAYANTS

Lorsque des services LAWIM sont associés à une transaction, leurs paiements sont suivis dans le workflow des services payants et des paiements.

Ces services restent distincts du prix final de la transaction.

Les règles détaillées sont définies dans la partie 9.

---

# CHAPITRE 142 — INDICATEURS

Chaque transaction produit des indicateurs.

Exemples.

* délai jusqu'à la transaction ;

* montant final ;

* taux de réussite ;

* durée de négociation ;

* nombre de visites ;

* nombre de rematchings ;

* délai moyen de paiement.

Ces indicateurs alimentent le Reporting.

---

# CHAPITRE 143 — APPRENTISSAGE

Chaque transaction améliore le moteur.

Exemples.

Les villas dans un quartier donné se vendent rapidement.

↓

Le moteur améliore ses prévisions.

---

Les appartements d'un certain standing nécessitent plusieurs visites.

↓

Le moteur adapte les recommandations.

---

# CHAPITRE 144 — RÈGLES ABSOLUES

Le workflow des transactions doit toujours :

✓ assurer la traçabilité complète ;

✓ vérifier les documents ;

✓ suivre les paiements de services LAWIM ;

✓ enregistrer les signatures ;

✓ mettre à jour automatiquement le statut du bien ;

✓ clôturer correctement le dossier.

Il ne doit jamais :

❌ finaliser une transaction sans accord ;

❌ perdre l'historique ;

❌ laisser un bien vendu ou loué participer au matching ;

❌ supprimer une transaction.

---

# CHAPITRE 145 — OBJECTIF FINAL

Le workflow des transactions constitue l'aboutissement de l'ensemble des processus de LAWIM.

Il garantit que chaque transaction est :

* traçable ;
* sécurisée ;
* documentée ;
* conforme aux règles métier ;

et qu'elle met automatiquement à jour :

* le bien ;
* le dossier ;
* les indicateurs ;
* les statistiques ;
* les tableaux de bord ;

afin de maintenir la cohérence globale du système.

---

# FIN DE LA PARTIE 8


# LAWIM

# 05-WORKFLOW-REFERENCE.md

# PARTIE 9

# Workflow des services payants et des paiements

Version 1.0

---

# CHAPITRE 147 — PRINCIPE FONDAMENTAL

LAWIM monétise des services.

Le modèle économique repose notamment sur :

* les frais de mise en relation ;
* les frais éventuels payés par les détenteurs de biens ;
* les frais éventuels payés par les demandeurs ;
* les services optionnels ;
* la visibilité premium ;
* le boost ;
* la vérification ;
* l'assistance.

Chaque paiement de service LAWIM est indépendant de la transaction immobilière.

---

# CHAPITRE 148 — TYPES DE SERVICES

LAWIM peut proposer notamment :

* mise en relation ;
* accès au contact ;
* publication premium ;
* visibilité premium ;
* boost ;
* vérification ;
* assistance.

Chaque service possède ses propres règles.

---

# CHAPITRE 149 — CYCLE DE VIE D'UN SERVICE

Tous les services utilisent le workflow suivant.

```text
Création

↓

Proposition

↓

Acceptation

↓

Paiement

↓

Activation

↓

Utilisation

↓

Expiration

↓

Archivage
```

---

# CHAPITRE 150 — DEMANDE DE SERVICE

Un service peut être demandé :

* par le détenteur ;
* par le demandeur ;
* par LAWIM AI (suggestion) ;
* par un collaborateur LAWIM.

La demande reçoit :

* un identifiant ;
* une date ;
* un statut.

---

# CHAPITRE 151 — TARIFICATION

Chaque service possède :

* un prix ;
* une devise ;
* une durée de validité ;
* des conditions d'utilisation.

Les prix ne sont jamais codés en dur.

Ils sont configurables.

---

# CHAPITRE 152 — PAYEUR

Le payeur peut être :

* le détenteur ;
* le demandeur ;
* une agence ;
* un partenaire.

Chaque paiement est rattaché :

* au dossier ;
* au bien si nécessaire ;
* au service concerné.

---

# CHAPITRE 153 — ÉTATS DU PAIEMENT

Les statuts autorisés sont :

* `PAYMENT_CREATED` ;
* `PAYMENT_INITIATED` ;
* `PAYMENT_PENDING` ;
* `PAYMENT_CONFIRMED` ;
* `PAYMENT_FAILED` ;
* `PAYMENT_CANCELLED` ;
* `PAYMENT_EXPIRED` ;
* `PAYMENT_REFUNDED` ;
* `PAYMENT_RECONCILED` ;
* `PAYMENT_DISPUTED`.

Toute modification de statut est historisée.

Lorsque le paiement est effectué via Campay, le statut confirmé ne peut être posé qu'après vérification serveur à serveur ou webhook validé.

Un service gratuit ne passe pas par le workflow de paiement ; il suit un état de service distinct.

---

# CHAPITRE 154 — VALIDATION

Un paiement est considéré comme valide uniquement lorsqu'il est confirmé.

Selon le moyen de paiement utilisé.

La validation peut être :

* automatique ;
* manuelle ;
* réalisée par un partenaire de paiement.

Pour Campay, la signature du webhook, l'idempotence et la cohérence du montant sont obligatoires.

---

# CHAPITRE 155 — ACTIVATION DU SERVICE

Après validation.

LAWIM active automatiquement le service.

Exemples.

Paiement de mise en relation.

↓

Autorisation de poursuivre la mise en relation.

---

Paiement d'accès au contact.

↓

Coordonnées autorisées.

---

Paiement de publication Premium.

↓

Annonce mise en avant.

---

Paiement de boost.

↓

Priorité dans les résultats.

---

Paiement de vérification.

↓

Contrôle déclenché.

---

Paiement d'assistance.

↓

Accompagnement activé.

---

# CHAPITRE 156 — EXPIRATION

Chaque service possède une durée de vie.

À son expiration.

LAWIM :

* désactive le service ;
* met à jour les indicateurs ;
* informe l'utilisateur si nécessaire.

---

# CHAPITRE 157 — REMBOURSEMENTS

Lorsque la politique commerciale l'autorise.

Un remboursement peut être initié.

Le système enregistre :

* le motif ;
* le montant ;
* la date ;
* l'auteur ;
* le statut.

Tous les remboursements sont tracés.

---

# CHAPITRE 158 — HISTORIQUE

Pour chaque service.

LAWIM conserve :

* toutes les demandes ;
* tous les paiements ;
* toutes les validations ;
* toutes les activations ;
* toutes les expirations ;
* tous les remboursements.

Aucune suppression n'est autorisée.

---

# CHAPITRE 159 — INDICATEURS

Les services alimentent notamment :

* chiffre d'affaires par service ;
* nombre de paiements ;
* nombre de paiements confirmés ;
* nombre de paiements échoués ;
* nombre de paiements en attente ;
* taux de conversion ;
* revenus par catégorie de service ;
* taux de remboursement ;
* services les plus utilisés.

Ces indicateurs sont utilisés par le Reporting.

---

# CHAPITRE 160 — NEXT BEST ACTION

Chaque service possède une Next Best Action.

Exemples.

* Attendre le paiement.

* Activer le service.

* Relancer le client.

* Vérifier la validation.

* Expirer le service.

Le moteur recalcule cette action après chaque événement.

---

# CHAPITRE 161 — AUTOMATISATION

LAWIM automatise notamment :

* la création des paiements ;
* l'émission des demandes de paiement vers Campay ;
* la réception et la vérification des webhooks Campay ;
* les relances ;
* l'activation ;
* l'expiration ;
* les notifications ;
* la mise à jour des tableaux de bord.

Les validations manuelles restent possibles selon les règles de gestion.

---

# CHAPITRE 162 — RÈGLES ABSOLUES

Le workflow des services doit toujours :

✓ distinguer clairement les paiements de services des transactions immobilières ;

✓ conserver la traçabilité complète ;

✓ activer automatiquement les services après validation ;

✓ activer les services uniquement après confirmation de paiement ;

✓ recalculer la Next Best Action ;

✓ respecter les SLA.

Il ne doit jamais :

❌ prélever un montant calculé sur le prix final d'une transaction ;

❌ mélanger un paiement de service avec un paiement entre les parties ;

❌ supprimer un paiement ;

❌ perdre l'historique.

---

# CHAPITRE 163 — OBJECTIF FINAL

Le workflow des services garantit que le modèle économique de LAWIM reste entièrement indépendant des montants des transactions immobilières.

Les revenus de LAWIM proviennent exclusivement des services proposés par la plateforme, conformément à la Constitution.

---

# FIN DE LA PARTIE 9


# LAWIM

# 05-WORKFLOW-REFERENCE.md

# PARTIE 10

# Workflow des litiges, réclamations et incidents

Version 1.0

---

# CHAPITRE 164 — PRINCIPE FONDAMENTAL

LAWIM favorise les transactions immobilières mais n'est pas partie au contrat conclu entre les utilisateurs.

En cas de litige, LAWIM assure :

* la traçabilité ;
* la conservation des preuves disponibles ;
* le suivi du dossier ;
* la médiation lorsque cela est possible.

LAWIM ne remplace jamais :

* le juge ;
* le notaire ;
* l'avocat ;
* les autorités administratives.

---

# CHAPITRE 165 — TYPES D'INCIDENTS

Les incidents peuvent notamment concerner :

* bien devenu indisponible ;
* informations inexactes ;
* annulation d'une visite ;
* absence d'un participant ;
* désaccord après visite ;
* non-respect d'un engagement ;
* paiement de service contesté ;
* comportement inapproprié ;
* usurpation d'identité ;
* fraude présumée ;
* faux documents ;
* utilisation abusive de la plateforme.

---

# CHAPITRE 166 — OUVERTURE D'UN INCIDENT

Un incident peut être déclaré par :

* le demandeur ;
* le détenteur ;
* un collaborateur LAWIM ;
* LAWIM AI lorsqu'une anomalie est détectée.

Chaque incident reçoit :

* un identifiant unique ;
* une date ;
* une priorité ;
* un niveau de gravité ;
* un responsable.

---

# CHAPITRE 167 — NIVEAUX DE PRIORITÉ

Les priorités officielles sont :

🔴 Critique

🟠 Élevée

🟡 Normale

🟢 Faible

La priorité influence les délais de traitement.

---

# CHAPITRE 168 — CYCLE DE VIE D'UN INCIDENT

```text
Signalement

↓

Qualification

↓

Analyse

↓

Collecte des informations

↓

Décision

↓

Résolution

↓

Clôture

↓

Archivage
```

Chaque changement d'état est historisé.

---

# CHAPITRE 169 — COLLECTE DES INFORMATIONS

Le moteur rassemble automatiquement les éléments disponibles :

* historique des conversations ;
* historique du dossier ;
* historique des visites ;
* historique des négociations ;
* historique des paiements de services ;
* documents transmis ;
* dates ;
* utilisateurs concernés.

Aucune donnée ne doit être supprimée.

---

# CHAPITRE 170 — MÉDIATION

Lorsque cela est possible.

LAWIM peut proposer une médiation.

La médiation consiste à faciliter les échanges.

LAWIM ne prend jamais de décision juridique à la place des parties.

---

# CHAPITRE 171 — FRAUDE

En cas de suspicion de fraude.

Le système peut automatiquement :

* suspendre temporairement un compte ;
* suspendre un bien ;
* suspendre une annonce ;
* suspendre une mise en relation.

Toute suspension est :

* motivée ;
* historisée ;
* réversible après vérification.

---

# CHAPITRE 172 — RÉCLAMATIONS SUR LES SERVICES LAWIM

Les réclamations portant sur :

* les paiements de services ;
* les mises en relation ;
* les services Premium ;
* les remboursements ;

sont traitées par le Support LAWIM.

Le traitement suit un workflow dédié.

---

# CHAPITRE 173 — INCIDENTS SUR LES BIENS

Les incidents concernant un bien peuvent entraîner :

* une demande de correction ;
* une suspension temporaire ;
* une vérification documentaire ;
* une vérification d'identité ;
* un archivage.

Le propriétaire est informé des décisions prises.

---

# CHAPITRE 174 — INCIDENTS SUR LES UTILISATEURS

Lorsqu'un utilisateur présente un comportement contraire aux règles.

LAWIM peut :

* envoyer un avertissement ;

* demander des justificatifs ;

* limiter certaines fonctionnalités ;

* suspendre temporairement le compte ;

* transmettre le dossier à un administrateur.

---

# CHAPITRE 175 — INCIDENTS SUR LES DOSSIERS

Un dossier peut être suspendu notamment en cas de :

* fraude présumée ;

* litige majeur ;

* demande des autorités ;

* demande expresse des parties.

La suspension conserve intégralement l'historique.

---

# CHAPITRE 176 — SLA DES INCIDENTS

Chaque incident possède un délai maximal de traitement.

Exemple.

Critique :

prise en charge immédiate.

---

Élevé :

moins de 24 heures.

---

Normal :

moins de 72 heures.

---

Faible :

selon les disponibilités du support.

Ces délais sont configurables.

---

# CHAPITRE 177 — TRAÇABILITÉ

Chaque action est enregistrée.

Le système conserve notamment :

* auteur ;

* date ;

* décision ;

* justification ;

* pièces jointes ;

* commentaires.

L'historique ne peut jamais être supprimé.

---

# CHAPITRE 178 — INDICATEURS

Les incidents alimentent les tableaux de bord.

Exemples.

* nombre d'incidents ;

* délai moyen de résolution ;

* taux de fraude ;

* taux de réclamations ;

* taux de satisfaction après résolution ;

* incidents par type de bien ;

* incidents par ville.

---

# CHAPITRE 179 — APPRENTISSAGE

Le moteur apprend des incidents.

Exemples.

Un détenteur reçoit plusieurs signalements fondés.

↓

Son indice de fiabilité diminue.

---

Un type d'annonce génère fréquemment des erreurs.

↓

Les contrôles automatiques sont renforcés.

L'objectif est d'améliorer continuellement la qualité de la plateforme.

---

# CHAPITRE 180 — RÈGLES ABSOLUES

Le workflow des incidents doit toujours :

✓ conserver toutes les preuves disponibles ;

✓ protéger les deux parties ;

✓ assurer une traçabilité complète ;

✓ respecter les SLA ;

✓ permettre une reprise normale du workflow lorsque le problème est résolu.

Il ne doit jamais :

❌ supprimer des preuves ;

❌ modifier l'historique ;

❌ rendre une décision judiciaire ;

❌ bloquer définitivement un utilisateur sans procédure prévue.

---

# CHAPITRE 181 — OBJECTIF FINAL

Le workflow des litiges, réclamations et incidents garantit que LAWIM reste une plateforme de confiance.

Chaque incident est :

* identifié ;
* traité ;
* documenté ;
* historisé ;

afin de protéger les utilisateurs, d'améliorer la qualité du service et de renforcer la fiabilité globale de la plateforme.

---

# FIN DE LA PARTIE 10

# LAWIM

# 05-WORKFLOW-REFERENCE.md

# PARTIE 11

# Workflow de clôture, archivage et conservation

Version 1.0

---

# CHAPITRE 182 — PRINCIPE FONDAMENTAL

Dans LAWIM.

Aucune donnée métier n'est supprimée.

Chaque objet suit son cycle de vie jusqu'à sa clôture puis son archivage.

La clôture met fin au workflow actif.

L'archivage conserve définitivement l'historique.

La suppression physique reste interdite sauf obligation légale, demande réglementaire valide ou décision exceptionnelle d'un administrateur habilité conformément aux règles de conservation de LAWIM.

---

# CHAPITRE 183 — OBJETS CONCERNÉS

Les règles de clôture s'appliquent notamment :

* aux dossiers ;
* aux biens ;
* aux conversations ;
* aux visites ;
* aux négociations ;
* aux transactions ;
* aux paiements de services ;
* aux incidents ;
* aux notifications ;
* aux workflows.

---

# CHAPITRE 184 — CONDITIONS DE CLÔTURE

Un objet peut être clôturé notamment lorsque :

✓ son objectif est atteint ;

✓ il est abandonné ;

✓ il devient définitivement sans objet ;

✓ une décision administrative le justifie.

La clôture doit toujours être motivée.

---

# CHAPITRE 185 — CLÔTURE D'UN DOSSIER

Un dossier peut être clôturé pour les raisons suivantes :

* transaction réalisée ;

* projet abandonné ;

* demande annulée ;

* absence prolongée du demandeur ;

* décision administrative.

Avant clôture.

LAWIM vérifie :

* qu'aucune visite n'est en attente ;

* qu'aucune négociation n'est ouverte ;

* qu'aucun paiement de service n'est bloqué ;

* qu'aucun incident critique n'est actif.

---

# CHAPITRE 186 — CLÔTURE D'UN BIEN

Un bien peut être clôturé lorsque :

* il est vendu ;

* il est loué ;

* son propriétaire le retire ;

* il est définitivement indisponible.

La clôture entraîne automatiquement :

* l'arrêt du matching ;

* l'arrêt des nouvelles visites ;

* la mise à jour des dossiers concernés.

---

# CHAPITRE 187 — CLÔTURE D'UNE CONVERSATION

Une conversation est clôturée lorsque :

* le dossier est terminé ;

* les parties mettent fin aux échanges ;

* une période d'inactivité configurable est dépassée.

La conversation reste consultable.

Elle n'est jamais supprimée.

---

# CHAPITRE 188 — CLÔTURE D'UNE NÉGOCIATION

Une négociation est clôturée lorsque :

* un accord est trouvé ;

* une partie abandonne ;

* le délai maximal est dépassé ;

* le bien devient indisponible.

La clôture déclenche automatiquement :

* la transaction ;

ou

* un rematching.

---

# CHAPITRE 189 — ARCHIVAGE

Après clôture.

Les objets passent en archivage.

Un objet archivé :

* n'est plus modifiable ;

* n'est plus utilisé dans les workflows actifs ;

* reste disponible pour :

  * l'audit ;

  * les statistiques ;

  * le reporting ;

  * l'apprentissage du moteur.

## Archivage longue durée

Après 3 ans d'archivage opérationnel, un objet peut passer en archivage longue durée.

L'archivage longue durée ne supprime pas les données.

Les données restent consultables selon les droits.

Les données ne participent plus aux workflows actifs.

Les données ne participent plus au matching.

Les données restent disponibles pour l'audit, les statistiques historiques, la conformité et le reporting.

La migration vers l'archivage longue durée est historisée.

Une réactivation reste possible uniquement par procédure administrative autorisée.

La suppression physique reste interdite, sauf obligation légale, demande réglementaire valide ou décision exceptionnelle d'un administrateur habilité conformément aux règles de conservation de LAWIM.

---

# CHAPITRE 190 — RÉOUVERTURE

Un objet archivé peut être réactivé uniquement dans les cas prévus.

Exemples :

* vente annulée ;

* fin de bail ;

* nouvelle demande ;

* décision administrative.

La réouverture conserve tout l'historique.

Aucune information n'est perdue.

---

# CHAPITRE 191 — MÉDIATION LAWIM

Lorsqu'un désaccord apparaît avant la clôture définitive d'un dossier.

LAWIM peut proposer une médiation.

La médiation est une démarche amiable.

Elle ne remplace jamais :

* un tribunal ;

* un notaire ;

* un avocat ;

* une autorité administrative.

Le Médiateur LAWIM intervient uniquement pour :

* faciliter le dialogue ;

* expliquer les procédures LAWIM ;

* rechercher une solution amiable ;

* documenter les échanges.

Le Médiateur LAWIM ne rend jamais une décision contraignante.

---

# CHAPITRE 192 — HISTORIQUE ET AUDIT

La clôture ou l'archivage ne supprime jamais :

* les états ;

* les événements ;

* les documents ;

* les conversations ;

* les paiements de services ;

* les visites ;

* les négociations ;

* les décisions ;

* les journaux d'audit.

Toutes les informations restent consultables selon les droits d'accès.

---

# CHAPITRE 193 — RÈGLES ABSOLUES

Le workflow de clôture doit toujours :

✓ vérifier que toutes les étapes précédentes sont terminées ;

✓ conserver l'intégralité de l'historique ;

✓ mettre à jour les indicateurs ;

✓ recalculer les statistiques ;

✓ libérer les ressources des workflows actifs ;

✓ permettre une réouverture lorsque les règles métier l'autorisent.

Il ne doit jamais :

❌ supprimer définitivement un objet métier ;

❌ perdre l'historique ;

❌ clôturer un dossier comportant une étape critique inachevée ;

❌ archiver un objet encore utilisé par un workflow actif.

---

# CHAPITRE 194 — OBJECTIF FINAL

Le workflow de clôture garantit que chaque objet métier de LAWIM termine son cycle de vie de manière :

* cohérente ;

* traçable ;

* réversible lorsque cela est prévu ;

* conforme à la Constitution LAWIM.

La mémoire de LAWIM constitue un actif stratégique.

Elle ne doit jamais être altérée ni perdue.

---


## CHAPITRE 195 — MÉDIATION LAWIM

### Principe

LAWIM peut proposer un processus de médiation lorsqu'un différend apparaît entre les parties.

La médiation est une démarche amiable destinée à faciliter la communication et à favoriser une solution acceptable par tous.

Elle intervient uniquement lorsque les parties acceptent d'y participer.

---

### Le Médiateur LAWIM

Le Médiateur LAWIM est un collaborateur ou un représentant officiellement désigné par LAWIM.

Son rôle consiste exclusivement à :

* écouter les différentes parties ;
* faciliter le dialogue ;
* expliquer les procédures de LAWIM ;
* rechercher une solution amiable ;
* documenter les échanges.

Le Médiateur LAWIM n'est ni juge, ni arbitre, ni notaire, ni avocat.

Il ne rend aucune décision contraignante.

---

### Déclenchement

Une médiation peut être proposée :

* par le demandeur ;
* par le détenteur ;
* par un collaborateur LAWIM ;
* automatiquement par LAWIM AI lorsqu'un conflit est détecté.

La médiation reste toujours facultative.

---

### Déroulement

Le workflow de médiation est le suivant :

```text
Incident

↓

Proposition de médiation

↓

Acceptation des parties

↓

Nomination du Médiateur LAWIM

↓

Échanges

↓

Proposition de solution

↓

Acceptation

↓

Clôture
```

Si une partie refuse la médiation, le dossier reprend son workflow normal.

---

### Traçabilité

Toutes les actions du Médiateur LAWIM sont historisées :

* date ;
* participants ;
* observations ;
* propositions ;
* issue de la médiation.

Les échanges restent confidentiels selon les règles définies par LAWIM.

---

### Fin de la médiation

Une médiation peut se terminer par :

* un accord amiable ;
* un désaccord ;
* un abandon ;
* une orientation vers une autorité compétente.

Dans tous les cas, le dossier conserve l'historique complet.

---

### Règles absolues

Le Médiateur LAWIM doit toujours :

✓ rester neutre ;

✓ respecter la confidentialité ;

✓ documenter les échanges ;

✓ faciliter le dialogue.

Il ne doit jamais :

❌ imposer une décision ;

❌ représenter une partie ;

❌ modifier l'historique du dossier ;

❌ rendre une décision juridique.

---

### Objectif

La médiation vise à résoudre rapidement les difficultés tout en préservant la confiance entre les utilisateurs et la qualité du service LAWIM.

Elle constitue un service d'accompagnement et non une procédure juridictionnelle.


# LAWIM

# 05-WORKFLOW-REFERENCE.md

# PARTIE 12

# Workflows transversaux et règles de cohérence

Version 1.0

---

# CHAPITRE 196 — PRINCIPE FONDAMENTAL

Les workflows décrits dans les parties précédentes ne fonctionnent jamais de manière isolée.

Chaque événement survenant dans LAWIM peut impacter plusieurs workflows simultanément.

Le présent chapitre définit les règles garantissant la cohérence globale du système.

---

# CHAPITRE 197 — PRINCIPE DE SYNCHRONISATION

Un changement d'état d'un objet métier doit automatiquement mettre à jour les objets qui en dépendent.

Exemples :

Bien vendu

↓

Dossiers mis à jour

↓

Matching interrompu

↓

Visites annulées

↓

Notifications envoyées

---

Paiement de service validé

↓

Mise en relation autorisée

↓

Conversation débloquée

↓

Next Best Action recalculée

---

# CHAPITRE 198 — OBJETS MÉTIER CONCERNÉS

Les objets suivants participent aux workflows transversaux :

* Projet immobilier ;
* Dossier ;
* Bien ;
* Conversation ;
* Matching ;
* Visite ;
* Négociation ;
* Transaction ;
* Paiement de service ;
* Notification ;
* Utilisateur ;
* Introduceur ;
* Agence ;
* Historique ;
* Journal d'audit.

---

# CHAPITRE 199 — ÉVÉNEMENTS GLOBAUX

Les événements suivants sont considérés comme transversaux.

* création ;
* modification ;
* suppression logique ;
* publication ;
* archivage ;
* paiement ;
* annulation ;
* suspension ;
* réactivation ;
* changement d'état.

Chaque événement peut déclencher plusieurs workflows.

---

# CHAPITRE 200 — MOTEUR D'ÉVÉNEMENTS

Tous les workflows communiquent par événements.

Aucun module ne doit modifier directement un autre module.

Exemple.

```text
Bien vendu

↓

Événement

PROPERTY_SOLD

↓

Workflow Dossiers

↓

Workflow Matching

↓

Workflow Conversations

↓

Workflow Notifications

↓

Workflow Reporting
```

Les modules sont faiblement couplés.

---

# CHAPITRE 201 — NEXT BEST ACTION

Chaque objet métier possède obligatoirement une Next Best Action.

Exemples.

Projet :

Créer le dossier.

---

Bien :

Compléter les photos.

---

Dossier :

Lancer un rematching.

---

Visite :

Confirmer le rendez-vous.

---

Transaction :

Préparer les documents.

Cette action est recalculée après chaque événement.

---

# CHAPITRE 202 — SLA GLOBAUX

Tous les workflows sont soumis aux SLA définis par LAWIM.

Lorsque le délai maximal est dépassé.

Le moteur déclenche automatiquement :

* une relance ;
* une notification ;
* un rematching ;
* une escalade ;
* ou une clôture selon le contexte.

L'inaction est interdite.

---

# CHAPITRE 203 — WORKFLOW PRINCIPAL

Le workflow principal de LAWIM est le suivant.

```text
Projet immobilier

↓

Création du dossier

↓

Qualification

↓

Matching

↓

Mise en relation

↓

Visite

↓

Négociation

↓

Transaction

↓

Clôture

↓

Archivage
```

Tous les autres workflows viennent enrichir ce parcours.

---

# CHAPITRE 204 — WORKFLOWS SPÉCIALISÉS

Selon le contexte.

Le moteur peut charger automatiquement un workflow spécialisé.

Exemples.

* appartement_location ;

* villa_vente ;

* terrain_vente_titre_foncier ;

* terrain_vente_droit_coutumier ;

* hôtel_vente ;

* immeuble_investissement.

Le choix du workflow dépend :

* du type de bien ;

* du type d'opération ;

* du contexte juridique ;

* du contexte commercial.

---

# CHAPITRE 205— ACTEURS DU WORKFLOW

Chaque workflow peut faire intervenir différents acteurs.

Acteurs obligatoires :

* 🤖 LAWIM AI ;
* 👤 Demandeur ;
* 🏠 Détenteur.

Acteurs optionnels selon le contexte :

* 👨🏽‍💼 Conseiller LAWIM ;
* 🤝 Introduceur ;
* 🏢 Agence ;
* ⚖️ Notaire ;
* 📐 Géomètre ;
* 👑 Chef traditionnel ;
* 🏛️ Service des domaines ;
* ⚖️ Avocat ;
* 👨🏽‍⚖️ Médiateur LAWIM ;
* 🏦 Banque ;
* autres partenaires.

Le moteur active uniquement les acteurs nécessaires.

---

# CHAPITRE 206 — WORKFLOW TEMPLATES

LAWIM fonctionne à partir de modèles de workflows (Workflow Templates).

Chaque template définit :

* les états ;
* les transitions ;
* les documents ;
* les acteurs ;
* les SLA ;
* les notifications ;
* les règles de décision.

Les templates sont versionnés.

Ils sont stockés en base de données.

Ils ne doivent jamais être codés en dur.

---

# CHAPITRE 207 — JOURNAL D'AUDIT

Toutes les transitions sont enregistrées.

Le journal d'audit conserve notamment :

* auteur ;
* rôle ;
* ancien état ;
* nouvel état ;
* date ;
* justification ;
* origine de l'action (IA, utilisateur, système).

Le journal est immuable.

---

# CHAPITRE 208 — RÉSILIENCE

LAWIM doit pouvoir reprendre automatiquement un workflow interrompu.

Exemples :

* coupure réseau ;

* redémarrage serveur ;

* interruption utilisateur ;

* échec temporaire d'un service.

Aucune information ne doit être perdue.

---

# CHAPITRE 209— RÈGLES ABSOLUES

Tous les workflows doivent :

✓ respecter la Constitution LAWIM ;

✓ utiliser les référentiels officiels ;

✓ recalculer la Next Best Action après chaque événement ;

✓ conserver la traçabilité complète ;

✓ respecter les SLA ;

✓ communiquer uniquement par événements.

Ils ne doivent jamais :

❌ modifier directement un autre workflow ;

❌ perdre l'historique ;

❌ créer des états non documentés ;

❌ contourner les règles métier ;

❌ créer des dépendances circulaires.

---

# CHAPITRE 210 — OBJECTIF FINAL

Le système de workflows constitue le cœur opérationnel de LAWIM.

Il garantit que chaque dossier, chaque bien, chaque utilisateur et chaque transaction évoluent de manière cohérente, traçable et automatisée.

Tous les développements futurs devront respecter les règles définies dans ce référentiel.

---

# CHAPITRE 211 — TRACKING MARKETING TRANSVERSE

Le Tracking Marketing constitue une capacité transverse partagée.

Il ne constitue pas un workflow indépendant et ne doit jamais être implémenté comme une logique séparée.

Les événements de tracking enrichissent les workflows existants, notamment la publication, la redirection, la conversation, le matching, la visite, le paiement et le reporting.

---

# CHAPITRE 212 — WORKFLOW DE PUBLICATION ENRICHI

Le workflow officiel de publication devient :

Création de la publication
↓
Validation
↓
Génération automatique du Tracking Code
↓
Association à une campagne éventuelle
↓
Association à un acteur
↓
Association à un ou plusieurs biens
↓
Association à un ou plusieurs services
↓
Publication sur le canal
↓
Journalisation
↓
Mise à jour des statistiques
↓
Disponibilité des dashboards

Le rôle de l'acteur est historisé séparément du Tracking Code.

---

# CHAPITRE 213 — WORKFLOW DE REDIRECTION ENRICHI

Utilisateur
↓
Clic sur le lien
↓
Validation du Tracking Code
↓
Contrôle d'intégrité
↓
Détection bot
↓
Détection doublon
↓
Journalisation
↓
Création éventuelle d'une session
↓
Redirection
↓
Mise à jour des statistiques
↓
Événement envoyé au Reporting
↓
Événement envoyé au Continuous Learning

---

# CHAPITRE 214 — WORKFLOW DE CONVERSION ET ATTRIBUTION

Publication
↓
Clic
↓
Redirection
↓
Visite
↓
Création éventuelle du compte
↓
Conversation
↓
Matching
↓
Visite terrain
↓
Service LAWIM
↓
Paiement Campay confirmé
↓
Conversion
↓
Historisation

Chaque conversion peut être reliée au canal, à la campagne, à la publication, à l'acteur, au bien, au service et au paiement Campay éventuel.

---

# FIN DE 05-WORKFLOW-REFERENCE.md
