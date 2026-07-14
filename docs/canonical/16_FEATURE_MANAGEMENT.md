# Feature Management

Version: 1.0
Date: 2026-07-14
Commit de reference: d30d61e1d89427ece9c180cec4639cce77fdcba3
Statut: CANONICAL

## Regles
Tout module majeur doit etre desactivable par Feature Flag global, sous-flag, environnement, profil, beta ou kill switch.

## Flags canoniques minimaux
| Flag | Domaine | Defaut reconstruction | Role |
| --- | --- | --- | --- |
| `LAWIM_FEATURE_CONVERSATION_V2` | Conversation | off | Active le nouveau runtime conversationnel. |
| `LAWIM_FEATURE_QUALIFICATION_V2` | Qualification | off | Active matrices executables. |
| `LAWIM_FEATURE_SEARCH_V2` | Search | off | Active orchestration search cible. |
| `LAWIM_FEATURE_MATCHING_V2` | Matching | off | Active scoring cible. |
| `LAWIM_FEATURE_RELATIONSHIP_V2` | Relationship | off | Active consentement et introduction cible. |
| `LAWIM_FEATURE_VISITS_CONVERSATION` | Visits | off | Autorise visites depuis Conversation cible. |
| `LAWIM_FEATURE_FINANCIAL_CORE` | Financial Core | on controle | Active le coeur financier. |
| `LAWIM_FEATURE_CAMPAY` | Campay | off par defaut | Active le connecteur Campay. |
| `AI_ORCHESTRATOR_ENABLED` | AI | off par defaut | Active les fournisseurs IA externes. |

## Audit et rollout
Chaque changement de flag produit AuditEvent avec acteur, raison, ancien et nouveau statut. Les activations progressives doivent definir environnement, population, date, rollback et test attendu.
