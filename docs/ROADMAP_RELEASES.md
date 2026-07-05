# ROADMAP_RELEASES

## Classification officielle des releases

- AAD = Microsoft Entra ID / Identity Provider / Authentication Scaffold
- AAE = Production Security & Secrets
- AAF = Migration OVH
- AAG = Monitoring & Observability
- AAH = Performance & Load Testing
- AAI = Go Live Certification
- AAJ = Production Deployment

## Règles de normalisation

- La phase AAD est officiellement clôturée.
- Le nom AAD ne doit plus être utilisé pour désigner la sécurité globale de production.
- Les tags et commits existants ne sont pas renommés.
- Seule la documentation est normalisée.

## Cloture OVH

- Le deploiement de production AAJ a ete finalise sur le snapshot `4c078fd8139f98d6cc34c6e6ff452165bee10bdd`.
- Le rollback vers `/opt/lawim/releases/bc46a686` est conserve.
