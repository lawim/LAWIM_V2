# Migration framework

## Objectif

La couche de migration de LAWIM V2 expose un scaffold de préparation à la montée de version pour les scénarios SQLite et PostgreSQL.

Ce document décrit un outillage local de certification pré-migration. Il ne lance aucune migration réelle et reste exclu du paquet OVH tant que la phase AAF n'est pas démarrée.

## Composants

- MigrationRegistry: registre des étapes de migration avec version de départ/arrivée et backend cible.
- MigrationPlanner: calcul du plan d’exécution à partir de la version courante et de la version cible.
- MigrationRunner: exécution des étapes, journalisation dans l’historique et mise à jour du statut de schéma.
- MigrationValidator: validation du schéma via la table schema_meta.
- RollbackManager: évaluation de la possibilité d’un rollback vers une version antérieure.

Le scaffold reste volontairement minimal:

- aucune migration ne s'exécute sans appel explicite;
- aucune écriture n'est effectuée sur une base réelle pendant les tests;
- aucune dépendance externe n'est ajoutée.

## Utilisation

```python
from lawim_v2.migration import (
    MigrationRegistry,
    MigrationRunner,
    MigrationState,
    MigrationHistory,
    MigrationStep,
    MigrationValidator,
)
```

Les migrations sont idempotentes et doivent toujours préserver la table schema_meta utilisée par le dépôt.
