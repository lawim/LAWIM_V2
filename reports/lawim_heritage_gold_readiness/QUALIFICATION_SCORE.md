# QUALIFICATION SCORE — Heritage Gold Readiness

**Audité par :** Qualification Expert (H0.3)
**Date :** 2026-07-15

## Score global : 56/100

## Sous-dimensions

| # | Dimension | Score | Justification |
|---|-----------|:-----:|---------------|
| 1 | **Profiles and roles** | 100 | 5 rôles avec scores de base et mapping intents parfaitement alignés avec lead_classifier_v1.json. |
| 2 | **Scoring matrices** | 70 | Boosters et pénalités OK (6+3 signaux). CRM V5 (7 facteurs avec poids) non vérifiable — aucune source ne correspond. |
| 3 | **Rules (pipeline, thresholds)** | 50 | Seuils V1 OK (≥80/60/40). Seuils V5 et pipeline 8 étapes non vérifiables dans les sources. |
| 4 | **Readiness criteria (min fields)** | 60 | Structure obligatoire/recommandée/optionnelle OK. Mais transaction et quartier manquent comme champs obligatoires dans le Gold. |
| 5 | **Mandatory vs optional** | 75 | Ordre qualification 10 étapes correct. Règles de formulation (1 question/message) OK. Stop criteria non sourcés directement. |
| 6 | **Escalation rules** | 50 | 3 types d'escalade corrects mais simplifiés par rapport aux 12+ déclencheurs réels dans les sources. |
| 7 | **Anti-fraud detection** | 25 | 4 couches documentées mais 3 sur 4 n'ont aucune implémentation. Seul broker_spam (-50) est vérifié. |
| 8 | **Agent network** | 20 | Opt-in et rating quasiment absents du Gold alors qu'ils existent dans le code (agent_optin.py, agent_rating.py). |

## Forces

- Rôles et mapping intents : parfaits
- Boosters et pénalités : valeurs exactes
- Seuils V1 : alignés
- Ordre qualification : correct

## Faiblesses critiques

- CRM V5 : non vérifiable (7 facteurs avec poids non trouvés dans les sources)
- Pipeline 8 étapes : non vérifiable
- Anti-fraude : 75% des couches sans implémentation
- Agent network : quasiment absent du Gold
- Champs manquants : transaction et quartier comme obligatoires

## Conclusion

La qualification est correcte sur les concepts de base (rôles, scores V1) mais insuffisante sur les détails d'implémentation (pipeline, anti-fraude, réseau d'agents). LAWIM_V2 pourrait reconstruire le scoring de base mais pas le pipeline CRM complet.
