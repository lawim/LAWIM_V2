# CONVERSATION SCORE — Heritage Gold Readiness

**Audité par :** Conversation Expert (H0.3)
**Date :** 2026-07-15

## Score global : 44/100

## Sous-dimensions

| # | Dimension | Score | Justification |
|---|-----------|:-----:|---------------|
| 1 | **Conversation flows** | 45 | 4 intents corrects mais pas de machine à états conversationnelle. Les flows séquentiels (ask_city→ask_neighborhood→...) sont purement conceptuels — le code ne contient que des réponses statiques. |
| 2 | **Memory management** | 55 | Champs court-terme corrects. Récupération Supabase long-terme OK. Historique tronqué à 50 entrées. Manque dans Gold : classification du type d'historique, génération de résumé naturel. Manque dans code : favorite_locations, investment_preferences documentés mais absents. |
| 3 | **Follow-up/relance** | 75 | Excellent alignement J1/J7/J30/J90 avec follow_up_system.py. Messages proches du code. Manque : table follow_ups, déduplication sent_hours. |
| 4 | **Objection handling** | 10 | **Gap critique.** 23 patterns documentés dans Gold mais ZÉRO implémentation dans le code. Aucune détection, catégorisation ou réponse aux objections. |
| 5 | **Escalation rules** | 5 | **Gap critique.** 5 conditions d'escalade documentées mais ZÉRO implémentation. Aucun routeur d'escalade, aucune redirection notaire, aucun handler SIGNALER. |
| 6 | **Humanization** | 60 | Gold documente les principes. Le code est plus riche (4 niveaux × 4 phrases d'accueil, 6 résumés, 6 transitions, 5 questions avec sélection aléatoire). Gold sous-documente la richesse réelle. |
| 7 | **Behavioral tracking** | 20 | Gold définit 8 événements de traçabilité. Aucun système d'événements structuré n'existe dans le code. Pas d'event emitter, pas de module d'audit. |
| 8 | **Response templates** | 65 | 7 templates sur 8 vérifiés (language_changed absent de multilingual_responses.py). Templates dupliqués sur 4 fichiers avec couverture inégale du Pidgin. Manque : format_property_response(). |
| 9 | **Channel-specific rules** | 30 | WhatsApp comme canal principal OK. Aucune logique canal-spécifique pour Telegram, Facebook, SMS, appel vocal. Les règles élaborées du Gold n'ont pas d'implémentation. |
| 10 | **Language handling** | 70 | Hiérarchie de détection correcte (DeepSeek→Gemini→Local). 3 langues OK. Commande LANGUE OK. Incohérence : language_handler.py ne supporte que FR/EN (pas Pidgin). |

## Forces

- Follow-up/relance bien documenté et aligné avec le code
- Langue : pipeline de détection et templates multilingues
- Humanisation : principes corrects même si sous-détaillés

## Faiblesses critiques

- Objection handling (10/100) : rien n'est implémenté
- Escalade (5/100) : rien n'est implémenté
- Behavioral tracking (20/100) : pas de système d'événements
- Channel-specific (30/100) : les règles n'existent que dans le Gold

## Conclusion

Le Gold surévalue les capacités de la conversation LAWIM. Les flows multi-étapes, les objections et les escalades sont documentés comme existants mais n'ont aucune implémentation. Sans ces éléments, LAWIM_V2 ne peut pas reproduire les interactions documentées.
