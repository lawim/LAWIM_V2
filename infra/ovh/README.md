# OVH

Ce dossier formalise la fondation OVH de LAWIM_V2.

## 1. Objectif

Documenter l'architecture cible d'hebergement et d'exploitation sur OVH sans ressource reelle, sans identifiant et sans certificat.

## 2. Architecture cible

- OVH porte la production;
- un serveur local sert de relais de continuite et de reprise;
- un disque externe porte la sauvegarde hebdomadaire;
- des espaces distants specialises completent la conservation;
- Docker et Docker Compose portent la couche d'execution;
- Nginx expose l'entree publique et termine TLS.

## 3. Organisation des ressources

- host de production;
- relais local de continuite;
- zone de sauvegarde et de restauration;
- plan d'administration;
- aucun serveur, compte, domaine ou certificat reel ne doit etre defini ici.

## 4. Exigences reseau et DNS

- les ports 80 et 443 sont reserves a l'entree publique;
- SSH reste limite aux besoins d'administration;
- aucun service interne ne doit etre expose directement;
- la strategie DNS reste conceptuelle: entree publique, entree d'administration et noms internes si necessaire;
- aucune zone DNS reelle n'est creee dans ce ticket.

## 5. Stockage et sauvegarde

- volumes systeme;
- volumes runtime;
- volume de journaux;
- volume de staging des sauvegardes;
- volume de staging des restaurations.

La chaine de sauvegarde suit le referentiel de stockage officiel:

1. OVH en production;
2. synchronisation vers le relais local;
3. sauvegarde locale;
4. sauvegarde hebdomadaire sur disque externe;
5. synchronisation vers les espaces distants specialises;
6. verification d'integrite;
7. test de restauration;
8. rapport automatique;
9. notification d'echec.

## 6. Administration

- comptes nommes;
- moindre privilege;
- acces par cle SSH;
- journalisation des acces;
- absence de comptes partages;
- aucun secret technique en clair.

## 7. Automatisation future

- `../check-env.sh` reste le squelette de verification des prerequis;
- `../install.sh` reste le squelette de preparation d'hebergement;
- les futurs scripts devront rester idempotents, explicites et non destructifs;
- aucune automatisation operationnelle n'est active a ce stade.

## 8. Integration avec Docker, Compose et Nginx

- Docker Compose porte l'assemblage des services sur le host cible;
- Nginx expose la couche publique;
- les variables d'environnement restent injectees hors depot;
- OVH fournit l'hebergement et la surface de reprise, pas la logique applicative.

## 9. Preparation pour T01.07

- les limites des secrets doivent rester externes;
- les futures automatisations peuvent reutiliser cette fondation sans redefinir l'architecture;
- le prochain ticket pourra s'appuyer sur les conventions de serveur et de reprise posees ici.
