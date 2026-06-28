# Certs

Ce dossier documente la politique de certificats Nginx.

Principes:
- aucun certificat reel ne doit etre commite;
- les certificats sont montes depuis l'exterieur au moment du deploiement;
- les cles privees restent hors depot;
- les certificats de developpement ou de preproduction sont generes et distribues par le layer operationnel.

Noms reserves:
- `lawim.crt`;
- `lawim.key`;
- `dhparam.pem` si une politique TLS l'exige plus tard.

Cette arborescence est purement documentaire a ce stade.
