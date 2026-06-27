# LAWIM

# 30-I18N-L10N-REFERENCE.md

# Référentiel officiel de l'internationalisation et de la localisation

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le présent document définit l'architecture multilingue officielle de LAWIM.

Il constitue la référence unique pour :

* l'internationalisation ;
* la localisation ;
* la gestion des langues ;
* les formats régionaux ;
* les règles de fallback ;
* la compatibilité Web, Mobile, API et IA.

---

# CHAPITRE 2 — PRINCIPE FONDAMENTAL

La langue est une donnée de contexte native.

Elle ne doit jamais être codée en dur dans un composant métier.

Toutes les couches doivent pouvoir afficher, interpréter et journaliser une même information dans plusieurs langues sans changer la logique métier.

---

# CHAPITRE 3 — LANGUES OFFICIELLES

LAWIM fonctionne nativement en :

* Français, langue par défaut ;
* English ;
* Pidgin English.

L'ajout d'une nouvelle langue doit rester possible sans modification du modèle métier.

---

# CHAPITRE 4 — SOURCES DE LANGUE

La langue active peut provenir de :

* la préférence utilisateur ;
* la session courante ;
* l'appareil ;
* l'en-tête `Accept-Language` ;
* l'en-tête `Content-Language` ;
* le contexte conversationnel ;
* la configuration admin ;
* une règle de fallback.

La hiérarchie de décision doit être documentée et stable.

---

# CHAPITRE 5 — FALLBACK

En cas d'absence de traduction ou de préférence valide, LAWIM revient automatiquement à :

* la langue utilisateur connue ;
* sinon le Français.

Le fallback doit être explicite, journalisé et testable.

---

# CHAPITRE 6 — FORMATS RÉGIONAUX

LAWIM doit gérer au minimum :

* les dates ;
* les heures ;
* les nombres ;
* les devises ;
* les fuseaux horaires ;
* les séparateurs décimaux ;
* les formats de téléphone ;
* les formats d'adresse.

Les formats régionaux doivent être cohérents avec la langue et le pays.

---

# CHAPITRE 7 — COUVERTURE TRANSVERSE

L'internationalisation couvre notamment :

* le Web ;
* le Mobile ;
* les API ;
* les dashboards ;
* LAWIM AI ;
* le Matching ;
* la Conversation ;
* les notifications ;
* les emails ;
* les SMS ;
* Campay ;
* le Reporting ;
* la documentation ;
* les tests.

---

# CHAPITRE 8 — RÈGLES ABSOLUES

Le système doit toujours :

✓ centraliser les clés de traduction ;

✓ éviter les textes codés en dur ;

✓ journaliser la langue effective ;

✓ permettre le changement dynamique ;

✓ conserver la cohérence des contenus fonctionnels ;

✓ rester compatible avec l'apprentissage continu.

Il ne doit jamais :

❌ mélanger une traduction et une règle métier ;

❌ dépendre d'un texte hardcodé pour une décision métier ;

❌ perdre la langue préférée de l'utilisateur ;

❌ casser la compatibilité d'une interface existante.

---

# CHAPITRE 9 — OBJECTIF FINAL

L'architecture i18n/l10n garantit que LAWIM reste exploitable par une audience multilingue sans fragmentation documentaire ni logique parallèle.
