# conf.d

Ce dossier reserve les virtual hosts additionnels de LAWIM_V2.

Principes:
- un fichier par virtual host ou par surcharge claire;
- nommage explicite et stable;
- aucun doublon avec `default.conf`;
- les futures configurations doivent rester compatibles avec le contrat Compose et le contrat d'environnement.

Usage attendu:
- extensions par domaine ou par role;
- surcharges temporaires de production;
- isolation des regles specifiques.
