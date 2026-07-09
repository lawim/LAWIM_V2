# I18N_LANGUAGES

## Objet

Ce document décrit le scaffold minimal de gestion des langues LAWIM_V2.

Le socle est partagé entre [`code/lawim_v2/i18n.py`](../code/lawim_v2/i18n.py) côté backend et [`frontend/packages/ui/src/i18n.tsx`](../frontend/packages/ui/src/i18n.tsx) côté interface.

Il expose une API sans dépendance externe pour normaliser, valider, traduire et persister le choix de langue.

## Langues supportées

| Code | Libellé officiel |
|---|---|
| `fr` | Français |
| `en` | Anglais |
| `pcm` | Pidgin camerounais |

## Langue par défaut

- Langue par défaut: `fr`
- Un appel sans langue explicite doit toujours résoudre le français.
- Le choix par défaut de l'interface est aussi `fr` quand aucun stockage local n'existe.

## Persistance frontale

Le frontend mémorise la langue choisie dans `localStorage` via la clé `lawim.language`.

Le sélecteur de langue actuel expose trois options:

- `fr`
- `en`
- `pcm`

Le contexte React relit cette valeur au démarrage de l'application et réapplique la langue sur le dashboard, le login et les modules dédiés.

## Normalisation

La normalisation convertit les variantes communes vers un code supporté.

Exemples:

- `fr-FR` -> `fr`
- `en_US` -> `en`
- `pcm-CM` -> `pcm`

Les variantes non reconnues reviennent au français.

Alias connus côté backend:

- `pidgin`
- `pidgin english`
- `cameroon pidgin`
- `cameroonian pidgin`

## Validation

La validation renvoie un booléen.

- `True` pour `fr`, `en`, `pcm` et leurs variantes de locale reconnues
- `False` pour les autres valeurs

## Traduction par clé

Fonctions exposées:

- `normalize_language(language)`
- `validate_language(language)`
- `translate(key, language=None)`

Côté frontend, les mêmes clés sont utilisées pour:

- la page d'accès;
- le dashboard cockpit;
- les cartes de module;
- les boutons et messages de statut;
- les erreurs et succès;
- `Nous écrire`;
- `Et maintenant ?`;
- `Déconnexion` / `Logout` / `Comot`.

Clés minimales gérées par le scaffold:

- `app.name`
- `language.fr`
- `language.en`
- `language.pcm`
- `auth.login.success`
- `auth.login.failed`
- `validation.required`
- `error.generic`
- `dashboard.*`
- `module.*`
- `shared.*`

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

## Note Release 08.1

La Release 08.1 a valide:

- FR comme langue par defaut;
- EN comme second jeu de libelles;
- Pidgin `pcm` comme variante officielle;
- la persistence du choix de langue;
- l application des traductions au login, au dashboard, aux cartes de modules, aux boutons et aux messages de status.

Les ecrans de recette visuelle sont publies dans `reports/product_reviews/Release_08_1/`.

## Note Release 08.3

La Release 08.3 a precise les textes de la page d'acces et du formulaire de creation de compte:

- `auth.login.identifier`
- `auth.login.identifier_help`
- `auth.login.password`
- `auth.login.submit`
- `auth.login.forgot_password`
- `auth.login.create_account`
- `auth.register.full_name`
- `auth.register.email`
- `auth.register.username`
- `auth.register.phone_e164`
- `auth.register.password`
- `auth.register.password_confirmation`
- `auth.register.preferred_language`
- `auth.register.accept_terms`
- `auth.contact.website`
- `auth.contact.email`
- `auth.contact.whatsapp`
- `auth.contact.facebook`

Le choix de langue reste memorise via `lawim.language` et reapplique au login, au register et au dashboard apres reconnexion.
