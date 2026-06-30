# LAWIM 2.x — Program Roadmap

**Programme :** LAWIM_2X  
**Branche :** `develop/2.0-intelligent-platform`  
**Base :** v1.0.0  
**Horizon initial :** 12 mois (aligné plan stratégique année 1)

---

## 1. Principes de roadmap

1. **Confiance avant croissance** — qualité des fondations 2.x avant acquisition massive.
2. **Incrémental** — chaque programme livre un incrément testable, pas un big bang.
3. **1.0 préservé** — maintenance 1.0.x indépendante ; 2.x sur branche develop.
4. **Données avant IA** — connaissance et projets structurés avant assistant avancé.
5. **Mesurable** — chaque programme définit des critères de sortie et KPI.

---

## 2. Vue d’ensemble des programmes

```
v1.0.0 (GA) ──► PROGRAM 001 (vision/strategy) ──► PROGRAM 002 … 009
                      │                              │
                      └─ READY_FOR_DG_REVIEW         └─ delivery waves
```

| ID | Programme | Objectif | Durée indicative |
|----|-----------|----------|------------------|
| **001** | Intelligent Platform Definition | Vision, architecture, gouvernance programme | ✓ (en cours) |
| **002** | Project Domain & Journey Foundation | Modèle Projet, parcours guidés, API | 4–6 semaines |
| **003** | Knowledge Engine MVP | Référentiel, ingestion, recherche interne | 4–6 semaines |
| **004** | Intelligent Assistant v1 | Copilote ancré connaissance + projet | 6–8 semaines |
| **005** | Partner Qualification & Directory | Annuaire partenaires, profils, zones | 4–6 semaines |
| **006** | Trust Scoring v1 | Score explicable biens/partenaires/données | 3–4 semaines |
| **007** | Services Marketplace Pilot | Catalogue services, commande, suivi | 6–8 semaines |
| **008** | Intelligent Search & Matching v2 | Sémantique, explications, projet-aware | 6–8 semaines |
| **009** | Mobile-First & Product Analytics | PWA, events, dashboards | 8–10 semaines |

Les durées sont indicatives pour une équipe petite ; ajustables par la DG.

---

## 3. PROGRAM 001 — Intelligent Platform (actuel)

**Statut :** clôture documentation — `lawim-2x-program-001`

**Livrables :**

- Vision produit 2.x
- Principes d’architecture
- Roadmap programmes
- Rapport DG

**Critères de sortie :** validation DG → lancement PROGRAM 002.

---

## 4. PROGRAM 002 — Project Domain & Journey Foundation

**Objectif :** Introduire le **Projet** comme entité centrale et les **parcours guidés** sans casser 1.0.

**Scope technique (preview) :**

- Modèle `Project` (type, budget, localisation cible, stade, liens property/conversation)
- Machine d’états parcours (qualification → recherche → …)
- API `/api/projects`, `/api/journeys`
- Extension bootstrap UI (lecture seule / wizard minimal)
- Tests harness + migration additive (schema v6+)

**Hors scope :** IA, marketplace, paiement Campay.

**KPI sortie :**

- Création et reprise de projet en < 2 min
- 100 % parcours traçables en audit log
- Suite 1.0 regression PASS

---

## 5. PROGRAM 003 — Knowledge Engine MVP

**Objectif :** Base de connaissance structurée alimentant assistant et parcours.

**Scope :**

- Entités : quartier, procédure, FAQ, fiche marché, checklist
- Stockage versionné (PostgreSQL + export)
- API recherche interne (`/api/knowledge/search`)
- Pipeline ingestion manuelle + import partenaire
- Alignement contenu éditorial (plan stratégique Partie 4)

**KPI :** ≥ 50 fiches qualifiées ; latence recherche < 200 ms p95.

---

## 6. PROGRAM 004 — Intelligent Assistant v1

**Objectif :** Copilote projet avec réponses ancrées.

**Scope :**

- Interface assistant (web + API)
- RAG sur knowledge engine + contexte projet autorisé
- Garde-fous : pas de conseil juridique définitif, disclaimer, escalade humaine
- Journalisation prompts/réponses (audit)

**KPI :** satisfaction ≥ 4/5 sur pilote 50 utilisateurs ; 0 fuite données cross-projet.

---

## 7. PROGRAM 005 — Partner Qualification

**Objectif :** Écosystème partenaires crédible.

**Scope :**

- Profil partenaire étendu (métier, zone, certifications, statut vérification)
- Workflow qualification admin
- Mise en relation projet → partenaire
- Intégration Telegram/WhatsApp (phase ultérieure possible)

**KPI :** 20 partenaires qualifiés en pilote ; délai mise en relation < 48 h.

---

## 8. PROGRAM 006 — Trust Scoring v1

**Objectif :** Score de confiance explicable.

**Scope :**

- Modèle de score composite (données, vérifs, historique, signalements)
- Affichage utilisateur (« pourquoi ce score »)
- API admin recalcul / override audité

**KPI :** 100 % scores avec facteurs explicites ; corrélation positive satisfaction.

---

## 9. PROGRAM 007 — Services Marketplace Pilot

**Objectif :** Monétisation par services (pas commissions immo).

**Scope :**

- Catalogue services (accompagnement, diaspora, visite…)
- Commande, statut, exécution, évaluation
- Préparation intégration Campay (stub → prod)
- Lien parcours projet

**KPI :** 3 services pilotes ; ≥ 10 commandes test ; NPS services mesuré.

---

## 10. PROGRAM 008 — Intelligent Search v2

**Objectif :** Recherche et matching orientés projet.

**Scope :**

- Index sémantique biens + connaissance
- Matching v2 (scores expliqués, critères projet)
- Enrichissement UI recherche

**KPI :** +20 % pertinence perçue vs matching 1.0 (étude A/B pilote).

---

## 11. PROGRAM 009 — Mobile-First & Analytics

**Objectif :** Mobile-first réel + pilotage produit.

**Scope :**

- PWA responsive, installable, notifications
- SDK events produit (frontend + backend)
- Dashboards : entonnoirs, rétention, parcours, services
- Export metrics (future Prometheus/BI)

**KPI :** ≥ 60 % sessions mobile pilote ; dashboards Direction opérationnels.

---

## 12. Alignement plan stratégique (année 1)

| Priorité plan stratégique | Programmes 2.x |
|---------------------------|----------------|
| Base de données qualifiée | 002, 008 |
| Réseau partenaires | 005, 006 |
| Confiance | 006, 004 (garde-fous) |
| Communauté | 009 (analytics, mobile) |
| Revenus services | 007 |
| LAWIM AI | 003, 004, 008 |
| Continuous learning | 003, 009 |

---

## 13. Jalons trimestriels (indicatif)

| Trimestre | Programmes cibles | Résultat attendu |
|-----------|-------------------|------------------|
| T1 | 001 → 002 → 003 | Projet + connaissance MVP |
| T2 | 004 → 005 | Assistant + partenaires pilote |
| T3 | 006 → 007 | Confiance + marketplace pilote |
| T4 | 008 → 009 | Recherche v2 + mobile + analytics |

---

## 14. Gouvernance programme

- **Comité Produit 2.x** : hebdomadaire, priorisation backlog programmes.
- **Comité Stratégique** : mensuel, validation jalons et budget.
- **Gate DG** : avant chaque PROGRAM N+1 (critères de sortie N validés).
- **Branches** : `develop/2.0-intelligent-platform` ; releases `2.0.0-alpha`, `2.0.0-beta`, `2.0.0` ultérieures.

---

*Roadmap vivante — révision trimestrielle par la Direction, sans modifier Constitution/Gouvernance historiques.*
