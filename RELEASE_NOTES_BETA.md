# LAWIM_V2 — Release Notes Beta

## Beta Candidate — Juin 2026

### Highlights

- Parcours **Seller / Buyer / Admin / Guest** testés E2E et négativement
- UI statique renforcée : échappement HTML, loaders, aperçus média, erreurs `[code] message`
- Sécurité : health public minimal, détail admin authentifié, users/metrics protégés, redaction credentials
- Media : validation magic-bytes + cohérence MIME
- Auth : validation email/mot de passe à l'inscription
- Configuration : `AppConfig.validate()` renforcée (production seed interdit)
- **64 tests** + smoke runtime + manifest Prisma

### Breaking / API changes (Beta)

| Endpoint | Avant | Beta |
|----------|-------|------|
| `GET /api/health` | Verbose public | Minimal public ; audit/metrics si admin authentifié |
| `GET /api/metrics` | Public | Admin authentifié requis |
| `GET /api/users` | Public + hash exposés | Admin authentifié ; DTO public sans secrets |
| `GET /api/properties?include_deleted=true` | Public | Admin requis |
| Upload média | MIME déclaré seul | Magic-bytes obligatoires |

### Commandes

```bash
./scripts/run-local.sh
./scripts/run-tests.sh
./scripts/run-compose-dev.sh
./scripts/run-compose-postgres.sh   # PostgreSQL optionnel
```

### Comptes démo

Mot de passe : `lawim-demo` — `admin@lawim.local`, `agent@lawim.local`, `owner@lawim.local`

### Limites connues

- Médias `/media/*` servis sans auth (chemins UUID)
- Pas de rate limiting
- UI statique sans tests navigateur headless
- PostgreSQL live non exercé automatiquement en CI
