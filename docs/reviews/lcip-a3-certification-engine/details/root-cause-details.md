# Root Cause Engine Details — LCIP A.3

## Fichier créé

`tests/gold_corpus/certification/diagnostics/root_cause_engine.py`

## COMPONENT_MAP

31 entrées mappant chaque assertion au composant responsable :

| Composant | Assertions |
|-----------|------------|
| ConversationJourneyOrchestrator | BIZ-0001, BIZ-0002, BIZ-0003, INT-0002, STATE-0001, STATE-0002 |
| ConversationStateService | MEM-0001, MEM-0002, MEM-0005, MEM-0007, IDEM-0001 |
| QualificationService | QLF-0001, QLF-0003, STATE-0003 |
| ConversationResponseValidator | LANG-0004, QST-0001, QST-0003 |
| ProviderOrchestrator | RUNTIME-0001, RUNTIME-0002 |
| ProgramFEngineAdapter | INT-0001, MEM-0003 |
| ... | ... |

## Fonctions

- `get_component()` : retourne le composant et la confiance pour une assertion
- `analyze_root_causes()` : analyse toutes les causes racines d'une liste de violations
- `build_component_summary()` : résume les violations par composant

## Contrôle

RCA-0001 : PASS
