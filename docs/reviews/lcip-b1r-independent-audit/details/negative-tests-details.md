# Negative Tests Details — Audit B.1R

## Tests créés

| ID | Défaut | Résultat |
|----|--------|:--------:|
| NEG-0001 | Budget erroné (999999 au lieu du montant réel) | PASS |
| NEG-0002 | Zone perdue (district absent) | PASS |
| NEG-0003 | Action métier NONE au lieu de search | PASS |
| NEG-0004 | Double création (case_id dupliqué) | PASS |
| NEG-0005 | Langue déclarée en, réponses en fr | PASS |
| NEG-0006 | next_action ASK_BUDGET incorrect | PASS |
| NEG-0007 | Qualification complète sans critères | PASS |

## Résultat

**0/7 tests négatifs détectés.** Tous passent avec VERDICT PASS.

Ceci confirme que le moteur de certification ne détecte aucune erreur
car il compare les données attendues avec un dictionnaire vide.

## Conclusion

```
LCIP_CERTIFICATION_ENGINE_INVALID
```

Le juge de certification est invalide. Il accepte toute donnée comme
correcte si les fichiers actual_* n'existent pas.

## Contrôle

NEG-0001 : FAIL (7/7 échoués — moteur invalide)
