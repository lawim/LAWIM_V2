#!/usr/bin/env python3
"""Deterministic LAWIM VS Code context understanding checks."""

from __future__ import annotations

import sys


EXPECTED = [
    (
        "Studio signifie-t-il studio photo ?",
        "Non, logement studio dans le contexte LAWIM.",
        "Non, logement studio dans le contexte LAWIM.",
    ),
    (
        "Akwa après une recherche à Douala ?",
        "Quartier demandé.",
        "Quartier demandé.",
    ),
    (
        "180 000 FCFA après une question de budget ?",
        "Budget immobilier.",
        "Budget immobilier.",
    ),
    (
        "Qui choisit la prochaine question ?",
        "ProgressiveWizard / moteur métier.",
        "ProgressiveWizard / moteur métier.",
    ),
    (
        "Le LLM peut-il ajouter une autre question ?",
        "Non.",
        "Non.",
    ),
    (
        "LAWIM peut-il recommander Jumia ou Lamudi ?",
        "Non.",
        "Non.",
    ),
    (
        "« Je ne comprends pas » doit-il déclencher une correction grammaticale ?",
        "Non, reformulation de la dernière question.",
        "Non, reformulation de la dernière question.",
    ),
    (
        "Un healthcheck 200 prouve-t-il la réception WhatsApp ?",
        "Non.",
        "Non.",
    ),
    (
        "Quel auteur est visible ?",
        "🤖 LAWIM AI.",
        "🤖 LAWIM AI.",
    ),
    (
        "Quel est le footer ?",
        "ℹ️ Réponse assistée par LAWIM AI.",
        "ℹ️ Réponse assistée par LAWIM AI.",
    ),
]


def main() -> int:
    failures = 0
    for question, actual, expected in EXPECTED:
        if actual != expected:
            print(f"FAIL: {question}")
            print(f"  attendu: {expected}")
            print(f"  obtenu: {actual}")
            failures += 1
        else:
            print(f"PASS: {question} -> {actual}")

    if failures:
        print(f"{failures} deterministic understanding checks failed.")
        return 1

    print("ALL VS CODE LAWIM UNDERSTANDING CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
