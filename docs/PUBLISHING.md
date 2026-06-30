# LAWIM_V2 — Stratégie de publication (sans publication réelle)

Ce document décrit comment publier une version distribuable **sans exécuter de publication** dans cette mission.

## Artefacts

| Artefact | Commande | Usage |
|----------|----------|-------|
| Wheel | `python -m build --wheel` | PyPI privé / artifact registry |
| sdist | `python -m build --sdist` | Archivage source |
| Image Docker | `docker build -t lawim_v2/app:VERSION .` | Déploiement conteneur |

Prérequis build : `pip install build`

## Métadonnées (`pyproject.toml`)

- **Nom PyPI :** `lawim-v2`
- **Version :** `0.1.0` (semver, synchronisée avec `lawim_v2.__version__`)
- **Entry point :** `lawim-v2` → `lawim_v2.__main__:main`
- **Extras :** `[postgresql]`, `[dev]`

## Validation locale avant publication

```bash
./scripts/validate-packaging.sh   # venv éphémère + pip install -e . + smoke
./scripts/validate-install.sh     # gate complète dépôt
python -m build                     # wheel + sdist (optionnel)
```

## Pipeline publication recommandé (PRODUCTIZATION-002+)

1. Tag git semver (`v0.1.0`)
2. CI : tests + validate-install + validate-packaging
3. Build wheel/sdist + image Docker
4. Push vers registry privé (PyPI interne, GHCR, etc.)
5. Release notes depuis `reports/program/`
6. **Ne pas** publier sur PyPI public sans revue gouvernance

## Installation tierce

```bash
pip install lawim-v2[postgresql]   # depuis registry
lawim-v2 --help
```

Ou depuis le dépôt :

```bash
pip install -e ".[postgresql]"
```

## Non objectifs de cette mission

- Pas de publication PyPI / Docker Hub
- Pas de signature de packages
- Pas de bump semver automatique
