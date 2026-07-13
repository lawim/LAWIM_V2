from __future__ import annotations

from typing import Any


def intent_dto(analysis: dict[str, Any]) -> dict[str, Any]:
    return {
        "primary_intent": analysis.get("primary_intent"),
        "primary_score": analysis.get("primary_score"),
        "is_multi_intent": analysis.get("is_multi_intent", False),
        "intents": [
            {
                "intent": i.get("intent"),
                "score": i.get("score"),
                "confidence": i.get("confidence"),
            }
            for i in analysis.get("intents", [])
        ],
        "entities": {
            "cities": analysis.get("entities", {}).get("cities", []),
            "budgets": analysis.get("entities", {}).get("budgets", []),
            "property_types": analysis.get("entities", {}).get("property_types", []),
            "surfaces_m2": analysis.get("entities", {}).get("surfaces_m2", []),
            "bedrooms": analysis.get("entities", {}).get("bedrooms", []),
            "timelines": analysis.get("entities", {}).get("timelines", []),
            "timeline": analysis.get("entities", {}).get("timeline"),
            "urgency": analysis.get("entities", {}).get("urgency"),
            "project_type": analysis.get("entities", {}).get("project_type"),
            "project_types": analysis.get("entities", {}).get("project_types", []),
            "land_status": analysis.get("entities", {}).get("land_status"),
            "lang": analysis.get("entities", {}).get("lang"),
            "confirmation": analysis.get("entities", {}).get("confirmation"),
        },
        "language": analysis.get("language"),
        "is_confirmation": analysis.get("is_confirmation"),
        "is_rejection": analysis.get("is_rejection"),
    }


def progression_dto(progression: dict[str, Any]) -> dict[str, Any]:
    return {
        "intent": progression.get("intent"),
        "progress_pct": progression.get("progress_pct", 0),
        "total_steps": progression.get("total_steps", 0),
        "required_fields": progression.get("required_fields", []),
        "optional_fields": progression.get("optional_fields", []),
        "known_required_fields": progression.get("known_required_fields", []),
        "known_optional_fields": progression.get("known_optional_fields", []),
        "known_fields": progression.get("known_fields", []),
        "known_labels": progression.get("known_labels", []),
        "missing_fields": progression.get("missing_fields", []),
        "missing_required_fields": progression.get("missing_required_fields", []),
        "missing_optional_fields": progression.get("missing_optional_fields", []),
        "next_question": progression.get("next_question"),
        "next_key": progression.get("next_key"),
        "complete": progression.get("complete", False),
        "minimum_search_ready": progression.get("minimum_search_ready", False),
        "search_ready": progression.get("search_ready", False),
        "commercial_maturity": progression.get("commercial_maturity"),
        "qualification_score": progression.get("qualification_score"),
        "required_completion_pct": progression.get("required_completion_pct"),
        "optional_completion_pct": progression.get("optional_completion_pct"),
        "next_action": progression.get("next_action"),
        "responsible_actor": progression.get("responsible_actor"),
        "transaction_stage": progression.get("transaction_stage"),
        "next_actions": progression.get("next_actions", []),
    }


def suggestion_dto(suggestion: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": suggestion.get("type") or suggestion.get("suggestion_type"),
        "content": suggestion.get("content"),
        "action": suggestion.get("action") or suggestion.get("target_action"),
        "partner": suggestion.get("partner") or suggestion.get("target_partner"),
        "priority": suggestion.get("priority", "medium"),
        "priority_order": suggestion.get("priority_order", 0),
        "status": suggestion.get("status"),
    }


def resumption_dto(resumption: dict[str, Any]) -> dict[str, Any]:
    return {
        "has_history": resumption.get("has_history", False),
        "short_summary": resumption.get("short_summary"),
        "summary": resumption.get("summary"),
        "objective": resumption.get("objective"),
        "city": resumption.get("city"),
        "confirmed_count": resumption.get("confirmed_count", 0),
        "pending_count": resumption.get("pending_count", 0),
        "last_action": resumption.get("last_action"),
        "next_step": resumption.get("next_step"),
        "next_question": resumption.get("next_question"),
        "language": resumption.get("language", "fr"),
    }
