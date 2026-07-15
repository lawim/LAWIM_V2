# HERITAGE GLOSSARY — Glossaire LAWIM

**Sources :** LAWIM `Directive/01-GLOSSAIRE.md`, LAWIMA, ancienne_structure
**Principe :** Glossaire des termes métier LAWIM — sans validation

---

## A

**Accompagnement** : Service payant (50 000 FCFA) d'assistance personnalisée pour la recherche ou la vente d'un bien immobilier.

**Acheteur** : Utilisateur cherchant à acquérir un bien immobilier. Score de base : 60.

**Agent** : Professionnel de l'immobilier inscrit sur LAWIM. Reçoit des leads par zone géographique. Noté par les clients (1-5).

**Agence** : Structure professionnelle employant des agents. Peut gérer plusieurs agents et voir tous les leads.

**Alias** : Variante orthographique ou synonyme d'un nom de lieu ou de type de bien. Stocké dans les fichiers `district_aliases.json` ou `search_aliases.json`.

**Anonymisation** : Processus RGPD de suppression des données personnelles d'un utilisateur. Déclenché par la commande `SUPPRIMER MES DONNÉES`. Délai : 7 jours.

**Anti-spam** : Système de limitation du nombre de messages par minute (10 msg/min). Blocage automatique pour 60 minutes.

**Archivage** : Passage d'une propriété en statut archivé après 90 jours d'inactivité.

## B

**Boost** : Option payante permettant d'augmenter la visibilité d'une propriété ou d'accélérer le matching.

**Budget** : Montant qu'un utilisateur est prêt à dépenser pour un bien. Extrait automatiquement des messages au format k, mille, ou chiffres.

**Broker** : Courtier ou intermédiaire non-agréé par LAWIM. Détecté par des mots-clés spécifiques ("je peux trouver", "j'ai un contact").

## C

**CamPay** : Service de paiement mobile camerounais intégré (feature flag désactivé dans le backup).

**Champ obligatoire** : Information minimale requise pour qualifier une demande (type de bien, ville, budget).

**City match** : Correspondance au niveau de la ville dans le matching (pondération : 30%).

**Closing** : Techniques de conclusion de vente (documentées dans le sales playbook).

**Cold** : Classe de lead à faible priorité (score < 40 en V1, < 0.3 en V5). Action : demander budget.

**Commande** : Mot-clé spécial envoyé par l'utilisateur (SIGNALER, SUPPRIMER MES DONNÉES, ACCOMPAGNEMENT, STATS, LANGUE, etc.).

**Complétude** : Score de qualité d'une propriété basé sur la présence et la qualité des champs (60% du Data Quality Score).

**Confiance** : Score de fiabilité d'une source de données (agent=90, google_form=85, import=70, whatsapp=50, unknown=30).

**Constitution** : Document fondamental de LAWIM définissant les 23 principes du projet.

**Crédit** : Solde d'un agent pour l'achat de leads. Prix par lead par défaut : 500 FCFA.

## D

**Data Quality Engine** : Module d'évaluation de la qualité des données immobilières (score sur 100, grades A+ à D).

**Demandeur** : Rôle de base d'un utilisateur cherchant un bien (niveau 1).

**Diaspora** : Camerounais vivant à l'étranger. Détecté par localisation ou indicatif téléphonique. Score boosté (+25).

**Diaspora investor** : Investisseur de la diaspora. Score de base le plus élevé (95).

**Dispute** : Litige utilisateur. Créé par la commande SIGNALER. Statuts : open, resolved.

**District** : Niveau de la hiérarchie territoriale camerounaise (entre commune/ville et quartier).

**Doublon** : Personne ou propriété enregistrée plusieurs fois. Détecté par téléphone, email ou similarité de nom.

## E

**Entity linking** : Résolution d'entités (correspondance entre termes équivalents, synonymes, abréviations).

**Escalade** : Règle de dialogue définissant quand passer d'une réponse IA à un humain.

**État** : Statut d'une propriété (available, pending, rented, sold, archived) ou d'un utilisateur (NEW_USER à INACTIVE).

## F

**Famille de biens** : Catégorie principale de bien immobilier (Résidentiel, Commercial, Industriel, Terrain, Agricole, Hôtellerie, Projet).

**Feature flag** : Interrupteur de fonctionnalité. Permet d'activer/désactiver des fonctionnalités sans déploiement.

**Feedback** : Évaluation de l'utilisateur (👍 = 5, 👎 = 1, note de 1 à 5).

**Fiabilité** : Score de confiance d'une source de données (40% du Data Quality Score).

**Flow** : Séquence d'étapes de qualification pour une intention donnée.

**Follow-up** : Système de relance automatique à J1, J7, J30, J90.

## G

**Grade** : Note de qualité (A+ ≥80, A ≥60, B ≥40, C ≥20, D <20).

**GreenAPI** : Fournisseur de l'API WhatsApp utilisé par LAWIM.

## H

**Hiérarchie territoriale** : Structure administrative du Cameroun (Pays → Région → Département → Arrondissement → Commune → Ville → District → Quartier).

**Hot** : Classe de lead prioritaire (score ≥ 80 en V1, ≥ 0.8 en V5). Action : appeler immédiatement.

## I

**Identity resolution** : Détection et fusion des personnes enregistrées en double.

**Intention** : Type de besoin exprimé par l'utilisateur (buy, rent, sell, search, investor, visit, etc.).

**Intermédiaire** : Positionnement de LAWIM — mise en relation sans commission.

**Investisseur** : Utilisateur cherchant un investissement immobilier. Score de base : 80.

## J

## K

**Knowledge entry** : Unité de connaissance dans la base de connaissances (type, valeur, synonymes, confiance, source).

**Knowledge builder** : Module de construction de profil utilisateur (32 champs extraits automatiquement).

**Knowledge enricher** : Module d'apprentissage automatique de nouvelles connaissances depuis les conversations.

## L

**Lead** : Opportunité commerciale générée par la qualification d'une conversation.

**Levenshtein** : Algorithme de distance utilisé pour la normalisation des noms de lieux (seuil max 3).

**Litige** : Réclamation utilisateur (voir Dispute).

**Locataire** : Utilisateur cherchant à louer. Score de base : 40.

**Localisation floue** : Expression approximative de localisation (barrage, carrefour, axe principal, non loin de).

**Long-term memory** : Mémoire des interactions au-delà de la session (rétention : 90 jours).

## M

**Master** : Super-administrateur LAWIM (niveau 7, permissions totales).

**Matching** : Processus d'appariement entre une demande (lead) et une offre (propriété).

**Mémoire** : Système de reconnaissance des utilisateurs récurrents avec 4 niveaux de familiarité (J1, J2, J3, J4).

**Multi-intention** : Capacité à détecter plusieurs intentions dans un même message (activée).

## N

**Neighborhood match** : Correspondance au niveau du quartier dans le matching (pondération : 25%).

**Niveau de confiance** : Score implicite de fiabilité d'un utilisateur (basé sur vérification téléphone, historique, notation).

**Notaire** : Professionnel juridique vers lequel LAWIM oriente pour les questions de droit immobilier.

## O

**Objection** : Réticence exprimée par un utilisateur (12 peurs acheteur, 8 peurs vendeur documentées).

**Omnicanal** : Stratégie multi-canal (WhatsApp principal, Telegram, Facebook, Dashboard).

**Opt-in** : Permission demandée à l'utilisateur avant de partager le contact d'un agent.

## P

**Permission** : Droit d'accès à une fonctionnalité du système. Associée à un rôle ou à un utilisateur spécifique.

**Pidgin** : Langue parlée au Cameroun, partiellement supportée (15 mots de détection).

**Pipeline** : Chaîne de traitement d'un message (normalisation → extraction → intention → scoring → classification → routage → réponse).

**Prix ferme** : Indication que le prix n'est pas négociable.

**Propriétaire** : Personne possédant un bien immobilier. État : PROPERTY_OWNER.

## Q

**Qualification** : Processus d'évaluation d'un lead (collecte d'informations, scoring, classification).

**Quartier** : Subdivision d'une ville. Données disponibles pour 10+ villes camerounaises.

## R

**Relance** : Message automatique envoyé à J1, J7, J30, J90 après un contact (voir Follow-up).

**Rematching** : Processus de ré-appariement après un échec ou un délai.

**Résolution d'identité** : Voir Identity resolution.

**RGPD** : Règlement Général sur la Protection des Données. Appliqué via la commande d'anonymisation.

**Rule engine** : Moteur de règles définissant le pipeline de traitement (5 versions documentées : V2 à V5).

## S

**Scoring** : Calcul du score de qualité d'un lead (0-100 ou 0-1 selon version).

**Search** : Intention de recherche (non spécifique achat/location).

**Seller** : Vendeur d'un bien immobilier. Score de base : 50.

**Signal** : Indicateur dans un message (urgence, prix, diaspora, broker, investisseur).

**Source** : Origine des données d'une propriété (agent, google_form, import, whatsapp).

**Spam** : Message indésirable. Pénalité de -50 dans le scoring. Blocage à 10 msg/min.

## T

**Tenant** : Locataire (terme anglais utilisé dans le code). Score de base : 40.

**Template** : Message type prédéfini (welcome, help, no_match, thanks, ask_name, ask_phone, stats).

**Titre foncier** : Document officiel de propriété. Boost matching : +10.

**Typo database** : Base de données des fautes d'orthographe courantes (villes, quartiers, types de biens, WhatsApp).

## U

**Urgence** : Signal d'immédiateté dans une demande. Boost de scoring : +20.

## V

**Variante orthographique** : Façon alternative d'écrire un nom de lieu (ex: bastos → basto, bastoss).

**Vendeur** : Personne mettant en vente un bien. Rôle distinct du propriétaire.

**Vice-master** : Super-administrateur adjoint (niveau 6). Peut gérer les permissions.

## W

**Warm** : Classe de lead moyenne priorité (score ≥ 60 en V1, ≥ 0.5 en V5). Action : envoyer des annonces.

**WhatsApp** : Canal de communication principal de LAWIM, via l'API GreenAPI.

## Z

**Zéro commission** : Principe fondamental de LAWIM — aucun frais sur les transactions immobilières.

**Zone** : Regroupement géographique pour le routage des leads vers les agents.

**Zone LAWIM** : Périmètre d'activité prioritaire défini par l'équipe.

---

*Document patrimonial — Aucune décision de reconstruction n'est prise ici.*
