# LAWIM

# 30B-TRANSLATION-REFERENCE.md

# Référentiel officiel des traductions

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le présent document définit la gestion officielle des clés et versions de traduction de LAWIM.

Il couvre notamment :

* les interfaces ;
* les notifications ;
* les emails ;
* les SMS ;
* Campay ;
* les API ;
* les erreurs ;
* les messages de validation ;
* les documents générés ;
* les textes d'aide.

---

# CHAPITRE 2 — CLÉS DE TRADUCTION

Chaque texte affichable doit être rattaché à une clé stable.

Une clé doit être :

* unique ;
* versionnée ;
* traçable ;
* réutilisable ;
* indépendante du rendu final.

---

# CHAPITRE 3 — VERSIONS

Chaque traduction doit conserver :

* la version source ;
* la version traduite ;
* la date ;
* l'auteur ;
* la validation ;
* l'historique.

---

# CHAPITRE 4 — RÈGLES

LAWIM doit :

* centraliser les chaînes ;
* interdire les textes codés en dur ;
* appliquer le fallback défini par le référentiel i18n/l10n ;
* versionner chaque modification ;
* journaliser les remplacements.

---

# CHAPITRE 5 — SOURCES

Les traductions peuvent provenir :

* du référentiel métier ;
* d'un administrateur validateur ;
* de LAWIM AI ;
* d'un traducteur humain ;
* d'un export ou import documentaire contrôlé.

LAWIM AI ne publie jamais une traduction sans validation humaine si le texte est critique.

---

# CHAPITRE 6 — OBJECTIF FINAL

Le référentiel des traductions garantit une présentation cohérente, versionnée et contrôlée des contenus LAWIM dans toutes les langues officielles.

---

# CHAPITRE 7 — LANGUES OFFICIELLES ET PERSISTANCE

Les langues officielles de l'interface sont:

* Français, langue par défaut;
* English;
* Pidgin English.

Le choix utilisateur doit être:

* mémorisé localement ou par le mécanisme officiel déjà validé;
* réappliqué à toute l'interface après reconnexion;
* propagé aux pages d'accès, dashboards, cartes, boutons, menus, messages d'erreur et messages de succès;
* appliqué aux libellés principaux, à `Nous écrire`, à `Et maintenant ?`, aux statistiques et à `Logout` / `Déconnexion` / `Comot`.

Une interface correctement traduite ne doit pas mélanger les langues au sein d'un même écran, sauf pour les éléments de marque ou les références officielles déjà validées.

---

# CHAPITRE 8 — ACCÈS ET CRÉATION DE COMPTE

Les écrans d'accès et de création de compte doivent être traduits de manière complète.

Les libellés clés à couvrir incluent notamment :

* `Identifiant` ;
* `Email, téléphone ou nom d'utilisateur` ;
* `Mot de passe` ;
* `Connexion` ;
* `Mot de passe oublié` ;
* `Créer un compte` ;
* `Nom complet` ;
* `Nom d'utilisateur` ;
* `Numéro WhatsApp` ;
* `Confirmation du mot de passe` ;
* `Langue préférée` ;
* `J'accepte les conditions`.

Les coordonnées compactes de pied de page doivent aussi être couvertes :

* `lawim.app` ;
* `contact@lawim.app` ;
* WhatsApp ;
* Facebook `@lawimofficial`.

Le choix de langue doit être conservé sur toute l'interface après reconnexion.
