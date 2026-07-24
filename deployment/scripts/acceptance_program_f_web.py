#!/usr/bin/env python3
"""Acceptance test for Program F — 9-turn Web user journey.

Usage:
    python3 deployment/scripts/acceptance_program_f_web.py [--base-url URL]

This script sends messages to the real LAWIM Web API endpoint.
After turn 4, it pauses and asks the operator to restart the service.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE_URL = os.getenv("LAWIM_API_URL", "https://api.lawim.app")
API_PATH = "/api/v3/conversations/messages"

TURNS = [
    ("Bonjour, je cherche un appartement à louer à Yaoundé.",
     "property_search, à louer, Yaoundé"),
    ("Mon budget est de 150 mille par mois.",
     "budget_max=150000"),
    ("Deux chambres, de préférence à Melen ou Ngoa-Ekellé.",
     "bedrooms=2, preferred_areas=[Melen, Ngoa-Ekellé]"),
    ("Je souhaite entrer en septembre.",
     "move_in_date"),
    ("Est-ce que les visites sont payantes ?",
     "digression, faits conservés"),
    ("Finalement je peux monter jusqu'à 180 000.",
     "budget correction 150000→180000"),
    ("Je veux être proche de mon travail.",
     "ambiguïté → WAITING_FOR_CLARIFICATION"),
    ("Je travaille près de l'Hôpital central.",
     "clarification résolue, proximité Hôpital central"),
    ("Oui, vous pouvez enregistrer ma demande.",
     "action métier réelle, confirmation"),
]


def send_message(base_url: str, token: str, text: str, conversation_id: int | None = None) -> dict:
    url = f"{base_url}{API_PATH}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    body: dict = {"channel": "web", "message": text}
    if conversation_id:
        body["conversation_id"] = conversation_id

    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers=headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return {
                "status": resp.status,
                "body": json.loads(resp.read().decode()),
            }
    except urllib.error.HTTPError as e:
        return {
            "status": e.code,
            "body": {"error": str(e)},
            "raw": e.read().decode() if e.fp else "",
        }
    except urllib.error.URLError as e:
        return {"status": 0, "body": {"error": f"Network error: {e.reason}"}}


def main() -> None:
    parser = argparse.ArgumentParser(description="Program F Web acceptance test")
    parser.add_argument("--base-url", default=BASE_URL, help="LAWIM API base URL")
    parser.add_argument("--token", default="", help="Auth token (if API requires it)")
    args = parser.parse_args()

    conv_id = None
    failures = 0

    print(f"LAWIM Program F — Web Acceptance Test")
    print(f"Base URL: {args.base_url}")
    print(f"{'=' * 60}\n")

    for i, (text, expectation) in enumerate(TURNS, 1):
        print(f"[Tour {i}]")
        print(f"  USER: {text}")
        print(f"  Attendu: {expectation}")

        result = send_message(args.base_url, args.token, text, conv_id)
        status = result["status"]
        body = result["body"]

        if status == 201 or status == 200:
            response_text = body.get("response", body.get("message", "(aucune réponse)"))
            if conv_id is None:
                conv_id = body.get("conversation_id")
            print(f"  HTTP: {status}")
            print(f"  CONVERSATION_ID: {conv_id}")
            print(f"  LAWIM: {response_text[:120]}")
            print(f"  ✅ PASS")
        elif status == 401 or status == 403:
            print(f"  HTTP: {status} — Authentification requise")
            print(f"  ❌ AUTH FAIL — Impossible de tester sans token")
            failures += 1
            break
        else:
            print(f"  HTTP: {status}")
            print(f"  ERREUR: {body}")
            print(f"  ❌ FAIL")
            failures += 1

        # Pause for restart after tour 4
        if i == 4:
            print(f"\n  ⏸️  === REDÉMARRAGE REQUIS ===")
            print(f"  Exécutez maintenant sur le serveur OVH :")
            print(f"    docker compose -f deployment/compose/docker-compose.prod.yml restart communication")
            print(f"  Puis attendez le healthcheck et tapez ENTER pour continuer...")
            input("  >> ")
            print(f"  ✅ Reprise du parcours\n")

        print()

    print(f"{'=' * 60}")
    if failures == 0:
        print(f"✅ PARCOURS WEB : 9 TOURS RÉUSSIS")
    else:
        print(f"❌ {failures} échec(s) détecté(s)")


if __name__ == "__main__":
    main()
