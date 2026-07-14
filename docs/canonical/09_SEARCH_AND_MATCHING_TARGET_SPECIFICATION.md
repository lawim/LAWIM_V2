# Specification Cible Search Et Matching

Version: 1.0
Date: 2026-07-14
Commit de reference: d30d61e1d89427ece9c180cec4639cce77fdcba3
Statut: CANONICAL

## Statut
Moteur actuel: UNVALIDATED, TO_DELETE, TO_REBUILD lorsqu'il depend de criteres ou d'etats non fiables.

## Search
Search transforme des criteres qualifies en requetes sur sources autorisees: biens LAWIM, annonces internes, partenaires verifies et donnees publiques explicitement autorisees. Il gere disponibilite, filtres, zero resultat, recherche active et alertes.

Zero resultat ne doit pas produire une fausse proposition. Le systeme explique les criteres bloquants et propose soit d'elargir les criteres, soit d'activer une alerte, soit de passer a un agent LAWIM.

## Matching
Matching classe des candidats par criteres obligatoires, criteres preferentiels, fraicheur, verification, diversite et compatibilites. Il produit un score explicable et les raisons principales.

## Interdictions
- Pas de matching avec criteres insuffisants.
- Pas de relation creee par Matching.
- Pas de donnees privees partagees dans un resultat.
- Pas de score opaque utilise comme unique justification.
