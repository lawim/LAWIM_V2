from __future__ import annotations

from typing import Any

TEMPLATES: dict[str, Any] = {}


def _register(name: str) -> Any:
    def decorator(func: Any) -> Any:
        TEMPLATES[name] = func
        return func
    return decorator


@_register("greeting")
def greeting(**kwargs: Any) -> str:
    return "Bonjour ! Je suis LAWIM, votre assistant immobilier intelligent. Comment puis-je vous aider aujourd'hui ?"


@_register("greeting_returning")
def greeting_returning(**kwargs: Any) -> str:
    project_summary = kwargs.get("project_summary", "un projet")
    return (
        f"Bonjour ! Je vois que vous avez un projet en cours concernant "
        f"{project_summary}. Souhaitez-vous le poursuivre ?"
    )


@_register("ask_intent")
def ask_intent(**kwargs: Any) -> str:
    return "Souhaitez-vous acheter, louer, vendre, construire ou rechercher un professionnel ?"


@_register("ask_city")
def ask_city(**kwargs: Any) -> str:
    return "Dans quelle ville recherchez-vous ?"


@_register("ask_budget")
def ask_budget(**kwargs: Any) -> str:
    return "Quel est votre budget ?"


@_register("ask_property_type")
def ask_property_type(**kwargs: Any) -> str:
    return "Quel type de bien recherchez-vous ? (appartement, maison, villa, terrain, studio, ...)"


@_register("ask_bedrooms")
def ask_bedrooms(**kwargs: Any) -> str:
    return "Combien de chambres souhaitez-vous ?"


@_register("ask_transaction_type")
def ask_transaction_type(**kwargs: Any) -> str:
    return "Souhaitez-vous acheter ou louer ?"


@_register("ask_clarification_amount")
def ask_clarification_amount(**kwargs: Any) -> str:
    raw_value = kwargs.get("raw_value", "")
    option1 = kwargs.get("option1", "")
    option2 = kwargs.get("option2", "")
    return (
        f"J'ai noté {raw_value}. Pouvez-vous préciser s'il s'agit de "
        f"{option1} FCFA ou {option2} FCFA ?"
    )


@_register("clarify_selection")
def clarify_selection(**kwargs: Any) -> str:
    return "J'ai trouvé plusieurs options correspondantes. Pouvez-vous préciser votre choix ?"


@_register("project_list")
def project_list(**kwargs: Any) -> str:
    count = kwargs.get("count", 0)
    projects = kwargs.get("projects", "")
    return f"Vous avez {count} projet(s) actif(s) :\n{projects}\nLequel souhaitez-vous poursuivre ?"


@_register("no_project")
def no_project(**kwargs: Any) -> str:
    return "Je n'ai pas trouvé de projet en cours. Souhaitez-vous en créer un nouveau ?"


@_register("await_search")
def await_search(**kwargs: Any) -> str:
    return "Parfait ! Je lance la recherche dans les bases LAWIM."


@_register("zero_results")
def zero_results(**kwargs: Any) -> str:
    return "Je n'ai pas trouvé de résultat correspondant à vos critères. Voulez-vous élargir votre recherche ?"


@_register("results_available")
def results_available(**kwargs: Any) -> str:
    count = kwargs.get("count", 0)
    return f"J'ai trouvé {count} résultat(s) correspondant à votre recherche."


@_register("ask_consent")
def ask_consent(**kwargs: Any) -> str:
    partner_name = kwargs.get("partner_name", "le professionnel")
    data = kwargs.get("data", "vos informations")
    return (
        f"Pour vous mettre en relation avec {partner_name}, j'ai besoin de "
        f"votre consentement pour partager les informations suivantes : {data}. Acceptez-vous ?"
    )


@_register("consent_granted")
def consent_granted(**kwargs: Any) -> str:
    return "Merci ! Votre consentement a été enregistré. Je procède à la mise en relation."


@_register("consent_denied")
def consent_denied(**kwargs: Any) -> str:
    return (
        "Compris. Je ne partagerai aucune information. "
        "Souhaitez-vous modifier vos critères de recherche ?"
    )


@_register("relationship_created")
def relationship_created(**kwargs: Any) -> str:
    partner_name = kwargs.get("partner_name", "le professionnel")
    return (
        f"La mise en relation avec {partner_name} a été créée. "
        f"Vous pouvez désormais échanger directement via LAWIM."
    )


@_register("handover")
def handover(**kwargs: Any) -> str:
    return (
        "Je transfère votre demande à un conseiller LAWIM. "
        "Un membre de notre équipe vous contactera prochainement."
    )


@_register("loop_handover")
def loop_handover(**kwargs: Any) -> str:
    return (
        "Je rencontre des difficultés à comprendre votre demande. "
        "Je vais vous transférer à un conseiller LAWIM qui pourra mieux vous aider."
    )


@_register("error")
def error(**kwargs: Any) -> str:
    return "Désolé, une erreur technique est survenue. Je vous transfère à un conseiller LAWIM."


@_register("ai_unavailable")
def ai_unavailable(**kwargs: Any) -> str:
    return "Le service d'assistance n'est pas disponible pour le moment. Je continue avec les options standard."


@_register("clarification_repeat")
def clarification_repeat(**kwargs: Any) -> str:
    return "Pourriez-vous reformuler votre réponse ?"


@_register("clarification_options")
def clarification_options(**kwargs: Any) -> str:
    options = kwargs.get("options", "")
    return f"Voici quelques options :\n{options}\nMerci de choisir l'une d'elles."


def get_template(name: str, **kwargs: Any) -> str | None:
    func = TEMPLATES.get(name)
    if func is None:
        return None
    return func(**kwargs)


def has_template(name: str) -> bool:
    return name in TEMPLATES
