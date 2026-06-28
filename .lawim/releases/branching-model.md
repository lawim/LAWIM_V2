# Branching Model

## Branches officielles
- main: base stable et production-ready;
- ticket/<ticket-id>-<slug>: branche de travail associee a un ticket;
- sprint/<sprint-id>: branche optionnelle de consolidation de sprint;
- release/<version>: branche de gel et de preparation de release;
- hotfix/<version>: branche courte pour correction urgente.

## Regles
- aucun commit direct sur main hors release ou hotfix approuve;
- chaque branche doit avoir une finalite tracee;
- une branche ticket ne doit pas servir a plusieurs tickets sans decision;
- une release branche est gelee sauf correction validee;
- un hotfix ne contourne pas la validation de traceabilite.

## Rattachement
- le Release Manager gouverne les branches de release;
- le Delivery Manager suit les branches de livraison;
- le Tech Lead surveille la coherence technique;
- le Directeur General arbitre les exceptions.

