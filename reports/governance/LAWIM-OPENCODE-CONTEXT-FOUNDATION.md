# LAWIM V2 — OpenCode Canonical Context Foundation

**Date :** 2026-07-20
**HEAD initial :** `31d4d6e4`
**Branche :** `governance/opencode-lawim-context-20260720`

## Fichiers existants audités

7 fichiers d'instructions agents analysés (`.opencode/AGENTS.md`, `governance/agent-boundaries.md`,
`templates/agent-prompt-template.md`, `.cursor/agents/prompt-generator.md`,
`frontend/docs/AGENTS.md`, `frontend/docs/AGENT_EXECUTION.md`, `frontend/docs/AGENT_REGISTRY.md`)
+ 20 fichiers `.cursor/agents/*.md`.

## Contradictions détectées

1. Trois taxonomies d'agents incompatibles (governance 11, Cursor 20, frontend 11)
2. Mode autonome OpenCode vs gouvernance DG-centrée
3. Conflit Git (OpenCode commit vs templates interdisant Git)
4. Référence manquante à `implementation/LAWIM_V2_IMPLEMENTATION_GOVERNANCE.md`

## Fichiers créés

| Fichier | Objet |
|---------|-------|
| `AGENTS.md` (racine) | 12 règles permanentes des agents |
| `docs/ai-context/LAWIM_CANONICAL_SCOPE.md` | Périmètre et identité LAWIM |
| `docs/ai-context/LAWIM_CONVERSATION_CONTRACT.md` | Architecture conversationnelle canonique |
| `docs/ai-context/LAWIM_ENGINEERING_RULES.md` | 15 règles techniques permanentes |
| `docs/ai-context/LAWIM_PRODUCTION_EVIDENCE_POLICY.md` | Niveaux de preuve et statuts |
| `docs/ai-context/LAWIM_SECRET_MANAGEMENT_POLICY.md` | Gestion des secrets |
| `docs/ai-context/LAWIM_CURRENT_STATE.md` | État actuel du projet |
| `opencode.json` | Configuration OpenCode |
| `.opencode/AGENTS.md` (mis à jour) | Référence la gouvernance projet |
| `reports/governance/LAWIM-OPENCODE-INSTRUCTION-AUDIT.md` | Audit des instructions |
| `reports/governance/LAWIM-OPENCODE-CONTEXT-FOUNDATION.md` | Présent rapport |
| `scripts/validation/validate_lawim_ai_context.py` | Validateur du contexte |
| `scripts/validation/test_lawim_agent_understanding.py` | Test de compréhension |

## Fichiers modifiés

- `.opencode/AGENTS.md` — réécrit pour référence à la gouvernance projet

## Validateur

`validate_lawim_ai_context.py` : ALL CHECKS PASSED
Vérifie : présence de tous les documents, règles anti-redirection, mémoire, preuve runtime,
séparation moteur/LLM, secrets, opencode.json valide.

## Test de compréhension

`test_lawim_agent_understanding.py` : All 6 understanding tests passed.
Questions testées : redirection externe, mémoire budget, décision prochaine question,
validation visite par LLM, preuve webhook, auteur visible.

## Limites

- Les documents `.cursor/agents/*.md` (20 fichiers) n'ont pas été modifiés — leur consolidation
  est une étape ultérieure distincte.
- Les règles de gouvernance DG-centrée et le mode autonome OpenCode restent en tension —
  le `.opencode/AGENTS.md` mis à jour clarifie que les documents projet priment.

## Prochaine étape recommandée

**ÉTAPE 2 — Reproduire la perte de contexte conversationnel,
créer les tests bloquants, puis reconnecter la mémoire et
ProgressiveWizard au runtime réel.**
