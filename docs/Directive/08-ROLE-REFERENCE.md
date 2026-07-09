LAWIM
08-ROLE-REFERENCE.md
Référentiel Officiel des Rôles, Permissions et Niveaux de Confiance

Version 1.0

PARTIE 1
Principes fondamentaux
CHAPITRE 1 — OBJECTIF

Le présent document définit le système officiel d'identité, de rôles, de permissions et de confiance de LAWIM.

Il constitue la référence unique pour :

l'inscription ;
l'authentification ;
les rôles ;
les permissions ;
les accès aux dashboards ;
les badges ;
le Trust Score ;
les agences ;
les membres de l'équipe LAWIM ;
la validation des comptes.

Aucun rôle, aucune permission et aucun badge ne doivent être créés en dehors de ce référentiel.

CHAPITRE 2 — PRINCIPE FONDAMENTAL

Dans LAWIM, l'identité est progressive.

Un utilisateur commence généralement comme demandeur.

Son rôle peut évoluer selon :

ses actions ;
les biens qu'il publie ;
les validations obtenues ;
son rattachement à une agence ;
son appartenance à l'équipe LAWIM ;
son niveau de confiance.

Le rôle principal affiché est toujours le rôle le plus élevé atteint.

Il n'y a pas de régression automatique.

CHAPITRE 3 — COMPTE UNIQUE

Chaque personne physique doit posséder un seul compte utilisateur.

Un compte peut cumuler plusieurs capacités.

Exemple :

Un agent immobilier peut aussi rechercher un bien pour lui-même.

Il conserve cependant son rôle principal d'agent.

Le système ne doit pas créer plusieurs comptes pour la même personne lorsqu'un seul compte suffit.

CHAPITRE 4 — PAGE DE CONNEXION UNIQUE

LAWIM utilise une seule page de connexion pour tous les utilisateurs.

Le dashboard affiché après connexion dépend :

de l'identité ;
du rôle principal ;
des rôles secondaires ;
des permissions ;
de l'organisation éventuelle ;
du Trust Score ;
des workflows actifs.

Il n'existe pas de page de connexion séparée par rôle.

CHAPITRE 5 — RÔLE PRINCIPAL

Le rôle principal représente le plus haut niveau fonctionnel atteint par l'utilisateur.

Exemples :

un demandeur qui publie son propre bien devient propriétaire ;
un propriétaire qui recherche un autre bien reste propriétaire ;
un agent qui recherche un bien reste agent ;
un responsable d'agence reste responsable d'agence ;
un membre LAWIM conserve son rôle interne.

Le rôle principal sert notamment à :

déterminer le dashboard principal ;
afficher l'identité ;
appliquer certaines priorités ;
définir le niveau général d'accès.
CHAPITRE 6 — RÔLES SECONDAIRES

Un utilisateur peut posséder plusieurs rôles secondaires.

Exemple :

Utilisateur :

rôle principal : Agent immobilier ;
rôle secondaire : Demandeur ;
rôle secondaire : Propriétaire.

Les rôles secondaires donnent accès à des fonctionnalités spécifiques, sans modifier l'identité principale affichée.

CHAPITRE 7 — PROGRESSION NON RÉGRESSIVE

Le système peut promouvoir automatiquement un utilisateur vers un rôle supérieur.

Le système ne peut jamais le rétrograder automatiquement.

Toute rétrogradation nécessite :

une intervention humaine ;
un administrateur habilité ;
un motif ;
une trace dans l'audit ;
une notification interne.

Exemples interdits automatiquement :

Agent → Demandeur ;
Propriétaire → Demandeur ;
Responsable agence → Agent.
CHAPITRE 8 — IDENTITÉ VISUELLE

Chaque rôle possède :

une icône ;
un nom affiché ;
une couleur éventuelle ;
un niveau de priorité.

Le nom affiché dans les conversations reste limité à huit caractères lorsque cela est requis par le référentiel conversationnel.

CHAPITRE 9 — PERMISSIONS

Les permissions déterminent ce que l'utilisateur peut faire.

Le rôle indique qui il est.

La permission indique ce qu'il peut faire.

Exemple :

Un propriétaire peut avoir le rôle Propriétaire mais ne pas encore avoir la permission "Agence vérifiée".

Les permissions peuvent être :

automatiques ;
accordées après validation ;
limitées dans le temps ;
suspendues ;
retirées manuellement.
CHAPITRE 10 — TRUST SCORE

LAWIM utilise un Trust Score pour mesurer le niveau de confiance d'un compte.

Le Trust Score ne remplace jamais le rôle.

Il complète l'identité.

Il peut influencer :

le matching ;
les badges ;
la visibilité ;
les validations ;
les priorités de traitement ;
les dashboards.
CHAPITRE 11 — BADGES

Les badges permettent d'afficher clairement les validations obtenues.

Exemples :

téléphone vérifié ;
e-mail vérifié ;
identité vérifiée ;
propriétaire vérifié ;
agence vérifiée ;
professionnel validé ;
partenaire LAWIM.

Les badges doivent être justifiés par des validations réelles.

CHAPITRE 12 — ORGANISATIONS

Une agence n'est pas un simple utilisateur.

Une agence est une organisation.

Elle possède :

un responsable ;
des agents ;
des biens ;
des dossiers ;
des validations ;
un niveau de confiance.

Une agence doit obligatoirement être validée avant d'être considérée comme agence vérifiée.

CHAPITRE 13 — ÉQUIPE LAWIM

Les membres de l'équipe LAWIM sont créés par un administrateur habilité.

L'administrateur principal peut créer tous les membres.

Son adjoint peut créer certains membres de rang inférieur, mais ces créations doivent être validées par l'administrateur principal.

Aucun utilisateur public ne peut devenir membre LAWIM automatiquement.

CHAPITRE 14 — TRAÇABILITÉ

Toute modification d'identité, de rôle, de permission, de badge ou de Trust Score doit être historisée.

L'historique conserve :

ancienne valeur ;
nouvelle valeur ;
auteur ;
date ;
motif ;
justification ;
documents éventuels.
CHAPITRE 15 — OBJECTIF FINAL

Le système de rôles et de confiance de LAWIM doit garantir :

la sécurité ;
la clarté ;
la confiance ;
la traçabilité ;
la progression naturelle des utilisateurs ;
la protection contre les faux profils ;
l'accès correct aux dashboards et fonctionnalités.

LAWIM doit toujours savoir qui agit, avec quel rôle, avec quels droits et avec quel niveau de confiance.

FIN DE LA PARTIE 1


# LAWIM

# 08-ROLE-REFERENCE.md

# PARTIE 2

# Cycle de vie de l'identité utilisateur

Version 1.0

---

# CHAPITRE 16 — PRINCIPE FONDAMENTAL

Chaque personne physique possède un compte utilisateur unique.

Ce compte évolue tout au long de sa vie sur la plateforme.

LAWIM privilégie l'évolution d'un même compte plutôt que la création de plusieurs comptes pour une même personne.

---

# CHAPITRE 17 — INSCRIPTION

L'inscription peut être réalisée :

* depuis le site Web ;
* depuis l'application mobile ;
* à partir d'un lien d'invitation ;
* à partir d'un QR Code ;
* par invitation d'une agence ;
* par invitation d'un membre LAWIM.

Toutes les inscriptions utilisent le même processus.

Le formulaire public de creation de compte demande au minimum :

* nom complet ;
* email unique ;
* username unique ;
* numero WhatsApp obligatoire ;
* mot de passe ;
* confirmation du mot de passe ;
* langue preferee ;
* acceptation des conditions.

Le backend refuse toute creation sans numero WhatsApp.

---

# CHAPITRE 18 — IDENTIFIANT PRINCIPAL

La connexion utilise un champ unique `Identifiant`.

Cet identifiant peut être :

* email ;
* numéro de téléphone WhatsApp au format international ;
* username.

Le backend résout correctement l'utilisateur sur ces trois formes d'identification.

Chaque email, chaque username et chaque numéro WhatsApp doivent rester uniques pour les comptes actifs.

---

# CHAPITRE 19 — VÉRIFICATION INITIALE

Avant creation, LAWIM verifie :

* la presence du nom complet ;
* la presence de l'email ;
* la presence du username ;
* la presence du numero WhatsApp ;
* la cohérence du mot de passe et de sa confirmation ;
* la langue preferee ;
* l'acceptation des conditions.

Le choix de langue est memorise des la creation du compte.

---

# CHAPITRE 20 — ACTIVATION DU COMPTE

Le compte public devient actif lorsque les validations de creation sont passees.

Le role initial de l'inscription publique est :

**user**

Le dashboard correspondant est alors genere automatiquement selon le role resolu.

Les comptes publics peuvent ensuite evoluer selon les regles de gouvernance.

---

# CHAPITRE 21 — ÉVOLUTION AUTOMATIQUE

Le système peut promouvoir automatiquement un utilisateur.

Exemples :

Demandeur

↓

Publication d'un bien

↓

Propriétaire

---

Demandeur

↓

Déclaration de gestion d'un bien

↓

Détenteur

---

Détenteur

↓

Validation professionnelle

↓

Agent immobilier

---

Agent

↓

Création d'une agence validée

↓

Responsable d'agence

---

Les promotions automatiques sont historisées.

---

# CHAPITRE 22 — VÉRIFICATION D'IDENTITÉ

Certaines fonctionnalités nécessitent une vérification d'identité.

LAWIM peut demander :

* Carte Nationale d'Identité ;
* Passeport ;
* Carte de séjour (selon le pays).

Les documents sont examinés par un membre habilité de l'équipe LAWIM.

Après validation, le badge :

🪪 **Identité vérifiée**

est attribué.

---

# CHAPITRE 23 — CRÉATION D'UNE AGENCE

Une agence ne peut pas être créée automatiquement.

Le demandeur doit fournir notamment :

* nom de l'agence ;
* responsable ;
* téléphone ;
* adresse ;
* localisation ;
* CNI du responsable.

Selon la situation juridique, LAWIM peut également demander :

* RCCM ;
* numéro contribuable ;
* autorisation d'exercice ;
* autres justificatifs.

Après contrôle.

L'agence reçoit le statut :

🏢 **Agence vérifiée**

---

# CHAPITRE 24 — AJOUT D'UN AGENT

Un responsable d'agence peut inviter un agent.

Le processus est le suivant :

Invitation

↓

Lien sécurisé

↓

Création du compte

↓

Téléphone vérifié

↓

CNI

↓

Validation LAWIM

↓

Agent actif

Chaque agent possède un compte personnel.

Le partage de comptes est interdit.

---

# CHAPITRE 25 — MEMBRES LAWIM

Les comptes de l'équipe LAWIM sont créés uniquement par un administrateur habilité.

L'administrateur principal peut créer tous les comptes.

Son adjoint peut créer des comptes de niveau inférieur.

Toutefois :

ces comptes restent inactifs jusqu'à leur validation par l'administrateur principal.

---

# CHAPITRE 26 — SUSPENSION

Un compte peut être :

* suspendu ;
* limité ;
* désactivé ;
* réactivé.

Toute suspension est :

* motivée ;
* historisée ;
* notifiée.

Les données du compte sont conservées conformément aux règles d'archivage.

---

# CHAPITRE 27 — FUSION DE COMPTES

Lorsqu'une même personne possède plusieurs comptes créés par erreur.

LAWIM peut procéder à une fusion administrative.

La fusion conserve notamment :

* l'historique ;
* les biens ;
* les conversations ;
* les workflows ;
* les documents ;
* les services ;
* les statistiques.

Aucune donnée ne doit être perdue.

---

# CHAPITRE 28 — SUPPRESSION D'UN COMPTE

La suppression physique d'un compte est exceptionnelle.

En règle générale.

Le compte est :

* désactivé ;
* archivé ;
* anonymisé lorsque la réglementation l'impose.

Les historiques nécessaires au fonctionnement et aux obligations légales sont conservés selon les règles de rétention.

---

# CHAPITRE 29 — RÈGLES ABSOLUES

Le cycle de vie d'un utilisateur doit toujours :

✓ commencer par un numéro de téléphone vérifié ;

✓ utiliser un compte unique ;

✓ permettre une progression naturelle ;

✓ empêcher les régressions automatiques ;

✓ garantir la traçabilité ;

✓ protéger les documents d'identité.

Il est interdit :

❌ de créer plusieurs comptes pour une même personne sans justification ;

❌ de promouvoir un utilisateur sans respecter les règles définies ;

❌ de partager un compte entre plusieurs personnes ;

❌ de supprimer définitivement un compte sans procédure officielle.

---

# CHAPITRE 30 — OBJECTIF FINAL

Le cycle de vie des utilisateurs garantit que chaque personne dispose d'une identité unique, évolutive et fiable.

Il permet à LAWIM de construire progressivement un écosystème de confiance où chaque rôle, chaque validation et chaque permission reposent sur une identité clairement établie et durable.

---

# FIN DE LA PARTIE 2

# LAWIM

# 08-ROLE-REFERENCE.md

# PARTIE 3

# Référentiel officiel des rôles

Version 1.0

---

# CHAPITRE 31 — PRINCIPE FONDAMENTAL

Les rôles définissent la fonction principale d'un utilisateur dans LAWIM.

Ils ne doivent pas être confondus avec :

* les permissions ;
* les badges ;
* le Trust Score ;
* les organisations.

Chaque utilisateur possède :

* un rôle principal ;
* éventuellement plusieurs rôles secondaires.

Le rôle principal est toujours le plus élevé atteint.

---

# CHAPITRE 32 — FAMILLES DE RÔLES

LAWIM distingue quatre grandes familles de rôles.

### Utilisateurs

* Demandeur
* Détenteur
* Propriétaire

---

### Professionnels

* Agent immobilier
* Responsable d'agence
* Administrateur d'agence

---

### Partenaires

* Notaire partenaire
* Géomètre partenaire
* Banquier partenaire
* Expert partenaire
* Prestataire partenaire

Cette liste pourra être enrichie sans modifier l'architecture générale.

---

### Équipe LAWIM

* Assistant
* Conseiller
* Médiateur
* Responsable opérationnel
* Administrateur
* Administrateur principal

---

# CHAPITRE 33 — DEMANDEUR

Le Demandeur est le rôle initial.

Il peut notamment :

* rechercher un bien ;
* créer un projet ;
* recevoir des propositions ;
* dialoguer avec les détenteurs ;
* commander des services LAWIM ;
* programmer des visites.

Tous les utilisateurs commencent par ce rôle.

---

# CHAPITRE 34 — DÉTENTEUR

Le Détenteur est une personne autorisée à publier ou gérer un bien.

Il peut être :

* propriétaire ;
* mandataire ;
* représentant familial ;
* gestionnaire ;
* administrateur de biens.

Le système peut demander des justificatifs selon le type de détention déclaré.

---

# CHAPITRE 35 — PROPRIÉTAIRE

Le Propriétaire est un détenteur qui déclare être propriétaire du bien.

LAWIM peut demander des documents justificatifs.

Exemples :

* titre foncier ;
* acte de vente ;
* attestation de propriété ;
* autres documents reconnus.

Le badge **Propriétaire vérifié** n'est attribué qu'après validation.

---

# CHAPITRE 36 — AGENT IMMOBILIER

L'Agent immobilier est un professionnel validé.

Conditions minimales :

* identité vérifiée ;
* rattachement à une agence ou activité indépendante déclarée ;
* validation LAWIM.

Il peut :

* gérer plusieurs biens ;
* représenter plusieurs propriétaires ;
* suivre plusieurs dossiers simultanément.

---

# CHAPITRE 37 — AGENCE

Une agence est une organisation.

Elle possède :

* un responsable ;
* des administrateurs d'agence ;
* des agents.

LAWIM recommande un minimum de trois agents actifs pour considérer une agence comme pleinement opérationnelle.

L'équipe LAWIM peut toutefois autoriser une phase de création avec un effectif inférieur afin de permettre son démarrage.

---

# CHAPITRE 38 — RESPONSABLE D'AGENCE

Le Responsable d'agence dirige l'organisation.

Il peut notamment :

* inviter des agents ;
* gérer les biens de l'agence ;
* suivre les performances ;
* demander des services LAWIM ;
* administrer les paramètres de l'agence.

Certaines opérations sensibles nécessitent une validation supplémentaire.

---

# CHAPITRE 39 — PARTENAIRES

LAWIM peut référencer différents partenaires.

Exemples :

* notaires ;
* géomètres ;
* banques ;
* assureurs ;
* photographes ;
* vidéastes ;
* déménageurs ;
* artisans ;
* diagnostiqueurs.

Chaque partenaire possède son propre processus de validation.

---

# CHAPITRE 40 — ÉQUIPE LAWIM

Les rôles internes sont attribués uniquement par l'administration.

Ils comprennent notamment :

* Assistant ;
* Conseiller ;
* Médiateur ;
* Responsable opérationnel ;
* Administrateur ;
* Administrateur principal.

Les rôles internes sont indépendants des rôles publics.

---

# CHAPITRE 41 — CUMUL DES RÔLES

Un utilisateur peut cumuler plusieurs rôles.

Exemples.

Un propriétaire peut être également demandeur.

Un agent immobilier peut rechercher un bien pour lui-même.

Un responsable d'agence peut être propriétaire de biens personnels.

Le Dashboard et les permissions tiennent compte de l'ensemble des rôles.

---

# CHAPITRE 42 — CHANGEMENT DE RÔLE

Les changements de rôle peuvent être :

* automatiques (selon les règles métier) ;
* validés par LAWIM ;
* administratifs.

Toute évolution est enregistrée dans l'historique.

Les rétrogradations automatiques sont interdites.

---

# CHAPITRE 43 — INACTIVITÉ

L'inactivité ne modifie jamais le rôle principal.

Exemples.

Un propriétaire qui ne publie plus de biens reste propriétaire.

Un agent qui ne réalise plus d'activité reste agent.

Les permissions opérationnelles peuvent être suspendues, mais le rôle reste conservé jusqu'à décision contraire.

---

# CHAPITRE 44 — AFFICHAGE DU RÔLE

Le Dashboard et les conversations affichent :

* l'icône du rôle principal ;
* le nom du rôle principal ;
* les badges de vérification pertinents.

Les rôles secondaires peuvent être consultés depuis le profil complet.

---

# CHAPITRE 45 — RÈGLES ABSOLUES

Les rôles doivent toujours :

✓ être clairement définis ;

✓ être traçables ;

✓ être évolutifs ;

✓ respecter la progression non régressive ;

✓ être compatibles avec les workflows.

Il est interdit :

❌ de créer un rôle hors référentiel ;

❌ d'attribuer un rôle sans respecter le processus prévu ;

❌ de partager un rôle entre plusieurs personnes ;

❌ de rétrograder automatiquement un utilisateur.

---

# CHAPITRE 46 — OBJECTIF FINAL

Le référentiel des rôles garantit que chaque utilisateur de LAWIM dispose d'une identité professionnelle claire, d'un niveau de responsabilité adapté et d'un parcours d'évolution cohérent.

Les rôles constituent la base des permissions, des dashboards, des workflows et de la confiance au sein de la plateforme.

---

# FIN DE LA PARTIE 3

# LAWIM

# 08-ROLE-REFERENCE.md

# PARTIE 4

# Permissions et contrôle d'accès

Version 1.0

---

# CHAPITRE 47 — PRINCIPE FONDAMENTAL

Les permissions déterminent les actions autorisées dans LAWIM.

Le rôle identifie l'utilisateur.

Les permissions déterminent ce qu'il peut faire.

Les permissions sont indépendantes des rôles, mais sont généralement accordées en fonction de ceux-ci.

---

# CHAPITRE 48 — NIVEAUX DE PERMISSION

LAWIM distingue cinq niveaux.

## Niveau 1

Lecture

L'utilisateur peut consulter.

---

## Niveau 2

Création

L'utilisateur peut créer.

---

## Niveau 3

Modification

L'utilisateur peut modifier les éléments dont il est responsable.

---

## Niveau 4

Validation

L'utilisateur peut approuver ou refuser certaines opérations.

---

## Niveau 5

Administration

L'utilisateur peut administrer le système ou une organisation.

---

# CHAPITRE 49 — DOMAINES DE PERMISSION

Les permissions sont regroupées par domaine.

Exemples.

🏠 Biens

💬 Conversations

📂 Dossiers

📅 Visites

🛠 Services LAWIM

📄 Documents

🏢 Agences

👥 Utilisateurs

📊 Reporting

⚙ Administration

Chaque domaine possède son propre ensemble de permissions.

---

# CHAPITRE 50 — HÉRITAGE

Les permissions peuvent être héritées.

Exemple.

Le Responsable d'agence hérite des permissions de l'Agent.

L'Administrateur principal hérite des permissions de tous les administrateurs.

Les permissions supplémentaires ne retirent jamais automatiquement les permissions déjà acquises.

---

# CHAPITRE 51 — DÉLÉGATION

Certaines permissions peuvent être déléguées temporairement.

Exemples.

* validation d'une visite ;

* suivi d'un dossier ;

* gestion d'un bien.

Toute délégation possède :

* un délégant ;
* un délégataire ;
* une durée ;
* un périmètre ;
* une date de fin.

Toutes les délégations sont historisées.

---

# CHAPITRE 52 — LIMITES

Certaines permissions ne sont jamais délégables.

Exemples.

* Administrateur principal ;

* validation finale d'une agence ;

* création d'un membre LAWIM ;

* suppression définitive de données ;

* restauration d'archives.

Ces opérations restent réservées aux profils autorisés.

---

# CHAPITRE 53 — VALIDATIONS

Les opérations sensibles nécessitent une validation.

Exemples.

* création d'une agence ;

* validation d'un agent ;

* changement de rôle ;

* validation de documents officiels ;

* accès à certaines archives.

Le système identifie automatiquement l'autorité compétente.

---

# CHAPITRE 54 — MATRICE DE PERMISSIONS

LAWIM maintient une matrice officielle.

Exemple simplifié.

| Domaine                     | Demandeur | Propriétaire | Agent        | Responsable Agence | Admin LAWIM |
| --------------------------- | --------- | ------------ | ------------ | ------------------ | ----------- |
| Consulter un bien           | ✅         | ✅            | ✅            | ✅                  | ✅           |
| Publier un bien             | ❌         | ✅            | ✅            | ✅                  | ✅           |
| Modifier ses biens          | ❌         | ✅            | ✅            | ✅                  | ✅           |
| Modifier un bien d'un tiers | ❌         | ❌            | Selon mandat | Selon mandat       | ✅           |
| Créer une agence            | ❌         | Demande      | Demande      | ❌                  | Validation  |
| Valider une agence          | ❌         | ❌            | ❌            | ❌                  | ✅           |

La matrice complète constitue une annexe du présent document.

---

# CHAPITRE 55 — CONTEXTE

Certaines permissions dépendent du contexte.

Exemples.

Un Agent peut modifier :

✔ les biens qui lui sont confiés.

Mais jamais :

❌ les biens gérés par une autre agence.

Les permissions peuvent dépendre :

* du bien ;
* du dossier ;
* de l'organisation ;
* du workflow ;
* de la région.

---

# CHAPITRE 56 — CONTRÔLE D'ACCÈS

Avant chaque action.

LAWIM vérifie :

Utilisateur

↓

Rôle

↓

Permissions

↓

Organisation

↓

Contexte

↓

Workflow

↓

Décision

Toute décision d'accès doit être explicable.

---

# CHAPITRE 57 — SUSPENSION DES PERMISSIONS

Une permission peut être suspendue.

Exemples.

* document expiré ;

* mandat terminé ;

* compte suspendu ;

* contrôle en cours.

La suspension d'une permission ne modifie pas le rôle principal.

---

# CHAPITRE 58 — TRAÇABILITÉ

Toutes les opérations sensibles enregistrent :

* utilisateur ;

* rôle ;

* permission utilisée ;

* objet concerné ;

* date ;

* adresse IP (si disponible) ;

* appareil utilisé (si disponible).

Ces informations alimentent l'audit.

---

# CHAPITRE 59 — RÈGLES ABSOLUES

Les permissions doivent toujours :

✓ respecter les rôles ;

✓ respecter les workflows ;

✓ respecter les organisations ;

✓ être auditables ;

✓ être réversibles.

Il est interdit :

❌ d'accorder une permission hors référentiel ;

❌ de contourner les validations obligatoires ;

❌ de modifier directement les permissions en base sans procédure ;

❌ d'utiliser un compte partagé.

---

# CHAPITRE 60 — OBJECTIF FINAL

Le système de permissions garantit que chaque utilisateur peut accomplir uniquement les actions correspondant à ses responsabilités, à son niveau de confiance et au contexte dans lequel il intervient.

Il protège les utilisateurs, les biens, les dossiers et les données de LAWIM tout en offrant la souplesse nécessaire aux organisations, aux agences et à l'équipe LAWIM.

---

# FIN DE LA PARTIE 4


# LAWIM

# 08-ROLE-REFERENCE.md

# PARTIE 5

# Trust Framework, vérifications et badges

Version 1.0

---

# CHAPITRE 61 — PRINCIPE FONDAMENTAL

LAWIM repose sur la confiance.

La confiance ne dépend pas uniquement du rôle d'un utilisateur.

Elle repose sur :

* son identité ;
* ses documents ;
* son historique ;
* son comportement ;
* ses validations ;
* son ancienneté.

Le Trust Framework permet d'évaluer et de renforcer cette confiance.

---

# CHAPITRE 62 — TRUST SCORE

Chaque utilisateur possède un Trust Score.

Le Trust Score est calculé automatiquement.

Il est utilisé notamment pour :

* améliorer le matching ;
* prioriser certains traitements ;
* renforcer la confiance entre utilisateurs ;
* guider LAWIM AI.

Le Trust Score n'est jamais utilisé comme seul critère de décision.

---

# CHAPITRE 63 — NIVEAUX DE CONFIANCE

LAWIM distingue plusieurs niveaux.

🔴 Niveau 1

Compte nouvellement créé.

---

🟠 Niveau 2

Téléphone vérifié.

---

🟡 Niveau 3

Identité vérifiée.

---

🟢 Niveau 4

Documents professionnels validés.

---

🔵 Niveau 5

Professionnel ou partenaire vérifié.

---

⭐ Niveau 6

Compte de référence reconnu par LAWIM.

Le calcul détaillé du Trust Score reste interne et peut évoluer sans modifier ce référentiel.

---

# CHAPITRE 64 — BADGES

Les badges permettent d'afficher immédiatement les principales validations.

Exemples :

📱 Téléphone vérifié

📧 E-mail vérifié

🪪 Identité vérifiée

🏠 Propriétaire vérifié

🏢 Agence vérifiée

🤝 Partenaire LAWIM

⭐ Professionnel vérifié

Les badges sont visibles :

* sur le profil ;
* dans les conversations ;
* dans certaines recherches ;
* dans les dashboards.

---

# CHAPITRE 65 — DOCUMENTS DE VÉRIFICATION

Selon le rôle demandé.

LAWIM peut exiger différents justificatifs.

Exemples.

Pour un propriétaire :

* titre foncier ;
* acte de vente ;
* attestation de propriété ;
* mandat.

---

Pour une agence :

* CNI du responsable ;
* RCCM (si applicable) ;
* numéro contribuable (si applicable) ;
* autorisation d'exercice (si applicable) ;
* justificatif d'adresse professionnelle.

---

Pour un partenaire :

Selon la profession.

Les exigences sont définies dans le catalogue des partenaires.

---

# CHAPITRE 66 — VALIDATION HUMAINE

Certaines validations ne peuvent être réalisées automatiquement.

Exemples :

* création d'une agence ;
* validation d'un agent ;
* validation d'un partenaire ;
* validation d'un propriétaire vérifié.

Ces validations sont effectuées par des membres habilités de l'équipe LAWIM.

LAWIM AI peut assister le contrôle mais ne prend jamais seul la décision finale.

---

# CHAPITRE 67 — CONTRÔLES PÉRIODIQUES

Certaines validations peuvent être réexaminées.

Exemples :

* document expiré ;
* mandat arrivé à échéance ;
* autorisation professionnelle expirée.

LAWIM notifie l'utilisateur avant l'expiration afin qu'il puisse renouveler ses documents.

---

# CHAPITRE 68 — SUSPICION ET FRAUDE

Lorsqu'une anomalie est détectée.

LAWIM peut :

* demander des justificatifs complémentaires ;
* suspendre certaines permissions ;
* limiter certaines fonctionnalités ;
* ouvrir un contrôle interne.

Toute décision est :

* motivée ;
* historisée ;
* réversible.

---

# CHAPITRE 69 — VISIBILITÉ

Toutes les informations ne sont pas publiques.

Les utilisateurs voient uniquement :

* les badges ;
* le niveau de vérification autorisé ;
* les informations rendues publiques par la plateforme.

Les documents d'identité et les justificatifs restent strictement confidentiels.

---

# CHAPITRE 70 — ÉVALUATIONS

Après certains services.

Les utilisateurs peuvent évaluer :

* la ponctualité ;
* la qualité du service ;
* la communication ;
* le professionnalisme.

Les évaluations participent à la réputation de l'utilisateur mais ne modifient jamais directement son rôle.

Des mécanismes de détection des abus doivent empêcher les évaluations frauduleuses.

---

# CHAPITRE 71 — DROIT DE CONTESTATION

Tout utilisateur peut demander la révision :

* d'un refus de validation ;
* d'une suspension ;
* d'un badge retiré.

La demande est examinée par un membre habilité de LAWIM.

Toutes les décisions sont historisées.

---

# CHAPITRE 72 — TRUST FRAMEWORK ET IA

LAWIM AI utilise le Trust Framework comme un indicateur parmi d'autres.

Il ne doit jamais :

* discriminer un utilisateur ;
* prendre seul une décision de suspension ;
* retirer un rôle ;
* supprimer un badge.

Les décisions importantes restent sous contrôle humain.

---

# CHAPITRE 73 — RÈGLES ABSOLUES

Le Trust Framework doit toujours :

✓ protéger les utilisateurs ;

✓ renforcer la confiance ;

✓ rester transparent dans ses principes ;

✓ protéger les données personnelles ;

✓ respecter les lois en vigueur.

Il est interdit :

❌ d'afficher publiquement les documents d'identité ;

❌ de modifier manuellement un Trust Score sans justification ;

❌ d'utiliser le Trust Score comme seul critère de refus d'un service ;

❌ de retirer un badge sans historique.

---

# CHAPITRE 74 — OBJECTIF FINAL

Le Trust Framework permet de créer un environnement où les utilisateurs, les professionnels, les agences et les partenaires peuvent interagir avec un niveau élevé de confiance.

Il renforce la crédibilité de LAWIM, améliore la qualité des échanges et sécurise les transactions et les services proposés par la plateforme.

---

# FIN DE LA PARTIE 5

# LAWIM

# 08-ROLE-REFERENCE.md

# PARTIE 6

# Organisations, agences et structures

Version 1.0

---

# CHAPITRE 75 — PRINCIPE FONDAMENTAL

LAWIM distingue deux catégories d'acteurs :

* les personnes physiques ;
* les organisations.

Une organisation regroupe plusieurs utilisateurs autour d'une activité commune.

Les organisations disposent de leurs propres droits, paramètres, statistiques et tableaux de bord.

---

# CHAPITRE 76 — TYPES D'ORGANISATIONS

LAWIM reconnaît notamment les organisations suivantes :

🏢 Agence immobilière

🏗 Promoteur immobilier

🏦 Banque partenaire

⚖ Étude notariale

📐 Cabinet de géomètre

📸 Prestataire de services

🏛 Administration publique

🏢 LAWIM

Cette liste peut évoluer sans modifier l'architecture.

---

# CHAPITRE 77 — STRUCTURE D'UNE ORGANISATION

Chaque organisation possède :

* un identifiant unique ;
* une raison sociale ;
* un nom commercial (optionnel) ;
* un responsable principal ;
* un ou plusieurs administrateurs ;
* des membres ;
* une adresse ;
* une géolocalisation ;
* un niveau de confiance ;
* des documents officiels ;
* un tableau de bord dédié.

---

# CHAPITRE 78 — CRÉATION D'UNE ORGANISATION

La création suit le workflow suivant.

```text
Demande

↓

Saisie des informations

↓

Téléversement des justificatifs

↓

Contrôle automatique

↓

Contrôle LAWIM

↓

Validation

↓

Organisation active
```

La création d'une organisation ne devient jamais effective sans validation lorsqu'elle nécessite des justificatifs réglementaires.

---

# CHAPITRE 79 — VALIDATION D'UNE AGENCE

Une agence immobilière doit fournir au minimum :

* CNI du responsable ;
* numéro de téléphone vérifié ;
* adresse e-mail ;
* adresse physique.

Selon son statut juridique, LAWIM peut également demander :

* RCCM ;
* numéro contribuable ;
* patente ou autorisation d'exercice ;
* logo ;
* justificatif de siège social.

Une agence ne devient **Agence vérifiée** qu'après validation.

---

# CHAPITRE 80 — COMPOSITION D'UNE AGENCE

Une agence comprend :

👤 Responsable d'agence

👥 Administrateurs d'agence

👨‍💼 Agents immobiliers

🧑‍💼 Collaborateurs éventuels

Le responsable peut inviter de nouveaux membres.

Les validations restent soumises aux règles définies dans ce référentiel.

---

# CHAPITRE 81 — EFFECTIF MINIMUM

Une agence peut être créée avec son responsable uniquement.

Toutefois, pour bénéficier du statut d'**Agence pleinement opérationnelle**, LAWIM recommande un minimum de trois agents actifs.

Certains services avancés peuvent être réservés aux agences atteignant ce seuil.

Cette règle reste paramétrable afin de s'adapter aux réalités du marché camerounais.

---

# CHAPITRE 82 — INVITATION DES MEMBRES

Les nouveaux membres rejoignent une organisation par invitation.

Workflow.

```text
Invitation

↓

Lien sécurisé

↓

Création du compte

↓

Téléphone vérifié

↓

Documents requis

↓

Validation

↓

Membre actif
```

Chaque membre possède son propre compte.

Les comptes partagés sont interdits.

---

# CHAPITRE 83 — ÉQUIPE LAWIM

LAWIM est également une organisation.

Elle comprend notamment :

👑 Administrateur principal

🛡 Administrateurs

📋 Responsables opérationnels

🤝 Conseillers

⚖ Médiateurs

🎧 Support

🤖 LAWIM AI

Chaque membre possède des responsabilités clairement définies.

---

# CHAPITRE 84 — ORGANIGRAMME

Chaque organisation dispose d'un organigramme.

Le Dashboard permet notamment de visualiser :

* les responsables ;
* les administrateurs ;
* les agents ;
* les collaborateurs.

Les responsabilités sont clairement identifiées.

---

# CHAPITRE 85 — DÉPART D'UN MEMBRE

Lorsqu'un membre quitte une organisation.

LAWIM :

* retire les permissions liées à l'organisation ;
* conserve son historique personnel ;
* conserve les traces d'audit ;
* transfère les dossiers ouverts selon les règles définies.

Le compte utilisateur reste actif.

---

# CHAPITRE 86 — CHANGEMENT DE RESPONSABLE

Le changement de responsable suit un processus sécurisé.

Il comprend :

* désignation du nouveau responsable ;
* validation LAWIM si nécessaire ;
* transfert des responsabilités ;
* conservation de l'historique.

Toutes les opérations sont historisées.

---

# CHAPITRE 87 — DISSOLUTION D'UNE ORGANISATION

Une organisation peut être :

* suspendue ;
* dissoute ;
* fusionnée avec une autre.

Avant toute dissolution.

LAWIM vérifie :

* les dossiers ouverts ;
* les biens gérés ;
* les services en cours ;
* les paiements ;
* les obligations légales.

Les données sont ensuite archivées conformément aux règles de conservation.

---

# CHAPITRE 88 — RÈGLES ABSOLUES

Les organisations doivent toujours :

✓ disposer d'un responsable identifié ;

✓ utiliser des comptes individuels ;

✓ conserver un historique complet ;

✓ respecter les workflows ;

✓ respecter les validations prévues.

Il est interdit :

❌ de partager un compte entre plusieurs collaborateurs ;

❌ de supprimer une organisation sans procédure officielle ;

❌ de modifier les responsabilités sans historisation ;

❌ de créer une organisation hors référentiel.

---

# CHAPITRE 89 — OBJECTIF FINAL

Le modèle d'organisation de LAWIM permet de gérer durablement aussi bien les agences immobilières que les partenaires, les entreprises et l'équipe LAWIM.

Il garantit une gouvernance claire, une traçabilité complète et une évolution harmonieuse de la plateforme.

---

# FIN DE LA PARTIE 6
# LAWIM

# 08-ROLE-REFERENCE.md

# PARTIE 7

# Gouvernance des rôles et délégation des responsabilités

Version 1.0

---

# CHAPITRE 90 — PRINCIPE FONDAMENTAL

Les rôles, permissions et responsabilités ne peuvent être attribués que par une autorité compétente.

Chaque changement doit être :

* autorisé ;
* tracé ;
* justifié ;
* réversible lorsque cela est applicable.

Aucun utilisateur ne peut modifier lui-même son propre rôle.

---

# CHAPITRE 91 — HIÉRARCHIE DES AUTORITÉS

LAWIM applique une hiérarchie stricte.

```text
Administrateur principal LAWIM

        │

Administrateur LAWIM

        │

Responsable opérationnel

        │

Conseiller / Médiateur

        │

Responsable d'agence

        │

Administrateur d'agence

        │

Agent immobilier

        │

Propriétaire / Détenteur

        │

Demandeur
```

Chaque niveau possède un périmètre d'action limité.

---

# CHAPITRE 92 — ATTRIBUTION DES RÔLES

Les rôles peuvent être attribués :

* automatiquement selon les workflows ;
* après validation humaine ;
* par décision administrative.

Chaque attribution est historisée.

Elle contient :

* auteur ;
* date ;
* ancien rôle ;
* nouveau rôle ;
* justification.

---

# CHAPITRE 93 — DÉLÉGATION

Certaines responsabilités peuvent être déléguées.

Exemples :

* validation de visites ;
* suivi d'un dossier ;
* gestion d'un portefeuille de biens ;
* remplacement temporaire.

Toute délégation précise :

* le délégant ;
* le délégataire ;
* la durée ;
* les permissions accordées ;
* les limites.

À expiration, les permissions sont retirées automatiquement.

---

# CHAPITRE 94 — DOUBLE VALIDATION

Certaines opérations nécessitent deux validations indépendantes.

Exemples :

* création d'un administrateur LAWIM ;
* création d'un administrateur principal ;
* validation d'une agence sensible ;
* suppression définitive d'une organisation ;
* restauration complète d'une sauvegarde.

Le principe des "quatre yeux" est appliqué :

Une personne propose.

Une autre valide.

---

# CHAPITRE 95 — SÉPARATION DES RESPONSABILITÉS

Aucun utilisateur ne doit pouvoir :

* créer ;
* valider ;
* contrôler ;

la même opération seul lorsque celle-ci présente un risque élevé.

Exemple.

Un administrateur peut créer un compte interne.

Un second administrateur doit le valider.

---

# CHAPITRE 96 — ABSENCE ET INTÉRIM

Lorsqu'un responsable est absent.

Ses responsabilités peuvent être transférées temporairement.

Conditions :

* durée définie ;
* périmètre limité ;
* historisation ;
* révocation automatique à échéance.

Aucune délégation permanente implicite n'est autorisée.

---

# CHAPITRE 97 — RÉVOCATION

Une responsabilité peut être retirée.

Motifs possibles :

* départ ;
* suspension ;
* fraude ;
* erreur d'attribution ;
* réorganisation.

La révocation :

* est historisée ;
* conserve les traces des actions passées ;
* ne supprime jamais les audits.

---

# CHAPITRE 98 — CONTRÔLE PÉRIODIQUE

LAWIM réalise régulièrement une revue des rôles.

Objectifs :

* détecter les comptes inactifs ;
* vérifier les délégations expirées ;
* contrôler les droits élevés ;
* supprimer les accès devenus inutiles.

Cette revue peut être automatisée avec validation humaine.

---

# CHAPITRE 99 — GOUVERNANCE DES ORGANISATIONS

Chaque organisation doit toujours disposer :

* d'un responsable identifié ;
* d'au moins un administrateur actif (si nécessaire) ;
* d'une liste des membres à jour.

Lorsqu'une organisation ne possède plus de responsable actif.

LAWIM ouvre automatiquement un workflow de régularisation.

---

# CHAPITRE 100 — COMPTES À PRIVILÈGES

Les comptes disposant de privilèges élevés sont soumis à des règles renforcées.

Exemples :

* authentification multifacteur obligatoire ;
* journalisation complète ;
* revue périodique des accès ;
* notifications en cas d'action sensible.

Ces comptes doivent être utilisés uniquement pour les tâches administratives.

---

# CHAPITRE 101 — DÉLÉGATION À LAWIM AI

LAWIM AI peut assister les utilisateurs.

Exemples :

* préparer une validation ;
* signaler une anomalie ;
* recommander une décision ;
* détecter une incohérence.

LAWIM AI ne peut jamais :

* attribuer un rôle ;
* retirer un rôle ;
* créer une organisation ;
* suspendre définitivement un utilisateur.

Les décisions finales reviennent toujours à un humain habilité.

---

# CHAPITRE 102 — AUDIT

Toutes les opérations de gouvernance sont enregistrées.

Le journal contient notamment :

* utilisateur concerné ;
* auteur de l'action ;
* organisation ;
* rôle ;
* permission ;
* justification ;
* date et heure ;
* résultat.

Les journaux sont conservés conformément à la politique d'archivage de LAWIM.

---

# CHAPITRE 103 — RÈGLES ABSOLUES

La gouvernance des rôles doit toujours :

✓ respecter la hiérarchie ;

✓ garantir la séparation des responsabilités ;

✓ empêcher l'escalade non autorisée des privilèges ;

✓ conserver une traçabilité complète ;

✓ permettre les contrôles et audits.

Il est interdit :

❌ de s'attribuer un rôle supérieur ;

❌ de contourner une double validation obligatoire ;

❌ d'utiliser un compte administrateur partagé ;

❌ de modifier directement les rôles en base de données ;

❌ d'accorder des privilèges permanents lorsqu'une délégation temporaire suffit.

---

# CHAPITRE 104 — OBJECTIF FINAL

La gouvernance des rôles garantit que chaque responsabilité attribuée dans LAWIM est légitime, contrôlée et traçable.

Elle protège la plateforme contre les erreurs, les abus de privilèges et les fraudes, tout en permettant une délégation souple et adaptée aux besoins opérationnels des agences, des partenaires et de l'équipe LAWIM.

---

# FIN DE LA PARTIE 7

# LAWIM

# 08-ROLE-REFERENCE.md

# PARTIE 8

# Role Engine, audit et règles absolues

Version 1.0

---

# CHAPITRE 105 — PRINCIPE FONDAMENTAL

Le système des rôles de LAWIM est piloté par un moteur unique :

**Role Engine**

Le Role Engine est responsable de toute évolution liée :

* aux utilisateurs ;
* aux organisations ;
* aux rôles ;
* aux permissions ;
* aux badges ;
* au Trust Framework.

Aucun changement de rôle ne doit être réalisé directement par le code applicatif.

---

# CHAPITRE 106 — RESPONSABILITÉS DU ROLE ENGINE

Le Role Engine assure notamment :

* création des identités ;
* attribution des rôles ;
* évolution automatique des rôles ;
* gestion des rôles secondaires ;
* calcul des permissions ;
* contrôle des délégations ;
* calcul du Trust Score ;
* attribution des badges ;
* suspension des permissions ;
* historique complet.

Toutes les décisions passent par ce moteur.

---

# CHAPITRE 107 — SOURCES D'ÉVOLUTION

Le Role Engine peut recevoir des événements provenant de plusieurs moteurs.

Exemples.

Workflow Engine

↓

Publication d'un bien

↓

Proposition de passage :

Demandeur

↓

Propriétaire

---

Organisation Engine

↓

Création d'une agence

↓

Proposition :

Responsable d'agence

---

Trust Framework

↓

Identité validée

↓

Badge Identité vérifiée

---

Notification Engine

↓

Document expiré

↓

Suspension d'une permission

---

LAWIM AI

↓

Suggestion

↓

Validation humaine

↓

Évolution éventuelle

---

# CHAPITRE 108 — DÉCISION

Le Role Engine ne modifie jamais directement un rôle.

Il applique systématiquement le processus suivant.

```text
Événement

↓

Analyse

↓

Contrôle des permissions

↓

Contrôle des documents

↓

Contrôle du Trust Score

↓

Validation éventuelle

↓

Décision

↓

Historisation

↓

Notification

↓

Mise à jour du Dashboard
```

Toutes les décisions doivent être explicables.

---

# CHAPITRE 109 — MOTEURS CONSOMMATEURS

Les autres moteurs utilisent les décisions du Role Engine.

Exemples.

Dashboard Engine

↓

Affichage du Dashboard.

---

Matching Engine

↓

Priorités.

---

Workflow Engine

↓

Étapes autorisées.

---

Notification Engine

↓

Notifications autorisées.

---

Reporting Engine

↓

Statistiques.

---

Storage Manager

↓

Droits d'accès aux documents.

Le Role Engine devient la référence unique des identités.

---

# CHAPITRE 110 — AUDIT

Chaque évolution est enregistrée.

Le journal contient notamment :

* utilisateur ;
* organisation ;
* ancien rôle ;
* nouveau rôle ;
* permissions modifiées ;
* badges ;
* Trust Score ;
* auteur ;
* origine de la décision ;
* justification ;
* date ;
* heure.

Les audits sont conservés conformément au référentiel de stockage.

---

# CHAPITRE 111 — HISTORIQUE

Le système conserve l'historique complet.

Exemple.

```text
01/02/2027

Création

↓

Demandeur

-----------------

15/02/2027

Publication d'un bien

↓

Propriétaire

-----------------

20/04/2027

Validation professionnelle

↓

Agent immobilier

-----------------

03/09/2027

Création agence

↓

Responsable d'agence
```

Aucun historique n'est perdu.

---

# CHAPITRE 112 — RESTAURATION

En cas d'erreur.

Une décision peut être annulée.

La restauration :

* conserve les traces ;
* crée un nouvel événement ;
* ne supprime jamais l'audit.

Toutes les restaurations sont historisées.

---

# CHAPITRE 113 — COMPATIBILITÉ

Le Role Engine doit rester compatible avec :

* 00-CONSTITUTION.md ;
* 03-CONVERSATION-REFERENCE.md ;
* 04-MATCHING-REFERENCE.md ;
* 05-WORKFLOW-REFERENCE.md ;
* 06-DATABASE-REFERENCE.md ;
* 07-DASHBOARD-REFERENCE.md ;
* 09-GEOLOCATION-REFERENCE.md ;
* 10-NOTIFICATION-REFERENCE.md ;
* 11-REPORTING-REFERENCE.md ;
* 14-STORAGE-REFERENCE.md.

En cas de conflit.

La Constitution prévaut toujours.

---

# CHAPITRE 114 — RÈGLES ABSOLUES

Le Role Engine doit toujours :

✓ garantir une identité unique ;

✓ empêcher les régressions automatiques ;

✓ respecter les workflows ;

✓ respecter les organisations ;

✓ protéger les documents ;

✓ assurer une traçabilité complète ;

✓ permettre les audits ;

✓ notifier les changements importants.

Il est interdit :

❌ de modifier directement les rôles en base de données ;

❌ d'attribuer un rôle sans événement déclencheur ;

❌ de contourner les validations obligatoires ;

❌ de supprimer un historique ;

❌ de créer un rôle hors référentiel.

---

# CHAPITRE 115 — OBJECTIF FINAL

Le Role Engine constitue le cœur du système d'identité de LAWIM.

Il garantit que chaque utilisateur, chaque organisation et chaque partenaire dispose en permanence :

* du bon rôle ;
* des bonnes permissions ;
* des bons badges ;
* du bon niveau de confiance ;
* des bons accès.

Toutes les décisions sont cohérentes, traçables et synchronisées avec l'ensemble des moteurs de la plateforme.

---

# FIN DE LA PARTIE 8

La partie suivante complète la gouvernance des rôles, des permissions, des badges et de l'archivage.

---

# CHAPITRE 118 — ADMINISTRATION DES RÔLES

Les rôles peuvent être :

* attribués ;
* retirés ;
* suspendus ;
* restaurés.

Toute opération nécessite :

* une autorité compétente ;
* une justification ;
* une trace dans l'audit.

Les changements sont immédiatement répercutés sur :

* les permissions ;
* le Dashboard ;
* les Workflows ;
* le Matching ;
* les Notifications.

---

# CHAPITRE 119 — ADMINISTRATION DES PERMISSIONS

Les permissions sont administrées exclusivement par le Role Engine.

Les administrateurs peuvent :

* accorder une permission exceptionnelle ;
* suspendre une permission ;
* déléguer une permission ;
* retirer une délégation.

Toutes les permissions exceptionnelles doivent comporter :

* un motif ;
* une date de début ;
* une date de fin (si applicable).

---

# CHAPITRE 120 — GESTION DES BADGES

Les badges peuvent être :

* attribués ;
* suspendus ;
* retirés.

Ils ne peuvent jamais être créés librement.

Tous les badges doivent appartenir au catalogue officiel de LAWIM.

La suppression d'un badge est historisée.

---

# CHAPITRE 121 — GESTION DU TRUST FRAMEWORK

Le calcul du Trust Score est automatisé.

Les administrateurs peuvent :

* consulter les éléments ayant conduit au score ;
* déclencher une réévaluation ;
* corriger une erreur de données.

Ils ne peuvent jamais modifier directement le score sans justification enregistrée.

---

# CHAPITRE 122 — CONFORMITÉ

Le système d'identité doit respecter :

* la législation camerounaise applicable ;
* les obligations de protection des données personnelles ;
* les politiques internes de LAWIM ;
* les règles de conservation des documents.

Les données d'identité ne sont accessibles qu'aux personnes autorisées.

---

# CHAPITRE 123 — ARCHIVAGE

Lorsqu'un compte est :

* désactivé ;
* fusionné ;
* clôturé ;
* suspendu durablement.

Les informations sont archivées conformément au référentiel de stockage.

Les archives conservent notamment :

* l'identité ;
* les rôles ;
* les permissions ;
* les badges ;
* le Trust Score ;
* l'historique des évolutions.

Les durées de conservation sont définies dans **14-STORAGE-REFERENCE.md**.

---

# CHAPITRE 124 — AUDITS

LAWIM peut réaliser des audits internes afin de vérifier :

* la cohérence des rôles ;
* les permissions actives ;
* les délégations en cours ;
* les comptes inactifs ;
* les comptes à privilèges ;
* les organisations.

Les rapports d'audit sont conservés selon la politique d'archivage.

---

# CHAPITRE 125 — IMPORT / EXPORT

Selon les permissions.

Le système peut permettre :

* l'export de certaines informations d'identité ;
* l'import contrôlé de comptes provenant d'une migration.

Toute opération d'import est validée avant intégration.

---

# CHAPITRE 126 — ÉVOLUTIVITÉ

Le modèle d'identité de LAWIM doit permettre l'ajout futur :

* de nouveaux rôles ;
* de nouveaux partenaires ;
* de nouveaux badges ;
* de nouveaux niveaux de confiance ;
* de nouveaux types d'organisation.

Ces évolutions ne doivent jamais remettre en cause les identités existantes.

---

# CHAPITRE 127 — RÈGLES ABSOLUES

Le système d'identité doit toujours :

✓ garantir un compte unique par personne ;

✓ conserver une progression non régressive des rôles ;

✓ séparer clairement rôles, permissions, badges et Trust Score ;

✓ assurer une traçabilité complète ;

✓ protéger les données personnelles ;

✓ permettre des audits complets ;

✓ respecter les règles d'archivage.

Il est interdit :

❌ de créer un rôle ou un badge hors référentiel ;

❌ de modifier directement les rôles en base de données ;

❌ de supprimer définitivement un historique d'identité ;

❌ de partager un compte entre plusieurs personnes ;

❌ de modifier le Trust Score sans justification.

---

# CHAPITRE 128 — OBJECTIF FINAL

Le système d'identité de LAWIM constitue le socle de confiance de la plateforme.

Il garantit qu'à tout moment :

* chaque personne est correctement identifiée ;
* chaque organisation est clairement représentée ;
* chaque utilisateur dispose des droits adaptés à ses responsabilités ;
* chaque décision est explicable, traçable et auditée.

Le présent référentiel doit permettre à LAWIM de croître sans remettre en cause la cohérence de son modèle d'identité.

---

# CHAPITRE 129 — COMPTES DE DÉMONSTRATION STANDARDISÉS

Les comptes de démonstration officiels suivent désormais une convention unique.

Ils peuvent se connecter avec :

* email ;
* username ;
* numéro WhatsApp.

Comptes officiels :

| Usage | Email | Username | Téléphone | Mot de passe |
| --- | --- | --- | --- | --- |
| Administrateur | `admin@lawim.app` | `admin` | `+237686822667` | `LAWIM@Demo2026µ` |
| Manager | `manager@lawim.app` | `manager` | `+237686822668` | `LAWIM@Demo2026µ` |
| Agent LAWIM | `agent@lawim.app` | `agent` | `+237686822669` | `LAWIM@Demo2026µ` |
| Utilisateur propriétaire | `owner@lawim.app` | `owner` | `+237686822670` | `LAWIM@Demo2026µ` |
| Investisseur / Banque | `investor@lawim.app` | `investor` | `+237686822671` | `LAWIM@Demo2026µ` |

---

# FIN DU DOCUMENT

Le présent **08-ROLE-REFERENCE.md** constitue la référence officielle pour la gestion des identités, des rôles, des organisations, des permissions, des badges et du Trust Framework de LAWIM.

Toute évolution future devra respecter les principes définis dans ce document et rester compatible avec les autres référentiels de la plateforme.

