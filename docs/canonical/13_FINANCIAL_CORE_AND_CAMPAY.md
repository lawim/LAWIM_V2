# Financial Core Et Campay

Version: 1.0
Date: 2026-07-14
Commit de reference: d30d61e1d89427ece9c180cec4639cce77fdcba3
Statut: CANONICAL

## Statut
Financial Core et Campay sont KEEP_AND_CLEAN sous reserve de controle continu. Ils sont independants de la reconstruction Conversation-Qualification-Search-Matching-Relationship.

## Responsabilites
Financial Core gere catalogues tarifaires, devis, factures, paiements, remboursements, commissions, payouts, ledger et rapprochement. Campay est un connecteur de paiement mobile money controle par flags, securite webhook, idempotence et rapprochement.

## Regles
- Une conversation peut initier une intention de paiement, jamais valider seule une transaction financiere.
- Les webhooks ne sont pas une preuve metier complete; ils prouvent un evenement fournisseur.
- Les operations financieres doivent etre auditables, idempotentes et reconciliables.
