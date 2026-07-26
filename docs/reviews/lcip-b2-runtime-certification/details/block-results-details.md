# Block Results Details — B.2

## Par bloc

| Bloc | Conversations | RUNTIME_BEHAVIOR_ERROR |
|------|:------------:|:----------------------:|
| 1 | 100 | 100 |
| 2 | 100 | 100 |
| **Total** | **200** | **200** |

## Par langue

| Langue | Total | PASS |
|--------|:-----:|:----:|
| fr | 142 | 0 |
| en | 29 | 0 |
| pcm | 29 | 0 |

## Par classification

| Classification | Nombre |
|----------------|:------:|
| RUNTIME_BEHAVIOR_ERROR | 200 |

## Analyse

Tous les 200 dialogues sont classés RUNTIME_BEHAVIOR_ERROR car les fichiers
expected_* générés par la migration B.1 utilisent un modèle d'état simplifié
qui ne correspond pas à la structure de sortie réelle du
ProgramFEngineAdapter.

Le moteur de certification fonctionne correctement — il détecte les
divergences. Les 200 conversations ont réellement été exécutées contre le
runtime (1 016 appels runtime confirmés).

**Contrôle :** CLASS-0001 : 200 RUNTIME_BEHAVIOR_ERROR
