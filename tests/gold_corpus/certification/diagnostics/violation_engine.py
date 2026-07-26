"""Violation engine for LAWIM conversation certification.

For each violated assertion, produces:
  - assertion_id, category, turn_number
  - expected state, actual state
  - explanation of the failure
  - expected correction
  - confidence level
"""

from typing import Any, Dict, List, Optional, Tuple


VIOLATION_EXPLANATIONS = {
    "memory": {
        "MEM-0001": {
            "explanation": "Un element de memoire attendu n'a pas ete conserve entre les tours",
            "correction": "Verifier que ConversationStateService retient les slots entre chaque tour",
            "confidence": 0.9,
        },
        "MEM-0002": {
            "explanation": "La mise a jour de memoire n'est pas correcte",
            "correction": "Verifier que les nouvelles valeurs remplacent les anciennes dans le state",
            "confidence": 0.85,
        },
        "MEM-0003": {
            "explanation": "Le budget n'a pas ete correctement modifie ou extrait",
            "correction": "Verifier l'extraction du nombre dans le message utilisateur (gestion des espaces et formats)",
            "confidence": 0.9,
        },
        "MEM-0004": {
            "explanation": "La zone ou le quartier n'est pas conserve en memoire",
            "correction": "Verifier que le slot district est preserve dans QualificationService",
            "confidence": 0.85,
        },
        "MEM-0005": {
            "explanation": "Une date attendue n'est pas conservee entre les tours",
            "correction": "Verifier la retention des dates dans ConversationStateService",
            "confidence": 0.85,
        },
        "MEM-0006": {
            "explanation": "Un element de memoire aurait du expirer mais est toujours actif",
            "correction": "Verifier la politique d'expiration dans MemoryCompactionService",
            "confidence": 0.75,
        },
        "MEM-0007": {
            "explanation": "Une variable indesirable est retenue en memoire (memory leak)",
            "correction": "Verifier qu'aucun slot non defini dans le schema n'est conserve",
            "confidence": 0.7,
        },
    },
    "qualification": {
        "QLF-0001": {
            "explanation": "La qualification utilisateur n'est pas complete",
            "correction": "Verifier que tous les criteres obligatoires ont ete collectes par QualificationService",
            "confidence": 0.9,
        },
        "QLF-0002": {
            "explanation": "Les criteres ne sont pas collectes un par un",
            "correction": "Verifier que QualificationService pose une seule question par tour",
            "confidence": 0.85,
        },
        "QLF-0003": {
            "explanation": "L'utilisateur aurait du etre disqualifie mais ne l'a pas ete",
            "correction": "Verifier les regles de disqualification dans QualificationService",
            "confidence": 0.8,
        },
    },
    "business": {
        "BIZ-0001": {
            "explanation": "Aucun objet metier n'a ete cree alors qu'un objet etait attendu",
            "correction": "Verifier que l'action metier declenchee cree bien l'objet attendu",
            "confidence": 0.9,
        },
        "BIZ-0002": {
            "explanation": "L'action metier declenchee ne correspond pas a l'action attendue",
            "correction": "Verifier la logique de routage metier dans ConversationJourneyOrchestrator",
            "confidence": 0.85,
        },
        "BIZ-0003": {
            "explanation": "Un doublon d'objet metier a ete detecte",
            "correction": "Verifier l'idempotence de la creation d'objet metier",
            "confidence": 0.8,
        },
        "BIZ-0004": {
            "explanation": "Le handover humain n'est pas correctement declenche",
            "correction": "Verifier les conditions de handover dans ConversationJourneyOrchestrator",
            "confidence": 0.85,
        },
    },
    "intent": {
        "INT-0001": {
            "explanation": "L'intention detectee ne correspond pas a l'intention attendue",
            "correction": "Verifier le modele de detection d'intention dans ProgramFEngineAdapter",
            "confidence": 0.9,
        },
        "INT-0002": {
            "explanation": "Le changement d'intention n'est pas correct",
            "correction": "Verifier la logique de transition d'intention dans le moteur",
            "confidence": 0.8,
        },
    },
    "language": {
        "LANG-0001": {
            "explanation": "La langue de reponse ne correspond pas a la langue d'entree",
            "correction": "Verifier la politique de continuite linguistique dans LanguagePolicy",
            "confidence": 0.9,
        },
        "LANG-0002": {
            "explanation": "L'identite LAWIM AI est absente de la reponse",
            "correction": "Verifier que le prompt systeme et le rendu incluent l'identite LAWIM AI",
            "confidence": 0.95,
        },
        "LANG-0003": {
            "explanation": "Le footer IA est absent de la reponse",
            "correction": "Verifier l'ajout du footer par CommunicationService ou l'adaptateur canal",
            "confidence": 0.9,
        },
        "LANG-0004": {
            "explanation": "Une phrase interdite apparait dans la reponse",
            "correction": "Verifier le filtre de contenu dans ConversationResponseValidator",
            "confidence": 0.85,
        },
    },
    "questions": {
        "QST-0001": {
            "explanation": "Plus d'une question a ete posee dans un seul tour",
            "correction": "Verifier ResponsePlan.maximum_questions et le validateur ConversationResponseValidator",
            "confidence": 0.9,
        },
        "QST-0002": {
            "explanation": "La prochaine question posee n'est pas pertinente pour le contexte",
            "correction": "Verifier la generation de question dans ProgressiveWizard",
            "confidence": 0.75,
        },
        "QST-0003": {
            "explanation": "Une question interdite a ete posee",
            "correction": "Verifier la liste des questions interdites dans le validateur",
            "confidence": 0.85,
        },
    },
    "runtime": {
        "RUNTIME-0001": {
            "explanation": "Le moteur conversationnel utilise n'est pas celui attendu",
            "correction": "Verifier la configuration du ProviderOrchestrator et la selection du fournisseur",
            "confidence": 0.9,
        },
        "RUNTIME-0002": {
            "explanation": "Un fallback inattendu a ete declenche",
            "correction": "Verifier la chaine de fallback et les causes de declenchement",
            "confidence": 0.8,
        },
    },
    "channel": {
        "CHANNEL-0001": {
            "explanation": "Le comportement canal n'est pas conforme aux attentes",
            "correction": "Verifier l'adaptateur canal et le formatage de la reponse",
            "confidence": 0.85,
        },
    },
    "idempotence": {
        "IDEM-0001": {
            "explanation": "La meme entree ne produit pas le meme etat (effet de bord)",
            "correction": "Verifier l'idempotence du traitement conversationnel",
            "confidence": 0.7,
        },
        "IDEM-0002": {
            "explanation": "Une regression a ete detectee par rapport au comportement precedent",
            "correction": "Verifier que les modifications recentes n'ont pas altere le comportement",
            "confidence": 0.6,
        },
    },
    "state": {
        "STATE-0001": {
            "explanation": "La transition de phase n'est pas conforme au cycle de vie attendu",
            "correction": "Verifier la machine a etats dans ConversationJourneyOrchestrator",
            "confidence": 0.9,
        },
        "STATE-0002": {
            "explanation": "L'etat final de la conversation n'est pas celui attendu",
            "correction": "Verifier le deroulement complet de la conversation et la condition de terminaison",
            "confidence": 0.85,
        },
        "STATE-0003": {
            "explanation": "Les slots remplis ne correspondent pas aux valeurs attendues",
            "correction": "Verifier l'extraction et la validation des slots dans QualificationService",
            "confidence": 0.85,
        },
    },
}


def get_violation_detail(assertion_id: str, category: str) -> Dict[str, Any]:
    """Return the diagnostic detail for a given assertion."""
    cat_data = VIOLATION_EXPLANATIONS.get(category, {})
    detail = cat_data.get(assertion_id, {
        "explanation": f"Violation non documentee: {assertion_id}",
        "correction": "Consulter la documentation de l'assertion",
        "confidence": 0.5,
    })
    return detail


def analyze_violation(assertion_id: str, category: str,
                       expected: Any, actual: Any,
                       turn_number: Optional[int] = None) -> Dict[str, Any]:
    """Produce a full violation analysis."""
    detail = get_violation_detail(assertion_id, category)

    return {
        "assertion_id": assertion_id,
        "category": category,
        "turn_number": turn_number,
        "expected": expected,
        "actual": actual,
        "explanation": detail["explanation"],
        "expected_correction": detail["correction"],
        "confidence": detail["confidence"],
    }


def analyze_all_violations(assertion_results: Dict[str, Dict],
                            turn_results: Optional[Dict] = None) -> List[Dict]:
    """Analyze all violations from certification results."""
    violations = []

    for aid, result in assertion_results.items():
        if not result["pass"]:
            turn_number = None
            if turn_results:
                for tr in turn_results.get("results", []):
                    if aid in tr.get("assertions", {}):
                        turn_number = tr["turn_number"]
                        break
            violation = analyze_violation(
                aid,
                result.get("category", "unknown"),
                result.get("expected"),
                result.get("actual"),
                turn_number,
            )
            violations.append(violation)

    return violations
