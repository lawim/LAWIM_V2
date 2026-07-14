# Modele De Donnees Canonique

Version: 1.0
Date: 2026-07-14
Commit de reference: d30d61e1d89427ece9c180cec4639cce77fdcba3
Statut: CANONICAL

## Distinctions obligatoires
Conversation != Projet != Dossier != Recherche != Relation.

- Conversation: fil d'interaction et messages sur un canal ou plusieurs canaux.
- Projet: objectif immobilier persistant porte par un utilisateur ou une organisation.
- Dossier: espace de suivi operationnel d'un projet, avec etapes, documents, relations et decisions.
- Recherche: demande structuree de biens ou services issue de criteres qualifies.
- Relation: lien cree entre parties identifiees apres consentements explicites.

## Objets fondamentaux
### User
- Definition: objet canonique `User` gere par Identity and Access.
- Identifiant: UUID ou identifiant technique stable expose comme reference publique non devinable.
- Proprietaire: Identity and Access.
- Cycle de vie: draft/active/suspended/closed/deleted lorsque applicable; les transitions sont auditees.
- Relations: uniquement via references explicites, jamais par interpretation d'un message libre.
- Donnees obligatoires: identifiant, proprietaire metier, statut, horodatages, source.
- Donnees sensibles: toute donnee personnelle, financiere, juridique, localisation precise ou document prive.
- Source de verite: repository du domaine proprietaire.
- Suppression: suppression logique si audit requis; purge physique selon politique de retention.
- Historisation: AuditEvent pour changement significatif.
- Consentement: requis avant partage a un tiers ou usage hors finalite initiale.

### Profile
- Definition: objet canonique `Profile` gere par Users and Profiles.
- Identifiant: UUID ou identifiant technique stable expose comme reference publique non devinable.
- Proprietaire: Users and Profiles.
- Cycle de vie: draft/active/suspended/closed/deleted lorsque applicable; les transitions sont auditees.
- Relations: uniquement via references explicites, jamais par interpretation d'un message libre.
- Donnees obligatoires: identifiant, proprietaire metier, statut, horodatages, source.
- Donnees sensibles: toute donnee personnelle, financiere, juridique, localisation precise ou document prive.
- Source de verite: repository du domaine proprietaire.
- Suppression: suppression logique si audit requis; purge physique selon politique de retention.
- Historisation: AuditEvent pour changement significatif.
- Consentement: requis avant partage a un tiers ou usage hors finalite initiale.

### ChannelIdentity
- Definition: objet canonique `ChannelIdentity` gere par Channels and Communication.
- Identifiant: UUID ou identifiant technique stable expose comme reference publique non devinable.
- Proprietaire: Channels and Communication.
- Cycle de vie: draft/active/suspended/closed/deleted lorsque applicable; les transitions sont auditees.
- Relations: uniquement via references explicites, jamais par interpretation d'un message libre.
- Donnees obligatoires: identifiant, proprietaire metier, statut, horodatages, source.
- Donnees sensibles: toute donnee personnelle, financiere, juridique, localisation precise ou document prive.
- Source de verite: repository du domaine proprietaire.
- Suppression: suppression logique si audit requis; purge physique selon politique de retention.
- Historisation: AuditEvent pour changement significatif.
- Consentement: requis avant partage a un tiers ou usage hors finalite initiale.

### Organization
- Definition: objet canonique `Organization` gere par Users and Profiles.
- Identifiant: UUID ou identifiant technique stable expose comme reference publique non devinable.
- Proprietaire: Users and Profiles.
- Cycle de vie: draft/active/suspended/closed/deleted lorsque applicable; les transitions sont auditees.
- Relations: uniquement via references explicites, jamais par interpretation d'un message libre.
- Donnees obligatoires: identifiant, proprietaire metier, statut, horodatages, source.
- Donnees sensibles: toute donnee personnelle, financiere, juridique, localisation precise ou document prive.
- Source de verite: repository du domaine proprietaire.
- Suppression: suppression logique si audit requis; purge physique selon politique de retention.
- Historisation: AuditEvent pour changement significatif.
- Consentement: requis avant partage a un tiers ou usage hors finalite initiale.

### Project
- Definition: objet canonique `Project` gere par Projects and Dossiers.
- Identifiant: UUID ou identifiant technique stable expose comme reference publique non devinable.
- Proprietaire: Projects and Dossiers.
- Cycle de vie: draft/active/suspended/closed/deleted lorsque applicable; les transitions sont auditees.
- Relations: uniquement via references explicites, jamais par interpretation d'un message libre.
- Donnees obligatoires: identifiant, proprietaire metier, statut, horodatages, source.
- Donnees sensibles: toute donnee personnelle, financiere, juridique, localisation precise ou document prive.
- Source de verite: repository du domaine proprietaire.
- Suppression: suppression logique si audit requis; purge physique selon politique de retention.
- Historisation: AuditEvent pour changement significatif.
- Consentement: requis avant partage a un tiers ou usage hors finalite initiale.

### Dossier
- Definition: objet canonique `Dossier` gere par Projects and Dossiers.
- Identifiant: UUID ou identifiant technique stable expose comme reference publique non devinable.
- Proprietaire: Projects and Dossiers.
- Cycle de vie: draft/active/suspended/closed/deleted lorsque applicable; les transitions sont auditees.
- Relations: uniquement via references explicites, jamais par interpretation d'un message libre.
- Donnees obligatoires: identifiant, proprietaire metier, statut, horodatages, source.
- Donnees sensibles: toute donnee personnelle, financiere, juridique, localisation precise ou document prive.
- Source de verite: repository du domaine proprietaire.
- Suppression: suppression logique si audit requis; purge physique selon politique de retention.
- Historisation: AuditEvent pour changement significatif.
- Consentement: requis avant partage a un tiers ou usage hors finalite initiale.

### Property
- Definition: objet canonique `Property` gere par Properties and Listings.
- Identifiant: UUID ou identifiant technique stable expose comme reference publique non devinable.
- Proprietaire: Properties and Listings.
- Cycle de vie: draft/active/suspended/closed/deleted lorsque applicable; les transitions sont auditees.
- Relations: uniquement via references explicites, jamais par interpretation d'un message libre.
- Donnees obligatoires: identifiant, proprietaire metier, statut, horodatages, source.
- Donnees sensibles: toute donnee personnelle, financiere, juridique, localisation precise ou document prive.
- Source de verite: repository du domaine proprietaire.
- Suppression: suppression logique si audit requis; purge physique selon politique de retention.
- Historisation: AuditEvent pour changement significatif.
- Consentement: requis avant partage a un tiers ou usage hors finalite initiale.

### Listing
- Definition: objet canonique `Listing` gere par Properties and Listings.
- Identifiant: UUID ou identifiant technique stable expose comme reference publique non devinable.
- Proprietaire: Properties and Listings.
- Cycle de vie: draft/active/suspended/closed/deleted lorsque applicable; les transitions sont auditees.
- Relations: uniquement via references explicites, jamais par interpretation d'un message libre.
- Donnees obligatoires: identifiant, proprietaire metier, statut, horodatages, source.
- Donnees sensibles: toute donnee personnelle, financiere, juridique, localisation precise ou document prive.
- Source de verite: repository du domaine proprietaire.
- Suppression: suppression logique si audit requis; purge physique selon politique de retention.
- Historisation: AuditEvent pour changement significatif.
- Consentement: requis avant partage a un tiers ou usage hors finalite initiale.

### Document
- Definition: objet canonique `Document` gere par Documents and GED.
- Identifiant: UUID ou identifiant technique stable expose comme reference publique non devinable.
- Proprietaire: Documents and GED.
- Cycle de vie: draft/active/suspended/closed/deleted lorsque applicable; les transitions sont auditees.
- Relations: uniquement via references explicites, jamais par interpretation d'un message libre.
- Donnees obligatoires: identifiant, proprietaire metier, statut, horodatages, source.
- Donnees sensibles: toute donnee personnelle, financiere, juridique, localisation precise ou document prive.
- Source de verite: repository du domaine proprietaire.
- Suppression: suppression logique si audit requis; purge physique selon politique de retention.
- Historisation: AuditEvent pour changement significatif.
- Consentement: requis avant partage a un tiers ou usage hors finalite initiale.

### Conversation
- Definition: objet canonique `Conversation` gere par Conversation.
- Identifiant: UUID ou identifiant technique stable expose comme reference publique non devinable.
- Proprietaire: Conversation.
- Cycle de vie: draft/active/suspended/closed/deleted lorsque applicable; les transitions sont auditees.
- Relations: uniquement via references explicites, jamais par interpretation d'un message libre.
- Donnees obligatoires: identifiant, proprietaire metier, statut, horodatages, source.
- Donnees sensibles: toute donnee personnelle, financiere, juridique, localisation precise ou document prive.
- Source de verite: repository du domaine proprietaire.
- Suppression: suppression logique si audit requis; purge physique selon politique de retention.
- Historisation: AuditEvent pour changement significatif.
- Consentement: requis avant partage a un tiers ou usage hors finalite initiale.

### Message
- Definition: objet canonique `Message` gere par Conversation.
- Identifiant: UUID ou identifiant technique stable expose comme reference publique non devinable.
- Proprietaire: Conversation.
- Cycle de vie: draft/active/suspended/closed/deleted lorsque applicable; les transitions sont auditees.
- Relations: uniquement via references explicites, jamais par interpretation d'un message libre.
- Donnees obligatoires: identifiant, proprietaire metier, statut, horodatages, source.
- Donnees sensibles: toute donnee personnelle, financiere, juridique, localisation precise ou document prive.
- Source de verite: repository du domaine proprietaire.
- Suppression: suppression logique si audit requis; purge physique selon politique de retention.
- Historisation: AuditEvent pour changement significatif.
- Consentement: requis avant partage a un tiers ou usage hors finalite initiale.

### Fact
- Definition: objet canonique `Fact` gere par Qualification.
- Identifiant: UUID ou identifiant technique stable expose comme reference publique non devinable.
- Proprietaire: Qualification.
- Cycle de vie: draft/active/suspended/closed/deleted lorsque applicable; les transitions sont auditees.
- Relations: uniquement via references explicites, jamais par interpretation d'un message libre.
- Donnees obligatoires: identifiant, proprietaire metier, statut, horodatages, source.
- Donnees sensibles: toute donnee personnelle, financiere, juridique, localisation precise ou document prive.
- Source de verite: repository du domaine proprietaire.
- Suppression: suppression logique si audit requis; purge physique selon politique de retention.
- Historisation: AuditEvent pour changement significatif.
- Consentement: requis avant partage a un tiers ou usage hors finalite initiale.

### SearchRequest
- Definition: objet canonique `SearchRequest` gere par Search.
- Identifiant: UUID ou identifiant technique stable expose comme reference publique non devinable.
- Proprietaire: Search.
- Cycle de vie: draft/active/suspended/closed/deleted lorsque applicable; les transitions sont auditees.
- Relations: uniquement via references explicites, jamais par interpretation d'un message libre.
- Donnees obligatoires: identifiant, proprietaire metier, statut, horodatages, source.
- Donnees sensibles: toute donnee personnelle, financiere, juridique, localisation precise ou document prive.
- Source de verite: repository du domaine proprietaire.
- Suppression: suppression logique si audit requis; purge physique selon politique de retention.
- Historisation: AuditEvent pour changement significatif.
- Consentement: requis avant partage a un tiers ou usage hors finalite initiale.

### Match
- Definition: objet canonique `Match` gere par Matching.
- Identifiant: UUID ou identifiant technique stable expose comme reference publique non devinable.
- Proprietaire: Matching.
- Cycle de vie: draft/active/suspended/closed/deleted lorsque applicable; les transitions sont auditees.
- Relations: uniquement via references explicites, jamais par interpretation d'un message libre.
- Donnees obligatoires: identifiant, proprietaire metier, statut, horodatages, source.
- Donnees sensibles: toute donnee personnelle, financiere, juridique, localisation precise ou document prive.
- Source de verite: repository du domaine proprietaire.
- Suppression: suppression logique si audit requis; purge physique selon politique de retention.
- Historisation: AuditEvent pour changement significatif.
- Consentement: requis avant partage a un tiers ou usage hors finalite initiale.

### Proposal
- Definition: objet canonique `Proposal` gere par Matching.
- Identifiant: UUID ou identifiant technique stable expose comme reference publique non devinable.
- Proprietaire: Matching.
- Cycle de vie: draft/active/suspended/closed/deleted lorsque applicable; les transitions sont auditees.
- Relations: uniquement via references explicites, jamais par interpretation d'un message libre.
- Donnees obligatoires: identifiant, proprietaire metier, statut, horodatages, source.
- Donnees sensibles: toute donnee personnelle, financiere, juridique, localisation precise ou document prive.
- Source de verite: repository du domaine proprietaire.
- Suppression: suppression logique si audit requis; purge physique selon politique de retention.
- Historisation: AuditEvent pour changement significatif.
- Consentement: requis avant partage a un tiers ou usage hors finalite initiale.

### Consent
- Definition: objet canonique `Consent` gere par Relationship.
- Identifiant: UUID ou identifiant technique stable expose comme reference publique non devinable.
- Proprietaire: Relationship.
- Cycle de vie: draft/active/suspended/closed/deleted lorsque applicable; les transitions sont auditees.
- Relations: uniquement via references explicites, jamais par interpretation d'un message libre.
- Donnees obligatoires: identifiant, proprietaire metier, statut, horodatages, source.
- Donnees sensibles: toute donnee personnelle, financiere, juridique, localisation precise ou document prive.
- Source de verite: repository du domaine proprietaire.
- Suppression: suppression logique si audit requis; purge physique selon politique de retention.
- Historisation: AuditEvent pour changement significatif.
- Consentement: requis avant partage a un tiers ou usage hors finalite initiale.

### Relationship
- Definition: objet canonique `Relationship` gere par Relationship.
- Identifiant: UUID ou identifiant technique stable expose comme reference publique non devinable.
- Proprietaire: Relationship.
- Cycle de vie: draft/active/suspended/closed/deleted lorsque applicable; les transitions sont auditees.
- Relations: uniquement via references explicites, jamais par interpretation d'un message libre.
- Donnees obligatoires: identifiant, proprietaire metier, statut, horodatages, source.
- Donnees sensibles: toute donnee personnelle, financiere, juridique, localisation precise ou document prive.
- Source de verite: repository du domaine proprietaire.
- Suppression: suppression logique si audit requis; purge physique selon politique de retention.
- Historisation: AuditEvent pour changement significatif.
- Consentement: requis avant partage a un tiers ou usage hors finalite initiale.

### Visit
- Definition: objet canonique `Visit` gere par Visits.
- Identifiant: UUID ou identifiant technique stable expose comme reference publique non devinable.
- Proprietaire: Visits.
- Cycle de vie: draft/active/suspended/closed/deleted lorsque applicable; les transitions sont auditees.
- Relations: uniquement via references explicites, jamais par interpretation d'un message libre.
- Donnees obligatoires: identifiant, proprietaire metier, statut, horodatages, source.
- Donnees sensibles: toute donnee personnelle, financiere, juridique, localisation precise ou document prive.
- Source de verite: repository du domaine proprietaire.
- Suppression: suppression logique si audit requis; purge physique selon politique de retention.
- Historisation: AuditEvent pour changement significatif.
- Consentement: requis avant partage a un tiers ou usage hors finalite initiale.

### Offer
- Definition: objet canonique `Offer` gere par Commercial Follow-up.
- Identifiant: UUID ou identifiant technique stable expose comme reference publique non devinable.
- Proprietaire: Commercial Follow-up.
- Cycle de vie: draft/active/suspended/closed/deleted lorsque applicable; les transitions sont auditees.
- Relations: uniquement via references explicites, jamais par interpretation d'un message libre.
- Donnees obligatoires: identifiant, proprietaire metier, statut, horodatages, source.
- Donnees sensibles: toute donnee personnelle, financiere, juridique, localisation precise ou document prive.
- Source de verite: repository du domaine proprietaire.
- Suppression: suppression logique si audit requis; purge physique selon politique de retention.
- Historisation: AuditEvent pour changement significatif.
- Consentement: requis avant partage a un tiers ou usage hors finalite initiale.

### Payment
- Definition: objet canonique `Payment` gere par Financial Core.
- Identifiant: UUID ou identifiant technique stable expose comme reference publique non devinable.
- Proprietaire: Financial Core.
- Cycle de vie: draft/active/suspended/closed/deleted lorsque applicable; les transitions sont auditees.
- Relations: uniquement via references explicites, jamais par interpretation d'un message libre.
- Donnees obligatoires: identifiant, proprietaire metier, statut, horodatages, source.
- Donnees sensibles: toute donnee personnelle, financiere, juridique, localisation precise ou document prive.
- Source de verite: repository du domaine proprietaire.
- Suppression: suppression logique si audit requis; purge physique selon politique de retention.
- Historisation: AuditEvent pour changement significatif.
- Consentement: requis avant partage a un tiers ou usage hors finalite initiale.

### Invoice
- Definition: objet canonique `Invoice` gere par Financial Core.
- Identifiant: UUID ou identifiant technique stable expose comme reference publique non devinable.
- Proprietaire: Financial Core.
- Cycle de vie: draft/active/suspended/closed/deleted lorsque applicable; les transitions sont auditees.
- Relations: uniquement via references explicites, jamais par interpretation d'un message libre.
- Donnees obligatoires: identifiant, proprietaire metier, statut, horodatages, source.
- Donnees sensibles: toute donnee personnelle, financiere, juridique, localisation precise ou document prive.
- Source de verite: repository du domaine proprietaire.
- Suppression: suppression logique si audit requis; purge physique selon politique de retention.
- Historisation: AuditEvent pour changement significatif.
- Consentement: requis avant partage a un tiers ou usage hors finalite initiale.

### Notification
- Definition: objet canonique `Notification` gere par Notifications.
- Identifiant: UUID ou identifiant technique stable expose comme reference publique non devinable.
- Proprietaire: Notifications.
- Cycle de vie: draft/active/suspended/closed/deleted lorsque applicable; les transitions sont auditees.
- Relations: uniquement via references explicites, jamais par interpretation d'un message libre.
- Donnees obligatoires: identifiant, proprietaire metier, statut, horodatages, source.
- Donnees sensibles: toute donnee personnelle, financiere, juridique, localisation precise ou document prive.
- Source de verite: repository du domaine proprietaire.
- Suppression: suppression logique si audit requis; purge physique selon politique de retention.
- Historisation: AuditEvent pour changement significatif.
- Consentement: requis avant partage a un tiers ou usage hors finalite initiale.

### FeatureFlag
- Definition: objet canonique `FeatureFlag` gere par Feature Management.
- Identifiant: UUID ou identifiant technique stable expose comme reference publique non devinable.
- Proprietaire: Feature Management.
- Cycle de vie: draft/active/suspended/closed/deleted lorsque applicable; les transitions sont auditees.
- Relations: uniquement via references explicites, jamais par interpretation d'un message libre.
- Donnees obligatoires: identifiant, proprietaire metier, statut, horodatages, source.
- Donnees sensibles: toute donnee personnelle, financiere, juridique, localisation precise ou document prive.
- Source de verite: repository du domaine proprietaire.
- Suppression: suppression logique si audit requis; purge physique selon politique de retention.
- Historisation: AuditEvent pour changement significatif.
- Consentement: requis avant partage a un tiers ou usage hors finalite initiale.

### AuditEvent
- Definition: objet canonique `AuditEvent` gere par Audit and Observability.
- Identifiant: UUID ou identifiant technique stable expose comme reference publique non devinable.
- Proprietaire: Audit and Observability.
- Cycle de vie: draft/active/suspended/closed/deleted lorsque applicable; les transitions sont auditees.
- Relations: uniquement via references explicites, jamais par interpretation d'un message libre.
- Donnees obligatoires: identifiant, proprietaire metier, statut, horodatages, source.
- Donnees sensibles: toute donnee personnelle, financiere, juridique, localisation precise ou document prive.
- Source de verite: repository du domaine proprietaire.
- Suppression: suppression logique si audit requis; purge physique selon politique de retention.
- Historisation: AuditEvent pour changement significatif.
- Consentement: requis avant partage a un tiers ou usage hors finalite initiale.
