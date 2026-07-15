# ROLE MODEL — Modèle de rôles LAWIM

**Sources :** LAWIM `Directive/08-ROLE-REFERENCE.md`, LAWIMA `02_KNOWLEDGE/user_roles/user_roles.json`, `05_AUTOMATIONS/scripts/implement_all.sql`, `03_ENGINE/agent_optin.py`, `agent_rating.py`, `07_DASHBOARD/agent_dashboard*.py`, `master_dashboard*.py`, `08_CONFIG/state_machine/USER_STATES.json`
**Principe :** Documentation exhaustive des rôles et permissions

---

## 1. Rôles dans le système

### 1.1 Rôles principaux

**Source :** LAWIMA `02_KNOWLEDGE/user_roles/user_roles.json`, `05_AUTOMATIONS/scripts/implement_all.sql`

| Rôle | Niveau | Description |
|------|--------|-------------|
| **demandeur** | 1 | Personne cherchant un bien immobilier |
| **vendeur** | 2 | Personne mettant en vente un bien |
| **acheteur** | — | Personne souhaitant acheter (statut implicite) |
| **locataire** | — | Personne souhaitant louer (statut implicite) |
| **investisseur** | — | Personne souhaitant investir |
| **agent** | 3 | Professionnel de l'immobilier |
| **agence** | 4 | Structure professionnelle |
| **assistant** | 5 | Assistant d'agence |
| **vice_master** | 6 | Super-administrateur adjoint |
| **master** | 7 | Super-administrateur |

### 1.2 Rôles externes / partenaires

**Source :** LAWIMA `05_AUTOMATIONS/scripts/implement_all.sql`

| Partenaire | Rôle dans le système |
|------------|---------------------|
| **Notaire** | Validation juridique des transactions |
| **Architecte** | Conception et plans |
| **Géomètre** | Bornage et mesures |
| **Artisan** | Travaux et rénovations |
| **Banque** | Financement et prêts |
| **Assurance** | Couverture des biens |

## 2. Matrice des permissions

**Source :** LAWIMA `05_AUTOMATIONS/scripts/implement_all.sql`

| Rôle | Voir biens | Publier annonce | Voir leads | Accepter leads | Gérer agents | Voir stats | Gérer permissions |
|------|------------|-----------------|------------|----------------|--------------|------------|-------------------|
| demandeur | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| vendeur | ✓ | ✓ (propres) | ✗ | ✗ | ✗ | ✗ | ✗ |
| agent | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ |
| agence | ✓ | ✓ | ✓ (tous) | ✓ | ✓ | ✗ | ✗ |
| assistant | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ |
| vice_master | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| master | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

### 2.1 Tables de permissions

**Source :** LAWIMA `05_AUTOMATIONS/scripts/implement_all.sql`

- `role_permissions` : Permissions associées à chaque rôle
- `user_permissions` : Permissions spécifiques par utilisateur
- `pending_permission_changes` : Changements de permissions en attente de validation

## 3. États des utilisateurs

**Source :** LAWIMA `08_CONFIG/state_machine/USER_STATES.json`

| État | Signification | Rôles possibles |
|------|---------------|-----------------|
| NEW_USER | Nouvel utilisateur non qualifié | demandeur |
| SEARCHING_PROPERTY | En recherche active | demandeur, acheteur, locataire, investisseur |
| PROPERTY_OWNER | Propriétaire déclaré | vendeur, propriétaire |
| AGENT | Agent professionnel | agent |
| LEAD_CREATED | Lead généré | demandeur, acheteur, locataire, investisseur |
| PREMIUM_AGENT | Agent avec abonnement premium | agent (premium) |
| INACTIVE | Utilisateur inactif (>90 jours) | tous |

## 4. Gestion des agents

### 4.1 Attribution des leads

**Source :** LAWIMA `03_ENGINE/agent_optin.py`, `05_AUTOMATIONS/scripts/implement_all.sql`

- Routage par zone géographique (table `agent_zones`)
- Historique de routage (`agent_routing_history`)
- Prix par lead par défaut : 500 FCFA
- Opt-in obligatoire avant partage du contact agent

### 4.2 Crédits des agents

**Source :** LAWIMA `05_AUTOMATIONS/scripts/implement_all.sql`

- Table `agent_credits` : credits, total_spent, last_recharge
- Table `boost_purchases` : boost_type, price, expires_at

### 4.3 Notation des agents

**Source :** LAWIMA `03_ENGINE/agent_rating.py`

- Échelle : 1 à 5
- Mise à jour après chaque interaction
- Affichée dans les résultats aux demandeurs

## 5. Hiérarchie des rôles

**Source :** LAWIM `Directive/08-ROLE-REFERENCE.md`

```
Master (niveau 7)
└── Vice-Master (niveau 6)
    └── Assistant (niveau 5)
        └── Agence (niveau 4)
            └── Agent (niveau 3)
                ├── Vendeur (niveau 2)
                └── Demandeur (niveau 1)
```

## 6. Niveaux de confiance

**Source :** LAWIMA `03_ENGINE/identity_resolution.py`, `anti_spam.py`

Concepts de confiance implicites dans le système :
- Nouvel utilisateur : confiance minimale
- Utilisateur vérifié (téléphone valide) : confiance de base
- Agent noté > 3/5 : confiance renforcée
- Propriétaire avec titre foncier : confiance élevée
- Utilisateur signalé ou spammeur : confiance révoquée

---

*Document patrimonial — Aucune décision de reconstruction n'est prise ici.*
