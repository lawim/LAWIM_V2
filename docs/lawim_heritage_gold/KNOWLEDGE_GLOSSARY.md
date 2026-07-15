# KNOWLEDGE GLOSSARY — Glossaire des Termes LAWIM (Gold Standard)

**Mission :** LAWIM Heritage Gold
**Date :** 15 juillet 2026
**Domaine :** Terminologie LAWIM exhaustive
**Statut :** Validé — Toute reconstruction doit respecter cette terminologie.

---

| Terme | Definition | Source | Domain |
|-------|------------|--------|--------|
| Accompagnement | Service payant (50 000 FCFA) d'assistance personnalisée pour la recherche ou la vente d'un bien immobilier | Directive/03-CONVERSATION-REFERENCE.md | Conversation |
| Acheteur | Utilisateur cherchant à acquérir un bien immobilier. Score de base : 60 | lead_classifier_v1.json | Qualification |
| Agent | Professionnel de l'immobilier inscrit sur LAWIM. Reçoit des leads par zone géographique. Noté par les clients (1-5) | 08-ROLE-REFERENCE.md | CRM |
| Agence | Structure professionnelle employant des agents. Peut gérer plusieurs agents et voir tous les leads | implement_all.sql | CRM |
| Alias | Variante orthographique ou synonyme d'un nom de lieu ou de type de bien | district_aliases.json | Language |
| Anonymisation | Processus RGPD de suppression des données personnelles d'un utilisateur. Déclenché par SUPPRIMER MES DONNÉES. Délai : 7 jours | Directive/15-SECURITY-REFERENCE.md | Security |
| Anti-spam | Système de limitation du nombre de messages par minute (10 msg/min). Blocage automatique pour 60 minutes | anti_spam.py | Security |
| Appartement meublé | Sous-type résidentiel avec pondérations spécifiques Type=15%, Op=10%, Ville/quartier=18%, Budget=18%, Chambres=12%, Mobilier/équip=12%, Durée=5%, Dispo=5%, Qualité=5% | Directive/04-DECISION-ENGINE-REFERENCE.md | Property |
| Appartement | Type de bien résidentiel avec pondérations Type=15%, Op=10%, Ville/quartier=20%, Budget=20%, Chambres=15%, Cuisine/douches=8%, Parking/balcon/étage=5%, Dispo=4%, Qualité=3% | Directive/04-DECISION-ENGINE-REFERENCE.md | Property |
| Apprentissage global | Connaissance du marché construite progressivement : délai moyen de vente par ville, quartiers demandés, saisonnalité | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch95) | Matching |
| Archivage | Passage d'une propriété en statut archivé après 90 jours d'inactivité | property_lifecycle_engine.py | Property |
| Assistant | Rôle niveau 5. Permet de voir les statistiques | implement_all.sql | CRM |
| Attribut | Caractéristique d'un bien immobilier (surface, chambres, étage, parking, etc.) | Directive/02H-ATTRIBUTE-CATALOG.md | Property |
| Bien agricole | Catégorie de bien avec pondérations Type=15%, Localité=15%, Prix=15%, Superficie=20%, Activité=10%, Situation juridique=10% | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch56) | Property |
| Bien immobilier | Unité foncière ou immobilière mise en vente ou location sur LAWIM | Directive/02-PROPERTY-REFERENCE.md | Property |
| Bien mixte/spécial | Catégorie avec pondérations Usage principal=20%, Usage secondaire=8%, Ville/quartier=15%, Prix=15%, Surface=12% | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch58) | Property |
| Blocage | Suspension temporaire d'un utilisateur après dépassement du quota de messages (60 minutes) | anti_spam.py | Security |
| Boost | Option payante permettant d'augmenter la visibilité d'une propriété ou d'accélérer le matching | FEATURE_FLAGS.json | Monetisation |
| Boost rule | Condition de matching avec bonus de score (ex: exact_neighborhood_match+25, exact_city_match+20) | property_matching_v1.json | Matching |
| Broker | Courtier ou intermédiaire non-agréé par LAWIM. Détecté par mots-clés spécifiques | RULE_ENGINE_V3.json | Qualification |
| Budget | Montant qu'un utilisateur est prêt à dépenser. Extrait automatiquement des messages | lead_classifier_v1.json | Qualification |
| Budget tolerance | Écart budgétaire accepté par type d'opération : rent=20%, buy=15%, invest=25% | property_matching_v1.json | Matching |
| Bureau/cabinet | Type commercial avec pondérations Type=15%, Ville/quartier=20%, Budget=20%, Surface=12% | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch53) | Property |
| Camfranglais | Langue camerounaise mélangeant français, anglais et pidgin. Présente dans les expressions WhatsApp mais PAS comme langue supportée à part entière | whatsapp_language.json | Language |
| CamPay | Service de paiement mobile camerounais intégré (feature flag désactivé) | FEATURE_FLAGS.json | Financial |
| Champ obligatoire | Information minimale requise pour qualifier une demande (type de bien, ville, budget) | Directive/03-CONVERSATION-REFERENCE.md | Qualification |
| City match | Correspondance au niveau de la ville dans le matching (pondération : 30% en V1) | property_matching_v1.json | Matching |
| City affinity | Matrice d'affinité entre villes camerounaises pour le matching géographique | city-affinity-matrix.md | Geography |
| Closing | Techniques de conclusion de vente documentées dans le sales playbook | Directive/48-LAWIM-SALES-PLAYBOOK.md | Negotiation |
| Cold | Classe de lead à faible priorité (score < 40 en V1, < 0.3 en V5) | lead_classifier_v1.json | Qualification |
| Commande | Mot-clé spécial : SIGNALER, SUPPRIMER MES DONNÉES, ACCOMPAGNEMENT, STATS, LANGUE, etc. | RESPONSE_POLICY.md | Conversation |
| Compatibilité critique | Niveau 1 de compatibilité : champs obligatoires sans lesquels aucun matching n'est possible | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch9) | Matching |
| Compatibilité fonctionnelle | Niveau 2 : le bien répond aux besoins principaux (chambres, superficie, budget) | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch9) | Matching |
| Compatibilité confort | Niveau 3 : garage, forage, jardin, piscine, balcon, terrasse | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch9) | Matching |
| Compatibilité préférentielle | Niveau 4 : quartier préféré, orientation, vue, proximité école/travail | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch9) | Matching |
| Complétude | Score de qualité basé sur la présence et qualité des champs (60% du Data Quality Score) | data_quality_engine.py | Property |
| Confiance | Score de fiabilité d'une source de données (agent=90, google_form=85, import=70, whatsapp=50, unknown=30) | data_quality_engine.py | Property |
| Constitution | Document fondamental de LAWIM définissant les 23 principes du projet | Directive/00-CONSTITUTION.md | Constitution |
| ContactChannel | Table de stockage des moyens de contact d'une personne (téléphone, email, WhatsApp) | implement_all.sql | CRM |
| Conversation memory | Mémoire de session conversationnelle avec 4 niveaux de familiarité (J1-J4) | conversation_memory.py | Conversation |
| Crédit | Solde d'un agent pour l'achat de leads. Prix par lead par défaut : 500 FCFA | agent_dashboard.py | CRM |
| Data Quality Engine | Module d'évaluation de la qualité des données immobilières (score sur 100, grades A+ à D) | data_quality_engine.py | Property |
| Data Quality Score | Score composite = complétude * 0.6 + fiabilité * 0.4 | data_quality_engine.py | Property |
| Décision Engine | Moteur de décision avancé couvrant matching, scoring, priorités et apprentissage (6 parties, 99+ chapitres) | Directive/04-DECISION-ENGINE-REFERENCE.md | Matching |
| Demandeur | Rôle de base d'un utilisateur cherchant un bien (niveau 1) | implement_all.sql | CRM |
| Département | Niveau administratif entre région et arrondissement (Cameroun) | district_hierarchy.json | Geography |
| Diaspora | Camerounais vivant à l'étranger. Détecté par localisation ou indicatif téléphonique. Score boosté (+25) | diaspora_filter.py | Qualification |
| Diaspora investor | Investisseur de la diaspora. Score de base le plus élevé (95). Bonus matching +20 | lead_classifier_v1.json | Qualification |
| Dispute | Litige utilisateur. Créé par la commande SIGNALER. Statuts : open, resolved | implement_all.sql | CRM |
| Distance réelle | Calcul de proximité géographique via GPS (pas à vol d'oiseau) | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch15) | Geography |
| District | Niveau de la hiérarchie territoriale camerounaise (entre commune/ville et quartier) | district_hierarchy.json | Geography |
| Document score | Score de situation documentaire : Titre foncier=100%, En cours=80%, Droit coutumier=60%, Inconnu=40% | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch29) | Matching |
| Doublon | Personne ou propriété enregistrée plusieurs fois. Détecté par téléphone, email ou similarité de nom | identity_resolution.py | CRM |
| Droit coutumier | Régime foncier traditionnel. Score documentaire : 60% | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch29) | Property |
| Entity linking | Résolution d'entités (correspondance entre termes équivalents, synonymes, abréviations) | entity_linking.json | Language |
| Escalade | Règle de dialogue définissant quand passer d'une réponse IA à un humain | Directive/03-CONVERSATION-REFERENCE.md | Conversation |
| État utilisateur | Statut d'un utilisateur (NEW_USER, SEARCHING_PROPERTY, PROPERTY_OWNER, AGENT, LEAD_CREATED, PREMIUM_AGENT, INACTIVE) | USER_STATES.json | CRM |
| Événement | Type d'action système (message.received, intent.detected, user.created, lead.created, match.generated, etc.) | EVENT_TYPES.json | CRM |
| Exclusion | Règle de matching éliminant des biens (archivé, budget hors tolérance, ville différente, déjà envoyé) | property_matcher_v5.py | Matching |
| Expression négociation | Termes de négociation de prix (prix ferme, à débattre, dernier prix, prix négociable) | negotiation.json | Negotiation |
| Famille de biens | Catégorie principale (Résidentiel, Commercial, Industriel, Terrain, Agricole, Hôtellerie, Projet) | Directive/02-PROPERTY-REFERENCE.md | Property |
| Feature flag | Interrupteur de fonctionnalité. Permet d'activer/désactiver sans déploiement | FEATURE_FLAGS.json | Configuration |
| Feedback | Évaluation de l'utilisateur (👍 = 5, 👎 = 1, note de 1 à 5) | feedback_handler.py | Conversation |
| Fiabilité | Score de confiance d'une source de données (40% du Data Quality Score) | data_quality_engine.py | Property |
| Flow | Séquence d'étapes de qualification pour une intention donnée | RULE_ENGINE_V5.json | Qualification |
| Follow-up | Système de relance automatique à J1(24h), J7(168h), J30(720h), J90(2160h) | follow_up_system.py | Conversation |
| Fraude | Système anti-fraude à 4 couches (broker_spam, duplicate_listing, fake_price, suspicious_urgency) | RULE_ENGINE_V5.json | Security |
| Grade | Note de qualité (A+ ≥80, A ≥60, B ≥40, C ≥20, D <20) | data_quality_engine.py | Property |
| GreenAPI | Fournisseur de l'API WhatsApp utilisé par LAWIM | follow_up_system.py | Conversation |
| Hiérarchie territoriale | Structure administrative : Pays → Région → Département → Arrondissement → Commune → Ville → District → Quartier | district_hierarchy.json | Geography |
| Holder score | Indice de fiabilité du détenteur = temps réponse × taux acceptation × visites honorées × transactions conclues | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch31) | Matching |
| Hot | Classe de lead prioritaire (score ≥ 80 en V1, ≥ 0.8 en V5). Action : appeler immédiatement | lead_classifier_v1.json | Qualification |
| Hôtel/auberge | Type avec pondérations Type=12%, Ville/quartier=15%, Prix=15%, Chambres/unités=18%, Taux occupation=10% | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch55) | Property |
| Identity resolution | Détection et fusion des personnes enregistrées en double. Scores : téléphone=100, email=95, nom+téléphone≥40 | identity_resolution.py | CRM |
| Immeuble/mini-cité | Type avec pondérations Type=15%, Ville/quartier=15%, Prix=15%, Unités=15%, Type d'unités=10%, Revenus=12% | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch48) | Property |
| Indice de tension | Mesure de tension marché par ville+quartier+type+opération (95% = très tendu, 25% = détendu) | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch96) | Matching |
| Intention | Type de besoin exprimé : buy, rent, sell, search, investor | intents/*.json | Qualification |
| Intermédiaire | Positionnement de LAWIM — mise en relation sans commission | Directive/00-CONSTITUTION.md | Constitution |
| Investisseur | Utilisateur cherchant un investissement immobilier. Score de base : 80 | lead_classifier_v1.json | Qualification |
| Knowledge builder | Module de construction de profil utilisateur (25 champs extraits) | knowledge_builder.py | Qualification |
| Knowledge enricher | Module d'apprentissage automatique de nouvelles connaissances depuis les conversations | knowledge_enricher.py | Qualification |
| Knowledge entry | Unité de connaissance (type, valeur, synonymes, confiance, source) | knowledge_entries (SQL) | Knowledge |
| Langue | Langue supportée : français (défaut), anglais, pidgin. Camfranglais partiel dans expressions | RESPONSE_POLICY.md | Language |
| Lead | Opportunité commerciale générée par la qualification d'une conversation | lead_classifier_v1.json | Qualification |
| Lead scoring rules | Poids de scoring : budget=20, location=15, urgency=20, diaspora=10, phone=5, property_type=15, investment_profile=10 | lead_scoring_rules.json | Qualification |
| Lead temperature | Classification des leads : HOT/WARM/COLD/LOW (V1) ou HOT/WARM/COLD/SPAM (V5) | lead_classifier_v1.json | Qualification |
| Levenshtein | Algorithme de distance utilisé pour la normalisation des noms de lieux (seuil max 3) | location_normalizer.py | Language |
| Litige | Réclamation utilisateur (voir Dispute) | implement_all.sql | CRM |
| Locataire | Utilisateur cherchant à louer. Score de base : 40 | lead_classifier_v1.json | Qualification |
| Localisation floue | Expression approximative (barrage, carrefour, axe principal, non loin de) | location_normalizer.py | Geography |
| Long-term memory | Mémoire au-delà de la session (rétention : 365 jours dans le code) | long_term_memory.py | Conversation |
| Maison | Type résidentiel avec pondérations Type=15%, Op=10%, Ville/quartier=18%, Budget=18%, Chambres=15%, Cour/clôture=10% | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch45) | Property |
| Master | Super-administrateur LAWIM (niveau 7, permissions totales). Password: lawim2026 | implement_all.sql | CRM |
| Matching | Processus d'appariement entre demande (lead) et offre (propriété) | Directive/04-MATCHING-REFERENCE.md | Matching |
| Matching dimensions (DE) | 6 dimensions Décision Engine : Type=25%, Opération=20%, Budget=15%, Localisation=15%, Critiques=15%, Recommandées=10% | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch26) | Matching |
| Mémoire | Système de reconnaissance avec 4 niveaux de familiarité (J1=1j, J2≤7j, J3≤30j, J4>30j) | conversation_memory.py | Conversation |
| Message history | Historique des messages pour analyse de cohérence et détection de changements d'intention | RULE_ENGINE_V5.json | Conversation |
| Monétisation | Modèle économique : crédits agents (500 FCFA/lead), boost, accompagnement 50k, zéro commission | core/monetisation.py | Monetisation |
| Multi-intention | Capacité à détecter plusieurs intentions dans un même message (activée) | RULE_ENGINE_V5.json | Qualification |
| Neighborhood match | Correspondance au niveau du quartier (pondération : 25% en V1) | property_matching_v1.json | Matching |
| Niveau de confiance | Score implicite de fiabilité basé sur vérification téléphone, historique, notation | identity_resolution.py | CRM |
| Non-compensation | Règle : un terrain bien situé ne compense pas recherche de villa ; piscine ne compense pas budget incompatible | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch61) | Matching |
| Notaire | Professionnel juridique vers lequel LAWIM oriente pour les questions de droit immobilier | Directive/03-CONVERSATION-REFERENCE.md | Conversation |
| Objection | Réticence exprimée par un utilisateur (10 peurs acheteur, 8 peurs vendeur documentées) | trust-and-objection-patterns.md | Negotiation |
| Omnicanal | Stratégie multi-canal (WhatsApp principal, Telegram, Facebook, Dashboard) | Directive/00-CONSTITUTION.md | Conversation |
| Opt-in | Permission demandée avant de partager le contact d'un agent. 4 étapes : détection → demande → log → partage | agent_optin.py | CRM |
| Partenaire externe | Notaire, architecte, géomètre, artisan, banque, assurance | 08-ROLE-REFERENCE.md | CRM |
| Permission | Droit d'accès associé à un rôle. Matrice 7×7 (7 rôles × 7 permissions) | implement_all.sql | CRM |
| Pidgin | Langue camerounaise supportée. Détection via 14 mots-clés | language_detector_ia.py | Language |
| Pipeline | Chaîne de traitement en 8 étapes : incoming → normalize → extract → detect_intent → context → scoring → classification → routing | RULE_ENGINE_V5.json | Qualification |
| Préférence apprise | Ajustement automatique du matching basé sur les refus/acceptations de l'utilisateur | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch19) | Matching |
| Prix ferme | Indication que le prix n'est pas négociable | negotiation.json | Negotiation |
| Propriétaire | Personne possédant un bien immobilier. État : PROPERTY_OWNER | USER_STATES.json | CRM |
| Propriété | Bien immobilier listé sur LAWIM. États : available, pending, rented, sold, archived | property_lifecycle_engine.py | Property |
| Qualification | Processus d'évaluation d'un lead (collecte d'informations, scoring, classification en 10 étapes) | RULE_ENGINE_V5.json | Qualification |
| Quartier | Subdivision d'une ville. Données disponibles pour 11+ villes camerounaises | neighborhoods/*.json | Geography |
| Région | Premier niveau administratif du Cameroun (10 régions) | geography/ | Geography |
| Relance | Message automatique à J1, J7, J30, J90 après un contact | follow_up_system.py | Conversation |
| Rematching | Ré-appariement après échec ou délai. Ne repart jamais de zéro, enrichit l'historique | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch64) | Matching |
| Résidentiel simple | Catégorie avec pondérations Type=20%, Op=10%, Ville/quartier=25%, Budget=25%, Douche/cuisine/meublé=10% | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch42) | Property |
| Response router | Hiérarchie de réponse : DeepSeek → Règles locales → Templates | response_router.py | Conversation |
| RGPD | Règlement Général sur la Protection des Données. Appliqué via SUPPRIMER MES DONNÉES | Directive/15-SECURITY-REFERENCE.md | Security |
| Rôle | Niveau d'accès : demandeur(1), vendeur(2), agent(3), agence(4), assistant(5), vice_master(6), master(7) | implement_all.sql | CRM |
| Rule engine | Moteur de règles définissant le pipeline (5 versions : V2 à V5) | RULE_ENGINE_V*.json | Qualification |
| Scoring | Calcul du score de qualité d'un lead (0-100 en V1, 0-1 en V5) | lead_classifier_v1.json | Qualification |
| Search | Intention de recherche non spécifique achat/location | intents/search_property.json | Qualification |
| Seller | Vendeur d'un bien immobilier. Score de base : 50 | lead_classifier_v1.json | Qualification |
| Signal | Indicateur dans un message (urgence, prix, diaspora, broker, investisseur) | intent_detector/ | Qualification |
| Signal d'opportunité | Événement déclencheur de rematching : baisse prix, nouveau bien, retour disponibilité | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch93) | Matching |
| Signal de risque | Alerte : propriétaire inactif, délais anormaux, documents incomplets, prix incohérent | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch94) | Matching |
| Source | Origine des données d'une propriété (agent, google_form, import, whatsapp) | data_quality_engine.py | Property |
| Spam | Message indésirable. Pénalité de -50 dans le scoring. Blocage à 10 msg/min | lead_classifier_v1.json | Security |
| Star rating | Notation par étoiles : ≥80=5/5, ≥60=4/5, ≥40=3/5, ≥20=2/5, <20=1/5 | property_matcher_v5.py | Matching |
| Subdivision | Division administrative entre arrondissement et commune (non implémentée dans les données) | district_hierarchy.json | Geography |
| Table CRM | Tables du système : persons, agents, properties, leads, disputes, agent_routing_history, agent_zones, agent_credits, boost_purchases, role_permissions, user_permissions, anonymization_requests, system_logs | implement_all.sql | CRM |
| Template | Message type prédéfini (welcome, help, no_match, thanks, ask_name, ask_phone, stats) | multilingual_responses.py | Language |
| Terrain agricole | Type avec pondérations Type=15%, Localité=15%, Prix=15%, Superficie=20%, Activité=8% | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch50) | Property |
| Terrain commercial | Type avec pondérations Type=15%, Zone/axe=18%, Prix=15%, Superficie=15%, Façade=8% | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch51) | Property |
| Terrain résidentiel | Type avec pondérations Type=15%, Op=8%, Ville/zone=18%, Prix/budget=17%, Superficie=15% | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch49) | Property |
| Titre foncier | Document officiel de propriété. Boost matching : +10. Score documentaire : 100% | property_matching_v1.json | Property |
| Transaction success score | Score composite : Compatibilité=30%, Géographie=15%, Disponibilité=10%, Documentaire=10%, Réactivité=10%, Historique=10%, Faisabilité=10%, Négociation=5% | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch90) | Matching |
| Trust index | Indice de confiance : Très élevé / Élevé / Moyen / Faible / Très faible | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch91) | Matching |
| Typo database | Base des fautes d'orthographe courantes (5 fichiers : cities, neighborhoods, property_types, whatsapp, general) | typo_database/*.json | Language |
| Urgence | Signal d'immédiateté dans une demande. Boost de scoring : +20 | lead_classifier_v1.json | Qualification |
| USER_FIELDS | 25 champs de profil utilisateur extraits par KnowledgeBuilder | knowledge_builder.py | Qualification |
| Variante orthographique | Façon alternative d'écrire un nom de lieu (bastos→basto, bastoss) | neighborhoods_typo.json | Language |
| Vendeur | Personne mettant en vente un bien. Rôle distinct du propriétaire. Niveau 2 | implement_all.sql | CRM |
| Vice-master | Super-administrateur adjoint (niveau 6). Peut gérer les permissions | implement_all.sql | CRM |
| Villa | Type résidentiel haut de gamme avec pondérations Type=12%, Op=8%, Ville/quartier=18%, Budget=17%, Chambres=15%, Cour/clôture=10% | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch46) | Property |
| Ville | Localité principale de recherche. 10 villes prioritaires : Douala, Yaoundé, Bafoussam, Bamenda, Buea, Limbe, Kribi, Nkongsamba, Garoua, Maroua | system_prompt_v1.md | Geography |
| Warm | Classe de lead moyenne priorité (score ≥ 60 en V1, ≥ 0.5 en V5). Action : envoyer annonces | lead_classifier_v1.json | Qualification |
| WhatsApp | Canal de communication principal via API GreenAPI | Directive/03-CONVERSATION-REFERENCE.md | Conversation |
| Zéro commission | Principe fondamental — aucun frais sur les transactions immobilières | Directive/00-CONSTITUTION.md | Constitution |
| Zone | Regroupement géographique pour le routage des leads vers les agents | agent_zones (SQL) | Geography |
| Zone LAWIM | Périmètre d'activité prioritaire défini par l'équipe | Directive/00-CONSTITUTION.md | Geography |
| Matching V1 | Système simple 5 dimensions : city=30%, neighborhood=25%, budget=25%, property_type=15%, title_status=5% | property_matching_v1.json | Matching |
| Matching V4 | Matching Supabase : filtre status='available', correspondance ville + budget | property_matcher_supabase.py | Matching |
| Matching V5 | Scoring par points : location=+40, budget exact=+50, ±10%=+35, ±30%=+20, ±50%=+10, type=+10 | property_matcher_v5.py | Matching |
| Decision Engine V1 | Moteur décisionnel complet avec 6 parties : matching, scoring, compatibilité, transaction, apprentissage, éthique | Directive/04-DECISION-ENGINE-REFERENCE.md | Matching |
| Pipeline V5 | 8 étapes : incoming_message → normalize_text → extract_entities → detect_intent → context_enrichment → lead_scoring → lead_classification → crm_routing | RULE_ENGINE_V5.json | Qualification |
| CRM scoring V5 | 7 facteurs pondérés : base_interest=0.15, property_type_match=0.20, location_precision=0.20, budget_presence=0.10, urgency_signal=0.15, visit_intent=0.20, trust_signal=0.10 | RULE_ENGINE_V5.json | CRM |
| Anti-fraud 4 layers | Couches : broker_spam_detection, duplicate_listing_detection, fake_price_detection, suspicious_urgency_detection | RULE_ENGINE_V5.json | Security |
| Behavior tracking | Traçage : message_history, response_time, budget_changes, visit_requests | RULE_ENGINE_V5.json | CRM |
| Agent routing | Routage des leads vers agents par zone géographique | agent_routing_history (SQL) | CRM |
| P0/P1/P2/P3 priority | Priorités de lead : P0=urgent(100-95), P1=high(90-85), P2=medium(75-60), P3=low(40) | lead_scoring.json | Qualification |
| Lead scoring rules weights | Poids des critères : budget=20, location=15, urgency=20, diaspora=10, phone=5, property_type=15, investment_profile=10 | lead_scoring_rules.json | Qualification |
| Recommended actions | Actions CRM : call_immediately, send_listings, request_budget, follow_up, ignore | RULE_ENGINE_V5.json | CRM |
| Reasoning priority | Ordre de raisonnement : intent → location → budget → property_type | reasoning_rules_v1.json | Matching |
| Reasoning steps | 7 étapes : detect_intent → detect_city → detect_neighborhood → detect_budget → classify_lead → match_properties → rank_results | reasoning_rules_v1.json | Matching |
| Confidence threshold | Seuil de confiance global pour le raisonnement : 0.70 | reasoning_rules_v1.json | Matching |
| Property lifecycle | Cycle de vie : available → pending → rented/sold/archived | property_lifecycle_engine.py | Property |
| Boutique/kiosque | Type commercial : Type=15%, Ville/quartier/marché=25%, Budget=20%, Surface=10%, Position=12% | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch52) | Property |
| Entrepôt/hangar | Type logistique : Type=15%, Zone=15%, Budget=15%, Surface=20%, Accès camion=12% | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch54) | Property |
| Bien industriel/logistique | Type : Type=15%, Zone indus=15%, Prix=15%, Surface=18%, Accès poids lourds=12% | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch57) | Property |
| Duplex | Type : Type=15%, Op=8%, Ville/quartier=18%, Budget=17%, Chambres=12%, Deux niveaux=12% | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch47) | Property |
| Diaspora filter | Module détectant la diaspora via indicateurs textuels et indicatifs téléphoniques | diaspora_filter.py | Qualification |
| Diaspora services | Table SQL des services dédiés diaspora : client_phone, service_type, price, status | implement_all.sql | CRM |
| Phone formatting | Normalisation téléphone : format Cameroun 237 + 9 chiffres, lien WhatsApp wa.me | phone_formatter.py | Language |
| Language detector | Détection hiérarchique des langues : DeepSeek → Gemini (commenté) → Règles locales | language_detector_ia.py | Language |
| Missing knowledge | Connaissances perdues par suppression des sources : 27 fichiers engine, 6 configs, 6 IA, 20+ DB, 2 SQL scripts | KNOWLEDGE_GAPS.md | Knowledge |
| Quality report | Rapport qualité de consolidation knowledge_unified : HIGH pour Géographie, Qualification, Matching, Langage, Commercial | quality_report.md | Knowledge |
| CAMEROON geography | 10 régions, 58 départements, 360 arrondissements, données GPS pour quartiers | geography/ | Geography |
| Master dashboard | Dashboard administrateur avec accès password protégé : "lawim2026" | master_dashboard.py | CRM |
| Multi-lingual responses | 7 templates en 3 langues (FR/EN/PID) : welcome, help, no_match, thanks, ask_name, ask_phone, stats | multilingual_responses.py | Language |
| Follow-up schedule | Calendrier relance : J1=24h, J7=168h, J30=720h, J90=2160h | follow_up_system.py | Conversation |
| GreenAPI endpoint | URL API : https://api.green-api.com/waInstance{ID}/sendMessage/{TOKEN} | follow_up_system.py | Conversation |
| Conversation summary | Format résumé : "Vous cherchiez [type] à [lieu] avec un budget de [montant] FCFA" | conversation_memory.py | Conversation |
| Lead fields | 10 champs lead : message, intent, budget, location, property_type, urgency, score, status, priority, diaspora_flag | knowledge_builder.py | Qualification |
| DeepSeek extraction | Extraction par IA : type, localisation, budget. Format sortie JSON | deepseek_prompt.txt | AI |
| I18N reference | 5 documents i18n : 30-I18N-L10N-REFERENCE.md, 30A-BUSINESS-DICTIONARY.md, 30B-TRANSLATION.md, 30C-LANGUAGE-DETECTION.md, 30D-MULTILINGUAL-SEARCH.md | Directive/30*.md | Language |
| WhatsApp language corpus | 7 fichiers corpus : whatsapp_language.json, diaspora_language.json, investor_language.json, negotiation.json, property_listing.json, property_search.json, urgency_signals.json | whatsapp_language/*.json | Language |
| 4 profiles acheteurs | Profils documentés dans le playbook : national (implicite), diaspora, investisseur, jeune actif (non trouvé) | Directive/48-LAWIM-SALES-PLAYBOOK.md | Negotiation |
| 3 profiles vendeurs | Profils : particulier, promoteur, bailleur (non trouvé comme profil distinct) | Directive/48-LAWIM-SALES-PLAYBOOK.md | Negotiation |
| 6 arguments LAWIM | Arguments commerciaux : zéro commission, mise en relation directe, matching intelligent (absent du playbook), accompagnement, WhatsApp, réseau agents vérifiés | Directive/48-LAWIM-SALES-PLAYBOOK.md | Negotiation |
| Sequence confiance | 5 étapes idéales : écoute active, apport d'information, proposition, traitement objections, closing | conversation-style-guide.md | Negotiation |
| Sales playbook | Document commercial complet : profils, objections, arguments, scripts WhatsApp, closing | Directive/48-LAWIM-SALES-PLAYBOOK.md | Negotiation |
| Student housing | Type de bien pour étudiants. Sous-catégorie résidentielle | Directive/02A-RESIDENTIAL-REFERENCE.md | Property |
| Colocation | Type de bien en location partagée | Directive/02A-RESIDENTIAL-REFERENCE.md | Property |
| Résidence meublée | Type de bien meublé pour location courte durée | Directive/02A-RESIDENTIAL-REFERENCE.md | Property |
| Résidence étudiante | Logement étudiant. Catégorie résidentielle spécifique | Directive/02A-RESIDENTIAL-REFERENCE.md | Property |
| Résidence médicalisée | Logement pour personnes âgées ou médicalisé | Directive/02A-RESIDENTIAL-REFERENCE.md | Property |
| Résidence hôtelière | Mixte résidentiel/hôtellerie (appart'hôtel) | Directive/02F-HOTEL-REFERENCE.md | Property |
| Centre commercial | Grand espace commercial avec plusieurs boutiques | Directive/02B-COMMERCIAL-REFERENCE.md | Property |
| Local commercial | Espace commercial individuel (boutique, magasin) | Directive/02B-COMMERCIAL-REFERENCE.md | Property |
| Entrepôt | Espace de stockage logistique | Directive/02C-INDUSTRIAL-REFERENCE.md | Property |
| Terrain constructible | Terrain avec permis de construire ou constructible | Directive/02D-LAND-REFERENCE.md | Property |
| Terrain non constructible | Terrain sans possibilité de construction | Directive/02D-LAND-REFERENCE.md | Property |
| Ferme | Propriété agricole avec bâtiments d'exploitation | Directive/02E-AGRICULTURAL-REFERENCE.md | Property |
| Plantation | Exploitation agricole (cacao, café, palmier, hévéa) | Directive/02E-AGRICULTURAL-REFERENCE.md | Property |
| Hôtel | Établissement hôtelier avec chambres et services | Directive/02F-HOTEL-REFERENCE.md | Property |
| Auberge | Petit établissement d'hébergement | Directive/02F-HOTEL-REFERENCE.md | Property |
| Lodge | Hébergement touristique en zone naturelle | Directive/02F-HOTEL-REFERENCE.md | Property |
| Projet immobilier | Programme de construction neuve ou de promotion | Directive/02G-PROJECT-REFERENCE.md | Property |
| VEFA | Vente en l'État Futur d'Achèvement (sur plan) | Directive/02G-PROJECT-REFERENCE.md | Property |
| Maroua | Ville prioritaire LAWIM (Extrême-Nord) | system_prompt_v1.md | Geography |
| Garoua | Ville prioritaire LAWIM (Nord) | system_prompt_v1.md | Geography |
| Nkongsamba | Ville prioritaire LAWIM (Littoral) | system_prompt_v1.md | Geography |
| Kribi | Ville prioritaire LAWIM (Sud) | system_prompt_v1.md | Geography |
| Limbe | Ville prioritaire LAWIM (Sud-Ouest) | system_prompt_v1.md | Geography |
| Buea | Ville prioritaire LAWIM (Sud-Ouest) | system_prompt_v1.md | Geography |
| Bamenda | Ville prioritaire LAWIM (Nord-Ouest) | system_prompt_v1.md | Geography |
| Bafoussam | Ville prioritaire LAWIM (Ouest) | system_prompt_v1.md | Geography |
| Yaoundé | Ville prioritaire LAWIM (Centre), capitale politique | system_prompt_v1.md | Geography |
| Douala | Ville prioritaire LAWIM (Littoral), capitale économique | system_prompt_v1.md | Geography |
| Akwa | Quartier de Douala, centre d'affaires | neighborhoods/douala.json | Geography |
| Bonapriso | Quartier résidentiel haut standing de Douala | neighborhoods/douala.json | Geography |
| Bonamoussadi | Quartier résidentiel de Douala | neighborhoods/douala.json | Geography |
| Makepe | Quartier résidentiel de Douala | neighborhoods/douala.json | Geography |
| Deido | Quartier de Douala | neighborhoods/douala.json | Geography |
| Bastos | Quartier résidentiel haut standing de Yaoundé | neighborhoods/yaounde.json | Geography |
| Essos | Quartier résidentiel de Yaoundé | neighborhoods/yaounde.json | Geography |
| Biyem Assi | Quartier résidentiel de Yaoundé | neighborhoods/yaounde.json | Geography |
| Mvog Mbi | Quartier de Yaoundé | neighborhoods/yaounde.json | Geography |
| Odza | Quartier résidentiel de Yaoundé | neighborhoods/yaounde.json | Geography |
| Nkoabang | Quartier périphérique de Yaoundé | neighborhoods/yaounde.json | Geography |
| 25 fraude signals | Signaux de fraude documentés dans le modèle comportemental (25 détails) | fraud-signals-and-verification.md | Security |
| City affinity matrix | Matrice d'affinité entre villes avec interdictions (Soa→Obala interdit, etc.) | city-affinity-matrix.md | Geography |
| Diaspora behavior model | Modèle comportemental des investisseurs diaspora | diaspora-behavior-model.md | Qualification |
| Market research | Étude de marché immobilier camerounais complète | Analyse __- marché immobilier camerounais_- groupe.md | Knowledge |
| LAWIM brand book | Guide de marque LAWIM complet | Directive/LAWIM-BRAND-BOOK.md | Constitution |
| LAWIM business plan | Plan d'affaires LAWIM complet | Directive/LAWIM-BUSINESS-PLAN.md | Constitution |
| LAWIM operations manual | Manuel d'opérations LAWIM | Directive/LAWIM-OPERATIONS-MANUAL.md | Constitution |
| Strategic launch plan | Plan stratégique de lancement LAWIM | Directive/Plan_strategique_lancement.md | Constitution |
| AI system prompt | Prompt système IA DeepSeek (73 lignes) | system_prompt_v1.md | AI |
| Conversation flow | Flot conversationnel en JSON pour le moteur IA | conversation_flows_v1.json | AI |
| Memory rules | Règles de mémoire pour le raisonnement IA | memory_rules_v1.json | AI |
| Reasoning rules | Règles de raisonnement : priorité, étapes, seuil confiance | reasoning_rules_v1.json | AI |
| Classification prompt | Prompt IA pour classification des messages | prompts/classification.py | AI |
| SOURCE_INVENTORY | Inventaire de ~220 fichiers legacy | knowledge_unified/sources/SOURCE_INVENTORY.md | Knowledge |
| TRACEABILITY_MATRIX | Matrice traçant 73 entrées legacy vers 50 fichiers consolidés | knowledge_unified/sources/TRACEABILITY_MATRIX.md | Knowledge |
| QUALITY_REPORT | Rapport qualité de consolidation par domaine | knowledge_unified/validation/quality_report.md | Knowledge |
| Ancienne structure | Branche legacy, sous-ensemble de LAWIMA (~300 fichiers présumés, 0 vérifiables) | LAWIM_BACKUP/ancienne_structure/ | Knowledge |
| Category 7 families | 7 familles de biens : Résidentiel, Commercial, Industriel, Terrain, Agricole, Hôtellerie, Projet | Directive/02-PROPERTY-REFERENCE.md | Property |
| Minimum property fields | Champs obligatoires annonce : Transaction, Type de bien, Ville, Prix, Description | minimum-fields-property.md | Property |
| LAWIM V2 | Version actuelle de LAWIM en développement | LAWIM_V2 | Knowledge |
| knowledge_unified | 50 fichiers consolidés à partir des sources legacy | knowledge_unified/ | Knowledge |

---

| Next Best Action (NBA) | Prochaine action optimale calculée automatiquement pour chaque objet métier. Réévaluée après chaque événement. 12 actions officielles. | 05-WORKFLOW-REFERENCE.md (Ch11, Ch69, Ch160, Ch201) | Workflow |
| Progressive Search Expansion | Élargissement progressif de la recherche quand aucun bien compatible n'est trouvé : normale → élargie → intelligente → continue → notification → relance. Ne clôture jamais le dossier. | 05-WORKFLOW-REFERENCE.md (Ch23-26) | Workflow |
| Continuous Market Surveillance | Surveillance silencieuse et permanente de tous les objets métier et événements marché. Déclenche automatiquement les actions prévues. | 05-WORKFLOW-REFERENCE.md (Ch79, Ch27) | Workflow |
| Health Score | Score de santé d'un objet métier. 5 types : Dossier, Propriété, Data Quality, Trust Score, Holder Reliability. Chaque objet possède un Health Score calculé. | 05-WORKFLOW-REFERENCE.md (Ch88), 04-DECISION-ENGINE-REFERENCE.md (Ch90-91) | Workflow |
| Indice de Confiance | Niveau de confiance attribué à chaque proposition : Très élevé / Élevé / Moyen / Faible / Très faible. Basé sur GPS confirmé, documents vérifiés, disponibilité récente, propriétaire actif. | 04-DECISION-ENGINE-REFERENCE.md (Ch91) | Matching |
| Indice de Tension du Marché | Mesure de tension par combinaison Ville+Quartier+Type+Opération. 95% = très tendu, 25% = détendu. Aide à adapter les recommandations. | 04-DECISION-ENGINE-REFERENCE.md (Ch96) | Matching |
| Apprentissage Global | Connaissance du marché construite progressivement : délai moyen de vente par ville, quartiers demandés, saisonnalité. N'affecte jamais les critères individuels des dossiers. | 04-DECISION-ENGINE-REFERENCE.md (Ch73, Ch95) | Matching |
| Transaction Success Score | Score composite (0-100%) représentant la probabilité de transaction réussie. 8 indicateurs pondérés : Compatibilité(30%), Géographie(15%), Disponibilité(10%), Documentaire(10%), Réactivité(10%), Historique(10%), Faisabilité(10%), Négociation(5%). | 04-DECISION-ENGINE-REFERENCE.md (Ch90) | Matching |
| SLA Métier | Délais maximums par type de bien pour matching, rematching et relance. Configurable. Ex: Appartement → matching immédiat, rematching 72h, relance 5 jours. | 05-WORKFLOW-REFERENCE.md (Ch22) | Workflow |
| Workflow actif | Workflow qui ne se contente pas d'attendre des événements. Surveille en permanence délais, opportunités, risques et changements du marché. Chaque objet a une NBA. | 05-WORKFLOW-REFERENCE.md (Ch10, Ch20) | Workflow |
| Non-compensation | Règle fondamentale : certains critères ne peuvent jamais compenser une incompatibilité majeure. Ex: Un terrain bien situé ne compense pas une recherche de villa. | 04-DECISION-ENGINE-REFERENCE.md (Ch61) | Matching |
| Décision Engine | Moteur décisionnel en 6 parties et 100 chapitres. Couvre matching, scoring, compatibilité, transaction, apprentissage et éthique. 12 actions officielles, matrice de décision. | 04-DECISION-ENGINE-REFERENCE.md | Matching |
| Star Rating | Notation par étoiles : ≥80=5/5, ≥60=4/5, ≥40=3/5, ≥20=2/5, <20=1/5 | property_matcher_v5.py | Matching |
| Pidgin | Langue camerounaise supportée partiellement. 14 mots-clés dans détecteur IA, 12 dans détecteur local. 8 templates partiels. | language_detector_ia.py, language_detector.py | Language |
| 10 buyer fears | Peurs acheteurs documentées : arnaque, titre foncier, prix excessif, vices cachés, litige, administratif, localisation, voisinage, accessibilité, financement. | trust-and-objection-patterns.md | Negotiation |
| 8 seller fears | Peurs vendeurs documentées : pas d'acheteur, prix trop bas, acheteur non solvable, arnaque, délais, occupants illégaux, litiges, biens saisis. | trust-and-objection-patterns.md | Negotiation |
| 4 buyer profiles | Profils acheteurs : national, diaspora, investisseur, jeune actif. | 48-LAWIM-SALES-PLAYBOOK.md | Negotiation |
| 3 seller profiles | Profils vendeurs : particulier, promoteur, bailleur. | 48-LAWIM-SALES-PLAYBOOK.md | Negotiation |
| Séquence confiance | 5 étapes : écoute active → information → proposition → objections → closing. | closing_techniques.md, conversation_tone.md | Negotiation |
| 8-step commercial process | Prospection → Qualification → Présentation → Proposition → Suivi → Conclusion → Activation → Fidélisation. | 48-LAWIM-SALES-PLAYBOOK.md | CRM |
| CRM Scoring V5 | 7 facteurs pondérés : base_interest(0.15), property_type_match(0.20), location_precision(0.20), budget_presence(0.10), urgency_signal(0.15), visit_intent(0.20), trust_signal(0.10). | RULE_ENGINE_V5.json | CRM |
| Identity resolution | Détection et fusion des personnes en double. Scores : téléphone=100, email=95, nom+téléphone≥40, nom+email≥40, nom seul≥20. | identity_resolution.py | CRM |
| 10 qualification steps | Intention → Type bien → Ville → Quartier → Budget → Délai → Critères → Préférences → Confirmation → Escalade. | RULE_ENGINE_V5.json | Qualification |
| Pipeline V5 | 8 étapes : incoming → normalize → extract → detect_intent → context → scoring → classification → routing. | RULE_ENGINE_V5.json | Qualification |
| Geo Score V4 | Formule : Affinité(40%) + Cluster(25%) + Produit(20%) + GPS(15%). | GEO_REFERENCE_MODEL_CAMEROON_V4.md | Geography |
| Mobility modes | STRICT (quartier demandé seul), FLEXIBLE (alternatives acceptées), VERY_FLEXIBLE (zone élargie). | geographic_scoring.md | Geography |
| 35 absolute geo rules | Règles absolues de géographie : ne jamais supprimer de ville active, ne jamais modifier des coordonnées sans historisation, double consentement pour position temps réel, etc. | 09-GEOLOCATION-REFERENCE.md | Geography |
| 4 anti-fraud layers | Couches anti-fraude : broker_spam_detection, duplicate_listing_detection, fake_price_detection, suspicious_urgency_detection. | RULE_ENGINE_V5.json | Security |
| 25 fraud signals | Signaux de fraude documentés dans le modèle comportemental. | fraud-signals-and-verification.md | Security |

*Document Gold — Terminologie exhaustive validée pour toute reconstruction LAWIM. Mise à jour H0.4 — Heritage Completion.*
