# LAWIM Role Model — Certified Gold Reference

---

## Overview

This document captures the complete LAWIM role model: role families, permission levels, trust levels, badges, agency structure, journey mapping, and fusion decisions. All entries are sourced and confidence-rated.

---

## 1. Six Role Families

| ID | Family | Roles Included | Source | Confidence |
|----|--------|----------------|--------|------------|
| GOLD-RL-001 | Demandeur | demandeur, buyer, tenant, investor, property_seeker | Directive/08-ROLE-REFERENCE.md, Ch.32-33 | HIGH |
| GOLD-RL-002 | Proprietaire | owner, seller, détenteur | Directive/08-ROLE-REFERENCE.md, Ch.34-35 | HIGH |
| GOLD-RL-003 | Agent | agent_immobilier, broker | Directive/08-ROLE-REFERENCE.md, Ch.36 | HIGH |
| GOLD-RL-004 | Operateur | responsable_agence, administrateur_agence, assistant | Directive/08-ROLE-REFERENCE.md, Ch.37-38 | HIGH |
| GOLD-RL-005 | Superviseur | conseiller, médiateur, responsable_opérationnel | Directive/08-ROLE-REFERENCE.md, Ch.40 | HIGH |
| GOLD-RL-006 | Admin | administrateur, administrateur_principal | Directive/08-ROLE-REFERENCE.md, Ch.40 | HIGH |

### Role Hierarchy (from implement_all.sql)

| ID | Role | Level | Parent | Source | Confidence |
|----|------|-------|--------|--------|------------|
| GOLD-RL-007 | demandeur | 1 | — | implement_all.sql (recovered) | HIGH |
| GOLD-RL-008 | vendeur/propriétaire | 2 | demandeur | implement_all.sql (recovered) | HIGH |
| GOLD-RL-009 | agent | 3 | propriétaire | implement_all.sql (recovered) | HIGH |
| GOLD-RL-010 | agence | 4 | agent | implement_all.sql (recovered) | HIGH |
| GOLD-RL-011 | assistant | 5 | agence | implement_all.sql (recovered) | HIGH |
| GOLD-RL-012 | vice_master | 6 | assistant | implement_all.sql (recovered) | HIGH |
| GOLD-RL-013 | master | 7 | vice_master | implement_all.sql (recovered) | HIGH |

---

## 2. Four Permission Levels

| ID | Level | Name | Description | Source | Confidence |
|----|-------|------|-------------|--------|------------|
| GOLD-RL-014 | Niveau 1 | Lecture (Read) | User can consult | Directive/08-ROLE-REFERENCE.md, Ch.48 | HIGH |
| GOLD-RL-015 | Niveau 2 | Création (Create) | User can create | Directive/08-ROLE-REFERENCE.md, Ch.48 | HIGH |
| GOLD-RL-016 | Niveau 3 | Modification (Edit) | User can modify items under their responsibility | Directive/08-ROLE-REFERENCE.md, Ch.48 | HIGH |
| GOLD-RL-017 | Niveau 4 | Validation (Approve) | User can approve or reject operations | Directive/08-ROLE-REFERENCE.md, Ch.48 | HIGH |

Note: 08-ROLE-REFERENCE.md Ch.48 defines 5 levels (including Niveau 5: Administration). The 4-level model in roles-matrix.md collapses Administration into a higher tier.

### Permission Matrix (from 08-ROLE-REFERENCE.md Ch.54)

| Domain | Demandeur | Propriétaire | Agent | Resp. Agence | Admin LAWIM |
|--------|-----------|--------------|-------|--------------|-------------|
| Consulter un bien | ✅ | ✅ | ✅ | ✅ | ✅ |
| Publier un bien | ❌ | ✅ | ✅ | ✅ | ✅ |
| Modifier ses biens | ❌ | ✅ | ✅ | ✅ | ✅ |
| Modifier bien tiers | ❌ | ❌ | Selon mandat | Selon mandat | ✅ |
| Créer une agence | ❌ | Demande | Demande | ❌ | Validation |
| Valider une agence | ❌ | ❌ | ❌ | ❌ | ✅ |

Source: Directive/08-ROLE-REFERENCE.md, Ch.54 — HIGH confidence.

---

## 3. Six Trust Levels

| ID | Level | Name | Icon | Description | Source | Confidence |
|----|-------|------|------|-------------|--------|------------|
| GOLD-RL-018 | Niveau 1 | Nouveau compte | 🔴 | Account newly created | Directive/08-ROLE-REFERENCE.md, Ch.63 | HIGH |
| GOLD-RL-019 | Niveau 2 | Téléphone vérifié | 🟠 | Phone number verified via OTP | Directive/08-ROLE-REFERENCE.md, Ch.63 | HIGH |
| GOLD-RL-020 | Niveau 3 | Identité vérifiée | 🟡 | Identity documents validated | Directive/08-ROLE-REFERENCE.md, Ch.63 | HIGH |
| GOLD-RL-021 | Niveau 4 | Documents pro validés | 🟢 | Professional documents verified | Directive/08-ROLE-REFERENCE.md, Ch.63 | HIGH |
| GOLD-RL-022 | Niveau 5 | Professionnel vérifié | 🔵 | Agent/partner validated | Directive/08-ROLE-REFERENCE.md, Ch.63 | HIGH |
| GOLD-RL-023 | Niveau 6 | Compte de référence | ⭐ | Recognized reference account | Directive/08-ROLE-REFERENCE.md, Ch.63 | HIGH |

---

## 4. Eight Badges

| ID | Badge | Icon | Requirement | Source | Confidence |
|----|-------|------|-------------|--------|------------|
| GOLD-RL-024 | Téléphone vérifié | 📱 | OTP validation completed | Directive/08-ROLE-REFERENCE.md, Ch.64 | HIGH |
| GOLD-RL-025 | E-mail vérifié | 📧 | Email address confirmed | Directive/08-ROLE-REFERENCE.md, Ch.64 | HIGH |
| GOLD-RL-026 | Identité vérifiée | 🪪 | CNI/passport validated by LAWIM team | Directive/08-ROLE-REFERENCE.md, Ch.64 | HIGH |
| GOLD-RL-027 | Propriétaire vérifié | 🏠 | Property ownership documents verified | Directive/08-ROLE-REFERENCE.md, Ch.64 | HIGH |
| GOLD-RL-028 | Agence vérifiée | 🏢 | Agency registration and documents approved | Directive/08-ROLE-REFERENCE.md, Ch.64 | HIGH |
| GOLD-RL-029 | Partenaire LAWIM | 🤝 | Partner (notaire, géomètre, banque) validated | Directive/08-ROLE-REFERENCE.md, Ch.64 | HIGH |
| GOLD-RL-030 | Professionnel vérifié | ⭐ | Professional status confirmed (agent, etc.) | Directive/08-ROLE-REFERENCE.md, Ch.64 | HIGH |
| GOLD-RL-031 | Agent actif | ✅ | Agent fully onboarded and active | Directive/08-ROLE-REFERENCE.md, Ch.24 | HIGH |

---

## 5. Agency Structure and Hierarchy

| ID | Concept | Description | Source | Confidence |
|----|---------|-------------|--------|------------|
| GOLD-RL-032 | Agency definition | An agency is an organization, not a simple user | Directive/08-ROLE-REFERENCE.md, Ch.12 | HIGH |
| GOLD-RL-033 | Agency components | Responsible + agents + admin + properties + files + validations + trust level | Directive/08-ROLE-REFERENCE.md, Ch.12 | HIGH |
| GOLD-RL-034 | Agency creation | Requires: name, responsible, phone, address, location, CNI, RCCM, tax ID | Directive/08-ROLE-REFERENCE.md, Ch.23 | HIGH |
| GOLD-RL-035 | Agent onboarding | Invitation → secure link → account creation → phone verification → CNI → LAWIM validation → active | Directive/08-ROLE-REFERENCE.md, Ch.24 | HIGH |
| GOLD-RL-036 | Minimum agents | LAWIM recommends minimum 3 active agents for operational agency | Directive/08-ROLE-REFERENCE.md, Ch.37 | HIGH |
| GOLD-RL-037 | Lead routing | Geographic zone routing via `agent_zones` table | implement_all.sql (recovered) | HIGH |
| GOLD-RL-038 | Lead cost | Default 500 FCFA per lead for agents | implement_all.sql (recovered) | MEDIUM |
| GOLD-RL-039 | Agent credits | Tables: `agent_credits` (credits, total_spent, last_recharge), `boost_purchases` (boost_type, price, expires_at) | implement_all.sql (recovered) | HIGH |
| GOLD-RL-040 | Agent rating | Scale 1-5, updated after each interaction | code/lawim_v2/crm/ (agent_rating.py equivalent) | HIGH |

---

## 6. Role-to-Journey Coverage Mapping

| ID | Journey | Roles Covered | Coverage | Source | Confidence |
|----|---------|--------------|----------|--------|------------|
| GOLD-RL-041 | Property search | demandeur, buyer, tenant, investor, diaspora_investor | FULL | roles-matrix.md (legacy) | MEDIUM |
| GOLD-RL-042 | Property listing | owner, seller, agent, agence | FULL | roles-matrix.md (legacy) | MEDIUM |
| GOLD-RL-043 | Matching & proposals | demandeur, agent | FULL | roles-matrix.md (legacy) | MEDIUM |
| GOLD-RL-044 | Visit scheduling | demandeur, agent, owner | FULL | roles-matrix.md (legacy) | MEDIUM |
| GOLD-RL-045 | Negotiation | demandeur, agent, owner | PARTIAL | roles-matrix.md (legacy) | MEDIUM |
| GOLD-RL-046 | Transaction | demandeur, agent, owner, notaire | PARTIAL | roles-matrix.md (legacy) | MEDIUM |
| GOLD-RL-047 | Post-sale follow-up | agent, owner | LIMITED | roles-matrix.md (legacy) | MEDIUM |
| GOLD-RL-048 | Admin supervision | assistant, vice_master, master, admin | FULL | roles-matrix.md (legacy) | MEDIUM |

---

## 7. Role Fusion Decisions

| ID | Decision | Rationale | Source | Confidence |
|----|----------|-----------|--------|------------|
| GOLD-RL-049 | buyer + tenant → demandeur | Both search for property; differentiated by transaction type, not role | roles-matrix.md + Directive/01-GLOSSAIRE.md | HIGH |
| GOLD-RL-050 | seller + owner → propriétaire | Owner who publishes property becomes seller contextually | roles-matrix.md + Directive/08-ROLE-REFERENCE.md, Ch.35 | HIGH |
| GOLD-RL-051 | agent + broker → agent | Single professional intermediary role | roles-matrix.md | MEDIUM |
| GOLD-RL-052 | investor + diaspora_investor → investisseur | Diaspora is a lead classification, not a separate role; both share investor role with different lead scores | roles-matrix.md + lead_classifier_v1.json | HIGH |
| GOLD-RL-053 | vice_master + master → administrateur | Internal hierarchy; both are admin family with graduated permissions | roles-matrix.md + Directive/08-ROLE-REFERENCE.md, Ch.40 | HIGH |
| GOLD-RL-054 | assistant → operateur | Assistant is agency operator, not admin; belongs in operateur family | roles-matrix.md | MEDIUM |

---

## 8. Partner Roles (External)

| ID | Partner | System Role | Source | Confidence |
|----|---------|-------------|--------|------------|
| GOLD-RL-055 | Notaire | Legal validation of transactions | Directive/08-ROLE-REFERENCE.md, Ch.39 | HIGH |
| GOLD-RL-056 | Géomètre | Surveying and measurements | Directive/08-ROLE-REFERENCE.md, Ch.39 | HIGH |
| GOLD-RL-057 | Banque | Financing and loans | Directive/08-ROLE-REFERENCE.md, Ch.39 | HIGH |
| GOLD-RL-058 | Assurance | Property coverage | Directive/08-ROLE-REFERENCE.md, Ch.39 | HIGH |
| GOLD-RL-059 | Photographe | Real estate photography | Directive/08-ROLE-REFERENCE.md, Ch.39 | HIGH |
| GOLD-RL-060 | Artisan | Renovation and works | Directive/08-ROLE-REFERENCE.md, Ch.39 | HIGH |
| GOLD-RL-061 | Expert partenaire | Domain expert | Directive/08-ROLE-REFERENCE.md, Ch.39 | HIGH |

---

*Certified Gold — 2026-07-15 — All entries sourced and confidence-rated.*
