# Financial Core Architecture

## 1. Objectif
Le Financial Core centralise les objets financiers de LAWIM_V2 sans dépendre d'un fournisseur de paiement spécifique. Il couvre le catalogue, la tarification, les devis, les factures, les avoirs, les reçus, les paiements, les remboursements, les abonnements, les commissions, les reversements, le journal financier et le rapprochement.

## 2. Architecture
Le noyau financier est intégré à l'architecture existante via:
- `LawimRepository` enrichi par `FinancialRepositoryMixin`
- `LawimServices.financial`
- routes `api/v2/financial/*` dans le serveur HTTP
- métriques financières et Campay
- permissions financières côté backend

Le stockage reste dans la base de données applicative existante. Aucun schéma parallèle n'est créé.

## 3. Limites
- La Partie 1 livre le Financial Core interne.
- L'adaptateur Campay est maintenant intégré comme connecteur isolé, mais la validation live sandbox/production reste soumise aux accès d'environnement.
- Le stockage documentaire détaillé et le cockpit métier financier complet sont désormais livrés par la Partie 2, avec une supervision administrative séparée.

## 4. Modèles
Modèles persistants mis en place:
- `FinancialProduct`
- `PricingRule`
- `Quote`, `QuoteLine`
- `Invoice`, `InvoiceLine`
- `CreditNote`, `CreditNoteLine`
- `Receipt`
- `PaymentProvider`
- `PaymentIntent`
- `PaymentAttempt`
- `PaymentTransaction`
- `ProviderEvent`
- `Refund`
- `SubscriptionPlan`
- `Subscription`
- `SubscriptionCycle`
- `CommissionRule`
- `Commission`
- `Payout`
- `LedgerAccount`
- `LedgerEntry`
- `ReconciliationRecord`
- `FinancialAuditEvent`

Dans l'implémentation actuelle, ces concepts sont portés par des tables `financial_*` et des payloads JSON structurés, ce qui permet d'avancer sans casser les conventions de persistance du dépôt.

## 5. Relations
Relations principales:
- un devis appartient à un client et peut être converti en facture
- une facture peut référencer un devis source
- une intention de paiement appartient à une facture
- une tentative appartient à une intention
- une transaction appartient à une intention et à une tentative
- un reçu est produit à partir d'une transaction réussie
- un remboursement référence une transaction et une facture
- un abonnement référence un plan et produit des cycles
- une commission référence une règle et une source métier
- un reversement regroupe une ou plusieurs commissions
- un rapprochement relie événements, transactions et objets financiers
- un audit financier conserve l'historique des transitions sensibles

## 6. Cycles De Vie
### Devis
`DRAFT -> ISSUED -> VIEWED -> ACCEPTED -> CONVERTED`

### Facture
`DRAFT -> ISSUED -> PARTIALLY_PAID -> PAID`
avec branches `OVERDUE`, `CANCELLED`, `VOID`, `REFUNDED`, `PARTIALLY_REFUNDED`

### Payment Intent
`CREATED -> PENDING -> PROCESSING -> REQUIRES_ACTION -> SUCCEEDED`
avec branches `FAILED`, `CANCELLED`, `EXPIRED`

### Payment Attempt
`PENDING -> PROCESSING -> SUCCEEDED`
avec branches `FAILED`, `CANCELLED`, `EXPIRED`

### Payment Transaction
`PENDING -> PROCESSING -> SUCCESSFUL`
avec branches `FAILED`, `CANCELLED`, `EXPIRED`, `REVERSED`, `PARTIALLY_REFUNDED`, `REFUNDED`

### Remboursement
`REQUESTED -> UNDER_REVIEW -> APPROVED -> PROCESSING -> SUCCEEDED`
avec branches `REJECTED`, `FAILED`, `CANCELLED`

### Abonnement
`PENDING -> TRIAL -> ACTIVE -> PAST_DUE -> SUSPENDED -> CANCELLED/EXPIRED/TERMINATED`

### Commission
`CALCULATED -> PENDING_VALIDATION -> VALIDATED -> PAYABLE -> SCHEDULED -> PAID`
avec branches `CANCELLED`, `DISPUTED`, `REVERSED`

### Rapprochement
`MATCHED`, `PARTIALLY_MATCHED`, `UNMATCHED`, `CONFLICT`, `MANUAL_REVIEW`, `RESOLVED`

## 7. Statuts
Les statuts sont centralisés dans `financial/constants.py` et validés par le moteur métier avant persistance.

## 8. Règles De Calcul
- Montants exprimés en unités minimales
- Pas de float pour les montants
- Arrondis centralisés avec `Decimal` et `ROUND_HALF_UP`
- Devise primaire: `XAF`
- Normalisation des numéros Mobile Money côté backend
- Totaux dérivés des lignes et du moteur tarifaire

La structure de tarification fournit:
- sous-total
- remises
- frais
- taxes
- total

## 9. Idempotence
La couche financière utilise des clés de référence stables pour:
- devis
- factures
- intentions de paiement
- tentatives
- transactions
- reçus
- remboursements
- commissions
- reversements
- événements de rapprochement

Le même appel logique doit retourner l'objet existant plutôt que créer un double effet.

## 10. Sécurité
- Permissions backend obligatoires
- Données financières limitées au strict nécessaire
- Secrets exclus du schéma financier
- Pas de dépendance frontend pour autoriser un paiement
- Aucun fournisseur externe n'est la source unique de vérité
- Les objets sensibles sont journalisés et auditables

## 11. Événements
Événements financiers principaux:
- `quote.created`
- `quote.issued`
- `quote.accepted`
- `invoice.created`
- `invoice.issued`
- `invoice.paid`
- `payment.intent.created`
- `payment.succeeded`
- `payment.failed`
- `receipt.generated`
- `refund.requested`
- `refund.approved`
- `refund.processed`
- `subscription.renewed`
- `commission.calculated`
- `commission.paid`
- `reconciliation.resolved`

Les événements ne transportent pas de secrets.

## 12. Permissions
Permissions financières ajoutées:
- lecture / gestion du catalogue
- lecture / gestion de la tarification
- création et émission de devis
- lecture et émission de factures
- initiation et lecture des paiements
- demande et approbation des remboursements
- gestion des abonnements
- lecture et validation des commissions
- gestion des reversements
- lecture du journal
- gestion du rapprochement
- lecture de l'audit financier
- gestion des fournisseurs de paiement

## 13. API
Routes principales implémentées:
- `/api/v2/financial/dashboard`
- `/api/v2/financial/readiness`
- `/api/v2/financial/providers`
- `/api/v2/financial/providers/health`
- `/api/v2/financial/providers/campay/webhook`
- `/api/v2/financial/catalog/products`
- `/api/v2/financial/catalog/pricing-rules`
- `/api/v2/financial/pricing/calculate`
- `/api/v2/financial/quotes`
- `/api/v2/financial/invoices`
- `/api/v2/financial/payments/intents`
- `/api/v2/financial/payments/intents/{id}/status`
- `/api/v2/financial/payments/attempts`
- `/api/v2/financial/payments/transactions`
- `/api/v2/financial/receipts`
- `/api/v2/financial/receipts/{id}`
- `/api/v2/financial/refunds`
- `/api/v2/financial/subscriptions`
- `/api/v2/financial/subscriptions/plans`
- `/api/v2/financial/commissions`
- `/api/v2/financial/commissions/rules`
- `/api/v2/financial/payouts`
- `/api/v2/financial/ledger/accounts`
- `/api/v2/financial/ledger/entries`
- `/api/v2/financial/reconciliation`
- `/api/v2/financial/audit`
- `/api/v2/financial/provider-events`

## 14. Journal Financier
Le journal financier interne représente les écritures logiques nécessaires au contrôle des flux LAWIM:
- créances clients
- paiements en attente
- encaissements confirmés
- revenus LAWIM
- commissions à payer
- reversements
- remboursements
- frais fournisseur
- taxes collectées
- ajustements
- écarts de rapprochement

Les écritures validées doivent rester immuables.

## 15. Rapprochement
Le rapprochement compare:
- intentions internes
- tentatives
- transactions
- événements fournisseur
- factures
- reçus
- écritures
- remboursements

Il doit pouvoir signaler:
- transaction orpheline
- doublon
- montant différent
- devise différente
- webhook manquant
- statut incohérent
- conflit manuel

## 16. Migrations
Le socle financier a été ajouté dans les scripts DDL existants et dans les migrations SQLite de compatibilité.
La version de schéma est conservée à `19` pour ne pas casser les validations historiques du dépôt pendant cette phase.

### Validation PostgreSQL réelle
- Moteur validé: PostgreSQL `16.14`
- Port local utilisé: `5433`
- DSN de validation: `postgresql://lawim:lawim@127.0.0.1:5433/lawim_v2`
- Démarrage local: `XDG_RUNTIME_DIR=/tmp/lawim_podman_runtime timeout 600s ./platform/start-postgres.sh`
- Diagnostic initial: runtime Podman rootless pointant vers un répertoire non writable sous `/run/user/1000`
- Correctif runtime: `platform/runtime-env.sh` force un `XDG_RUNTIME_DIR` writable sous `/tmp`
- Correctif de seed PostgreSQL: `PostgreSQLLawimRepository.initialize()` réutilise maintenant les hooks de seed communs, y compris `seed_financial_catalog()`
- Correctif de seed communication: les tables génériques `whatsapp_accounts`, `telegram_bots` et `sms_providers` reçoivent aussi `updated_at`
- Correctif métier: `request_refund()` charge maintenant la facture cible avant de construire le payload
- Vérifications exécutées:
  - `pg_isready -h 127.0.0.1 -p 5433 -U lawim -d lawim_v2`
  - `PGPASSWORD=lawim psql -h 127.0.0.1 -p 5433 -U lawim -d lawim_v2 -c "SELECT version(); SELECT current_database(); SELECT current_user; SELECT NOW();"`
  - `LAWIM_TEST_POSTGRES_URL=postgresql://lawim:lawim@127.0.0.1:5433/lawim_v2 ./.venv-platform/bin/python -m unittest tests.test_financial_core -v`
  - `LAWIM_TEST_POSTGRES_URL=postgresql://lawim:lawim@127.0.0.1:5433/lawim_v2 ./.venv-platform/bin/python -m unittest tests.test_productization -v`
  - `LAWIM_TEST_POSTGRES_URL=postgresql://lawim:lawim@127.0.0.1:5433/lawim_v2 timeout 1200s ./platform/run-postgres-tests.sh`
- Le seed financier sur PostgreSQL est idempotent sur une base propre et le catalogue Campay est présent au premier démarrage.

## 17. Intégration Avec LAWIM
L'intégration réelle se fait par:
- `LawimServices.financial`
- `seed_financial_catalog()` dans `LawimRepository.initialize()`
- `PostgreSQLLawimRepository.initialize()` aligne désormais les mêmes hooks de seed sur PostgreSQL
- compteurs d'observabilité
- règles de sécurité
- routes HTTP du serveur

## 18. Intégration Future Campay
Campay est intégré comme premier fournisseur concret du Financial Core:
- adaptateur isolé dans `code/lawim_v2/financial/providers/campay.py`
- registre générique des fournisseurs via `PaymentProviderRegistry`
- authentification par jeton avec cache
- initiation de paiement côté backend
- vérification de statut serveur à serveur
- validation de webhook sur payload brut
- santé du fournisseur via `GET /api/balance/`
- support du catalogue Campay dans le seed financier

Les capacités supportées restent bornées par l'API réellement documentée et par les accès de test disponibles. Les remboursements automatiques et les annulations fournisseur ne sont pas exposés par le connecteur actuel.

## 19. Tests
Tests exécutés pour cette partie:
- compilation Python ciblée
- tests financiers unitaires et API
- tests de compatibilité historiques
- tests de productisation
- validation des règles de configuration
- tests PostgreSQL réels
- harness PostgreSQL de plateforme

Résultats:
- `tests.test_financial_core`: 9 tests, 9 réussites
- `tests.test_productization`: 4 tests, 4 réussites
- `tests.test_runtime_smoke`: 2 tests, 2 réussites
- `ReleaseProgramHPersistenceTests`: 9 tests, 9 réussites
- `ReleaseProgramHConstantsTests`: 69 tests, 69 réussites
- `tests.test_rc_postgresql`: 5 tests, 5 réussites
- `tests.test_financial_core.PostgreSQLFinancialCoreIntegrationTests`: 1 test, 1 réussite
- `platform/run-postgres-tests.sh`: smoke PostgreSQL OK

## 20. Décisions Techniques
- garder le schéma version 19 pour ne pas casser le reste du dépôt
- utiliser des payloads JSON structurés sur des tables génériques `financial_*`
- centraliser les calculs dans `financial/engines.py`
- stocker les propriétaires métier dans les payloads pour rendre les filtres de scope fiables
- traiter Campay comme adaptateur, pas comme noyau métier
- démarrer PostgreSQL local via Podman rootless avec un runtime writable explicite afin d'éviter le blocage `/run/user/1000`

## 21. Éléments Restants Pour Les Parties 2 Et 3
- validation live sandbox/production Campay quand les accès sont fournis
- durcissement éventuel du cycle de remboursement fournisseur si l'API Campay l'autorise
- déploiement OVH
- recette de production
- rollback de release
- documentation d'exploitation finale

## Flux Principal
```mermaid
flowchart LR
    Catalog[Catalogue financier] --> Pricing[Tarification]
    Pricing --> Quote[Devis]
    Quote --> Invoice[Facture]
    Invoice --> PaymentIntent[Payment Intent]
    PaymentIntent --> Provider[Fournisseur de paiement]
    Provider --> PaymentTransaction[Transaction]
    PaymentTransaction --> Receipt[Reçu]
    PaymentTransaction --> Ledger[Journal financier]
    PaymentTransaction --> Commission[Commission]
    Commission --> Payout[Reversement]
    PaymentTransaction --> Reconciliation[Rapprochement]
```
