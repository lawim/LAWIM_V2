# Rapport de Validation — PROPERTY_MODEL.md

**Auditeur :** Système de validation LAWIM  
**Date :** 2026-07-15  
**Branches vérifiées :** LAWIM, LAWIMA, ancienne_structure

---

## 1. Familles de biens (7 familles)

| # | Statut | Détail | Confiance |
|---|--------|--------|-----------|
| **1** | PARTIELLEMENT VALIDÉ | `02-PROPERTY-REFERENCE.md` listings 7 familles dans les fichiers `02A`→`02G`. Tous les fichiers existent. Différence mineure : le document source utilise "foncier" (pas "Terrain") et "hôtelier" (pas "Hôtellerie"). Conceptuellement correct. | ÉLEVÉE |

## 2. Types et sous-types

| # | Statut | Détail | Confiance |
|---|--------|--------|-----------|
| **2** | VALIDÉ | `property_types.py:7` → `["appartement","maison","villa","studio","duplex","chambre","immeuble residentiel"]`. Correspond exactement (orthographe sans accent dans la source). | ÉLEVÉE |
| **3** | VALIDÉ | `property_types.py:12-15` → `["terrain residentiel","terrain construction","terrain agricole","terrain commercial","terrain nu","location terrain","terre"]`. Correspond. | ÉLEVÉE |
| **4** | VALIDÉ | `property_types.py:20-23` → `["boutique","magasin","immeuble commercial","bureau","entrepôt","local commercial","commerce"]`. Correspond. | ÉLEVÉE |
| **5** | VALIDÉ | `property_types.py:28` → `["parking","garage","atelier"]`. Correspond. | ÉLEVÉE |

## 3. Cycle de vie

| # | Statut | Détail | Confiance |
|---|--------|--------|-----------|
| **6** | VALIDÉ | `property_lifecycle_engine.py:18-24` → 5 états : available, pending, rented, sold, archived. Correspond. | ÉLEVÉE |
| **7** | VALIDÉ | `property_lifecycle_engine.py:19-23` → Transitions exactement comme documentées. `available→pending/archived`, `pending→rented/sold/available/archived`, `rented→archived`, `sold→archived`, `archived→available`. | ÉLEVÉE |
| **8** | VALIDÉ | `property_lifecycle_engine.py:61` → `auto_archive_expired(self, days=90)` : archivage après 90 jours d'inactivité. | ÉLEVÉE |

## 4. Titres fonciers

| # | Statut | Détail | Confiance |
|---|--------|--------|-----------|
| **9** | PARTIELLEMENT VALIDÉ | `title_status.json` contient `"titre_foncier"` (ligne 3) mais **pas** le `boost +10`. Le boost +10 pour `title_foncier` se trouve en réalité dans `property_matching_v1.json:33-35` → `{"condition":"title_foncier","boost":10}`. Source référencée incorrecte. | MOYENNE |

## 5. Qualité des données

| # | Statut | Détail | Confiance |
|---|--------|--------|-----------|
| **10** | VALIDÉ | `data_quality_engine.py:76` → `quality_score = int(completeness * 0.6 + reliability * 0.4)` : complétude 60%, fiabilité 40%. | ÉLEVÉE |
| **11** | VALIDÉ | Poids complétude : titre 10% (l.42), description 15% (l.48-52), prix 15% (l.56), localisation 15% (l.60), type 15% (l.64), images 15% max 3pts/image (l.69). Correspond exactement. | ÉLEVÉE |
| **12** | VALIDÉ | `data_quality_engine.py:19-25` → agent=90, google_form=85, import=70, whatsapp=50, unknown=30. Correspond. | ÉLEVÉE |
| **13** | VALIDÉ | `data_quality_engine.py:146-155` → A+≥80, A≥60, B≥40, C≥20, D<20. Correspond. | ÉLEVÉE |

## 6. Prix et évaluations

| # | Statut | Détail | Confiance |
|---|--------|--------|-----------|
| **14** | NON VALIDÉ | Le document référence `lawim_engine_v1.py` mais ce fichier **ne contient aucun parsing de prix**. Il s'agit d'un simple orchestrateur (65 lignes). Les formats `k_format`/`mille_format` sont implémentés dans `core/gateway_fixed.py:59-68` et autres fichiers gateway, pas dans la source indiquée. | FAIBLE |
| **15** | NON VALIDÉ | Le document référence `property_matcher_v5.py` mais ce fichier **n'a pas de scoring budget** (≥500k→+30, etc.). Ce scoring se trouve dans `lead_scorer_supabase.py:28-33` → `if budget >= 500000: score += 30` etc. Source référencée incorrecte. | FAIBLE |

## 7. Champs spécifiques par catégorie

| # | Statut | Détail | Confiance |
|---|--------|--------|-----------|
| **16** | PARTIELLEMENT VALIDÉ | Les champs exacts `rooms, bedrooms, bathrooms, floor, has_elevator, is_furnished` sont dans `property_types.py:36` (SPECIFIC_FIELDS["logement"]), **pas** dans `property_categories.py` qui contient des champs en français. Le concept est correct, la source référencée est partiellement erronée. | MOYENNE |
| **17** | VALIDÉ | `property_types.py:37` → `["surface","is_agricultural","is_constructible","has_water","has_electricity"]`. Correspond. | ÉLEVÉE |
| **18** | VALIDÉ | `property_types.py:38` → `["surface","front_window","parking_spots","has_signage"]`. Correspond. | ÉLEVÉE |

## 8. Champs minimum d'une annonce

| # | Statut | Détail | Confiance |
|---|--------|--------|-----------|
| **19** | VALIDÉ | `minimum-fields-property.md` liste comme obligatoires : Transaction, Type de bien, Ville, Prix, Description (parmi d'autres). Les 5 champs cités sont bien présents comme obligatoires. | ÉLEVÉE |

## 9. Statuts de transaction / Paiement

| # | Statut | Détail | Confiance |
|---|--------|--------|-----------|
| **20** | NON VALIDÉ | `monetisation.py` ne contient **pas 10 statuts de paiement explicites**. Les statuts trouvés sont : `completed`, `pending`, `paid`, `active`, `expired` (+ `new`/`contacted`/etc. dans les leads via kanban.py). Aucune liste de 10 statuts n'existe dans le fichier référencé. | FAIBLE |

---

## Résumé PROPERTY_MODEL

| Statut | Nombre |
|--------|--------|
| VALIDÉ | 12 |
| PARTIELLEMENT VALIDÉ | 3 |
| NON VALIDÉ | 3 |
| INTROUVABLE | 0 |
| **Total** | **18** (hors #1 cadre) |

**Problèmes majeurs :** Références de sources incorrectes pour les claims #9, #14, #15. Le scoring budget et les formats de prix existent bien dans le code mais pas dans les fichiers cités.
