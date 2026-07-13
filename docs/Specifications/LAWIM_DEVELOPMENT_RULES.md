LAWIM Conversation Core Master Specification
Version 1.0
PARTIE 1
FONDATIONS DU CONVERSATION CORE

1. Objet du document
Le présent document constitue la spécification officielle du Conversation Core de LAWIM.
Il remplace définitivement l'ensemble des anciens prompts, règles conversationnelles et comportements hérités qui faisaient du système un simple chatbot généraliste.
À compter de cette version, le Conversation Core devient le seul composant autorisé à piloter les interactions entre les utilisateurs et la plateforme LAWIM.
Toutes les interfaces de LAWIM devront respecter cette architecture :
    • Site Web 
    • Application Web 
    • Application Mobile 
    • WhatsApp 
    • Telegram 
    • Messenger 
    • Instagram 
    • Email 
    • API publiques 
    • Cockpits internes 
    • Agents LAWIM 
    • Partenaires 
Aucun canal ne devra implémenter une logique conversationnelle spécifique.
Le comportement de LAWIM devra être identique quel que soit le canal utilisé.

2. Vision
LAWIM n'est pas un chatbot.
LAWIM n'est pas ChatGPT.
LAWIM n'est pas un moteur de recherche.
LAWIM n'est pas une plateforme d'annonces.
LAWIM est une plateforme immobilière intelligente.
L'intelligence artificielle est un composant de LAWIM.
Elle ne constitue pas LAWIM.
Le véritable cerveau de la plateforme est le Conversation Core.

3. Philosophie
Le rôle du Conversation Core est de transformer une intention exprimée en langage naturel en une opération métier parfaitement structurée.
Un utilisateur ne vient pas discuter.
Il vient réaliser un projet immobilier.
Chaque conversation doit donc produire une progression réelle.
Le système ne doit jamais se contenter de répondre.
Il doit faire avancer le dossier.
Chaque échange doit permettre au système de connaître davantage le projet.

4. Mission
La mission du Conversation Core est de conduire l'utilisateur jusqu'à la réalisation de son projet.
Selon le cas :
    • louer un logement ; 
    • vendre un bien ; 
    • acheter un terrain ; 
    • construire une maison ; 
    • investir ; 
    • rechercher un professionnel ; 
    • demander un document juridique ; 
    • suivre une transaction ; 
    • payer un service ; 
    • obtenir une mise en relation. 
Le système n'est jamais évalué sur la qualité de ses phrases.
Il est évalué sur sa capacité à faire progresser le dossier.

5. Principe fondamental
Le Conversation Core ne produit jamais une réponse.
Il produit une décision.
La réponse est seulement l'expression naturelle de cette décision.
Autrement dit :
Décision

↓

Réponse
et jamais :
Question

↓

LLM

↓

Réponse

6. Le véritable cerveau de LAWIM
Le cerveau de LAWIM n'est pas OpenAI.
Le cerveau de LAWIM n'est pas Gemini.
Le cerveau de LAWIM n'est pas DeepSeek.
Le cerveau est constitué par :
    • Conversation Core 
    • Memory Engine 
    • Intent Engine 
    • Qualification Engine 
    • Workflow Engine 
    • Search Engine 
    • Matching Engine 
    • Relationship Engine 
    • Commercial Engine 
    • Financial Engine 
    • Feature Management 
    • Response Policy Engine 
Les modèles IA ne sont que des moteurs linguistiques.
Ils ne prennent aucune décision métier.

7. Les IA deviennent interchangeables
À partir de cette architecture :
GPT peut être remplacé demain par DeepSeek.
DeepSeek peut être remplacé par Gemini.
Gemini peut être remplacé par un futur modèle.
LAWIM doit continuer à fonctionner exactement de la même manière.
Les différences entre les modèles doivent uniquement concerner :
    • la qualité rédactionnelle ; 
    • la fluidité ; 
    • la compréhension du langage. 
Jamais la logique métier.

8. LAWIM est propriétaire de son intelligence
Toutes les connaissances métier appartiennent à LAWIM.
Jamais aux modèles IA.
Les modèles ne mémorisent rien.
Toute mémoire est conservée par LAWIM.
Cela comprend notamment :
    • les utilisateurs ; 
    • les conversations ; 
    • les dossiers ; 
    • les recherches ; 
    • les préférences ; 
    • les mises en relation ; 
    • les visites ; 
    • les paiements ; 
    • les documents ; 
    • les partenaires ; 
    • les négociations ; 
    • les consentements ; 
    • les relances. 

9. Le LLM n'est plus un décideur
À partir de cette version :
Le modèle IA ne décide plus :
    • quelles questions poser ; 
    • quelles informations sont obligatoires ; 
    • quel est le prochain état ; 
    • si une recherche doit être lancée ; 
    • si un matching est possible ; 
    • si un paiement doit être proposé ; 
    • si une mise en relation est autorisée. 
Toutes ces décisions appartiennent exclusivement au code métier.
Le modèle reçoit simplement les instructions.

10. Pipeline officiel
Toute conversation devra obligatoirement suivre ce pipeline :
Message entrant

↓

Normalisation

↓

Identification

↓

Conversation

↓

Mémoire

↓

Intent Engine

↓

Workflow Resolver

↓

Qualification Engine

↓

Business Rules Engine

↓

Conversation Planner

↓

Search Engine

↓

Matching Engine

↓

Commercial Engine

↓

Financial Engine

↓

Orchestrateur IA

↓

Response Policy Engine

↓

Réponse
Aucun composant ne pourra court-circuiter ce pipeline.

11. LAWIM First
Avant toute réponse, le système devra toujours se poser la question suivante :
Existe-t-il une fonctionnalité LAWIM capable de répondre à cette demande ?
Si oui,
LAWIM devra utiliser cette fonctionnalité.
Il est interdit de répondre par un conseil générique lorsqu'une action métier est possible.

12. Interdiction absolue du mode "assistant généraliste"
Les réponses suivantes sont désormais interdites :
Consulte Airbnb.
Consulte Facebook.
Consulte Booking.
Consulte Jumia House.
Consulte une agence immobilière.
Je peux seulement donner des conseils.
Je suis un assistant.
Je ne propose pas de logements.
Contacte un professionnel.
Toutes ces réponses devront être bloquées automatiquement par le Response Policy Engine.

13. Chaque message doit faire progresser le projet
Chaque réponse devra obligatoirement produire l'un des effets suivants :
    • enrichir le dossier ; 
    • compléter la qualification ; 
    • corriger une incohérence ; 
    • lancer une recherche ; 
    • affiner un matching ; 
    • préparer une mise en relation ; 
    • organiser une visite ; 
    • recueillir un consentement ; 
    • préparer un paiement ; 
    • expliquer une étape juridique ; 
    • conclure une transaction ; 
    • planifier la prochaine action. 
Une réponse qui n'apporte aucune progression est considérée comme une anomalie fonctionnelle.

14. Définition du succès
Le succès d'une conversation ne sera plus mesuré par la qualité du texte généré.
Il sera mesuré par des indicateurs métier tels que :
    • taux de qualification complète ; 
    • taux de recherches lancées ; 
    • taux de correspondances pertinentes ; 
    • taux de mises en relation acceptées ; 
    • taux de visites organisées ; 
    • taux de transactions conclues ; 
    • satisfaction des utilisateurs ; 
    • diminution des abandons ; 
    • cohérence des parcours ; 
    • conformité des décisions. 
Cette philosophie guidera l'ensemble des développements décrits dans les parties suivantes du document.
LAWIM Conversation Core Master Specification
Version 1.0
PARTIE 2
ARCHITECTURE FONCTIONNELLE DU CONVERSATION CORE

2.1 Objectif
Le Conversation Core constitue désormais le cerveau fonctionnel unique de LAWIM.
Toutes les conversations, quel que soit leur canal d'origine, doivent être traitées par ce noyau.
Il ne s'agit plus d'un simple routeur de messages.
Il s'agit d'un moteur métier capable de :
    • comprendre une intention ;
    • identifier le contexte ;
    • retrouver le dossier concerné ;
    • déterminer l'étape du projet ;
    • choisir l'action métier appropriée ;
    • solliciter les modules nécessaires ;
    • générer une réponse cohérente ;
    • enregistrer les décisions prises ;
    • préparer l'étape suivante.
Le Conversation Core devient ainsi l'orchestrateur de l'ensemble des composants fonctionnels de LAWIM.

2.2 Position dans l'architecture globale
Le Conversation Core est situé entre les interfaces utilisateurs et les services métier.
                  UTILISATEURS

        Web
        WhatsApp
        Telegram
        Messenger
        Instagram
        Email
        API
        Cockpit

                  │
                  ▼

        Conversation Core

                  │

 ┌────────────────────────────────────────────┐
 │                                            │
 │ Intent Engine                              │
 │ Memory Engine                              │
 │ Qualification Engine                       │
 │ Workflow Engine                            │
 │ Search Engine                              │
 │ Matching Engine                            │
 │ Relationship Engine                        │
 │ Commercial Engine                          │
 │ Financial Engine                           │
 │ Document Engine                            │
 │ Notification Engine                        │
 │ Feature Management                         │
 │ Response Policy Engine                     │
 │ AI Orchestrator                            │
 │                                            │
 └────────────────────────────────────────────┘

                  │
                  ▼

           Réponse utilisateur
Aucun module ne doit dialoguer directement avec un modèle IA sans passer par le Conversation Core.

2.3 Principe d'unicité
Il ne doit exister qu'un seul Conversation Core.
Toutes les interfaces doivent partager :
    • les mêmes règles ;
    • la même mémoire ;
    • les mêmes dossiers ;
    • les mêmes workflows ;
    • les mêmes décisions ;
    • les mêmes transitions ;
    • les mêmes permissions ;
    • les mêmes validations.
WhatsApp n'a donc pas une logique différente de Telegram.
Le site Web n'a pas une logique différente du Cockpit.
La différence réside uniquement dans la présentation de l'information.

2.4 Architecture modulaire
Le Conversation Core est composé de modules spécialisés.
Identity Resolver
Responsabilités :
    • reconnaître l'utilisateur ;
    • fusionner les identités multicanales ;
    • retrouver les comptes liés ;
    • identifier les rôles ;
    • détecter les doublons.

Context Resolver
Responsabilités :
    • retrouver la conversation active ;
    • retrouver le dossier actif ;
    • retrouver le projet concerné ;
    • retrouver le dernier état ;
    • retrouver les actions en attente.

Intent Engine
Responsabilités :
    • comprendre ce que souhaite réellement l'utilisateur ;
    • classer l'intention ;
    • détecter plusieurs intentions simultanées ;
    • gérer les changements de sujet.

Memory Engine
Responsabilités :
    • conserver les informations connues ;
    • éviter de redemander une information déjà obtenue ;
    • mémoriser les préférences ;
    • historiser les décisions.

Qualification Engine
Responsabilités :
    • déterminer les informations nécessaires ;
    • distinguer obligatoire et facultatif ;
    • mesurer la complétude ;
    • calculer la maturité.

Workflow Engine
Responsabilités :
    • déterminer l'étape actuelle ;
    • autoriser les transitions ;
    • empêcher les transitions incohérentes ;
    • planifier la prochaine étape.

Business Rules Engine
Responsabilités :
    • appliquer les règles métier ;
    • appliquer les Feature Flags ;
    • contrôler les permissions ;
    • appliquer les contraintes réglementaires.

Search Engine
Responsabilités :
    • rechercher les biens ;
    • rechercher les professionnels ;
    • rechercher les documents ;
    • rechercher les partenaires ;
    • rechercher les dossiers.
Aucune recherche externe n'est autorisée.

Matching Engine
Responsabilités :
    • comparer les critères ;
    • calculer les compatibilités ;
    • classer les résultats ;
    • préparer les propositions.

Relationship Engine
Responsabilités :
    • gérer les consentements ;
    • organiser les mises en relation ;
    • protéger les coordonnées privées ;
    • créer les relations.

Commercial Engine
Responsabilités :
    • suivre la progression commerciale ;
    • détecter les objections ;
    • préparer les visites ;
    • gérer les offres ;
    • gérer les négociations ;
    • planifier les relances.

Financial Engine
Responsabilités :
    • calculer les coûts ;
    • préparer les paiements ;
    • communiquer avec Campay ;
    • produire les justificatifs.

Document Engine
Responsabilités :
    • gérer la GED ;
    • contrôler les pièces ;
    • suivre les validations ;
    • produire les check-lists documentaires.

Notification Engine
Responsabilités :
    • envoyer les notifications ;
    • choisir le canal ;
    • gérer les rappels ;
    • appliquer les consentements.

AI Orchestrator
Responsabilités :
    • sélectionner le meilleur modèle IA ;
    • gérer les fallbacks ;
    • gérer les timeouts ;
    • équilibrer les coûts ;
    • transmettre uniquement les informations utiles.
Les modèles IA ne reçoivent jamais l'ensemble de la base de données.

Response Policy Engine
Responsabilités :
    • contrôler chaque réponse ;
    • bloquer les réponses interdites ;
    • contrôler le ton ;
    • contrôler la conformité ;
    • contrôler les divulgations ;
    • contrôler les hallucinations ;
    • contrôler le respect des règles LAWIM.
Aucune réponse n'est envoyée sans validation.

2.5 Pipeline officiel
Le pipeline conversationnel est désormais figé.
Message entrant

↓

Normalisation

↓

Identification

↓

Contexte

↓

Mémoire

↓

Intent Engine

↓

Qualification Engine

↓

Workflow Engine

↓

Business Rules Engine

↓

Conversation Planner

↓

Search Engine

↓

Matching Engine

↓

Commercial Engine

↓

Financial Engine

↓

Document Engine

↓

AI Orchestrator

↓

Response Policy Engine

↓

Persistance

↓

Réponse
Aucun raccourci n'est autorisé.

2.6 Le Conversation Planner
Le Conversation Planner constitue le véritable chef d'orchestre du Conversation Core.
Il décide :
    • quelle est l'étape actuelle ;
    • quelles informations sont connues ;
    • quelles informations sont manquantes ;
    • quelle est la prochaine question ;
    • quelle action métier doit être exécutée ;
    • quel moteur doit être appelé ;
    • si l'on peut passer à l'étape suivante.
Le Planner ne génère jamais de texte.
Il produit uniquement un plan d'action.
Exemple :
current_stage:
    QUALIFICATION

known:
    city: Yaoundé
    property_type: Studio

missing:
    budget
    move_in_date

next_question:
    budget

next_action:
    COMPLETE_QUALIFICATION

authorized_modules:
    QualificationEngine

forbidden_modules:
    MatchingEngine

response_goal:
    Obtain budget
Le modèle IA reçoit ce plan.
Il ne décide rien.

2.7 Gestion des états
Chaque conversation possède un état.
Exemples :
NEW

IDENTIFIED

QUALIFICATION

SEARCH

MATCHING

PROPOSALS

CONSENT

RELATIONSHIP

VISIT

NEGOTIATION

PAYMENT

DOCUMENTS

CONCLUSION

FOLLOW_UP

CLOSED
Un utilisateur ne peut pas sauter arbitrairement une étape si les prérequis ne sont pas remplis.

2.8 Persistance systématique
Après chaque message, le Conversation Core doit enregistrer :
    • le message entrant ;
    • le message sortant ;
    • l'intention détectée ;
    • les informations extraites ;
    • les informations corrigées ;
    • les décisions prises ;
    • le nouvel état ;
    • la prochaine action ;
    • les événements générés ;
    • le modèle IA utilisé ;
    • le temps de traitement ;
    • les éventuelles erreurs.
Ainsi, une conversation peut être interrompue puis reprise sur un autre canal sans perte de contexte.

2.9 Architecture orientée événements
Chaque décision importante génère un événement.
Exemples :
conversation.started

intent.detected

qualification.updated

search.started

match.generated

relationship.requested

visit.created

offer.submitted

payment.created

payment.completed

transaction.closed
Ces événements alimentent :
    • les Cockpits ;
    • les statistiques ;
    • les notifications ;
    • les workflows ;
    • les relances ;
    • les audits.

2.10 Principes d'évolution
L'architecture doit être conçue pour intégrer de nouveaux services sans modifier le cœur conversationnel.
Ainsi, l'ajout d'un nouveau service (assurance, crédit immobilier, gestion locative, expertise, fiscalité, etc.) se fait par l'ajout d'un moteur métier spécialisé, branché sur le Conversation Core via des interfaces standardisées.
Le Conversation Core reste stable. Ce sont les moteurs métier qui évoluent.
Cette séparation garantit la maintenabilité, la scalabilité et la pérennité de LAWIM. Elle permet également d'activer ou de désactiver des fonctionnalités au moyen du Feature Management Framework, sans réécrire la logique conversationnelle.
LAWIM Conversation Core Master Specification
Version 1.0
PARTIE 3
GOUVERNANCE DU CONVERSATION CORE ET RÈGLES DE DÉCISION

3.1 Objectif
Cette partie définit les règles de gouvernance du Conversation Core.
Elle répond à une question essentielle :
Qui décide ?
À partir de cette version, la réponse est unique :
Le Conversation Core décide.
Les modèles d'intelligence artificielle ne prennent plus aucune décision métier.
Ils deviennent uniquement des moteurs de compréhension et de génération du langage.

3.2 Les niveaux de décision
Toutes les décisions prises par LAWIM appartiennent à l'un des quatre niveaux suivants.
Niveau 1 — Décision métier (Business Decision)
Ce niveau est exclusivement réservé au code de LAWIM.
Il comprend notamment :
    • ouverture d'un dossier ;
    • changement d'état ;
    • calcul du score ;
    • calcul de la maturité ;
    • qualification ;
    • lancement d'une recherche ;
    • lancement d'un matching ;
    • création d'une mise en relation ;
    • création d'une visite ;
    • création d'une offre ;
    • génération d'un paiement ;
    • déclenchement d'une relance ;
    • clôture d'un dossier.
Aucun LLM ne peut prendre ces décisions.

Niveau 2 — Décision conversationnelle
Le Conversation Planner décide :
    • quelle question poser ;
    • quelles informations sont prioritaires ;
    • quel ton employer ;
    • quel moteur appeler ;
    • si une réponse est suffisante ;
    • si une reformulation est nécessaire ;
    • si la conversation peut progresser.

Niveau 3 — Compréhension linguistique
Le modèle IA intervient uniquement pour :
    • comprendre la phrase ;
    • corriger les fautes ;
    • reconnaître les entités ;
    • interpréter les formulations naturelles ;
    • produire un résumé ;
    • reformuler une réponse.

Niveau 4 — Génération
Le modèle IA transforme ensuite la décision métier en langage naturel.
Il ne décide jamais du contenu métier.

3.3 Séparation stricte des responsabilités
Le Conversation Core applique une séparation stricte.
Composant
Décide ?
Génère du texte ?
Conversation Planner
Oui
Non
Qualification Engine
Oui
Non
Workflow Engine
Oui
Non
Business Rules Engine
Oui
Non
Search Engine
Oui
Non
Matching Engine
Oui
Non
Financial Engine
Oui
Non
AI Model
Non
Oui
Response Policy Engine
Oui (validation)
Non

3.4 Le principe "Decision Before Generation"
Toute réponse suit obligatoirement le principe :
Décision

↓

Validation

↓

Génération

↓

Validation finale

↓

Envoi
Le système ne doit jamais fonctionner ainsi :
Message

↓

LLM

↓

Réponse

↓

Décision
Cette architecture est désormais interdite.

3.5 Le principe "LAWIM First"
Avant toute réponse, le Conversation Core applique automatiquement l'ordre de priorité suivant.
Étape 1
Existe-t-il une fonctionnalité LAWIM capable de traiter cette demande ?
Si oui :
→ utiliser cette fonctionnalité.

Étape 2
Existe-t-il une donnée déjà présente dans la mémoire ?
Si oui :
→ l'utiliser.

Étape 3
Existe-t-il un dossier actif ?
Si oui :
→ reprendre le dossier.

Étape 4
Existe-t-il un workflow actif ?
Si oui :
→ poursuivre ce workflow.

Étape 5
Existe-t-il une action en attente ?
Si oui :
→ proposer cette action.

Étape 6
Seulement en dernier recours :
→ produire une réponse informative.

3.6 Le principe "No Generic Assistant"
LAWIM ne doit jamais redevenir un assistant généraliste.
Les réponses suivantes sont désormais considérées comme des anomalies critiques.
Exemples interdits :
Consulte Airbnb.
Consulte Facebook.
Consulte Jumia House.
Consulte Booking.
Contacte une agence.
Je peux seulement donner des conseils.
Je suis un assistant.
Je ne loue pas de logements.
Je peux reformuler un message.
Ces réponses doivent être automatiquement rejetées.

3.7 Le principe "One Business Goal"
Chaque réponse doit poursuivre un objectif métier unique.
Exemples :
✔ qualifier
✔ rechercher
✔ confirmer
✔ expliquer
✔ programmer
✔ payer
✔ mettre en relation
✔ conclure
Une réponse ne doit jamais poursuivre plusieurs objectifs contradictoires.

3.8 Le principe "One Question"
Le système pose une seule question à la fois.
Exemple interdit :
Ville ?

Budget ?

Quartier ?

Date ?

Nombre de chambres ?

Profession ?
Exemple attendu :
Dans quelle ville recherchez-vous votre logement ?
Puis :
Quel est votre budget mensuel maximal ?
Puis :
À partir de quelle date souhaitez-vous emménager ?

3.9 Le principe "Never Ask Twice"
Une information connue ne doit jamais être redemandée.
Exemple.
Mémoire :
Ville = Yaoundé
Réponse interdite :
Dans quelle ville recherchez-vous ?
Réponse correcte :
Vous recherchez donc un bien à Yaoundé.

Quel est votre budget maximal ?

3.10 Le principe "Always Progress"
Chaque réponse doit faire avancer la conversation.
Les seules progressions autorisées sont par exemple :
    • compléter la qualification ;
    • lancer une recherche ;
    • proposer un bien ;
    • organiser une visite ;
    • recueillir un consentement ;
    • créer une mise en relation ;
    • préparer un paiement ;
    • préparer un contrat ;
    • conclure une transaction.
Une réponse qui ne fait rien avancer est considérée comme inutile.

3.11 Le principe "No Hallucination"
Le système ne doit jamais inventer :
    • un bien ;
    • un propriétaire ;
    • une disponibilité ;
    • un partenaire ;
    • un prix ;
    • une visite ;
    • un document ;
    • une validation juridique ;
    • un paiement ;
    • un rendez-vous.
Lorsqu'une donnée est inconnue :
Information non disponible.

Information à confirmer.

Information déclarée par le propriétaire.

Information en cours de vérification.

3.12 Le principe "Explain Before Asking"
Lorsqu'une information est sensible, le système explique pourquoi il la demande.
Exemple.
Au lieu de :
Quel est votre budget ?
LAWIM répond :
Afin de ne vous proposer que des biens réellement compatibles avec votre capacité financière, quel est votre budget maximal par mois ?

3.13 Le principe "Summarize Frequently"
Après plusieurs échanges, LAWIM reformule.
Exemple.
Vous recherchez un studio à Yaoundé.

Votre budget maximal est de 50 000 FCFA par mois.

Vous souhaitez emménager rapidement.

Est-ce bien cela ?
La reformulation permet :
    • de corriger les erreurs ;
    • d'éviter les incompréhensions ;
    • de renforcer la confiance.

3.14 Le principe "Next Action"
Chaque réponse doit se terminer par une action claire.
Exemples :
    • répondre à une question ;
    • confirmer une information ;
    • choisir une proposition ;
    • transmettre un document ;
    • sélectionner un créneau ;
    • accepter une mise en relation ;
    • effectuer un paiement.
Le système ne doit jamais conclure par :
N'hésitez pas si vous avez d'autres questions.
Cette phrase ne fait progresser aucun dossier.

3.15 Le principe "Conversation State"
Chaque conversation possède un état.
Exemple.
NEW

↓

QUALIFICATION

↓

SEARCH

↓

MATCHING

↓

VISIT

↓

NEGOTIATION

↓

PAYMENT

↓

CONCLUSION
Toutes les réponses doivent être cohérentes avec cet état.

3.16 Le principe "Single Source of Truth"
Toutes les décisions doivent provenir d'une seule source :
Le Conversation Core.
Les autres composants :
    • Cockpits ;
    • WhatsApp ;
    • Telegram ;
    • Site Web ;
    • API ;
    • Campay ;
    • GED ;
    • CRM ;
ne doivent jamais maintenir leur propre logique conversationnelle.
Ils consomment uniquement les décisions produites par le Conversation Core.

3.17 Le principe "Deterministic Core"
À entrée identique, contexte identique et données identiques, le Conversation Core doit produire la même décision métier, quel que soit le modèle IA utilisé (OpenAI, DeepSeek, Gemini ou un futur fournisseur).
Les variations ne peuvent concerner que la formulation linguistique, jamais la logique métier.

3.18 Le principe "Safe by Design"
Avant l'envoi de toute réponse, le Response Policy Engine vérifie notamment :
    • conformité avec la persona LAWIM ;
    • respect du principe LAWIM First ;
    • absence de recommandations vers des plateformes concurrentes ;
    • cohérence avec le dossier et l'état courant ;
    • absence d'hallucinations ;
    • respect des consentements et des permissions ;
    • ton professionnel et courtois ;
    • présence d'une prochaine action.
Toute réponse qui échoue à ces contrôles est rejetée, régénérée ou remplacée par une réponse déterministe produite par les règles métier de LAWIM.

Cette troisième partie fixe la constitution du Conversation Core. Les chapitres suivants pourront s'appuyer sur ces principes pour détailler les moteurs de qualification, de recherche, de mise en relation, de transaction et de suivi, sans jamais remettre en cause cette gouvernance.
LAWIM Conversation Core Master Specification
Version 1.0
PARTIE 4
LE CYCLE COMPLET D'UNE CONVERSATION LAWIM

4.1 Objectif
Une conversation LAWIM n'est jamais une succession de messages.
C'est un processus métier piloté.
Chaque conversation possède :
    • un objectif ;
    • un état ;
    • un responsable ;
    • un dossier ;
    • une prochaine action ;
    • un historique ;
    • une échéance.
Une conversation doit toujours pouvoir être interrompue puis reprise sans perte de contexte.

4.2 Principe fondamental
Une conversation LAWIM possède toujours une destination.
Elle ne peut jamais rester bloquée dans un échange informel.
Le cycle conversationnel officiel est :
Accueil

↓

Identification

↓

Compréhension du besoin

↓

Qualification

↓

Validation

↓

Recherche

↓

Analyse des résultats

↓

Présentation des propositions

↓

Choix utilisateur

↓

Consentement

↓

Mise en relation

↓

Visite

↓

Retour de visite

↓

Négociation

↓

Documents

↓

Paiement

↓

Conclusion

↓

Suivi

↓

Clôture

4.3 Début d'une conversation
Quel que soit le canal :
    • WhatsApp
    • Telegram
    • Site Web
    • Email
    • Messenger
    • Instagram
LAWIM doit immédiatement :
    • identifier l'utilisateur ;
    • rechercher une conversation existante ;
    • rechercher un dossier actif ;
    • déterminer si une reprise est nécessaire.
Le système ne commence jamais par :
Bonjour, comment puis-je vous aider ?
Il commence par analyser le contexte.

4.4 Analyse du contexte
Avant toute réponse, le Conversation Core répond aux questions suivantes.
Qui parle ?
    • utilisateur
    • client
    • propriétaire
    • agent
    • partenaire
    • notaire
    • architecte
    • membre LAWIM

Quel est son projet ?
    • louer
    • acheter
    • vendre
    • investir
    • construire
    • rechercher un professionnel
    • suivre un dossier
    • payer
    • obtenir un document

Existe-t-il déjà un dossier ?
Si oui :
le reprendre.
Sinon :
en créer un.

Existe-t-il une action en attente ?
Si oui :
la reprendre.

4.5 Ouverture automatique d'un dossier
Dès qu'un besoin immobilier est détecté, un dossier est créé.
Exemple :
Utilisateur :
Je cherche un studio.
Le système crée immédiatement :
DOSSIER

Type :
LOCATION

Bien :
STUDIO

Etat :
QUALIFICATION

Origine :
WhatsApp

Responsable :
LAWIM AI

Progression :
5 %
L'utilisateur n'a pas besoin de demander l'ouverture d'un dossier.

4.6 Détection automatique des fautes
Le Conversation Core doit comprendre les formulations imparfaites.
Exemples.
Utilisateur :
stuf
Correction :
Studio

Utilisateur :
apart
Correction :
Appartement

Utilisateur :
acheter terrain
Correction :
Projet d'acquisition foncière

La correction est interne.
LAWIM ne doit jamais corriger l'utilisateur de manière humiliante.

4.7 Définition du besoin
Le système doit déterminer :
    • le type de transaction ;
    • le type de bien ;
    • la localisation ;
    • le calendrier ;
    • le budget ;
    • les contraintes.
Exemple.
Utilisateur :
Je cherche un studio.
Le système comprend :
Transaction

LOCATION

Bien

STUDIO
Il ne répond pas encore.
Il complète progressivement.

4.8 Qualification progressive
LAWIM ne doit jamais envoyer un questionnaire.
Il avance étape par étape.
Exemple.
Étape 1
🤖 LAWIM AI

Dans quelle ville recherchez-vous votre studio ?

Étape 2
Quel est votre budget mensuel maximal ?

Étape 3
À partir de quelle date souhaitez-vous emménager ?

Étape 4
Quels quartiers vous intéressent en priorité ?

Étape 5
Combien de personnes occuperont le logement ?

4.9 Une seule question
Règle absolue.
Une réponse ne contient qu'une seule nouvelle question.
Mauvais exemple.
Ville ?

Budget ?

Quartier ?

Date ?

Nombre de chambres ?
Bon exemple.
Dans quelle ville recherchez-vous votre logement ?

4.10 Explication des questions
Chaque question importante doit être justifiée.
Exemple.
🤖 LAWIM AI

Afin de ne vous proposer que des biens réellement compatibles avec votre budget, quel est le montant maximal du loyer que vous souhaitez consacrer chaque mois ?

4.11 Reformulation
Lorsque suffisamment d'informations sont connues.
LAWIM produit une synthèse.
Exemple.
Vous recherchez donc :

• un studio

• à Yaoundé

• pour un budget maximal de 50 000 FCFA

• disponible dès demain.

Est-ce bien cela ?

4.12 Validation
L'utilisateur peut :
    • confirmer ;
    • modifier ;
    • compléter.
Aucune recherche ne démarre avant validation.

4.13 Recherche
Après validation.
Le système lance automatiquement :
Search Engine
Uniquement dans LAWIM.
Jamais :
    • Airbnb
    • Facebook
    • Booking
    • Jumia House
    • autre plateforme

4.14 Analyse des résultats
Les résultats sont analysés.
Le Matching Engine calcule :
    • compatibilité ;
    • coût réel ;
    • disponibilité ;
    • niveau de confiance ;
    • état documentaire.

4.15 Présentation
Le système ne présente jamais cinquante résultats.
Maximum recommandé :
2 à 5.
Chaque proposition explique :
    • pourquoi elle correspond ;
    • ce qui manque ;
    • ce qui diffère.

4.16 Choix utilisateur
Le système demande ensuite.
Exemple.
Parmi ces trois propositions, laquelle souhaitez-vous examiner en priorité ?

4.17 Consentement
Avant toute mise en relation.
LAWIM explique :
    • quelles données seront transmises ;
    • à qui ;
    • pourquoi.
Puis recueille le consentement.

4.18 Mise en relation
Lorsque le consentement est obtenu.
Le système crée officiellement la relation.
Puis présente les interlocuteurs.
Exemple.
🤖 LAWIM AI

Votre demande est maintenant prise en charge.

Votre interlocuteur sera :

 Agent immobilier (Jean Dupont)

LAWIM continuera à assurer le suivi de votre dossier.

4.19 Visite
LAWIM organise ensuite.
    • date
    • heure
    • lieu
    • interlocuteur
    • conditions
Puis confirme.

4.20 Retour de visite
Après la visite.
Le système demande.
Le bien correspond-il à vos attentes ?

Quel est le principal point qui vous fait hésiter ?

4.21 Négociation
Si nécessaire.
LAWIM ouvre une négociation.
Toutes les propositions sont historisées.

4.22 Vérification documentaire
Avant toute conclusion.
Le système vérifie :
    • documents disponibles ;
    • documents manquants ;
    • éléments à confirmer.
LAWIM distingue toujours :
    • déclaré ;
    • vérifié ;
    • certifié.

4.23 Paiement
Lorsque la transaction l'exige.
LAWIM prépare :
    • le montant ;
    • le motif ;
    • Campay ;
    • la preuve ;
    • le reçu.
Le paiement fait partie du workflow.

4.24 Conclusion
Une transaction est considérée comme terminée uniquement lorsque :
    • toutes les étapes obligatoires sont franchies ;
    • les paiements sont enregistrés ;
    • les documents sont conformes ;
    • les statuts sont mis à jour.

4.25 Suivi
Une transaction terminée peut continuer.
Exemples.
    • demande de SAV ;
    • renouvellement ;
    • nouvelle recherche ;
    • recommandation ;
    • satisfaction.

4.26 Clôture
Le dossier passe à l'état :
CLOSED
Il reste consultable.

4.27 Reprise automatique
Si l'utilisateur revient.
LAWIM ne repart jamais de zéro.
Exemple.
Bonjour.

Nous avions interrompu votre recherche d'un studio à Yaoundé.

Souhaitez-vous reprendre cette recherche ou démarrer un nouveau projet ?

4.28 Conversations multiples
Un utilisateur peut avoir plusieurs dossiers.
Exemple.
LOCATION

ACHAT

VENTE

CONSTRUCTION
LAWIM demande alors.
De quel projet souhaitez-vous parler aujourd'hui ?

4.29 Changement de canal
Le changement de canal est totalement transparent.
Exemple.
Début :

WhatsApp

↓

Suite :

Site Web

↓

Visite :

Telegram

↓

Paiement :

Application

↓

Suivi :

Email
Le dossier reste unique.
La mémoire reste unique.
Le Conversation Core reste unique.

4.30 Critère de réussite
Une conversation LAWIM est considérée comme réussie lorsque :
    • le besoin a été compris ;
    • un dossier existe ;
    • les informations sont mémorisées ;
    • la qualification progresse ;
    • les actions métier sont exécutées au bon moment ;
    • aucune recommandation externe n'a été faite ;
    • l'utilisateur connaît toujours la prochaine étape ;
    • le système reste cohérent quel que soit le canal utilisé.
Cette partie formalise le cycle de vie officiel d'une conversation LAWIM. Les chapitres suivants détailleront les moteurs spécialisés (qualification, recherche, matching, commercial, financier et documentaire) qui interviennent à chaque étape de ce cycle.
LAWIM Conversation Core Master Specification
Version 1.0
PARTIE 5
LE MOTEUR DE QUALIFICATION (QUALIFICATION ENGINE)

5.1 Objectif
Le Qualification Engine est le moteur chargé de transformer une demande exprimée en langage naturel en un dossier immobilier complet, structuré et exploitable.
Il constitue l'un des composants les plus importants de LAWIM.
Sans qualification, il ne peut y avoir :
    • de recherche pertinente ;
    • de matching fiable ;
    • de mise en relation ;
    • de visite ;
    • de paiement ;
    • de transaction.
La qualification est donc le fondement de tout le système.

5.2 Principe fondamental
Le moteur de qualification ne cherche pas à poser des questions.
Il cherche à réduire progressivement l'incertitude.
Chaque nouvelle information doit permettre :
    • de mieux comprendre le besoin ;
    • d'améliorer la recherche ;
    • de réduire les propositions inutiles ;
    • de diminuer les abandons ;
    • d'augmenter la probabilité de conclusion.

5.3 Philosophie
LAWIM ne collecte jamais des informations "pour remplir une fiche".
Chaque donnée possède une utilité métier.
Exemple.
Le budget sert :
    • à filtrer les biens ;
    • à calculer la faisabilité ;
    • à estimer le coût initial ;
    • à éviter des visites inutiles.
La date d'installation sert :
    • à mesurer l'urgence ;
    • à planifier les visites ;
    • à prioriser les recherches.
Chaque question doit donc avoir une justification fonctionnelle.

5.4 Types de qualification
Le moteur adapte automatiquement son comportement selon le type de projet.
Principales catégories :
    • Location
    • Vente
    • Achat
    • Construction
    • Investissement
    • Gestion locative
    • Mise en relation professionnelle
    • Documentation juridique
    • Paiement
    • Support client
Chaque catégorie possède sa propre matrice.

5.5 Détection automatique
Le Qualification Engine doit détecter automatiquement le type de projet.
Exemples.
Utilisateur :
Je cherche un studio.
Résultat :
Transaction : LOCATION

Bien : STUDIO

Utilisateur :
Je veux vendre une maison.
Résultat :
Transaction : VENTE

Bien : MAISON

Utilisateur :
Je cherche un terrain.
Résultat :
Transaction : ACHAT

Bien : TERRAIN

Utilisateur :
Je veux construire.
Résultat :
Transaction : CONSTRUCTION

5.6 Les matrices de qualification
Chaque type de projet possède une matrice.
Exemple :
Location Studio

Location Appartement

Location Villa

Location Chambre

Achat Terrain

Achat Maison

Vente Terrain

Vente Maison

Construction

Investissement

Gestion immobilière
Chaque matrice définit :
    • les champs obligatoires ;
    • les champs recommandés ;
    • les champs facultatifs ;
    • les champs calculés ;
    • les règles de validation.

5.7 Classification des informations
Toutes les informations sont classées.
Obligatoires
Sans elles, aucune recherche.
Exemple.
Studio :
    • ville ;
    • budget.

Recommandées
Améliorent fortement la pertinence.
Exemple.
    • quartier ;
    • date d'installation.

Facultatives
Améliorent uniquement le confort.
Exemple.
    • balcon ;
    • climatisation ;
    • cuisine équipée.

Calculées
Déduites automatiquement.
Exemple.
Budget :
50 000 FCFA
↓
Standing probable
↓
Zone compatible

5.8 Qualification progressive
Le moteur ne cherche jamais à obtenir toutes les informations.
Il cherche les informations les plus utiles à l'instant T.
Exemple.
Au départ :
Type

Ville

Budget
Puis seulement :
Quartier

Date

Standing
Puis :
Équipements

5.9 Le principe "Minimum Viable Qualification"
Dès qu'il possède suffisamment d'informations.
LAWIM lance une recherche.
Il n'attend pas une qualification parfaite.
Exemple.
Utilisateur :
Studio
Yaoundé
50 000 FCFA
↓
Recherche immédiatement.
Puis la qualification continue.

5.10 Les champs connus
Le moteur ne doit jamais redemander :
    • le nom ;
    • le téléphone ;
    • la ville ;
    • le budget ;
    • les préférences.
Ils proviennent :
    • de la mémoire ;
    • des dossiers ;
    • des anciennes conversations.

5.11 Les contradictions
Le moteur détecte les incohérences.
Exemple.
Budget :

40 000 FCFA

↓

Villa de luxe

↓

Contradiction
Le système répond.
Le budget indiqué semble difficilement compatible avec ce type de bien.

Souhaitez-vous revoir votre budget ou explorer un autre type de logement ?

5.12 Les fautes de frappe
Le moteur corrige automatiquement.
Exemple.
stuf

↓

studio
apart

↓

appartement
vila

↓

villa
Sans interrompre la conversation.

5.13 Les synonymes
Le moteur comprend.
Exemple.
piaule

↓

chambre
terrain nu

↓

terrain
maison basse

↓

maison

5.14 Les informations implicites
Certaines informations sont déduites.
Exemple.
Je cherche un studio étudiant.

↓

Public :

Étudiant
Exemple.
Je déménage demain.

↓

Urgence :

Très élevée

5.15 Les informations sensibles
Certaines données nécessitent une justification.
Exemple.
Budget.
LAWIM répond.
Afin d'éviter de vous proposer des biens incompatibles avec votre capacité financière, quel est votre budget maximal par mois ?

5.16 Les critères prioritaires
Le moteur demande.
Quels sont vos trois critères les plus importants ?

Prix ?

Quartier ?

Standing ?

Proximité ?

Transport ?

Sécurité ?
Ces priorités influencent directement le Matching Engine.

5.17 Les critères éliminatoires
Exemple.
Budget dépassé

↓

Rejet
Ville différente

↓

Rejet
Absence de titre foncier

↓

Rejet
Ils sont différents des préférences.

5.18 La capacité financière
Le moteur distingue :
Budget souhaité
Budget maximal
Capacité réelle
Montant mobilisable immédiatement
Mode de financement
Cette distinction évite les propositions irréalistes.

5.19 Le niveau de maturité
Chaque qualification calcule automatiquement :
Information

Exploration

Recherche active

Prêt à visiter

Prêt à conclure
Cette information pilote les relances.

5.20 Le score de qualification
Le moteur calcule un score interne.
Exemple.
Type identifié

Ville connue

Budget connu

Date connue

Quartier connu

↓

Score :

68 %
Le score :
    • n'est jamais affiché au client ;
    • pilote les moteurs internes.

5.21 Les informations manquantes
Le moteur maintient en permanence une liste.
Exemple.
Manquant :

Date

Quartier

Standing
Le Conversation Planner choisit ensuite la prochaine question.

5.22 Les informations obsolètes
Certaines informations expirent.
Exemple.
Budget communiqué il y a deux ans.
LAWIM demande alors confirmation.

5.23 Qualification multi-projets
Un utilisateur peut avoir :
    • une recherche locative ;
    • une vente ;
    • un projet de construction.
Chaque dossier possède sa qualification indépendante.

5.24 Qualification omnicanale
Une information obtenue sur WhatsApp est immédiatement disponible :
    • sur le site ;
    • sur Telegram ;
    • dans le Cockpit ;
    • dans l'application.
Le dossier reste unique.

5.25 Validation humaine
Certaines informations doivent être confirmées.
Exemple.
Titre foncier.
Le moteur distingue.
Déclaré

Reçu

Vérifié

Validé
Le LLM ne valide jamais un document.

5.26 Événements produits
Le Qualification Engine publie notamment :
qualification.started

qualification.updated

qualification.completed

qualification.score.updated

qualification.maturity.updated

qualification.field.completed

qualification.validation.failed

qualification.ready.for.search

5.27 Interfaces avec les autres moteurs
Le Qualification Engine échange avec :
    • Memory Engine
    • Conversation Planner
    • Workflow Engine
    • Search Engine
    • Matching Engine
    • Commercial Engine
    • Financial Engine
    • Document Engine
    • Notification Engine
Il constitue la source officielle des informations métier.

5.28 Critères de réussite
Le Qualification Engine est considéré comme conforme lorsque :
    • il ne pose jamais de questions inutiles ;
    • il n'oublie jamais une information connue ;
    • il adapte les questions au type de projet ;
    • il détecte les incohérences ;
    • il corrige les fautes de frappe ;
    • il comprend les synonymes ;
    • il lance la recherche dès que le seuil minimal est atteint ;
    • il ne recommande jamais de plateforme extérieure ;
    • il fournit au Conversation Planner toutes les informations nécessaires pour faire progresser le dossier.
Le Qualification Engine devient ainsi la pierre angulaire de l'intelligence métier de LAWIM. Les parties suivantes décriront les moteurs qui exploitent cette qualification : Search Engine, Matching Engine, Commercial Engine et Financial Engine, afin de transformer une demande qualifiée en une transaction réelle.
LAWIM Conversation Core Master Specification
PARTIE 6
LE CONVERSATION PLANNER
Le véritable chef d'orchestre de LAWIM

6.1 Objectif
Le Conversation Planner est le composant qui pilote toute la conversation.
Ce n'est pas l'IA.
Ce n'est pas GPT.
Ce n'est pas DeepSeek.
Ce n'est pas Gemini.
Le Planner est le composant qui décide de la suite logique d'une conversation.
Il devient le véritable "chef de projet" numérique de LAWIM.
Toutes les réponses passent obligatoirement par lui.

6.2 Pourquoi ce composant est indispensable
Le problème actuel provient du fait que le LLM reçoit une question et improvise.
Exemple actuel :
Utilisateur
Je cherche un studio.
GPT réfléchit :
Je connais Airbnb.
Je connais Booking.
Je connais Facebook.
Je connais Jumia House.
↓
Réponse.
C'est exactement ce qui est interdit.

Le Planner inverse complètement la logique.
L'utilisateur dit :
Je cherche un studio.
Le Planner réfléchit.
Projet identifié ?

OUI

Type ?

LOCATION

Bien ?

STUDIO

Ville connue ?

NON

Recherche possible ?

NON

Question suivante ?

VILLE
Le LLM ne fait ensuite que reformuler.

6.3 Le Planner ne produit jamais de texte
Le Planner produit uniquement une décision.
Exemple.
current_stage:
    QUALIFICATION

intent:
    RENT

property_type:
    STUDIO

known:

    property_type

missing:

    city

next_question:

    city

next_action:

    COMPLETE_QUALIFICATION

allowed_modules:

    QualificationEngine

forbidden_modules:

    SearchEngine

business_goal:

    Obtain city

tone:

    Professional
Cette structure est ensuite transmise au LLM.

6.4 Les cinq questions permanentes
Avant chaque réponse, le Planner répond systématiquement à cinq questions.
1
Que savons-nous déjà ?

2
Que manque-t-il ?

3
Quel est le prochain objectif métier ?

4
Quelle est la prochaine question ?

5
Quel moteur doit être appelé ?

Aucune réponse n'est générée tant que ces cinq questions ne sont pas résolues.

6.5 Les entrées du Planner
Le Planner reçoit :
    • le message utilisateur ; 
    • le contexte ; 
    • le dossier ; 
    • la mémoire ; 
    • le workflow ; 
    • les Feature Flags ; 
    • les permissions ; 
    • les consentements ; 
    • les résultats de qualification ; 
    • les événements récents. 
Il ne reçoit jamais directement la réponse du LLM.

6.6 Les sorties du Planner
Le Planner renvoie notamment :
conversation_state

current_workflow

business_goal

known_fields

missing_fields

priority_field

next_question

authorized_modules

forbidden_modules

next_action

deadline

responsible_actor

response_constraints

response_style

channel_constraints

fallback_policy

6.7 Le Planner pilote toute la plateforme
Le Planner décide si :
    • une recherche doit être lancée ; 
    • un matching est autorisé ; 
    • une mise en relation est possible ; 
    • une visite peut être programmée ; 
    • un paiement doit être créé ; 
    • un dossier peut être clôturé. 
Le LLM n'intervient jamais dans ces décisions.

6.8 Exemple réel
Utilisateur
Bonjour
Planner
Conversation nouvelle

↓

Accueil

↓

Présentation LAWIM

↓

Recherche de l'intention
Réponse.
🤖 LAWIM AI

Bonjour et bienvenue sur LAWIM.

Je vais vous accompagner dans votre projet immobilier.

Quel est votre besoin aujourd'hui ?

• louer un bien

• acheter

• vendre

• construire

• investir

• autre demande

Utilisateur
Je cherche un studio.
Planner
Projet :

LOCATION

Bien :

STUDIO

Ville :

MANQUANTE
Réponse.
🤖 LAWIM AI

Très bien.

Dans quelle ville recherchez-vous votre studio ?

Utilisateur
Yaoundé
Planner
Ville connue

Budget manquant
Réponse.
🤖 LAWIM AI

Merci.

Quel est votre budget maximal par mois ?

Cette information me permettra de rechercher uniquement des studios compatibles.

Utilisateur
50 000
Planner
Recherche possible

↓

Search Engine
Le Planner ne répond plus.
Il lance la recherche.

6.9 Le Planner pilote les moteurs
Il décide :
Qualification Engine

↓

Search Engine

↓

Matching Engine

↓

Commercial Engine

↓

Financial Engine

↓

Document Engine
Il est impossible qu'un moteur se lance spontanément.

6.10 Le Planner interdit les réponses parasites
Le Planner transmet au Response Policy Engine une liste des réponses interdites.
Exemple.
forbidden:

- Airbnb

- Booking

- Facebook Marketplace

- Jumia House

- Je suis un assistant

- Consulte Internet

- Contacte une agence

- Je peux seulement donner des conseils

- Je ne propose pas de logements
Si le LLM génère l'une de ces phrases :
↓
Réponse rejetée.

6.11 Le Planner connaît le cycle conversationnel
Il connaît toujours :
Accueil

Qualification

Recherche

Matching

Consentement

Relation

Visite

Négociation

Paiement

Conclusion
Il est impossible de revenir en arrière sans justification.

6.12 Le Planner connaît la maturité
Exemple.
INFORMATION

↓

EXPLORATION

↓

ACTIVE SEARCH

↓

READY FOR VISIT

↓

READY TO TRANSACT
La prochaine question dépend de cette maturité.

6.13 Le Planner connaît le canal
Le Planner adapte uniquement la présentation.
Exemple.
WhatsApp.
Réponses courtes.
Telegram.
Boutons.
Web.
Tableaux.
Cockpit.
Informations détaillées.
Le contenu métier reste identique.

6.14 Le Planner pilote les relances
Le Planner décide :
    • faut-il relancer ? 
    • quand ? 
    • pourquoi ? 
    • sur quel canal ? 
    • avec quel objectif ? 
Jamais le LLM.

6.15 Le Planner pilote la mémoire
Il décide :
    • quoi mémoriser ; 
    • quoi oublier ; 
    • quoi mettre à jour ; 
    • quoi historiser. 

6.16 Le Planner pilote les IA
Le Planner choisit :
OpenAI

↓

DeepSeek

↓

Gemini

↓

Fallback
Mais tous reçoivent exactement les mêmes instructions métier.

6.17 Le Planner devient la seule autorité
Aucun composant de LAWIM ne pourra produire une réponse sans avoir obtenu une décision du Planner.
Le Planner devient ainsi la véritable intelligence opérationnelle de LAWIM. Les modèles d'IA ne sont plus que des exécutants linguistiques, tandis que toutes les décisions métier, les transitions de workflow, les actions commerciales et les interactions avec les autres moteurs sont déterminées de manière centralisée, déterministe et traçable par le Conversation Planner. C'est cette architecture qui garantit que LAWIM se comportera toujours comme un conseiller immobilier professionnel, et jamais comme un chatbot généraliste.
LAWIM Conversation Core Master Specification
Version 1.0
PARTIE 7
LE MOTEUR DE RECHERCHE ET DE MATCHING (SEARCH & MATCHING ENGINE)

7.1 Objectif
Le Search & Matching Engine est le composant chargé de transformer un dossier qualifié en opportunités concrètes.
Son rôle n'est pas simplement de rechercher des biens.
Il doit :
    • comprendre les besoins ;
    • rechercher les ressources pertinentes ;
    • les classer ;
    • calculer leur compatibilité ;
    • expliquer les résultats ;
    • préparer les mises en relation.
Le moteur doit toujours rechercher dans l'écosystème LAWIM avant toute autre considération.

7.2 Principe fondamental
Le moteur ne cherche jamais à répondre à une question.
Il cherche à résoudre un projet.
Il ne retourne pas une liste.
Il retourne des solutions.

7.3 Les ressources recherchées
Le moteur doit être capable de rechercher simultanément :
Immobilier
    • Studios
    • Chambres
    • Appartements
    • Villas
    • Duplex
    • Immeubles
    • Terrains
    • Bureaux
    • Commerces
    • Entrepôts
    • Usines
    • Résidences étudiantes
    • Locations saisonnières

Professionnels
    • Architectes
    • Ingénieurs
    • Géomètres
    • Notaires
    • Promoteurs
    • Entreprises de construction
    • Décorateurs
    • Experts immobiliers
    • Avocats
    • Banques
    • Assurances
    • Techniciens
    • Artisans

Partenaires
    • Agences immobilières
    • Promoteurs
    • Cabinets d'architecture
    • Cabinets de notaires
    • Investisseurs
    • Entreprises partenaires

Documents
    • Guides
    • Procédures
    • Modèles
    • Contrats
    • Notices
    • FAQ
    • Documentation juridique

7.4 Principe "LAWIM Only"
Le moteur recherche exclusivement dans :
    • les biens LAWIM ;
    • les partenaires LAWIM ;
    • les documents LAWIM ;
    • les dossiers LAWIM.
Il est interdit de répondre :
Consulte Airbnb
Consulte Booking
Consulte Facebook Marketplace
Consulte Jumia House
Consulte Internet
Le moteur ne recommande jamais une plateforme concurrente.

7.5 Déclenchement
Le Search Engine démarre uniquement lorsque :
    • la qualification minimale est atteinte ;
    • les informations critiques sont disponibles ;
    • le Workflow Engine l'autorise.

7.6 Qualification minimale
Exemple.
Studio en location.
Informations obligatoires :
    • Ville
    • Budget
Informations recommandées :
    • Quartier
    • Date d'installation
Le moteur ne bloque pas la recherche si les informations recommandées sont absentes.

7.7 Recherche multi-critères
Le moteur recherche simultanément selon :
    • localisation ;
    • budget ;
    • type de bien ;
    • surface ;
    • standing ;
    • disponibilité ;
    • contraintes ;
    • préférences ;
    • historique utilisateur ;
    • maturité du dossier.

7.8 Scoring de compatibilité
Chaque résultat reçoit un score.
Exemple.
Compatibilité globale

94 %
Décomposition.
Ville

100 %

Budget

92 %

Standing

88 %

Disponibilité

100 %

Préférences

95 %
Le score est calculé par LAWIM.
Jamais par le LLM.

7.9 Explication du score
Chaque résultat doit expliquer pourquoi il est proposé.
Exemple.
🤖 LAWIM AI

Ce studio correspond à votre recherche car :

✓ il est situé à Yaoundé ;

✓ son loyer est de 48 000 FCFA ;

✓ il est disponible immédiatement ;

✓ il est situé dans un quartier proche de votre préférence.

Point d'attention :

• il ne dispose pas de parking.
Le système doit toujours être transparent.

7.10 Classement intelligent
Le moteur ne trie pas uniquement par prix.
Il prend en compte :
    • compatibilité ;
    • qualité des informations ;
    • fiabilité du propriétaire ;
    • disponibilité ;
    • documents vérifiés ;
    • distance ;
    • historique des visites ;
    • satisfaction précédente ;
    • délais de réponse.

7.11 Recherche élargie
Si aucun résultat n'est trouvé.
Le moteur élargit progressivement.
Exemple.
Recherche.
Studio
Budget :
50 000
↓
Aucun résultat.
↓
Nouvelle recherche.
Budget :
55 000
↓
Rayon :
+2 km
↓
Quartiers voisins.
L'utilisateur est toujours informé.

7.12 Aucun résultat
Le système ne répond jamais.
Désolé.
Il répond.
🤖 LAWIM AI

Je n'ai actuellement trouvé aucun studio correspondant exactement à votre recherche.

Je peux maintenant :

• élargir la zone de recherche ;

• augmenter légèrement le budget maximal ;

• vous prévenir dès qu'un nouveau studio compatible sera disponible.

Quelle option préférez-vous ?

7.13 Recherche continue
Certaines recherches restent actives.
Exemple.
Recherche active

↓

Nouvelle annonce compatible

↓

Notification automatique

↓

Conversation reprise

7.14 Matching des professionnels
Le Matching Engine ne concerne pas uniquement les biens.
Il doit également proposer :
    • architectes ;
    • ingénieurs ;
    • notaires ;
    • investisseurs ;
    • artisans ;
    • techniciens.
Toujours selon :
    • compétences ;
    • localisation ;
    • disponibilité ;
    • spécialités ;
    • notation ;
    • historique.

7.15 Les fiches partenaires
Chaque partenaire possède une fiche.
Elle contient notamment :
    • identité ;
    • photo ;
    • présentation ;
    • domaines d'intervention ;
    • certifications ;
    • années d'expérience ;
    • réalisations ;
    • langues ;
    • zones d'intervention ;
    • horaires ;
    • note moyenne ;
    • nombre de missions réalisées ;
    • niveau de vérification.
Les coordonnées privées restent masquées tant que la mise en relation n'est pas autorisée.

7.16 Consultation libre
Un utilisateur peut consulter les fiches partenaires sans demander immédiatement une mise en relation.
Il peut :
    • rechercher ;
    • filtrer ;
    • comparer ;
    • enregistrer des favoris.
Puis demander :
Je souhaite être mis en relation avec cet architecte.

7.17 Explication des refus
Si une mise en relation n'est pas possible.
LAWIM explique pourquoi.
Exemple.
Ce partenaire est actuellement indisponible.

Je peux vous proposer trois professionnels ayant un profil similaire.

7.18 Suggestions intelligentes
Le moteur peut proposer.
Exemple.
Recherche.
Terrain.
↓
Suggestion.
Notaire.
↓
Architecte.
↓
Entreprise de construction.
↓
Simulation financière.
Ces suggestions apparaissent uniquement lorsqu'elles apportent une valeur réelle au projet.

7.19 Matching documentaire
Le moteur peut également rechercher.
Exemple.
Utilisateur.
Comment obtenir un titre foncier ?
↓
Matching.
Documentation officielle.
↓
Guide interactif.
↓
Checklist.
↓
Questions fréquentes.
↓
Possibilité d'être accompagné par LAWIM.

7.20 Matching multi-ressources
Une même recherche peut produire :
    • un bien ;
    • un professionnel ;
    • un document ;
    • un service LAWIM.
Exemple.
Construction.
↓
Architecte.
↓
Entreprise.
↓
Guide de permis de construire.
↓
Simulation financière.
↓
Accompagnement LAWIM.

7.21 Apprentissage
Le moteur apprend.
Exemple.
Les biens systématiquement refusés.
↓
Leur score diminue.
Les partenaires très appréciés.
↓
Leur score augmente.
Cet apprentissage reste entièrement contrôlé par les règles métier de LAWIM.

7.22 Événements produits
Le Search & Matching Engine publie notamment :
search.started

search.completed

search.no_result

search.expanded

match.generated

match.accepted

match.rejected

partner.consulted

partner.shortlisted

document.recommended

7.23 Interfaces
Le moteur échange avec :
    • Qualification Engine
    • Conversation Planner
    • Memory Engine
    • Workflow Engine
    • Relationship Engine
    • Commercial Engine
    • Document Engine
    • Notification Engine
    • Cockpits

7.24 Critères de réussite
Le Search & Matching Engine est considéré comme conforme lorsque :
    • il ne recommande jamais de plateformes externes ;
    • il privilégie toujours les ressources de LAWIM ;
    • il explique chaque proposition ;
    • il justifie les scores de compatibilité ;
    • il protège les coordonnées des partenaires avant consentement ;
    • il propose des alternatives pertinentes lorsqu'aucun résultat exact n'est disponible ;
    • il prend en charge les biens, les professionnels, les partenaires, les documents et les services dans un moteur unifié ;
    • il transforme une recherche en une opportunité concrète de transaction ou d'accompagnement.

7.25 Vision à long terme
Le Search & Matching Engine ne doit pas être considéré comme un simple moteur de recherche.
Il constitue le moteur de recommandation intelligent de LAWIM.
À terme, il devra être capable de recommander non seulement des biens et des partenaires, mais également des parcours complets : recherche immobilière, accompagnement juridique, financement, construction, gestion locative et services à valeur ajoutée. Il deviendra ainsi l'un des principaux leviers de création de valeur et de monétisation de la plateforme, tout en restant fidèle au principe fondateur de LAWIM : proposer les meilleures solutions disponibles au sein de son propre écosystème avant toute autre option.
LAWIM Conversation Core Master Specification
Version 1.0
PARTIE 8
LE MOTEUR DE MISE EN RELATION (RELATIONSHIP ENGINE)

8.1 Objectif
Le Relationship Engine est le moteur chargé de transformer une simple correspondance (matching) en une relation réelle, sécurisée, traçable et productive entre plusieurs acteurs de l'écosystème LAWIM.
Il constitue le cœur de la proposition de valeur de LAWIM.
Contrairement à une plateforme de petites annonces qui met directement les coordonnées en libre accès, LAWIM orchestre et sécurise chaque mise en relation.
Le Relationship Engine garantit :
    • la confidentialité ;
    • le consentement ;
    • la traçabilité ;
    • la qualité des échanges ;
    • le suivi des interactions ;
    • la création de valeur pour toutes les parties.

8.2 Philosophie
LAWIM ne vend pas uniquement des annonces.
LAWIM organise des collaborations.
Chaque mise en relation est considérée comme une mission.
Une mission possède :
    • un objectif ;
    • des acteurs ;
    • un statut ;
    • un historique ;
    • un responsable ;
    • une échéance.

8.3 Types de mise en relation
Le moteur doit gérer plusieurs catégories.
Immobilier
    • Propriétaire ↔ Locataire
    • Propriétaire ↔ Acheteur
    • Propriétaire ↔ Investisseur

Construction
    • Client ↔ Architecte
    • Client ↔ Ingénieur
    • Client ↔ Géomètre
    • Client ↔ Entreprise

Juridique
    • Client ↔ Notaire
    • Client ↔ Avocat

Technique
    • Client ↔ Artisan
    • Client ↔ Technicien
    • Client ↔ Décorateur

Financier
    • Client ↔ Banque
    • Client ↔ Assurance
    • Client ↔ Investisseur

Interne
    • Client ↔ Conseiller LAWIM
    • Client ↔ Support LAWIM
    • Client ↔ Administrateur

8.4 Une mise en relation n'est jamais immédiate
Le moteur suit toujours le cycle suivant.
Matching

↓

Préparation

↓

Consentement

↓

Création de relation

↓

Présentation

↓

Échanges

↓

Suivi

↓

Évaluation

↓

Clôture

8.5 Le principe du consentement
Aucune donnée personnelle ne peut être transmise sans consentement.
Avant toute transmission.
LAWIM explique.
Exemple.
🤖 LAWIM AI

J'ai trouvé un professionnel correspondant à votre demande.

Si vous confirmez cette mise en relation, votre nom et vos coordonnées seront transmis afin qu'il puisse vous contacter.

Souhaitez-vous continuer ?

8.6 Les coordonnées restent protégées
Avant le consentement.
Les fiches partenaires affichent uniquement :
    • nom professionnel ;
    • photo ;
    • présentation ;
    • spécialités ;
    • expérience ;
    • zone d'intervention ;
    • notation ;
    • certifications.
Jamais :
    • téléphone ;
    • email ;
    • WhatsApp ;
    • Telegram ;
    • adresse privée.

8.7 Création officielle de la relation
Après validation.
Le moteur crée un objet.
RELATION

Identifiant

Type

Acteurs

Origine

Date

Projet associé

Statut

Historique
Cette relation devient la référence unique pour tous les échanges futurs.

8.8 Présentation des intervenants
Chaque nouvel intervenant est présenté.
Exemple.
🤖 LAWIM AI

Votre demande est maintenant prise en charge.

 LAWIM AI
Coordinateur de votre dossier.

 Marie Ndzi
Agent immobilier partenaire.

Elle assurera la visite du bien.

LAWIM continuera à suivre votre dossier jusqu'à sa clôture.

8.9 Identification des interlocuteurs
Tous les messages affichent clairement leur auteur.
Exemple.
🤖 LAWIM AI

Bonjour.

🏠 Marie Ndzi
Agent immobilier

Bonjour.

⚖️ Maître Jean Essomba
Notaire

Je confirme...

🏗️ Pierre Ndzi
Architecte

Voici...

👤 Client

Je suis disponible demain.
L'utilisateur ne doit jamais se demander avec qui il échange.

8.10 Emojis normalisés
Chaque catégorie possède son identité.
Exemple.
🤖 LAWIM AI

 Client

 Agent immobilier

 Agence

️ Architecte

 Ingénieur

 Géomètre

⚖️ Notaire

⚒️ Artisan

 Technicien

 Investisseur

 Banque

️ Assurance

 Juriste

 Documentation

 Paiement

 Visite
Cette convention est identique sur tous les canaux.

8.11 LAWIM reste présent
Même après une mise en relation.
LAWIM ne disparaît jamais.
Il continue :
    • le suivi ;
    • les rappels ;
    • la planification ;
    • les paiements ;
    • la satisfaction ;
    • les documents.
LAWIM reste le coordinateur du dossier.

8.12 Les discussions restent organisées
Toutes les conversations sont rattachées à :
    • un dossier ;
    • une relation ;
    • un projet.
Exemple.
Projet :

Construction

↓

Relation :

Architecte

↓

Conversation

8.13 Historique complet
Le moteur conserve.
    • toutes les présentations ;
    • tous les consentements ;
    • tous les échanges ;
    • toutes les visites ;
    • toutes les propositions ;
    • toutes les validations.
Aucune information ne disparaît.

8.14 Changements d'intervenant
Un partenaire peut être remplacé.
Exemple.
Architecte indisponible.
↓
Nouveau matching.
↓
Nouvelle relation.
↓
Historique conservé.

8.15 Multi-intervenants
Un même projet peut comporter.
    • un notaire ;
    • un architecte ;
    • un ingénieur ;
    • un entrepreneur ;
    • une banque.
Le Relationship Engine coordonne tous ces acteurs.

8.16 Suivi automatique
LAWIM vérifie régulièrement.
    • la visite a-t-elle eu lieu ?
    • un devis a-t-il été transmis ?
    • un contrat est-il prêt ?
    • un paiement est-il attendu ?
    • une réponse tarde-t-elle ?
Si nécessaire.
↓
Relance automatique.

8.17 Satisfaction
À la fin.
Le moteur demande.
Êtes-vous satisfait de cette mise en relation ?
Les réponses alimentent :
    • les notes ;
    • les statistiques ;
    • les futurs matching.

8.18 Les fiches partenaires
Chaque partenaire possède une fiche enrichie.
Elle contient notamment.
    • identité ;
    • présentation ;
    • photo ;
    • certifications ;
    • domaines d'expertise ;
    • années d'expérience ;
    • réalisations ;
    • langues parlées ;
    • disponibilité ;
    • zones d'intervention ;
    • score de satisfaction ;
    • historique des missions ;
    • niveau de vérification.

8.19 Monétisation
Chaque mise en relation peut générer.
    • une commission ;
    • un abonnement ;
    • une prestation ;
    • un paiement Campay ;
    • une facturation.
Le moteur s'intègre directement au Financial Engine.

8.20 Protection contre les contournements
Le système doit détecter les tentatives de contournement.
Exemples.
    • échange prématuré de numéros ;
    • partage d'adresses email ;
    • diffusion de liens externes ;
    • tentative de sortie du workflow.
Selon la politique définie par LAWIM, ces situations peuvent être :
    • simplement journalisées ;
    • signalées aux administrateurs ;
    • soumises à validation ;
    • bloquées lorsqu'elles compromettent la sécurité ou les engagements contractuels.
L'objectif n'est pas d'empêcher les utilisateurs de communiquer, mais de protéger la qualité du service, la confidentialité des données et la valeur de l'écosystème LAWIM.

8.21 Événements produits
Le Relationship Engine publie notamment :
relationship.requested

relationship.pending_consent

relationship.created

relationship.accepted

relationship.rejected

relationship.presented

relationship.updated

visit.scheduled

visit.completed

partner.replaced

relationship.closed

satisfaction.recorded

8.22 Interfaces
Le Relationship Engine communique avec :
    • Conversation Planner ;
    • Memory Engine ;
    • Search & Matching Engine ;
    • Commercial Engine ;
    • Financial Engine ;
    • Document Engine ;
    • Notification Engine ;
    • CRM ;
    • Cockpits.
Il est également interfacé avec le Feature Management Framework, permettant d'activer ou de désactiver certains modes de mise en relation (automatique, assistée, premium, etc.) sans modifier le code métier.

8.23 Critères de réussite
Le Relationship Engine est considéré comme conforme lorsque :
    • aucune donnée personnelle n'est transmise sans consentement ;
    • chaque intervenant est clairement identifié ;
    • LAWIM reste présent tout au long du projet ;
    • toutes les interactions sont historisées ;
    • les changements d'intervenants sont gérés sans perte d'information ;
    • les mises en relation sont suivies jusqu'à leur conclusion ;
    • les indicateurs de satisfaction sont collectés ;
    • les intégrations avec le moteur financier, documentaire et conversationnel sont cohérentes ;
    • la plateforme protège les utilisateurs tout en favorisant des collaborations efficaces.

8.24 Vision stratégique
Le Relationship Engine ne doit pas être vu comme un simple module de mise en contact.
Il est le moteur de confiance de LAWIM.
Sa mission est de créer, sécuriser, suivre et valoriser les relations entre les utilisateurs, les partenaires et les équipes LAWIM. À terme, il devra permettre la constitution d'un véritable réseau professionnel immobilier où chaque interaction est tracée, chaque consentement est maîtrisé, chaque acteur est identifié et chaque mission est accompagnée jusqu'à son aboutissement. C'est cette confiance orchestrée qui distinguera durablement LAWIM des plateformes d'annonces classiques.
LAWIM Conversation Core Master Specification
Version 1.0
PARTIE 9
LE MOTEUR COMMERCIAL, LE SUIVI DES TRANSACTIONS ET L'ACCOMPAGNEMENT CLIENT (COMMERCIAL ENGINE)

9.1 Objectif
Le Commercial Engine est le moteur chargé de transformer une simple recherche en une transaction aboutie.
Contrairement à un CRM traditionnel qui enregistre uniquement les échanges commerciaux, le Commercial Engine de LAWIM accompagne activement chaque utilisateur jusqu'à la réussite de son projet.
Sa mission est de coordonner :
    • les opportunités ;
    • les échanges ;
    • les visites ;
    • les négociations ;
    • les relances ;
    • les décisions ;
    • les paiements ;
    • les signatures ;
    • le suivi après transaction.
Le Commercial Engine devient le véritable gestionnaire de projet immobilier.

9.2 Philosophie
LAWIM ne cherche pas uniquement à répondre.
LAWIM accompagne.
Une conversation ne doit jamais s'arrêter parce que l'utilisateur ne répond plus.
Elle reste vivante.
Le système suit le projet jusqu'à sa conclusion.

9.3 Définition d'une opportunité
Une opportunité représente une possibilité réelle de faire progresser un projet.
Exemples :
    • un bien compatible ;
    • un partenaire disponible ;
    • une visite possible ;
    • une négociation ouverte ;
    • un paiement en attente ;
    • un document manquant ;
    • une offre à transmettre.
Chaque opportunité possède un cycle de vie.

9.4 Pipeline commercial
Le pipeline officiel est le suivant :
Prospection

↓

Qualification

↓

Recherche

↓

Matching

↓

Présentation

↓

Consentement

↓

Mise en relation

↓

Visite

↓

Retour

↓

Négociation

↓

Accord

↓

Paiement

↓

Documents

↓

Conclusion

↓

Suivi

↓

Fidélisation
Tous les Cockpits utilisent exactement ce pipeline.

9.5 Les états commerciaux
Chaque dossier possède un état commercial.
Prospect

↓

Lead qualifié

↓

Recherche active

↓

Proposition envoyée

↓

Visite planifiée

↓

Visite réalisée

↓

Négociation

↓

Accord

↓

Paiement

↓

Transaction terminée

↓

Suivi

↓

Archivé
Ces états sont indépendants des canaux.

9.6 Détection des opportunités
Le Commercial Engine détecte automatiquement :
    • un utilisateur prêt à louer ;
    • un propriétaire prêt à vendre ;
    • un investisseur actif ;
    • un partenaire disponible ;
    • un paiement imminent ;
    • un risque d'abandon.

9.7 Les prochaines actions
Chaque dossier possède une prochaine action.
Exemple :
Attendre le budget

↓

Rechercher des biens

↓

Programmer une visite

↓

Attendre le consentement

↓

Préparer un paiement

↓

Relancer le client
Il n'existe jamais de dossier sans prochaine action.

9.8 Gestion des visites
Une visite est une entité métier.
Elle possède :
    • un identifiant ;
    • une date ;
    • une heure ;
    • un lieu ;
    • un bien ;
    • un responsable ;
    • un participant ;
    • un statut.
États possibles :
Créée

↓

Confirmée

↓

Reportée

↓

Réalisée

↓

Annulée

9.9 Retour de visite
Après chaque visite.
LAWIM reprend automatiquement la conversation.
Exemple.
🤖 LAWIM AI

Bonjour.

La visite prévue aujourd'hui s'est-elle déroulée comme prévu ?
Puis.
Le bien vous convient-il ?

Souhaitez-vous poursuivre ?

9.10 Gestion des objections
Le moteur identifie automatiquement les objections.
Exemples.
    • prix trop élevé ;
    • quartier ;
    • état du bien ;
    • superficie ;
    • délai ;
    • documents ;
    • financement.
Chaque objection est historisée.

9.11 Négociation
Le Commercial Engine ouvre une négociation.
Chaque proposition contient :
    • auteur ;
    • date ;
    • montant ;
    • justification ;
    • statut.
Exemple.
Offre :

12 000 000 FCFA

↓

Contre-offre :

11 500 000 FCFA

↓

Acceptée
Toutes les versions sont conservées.

9.12 Gestion des échéances
Le moteur surveille :
    • les rendez-vous ;
    • les paiements ;
    • les signatures ;
    • les délais administratifs ;
    • les échéances contractuelles.
Chaque échéance peut déclencher une notification.

9.13 Les relances intelligentes
LAWIM ne relance jamais au hasard.
Le Planner décide :
    • faut-il relancer ?
    • quand ?
    • sur quel canal ?
    • avec quel objectif ?
Exemples.
Visite oubliée

↓

Relance
Paiement non effectué

↓

Relance
Document manquant

↓

Relance

9.14 Détection des abandons
Le moteur calcule un risque d'abandon.
Exemple.
Silence depuis 15 jours

↓

Probabilité d'abandon élevée
LAWIM adapte alors sa stratégie.

9.15 Changement de projet
Un utilisateur peut changer d'avis.
Exemple.
Studio.
↓
Appartement.
Le moteur adapte automatiquement :
    • la qualification ;
    • la recherche ;
    • le matching.
Sans perdre l'historique.

9.16 Multi-projets
Le Commercial Engine gère plusieurs projets simultanément.
Exemple.
Projet A
Location.
Projet B
Construction.
Projet C
Vente.
Chaque pipeline est indépendant.

9.17 Collaboration avec les équipes LAWIM
Le moteur peut affecter un dossier à :
    • LAWIM AI ;
    • un conseiller LAWIM ;
    • un commercial ;
    • un administrateur.
Le changement est transparent pour l'utilisateur.

9.18 Collaboration avec les partenaires
Les partenaires disposent d'une vue limitée.
Ils voient uniquement :
    • les missions qui leur sont attribuées ;
    • les informations autorisées ;
    • les actions attendues.

9.19 Historique commercial
Le moteur conserve :
    • toutes les offres ;
    • toutes les contre-offres ;
    • toutes les visites ;
    • tous les refus ;
    • toutes les validations ;
    • toutes les relances ;
    • tous les paiements.
Aucun événement commercial n'est perdu.

9.20 KPI commerciaux
Le Commercial Engine calcule notamment :
    • taux de conversion ;
    • durée moyenne d'une transaction ;
    • nombre de visites ;
    • taux de réussite des visites ;
    • taux de négociation ;
    • taux de paiement ;
    • taux d'abandon ;
    • satisfaction client ;
    • chiffre d'affaires généré.
Ces indicateurs alimentent les Cockpits.

9.21 Intégration avec Campay
Le Commercial Engine communique directement avec le Financial Engine.
Exemple.
Transaction validée

↓

Paiement Campay

↓

Confirmation

↓

Reçu

↓

Suite du workflow
Le paiement est une étape du projet.
Pas un processus isolé.

9.22 Accompagnement après transaction
Une transaction terminée ne clôture pas nécessairement la relation.
LAWIM peut ensuite proposer :
    • assistance administrative ;
    • gestion locative ;
    • rénovation ;
    • assurance ;
    • financement ;
    • nouveaux projets ;
    • programme de fidélité.
Le client reste membre de l'écosystème.

9.23 Gestion des litiges
Le moteur ouvre un dossier de litige.
Il enregistre :
    • les faits ;
    • les pièces ;
    • les intervenants ;
    • les décisions ;
    • les actions correctives.
Toutes les étapes sont historisées.

9.24 Événements produits
Le Commercial Engine publie notamment :
lead.created

lead.qualified

visit.created

visit.confirmed

visit.completed

objection.detected

negotiation.started

offer.created

offer.accepted

offer.rejected

payment.requested

payment.completed

transaction.closed

followup.created

customer.satisfied

customer.unsatisfied

9.25 Interfaces
Le Commercial Engine interagit avec :
    • Conversation Planner ;
    • Qualification Engine ;
    • Search & Matching Engine ;
    • Relationship Engine ;
    • Financial Engine ;
    • Document Engine ;
    • Notification Engine ;
    • CRM ;
    • Cockpits.
Il constitue le moteur opérationnel des transactions.

9.26 Critères de réussite
Le Commercial Engine est conforme lorsque :
    • chaque dossier possède une prochaine action ;
    • aucune opportunité n'est oubliée ;
    • les visites sont suivies ;
    • les négociations sont historisées ;
    • les paiements sont intégrés au workflow ;
    • les relances sont intelligentes ;
    • les risques d'abandon sont détectés ;
    • les équipes LAWIM et les partenaires collaborent dans un cadre sécurisé ;
    • les KPI sont calculés en temps réel ;
    • la conversation accompagne réellement l'utilisateur jusqu'à la réussite de son projet.

9.27 Vision stratégique
Le Commercial Engine ne doit jamais être perçu comme un simple CRM.
Il constitue le moteur d'exécution de LAWIM.
Son rôle est de faire passer chaque utilisateur d'une intention à une réalisation concrète, en orchestrant les interactions entre les moteurs métier, les partenaires, les équipes LAWIM et les services financiers. C'est lui qui transforme l'intelligence conversationnelle en résultats mesurables : transactions conclues, utilisateurs satisfaits, partenaires engagés et valeur créée pour l'ensemble de l'écosystème LAWIM.
LAWIM Conversation Core Master Specification
Version 1.0
PARTIE 10
LE MOTEUR FINANCIER (FINANCIAL ENGINE), LES PAIEMENTS, LA FACTURATION ET LA MONÉTISATION

10.1 Objectif
Le Financial Engine est le moteur chargé de gérer l'ensemble des flux financiers de LAWIM.
Il constitue le socle économique de la plateforme.
Son rôle ne se limite pas au paiement.
Il doit également gérer :
    • la facturation ;
    • les devis ;
    • les commissions ;
    • les abonnements ;
    • les remboursements ;
    • les répartitions financières ;
    • les revenus partenaires ;
    • les justificatifs ;
    • les audits financiers.
Toutes les opérations financières transitent exclusivement par ce moteur.

10.2 Philosophie
Dans LAWIM, le paiement n'est jamais un évènement isolé.
Il constitue une étape naturelle d'un workflow métier.
Exemple.
Recherche

↓

Matching

↓

Mise en relation

↓

Validation

↓

Paiement

↓

Suite du projet
Le paiement ne coupe jamais la conversation.
Il la fait progresser.

10.3 Intégration Campay
Campay devient le fournisseur officiel de paiement mobile.
Le moteur doit gérer :
    • MTN Mobile Money
    • Orange Money
avec la possibilité d'ajouter ultérieurement :
    • Visa
    • Mastercard
    • Stripe
    • PayPal
    • banques partenaires
sans modifier le cœur du moteur.

10.4 Architecture
Le Financial Engine pilote :
Tarification

↓

Devis

↓

Facturation

↓

Paiement

↓

Confirmation

↓

Répartition

↓

Reçu

↓

Audit

10.5 Les produits commercialisables
Le moteur doit pouvoir facturer :
Services LAWIM
    • Mise en relation
    • Recherche Premium
    • Dossier Premium
    • Accompagnement personnalisé
    • Expertise
    • Vérification documentaire
    • Estimation immobilière

Prestations partenaires
    • Honoraires
    • Études
    • Plans
    • Devis
    • Travaux
    • Visites

Produits numériques
    • Guides
    • Documents
    • Modèles
    • Formations
    • Rapports

Abonnements
    • Particulier Premium
    • Professionnel
    • Agence
    • Promoteur
    • Entreprise

10.6 Catalogue des services
Le Financial Engine ne contient jamais les prix en dur.
Les tarifs proviennent d'un catalogue dynamique.
Chaque service possède :
    • identifiant
    • nom
    • catégorie
    • description
    • prix
    • devise
    • TVA
    • conditions
    • Feature Flag
Les administrateurs peuvent modifier ce catalogue sans redéploiement.

10.7 Tarification intelligente
Le moteur peut calculer :
    • prix fixe
    • prix variable
    • pourcentage
    • abonnement
    • commission
    • tarif dégressif
    • tarif promotionnel
    • remise partenaire

10.8 Génération d'un devis
Avant un paiement.
LAWIM présente toujours.
Exemple.
Mise en relation Premium

Montant :

10 000 FCFA

Frais :

0 FCFA

Total :

10 000 FCFA
L'utilisateur valide.
Puis seulement.
↓
Paiement.

10.9 Création d'une facture
Toute prestation génère :
    • numéro unique
    • client
    • fournisseur
    • objet
    • montant
    • TVA
    • devise
    • statut
    • date
Les factures sont archivées dans la GED.

10.10 Cycle de paiement
Le workflow officiel est.
Création

↓

Validation

↓

Paiement

↓

Confirmation

↓

Reçu

↓

Comptabilisation

↓

Archivage

10.11 États d'un paiement
Créé

↓

En attente

↓

Initialisé

↓

Autorisé

↓

Confirmé

↓

Réussi

↓

Échoué

↓

Expiré

↓

Annulé

↓

Remboursé
Tous ces états sont historisés.

10.12 Idempotence
Le moteur garantit.
Une transaction.
↓
Un seul paiement.
Même si :
    • webhook reçu plusieurs fois ;
    • double clic utilisateur ;
    • reconnexion.
Aucune double facturation n'est possible.

10.13 Webhooks
Tous les webhooks Campay sont :
    • signés ;
    • vérifiés ;
    • journalisés ;
    • historisés.
Aucun webhook non authentifié n'est accepté.

10.14 Réconciliation
Le moteur compare automatiquement.
Campay
↓
LAWIM
↓
Comptabilité
Toute incohérence déclenche une alerte.

10.15 Répartition financière
Un paiement peut être réparti.
Exemple.
Client

↓

Paiement

↓

LAWIM

↓

Commission

↓

Partenaire

↓

Taxes
Le calcul est automatique.

10.16 Paiements partiels
Le moteur supporte.
    • acompte
    • solde
    • échéancier
    • paiement fractionné

10.17 Remboursements
Le moteur gère.
    • remboursement total
    • remboursement partiel
    • avoir
    • annulation
Toutes les opérations restent traçables.

10.18 Monnaies
Le moteur doit être multi-devises.
Devise principale.
FCFA.
Prévoir.
    • EUR
    • USD
    • GBP
pour les évolutions futures.

10.19 Documents financiers
Chaque opération produit.
    • facture
    • reçu
    • justificatif
    • journal
    • audit
Tous les documents sont archivés dans la GED.

10.20 Notifications
Le moteur informe automatiquement.
Paiement créé.
↓
Paiement confirmé.
↓
Paiement refusé.
↓
Paiement expiré.
↓
Paiement remboursé.

10.21 Tableau de bord financier
Le Cockpit affiche notamment.
    • chiffre d'affaires
    • paiements du jour
    • commissions
    • revenus partenaires
    • paiements échoués
    • remboursements
    • abonnements actifs
    • créances
    • prévisions

10.22 KPI financiers
Le moteur calcule.
    • chiffre d'affaires
    • panier moyen
    • taux de conversion
    • délai moyen de paiement
    • taux d'échec
    • taux de remboursement
    • revenus par service
    • revenus par partenaire
    • revenus par canal

10.23 Sécurité
Toutes les opérations sont.
    • signées
    • historisées
    • auditées
    • horodatées
Les secrets Campay ne sont jamais exposés.
Les clés sont gérées par le Secret Manager.

10.24 Intégration conversationnelle
Le Financial Engine ne dialogue jamais directement avec l'utilisateur.
Le Conversation Planner décide.
Exemple.
Projet terminé

↓

Paiement requis

↓

Conversation Planner

↓

Financial Engine

↓

Campay

↓

Confirmation

↓

Conversation reprend
Le paiement fait partie du dialogue.

10.25 Monétisation de la plateforme
Le moteur doit permettre à LAWIM de générer des revenus sur plusieurs axes.
Revenus directs
    • frais de mise en relation ;
    • abonnements ;
    • prestations LAWIM ;
    • ventes de documents ;
    • accompagnement personnalisé.

Revenus partenaires
    • commissions ;
    • abonnements professionnels ;
    • visibilité Premium ;
    • sponsoring.

Revenus futurs
    • assurances ;
    • crédits immobiliers ;
    • gestion locative ;
    • services de maintenance ;
    • fiscalité ;
    • investissement.
Le modèle économique doit rester extensible.

10.26 Feature Flags
Chaque service commercialisable possède un Feature Flag.
Exemple.
premium_matching

expert_reports

paid_documents

architect_directory

subscription_agency

construction_pack
Un administrateur peut les activer ou les désactiver sans redéploiement.

10.27 Événements produits
Le Financial Engine publie notamment.
invoice.created

invoice.sent

payment.created

payment.started

payment.authorized

payment.completed

payment.failed

payment.expired

payment.refunded

receipt.generated

commission.calculated

subscription.activated

subscription.renewed

subscription.expired

10.28 Interfaces
Le Financial Engine communique avec.
    • Conversation Planner ;
    • Commercial Engine ;
    • Relationship Engine ;
    • Campay ;
    • GED ;
    • Notification Engine ;
    • CRM ;
    • Cockpits ;
    • Reporting ;
    • Comptabilité.

10.29 Critères de réussite
Le Financial Engine est considéré comme conforme lorsque :
    • tous les paiements sont traçables ;
    • aucune double facturation n'est possible ;
    • les webhooks sont sécurisés ;
    • les factures et reçus sont générés automatiquement ;
    • les revenus sont correctement répartis ;
    • les indicateurs financiers sont disponibles en temps réel ;
    • le paiement s'intègre naturellement au parcours conversationnel ;
    • la plateforme peut faire évoluer son modèle économique sans modifier le cœur applicatif.

10.30 Vision stratégique
Le Financial Engine n'est pas un simple module de paiement.
Il constitue le moteur économique de LAWIM.
Sa mission est de transformer la valeur créée par les interactions, les mises en relation, les prestations, les partenaires et les services numériques en revenus durables, traçables et auditables. Grâce à son intégration complète avec le Conversation Core, le Commercial Engine et Campay, il garantit que chaque transaction est sécurisée, documentée et cohérente avec le parcours utilisateur.
À terme, il devra permettre à LAWIM de gérer l'ensemble de son écosystème financier, depuis la simple mise en relation jusqu'aux abonnements, aux commissions, aux prestations complexes et aux futurs services financiers intégrés, tout en restant piloté par les mêmes principes de transparence, de sécurité et de gouvernance que le reste de la plateforme.
LAWIM Conversation Core Master Specification
Version 1.0
PARTIE 11
LE MEMORY ENGINE, L'ORCHESTRATEUR MULTI-IA ET LA GOUVERNANCE DE L'INTELLIGENCE

11.1 Objectif
Le Memory Engine constitue la mémoire officielle de LAWIM.
L'AI Orchestrator constitue le répartiteur intelligent des modèles d'intelligence artificielle.
Ensemble, ils garantissent que :
    • les modèles IA restent interchangeables ;
    • aucune connaissance métier n'est perdue ;
    • toutes les conversations peuvent être reprises ;
    • la plateforme conserve une intelligence cohérente dans le temps.
Le Memory Engine est la mémoire.
L'AI Orchestrator est le répartiteur.
Le Conversation Planner reste le décideur.

11.2 Principe fondamental
La mémoire appartient exclusivement à LAWIM.
Jamais à GPT.
Jamais à Gemini.
Jamais à DeepSeek.
Jamais à un futur modèle.
Les modèles IA doivent être considérés comme sans mémoire.
Toute la mémoire doit être reconstruite avant chaque appel au LLM.

11.3 Architecture officielle
Utilisateur

↓

Conversation Core

↓

Memory Engine

↓

Conversation Planner

↓

AI Orchestrator

↓

LLM

↓

Response Policy Engine

↓

Utilisateur
Les modèles IA ne communiquent jamais directement avec la base de données.

11.4 Types de mémoire
Le Memory Engine gère plusieurs niveaux.
Mémoire utilisateur
Informations stables.
Exemples :
    • identité ;
    • langue ;
    • préférences ;
    • consentements ;
    • canaux favoris ;
    • coordonnées.

Mémoire conversationnelle
Conserve :
    • les échanges ;
    • les résumés ;
    • les intentions ;
    • les décisions.

Mémoire projet
Chaque projet possède sa mémoire.
Exemple.
Projet :
Construction.
↓
Documents.
↓
Architecte.
↓
Paiements.
↓
Visites.
↓
Historique.

Mémoire métier
Conserve.
    • règles ;
    • workflows ;
    • scores ;
    • événements ;
    • états.

Mémoire documentaire
Conserve.
    • contrats ;
    • devis ;
    • plans ;
    • pièces justificatives ;
    • guides.

11.5 Une mémoire unique
Quel que soit le canal.
WhatsApp

↓

Telegram

↓

Web

↓

Email

↓

Messenger
Tous alimentent exactement la même mémoire.
Il n'existe jamais plusieurs historiques.

11.6 Persistance obligatoire
Après chaque message.
Le système enregistre.
    • message entrant ;
    • message sortant ;
    • résumé ;
    • état courant ;
    • décision ;
    • prochaine action ;
    • moteur utilisé ;
    • modèle IA utilisé ;
    • temps de réponse ;
    • événements produits.
Aucune conversation ne disparaît.

11.7 Résumé intelligent
Les conversations longues ne sont jamais envoyées intégralement aux modèles IA.
Le Memory Engine produit automatiquement :
    • un résumé ;
    • les décisions importantes ;
    • les informations connues ;
    • les informations manquantes ;
    • la prochaine action.
Le LLM reçoit ce résumé plutôt que des centaines de messages.

11.8 Reconstruction du contexte
Avant chaque appel IA.
Le système reconstruit.
Utilisateur

+

Projet

+

Résumé

+

Workflow

+

Qualification

+

Mémoire

↓

Contexte IA
Le contexte est donc déterministe.

11.9 Gouvernance des modèles IA
Le système peut utiliser.
    • OpenAI
    • DeepSeek
    • Gemini
    • futurs modèles
Tous respectent exactement les mêmes règles métier.

11.10 AI Orchestrator
L'Orchestrateur choisit automatiquement.
    • quel modèle utiliser ;
    • quel coût accepter ;
    • quel délai maximal ;
    • quel fallback appliquer.
Le choix dépend notamment :
    • du type de tâche ;
    • de la disponibilité ;
    • du coût ;
    • des performances ;
    • des Feature Flags.

11.11 Sélection intelligente
Exemple.
Correction orthographique

↓

Modèle rapide

Analyse complexe

↓

Modèle avancé

Résumé documentaire

↓

Modèle spécialisé
Le choix reste transparent pour l'utilisateur.

11.12 Fallback automatique
Si un modèle échoue.
Le système applique automatiquement.
OpenAI

↓

DeepSeek

↓

Gemini

↓

Fallback déterministe
La conversation continue.
L'utilisateur ne doit jamais constater une panne.

11.13 Prompt Builder
Aucun prompt n'est écrit directement dans le code métier.
Le Prompt Builder assemble automatiquement.
    • persona ;
    • contexte ;
    • résumé ;
    • décisions ;
    • contraintes ;
    • style ;
    • langue.
Le prompt final est généré dynamiquement.

11.14 Les modèles ne décident jamais
Les LLM ne décident jamais :
    • du workflow ;
    • du score ;
    • du matching ;
    • des paiements ;
    • des recherches ;
    • des partenaires ;
    • des mises en relation.
Ils répondent uniquement à la demande du Planner.

11.15 Validation après génération
Une réponse IA n'est jamais envoyée directement.
Le Response Policy Engine vérifie.
    • conformité LAWIM ;
    • cohérence métier ;
    • hallucinations ;
    • plateformes externes ;
    • sécurité ;
    • ton ;
    • prochaine action.
Si la réponse échoue.
↓
Nouvelle génération.
Ou réponse déterministe.

11.16 Gestion des hallucinations
Le système compare.
Réponse IA.
↓
Mémoire.
↓
Base métier.
↓
Workflow.
Toute contradiction est signalée.
La réponse est rejetée.

11.17 Mémoire omnicanale
Exemple.
WhatsApp.
↓
Qualification.
↓
Télégram.
↓
Recherche.
↓
Web.
↓
Paiement.
↓
Cockpit.
↓
Suivi.
Le dossier reste unique.

11.18 Gestion des canaux secondaires
Chaque utilisateur peut enregistrer.
    • plusieurs numéros WhatsApp ;
    • plusieurs comptes Telegram ;
    • plusieurs adresses email.
L'un est principal.
Les autres sont secondaires.
Le Memory Engine les relie tous au même utilisateur.

11.19 Authentification
L'adresse officielle de LAWIM est :
contact@lawim.app
Elle constitue :
    • l'adresse officielle de communication ;
    • l'adresse d'authentification par email ;
    • l'adresse d'inscription ;
    • l'adresse d'envoi des notifications système.
Lors d'une inscription.
LAWIM peut envoyer une confirmation.
    • par email ;
    • par WhatsApp ;
    • par Telegram.
Selon les moyens renseignés.

11.20 Résolution d'identité
Le moteur fusionne automatiquement.
Exemple.
Même utilisateur.
↓
WhatsApp.
↓
Telegram.
↓
Email.
↓
Web.
↓
Application.
↓
Même identité.
↓
Même mémoire.
↓
Même dossier.

11.21 Confidentialité
Les modèles IA ne reçoivent jamais.
    • les secrets ;
    • les mots de passe ;
    • les clés API ;
    • les tokens ;
    • les données financières complètes ;
    • les coordonnées non autorisées.
Seules les informations nécessaires sont transmises.

11.22 Journalisation
Chaque appel IA est historisé.
Exemple.
    • modèle ;
    • version ;
    • coût ;
    • durée ;
    • tokens ;
    • succès ;
    • fallback éventuel.
Ces informations alimentent les Cockpits techniques.

11.23 Feature Flags IA
Les administrateurs peuvent activer.
Exemple.
use_openai

use_deepseek

use_gemini

enable_fallback

enable_cost_optimizer

enable_smart_routing

enable_local_llm
Sans modifier le code.

11.24 Événements produits
Le Memory Engine publie.
conversation.saved

memory.updated

summary.generated

context.rebuilt

identity.merged

history.archived
L'Orchestrateur publie.
ai.requested

ai.completed

ai.failed

ai.fallback

ai.timeout

ai.provider.changed

response.validated

11.25 Interfaces
Le Memory Engine communique avec.
    • Conversation Planner ;
    • Qualification Engine ;
    • Search Engine ;
    • Relationship Engine ;
    • Commercial Engine ;
    • Financial Engine ;
    • Document Engine ;
    • Cockpits.
L'AI Orchestrator communique avec.
    • OpenAI ;
    • DeepSeek ;
    • Gemini ;
    • futurs fournisseurs.

11.26 Critères de réussite
Le système est considéré comme conforme lorsque :
    • la mémoire est unique ;
    • tous les canaux partagent le même contexte ;
    • les modèles IA sont interchangeables ;
    • aucun modèle ne prend de décision métier ;
    • les conversations sont reprises sans perte d'information ;
    • les hallucinations sont détectées ;
    • les fallbacks fonctionnent automatiquement ;
    • les réponses sont validées avant envoi ;
    • les appels IA sont auditables ;
    • la gouvernance de l'intelligence appartient exclusivement à LAWIM.

11.27 Vision stratégique
Le Memory Engine et l'AI Orchestrator garantissent l'indépendance technologique de LAWIM.
Grâce à eux, la plateforme n'est jamais dépendante d'un fournisseur d'IA particulier. Les modèles évoluent, changent ou sont remplacés, tandis que la mémoire, les règles métier, les workflows et l'expérience utilisateur restent entièrement maîtrisés par LAWIM.
Cette architecture fait du Conversation Core un véritable système d'intelligence immobilière souverain, où l'IA est un outil au service de la plateforme, et non l'inverse.
LAWIM Conversation Core Master Specification
Version 1.0
PARTIE 12
LE RESPONSE POLICY ENGINE, LE FEATURE MANAGEMENT FRAMEWORK, LES TESTS ET LA PRÉPARATION À LA MISE EN PRODUCTION

12.1 Objectif
Cette dernière partie définit les règles qui garantissent que LAWIM reste conforme à sa philosophie, quel que soit :
    • le canal utilisé ;
    • le modèle d'IA utilisé ;
    • le service activé ;
    • le partenaire impliqué ;
    • la version déployée.
Elle constitue la couche de gouvernance finale de la plateforme.
Le Response Policy Engine devient le dernier rempart avant l'envoi d'une réponse.
Le Feature Management Framework devient le mécanisme officiel d'activation des fonctionnalités.

12.2 Le Response Policy Engine
Aucune réponse produite par une IA n'est envoyée directement à l'utilisateur.
Le Response Policy Engine contrôle systématiquement chaque réponse.
Pipeline officiel :
Conversation Planner

↓

LLM

↓

Response Policy Engine

↓

Validation

↓

Utilisateur

12.3 Contrôles obligatoires
Avant l'envoi d'une réponse, le moteur vérifie notamment :
    • conformité avec la persona LAWIM ;
    • cohérence avec le dossier actif ;
    • cohérence avec le workflow ;
    • cohérence avec les informations mémorisées ;
    • respect des règles métier ;
    • respect des Feature Flags ;
    • respect des consentements ;
    • respect de la confidentialité ;
    • absence d'informations interdites ;
    • présence d'une prochaine action.

12.4 Réponses interdites
Le moteur doit automatiquement rejeter les réponses contenant notamment :
Consulte Airbnb.
Consulte Facebook Marketplace.
Consulte Booking.
Consulte Jumia House.
Cherchez sur Internet.
Contactez une agence immobilière.
Je suis un assistant IA.
Je peux seulement donner des conseils.
Je ne propose pas ce service.
Je ne peux pas vous aider.
Contactez un professionnel.
Si LAWIM possède une fonctionnalité permettant de traiter la demande, celle-ci doit toujours être privilégiée.

12.5 Hallucinations
Le moteur vérifie que la réponse ne contient pas :
    • un bien inexistant ;
    • un partenaire inexistant ;
    • un paiement inexistant ;
    • une disponibilité inventée ;
    • un document non vérifié ;
    • une promesse impossible à tenir.
Si une information ne peut être confirmée, LAWIM doit clairement l'indiquer.

12.6 Vérification métier
Avant validation, le moteur contrôle que :
    • le projet est cohérent ;
    • la prochaine action est logique ;
    • la réponse fait progresser le dossier ;
    • aucune étape obligatoire n'est ignorée.
Une réponse qui ne fait pas progresser le projet est rejetée.

12.7 Vérification conversationnelle
Le moteur contrôle également :
    • une seule question à la fois ;
    • ton professionnel ;
    • langage naturel ;
    • absence de répétition ;
    • résumé lorsque nécessaire ;
    • annonce claire de la prochaine étape.

12.8 Vérification omnicanale
Le contenu métier est identique sur :
    • Web ;
    • WhatsApp ;
    • Telegram ;
    • Messenger ;
    • Instagram ;
    • Email.
Seule la présentation varie.
Exemple :
WhatsApp :
message court.
Web :
fiche détaillée.
Telegram :
boutons.
Le fond reste identique.

12.9 Identification des intervenants
Toutes les conversations doivent clairement indiquer l'auteur des messages.
Exemple.
🤖 LAWIM AI

Bonjour.
🏠 Marie Ndzi
Agent immobilier
⚖️ Maître Jean Essomba
Notaire
🏗️ Pierre Ndzi
Architecte
👤 Client
L'utilisateur ne doit jamais douter de l'identité de son interlocuteur.

12.10 Avertissement IA
Lorsque cela est pertinent, LAWIM rappelle avec transparence :
Certaines réponses sont générées avec l'assistance de l'intelligence artificielle. Malgré les contrôles effectués, des erreurs restent possibles. Pour toute décision juridique, financière ou technique importante, nous vous recommandons de vérifier les informations auprès d'un professionnel compétent.
Cet avertissement ne doit pas apparaître à chaque réponse.
Il est affiché uniquement lorsque le contexte le justifie.

12.11 Feature Management Framework
Toutes les fonctionnalités de LAWIM sont pilotées par des Feature Flags.
Aucune fonctionnalité ne doit être supprimée.
Elle peut simplement être désactivée.

12.12 Principe
Chaque module possède un Feature Flag.
Exemple.
conversation_core

relationship_engine

financial_engine

campay

document_center

partner_directory

legal_library

construction_module

investment_module

insurance_module

credit_module

marketplace

smart_matching

ai_assistant

premium_matching

professional_directory

notifications

email

whatsapp

telegram

messenger

instagram

12.13 Administration
Le Cockpit Administrateur doit permettre :
    • d'activer une fonctionnalité ;
    • de la désactiver ;
    • de planifier son activation ;
    • de définir les profils autorisés ;
    • de suivre son utilisation.
Aucun redéploiement n'est nécessaire.

12.14 Activation par environnement
Les Feature Flags peuvent varier selon :
    • développement ;
    • recette ;
    • préproduction ;
    • production.
Exemple.
Campay DEV

↓

Actif

Campay PROD

↓

Inactif

12.15 Activation par profil
Une fonctionnalité peut être réservée à :
    • administrateurs ;
    • équipes LAWIM ;
    • partenaires ;
    • agences ;
    • utilisateurs Premium ;
    • bêta-testeurs.

12.16 Observabilité
Tous les moteurs produisent des métriques.
Le Cockpit affiche notamment :
    • nombre de conversations ;
    • temps moyen de réponse ;
    • recherches ;
    • matching ;
    • mises en relation ;
    • paiements ;
    • revenus ;
    • erreurs ;
    • fallbacks IA ;
    • coût des modèles IA.

12.17 Journal d'audit
Toutes les décisions importantes sont historisées.
Exemples.
    • activation d'un Feature Flag ;
    • changement de workflow ;
    • paiement ;
    • suppression ;
    • validation ;
    • mise en relation.
Chaque événement possède :
    • auteur ;
    • date ;
    • origine ;
    • justification.

12.18 Tests obligatoires
Avant toute mise en production, les tests suivants doivent être exécutés.
Tests unitaires
Tous les moteurs.

Tests d'intégration
Communication entre moteurs.

Tests conversationnels
Location.
Vente.
Construction.
Investissement.
Documentation.
Paiement.

Tests omnicanaux
Même conversation.
WhatsApp.
↓
Telegram.
↓
Web.
↓
Cockpit.

Tests IA
OpenAI.
↓
DeepSeek.
↓
Gemini.
↓
Fallback.
Les résultats métier doivent rester identiques.

Tests Campay
    • sandbox ;
    • production ;
    • webhooks ;
    • idempotence ;
    • remboursements.

Tests de sécurité
    • authentification ;
    • autorisations ;
    • secrets ;
    • injections ;
    • fraude.

Tests de performance
    • montée en charge ;
    • temps de réponse ;
    • disponibilité.

12.19 Critères de validation
LAWIM est considéré comme prêt lorsque :
    • Conversation Core unique ;
    • Planner opérationnel ;
    • Memory Engine partagé ;
    • Orchestrateur IA opérationnel ;
    • Feature Management Framework actif ;
    • Campay validé ;
    • omnicanal validé ;
    • Cockpits validés ;
    • Documentation validée ;
    • Tests validés ;
    • Build production valide ;
    • Déploiement validé.

12.20 Déploiement
Le pipeline officiel est :
Développement

↓

Tests unitaires

↓

Tests d'intégration

↓

Tests conversationnels

↓

Validation fonctionnelle

↓

Préproduction

↓

Production

↓

Monitoring
Aucune mise en production ne peut contourner ce processus.

12.21 Gouvernance documentaire
Toute évolution de LAWIM doit être accompagnée de :
    • la mise à jour de cette spécification ;
    • la mise à jour de la documentation technique ;
    • la mise à jour des API ;
    • la mise à jour des tests ;
    • la mise à jour des Cockpits si nécessaire.
La documentation est considérée comme une composante du produit.

12.22 Vision finale
À l'issue de cette spécification, LAWIM ne doit plus être considéré comme un chatbot enrichi.
Il devient une plateforme immobilière intelligente, omnicanale et pilotée par un moteur conversationnel souverain.
Le Conversation Core constitue désormais l'unique cerveau métier de la plateforme.
Les modèles d'intelligence artificielle (OpenAI, DeepSeek, Gemini ou futurs fournisseurs) deviennent des composants d'exécution linguistique, entièrement gouvernés par les règles de LAWIM.
Toutes les décisions — qualification, recherche, matching, mise en relation, accompagnement, transactions, paiements, documentation et suivi — appartiennent exclusivement au code métier de LAWIM.
Cette architecture garantit :
    • une expérience utilisateur cohérente sur tous les canaux ;
    • une indépendance vis-à-vis des fournisseurs d'IA ;
    • une gouvernance centralisée des décisions ;
    • une évolutivité par Feature Flags ;
    • une traçabilité complète des opérations ;
    • une sécurité renforcée ;
    • un modèle économique extensible.
Cette spécification devient la référence officielle du développement du Conversation Core de LAWIM. Toute nouvelle fonctionnalité, toute évolution technique ou métier et toute intervention sur le système conversationnel devront être conformes aux principes, aux architectures et aux règles définis dans ce document.
Je pense qu'il manque une dernière partie qui est, à mon avis, essentielle. Les 12 premières parties décrivent parfaitement comment fonctionne le Conversation Core, mais elles ne répondent pas complètement à une question fondamentale :
Comment développe-t-on désormais LAWIM sans casser cette architecture ?
Autrement dit, il manque une constitution du développement.
C'est cette partie qui empêchera, dans six mois ou dans deux ans, un développeur (ou une IA) de réintroduire un chatbot généraliste ou une logique parallèle.
Je proposerais donc une Partie 13, qui deviendra la référence absolue pour tous les futurs développements.

LAWIM Conversation Core Master Specification
Version 1.0
PARTIE 13
GOUVERNANCE DU DÉVELOPPEMENT, RÈGLES D'ÉVOLUTION ET CONSTITUTION TECHNIQUE DE LAWIM

13.1 Objet
Cette partie constitue la Constitution Technique de LAWIM.
Elle définit les règles auxquelles devront se conformer tous les développements futurs.
Aucune évolution de LAWIM ne peut être réalisée en contradiction avec cette constitution.
Elle s'impose :
    • aux développeurs ;
    • aux architectes ;
    • aux intégrateurs ;
    • aux partenaires ;
    • aux intelligences artificielles (Codex, ChatGPT, Claude Code, Gemini, etc.) utilisées pour développer le projet.

13.2 Le Conversation Core est le cerveau unique
À compter de cette version, le Conversation Core devient l'unique point d'entrée logique de la plateforme.
Il est interdit de développer :
    • un second moteur conversationnel ;
    • une logique spécifique à un canal ;
    • un chatbot indépendant ;
    • une logique métier embarquée dans un contrôleur ;
    • une décision métier directement dans un prompt IA.
Toute nouvelle fonctionnalité doit obligatoirement passer par le Conversation Core.

13.3 Les moteurs métier sont les seules autorités
Chaque domaine fonctionnel appartient à un moteur spécialisé.
Domaine
Autorité
Conversation
Conversation Core
Qualification
Qualification Engine
Recherche
Search Engine
Correspondance
Matching Engine
Mise en relation
Relationship Engine
Commerce
Commercial Engine
Paiement
Financial Engine
Documents
Document Engine
Mémoire
Memory Engine
IA
AI Orchestrator
Gouvernance
Response Policy Engine
Activation
Feature Management Framework
Aucun autre composant ne peut implémenter une logique concurrente.

13.4 Principe "Single Source of Truth"
Une information ne possède qu'une seule source officielle.
Exemples :
    • l'identité utilisateur appartient au Memory Engine ;
    • le statut d'un dossier appartient au Workflow Engine ;
    • les paiements appartiennent au Financial Engine ;
    • les conversations appartiennent au Conversation Core ;
    • les partenaires appartiennent au Relationship Engine.
Toute duplication est interdite.

13.5 Principe "Configuration plutôt que code"
Tout ce qui peut être configuré ne doit pas être codé en dur.
Exemples :
    • tarifs ;
    • workflows ;
    • types de biens ;
    • catégories de partenaires ;
    • types de documents ;
    • règles de qualification ;
    • Feature Flags ;
    • modèles IA ;
    • paramètres de relance.

13.6 Principe "Feature Flag First"
Toute nouvelle fonctionnalité est développée derrière un Feature Flag.
Cycle officiel :
Développement

↓

Tests

↓

Feature Flag OFF

↓

Validation interne

↓

Feature Flag ON (bêta)

↓

Validation

↓

Production
Une fonctionnalité n'est jamais supprimée ; elle peut simplement être désactivée.

13.7 Compatibilité ascendante
Toute évolution doit préserver :
    • les API publiques ;
    • les conversations existantes ;
    • les dossiers en cours ;
    • les identifiants ;
    • les historiques.
Une migration est obligatoire lorsque la compatibilité ne peut être garantie.

13.8 Documentation obligatoire
Aucun développement n'est considéré comme terminé sans :
    • documentation technique ;
    • documentation fonctionnelle ;
    • mise à jour de cette spécification ;
    • tests ;
    • rapport de livraison.
La documentation fait partie du livrable.

13.9 Tests obligatoires
Toute évolution doit être accompagnée de :
    • tests unitaires ;
    • tests d'intégration ;
    • tests conversationnels ;
    • tests omnicanaux ;
    • tests de non-régression.
Une fonctionnalité sans tests est considérée comme incomplète.

13.10 Interdictions
Il est interdit :
    • d'appeler directement un LLM depuis un contrôleur ;
    • d'accéder directement à Campay sans le Financial Engine ;
    • d'envoyer un message sans passer par le Conversation Core ;
    • d'écrire une logique métier dans un prompt ;
    • de recommander des plateformes concurrentes lorsque LAWIM peut traiter la demande ;
    • de stocker des secrets dans le code ;
    • de contourner le Response Policy Engine.

13.11 Développement assisté par IA
Les assistants de développement (Codex, ChatGPT, Claude Code, Gemini, etc.) doivent respecter les règles suivantes :
    • ne jamais créer de logique métier parallèle ;
    • réutiliser les moteurs existants avant d'en créer de nouveaux ;
    • rechercher les composants existants avant toute implémentation ;
    • préserver la cohérence architecturale ;
    • documenter toute nouvelle interface.
Les IA sont des assistants de développement, pas des architectes de la plateforme.

13.12 Gestion des migrations
Toute évolution impactant les données doit fournir :
    • un script de migration ;
    • un script de retour arrière lorsque cela est possible ;
    • des tests de migration ;
    • une documentation de migration.

13.13 Critères d'acceptation d'une nouvelle fonctionnalité
Une fonctionnalité est acceptée uniquement si :
    • elle respecte l'architecture du Conversation Core ;
    • elle utilise les moteurs métier existants ;
    • elle est pilotée par un Feature Flag ;
    • elle est documentée ;
    • elle est testée ;
    • elle est intégrée aux Cockpits si nécessaire ;
    • elle est compatible avec l'omnicanal ;
    • elle est compatible avec le système de mémoire partagé ;
    • elle est compatible avec l'orchestrateur multi-IA.

13.14 Vision à long terme
LAWIM est conçu comme une plateforme intelligente modulaire, et non comme un assemblage de fonctionnalités.
Chaque nouveau service — immobilier, juridique, financier, documentaire ou autre — devra s'intégrer dans cette architecture sans remettre en cause les principes fondateurs définis dans cette spécification.
Cette constitution garantit que LAWIM pourra évoluer pendant de nombreuses années tout en conservant une architecture cohérente, maintenable, testable et indépendante des technologies ou des fournisseurs d'IA du moment.

13.15 Clause finale
La présente spécification constitue la référence architecturale officielle de LAWIM.
En cas de contradiction entre une implémentation, un prompt de développement, une documentation ou une évolution future, les principes définis dans cette spécification prévalent.
Toute proposition d'évolution devra démontrer explicitement sa conformité à cette architecture ou, si elle nécessite une évolution de celle-ci, faire l'objet d'une révision formelle de cette spécification avant son implémentation.
Ainsi, LAWIM conserve un développement maîtrisé, une gouvernance claire et une cohérence fonctionnelle durable, indépendamment des équipes, des technologies ou des modèles d'intelligence artificielle utilisés au fil du temps.
LAWIM Conversation Core Master Specification
Version 1.0
PARTIE 14
L'ADMINISTRATION DE LA PLATEFORME, LES COCKPITS ET LA GOUVERNANCE OPÉRATIONNELLE

14.1 Objectif
Cette partie définit la gouvernance quotidienne de LAWIM.
Une fois la plateforme en production, son fonctionnement ne repose plus uniquement sur le code, mais également sur sa capacité à être administrée, supervisée, configurée et pilotée sans redéploiement.
Le Cockpit Administrateur devient le centre de contrôle unique de LAWIM.
Toutes les opérations d'administration doivent être réalisables depuis les Cockpits.

14.2 Principe fondamental
Le code ne doit jamais être modifié pour :
    • changer un tarif ; 
    • activer une fonctionnalité ; 
    • modifier un workflow ; 
    • ajouter un partenaire ; 
    • modifier une catégorie ; 
    • créer un nouveau document ; 
    • changer un texte ; 
    • modifier une règle métier configurable. 
Tout cela doit être administrable.

14.3 Les Cockpits
LAWIM comporte plusieurs Cockpits spécialisés.
Cockpit Super Administrateur
Responsabilités :
    • gestion globale ; 
    • configuration ; 
    • sécurité ; 
    • Feature Flags ; 
    • utilisateurs ; 
    • IA ; 
    • supervision. 

Cockpit Commercial
Responsabilités :
    • prospects ; 
    • transactions ; 
    • pipeline ; 
    • relances ; 
    • visites. 

Cockpit Immobilier
Responsabilités :
    • biens ; 
    • propriétaires ; 
    • annonces ; 
    • disponibilité. 

Cockpit Partenaires
Responsabilités :
    • architectes ; 
    • notaires ; 
    • entreprises ; 
    • agences ; 
    • investisseurs. 

Cockpit Financier
Responsabilités :
    • Campay ; 
    • paiements ; 
    • factures ; 
    • commissions ; 
    • abonnements. 

Cockpit Documentation
Responsabilités :
    • guides ; 
    • FAQ ; 
    • procédures ; 
    • modèles ; 
    • GED. 

Cockpit IA
Responsabilités :
    • orchestrateur ; 
    • coûts ; 
    • performances ; 
    • prompts ; 
    • mémoire ; 
    • statistiques IA. 

Cockpit Technique
Responsabilités :
    • santé de la plateforme ; 
    • sauvegardes ; 
    • Disaster Recovery ; 
    • logs ; 
    • monitoring ; 
    • déploiements. 

14.4 Administration des utilisateurs
Le Cockpit doit permettre :
    • création ; 
    • suspension ; 
    • réactivation ; 
    • suppression logique ; 
    • fusion de comptes ; 
    • gestion des rôles ; 
    • historique des connexions ; 
    • gestion des canaux. 

14.5 Gestion des rôles
LAWIM repose sur un contrôle d'accès par rôles (RBAC), extensible si nécessaire vers des permissions plus fines.
Rôles principaux :
    • Super Administrateur ; 
    • Administrateur ; 
    • Responsable Commercial ; 
    • Conseiller LAWIM ; 
    • Agent immobilier ; 
    • Partenaire ; 
    • Architecte ; 
    • Notaire ; 
    • Entreprise ; 
    • Client ; 
    • Visiteur. 
Chaque rôle possède :
    • permissions ; 
    • menus ; 
    • Feature Flags ; 
    • workflows autorisés. 

14.6 Administration des Feature Flags
Le Cockpit affiche tous les Feature Flags.
Pour chacun :
    • état ; 
    • description ; 
    • version ; 
    • date d'activation ; 
    • administrateur responsable ; 
    • environnement ; 
    • impact métier. 

14.7 Gestion des partenaires
Le Cockpit permet :
    • création ; 
    • validation ; 
    • suspension ; 
    • archivage ; 
    • vérification documentaire ; 
    • notation ; 
    • certification. 

14.8 Gestion des contenus
Les administrateurs peuvent publier :
    • documents juridiques ; 
    • guides ; 
    • procédures ; 
    • modèles ; 
    • actualités ; 
    • annonces institutionnelles. 
Le contenu est versionné.

14.9 Observabilité
Tous les moteurs remontent leurs indicateurs.
Le Cockpit affiche notamment :
    • conversations actives ; 
    • dossiers ouverts ; 
    • recherches ; 
    • mises en relation ; 
    • paiements ; 
    • coûts IA ; 
    • erreurs ; 
    • temps de réponse ; 
    • disponibilité ; 
    • taux de conversion. 

14.10 Santé de la plateforme
Le Cockpit doit présenter une vue temps réel des composants :
    • API ; 
    • PostgreSQL ; 
    • Redis ; 
    • Campay ; 
    • Green API ; 
    • Telegram ; 
    • Email ; 
    • IA ; 
    • sauvegardes ; 
    • Disaster Recovery. 
Chaque service possède :
    • statut ; 
    • disponibilité ; 
    • latence ; 
    • dernière erreur. 

14.11 Gouvernance des IA
Le Cockpit IA permet notamment :
    • d'activer ou désactiver un fournisseur ; 
    • de modifier les priorités (OpenAI, DeepSeek, Gemini, etc.) ; 
    • de suivre les coûts par fournisseur ; 
    • de visualiser les taux de fallback ; 
    • de consulter les performances ; 
    • de suivre les temps de réponse. 

14.12 Audit
Toutes les actions d'administration sont historisées.
Chaque événement contient :
    • utilisateur ; 
    • rôle ; 
    • date ; 
    • adresse IP (si disponible) ; 
    • action ; 
    • ancienne valeur ; 
    • nouvelle valeur ; 
    • justification éventuelle. 
Les journaux d'audit sont inaltérables.

14.13 Supervision des workflows
Le Cockpit permet de visualiser :
    • le pipeline des dossiers ; 
    • les blocages ; 
    • les retards ; 
    • les étapes en attente ; 
    • les relances automatiques ; 
    • les erreurs métier. 

14.14 Administration documentaire
Le Cockpit permet de gérer :
    • la bibliothèque documentaire ; 
    • les catégories ; 
    • les versions ; 
    • les langues ; 
    • les droits d'accès ; 
    • les dates de publication ; 
    • les dates d'expiration. 

14.15 Sauvegardes et reprise
Le Cockpit Technique centralise :
    • les sauvegardes ; 
    • les Recovery Bundles ; 
    • les tests de restauration ; 
    • les indicateurs RPO/RTO ; 
    • le Recovery Readiness Score ; 
    • les historiques d'exécution. 

14.16 Gouvernance des déploiements
Chaque déploiement est enregistré avec :
    • version ; 
    • commit Git ; 
    • tag ; 
    • environnement ; 
    • date ; 
    • responsable ; 
    • résultats des tests ; 
    • validations ; 
    • possibilité de retour arrière (rollback). 

14.17 KPI de gouvernance
Le Cockpit fournit notamment :
    • disponibilité de la plateforme ; 
    • nombre d'utilisateurs actifs ; 
    • taux de conversion ; 
    • temps moyen de qualification ; 
    • temps moyen jusqu'à la mise en relation ; 
    • temps moyen jusqu'au paiement ; 
    • satisfaction des utilisateurs ; 
    • satisfaction des partenaires ; 
    • coût moyen par conversation IA ; 
    • revenus par service ; 
    • revenus par partenaire. 

14.18 Vision stratégique
Le Cockpit Administrateur n'est pas un simple panneau de configuration.
Il constitue le centre de pilotage de LAWIM.
À partir d'un seul environnement, les administrateurs doivent pouvoir superviser les opérations, gouverner les fonctionnalités, suivre les performances, contrôler les coûts, administrer les partenaires, assurer la conformité réglementaire, piloter les déploiements et garantir la qualité de service.
Cette gouvernance opérationnelle complète l'architecture définie dans les parties précédentes et permet à LAWIM d'évoluer comme une plateforme professionnelle, administrable et scalable, sans dépendre d'interventions techniques pour les opérations courantes.

