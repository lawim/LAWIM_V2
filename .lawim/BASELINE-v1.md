# LAWIM AIOS Baseline v1

Date de reference: 2026-06-28
Version de reference: 1.0
Statut: FROZEN

## Objet

Ce document fixe l'etat officiel de reference du systeme avant le demarrage du developpement applicatif. Toute divergence a partir de cet etat doit etre consideree comme un changement par rapport a la baseline et doit etre tracee dans le PCC.

## Snapshot officiel

| Domaine | Etat officiel |
| --- | --- |
| Gouvernance | DG, PMO, PCC, workflow, statuts, checklists et modeles de release sont definis |
| Programme | INITIALISE |
| Sprint actif | Sprint 001 |
| Statut du sprint 001 | INITIALISE |
| Decision programme | GO AVEC RESERVES |
| Livraison applicative | Aucun developpement applicatif demarre |
| Release history | Vide, conserve en mode append-only |
| Risques | R-001, R-002 et R-003 ouverts |
| Dependances | D-001 confirme, D-002 confirme, D-003 en attente |
| Traceability set | PCC, history, validations, checklists et workflow disponibles |

## Etat de reference

- les referentiels de pilotage existent et sont actifs;
- le workflow officiel des tickets est fige;
- le modele de statut des tickets et des sprints est fige;
- le sprint 001 constitue la premiere fenetre de livraison controlee;
- aucune creation d'agent n'est requise pour cette baseline;
- aucun ticket applicatif n'est valide comme execute a ce stade;
- aucune release n'est publiee;
- les journaux de release sont vides mais prets a recevoir des entrees append-only.

## Elements confirmes

- D-001: Bootstrap Pack valide.
- D-002: Base operationnelle Sprint 001.
- PCC initialise pour le programme LAWIM_V2.
- La decision initiale du programme est enregistree au 2026-06-28.

## Points ouverts connus

- R-001: backlog canonique non totalement verifie.
- R-002: risque de derive de secret ou de configuration.
- R-003: ambiguite d'infrastructure entre environnements.
- D-003: prerequis T01.02 a confirmer.

## Regles de baseline

- cette baseline est la reference commune avant toute execution applicative;
- toute deviation doit etre comparee a ce document avant d'entrer en production de developpement;
- toute modification de gouvernance, de workflow ou de status impose une decision DG et une nouvelle version;
- aucune reinterpretation retrospective de l'etat initial n'est autorisee sans trace formelle;
- la baseline ne remplace ni le PCC ni les journaux, elle les cadre.

## Conclusion

LAWIM AIOS v1.0 est fige sur une base documentaire, gouvernance et pilotage. Le systeme est pret a entrer en production de developpement sous controle de tickets.
