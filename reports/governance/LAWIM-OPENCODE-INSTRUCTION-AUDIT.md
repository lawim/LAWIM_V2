# LAWIM V2 — OpenCode Instruction Audit

**Date :** 2026-07-20
**HEAD :** `31d4d6e4`
**Branche :** `governance/opencode-lawim-context-20260720`

## Périmètre

Tous les fichiers susceptibles de piloter les agents OpenCode, Cursor et les assistants IA sur LAWIM_V2.

## Fichiers audités

| Fichier | Type |
|---------|------|
| `.opencode/AGENTS.md` | Règles OpenCode projet |
| `governance/agent-boundaries.md` | Périmètres des rôles |
| `templates/agent-prompt-template.md` | Template de prompt agent |
| `.cursor/agents/prompt-generator.md` | Générateur de prompt |
| `.cursor/agents/*.md` (20 fichiers) | Rôles Cursor |
| `frontend/docs/AGENTS.md` | Agents runtime frontend |
| `frontend/docs/AGENT_EXECUTION.md` | Runtime exécution |
| `frontend/docs/AGENT_REGISTRY.md` | Registre d'agents |
| `docs/governance/` | Documents de gouvernance |
| `docs/runtime/` | Documents runtime |
| `docs/knowledge_execution/` | Documents exécution |
| `reports/program/` | Rapports programme |
| `reports/release/` | Rapports release |

## Contradictions détectées

### 1. Trois taxonomies d'agents incompatibles

| Source | # Agents | Modèle |
|--------|----------|--------|
| `governance/agent-boundaries.md` | 11 | DG-centré |
| `.cursor/agents/*.md` | 20 | DG-centré |
| `frontend/docs/AGENTS.md` | 11 | Brain-centré |

### 2. Mode autonome OpenCode vs gouvernance DG

`.opencode/AGENTS.md` : « Never ask for permission »
`governance/operating-model.md` : « Toute décision revient au Directeur Général »

### 3. Conflit Git

`.opencode/AGENTS.md` : « Commit when milestone complete »
`templates/agent-prompt-template.md` : « Ne lance jamais Git »

### 4. Référence manquante

`implementation/LAWIM_V2_IMPLEMENTATION_GOVERNANCE.md` référencé mais introuvable.

## Doublons

- « Aucun agent ne modifie la Constitution » dans 4 fichiers
- Mode autonome OpenCode dupliqué système ↔ projet
- Structure de rôle identique dans les 20 fichiers `.cursor/agents/`

## Informations obsolètes

- `agent-boundaries.md` liste 11 agents mais `.cursor/agents/` en a 20
- « Mission 2 decommissioning » dans `frontend/docs/AGENTS.md` (contexte historique)

## Secret potentiel

- `docs/knowledge_execution/KNOWLEDGE_EXECUTION_INVENTORY.md:289` : mot de passe « lawim2026 » en clair

## Recommandations

1. Créer `docs/ai-context/` comme source unique de vérité pour les agents
2. Distinguer agents de gouvernance, de développement et runtime
3. Remplacer le mode autonome par un mode gouverné avec références
4. Consolider les règles dupliquées
5. Supprimer ou marquer les références obsolètes
6. Vérifier le mot de passe en clair
