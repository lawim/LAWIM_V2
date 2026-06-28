# snippets

Ce dossier reserve les fragments Nginx reutilisables.

Principes:
- fragments courts et sans valeur metier;
- aucun domaine reel;
- aucune cle ni aucun secret;
- les snippets servent aux headers, au proxy, au TLS et aux reglages communs.

Usage attendu:
- factoriser les blocs communs;
- reduire la duplication entre virtual hosts;
- garder `default.conf` lisible.
