# LAWIM_V2 - TICKET EXECUTION STANDARD V2

- Date: 2026-06-28
- Statut: READY_FOR_DG_ADOPTION
- Portee: tous les tickets futurs
- Reference de stabilisation: DG-0027
- Nature: standard operationnel unique pour l execution des tickets

## 0. Objet

Ce document fige la methode d execution de tous les tickets LAWIM_V2.

Il definit un enchainement unique, lisible et reproductible pour:

- preparer le contexte avant execution;
- securiser le ticket precedent;
- executer le ticket courant;
- produire un rapport standard;
- preparer la suite.

Ce standard est compatible avec la gouvernance existante, la Constitution, le Bootstrap Pack, le PCC et les historiques.

Il ne modifie aucune regle de gouvernance et n ajoute aucun moteur d execution. Il formalise seulement l ordre documentaire et operationnel.

## 1. Pre-vol Git

Avant toute action sur un ticket, l execution doit lire Git dans cet ordre exact:

1. `git status`
2. `git branch`
3. `git log --oneline -3`
4. `git tag --sort=-creatordate | head -3`

### 1.1 Lecture attendue

- `git status` controle l etat du depot.
- `git branch` confirme la branche active et detecte un eventuel etat detached.
- `git log --oneline -3` confirme le dernier historique utile.
- `git tag --sort=-creatordate | head -3` confirme les derniers marqueurs de livraison.

### 1.2 Criteres de blocage

L execution est bloquee immediatement si:

- le depot Git n est pas propre;
- la branche active est inconnue, inattendue ou detachee;
- l historique recent ne correspond pas au contexte du ticket;
- les derniers tags ne sont pas coherents avec la chaine de fermeture precedente;
- le ticket precedent n est pas securise avant demarrage du ticket courant.

En cas de blocage, aucune modification ne doit commencer avant une decision explicite ou une correction tracee.

## 2. Securisation du ticket precedent

Avant de demarrer un nouveau ticket, le ticket precedent doit etre securise dans l ordre officiel suivant:

1. `git add .`
2. `git commit`
3. `git tag`
4. `git push` si applicable
5. `git push --tags` si applicable

### 2.1 Regle operationnelle

- `git add .` collecte les livrables, traces et rapports autorises.
- `git commit` fige la livraison.
- `git tag` marque le point de reference de la livraison.
- `git push` est execute uniquement si un remote est configure et autorise.
- `git push --tags` est execute uniquement si le push distant est applicable.

### 2.2 Discipline de fermeture

La securisation du ticket precedent est une condition d entree du ticket suivant.

Si cette etape est incomplete, le ticket courant ne doit pas avancer.

## 3. Contrat d execution d un ticket

Chaque ticket doit etre pilote par un contrat d execution explicite et stable.

Le contrat doit contenir exactement les sections obligatoires suivantes, dans cet ordre:

1. Pre-vol Git
2. Securisation
3. Contrat du ticket
4. Contexte
5. Mission
6. Controles
7. Rapport
8. Preparation Git
9. Preparation du ticket suivant

### 3.1 Contenu minimal attendu

#### 3.1.1 Pre-vol Git

- etat Git;
- branche;
- historique recent;
- tags recents;
- blocages eventuels.

#### 3.1.2 Securisation

- trace de fermeture du ticket precedent;
- commit;
- tag;
- push si applicable;
- preuve que le ticket precedent est fige.

#### 3.1.3 Contrat du ticket

- identifiant du ticket;
- sprint de rattachement;
- owner ou role responsable;
- objectif;
- perimetre;
- dependances;
- livrables attendus;
- criteres d acceptation;
- risques connus;
- exclusions explicites.

#### 3.1.4 Contexte

- PCC pertinent;
- documents de reference;
- historiques utiles;
- rapport precedent;
- contraintes de gouvernance applicables.

#### 3.1.5 Mission

- travail a realiser;
- resultat attendu;
- niveau de reutilisation attendu;
- limite de perimetre;
- condition d arret si une decision de gouvernance est requise.

#### 3.1.6 Controles

- controles architecture;
- controles QA;
- controles security;
- controles PCC;
- controles Git;
- controles de dependances;
- controles de coherence documentaire.

#### 3.1.7 Rapport

- structure du rapport;
- emplacement du rapport;
- elements obligatoires du rapport;
- bloc YAML final normalise;
- regle de decision associee.

#### 3.1.8 Preparation Git

- chemins a ajouter;
- message de commit propose;
- tag recommande;
- etat de preparation au push;
- preuve de fermeture locale.

#### 3.1.9 Preparation du ticket suivant

- contexte de releve;
- dependances ouvertes;
- point d attention;
- prochain ticket attendu;
- eventuelle action d attente.

### 3.2 Regle de stabilite

Les noms des sections sont fixes.

Un moteur futur peut les lire comme des etapes normales sans que la gouvernance ait besoin de changer.

## 4. Structure obligatoire des rapports

Tous les rapports produits sous ce standard doivent contenir, dans cet ordre:

1. Resume narratif
2. Controles realises
3. Decisions
4. Risques
5. Recommandations

### 4.1 Regle de redaction

- le resume narratif doit expliquer ce qui a ete fait et pourquoi;
- les controles realises doivent lister les verifications effectuees;
- les decisions doivent indiquer les arbitrages ou constats utiles;
- les risques doivent distinguer les risques bloquants des risques residuels;
- les recommandations doivent proposer la suite operationnelle.

### 4.2 Bloc YAML final normalise

Chaque rapport doit se terminer par un bloc YAML strictement normalise avec les champs suivants:

```yaml
ticket:
status:
git:
qa:
security:
architecture:
pcc:
blocking_risk:
next_ticket:
decision_required:
```

### 4.3 Regles YAML

- les cles YAML doivent rester exactement celles listees ci-dessus;
- aucune cle supplementaire ne doit remplacer une cle obligatoire;
- les valeurs doivent rester simples, stables et lisibles par un outil;
- les statuts doivent rester coherents avec le vocabulaire officiel du projet.

## 5. Politique de blocage

Un ticket doit s arreter immediatement si l un des cas suivants est constate:

- depot Git non propre;
- revue QA en echec;
- revue security en echec;
- modification de gouvernance;
- dependance non satisfaite;
- risque bloquant.

### 5.1 Regle d arret

En cas de blocage:

- aucune extension de perimetre ne doit etre tentee;
- aucune fermeture fictive ne doit etre produite;
- aucun changement de gouvernance ne doit etre implique;
- le blocage doit etre trace dans le rapport et, si necessaire, dans le PCC.

## 6. Compatibilite LAWIM Orchestrator

Ce standard est concu pour etre consommable par un futur LAWIM Orchestrator ou Workflow Engine sans exiger leur implementation aujourd hui.

### 6.1 Principes de compatibilite

- sections stables;
- ordre stable;
- vocabulaire stable;
- bloc YAML final normalise;
- decision explicite;
- aucune dependance a une interpretation libre.

### 6.2 Limites

Ce standard ne:

- cree pas de nouveau service;
- ne remplace pas la gouvernance;
- ne redefinit pas le workflow officiel;
- n impose pas une implementation technique immediate;
- ne modifie ni le Bootstrap Pack ni la Constitution.

### 6.3 Lecture machine future

Un moteur futur pourra:

- detecter le pre-vol;
- identifier le blocage;
- lire la mission;
- valider les controles;
- extraire la decision;
- interpreter le YAML final;
- preparer la suite.

## 7. Rappel de conformite

Ce standard est aligne avec:

- DG-0027 pour la reprise normale et la methodologie stabilisee;
- le PCC comme reference de coordination;
- `49-TICKET-EXECUTOR-REFERENCE.md` pour le role d entree unique;
- `33-CODEX-IMPLEMENTATION-RULES.md` pour la discipline d execution;
- `38-GIT-STRATEGY.md` pour la trajectoire Git;
- `11-REPORTING-REFERENCE.md` pour la logique de rapport;
- `templates/ticket-execution-report-template.md` pour la structure documentaire.

## 8. Objectif final

Ce standard garantit que chaque ticket futur est execute de maniere controlee, tracee, reutilisable et machine-readable, sans confusion entre execution, gouvernance et implementation future.

# FIN DU DOCUMENT
