# PROPERTY MODEL — Modèle immobilier LAWIM

**Sources :** LAWIM `Directive/02*.md`, LAWIMA `property_types.py`, `property_lifecycle_engine.py`, `data_quality_engine.py`, `title_status`, `property_matcher/`
**Principe :** Documentation exhaustive des connaissances sur les biens immobiliers

---

## 1. Familles de biens

### 1.1 Hiérarchie des types

**Source :** LAWIM `Directive/02-PROPERTY-REFERENCE.md`

7 familles principales documentées individuellement :

| Famille | Document | Code |
|---------|----------|------|
| Résidentiel | `02A-RESIDENTIAL-REFERENCE.md` | residential |
| Commercial | `02B-COMMERCIAL-REFERENCE.md` | commercial |
| Industriel | `02C-INDUSTRIAL-REFERENCE.md` | industrial |
| Terrain | `02D-LAND-REFERENCE.md` | land |
| Agricole | `02E-AGRICULTURAL-REFERENCE.md` | agricultural |
| Hôtellerie | `02F-HOTEL-REFERENCE.md` | hotel |
| Projet | `02G-PROJECT-REFERENCE.md` | project |

### 1.2 Types et sous-types dans le code

**Source :** LAWIMA `03_ENGINE/property_types.py`

**Logement :** appartement, maison, villa, studio, duplex, chambre, immeuble résidentiel
**Terrain :** terrain résidentiel, terrain construction, terrain agricole, terrain commercial, terrain nu, location terrain, terre
**Commerce :** boutique, magasin, immeuble commercial, bureau, entrepôt, local commercial, commerce
**Autre :** parking, garage, atelier

### 1.3 Types dans le knowledge JSON

**Source :** LAWIMA `02_KNOWLEDGE/property_types/property_types.json`

Types listés avec expressions associées en FR/EN.

### 1.4 Catalogue d'attributs

**Source :** LAWIM `Directive/02H-ATTRIBUTE-CATALOG.md`

Catalogue complet des attributs pour tous les types de biens. Non détaillé ici, voir le document source pour la liste exhaustive.

## 2. Types de transactions

**Source :** LAWIMA `02_KNOWLEDGE` (transaction types), conversations patterns

Transactions supportées :
- **Vente** (buy, buy_property, achat, acquisition)
- **Location** (rent, rent_property, location, leasing)
- **Investissement** (investor, investor_intent, investissement)
- **Recherche** (search, search_property)

## 3. Cycle de vie des propriétés

**Source :** LAWIMA `03_ENGINE/property_lifecycle_engine.py`

### 3.1 États

| État | Description | Icône |
|------|-------------|-------|
| available | Disponible | 🏠 |
| pending | En cours de transaction | ⏳ |
| rented | Loué | 🔑 |
| sold | Vendu | 💰 |
| archived | Archivé | 📦 |

### 3.2 Transitions autorisées

```
available ──► pending (mise en transaction)
available ──► archived (archivage direct)
pending   ──► rented (location confirmée)
pending   ──► sold (vente confirmée)
pending   ──► available (transaction annulée)
pending   ──► archived (échec transaction)
rented    ──► archived (fin de location)
sold      ──► archived (vente finalisée)
archived  ──► available (remise en ligne)
```

### 3.3 Archivage automatique

- 90 jours d'inactivité → archivage automatique
- Règle : `if days_since_last_activity > 90: auto_archive()`

## 4. Types de titres fonciers

**Source :** LAWIMA `02_KNOWLEDGE/title_status/title_status.json`

Types identifiés :
- **title_foncier** : Titre foncier (boost matching +10)
- Autres statuts listés dans le fichier JSON (non exhaustif ici)

## 5. Qualité des données immobilières

**Source :** LAWIMA `03_ENGINE/data_quality_engine.py`

### 5.1 Score de qualité (0-100)

**Complétude (60% du score total) :**

| Champ | Poids |
|-------|-------|
| Titre | 10% |
| Description (>100 caractères = 15pts, >50 = 10pts, >20 = 5pts) | 15% |
| Prix | 15% |
| Localisation | 15% |
| Type de bien | 15% |
| Images (max 3pts par image, plafond 15pts) | 15% |

**Fiabilité de la source (40% du score total) :**

| Source | Score de fiabilité |
|--------|-------------------|
| Agent | 90 |
| Google Form | 85 |
| Import | 70 |
| WhatsApp | 50 |
| Unknown | 30 |

### 5.2 Grille de notation

| Grade | Score | Icône |
|-------|-------|-------|
| A+ | ≥ 80 | 🟢 |
| A | ≥ 60 | 🟢 |
| B | ≥ 40 | 🟡 |
| C | ≥ 20 | 🔴 |
| D | < 20 | 🔴 |

## 6. Prix et évaluations

**Source :** LAWIMA `02_KNOWLEDGE/pricing/`, `03_ENGINE/lawim_engine_v1.py`

### 6.1 Formats de prix reconnus

- **k_format** : "150k" → 150 000
- **mille_format** : "150 mille" → 150 000
- **range_detection** : "entre 100 et 200" → min=100000, max=200000
- **Direct digits** : 3-9 chiffres consécutifs

### 6.2 Expressions de prix

**Source :** LAWIMA `02_KNOWLEDGE/pricing/pricing.json`, `pricing_expressions/pricing_expressions.json`

Expressions et règles de prix listées dans les fichiers JSON.

### 6.3 Scoring budget

**Source :** LAWIMA `03_ENGINE/property_matcher/property_matcher_v5.py`

- Budget ≥ 500k → +30 pts
- Budget ≥ 200k → +20 pts
- Budget ≥ 100k → +10 pts

### 6.4 Signal prix dans les messages

**Source :** LAWIMA `03_ENGINE/lawim_engine_v1.py`

Patterns détectés : `prix`, `budget`, `max`, `k`, `mille`, `000`, `fcfa`

## 7. Champs spécifiques par catégorie

**Source :** LAWIMA `07_DASHBOARD/property_categories.py`

### 7.1 Logement (6 sous-catégories)
- rooms, bedrooms, bathrooms, floor, has_elevator, is_furnished

### 7.2 Terrain (5 sous-catégories)
- surface, is_agricultural, is_constructible, has_water, has_electricity

### 7.3 Commerce (6 sous-catégories)
- surface, front_window, parking_spots, has_signage

### 7.4 Autre (3 sous-catégories)
- parking, garage, atelier

## 8. Champs minimum d'une annonce

**Source :** LAWIM `KNOWLEDGE/minimum-fields-property.md`

### 8.1 Champs obligatoires
- Type de bien
- Transaction (vente/location)
- Prix
- Ville
- Description

### 8.2 Champs fortement recommandés
- Quartier
- Surface
- Nombre de pièces
- Photos
- Titre de propriété (pour vente)

### 8.3 Champs optionnels
- Étage
- Ascenseur
- Meublé
- Parking
- Date de disponibilité

## 9. Qualification des biens

**Source :** LAWIM `KNOWLEDGE/property-qualification-reference.md`

Critères de qualification d'un bien (non exhaustif, voir source) :
- Existence légale (titre foncier, acte de vente)
- Conformité physique (correspondance description/réalité)
- Prix de marché (comparaison avec biens similaires)
- Accessibilité (routes, transports)
- Risques (zone inondable, litige)

## 10. Statuts de transaction

**Source :** LAWIMA core/monetisation.py

Dix statuts de paiement identifiés dans le code de monétisation (non détaillés, voir source).

---

*Document patrimonial — Aucune décision de reconstruction n'est prise ici.*
