# Restart B000083 Details — LCIP B.4R-F

## Dialogue

| Turn | Role | Text |
|:----:|------|------|
| 0 | user | Je cherche un appartement a louer a Yaounde. |
| 1 | assistant | Quel budget mensuel ? |
| 2 | user | 180 000 FCFA. |
| 3 | assistant | Combien de chambres ? |
| 4 | user | Deux chambres. |
| **5** | **system** | **SERVICE_RESTART** |
| 6 | user | Je prefere Melen ou Ngoa-Ekelle. |
| 7 | assistant | A partir de quand souhaitez-vous emmenager ? |
| 8 | user | En septembre. |
| 9 | assistant | Souhaitez-vous enregistrer cette recherche ? |
| 10 | user | Oui. |
| 11 | assistant | La recherche a ete enregistree. |

## Restart Processing

1. Turn 0-4 executed normally (facts: Yaounde, 180000, 2 bedrooms)
2. Turn 5 detected as SERVICE_RESTART
3. State captured from SQLite before restart
4. New ProgramFEngineAdapter created (same DB)
5. New ConversationJourneyOrchestrator created
6. Turn 6-11 executed normally with new runtime
7. Business object created at end: unique

## State Persistence

- Facts before: city=Yaounde, budget_max=180000, bedrooms=2
- Facts after restart: preserved (area added: Melen/Ngoa-Ekelle)
- Everything completed successfully
- Business object: unique (1 object)
