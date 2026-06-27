# LAWIM

# 30D-MULTILINGUAL-SEARCH-REFERENCE.md

# Référentiel officiel de recherche multilingue

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le présent document définit la recherche tolérante et multilingue de LAWIM.

Il couvre :

* la recherche en français ;
* la recherche en English ;
* la recherche en Pidgin English ;
* les synonymes ;
* les variantes ;
* la correction orthographique ;
* la traduction automatique ;
* la recherche phonétique.

---

# CHAPITRE 2 — PRINCIPE FONDAMENTAL

Le moteur doit produire les mêmes résultats métier quelle que soit la langue utilisée.

La langue sert à l'expression.

Le sens sert au matching.

---

# CHAPITRE 3 — PIPELINE DE RECHERCHE

Le pipeline officiel est :

* détection de langue ;
* normalisation ;
* correction orthographique ;
* expansion des synonymes ;
* traduction fonctionnelle si nécessaire ;
* recherche phonétique ;
* classement ;
* restitution.

---

# CHAPITRE 4 — EXEMPLES DE SYNONYMES

Le moteur doit comprendre par exemple :

* House ;
* Maison ;
* Home ;
* Compound ;
* Habitation ;
* Logement ;
* Appartement ;
* Flat ;
* Apartment ;
* Studio ;
* Chambre.

---

# CHAPITRE 5 — RÈGLES

La recherche ne doit jamais :

* dépendre de la langue exacte saisie ;
* ignorer les expressions locales ;
* bloquer une recherche à cause d'une faute fréquente ;
* produire un résultat différent pour le même concept métier.

---

# CHAPITRE 6 — OBJECTIF FINAL

La recherche multilingue doit permettre à LAWIM d'interpréter un besoin dans plusieurs langues sans divergence de résultat métier.

