# Ticket Workflow

## Portee
Workflow officiel des tickets LAWIM_V2.

## Principe
Un ticket suit une chaine de statut unique. Aucun etat ne peut etre saute sans decision explicite du Directeur General et trace dans le PCC.

## Workflow officiel

BROUILLON

-> 

VALIDE DG

-> 

PLANIFIE

-> 

ASSIGNE

-> 

EN COURS

-> 

REVUE ARCHITECTE

-> 

REVUE QA

-> 

REVUE SECURITY

-> 

INTEGRATION

-> 

VALIDATION DG

-> 

FERME

## Acteurs de reference

- Directeur General: autorite de gouvernance et validation finale;
- PMO: enregistre les statuts et trace les decisions;
- Product Owner: confirme la coherence fonctionnelle et les criteres d'acceptation;
- Tech Lead: supervise la coherence technique pendant l'execution;
- Chief Architect: valide la qualite architecturale;
- QA: valide la qualite fonctionnelle et la non-regression;
- Security: valide les points de securite;
- Integration Manager: valide l'integration de bout en bout;
- Release Manager: prepare la livraison et la version;
- Delivery Manager: suit la livraison et la demonstration;
- Review Board: emet un avis final de consolidation.

## Transition detaillee

### BROUILLON -> VALIDE DG
- Acteurs autorises: Directeur General, PMO.
- Conditions d'entree: le ticket existe, son titre est pose, le besoin est identifiable.
- Conditions de sortie: objectif, perimetre, dependances et criteres d'acceptation sont suffisamment documentes.
- Regle: seul le Directeur General autorise la sortie du brouillon.

### VALIDE DG -> PLANIFIE
- Acteurs autorises: Directeur General, PMO.
- Conditions d'entree: validation DG tracee, ticket coherent avec le programme et le sprint.
- Conditions de sortie: priorite, fenetre de delivery et intention d'assignation sont fixes.
- Regle: le ticket ne peut pas etre planifie sans trace de validation.

### PLANIFIE -> ASSIGNE
- Acteurs autorises: Directeur General, PMO, Delivery Manager.
- Conditions d'entree: le ticket est place dans un sprint ou une file d'execution.
- Conditions de sortie: un responsable d'execution est nomme et la charge est explicite.
- Regle: l'assignation doit preciser le responsable principal.

### ASSIGNE -> EN COURS
- Acteurs autorises: responsable d'execution, PMO.
- Conditions d'entree: l'assignation est acceptee et les prerequis minimaux sont en place.
- Conditions de sortie: le travail est lance, trace, et le contexte de livraison est ouvert.
- Regle: un ticket assigne mais non demarre doit rester visible.

### EN COURS -> REVUE ARCHITECTE
- Acteurs autorises: responsable d'execution, Tech Lead, Chief Architect.
- Conditions d'entree: livrable technique complet ou suffisamment forme pour revue.
- Conditions de sortie: la structure technique, les dependances et les conventions sont acceptables.
- Regle: tout ecart majeur renvoie le ticket en EN COURS avec corrections tracees.

### REVUE ARCHITECTE -> REVUE QA
- Acteurs autorises: Chief Architect, QA, Tech Lead.
- Conditions d'entree: la structure technique est validee.
- Conditions de sortie: les criteres de qualite et de non-regression peuvent etre testes.
- Regle: un refus architecture impose un retour en EN COURS.

### REVUE QA -> REVUE SECURITY
- Acteurs autorises: QA, Security.
- Conditions d'entree: les tests et criteres d'acceptation sont satisfaits ou documentes.
- Conditions de sortie: aucun defaut bloquant de qualite n'empeche la revue de securite.
- Regle: un echec QA renvoie en EN COURS avec la liste de corrections.

### REVUE SECURITY -> INTEGRATION
- Acteurs autorises: Security, Integration Manager.
- Conditions d'entree: les exigences de securite sont suffisantes et les risques sont traces.
- Conditions de sortie: le livrable peut etre integre sans perte de controle.
- Regle: un echec securite renvoie en EN COURS ou PLANIFIE selon la nature de l'ecart.

### INTEGRATION -> VALIDATION DG
- Acteurs autorises: Integration Manager, Release Manager, Delivery Manager, PMO.
- Conditions d'entree: l'integration de bout en bout est concluante et la version candidate est preparable.
- Conditions de sortie: le paquet de livraison est pret pour la decision finale du Directeur General.
- Regle: toute dependance non resolue bloque la validation finale.

### VALIDATION DG -> FERME
- Acteurs autorises: Directeur General, PMO.
- Conditions d'entree: toutes les revues sont terminees, les preuves sont archivees et la livraison est lisible.
- Conditions de sortie: le ticket est clos dans le PCC, les journaux sont mis a jour et la reference est figee.
- Regle: seul le Directeur General peut fermer definitivement un ticket.

## Regles de retour

- Si la revue architecte echoue, retour en EN COURS.
- Si la revue QA echoue, retour en EN COURS.
- Si la revue Security echoue, retour en EN COURS ou PLANIFIE selon le type de correction.
- Si l'integration echoue, retour en EN COURS ou PLANIFIE selon la dependance a traiter.
- Si la validation DG echoue, retour en PLANIFIE ou EN COURS selon le niveau de reprise requis.

## Regles de traceabilite

- chaque transition doit etre datee;
- chaque validation doit avoir un valideur nomme;
- chaque retour doit avoir une raison;
- chaque fermeture doit pointer vers un historique.

