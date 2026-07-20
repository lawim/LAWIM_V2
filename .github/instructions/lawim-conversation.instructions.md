---
applyTo: "code/lawim_v2/communication/**/*.py,code/lawim_v2/conversation/**/*.py,code/lawim_v2/knowledge_runtime/**/*.py,tests/test_conversation*.py,tests/test_*whatsapp*.py,tests/test_*telegram*.py,frontend/**/*conversation*,frontend/**/*chat*"
---

# LAWIM — Contrat du module conversationnel

La chaîne canonique est :

message entrant
→ normalisation
→ acteur
→ conversation
→ état persistant
→ langue
→ intention
→ extraction des critères
→ fusion
→ qualification
→ ProgressiveWizard
→ prochaine action
→ ResponsePlan
→ formulation
→ ResponseValidator
→ renderer
→ persistance
→ livraison

Interdictions :

- aucun chemin direct message → LLM ;
- aucune réponse générale d’assistant neutre ;
- aucun refus d’agir pour LAWIM ;
- aucune redirection immobilière externe ;
- aucune traduction non demandée ;
- aucune correction grammaticale non demandée ;
- aucun changement de langue non demandé ;
- aucune deuxième question ;
- aucun critère connu redemandé ;
- aucune exigence facultative suggérée prématurément ;
- aucun handover automatique sans objet persistant.

Priorité d’interprétation :

1. conversation active ;
2. dernière question ;
3. intention métier ;
4. vocabulaire immobilier LAWIM ;
5. interprétation générale seulement en dernier recours.

Exemples obligatoires :

- studio → logement studio ;
- studio meublé → property_type=studio, furnished=true ;
- pour habitation → property_usage=residential ;
- Akwa dans une recherche à Douala → district=Akwa ;
- 180 000 FCFA après une question de budget → budget_xaf=180000 ;
- je ne comprends pas → reformuler la dernière question ;
- I don't understand English dans une conversation française → continuer en français.

Tout tour doit produire un ResponsePlan avant tout appel à un fournisseur IA.
