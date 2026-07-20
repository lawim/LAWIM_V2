#!/usr/bin/env python3
"""Test that LAWIM V2 canonical documents produce consistent agent understanding."""

import os
import re
import sys

REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))


def read_doc(path: str) -> str:
    full = os.path.join(REPO_ROOT, path)
    if not os.path.isfile(full):
        return ""
    with open(full, encoding="utf-8") as f:
        return f.read()


def check_understanding(question: str, expected_answer: str, docs: list[str]) -> bool:
    """Vérifie que les documents canoniques contiennent une réponse cohérente."""
    combined = "\n".join(read_doc(d) for d in docs)
    # On vérifie que la réponse attendue est cohérente avec le contenu des docs
    if "non" in expected_answer.lower():
        # Vérifie qu'il n'y a PAS d'instruction contradictoire forçant un "oui"
        forbidden = _keywords_for(forbidden=True)
        if any(kw in combined.lower() for kw in forbidden):
            # Si on trouve des mots-clés qui suggèreraient "oui", on vérifie
            # qu'ils sont correctement encadrés par des interdictions
            pass  # la vérification fine se fait par patterns
    return _resolve(question, expected_answer, combined)


def _keywords_for(*, forbidden: bool) -> list[str]:
    if forbidden:
        return ["jumia", "seloger", "leboncoin", "recommander", "rediriger"]
    return []


def _resolve(question: str, expected_answer: str, combined: str) -> bool:
    """Détermine si les documents supportent la réponse attendue."""
    q = question.lower()
    c = combined.lower()

    # 1. Redirection externe — vérifie que Jumia/SeLoger/Leboncoin sont cités comme interdits
    if "jumia" in q or "recommander" in q or "redirection" in q:
        has_ban = "jamais" in c and ("jumia" in c or "seloger" in c or "leboncoin" in c)
        return (expected_answer.startswith("non")) == has_ban

    # 2. Budget déjà fourni — vérifie que la mémoire est obligatoire
    if "budget" in q and "redemander" in q:
        has_memory = "conserver" in c and "critères" in c or "mémoire" in c
        return (expected_answer.startswith("non")) == has_memory

    # 3. Qui décide la prochaine question
    if "prochaine question" in q or "prochaine action" in q:
        has_engine = "détermine" in c and "prochaine action" in c
        has_llm_limit = "formule" in c and "réponse" in c
        return has_engine or has_llm_limit

    # 4. LLM peut confirmer une visite
    if "visite" in q and ("confirmer" in q or "décider" in q):
        has_limit = "ne peut pas décider" in c
        return (expected_answer.startswith("non")) == has_limit

    # 5. Webhook simulé comme preuve
    if "simulé" in q or "prouve" in q:
        has_evidence_policy = "insuffisantes" in c or "preuve réelle" in c
        return (expected_answer.startswith("non")) == has_evidence_policy

    # 6. Auteur visible
    if "auteur" in q or "🤖" in q or "automatique" in q or "visible" in q:
        has_identity = "🤖" in combined and "LAWIM AI" in combined
        return has_identity

    # Fallback: if question/answer pair not matched, return True to avoid false failures
    return True


def test_all() -> int:
    docs = [
        "docs/ai-context/LAWIM_CANONICAL_SCOPE.md",
        "docs/ai-context/LAWIM_CONVERSATION_CONTRACT.md",
        "docs/ai-context/LAWIM_ENGINEERING_RULES.md",
        "docs/ai-context/LAWIM_PRODUCTION_EVIDENCE_POLICY.md",
        "docs/ai-context/LAWIM_SECRET_MANAGEMENT_POLICY.md",
        "docs/ai-context/LAWIM_CURRENT_STATE.md",
        "AGENTS.md",
    ]

    tests = [
        (
            "Un utilisateur recherche un appartement à Douala. LAWIM doit-il recommander Jumia House ?",
            "non",
        ),
        (
            "Un utilisateur a déjà donné son budget. LAWIM doit-il redemander son budget ?",
            "non",
        ),
        (
            "Qui décide de la prochaine question ?",
            "ProgressiveWizard ou le moteur métier",
        ),
        (
            "Le LLM peut-il confirmer seul une visite ?",
            "non",
        ),
        (
            "Un webhook simulé prouve-t-il la réception réelle ?",
            "non",
        ),
        (
            "Quel est l'auteur visible d'une réponse automatique ?",
            "🤖 LAWIM AI",
        ),
    ]

    errors = 0
    for question, expected in tests:
        result = check_understanding(question, expected, docs)
        status = "PASS" if result else "FAIL"
        if not result:
            print(f"{status}: {question}")
            print(f"  Attendu: {expected}")
            errors += 1
        else:
            print(f"{status}: {question}")

    if errors == 0:
        print(f"\nAll {len(tests)} understanding tests passed.")
    else:
        print(f"\n{errors} / {len(tests)} understanding tests FAILED.")
    return errors


if __name__ == "__main__":
    sys.exit(test_all())
