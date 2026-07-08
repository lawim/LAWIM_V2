# État du déploiement OVH

## Statut
Le déploiement final a été appliqué sur OVH.

## Artefact produit
- `release/ovh/artefacts/lawim-v2-postgresql-compat.tar.gz`
- SHA256: `05aed8ab224f70026bfabf333b68545dad463db1118f2d6569e1eafbf4b4adb9`
- Release déployée: `/opt/lawim/releases/29eb91c1`

## Validation effectuée
- `/api/health` OK
- login admin OK
- login agent OK
- login owner OK
- dashboard court et lisible
- logout visible
- formulaire login absent après connexion
- traduction FR / EN / Pidgin effective
- matching partenaires opérationnel
- Docker healthy
- Redis healthy
- PostgreSQL healthy
