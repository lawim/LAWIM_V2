# LAWIM

# 02-PROPERTY-REFERENCE.md

# Référentiel maître des biens immobiliers

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le présent document définit le référentiel maître de tous les biens immobiliers gérés par LAWIM.

Il constitue la référence unique pour :

* les concepts communs ;
* les règles communes ;
* les attributs communs ;
* les workflows communs ;
* les règles de publication ;
* les règles de validation ;
* les règles d'archivage ;
* les règles de matching communes.

---

# CHAPITRE 2 — PRINCIPE D'HÉRITAGE

Les biens immobiliers sont décrits par un modèle maître, puis par des sous-référentiels spécialisés.

Le maître définit ce qui est commun à tous les biens.

Les sous-référentiels définissent uniquement les spécificités de chaque famille.

Il est interdit de recopier les règles générales dans chaque sous-référentiel.

---

# CHAPITRE 3 — SOUS-RÉFÉRENTIELS OFFICIELS

Les familles documentées par LAWIM sont les suivantes :

* [02A-RESIDENTIAL-REFERENCE.md](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM/Directive/02A-RESIDENTIAL-REFERENCE.md)
* [02B-COMMERCIAL-REFERENCE.md](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM/Directive/02B-COMMERCIAL-REFERENCE.md)
* [02C-INDUSTRIAL-REFERENCE.md](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM/Directive/02C-INDUSTRIAL-REFERENCE.md)
* [02D-LAND-REFERENCE.md](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM/Directive/02D-LAND-REFERENCE.md)
* [02E-AGRICULTURAL-REFERENCE.md](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM/Directive/02E-AGRICULTURAL-REFERENCE.md)
* [02F-HOTEL-REFERENCE.md](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM/Directive/02F-HOTEL-REFERENCE.md)
* [02G-PROJECT-REFERENCE.md](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM/Directive/02G-PROJECT-REFERENCE.md)

Les référentiels transversaux associés sont :

* [02H-ATTRIBUTE-CATALOG.md](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM/Directive/02H-ATTRIBUTE-CATALOG.md)
* [02I-PRICING-REFERENCE.md](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM/Directive/02I-PRICING-REFERENCE.md)

---

# CHAPITRE 4 — FAMILLES D'OBJETS

LAWIM reconnaît les familles suivantes :

* résidentiel ;
* commercial ;
* industriel ;
* foncier ;
* agricole ;
* hôtelier ;
* projet immobilier.

Chaque famille peut contenir plusieurs types spécialisés.

---

# CHAPITRE 5 — CONCEPTS COMMUNS

Tous les biens partagent notamment les concepts suivants :

* famille ;
* type ;
* opération ;
* détenteur ;
* statut ;
* disponibilité ;
* localisation ;
* média ;
* documentation ;
* prix ;
* archivage ;
* score de matching.

Ces concepts sont normalisés par le glossaire, le catalogue d'attributs et le référentiel prix.

---

# CHAPITRE 6 — ATTRIBUTS COMMUNS

Les attributs communs à tous les biens sont notamment :

* famille de bien ;
* type de bien ;
* opération autorisée ;
* ville ;
* quartier ou zone ;
* coordonnées ou repère géographique ;
* disponibilité ;
* état de publication ;
* état d'archivage ;
* prix ou fourchette de prix ;
* source d'origine ;
* détenteur ;
* documents de preuve ou de contrôle lorsque requis.

Les valeurs exactes sont normalisées par [02H-ATTRIBUTE-CATALOG.md](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM/Directive/02H-ATTRIBUTE-CATALOG.md).

---

# CHAPITRE 7 — WORKFLOW COMMUN

Tout bien suit un cycle commun :

1. réception ou saisie ;
2. normalisation ;
3. classification ;
4. validation ;
5. publication ou mise en attente ;
6. matching ;
7. mise en relation si applicable ;
8. suivi ;
9. archivage ;
10. conservation historique.

Les sous-référentiels peuvent ajouter des étapes spécifiques, mais ne doivent pas casser ce socle.

---

# CHAPITRE 8 — RÈGLES DE PUBLICATION

Un bien ne peut être publié que si :

* sa famille est identifiée ;
* son type est cohérent ;
* sa localisation minimale est connue ;
* son prix est renseigné selon [02I-PRICING-REFERENCE.md](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM/Directive/02I-PRICING-REFERENCE.md) ;
* son détenteur est identifiable ;
* ses informations critiques sont normalisées ;
* les pièces obligatoires sont présentes lorsque la famille les exige.

---

# CHAPITRE 9 — RÈGLES DE VALIDATION

La validation vérifie notamment :

* la cohérence entre type et famille ;
* la cohérence entre opération et usage ;
* la cohérence entre localisation et disponibilité ;
* la cohérence entre prix et marché ;
* l'absence d'attribut interdit ;
* la conformité documentaire ;
* la qualité minimale des médias et des données.

La validation peut être humaine, assistée ou automatique selon le contexte.

---

# CHAPITRE 10 — RÈGLES DE MATCHING

Le matching commun repose sur :

* la famille de bien ;
* le type de bien ;
* l'opération ;
* la localisation ;
* le prix ;
* la disponibilité ;
* les attributs spécifiques de la famille ;
* la qualité des données ;
* les préférences et la mémoire conversationnelle.

Le matching ne doit jamais ignorer le référentiel spécialisé de la famille concernée.

---

# CHAPITRE 11 — RÈGLES D'ARCHIVAGE

Un bien peut être archivé lorsqu'il :

* n'est plus publiable ;
* a été vendu, loué ou retiré ;
* est obsolète ;
* est en litige ;
* doit être conservé à des fins historiques, juridiques ou d'audit.

L'archivage s'applique selon [14-STORAGE-REFERENCE.md](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM/Directive/14-STORAGE-REFERENCE.md).

---

# CHAPITRE 12 — RÈGLES ABSOLUES

Le référentiel maître doit toujours :

* rester la source des règles générales ;
* éviter les doublons avec les sous-référentiels ;
* rester cohérent avec le glossaire ;
* rester cohérent avec les prix ;
* rester cohérent avec la géolocalisation ;
* rester cohérent avec la base de données et les tests.

Il est interdit :

* de créer des règles générales contradictoires dans un sous-référentiel ;
* de publier un bien sans famille ou sans type ;
* de créer une commission immobilière sur les ventes ou locations ;
* d'archiver un bien sans respecter la politique de stockage.

---

# CHAPITRE 13 — OBJECTIF FINAL

Le référentiel maître des biens doit permettre à LAWIM de traiter tous les biens immobiliers avec une logique commune, normalisée et gouvernée, tout en laissant à chaque famille son espace spécialisé.

---

# FIN DU DOCUMENT

Le présent **02-PROPERTY-REFERENCE.md** constitue le référentiel maître officiel de tous les biens immobiliers de LAWIM.
