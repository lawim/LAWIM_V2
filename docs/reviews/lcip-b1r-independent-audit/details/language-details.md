# Language Details — Audit B.1R

## Source

| Langue | Nombre | Pourcentage |
|--------|:------:|:----------:|
| UNSET | 790 | 79.8% |
| fr | 142 | 14.3% |
| en | 29 | 2.9% |
| pcm | 29 | 2.9% |

## Migré (B.1)

| Langue | Nombre |
|--------|:------:|
| fr | 932 |
| en | 29 |
| pcm | 29 |

## Problème

Le script de migration utilise :
```python
language = src_conv.get("language", "fr")
```

Quand `language` est "UNSET" (790 cas), il n'est pas dans la liste
["fr", "en", "pcm"], donc la valeur "UNSET" est conservée... mais le
mapping de catégorie n'est pas concerné.

En réalité, le script garde `language` tel quel et `expected_language`
contient aussi "UNSET". Mais dans les 790 conversations où la langue
n'est pas définie, le dialogue en français est supposé.

## Conclusion

**790 conversations (79.8%) n'ont pas de langue définie dans la source.**
La B.1 les a traitées comme français par défaut sans le signaler.

## Contrôle

LANG-0001 : FAIL (790 UNSET → fr par défaut, non signalé)
