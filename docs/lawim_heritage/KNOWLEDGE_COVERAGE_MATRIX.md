# KNOWLEDGE COVERAGE MATRIX — Matrice de couverture des connaissances

**Sources :** LAWIM, LAWIMA, ancienne_structure
**Principe :** Cartographie de présence des connaissances par branche et domaine — sans validation

---

## 1. Matrice de couverture par domaine

| Domaine | Sous-domaine | LAWIM | LAWIMA | ancienne | Source la plus riche |
|---------|-------------|-------|--------|----------|---------------------|
| **Immobilier** | Types de biens | ✓✓ | ✓ | ✓ | LAWIM (9 docs Directive/02) |
| | Attributs | ✓✓ | ✓ | ✓ | LAWIM Directive/02H |
| | Cycles de vie | ~ | ✓✓ | ✓✓ | LAWIMA property_lifecycle_engine |
| | Transactions | ✓ | ✓✓ | ✓ | LAWIMA (données + code) |
| | Prix/scoring | ✓ | ✓✓ | ✓ | LAWIMA pricing, budget scoring |
| | Titres fonciers | ~ | ✓ | ✓ | LAWIMA title_status |
| | Qualité données | ~ | ✓✓ | ~ | LAWIMA data_quality_engine |
| **Géographie** | Villes | ✓✓ | ✓ | ✓ | LAWIM (fichiers cities + connaissance) |
| | Quartiers | ✓✓ | ✓✓ | ✓ | LAWIM + LAWIMA (11 fichiers) |
| | Hiérarchie territ. | ✓✓ | ~ | ~ | LAWIM district_hierarchy |
| | GPS | ✓✓ | ~ | ~ | LAWIM (geography/ fichiers GPS) |
| | Alias/normalisation | ✓ | ✓✓ | ✓ | LAWIMA location_normalizer |
| | Scoring géo | ~ | ✓ | ✓ | LAWIMA property_matching_v1 |
| | Districts manquants | ✓ | ~ | ~ | LAWIM (3 fichiers .txt) |
| **Qualification** | Profils utilisateurs | ✓ | ✓✓ | ✓ | LAWIMA lead_classifier |
| | Scoring leads | ✓ | ✓✓ | ✓ | LAWIMA (2 dossiers scoring) |
| | Seuils (HOT/WARM/COLD) | ~ | ✓✓ | ✓✓ | LAWIMA (V1 + V5) |
| | Boosters/pénalités | ~ | ✓✓ | ✓ | LAWIMA lead_classifier |
| | Pipeline V5 | ~ | ✓✓ | ✓✓ | LAWIMA RULE_ENGINE_V5 |
| | Champs obligatoires | ✓✓ | ~ | ~ | LAWIM qualification-questions |
| **Intentions** | Buy | ✓✓ | ✓✓ | ✓✓ | Identique dans les 3 branches |
| | Rent | ✓✓ | ✓✓ | ✓✓ | Identique dans les 3 branches |
| | Sell | ✓✓ | ✓✓ | ✓✓ | Identique dans les 3 branches |
| | Search | ✓✓ | ✓✓ | ✓✓ | Identique dans les 3 branches |
| | Investor | ✓✓ | ✓✓ | ✓✓ | Identique dans les 3 branches |
| | Sous-intentions | ✓ | ✓✓ | ✓ | LAWIMA (code engine) |
| **Conversation** | Règles dialogue | ✓✓ | ✓✓ | ✓ | LAWIM + LAWIMA |
| | Politique réponse | ✓ | ✓✓ | ✓✓ | LAWIMA RESPONSE_POLICY |
| | Mémoire | ~ | ✓✓ | ✓✓ | LAWIMA conversation_memory |
| | Long terme | ~ | ✓✓ | ✓✓ | LAWIMA long_term_memory |
| | Relances | ~ | ✓✓ | ✓✓ | LAWIMA follow_up_system |
| | Commandes | ~ | ✓✓ | ~ | LAWIMA engine |
| | Feedback | ~ | ✓✓ | ✓✓ | LAWIMA feedback_handler |
| | Langues (FR/EN/PID) | ✓ | ✓✓ | ✓✓ | LAWIMA multilingual_responses |
| **Matching** | Dimensions/poids | ✓ | ✓✓ | ✓✓ | LAWIMA property_matching_v1 |
| | Tolérances budget | ✓ | ✓✓ | ✓✓ | LAWIMA config |
| | Boosts/exclusions | ✓ | ✓✓ | ✓✓ | LAWIMA matcher v5 |
| | Scoring étoiles | ~ | ✓✓ | ✓✓ | LAWIMA matcher v5 |
| | Rematching | ✓ | ~ | ~ | LAWIM matching docs |
| | Request engine | ✓ | ~ | ~ | LAWIM 3 docs request engine |
| **CRM** | Rôles | ✓✓ | ✓✓ | ✓ | LAWIM Directive/08 + LAWIMA user_roles |
| | Permissions | ~ | ✓✓ | ~ | LAWIMA SQL scripts |
| | États utilisateur | ~ | ✓✓ | ✓✓ | LAWIMA USER_STATES |
| | Événements | ~ | ✓✓ | ✓✓ | LAWIMA EVENT_TYPES |
| | Agents (optin/rating) | ~ | ✓✓ | ✓✓ | LAWIMA agent_optin/rating |
| | Dashboards | ~ | ✓✓ | ✓✓ | LAWIMA dashboards (8 versions) |
| | Identity resolution | ~ | ✓✓ | ✓✓ | LAWIMA identity_resolution |
| | Anti-spam | ~ | ✓✓ | ✓✓ | LAWIMA anti_spam |
| **Négociation** | Objections | ✓✓ | ~ | ~ | LAWIM trust patterns |
| | Peurs (12+8) | ✓✓ | ~ | ~ | LAWIM fraud-signals |
| | Techniques vente | ✓✓ | ~ | ~ | LAWIM sales-playbook |
| | Argumentaires | ✓✓ | ~ | ~ | LAWIM playbook + commercial/ |
| | Relance commerciale | ~ | ✓✓ | ~ | LAWIMA follow_up_system |
| **Langage** | Synonymes | ✓ | ✓✓ | ✓ | LAWIMA entity_linking |
| | Alias | ✓ | ✓✓ | ✓ | LAWIMA search_aliases |
| | Fautes courantes | ✓✓ | ✓✓ | ✓ | LAWIM + LAWIMA (5 fichiers typo) |
| | Expressions cameroun. | ✓✓ | ✓✓ | ✓ | LAWIM whatsapp_language |
| | Vocabulaire immo | ✓ | ✓ | ✓ | LAWIM + LAWIMA |
| | Formatage téléphone | ~ | ✓✓ | ✓✓ | LAWIMA phone_formatter |
| **Datasets** | JSON knowledge | ✓✓ | ✓✓✓ | ✓ | LAWIMA (200+ fichiers) |
| | CSV runtime | ~ | ✓✓ | ✓✓ | LAWIMA database |
| | SQL schemas | ~ | ✓✓ | ✓✓ | LAWIMA scripts |
| | Config IA | ~ | ✓✓ | ✓✓ | LAWIMA 06_AI_MODELS |
| | Règles moteur | ~ | ✓✓ | ✓✓ | LAWIMA RULE_ENGINE (5 versions) |
| **Monétisation** | Services payants | ✓ | ✓✓ | ~ | LAWIMA monetisation |
| | Feature flags | ~ | ✓✓ | ~ | LAWIMA FEATURE_FLAGS |
| | Credits/boosts | ~ | ✓ | ~ | LAWIMA SQL scripts |
| **Sécurité** | RGPD | ✓ | ✓✓ | ✓ | LAWIMA RESPONSE_POLICY |
| | Anti-fraud | ✓✓ | ✓ | ~ | LAWIM fraud-signals |
| | Anti-spam | ~ | ✓✓ | ✓✓ | LAWIMA anti_spam |
| **Documentation** | Architecture | ✓✓ | ~ | ~ | LAWIM Directive/ |
| | Implémentation | ✓✓ | ~ | ~ | LAWIM Directive/ |
| | Marketing/vente | ✓✓ | ✓ | ~ | LAWIM sales-playbook + brand |
| | Finance | ~ | ✓ | ~ | LAWIMA docx |
| | Technique | ✓✓ | ✓ | ✓ | LAWIM + LAWIMA |

Légende :
- ✓✓✓ : Source primaire exhaustive
- ✓✓ : Source complète
- ✓ : Source partielle
- ~ : Absent ou non trouvé

## 2. Domaines les plus aboutis

| Rang | Domaine | Raison |
|------|---------|--------|
| 1 | **Immobilier (types/attributs)** | 9 documents de référence dédiés + données JSON |
| 2 | **Géographie** | Hiérarchie complète, 11 fichiers quartiers, GPS, alias |
| 3 | **Scoring/Qualification** | 5 versions évolutives de règles (V2→V5), 2 jeux de données |
| 4 | **Langage WhatsApp** | 7 fichiers de corpus, 5 fichiers de correction |
| 5 | **Conversation** | Mémoire, relances, feedback, commandes, politique |
| 6 | **Matching** | Dimensions documentées, 3 versions d'implémentation |
| 7 | **CRM** | Rôles, permissions, dashboards, cycles de vie |
| 8 | **Intentions** | 5 fichiers complets FR/EN/Pidgin |

## 3. Domaines les moins aboutis / à investiguer

| Rang | Domaine | Lacune |
|------|---------|--------|
| 1 | **Négociation détaillée** | Playbook existe mais pas de règles structurées exploitables |
| 2 | **Monétisation** | Feature flags désactivés, logique partielle |
| 3 | **Fraude** | 25 signaux documentés mais pas de règles de détection automatisées |
| 4 | **Partenaires externes** | Rôles (notaire, architecte, etc.) listés mais pas de processus associés |
| 5 | **Workflows avancés** | States et events définis mais pas de règles de transition automatisées |

## 4. Connaissances potentiellement perdues

| Connaissance | Raison de l'absence |
|-------------|---------------------|
| **Logique détaillée de l'ADR-009** | Documenté dans LAWIM_V2 mais pas dans les branches legacy |
| **Processus d'escalade complets** | Partiellement dans conversation-patterns.md |
| **Règles de pricing avancées** | pricing.json présent mais contenu non vérifié |
| **Détail des documents financiers (.docx)** | Format non lisible, contenu non extrait |
| **Contenu des documents marketing (.odt)** | Format non lisible, contenu non extrait |

## 5. Connaissances dupliquées (même contenu dans plusieurs branches)

| Connaissance | Branches | Degré de similarité |
|-------------|----------|---------------------|
| Intents (5 fichiers) | LAWIM + LAWIMA + ancienne | Identique |
| Quartiers | LAWIM + LAWIMA | Très similaire |
| WhatsApp language (7 fichiers) | LAWIM + LAWIMA | Identique |
| Entity linking | LAWIM + LAWIMA + ancienne | Identique |
| Typo database | LAWIM + LAWIMA + ancienne | Identique |
| Property types | LAWIM + LAWIMA + ancienne | Similaire |
| User roles | LAWIM + LAWIMA + ancienne | Identique |
| Lead scoring | LAWIM + LAWIMA | Similaire (chemins différents) |

## 6. Connaissances uniques par branche

### LAWIM (uniques)
- 9 documents de référence propriété (Directive/02*)
- Constitution (23 articles)
- Sales playbook
- Brand book
- Business plan
- Operations manual
- Marketing plan
- Master dataset (8765 lignes)
- Signaux de fraude (25 détails)
- Matrice d'affinité des villes
- Modèle comportement diaspora
- District hierarchy
- GPS data (4 fichiers)
- Districts manquants (3 fichiers .txt)
- Analyse marché immobilier
- 7 documents matching engine
- 3 documents request engine

### LAWIMA (uniques)
- 5 versions de règles moteur (V2→V5)
- Data quality engine (scores complets)
- Knowledge builder (32 champs profil)
- Identity resolution (algorithme)
- Feature flags
- Dashboards (8 versions agent, 4 versions master)
- Monétisation (code)
- Archives (61+84 fichiers)
- Prompt système IA (73 lignes)
- 84 fichiers repair backup

### ancienne_structure (uniques)
- Aucun contenu unique identifié (sous-ensemble de LAWIMA)

---

*Document patrimonial — Aucune décision de reconstruction n'est prise ici.*
