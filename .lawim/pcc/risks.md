# Risks PCC

| ID | Risk | Impact | Probability | Mitigation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| R-001 | Backlog canonique non totalement verifie | Medium | Medium | Verifier le backlog avant les tickets metier | Directeur General | Open |
| R-002 | Derive de secret ou de configuration | High | Medium | Appliquer les regles de securite et de traceabilite | Securite | Open |
| R-003 | Ambiguite d'infrastructure entre environnements | High | Medium | Formaliser les conventions d'environnement et de deploiement | DevOps | Open |
| R-004 | Derive entre la base Docker et les overlays environnementaux | High | Medium | Promouvoir le meme digest, figer les tags et reutiliser la base commune | DevOps | Open |
| R-005 | Drift between Compose overlays and environment contracts | High | Medium | Keep resource names stable, externalize environment values and validate merged config | DevOps | Open |
