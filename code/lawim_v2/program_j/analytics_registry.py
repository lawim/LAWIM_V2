from __future__ import annotations

from typing import Any

from .analytics_models import (
    AggregationType,
    MetricDefinition,
    MetricDomain,
    MetricStatus,
)

_METRICS: list[MetricDefinition] = [
    MetricDefinition("CAMPAIGNS_TOTAL", "Total campagnes", "Nombre total de campagnes",
                      MetricDomain.CAMPAIGN, "campagnes", AggregationType.COUNT,
                      "COUNT(external_campaigns)", "1.0"),
    MetricDefinition("PUBLICATIONS_TOTAL", "Total publications", "Nombre total de publications",
                      MetricDomain.PUBLICATION, "publications", AggregationType.COUNT,
                      "COUNT(external_publications)", "1.0"),
    MetricDefinition("CLICKS_TOTAL", "Clics totaux", "Nombre total de clics",
                      MetricDomain.CHANNEL, "clics", AggregationType.COUNT,
                      "COUNT(redirect_logs WHERE NOT is_bot)", "1.0"),
    MetricDefinition("CLICKS_UNIQUE", "Clics uniques", "Clics depuis des sessions distinctes",
                      MetricDomain.CHANNEL, "clics", AggregationType.DISTINCT_COUNT,
                      "DISTINCT_COUNT(redirect_logs.session_id WHERE NOT is_bot)", "1.0"),
    MetricDefinition("REDIRECTS_TOTAL", "Redirections totales", "Nombre total de redirections",
                      MetricDomain.CHANNEL, "redirections", AggregationType.COUNT,
                      "COUNT(redirect_logs)", "1.0"),
    MetricDefinition("BOT_EVENTS_TOTAL", "Événements bots", "Événements détectés comme bots",
                      MetricDomain.CHANNEL, "événements", AggregationType.COUNT,
                      "COUNT(redirect_logs WHERE is_bot)", "1.0"),
    MetricDefinition("CONVERSATIONS_STARTED", "Conversations démarrées",
                      "Nombre de conversations créées", MetricDomain.CONVERSATION,
                      "conversations", AggregationType.COUNT,
                      "COUNT(conversations)", "1.0"),
    MetricDefinition("LEADS_CREATED", "Leads créés", "Nombre de leads générés",
                      MetricDomain.CONVERSION, "leads", AggregationType.COUNT,
                      "COUNT(leads)", "1.0"),
    MetricDefinition("QUALIFICATIONS_STARTED", "Qualifications démarrées",
                      "Sessions de qualification commencées", MetricDomain.QUALIFICATION,
                      "qualifications", AggregationType.COUNT,
                      "COUNT(qualification_sessions)", "1.0"),
    MetricDefinition("QUALIFICATIONS_COMPLETED", "Qualifications terminées",
                      "Sessions de qualification terminées", MetricDomain.QUALIFICATION,
                      "qualifications", AggregationType.COUNT,
                      "COUNT(qualification_sessions WHERE completed)", "1.0"),
    MetricDefinition("MATCHINGS_CREATED", "Matchings créés", "Matchings générés",
                      MetricDomain.MATCHING, "matchings", AggregationType.COUNT,
                      "COUNT(matchings)", "1.0"),
    MetricDefinition("VISITS_REQUESTED", "Visites demandées", "Demandes de visite",
                      MetricDomain.VISIT, "visites", AggregationType.COUNT,
                      "COUNT(visit_requests)", "1.0"),
    MetricDefinition("VISITS_COMPLETED", "Visites réalisées", "Visites effectuées",
                      MetricDomain.VISIT, "visites", AggregationType.COUNT,
                      "COUNT(visit_requests WHERE completed)", "1.0"),
    MetricDefinition("TRANSACTIONS_STARTED", "Transactions démarrées",
                      "Transactions initiées", MetricDomain.TRANSACTION,
                      "transactions", AggregationType.COUNT, "COUNT(transactions)", "1.0"),
    MetricDefinition("TRANSACTIONS_COMPLETED", "Transactions terminées",
                      "Transactions finalisées", MetricDomain.TRANSACTION,
                      "transactions", AggregationType.COUNT,
                      "COUNT(transactions WHERE completed)", "1.0"),
    MetricDefinition("PAYMENTS_INITIATED", "Paiements initiés",
                      "Paiements commencés", MetricDomain.PAYMENT,
                      "paiements", AggregationType.COUNT, "COUNT(payments)", "1.0"),
    MetricDefinition("PAYMENTS_CONFIRMED", "Paiements confirmés",
                      "Paiements réussis", MetricDomain.PAYMENT,
                      "paiements", AggregationType.COUNT,
                      "COUNT(payments WHERE confirmed)", "1.0"),
    MetricDefinition("CONVERSIONS_TOTAL", "Conversions totales",
                      "Nombre total de conversions", MetricDomain.CONVERSION,
                      "conversions", AggregationType.COUNT, "COUNT(conversion_events)", "1.0"),
    MetricDefinition("CONVERSION_RATE", "Taux de conversion",
                      "Proportion de leads convertis", MetricDomain.CONVERSION,
                      "%", AggregationType.RATE,
                      "CONVERSIONS_TOTAL / LEADS_CREATED * 100", "1.0",
                      dimensions=("channel", "campaign", "publication")),
    MetricDefinition("REVENUE_TOTAL", "Revenu total",
                      "Somme des valeurs monétaires converties", MetricDomain.PAYMENT,
                      "FCFA", AggregationType.SUM, "SUM(conversion_events.monetary_value)", "1.0"),
    MetricDefinition("AVERAGE_RESPONSE_TIME", "Temps de réponse moyen",
                      "Délai moyen de première réponse", MetricDomain.CONVERSATION,
                      "minutes", AggregationType.AVG,
                      "AVG(message.sent_at - message.received_at)", "1.0"),
    MetricDefinition("AVERAGE_CONVERSION_TIME", "Délai moyen de conversion",
                      "Temps entre premier contact et conversion", MetricDomain.CONVERSION,
                      "jours", AggregationType.AVG,
                      "AVG(conversion.occurred_at - first_touchpoint.occurred_at)", "1.0"),
    MetricDefinition("HUMAN_HANDOVER_RATE", "Taux de handover humain",
                      "Proportion de conversations passées à un humain",
                      MetricDomain.CONVERSATION, "%", AggregationType.RATE,
                      "HANDOVER_COUNT / CONVERSATIONS_STARTED * 100", "1.0"),
    MetricDefinition("DUPLICATE_RATE", "Taux de doublons",
                      "Proportion d'événements en doublon", MetricDomain.GENERAL,
                      "%", AggregationType.RATE,
                      "DUPLICATE_COUNT / TOTAL_EVENTS * 100", "1.0"),
    MetricDefinition("ATTRIBUTION_COVERAGE_RATE", "Taux de couverture d'attribution",
                      "Proportion de conversions avec attribution", MetricDomain.CONVERSION,
                      "%", AggregationType.RATE,
                      "CONVERSIONS_WITH_ATTRIBUTION / CONVERSIONS_TOTAL * 100", "1.0"),
]

_BY_CODE: dict[str, MetricDefinition] = {m.metric_code: m for m in _METRICS}


def get_metric(code: str) -> MetricDefinition | None:
    return _BY_CODE.get(code)


def list_metrics() -> list[MetricDefinition]:
    return list(_METRICS)


def metric_codes() -> list[str]:
    return [m.metric_code for m in _METRICS]


def metric_count() -> int:
    return len(_METRICS)


def to_dict_list() -> list[dict[str, Any]]:
    return [m.to_dict() for m in _METRICS]
