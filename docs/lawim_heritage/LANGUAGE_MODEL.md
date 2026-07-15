# LANGUAGE MODEL — Modèle de langage LAWIM

**Sources :** LAWIM `KNOWLEDGE/whatsapp_language/` (7 fichiers), `KNOWLEDGE/typo_database/` (5 fichiers), `KNOWLEDGE/vocabulary/real_estate_vocabulary.json`, `KNOWLEDGE/search_aliases/search_aliases.json`, LAWIMA `02_KNOWLEDGE/whatsapp_language/` (7 fichiers), `02_KNOWLEDGE/typo_database/` (5 fichiers), `02_KNOWLEDGE/vocabulary/real_estate_vocabulary.json`, `02_KNOWLEDGE/entity_linking/entity_linking.json`, `03_ENGINE/language_handler.py`, `language_detector.py`, `language_detector_ia.py`, `multilingual_responses.py`, `location_normalizer.py`, `phone_formatter.py`
**Principe :** Documentation exhaustive des connaissances linguistiques

---

## 1. Langues supportées

**Source :** LAWIMA `03_ENGINE/language_handler.py`, `language_detector.py`, `multilingual_responses.py`

| Langue | Code | Statut |
|--------|------|--------|
| Français | FR | Langue par défaut, complète |
| Anglais | EN | Complète |
| Pidgin Cameroon | PID | Partielle (15 mots de détection) |
| Camfranglais | — | Détection limitée dans les expressions |

## 2. Détection de langue

### 2.1 Détection par règles locales

**Source :** LAWIMA `03_ENGINE/language_detector.py`

**Mots-clés français (20) :**
bonjour, salut, appartement, maison, terrain, location, achat, vente, prix, budget, urgent, merci, je, tu, il, elle, nous, vous

**Mots-clés anglais (20) :**
hello, hi, apartment, house, land, rent, buy, sale, price, budget, urgent, thanks, i, you, he, she, we, they

**Mots-clés pidgin (15) :**
how far, wahala, chap, gbedu, comot, dey, sabi, small, plenty, chop, wetin, na, abeg, now now

### 2.2 Détection IA hiérarchique

**Source :** LAWIMA `03_ENGINE/language_detector_ia.py`

Hiérarchie de détection :
1. DeepSeek (analyse IA)
2. Gemini (à implémenter — non disponible dans le backup)
3. Règles locales (fallback)

### 2.3 Persistance du choix de langue

**Source :** LAWIMA `03_ENGINE/language_handler.py`

La langue de l'utilisateur est persistée et utilisée pour toutes les interactions futures. Commande `LANGUE` pour changer.

## 3. Messages multilingues

**Source :** LAWIMA `03_ENGINE/multilingual_responses.py`

Templates disponibles en FR, EN, PID :

| Template | Usage |
|----------|-------|
| welcome | Message de bienvenue |
| help | Message d'aide |
| no_match (search_query) | Aucun résultat |
| thanks | Remerciement |
| ask_name | Demande du nom |
| ask_phone | Demande du téléphone |
| stats | Statistiques (leads, acceptés, conversion, note/5) |
| language_changed | Confirmation changement de langue |

## 4. Synonymes et alias

### 4.1 Entity Linking

**Source :** LAWIMA `02_KNOWLEDGE/entity_linking/entity_linking.json`

Fichier JSON contenant les correspondances entre entités (termes équivalents, synonymes, abréviations). Utilisé pour la résolution d'entités dans les messages.

### 4.2 Search Aliases

**Source :** LAWIM `KNOWLEDGE/search_aliases/search_aliases.json`, LAWIMA `02_KNOWLEDGE/search_aliases/search_aliases.json`

Alias de recherche pour les termes immobiliers. Permet de trouver des biens même avec des termes non standards.

### 4.3 Property Type Aliases

**Source :** LAWIMA `02_KNOWLEDGE/property_types/property_types.json`

Correspondances multi-langues pour les types de biens (intégré dans le fichier property_types.json).

### 4.4 Normalisation cross-langue (dans le code)

**Source :** LAWIMA `03_ENGINE/property_types.py`

| Terme | Normalisé |
|-------|-----------|
| apartment | appartement |
| flat | appartement |
| house | maison |
| room | chambre |
| land | terrain |
| furnished | meublé |

## 5. Fautes courantes et variantes orthographiques

**Source :** LAWIM `KNOWLEDGE/typo_database/` (5 fichiers), LAWIMA `02_KNOWLEDGE/typo_database/` (5 fichiers)

### 5.1 Fichiers de correction

| Fichier | Contenu |
|---------|---------|
| `cities_typo.json` | Fautes courantes sur les noms de villes |
| `neighborhoods_typo.json` | Fautes courantes sur les noms de quartiers |
| `property_types_typo.json` | Fautes courantes sur les types de biens |
| `whatsapp_typo.json` | Fautes spécifiques au langage WhatsApp |
| `typo_database.json` | Base agrégée de toutes les fautes |

### 5.2 Exemples de variantes (location_normalizer)

**Source :** LAWIMA `03_ENGINE/location_normalizer.py`

**Yaoundé :**
- bastos → bastos, basto, bastoss, bastos village
- essos → essos, esos, essoss
- biyem_assi → biyem, biyem-assi, biyemassi, biem assi
- odza → odza, odzaa, odja

**Douala :**
- akwa → akwa, aqua, akwah
- bonamoussadi → bonamoussadi, bona moussadi, bonamussadi

### 5.3 Algorithme de correction

**Source :** LAWIMA `03_ENGINE/location_normalizer.py`

- Distance de Levenshtein (seuil max 3)
- Correspondance par dictionnaire (synonym database)
- Apprentissage de nouvelles variantes (knowledge_enricher)

## 6. Vocabulaire immobilier

**Source :** LAWIM `KNOWLEDGE/vocabulary/real_estate_vocabulary.json`, LAWIMA `02_KNOWLEDGE/vocabulary/real_estate_vocabulary.json`

Corpus de vocabulaire immobilier structuré par catégories (termes techniques, expressions courantes, etc.).

## 7. Langage WhatsApp

**Source :** LAWIM `KNOWLEDGE/whatsapp_language/` (7 fichiers), LAWIMA `02_KNOWLEDGE/whatsapp_language/` (7 fichiers)

### 7.1 Fichiers de langage WhatsApp

| Fichier | Contenu |
|---------|---------|
| `whatsapp_language.json` | Corpus principal du langage WhatsApp |
| `diaspora_language.json` | Expressions spécifiques à la diaspora |
| `investor_language.json` | Expressions des investisseurs |
| `negotiation.json` | Expressions de négociation |
| `property_listing.json` | Expressions d'annonces immobilières |
| `property_search.json` | Expressions de recherche de biens |
| `urgency_signals.json` | Signaux d'urgence |

### 7.2 Contenu des fichiers

Chaque fichier contient des listes d'expressions classées par :
- Catégorie
- Langue (FR, EN, PID)
- Contexte d'utilisation

## 8. Expressions camerounaises

**Source :** LAWIM `KNOWLEDGE/whatsapp_language/` (données)

Expressions spécifiques au contexte camerounais présentes dans les fichiers de langage WhatsApp (non listées exhaustivement ici).

## 9. Internationalisation

**Source :** LAWIM `Directive/30-I18N-L10N-REFERENCE.md`, `30A-BUSINESS-DICTIONARY-REFERENCE.md`, `30B-TRANSLATION-REFERENCE.md`, `30C-LANGUAGE-DETECTION-REFERENCE.md`, `30D-MULTILINGUAL-SEARCH-REFERENCE.md`

5 documents dédiés à l'internationalisation :
- **30-I18N-L10N-REFERENCE.md** : Stratégie d'internationalisation
- **30A-BUSINESS-DICTIONARY-REFERENCE.md** : Dictionnaire métier multilingue
- **30B-TRANSLATION-REFERENCE.md** : Correspondances de traduction
- **30C-LANGUAGE-DETECTION-REFERENCE.md** : Spécifications détection langue
- **30D-MULTILINGUAL-SEARCH-REFERENCE.md** : Recherche multilingue

## 10. Formatage téléphonique

**Source :** LAWIMA `03_ENGINE/phone_formatter.py`

### 10.1 Pays supportés

30 codes pays couverts (non listés exhaustivement).

### 10.2 Format standard Cameroun

237 + 9 chiffres

### 10.3 Règles de normalisation

- Suppression des caractères non numériques
- Ajout automatique de 237 si 9 chiffres
- Affichage formaté : 🇨🇲 +237 697 852 456

### 10.4 WhatsApp link

`https://wa.me/{numéro_normalisé}`

### 10.5 Détection diaspora par indicatif

Les indicatifs étrangers (+33, +1, +44, +49) déclenchent le flag diaspora.

---

*Document patrimonial — Aucune décision de reconstruction n'est prise ici.*
