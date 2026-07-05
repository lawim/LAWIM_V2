# NEXT_RELEASES

## Prochaines releases officielles

| Release | Objectif | Statut |
|---|---|---|
| AAE | Production Security & Secrets | À démarrer |
| AAF | Migration OVH | À démarrer |
| AAG | Monitoring & Observability | À démarrer |
| AAH | Performance & Load Testing | À démarrer |
| AAI | Go Live Certification | À démarrer |
| AAJ | Production Deployment | Clôturée |

La phase AAD est close. La prochaine release officielle est AAE.

## Module langues prêt avant migration

- Le module langues LAWIM_V2 est intégré, minimal et non invasif.
- Langues officielles: `fr`, `en`, `pcm`.
- Le fallback français est actif par défaut.
- Aucun impact base de données ni migration.

## Consolidation pre-gel

- La source intelligence comprend maintenant les signaux pidgin/pcm courants du contexte camerounais.
- Le CRM applique des heuristiques de scoring plus proches des référentiels LAWIMA retenus comme meilleurs.
- Aucun nouveau périmètre métier n'est ouvert par cette consolidation.

## Deploiement termine

- La release AAJ de production est maintenant cloturee sur le snapshot `4c078fd8139f98d6cc34c6e6ff452165bee10bdd`.
- Les prochaines activations fonctionnelles concernent la configuration Google Drive, les sauvegardes, WhatsApp Business, Facebook, le stockage distribue et l'exploitation courante.

## Geo reference follow-up

- Etendre progressivement le catalogue avec des villages, quartiers secondaires et arrondissements mieux documentes.
- Ajouter des coordinates mieux sourcées lorsque des donnees fiables sont disponibles.
- Introduire des regles d'affinite territoriale plus fines si le besoin produit le justifie.
- Garder les donnees brutes historiques hors du runtime et ne conserver que les referentiels nettoyes.
- GEO Intelligence is now closed; future geo changes must go through the normal release planning cycle.
