# LAWIM

# 06-DATABASE-REFERENCE.md

# Référentiel officiel de la base de données

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le présent document définit le modèle de données officiel de LAWIM.

Il constitue la référence unique pour :

* la structure logique des entités ;
* les relations entre objets métier ;
* les règles d'unicité ;
* les index fonctionnels ;
* les cycles de vie des enregistrements ;
* l'archivage des données ;
* la cohérence avec Prisma et PostgreSQL.

---

# CHAPITRE 2 — PRINCIPE FONDAMENTAL

Chaque donnée métier possède :

* un propriétaire fonctionnel ;
* un cycle de vie ;
* un niveau de sensibilité ;
* une règle d'archivage ;
* une règle de traçabilité.

La base de données persiste la vérité opérationnelle, mais ne définit pas seule les règles métier.

---

# CHAPITRE 3 — RÉFÉRENCES OBLIGATOIRES

Le modèle de données applique obligatoirement :

* 00-CONSTITUTION.md ;
* 01-GLOSSAIRE.md ;
* 02-PROPERTY-REFERENCE.md ;
* 02H-ATTRIBUTE-CATALOG.md ;
* 02I-PRICING-REFERENCE.md ;
* 03-CONVERSATION-REFERENCE.md ;
* 04-MATCHING-REFERENCE.md ;
* 05-WORKFLOW-REFERENCE.md ;
* 08-ROLE-REFERENCE.md ;
* 09-GEOLOCATION-REFERENCE.md ;
* 10-NOTIFICATION-REFERENCE.md ;
* 11-REPORTING-REFERENCE.md ;
* 14-STORAGE-REFERENCE.md.

---

# CHAPITRE 4 — PÉRIMÈTRE PRIS EN CHARGE

Le schéma officiel couvre notamment :

* l'identité ;
* les préférences ;
* les biens ;
* la géographie ;
* les demandes ;
* les leads ;
* les relations ;
* les messages ;
* les relances ;
* les offres de négociation ;
* les transactions ;
* les enquêtes de satisfaction ;
* les scores ;
* les audits ;
* les contacts ;
* les sessions de qualification ;
* les demandes de connexion ;
* les offres de services ;
* les achats de services ;
* les OTP ;
* les factures ;
* les opérations de paiement ;
* les webhooks de paiement ;
* les reçus de paiement ;
* les états de rapprochement ;
* les remboursements éventuels.

---

# CHAPITRE 5 — ENTITÉS D'IDENTITÉ

## User

Entité centrale représentant une personne physique ou un utilisateur de LAWIM.

## UserPreference

Préférences déclarées ou déduites pour guider les recherches et le matching.

## Contact

Contact métier lié ou non à un utilisateur.

## Introducer

Intermédiaire ou source d'introduction d'un bien ou d'un acteur.

## OtpChallenge

Challenge de vérification temporaire pour l'authentification par téléphone.

---

# CHAPITRE 6 — ENTITÉS IMMOBILIÈRES ET GÉOGRAPHIQUES

## Property

Représentation d'un bien immobilier.

## PropertyMedia

Média lié à un bien, avec règle potentielle de rétention.

## City

Ville ou commune de référence.

## Neighborhood

Quartier ou zone normalisée.

## GeoReference

Repère géographique générique.

Ces entités doivent être cohérentes avec le référentiel géographique et le catalogue d'attributs.

---

# CHAPITRE 7 — ENTITÉS DEMANDE ET MATCHING

## Request

Demande ou besoin immobilier structuré.

## Lead

Résultat de matching entre un bien et une demande.

## QualificationSession

Contexte de qualification conversationnelle multicanal.

## ConnectionRequest

Demande formelle de connexion entre une demande et un bien.

## ScoreSnapshot

Photographie historique d'un score calculé pour une entité.

---

# CHAPITRE 8 — ENTITÉS DE RELATION ET DE CONVERSATION

## Relationship

Relation opérationnelle ouverte après le matching et le double consentement.

## RelationshipMessage

Message échangé dans le cadre d'une relation.

## FollowUpEvent

Événement de relance ou de suivi.

## NegotiationOffer

Offre ou contre-offre de négociation.

Ces entités sont structurées pour préserver l'historique complet des échanges.

---

# CHAPITRE 9 — ENTITÉS DE TRANSACTION ET DE MONÉTISATION

## Transaction

Clôture commerciale ou locative issue d'une relation aboutie.

## SatisfactionSurvey

Retour structuré après transaction.

## ServiceOffering

Catalogue des services LAWIM facturables.

## Purchase

Achat d'un service LAWIM.

## Invoice

Pièce de facturation liée à un achat ou à un service.

## PaymentOperation

Opération de paiement liée à un service LAWIM, avec référence unique, montant, devise, prestataire et statut.

## PaymentWebhookEvent

Événement technique reçu d'un prestataire de paiement, notamment Campay.

## PaymentReceipt

Preuve de paiement émise après confirmation.

## PaymentReconciliation

État de rapprochement entre LAWIM et le prestataire de paiement.

## Refund

Remboursement éventuel rattaché à une opération de paiement.

La base de données ne doit jamais créer de commission transactionnelle inexistante.

---

# CHAPITRE 10 — ENTITÉS DE GOUVERNANCE

## AuditLog

Journal d'audit des actions significatives.

Cette entité doit conserver :

* l'action ;
* la cible ;
* l'acteur ;
* l'horodatage ;
* le motif ;
* les modifications.

---

# CHAPITRE 11 — RELATIONS MAJEURES

Les relations structurantes sont notamment :

* User -> Request ;
* User -> Lead ;
* User -> Relationship ;
* User -> Property ;
* Property -> PropertyMedia ;
* City -> Neighborhood ;
* Request -> Lead ;
* Lead -> Relationship ;
* Relationship -> RelationshipMessage ;
* Relationship -> FollowUpEvent ;
* Relationship -> NegotiationOffer ;
* Relationship -> Transaction ;
* Transaction -> SatisfactionSurvey ;
* User -> Purchase ;
* User -> Invoice ;
* User -> PaymentOperation ;
* Purchase -> PaymentOperation ;
* PaymentOperation -> PaymentWebhookEvent ;
* PaymentOperation -> PaymentReceipt ;
* PaymentOperation -> PaymentReconciliation ;
* PaymentOperation -> Refund.

Le modèle doit préserver l'intégrité référentielle.

---

# CHAPITRE 12 — UNICITÉ ET INDEXATION

Les contraintes d'unicité et les index doivent soutenir les usages métier.

Exemples :

* email unique pour `User` ;
* combinaison géographique unique pour certains enregistrements de propriété ;
* conversation key unique pour `QualificationSession` ;
* combinaison métier unique pour certains leads ;
* invoice number unique pour `Invoice` ;
* payment reference unique pour `PaymentOperation`.

Les index servent la recherche, le tri, le suivi et les audits.

---

# CHAPITRE 13 — CYCLE DE VIE ET ARCHIVAGE

Chaque entité suit un cycle de vie cohérent avec les workflows et le stockage.

Règles communes :

* création ;
* qualification ou validation ;
* utilisation ;
* archivage ;
* suppression ou conservation prolongée selon la politique de stockage.

Les suppressions définitives doivent être exceptionnelles et conformes au référentiel de stockage.

---

# CHAPITRE 14 — NORMALISATION DES DONNÉES

Les valeurs stockées doivent être normalisées par rapport :

* au glossaire ;
* au catalogue d'attributs ;
* au référentiel des biens ;
* au référentiel géographique.

Les libellés libres peuvent être conservés comme historique, mais les valeurs canoniques doivent rester la base de traitement.

---

# CHAPITRE 15 — CONFIDENTIALITÉ ET ACCÈS

Les données de la base ne sont accessibles qu'aux moteurs et rôles autorisés.

Les données sensibles incluent notamment :

* l'identité ;
* les coordonnées de contact ;
* les coordonnées géographiques sensibles ;
* les documents ;
* les historiques de messages ;
* les données financières ;
* les traces d'audit.

---

# CHAPITRE 16 — INTERACTIONS TECHNIQUES

Le schéma logique s'appuie sur :

* PostgreSQL pour la persistance ;
* Prisma pour le modèle applicatif ;
* le Storage Lifecycle Manager pour l'archivage ;
* le Reporting Engine pour les indicateurs ;
* le Dashboard Engine pour l'affichage ;
* le Matching Engine pour les scores ;
* le Workflow Engine pour les transitions ;
* le Notification Engine pour les événements.

La base de données ne doit pas abriter de logique métier non documentée.

---

# CHAPITRE 17 — INTERNATIONALISATION ET STATUTS DE PAIEMENT

Le schéma officiel doit également couvrir les structures de support multilingue :

## Language

Langue officielle de travail.

## LanguagePreference

Préférence de langue liée à un utilisateur, une session ou un appareil.

## BusinessDictionary

Référentiel des concepts métier multilingues.

## BusinessConcept

Concept canonique avec synonymes, variantes et poids sémantique.

## Translation

Traduction effective d'une clé fonctionnelle.

## TranslationKey

Clé stable utilisée dans les interfaces et notifications.

## TranslationVersion

Historique versionné d'une traduction.

## TranslationSource

Source validée d'une traduction.

## Localization

Paramètres régionaux, formats, devise et fuseau horaire.

## Synonym

Synonyme métier ou linguistique rattaché à un concept.

## BusinessAlias

Alias métier ou expression locale.

## BusinessExpression

Expression libre reconnue par le moteur conversationnel ou le moteur de recherche.

## LanguageStatistics

Statistiques d'usage par langue.

## LanguageUsage

Traçabilité de l'usage d'une langue par contexte.

## TranslationHistory

Historique complet des changements de traduction.

Les paiements doivent utiliser une taxonomie unique :

* `PAYMENT_CREATED` ;
* `PAYMENT_INITIATED` ;
* `PAYMENT_PENDING` ;
* `PAYMENT_CONFIRMED` ;
* `PAYMENT_FAILED` ;
* `PAYMENT_CANCELLED` ;
* `PAYMENT_EXPIRED` ;
* `PAYMENT_REFUNDED` ;
* `PAYMENT_RECONCILED` ;
* `PAYMENT_DISPUTED`.

La correspondance avec les statuts techniques Campay doit être explicite, documentée et testée.

---

# CHAPITRE 18 — TRACKING MARKETING, ATTRIBUTION ET ANALYTICS

Le modèle de données de LAWIM doit intégrer une couche transverse de tracking marketing sans créer de logique métier parallèle.

## ExternalChannel

Canal externe de diffusion ou d'entrée de trafic.

Exemples :

* Facebook ;
* WhatsApp ;
* Telegram ;
* Instagram ;
* TikTok ;
* Email ;
* SMS ;
* QR Code ;
* site partenaire ;
* site LAWIM.

## ExternalCampaign

Campagne marketing structurée avec les attributs suivants :

* campaignId ;
* campaignName ;
* campaignType ;
* campaignObjective ;
* campaignOwner ;
* campaignStatus ;
* budget éventuel ;
* startDate ;
* endDate.

## ExternalPublication

Publication marketing ou de diffusion avec les attributs suivants :

* publicationId ;
* trackingCode ;
* campaignId ;
* actorId ;
* actorRoleAtPublication ;
* actorCurrentRoles ;
* organizationId éventuel ;
* agencyId éventuel ;
* teamId éventuel ;
* channel ;
* title ;
* content ;
* language ;
* propertyId éventuel ;
* serviceId éventuel ;
* createdAt ;
* publishedAt ;
* status.

## TrackingCode

Clé unique de traçabilité.

Format officiel :

* `FB-LAWIM-000128-2026-06-001` ;
* `WA-LAWIM-000014-2026-06-014` ;
* `TG-LAWIM-000045-2026-07-003`.

Le Tracking Code est stable, lisible, partageable et immuable après création.

## LeadSource

Source d'origine d'un lead.

## LeadAttribution

Attribution analytique d'un lead ou d'une conversion.

La table doit pouvoir conserver :

* first_touch ;
* last_touch ;
* multi_touch ;
* LAWIM Attribution ;
* attributionWindow ;
* déduplication ;
* référence à la campagne, à la publication, au canal, à l'acteur et à la conversion.

## RedirectLog

Journal de redirection conservant notamment :

* trackingCode ;
* date ;
* heure ;
* session ;
* device ;
* browser ;
* operatingSystem ;
* country ;
* city ;
* zone LAWIM ;
* language ;
* sourceUrl ;
* targetUrl ;
* isBot ;
* isDuplicate ;
* consentStatus.

Aucune donnée personnelle inutile ne doit être conservée.

## ConversionEvent

Événement de conversion pouvant être relié au canal, à la campagne, à la publication, à l'acteur, au bien, au service, à la conversation, au matching, à la visite et au paiement Campay éventuel.

## CampaignPerformance

Agrégats de performance par campagne.

## ChannelPerformance

Agrégats de performance par canal.

## ActorPerformance

Agrégats de performance par acteur immuable.

## PublicationPerformance

Agrégats de performance par publication.

## MarketingAnalytics

Vue analytique transverse permettant de recalculer les statistiques à partir des événements historisés.

Les statistiques doivent rester recalculables par jointure.

---

# CHAPITRE 19 — OBJECTIF FINAL

Le modèle de données de LAWIM doit rester lisible, traçable, normalisé et évolutif, tout en servant directement les besoins du matching, de la conversation, des transactions, de l'archivage, du tracking marketing et du pilotage de la plateforme.

---

# FIN DU DOCUMENT

Le présent **06-DATABASE-REFERENCE.md** constitue la référence officielle du modèle de données de LAWIM.
