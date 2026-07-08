# LAWIM

# 04-MATCHING-REFERENCE.md

# Référentiel officiel du moteur de matching

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le présent document définit les règles officielles du moteur de matching de LAWIM.

Il constitue la référence unique pour :

* le matching ;
* le rematching ;
* le classement des biens ;
* la génération des leads ;
* l'explication des scores ;
* la priorisation des propositions.

---

# CHAPITRE 2 — MISSION

Le moteur de matching a pour mission d'identifier les biens les plus pertinents pour un dossier donné, à un instant donné, selon les règles métiers officielles de LAWIM.

Il ne s'agit pas d'une simple recherche en base. Le moteur compare un besoin normalisé à des biens normalisés et produit un classement explicable.

---

# CHAPITRE 3 — RÉFÉRENCES OBLIGATOIRES

Le moteur de matching applique obligatoirement :

* 00-CONSTITUTION.md ;
* 01-GLOSSAIRE.md ;
* 02-PROPERTY-REFERENCE.md ;
* 02H-ATTRIBUTE-CATALOG.md ;
* 02I-PRICING-REFERENCE.md ;
* 03-CONVERSATION-REFERENCE.md ;
* 06-DATABASE-REFERENCE.md ;
* 09-GEOLOCATION-REFERENCE.md ;
* 11-REPORTING-REFERENCE.md ;
* 13-ARCHITECTURE-GOVERNANCE-REFERENCE.md.

Les séquences décisionnelles détaillées sont décrites dans **04-DECISION-ENGINE-REFERENCE.md**.

Le Decision Engine y est documenté comme sous-moteur officiel du Matching Engine.

Le nom historique `TSE` est un alias non normatif.

---

# CHAPITRE 4 — PRINCIPES FONDAMENTAUX

Le moteur respecte toujours les principes suivants :

* commencer dès que les champs critiques sont connus ;
* utiliser uniquement des données normalisées ;
* écarter les biens incompatibles ;
* conserver la traçabilité complète du calcul ;
* apprendre des décisions humaines validées ;
* rester explicable.

Le matching ne bloque jamais une conversation utile.

---

# CHAPITRE 5 — ENTRÉES DU MOTEUR

Le moteur exploite notamment :

* le type de bien ;
* la famille de bien ;
* l'opération recherchée ;
* le budget ;
* la ville ;
* le quartier ;
* les repères géographiques ;
* la disponibilité ;
* les caractéristiques obligatoires ;
* les caractéristiques recommandées ;
* l'historique du dossier ;
* les refus précédents ;
* la fraîcheur des données ;
* le niveau de confiance des acteurs.

---

# CHAPITRE 6 — FILTRE ÉLIMINATOIRE

Avant le calcul de score, le moteur retire tous les biens incompatibles.

Exemples :

* une demande de location ne reçoit pas une vente ;
* un besoin résidentiel ne reçoit pas un bien commercial ;
* un budget dépassé de manière manifeste peut être écarté ;
* un bien indisponible n'est pas proposé ;
* un attribut interdit par le référentiel du bien ne doit pas être demandé ni utilisé.

---

# CHAPITRE 7 — CALCUL DU SCORE

Le score de matching est calculé à partir de plusieurs familles de critères :

* compatibilité critique ;
* compatibilité fonctionnelle ;
* compatibilité géographique ;
* compatibilité de confort ;
* compatibilité préférentielle ;
* confiance de la donnée ;
* fraîcheur ;
* historique de réaction.

Chaque lead doit pouvoir être justifié par une décomposition lisible.

---

# CHAPITRE 8 — CLASSEMENT

Le moteur produit une liste ordonnée de propositions.

Le classement favorise :

* les biens les plus conformes ;
* les biens les plus fiables ;
* les biens les plus proches du besoin réel ;
* les biens les plus récents ou confirmés ;
* les biens capables d'aboutir à une mise en relation utile.

Le nombre de résultats ne prime jamais sur leur qualité.

---

# CHAPITRE 9 — REMATCHING

Le rematching est déclenché lorsque :

* le besoin est corrigé ;
* un budget change ;
* une ville ou un quartier change ;
* un nouveau bien est publié ;
* un bien devient indisponible ;
* un refus est enregistré ;
* une visite ou une négociation modifie le contexte.

Le rematching ne remet pas en cause l'historique. Il l'enrichit.

---

# CHAPITRE 10 — INTERACTIONS AVEC LES AUTRES MOTEURS

Le moteur de matching dépend notamment de :

* Conversation Engine pour la qualification ;
* Geo Engine pour la proximité ;
* Database Engine pour la persistance ;
* Notification Engine pour les alertes ;
* Dashboard Engine pour l'affichage ;
* Reporting Engine pour les KPI ;
* LAWIM AI pour la compréhension et les pondérations.

Aucun moteur ne peut contourner le matching pour fabriquer une proposition non validée.

---

# CHAPITRE 11 — LEADS ET MISE EN RELATION

Chaque proposition pertinente peut générer un lead.

Le lead est un artefact de matching, pas une transaction.

Il sert à :

* tracer la compatibilité ;
* suivre les décisions ;
* préparer une mise en relation ;
* conserver le contexte de score.

Le passage de lead à relation est gouverné par les workflows et le double consentement.

---

# CHAPITRE 12 — APPRENTISSAGE CONTRÔLÉ

Le moteur peut ajuster ses pondérations à partir des décisions réellement observées :

* acceptations ;
* refus ;
* visites ;
* transactions abouties ;
* retours utilisateurs ;
* retours partenaires.

Aucun ajustement automatique ne doit modifier seul une règle métier.

Toute évolution de pondération nécessite validation humaine et historisation.

---

# CHAPITRE 13 — EXPLICABILITÉ

Chaque résultat doit être justifiable en langage métier.

Exemple de justification :

* ville correcte ;
* quartier proche ;
* budget respecté ;
* surface compatible ;
* disponibilité immédiate ;
* meilleure confiance de la donnée.

Cette explicabilité est obligatoire pour les utilisateurs, les équipes internes et les audits.

---

# CHAPITRE 14 — RÈGLES ABSOLUES

Le moteur de matching doit toujours :

* respecter le référentiel des biens ;
* respecter le catalogue d'attributs ;
* ignorer les données non normalisées ;
* produire un score traçable ;
* rester compatible avec les autres moteurs ;
* conserver l'historique des décisions.

Il est interdit :

* de proposer un bien incompatible ;
* de calculer un score sans base traçable ;
* de contourner le moteur conversationnel ;
* d'écrire des pondérations non documentées ;
* de déclencher un rematching hors règle.

---

# CHAPITRE 15 — OBJECTIF FINAL

Le moteur de matching doit maximiser la pertinence des mises en relation, la satisfaction des parties et la probabilité de résolution d'un dossier immobilier, sans jamais sacrifier la traçabilité ni la conformité.

---

# CHAPITRE 16 — SUPPORT MULTILINGUE

Le moteur de matching doit être indépendant de la langue d'expression.

Il doit normaliser les synonymes, les variantes et les expressions locales via 30A-BUSINESS-DICTIONARY-REFERENCE.md et 30D-MULTILINGUAL-SEARCH-REFERENCE.md.

Le sens métier prime sur la langue de saisie.

---

# CHAPITRE 17 — MATCHING TRANSVERSAL LIME

Le moteur est désormais transversal et doit pouvoir servir plusieurs types de besoins, pas uniquement les biens immobiliers.

L'acronyme interne `LIME` désigne le **LAWIM Intelligent Matching Engine**.

Il doit pouvoir matcher notamment :

* utilisateur ↔ bien ;
* utilisateur ↔ photographe ;
* utilisateur ↔ architecte ;
* utilisateur ↔ notaire ;
* utilisateur ↔ banque / financement ;
* utilisateur ↔ artisan ;
* utilisateur ↔ diagnostiqueur ;
* utilisateur ↔ déménageur ;
* utilisateur ↔ autre partenaire.

Les critères de score minimaux sont :

* localisation ;
* disponibilité ;
* spécialité ;
* type de besoin ;
* langue ;
* prix ou budget ;
* notation ;
* délai ;
* compatibilité avec le projet.

Le moteur doit être exploitable via une API claire qui permet :

* d'exprimer un besoin ;
* de récupérer les meilleurs matchs ;
* d'expliquer pourquoi un match est proposé.

La recommandation doit rester explicite et non prescriptive :

* LAWIM accompagne et met en relation ;
* LAWIM ne décide jamais à la place de l'utilisateur ;
* LAWIM propose lorsqu'il y a une vraie pertinence ;
* si l'utilisateur exprime un besoin, LAWIM répond ;
* aucune action ne doit mener à une impasse.

Les réponses doivent donc exposer :

* le type de cible (`property` ou `partner`) ;
* les critères résolus ;
* les raisons lisibles ;
* un ordre de classement ;
* une explication métier lisible.

---

# CHAPITRE 18 — EXTENSION TRANSVERSALE RELEASE 08.1

La Release 08.1 a étendu le moteur de matching au-dela des biens immobiliers.

Le moteur peut maintenant servir de premiere couche de mise en relation pour:

* photographe;
* architecte;
* notaire;
* banque / financement;
* artisan;
* diagnostiqueur;
* demenageur;
* autre partenaire de projet.

Les criteres utilises pour ce matching transversal sont:

* localisation;
* disponibilite;
* specialite;
* type de besoin;
* langue;
* budget;
* notation;
* delai;
* compatibilite avec le projet.

Chaque proposition reste argumentee, utile et non bloquante.

---

# CHAPITRE 18 — FIN DU DOCUMENT

Le présent **04-MATCHING-REFERENCE.md** constitue le référentiel officiel du matching de LAWIM.
