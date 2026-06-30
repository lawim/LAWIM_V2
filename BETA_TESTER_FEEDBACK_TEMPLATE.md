# LAWIM_V2 Beta 1.0.0 — Formulaire de retour testeur

Copier ce modèle, le remplir et le renvoyer par le canal défini par l'équipe LAWIM.

---

## Identité du testeur

| Champ | Valeur |
|-------|--------|
| Nom / équipe | |
| Date du test | |
| Tag testé | `v1.0.0-beta` / `v1.0.0-beta-validated` / autre : |
| Commit (si connu) | `git rev-parse HEAD` → |

---

## Environnement

| Champ | Valeur |
|-------|--------|
| OS | |
| Python (`python3 --version`) | |
| Docker (oui/non, version) | |
| Mode d'install | clone Git / pip editable / Compose seul |
| Moteur DB testé | SQLite / PostgreSQL / les deux |

---

## Résultats validation

| Commande | Résultat (OK / FAIL) | Notes |
|----------|----------------------|-------|
| `./scripts/install.sh` | | |
| `./scripts/validate-install.sh` | | |
| `./scripts/run-local.sh` | | |
| `./scripts/run-compose-dev.sh` (si testé) | | |
| `./scripts/run-compose-postgres.sh` (si testé) | | |

---

## Parcours testés

Cocher et noter OK / FAIL / PARTIEL :

| Parcours | Statut | Commentaire |
|----------|--------|-------------|
| Guest — bootstrap + listings publics | | |
| Buyer — login, matches, conversation | | |
| Seller — création bien, média, publication | | |
| Admin — users, orgs, events, health détaillé | | |
| Logout / session expirée | | |

---

## Bugs et anomalies

### Bug 1

| Champ | Valeur |
|-------|--------|
| Priorité | P0 / P1 / P2 |
| Titre | |
| Steps to reproduce | 1. … 2. … 3. … |
| Résultat attendu | |
| Résultat observé | |
| Logs / message d'erreur | |
| Endpoint ou écran | |

### Bug 2

_(dupliquer la section si nécessaire)_

---

## UX et documentation

| Question | Réponse |
|----------|---------|
| L'installation était-elle claire ? (1–5) | |
| Le guide [BETA_DISTRIBUTION_GUIDE.md](BETA_DISTRIBUTION_GUIDE.md) suffisant ? | |
| Points de friction | |
| Suggestions doc / UI | |

---

## Sécurité (si applicable)

| Observation | Détail |
|-------------|--------|
| Comportement inattendu auth/RBAC | |
| Exposition de données sensibles | |
| Autre | |

> Ne pas inclure de secrets réels ni de dumps de base de données.

---

## Synthèse

| Question | Réponse |
|----------|---------|
| Recommanderiez-vous cette Beta pour un pilote élargi ? | Oui / Non / Avec réserves |
| Bloquants identifiés | |
| Commentaire libre | |

---

*Merci pour votre participation au programme Beta LAWIM_V2.*
