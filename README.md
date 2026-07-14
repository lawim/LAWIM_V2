# LAWIM_V2

LAWIM_V2 est une plateforme immobiliere intelligente pour le Cameroun. La specification produit et technique active est desormais centralisee dans [docs/canonical/README.md](docs/canonical/README.md).

## Source de verite
- Specification canonique: [docs/canonical/README.md](docs/canonical/README.md)
- ADR actifs: [docs/adr/](docs/adr/)
- Rapport Mission 1: [reports/product_reviews/LAWIM_V2_Mission_1_Canonical_Documentation_Refoundation.md](reports/product_reviews/LAWIM_V2_Mission_1_Canonical_Documentation_Refoundation.md)

Les anciens rapports et documents remplaces ne sont pas des specifications actives. Git conserve l'historique.

## Statut de refondation
Conversation, qualification conversationnelle, search orchestration, matching, relationship, consentement, visites et suivi conversationnels sont a reconstruire a zero selon le canon. Les fondations independantes IAM, profils, canaux verifies, CRM, biens et annonces, GED, Financial Core, Campay, notifications, feature management, audit, monitoring, backup, PostgreSQL, Redis, Docker et deploiement sont conservees sous controle.

## Validation documentaire
```bash
python3 scripts/validate_canonical_docs.py
```
