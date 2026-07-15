# RISK MATRIX — Heritage Gold Readiness

**Évalué par :** Risk Assessor (H0.3)
**Date :** 2026-07-15

## Risques par domaine

### Matching (93/100) — Risque FAIBLE

| Risque | Probabilité | Impact | Description |
|--------|:-----------:|:------:|-------------|
| Algorithme décisionnel erroné | Moyenne | Moyen | L'algorithme 10 étapes cité ne correspond pas à la source |
| Rematching incomplet | Faible | Faible | 19+ déclencheurs vs 6 documentés |
| Préférences manquantes | Faible | Faible | Niveau 4 compatibilité préférentielle absent |

### Négociation (78/100) — Risque MOYEN

| Risque | Probabilité | Impact | Description |
|--------|:-----------:|:------:|-------------|
| Aucun script commercial | Élevée | Élevé | LAWIM_V2 ne peut pas générer les interactions commerciales |
| Diaspora incomplet | Élevée | Moyen | Seulement 45% des comportements documentés |
| Persuasion sous-documentée | Moyenne | Faible | Pas de section dédiée |

### Langue (71/100) — Risque MOYEN

| Risque | Probabilité | Impact | Description |
|--------|:-----------:|:------:|-------------|
| Entity linking 50% fabriqué | Élevée | Élevé | 10 paires inventées induisent en erreur |
| IDs normalisés inventés | Élevée | Moyen | APT, STU, CHB n'existent pas dans le code |
| Templates sans emojis | Faible | Faible | Différence esthétique seulement |

### Qualification (56/100) — Risque ÉLEVÉ

| Risque | Probabilité | Impact | Description |
|--------|:-----------:|:------:|-------------|
| Pipeline 8 étapes non vérifiable | Élevée | Élevé | Impossible de savoir si le pipeline décrit est correct |
| CRM V5 7 facteurs non vérifiables | Élevée | Élevé | Poids non trouvés dans les sources |
| Anti-fraude sans implémentation | Élevée | Élevé | 3/4 couches totalement absentes |
| Agent network sous-documenté | Élevée | Moyen | Opt-in et rating quasi absents |

### CRM (52/100) — Risque ÉLEVÉ

| Risque | Probabilité | Impact | Description |
|--------|:-----------:|:------:|-------------|
| Lead routing aspirationnel | Élevée | Critique | Pipeline 8 étapes vs 3 étapes réel |
| Rôles sous-documentés | Élevée | Élevé | 2760 lignes de source non exploitées |
| Partenaires non documentés | Moyenne | Moyen | 5 types de partenaires absents |
| Anti-fraude inexistant | Élevée | Moyen | 4 couches annoncées, 0 présentes |

### Géographie (46/100) — Risque ÉLEVÉ

| Risque | Probabilité | Impact | Description |
|--------|:-----------:|:------:|-------------|
| Voisinage quasi inexistant | Élevée | Critique | 0 liens nearby, affinité pour 2 villes seulement |
| GPS sans metadata | Élevée | Élevé | Impossible de qualifier la fiabilité GPS |
| Alias districts vides | Élevée | Élevé | 382/382 districts sans alias |
| Hiérarchie à 60% vide | Élevée | Moyen | 5/10 niveaux sans données |

### Conversation (44/100) — Risque CRITIQUE

| Risque | Probabilité | Impact | Description |
|--------|:-----------:|:------:|-------------|
| Objection handling inexistant | Élevée | Critique | 23 patterns documentés mais 0 implémentés |
| Escalade inexistante | Élevée | Critique | 5 conditions documentées mais 0 implémentées |
| Behavioral tracking absent | Élevée | Élevé | Pas de système d'événements |
| Channel rules inapplicables | Élevée | Moyen | Règles sans implémentation technique |

## Risques globaux

### Risques critiques pour LAWIM_V2

| Risque | Domaine | Impact reconstruction |
|--------|---------|----------------------|
| Pas de machines à états | Workflow | ❌ Bloque toute orchestration — LAWIM_V2 serait un système linéaire sans capacité de workflow |
| Pas de NBA Engine | Architecture | ❌ Système passif — ne peut pas proposer, suivre, ou optimiser |
| Pas de données de voisinage | Géographie | ❌ Matching géographique limité à la ville exacte |
| Pas d'objection handling | Conversation | ❌ Les objections des clients restent sans réponse |
| Pas de sales scripts | Négociation | ❌ Pas d'outils commerciaux pour les agents |

### Risques majeurs

| Risque | Domaine | Impact reconstruction |
|--------|---------|----------------------|
| Pipeline CRM non vérifiable | CRM | ⚠️ Le routage des leads est spéculatif |
| Anti-fraude non implémenté | CRM/Qualif | ⚠️ Pas de protection contre les abus |
| Roles sous-documentés | CRM | ⚠️ La gestion des permissions est incomplète |
| Entity linking fabriqué | Langue | ⚠️ Les synonymes sont partiellement erronés |
| GPS sans metadata | Géographie | ⚠️ La fiabilité des coordonnées est inconnue |

## Heatmap globale

```
                    Probabilité
               Faible   Moyenne   Élevée
              ┌────────┬────────┬────────┐
     Critique  │        │        │  ████  │  Conversation
              │        │        │  ████  │  Workflow (gaps)
              ├────────┼────────┼────────┤
     Élevé    │        │  ██    │  █████ │  CRM, Géographie, Qualification
              │        │        │  █████ │
              ├────────┼────────┼────────┤
     Moyen    │  ██    │  ██    │  ██    │  Langue, Négociation
              │        │        │        │
              ├────────┼────────┼────────┤
     Faible   │  ██    │  ██    │        │  Matching
              │        │        │        │
              └────────┴────────┴────────┘
```

## Conclusion risques

Sur 7 domaines audités :
- **1** (Matching) : risque FAIBLE — prêt pour reconstruction
- **2** (Négociation, Langue) : risque MOYEN — nécessite des correctifs ciblés
- **3** (Qualification, CRM, Géographie) : risque ÉLEVÉ — nécessite un travail substantiel
- **1** (Conversation) : risque CRITIQUE — nécessite une reconstruction complète
