# LAWIM 2.x — PROGRAM 001 Report
## Intelligent Real Estate Platform — Definition

**Programme :** LAWIM_2X_PROGRAM_001  
**Date :** 2026-06-29  
**Branche :** `develop/2.0-intelligent-platform`  
**Base publiée :** v1.0.0  
**Auteur :** Équipe programme LAWIM 2.x

---

## Executive summary

LAWIM 2.x démarre sur la branche `develop/2.0-intelligent-platform`, à partir du socle **v1.0.0** gelé et publié. Ce programme 001 ne livre **aucune fonctionnalité métier** : il définit la vision, la roadmap et les principes d’architecture pour transformer LAWIM d’un monolithe listings/conversations en **plateforme d’accompagnement immobilier intelligent**.

La promesse 2.x : partir du **projet de vie** de l’utilisateur, le guider avec confiance, connecter des partenaires qualifiés, et s’appuyer sur un moteur de connaissance et un assistant ancré — aligné sur le [Plan Stratégique 2026–2027](../strategy/PLAN_STRATEGIQUE_DEPLOIEMENT_LAWIM_2026_2027_V2.md).

**Statut :** prêt pour revue Direction Générale.

---

## 1. Synthèse de la vision 2.x

LAWIM 2.x repose sur **dix piliers produit** :

| # | Pilier | Résumé |
|---|--------|--------|
| 1 | Accompagnement projet | Le Projet remplace l’annonce comme point d’entrée |
| 2 | Assistant intelligent | Copilote RAG, décision humaine |
| 3 | Moteur de connaissance | Référentiel marché, quartiers, procédures |
| 4 | Parcours guidés | State machines, reprise multi-session |
| 5 | Partenaires qualifiés | Annuaire vérifié, mise en relation contextuelle |
| 6 | Scoring de confiance | Scores explicables biens/partenaires |
| 7 | Marketplace services | Monétisation sans commission immo |
| 8 | Recherche intelligente | Sémantique + matching projet-aware |
| 9 | Mobile-first | PWA puis apps si justifié |
| 10 | Analytics produit | Events, entonnoirs, dashboards Direction |

Document détaillé : [LAWIM_2X_PRODUCT_VISION.md](../strategy/LAWIM_2X_PRODUCT_VISION.md).

---

## 2. Écarts entre LAWIM 1.0 et 2.x

### 2.1 État LAWIM 1.0 (v1.0.0)

Inventaire issu du code applicatif (`code/lawim_v2/`) et des rapports WEEK-001/002 :

| Domaine | 1.0 | Limite pour la vision stratégique |
|---------|-----|-----------------------------------|
| Modèle centrale | Property listing | Pas de concept Projet |
| Matching | Règles + scoring numérique | Pas sémantique, pas explication |
| Conversations | Oui, négociation par stades | Pas intégrées à un parcours global |
| Auth / RBAC | admin, agent, owner | Pas rôle partenaire / éditeur connaissance |
| Persistance | SQLite + PostgreSQL, schema v5 | Pas tables connaissance/trust/analytics |
| UI | Bootstrap monolithique web | Pas mobile-first / PWA |
| IA | Aucune | — |
| Partenaires | Agents basiques | Pas qualification ni marketplace |
| Paiement | Aucun | Campay prévu stratégie uniquement |
| Analytics | Audit events | Pas entonnoirs produit / BI |
| Ops | `/readyz`, métriques latence, CI | Base solide à étendre |

### 2.2 Gap structurant

```
1.0 :  User → Property → Match → Conversation
2.x :  User → Project → Journey → [Knowledge, Assistant, Partners, Services]
                              → Property / Match (sous-étapes)
```

### 2.3 Ce qui est préservé

- Runtime Python 3.12, packaging, migrations additives
- Sécurité (sessions, RBAC, rate limit, CORS, config prod)
- Branches 1.0 gelées (`main`, `maintenance/1.0.x`, `release/1.0.0-beta`)
- Règle : pas de commission sur transactions immobilières

---

## 3. Grands modules 2.x

Architecture **monolithe modulaire** (décision 2.0) :

| Module | Rôle |
|--------|------|
| **project** | Entité Projet, budget, type, stade |
| **journey** | Parcours guidés, machines d’états |
| **knowledge** | Ingestion, versioning, recherche contenu |
| **assistant** | Gateway RAG, garde-fous, audit |
| **partners** | Qualification, annuaire, zones |
| **trust** | Scoring explicable |
| **marketplace** | Catalogue et commandes services |
| **search_v2** | Recherche hybride + matching enrichi |
| **analytics** | Product events et agrégats |

Schéma et principes : [LAWIM_2X_ARCHITECTURE_PRINCIPLES.md](../strategy/LAWIM_2X_ARCHITECTURE_PRINCIPLES.md).

---

## 4. Programmes de travail proposés

| Programme | Intitulé | Priorité |
|-----------|----------|----------|
| **001** | Intelligent Platform Definition | ✓ Clôture doc |
| **002** | Project Domain & Journey Foundation | **P0 — prochain** |
| **003** | Knowledge Engine MVP | P0 |
| **004** | Intelligent Assistant v1 | P1 |
| **005** | Partner Qualification & Directory | P1 |
| **006** | Trust Scoring v1 | P1 |
| **007** | Services Marketplace Pilot | P2 |
| **008** | Intelligent Search & Matching v2 | P2 |
| **009** | Mobile-First & Product Analytics | P2 |

Roadmap détaillée : [LAWIM_2X_PROGRAM_ROADMAP.md](../strategy/LAWIM_2X_PROGRAM_ROADMAP.md).

---

## 5. Risques

| Risque | Impact | Mitigation |
|--------|--------|------------|
| Scope creep IA | Retards, coûts, confiance | RAG + garde-fous ; PROGRAM 003 avant 004 |
| Dette si big bang | Régression 1.0 | Monolithe modulaire, migrations additives |
| Données connaissance faibles | Assistant inutile | Ingestion manuelle MVP + partenaires |
| Partenaires non qualifiés | Perte confiance (pilier #1) | PROGRAM 005 avant marketplace large |
| Mobile négligé | Adoption Cameroun | Mobile-first dès PROGRAM 009, API dès 002 |
| Fuite données cross-projet | Légal / réputation | Isolation RBAC + tests sécurité |
| Dépendance LLM externe | Coût / souveraineté | Provider configurable ; ADR en 002 |
| Équipe petite | Jalons slip | Programmes courts, critères de sortie stricts |
| Divergence branches 1.0/2.x | Maintenance double | Gel 1.0 ; correctifs via maintenance/1.0.x seulement |

---

## 6. Première mission de développement recommandée

### LAWIM_2X_PROGRAM_002 — Project Domain & Journey Foundation

**Pourquoi en premier :**

1. Ancrage produit « facilitateur de projets » sans dépendre de l’IA.
2. Fondation pour assistant, marketplace, trust et search v2.
3. Migration additive compatible avec runtime 1.0 et suite de tests existante (~90 tests).

**Livrables attendus PROGRAM 002 :**

- Modèle `Project` + API `/api/v2/projects`
- Machine d’états parcours minimal (qualification → recherche)
- Lien optionnel Property / Conversation → Project
- Schema migration v6, tests intégration, doc ADR-002
- Régression 1.0 PASS, tag `lawim-2x-program-002`

**Hors scope PROGRAM 002 :** LLM, Campay, marketplace, PWA complète.

**Gate DG :** validation de ce rapport → GO PROGRAM 002.

---

## 7. Documents produits (PROGRAM 001)

| Document | Chemin |
|----------|--------|
| Vision produit | `docs/strategy/LAWIM_2X_PRODUCT_VISION.md` |
| Roadmap programmes | `docs/strategy/LAWIM_2X_PROGRAM_ROADMAP.md` |
| Principes architecture | `docs/strategy/LAWIM_2X_ARCHITECTURE_PRINCIPLES.md` |
| Rapport PROGRAM 001 | `reports/program/LAWIM-2X-PROGRAM-001-INTELLIGENT-PLATFORM-REPORT.md` |

---

## 8. Pré-vol (contrôle branche)

| Contrôle | Résultat |
|----------|----------|
| Racine dépôt | `/media/abel/5688bf41-1616-43e6-95c7-b9f1f043c850/LAWIM_V2` |
| Branche | `develop/2.0-intelligent-platform` |
| Tag v1.0.0 | Présent |
| Dépôt sale (pré-vol) | Non |
| RELEASE_NOTES_GA_1.0.0.md | Absent (non bloquant) |

---

## 9. Bloc programme (machine-readable)

```yaml
program: LAWIM_2X
status: READY_FOR_DG_REVIEW
base_version: v1.0.0
branch: develop/2.0-intelligent-platform
strategy: DEFINED
roadmap: DEFINED
architecture_principles: DEFINED
next_program: LAWIM_2X_PROGRAM_002
decision_required: true
```

---

## 10. Prochaines actions

1. **DG** : revue vision / roadmap / architecture — décision GO/NO-GO PROGRAM 002.
2. **Produit** : affiner personas diaspora et services pilote marketplace.
3. **Tech** : préparer ADR provider LLM et structure `code/lawim_v2/modules/`.
4. **Programme 002** : démarrer après validation DG.

---

*Fin du rapport LAWIM_2X_PROGRAM_001 — Intelligent Real Estate Platform Definition.*
