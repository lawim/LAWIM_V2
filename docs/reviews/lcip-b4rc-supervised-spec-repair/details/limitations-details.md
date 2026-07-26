# Limitations — LCIP B.4R-C

## Limitations Identifiées

1. **Runtime non exécuté** — Les spécifications sont statiquement approuvées mais n'ont pas été exécutées contre le runtime. Statut : UNDETERMINED.

2. **Génération automatisée** — Les fiches de revue ont été générées par script. Une revue humaine manuelle n'a pas été réalisée pour chaque fichier.

3. **Tautologie non testée** — Aucun test de tautologie n'a été exécuté sur les spécifications générées (comparaison expected ≠ actual).

4. **Provenance simplifiée** — La provenance des faits est documentée mais utilise une heuristique simple. Une analyse plus fine pourrait révéler des incohérences.

5. **Pas de test cross-canal** — Les conversations sélectionnées viennent de web, Telegram et WhatsApp mais aucune validation cross-canal n'a été effectuée.

6. **Échantillon limité** — 20 conversations sur 990 (2%). La généralisation aux 200 spécifications Gold nécessite une validation supplémentaire.

## Risques

- Risque que le générateur automatique produise des erreurs similaires à B.4
- Risque que le runtime se comporte différemment des spécifications attendues
- Risque que certaines règles EXP-00XX soient trop permissives

## Recommandations

1. Exécuter runtime sur les 20 spécifications approuvées
2. Faire valider par un pair humain 5 fiches de revue aléatoires
3. Avant généralisation aux 200, vérifier que le générateur est fiable
4. Ajouter des tests de tautologie systématiques
