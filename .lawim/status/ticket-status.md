# Ticket Status

## Principe
Les statuts de ticket sont alignes sur le workflow officiel.

## Etats officiels

| Etat | Signification | Acteur principal | Sortie attendue |
| --- | --- | --- | --- |
| BROUILLON | Ticket en cours de redaction | DG / PMO | Ticket complet et lisible |
| VALIDE DG | Ticket approuve par le Directeur General | Directeur General | Ticket pret pour la planification |
| PLANIFIE | Ticket place dans une sequence de livraison | DG / PMO / Delivery Manager | Assignation possible |
| ASSIGNE | Responsable d'execution nomme | PMO / Delivery Manager | Demarrage de travail |
| EN COURS | Execution active | Responsable d'execution | Livrable pret pour revue architecte |
| REVUE ARCHITECTE | Controle de la coherence technique | Chief Architect / Tech Lead | Validation ou retour en correction |
| REVUE QA | Controle qualite et non-regression | QA | Validation ou retour en correction |
| REVUE SECURITY | Controle securite | Security | Validation ou retour en correction |
| INTEGRATION | Controle de cohesion de bout en bout | Integration Manager | Version candidate |
| VALIDATION DG | Decision finale de gouvernance | Directeur General | Ticket clos ou renvoye |
| FERME | Ticket acheve et archive | Directeur General / PMO | Trace definitive |

## Regles
- un seul statut officiel a la fois;
- aucun saut de statut sans decision DG;
- chaque changement doit laisser une trace dans le PCC;
- les retours en correction se font vers EN COURS sauf cas documente autrement.

