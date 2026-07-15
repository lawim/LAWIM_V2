# RAPPORT D'EXTRACTION DU PATRIMOINE MÉTIER LAWIM

**Date :** 2026-07-15
**Source :** `/media/abel/Doc/Drive/d/LAWIM_BACKUP_20260608_125026/LAWIM/`
**Objectif :** Extraction exhaustive de toute la connaissance métier pour reconstruction

---

## 1. DOMAINE IMMOBILIER

### 1.1 Familles de biens (7 familles officielles)
Source : `02-PROPERTY-REFERENCE.md`, `02A` à `02G`

| Famille | Types inclus |
|---------|-------------|
| **Résidentiel** | chambre, chambre_moderne, studio, studio_meuble, appartement, appartement_meuble, duplex, maison, villa, immeuble_residentiel, mini_cite, residence |
| **Commercial** | boutique, bureau, local commercial, showroom, restaurant, espace de service, cellule commerciale, surface de vente, plateau commercial |
| **Industriel** | entrepôt, dépôt, usine, atelier, plateforme logistique, site de production, local de stockage lourd, espace technique |
| **Foncier** | terrain nu, parcelle, lot, terrain titré, terrain non titré, terrain à bâtir, terrain viabilisé, terrain agricole urbain, terrain de réserve |
| **Agricole** | ferme, plantation, verger, ranch, serre, parcelle agricole, exploitation rurale, domaine agricole |
| **Hôtelier** | hôtel, guesthouse, lodge, aparthotel, résidence hôtelière, appartement de service, hébergement meublé de courte durée |
| **Projet immobilier** | projet résidentiel, projet commercial, projet mixte, lotissement, programme neuf, construction en cours, opération de promotion, pré-commercialisation |

### 1.2 Attributs canoniques des biens
Source : `02H-ATTRIBUTE-CATALOG.md`

**Attributs d'identité :** user, demandeur, proprietaire, introduceur, detenteur, agent_immobilier, agence_immobiliere, gestionnaire, partenaire, membre_lawim, administrateur, notaire

**Attributs métier immobiliers :**
- `famille_bien` : residentiel, commercial, industriel, agricole, hotelier, mixte
- `type_bien_residentiel` : chambre, chambre_moderne, studio, studio_meuble, appartement, appartement_meuble, duplex, maison, villa, immeuble_residentiel, mini_cite, residence
- `operation` : vente, location, location_meublee, bail_professionnel, bail_commercial
- `standing` : standard, good, premium, vip, exclusive, luxury
- `disponibilite` : immediate, aujourd_hui, cette_semaine, ce_mois, date_precise
- `statut_bien` : created, qualified, published, deactivated, sold, archived
- `statut_demande` : draft, active, paused, converted, archived

**Attributs complémentaires :**
- budget_min, budget_max (numérique)
- superficie (m²)
- chambres, salles_de_bain (entier)
- parking : aucun, moto, 1_vehicule, 2_vehicules, 3_plus
- securite : aucune, gardien, barriere, cloture, videosurveillance
- amenity : forage, compteur_eneo, compteur_camwater, balcon, jardin, piscine, climatisation, internet
- type_douche : interne, externe, partagee
- type_cuisine : interne, externe, kitchenette
- acces : independant, partagé
- mobilier : meuble, non_meuble
- source_origine : annonce, saisie_directe, import, relation, partenaire, autre

**Attributs de prix :** prix_vente, loyer, caution, avance_loyer, mensualite, frais_service, devise, taxe_estimee, estimation_prix, fourchette_marche, historique_prix, variation_prix

**Attributs juridiques :** mandat, procuration, titre_foncier, rccm, numero_contribuable, piece_identite, contrôle_documentaire, visite, transaction

### 1.3 Statuts de bien (cycle de vie complet)
Source : `05-WORKFLOW-REFERENCE.md` Partie 3

États officiels : Création → Qualification → Validation → Publié → Disponible → Matching → Visites → Négociation → Réservé → Transaction → Indisponible → Réactivation éventuelle → Archivé

Valeurs de disponibilité : Disponible, Réservé, Sous négociation, Sous compromis, Loué, Vendu, Suspendu, Archivé

### 1.4 Règles de propriété (property rules)
Source : `REFERENCE/07-BUSINESS-RULES.md`

- "Meublé" est un modificateur, pas un type autonome
- Propriété, disponibilité et documents doivent rester visibles dans le workflow
- Un bien peut être : publié, mis à jour, mis en pause, réactivé, archivé
- Un bien peut être boosté sans changer son trust score ou verification score
- Une transaction peut exister même si les documents sont encore en attente
- Une transaction peut exister même si les paiements sont encore en attente

### 1.5 Status de titre foncier (title_status)
Source : `KNOWLEDGE/title_status/title_status.json`

Valeurs officielles : titre_foncier, attestation, concession, certificat_occupation, non_documente

### 1.6 Synonymes et alias de types de biens
Source : `KNOWLEDGE/search_aliases/search_aliases.json`

- terrain → parcelle, foncier, terrain nu, ground, plot, land, terre
- villa → maison luxe, maison de standing, luxury house, mansion, grande maison
- maison → house, bungalow, maison entière, maison complète
- appartement → appart, flat, apartment, appart meublé, appartement meublé
- duplex → two-story, two storey, duplex moderne
- bureau → office, professional office, bureau pro
- commerce → boutique, shop, local commercial, boutique commerciale
- immeuble → building, building cameroun, immeuble de rapport
- entrepôt → warehouse, dépôt, stockage, magasin stockage
- studio → one-room, studio meublé, cosy

### 1.7 Biens meublés (champs supplémentaires)
Source : `KNOWLEDGE/minimum-fields-property.md`

Champs additionnels : inventaire, état du mobilier, caution, entretien, nettoyage, remplacement en cas de casse, photos du mobilier

---

## 2. DOMAINE GÉOGRAPHIQUE

### 2.1 Hiérarchie territoriale
Source : `09-GEOLOCATION-REFERENCE.md`

Pays → Région → Département → Arrondissement → Commune → Ville → Quartier → Secteur → Point de repère → Coordonnées GPS

LAWIM ne suppose jamais que tous les niveaux sont disponibles.

### 2.2 Niveaux de précision géographique (6 niveaux)
Source : `09-GEOLOCATION-REFERENCE.md`

Niveau 1: Pays | Niveau 2: Ville/commune | Niveau 3: Quartier | Niveau 4: Secteur/point de repère | Niveau 5: Adresse précise | Niveau 6: Coordonnées GPS

### 2.3 Niveaux de visibilité de localisation (6 niveaux)
Source : `09-GEOLOCATION-REFERENCE.md` Partie 3

Niveau 1: Ville uniquement | Niveau 2: Ville + quartier | Niveau 3: Quartier + secteur | Niveau 4: Position approximative carte | Niveau 5: Adresse complète | Niveau 6: Coordonnées GPS exactes

### 2.4 Zones LAWIM
Source : `09-GEOLOCATION-REFERENCE.md`

- Bassin immobilier cohérent utilisé pour la recherche, matching et analyse territoriale
- Indépendantes des limites administratives
- Peuvent regrouper : un quartier, plusieurs quartiers, une partie d'un quartier, plusieurs communes, une agglomération
- Une Zone LAWIM peut être découpée en secteurs

### 2.5 Matrice d'affinité géographique
Source : `09-GEOLOCATION-REFERENCE.md`

Chaque quartier possède une matrice d'affinité identifiant automatiquement :
- les quartiers équivalents
- les quartiers voisins
- les quartiers complémentaires

Exemple : Bastos → suggestions Golf, Dragages, Bastos Sud

### 2.6 Villes officielles (avec priority_rank)
Source : `KNOWLEDGE/LAWIM_MASTER_DATASET.json`

| City ID | Ville | Région | Priorité |
|---------|-------|--------|----------|
| CM-YDE | Yaoundé | Centre | 1 |
| CM-DLA | Douala | Littoral | 2 |
| CM-GOU | Garoua | Nord | 3 |
| CM-BFS | Bafoussam | Ouest | 4 |
| CM-BUE | Buea | Sud-Ouest | 5 |
| CM-KRI | Kribi | Sud | 6 |
| CM-LIM | Limbe | Sud-Ouest | 7 |
| CM-NKS | Nkongsamba | Littoral | 8 |

### 2.7 Points de repère reconnus
Source : `09-GEOLOCATION-REFERENCE.md`

Carrefour, Marché, Hôpital, École, Université, Station-service, Mairie, Chefferie, Église, Mosquée, Centre commercial

Aussi : village, lieu-dit, carrefour, station-service, école, université, chefferie, marché, église, mosquée (pour environnements sans adresse postale)

### 2.8 Quartiers de Yaoundé (avec profils marché)
Source : `KNOWLEDGE/LAWIM_MASTER_DATASET.json`

**Bastos** (haut standing) : Ambassade France, Ambassade USA, Mont Febe ; cible diaspora, expat, diplomate, investisseur ; biens typiques : villa, duplex, furnished_apartment, penthouse

**Melen** (étudiant) : Université Yaoundé I, Campus Ngoa-Ekelle, Polytech, CHUY ; cible étudiants, jeunes actifs, démarcheurs ; biens typiques : studio, chambre, mini-studio

**Autres quartiers** : Mvan, Messa, Etoudi, Nlongkak, Mokolo, Biyemassi, Oyer, Mendong, Odza, Simbock

### 2.9 Quartiers de Douala
Source : `KNOWLEDGE/immobilier_cameroun.json`

Bonapriso, Akwa, Bonamoussadi, Makepe, Logbessou, Deido, Ndokoti, Bonaberi, Bonanjo

### 2.10 Alias et fautes de villes
Source : `KNOWLEDGE/LAWIM_MASTER_DATASET.json`

**Yaoundé** alias : Ongola, Yaounde Ville, Yde, Siège des institutions, Cité des sept collines
Fautes : yaounde, younde, yaoundé, yade, yaounder, yand
Variants sociaux : yaounde237, yde237, ongola237

**Douala** alias : Dla, Capitale économique, Douala Ville, Cité des Sawa
Fautes : douala, doula, dola, doull, doala

**Buea** alias : Buea Town, UB City, Munya
**Limbe** alias : Victoria, L-Town
**Kribi** alias : Kribi Beach, Kribi Port, Kribi Centre, Cité balnéaire

---

## 3. DOMAINE QUALIFICATION (profils utilisateurs, champs)

### 3.1 Champ critique universel
Source : `KNOWLEDGE/qualification-implementation-backlog.md`

Toute demande et tout bien nécessite : type de transaction, type de bien, localisation, budget
Statuts si incomplet : `INCOMPLETE`, `MISSING_CORE_FIELDS`

### 3.2 Ordre de qualification
Source : `KNOWLEDGE/qualification-implementation-backlog.md`, `REFERENCE/02-CONVERSATION.md`

1. Transaction (intention)
2. Type de bien
3. Ville
4. Quartier ou zone
5. Budget
6. Contraintes de base liées à l'intention
7. Champs spécifiques au bien
8. Confort et préférences
9. Confiance, documents et disponibilité
10. Confirmation ou escalade

### 3.3 Champs obligatoires par type de demande
Source : `KNOWLEDGE/minimum-fields-request.md`

**Commun à toute demande :** transaction, ville, quartier/zone, type de bien, budget, délai/disponibilité, contact, canal préféré, urgence (recommandé)

**Location :** ville, quartier, type de bien, budget mensuel, nombre de chambres, nombre de douches, délai, meublé/non meublé, contact

**Achat :** ville, quartier/zone, type de bien, budget total, surface/nbre pièces, usage, urgence, préférence documents/titre, contact

**Terrain :** ville, quartier/axe, surface souhaitée, budget, usage, documents souhaités, accessibilité, délai, contact

**Commercial :** ville, quartier/zone, type de local, surface, budget, usage autorisé, disponibilité, contact

**Investissement :** ville, type de bien, budget, horizon placement, niveau de risque, stratégie, contact

### 3.4 Champs obligatoires par type de publication de bien
Source : `KNOWLEDGE/minimum-fields-property.md`

**Commun à tout bien :** transaction, type de bien, ville, quartier/zone, prix, disponibilité, photos, contact, description courte, documents/titre (recommandé pour vente et terrain)

### 3.5 Champs critiques par type de bien (Niveau 2)
Source : `KNOWLEDGE/qualification-implementation-backlog.md`

- **Studio/chambre :** loyer, quartier, meublé/non meublé, douche, cuisine, disponibilité
- **Appartement :** loyer/prix, chambres, douches, salon, étage, parking, charges, meublé/non meublé
- **Maison/villa/duplex :** prix, chambres, douches, surface, cour, parking, sécurité, documents si vente
- **Terrain :** surface, prix global, prix au m², documents, lotissement, accessibilité, façade, usage prévu
- **Bureau :** surface, loyer, accessibilité, parking, disponibilité
- **Boutique/magasin :** usage, visibilité, flux piéton, surface, loyer, parking, accessibilité
- **Entrepôt :** surface, accès poids lourds, hauteur, sécurité, loyer
- **Immeuble :** nombre de niveaux, nombre d'unités, revenus générés, occupation, documents, prix

### 3.6 Champs interdits / à ne pas demander
Source : `REFERENCE/02-CONVERSATION.md`, `REFERENCE/07-BUSINESS-RULES.md`

- "Nombre de pièces ?" comme question principale pour du résidentiel
- "Standing ?" comme question obligatoire
- "Avez-vous un autre critère important à ajouter ?" (question fourre-tout)
- Pour un terrain : ne pas demander chambres, douches, salon, pièces, standing
- Pour un studio/chambre : ne pas demander nombre de chambres
- Piscine comme critère principal pour un terrain

---

## 4. DOMAINE INTENTIONS

### 4.1 Intentions officielles
Source : `KNOWLEDGE/intents/`

**BUY_PROPERTY** (priorité VERY_HIGH, poids lead score: 50)
- Mots-clés : acheter, achat, propriétaire, terrain, villa, immeuble
- Expressions FR : je veux acheter, terrain à vendre, je cherche une maison à acheter, je veux devenir propriétaire
- Expressions EN : i want to buy, looking to purchase, house for sale, land for sale
- Expressions Pidgin : i wan buy house, i wan buy land, which land dey available
- Patterns budget : 5M, 10M, 20M, 50M, 100M, budget 30 millions
- Purchase signals : titre foncier, documents, notaire, proprio direct, terrain titré

**RENT_PROPERTY** (priorité HIGH, poids lead score: 30)
- Mots-clés : louer, location, logement, appartement, maison, studio
- Expressions FR : je veux louer, je cherche une maison, besoin d'un appartement, location urgente
- Expressions EN : looking for apartment, need house urgently, want to rent
- Expressions Pidgin : i di find house, i wan rent house, house dey ?

**SELL_PROPERTY** (priorité VERY_HIGH, poids lead score: 60)
- Mots-clés : vendre, vente, céder, terrain, maison, villa
- Expressions FR : je vends, maison à vendre, terrain à vendre, vente urgente, propriétaire direct
- Expressions EN : house for sale, land for sale, selling property, looking for buyer
- Expressions Pidgin : i di sell house, i get land for sale, buyer dey ?
- Seller signals : proprio, titre foncier, vente urgente, dernier prix, prix négociable

**SEARCH_PROPERTY** et **INVESTOR_INTENT** également présents dans le dossier intents/

### 4.2 Classification des intentions
Source : `KNOWLEDGE/immobilier_cameroun.json`

```json
"buy": ["cherche", "recherche", "veux", "achète", "acheter", "trouver", "acquérir", "recherch"]
"rent": ["loue", "location", "louer", "locataire", "loyer", "looking for", "i want to rent", "need a house", "rent a house", "looking to rent", "find house", "dey find", "need house", "want house", "i dey find", "we dey find"]
"sell": ["vends", "vendre", "propose", "cède", "cession"]
"urgence": ["urgent", "asap", "rapidement", "vite", "prompt", "urgence", "dernier", "dépêche", "immédiat", "ce week-end"]
```

### 4.3 Intentions par canal WhatsApp
Source : `KNOWLEDGE/whatsapp_language/whatsapp_language.json`

697 entrées multilingues (fr, en, pidgin) couvrant les intentions : buy, rent, sell, search, investor
Exemples Pidgin : "I di find land for Buea", "I wan buy duplex Buea 3 room", "Wetin price land Buea now", "House dey ?"

---

## 5. DOMAINE CONVERSATION

### 5.1 Règles de dialogue fondamentales
Source : `00-CONSTITUTION.md`, `03-CONVERSATION-REFERENCE.md`

- Comprendre avant de répondre
- Ne jamais poser une question inutile
- Ne jamais redemander une information déjà connue
- Ne jamais poser une question dont la réponse est déductible
- Commencer le matching dès que possible
- Ne jamais attendre une qualification complète pour agir
- Ton naturel
- Adapter les questions au contexte
- Ne jamais suivre un questionnaire fixe
- Comprendre les expressions camerounaises courantes
- Une seule question à la fois
- 1 à 3 phrases maximum par réponse
- Vocabulaire simple

### 5.2 Principes de la conversation
Source : `00-CONSTITUTION.md` Article 4

- **Principe 1** : Information déjà donnée = jamais redemandée
- **Principe 2** : Correction utilisateur remplace immédiatement l'ancienne valeur
- **Principe 3** : Ne jamais poser une question dont la réponse est déductible
- **Principe 4** : Rechercher en permanence les informations critiques dans les messages
- **Principe 5** : Matching commence dès que les infos critiques sont disponibles
- **Principe 6** : Pas de questionnaire fixe — suit uniquement les infos manquantes
- **Principe 7** : S'adapter aux usages camerounais (expressions locales prioritaires)
- **Principe 8** : Compatible avec les standards internationaux

### 5.3 Patterns de conversation
Source : `KNOWLEDGE/conversation-patterns.md`

| Pattern | Signaux typiques | Move système |
|---------|-----------------|--------------|
| Search/buy | "je cherche", "need house", budget, ville, quartier, type | Créer/affiner Request, rechercher et classer |
| Rent | Langage location, durée, taille ménage, budget, quartier | Qualifier durée, localisation, budget |
| Sell/listing | "je vends", détails bien, statut titre, disponibilité | Créer Property, valider ownership |
| Investor | ROI, cashflow, yield, return, rentable | Questions investisseur, priorité rendement/risque |
| Negotiation | "dernier prix", "prix négociable", "on peut s'entendre" | Context negotiation, jamais réduire au seul prix |
| Urgency | urgent, asap, today, before week end | Priorité augmentée, intervalle follow-up compressé |
| Chatty user | Conversation normale, questions annexes | Garder le fil, extraire signaux progressivement |
| Language switch | FR→EN ou FR→Pidgin | Changer langue sans redémarrer conversation |
| Title transparency | Statut titre, documents, preuve propriété | Afficher statut titre et vérification |
| Human transfer | Besoin approbation, incertitude, dispute | Transférer avec historique |

### 5.4 Questions autorisées
Source : `REFERENCE/02-CONVERSATION.md`

- C'est pour louer, acheter, vendre ou investir ?
- Quel type de bien cherchez-vous ?
- Dans quelle ville ?
- Quel quartier ou quelle zone ?
- Quel budget prévoir ?
- Combien de chambres ?
- Combien de douches ?
- Meublé ou non meublé ?
- A partir de quand voulez-vous avancer ?
- Le terrain est titré et loti ?
- Quel usage prévoyez-vous ?

### 5.5 Questions interdites
Source : `REFERENCE/02-CONVERSATION.md`, `REFERENCE/07-BUSINESS-RULES.md`

- "Avez-vous un autre critère important à ajouter ?" (fourre-tout)
- "Comme le nombre de pièces ou le standing ?"
- "Nombre de pièces ?" comme question principale
- "Standing ?" comme question principale
- Toute question qui répète un champ déjà capturé
- Questions qui poussent un catch-all générique
- "standing" comme question systématique

### 5.6 Règles de correction et continuité
Source : `REFERENCE/02-CONVERSATION.md`, `REFERENCE/03-PROPERTY-QUALIFICATION.md`

- Si l'utilisateur change de ville → mettre à jour la fiche active, effacer le contexte quartier
- Si l'utilisateur change de type de bien → réinitialiser les champs dépendants
- Si l'utilisateur change de budget → mettre à jour immédiatement
- Si l'utilisateur corrige une valeur → la correction écrase l'ancienne
- Ne pas fusionner une correction avec une ancienne requête
- Ne pas laisser un ancien budget remplacer la dernière valeur explicite

### 5.7 Critères d'arrêt de la qualification
Source : `REFERENCE/02-CONVERSATION.md`

Arrêter la qualification tôt quand :
- La ville n'est pas couverte par le workflow actif
- L'inventaire est vide
- L'utilisateur demande un humain
- Le fil devient répétitif ou confus
- L'utilisateur commence clairement une nouvelle demande

### 5.8 Gestion de la mémoire conversationnelle
Source : `REFERENCE/02-CONVERSATION.md`

- Garder l'archive complète
- Réutiliser la fenêtre de contexte récente pour la réponse active
- Résumer seulement quand le fil devient trop long
- Ne jamais perdre l'identité métier de la demande
- Un nouveau message = une réponse, pas plusieurs réponses parallèles

### 5.9 Règles de collecte
Source : `KNOWLEDGE/minimum-fields-request.md`

- Ne pas demander tous les champs d'un coup
- Ne pas demander les options avant les obligations
- Ne pas bloquer une demande simple sur un détail cosmétique
- Ne pas envoyer vers équipe humaine si une question courte suffit
- Escalader dès que le titre, l'usage ou la priorité restent flous

---

## 6. DOMAINE MATCHING

### 6.1 Principes fondamentaux du matching
Source : `04-MATCHING-REFERENCE.md`

- Matching commence dès que les champs critiques sont connus
- Matching est dynamique (chaque nouvelle info peut modifier les résultats)
- Matching est permanent (continue tant que le dossier est actif)
- Matching apprend des décisions des utilisateurs
- Matching privilégie la satisfaction du demandeur (qualité > quantité)

### 6.2 Déclencheurs de matching
Source : `04-MATCHING-REFERENCE.md`

Automatique lors de : création dossier, correction, modification budget, changement ville, changement type de bien, publication nouveau bien, retour disponibilité, refus, visite, échec négociation

### 6.3 Quatre niveaux de compatibilité
Source : `04-MATCHING-REFERENCE.md` Partie 2

| Niveau | Description | Exemples |
|--------|-------------|---------|
| **1. Critique** | Champs critiques — sans, aucun matching possible | Type de bien, opération, localisation, budget |
| **2. Fonctionnelle** | Répond aux besoins principaux | Nbre chambres, superficie, budget |
| **3. Confort** | Appréciés mais non indispensables | Garage, forage, jardin, piscine, balcon, terrasse |
| **4. Préférentielle** | Préférences observées | Quartier préféré, orientation, vue, proximité école/travail |

### 6.4 Score de compatibilité global
Source : `04-MATCHING-REFERENCE.md` Partie 3

Le score global combine :
- Score Immobilier
- Score Géographique
- Disponibilité
- Documents
- Qualité
- Fiabilité détenteur
- Probabilité de transaction

Score de 0 à 100. Si score < 60%, le bien n'est jamais proposé.

### 6.5 Score immobilier (pondérations générales)
Source : `04-MATCHING-REFERENCE.md` Partie 3

| Critère | Poids |
|---------|-------|
| Type de bien | 25% |
| Opération | 20% |
| Budget | 15% |
| Localisation | 15% |
| Caractéristiques critiques | 15% |
| Caractéristiques recommandées | 10% |

### 6.6 Score de disponibilité
Source : `04-MATCHING-REFERENCE.md`

- 100% : Disponible
- 70% : Réservation en cours
- 30% : Réponse propriétaire en attente
- 0% : Vendu/Loué/Archivé (jamais proposé)

### 6.7 Score documentaire
Source : `04-MATCHING-REFERENCE.md`

- Titre foncier : 100%
- En cours d'immatriculation : 80%
- Droit coutumier : 60%
- Documents inconnus : 40%

### 6.8 Pondérations par type de bien (détaillées)
Source : `04-MATCHING-REFERENCE.md` Partie 4

**Résidentiel individuel simple** (chambre, chambre moderne, studio, studio meublé) :
| Critère | Poids |
|---------|-------|
| Type exact du bien | 20% |
| Opération | 10% |
| Ville/quartier | 25% |
| Budget | 25% |
| Douche/cuisine/meublé | 10% |
| Disponibilité | 5% |
| Qualité infos | 5% |

**Appartement :**
| Critère | Poids |
|---------|-------|
| Type exact | 15% |
| Opération | 10% |
| Ville/quartier | 20% |
| Budget | 20% |
| Nbre chambres | 15% |
| Cuisine/douches | 8% |
| Parking/balcon/étage | 5% |
| Disponibilité | 4% |
| Qualité | 3% |

**Maison :**
| Critère | Poids |
|---------|-------|
| Type exact | 15% |
| Opération | 10% |
| Ville/quartier | 18% |
| Budget | 18% |
| Nbre chambres | 15% |
| Cour/clôture | 10% |
| Douches/cuisine | 6% |
| Parking/forage/dépendance | 5% |
| Qualité | 3% |

**Villa :**
| Critère | Poids |
|---------|-------|
| Type exact | 12% |
| Opération | 8% |
| Ville/quartier | 18% |
| Budget | 17% |
| Nbre chambres | 15% |
| Cour/clôture/barrière | 10% |
| Dépendance/garage | 8% |
| Forage/sécurité/groupe électrogène | 5% |
| Piscine/jardin/confort | 4% |
| Qualité | 3% |

**Terrain résidentiel/parcelle :**
| Critère | Poids |
|---------|-------|
| Type exact | 15% |
| Opération | 8% |
| Ville/zone | 18% |
| Prix/budget | 17% |
| Superficie | 15% |
| Situation juridique | 12% |
| Accès/distance axe principal | 7% |
| Eau/électricité proches | 4% |
| GPS/bornage/qualité | 4% |

**Boutique/kiosque/échoppe :**
| Critère | Poids |
|---------|-------|
| Type exact | 15% |
| Ville/quartier/marché | 25% |
| Budget | 20% |
| Surface | 10% |
| Position commerciale | 12% |
| Disponibilité | 8% |
| Électricité/sécurité | 5% |
| Qualité | 5% |

**Bureau/cabinet/coworking :**
| Critère | Poids |
|---------|-------|
| Type exact | 15% |
| Ville/quartier | 20% |
| Budget | 20% |
| Surface | 12% |
| Accessibilité | 10% |
| Parking | 8% |
| Internet/climatisation | 5% |
| Étage/ascenseur | 5% |
| Qualité | 5% |

**Entrepôt/hangar/dépôt :**
| Critère | Poids |
|---------|-------|
| Type exact | 15% |
| Zone | 15% |
| Budget | 15% |
| Surface | 20% |
| Accès camion | 12% |
| Hauteur/quai | 8% |
| Sécurité/clôture | 6% |
| Électricité/eau | 4% |
| Qualité | 5% |

**Hôtel/auberge/motel :**
| Critère | Poids |
|---------|-------|
| Type exact | 12% |
| Ville/quartier/axe | 15% |
| Prix | 15% |
| Nbre chambres/unités | 18% |
| État exploitation | 10% |
| Taux occupation/revenus | 10% |
| Parking/restaurant/services | 8% |
| Documents/autorisations | 5% |
| Qualité | 7% |

### 6.9 Règles de matching supplémentaires
Source : `04-MATCHING-REFERENCE.md`

- Ne jamais proposer > 5 biens lors d'un premier matching
- Éviter de proposer plusieurs biens quasiment identiques
- Tout bien refusé définitivement n'est jamais reproposé (sauf baisse importante de prix, modification majeure, changement du besoin)
- Le budget peut être légèrement dépassé si les autres critères sont excellents
- La localisation utilise la distance réelle (GPS) quand disponible
- Les détenteurs fiables (réactifs) sont privilégiés
- Le matching apprend : si 3 refus pour absence garage → garage devient prioritaire

### 6.10 Lead Scoring Rules
Source : `KNOWLEDGE/scoring/lead_scoring_rules.json`

Poids de scoring : budget=20, location=15, urgency=20, diaspora=10, phone=5, property_type=15, investment_profile=10

### 6.11 Scores V1 (historique)
Source : `KNOWLEDGE/master/05_SCORING_V1.md`, `KNOWLEDGE/master/04_MATCHING_V1.md`

Scores : Opportunity Score, Trust Score, Quality Score, Freshness Score, Conversion Score
Matching V1 : Géographie, Budget, Standing, Mobilité, Flexibilité, Fraîcheur, Réalisme

---

## 7. DOMAINE CRM / RÔLES / ACTEURS

### 7.1 Familles de rôles
Source : `08-ROLE-REFERENCE.md` Partie 3

**Utilisateurs :** Demandeur, Détenteur, Propriétaire
**Professionnels :** Agent immobilier, Responsable d'agence, Administrateur d'agence
**Partenaires :** Notaire partenaire, Géomètre partenaire, Banquier partenaire, Expert partenaire, Prestataire partenaire
**Équipe LAWIM :** Assistant, Conseiller, Médiateur, Responsable opérationnel, Administrateur, Administrateur principal

### 7.2 Rôle principal et rôles secondaires
Source : `08-ROLE-REFERENCE.md`

- Chaque utilisateur a un rôle principal (le plus élevé atteint)
- Peut avoir plusieurs rôles secondaires
- Pas de régression automatique
- Rétrogradation nécessite intervention humaine + motif + audit

### 7.3 Hiérarchie des autorités
Source : `08-ROLE-REFERENCE.md` Partie 7

Administrateur principal LAWIM → Administrateur → Responsable opérationnel → Conseiller/Médiateur → Responsable d'agence → Administrateur d'agence → Agent immobilier → Propriétaire/Détenteur → Demandeur

### 7.4 Évolution automatique des rôles
Source : `08-ROLE-REFERENCE.md` Partie 2

Demandeur → (publication d'un bien) → Propriétaire
Demandeur → (déclaration gestion bien) → Détenteur
Détenteur → (validation professionnelle) → Agent immobilier
Agent → (création agence validée) → Responsable d'agence

### 7.5 Permissions (5 niveaux)
Source : `08-ROLE-REFERENCE.md` Partie 4

Niveau 1: Lecture | Niveau 2: Création | Niveau 3: Modification | Niveau 4: Validation | Niveau 5: Administration

### 7.6 Trust Score (6 niveaux de confiance)
Source : `08-ROLE-REFERENCE.md` Partie 5

🔴 N1: Compte créé | 🟠 N2: Téléphone vérifié | 🟡 N3: Identité vérifiée | 🟢 N4: Documents pros validés | 🔵 N5: Pro/partenaire vérifié | ⭐ N6: Compte de référence

### 7.7 Badges officiels
Source : `08-ROLE-REFERENCE.md` Partie 5

📱 Téléphone vérifié, 📧 E-mail vérifié, 🪪 Identité vérifiée, 🏠 Propriétaire vérifié, 🏢 Agence vérifiée, 🤝 Partenaire LAWIM, ⭐ Professionnel vérifié

### 7.8 Acteurs CRM V1 (historique)
Source : `KNOWLEDGE/master/06_ACTORS_V1.md`, `KNOWLEDGE/master/02_CRM_V1.md`

Acteurs : Demandeur, Propriétaire/Vendeur, Agent Immobilier
(Gestionnaire = Agent Immobilier ; Promoteur = Propriétaire/Vendeur)

Flux CRM : Contact → Dossier Client → Opportunité → Match → Mise en relation → Follow-Up → Transaction

### 7.9 Documents de vérification
Source : `08-ROLE-REFERENCE.md` Partie 5

**Pour propriétaire :** titre foncier, acte de vente, attestation de propriété, mandat
**Pour agence :** CNI responsable, RCCM, numéro contribuable, autorisation d'exercice, justificatif adresse
**Pour partenaire :** selon profession

### 7.10 Compte unique
Source : `08-ROLE-REFERENCE.md`

- Chaque personne physique = un seul compte
- Le numéro de téléphone est l'identifiant principal
- Un compte peut cumuler plusieurs rôles
- Pas de partage de compte entre plusieurs personnes

---

## 8. DOMAINE NÉGOCIATION

### 8.1 Dynamiques de négociation marché camerounais
Source : `KNOWLEDGE/negotiation-patterns.md`

- Le marché fonctionne beaucoup par négociation
- Vendeur : prix ambitieux initial + marge intégrée ; attend que l'acheteur propose le premier prix
- Acheteur : négocie tôt après première offre ; compare comme levier
- Agence : preuve comme levier
- LAWIM accompagne la négociation — ne simule pas agent commercial agressif

### 8.2 Objections prix fréquentes
Source : `KNOWLEDGE/negotiation-patterns.md`

| Formulation | Signification | Réponse LAWIM |
|-------------|---------------|---------------|
| "Dernier prix ?" / "Combien dernier ?" | Test, curiosité | Contexte marché, discussion possible |
| "C'est négociable ?" | Ouverture | Honnêteté sur marge culturelle |
| "Trop cher" | Comparaison FB | Rester sur quartier demandé |
| "Pourquoi si bas ?" | Méfiance fraude | Vérification, pas accusation |

### 8.3 Expressions de négociation
Source : `KNOWLEDGE/whatsapp_language/negotiation.json`

dernier prix, prix ferme, prix négociable, à débattre, on peut s'entendre, best price, nego possible, combien dernier ?

### 8.4 Ton LAWIM en négociation
Source : `KNOWLEDGE/negotiation-patterns.md`

**À faire :** Reconnaître que négocier est normal, question utile sur budget/délai, contexte marché quartier, handoff si dispute, rester accompagnant
**À éviter :** "Prix ferme, non négociable" sans contexte, multiplier questions prix, ville voisine "moins cher", trancher comme juge, ton commercial agressif

### 8.5 Moments clés de la négociation
Source : `KNOWLEDGE/negotiation-patterns.md`

Annonce/premier contact → comparaison (pas négociation ferme) → Visite ou vidéo crédible → négociation s'intensifie → Preuves documents OK → offre/contre-offre → Validation famille/budget → conclusion ou abandon

### 8.6 Négociation et diaspora
Source : `KNOWLEDGE/negotiation-patterns.md`

Compare frais globaux, rejette pression, paiements échelonnés sécurisés, validation familiale avant offre ferme

---

## 9. DOMAINE LANGAGE / SYNONYMES / ALIAS

### 9.1 Synonymes autorisés (catalogue attributs)
Source : `02H-ATTRIBUTE-CATALOG.md`

- client → demandeur
- locataire → demandeur (selon contexte)
- acheteur → demandeur (selon contexte)
- propriétaire mandaté → détenteur
- agence → agence_immobiliere
- location meublée → location_meublee
- bail pro → bail_professionnel
- TF → titre_foncier
- yaounde / yde → Yaoundé
- douala centre / centre ville → quartier ou zone

### 9.2 Entity Linking (relations entre termes)
Source : `KNOWLEDGE/entity_linking/entity_linking.json`

Types de relations : equivalent_to, synonym, related_to, typo_of
Exemples : terrain ↔ parcelle (equivalent_to), villa ↔ maison de luxe (equivalent_to), climatisation ↔ AC (synonym), climatisation ↔ air conditionn (synonym)

### 9.3 Base de fautes d'orthographe (typo database)
Source : `KNOWLEDGE/typo_database/`

Cinq fichiers couvrant les fautes de : villes, quartiers, types de biens, WhatsApp, et une base générale

### 9.4 Vocabulaire camerounais autorisé
Source : `REFERENCE/02-CONVERSATION.md`

Utiliser : chambres, douches, salons, quartier, zone, budget
Ne pas utiliser : "pièces" comme question principale résidentielle, "standing" comme question obligatoire

Expressions locales prioritaires : chambre moderne, mini-cité, droit coutumier, titre foncier, chambre avec douche, studio meublé

### 9.5 Langues supportées
Source : `00-CONSTITUTION.md` Article 23, `18-LAWIM-AI-REFERENCE.md`

LAWIM fonctionne nativement en : Français, English, Pidgin English
Support multilingue via : Business Dictionary, Translation, Language Detection, Multilingual Search

---

## 10. DOMAINE DATASETS

### 10.1 LAWIM_MASTER_DATASET.json
Source : `KNOWLEDGE/LAWIM_MASTER_DATASET.json` (8765 lignes)

Contient :
- Référentiel des villes (8 villes avec ID, région, priorité)
- Alias de villes (avec variantes sociales et fautes)
- Profils détaillés de quartiers (landmarks, references informelles, zones liées, profil marché)
- Quartiers couverts : Bastos, Melen, Mvan, Messa, Etoudi, Nlongkak, Mokolo, Biyemassi, Oyer, Mendong, Odza, Simbock (Yaoundé)
- Chaque quartier a : landmarks, informal_references, related_zones, market_profile (segment, target, common_properties)

### 10.2 immobilier_cameroun.json
Source : `KNOWLEDGE/immobilier_cameroun.json`

Mapping villes→quartiers, types de biens→synonymes, intentions→mots-clés, urgence→signaux

### 10.3 Jeux de données générés
Source : `KNOWLEDGE/generated/`

Sous répertoires : dataset_v1, dataset_v2, dataset_v3, intents_v1, neighborhoods_v1, vocabulary_v1, backups

### 10.4 Autres datasets JSON
- `geography/cameroon_geography.json` (géographie complète du Cameroun)
- `geography/district_aliases.json` (alias de districts/quartiers)
- `geography/district_hierarchy.json` (hiérarchie des districts)
- `geography/neighborhood_gps.json` (coordonnées GPS des quartiers)
- `geography/neighborhood_inventory.json` (inventaire des quartiers)
- `whatsapp_language/whatsapp_language.json` (697 entrées multilingues)
- `whatsapp_language/diaspora_language.json` (langage diaspora)
- `whatsapp_language/urgency_signals.json` (signaux d'urgence)
- `whatsapp_language/property_search.json` (langage recherche)
- `whatsapp_language/property_listing.json` (langage publication)
- `typo_database/typo_database.json` (base de fautes générale)

---

## 11. DOMAINE RÈGLES MÉTIER (transverses)

### 11.1 Règles absolues (Constitution)
Source : `00-CONSTITUTION.md`

- **Article 5** : Constitution = seule source officielle des règles métier. Code n'est qu'une implémentation.
- **Article 6** : Règle d'irréversibilité — pas d'ancienne logique pour compatibilité, pas de code mort
- **Article 7** : Hiérarchie : Constitution > Référentiel biens > Conversation > Matching > Workflow > DB > Code
- **Article 8** : Aucun développeur/IA/outil ne peut inventer une règle métier
- **Article 9** : Qualité = respect Constitution + pas de logique contradictoire + tests passent + données/workflows conformes

### 11.2 Règles de l'opération manual
Source : `DIRECTIVE/LAWIM-OPERATIONS-MANUAL.md`

- Organisation quotidienne : suivi tickets, partenaires, biens, réclamations, paiements, anomalies, priorités, urgences
- Support : répondre vite, clairement, tracer chaque demande, escalader cas sensibles, ne jamais promettre ce qui n'est pas validé
- Qualité : contrôler cohérence des annonces, vérifications, réponses, statuts, documents, services

### 11.3 Règles du Business Plan
Source : `DIRECTIVE/LAWIM-BUSINESS-PLAN.md`

- Sources de revenus : mise en relation, accès contact, visibilité premium, boost, vérification, assistance, photographie, vidéo, services partenaires, accompagnement diaspora, IA, publication
- Pas de commission immobilière
- Prix transparents, services explicites, consentement avant activation

### 11.4 Règles commerciales (Sales Playbook)
Source : `48-LAWIM-SALES-PLAYBOOK.md`

- Ne jamais promettre vente garantie, location garantie
- Ne jamais inventer un bien
- Ne jamais masquer les conditions
- Toujours présenter les services payants avant engagement
- Toujours respecter la confidentialité
- Toujours rappeler : aucune commission sur vente ou location

### 11.5 Contradictions résolues
Source : `REFERENCE/07-BUSINESS-RULES.md`

Ces patterns sont obsolètes :
- standing comme question obligatoire
- "pièces" comme question principale résidentielle
- substitution de ville avec une ville voisine
- un seul dashboard pour tous les rôles
- conversation qui redémarre après une correction

### 11.6 Règles de données et stockage
Source : `06-DATABASE-REFERENCE.md`, `REFERENCE/07-BUSINESS-RULES.md`

- Les données importantes sont archivées, pas supprimées physiquement
- L'archivage logique est préféré à la suppression destructive
- Le contexte historique doit rester reconstructible
- L'email est unique pour User
- Le numéro de téléphone est l'identifiant principal (vérifié par OTP)

### 11.7 SLA métier (délais)
Source : `05-WORKFLOW-REFERENCE.md` Partie 2

| Type de bien | Premier matching | Premier rematching | Première relance |
|--------------|-----------------|-------------------|-----------------|
| Chambre | immédiat | 24h | 48h |
| Studio | immédiat | 48h | 72h |
| Appartement | immédiat | 72h | 5 jours |
| Maison | immédiat | 5 jours | 7 jours |
| Villa | immédiat | 7 jours | 10 jours |
| Duplex | immédiat | 7 jours | 10 jours |
| Terrain résidentiel | immédiat | 10 jours | 15 jours |
| Terrain agricole | immédiat | 15 jours | 20 jours |
| Terrain industriel | immédiat | 20 jours | 30 jours |
| Commerce | immédiat | 7 jours | 10 jours |
| Bureau | immédiat | 10 jours | 15 jours |
| Entrepôt | immédiat | 15 jours | 20 jours |
| Hôtel | immédiat | 30 jours | 45 jours |
| Immeuble | immédiat | 30 jours | 45 jours |

### 11.8 Cinétique par type de bien (rotation normale)
Source : `05-WORKFLOW-REFERENCE.md`

| Type | Rotation normale |
|------|-----------------|
| Chambre | 1 à 4 semaines |
| Studio | 2 à 8 semaines |
| Appartement | 1 à 4 mois |
| Villa | 3 à 12 mois |
| Terrain résidentiel | 3 à 18 mois |
| Terrain agricole | 6 à 36 mois |
| Commerce | 1 à 6 mois |
| Bureau | 2 à 8 mois |
| Hôtel | 6 à 36 mois |

### 11.9 Workflow dossier (états officiels)
Source : `05-WORKFLOW-REFERENCE.md` Partie 4

Création → Qualification → Matching → Présentation → Attente décision demandeur → Contact détenteur → Attente décision détenteur → Mise en relation → Visite → Négociation → Accord → Transaction → Clôture → Archivage

### 11.10 Rappels automatiques visites
Source : `05-WORKFLOW-REFERENCE.md` Partie 6

Default : 24h avant visite, 2h avant visite

### 11.11 Workflow silence détenteur
Source : `05-WORKFLOW-REFERENCE.md` Partie 5

Premier rappel → Deuxième rappel → Dernier rappel → Bien marqué "à confirmer" → Rematching

---

## 12. SIGNALÉTIQUE MARCHÉ CAMEROUNAIS

### 12.1 Confiance et méfiance
Source : `KNOWLEDGE/trust-and-objection-patterns.md`

- Méfiance initiale normale — ne pas interpréter comme hostilité ou manque d'intérêt
- Réponse LAWIM : réassurance, pédagogie, transparence — jamais pression commerciale
- L'acheteur reste en retenue jusqu'à preuve (documents, visite ou validation proche/famille)
- La conversion suit : Intérêt → Vérification → Réassurance → Visite → Validation documentaire → Décision

### 12.2 Validation sociale
Source : `KNOWLEDGE/conversation-patterns.md`

Expressions normales au Cameroun : "Mon grand frère doit voir", "Mon cousin va vérifier", "Mon oncle est sur place", "Ma femme doit valider", "Mon mari doit regarder"
→ LAWIM ne doit pas considérer cela comme une objection mais comme une étape normale du cycle de décision

### 12.3 Peurs des acheteurs
Source : `KNOWLEDGE/trust-and-objection-patterns.md`

Fraude/arnaque, paiement anticipé sans visite, faux propriétaire, dossier juridique flou, conflits familiaux/successoraux, zone enclavée, vendeur peu crédible, mauvaise affaire/revente, frais cachés

### 12.4 Peurs des vendeurs
Source : `KNOWLEDGE/trust-and-objection-patterns.md`

Acheteurs non sérieux, négociation agressive, perte de temps, divulgation excessive, vente à perte, arnaque acheteur, visibilité insuffisante, mauvaise image du bien

### 12.5 Signaux de fraude
Source : `KNOWLEDGE/fraud-signals-and-verification.md`

Prix anormalement bas, photos génériques/floues, annonce sans WhatsApp/contact flou, silence prolongé vendeur, urgence artificielle, impossibilité de visiter, absence de papiers, incohérence discours, annonce trop répétée, annonce floue/texte seul

### 12.6 Signaux de sérieux (positifs)
Source : `KNOWLEDGE/fraud-signals-and-verification.md`

**Acheteur sérieux :** visite, demande titre, prix net, demande charges, délai
**Vendeur sérieux :** cohérence, documents, questions difficiles OK, accès
**Prospect sérieux :** peu de questions mais précises

### 12.7 Comportement diaspora (spécificités)
Source : `KNOWLEDGE/diaspora-behavior-model.md`

- Plus exigeant que l'acheteur local
- Exige : crédibilité intermédiaire, preuves avant engagement, documents numérisés, vidéo en direct, preuves géolocalisées, suivi structuré
- Peur principale : arnaque documentaire
- Rejette : transactions informelles, vendeurs pressants, improvisation, réponses vagues, incohérences, urgences artificielles
- Parcours : Contact → crédibilité → preuves visuelles → documents numérisés → relais local → validation familiale → paiement échelonné sécurisé → suivi documenté

### 12.8 Objections fréquentes et réponses LAWIM
Source : `48-LAWIM-SALES-PLAYBOOK.md`, `KNOWLEDGE/trust-and-objection-patterns.md`

| Objection | Réponse LAWIM |
|-----------|---------------|
| "Je peux publier gratuitement sur Facebook" | LAWIM apporte suivi, structure, vérification, services utiles |
| "Je travaille déjà avec des agents" | LAWIM ajoute visibilité et cadre, n'empêche pas relations existantes |
| "Je ne veux pas payer" | Certains services gratuits, certains payants ; prix présenté avant |
| "Comment savoir que c'est fiable ?" | LAWIM structure, trace, vérifie |
| "Est-ce une agence ?" | Non, plateforme de services et mise en relation |
| "Prenez-vous une commission ?" | Non, LAWIM ne prélève aucune commission |
| "Le titre est bon ?" | Statut documents connu, pas promesse vague |
| "Je peux visiter ?" (refus visite) | Prioriser visite ou vidéo live |
| "Pourquoi si bas / si haut ?" | Explication marché, pas défense agressive |

---

## 13. SERVICES LAWIM ET MONÉTISATION

### 13.1 Services payants
Source : `01-GLOSSAIRE.md`, `48-LAWIM-SALES-PLAYBOOK.md`

- Mise en relation payante
- Accompagnement de visite
- Accompagnement de transaction
- Contrôle documentaire
- Photographie
- Vidéo
- Vérification
- Boost
- Visibilité premium
- Assistance
- Accompagnement diaspora

### 13.2 Modèle économique
Source : `DIRECTIVE/LAWIM-BUSINESS-PLAN.md`

- **Revenus :** mise en relation, accès contact, visibilité premium, boost, vérification, assistance, photo, vidéo, services partenaires, accompagnement diaspora, IA, publication
- **Règle absolue :** pas de commission sur les ventes ou locations immobilières

### 13.3 Statuts de paiement (taxonomie unique)
Source : `06-DATABASE-REFERENCE.md`

PAYMENT_CREATED → PAYMENT_INITIATED → PAYMENT_PENDING → PAYMENT_CONFIRMED → PAYMENT_FAILED → PAYMENT_CANCELLED → PAYMENT_EXPIRED → PAYMENT_REFUNDED → PAYMENT_RECONCILED → PAYMENT_DISPUTED

---

## 14. WORKFLOW MOTEUR DE REMATCHING

### 14.1 Événements déclencheurs de rematching
Source : `04-MATCHING-REFERENCE.md` Partie 5

**Côté demandeur :** modification budget, changement ville, changement quartier, changement type de bien, ajout/suppression critère, refus bien, abandon visite, nouvelle préférence

**Côté bien :** publication, modification, baisse/hausse prix, changement disponibilité, ajout photos/GPS/documents, amélioration qualification

**Côté détenteur :** acceptation, refus, absence réponse, indisponibilité temporaire, retour disponibilité

**Côté système :** nouvelle règle métier, recalcul périodique, apprentissage global, correction données

### 14.2 Règles impératives du rematching
Source : `04-MATCHING-REFERENCE.md` Partie 5

- ✓ Apprendre de chaque décision
- ✓ Réagir immédiatement aux changements significatifs
- ✓ Conserver l'historique des propositions
- ✓ Éviter les propositions répétitives
- ✓ Expliquer chaque nouvelle recommandation
- ✓ Privilégier qualité > quantité
- ❌ Jamais repartir de zéro
- ❌ Jamais oublier les préférences acquises
- ❌ Jamais proposer un bien définitivement écarté sans justification
- ❌ Jamais effectuer des recalculs inutiles

---

**FIN DU RAPPORT**

Ce document contient l'intégralité du patrimoine métier extrait des sources de LAWIM. Il est structuré par domaine et prêt à servir de base pour la reconstruction des règles métier, de la base de connaissances et de l'implémentation.
