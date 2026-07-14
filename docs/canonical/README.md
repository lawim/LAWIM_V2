# LAWIM_V2 - Referentiel Canonique

Version: 1.0
Date: 2026-07-14
Commit de reference: d30d61e1d89427ece9c180cec4639cce77fdcba3
Statut: CANONICAL

## Role
Ce repertoire est le seul point d'entree actif de la specification LAWIM_V2. Tout autre document du depot est soit un runbook operationnel, soit un rapport historique, soit un artefact technique. Aucun rapport ne remplace une specification canonique.

## Ordre de lecture
1. [00_LAWIM_VISION_AND_SCOPE.md](00_LAWIM_VISION_AND_SCOPE.md)
2. [01_PRINCIPLES_AND_GOVERNANCE.md](01_PRINCIPLES_AND_GOVERNANCE.md)
3. [02_USERS_ROLES_AND_ACTORS.md](02_USERS_ROLES_AND_ACTORS.md)
4. [03_DOMAIN_BOUNDARIES.md](03_DOMAIN_BOUNDARIES.md)
5. [04_CANONICAL_DATA_MODEL.md](04_CANONICAL_DATA_MODEL.md)
6. Documents de domaines 05 a 21
7. [22_REBUILD_SCOPE_AND_DECOMMISSION_PLAN.md](22_REBUILD_SCOPE_AND_DECOMMISSION_PLAN.md)
8. [23_TRACEABILITY_MATRIX.md](23_TRACEABILITY_MATRIX.md)
9. [24_GLOSSARY.md](24_GLOSSARY.md)

## Gouvernance
- Toute fonctionnalite doit pointer vers un Requirement ID de [23_TRACEABILITY_MATRIX.md](23_TRACEABILITY_MATRIX.md).
- Toute evolution de domaine modifie la specification avant le code.
- Tout changement majeur est documente par un ADR dans `docs/adr/`.
- Les documents remplaces sont supprimes du depot actif; Git est l'historique.
- Les runbooks d'exploitation peuvent rester hors `docs/canonical/` uniquement s'ils ne redefinissent pas le produit.
- Les rapports restent des constats dates et ne sont jamais des preuves metier sans tests d'acceptation.

## Relation avec ADR, runbooks et rapports
Les ADR expliquent une decision d'architecture. Les runbooks expliquent comment operer une capacite deja definie. Les rapports de livraison decrivent ce qui a ete fait a un instant donne. Le referentiel canonique definit ce qui doit exister.
