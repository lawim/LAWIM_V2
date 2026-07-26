# Placeholder Details — A.3R-C

## Audit des sources ZIP

Recherche des patterns "User turn", "Assistant turn", "Assistant reply", etc.
dans les champs `text` des messages des 10 archives uniques.

## Résultats

| Bloc | Conversations | Placeholders | % |
|------|:------------:|:------------:|:-:|
| BLOCK_01 | 100 | 0 | 0% |
| BLOCK_02 | 100 | 0 | 0% |
| BLOCK_03 | 90 | 90 | 100% |
| BLOCK_04 | 100 | 100 | 100% |
| BLOCK_05 | 100 | 100 | 100% |
| BLOCK_06 | 100 | 100 | 100% |
| BLOCK_07 | 100 | 100 | 100% |
| BLOCK_08 | 100 | 100 | 100% |
| BLOCK_09 | 100 | 100 | 100% |
| BLOCK_10 | 100 | 100 | 100% |
| **Total** | **990** | **790** | **79.8%** |

## Conclusion

Seuls les blocs 1 et 2 (200 conversations) contiennent de véritables dialogues.
Les blocs 3 à 10 (790 conversations) sont des templates avec "User turn" et
"Assistant turn" comme contenu textuel.

Ces 790 conversations devraient être classées `PLACEHOLDER_TEMPLATE` et ne
peuvent pas être certifiées comme dialogues réels.

## Fichier

`evidence/normalized/source-placeholder-audit.jsonl` (990 lignes)

**Contrôle :** PH-0001 : 790/990 PLACEHOLDER_TEMPLATE
