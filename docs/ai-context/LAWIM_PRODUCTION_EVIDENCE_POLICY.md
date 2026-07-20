# LAWIM — Politique de Preuve de Production

## Preuves insuffisantes

Les éléments suivants ne permettent pas de déclarer une fonctionnalité opérationnelle sur un canal réel :

- code présent dans le dépôt
- tests unitaires réussis
- build réussi
- conteneur Docker healthy
- healthz retourne 200
- readyz retourne 200
- webhook configuré dans l'API
- payload simulé accepté par l'endpoint
- Green API retourne `authorized`
- Telegram `getMe` retourne `ok`
- tag Git créé
- rapport rédigé

Ces éléments sont des preuves de déploiement technique, pas de fonctionnement réel.

## Preuves requises

Pour déclarer un canal réel opérationnel, fournir pour chaque message de test :

1. message réel envoyé par un utilisateur (ou depuis le terminal utilisateur)
2. webhook réel reçu et horodaté
3. `correlation_id` ou identifiant de bout en bout
4. pipeline conversationnel exécuté (intention, qualification, agent)
5. réponse générée avec contenu contextuel
6. adaptateur sortant appelé avec identifiant fournisseur
7. identifiant fournisseur obtenu (`idMessage` pour WhatsApp, `message_id` pour Telegram)
8. réponse reçue sur le terminal utilisateur
9. contenu de la réponse vérifié (identité, footer, contexte)
10. logs complets sans secret

## Statuts autorisés

| Statut | Définition |
|--------|------------|
| `IMPLEMENTED` | Code écrit, testé et fusionné |
| `LOCALLY_TESTED` | Testé en environnement local ou de développement |
| `DEPLOYED` | Déployé sur le serveur de production |
| `TECHNICALLY_REACHABLE` | L'infrastructure est en place (webhooks, API) |
| `RUNTIME_VALIDATED` | Un message réel a traversé tout le pipeline |
| `USER_ACCEPTED` | Validé par un utilisateur réel sur son terminal |

Ne pas remplacer ces statuts par un simple `COMPLETE`, `VERIFIED` ou `LIVE` sans preuve adaptée.
