# LAWIM

# 07-DASHBOARD-REFERENCE.md

# Référentiel officiel du Dashboard

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le présent document définit les règles officielles du Dashboard de LAWIM.

Il constitue la référence unique pour :

* l'affichage d'accueil ;
* les widgets ;
* les tableaux de bord par rôle ;
* les raccourcis métiers ;
* les alertes de priorité ;
* les vues contextualisées ;
* les indicateurs de pilotage.

---

# CHAPITRE 2 — PRINCIPE FONDAMENTAL

Le Dashboard est une projection opérationnelle de la plateforme.

Il affiche l'état de LAWIM, mais ne crée aucune règle métier et ne devient jamais la source de vérité.

Les décisions proviennent des moteurs officiels, pas du Dashboard.

---

# CHAPITRE 3 — RÉFÉRENCES OBLIGATOIRES

Le Dashboard applique obligatoirement :

* 00-CONSTITUTION.md ;
* 03-CONVERSATION-REFERENCE.md ;
* 04-MATCHING-REFERENCE.md ;
* 05-WORKFLOW-REFERENCE.md ;
* 06-DATABASE-REFERENCE.md ;
* 02I-PRICING-REFERENCE.md ;
* 08-ROLE-REFERENCE.md ;
* 09-GEOLOCATION-REFERENCE.md ;
* 10-NOTIFICATION-REFERENCE.md ;
* 11-REPORTING-REFERENCE.md ;
* 29-CAMPAY-PAYMENT-REFERENCE.md ;
* 13-ARCHITECTURE-GOVERNANCE-REFERENCE.md.

---

# CHAPITRE 4 — COMPORTEMENT DYNAMIQUE

Le Dashboard varie selon :

* le rôle de l'utilisateur ;
* les permissions disponibles ;
* les workflows actifs ;
* les événements récents ;
* les notifications prioritaires ;
* les recommandations de LAWIM AI ;
* le contexte géographique et métier.

Deux utilisateurs ne doivent jamais voir exactement la même première page si leur contexte diffère.

---

# CHAPITRE 5 — CONTENU PRIORITAIRE

Le Dashboard met en avant en priorité :

* les actions urgentes ;
* les dossiers en retard ;
* les visites à venir ;
* les matchs récents ;
* les demandes non traitées ;
* les services payants en attente ;
* les paiements Campay en attente de confirmation ;
* les alertes de sécurité ;
* les éléments nécessitant validation humaine.

Les statistiques ne doivent jamais masquer une action critique.

---

# CHAPITRE 6 — VUES PAR RÔLE

Exemples de vues :

* demandeur : biens proposés, suivi du dossier, visites, messages, notifications ;
* propriétaire : demandes liées, mise en relation, visites, état des biens, services ;
* agence : portefeuille, dossiers, agents, performances, validations ;
* membre LAWIM : files de traitement, alertes, audits, contrôles ;
* administrateur : supervision, sécurité, gouvernance, indicateurs globaux.

Les vues sont spécialisées, mais la logique de fond reste commune.

---

# CHAPITRE 7 — WIDGETS

Les widgets sont les unités d'affichage du Dashboard.

Ils peuvent présenter :

* des cartes de synthèse ;
* des listes d'actions ;
* des indicateurs ;
* des calendriers ;
* des cartes géographiques ;
* des notifications ;
* des recommandations IA ;
* des raccourcis vers les workflows.

Un widget lent ne doit jamais bloquer l'ensemble du Dashboard.

---

# CHAPITRE 8 — PERSONNALISATION

L'utilisateur peut personnaliser :

* la langue ;
* certains raccourcis ;
* l'ordre des widgets secondaires ;
* certains filtres d'affichage ;
* les préférences visuelles autorisées.

Les éléments critiques restent imposés par le système.

La personnalisation doit être synchronisée sur les supports autorisés.

---

# CHAPITRE 9 — CONTINUITÉ MULTI-SUPPORT

Le Dashboard doit offrir une expérience cohérente sur :

* Web ;
* Mobile ;
* Tablette.

L'utilisateur doit retrouver la même logique de travail, même si la présentation change selon l'écran.

---

# CHAPITRE 10 — PERFORMANCE ET ACCESSIBILITÉ

Le Dashboard doit être :

* rapide à ouvrir ;
* réactif ;
* lisible ;
* compatible avec des connexions moyennes ;
* utilisable sur petits écrans ;
* accessible aux contrastes et tailles de caractères raisonnables.

Les contenus critiques doivent rester visibles sans action supplémentaire.

---

# CHAPITRE 11 — NOTIFICATIONS ET ALERTES

Les alertes prioritaires peuvent être affichées directement dans le Dashboard.

Le Dashboard doit :

* regrouper les notifications similaires ;
* distinguer les urgences des simples informations ;
* éviter la surcharge visuelle ;
* faire apparaître clairement l'origine de l'événement.

---

# CHAPITRE 12 — TRAÇABILITÉ

Le Dashboard ne conserve pas la vérité métier, mais il doit refléter des données traçables.

Chaque bloc affiché doit pouvoir être relié :

* à un workflow ;
* à un lead ;
* à une notification ;
* à une opération de paiement ;
* à un indicateur ;
* à une source de données.

---

# CHAPITRE 13 — RÈGLES ABSOLUES

Le Dashboard doit toujours :

* respecter les permissions ;
* masquer les informations non autorisées ;
* éviter les doublons d'information ;
* ne jamais inventer de donnée ;
* ne jamais décider à la place des moteurs ;
* rester conforme aux référentiels officiels.

Il est interdit :

* d'afficher une commission transactionnelle inexistante comme revenu LAWIM ;
* de présenter un état non confirmé comme validé ;
* de contourner les règles de confidentialité.

---

# CHAPITRE 14 — OBJECTIF FINAL

Le Dashboard doit donner à chaque utilisateur une vision claire, utile et contextuelle de ce qui mérite son attention, sans rompre la cohérence des moteurs ni la traçabilité des décisions.

---

# CHAPITRE 15 — SUPPORT MULTILINGUE

Le Dashboard doit afficher les libellés, KPI et notifications dans la langue de l'utilisateur lorsque cela est disponible.

Les statistiques linguistiques doivent être visibles et exploitables.

Le Dashboard s'appuie sur 30-I18N-L10N-REFERENCE.md et 30B-TRANSLATION-REFERENCE.md pour le rendu multilingue.

---

# CHAPITRE 16 — TRACKING MARKETING ET STATISTIQUES

Les dashboards existants doivent être enrichis avec des blocs marketing sans créer de dashboard supplémentaire.

Le Dashboard Administration peut afficher notamment :

* le nombre total de campagnes ;
* le nombre de publications ;
* le nombre de clics ;
* le nombre de clics uniques ;
* les robots détectés ;
* les redirections ;
* les conversions ;
* les paiements Campay ;
* les revenus des services ;
* les meilleurs canaux ;
* les meilleurs acteurs.

Le Dashboard Reporting peut afficher notamment :

* les comparaisons annuelles ;
* les comparaisons mensuelles ;
* les comparaisons hebdomadaires ;
* les comparaisons journalières ;
* l'évolution des campagnes ;
* l'évolution des publications ;
* l'évolution des acteurs ;
* l'évolution des canaux.

Le Dashboard Matching peut afficher notamment :

* l'origine des matchings ;
* la provenance par canal ;
* la provenance par campagne ;
* la provenance par publication ;
* la provenance par acteur ;
* la provenance par ville ;
* la provenance par type de bien ;
* la provenance par langue.

Le Dashboard Campay peut afficher notamment :

* les paiements issus de Facebook, WhatsApp, Telegram, Instagram, TikTok, du site LAWIM, du QR Code, des emails, des SMS, des partenaires, des agences, des agents et des membres LAWIM ;
* les revenus par campagne ;
* les revenus par publication ;
* les revenus par acteur ;
* les revenus par canal.

Le Dashboard Continuous Learning peut afficher notamment :

* les meilleures campagnes ;
* les meilleurs horaires ;
* les meilleurs jours ;
* les meilleures villes ;
* les meilleurs quartiers ;
* les meilleurs types de biens ;
* les canaux les plus performants ;
* les acteurs les plus performants ;
* les publications les plus performantes ;
* les langues les plus efficaces ;
* les recommandations IA.

Le Dashboard Administration peut également afficher les tableaux SIE :

* les sources d'acquisition actives ;
* les sources avec contexte enrichi ;
* les imports d'URL ;
* les Reference Codes ;
* les liens WhatsApp générés ;
* les statistiques de conversion par source.

---

# CHAPITRE 17 — OBJECTIF FINAL

Le présent **07-DASHBOARD-REFERENCE.md** constitue le référentiel officiel du Dashboard de LAWIM.

# FIN DU DOCUMENT
