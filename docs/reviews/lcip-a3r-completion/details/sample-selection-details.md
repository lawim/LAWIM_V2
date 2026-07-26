# Sample Selection Details — A.3R-C

## Échantillon déterministe seed=42

30 conversations sélectionnées depuis les 10 blocs :

| Groupe | Blocs | Taille |
|--------|-------|:------:|
| Block 1 | BLOCK_01 | 10 |
| Block 2 | BLOCK_02 | 10 |
| Others | BLOCKS 03-10 | 10 |
| **Total** | | **30** |

## Fichier

`tests/gold_corpus/certification/samples/a3r-seed42-sample.json`

## Limitations

Sur les 30 sélectionnées, les 10 du groupe "others" proviennent des blocs 3-10
qui sont des templates (placeholders). Ces conversations ne sont pas exécutables
comme dialogues réels. Seules les 20 des blocs 1 et 2 sont des dialogues
authentiques.

Pour une exécution runtime complète, l'échantillon devrait être filtré pour
exclure les `PLACEHOLDER_TEMPLATE`.

**Contrôle :** SMP-0001 : 30 SELECTED (20 executables)
