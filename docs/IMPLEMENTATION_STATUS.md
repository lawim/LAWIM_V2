# IMPLEMENTATION_STATUS

## État documentaire

- AAD : livré comme architecture d’identity provider optionnelle, clôturée comme phase Entra ID.
- AAE : prochaine release documentaire et opérationnelle dédiée à la sécurité de production.
- AAF à AAJ : releases planifiées, non livrées dans cette normalisation.

## Module langues LAWIM_V2

- Intégré sous forme de scaffold minimal dans `code/lawim_v2/i18n.py`.
- Langues officielles: `fr`, `en`, `pcm`.
- Fallback français appliqué par défaut.
- Non invasif, sans impact base de données, prêt avant la phase Migration.

## Projection de release OVH

- Projection `release/` ajoutée pour la release industrialisée et les manifestes de déploiement.
- Paquet OVH décrit comme projection minimale, sans documentation interne, sans tests et sans secret réel.
- Aucun impact sur le schéma de base de données, les règles métier ou la phase Migration.

## Règle de gouvernance

Toute future référence à la sécurité globale de production doit utiliser les noms AAE/AAF/AAG/AAH/AAI/AAJ selon le périmètre concerné.
