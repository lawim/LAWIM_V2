---
applyTo: "tests/**/*.py,reports/testing/**/*.md,reports/incidents/**/*.md,reports/release/**/*.md,deployment/**/*.sh,scripts/**/*.py"
---

# LAWIM — Tests et preuves

Tout défaut doit d’abord être reproduit.

Ne jamais assouplir un test pour rendre le résultat positif.

Distinguer obligatoirement :

- IMPLEMENTED
- LOCALLY_TESTED
- DEPLOYED
- TECHNICALLY_REACHABLE
- RUNTIME_VALIDATED
- USER_ACCEPTED

Pour WhatsApp ou Telegram, USER_ACCEPTED exige :

- message réel envoyé ;
- webhook réel reçu ;
- conversation corrélée ;
- réponse métier générée ;
- adaptateur sortant appelé ;
- message réellement reçu sur le terminal ;
- contenu vérifié.

Les éléments suivants ne suffisent pas :

- build réussi ;
- tests unitaires ;
- conteneur healthy ;
- healthz 200 ;
- readyz 200 ;
- webhook simulé ;
- Green API authorized ;
- Telegram getMe ok ;
- tag Git ;
- rapport de certification.
