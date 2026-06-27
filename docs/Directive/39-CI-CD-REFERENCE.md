# LAWIM

# 39-CI-CD-REFERENCE.md

# Référentiel officiel CI/CD

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le présent document définit le pipeline d'intégration et de déploiement continu de LAWIM.

---

# CHAPITRE 2 — ÉTAPES

Le pipeline doit couvrir :

* lint ;
* build ;
* tests ;
* sécurité ;
* analyse qualité ;
* migration Prisma ;
* déploiement staging ;
* recette ;
* déploiement production ;
* rollback.
* contrôles de cohérence des lots de tracking marketing transverse ;

---

# CHAPITRE 3 — RÈGLES

Le pipeline doit être :

* reproductible ;
* journalisé ;
* versionné ;
* compatible avec les environnements de préproduction et de production.

---

# CHAPITRE 4 — OBJECTIF FINAL

Le référentiel CI/CD garantit une livraison contrôlée de LAWIM.

Les étapes du pipeline doivent conserver les KPI, dashboards et rapports marketing cohérents d'un environnement à l'autre.
