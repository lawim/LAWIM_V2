# Frontieres De Domaines

Version: 1.0
Date: 2026-07-14
Commit de reference: d30d61e1d89427ece9c180cec4639cce77fdcba3
Statut: CANONICAL

## Carte canonique
| Domaine | Statut futur | Mission | Objets possedes |
| --- | --- | --- | --- |
| Identity and Access | KEEP_AND_CLEAN | Authentifier, autoriser, gerer sessions et roles. | User, Session, Role, Permission |
| Users and Profiles | KEEP_AND_CLEAN | Gerer profils, organisations et preferences. | User, Profile, Organization |
| Channels and Communication | KEEP_AND_CLEAN | Connecteurs Web, WhatsApp, Telegram, Email et notifications. | ChannelIdentity, Message, Notification |
| CRM | KEEP_AND_CLEAN | Contacts, leads, pipeline, suivi humain non conversationnel. | Contact, Lead, Followup |
| Properties and Listings | KEEP_AND_CLEAN | Biens, annonces, publication, disponibilites, medias. | Property, Listing |
| Projects and Dossiers | KEEP_AND_CLEAN | Projet metier persistant et dossier de suivi. | Project, Dossier |
| Documents and GED | KEEP_AND_CLEAN | Documents, pieces, preuves et informations juridiques. | Document |
| Conversation | REBUILD_FROM_ZERO | Interaction, contexte, messages et orchestration conversationnelle cible. | Conversation, Message, Fact |
| Qualification | REBUILD_FROM_ZERO | Matrices executables et progression de maturite. | Fact, SearchRequest |
| Search | REBUILD_FROM_ZERO | Transformation de criteres en recherches verifiables. | SearchRequest |
| Matching | REBUILD_FROM_ZERO | Score, classement et explicabilite. | Match, Proposal |
| Relationship | REBUILD_FROM_ZERO | Consentement, introduction et conversation multipartite. | Consent, Relationship |
| Visits | REVIEW | Planifier, confirmer et tracer les visites. | Visit |
| Commercial Follow-up | REVIEW | Suivre offres, relances et satisfaction. | Offer, Followup |
| Transactions | REVIEW | Etapes transactionnelles sans se substituer au notaire. | Transaction, Offer |
| Financial Core | KEEP_AND_CLEAN | Paiements, factures, commissions et ledger. | Payment, Invoice |
| Campay | KEEP_AND_CLEAN | Connecteur de paiement mobile money. | PaymentProvider |
| Notifications | KEEP_AND_CLEAN | Templates, preferences et livraison. | Notification |
| Feature Management | KEEP_AND_CLEAN | Flags, kill switches, rollout et audit. | FeatureFlag |
| Administration and Cockpits | KEEP_AND_CLEAN | Vues de pilotage et actions internes. | CockpitView |
| Audit and Observability | KEEP_AND_CLEAN | Journalisation, traces, metriques et alertes. | AuditEvent |
| Backup and Disaster Recovery | KEEP_AND_CLEAN | Sauvegarde, restauration et reprise. | Backup, RecoveryBundle |

## Dependances autorisees
- Les canaux peuvent appeler Conversation cible ou Notifications, jamais decider seuls.
- Conversation cible peut lire Project, Dossier, User, ChannelIdentity et appeler Qualification, Search, Matching, Relationship via contrats.
- Qualification produit des faits normalises; elle ne cree pas de relation.
- Search lit des criteres et sources autorisees; Matching classe des resultats; Relationship gere consentement et introduction.
- Financial Core ne depend pas de Conversation pour sa validite comptable.

## Dependances interdites
- Un fournisseur IA ne peut pas ecrire directement une decision metier.
- Un adaptateur WhatsApp, Telegram, Email ou Web ne peut pas posseder de memoire metier.
- Matching ne peut pas creer une relation.
- Relationship ne peut pas inventer un consentement.
- Un dossier ne peut pas etre une simple session de chat.
