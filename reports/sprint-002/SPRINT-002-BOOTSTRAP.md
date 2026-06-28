# Sprint 002 Bootstrap

- Date: 2026-06-28
- Scope: Sprint 002 preparation only
- Status: PREPARED

## 1. Contexte herite du Sprint 001

- Sprint 001 est officiellement cloture.
- Le socle herite couvre Infrastructure, Docker, Docker Compose, environnements, Nginx, OVH, Secrets, CI/CD, Logging et Monitoring.
- Aucun ticket Sprint 002 n'a ete ouvert.
- La cloture du Sprint 001 est en statut GO AVEC RESERVES, avec architecture, QA et security en PASS.
- Le risque bloquant reste false dans le rapport de cloture.

## 2. Gouvernance applicable

- La documentation officielle prime sur toute autre source.
- Un ticket ne couvre qu'une responsabilite principale.
- Un sprint ne peut etre valide que si les tickets sont conformes au plan directeur.
- Une IA ne peut pas modifier seule les regles fondatrices.
- Toute decision sensible doit etre explicite, tracable et relue.
- Toute implementation doit etre testee avant validation.
- Le workflow officiel reste: BROUILLON -> VALIDE DG -> PLANIFIE -> ASSIGNE -> EN COURS -> REVUE ARCHITECTE -> REVUE QA -> REVUE SECURITY -> INTEGRATION -> VALIDATION DG -> FERME.
- Cette mission ne modifie ni la gouvernance, ni les contrats, ni les regles metier.

## 3. Conventions Git

- Le depot contient une strategie Git generale et un modele operationnel de branches.
- La discipline commune est la suivante: pas de commit direct sur `main` hors flux approuve, une finalite tracee par branche, une revue avant fusion, et des commits explicites.
- Les branches operationnelles restent des branches dediees, par exemple `ticket/<ticket-id>-<slug>`, `sprint/<sprint-id>`, `release/<version>` et `hotfix/<version>`.
- Les tags et messages Git doivent rester lisibles et rattaches a un ticket, un sprint ou une version documentee.
- Sprint 002 ne doit pas etre ouvert par cette mission.

## 4. Conventions de rapport

- Les rapports d'execution doivent suivre `templates/ticket-execution-report-template.md`.
- La structure attendue reste stable: objectif, resume, reutilisation de l'existant, travaux realises, decisions techniques, fichiers impactes, fichiers crees, fichiers modifies, fichiers reutilises, controles effectues, validation des criteres d'acceptation, risques, dette technique, recommandations, mise a jour PCC, mise a jour History, proposition de message Git, proposition de tag recommande, preparation du ticket suivant, et etat propose du ticket.
- Le rapport doit decrire uniquement le ticket execute.
- Les sections de reutilisation et de traçabilite restent obligatoires.
- Les rapports Sprint 001 sont la reference de style immediate pour le Sprint 002.

## 5. Conventions YAML

- Le bloc YAML standard se place en fin de rapport d'execution.
- Le bloc est unique, fence avec `yaml`, et utilise des cles stables en minuscules.
- Les champs standard sont: `ticket`, `status`, `qa`, `security`, `architecture`, `git`, `pcc`, `history`, `blocking_risk`, `next_ticket`, `decision_required`.
- Les valeurs doivent exprimer un etat synthetique, pas une narration.
- Le bloc YAML sert de resume machine-readable sans remplacer le texte du rapport.

## 6. Reutiliser avant de creer

- Verifier d'abord les templates, les tickets precedents, les historiques et le PCC.
- Reutiliser les fichiers, les conventions et les formulations deja presentes quand ils suffisent.
- Creer uniquement ce qui manque vraiment et qui est justifie.
- Documenter dans le rapport ce qui a ete analyse, reutilise, modifie et cree.
- Ne pas dupliquer un contrat deja stabilise.

## 7. Points d'attention issus de la cloture du Sprint 001

- T01.04 n'a pas de rapport dedie, mais son contrat est couvert par `env/README.md` et les exemples de configuration.
- Les secrets et certificats restent externalises; aucun secret reel ne doit etre introduit dans le depot.
- CI/CD, monitoring et autres activations operationnelles restent conceptuels tant qu'un ticket explicite ne les ouvre pas.
- Le Sprint 001 reste la reference de methode tant que la decision DG pour la suite n'est pas tracee.
- Aucune fonctionnalite ne doit etre developpee dans ce bootstrap.

## 8. Preparation du Sprint 002

- Le dossier de preparation est pose sans ouverture de ticket.
- Les conventions hereditees du Sprint 001 sont figees comme base de travail.
- Les futures ouvertures devront reutiliser les contrats et les templates existants.
- La mission s'arrete apres remise du present document.
