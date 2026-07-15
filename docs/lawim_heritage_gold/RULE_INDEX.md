# RULE INDEX — Index des Règles Métier (Gold Standard)

**Mission :** LAWIM Heritage Gold
**Date :** 15 juillet 2026
**Statut :** Index exhaustif de toutes les règles métier

---

## Constitution

| Rule ID | Domain | Rule Description | Source | Confidence |
|---------|--------|------------------|--------|------------|
| CONST-001 | Constitution | Zéro commission sur les transactions immobilières | Directive/00-CONSTITUTION.md (Art.1) | VALIDATED |
| CONST-002 | Constitution | LAWIM finance son activité par les services et mise en relation payante | Directive/00-CONSTITUTION.md (Art.1) | VALIDATED |
| CONST-003 | Constitution | Protection des données personnelles (RGPD) | Directive/00-CONSTITUTION.md (Art.2) | VALIDATED |
| CONST-004 | Constitution | WhatsApp comme canal principal | Directive/00-CONSTITUTION.md (Art.9) | VALIDATED |
| CONST-005 | Constitution | Stratégie multi-canal (WhatsApp, Telegram, Facebook, Dashboard) | Directive/00-CONSTITUTION.md (Art.10) | VALIDATED |
| CONST-006 | Constitution | Matching comme cœur du moteur | Directive/00-CONSTITUTION.md (Art.14) | VALIDATED |
| CONST-007 | Constitution | Qualification comme fondation de l'expérience | Directive/00-CONSTITUTION.md (Art.15) | VALIDATED |
| CONST-008 | Constitution | Agents et clients au centre du modèle | Directive/00-CONSTITUTION.md (Art.20) | VALIDATED |
| CONST-009 | Constitution | Architecture offline-first | Directive/00-CONSTITUTION.md (Art.22) | VALIDATED |
| CONST-010 | Constitution | DeepSeek comme moteur IA principal (Article 18) | Directive/00-CONSTITUTION.md (Art.18) | VALIDATED |

## Property

| Rule ID | Domain | Rule Description | Source | Confidence |
|---------|--------|------------------|--------|------------|
| PROP-001 | Property | 7 familles de biens : Résidentiel, Commercial, Industriel, Terrain, Agricole, Hôtellerie, Projet | Directive/02-PROPERTY-REFERENCE.md | VALIDATED |
| PROP-002 | Property | Champs obligatoires annonce : Transaction, Type de bien, Ville, Prix, Description | minimum-fields-property.md | VALIDATED |
| PROP-003 | Property | Cycle de vie : 5 états (available, pending, rented, sold, archived) | property_lifecycle_engine.py | VALIDATED |
| PROP-004 | Property | Transitions : available→pending/archived, pending→rented/sold/available/archived, rented/sold→archived, archived→available | property_lifecycle_engine.py | VALIDATED |
| PROP-005 | Property | Auto-archivage après 90 jours d'inactivité | property_lifecycle_engine.py | VALIDATED |
| PROP-006 | Property | Data Quality Score = complétude*0.6 + fiabilité*0.4 | data_quality_engine.py | VALIDATED |
| PROP-007 | Property | Poids complétude : titre=10%, description=15%, prix=15%, localisation=15%, type=15%, images=15% (max 3pts/image) | data_quality_engine.py | VALIDATED |
| PROP-008 | Property | Fiabilité source : agent=90, google_form=85, import=70, whatsapp=50, unknown=30 | data_quality_engine.py | VALIDATED |
| PROP-009 | Property | Grades qualité : A+≥80, A≥60, B≥40, C≥20, D<20 | data_quality_engine.py | VALIDATED |
| PROP-010 | Property | Prix scoring : budget≥500k→+30, ≥100M→+50 | lead_scorer_supabase.py | PARTIAL |
| PROP-011 | Property | Formats prix : k_format, mille_format dans gateway_fixed.py | gateway_fixed.py | PARTIAL |

## Matching

| Rule ID | Domain | Rule Description | Source | Confidence |
|---------|--------|------------------|--------|------------|
| MATCH-001 | Matching | Dimensions V1 : city=30%, neighborhood=25%, budget=25%, property_type=15%, title_status=5% | property_matching_v1.json | VALIDATED |
| MATCH-002 | Matching | Dimensions DE : Type=25%, Opération=20%, Budget=15%, Localisation=15%, Critiques=15%, Recommandées=10% | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch26) | VALIDATED |
| MATCH-003 | Matching | Tolérances budgétaires : rent=20%, buy=15%, invest=25% | property_matching_v1.json | VALIDATED |
| MATCH-004 | Matching | Boost exact_neighborhood_match=+25 | property_matching_v1.json | VALIDATED |
| MATCH-005 | Matching | Boost exact_city_match=+20 | property_matching_v1.json | VALIDATED |
| MATCH-006 | Matching | Boost budget_within_range=+15 | property_matching_v1.json | VALIDATED |
| MATCH-007 | Matching | Boost title_foncier=+10 | property_matching_v1.json | VALIDATED |
| MATCH-008 | Matching | Boost diaspora_investor=+20 | property_matching_v1.json | VALIDATED |
| MATCH-009 | Matching | Seuil minimum match = 60/100 | property_matching_v1.json | VALIDATED |
| MATCH-010 | Matching | Max résultats = 10 (V1), max 5 au premier matching (DE) | property_matching_v1.json, Directive/04-DECISION-ENGINE-REFERENCE.md (Ch34) | VALIDATED |
| MATCH-011 | Matching | Score <60% = jamais proposé | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch26) | VALIDATED |
| MATCH-012 | Matching | 4 niveaux compatibilité : Critique, Fonctionnelle, Confort, Préférentielle | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch9) | VALIDATED |
| MATCH-013 | Matching | Principe de non-compensation (terrain ne compense pas villa) | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch61) | VALIDATED |
| MATCH-014 | Matching | Apprentissage des refus : 3 refus → priorisation | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch19) | VALIDATED |
| MATCH-015 | Matching | Rematching : ne repart jamais de zéro | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch64) | VALIDATED |
| MATCH-016 | Matching | Rematching : seulement dossiers concernés | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch66) | VALIDATED |
| MATCH-017 | Matching | Bien refusé définitivement → jamais reproposé (sauf exceptions) | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch71) | VALIDATED |
| MATCH-018 | Matching | Exceptions reproposition : baisse prix, modif majeure, changement besoin, demande explicite | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch71) | VALIDATED |
| MATCH-019 | Matching | Star rating : ≥80=5/5, ≥60=4/5, ≥40=3/5, ≥20=2/5, <20=1/5 | property_matcher_v5.py | VALIDATED |
| MATCH-020 | Matching | V5 scoring : location=+40, budget exact=+50, ±10%=+35, ±30%=+20, ±50%=+10, type=+10 | property_matcher_v5.py | VALIDATED |
| MATCH-021 | Matching | V4 : filtre status='available', correspondance ville+budget | property_matcher_supabase.py | VALIDATED |
| MATCH-022 | Matching | Exclusions : archivé, budget hors tolérance, ville différente, déjà envoyé | MATCHING_ENGINE_V1_SUMMARY.md | VALIDATED |
| MATCH-023 | Matching | Exclusion : opération incompatible, type incompatible, bien indisponible | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch25) | VALIDATED |
| MATCH-024 | Matching | Transaction Success Score : 8 indicateurs (Compatibilité=30%, Géographie=15%, etc.) | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch90) | VALIDATED |
| MATCH-025 | Matching | Score disponibilité : 100%=Disponible, 70%=Réservation, 30%=Attente, 0%=Vendu/Loué/Archivé | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch28) | VALIDATED |
| MATCH-026 | Matching | Score documentaire : Titre foncier=100%, En cours=80%, Droit coutumier=60%, Inconnu=40% | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch29) | VALIDATED |
| MATCH-027 | Matching | Holder score = temps réponse × taux acceptation × visites honorées × transactions conclues | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch31) | VALIDATED |
| MATCH-028 | Matching | Budget flexible : bien légèrement supérieur possible si autres critères excellents | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch13) | VALIDATED |
| MATCH-029 | Matching | Raisonnement : priorité intent→location→budget→property_type | reasoning_rules_v1.json | VALIDATED |
| MATCH-030 | Matching | 7 étapes raisonnement : detect_intent→detect_city→...→rank_results | reasoning_rules_v1.json | VALIDATED |
| MATCH-031 | Matching | Seuil confiance raisonnement = 0.70 | reasoning_rules_v1.json | VALIDATED |
| MATCH-032 | Matching | Diversité : éviter biens identiques (3 apparts même immeuble → 1 présenté) | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch77) | VALIDATED |
| MATCH-033 | Matching | Explainability : top 3 critères expliqués pour chaque proposition | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch60) | VALIDATED |
| MATCH-034 | Matching | Règles absolues : jamais bien incompatible, jamais bien vendu, jamais deux fois après refus | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch38) | VALIDATED |

## Geography

| Rule ID | Domain | Rule Description | Source | Confidence |
|---------|--------|------------------|--------|------------|
| GEO-001 | Geography | Hiérarchie : Pays→Région→Département→Arrondissement→Commune→Ville→District→Quartier | district_hierarchy.json | PARTIAL |
| GEO-002 | Geography | 10 villes prioritaires : Douala, Yaoundé, Bafoussam, Bamenda, Buea, Limbe, Kribi, Nkongsamba, Garoua, Maroua | system_prompt_v1.md | VALIDATED |
| GEO-003 | Geography | Quartiers disponibles pour 11+ villes | neighborhoods/*.json | VALIDATED |
| GEO-004 | Geography | Normalisation Levenshtein seuil max = 3 | location_normalizer.py | VALIDATED |
| GEO-005 | Geography | Extraction localisation via patterns : r'à\s+([A-Za-z]+)', r'dans\s+([A-Za-z]+)', r'quartier\s+([A-Za-z]+)' | knowledge_enricher.py | VALIDATED |
| GEO-006 | Geography | Confiance extraction : min(100, count*20) | knowledge_enricher.py | VALIDATED |
| GEO-007 | Geography | GPS disponibles pour quartiers (3 fichiers) | geography/neighborhood_gps.json, gemini_recovered_gps.json, neighborhood_inventory_final.json | VALIDATED |
| GEO-008 | Geography | City affinity : Ville exacte→Quartier exact→Affinité forte→Validation→WAITLISTED | city-affinity-matrix.md | VALIDATED |
| GEO-009 | Geography | Interdictions géographiques : Soa→Obala, Soa→Bafia, Yaoundé→Soa, Douala→Dibombari | city-affinity-matrix.md | VALIDATED |
| GEO-010 | Geography | Distance réelle (GPS) pas à vol d'oiseau | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch15) | VALIDATED |
| GEO-011 | Geography | Score géographique : ville+quartier+GPS+distance réele+temps trajet | Directive/04-DECISION-ENGINE-REFERENCE.md (Ch27) | VALIDATED |

## Qualification

| Rule ID | Domain | Rule Description | Source | Confidence |
|---------|--------|------------------|--------|------------|
| QUAL-001 | Qualification | Scores base : tenant=40, buyer=60, seller=50, investor=80, diaspora_investor=95 | lead_classifier_v1.json | VALIDATED |
| QUAL-002 | Qualification | Boosters : budget_detected=+15, city_detected=+10, neighborhood_detected=+10, urgent_request=+20, diaspora_detected=+25, cash_purchase=+15 | lead_classifier_v1.json | VALIDATED |
| QUAL-003 | Qualification | Pénalités : missing_budget=-10, unclear_location=-10, spam_like_message=-50 | lead_classifier_v1.json | VALIDATED |
| QUAL-004 | Qualification | Seuils V1 : HOT≥80, WARM≥60, COLD≥40, LOW<40 | lead_classifier_v1.json | VALIDATED |
| QUAL-005 | Qualification | Seuils V5 : HOT≥0.8, WARM≥0.5, COLD≥0.3, SPAM≤0.2 | RULE_ENGINE_V5.json | VALIDATED |
| QUAL-006 | Qualification | Pipeline 8 étapes V5 : incoming→normalize→extract→detect_intent→context→scoring→classification→routing | RULE_ENGINE_V5.json | VALIDATED |
| QUAL-007 | Qualification | 10 étapes qualification : Intention→Type bien→Ville→Quartier→Budget→Délai→Critères→Préférences→Confirmation→Escalade | RULE_ENGINE_V5.json | VALIDATED |
| QUAL-008 | Qualification | Mapping intents→rôles : RENT→tenant, BUY→buyer, SELL→seller, INVESTOR→investor/diaspora_investor | lead_classifier_v1.json | VALIDATED |
| QUAL-009 | Qualification | Actions : call_immediately, send_listings, request_budget, follow_up, ignore | RULE_ENGINE_V5.json | VALIDATED |
| QUAL-010 | Qualification | 25 USER_FIELDS extraits par KnowledgeBuilder | knowledge_builder.py | PARTIAL |
| QUAL-011 | Qualification | 10 LEAD_FIELDS : message, intent, budget, location, property_type, urgency, score, status, priority, diaspora_flag | knowledge_builder.py | PARTIAL |
| QUAL-012 | Qualification | 4 comportements traqués : message_history, response_time, budget_changes, visit_requests | RULE_ENGINE_V5.json | VALIDATED |
| QUAL-013 | Qualification | Ordre qualification strict : 1 message par question (WhatsApp), 2-3 champs (Telegram) | Directive/03-CONVERSATION-REFERENCE.md | VALIDATED |
| QUAL-014 | Qualification | Pas de redemande, pas de redémarrage, correction écrase contexte | Directive/03-CONVERSATION-REFERENCE.md | VALIDATED |
| QUAL-015 | Qualification | Critères arrêt : ville non couverte, inventaire vide, demande humain, thread répétitif (3 échanges) | Directive/03-CONVERSATION-REFERENCE.md | VALIDATED |
| QUAL-016 | Qualification | Indicateurs diaspora : 13 localisations + 4 indicatifs téléphoniques | diaspora_filter.py | VALIDATED |
| QUAL-017 | Qualification | Lead scoring rules : budget=20, location=15, urgency=20, diaspora=10, phone=5, property_type=15, investment_profile=10 | lead_scoring_rules.json | VALIDATED |
| QUAL-018 | Qualification | Priorités leads : P0(100-95), P1(90-85), P2(75-60), P3(40) | lead_scoring.json | VALIDATED |
| QUAL-019 | Qualification | Types additionnels : property_seeker, agent, owner, broker | RULE_ENGINE_V3.json | VALIDATED |

## Conversation

| Rule ID | Domain | Rule Description | Source | Confidence |
|---------|--------|------------------|--------|------------|
| CONV-001 | Conversation | Positionnement : intermédiaire, zéro commission, aucune garantie, accompagnement 50k | RESPONSE_POLICY.md | VALIDATED |
| CONV-002 | Conversation | Ton : professionnel, courtois, vendeur, vouvoiement systématique | RESPONSE_POLICY.md | VALIDATED |
| CONV-003 | Conversation | Langues supportées : français, anglais, pidgin (3 langues, pas 4) | RESPONSE_POLICY.md | PARTIAL |
| CONV-004 | Conversation | Question juridique → notaire | RESPONSE_POLICY.md | VALIDATED |
| CONV-005 | Conversation | DeepSeek extrait : type, localisation, budget | RESPONSE_POLICY.md | VALIDATED |
| CONV-006 | Conversation | Match trouvé → notifier agent/propriétaire | RESPONSE_POLICY.md | VALIDATED |
| CONV-007 | Conversation | Accompagnement payant 50k | RESPONSE_POLICY.md | VALIDATED |
| CONV-008 | Conversation | Litige → SIGNALER | RESPONSE_POLICY.md | VALIDATED |
| CONV-009 | Conversation | RGPD → SUPPRIMER MES DONNÉES (7 jours délai) | RESPONSE_POLICY.md | VALIDATED |
| CONV-010 | Conversation | 4 niveaux familiarité : J1(1j), J2(≤7j), J3(≤30j), J4(>30j) | conversation_memory.py | VALIDATED |
| CONV-011 | Conversation | Format résumé : "Vous cherchiez [type] à [lieu] avec [budget] FCFA" | conversation_memory.py | VALIDATED |
| CONV-012 | Conversation | Nouveaux biens simulés : random.randint(1,5) | conversation_memory.py | VALIDATED |
| CONV-013 | Conversation | Rétention long terme : 365 jours (pas 90 comme documenté) | long_term_memory.py (via SOURCE_INDEX SLE-003 : "12mois+"), CONVERSATION_VALIDATION.md | PARTIAL |
| CONV-014 | Conversation | Lead >12 mois relançable | long_term_memory.py | VALIDATED |
| CONV-015 | Conversation | Satisfaction précédente consultée (check_previous_property_satisfaction) | long_term_memory.py | VALIDATED |
| CONV-016 | Conversation | Relances : J1(24h), J7(168h), J30(720h), J90(2160h) | follow_up_system.py | VALIDATED |
| CONV-017 | Conversation | Hiérarchie réponse : DeepSeek → Règles locales → Templates | response_router.py | VALIDATED |
| CONV-018 | Conversation | Format JSON DeepSeek : extracted, missing, response_text, confidence, routing | deepseek_prompt.txt | PARTIAL |
| CONV-019 | Conversation | 7 templates multilingues (welcome, help, no_match, thanks, ask_name, ask_phone, stats) en FR/EN/PID | multilingual_responses.py | VALIDATED |
| CONV-020 | Conversation | Format affichage biens : "N. *description*\\n📍 localisation\\n💰 prix\\n⭐ notes" | multilingual_responses.py | VALIDATED |
| CONV-021 | Conversation | Feedback : 👍=5, 👎=1, note X | feedback_handler.py | VALIDATED |
| CONV-022 | Conversation | 10 peurs acheteurs (pas 12), 8 peurs vendeurs | trust-and-objection-patterns.md | PARTIAL |
| CONV-023 | Conversation | Signaux d'intention : 3/7 implémentés (sell, investor_lead, search) | intents/*.json | PARTIAL |

## Negotiation

| Rule ID | Domain | Rule Description | Source | Confidence |
|---------|--------|------------------|--------|------------|
| NEGO-001 | Negotiation | 4 profils acheteurs : national, diaspora, investisseur, jeune actif | Directive/48-LAWIM-SALES-PLAYBOOK.md | PARTIAL |
| NEGO-002 | Negotiation | 3 profils vendeurs : particulier, promoteur, bailleur | Directive/48-LAWIM-SALES-PLAYBOOK.md | PARTIAL |
| NEGO-003 | Negotiation | 12 peurs acheteurs documentées (10 réelles dans source) | trust-and-objection-patterns.md | PARTIAL |
| NEGO-004 | Negotiation | 8 peurs vendeurs documentées (confirmé via H0.4) | trust-and-objection-patterns.md + knowledge_unified/commercial/objection_handling.md | VALIDATED |
| NEGO-005 | Negotiation | 6 arguments LAWIM : zéro commission, mise en relation, matching intelligent, accompagnement, WhatsApp, réseau agents vérifiés | Directive/48-LAWIM-SALES-PLAYBOOK.md | PARTIAL |
| NEGO-006 | Negotiation | 5 arguments propriétés : proximité, accessibilité, sécurité, potentiel, cadre de vie | Directive/48-LAWIM-SALES-PLAYBOOK.md | NON_VALIDE |
| NEGO-007 | Negotiation | 4 moments clés : fin d'année, rentrée, saison sèche, transferts diaspora | negotiation-patterns.md | NON_VALIDE |
| NEGO-008 | Negotiation | Expressions négociation prix : prix ferme, à débattre, dernier prix (3/6 confirmés) | negotiation.json | PARTIAL |
| NEGO-009 | Negotiation | 5 principes ton : professionnel, expertise, patience, adaptation, validation | knowledge_unified/commercial/conversation_tone.md (version consolidée trouvée H0.4) | PARTIAL |
| NEGO-010 | Negotiation | Séquence confiance 5 étapes : écoute active, information, proposition, objections, closing | knowledge_unified/commercial/closing_techniques.md + conversation_tone.md (versions consolidées trouvées H0.4) | PARTIAL |
| NEGO-011 | Negotiation | Calendrier relance : J1, J7, J30, J90 | follow_up_system.py | VALIDATED |
| NEGO-012 | Negotiation | Signaux urgence : urgent, asap (mentionnés dans conversation-patterns.md) | conversation-patterns.md | PARTIAL |
| NEGO-013 | Negotiation | Signaux investisseur : investir, rentable, ROI (3/5 confirmés) | investor_intent.json | PARTIAL |
| NEGO-014 | Negotiation | Signaux diaspora : diaspora, je vis à, indicatifs étrangers (partiels) | investor_intent.json | PARTIAL |

## CRM

| Rule ID | Domain | Rule Description | Source | Confidence |
|---------|--------|------------------|--------|------------|
| CRM-001 | CRM | 7 rôles niveaux 1-7 : demandeur(1), vendeur(2), agent(3), agence(4), assistant(5), vice_master(6), master(7) | implement_all.sql, user_roles.json | VALIDATED |
| CRM-002 | CRM | Matrice permissions 7×7 documentée | implement_all.sql | VALIDATED |
| CRM-003 | CRM | 7 états utilisateur : NEW_USER, SEARCHING_PROPERTY, PROPERTY_OWNER, AGENT, LEAD_CREATED, PREMIUM_AGENT, INACTIVE | USER_STATES.json | VALIDATED |
| CRM-004 | CRM | 11 types événements : message.received, intent.detected, user.created, user.state_changed, property.created, lead.created, match.generated, payment.success, subscription.renewed, boost.applied, access.granted | EVENT_TYPES.json | VALIDATED |
| CRM-005 | CRM | Agent Opt-In : 4 étapes (détection→demande→log→partage) | agent_optin.py | VALIDATED |
| CRM-006 | CRM | Agent Rating : échelle 1-5 | agent_rating.py | VALIDATED |
| CRM-007 | CRM | Prix lead par défaut : 500 FCFA | agent_dashboard.py | VALIDATED |
| CRM-008 | CRM | Identity resolution : téléphone=100, email=95, nom+téléphone≥40 | identity_resolution.py | VALIDATED |
| CRM-009 | CRM | Master Dashboard password : "lawim2026" | master_dashboard.py | VALIDATED |
| CRM-010 | CRM | 20 tables CRM documentées (15 confirmées dans implement_all.sql) | implement_all.sql | VALIDATED |
| CRM-011 | CRM | Diaspora services table : client_phone, service_type, price, status | implement_all.sql | VALIDATED |
| CRM-012 | CRM | 6 partenaires externes : notaire, architecte, géomètre, artisan, banque, assurance | 08-ROLE-REFERENCE.md | VALIDATED |
| CRM-013 | CRM | 18 acteurs listés (répartis entre user_roles, SQL, et reference docs) | 08-ROLE-REFERENCE.md | PARTIAL |
| CRM-014 | CRM | CRM scoring V5 : 7 facteurs pondérés (total=1.0) | RULE_ENGINE_V5.json | VALIDATED |
| CRM-015 | CRM | Hierarchie rôles : Master→Vice-Master→Assistant→Agence→Agent→Vendeur→Demandeur | 08-ROLE-REFERENCE.md | VALIDATED |

## Language

| Rule ID | Domain | Rule Description | Source | Confidence |
|---------|--------|------------------|--------|------------|
| LANG-001 | Language | Langue par défaut : français | language_handler.py | VALIDATED |
| LANG-002 | Language | Détection hiérarchique : DeepSeek → Gemini (commenté) → Règles locales | language_detector_ia.py | VALIDATED |
| LANG-003 | Language | Commande LANGUE : set_user_language() avec persistance | language_handler.py | VALIDATED |
| LANG-004 | Language | 7 templates multilingues (FR/EN/PID) : welcome, help, no_match, thanks, ask_name, ask_phone, stats | multilingual_responses.py | VALIDATED |
| LANG-005 | Language | 33 entrées entity_linking avec relations : equivalent_to, synonym, related_to, typo_of, abbreviation_of | entity_linking.json | VALIDATED |
| LANG-006 | Language | 5 fichiers typo_database (cities, neighborhoods, property_types, whatsapp, general) | typo_database/*.json | VALIDATED |
| LANG-007 | Language | 7 fichiers whatsapp_language (whatsapp, diaspora, investor, negotiation, listing, search, urgency) | whatsapp_language/*.json | VALIDATED |
| LANG-008 | Language | 5 docs i18n (30-I18N-L10N-REFERENCE, 30A-30D) | Directive/30*.md | VALIDATED |
| LANG-009 | Language | 38 codes pays téléphone dans phone_formatter | phone_formatter.py | VALIDATED |
| LANG-010 | Language | Format Cameroun : 237 + 9 chiffres | phone_formatter.py | VALIDATED |
| LANG-011 | Language | WhatsApp link : https://wa.me/{normalized} | phone_formatter.py | VALIDATED |
| LANG-012 | Language | 12 mots pidgin dans language_detector.py, 14 dans language_detector_ia.py | language_detector.py | PARTIAL |
| LANG-013 | Language | 18 mots-clés français max (pas 20) | language_detector_ia.py | NON_VALIDE |
| LANG-014 | Language | 18 mots-clés anglais max (pas 20) | language_detector_ia.py | NON_VALIDE |

## Security

| Rule ID | Domain | Rule Description | Source | Confidence |
|---------|--------|------------------|--------|------------|
| SEC-001 | Security | Anti-spam : max 10 messages/minute | anti_spam.py | VALIDATED |
| SEC-002 | Security | Blocage automatique : 60 minutes | anti_spam.py | VALIDATED |
| SEC-003 | Security | Table blocked_users pour suivi des spammers | anti_spam.py | VALIDATED |
| SEC-004 | Security | Anti-fraud 4 couches : broker_spam, duplicate_listing, fake_price, suspicious_urgency | RULE_ENGINE_V5.json | VALIDATED |
| SEC-005 | Security | Anonymisation RGPD : SUPPRIMER MES DONNÉES, 7 jours délai | Directive/15-SECURITY-REFERENCE.md | VALIDATED |
| SEC-006 | Security | Niveaux confiance implicites : nouveau (min), vérifié (base), agent noté>3 (renforcé), titre foncier (élevé), spammeur (révoqué) | identity_resolution.py, anti_spam.py | VALIDATED |
| SEC-007 | Security | 25 signaux de fraude documentés | fraud-signals-and-verification.md | VALIDATED |

---

*Document Gold — Index exhaustif des règles métier. Total: 99+ règles documentées.*
