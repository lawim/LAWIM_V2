# LAWIM

# 02I-PRICING-REFERENCE.md

# Référentiel officiel des prix immobiliers

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le présent document définit les règles officielles de traitement des prix immobiliers dans LAWIM.

Il constitue la référence unique pour :

* les prix de vente ;
* les loyers ;
* les cautions ;
* les avances de loyer ;
* les mensualités ;
* les dépôts de garantie ;
* les frais liés aux services LAWIM ;
* les devises ;
* les taxes éventuelles ;
* la négociation ;
* l'historique des prix ;
* l'estimation ;
* les fourchettes de marché ;
* les indicateurs de variation.

Il est utilisé notamment par :

* Matching Engine ;
* Reporting Engine ;
* Dashboard Engine ;
* LAWIM AI.

---

# CHAPITRE 2 — PRINCIPE FONDAMENTAL

Le prix est une donnée métier immobilière.

Il ne définit pas le modèle économique de LAWIM.

Il ne crée aucune commission transactionnelle.

Les revenus LAWIM restent définis par la Constitution et les référentiels de services.

---

# CHAPITRE 3 — RÉFÉRENCES OBLIGATOIRES

Le référentiel prix applique obligatoirement :

* [02-PROPERTY-REFERENCE.md](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/docs/Directive/02-PROPERTY-REFERENCE.md)
* [02H-ATTRIBUTE-CATALOG.md](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/docs/Directive/02H-ATTRIBUTE-CATALOG.md)
* [03-CONVERSATION-REFERENCE.md](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/docs/Directive/03-CONVERSATION-REFERENCE.md)
* [04-MATCHING-REFERENCE.md](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/docs/Directive/04-MATCHING-REFERENCE.md)
* [06-DATABASE-REFERENCE.md](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/docs/Directive/06-DATABASE-REFERENCE.md)
* [07-DASHBOARD-REFERENCE.md](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/docs/Directive/07-DASHBOARD-REFERENCE.md)
* [11-REPORTING-REFERENCE.md](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/docs/Directive/11-REPORTING-REFERENCE.md)
* [14-STORAGE-REFERENCE.md](/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2/docs/Directive/14-STORAGE-REFERENCE.md)

---

# CHAPITRE 4 — CONCEPTS PRIX

LAWIM traite notamment :

* prix affiché ;
* prix négociable ;
* prix final ;
* loyer ;
* caution ;
* avance ;
* dépôt de garantie ;
* mensualité ;
* frais de service ;
* taxes ;
* estimation ;
* fourchette de marché ;
* historique de variation ;
* prix en monnaie locale ou étrangère.

---

# CHAPITRE 5 — RÈGLES DE NORMALISATION

Chaque prix doit être associé à :

* une devise ;
* une période de validité si nécessaire ;
* une source ;
* un contexte ;
* un niveau de négociation ;
* un historique.

Les formats libres doivent être convertis vers une représentation canonique.

---

# CHAPITRE 6 — RÈGLES DE MATCHING

Le moteur de matching utilise les prix pour :

* éliminer les biens hors budget ;
* classer les propositions ;
* calculer les marges de négociation ;
* comparer le marché local ;
* pondérer la pertinence d'un bien.

---

# CHAPITRE 7 — RÈGLES DE REPORTING

Le Reporting Engine et le Dashboard Engine exploitent les prix pour :

* suivre les loyers ;
* suivre les prix de vente ;
* suivre les cautions ;
* mesurer les variations ;
* produire des fourchettes de marché ;
* analyser la dynamique des offres.

---

# CHAPITRE 8 — RÈGLES DE DIALOGUE

Le moteur conversationnel et LAWIM AI peuvent :

* détecter un prix exprimé librement ;
* convertir les unités implicites ;
* distinguer le loyer de la caution ;
* distinguer le prix demandé du prix négocié ;
* demander une précision si le prix est ambigu.

---

# CHAPITRE 9 — RÈGLES ABSOLUES

Le référentiel prix doit toujours :

* rester indépendant du modèle économique de LAWIM ;
* éviter toute commission transactionnelle ;
* conserver l'historique des variations ;
* rester compatible avec le marché camerounais ;
* rester compatible avec le matching, le reporting, le dashboard et LAWIM AI.

Il est interdit :

* de transformer un prix en commission ;
* de masquer une devise ;
* d'écraser l'historique sans trace ;
* de publier un prix incohérent sans signalement.

---

# CHAPITRE 10 — OBJECTIF FINAL

Le référentiel prix doit permettre à LAWIM de comprendre, comparer, négocier et historiser tous les montants immobiliers utiles au parcours utilisateur.

---

# FIN DU DOCUMENT

Le présent **02I-PRICING-REFERENCE.md** constitue le référentiel officiel des prix immobiliers de LAWIM.
