# CRM MODEL — Modèle CRM LAWIM

**Sources :** LAWIMA `08_CONFIG/state_machine/USER_STATES.json`, `EVENT_TYPES.json`, `02_KNOWLEDGE/user_roles/user_roles.json`, `02_KNOWLEDGE/crm_schema/crm_schema.json`, `03_ENGINE/agent_optin.py`, `agent_rating.py`, `identity_resolution.py`, `05_AUTOMATIONS/scripts/implement_all.sql`, `setup_database.sql`, `07_DASHBOARD/agent_dashboard*.py`, `master_dashboard*.py`, LAWIM `Directive/08-ROLE-REFERENCE.md`
**Principe :** Documentation exhaustive des rôles, acteurs et relations CRM

---

## 1. Acteurs du système

**Source :** LAWIMA `02_KNOWLEDGE/user_roles/user_roles.json`, `05_AUTOMATIONS/scripts/implement_all.sql`

### 1.1 Familles d'acteurs

| Acteur | Description | Code dans le système |
|--------|-------------|---------------------|
| **Demandeur** | Personne cherchant un bien | demandeur |
| **Propriétaire** | Personne possédant un bien | proprietaire, property_owner |
| **Vendeur** | Personne mettant en vente | vendeur, seller |
| **Acheteur** | Personne souhaitant acheter | acheteur, buyer |
| **Locataire** | Personne souhaitant louer | locataire, tenant |
| **Investisseur** | Personne souhaitant investir | investisseur, investor |
| **Agent** | Professionnel immobilier | agent |
| **Agence** | Structure professionnelle | agence |
| **Assistant** | Assistant d'agence | assistant |
| **Vice-Master** | Super-admin adjoint | vice_master |
| **Master** | Super-administrateur | master |
| **Courtier/Broker** | Intermédiaire non-agréé | broker |
| **Notaire** | Professionnel juridique | notaire |
| **Architecte** | Professionnel technique | architecte |
| **Géomètre** | Professionnel technique | geometre |
| **Artisan** | Prestataire de services | artisan |
| **Banque** | Institution financière | banque |
| **Assurance** | Compagnie d'assurance | assurance |

### 1.2 Hiérarchie des permissions

**Source :** LAWIMA `05_AUTOMATIONS/scripts/implement_all.sql`

| Rôle | Permissions |
|------|-------------|
| demandeur | view_properties, post_request |
| vendeur | post_property, view_own_properties |
| agent | view_leads, accept_leads |
| agence | view_all_leads, manage_agents |
| assistant | view_stats |
| vice_master | manage_permissions |
| master | manage_all |

### 1.3 Niveaux de rôle

**Source :** LAWIMA `01_DATABASE` (schéma persons)

- max_role_level (INTEGER DEFAULT 1)
- max_role (TEXT DEFAULT 'demandeur')
- is_admin (BOOLEAN)
- is_vendor (BOOLEAN)

## 2. États utilisateur

**Source :** LAWIMA `08_CONFIG/state_machine/USER_STATES.json`

| État | Description |
|------|-------------|
| NEW_USER | Nouvel utilisateur |
| SEARCHING_PROPERTY | En recherche de bien |
| PROPERTY_OWNER | Propriétaire d'un bien |
| AGENT | Agent immobilier |
| LEAD_CREATED | Lead créé |
| PREMIUM_AGENT | Agent premium |
| INACTIVE | Utilisateur inactif |

## 3. Types d'événements

**Source :** LAWIMA `08_CONFIG/state_machine/EVENT_TYPES.json`

| Événement | Description |
|-----------|-------------|
| message.received | Message reçu |
| intent.detected | Intention détectée |
| user.created | Utilisateur créé |
| user.state_changed | Changement d'état |
| property.created | Propriété créée |
| lead.created | Lead créé |
| match.generated | Match généré |
| payment.success | Paiement réussi |
| subscription.renewed | Abonnement renouvelé |
| boost.applied | Boost appliqué |
| access.granted | Accès accordé |

## 4. Gestion des agents

### 4.1 Agent Opt-In

**Source :** LAWIMA `03_ENGINE/agent_optin.py`

Processus de permission avant partage :
1. Détection du besoin → recherche d'agent dans la zone
2. Demande de permission : "Voulez-vous recevoir son contact ?"
3. Log dans `agent_optins` (statut : accepted/declined)
4. Partage du contact si accepté

### 4.2 Notation des agents

**Source :** LAWIMA `03_ENGINE/agent_rating.py`

- Échelle : 1 à 5
- Moyenne mise à jour dans `whatsapp_agents`
- Affichage : `⭐ X/5` ou `🆕` pour nouveau

### 4.3 Prix des leads

**Source :** LAWIMA `07_DASHBOARD/agent_dashboard*.py`

- Prix par lead par défaut : 500 FCFA
- Configurable par agent

### 4.4 Zones des agents

**Source :** LAWIMA `agents` table (zone field)

Routage des leads par zone géographique :
- Les leads sont routés vers les agents de la zone correspondante
- Historique dans `agent_routing_history`

### 4.5 Crédits agents

**Source :** LAWIMA `05_AUTOMATIONS/scripts/implement_all.sql`

Table `agent_credits` :
- credits (solde)
- total_spent (total dépensé)
- last_recharge (dernière recharge)

Table `boost_purchases` :
- boost_type (type de boost)
- price (prix)
- expires_at (date d'expiration)

## 5. Tables CRM (schéma complet)

**Source :** LAWIMA `05_AUTOMATIONS/scripts/implement_all.sql`, `setup_database.sql`

### 5.1 Tables principales

| Table | Description |
|-------|-------------|
| persons | Personnes (utilisateurs, prospects, clients) |
| contact_channels | Canaux de contact |
| agents | Agents immobiliers |
| properties | Biens immobiliers |
| leads | Opportunités commerciales |
| data_sources | Sources d'import des données |
| knowledge_entries | Base de connaissance |
| events | Journal d'événements |

### 5.2 Tables de gestion

| Table | Description |
|-------|-------------|
| agent_routing_history | Historique de routage des leads |
| agent_zones | Zones d'activité des agents |
| agent_credits | Crédits des agents |
| boost_purchases | Achats de boosts |
| role_permissions | Permissions par rôle |
| user_permissions | Permissions spécifiques par utilisateur |
| pending_permission_changes | Changements de permissions en attente |

### 5.3 Tables de contentieux et conformité

| Table | Description |
|-------|-------------|
| disputes | Litiges et réclamations |
| anonymization_requests | Demandes RGPD d'effacement |

### 5.4 Tables d'apprentissage

| Table | Description |
|-------|-------------|
| training_conversations | Conversations d'entraînement |
| system_logs | Logs système |
| whatsapp_logs | Logs WhatsApp |

## 6. Résolution d'identité

**Source :** LAWIMA `03_ENGINE/identity_resolution.py`

### 6.1 Critères de détection des doublons

| Critère | Score de correspondance |
|---------|----------------------|
| Téléphone identique | 100 |
| Email identique | 95 |
| Prénom identique + nom similaire + téléphone similaire | ≥ 40 |

### 6.2 Algorithme de fusion
- Détection des candidats doublons
- Calcul du score de correspondance
- Seuil de confirmation : ≥ 40
- Statut : pending (en attente)
- Table : `duplicate_candidates`

## 7. Dashboards CRM

**Source :** LAWIMA `07_DASHBOARD/`

### 7.1 Master Dashboard

**Sources :** `master_dashboard.py`, `master_dashboard_v2.py`, `master_dashboard_v3.py`, `master_dashboard_supabase.py`

- Authentification : password "[REDACTED-DEFAULT-PASSWORD]"
- Métriques : total leads, leads acceptés, score moyen, agents actifs
- Onglets :
  - Statistiques (évolution 7 jours, répartition intention, répartition score)
  - Tous les leads (dataframe + export CSV)
  - Configuration

### 7.2 Agent Dashboard

**Sources :** `agent_dashboard.py` à `agent_dashboard_v8.py`

- Authentification : par numéro WhatsApp
- Métriques agent : leads reçus, acceptés, taux conversion, note moyenne
- Onglets :
  - Leads reçus
  - Statistiques (performance, répartition statuts)
  - Profil (nom, téléphone, spécialité, zone, prix par lead)

## 8. Diaspora

**Source :** LAWIMA `03_ENGINE/diaspora_filter.py`

Services dédiés pour la diaspora (table `diaspora_services`).
Détection par localisation et indicatif téléphonique.
Propriétés marquées `diaspora_ready` pour filtrage.

---

*Document patrimonial — Aucune décision de reconstruction n'est prise ici.*
