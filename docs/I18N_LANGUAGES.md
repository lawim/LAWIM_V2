# I18N_LANGUAGES

## Objet

Ce document décrit le scaffold minimal de gestion des langues LAWIM_V2.

Le module vit dans [`code/lawim_v2/i18n.py`](../code/lawim_v2/i18n.py) et expose une API sans dépendance externe pour normaliser, valider et traduire des clés.

## Langues supportées

| Code | Libellé officiel |
|---|---|
| `fr` | Français |
| `en` | Anglais |
| `pcm` | Pidgin camerounais |

## Langue par défaut

- Langue par défaut: `fr`
- Un appel sans langue explicite doit toujours résoudre le français.

## Normalisation

La normalisation convertit les variantes communes vers un code supporté.

Exemples:

- `fr-FR` -> `fr`
- `en_US` -> `en`
- `pcm-CM` -> `pcm`

Les variantes non reconnues reviennent au français.

## Validation

La validation renvoie un booléen.

- `True` pour `fr`, `en`, `pcm` et leurs variantes de locale reconnues
- `False` pour les autres valeurs

## Traduction par clé

Fonctions exposées:

- `normalize_language(language)`
- `validate_language(language)`
- `translate(key, language=None)`

Clés minimales gérées par le scaffold:

- `app.name`
- `language.fr`
- `language.en`
- `language.pcm`
- `auth.login.success`
- `auth.login.failed`
- `validation.required`
- `error.generic`

## Comportement de fallback

L'ordre de résolution est volontairement simple:

1. langue demandée si elle est supportée;
2. fallback vers le français;
3. fallback lisible sous la forme `"[cle]"` si la clé est inconnue;
4. si la clé est vide, retour de `"[missing.translation]"`.

## Limites volontaires du scaffold

Ce module reste minimal par conception.

- pas de chargement de catalogues externes;
- pas de pluralisation;
- pas de gestion des paramètres de format régional;
- pas de dépendance à un framework i18n tiers;
- pas d'impact base de données;
- pas de migration associée.

## Extension future

Pour étendre le module plus tard:

1. ajouter le nouveau code langue à `SUPPORTED_LANGUAGES`;
2. compléter le dictionnaire `_TRANSLATIONS`;
3. maintenir le français comme fallback;
4. ajouter des tests pour la nouvelle langue;
5. conserver les clés stables pour éviter la fragmentation documentaire.

## Note de gouvernance

Le module langues est intégré, minimal, non invasif et prêt avant la phase Migration.

Il ne modifie ni le schéma, ni les migrations, ni les règles métier.
