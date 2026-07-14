# Principes Et Gouvernance

Version: 1.0
Date: 2026-07-14
Commit de reference: d30d61e1d89427ece9c180cec4639cce77fdcba3
Statut: CANONICAL

## Regles absolues
1. Une notion metier a une seule definition canonique.
2. Un domaine a une responsabilite canonique et des frontieres explicites.
3. Une specification definit ce qui doit exister.
4. Un rapport decrit ce qui a ete fait a un instant donne.
5. Une preuve demontre un comportement valide selon le standard d'acceptation.
6. Un test technique isole ne valide pas un comportement metier.
7. Aucun document concurrent ne doit etre cree.
8. Les documents remplaces sont supprimes; Git constitue l'historique.
9. Les Feature Flags encadrent toute activation majeure.
10. Un statut `VALIDE` exige les preuves de [20_TESTING_AND_ACCEPTANCE_STANDARD.md](20_TESTING_AND_ACCEPTANCE_STANDARD.md).

## Processus de modification
Toute demande commence par l'identification ou la creation d'un Requirement ID. La specification canonique et, si necessaire, un ADR sont modifies avant le code. Le code, l'API, les tests et les runbooks sont ensuite alignes. Les anciennes references sont supprimees dans le meme changement.

## Documents actifs autorises
- `docs/canonical/` pour la specification.
- `docs/adr/` pour les decisions.
- Runbooks operationnels hors specification, a condition de pointer vers le canon et de ne pas redefinir le produit.

## Documents interdits
Les dossiers `archive`, `legacy`, `old`, `deprecated` ou equivalents sont interdits dans le depot actif pour conserver d'anciens referentiels.
