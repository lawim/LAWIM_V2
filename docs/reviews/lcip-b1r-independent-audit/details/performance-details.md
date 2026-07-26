# Performance Details — Audit B.1R

## Temps annoncé

B.1 annonce : 990 conversations en 1.4 seconde

## Explication

Ce temps est cohérent avec une opération qui :
1. Charge 2 fichiers JSON par conversation (expected_state, conversation)
2. Compare quelques champs
3. Écrit 4 fichiers de sortie

Aucun appel réseau, aucune inference IA, aucune base de données.

## Calcul

- 1.4s / 990 = ~1.4ms par conversation
- C'est le temps de lecture/écriture de petits fichiers JSON
- Un vrai runtime conversationnel prendrait au moins 2-5 secondes par tour
  (appel API IA, état, persistance)

## Temps réel estimé pour une vraie certification

```
990 conversations × 3-5 tours × 3-5 secondes par tour
= ~9 000 à 25 000 secondes
= ~2.5 à 7 heures
```

Les 1.4 secondes de B.1 prouvent qu'aucun runtime n'a été exécuté.

## Contrôle

PERF-0001 : EXPLAINED (1.4s = lecture fichier, pas runtime)
